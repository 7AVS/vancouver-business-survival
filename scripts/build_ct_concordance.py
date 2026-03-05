#!/usr/bin/env python3.12
"""
Build CT → Local Area concordance for Vancouver.

For each census year (2006, 2011, 2016, 2021):
  1. Load Vancouver CMA CT boundary shapefile
  2. Spatial-join with CoV 22 local-area polygons
  3. Compute fractional overlap by area
  4. Output one row per (ct_id, census_year, local_area) with overlap_fraction

Output: data/processed/ct_local_area_concordance.csv
  columns: ct_id, census_year, local_area, overlap_fraction

CT ID format: CTUID as it appears in the shapefile (e.g. '9330001.01')
  — this matches:
      2011/2021 census data: CTUID / ALT_GEO_CODE directly
      2006/2016 census data: ALT_GEO_CODE with int format 933000101
          convert: '9330001.01' -> '933000101' (remove dot)

Author: built via Claude Code, 2026-03-03
"""

import geopandas as gpd
import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings("ignore")

# ── Paths ─────────────────────────────────────────────────────────────────────
PROJECT = Path("/home/aurora/projects/sites/portfolio-projects/van-property-tax")
BDIR    = PROJECT / "data/raw/census/boundaries"
LOCAL_AREA_FILE = PROJECT / "data/raw/local-area-boundary.geojson"
OUTPUT_CSV  = PROJECT / "data/processed/ct_local_area_concordance.csv"
OUTPUT_DIR  = PROJECT / "data/processed"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# ── Shapefile config ───────────────────────────────────────────────────────────
SHAPEFILES = {
    2006: BDIR / "2006/gct_000b06a_e.shp",
    2011: BDIR / "2011/gct_000b11a_e.shp",
    2016: BDIR / "2016/lct_000b16a_e.shp",
    2021: BDIR / "2021/lct_000b21a_e.shp",
}

# Vancouver CMA code in boundary files
VAN_CMA = "933"

# ── Target CRS for area calculations ─────────────────────────────────────────
# BC Albers — EPSG:3005 — equal-area, suitable for BC
AREA_CRS = "EPSG:3005"


def load_vancouver_cts(year: int) -> gpd.GeoDataFrame:
    """Load CT polygons for Vancouver CMA from the national shapefile."""
    shp = SHAPEFILES[year]
    gdf = gpd.read_file(shp)

    if year == 2021:
        # 2021 has no CMAUID; identify Vancouver by CTUID prefix '933'
        van = gdf[gdf["CTUID"].str.startswith(VAN_CMA)].copy()
    else:
        van = gdf[gdf["CMAUID"].astype(str) == VAN_CMA].copy()

    van = van[["CTUID", "geometry"]].reset_index(drop=True)
    # Ensure CTUID is stored as string (looks like a float but must be treated as ID)
    van["CTUID"] = van["CTUID"].astype(str)
    van["census_year"] = year

    # Reproject to AREA_CRS for consistent area math
    van = van.to_crs(AREA_CRS)
    return van


def load_local_areas() -> gpd.GeoDataFrame:
    """Load CoV 22 local area boundaries and reproject to AREA_CRS."""
    la = gpd.read_file(LOCAL_AREA_FILE)[["name", "geometry"]]
    la = la.rename(columns={"name": "local_area"})
    la = la.to_crs(AREA_CRS)
    return la


def build_concordance_for_year(year: int, ct_gdf: gpd.GeoDataFrame, la_gdf: gpd.GeoDataFrame) -> pd.DataFrame:
    """
    Spatial overlay: for each CT polygon, compute fractional overlap
    with each local area polygon.

    Returns DataFrame with columns:
        ct_id, census_year, local_area, overlap_fraction
    """
    # Compute original CT areas (in AREA_CRS metres²)
    ct_gdf = ct_gdf.copy()
    ct_gdf["ct_area_m2"] = ct_gdf.geometry.area

    # Overlay: intersection gives fragments; each fragment has a CT and a local area
    overlay = gpd.overlay(ct_gdf, la_gdf, how="intersection", keep_geom_type=False)
    overlay["fragment_area_m2"] = overlay.geometry.area

    # For each CT: overlap_fraction = fragment_area / ct_area
    result = overlay.merge(
        ct_gdf[["CTUID", "ct_area_m2"]],
        on="CTUID",
        suffixes=("", "_orig")
    )
    result["overlap_fraction"] = result["fragment_area_m2"] / result["ct_area_m2_orig"]

    # Keep only meaningful overlaps (> 0.1% to filter out boundary slivers)
    result = result[result["overlap_fraction"] > 0.001].copy()

    # Normalize fractions within each CT so they sum to 1.0
    # (handles floating-point edge cases and CTs that slightly extend beyond all local areas)
    ct_totals = result.groupby("CTUID")["overlap_fraction"].sum().rename("fraction_sum")
    result = result.merge(ct_totals, on="CTUID")
    result["overlap_fraction"] = (result["overlap_fraction"] / result["fraction_sum"]).round(6)

    # Tidy up
    out = result[["CTUID", "census_year", "local_area", "overlap_fraction"]].copy()
    out = out.rename(columns={"CTUID": "ct_id"})
    # Force ct_id to string to preserve ID semantics (e.g. '9330001.01' not 9330001.01 float)
    out["ct_id"] = out["ct_id"].astype(str)
    out = out.sort_values(["ct_id", "overlap_fraction"], ascending=[True, False])
    out = out.reset_index(drop=True)
    return out


def main():
    print("Loading local area boundaries...")
    la_gdf = load_local_areas()
    print(f"  {len(la_gdf)} local areas: {sorted(la_gdf['local_area'].tolist())}")

    all_concordance = []
    ct_counts = {}
    unmatched_cts = {}

    for year in [2006, 2011, 2016, 2021]:
        print(f"\nProcessing {year}...")
        ct_gdf = load_vancouver_cts(year)
        print(f"  Loaded {len(ct_gdf)} CTs for Vancouver CMA")

        concordance = build_concordance_for_year(year, ct_gdf, la_gdf)
        print(f"  Concordance rows: {len(concordance)}")

        # Check coverage
        matched_cts = concordance["ct_id"].nunique()
        total_cts = ct_gdf["CTUID"].nunique()
        unmatched = ct_gdf[~ct_gdf["CTUID"].isin(concordance["ct_id"])]["CTUID"].tolist()
        print(f"  CTs matched to at least one local area: {matched_cts}/{total_cts}")
        if unmatched:
            print(f"  UNMATCHED CTs (outside all local areas): {len(unmatched)}")
            print(f"    {unmatched[:10]}")

        ct_counts[year] = {"total": total_cts, "matched": matched_cts}
        unmatched_cts[year] = unmatched

        # Check local area coverage
        covered_areas = concordance["local_area"].nunique()
        print(f"  Local areas with CT coverage: {covered_areas}/22")
        uncovered = [a for a in la_gdf["local_area"].tolist() if a not in concordance["local_area"].values]
        if uncovered:
            print(f"  UNCOVERED local areas: {uncovered}")

        all_concordance.append(concordance)

    # Combine all years
    full_concordance = pd.concat(all_concordance, ignore_index=True)
    full_concordance.to_csv(OUTPUT_CSV, index=False)
    print(f"\nSaved concordance: {OUTPUT_CSV}")
    print(f"Total rows: {len(full_concordance)}")
    print(f"Columns: {full_concordance.columns.tolist()}")

    # Summary table
    print("\n=== Coverage Summary ===")
    for year in [2006, 2011, 2016, 2021]:
        c = ct_counts[year]
        print(f"  {year}: {c['matched']}/{c['total']} CTs matched ({100*c['matched']/c['total']:.1f}%)")

    # Print multi-area CTs (span more than one local area)
    print("\n=== CTs spanning multiple local areas ===")
    multi = full_concordance.groupby(["ct_id", "census_year"]).size()
    multi_ct = multi[multi > 1]
    print(f"Total (ct, year) pairs spanning >1 local area: {len(multi_ct)}")
    if len(multi_ct) > 0:
        sample = multi_ct.reset_index().rename(columns={0: "num_areas"})
        print(sample.groupby("census_year")["num_areas"].describe().to_string())

    return full_concordance, ct_counts, unmatched_cts


if __name__ == "__main__":
    concordance, ct_counts, unmatched_cts = main()
    print("\nDone.")
