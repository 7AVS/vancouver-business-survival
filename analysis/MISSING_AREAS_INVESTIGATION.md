# Missing Areas Investigation: Fast Path to 6 Local Areas

**Date**: 2026-03-03
**Investigator**: Claude Code (Desk-Mode Agent)
**Question**: Is there a fast path to get land value data for the 6 local areas currently missing from `neighbourhood_land_values.csv`?

**Missing areas**: Grandview-Woodland, Kensington-Cedar Cottage, Kitsilano, South Cambie, Victoria-Fraserview, West Point Grey

---

## Verdict: MODERATE (not trivial, not hard)

The data exists in `address_to_area.csv` already — no new geocoding required. The fix requires extending the lookup schema to support 3+ areas per code and re-running `compute_land_values.py`. Estimated effort: 2–3 hours of coding + ~20 min compute.

---

## Step 1: Schema Audit — All Columns in the Property Tax CSVs

All four property tax files share the same core schema:

```
pid, legal_type, folio, land_coordinate, zoning_district, zoning_classification,
lot, plan, block, district_lot, from_civic_number, to_civic_number, street_name,
property_postal_code, narrative_legal_line1–5, current_land_value,
current_improvement_value, tax_assessment_year, previous_land_value,
previous_improvement_value, year_built, big_improvement_year, tax_levy,
neighbourhood_code, report_year, [note — 2020-present only]
```

**Definitive answer on each geographic field type:**

| Field | Type | Usable for area assignment? |
|-------|------|-----------------------------|
| `neighbourhood_code` | BC Assessment internal code (001–030), NOT a CoV local area | No — root cause of the problem |
| `from_civic_number` | Street number, present for ~50.5% of rows (mostly STRATA) | Partial — only strata units have it |
| `street_name` | Street name, present for ~99.9% of rows | Street-level only — no civic number for 97.1% of unique parcels |
| `property_postal_code` | Postal code, present for ~60% of rows | Too coarse — each FSA/LDU spans multiple local areas |
| `land_coordinate` | BC Assessment parcel ID (8-digit integer) | No coordinates — it's an ID, not lat/lon |
| `pid` | BC Assessment PID (formatted as `XXX-XXX-XXX`) | No coordinates — administrative ID |
| `folio` | = land_coordinate + strata unit suffix | Same as land_coordinate |
| `zoning_district` | RS-1, CD-1, etc. | Zoning codes span area boundaries — not usable |
| No `localarea` field | — | NOT PRESENT in any version of the bulk CSV or API |

**No direct area identifier exists in the property tax data.** The CoV Open Data API was confirmed to return the same schema — `geo_local_area` does not appear in any API response (a prior investigation in `A1_APPROACH_REVIEW.md` suggested checking for it; it is confirmed absent).

---

## Step 2: Why the 6 Areas Are Missing — Root Cause

The current `neighbourhood_code_lookup.csv` was built by `geocode_bulk.py`: sample 50 addresses per neighbourhood code, geocode them via BC Geocoder, do a point-in-polygon test against the CoV boundary GeoJSON, then assign the **plurality area** as `primary` and the **second-most-common area** as `secondary`.

The 6 missing areas are **never the plurality** in any of the 30 codes. They appear as minorities:

| Missing Area | Codes Where It Appears | Max Sample % | Notes |
|---|---|---|---|
| Grandview-Woodland | 001, 012–015, 017, 019, 021, 024–026, 028 | 28% (code 019) | Spread thin across 11 codes |
| Kensington-Cedar Cottage | 005, 015, 016, 019, 023 | 16% (code 015) | Small area, always a minority |
| Kitsilano | 002 only | 8% (code 002) | Appears in only 1 code |
| South Cambie | 003, 005, 007, 009 | 6% (code 009) | Small area, low sample counts |
| Victoria-Fraserview | 019, 023, 024, 025 | 6% (code 024) | Consistently small minority |
| West Point Grey | 001–009, 011, 030 | 12% (code 001) | Spread across 10+ codes |

The fundamental problem is structural: **BC Assessment neighbourhood codes (001–030) are not aligned with CoV local areas (22 areas)**. Each code covers portions of multiple CoV neighbourhoods. The current lookup discards any area below the plurality threshold, which silently drops these 6 areas.

---

## Step 3: Geographic Data Available for a Spatial Approach

### What we have
- `data/raw/local-area-boundary.geojson`: 22 CoV boundary polygons (Shapely-compatible, already used)
- `data/processed/address_to_area.csv`: 1,462 geocoded addresses with `lat`, `lon`, `local_area_name` (includes all 6 missing areas)
- BC Geocoder API: free, ~5 req/s, handles Vancouver addresses well

### Address coverage reality
- STRATA properties (84.8% have civic numbers): ~50K unique building addresses across all files
- LAND properties (99.8% lack civic numbers): ~94K+ unique parcels with **only a street name**, no house number
- Total rows: 4,252,891 across 4 files; 52.7% lack a civic number entirely

**Geocoding the full dataset is not feasible as a bulk row-level operation** (4.25M rows). But it IS feasible at the unique-address level with the right strategy:

| Approach | Unique units to geocode | Time estimate | Coverage |
|----------|------------------------|---------------|----------|
| Unique (civic, street) pairs — all 4 files | 50,826 | ~2.8 hrs at 5 req/s | ~47% of rows |
| Unique land_coordinates (parcels) | ~95,000 | Not directly geocodable — parcel IDs, not addresses | — |
| Single-address per building (strata only) | ~50K | Same as above | Strata only |

The 52.7% of rows with no civic number (mostly LAND/SFH parcels) would require BC Assessment parcel-to-coordinate data, which is not publicly available without a licensed MapBC/ParcelMap BC subscription.

---

## Step 4: The Actual Fast Path

### Option A — TRIVIAL: Extend the existing lookup (recommended)

**The data already exists in `address_to_area.csv`.** The 1,462 geocoded addresses include properties from all 6 missing areas. The fix is:

1. Re-read `address_to_area.csv` and compute the full area distribution for each of the 30 codes (not just top-2)
2. Update `neighbourhood_code_lookup.csv` to support a third (and possibly fourth) area weight column
3. Update `compute_land_values.py` to read the tertiary weight columns
4. Re-run `compute_land_values.py`

**What this gives you:** The 6 missing areas gain fractional representation based on their share of the geocoded sample. The sample is 50 addresses per code, so minority areas at 8–28% are statistically meaningful (4–14 out of 50). This is better than zero — which is the current state.

**Limitation:** The sample percentages are noisy estimates, especially for low-count entries (e.g., Kitsilano appearing 4/50 times in code 002, or South Cambie 3/50 in code 009). The areas will appear in the output but with less precision than areas with higher sample fractions. Results should be flagged as LOW-confidence.

**Estimated effort:** 2–3 hours to extend the lookup schema, update the compute script, validate output.

**No new geocoding required.**

---

### Option B — MODERATE: Full strata address geocoding

Geocode all ~50K unique (civic, street) pairs, build a `(civic, street) → local_area` lookup table, join against the full dataset for strata rows.

- Covers ~47% of rows (strata units with civic numbers)
- Remaining 53% (LAND parcels, no civic number) still need the code-based lookup
- Time: ~3 hours of geocoding + several hours of coding
- Result: Higher-precision area assignment for strata, code-lookup fallback for SFH/lots

**When this makes sense:** If the fractional-weight approach (Option A) produces suspicious results for a specific area, targeted geocoding of the relevant codes' addresses would validate or correct it.

---

### Option C — HARD: Full parcel-level spatial join

Geocode all 95K unique parcels, including the 97% that only have a street name.

- Street-only geocoding returns a street centroid, not a parcel point — introduces spatial error at boundaries
- For properties on streets that straddle two CoV areas (e.g., a street on the Kitsilano/Arbutus Ridge boundary), errors are systematic
- Time: ~7 hours of geocoding + full rebuild
- Result: Best coverage but still imperfect for boundary parcels; still misses parcels with no street name (0.1%)

---

### Option D — IMPOSSIBLE for this dataset

A direct `geo_local_area` field does **not** exist in the property tax data — neither in the bulk CSV nor in the CoV Open Data API. The `taxyvr` R package documentation that suggested this field exists was describing a different or earlier version of the data; it is confirmed absent in the current downloads.

---

## Recommendation

**Use Option A.** Here is the specific implementation plan:

### What to change in `neighbourhood_code_lookup.csv`

Add `tertiary_local_area` and `tertiary_pct` columns. Populate from `address_to_area.csv` for any area that:
1. Appears in >0% of the geocoded sample for a code
2. Is not already the primary or secondary area
3. Is one of the 6 currently missing areas (prioritize these)

Key entries to add (from the existing 50-sample data):

| Code | Currently Primary | Currently Secondary | Tertiary to Add | Tertiary % |
|------|------------------|--------------------|----|---|
| 019 | Sunset (30%) | Riley Park (30%) | Grandview-Woodland | 28% |
| 014 | Mount Pleasant (30%) | Hastings-Sunrise (28%) | Grandview-Woodland | 24% |
| 015 | Riley Park (30%) | Killarney (20%) | Kensington-Cedar Cottage | 16% |
| 001 | Mount Pleasant (54%) | Dunbar-Southlands (32%) | West Point Grey | 12% |
| 021 | Mount Pleasant (44%) | Hastings-Sunrise (28%) | Grandview-Woodland | 14% |
| 017 | Sunset (22%) | Strathcona (22%) | Grandview-Woodland | 12% |
| 003 | Riley Park (72%) | West Point Grey (10%) | *(already 2nd)* | — |
| 002 | Mount Pleasant (54%) | Arbutus Ridge (10%) | Kitsilano | 8% |
| 019 | *(above)* | | Kensington-Cedar Cottage | 8% |
| 009 | Riley Park (46%) | Downtown (38%) | South Cambie | 6% |
| 024 | Sunset (38%) | Killarney (26%) | Victoria-Fraserview | 6% |

Note: West Point Grey already appears as secondary in code 003. The compute script should pick it up from there — check if it does, and if not, it's a bug in the script (it only emits secondary if confidence is not HIGH and secondary is non-empty).

### What to change in `compute_land_values.py`

The `code_weights` dict build loop currently only reads `primary_local_area` and `secondary_local_area`. Extend it to read `tertiary_local_area` (and `tertiary_pct`) when present. The rest of the pipeline is already area-agnostic — it iterates over `code_weights[code]` which can have any number of `(area, weight)` tuples.

---

## Data Quality Caveat

The 50-sample geocoding was done on addresses that **skew toward strata properties** (they have civic numbers; LAND parcels mostly don't). Strata units are concentrated in certain building types (condos, apartments) and in higher-density areas. This means the sample-based percentages may underrepresent the true fraction of SFH lots in areas like West Point Grey, Kitsilano, and South Cambie (which are heavily residential).

In other words: the Option A fix will produce **an improvement over zero** but the resulting percentages should be treated as rough estimates, not ground truth. Flag these 6 areas with a `LOW` confidence marker in the output.

---

## Files Referenced

| File | Role |
|------|------|
| `data/raw/property-tax-report-*.csv` | Source data (no local_area field) |
| `data/processed/neighbourhood_code_lookup.csv` | Current lookup — needs tertiary columns |
| `data/processed/address_to_area.csv` | 1,462 geocoded samples — already has the data |
| `data/raw/local-area-boundary.geojson` | 22 CoV boundary polygons |
| `scripts/geocode_bulk.py` | Built the 50-sample lookup |
| `scripts/compute_land_values.py` | Reads the lookup, needs tertiary column support |
| `docs/A1_APPROACH_REVIEW.md` | Prior adversarial review of this exact problem |
