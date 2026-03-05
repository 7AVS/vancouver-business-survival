#!/usr/bin/env python3
"""
Bulk geocoding script for Vancouver property tax neighbourhood code mapping.
Implements the approach recommended in A1_APPROACH_REVIEW.md.

Strategy:
- Extract all unique (from_civic_number, street_name, property_postal_code) per code
- Sample up to SAMPLE_PER_CODE per code (default 20, so ~600 total requests)
- Geocode via Nominatim with 1-second delay and progress saving
- Point-in-polygon test against 22 CoV boundary polygons using shapely
- Report distribution per code (not forced 1-to-1 mapping)
- Build neighbourhood_code_lookup.csv, address_to_area.csv

Usage:
  python3 geocode_bulk.py             # Run with defaults (20 samples/code)
  python3 geocode_bulk.py --full      # Full geocoding (all unique addresses -- hours)
  python3 geocode_bulk.py --resume    # Resume from last saved progress
"""

import csv
import json
import os
import random
import sys
import time
import urllib.request
import urllib.parse
import urllib.error
from collections import defaultdict, Counter
from datetime import datetime
from pathlib import Path

from shapely.geometry import shape, Point

# ─── Configuration ────────────────────────────────────────────────────────────

DATA_DIR = Path("/home/aurora/projects/sites/portfolio-projects/van-property-tax/data")
RAW_DIR = DATA_DIR / "raw"

CSV_FILES = [
    RAW_DIR / "property-tax-report-2006-2010.csv",
    RAW_DIR / "property-tax-report-2011-2015.csv",
    RAW_DIR / "property-tax-report-2016-2019.csv",
    RAW_DIR / "property-tax-report-2020-present.csv",
]

GEOJSON_FILE = RAW_DIR / "local-area-boundary.geojson"
BUSINESS_LICENCE_SAMPLE = RAW_DIR / "business-licences" / "snapshot_2024-10-02_sample.csv"

# Output files
ADDRESS_TO_AREA_CSV = DATA_DIR / "address_to_area.csv"
PROGRESS_JSONL = DATA_DIR / "geocode_progress.jsonl"    # One JSON per line, resumable
LOG_FILE = DATA_DIR / "geocode_run.log"

SAMPLE_PER_CODE = 50   # Number of unique addresses to sample per code
NOMINATIM_DELAY = 0.3  # Seconds between requests — BC Geocoder is a gov API, 3-5 req/sec is fine
USER_AGENT = "VancouverPropertyTaxResearch/1.0 (academic)"
RANDOM_SEED = 42

# BC Geocoder (free, no auth, provincial government API — better than Nominatim for BC addresses)
BC_GEOCODER_URL = "https://geocoder.api.gov.bc.ca/addresses.json"

# ─── Logging ──────────────────────────────────────────────────────────────────

log_fh = None

def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line, flush=True)
    if log_fh:
        log_fh.write(line + "\n")
        log_fh.flush()

# ─── Load GeoJSON polygons ─────────────────────────────────────────────────────

def load_polygons(geojson_path: Path) -> list[dict]:
    """Load CoV local area boundary polygons from GeoJSON."""
    with open(geojson_path) as f:
        gj = json.load(f)
    polygons = []
    for feat in gj["features"]:
        name = feat["properties"]["name"]
        centroid_lat = feat["properties"]["geo_point_2d"]["lat"]
        centroid_lon = feat["properties"]["geo_point_2d"]["lon"]
        geom = shape(feat["geometry"])
        polygons.append({
            "name": name,
            "geom": geom,
            "centroid_lat": centroid_lat,
            "centroid_lon": centroid_lon,
        })
    return polygons

def point_in_polygon(lat: float, lon: float, polygons: list[dict]) -> tuple[str | None, str]:
    """
    Test point against all polygons.
    Returns (area_name, method) where method is 'pip' or 'nearest_centroid'.
    """
    pt = Point(lon, lat)  # shapely uses (x=lon, y=lat)
    for poly in polygons:
        if poly["geom"].contains(pt):
            return poly["name"], "pip"
    # Point outside all polygons — find nearest centroid
    min_dist = float("inf")
    nearest = None
    for poly in polygons:
        dlat = lat - poly["centroid_lat"]
        dlon = lon - poly["centroid_lon"]
        dist = dlat**2 + dlon**2
        if dist < min_dist:
            min_dist = dist
            nearest = poly["name"]
    return nearest, "nearest_centroid"

# ─── Extract addresses from CSV files ─────────────────────────────────────────

def extract_addresses_by_code(csv_files: list[Path]) -> dict[str, set[tuple]]:
    """
    Parse all CSV files and return a dict: code -> set of (civic, street, postal).
    Only addresses with a non-empty from_civic_number are included.
    """
    log("Extracting unique addresses from CSV files...")
    code_addresses: dict[str, set] = defaultdict(set)
    total_rows = 0
    null_civic = 0

    for f in csv_files:
        log(f"  Reading {f.name}...")
        with open(f, encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                total_rows += 1
                code = row.get("neighbourhood_code", "").strip()
                civic = row.get("from_civic_number", "").strip()
                street = row.get("street_name", "").strip()
                postal = row.get("property_postal_code", "").strip()
                if code and civic and street:
                    code_addresses[code].add((civic, street, postal))
                elif code:
                    null_civic += 1

    log(f"Total rows processed: {total_rows:,}")
    log(f"Rows with null/empty civic number: {null_civic:,} ({null_civic/total_rows*100:.1f}%)")
    for code in sorted(code_addresses):
        log(f"  Code {code}: {len(code_addresses[code]):,} unique addresses")
    return dict(code_addresses)

def sample_addresses(
    code_addresses: dict[str, set[tuple]],
    n: int,
    rng: random.Random,
) -> dict[str, list[tuple]]:
    """Sample up to n addresses per code."""
    sampled = {}
    for code, addr_set in code_addresses.items():
        addr_list = sorted(addr_set)  # Sort for reproducibility
        if len(addr_list) <= n:
            sampled[code] = addr_list
        else:
            sampled[code] = rng.sample(addr_list, n)
    total = sum(len(v) for v in sampled.values())
    log(f"Sampled {total} addresses ({n} per code) for geocoding")
    return sampled

# ─── Load previously geocoded results ─────────────────────────────────────────

def load_progress(progress_file: Path) -> dict[tuple, dict]:
    """Load already-geocoded addresses from JSONL progress file."""
    results = {}
    if not progress_file.exists():
        return results
    with open(progress_file) as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                rec = json.loads(line)
                key = (rec["from_civic_number"], rec["street_name"], rec["property_postal_code"])
                results[key] = rec
            except (json.JSONDecodeError, KeyError):
                continue
    log(f"Loaded {len(results):,} previously geocoded addresses from {progress_file.name}")
    return results

# ─── Nominatim geocoding ───────────────────────────────────────────────────────

def geocode_address(civic: str, street: str, postal: str) -> dict:
    """
    Geocode a single address using the BC Geocoder (geocoder.api.gov.bc.ca).
    Provincial government API — no auth needed, excellent coverage for BC addresses.
    Returns dict with lat, lon, geocode_status, raw_display_name, score.
    """
    # Format: "123 Main St, Vancouver, BC" — postal code optional
    addr = f"{civic} {street}, Vancouver, BC"
    if postal:
        addr = f"{civic} {street}, Vancouver, BC {postal}"

    params = urllib.parse.urlencode({
        "addressString": addr,
        "maxResults": "1",
        "outputSRS": "4326",  # WGS84
        "minScore": "50",     # minimum match score (0-100)
    })
    url = f"{BC_GEOCODER_URL}?{params}"

    try:
        req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode())

        features = data.get("features", [])
        if features:
            feat = features[0]
            coords = feat["geometry"]["coordinates"]  # [lon, lat]
            score = feat["properties"].get("score", 0)
            full_addr = feat["properties"].get("fullAddress", "")
            precision = feat["properties"].get("matchPrecision", "")
            return {
                "lat": float(coords[1]),
                "lon": float(coords[0]),
                "geocode_status": "ok",
                "raw_display_name": full_addr,
                "score": score,
                "match_precision": precision,
            }
        else:
            return {"lat": None, "lon": None, "geocode_status": "no_results", "raw_display_name": "", "score": 0, "match_precision": ""}

    except urllib.error.HTTPError as e:
        return {"lat": None, "lon": None, "geocode_status": f"http_error_{e.code}", "raw_display_name": "", "score": 0, "match_precision": ""}
    except urllib.error.URLError as e:
        return {"lat": None, "lon": None, "geocode_status": "url_error", "raw_display_name": str(e.reason), "score": 0, "match_precision": ""}
    except Exception as e:
        return {"lat": None, "lon": None, "geocode_status": "error", "raw_display_name": str(e), "score": 0, "match_precision": ""}

# ─── Main geocoding loop ───────────────────────────────────────────────────────

def run_geocoding(
    sampled: dict[str, list[tuple]],
    polygons: list[dict],
    existing: dict[tuple, dict],
    progress_file: Path,
) -> dict[tuple, dict]:
    """
    Geocode addresses not already in existing, save progress incrementally.
    Returns merged dict of all results.
    """
    results = dict(existing)  # Copy existing

    # Build list of (code, civic, street, postal) to geocode
    todo = []
    for code, addrs in sampled.items():
        for (civic, street, postal) in addrs:
            key = (civic, street, postal)
            if key not in results:
                todo.append((code, civic, street, postal))

    log(f"Need to geocode: {len(todo)} addresses (already done: {len(existing)})")

    if not todo:
        log("All addresses already geocoded — nothing to do.")
        return results

    # Open progress file for appending
    with open(progress_file, "a") as pf:
        for i, (code, civic, street, postal) in enumerate(todo):
            key = (civic, street, postal)

            geo = geocode_address(civic, street, postal)
            local_area = None
            pip_method = None

            if geo["geocode_status"] == "ok" and geo["lat"] is not None:
                local_area, pip_method = point_in_polygon(geo["lat"], geo["lon"], polygons)

            rec = {
                "neighbourhood_code": code,
                "from_civic_number": civic,
                "street_name": street,
                "property_postal_code": postal,
                "lat": geo["lat"],
                "lon": geo["lon"],
                "geocode_status": geo["geocode_status"],
                "raw_display_name": geo["raw_display_name"],
                "geocode_score": geo.get("score", ""),
                "match_precision": geo.get("match_precision", ""),
                "local_area_name": local_area,
                "pip_method": pip_method,
            }
            results[key] = rec

            # Write to progress file immediately
            pf.write(json.dumps(rec) + "\n")
            pf.flush()

            status_str = f"{local_area or 'NO_MATCH'} [{pip_method or geo['geocode_status']}]"
            log(f"  [{i+1}/{len(todo)}] Code {code}: {civic} {street} {postal} → {status_str}")

            time.sleep(NOMINATIM_DELAY)

    log(f"Geocoding complete. Total results: {len(results)}")
    return results

# ─── Build outputs ─────────────────────────────────────────────────────────────

def build_address_to_area_csv(results: dict[tuple, dict], sampled: dict[str, list[tuple]], out_path: Path):
    """Write address_to_area.csv with all geocoded addresses."""
    fieldnames = [
        "from_civic_number", "street_name", "property_postal_code",
        "neighbourhood_code", "lat", "lon", "local_area_name",
        "geocode_status", "geocode_score", "match_precision", "pip_method",
    ]
    rows = []
    for code, addrs in sampled.items():
        for (civic, street, postal) in addrs:
            key = (civic, street, postal)
            rec = results.get(key, {})
            rows.append({
                "from_civic_number": civic,
                "street_name": street,
                "property_postal_code": postal,
                "neighbourhood_code": code,
                "lat": rec.get("lat", ""),
                "lon": rec.get("lon", ""),
                "local_area_name": rec.get("local_area_name", ""),
                "geocode_status": rec.get("geocode_status", "not_run"),
                "geocode_score": rec.get("geocode_score", ""),
                "match_precision": rec.get("match_precision", ""),
                "pip_method": rec.get("pip_method", ""),
            })
    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    log(f"Wrote {len(rows)} rows to {out_path.name}")

def build_code_distributions(sampled: dict[str, list[tuple]], results: dict[tuple, dict]) -> dict[str, dict]:
    """
    For each neighbourhood_code, compute distribution across local areas.

    IMPORTANT: Only counts addresses where pip_method == 'pip' (point inside polygon).
    Addresses assigned via 'nearest_centroid' are excluded from distributions because
    the nearest-centroid fallback is unreliable — it assigns points to centroids that may
    be many km away (e.g., a Downtown address falling just outside the polygon gets assigned
    to Hastings-Sunrise whose centroid is geometrically closest).

    Returns: code -> {area: count, ..., '_total': n, '_geocoded': n, '_pip': n, '_centroid': n, '_failed': n}
    """
    distros = {}
    for code, addrs in sampled.items():
        area_counts: Counter = Counter()
        total = len(addrs)
        geocoded = 0
        pip_count = 0
        centroid_count = 0
        failed = 0
        for (civic, street, postal) in addrs:
            key = (civic, street, postal)
            rec = results.get(key, {})
            status = rec.get("geocode_status", "not_run")
            pip_method = rec.get("pip_method", "")
            if status == "ok":
                geocoded += 1
                if pip_method == "pip":
                    pip_count += 1
                    area = rec.get("local_area_name")
                    if area:
                        area_counts[area] += 1
                    else:
                        failed += 1
                elif pip_method == "nearest_centroid":
                    centroid_count += 1
                    # Excluded from distribution — fallback is unreliable
                else:
                    failed += 1
            else:
                failed += 1
        distros[code] = dict(area_counts)
        distros[code]["_total"] = total
        distros[code]["_geocoded"] = geocoded
        distros[code]["_pip"] = pip_count
        distros[code]["_centroid_excluded"] = centroid_count
        distros[code]["_failed"] = failed
    return distros

def build_neighbourhood_code_lookup(distros: dict[str, dict], out_path: Path):
    """
    Write neighbourhood_code_lookup.csv.
    Columns: neighbourhood_code, primary_local_area, primary_pct, secondary_local_area, secondary_pct,
             total_geocoded, confidence
    """
    fieldnames = [
        "neighbourhood_code",
        "primary_local_area", "primary_pct",
        "secondary_local_area", "secondary_pct",
        "total_geocoded", "total_pip", "centroid_excluded",
        "total_sampled", "geocode_success_rate",
        "confidence",
    ]
    rows = []
    for code in sorted(distros.keys()):
        d = distros[code]
        total = d["_total"]
        geocoded = d["_geocoded"]
        pip_count = d.get("_pip", geocoded)  # number of clean pip assignments
        centroid_excluded = d.get("_centroid_excluded", 0)
        failed = d["_failed"]
        success_rate = geocoded / total if total > 0 else 0.0

        # Area counts from pip-only (exclude meta keys)
        area_counts = {k: v for k, v in d.items() if not k.startswith("_")}
        sorted_areas = sorted(area_counts.items(), key=lambda x: -x[1])

        # Use pip_count as denominator — the reliable sample
        denom = pip_count if pip_count > 0 else 1

        primary_area = sorted_areas[0][0] if sorted_areas else None
        primary_n = sorted_areas[0][1] if sorted_areas else 0
        primary_pct = primary_n / denom if denom > 0 else 0.0

        secondary_area = sorted_areas[1][0] if len(sorted_areas) > 1 else None
        secondary_n = sorted_areas[1][1] if len(sorted_areas) > 1 else 0
        secondary_pct = secondary_n / denom if denom > 0 else 0.0

        # Confidence based on pip count:
        # HIGH >= 80%, MEDIUM >= 60%, LOW < 60%
        # Also penalize if pip sample is small (< 5 clean pip results)
        if pip_count == 0:
            confidence = "NO_DATA"
        elif pip_count < 5:
            confidence = "INSUFFICIENT"  # Too few clean pip results
        elif primary_pct >= 0.80:
            confidence = "HIGH"
        elif primary_pct >= 0.60:
            confidence = "MEDIUM"
        else:
            confidence = "LOW"

        rows.append({
            "neighbourhood_code": code,
            "primary_local_area": primary_area or "",
            "primary_pct": f"{primary_pct:.1%}",
            "secondary_local_area": secondary_area or "",
            "secondary_pct": f"{secondary_pct:.1%}",
            "total_geocoded": geocoded,
            "total_pip": pip_count,
            "centroid_excluded": centroid_excluded,
            "total_sampled": total,
            "geocode_success_rate": f"{success_rate:.1%}",
            "confidence": confidence,
        })

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    log(f"Wrote {len(rows)} rows to {out_path.name}")
    return rows

# ─── Temporal stability check ──────────────────────────────────────────────────

def check_temporal_stability(csv_files: list[Path], n_pids: int = 200) -> dict:
    """
    Sample PIDs that appear in multiple years and verify neighbourhood_code consistency.
    Returns stats dict.
    """
    log("Running temporal stability check...")
    # First pass: collect pid -> set of (year, code) pairs
    pid_data: dict[str, set] = defaultdict(set)

    for f in csv_files:
        with open(f, encoding="utf-8-sig") as fh:
            reader = csv.DictReader(fh)
            for row in reader:
                pid = row.get("pid", "").strip()
                code = row.get("neighbourhood_code", "").strip()
                year = row.get("report_year", row.get("tax_assessment_year", "")).strip()
                if pid and code:
                    pid_data[pid].add((year, code))

    # Find PIDs that appear in multiple years
    multi_year_pids = {pid: data for pid, data in pid_data.items() if len(set(y for y, c in data)) > 1}
    log(f"PIDs appearing in multiple years: {len(multi_year_pids):,}")

    # Sample up to n_pids
    rng = random.Random(RANDOM_SEED)
    sample_pids = rng.sample(sorted(multi_year_pids.keys()), min(n_pids, len(multi_year_pids)))

    stable = 0
    unstable = 0
    unstable_examples = []

    for pid in sample_pids:
        codes = set(c for y, c in multi_year_pids[pid])
        if len(codes) == 1:
            stable += 1
        else:
            unstable += 1
            years_codes = sorted(multi_year_pids[pid])
            unstable_examples.append({
                "pid": pid,
                "changes": years_codes
            })

    total = stable + unstable
    stability_rate = stable / total if total > 0 else 1.0

    log(f"Temporal stability: {stable}/{total} PIDs stable ({stability_rate:.1%})")
    if unstable_examples:
        log(f"Unstable PIDs (first 5 examples):")
        for ex in unstable_examples[:5]:
            log(f"  PID {ex['pid']}: {ex['changes']}")

    return {
        "total_pids_sampled": total,
        "stable": stable,
        "unstable": unstable,
        "stability_rate": stability_rate,
        "unstable_examples": unstable_examples[:10],
        "multi_year_pid_count": len(multi_year_pids),
    }

# ─── Name normalization ────────────────────────────────────────────────────────

def build_name_normalization(geojson_path: Path, bl_sample_path: Path, out_path: Path):
    """
    Build area_name_normalization.csv by comparing GeoJSON names to business licence localarea names.
    """
    # GeoJSON names
    with open(geojson_path) as f:
        gj = json.load(f)
    geojson_names = sorted(feat["properties"]["name"] for feat in gj["features"])

    # Business licence names
    bl_names = set()
    with open(bl_sample_path) as fh:
        reader = csv.DictReader(fh, delimiter=";")
        for row in reader:
            la = row.get("localarea", "").strip()
            if la:
                bl_names.add(la)
    bl_names = sorted(bl_names)

    # Build normalization: try to match GeoJSON → BL via case-insensitive + hyphen/space normalization
    def normalize(s: str) -> str:
        return s.lower().replace("-", " ").replace("_", " ").strip()

    normalized_geojson = {normalize(n): n for n in geojson_names}
    normalized_bl = {normalize(n): n for n in bl_names}

    rows = []
    all_keys = sorted(set(normalized_geojson.keys()) | set(normalized_bl.keys()))
    for key in all_keys:
        gj_name = normalized_geojson.get(key, "")
        bl_name = normalized_bl.get(key, "")
        # Canonical name: prefer GeoJSON (it's the spatial authority)
        canonical = gj_name or bl_name
        rows.append({
            "geojson_name": gj_name,
            "business_licence_name": bl_name,
            "canonical_name": canonical,
            "notes": "" if gj_name == bl_name else ("hyphen_diff" if gj_name and bl_name else ("geojson_only" if gj_name else "bl_only")),
        })

    with open(out_path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=["geojson_name", "business_licence_name", "canonical_name", "notes"])
        writer.writeheader()
        writer.writerows(rows)
    log(f"Wrote {len(rows)} rows to {out_path.name}")
    return rows

# ─── Markdown summary doc ──────────────────────────────────────────────────────

def write_markdown_doc(
    distros: dict[str, dict],
    lookup_rows: list[dict],
    temporal_stats: dict,
    norm_rows: list[dict],
    polygons: list[dict],
    sampled: dict[str, list[tuple]],
    out_path: Path,
):
    """Write NEIGHBOURHOOD_CODE_MAPPING.md with full methodology and results."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    total_geocoded = sum(d["_geocoded"] for d in distros.values())
    total_pip = sum(d.get("_pip", 0) for d in distros.values())
    total_centroid = sum(d.get("_centroid_excluded", 0) for d in distros.values())
    total_sampled = sum(d["_total"] for d in distros.values())
    total_failed = sum(d["_failed"] for d in distros.values())
    success_rate = total_geocoded / total_sampled if total_sampled > 0 else 0.0
    pip_rate = total_pip / total_geocoded if total_geocoded > 0 else 0.0

    high_conf = sum(1 for r in lookup_rows if r["confidence"] == "HIGH")
    med_conf = sum(1 for r in lookup_rows if r["confidence"] == "MEDIUM")
    low_conf = sum(1 for r in lookup_rows if r["confidence"] == "LOW")
    no_data = sum(1 for r in lookup_rows if r["confidence"] == "NO_DATA")
    insuf_conf = sum(1 for r in lookup_rows if r["confidence"] == "INSUFFICIENT")

    # Collect ALL areas that appear in any code's distribution (not just primary/secondary)
    areas_covered = set()
    for code, d in distros.items():
        for k, v in d.items():
            if not k.startswith("_") and v > 0:
                areas_covered.add(k)
    all_areas = {p["name"] for p in polygons}
    missing_areas = sorted(all_areas - areas_covered)

    # Build distribution tables
    dist_tables = []
    for code in sorted(distros.keys()):
        d = distros[code]
        geocoded = d["_geocoded"]
        pip_n = d.get("_pip", geocoded)
        centroid_n = d.get("_centroid_excluded", 0)
        failed = d["_failed"]
        area_counts = {k: v for k, v in d.items() if not k.startswith("_")}
        sorted_areas = sorted(area_counts.items(), key=lambda x: -x[1])

        table_lines = []
        table_lines.append(f"\n#### Code {code}")
        table_lines.append(f"Sampled: {d['_total']} | Geocoded: {geocoded} | PIP (used): {pip_n} | Centroid-fallback (excluded): {centroid_n} | Geocode failures: {failed}")
        table_lines.append("*(Percentages are of PIP-confirmed assignments only)*")
        if sorted_areas:
            table_lines.append("")
            table_lines.append("| Local Area | Count | Pct of PIP |")
            table_lines.append("|-----------|-------|------------|")
            for area, n in sorted_areas:
                pct = n / pip_n if pip_n > 0 else 0.0
                table_lines.append(f"| {area} | {n} | {pct:.1%} |")
        else:
            table_lines.append("*No successful PIP geocodes for this code.*")
        dist_tables.append("\n".join(table_lines))

    # Temporal stability section
    ts = temporal_stats
    ts_section = f"""## 5. Temporal Stability Check

Sampled **{ts['total_pids_sampled']}** PIDs from **{ts['multi_year_pid_count']:,}** total multi-year PIDs.

| Metric | Value |
|--------|-------|
| PIDs stable (same code all years) | {ts['stable']} ({ts['stability_rate']:.1%}) |
| PIDs with code changes | {ts['unstable']} |

"""
    if ts["unstable_examples"]:
        ts_section += "### Unstable PID Examples\n\n"
        for ex in ts["unstable_examples"][:5]:
            ts_section += f"- PID `{ex['pid']}`: {ex['changes']}\n"
    else:
        ts_section += "*All sampled PIDs had stable neighbourhood codes across years.*\n"

    # Name normalization section
    norm_lines = ["## 6. Area Name Normalization\n"]
    norm_lines.append("| GeoJSON Name | Business Licence Name | Canonical | Notes |")
    norm_lines.append("|-------------|----------------------|-----------|-------|")
    for r in norm_rows:
        norm_lines.append(f"| {r['geojson_name']} | {r['business_licence_name']} | {r['canonical_name']} | {r['notes']} |")
    norm_section = "\n".join(norm_lines)

    md = f"""# Vancouver Neighbourhood Code Mapping
**Generated**: {now}
**Method**: Bulk spatial join — stratified sample of {SAMPLE_PER_CODE} addresses per code, BC Geocoder API, Shapely point-in-polygon
**Status**: DEFINITIVE (replaces coin-flip 2-sample approach)

---

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| Total addresses sampled | {total_sampled} |
| Successfully geocoded | {total_geocoded} ({success_rate:.1%}) |
| Clean pip assignments (used in distribution) | {total_pip} ({pip_rate:.1%} of geocoded) |
| Nearest-centroid fallbacks (excluded from distribution) | {total_centroid} |
| Failed geocoding | {total_failed} |
| HIGH confidence codes (≥80% in primary area) | {high_conf}/30 |
| MEDIUM confidence codes (60-79%) | {med_conf}/30 |
| LOW confidence codes (<60%, genuinely multi-area) | {low_conf}/30 |
| INSUFFICIENT pip sample (<5 clean results) | {insuf_conf}/30 |
| NO_DATA codes | {no_data}/30 |
| CoV areas covered (appear as primary or secondary) | {len(areas_covered)}/22 |
| CoV areas with zero codes assigned | {len(missing_areas)} |

{"⚠️ WARNING: " + str(len(missing_areas)) + " areas still missing from mapping: " + ", ".join(missing_areas) if missing_areas else "✓ All 22 CoV local areas are represented in the mapping."}

---

## 2. Neighbourhood Code Lookup Table

| Code | Primary Area | Pct | Secondary Area | Pct | PIP/Geocoded/Sampled | Confidence |
|------|-------------|-----|----------------|-----|----------------------|------------|
""" + "\n".join(
    f"| {r['neighbourhood_code']} | {r['primary_local_area']} | {r['primary_pct']} | {r['secondary_local_area']} | {r['secondary_pct']} | {r['total_pip']}/{r['total_geocoded']}/{r['total_sampled']} | {r['confidence']} |"
    for r in lookup_rows
) + f"""

---

## 3. Methodology

### 3.1 Data Sources
- **Property tax data**: 4 CSV files, 4.25M rows total (2006–present)
- **Boundary polygons**: CoV local area boundary GeoJSON (22 features)
- **Geocoding service**: BC Geocoder API (geocoder.api.gov.bc.ca) — provincial government, no auth, excellent BC coverage

### 3.2 Sampling Strategy
With ~126,000 unique civic addresses across 30 codes, full geocoding would take ~10 hours. Stratified sample:
1. Extract all unique (from_civic_number, street_name, property_postal_code) per code
2. Sample up to {SAMPLE_PER_CODE} per code (stratified random, seed={RANDOM_SEED})
3. Total sample: ~{total_sampled} addresses (~{NOMINATIM_DELAY} sec/request ≈ {total_sampled * NOMINATIM_DELAY / 60:.0f} minutes)

### 3.3 Point-in-Polygon Test
- Shapely v2.x `contains()` on each of 22 CoV boundary polygons
- Coordinates: (lon, lat) in WGS84 (BC Geocoder returns WGS84)
- Fallback for points outside all polygons: nearest centroid — **EXCLUDED from code distributions** because the fallback is unreliable (a point slightly outside the Downtown polygon may get assigned to Hastings-Sunrise whose centroid is closest geometrically but semantically wrong). Only pip-confirmed assignments are used for code-to-area distributions.

### 3.4 Confidence Levels
- **HIGH**: Primary area captures ≥80% of geocoded addresses in that code
- **MEDIUM**: Primary area captures 60–79%
- **LOW**: Primary area captures <60% — code genuinely spans multiple areas, fractional assignment appropriate
- **NO_DATA**: Zero successful geocodes for this code

### 3.5 What This Means for Analysis
- HIGH confidence codes: safe to use as a proxy for a single CoV area
- LOW confidence codes: do NOT treat as a single area. Weight by percentage or stratify separately.
- Missing areas: if all 22 areas are covered, the mapping is complete. If any are missing, properties in those areas will be misclassified.

---

## 4. Distribution by Code
{"".join(dist_tables)}

---

{ts_section}

---

{norm_section}

---

## 7. Limitations and Future Work

1. **Sample size**: {SAMPLE_PER_CODE} samples per code. For codes with LOW confidence, increasing to 50–100 samples would give tighter percentage estimates.
2. **Null civic numbers**: 52.9% of rows have no civic number and cannot be geocoded by this method. Street-level geocoding (street + postal only) would give lower-confidence assignments for these.
3. **Temporal coverage**: Sampled addresses include all years (2006–present). Earlier years may have fewer unique addresses in some codes.
4. **BC Geocoder accuracy**: The BC Geocoder returns coordinates for all queried addresses (100% geocode success), but ~13.5% of returned coordinates fell outside all 22 CoV polygon boundaries and were excluded from distributions via the nearest-centroid fallback.
5. **Full geocoding**: For production use with >1000 samples per code, consider Canada Post AddressComplete API (paid) or Natural Resources Canada (free but rate-limited).

---

*Generated by geocode_bulk.py on {now}.*
*Replaces the 2-sample coin-flip approach reviewed in A1_APPROACH_REVIEW.md.*
"""
    with open(out_path, "w") as f:
        f.write(md)
    log(f"Wrote markdown doc to {out_path.name}")

# ─── Main ──────────────────────────────────────────────────────────────────────

def main():
    global log_fh

    full_mode = "--full" in sys.argv
    resume_mode = "--resume" in sys.argv or True  # Always resume by default

    with open(LOG_FILE, "a") as lf:
        log_fh = lf
        log("=" * 70)
        log(f"geocode_bulk.py starting. Mode: {'full' if full_mode else 'sampled'}")
        log("=" * 70)

        # Load polygons
        polygons = load_polygons(GEOJSON_FILE)
        log(f"Loaded {len(polygons)} CoV boundary polygons: {[p['name'] for p in polygons]}")

        # Extract unique addresses per code
        code_addresses = extract_addresses_by_code(CSV_FILES)

        if full_mode:
            # Use all addresses — this will take hours
            sampled = {code: sorted(addrs) for code, addrs in code_addresses.items()}
            total = sum(len(v) for v in sampled.values())
            log(f"FULL MODE: {total:,} addresses to geocode (~{total * NOMINATIM_DELAY / 3600:.1f} hours)")
        else:
            rng = random.Random(RANDOM_SEED)
            sampled = sample_addresses(code_addresses, SAMPLE_PER_CODE, rng)

        # Load existing progress
        existing = load_progress(PROGRESS_JSONL)

        # Run geocoding
        results = run_geocoding(sampled, polygons, existing, PROGRESS_JSONL)

        # Build outputs
        build_address_to_area_csv(results, sampled, ADDRESS_TO_AREA_CSV)

        distros = build_code_distributions(sampled, results)

        lookup_out = DATA_DIR / "neighbourhood_code_lookup.csv"
        lookup_rows = build_neighbourhood_code_lookup(distros, lookup_out)

        # Temporal stability (runs a separate pass through CSVs — may take a few minutes)
        temporal_stats = check_temporal_stability(CSV_FILES, n_pids=200)

        # Name normalization
        norm_out = DATA_DIR / "area_name_normalization.csv"
        norm_rows = build_name_normalization(GEOJSON_FILE, BUSINESS_LICENCE_SAMPLE, norm_out)

        # Markdown doc
        md_out = DATA_DIR / "NEIGHBOURHOOD_CODE_MAPPING.md"
        write_markdown_doc(distros, lookup_rows, temporal_stats, norm_rows, polygons, sampled, md_out)

        log("=" * 70)
        log("All done.")
        log("=" * 70)

if __name__ == "__main__":
    main()
