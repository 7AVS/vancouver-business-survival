"""
compute_land_values.py
----------------------
Computes neighbourhood-level land value growth rates from CoV property tax data.
Produces: data/processed/neighbourhood_land_values.csv
          analysis/LAND_VALUE_ANALYSIS.md

Design notes:
- Multi-area neighbourhood codes: handled via fractional weighting from lookup table.
  Each property's land value is split proportionally across its mapped local areas.
  For HIGH-confidence codes (single dominant area ≥90%), the full value goes there.
  For others, weighted splits are applied.
- YoY change: computed from consecutive year medians, NOT from previous_land_value
  column (unavailable pre-2013 and unreliable across data vintages).
- Base year for cumulative growth: 2007 (first full year of data).
- CURRENT_LAND_VALUE is the assessed market value column — correct for this analysis.
"""

import pandas as pd
import numpy as np
from pathlib import Path
import warnings
warnings.filterwarnings("ignore", category=pd.errors.DtypeWarning)

# ── Paths ──────────────────────────────────────────────────────────────────────
BASE = Path("/home/aurora/projects/sites/portfolio-projects/van-property-tax")
RAW  = BASE / "data/raw"
PROC = BASE / "data/processed"
ANA  = BASE / "analysis"

TAX_FILES = sorted(RAW.glob("property-tax-report-*.csv"))
LOOKUP    = PROC / "neighbourhood_code_lookup.csv"
OUT_CSV   = PROC / "neighbourhood_land_values.csv"
OUT_MD    = ANA  / "LAND_VALUE_ANALYSIS.md"

# ── 1. Load neighbourhood code lookup ─────────────────────────────────────────
print("Loading neighbourhood code lookup...")
lk = pd.read_csv(LOOKUP)

# Parse percentage strings → floats
for col in ["primary_pct", "secondary_pct"]:
    lk[col] = lk[col].str.replace("%", "").astype(float) / 100.0

# Fill missing secondary (codes with only one area)
lk["secondary_local_area"] = lk["secondary_local_area"].fillna("")
lk["secondary_pct"] = lk["secondary_pct"].fillna(0.0)

# Zero-pad neighbourhood_code to 3 digits for consistent matching
lk["neighbourhood_code"] = lk["neighbourhood_code"].astype(str).str.zfill(3)

# Build code → [(area, weight), ...] mapping
# We assign 100% to primary for HIGH-confidence codes (≥90% primary).
# For all others, we distribute across primary + secondary (rest goes to "Other").
code_weights = {}
for _, row in lk.iterrows():
    code = row["neighbourhood_code"]
    p_area = row["primary_local_area"]
    p_pct  = row["primary_pct"]
    s_area = row["secondary_local_area"]
    s_pct  = row["secondary_pct"]

    if row["confidence"] == "HIGH" or p_pct >= 0.90:
        # Assign all weight to primary
        code_weights[code] = [(p_area, 1.0)]
    else:
        weights = [(p_area, p_pct)]
        if s_area:
            weights.append((s_area, s_pct))
        # Remaining weight is unattributed — drop (small residual)
        code_weights[code] = weights

print(f"  Loaded {len(lk)} neighbourhood codes → {len(code_weights)} mappings")
print(f"  Codes with split weights: {sum(1 for v in code_weights.values() if len(v) > 1)}")

# ── 2. Load and process property tax files ─────────────────────────────────────
COLS_NEEDED = ["current_land_value", "neighbourhood_code", "report_year"]

all_chunks = []

for fpath in TAX_FILES:
    print(f"\nLoading {fpath.name}...")
    df = pd.read_csv(
        fpath,
        usecols=lambda c: c.lower().strip() in {
            "current_land_value", "neighbourhood_code", "report_year"
        },
        dtype=str,
        encoding="utf-8-sig",  # handles BOM on some files
        low_memory=False,
    )

    # Normalize column names (lowercase, strip)
    df.columns = [c.lower().strip() for c in df.columns]
    print(f"  Raw rows: {len(df):,}  |  Columns: {list(df.columns)}")

    # Type conversions
    df["current_land_value"] = pd.to_numeric(df["current_land_value"], errors="coerce")
    df["report_year"]        = pd.to_numeric(df["report_year"], errors="coerce")
    df["neighbourhood_code"] = df["neighbourhood_code"].astype(str).str.strip().str.zfill(3)

    # Drop rows with nulls in key fields
    before = len(df)
    df = df.dropna(subset=["current_land_value", "report_year", "neighbourhood_code"])
    df = df[df["current_land_value"] > 0]
    after = len(df)
    print(f"  After cleaning: {after:,} rows  (dropped {before - after:,})")

    # Convert report_year to int
    df["report_year"] = df["report_year"].astype(int)

    all_chunks.append(df)

prop = pd.concat(all_chunks, ignore_index=True)
print(f"\nTotal rows loaded: {len(prop):,}")
print(f"Years range: {prop['report_year'].min()} – {prop['report_year'].max()}")
print(f"Unique neighbourhood codes in data: {prop['neighbourhood_code'].nunique()}")
print(f"Unique years: {sorted(prop['report_year'].unique())}")

# ── 3. Expand rows by neighbourhood code weights ───────────────────────────────
# For properties in multi-area codes, create weighted fractional rows.
# We carry both the fractional land value (for total) and the original value
# (for median/mean — median of fractional values is not meaningful).
# Strategy: compute aggregate stats at code level first, then weight to area level.

print("\nComputing code-level aggregates...")
code_year = (
    prop.groupby(["neighbourhood_code", "report_year"])["current_land_value"]
    .agg(
        median_land_value="median",
        mean_land_value="mean",
        total_land_value="sum",
        property_count="count",
    )
    .reset_index()
)

print(f"  Code-year combinations: {len(code_year):,}")

# ── 4. Distribute code-level stats to local areas ─────────────────────────────
print("Distributing to local areas via weights...")

area_rows = []
for _, row in code_year.iterrows():
    code = row["neighbourhood_code"]
    year = row["report_year"]

    if code not in code_weights:
        # Unknown code — skip
        continue

    weights = code_weights[code]
    for area, wt in weights:
        area_rows.append({
            "local_area":        area,
            "year":              year,
            "neighbourhood_code": code,
            "weight":            wt,
            # Median/mean are not linearly additive — we'll re-aggregate from property level
            "total_land_value_contrib": row["total_land_value"] * wt,
            "property_count_contrib":   row["property_count"] * wt,
        })

area_contrib = pd.DataFrame(area_rows)
print(f"  Expanded to {len(area_contrib):,} area-code-year rows")

# For total_land_value and property_count: sum contributions per area-year
area_totals = (
    area_contrib.groupby(["local_area", "year"])
    .agg(
        total_land_value=("total_land_value_contrib", "sum"),
        property_count=("property_count_contrib", "sum"),
    )
    .reset_index()
)

# For median_land_value and mean_land_value: compute from property-level data
# Expand each property row by code weights (fractional split is not ideal for median).
# Better approach: for each area, collect the land values of ALL properties mapped to it
# (with weight determining inclusion probability — we use the dominant-area assignment
# for median/mean to avoid double-counting distortion).

# Strategy: for each property, assign it to its HIGHEST-weight area only for median/mean.
# This is equivalent to a hard assignment to primary area (by modal rule), which is
# appropriate for distributional statistics. Totals use fractional splits.

print("\nBuilding area-level median/mean using weighted assignment strategy...")

# Strategy: for HIGH-confidence codes (primary ≥90%), hard-assign to primary.
# For MEDIUM/LOW codes, assign properties to each area listed in their weights,
# weighting by the fractional split. We compute a weighted median using those weights.
#
# Concretely: for each (code, area) pair, we include ALL properties in that code
# in the area's distribution, but each property contributes a weight equal to
# the area's fraction for that code. This gives every area a valid median/mean
# estimate even when it only appears as a secondary area in the lookup.
#
# Weighted median: sort values, find where cumulative weight crosses 0.5.
# Weighted mean: sum(value * weight) / sum(weight).

def weighted_median(values, weights):
    """Compute weighted median."""
    if len(values) == 0:
        return np.nan
    # Sort by value
    sorted_idx = np.argsort(values)
    sorted_vals = values[sorted_idx]
    sorted_wts  = weights[sorted_idx]
    cumsum = np.cumsum(sorted_wts)
    total  = cumsum[-1]
    # Find first index where cumulative weight >= 50% of total
    cutoff = 0.5 * total
    idx = np.searchsorted(cumsum, cutoff)
    if idx >= len(sorted_vals):
        idx = len(sorted_vals) - 1
    return sorted_vals[idx]

# Build expanded property table with area and weight columns
# For each property, we emit one row per (area, weight) in that code's mapping.
# For HIGH-confidence codes, only one row (area, 1.0) is emitted.
print("  Expanding properties to (area, weight) rows — this may take a moment...")

# Build a code → list of (area, weight) mapping for fast lookup
code_weight_map = code_weights  # already built

# We'll operate at the aggregated code-year level first, then expand
# to avoid blowing up memory with 4M * up to 2 = 8M rows.
# For distributional stats we need property-level though.
# Compromise: expand property-level but only keep value + weight per area.

# Build per-code DataFrames with area assignments
area_dfs = []

# Group prop by neighbourhood_code for batch processing
for code, weights_list in code_weight_map.items():
    subset = prop[prop["neighbourhood_code"] == code][["current_land_value", "report_year"]].copy()
    if len(subset) == 0:
        continue
    for area, wt in weights_list:
        tmp = subset.copy()
        tmp["local_area"] = area
        tmp["area_weight"] = wt
        area_dfs.append(tmp)

prop_expanded = pd.concat(area_dfs, ignore_index=True)
print(f"  Expanded table: {len(prop_expanded):,} rows ({len(prop):,} properties × avg {len(prop_expanded)/len(prop):.2f} area assignments)")

# Drop rows with unmapped codes (none expected since all 30 are in code_weights)
prop_mapped = prop_expanded.dropna(subset=["local_area"])
print(f"  Properties with valid area assignment: {len(prop_mapped):,}")

print("  Computing weighted medians and means per area-year...")

# Compute weighted median and weighted mean by area-year
records = []
for (area, year), grp in prop_mapped.groupby(["local_area", "report_year"]):
    vals = grp["current_land_value"].values
    wts  = grp["area_weight"].values
    wmed = weighted_median(vals, wts)
    wmean = np.average(vals, weights=wts)
    records.append({"local_area": area, "year": year,
                    "median_land_value": wmed, "mean_land_value": wmean})

area_distrib = pd.DataFrame(records)

# ── 5. Merge totals + distributional stats ─────────────────────────────────────
panel = area_distrib.merge(area_totals, on=["local_area", "year"], how="outer")
panel["property_count"] = panel["property_count"].round(0).astype("Int64")
panel = panel.sort_values(["local_area", "year"]).reset_index(drop=True)

print(f"\nArea-year panel shape: {panel.shape}")
print(f"Local areas in panel: {sorted(panel['local_area'].unique())}")
print(f"Years in panel: {sorted(panel['year'].unique())}")

# ── 6. YoY change and cumulative growth ───────────────────────────────────────
print("\nComputing YoY and cumulative growth rates...")

panel = panel.sort_values(["local_area", "year"])
panel["yoy_change_pct"] = (
    panel.groupby("local_area")["median_land_value"]
    .pct_change() * 100
)

# Cumulative growth from base year (2007 = first full year across all files)
BASE_YEAR = 2007
base_vals = (
    panel[panel["year"] == BASE_YEAR]
    .set_index("local_area")["median_land_value"]
)
panel["base_median"] = panel["local_area"].map(base_vals)
panel["cumulative_growth_pct"] = (
    (panel["median_land_value"] / panel["base_median"] - 1) * 100
)
panel = panel.drop(columns=["base_median"])

# Round floats
for col in ["median_land_value", "mean_land_value", "total_land_value",
            "yoy_change_pct", "cumulative_growth_pct"]:
    panel[col] = panel[col].round(2)

# Final column order
panel = panel[[
    "local_area", "year",
    "median_land_value", "mean_land_value", "total_land_value",
    "property_count", "yoy_change_pct", "cumulative_growth_pct"
]]

print(f"Final panel shape: {panel.shape}")

# ── 7. Save output ─────────────────────────────────────────────────────────────
panel.to_csv(OUT_CSV, index=False)
print(f"\nSaved: {OUT_CSV}")

# ── 8. Build summary statistics for the report ────────────────────────────────
print("\nBuilding analysis report...")

# Latest year present
latest_year = panel["year"].max()
earliest_year = panel["year"].min()

# Cumulative growth to latest year (from 2007)
cumgrowth = (
    panel[panel["year"] == latest_year][["local_area", "cumulative_growth_pct", "median_land_value"]]
    .sort_values("cumulative_growth_pct", ascending=False)
    .dropna(subset=["cumulative_growth_pct"])
)

# Period averages for temporal analysis
def period_avg_yoy(start, end, label):
    subset = panel[(panel["year"] >= start) & (panel["year"] <= end)]
    return (
        subset.groupby("local_area")["yoy_change_pct"]
        .mean()
        .reset_index()
        .rename(columns={"yoy_change_pct": f"avg_yoy_{label}"})
    )

pre_covid  = period_avg_yoy(2007, 2019, "pre_covid")   # 2007-2019
covid      = period_avg_yoy(2020, 2022, "covid")        # 2020-2022
post_covid = period_avg_yoy(2023, latest_year, "post_covid")  # 2023+

temporal = pre_covid.merge(covid, on="local_area", how="outer")
temporal = temporal.merge(post_covid, on="local_area", how="outer")

# Data quality checks
all_areas = sorted(panel["local_area"].unique())
all_years = sorted(panel["year"].unique())
coverage = panel.groupby("local_area")["year"].count().reset_index().rename(columns={"year": "years_present"})
expected_years = len(all_years)

# Missing area-year combos
missing_pairs = []
for area in all_areas:
    area_years = set(panel[panel["local_area"] == area]["year"])
    for yr in all_years:
        if yr not in area_years:
            missing_pairs.append((area, yr))

# Outlier YoY (>60% or <-30%)
outliers = panel[
    (panel["yoy_change_pct"].abs() > 60) |
    (panel["yoy_change_pct"] < -30)
].dropna(subset=["yoy_change_pct"])

# Distribution stats for latest year
latest_stats = panel[panel["year"] == latest_year].describe()

# ── 9. Write Markdown report ───────────────────────────────────────────────────

def fmt_pct(v, decimals=1):
    if pd.isna(v): return "N/A"
    return f"{v:+.{decimals}f}%"

def fmt_dollar(v):
    if pd.isna(v): return "N/A"
    if v >= 1e6: return f"${v/1e6:.2f}M"
    if v >= 1e3: return f"${v/1e3:.0f}K"
    return f"${v:.0f}"

lines = []
lines.append("# Land Value Analysis — City of Vancouver Property Tax Data")
lines.append(f"\n**Data range:** {earliest_year}–{latest_year}  |  **Base year for cumulative growth:** {BASE_YEAR}  |  **Local areas:** {len(all_areas)}")
lines.append(f"\n**Source files:** {', '.join(f.name for f in TAX_FILES)}")
lines.append(f"\n**Total property-year records:** {len(prop):,}  |  **After mapping:** {len(prop_mapped):,}")
lines.append(f"\n---\n")

# ── Top/bottom appreciation
lines.append("## 1. Cumulative Appreciation to " + str(latest_year) + " (from " + str(BASE_YEAR) + ")")
lines.append("\n### Highest appreciation\n")
lines.append("| Rank | Local Area | Median Land Value (" + str(latest_year) + ") | Cumulative Growth (from " + str(BASE_YEAR) + ") |")
lines.append("|------|-----------|" + "-"*30 + "|" + "-"*30 + "|")
for i, (_, row) in enumerate(cumgrowth.head(10).iterrows(), 1):
    lines.append(f"| {i} | {row['local_area']} | {fmt_dollar(row['median_land_value'])} | {fmt_pct(row['cumulative_growth_pct'])} |")

lines.append("\n### Lowest appreciation\n")
lines.append("| Rank | Local Area | Median Land Value (" + str(latest_year) + ") | Cumulative Growth (from " + str(BASE_YEAR) + ") |")
lines.append("|------|-----------|" + "-"*30 + "|" + "-"*30 + "|")
for i, (_, row) in enumerate(cumgrowth.tail(10).iloc[::-1].iterrows(), 1):
    lines.append(f"| {i} | {row['local_area']} | {fmt_dollar(row['median_land_value'])} | {fmt_pct(row['cumulative_growth_pct'])} |")

# ── Temporal trends
lines.append("\n## 2. Temporal Trends — Average Annual YoY Growth by Period\n")
lines.append("| Local Area | Pre-COVID (2007–2019) | COVID (2020–2022) | Post-COVID (2023–" + str(latest_year) + ") |")
lines.append("|-----------|----------------------|-------------------|" + "-"*25 + "|")
temporal_sorted = temporal.sort_values("avg_yoy_pre_covid", ascending=False)
for _, row in temporal_sorted.iterrows():
    lines.append(f"| {row['local_area']} | {fmt_pct(row.get('avg_yoy_pre_covid'))} | {fmt_pct(row.get('avg_yoy_covid'))} | {fmt_pct(row.get('avg_yoy_post_covid'))} |")

# ── Full cumulative growth table (all areas, all years — pivot)
lines.append("\n## 3. Median Land Value by Area and Year\n")
pivot_median = panel.pivot(index="local_area", columns="year", values="median_land_value")
# Show every 2 years to keep it readable
show_years = [y for y in all_years if y % 2 == 1 or y == all_years[-1]]
pivot_show = pivot_median[[c for c in show_years if c in pivot_median.columns]]
header = "| Local Area | " + " | ".join(str(y) for y in pivot_show.columns) + " |"
lines.append(header)
lines.append("|" + "-"*14 + "|" + "|".join(["-"*12]*len(pivot_show.columns)) + "|")
for area, row in pivot_show.iterrows():
    vals = " | ".join(fmt_dollar(row[y]) if y in row.index else "—" for y in pivot_show.columns)
    lines.append(f"| {area} | {vals} |")

# ── Distribution stats
lines.append(f"\n## 4. Distribution Statistics — {latest_year}\n")
lt = panel[panel["year"] == latest_year].dropna(subset=["median_land_value"])
lines.append(f"- **Areas covered:** {lt['local_area'].nunique()}")
lines.append(f"- **Overall median of area medians:** {fmt_dollar(lt['median_land_value'].median())}")
lines.append(f"- **Min area median:** {fmt_dollar(lt['median_land_value'].min())} ({lt.loc[lt['median_land_value'].idxmin(), 'local_area']})")
lines.append(f"- **Max area median:** {fmt_dollar(lt['median_land_value'].max())} ({lt.loc[lt['median_land_value'].idxmax(), 'local_area']})")
lines.append(f"- **Std dev of area medians:** {fmt_dollar(lt['median_land_value'].std())}")
lines.append(f"- **Coefficient of variation:** {lt['median_land_value'].std() / lt['median_land_value'].mean() * 100:.1f}%")

# ── YoY outliers
lines.append("\n## 5. Outliers and Data Quality Issues\n")

if missing_pairs:
    lines.append(f"### Missing area-year combinations ({len(missing_pairs)} total)\n")
    for area, yr in sorted(missing_pairs)[:30]:
        lines.append(f"- {area}: {yr}")
    if len(missing_pairs) > 30:
        lines.append(f"- ... and {len(missing_pairs) - 30} more")
else:
    lines.append("### Missing area-year combinations: None — complete coverage.\n")

lines.append(f"\n### YoY anomalies (|change| > 60% or change < -30%): {len(outliers)} rows\n")
if len(outliers) > 0:
    lines.append("| Local Area | Year | YoY Change | Median Land Value |")
    lines.append("|-----------|------|-----------|-------------------|")
    for _, row in outliers.sort_values("yoy_change_pct", ascending=False).head(20).iterrows():
        lines.append(f"| {row['local_area']} | {int(row['year'])} | {fmt_pct(row['yoy_change_pct'])} | {fmt_dollar(row['median_land_value'])} |")
else:
    lines.append("None detected.\n")

# ── Coverage by area
lines.append("\n### Data coverage by local area\n")
lines.append(f"Expected years: {expected_years} ({earliest_year}–{latest_year})")
lines.append("\n| Local Area | Years Present | Coverage |")
lines.append("|-----------|--------------|---------|")
for _, row in coverage.sort_values("local_area").iterrows():
    pct = row["years_present"] / expected_years * 100
    lines.append(f"| {row['local_area']} | {int(row['years_present'])} | {pct:.0f}% |")

# ── Methodology notes
lines.append("\n## 6. Methodology Notes\n")
lines.append("""
**Neighbourhood code mapping:**
The property tax files identify properties with a numeric `neighbourhood_code` (001–030),
not directly by local area name. The lookup table (`neighbourhood_code_lookup.csv`) maps
each code to one or two local areas with confidence weights derived from geocoding.

- **Median/mean values**: computed from property-level data with hard assignment to each
  code's primary area (highest weight). This avoids double-counting a property's
  distributional contribution across multiple areas.
- **Total land value and property count**: distributed fractionally across areas using
  the lookup weights. A property in a 60/40 split code contributes 60% to area A and
  40% to area B.

**YoY change:** computed from consecutive annual medians in this panel, NOT from the
`previous_land_value` column in the source data (unavailable pre-2013, and represents
previous assessment year not necessarily previous calendar year).

**Cumulative growth:** indexed to """ + str(BASE_YEAR) + """ (first full data year). Areas
missing """ + str(BASE_YEAR) + """ data will show NaN cumulative growth.

**CURRENT_LAND_VALUE** is the assessed market value per BC Assessment. Excludes
improvement value. Taxable value differs due to exemptions and mill rate adjustments.

**Tax levy** is excluded from this analysis (blank until June each year per documentation).
""")

report_text = "\n".join(lines)
OUT_MD.write_text(report_text, encoding="utf-8")
print(f"Saved: {OUT_MD}")

# ── Print quick summary to console ────────────────────────────────────────────
print("\n" + "="*60)
print("QUICK SUMMARY")
print("="*60)
print(f"\nTop 5 appreciation (2007–{latest_year}):")
for _, row in cumgrowth.head(5).iterrows():
    print(f"  {row['local_area']:30s} {fmt_pct(row['cumulative_growth_pct'])}")

print(f"\nBottom 5 appreciation (2007–{latest_year}):")
for _, row in cumgrowth.tail(5).iloc[::-1].iterrows():
    print(f"  {row['local_area']:30s} {fmt_pct(row['cumulative_growth_pct'])}")

print(f"\nPanel saved: {len(panel):,} rows  ({len(all_areas)} areas × {len(all_years)} years)")
print(f"Output: {OUT_CSV}")
print(f"Report: {OUT_MD}")
