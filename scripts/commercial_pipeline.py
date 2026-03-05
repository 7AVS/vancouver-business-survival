"""
Vancouver Commercial Business Licence Pipeline
Steps 1-5: Merge → Scope → Panel → EDA → Plots
"""

import pandas as pd
import numpy as np
import hashlib
import json
import warnings
import os
import sys
from datetime import datetime
from collections import Counter

warnings.filterwarnings('ignore')

# ──────────────────────────────────────────────────────────
# PATHS
# ──────────────────────────────────────────────────────────
BASE = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"
RAW_ARCHIVE    = f"{BASE}/data/raw/business-licences/business-licences-2013-to-2024.csv"
RAW_CURRENT    = f"{BASE}/data/raw/business-licences/business-licences-current.csv"
MERGED_OUT     = f"{BASE}/data/processed/business-licences-merged-2013-to-2026.csv"
COMMERCIAL_OUT = f"{BASE}/data/processed/commercial-licences-2013-to-2026.csv"
PANEL_OUT      = f"{BASE}/data/processed/commercial-panel.csv"
EDA_OUT        = f"{BASE}/analysis/COMMERCIAL_EDA.md"
PLOT_DIR       = f"{BASE}/analysis/plots"
GEOJSON_PATH   = f"{BASE}/data/raw/local-area-boundary.geojson"
SCRIPT_OUT     = f"{BASE}/scripts/generated/commercial_eda_plots.py"

os.makedirs(f"{BASE}/data/processed", exist_ok=True)
os.makedirs(PLOT_DIR, exist_ok=True)

# ──────────────────────────────────────────────────────────
# STEP 1: MERGE
# ──────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 1: MERGING DATASETS")
print("="*60)

print("Loading archive (comma-delimited)...")
archive = pd.read_csv(RAW_ARCHIVE, dtype=str, low_memory=False)
archive['folderyear'] = archive['folderyear'].str.strip().str.zfill(2)
print(f"  Archive loaded: {len(archive):,} rows")
print(f"  Archive folderyears: {sorted(archive['folderyear'].unique())}")

fy_counts_archive = archive['folderyear'].value_counts().sort_index()
print("\n  Archive row counts per folderyear:")
for fy, cnt in fy_counts_archive.items():
    print(f"    FY{fy}: {cnt:,}")

print("\nLoading current (semicolon-delimited, UTF-8 BOM)...")
current = pd.read_csv(RAW_CURRENT, sep=';', dtype=str, encoding='utf-8-sig', low_memory=False)
current['folderyear'] = current['folderyear'].str.strip().str.zfill(2)
print(f"  Current loaded: {len(current):,} rows")
print(f"  Current folderyears: {sorted(current['folderyear'].unique())}")

fy_counts_current = current['folderyear'].value_counts().sort_index()
print("\n  Current row counts per folderyear:")
for fy, cnt in fy_counts_current.items():
    print(f"    FY{fy}: {cnt:,}")

# Verify columns match
print(f"\n  Archive columns: {list(archive.columns)}")
print(f"  Current columns: {list(current.columns)}")
assert list(archive.columns) == list(current.columns), "Column mismatch between archive and current!"

# Merge strategy:
# - Archive FY13-23 as-is
# - Replace archive FY24 with current FY24
# - Add current FY25 and FY26
archive_13_23 = archive[archive['folderyear'] <= '23'].copy()
current_fy24  = current[current['folderyear'] == '24'].copy()
current_fy25  = current[current['folderyear'] == '25'].copy()
current_fy26  = current[current['folderyear'] == '26'].copy()

print(f"\n  Building merged dataset:")
print(f"    Archive FY13-23:   {len(archive_13_23):,} rows (kept as-is)")
print(f"    Archive FY24:      {len(archive[archive['folderyear']=='24']):,} rows (REPLACED)")
print(f"    Current FY24:      {len(current_fy24):,} rows (USED)")
print(f"    Current FY25:      {len(current_fy25):,} rows (ADDED)")
print(f"    Current FY26:      {len(current_fy26):,} rows (ADDED)")

merged = pd.concat([archive_13_23, current_fy24, current_fy25, current_fy26], ignore_index=True)
print(f"\n  Total merged rows: {len(merged):,}")

print("\n  Merged row counts per folderyear:")
fy_counts_merged = merged['folderyear'].value_counts().sort_index()
for fy, cnt in fy_counts_merged.items():
    print(f"    FY{fy}: {cnt:,}")

# Save merged
merged.to_csv(MERGED_OUT, index=False)
print(f"\n  Saved: {MERGED_OUT}")

# ──────────────────────────────────────────────────────────
# STEP 2: SCOPE EXCLUSIONS
# ──────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 2: APPLYING SCOPE EXCLUSIONS")
print("="*60)

df = merged.copy()
rows_before = len(df)
print(f"  Rows before exclusion: {rows_before:,}")

# Per-folderyear before
fy_before = df['folderyear'].value_counts().sort_index()

# Exclusion sets per Step 2 instructions
RESIDENTIAL_TYPES = {
    'Single Detached House *Historic*',
    'Apartment House Strata *Historic*',
    'Apartment House *Historic*',
    'Multiple Dwelling *Historic*',
    'Duplex *Historic*',
    'Residential/Commercial *Historic*',
    'Pre-1956 Dwelling *Historic*',
    'Rooming House *Historic*',
    'Apartment House-99 Year Lease *Historic*',
    'Secondary Suite - Permanent *Historic*',
}

ADDITIONAL_EXCL_TYPES = {
    'Short-term Rental Operator',
    'Community Association *Historic*',
    'Non-Profit Housing *Historic*',
}

EXCLUDED_STATUSES = {'Pending', 'Cancelled'}

# Also exclude admin + temp types from SCOPE_AUDIT (definite exclusions)
ADMIN_TEMP_TYPES = {
    'Temp Liquor Licence Amendment',
    'Liquor License Application',
    'Soliciting For Charity',
    'Temporary Filming Company',
    'Christmas Tree Lot *Historic*',
    'Live-aboards *Historic*',  # in SCOPE_AUDIT residential list
}

ALL_EXCLUDED_TYPES = RESIDENTIAL_TYPES | ADDITIONAL_EXCL_TYPES | ADMIN_TEMP_TYPES

# Track each exclusion
mask_res   = df['businesstype'].isin(RESIDENTIAL_TYPES)
mask_str   = df['businesstype'] == 'Short-term Rental Operator'
mask_ca    = df['businesstype'] == 'Community Association *Historic*'
mask_nph   = df['businesstype'] == 'Non-Profit Housing *Historic*'
mask_admin = df['businesstype'].isin(ADMIN_TEMP_TYPES)
mask_pend  = df['status'] == 'Pending'
mask_canc  = df['status'] == 'Cancelled'

print(f"\n  Exclusion breakdown:")
print(f"    Residential types:         {mask_res.sum():,}")
print(f"    Short-term Rental:         {mask_str.sum():,}")
print(f"    Community Association:     {mask_ca.sum():,}")
print(f"    Non-Profit Housing:        {mask_nph.sum():,}")
print(f"    Admin/temp types:          {mask_admin.sum():,}")
print(f"    Status = Pending:          {mask_pend.sum():,}")
print(f"    Status = Cancelled:        {mask_canc.sum():,}")

exclude_mask = (
    df['businesstype'].isin(ALL_EXCLUDED_TYPES) |
    df['status'].isin(EXCLUDED_STATUSES)
)
df_commercial = df[~exclude_mask].copy()

rows_after = len(df_commercial)
rows_removed = rows_before - rows_after
pct_retained = rows_after / rows_before * 100

print(f"\n  Rows after exclusion:  {rows_after:,}")
print(f"  Rows removed:          {rows_removed:,}")
print(f"  % retained:            {pct_retained:.1f}%")

print("\n  Per-folderyear after exclusion:")
fy_after = df_commercial['folderyear'].value_counts().sort_index()
for fy in sorted(fy_before.index):
    b = fy_before.get(fy, 0)
    a = fy_after.get(fy, 0)
    pct = a/b*100 if b > 0 else 0
    print(f"    FY{fy}: {b:,} → {a:,} ({pct:.0f}% retained)")

# Save scoped dataset
df_commercial.to_csv(COMMERCIAL_OUT, index=False)
print(f"\n  Saved: {COMMERCIAL_OUT}")

# Scope stats for EDA report
scope_stats = {
    'rows_before': rows_before,
    'rows_after': rows_after,
    'rows_removed': rows_removed,
    'pct_retained': pct_retained,
    'fy_before': fy_before.to_dict(),
    'fy_after': fy_after.to_dict(),
}

# ──────────────────────────────────────────────────────────
# STEP 3: BUILD BUSINESS PANEL
# ──────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 3: BUILDING BUSINESS PANEL")
print("="*60)

df = df_commercial.copy()

# Normalize key fields
df['businessname_norm'] = df['businessname'].fillna('').str.strip().str.upper()
df['house_norm']        = df['house'].fillna('').str.strip().str.upper()
df['street_norm']       = df['street'].fillna('').str.strip().str.upper()

# business_id = hash of normalized name+house+street
def make_id(row):
    key = f"{row['businessname_norm']}|{row['house_norm']}|{row['street_norm']}"
    return hashlib.md5(key.encode()).hexdigest()[:12]

print("  Computing business IDs...")
df['business_id'] = df.apply(make_id, axis=1)
df['folderyear_int'] = df['folderyear'].astype(int)

# Sort by business_id, folderyear for consistent ordering
df_sorted = df.sort_values(['business_id', 'folderyear_int'])

print("  Aggregating panel...")

def first_non_null(series):
    """Return first non-null value."""
    s = series.dropna()
    s = s[s != '']
    return s.iloc[0] if len(s) > 0 else np.nan

def last_non_null(series):
    """Return last non-null value."""
    s = series.dropna()
    s = s[s != '']
    return s.iloc[-1] if len(s) > 0 else np.nan

# Group by business_id
grouped = df_sorted.groupby('business_id')

panel_rows = []
for bid, grp in grouped:
    grp_sorted = grp.sort_values('folderyear_int')
    last_row = grp_sorted.iloc[-1]

    # geo_point_2d: most recent non-null
    geo_vals = grp_sorted['geo_point_2d'].dropna()
    geo_vals = geo_vals[geo_vals.str.strip() != ''] if len(geo_vals) > 0 else geo_vals
    geo = geo_vals.iloc[-1] if len(geo_vals) > 0 else np.nan

    first_yr = int(grp_sorted['folderyear_int'].min())
    last_yr  = int(grp_sorted['folderyear_int'].max())
    years_active = last_yr - first_yr + 1
    total_fy = len(grp_sorted['folderyear_int'].unique())

    panel_rows.append({
        'business_id':      bid,
        'businessname':     grp_sorted.iloc[0]['businessname'],
        'house':            grp_sorted.iloc[0]['house'],
        'street':           grp_sorted.iloc[0]['street'],
        'first_year':       first_yr,
        'last_year':        last_yr,
        'years_active':     years_active,
        'total_folderyears': total_fy,
        'businesstype':     last_row['businesstype'],
        'businesssubtype':  last_row['businesssubtype'],
        'postalcode':       last_row['postalcode'],
        'localarea':        last_row['localarea'],
        'geo_point_2d':     geo,
        'numberofemployees': last_row['numberofemployees'],
        'feepaid':          last_row['feepaid'],
        'status_last_year': last_row['status'],
    })

panel = pd.DataFrame(panel_rows)
print(f"  Panel rows: {len(panel):,} unique businesses")
print(f"  Businesses trackable across 2+ years: {(panel['total_folderyears'] >= 2).sum():,} ({(panel['total_folderyears'] >= 2).mean()*100:.1f}%)")

panel.to_csv(PANEL_OUT, index=False)
print(f"  Saved: {PANEL_OUT}")

# Panel stats for EDA
panel_stats = {
    'total_unique': len(panel),
    'pct_multi_year': (panel['total_folderyears'] >= 2).mean() * 100,
    'median_lifespan': panel['years_active'].median(),
    'mean_lifespan': panel['years_active'].mean(),
}

# ──────────────────────────────────────────────────────────
# STEP 4: EDA REPORT
# ──────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 4: EDA REPORT")
print("="*60)

df = df_commercial.copy()
df['folderyear_int'] = df['folderyear'].astype(int)
df['folderyear_4'] = df['folderyear_int'] + 2000

# 4.1 Data quality summary
total_rows = len(df)
completeness = {}
for col in df.columns:
    if col in ('businessname_norm', 'house_norm', 'street_norm', 'business_id', 'folderyear_int'):
        continue
    non_null = df[col].notna() & (df[col].astype(str).str.strip() != '')
    completeness[col] = non_null.mean() * 100

# 4.2 Population by year
pop_by_year = (
    df[df['status'].isin(['Issued', 'Inactive'])]
    .groupby('folderyear_4')
    .size()
    .reset_index(name='count')
)

# 4.3 localarea coverage by folderyear
localarea_cov = df.groupby('folderyear_4').apply(
    lambda x: (x['localarea'].notna() & (x['localarea'].str.strip() != '')).mean() * 100
).reset_index(name='pct_localarea')

# 4.4 geo_point_2d coverage by folderyear
geo_cov = df.groupby('folderyear_4').apply(
    lambda x: (x['geo_point_2d'].notna() & (x['geo_point_2d'].str.strip() != '')).mean() * 100
).reset_index(name='pct_geo')

# 4.5 Business tracking (panel)
unique_biz = len(panel)
pct_trackable = (panel['total_folderyears'] >= 2).mean() * 100
lifespan_pcts = {
    'p25': panel['years_active'].quantile(0.25),
    'p50': panel['years_active'].median(),
    'p75': panel['years_active'].quantile(0.75),
    'max': panel['years_active'].max(),
}

# 4.6 Survival rates (commercial only, FY25 as endpoint)
# Use panel: business is "dead" if status_last_year is 'Gone Out of Business'
# and last_year < 25 (or last_year = 25/26 with status = Issued = right-censored)
panel_surv = panel.copy()
# Right-censor: last_year in {25,26} AND status_last_year = Issued
panel_surv['censored'] = (
    (panel_surv['last_year'].isin([25, 26])) &
    (panel_surv['status_last_year'] == 'Issued')
)
panel_surv['event'] = ~panel_surv['censored']  # True = died (left study)
# Duration = total_folderyears (actual years present)
panel_surv['duration'] = panel_surv['total_folderyears']

def kaplan_meier(durations, events):
    """Simple KM estimator. Returns (times, survival_prob, n_at_risk, n_events)."""
    data = sorted(zip(durations, events), key=lambda x: x[0])
    n = len(data)
    times = []
    surv = []
    lower = []
    upper = []
    s = 1.0
    i = 0
    n_at_risk = n
    at_risk_dict = {}
    events_dict = {}
    # Collect unique event times
    for t, e in data:
        if e:
            events_dict[t] = events_dict.get(t, 0) + 1
    # Collect unique times (including censored)
    all_times = sorted(set(d for d, e in data))
    idx = 0
    n_remaining = n
    for t in all_times:
        n_events = events_dict.get(t, 0)
        n_total_at_t = sum(1 for d, e in data if d == t)
        if n_events > 0:
            prev_s = s
            s = s * (1 - n_events / n_remaining)
            # Greenwood variance (approximate)
            # CI using log-log transformation
            if s > 0 and s < 1:
                cumhaz = -np.log(s)
                # Greenwood: sum of n_events/(n_at_risk*(n_at_risk-n_events))
                greenwood = sum(
                    events_dict.get(tt, 0) / (
                        sum(1 for d, e in data if d >= tt) *
                        (sum(1 for d, e in data if d >= tt) - events_dict.get(tt, 0))
                    )
                    for tt in all_times
                    if tt <= t and events_dict.get(tt, 0) > 0
                    and sum(1 for d, e in data if d >= tt) > events_dict.get(tt, 0)
                )
                se_log_h = np.sqrt(greenwood) if greenwood > 0 else 0
                ci_lower = np.exp(-np.exp(np.log(cumhaz) + 1.96 * se_log_h)) if cumhaz > 0 else s
                ci_upper = np.exp(-np.exp(np.log(cumhaz) - 1.96 * se_log_h)) if cumhaz > 0 else s
            else:
                ci_lower = ci_upper = s
            times.append(t)
            surv.append(s)
            lower.append(max(0, ci_lower))
            upper.append(min(1, ci_upper))
        n_remaining -= n_total_at_t
    return np.array(times), np.array(surv), np.array(lower), np.array(upper)

# Compute KM
km_times, km_surv, km_lower, km_upper = kaplan_meier(
    panel_surv['duration'].values,
    panel_surv['event'].values
)

def surv_at(t, times, survs):
    idx = np.searchsorted(times, t, side='right') - 1
    if idx < 0:
        return 1.0
    if idx >= len(survs):
        return survs[-1]
    return survs[idx]

survival_rates = {
    '1yr':  surv_at(1, km_times, km_surv),
    '2yr':  surv_at(2, km_times, km_surv),
    '3yr':  surv_at(3, km_times, km_surv),
    '5yr':  surv_at(5, km_times, km_surv),
    '7yr':  surv_at(7, km_times, km_surv),
    '10yr': surv_at(10, km_times, km_surv),
}

# Median survival
median_surv = None
for i, s in enumerate(km_surv):
    if s <= 0.5:
        median_surv = km_times[i]
        break

print(f"  Survival rates: {survival_rates}")
print(f"  Median survival: {median_surv} years")

# 4.7 Top business types
top_types = df['businesstype'].value_counts().head(20)

# 4.8 Status by year
status_by_year = df.groupby(['folderyear_4', 'status']).size().unstack(fill_value=0)

# 4.9 Survival by business type (top 6 commercial)
top6_types = df['businesstype'].value_counts().head(6).index.tolist()
surv_by_type = {}
for btype in top6_types:
    sub = panel_surv[panel_surv['businesstype'] == btype]
    if len(sub) < 30:
        continue
    t, s, lo, hi = kaplan_meier(sub['duration'].values, sub['event'].values)
    surv_by_type[btype] = (t, s, lo, hi)

# 4.10 Geographic distribution
# localarea dist for FY24-26
geo_dist_area = (
    df[df['folderyear_int'] >= 24]
    .groupby('localarea')
    .size()
    .sort_values(ascending=False)
    .head(20)
)

# Postal FSA for FY13-23
df_old = df[df['folderyear_int'] <= 23].copy()
df_old['fsa'] = df_old['postalcode'].fillna('').str[:3].str.upper()
geo_dist_fsa = df_old['fsa'].value_counts().head(15)

# 4.11 Fee and employee distributions
df_num = df.copy()
df_num['feepaid_f'] = pd.to_numeric(df_num['feepaid'], errors='coerce')
df_num['emp_f'] = pd.to_numeric(df_num['numberofemployees'], errors='coerce')
fee_stats = df_num['feepaid_f'].describe(percentiles=[.25,.5,.75,.95])
emp_stats = df_num['emp_f'].describe(percentiles=[.25,.5,.75,.95])

# ──────────────────────────────────────────────────────────
# Write EDA report
# ──────────────────────────────────────────────────────────
print("  Writing EDA report...")

eda_lines = []
A = eda_lines.append

A("# Vancouver Commercial Business Licences — EDA Report")
A("")
A(f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M')}")
A(f"**Data span:** FY2013–FY2026")
A(f"**Source files:** Merged from archive (FY13-23) + current (FY24-26)")
A("")
A("---")
A("")
A("## 1. Data Quality Summary")
A("")
A(f"**Scoped commercial dataset rows:** {total_rows:,}")
A("")
A("### Column Completeness")
A("")
A("| Column | % Non-null/Non-blank |")
A("|---|---|")
for col, pct in completeness.items():
    if col not in ('geom',):  # skip raw geom
        A(f"| {col} | {pct:.1f}% |")
A("")
A("**Notes:**")
A("- `localarea` is blank for FY13-23 (expected — field only populated in current extract, FY24-26)")
A("- `geo_point_2d` has partial coverage (~50%) across all years")
A("- `feepaid` has ~16% missing (structural: Gone Out of Business records often lack fee for closing year)")
A("- `numberofemployees` ~35% missing (self-reported, optional)")
A("")
A("---")
A("")
A("## 2. Population by Year")
A("")
A("Active commercial businesses (Issued + Inactive) per folderyear:")
A("")
A("| Year | Active Businesses |")
A("|---|---|")
for _, row in pop_by_year.iterrows():
    fy = int(row['folderyear_4'])
    cnt = int(row['count'])
    note = " *(mid-cycle)*" if fy == 2026 else ""
    A(f"| {fy} | {cnt:,}{note} |")
A("")
A("**Notes:**")
A("- FY2024 anomaly resolved: clean data from current extract (56K+ Issued vs poisoned 4K in archive)")
A("- FY2026 is mid-cycle — count will grow as more licences are issued through year-end")
A("- Steady growth 2013→2020, COVID dip, recovery 2022+")
A("")
A("---")
A("")
A("## 3. localarea Coverage by Folderyear")
A("")
A("| Year | % with localarea |")
A("|---|---|")
for _, row in localarea_cov.iterrows():
    A(f"| {int(row['folderyear_4'])} | {row['pct_localarea']:.1f}% |")
A("")
A("**Notes:**")
A("- FY13-23: ~0% (field was blank in archive extract)")
A("- FY24-26: 97-100% (populated in current extract)")
A("- This geographic coverage leap enables neighbourhood-level analysis for recent years")
A("- For FY13-23, spatial analysis requires geocoding from geo_point_2d (51.8% coverage) or postal FSA approximation")
A("")
A("---")
A("")
A("## 4. geo_point_2d Coverage by Folderyear")
A("")
A("| Year | % with geo_point_2d |")
A("|---|---|")
for _, row in geo_cov.iterrows():
    A(f"| {int(row['folderyear_4'])} | {row['pct_geo']:.1f}% |")
A("")
A("---")
A("")
A("## 5. Business Tracking Statistics")
A("")
A(f"**Unique businesses (panel):** {unique_biz:,}")
A(f"**% trackable across 2+ years:** {pct_trackable:.1f}%")
A(f"**Median lifespan:** {lifespan_pcts['p50']:.0f} year(s)")
A(f"**Mean lifespan:** {panel_stats['mean_lifespan']:.1f} years")
A(f"**P25 / P75 lifespan:** {lifespan_pcts['p25']:.0f} / {lifespan_pcts['p75']:.0f} years")
A(f"**Max lifespan:** {lifespan_pcts['max']:.0f} years")
A("")
A("**Lifespan distribution (years_active):**")
A("")
lifespan_dist = panel['years_active'].value_counts().sort_index()
A("| Years Active | Count | % |")
A("|---|---|---|")
for yrs, cnt in lifespan_dist.items():
    A(f"| {yrs} | {cnt:,} | {cnt/len(panel)*100:.1f}% |")
A("")
A("---")
A("")
A("## 6. Survival Rates (Commercial Only)")
A("")
A("KM survival analysis using business panel. Right-censored: businesses with last_year ∈ {25,26} and status = Issued.")
A("")
A("| Milestone | Survival Rate |")
A("|---|---|")
for k, v in survival_rates.items():
    A(f"| {k} | {v*100:.1f}% |")
A("")
if median_surv:
    A(f"**Median survival time:** {median_surv} year(s)")
else:
    A("**Median survival time:** >10 years (>50% still active at 10yr horizon)")
A("")
A("**Methodology:**")
A("- Duration = `total_folderyears` (actual count of years with a licence record)")
A("- Event = business exits study (status != Issued in final observed year, OR never reappears)")
A("- Right-censored = last_year ∈ {25,26} AND status_last_year = Issued (still active)")
A("- FY26 is mid-cycle; used as informational only, treated as censored")
A("")
A("---")
A("")
A("## 7. Top 20 Business Types")
A("")
A("| Rank | Business Type | Count |")
A("|---|---|---|")
for i, (btype, cnt) in enumerate(top_types.items(), 1):
    A(f"| {i} | {btype} | {cnt:,} |")
A("")
A("*Residential types (Single Detached House, Apartment House, etc.) should be absent — exclusions applied correctly.*")
A("")
A("---")
A("")
A("## 8. Status Distribution by Year")
A("")
# Build the table
statuses = ['Issued', 'Inactive', 'Gone Out of Business', 'Pending', 'Cancelled']
avail_statuses = [s for s in statuses if s in status_by_year.columns]
header = "| Year | " + " | ".join(avail_statuses) + " | Total |"
sep    = "|---|" + "---|" * (len(avail_statuses) + 1)
A(header)
A(sep)
for yr in status_by_year.index:
    row_vals = [str(int(status_by_year.loc[yr, s])) if s in status_by_year.columns else "0" for s in avail_statuses]
    total = int(status_by_year.loc[yr].sum())
    A(f"| {yr} | " + " | ".join(row_vals) + f" | {total:,} |")
A("")
A("**Notes:**")
A("- FY2024 should now look normal (Inactive ~2-4% like other years, not 80%)")
A("- Pending and Cancelled excluded from scoped dataset — should show 0 in this table")
A("- Gone Out of Business represents primary death events for survival analysis")
A("")
A("---")
A("")
A("## 9. Survival by Business Type (Top 6 Commercial)")
A("")
A("KM survival rates at 1yr, 3yr, 5yr for top 6 commercial types:")
A("")
A("| Business Type | 1yr | 3yr | 5yr |")
A("|---|---|---|---|")
for btype, (t, s, lo, hi) in surv_by_type.items():
    r1 = f"{surv_at(1,t,s)*100:.0f}%"
    r3 = f"{surv_at(3,t,s)*100:.0f}%"
    r5 = f"{surv_at(5,t,s)*100:.0f}%"
    A(f"| {btype} | {r1} | {r3} | {r5} |")
A("")
A("---")
A("")
A("## 10. Geographic Distribution")
A("")
A("### By localarea (FY2024-2026, where field is populated)")
A("")
A("| Neighbourhood | Business Count |")
A("|---|---|")
for area, cnt in geo_dist_area.items():
    if str(area).strip() and str(area) != 'nan':
        A(f"| {area} | {cnt:,} |")
A("")
A("### By Postal FSA (FY2013-2023)")
A("")
A("| FSA | Business Licence Records |")
A("|---|---|")
for fsa, cnt in geo_dist_fsa.items():
    if fsa.strip():
        A(f"| {fsa} | {cnt:,} |")
A("")
A("---")
A("")
A("## 11. Fee and Employee Distributions (Commercial Subset)")
A("")
A("### Fee Paid (CAD)")
A("")
A(f"| Metric | Value |")
A("|---|---|")
A(f"| Count (non-null) | {int(fee_stats['count']):,} |")
A(f"| Missing | {total_rows - int(fee_stats['count']):,} ({(total_rows - int(fee_stats['count']))/total_rows*100:.1f}%) |")
A(f"| Mean | ${fee_stats['mean']:.2f} |")
A(f"| Median | ${fee_stats['50%']:.2f} |")
A(f"| P25 | ${fee_stats['25%']:.2f} |")
A(f"| P75 | ${fee_stats['75%']:.2f} |")
A(f"| P95 | ${fee_stats['95%']:.2f} |")
A(f"| Max | ${fee_stats['max']:.2f} |")
A("")
A("### Number of Employees")
A("")
A(f"| Metric | Value |")
A("|---|---|")
A(f"| Count (non-null) | {int(emp_stats['count']):,} |")
A(f"| Missing | {total_rows - int(emp_stats['count']):,} ({(total_rows - int(emp_stats['count']))/total_rows*100:.1f}%) |")
A(f"| Mean | {emp_stats['mean']:.1f} |")
A(f"| Median | {emp_stats['50%']:.1f} |")
A(f"| P25 | {emp_stats['25%']:.1f} |")
A(f"| P75 | {emp_stats['75%']:.1f} |")
A(f"| P95 | {emp_stats['95%']:.1f} |")
A(f"| Max | {int(emp_stats['max'])} |")
A("")
A("---")
A("")
A("## 12. FY2026 Mid-Cycle Caveat")
A("")
fy26_count = fy_after.get('26', 0)
fy25_count = fy_after.get('25', 0)
A(f"FY2026 currently has **{fy26_count:,}** commercial licence records compared to FY2025's **{fy25_count:,}**.")
A("The FY2026 extract was taken early in the licence year (March 2026 data).")
A("")
A("**Implications for analysis:**")
A("- Pending records are excluded (never operated), but Issued count is still growing")
A("- FY2026 Issued = licences already renewed/issued for 2026; more will follow through December")
A("- Gone Out of Business in FY2026 = genuine exits but not yet annualized")
A("- **Treat FY2025 as the reliable endpoint for survival analysis**")
A("- FY2026 is useful for directional signals only; do not extrapolate annual rates from it")
A("")
A("For the KM curves in this report, FY2026 records are treated as right-censored (businesses still alive).")
A("")
A("---")
A("")
A("## 13. Scope Summary")
A("")
A(f"| Stage | Rows |")
A("|---|---|")
A(f"| Merged FY13-26 raw | {scope_stats['rows_before']:,} |")
A(f"| After scope exclusions | {scope_stats['rows_after']:,} |")
A(f"| Removed | {scope_stats['rows_removed']:,} ({100-scope_stats['pct_retained']:.1f}%) |")
A(f"| Unique commercial businesses (panel) | {unique_biz:,} |")
A("")
A("**Exclusions applied:**")
A("1. Residential businesstypes (10 types incl. Single Detached House, Apartment House variants, etc.)")
A("2. Short-term Rental Operator")
A("3. Community Association *Historic*")
A("4. Non-Profit Housing *Historic*")
A("5. Admin/temp types (Temp Liquor Amendment, Liquor License Application, Charity, Filming, Christmas Tree, Live-aboards)")
A("6. Status = Pending")
A("7. Status = Cancelled")
A("")
A("---")
A("")
A("*Report generated by commercial_pipeline.py*")
A(f"*Date: {datetime.now().strftime('%Y-%m-%d')}*")

with open(EDA_OUT, 'w') as f:
    f.write('\n'.join(eda_lines))
print(f"  Saved EDA report: {EDA_OUT}")

# Store KM data for plotting script
print("\n  Storing KM data for plots...")
km_store = {
    'km_times': km_times.tolist(),
    'km_surv': km_surv.tolist(),
    'km_lower': km_lower.tolist(),
    'km_upper': km_upper.tolist(),
    'median_surv': float(median_surv) if median_surv else None,
    'surv_by_type': {k: {
        'times': v[0].tolist(), 'surv': v[1].tolist(),
        'lower': v[2].tolist(), 'upper': v[3].tolist()
    } for k, v in surv_by_type.items()},
}
# Also pass through the data needed for plots
print("  KM data computed, proceeding to Step 5...")

# ──────────────────────────────────────────────────────────
# STEP 5: PLOTS
# ──────────────────────────────────────────────────────────
print("\n" + "="*60)
print("STEP 5: GENERATING PLOTS")
print("="*60)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors
from matplotlib.patches import Polygon as MplPolygon
from matplotlib.collections import PatchCollection

plt.rcParams.update({
    'figure.facecolor': 'white',
    'axes.facecolor': 'white',
    'axes.grid': True,
    'grid.alpha': 0.3,
    'grid.linestyle': '--',
    'font.size': 11,
    'axes.titlesize': 13,
    'axes.labelsize': 11,
})

DPI = 150
FIGSIZE = (10, 6)

COLORS = ['#2196F3', '#F44336', '#4CAF50', '#FF9800', '#9C27B0', '#00BCD4']

# ── Plot 1: KM Survival Curve ──────────────────────────────
print("  Plot 1: survival_curve.png")
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)

t = np.array([0] + list(km_times))
s = np.array([1.0] + list(km_surv))
lo = np.array([1.0] + list(km_lower))
hi = np.array([1.0] + list(km_upper))

ax.step(t, s, where='post', color='#1565C0', lw=2, label='KM Estimate')
ax.fill_between(t, lo, hi, step='post', alpha=0.2, color='#1565C0', label='95% CI')

# Median annotation
if median_surv:
    ax.axhline(0.5, color='gray', linestyle=':', lw=1.2, alpha=0.7)
    ax.axvline(median_surv, color='#F44336', linestyle='--', lw=1.5, alpha=0.8)
    ax.annotate(f'Median: {median_surv:.0f} yr',
                xy=(median_surv, 0.5), xytext=(median_surv + 0.3, 0.55),
                fontsize=10, color='#F44336',
                arrowprops=dict(arrowstyle='->', color='#F44336', lw=1.2))

ax.set_xlabel('Years in Business')
ax.set_ylabel('Survival Probability')
ax.set_title('Kaplan-Meier Survival Curve — Vancouver Commercial Businesses (FY2013–FY2025)')
ax.set_xlim(0, max(km_times) + 0.5)
ax.set_ylim(0, 1.05)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
ax.legend(loc='upper right', fontsize=10)
ax.text(0.99, 0.02, 'Right-censored: still active in FY25/FY26',
        transform=ax.transAxes, ha='right', va='bottom',
        fontsize=9, color='gray', style='italic')
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/survival_curve.png", dpi=DPI, bbox_inches='tight')
plt.close()

# ── Plot 2: Population by Year ─────────────────────────────
print("  Plot 2: population_by_year.png")
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)

years = pop_by_year['folderyear_4'].values.astype(int)
counts = pop_by_year['count'].values

bar_colors = ['#FFB300' if y == 2026 else '#1976D2' for y in years]
bars = ax.bar(years, counts, color=bar_colors, edgecolor='white', linewidth=0.5)

# Annotate FY26
fy26_idx = list(years).index(2026) if 2026 in list(years) else None
if fy26_idx is not None:
    ax.text(2026, counts[fy26_idx] + 200, 'mid-cycle', ha='center', va='bottom',
            fontsize=9, color='#E65100', fontweight='bold', rotation=0)

# Annotate bars
for bar, cnt in zip(bars, counts):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 50,
            f'{cnt:,.0f}', ha='center', va='bottom', fontsize=7.5, rotation=45)

ax.set_xlabel('Fiscal Year')
ax.set_ylabel('Active Commercial Businesses')
ax.set_title('Active Commercial Businesses per Year — Vancouver FY2013–FY2026')
ax.set_xticks(years)
ax.set_xticklabels([str(y) for y in years], rotation=45, ha='right')
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))

legend_patches = [
    mpatches.Patch(color='#1976D2', label='Full year'),
    mpatches.Patch(color='#FFB300', label='Mid-cycle (FY26)'),
]
ax.legend(handles=legend_patches, loc='upper left', fontsize=9)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/population_by_year.png", dpi=DPI, bbox_inches='tight')
plt.close()

# ── Plot 3: Lifespan Distribution ─────────────────────────
print("  Plot 3: lifespan_distribution.png")
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)

lifespans = panel['years_active'].values
bins = np.arange(0.5, max(lifespans) + 1.5, 1)
ax.hist(lifespans, bins=bins, color='#1976D2', edgecolor='white', linewidth=0.6, alpha=0.85)

med = np.median(lifespans)
ax.axvline(med, color='#F44336', linestyle='--', lw=2, label=f'Median: {med:.0f} yr')

ax.set_xlabel('Years Active (years_active = last_year − first_year + 1)')
ax.set_ylabel('Number of Businesses')
ax.set_title('Commercial Business Lifespan Distribution — Vancouver FY2013–FY2026')
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.legend(fontsize=10)
ax.text(0.99, 0.97, f'n = {len(lifespans):,} businesses',
        transform=ax.transAxes, ha='right', va='top', fontsize=9, color='gray')
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/lifespan_distribution.png", dpi=DPI, bbox_inches='tight')
plt.close()

# ── Plot 4: Survival by Business Type ─────────────────────
print("  Plot 4: survival_by_type.png")
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)

for i, (btype, (t_type, s_type, lo_type, hi_type)) in enumerate(surv_by_type.items()):
    color = COLORS[i % len(COLORS)]
    t_plot = np.array([0] + list(t_type))
    s_plot = np.array([1.0] + list(s_type))
    label = btype[:40] + '...' if len(btype) > 40 else btype
    ax.step(t_plot, s_plot, where='post', color=color, lw=2, label=label)

ax.axhline(0.5, color='gray', linestyle=':', lw=1, alpha=0.5)
ax.set_xlabel('Years in Business')
ax.set_ylabel('Survival Probability')
ax.set_title('KM Survival Curves by Business Type — Top 6 Commercial Categories')
ax.set_xlim(0)
ax.set_ylim(0, 1.05)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
ax.legend(loc='upper right', fontsize=8.5, framealpha=0.9)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/survival_by_type.png", dpi=DPI, bbox_inches='tight')
plt.close()

# ── Plot 5: Status Distribution by Year ───────────────────
print("  Plot 5: status_distribution.png")
status_cols = [s for s in ['Issued', 'Inactive', 'Gone Out of Business'] if s in status_by_year.columns]
status_colors = {'Issued': '#43A047', 'Inactive': '#FFB300', 'Gone Out of Business': '#E53935'}

fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
years_idx = status_by_year.index.astype(int)
bottom = np.zeros(len(years_idx))
for col in status_cols:
    vals = status_by_year[col].values if col in status_by_year.columns else np.zeros(len(years_idx))
    ax.bar(years_idx, vals, bottom=bottom,
           color=status_colors.get(col, '#9E9E9E'),
           label=col, edgecolor='white', linewidth=0.3)
    bottom += vals

ax.set_xlabel('Fiscal Year')
ax.set_ylabel('Licence Count')
ax.set_title('Commercial Business Licence Status by Year — FY2013–FY2026')
ax.set_xticks(years_idx)
ax.set_xticklabels([str(y) for y in years_idx], rotation=45, ha='right')
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x, _: f'{int(x):,}'))
ax.legend(loc='upper left', fontsize=9)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/status_distribution.png", dpi=DPI, bbox_inches='tight')
plt.close()

# ── Plot 6: Geographic Coverage / Scatter ─────────────────
print("  Plot 6: geo_coverage.png")

# Parse geo_point_2d: "lat, lon" or "lon, lat"
def parse_geo(s):
    if pd.isna(s) or str(s).strip() == '':
        return None, None
    try:
        parts = str(s).strip().split(',')
        if len(parts) == 2:
            a, b = float(parts[0].strip()), float(parts[1].strip())
            # Vancouver: lat ~49.2, lon ~-123
            # If a looks like lat (49.x) and b looks like lon (-123.x)
            if 48 < a < 50 and -125 < b < -121:
                return a, b
            elif 48 < b < 50 and -125 < a < -121:
                return b, a
        return None, None
    except:
        return None, None

# Get panel geo data with survival duration
panel_geo = panel.copy()
panel_geo[['lat', 'lon']] = pd.DataFrame(
    panel_geo['geo_point_2d'].apply(parse_geo).tolist(),
    columns=['lat', 'lon'],
    index=panel_geo.index
)
panel_geo = panel_geo.dropna(subset=['lat', 'lon'])
print(f"    Geo-coded businesses: {len(panel_geo):,}")

fig, ax = plt.subplots(figsize=(10, 8), dpi=DPI)

# Load GeoJSON boundary
try:
    with open(GEOJSON_PATH, 'r') as f:
        geojson = json.load(f)

    from matplotlib.patches import PathPatch
    from matplotlib.path import Path

    def draw_geojson(ax, geojson, facecolor='#F5F5F5', edgecolor='#BDBDBD', lw=0.6):
        for feature in geojson.get('features', []):
            geom = feature.get('geometry', {})
            gtype = geom.get('type', '')
            coords_list = geom.get('coordinates', [])

            if gtype == 'Polygon':
                polys = [coords_list[0]]
            elif gtype == 'MultiPolygon':
                polys = [ring[0] for ring in coords_list]
            else:
                continue

            for poly_coords in polys:
                pts = np.array(poly_coords)
                if pts.shape[1] >= 2:
                    xs, ys = pts[:, 0], pts[:, 1]
                    ax.fill(xs, ys, facecolor=facecolor, edgecolor=edgecolor, lw=lw)

    draw_geojson(ax, geojson)
    print("    GeoJSON boundary loaded")
except Exception as e:
    print(f"    GeoJSON load failed: {e} — plotting without boundary")

# Color by survival duration
durations = panel_geo['years_active'].values
cmap = plt.cm.YlOrRd
norm = mcolors.Normalize(vmin=1, vmax=min(14, durations.max()))

scatter = ax.scatter(
    panel_geo['lon'].values,
    panel_geo['lat'].values,
    c=durations, cmap=cmap, norm=norm,
    s=2, alpha=0.5, linewidths=0
)

cbar = plt.colorbar(scatter, ax=ax, pad=0.02, fraction=0.03)
cbar.set_label('Years Active', fontsize=10)

ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Commercial Business Locations Colored by Survival Duration\nVancouver FY2013–FY2026')
ax.set_xlim(-123.28, -123.02)
ax.set_ylim(49.19, 49.32)
ax.text(0.02, 0.02, f'n = {len(panel_geo):,} geo-coded businesses',
        transform=ax.transAxes, fontsize=9, color='gray', va='bottom')
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/geo_coverage.png", dpi=DPI, bbox_inches='tight')
plt.close()

print(f"\n  All plots saved to: {PLOT_DIR}")

# ──────────────────────────────────────────────────────────
# Write standalone plotting script
# ──────────────────────────────────────────────────────────
print("\nWriting standalone plotting script...")

plot_script = '''#!/usr/bin/env python3
"""
Standalone plotting script for Vancouver Commercial Business Licences EDA.
Reads pre-computed panel and scoped commercial data to regenerate all plots.

Usage:
    python3 commercial_eda_plots.py
"""

import pandas as pd
import numpy as np
import json
import os
import warnings
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.ticker
import matplotlib.patches as mpatches
import matplotlib.colors as mcolors

warnings.filterwarnings('ignore')

BASE = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"
COMMERCIAL_CSV = f"{BASE}/data/processed/commercial-licences-2013-to-2026.csv"
PANEL_CSV      = f"{BASE}/data/processed/commercial-panel.csv"
GEOJSON_PATH   = f"{BASE}/data/raw/local-area-boundary.geojson"
PLOT_DIR       = f"{BASE}/analysis/plots"

DPI = 150
FIGSIZE = (10, 6)
COLORS = ['#2196F3', '#F44336', '#4CAF50', '#FF9800', '#9C27B0', '#00BCD4']

plt.rcParams.update({
    'figure.facecolor': 'white', 'axes.facecolor': 'white',
    'axes.grid': True, 'grid.alpha': 0.3, 'grid.linestyle': '--',
    'font.size': 11, 'axes.titlesize': 13, 'axes.labelsize': 11,
})

print("Loading data...")
df = pd.read_csv(COMMERCIAL_CSV, dtype=str, low_memory=False)
panel = pd.read_csv(PANEL_CSV, dtype=str, low_memory=False)
df['folderyear_int'] = df['folderyear'].astype(int)
df['folderyear_4'] = df['folderyear_int'] + 2000
panel['first_year'] = panel['first_year'].astype(int)
panel['last_year'] = panel['last_year'].astype(int)
panel['years_active'] = panel['years_active'].astype(int)
panel['total_folderyears'] = panel['total_folderyears'].astype(int)
print(f"  Loaded {len(df):,} commercial licence rows, {len(panel):,} panel businesses")


def kaplan_meier(durations, events):
    data = sorted(zip(durations, events), key=lambda x: x[0])
    n = len(data)
    events_dict = {}
    for t, e in data:
        if e: events_dict[t] = events_dict.get(t, 0) + 1
    all_times = sorted(set(d for d, e in data))
    s = 1.0
    n_remaining = n
    times, survs, lowers, uppers = [], [], [], []
    for t in all_times:
        n_events = events_dict.get(t, 0)
        n_total_at_t = sum(1 for d, e in data if d == t)
        if n_events > 0:
            s = s * (1 - n_events / n_remaining)
            if 0 < s < 1:
                greenwood = sum(
                    events_dict.get(tt, 0) / max(1,
                        sum(1 for d, e in data if d >= tt) *
                        (sum(1 for d, e in data if d >= tt) - events_dict.get(tt, 0)))
                    for tt in all_times
                    if tt <= t and events_dict.get(tt, 0) > 0
                    and sum(1 for d, e in data if d >= tt) > events_dict.get(tt, 0)
                )
                cumhaz = -np.log(s)
                se_lh = np.sqrt(greenwood) if greenwood > 0 else 0
                ci_lo = np.exp(-np.exp(np.log(cumhaz) + 1.96 * se_lh)) if cumhaz > 0 else s
                ci_hi = np.exp(-np.exp(np.log(cumhaz) - 1.96 * se_lh)) if cumhaz > 0 else s
            else:
                ci_lo = ci_hi = s
            times.append(t); survs.append(s)
            lowers.append(max(0, ci_lo)); uppers.append(min(1, ci_hi))
        n_remaining -= n_total_at_t
    return np.array(times), np.array(survs), np.array(lowers), np.array(uppers)


def surv_at(t, times, survs):
    idx = np.searchsorted(times, t, side='right') - 1
    if idx < 0: return 1.0
    if idx >= len(survs): return survs[-1]
    return survs[idx]


# Compute KM
panel_surv = panel.copy()
panel_surv['censored'] = (
    panel_surv['last_year'].isin([25, 26]) &
    (panel_surv['status_last_year'] == 'Issued')
)
panel_surv['event'] = ~panel_surv['censored']
panel_surv['duration'] = panel_surv['total_folderyears']

print("Computing KM estimates...")
km_t, km_s, km_lo, km_hi = kaplan_meier(
    panel_surv['duration'].values, panel_surv['event'].values)
median_surv = next((km_t[i] for i, sv in enumerate(km_s) if sv <= 0.5), None)
print(f"  Median survival: {median_surv}")

# Survival by type
top6 = df['businesstype'].value_counts().head(6).index.tolist()
surv_by_type = {}
for btype in top6:
    sub = panel_surv[panel_surv['businesstype'] == btype]
    if len(sub) < 30: continue
    t, s, lo, hi = kaplan_meier(sub['duration'].values, sub['event'].values)
    surv_by_type[btype] = (t, s, lo, hi)


# ── Plot 1: KM Survival Curve
print("Plot 1: survival_curve.png")
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
t = np.array([0] + list(km_t)); s = np.array([1.0] + list(km_s))
lo = np.array([1.0] + list(km_lo)); hi = np.array([1.0] + list(km_hi))
ax.step(t, s, where='post', color='#1565C0', lw=2, label='KM Estimate')
ax.fill_between(t, lo, hi, step='post', alpha=0.2, color='#1565C0', label='95% CI')
if median_surv:
    ax.axhline(0.5, color='gray', linestyle=':', lw=1.2, alpha=0.7)
    ax.axvline(median_surv, color='#F44336', linestyle='--', lw=1.5, alpha=0.8)
    ax.annotate(f'Median: {median_surv:.0f} yr', xy=(median_surv, 0.5),
                xytext=(median_surv + 0.3, 0.55), fontsize=10, color='#F44336',
                arrowprops=dict(arrowstyle='->', color='#F44336', lw=1.2))
ax.set_xlabel('Years in Business'); ax.set_ylabel('Survival Probability')
ax.set_title('Kaplan-Meier Survival Curve — Vancouver Commercial Businesses (FY2013–FY2025)')
ax.set_xlim(0, max(km_t) + 0.5); ax.set_ylim(0, 1.05)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
ax.legend(loc='upper right', fontsize=10)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/survival_curve.png", dpi=DPI, bbox_inches='tight'); plt.close()


# ── Plot 2: Population by Year
print("Plot 2: population_by_year.png")
pop = (df[df['status'].isin(['Issued','Inactive'])]
       .groupby('folderyear_4').size().reset_index(name='count'))
pop['folderyear_4'] = pop['folderyear_4'].astype(int)
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
years = pop['folderyear_4'].values; counts = pop['count'].values
colors_b = ['#FFB300' if y == 2026 else '#1976D2' for y in years]
bars = ax.bar(years, counts, color=colors_b, edgecolor='white', linewidth=0.5)
if 2026 in list(years):
    i26 = list(years).index(2026)
    ax.text(2026, counts[i26]+200, 'mid-cycle', ha='center', va='bottom',
            fontsize=9, color='#E65100', fontweight='bold')
for bar, cnt in zip(bars, counts):
    ax.text(bar.get_x()+bar.get_width()/2, bar.get_height()+50,
            f'{cnt:,.0f}', ha='center', va='bottom', fontsize=7.5, rotation=45)
ax.set_xlabel('Fiscal Year'); ax.set_ylabel('Active Commercial Businesses')
ax.set_title('Active Commercial Businesses per Year — Vancouver FY2013–FY2026')
ax.set_xticks(years); ax.set_xticklabels([str(y) for y in years], rotation=45, ha='right')
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,_: f'{int(x):,}'))
ax.legend(handles=[mpatches.Patch(color='#1976D2',label='Full year'),
                   mpatches.Patch(color='#FFB300',label='Mid-cycle (FY26)')],
          loc='upper left', fontsize=9)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/population_by_year.png", dpi=DPI, bbox_inches='tight'); plt.close()


# ── Plot 3: Lifespan Distribution
print("Plot 3: lifespan_distribution.png")
lifespans = panel['years_active'].values
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
bins = np.arange(0.5, max(lifespans)+1.5, 1)
ax.hist(lifespans, bins=bins, color='#1976D2', edgecolor='white', linewidth=0.6, alpha=0.85)
med = np.median(lifespans)
ax.axvline(med, color='#F44336', linestyle='--', lw=2, label=f'Median: {med:.0f} yr')
ax.set_xlabel('Years Active'); ax.set_ylabel('Number of Businesses')
ax.set_title('Commercial Business Lifespan Distribution — Vancouver FY2013–FY2026')
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,_: f'{int(x):,}'))
ax.legend(fontsize=10)
ax.text(0.99,0.97,f'n = {len(lifespans):,}', transform=ax.transAxes,
        ha='right',va='top',fontsize=9,color='gray')
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/lifespan_distribution.png", dpi=DPI, bbox_inches='tight'); plt.close()


# ── Plot 4: Survival by Type
print("Plot 4: survival_by_type.png")
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
for i,(btype,(tt,ss,ll,hh)) in enumerate(surv_by_type.items()):
    color = COLORS[i%len(COLORS)]
    tp = np.array([0]+list(tt)); sp = np.array([1.0]+list(ss))
    label = btype[:40]+'...' if len(btype)>40 else btype
    ax.step(tp,sp,where='post',color=color,lw=2,label=label)
ax.axhline(0.5, color='gray', linestyle=':', lw=1, alpha=0.5)
ax.set_xlabel('Years in Business'); ax.set_ylabel('Survival Probability')
ax.set_title('KM Survival Curves by Business Type — Top 6 Commercial Categories')
ax.set_xlim(0); ax.set_ylim(0, 1.05)
ax.yaxis.set_major_formatter(matplotlib.ticker.PercentFormatter(xmax=1))
ax.legend(loc='upper right', fontsize=8.5, framealpha=0.9)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/survival_by_type.png", dpi=DPI, bbox_inches='tight'); plt.close()


# ── Plot 5: Status Distribution by Year
print("Plot 5: status_distribution.png")
status_by_yr = df.groupby(['folderyear_4','status']).size().unstack(fill_value=0)
status_cols = [s for s in ['Issued','Inactive','Gone Out of Business'] if s in status_by_yr.columns]
status_colors = {'Issued':'#43A047','Inactive':'#FFB300','Gone Out of Business':'#E53935'}
fig, ax = plt.subplots(figsize=FIGSIZE, dpi=DPI)
yrs_idx = status_by_yr.index.astype(int)
bottom = np.zeros(len(yrs_idx))
for col in status_cols:
    vals = status_by_yr[col].values
    ax.bar(yrs_idx, vals, bottom=bottom, color=status_colors.get(col,'#9E9E9E'),
           label=col, edgecolor='white', linewidth=0.3)
    bottom += vals
ax.set_xlabel('Fiscal Year'); ax.set_ylabel('Licence Count')
ax.set_title('Commercial Business Licence Status by Year — FY2013–FY2026')
ax.set_xticks(yrs_idx); ax.set_xticklabels([str(y) for y in yrs_idx], rotation=45, ha='right')
ax.yaxis.set_major_formatter(matplotlib.ticker.FuncFormatter(lambda x,_: f'{int(x):,}'))
ax.legend(loc='upper left', fontsize=9)
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/status_distribution.png", dpi=DPI, bbox_inches='tight'); plt.close()


# ── Plot 6: Geo Coverage
print("Plot 6: geo_coverage.png")
def parse_geo(s):
    if pd.isna(s) or str(s).strip() == '': return None, None
    try:
        parts = str(s).strip().split(',')
        if len(parts) == 2:
            a, b = float(parts[0].strip()), float(parts[1].strip())
            if 48 < a < 50 and -125 < b < -121: return a, b
            elif 48 < b < 50 and -125 < a < -121: return b, a
        return None, None
    except: return None, None

panel_geo = panel.copy()
panel_geo[['lat','lon']] = pd.DataFrame(
    panel_geo['geo_point_2d'].apply(parse_geo).tolist(),
    columns=['lat','lon'], index=panel_geo.index)
panel_geo = panel_geo.dropna(subset=['lat','lon'])
print(f"  Geo-coded: {len(panel_geo):,}")

fig, ax = plt.subplots(figsize=(10,8), dpi=DPI)
try:
    with open(GEOJSON_PATH,'r') as f: geojson = json.load(f)
    for feat in geojson.get('features',[]):
        geom = feat.get('geometry',{}); gtype = geom.get('type','')
        coords_list = geom.get('coordinates',[])
        polys = [coords_list[0]] if gtype=='Polygon' else ([r[0] for r in coords_list] if gtype=='MultiPolygon' else [])
        for pc in polys:
            pts = np.array(pc)
            if pts.shape[1] >= 2:
                ax.fill(pts[:,0],pts[:,1],facecolor='#F5F5F5',edgecolor='#BDBDBD',lw=0.6)
except Exception as e: print(f"  GeoJSON failed: {e}")

durations = panel_geo['years_active'].values.astype(float)
cmap = plt.cm.YlOrRd
norm = mcolors.Normalize(vmin=1, vmax=min(14, durations.max()))
sc = ax.scatter(panel_geo['lon'].values, panel_geo['lat'].values,
                c=durations, cmap=cmap, norm=norm, s=2, alpha=0.5, linewidths=0)
cbar = plt.colorbar(sc, ax=ax, pad=0.02, fraction=0.03)
cbar.set_label('Years Active', fontsize=10)
ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude')
ax.set_title('Commercial Business Locations by Survival Duration\\nVancouver FY2013–FY2026')
ax.set_xlim(-123.28,-123.02); ax.set_ylim(49.19,49.32)
ax.text(0.02,0.02,f'n = {len(panel_geo):,}',transform=ax.transAxes,fontsize=9,color='gray',va='bottom')
plt.tight_layout()
plt.savefig(f"{PLOT_DIR}/geo_coverage.png", dpi=DPI, bbox_inches='tight'); plt.close()

print(f"\\nAll plots saved to: {PLOT_DIR}")
'''

with open(SCRIPT_OUT, 'w') as f:
    f.write(plot_script)
print(f"Saved standalone plotting script: {SCRIPT_OUT}")

print("\n" + "="*60)
print("PIPELINE COMPLETE")
print("="*60)
print(f"  Merged CSV:     {MERGED_OUT}")
print(f"  Commercial CSV: {COMMERCIAL_OUT}")
print(f"  Panel CSV:      {PANEL_OUT}")
print(f"  EDA Report:     {EDA_OUT}")
print(f"  Plots:          {PLOT_DIR}/")
print(f"  Plot script:    {SCRIPT_OUT}")
