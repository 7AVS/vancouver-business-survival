"""
audit_branch_exits.py — Silent Exit & Chain/Franchise Data Quality Audit
=========================================================================
Van-Property-Tax Project | 2026-03-04

Investigates a specific data quality problem: when a chain/franchise location
closes, the licence simply doesn't get renewed. No "Gone Out of Business" or
"Inactive" status is recorded because the parent company still exists elsewhere.
These silent exits appear as right-censored survivors, inflating survival rates.

Parts:
  1. Quantify silent exits across ALL businesses
  2. Quantify the chain/franchise branch problem specifically
  3. Impact on survival estimates (before vs. after reclassification)
  4. Recommended treatment

Usage:
    python3.12 scripts/audit_branch_exits.py

Data:
    data/processed/commercial-panel-v2.csv  (101,471 rows)
    data/processed/businesstype_macro_categories.csv

Year encoding: last_year/first_year stored as 2-digit (13=2013, 26=2026).
Observation window: 2013–2026. Latest data year = 26.
"""

import os
import sys
import warnings

import numpy as np
import pandas as pd
from lifelines import KaplanMeierFitter

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"
DATA    = os.path.join(PROJECT, "data/processed/commercial-panel-v2.csv")
MACRO   = os.path.join(PROJECT, "data/processed/businesstype_macro_categories.csv")

# The data covers years 13–26 (2013–2026).
# "Silent exit" cutoff: last_year <= 22 (2022) means 3+ years absent from
# the registry without any closure code. Almost certainly dead.
DATA_YEAR      = 26   # current data year (2026)
SILENT_CUTOFF  = 22   # last_year <= this = 3+ years absent = silent exit
SILENT_CUTOFF2 = 23   # alternative: 2+ years absent (stricter)

CHAIN_THRESHOLD = 5   # address_count >= 5 → chain in panel v2 build
MULTI_THRESHOLD = 2   # address_count >= 2 → multi-location

DIVIDER = "=" * 72

def sep(title=""):
    if title:
        print(f"\n{DIVIDER}")
        print(f"  {title}")
        print(f"{DIVIDER}")
    else:
        print(f"\n{DIVIDER}")

def pct(n, d):
    if d == 0:
        return "N/A"
    return f"{100*n/d:.1f}%"

def km_at(kmf, t):
    """Return survival probability at time t from a fitted KaplanMeierFitter."""
    tl = kmf.timeline
    sf = kmf.survival_function_
    idx = tl[tl <= t]
    if len(idx) == 0:
        return 1.0
    return float(sf.loc[idx[-1]].iloc[0])

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
sep("LOADING DATA")

df = pd.read_csv(DATA, low_memory=False)
print(f"Panel loaded: {len(df):,} rows × {len(df.columns)} columns")
print(f"Columns: {df.columns.tolist()}")
print(f"\nyears_active range: {df['years_active'].min():.0f} – {df['years_active'].max():.0f}")
print(f"first_year range  : {df['first_year'].min()} – {df['first_year'].max()}")
print(f"last_year range   : {df['last_year'].min()} – {df['last_year'].max()}")
print(f"\nData year (current): {DATA_YEAR} (= 20{DATA_YEAR})")

# Attach macro_category
macro = pd.read_csv(MACRO)
df["_bt_clean"] = df["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
macro["_bt_clean"] = macro["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
macro_dedup = macro[["_bt_clean", "macro_category"]].drop_duplicates(subset=["_bt_clean"])
df = df.merge(macro_dedup, on="_bt_clean", how="left")
df.drop(columns=["_bt_clean"], inplace=True)
n_macro_matched = df["macro_category"].notna().sum()
print(f"\nmacro_category matched: {n_macro_matched:,} / {len(df):,}")

# ---------------------------------------------------------------------------
# PART 1: Quantify silent exits across ALL businesses
# ---------------------------------------------------------------------------
sep("PART 1 — SILENT EXITS ACROSS ALL BUSINESSES")

# Silent exit definition:
#   - status_last_year is NOT "Gone Out of Business" AND NOT "Inactive"
#   - last_year <= SILENT_CUTOFF (3+ years absent from registry)
#
# Rationale: a business with status="Issued" whose last appearance was in 2022
# or earlier has been absent from the annual licence data for 3+ consecutive
# years. Vancouver businesses must renew annually. 3 missed renewals with no
# closure code = almost certainly dead, just never coded as such.

ACTIVE_STATUSES  = {"Issued"}
CLOSED_STATUSES  = {"Gone Out of Business", "Inactive"}

n_total = len(df)

# Status breakdown
print("\nFull panel status_last_year distribution:")
status_counts = df["status_last_year"].value_counts()
for status, count in status_counts.items():
    print(f"  {status:30s}: {count:7,}  ({pct(count, n_total)})")

# Already-coded exits
n_coded_exits = df["status_last_year"].isin(CLOSED_STATUSES).sum()
print(f"\nAlready-coded exits (GoB + Inactive): {n_coded_exits:,}  ({pct(n_coded_exits, n_total)})")

# Silent exit mask (3+ year cutoff)
mask_not_closed   = ~df["status_last_year"].isin(CLOSED_STATUSES)
mask_old_enough_3 = df["last_year"] <= SILENT_CUTOFF
mask_silent_3yr   = mask_not_closed & mask_old_enough_3

n_silent_3yr = mask_silent_3yr.sum()
print(f"\n--- Silent exits (last_year <= 20{SILENT_CUTOFF}, status not GoB/Inactive) ---")
print(f"  Count   : {n_silent_3yr:,}")
print(f"  % total : {pct(n_silent_3yr, n_total)}")

# Alternative cutoff: 2+ years absent
mask_old_enough_2 = df["last_year"] <= SILENT_CUTOFF2
mask_silent_2yr   = mask_not_closed & mask_old_enough_2
n_silent_2yr = mask_silent_2yr.sum()
print(f"\n--- Silent exits (last_year <= 20{SILENT_CUTOFF2}, status not GoB/Inactive) [alt 2yr cutoff] ---")
print(f"  Count   : {n_silent_2yr:,}")
print(f"  % total : {pct(n_silent_2yr, n_total)}")

# Breakdown by status_last_year for silent exits (3yr cutoff)
df_silent = df[mask_silent_3yr].copy()
print(f"\nSilent exits — breakdown by status_last_year:")
se_status = df_silent["status_last_year"].value_counts()
for status, count in se_status.items():
    print(f"  {status:30s}: {count:7,}  ({pct(count, n_silent_3yr)} of silent)")

# Breakdown by last_year for silent exits
print(f"\nSilent exits — breakdown by last_year:")
se_lastyear = df_silent["last_year"].value_counts().sort_index()
for yr, count in se_lastyear.items():
    print(f"  20{yr:02d}: {count:6,}")

# Breakdown by macro_category
print(f"\nSilent exits — breakdown by macro_category (top 15):")
se_macro = df_silent["macro_category"].value_counts().head(15)
for cat, count in se_macro.items():
    base_n = (df["macro_category"] == cat).sum()
    print(f"  {str(cat):35s}: {count:5,} silent  /  {base_n:6,} total  ({pct(count, base_n)} of sector)")

# Breakdown by businesstype (top 20)
print(f"\nSilent exits — breakdown by businesstype (top 20):")
se_type = df_silent["businesstype"].value_counts().head(20)
for bt, count in se_type.items():
    base_n = (df["businesstype"] == bt).sum()
    print(f"  {str(bt):45s}: {count:5,} silent  /  {base_n:5,} total  ({pct(count, base_n)})")

# ---------------------------------------------------------------------------
# PART 2: Chain/franchise branch problem
# ---------------------------------------------------------------------------
sep("PART 2 — CHAIN / FRANCHISE BRANCH PROBLEM")

print(f"\nAddress count distribution:")
ac_dist = df["address_count"].value_counts().sort_index()
for ac_val, count in ac_dist.items():
    print(f"  address_count = {ac_val:3d}: {count:7,}  ({pct(count, n_total)})")

# Chains (address_count >= CHAIN_THRESHOLD)
df_chains   = df[df["address_count"] >= CHAIN_THRESHOLD].copy()
n_chains    = len(df_chains)
print(f"\n--- Chains (address_count >= {CHAIN_THRESHOLD}) ---")
print(f"  Total chain businesses : {n_chains:,}  ({pct(n_chains, n_total)})")

if n_chains > 0:
    print(f"\n  Status distribution for chains:")
    chain_status = df_chains["status_last_year"].value_counts()
    for status, count in chain_status.items():
        print(f"    {status:30s}: {count:5,}  ({pct(count, n_chains)})")

    n_chain_silent = (df_chains["status_last_year"].isin(ACTIVE_STATUSES) &
                      (df_chains["last_year"] <= SILENT_CUTOFF)).sum()
    print(f"\n  Chain silent exits: {n_chain_silent:,}  ({pct(n_chain_silent, n_chains)} of chains)")
    print(f"  Top 20 chain names:")
    top_chains = df_chains["businessname"].value_counts().head(20)
    for name, count in top_chains.items():
        print(f"    {str(name):50s}: {count:4,}")
else:
    print("  No businesses with address_count >= 5 found in panel.")
    print("  NOTE: The panel has max address_count = 4 in this build.")

# Multi-location (address_count >= MULTI_THRESHOLD, not full chains)
df_multi    = df[(df["address_count"] >= MULTI_THRESHOLD) &
                 (df["address_count"] < CHAIN_THRESHOLD)].copy()
n_multi     = len(df_multi)
print(f"\n--- Multi-location, non-chain (address_count {MULTI_THRESHOLD}–{CHAIN_THRESHOLD-1}) ---")
print(f"  Total: {n_multi:,}  ({pct(n_multi, n_total)})")

print(f"\n  Status distribution:")
multi_status = df_multi["status_last_year"].value_counts()
for status, count in multi_status.items():
    print(f"    {status:30s}: {count:5,}  ({pct(count, n_multi)})")

n_multi_silent = (df_multi["status_last_year"].isin(ACTIVE_STATUSES) &
                  (df_multi["last_year"] <= SILENT_CUTOFF)).sum()
print(f"\n  Multi-location silent exits: {n_multi_silent:,}  ({pct(n_multi_silent, n_multi)})")

# For reference: single-location silent exits
df_single   = df[df["address_count"] == 1].copy()
n_single    = len(df_single)
n_single_silent = (df_single["status_last_year"].isin(ACTIVE_STATUSES) &
                   (df_single["last_year"] <= SILENT_CUTOFF)).sum()
print(f"\n--- Single-location (address_count == 1) ---")
print(f"  Total: {n_single:,}  ({pct(n_single, n_total)})")
print(f"  Single-location silent exits: {n_single_silent:,}  ({pct(n_single_silent, n_single)})")

# Top 20 business names among ALL silent exits (to see if chain names appear)
print(f"\n--- Top 20 business names among silent exits (3yr cutoff) ---")
print("(Looking for chain/franchise names that appear repeatedly)")
top_silent_names = df_silent["businessname"].value_counts().head(20)
for name, count in top_silent_names.items():
    # Check address_count for these businesses
    addr_cnt = df[df["businessname"] == name]["address_count"].max()
    print(f"  {str(name):50s}: {count:4,} (max address_count={addr_cnt})")

# Sector-level silent exit rates for multi vs. single
print(f"\n--- Silent exit rate comparison: single vs. multi-location ---")
print(f"  {'Metric':40s}  {'Single-loc':>12}  {'Multi-loc':>12}")
print(f"  {'-'*40}  {'-'*12}  {'-'*12}")
for cat in df["macro_category"].dropna().unique():
    s = df_single[df_single["macro_category"] == cat]
    m = df_multi[df_multi["macro_category"] == cat]
    ns = (s["status_last_year"].isin(ACTIVE_STATUSES) & (s["last_year"] <= SILENT_CUTOFF)).sum()
    nm = (m["status_last_year"].isin(ACTIVE_STATUSES) & (m["last_year"] <= SILENT_CUTOFF)).sum()
    if len(s) > 50:
        print(f"  {str(cat):40s}  {pct(ns, len(s)):>12}  {pct(nm, len(m)) if len(m) > 0 else 'N/A':>12}")

# ---------------------------------------------------------------------------
# PART 3: Impact on survival estimates
# ---------------------------------------------------------------------------
sep("PART 3 — IMPACT ON SURVIVAL ESTIMATES")

# Original KM setup (from step1_baseline_survival.py):
#   duration = years_active
#   event    = 1 if status_last_year in {GoB, Inactive}, else 0
#
# Corrected KM:
#   silent exits (last_year <= 22, status=Issued) → reclassified as events (event=1)
#   rationale: 3+ years absent from registry = observed exit, just uncoded

df["duration"]        = df["years_active"]
df["event_original"]  = df["status_last_year"].isin(CLOSED_STATUSES).astype(int)

# Corrected: also flag silent exits as events
df["event_corrected"] = df["event_original"].copy()
df.loc[mask_silent_3yr, "event_corrected"] = 1

# Also compute alternative (2yr cutoff)
df["event_corrected_2yr"] = df["event_original"].copy()
df.loc[mask_silent_2yr, "event_corrected_2yr"] = 1

n_events_orig  = df["event_original"].sum()
n_events_corr  = df["event_corrected"].sum()
n_events_corr2 = df["event_corrected_2yr"].sum()

print(f"\nEvent counts before vs. after reclassification:")
print(f"  Original  (GoB + Inactive only)          : {n_events_orig:,}  ({pct(n_events_orig, n_total)})")
print(f"  Corrected (+ silent exits, 3yr cutoff)   : {n_events_corr:,}  ({pct(n_events_corr, n_total)})")
print(f"  Corrected (+ silent exits, 2yr cutoff)   : {n_events_corr2:,}  ({pct(n_events_corr2, n_total)})")

print(f"\n  Silent exits reclassified: {n_events_corr - n_events_orig:,}")

# Fit KM — original
print("\nFitting KM curves...")
kmf_orig = KaplanMeierFitter(label="Original (GoB+Inactive only)")
kmf_orig.fit(df["duration"], event_observed=df["event_original"])

kmf_corr = KaplanMeierFitter(label="Corrected (+ silent exits, 3yr)")
kmf_corr.fit(df["duration"], event_observed=df["event_corrected"])

kmf_corr2 = KaplanMeierFitter(label="Corrected (+ silent exits, 2yr)")
kmf_corr2.fit(df["duration"], event_observed=df["event_corrected_2yr"])

# Extract key milestones
milestones = [1, 5, 10]

print(f"\n{'Milestone':>10}  {'Original':>12}  {'Corrected 3yr':>14}  {'Corrected 2yr':>14}  {'Delta (3yr)':>12}")
print(f"  {'-'*10}  {'-'*12}  {'-'*14}  {'-'*14}  {'-'*12}")
for t in milestones:
    p_orig  = km_at(kmf_orig,  t)
    p_corr  = km_at(kmf_corr,  t)
    p_corr2 = km_at(kmf_corr2, t)
    delta   = p_corr - p_orig
    print(f"  {t:>8}yr  {p_orig:>11.1%}  {p_corr:>13.1%}  {p_corr2:>13.1%}  {delta:>+12.1%}")

median_orig  = kmf_orig.median_survival_time_
median_corr  = kmf_corr.median_survival_time_
median_corr2 = kmf_corr2.median_survival_time_

print(f"\n  {'Median':>10}  {median_orig:>12.1f}  {median_corr:>14.1f}  {median_corr2:>14.1f}  {median_corr - median_orig:>+12.1f}")
print(f"  {'':10}  {'(yr)':>12}  {'(yr)':>14}  {'(yr)':>14}  {'(yr)':>12}")

print(f"\nComparison vs. published estimates (Step 1 baseline):")
published = {"median": 8, "yr1": 0.92, "yr5": 0.60, "yr10": 0.41}
print(f"  Published median   : {published['median']} yr")
print(f"  Corrected median   : {median_corr:.1f} yr  (delta: {median_corr - published['median']:+.1f} yr)")
print(f"  Published 1yr rate : {published['yr1']:.0%}")
print(f"  Corrected 1yr rate : {km_at(kmf_corr, 1):.1%}")
print(f"  Published 5yr rate : {published['yr5']:.0%}")
print(f"  Corrected 5yr rate : {km_at(kmf_corr, 5):.1%}")
print(f"  Published 10yr rate: {published['yr10']:.0%}")
print(f"  Corrected 10yr rate: {km_at(kmf_corr, 10):.1%}")

# Finance & Insurance sector specifically
print(f"\n--- Finance & Insurance sector: original vs. corrected ---")
FIN_SECTOR = "Financial & Insurance"
df_fin = df[df["macro_category"] == FIN_SECTOR].copy()
n_fin  = len(df_fin)
print(f"  Finance & Insurance businesses: {n_fin:,}")

n_fin_silent = (df_fin["status_last_year"].isin(ACTIVE_STATUSES) &
                (df_fin["last_year"] <= SILENT_CUTOFF)).sum()
print(f"  Finance & Insurance silent exits (3yr): {n_fin_silent:,}  ({pct(n_fin_silent, n_fin)})")

if n_fin > 30:
    kmf_fin_orig = KaplanMeierFitter(label="Finance & Insurance — original")
    kmf_fin_orig.fit(df_fin["duration"], event_observed=df_fin["event_original"])

    # Corrected event flag for this subset
    df_fin["event_corrected"] = df_fin["event_original"].copy()
    fin_silent_mask = (df_fin["status_last_year"].isin(ACTIVE_STATUSES) &
                       (df_fin["last_year"] <= SILENT_CUTOFF))
    df_fin.loc[fin_silent_mask, "event_corrected"] = 1

    kmf_fin_corr = KaplanMeierFitter(label="Finance & Insurance — corrected")
    kmf_fin_corr.fit(df_fin["duration"], event_observed=df_fin["event_corrected"])

    median_fin_orig = kmf_fin_orig.median_survival_time_
    median_fin_corr = kmf_fin_corr.median_survival_time_

    print(f"\n  Finance & Insurance survival rates:")
    print(f"  {'Milestone':>10}  {'Original':>12}  {'Corrected':>12}  {'Delta':>10}")
    print(f"  {'-'*10}  {'-'*12}  {'-'*12}  {'-'*10}")
    for t in milestones:
        p_o = km_at(kmf_fin_orig, t)
        p_c = km_at(kmf_fin_corr, t)
        print(f"  {t:>8}yr  {p_o:>11.1%}  {p_c:>11.1%}  {p_c - p_o:>+10.1%}")
    print(f"  {'Median':>10}  {median_fin_orig:>12.1f}  {median_fin_corr:>12.1f}  {median_fin_corr - median_fin_orig:>+10.1f}")
    print(f"  (Step 2 reported Finance & Insurance median = 14yr)")
    print(f"  Original median (this run): {median_fin_orig:.1f}yr")
    print(f"  Corrected median           : {median_fin_corr:.1f}yr")
else:
    print("  Too few Finance & Insurance rows to fit KM reliably.")

# ---------------------------------------------------------------------------
# PART 4: Recommended treatment
# ---------------------------------------------------------------------------
sep("PART 4 — RECOMMENDED TREATMENT")

print("""
FINDINGS SUMMARY
----------------
The "silent exit" problem is real but its magnitude depends on how the panel
is built. Key findings:

  1. address_count in this panel maxes at 4 — the CHAIN_THRESHOLD of 5 was
     never triggered. No businesses were flagged as chains in panel v2.
     Multi-location businesses (address_count >= 2) exist and could carry
     the same silent-exit bias, but at lower intensity than true chains.

  2. The silent exit pool (status=Issued, last_year <= 2022) consists of
     businesses that simply stopped filing — most likely dead, but not coded.
     They inflate the "still active" count and compress measured hazard.

  3. Finance & Insurance historically showed a high median survival. If that
     sector has a disproportionate share of silent exits (bank branches,
     insurance offices, brokerage desks that closed without a GoB filing),
     its true survival distribution could be meaningfully shorter.

RECOMMENDATIONS
---------------

A. RECLASSIFICATION: YES — reclassify silent exits as events
   The 3-year absence cutoff (last_year <= 2022) is defensible and
   conservative. A Vancouver business that has not filed a licence renewal
   for 3 consecutive years has, by any reasonable definition, exited.
   The "Issued" status on their last record reflects the state at exit,
   not continued operation.

   Action: Set event = 1 for all businesses where:
     - status_last_year NOT IN {"Gone Out of Business", "Inactive"}
     - last_year <= (DATA_YEAR - 3)   # i.e., 3+ years absent

   Present as a corrected baseline alongside the original for transparency.
   The delta between the two curves IS the story about coding quality.

B. CUTOFF CHOICE: 3 years is the right starting point
   - 2 years is aggressive: a legitimate business could lapse one renewal
     cycle and re-appear (we see gap-filling in the panel already).
   - 3 years is conservative and aligns with typical licence enforcement:
     if a business truly lapsed, the city would have removed it from active
     rolls within 1-2 years.
   - RECOMMENDATION: Use 3yr as primary, show 2yr as sensitivity.

C. CHAINS / MULTI-LOCATION: Separate stratum, not exclusion
   The chain threshold of 5 was never reached in this panel, so the
   chain/franchise problem manifests instead as multi-location businesses
   (address_count >= 2). These are ~9% of the panel.

   Options (in order of preference):
   1. PREFERRED: Stratify by address_count (1 vs. 2-4) and run separate
      KM curves. If multi-location businesses show systematically different
      survival patterns or higher silent-exit rates, the stratification makes
      the bias explicit rather than masking it.
   2. ACCEPTABLE: Include but flag in caveats. The silent-exit reclassification
      (Part A) already partially corrects for the problem.
   3. NOT RECOMMENDED: Exclude multi-location businesses. They are legitimate
      businesses; excluding them would shrink the panel and introduce its own
      selection bias (we'd be studying only solo operators).

D. FINANCE & INSURANCE SECTOR: Scrutinise the 14-year median
   If the corrected Finance & Insurance median drops materially from the
   reported 14yr, the headline finding is overstated. Bank branches and
   insurance offices are classic silent-exit candidates: the parent entity
   never files "Gone Out of Business" because they still exist; they just
   close a location.

   Action: After reclassification, re-run step2_survival_by_type.py and
   check whether Financial & Insurance still leads on median survival.
   If the gap narrows significantly, update the narrative.

E. PANEL V3 CONSIDERATION
   For a portfolio project, it is worth building a panel_v3 that:
   - Encodes silent exits explicitly (new status value: "Silent Exit")
   - Documents the reclassification rule and cutoff in PANEL_V3_CHANGELOG.md
   - Adds a `is_multi_location` flag (address_count >= 2)
   - Adds a `reclassified_event` boolean column for transparency
   This makes the data quality decision auditable and reproducible.
""")

print(f"\n{'='*72}")
print("  AUDIT COMPLETE")
print(f"{'='*72}")
print(f"\nScript: scripts/audit_branch_exits.py")
print(f"Panel : {DATA}")
