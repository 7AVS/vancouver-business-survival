"""
Backfill localarea in commercial-panel-v2.csv
=======================================================================
Strategy (in priority order):
  1. Match (house, street) → most recent localarea from raw licence data
     - Source A: business-licences-current.csv  (FY24-26, semicolon-sep, UTF-8 BOM)
     - Source B: business-licences-2013-to-2024.csv  (archive — 0 localarea values, skipped)
  2. Match (house, street) → address_to_area.csv (1,461 geocoded addresses)
  3. Match postal code prefix → neighbourhood_code_lookup.csv (highest-weight area)
  4. Report remaining unmapped

NOTE: Uses .map() on the full panel index rather than merge-then-loc to avoid
index-reset corruption. Each fill step only writes to rows that are still null.

Usage:
    /home/aurora/projects/sites/portfolio-projects/van-property-tax/.venv/bin/python \
        scripts/backfill_localarea.py
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

import pandas as pd
import numpy as np

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT   = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"
PANEL     = os.path.join(PROJECT, "data/processed/commercial-panel-v2.csv")
RAW_CURR  = os.path.join(PROJECT, "data/raw/business-licences/business-licences-current.csv")
ADDR_AREA = os.path.join(PROJECT, "data/processed/address_to_area.csv")
NCODE_LU  = os.path.join(PROJECT, "data/processed/neighbourhood_code_lookup.csv")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def make_addr_key(house_series, street_series):
    """Normalised (house, street) key: uppercase, stripped."""
    h = house_series.astype(str).str.strip().str.upper()
    s = street_series.astype(str).str.strip().str.upper()
    return h + "|||" + s

def pct_to_float(s):
    """'54.0%' → 0.54"""
    if pd.isna(s):
        return 0.0
    return float(str(s).replace("%", "").strip()) / 100.0

# ---------------------------------------------------------------------------
# 1. Load panel
# ---------------------------------------------------------------------------
print("=" * 60)
print("Step 1: Loading commercial panel…")
panel = pd.read_csv(PANEL, low_memory=False)
n_total    = len(panel)
n_already  = panel["localarea"].notna().sum()
n_null_ini = n_total - n_already
print(f"  {n_total:,} businesses loaded")
print(f"  {n_already:,} already have localarea ({100*n_already/n_total:.1f}%)")
print(f"  {n_null_ini:,} need backfill")

# Pre-compute normalised address key for every panel row
panel["_addr_key"] = make_addr_key(panel["house"], panel["street"])
# Track fill source (informational only)
panel["_fill_source"] = "original"
panel.loc[panel["localarea"].isna(), "_fill_source"] = pd.NA

# ---------------------------------------------------------------------------
# 2. Build address→localarea lookup from current raw licence file (FY24-26)
# ---------------------------------------------------------------------------
print("\nStep 2: Building address→localarea lookup from raw licence data…")
print("  Loading business-licences-current.csv (FY24-26, semicolon-delimited)…")
curr = pd.read_csv(
    RAW_CURR,
    sep=";",
    low_memory=False,
    encoding="utf-8-sig",
    usecols=["folderyear", "house", "street", "localarea"],
)
print(f"    {len(curr):,} rows, localarea non-null: {curr['localarea'].notna().sum():,}")

curr_valid = curr.dropna(subset=["house", "street", "localarea"]).copy()
curr_valid["_addr_key"] = make_addr_key(curr_valid["house"], curr_valid["street"])
# Most recent year first → drop_duplicates keeps first = most recent
curr_valid = curr_valid.sort_values("folderyear", ascending=False)
addr_dict = (
    curr_valid.drop_duplicates("_addr_key")
    .set_index("_addr_key")["localarea"]
    .to_dict()
)
print(f"  Unique (house, street) → localarea mappings: {len(addr_dict):,}")

print("  (Archive file business-licences-2013-to-2024.csv has 0 localarea values — skipped)")

# ---------------------------------------------------------------------------
# 3. Apply raw-data lookup to panel nulls
# ---------------------------------------------------------------------------
print("\nStep 3: Applying address lookup to panel…")
null_mask = panel["localarea"].isna()
raw_match = panel.loc[null_mask, "_addr_key"].map(addr_dict)
filled_raw = raw_match.notna()
n_raw = filled_raw.sum()
panel.loc[null_mask & filled_raw, "localarea"]    = raw_match[filled_raw]
panel.loc[null_mask & filled_raw, "_fill_source"] = "raw_licence_lookup"
print(f"  Filled {n_raw:,} / {null_mask.sum():,} null businesses via (house, street) lookup")

# ---------------------------------------------------------------------------
# 4. Apply address_to_area.csv for remaining nulls
# ---------------------------------------------------------------------------
print("\nStep 4: Applying address_to_area.csv…")
addr_geo = pd.read_csv(ADDR_AREA, low_memory=False)
addr_geo_valid = addr_geo.dropna(subset=["from_civic_number", "street_name", "local_area_name"]).copy()
addr_geo_valid["_addr_key"] = make_addr_key(
    addr_geo_valid["from_civic_number"], addr_geo_valid["street_name"]
)
geo_dict = (
    addr_geo_valid.sort_values("geocode_score", ascending=False)
    .drop_duplicates("_addr_key")
    .set_index("_addr_key")["local_area_name"]
    .to_dict()
)
print(f"  address_to_area lookup: {len(geo_dict):,} entries")

null_mask2 = panel["localarea"].isna()
geo_match  = panel.loc[null_mask2, "_addr_key"].map(geo_dict)
filled_geo = geo_match.notna()
n_geo = filled_geo.sum()
panel.loc[null_mask2 & filled_geo, "localarea"]    = geo_match[filled_geo]
panel.loc[null_mask2 & filled_geo, "_fill_source"] = "address_to_area"
print(f"  Filled {n_geo:,} / {null_mask2.sum():,} remaining nulls via address_to_area")

# ---------------------------------------------------------------------------
# 5. Postal code prefix → neighbourhood → local area
# ---------------------------------------------------------------------------
print("\nStep 5: Postal code prefix matching…")
ncode = pd.read_csv(NCODE_LU, low_memory=False)
ncode["_primary_pct_f"] = ncode["primary_pct"].apply(pct_to_float)

# Map: neighbourhood_code (int) → primary_local_area
ncode_to_area = (
    ncode.set_index("neighbourhood_code")[["primary_local_area", "_primary_pct_f"]]
    .to_dict("index")
)

# Map: postal_prefix → neighbourhood_code (mode per prefix from geocoded data)
addr_postal = addr_geo.dropna(subset=["property_postal_code", "neighbourhood_code"]).copy()
addr_postal["_postal_prefix"] = (
    addr_postal["property_postal_code"].astype(str).str.strip().str.upper().str[:3]
)
postal_to_ncode = (
    addr_postal.groupby("_postal_prefix")["neighbourhood_code"]
    .agg(lambda x: x.value_counts().index[0])  # mode
    .to_dict()
)

# Combine: postal_prefix → local_area (via ncode)
postal_area_dict = {}
for prefix, nc in postal_to_ncode.items():
    if nc in ncode_to_area:
        postal_area_dict[prefix] = ncode_to_area[nc]["primary_local_area"]

print(f"  Postal prefix → localarea mappings: {len(postal_area_dict):,} prefixes covered")

null_mask3 = panel["localarea"].isna()
panel["_postal_prefix"] = (
    panel["postalcode"].astype(str).str.strip().str.upper().str[:3]
)
postal_match = panel.loc[null_mask3, "_postal_prefix"].map(postal_area_dict)
filled_postal = postal_match.notna()
n_postal = filled_postal.sum()
panel.loc[null_mask3 & filled_postal, "localarea"]    = postal_match[filled_postal]
panel.loc[null_mask3 & filled_postal, "_fill_source"] = "postal_prefix"
print(f"  Filled {n_postal:,} / {null_mask3.sum():,} remaining nulls via postal prefix")

# ---------------------------------------------------------------------------
# 6. Coverage report
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("COVERAGE REPORT")
print("=" * 60)

n_orig    = n_already                        # pre-existing
n_unmapped = panel["localarea"].isna().sum()
n_mapped   = panel["localarea"].notna().sum()

print(f"\nFill source breakdown:")
print(f"  Original (pre-existing)     : {n_orig:>8,}  ({100*n_orig/n_total:.1f}%)")
print(f"  Raw licence lookup          : {n_raw:>8,}  ({100*n_raw/n_total:.1f}%)")
print(f"  address_to_area.csv         : {n_geo:>8,}  ({100*n_geo/n_total:.1f}%)")
print(f"  Postal prefix lookup        : {n_postal:>8,}  ({100*n_postal/n_total:.1f}%)")
print(f"  Unmapped (null)             : {n_unmapped:>8,}  ({100*n_unmapped/n_total:.1f}%)")
print(f"  ─────────────────────────────────────────")
print(f"  Total businesses            : {n_total:>8,}")
print(f"  Total with localarea        : {n_mapped:>8,}  ({100*n_mapped/n_total:.1f}%)")

coverage_pct = 100 * n_mapped / n_total
print(f"\nOverall coverage: {coverage_pct:.1f}%")

# Coverage by first_year
print("\nCoverage by first_year:")
year_grp = panel.groupby("first_year").apply(
    lambda g: pd.Series({
        "total":    len(g),
        "with_area": g["localarea"].notna().sum(),
    })
).reset_index()
year_grp["pct"] = 100 * year_grp["with_area"] / year_grp["total"]
year_grp["pct"] = year_grp["pct"].map("{:.1f}%".format)
print(year_grp.to_string(index=False))

# Unmapped breakdown
n_unmapped_no_addr    = panel[panel["localarea"].isna() & ~panel["has_address"]].shape[0]
n_unmapped_addr_no_la = panel[panel["localarea"].isna() & panel["has_address"]].shape[0]
n_unmapped_no_postal  = panel[panel["localarea"].isna() & panel["postalcode"].isna()].shape[0]
print(f"\nUnmapped breakdown:")
print(f"  No address at all                   : {n_unmapped_no_addr:,}")
print(f"  Has address, not in FY24-26 data     : {n_unmapped_addr_no_la:,}")
print(f"  Has postalcode but prefix not covered : {panel[panel['localarea'].isna() & panel['postalcode'].notna()].shape[0]:,}")
print(f"  No postalcode                         : {n_unmapped_no_postal:,}")

# ---------------------------------------------------------------------------
# 7. Threshold check before save
# ---------------------------------------------------------------------------
if coverage_pct < 60:
    print(f"\n{'!' * 60}")
    print(f"STOPPING: Coverage {coverage_pct:.1f}% is below 60% threshold.")
    print(f"Do not run Step 3 on this data — results would be unreliable.")
    print(f"{'!' * 60}")
    panel.drop(columns=["_addr_key", "_fill_source", "_postal_prefix"], inplace=True, errors="ignore")
    sys.exit(1)

print(f"\nCoverage {coverage_pct:.1f}% meets threshold (>=60%). Proceeding to save.")

# ---------------------------------------------------------------------------
# 8. Save updated panel
# ---------------------------------------------------------------------------
print("\nSaving updated panel…")
panel.drop(columns=["_addr_key", "_fill_source", "_postal_prefix"], inplace=True, errors="ignore")
panel.to_csv(PANEL, index=False)
print(f"  Saved to {PANEL}")
print("\nBackfill complete.")
