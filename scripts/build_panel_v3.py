"""
build_panel_v3.py
=================
Applies two corrections to commercial-panel-v2.csv to produce commercial-panel-v3.csv.

Correction 1: Silent Exit Reclassification
  - Businesses with status_last_year == "Issued" but last_year <= 2022 are
    reclassified as deaths (they stopped renewing 3+ years ago without a formal closure).
  - Adds: silent_exit (bool), event_v3 (int)

Correction 2: Chain/Franchise Identification
  - Same normalized business name appearing in 5+ distinct business_ids = chain.
  - Adds: chain_name (str or NaN), is_chain (bool), chain_location_count (int)

Output: data/processed/commercial-panel-v3.csv
Renames v2 to:  data/processed/_SUPERSEDED_commercial-panel-v2.csv
"""

import re
import os
import shutil
import pandas as pd
from lifelines import KaplanMeierFitter

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT_ROOT = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"
V2_PATH      = os.path.join(PROJECT_ROOT, "data/processed/commercial-panel-v2.csv")
V3_PATH      = os.path.join(PROJECT_ROOT, "data/processed/commercial-panel-v3.csv")
V2_ARCHIVE   = os.path.join(PROJECT_ROOT, "data/processed/_SUPERSEDED_commercial-panel-v2.csv")

# ---------------------------------------------------------------------------
# Load
# ---------------------------------------------------------------------------
print("=" * 70)
print("BUILDING COMMERCIAL PANEL V3")
print("=" * 70)
print(f"\nLoading v2 from: {V2_PATH}")
df = pd.read_csv(V2_PATH, low_memory=False)
print(f"Loaded {len(df):,} rows x {df.shape[1]} columns")
print(f"Columns: {list(df.columns)}")


# ---------------------------------------------------------------------------
# CORRECTION 1: Silent Exit Reclassification
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("CORRECTION 1: SILENT EXIT RECLASSIFICATION")
print("=" * 70)

# last_year is stored as 2-digit (13..26 = 2013..2026) per the value_counts we saw.
# Threshold: last_year <= 22  (i.e., <= 2022)
SILENT_EXIT_THRESHOLD = 22   # 2-digit year (22 = 2022)

df["silent_exit"] = (
    (df["status_last_year"] == "Issued") &
    (df["last_year"] <= SILENT_EXIT_THRESHOLD)
)

# event_v3 = 1 if formal closure (Gone Out of Business / Inactive) OR silent exit
df["event_v3"] = (
    (df["status_last_year"].isin(["Gone Out of Business", "Inactive"])) |
    (df["silent_exit"])
).astype(int)

n_silent = df["silent_exit"].sum()
pct_silent = n_silent / len(df) * 100
print(f"  Silent exits reclassified : {n_silent:,}  ({pct_silent:.1f}% of all businesses)")
print(f"  Breakdown of silent exits by last_year:")
print(df[df["silent_exit"]]["last_year"].value_counts().sort_index().to_string())

# Original event indicator (for comparison)
df["event_v2"] = df["status_last_year"].isin(["Gone Out of Business", "Inactive"]).astype(int)
original_event_rate = df["event_v2"].mean() * 100
corrected_event_rate = df["event_v3"].mean() * 100
print(f"\n  Original  event rate (v2) : {original_event_rate:.1f}%")
print(f"  Corrected event rate (v3) : {corrected_event_rate:.1f}%")
print(f"  Delta                     : +{corrected_event_rate - original_event_rate:.1f} pp")


# ---------------------------------------------------------------------------
# CORRECTION 2: Chain/Franchise Identification
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("CORRECTION 2: CHAIN / FRANCHISE IDENTIFICATION")
print("=" * 70)

COMMON_SUFFIXES = r"\b(ltd|inc|corp|co|llc|limited|corporation|company)\b"

def normalize_name(name):
    """Lowercase, strip whitespace, remove punctuation, remove common suffixes."""
    if pd.isna(name) or str(name).strip() == "":
        return None
    n = str(name).lower().strip()
    n = re.sub(r"[^\w\s]", " ", n)          # remove punctuation → space
    n = re.sub(COMMON_SUFFIXES, " ", n)      # strip common suffixes
    n = re.sub(r"\s+", " ", n).strip()       # collapse whitespace
    return n if n else None

df["_norm_name"] = df["businessname"].apply(normalize_name)

# Count distinct business_ids per normalized name (exclude None names)
valid_names = df[df["_norm_name"].notna()]
chain_counts = (
    valid_names.groupby("_norm_name")["business_id"]
    .nunique()
    .rename("_biz_count")
)

CHAIN_THRESHOLD = 5
chains = chain_counts[chain_counts >= CHAIN_THRESHOLD]
chain_set = set(chains.index)

print(f"  Chain threshold           : {CHAIN_THRESHOLD}+ distinct business_ids")
print(f"  Unique normalized names   : {len(chain_counts):,}")
print(f"  Names qualifying as chains: {len(chains):,}")

# Map back to df
df["chain_name"] = df["_norm_name"].where(df["_norm_name"].isin(chain_set), other=None)
df["is_chain"] = df["chain_name"].notna()
df["chain_location_count"] = df["_norm_name"].map(chain_counts).where(
    df["_norm_name"].isin(chain_set), other=0
).fillna(0).astype(int)

# Drop working column
df.drop(columns=["_norm_name", "event_v2"], inplace=True)

n_chain_biz = df["is_chain"].sum()
pct_chain = n_chain_biz / len(df) * 100
n_chain_groups = df[df["is_chain"]]["chain_name"].nunique()
print(f"  Businesses flagged as chain: {n_chain_biz:,}  ({pct_chain:.1f}% of all businesses)")
print(f"  Distinct chain groups      : {n_chain_groups:,}")


# ---------------------------------------------------------------------------
# OVERLAP: Chains that are also silent exits
# ---------------------------------------------------------------------------
overlap = (df["is_chain"] & df["silent_exit"]).sum()
print(f"\n  Overlap (chain AND silent_exit): {overlap:,}")


# ---------------------------------------------------------------------------
# TOP 30 CHAINS
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("TOP 30 CHAINS BY LOCATION COUNT")
print("=" * 70)

top30 = (
    df[df["is_chain"]]
    .groupby("chain_name")["business_id"]
    .nunique()
    .sort_values(ascending=False)
    .head(30)
    .reset_index()
)
top30.columns = ["normalized_name", "location_count"]

# Also pull a sample of original names for readability
sample_names = (
    df[df["is_chain"]]
    .groupby("chain_name")["businessname"]
    .agg(lambda x: x.dropna().iloc[0] if x.dropna().any() else "")
    .rename("sample_original_name")
)
top30 = top30.merge(sample_names, left_on="normalized_name", right_index=True, how="left")

print(f"\n{'Rank':<6} {'Locations':<12} {'Normalized Name':<45} {'Sample Original Name'}")
print("-" * 100)
for i, row in top30.iterrows():
    print(f"{i+1:<6} {row['location_count']:<12} {row['normalized_name']:<45} {row['sample_original_name']}")


# ---------------------------------------------------------------------------
# SUMMARY STATS
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("SUMMARY STATISTICS")
print("=" * 70)
print(f"  Total businesses          : {len(df):,}")
print(f"  Silent exits (reclassed)  : {n_silent:,}  ({pct_silent:.1f}%)")
print(f"  Chain businesses          : {n_chain_biz:,}  ({pct_chain:.1f}%)")
print(f"  Chain AND silent_exit     : {overlap:,}")
print(f"  Original  event rate (v2) : {original_event_rate:.1f}%")
print(f"  Corrected event rate (v3) : {corrected_event_rate:.1f}%")


# ---------------------------------------------------------------------------
# KAPLAN-MEIER VALIDATION
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("KAPLAN-MEIER VALIDATION")
print("=" * 70)

def km_stats(durations, events, label):
    """Fit KM and return median + survival at key timepoints."""
    kmf = KaplanMeierFitter()
    kmf.fit(durations=durations, event_observed=events, label=label)
    timeline = kmf.survival_function_at_times([1, 5, 10])
    median = kmf.median_survival_time_
    y1  = timeline.iloc[0] * 100
    y5  = timeline.iloc[1] * 100
    y10 = timeline.iloc[2] * 100
    return median, y1, y5, y10

print("\n  Using 'years_active' as duration column.")
dur = df["years_active"]

# -- Original event (v2: status_last_year only)
orig_events = df["status_last_year"].isin(["Gone Out of Business", "Inactive"])
med_orig, y1_orig, y5_orig, y10_orig = km_stats(dur, orig_events, "v2_original")

# -- Corrected event (v3: + silent exits)
corr_events = df["event_v3"]
med_corr, y1_corr, y5_corr, y10_corr = km_stats(dur, corr_events, "v3_corrected")

# -- Corrected, non-chains only
indep = df[df["is_chain"] == False]
dur_indep = indep["years_active"]
corr_events_indep = indep["event_v3"]
med_indep, y1_indep, y5_indep, y10_indep = km_stats(dur_indep, corr_events_indep, "v3_independents")

print(f"\n  {'Metric':<30} {'V2 Original':>14} {'V3 Corrected':>14} {'V3 Independents':>16}")
print("  " + "-" * 78)
print(f"  {'N':<30} {len(dur):>14,} {len(dur):>14,} {len(dur_indep):>16,}")
print(f"  {'Median survival (yrs)':<30} {med_orig:>14.1f} {med_corr:>14.1f} {med_indep:>16.1f}")
print(f"  {'Year-1 survival (%)':<30} {y1_orig:>14.1f} {y1_corr:>14.1f} {y1_indep:>16.1f}")
print(f"  {'Year-5 survival (%)':<30} {y5_orig:>14.1f} {y5_corr:>14.1f} {y5_indep:>16.1f}")
print(f"  {'Year-10 survival (%)':<30} {y10_orig:>14.1f} {y10_corr:>14.1f} {y10_indep:>16.1f}")


# ---------------------------------------------------------------------------
# SAVE & RENAME
# ---------------------------------------------------------------------------
print("\n" + "=" * 70)
print("SAVING")
print("=" * 70)

# Verify new columns are present
new_cols = ["silent_exit", "event_v3", "chain_name", "is_chain", "chain_location_count"]
print(f"\n  New columns added: {new_cols}")
print(f"  Total columns in v3: {df.shape[1]}")

df.to_csv(V3_PATH, index=False)
print(f"  Saved v3 to: {V3_PATH}")

shutil.move(V2_PATH, V2_ARCHIVE)
print(f"  Renamed v2 to: {V2_ARCHIVE}")

print("\n  Done.\n")
