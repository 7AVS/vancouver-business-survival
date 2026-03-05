#!/usr/bin/env python3
"""
regenerate_all_plots.py
=======================
Regenerates ALL plots for the Vancouver Business Survival Analysis with
fixes from the visual audit:

  Step 1 — baseline KM curve (fix risk table text overlap)
  Step 3 — neighbourhood survival (replace spaghetti with 2x5 small multiples)
  Step 4 — scatter plot (fix overlapping labels with adjustText)
  Step 5 — forest plot (group by type/area/continuous, rename duplicate 'Other')
  Step 5 — model comparison (fix misleading AIC axis, add delta annotations)

Run:
    cd /home/aurora/projects/sites/portfolio-projects/van-property-tax
    source .venv/bin/activate
    python scripts/regenerate_all_plots.py
"""

import warnings
warnings.filterwarnings("ignore")

import os
import sys
import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.lines import Line2D
from scipy import stats as scipy_stats
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test

try:
    from adjustText import adjust_text
    HAS_ADJUST_TEXT = True
except ImportError:
    HAS_ADJUST_TEXT = False
    print("WARNING: adjustText not found — will use manual offsets for scatter labels")

# ── Paths ────────────────────────────────────────────────────────────────────
PROJECT  = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"
PLOTS    = os.path.join(PROJECT, "analysis/plots")
os.makedirs(PLOTS, exist_ok=True)

# ── Style constants ──────────────────────────────────────────────────────────
ANNO_COLOR = "#2c2c2c"
REF_RED    = "#cc3333"
SPINE_GREY = "#dddddd"
GRID_GREY  = "#eeeeee"
SOURCE_GREY = "#888888"

SOURCE_BIZ = (
    "Source: City of Vancouver Open Data — Business Licences 2013–2026. "
    "Analysis: Andre Santos / Aurora."
)
SOURCE_TAX = (
    "Source: City of Vancouver Open Data — Business Licences 2013–2026 + "
    "Property Tax Assessments. Independent businesses only."
)
SOURCE_COX = (
    "Source: City of Vancouver Open Data — Business Licences + Property Tax "
    "Assessments 2013–2025. Blue = significant (p<0.05). Grey = not significant."
)

def style_ax(ax):
    """Apply standard minimal style to an axes."""
    ax.set_facecolor("white")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(SPINE_GREY)
    ax.spines["bottom"].set_color(SPINE_GREY)
    ax.tick_params(axis="both", which="major", labelsize=9, color=SPINE_GREY)

def source_note(fig, text, y=0.01):
    fig.text(0.01, y, text, fontsize=7, color=SOURCE_GREY, ha="left", va="bottom")

# ═══════════════════════════════════════════════════════════════════════════════
# DATA LOADING (done once, shared across all plots)
# ═══════════════════════════════════════════════════════════════════════════════
print("=" * 70)
print("Loading data...")
print("=" * 70)

# --- Panel v3 (main — used for all steps) ---
# v2 has been superseded by v3. v3 still contains status_last_year, so the
# original step1/step2/step3 event definition (status_last_year in
# ['Gone Out of Business', 'Inactive']) is fully reproducible from v3.
df_v3 = pd.read_csv(f"{PROJECT}/data/processed/commercial-panel-v3.csv", low_memory=False)
print(f"  Panel v3: {len(df_v3):,} rows")

# Alias df_v2 → df_v3 so all downstream code works unchanged
df_v2 = df_v3.copy()

# --- Macro categories ---
macro = pd.read_csv(f"{PROJECT}/data/processed/businesstype_macro_categories.csv")

# --- Land values ---
land = pd.read_csv(f"{PROJECT}/data/processed/neighbourhood_land_values.csv")
print(f"  Land values: {len(land):,} rows, {land['local_area'].nunique()} areas")

# --- Join macro to v2 ---
def attach_macro(df):
    """Strip *Historic* and join macro_category + gentrification_signal."""
    df = df.copy()
    df["_bt"] = df["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
    m = macro.copy()
    m["_bt"] = m["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
    m_dedup = m[["_bt", "macro_category", "gentrification_signal"]].drop_duplicates(subset=["_bt"])
    df = df.merge(m_dedup, on="_bt", how="left").drop(columns=["_bt"])
    return df

df_v2 = attach_macro(df_v2)
print(f"  macro_category joined to v2: {df_v2['macro_category'].notna().sum():,} matched")

# --- v2 survival columns (status_last_year event definition) ---
df_v2["duration"] = df_v2["years_active"]
df_v2["event"]    = df_v2["status_last_year"].isin(["Gone Out of Business", "Inactive"]).astype(int)

# --- Build Cox dataset (exactly as in step5_cox_regression.py) ---
df_cox = df_v3.copy()
df_cox["_bt"] = df_cox["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
macro_copy = macro.copy()
macro_copy["_bt"] = macro_copy["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
macro_dedup = macro_copy[["_bt", "macro_category", "gentrification_signal"]].drop_duplicates(subset=["_bt"])
df_cox = df_cox.merge(macro_dedup, on="_bt", how="left").drop(columns=["_bt"])
df_cox = df_cox[df_cox["is_chain"] == False].copy()

area_map = {
    "Arbutus-Ridge": "Arbutus Ridge",
    "Kensington-Cedar Cottage": "Kensington-Cedar Cottage",
    "Hastings-Sunrise": "Hastings-Sunrise",
    "Riley Park": "Riley Park",
    "Renfrew-Collingwood": "Renfrew-Collingwood",
    "Dunbar-Southlands": "Dunbar-Southlands",
}
df_cox["_area"] = df_cox["localarea"].map(lambda x: area_map.get(x, x) if pd.notna(x) else x)
df_cox["entry_year_4d"] = df_cox["first_year"].apply(lambda y: 2000 + int(y) if y < 100 else int(y))

land_entry = land[["local_area", "year", "median_land_value"]].copy()
land_entry.rename(columns={"local_area": "_area", "year": "entry_year_4d",
                            "median_land_value": "entry_land_value"}, inplace=True)
df_cox = df_cox.merge(land_entry, on=["_area", "entry_year_4d"], how="left")

df_cox["duration"] = df_cox["years_active"]
df_cox["event"]    = df_cox["event_v3"].astype(int)

cox_df = df_cox.dropna(subset=["macro_category", "localarea", "entry_land_value"]).copy()
print(f"  Cox regression sample: {len(cox_df):,} businesses")

top_types = cox_df["macro_category"].value_counts().head(9).index.tolist()
cox_df["type_group"] = cox_df["macro_category"].apply(lambda x: x if x in top_types else "Other")

top_areas = cox_df["localarea"].value_counts().head(10).index.tolist()
cox_df["area_group"] = cox_df["localarea"].apply(lambda x: x if x in top_areas else "Other")

cox_df["log_land_value"] = np.log(cox_df["entry_land_value"])
cox_df["entry_year_centered"] = cox_df["entry_year_4d"] - 2013
emp_median = cox_df["numberofemployees"].median()
cox_df["n_employees"] = cox_df["numberofemployees"].fillna(emp_median)
cox_df["n_employees"] = cox_df["n_employees"].clip(upper=cox_df["n_employees"].quantile(0.99))

# Fit all three Cox models (needed for forest plot + model comparison)
print("\nFitting Cox models (M1, M2, M3)...")
type_dummies = pd.get_dummies(cox_df["type_group"], prefix="type", drop_first=True, dtype=float)
area_dummies = pd.get_dummies(cox_df["area_group"], prefix="area", drop_first=True, dtype=float)

m1_df = pd.concat([cox_df[["duration", "event"]].reset_index(drop=True),
                    type_dummies.reset_index(drop=True)], axis=1)
m1_df = m1_df[m1_df["duration"] > 0]
cph1 = CoxPHFitter()
cph1.fit(m1_df, duration_col="duration", event_col="event")
print(f"  M1 concordance: {cph1.concordance_index_:.4f}")

m2_df = pd.concat([cox_df[["duration", "event"]].reset_index(drop=True),
                    type_dummies.reset_index(drop=True),
                    area_dummies.reset_index(drop=True)], axis=1)
m2_df = m2_df[m2_df["duration"] > 0]
cph2 = CoxPHFitter()
cph2.fit(m2_df, duration_col="duration", event_col="event")
print(f"  M2 concordance: {cph2.concordance_index_:.4f}")

m3_df = pd.concat([cox_df[["duration", "event", "log_land_value",
                              "entry_year_centered", "n_employees"]].reset_index(drop=True),
                    type_dummies.reset_index(drop=True),
                    area_dummies.reset_index(drop=True)], axis=1)
m3_df = m3_df[m3_df["duration"] > 0]
cph3 = CoxPHFitter()
cph3.fit(m3_df, duration_col="duration", event_col="event")
print(f"  M3 concordance: {cph3.concordance_index_:.4f}")
print(f"  M1 AIC: {cph1.AIC_partial_:,.1f}")
print(f"  M2 AIC: {cph2.AIC_partial_:,.1f}")
print(f"  M3 AIC: {cph3.AIC_partial_:,.1f}")

# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 1 — STEP 1: Baseline KM curve (fix risk table overlap)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Plot 1: Step 1 — Baseline survival (fixed risk table)")
print("=" * 70)

BLUE_DARK  = "#1a4a6b"
BLUE_LIGHT = "#cfe2f3"
GRAY_SENS  = "#888888"

df1 = df_v2.copy()
df1_excl = df1[df1["first_year"] != 13].copy()

kmf_full = KaplanMeierFitter(label="All businesses")
kmf_full.fit(df1["duration"], event_observed=df1["event"])

kmf_excl = KaplanMeierFitter(label="Excl. 2013 entrants")
kmf_excl.fit(df1_excl["duration"], event_observed=df1_excl["event"])

def km_at(kmf, t):
    tl = kmf.timeline
    sf = kmf.survival_function_
    idx = tl[tl <= t]
    if len(idx) == 0:
        return 1.0
    return float(sf.loc[idx[-1]].iloc[0])

milestones = [1, 3, 5, 7, 10]
milestone_stats = {t: km_at(kmf_full, t) for t in milestones}
median_full = kmf_full.median_survival_time_

# Number at risk
event_table = kmf_full.event_table
risk_times  = [0, 1, 2, 3, 4, 5, 7, 10, 14]
at_risk_vals = []
for rt in risk_times:
    et_idx = event_table.index[event_table.index <= rt]
    if len(et_idx) == 0:
        at_risk_vals.append(int(df1["duration"].count()))
    else:
        at_risk_vals.append(int(event_table.loc[et_idx[-1], "at_risk"]))

# FIX: Add extra bottom margin so risk table has room, and use smaller fonts
fig, ax = plt.subplots(figsize=(10, 8))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Main KM curve
t  = kmf_full.timeline
sf = kmf_full.survival_function_.values.flatten()
ci = kmf_full.confidence_interval_survival_function_
ax.step(t, sf, where="post", color=BLUE_DARK, linewidth=2.2,
        label=f"All businesses (n={len(df1):,})", zorder=5)
ax.fill_between(t, ci.iloc[:, 0].values, ci.iloc[:, 1].values,
                step="post", color=BLUE_LIGHT, alpha=0.5, label="95% CI", zorder=3)

# Sensitivity curve
t2  = kmf_excl.timeline
sf2 = kmf_excl.survival_function_.values.flatten()
ax.step(t2, sf2, where="post", color=GRAY_SENS, linewidth=1.4, linestyle="--",
        label=f"Excl. 2013 entrants (n={len(df1_excl):,})", zorder=4)

# Milestone annotations
for t_mark in [1, 3, 5, 10]:
    prob = milestone_stats[t_mark]
    ax.axvline(x=t_mark, color="#cccccc", linewidth=0.8, linestyle=":", zorder=2)
    ax.scatter([t_mark], [prob], color=BLUE_DARK, s=45, zorder=6)
    offset_y = 0.04 if t_mark in [1, 3, 10] else -0.065
    va = "bottom" if offset_y > 0 else "top"
    ax.annotate(
        f"{prob:.0%} at {t_mark}yr",
        xy=(t_mark, prob),
        xytext=(t_mark + 0.15, prob + offset_y),
        fontsize=8.5, color=ANNO_COLOR, fontweight="semibold", va=va, ha="left",
    )

# Median line
if not np.isnan(median_full):
    ax.axhline(y=0.5, color=REF_RED, linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
    ax.annotate(f"Median: {median_full:.0f} yr",
                xy=(median_full, 0.5), xytext=(median_full + 0.25, 0.52),
                fontsize=8.5, color=REF_RED, fontweight="semibold")
    ax.scatter([median_full], [0.5], color=REF_RED, s=55, zorder=6, marker="D")

# Risk table below the plot using transform so labels don't overlap numbers
RISK_Y_TOP   = -0.16   # axes fraction
RISK_Y_YEAR  = -0.22   # axes fraction
RISK_FONTSIZE = 7.5

# Row labels — use axes fraction for both x and y to avoid data-space crowding
ax.text(-0.06, RISK_Y_TOP, "At risk:", transform=ax.transAxes,
        fontsize=RISK_FONTSIZE, color="#555555", ha="right", va="top")
for rt, ar in zip(risk_times, at_risk_vals):
    ax.annotate(f"{ar:,}",
                xy=(rt, RISK_Y_TOP), xycoords=("data", "axes fraction"),
                fontsize=RISK_FONTSIZE, color="#555555", ha="center", va="top")

ax.text(-0.06, RISK_Y_YEAR, "Year:", transform=ax.transAxes,
        fontsize=RISK_FONTSIZE, color="#555555", ha="right", va="top")
for rt in risk_times:
    cal_yr = "2013" if rt == 0 else str(int(2013 + rt - 1))
    ax.annotate(cal_yr,
                xy=(rt, RISK_Y_YEAR), xycoords=("data", "axes fraction"),
                fontsize=RISK_FONTSIZE, color="#555555", ha="center", va="top")

# Thin separator line above risk table
ax.axhline(y=0, xmin=0, xmax=1, color=SPINE_GREY, linewidth=0.6, zorder=1)

ax.set_xlim(-0.3, 14.5)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("Years in business", fontsize=11, labelpad=8)
ax.set_ylabel("Probability of survival", fontsize=11, labelpad=8)
ax.set_title("Business Survival in Vancouver (2013–2025)",
             fontsize=14, fontweight="bold", pad=14)

ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.xaxis.set_major_locator(mticker.MultipleLocator(1))

style_ax(ax)
ax.grid(axis="y", color=GRID_GREY, linewidth=0.7, zorder=1)

handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc="upper right", fontsize=9,
          frameon=True, framealpha=0.9, edgecolor=SPINE_GREY)

source_note(fig, SOURCE_BIZ, y=0.002)

# Extra bottom margin so risk table text isn't clipped
plt.tight_layout(rect=[0, 0.12, 1, 1])
out = os.path.join(PLOTS, "step1_baseline_survival.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white", edgecolor="none")
plt.close()
print(f"  Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 2 — STEP 3: Small multiples (2×5) neighbourhood survival
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Plot 2: Step 3 — Neighbourhood survival (small multiples 2×5)")
print("=" * 70)

# Use v2 data (step 3 originally used v2)
df3 = df_v2.copy()
df3 = df3[df3["localarea"].notna()].copy()
df3 = df3[df3["localarea"] != "Out of Town"].copy()
df3 = df3[df3["duration"] >= 1].copy()

# Top 10 neighbourhoods by count
top10_names = df3["localarea"].value_counts().head(10).index.tolist()

# Fit baseline (all areas)
kmf_baseline = KaplanMeierFitter()
kmf_baseline.fit(df3["duration"], event_observed=df3["event"])
t_base = kmf_baseline.timeline
sf_base = kmf_baseline.survival_function_.values.flatten()

# Fit per neighbourhood
kmf_fits = {}
for nb in top10_names:
    sub = df3[df3["localarea"] == nb]
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], event_observed=sub["event"], label=nb)
    med = kmf.median_survival_time_
    med_str = f"{med:.0f}yr" if (not np.isinf(med) and not np.isnan(med)) else ">14yr"
    sf5 = kmf.survival_function_at_times([5]).values[0]
    kmf_fits[nb] = {"kmf": kmf, "n": len(sub), "med_str": med_str, "sf5": sf5}
    print(f"    {nb:<28}  n={len(sub):>6,}  median={med_str}  5yr={sf5:.1%}")

# 10-colour palette (distinct)
PALETTE10 = [
    "#1a4a6b", "#e07b39", "#2a9d5c", "#9b59b6", "#d4a017",
    "#c0392b", "#16a085", "#7f8c8d", "#2980b9", "#884ea0",
]

# Small multiples: 2 rows × 5 cols
fig, axes = plt.subplots(2, 5, figsize=(16, 7), sharey=True)
fig.patch.set_facecolor("white")

for idx, nb in enumerate(top10_names):
    row_i = idx // 5
    col_i = idx % 5
    ax = axes[row_i, col_i]
    ax.set_facecolor("white")

    color = PALETTE10[idx]
    fit_data = kmf_fits[nb]
    kmf = fit_data["kmf"]

    # Grey baseline (all areas, no CI)
    ax.step(t_base, sf_base, where="post", color="#cccccc", linewidth=1.0,
            alpha=0.7, zorder=2)

    # This neighbourhood's KM curve (no CI for cleanliness)
    t_nb = kmf.timeline
    sf_nb = kmf.survival_function_.values.flatten()
    ax.step(t_nb, sf_nb, where="post", color=color, linewidth=1.8, zorder=4)

    # 50% reference line
    ax.axhline(y=0.5, color="#dddddd", linewidth=0.6, linestyle="--", zorder=1)

    # Median dot
    med_val = kmf.median_survival_time_
    if not np.isinf(med_val) and not np.isnan(med_val):
        sf_at_med = kmf.survival_function_at_times([med_val]).values[0]
        ax.scatter([med_val], [sf_at_med], s=30, color=color, zorder=5)

    # Title with n and median
    ax.set_title(
        f"{nb}\n(n={fit_data['n']:,}  med={fit_data['med_str']})",
        fontsize=8.5, fontweight="bold", color=ANNO_COLOR, pad=4,
    )

    # Axis formatting
    ax.set_xlim(0, 14.5)
    ax.set_ylim(0, 1.05)
    ax.xaxis.set_major_locator(mticker.MultipleLocator(5))
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color(SPINE_GREY)
    ax.spines["bottom"].set_color(SPINE_GREY)
    ax.tick_params(axis="both", which="major", labelsize=7.5, color=SPINE_GREY)

    # Only show y-label on leftmost column
    if col_i == 0:
        ax.set_ylabel("Survival", fontsize=8, color=ANNO_COLOR)
    # Only show x-label on bottom row
    if row_i == 1:
        ax.set_xlabel("Years", fontsize=8, color=ANNO_COLOR)

# Shared legend outside the grid
legend_handles = [
    Line2D([0], [0], color="#cccccc", linewidth=1.5, label="All Vancouver (baseline)"),
    Line2D([0], [0], color="#444444", linewidth=2.0, label="Neighbourhood KM curve"),
]
fig.legend(handles=legend_handles, loc="lower center", ncol=2, fontsize=9,
           frameon=True, framealpha=0.9, edgecolor=SPINE_GREY, bbox_to_anchor=(0.5, -0.02))

fig.suptitle(
    "Business Survival by Neighbourhood — Vancouver (2013–2025)\n"
    "Grey = all-areas baseline, Coloured = neighbourhood curve",
    fontsize=13, fontweight="bold", color=ANNO_COLOR, y=1.02,
)

source_note(fig, SOURCE_BIZ, y=0.0)

plt.tight_layout(rect=[0, 0.04, 1, 1])
out = os.path.join(PLOTS, "step3_survival_by_neighbourhood.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white", edgecolor="none")
plt.close()
print(f"  Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 3 — STEP 4: Scatter plot (fix overlapping labels)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Plot 3: Step 4 — Scatter (fixed labels with adjustText)")
print("=" * 70)

# Rebuild the scatter data exactly as in step4_land_value_survival.py
df4 = df_v3.copy()
df4 = df4[df4["is_chain"] == False].copy()
df4 = df4[df4["localarea"].notna()].copy()
df4 = df4[df4["localarea"] != "Out of Town"].copy()
df4["duration"] = df4["years_active"]
df4["event"]    = df4["event_v3"].astype(int)
df4 = df4[df4["duration"] >= 1].copy()

# Build area_name_map (same logic as step4)
lv_areas = set(land["local_area"].unique())
area_name_map4 = {}
for area in df4["localarea"].unique():
    if area in lv_areas:
        area_name_map4[area] = area
    elif area.replace("-", " ") in lv_areas:
        area_name_map4[area] = area.replace("-", " ")
    else:
        area_name_map4[area] = area

df4["localarea_lv"] = df4["localarea"].map(area_name_map4)

# Average land value per neighbourhood (across all years)
lv_avg = land.groupby("local_area")["median_land_value"].mean().reset_index()
lv_avg.columns = ["localarea", "avg_land_value"]

# Fit KM per neighbourhood (n>=100) for scatter
print("  Fitting KM per neighbourhood for scatter...")
nb_stats = []
for nb in df4["localarea"].unique():
    sub = df4[df4["localarea"] == nb]
    if len(sub) < 100:
        continue
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], event_observed=sub["event"])
    med = kmf.median_survival_time_
    sf5 = kmf.survival_function_at_times([5]).values[0]
    nb_lv = area_name_map4.get(nb, nb)
    nb_stats.append({
        "localarea": nb,
        "localarea_lv": nb_lv,
        "n": len(sub),
        "median_survival": med if (not np.isinf(med) and not np.isnan(med)) else 14.0,
        "sf5": sf5,
    })

nb_df = pd.DataFrame(nb_stats)
nb_df = nb_df.merge(lv_avg, left_on="localarea_lv", right_on="localarea", how="inner",
                    suffixes=("", "_lv"))
for col in ["localarea_lv", "localarea_lv_lv"]:
    if col in nb_df.columns:
        nb_df = nb_df.drop(columns=[col])

# Merge Arbutus Ridge naming variants
ar_mask = nb_df["localarea"].isin(["Arbutus Ridge", "Arbutus-Ridge"])
if ar_mask.sum() > 1:
    ar_rows = nb_df[ar_mask]
    combined_n   = ar_rows["n"].sum()
    combined_med = np.average(ar_rows["median_survival"], weights=ar_rows["n"])
    combined_sf5 = np.average(ar_rows["sf5"], weights=ar_rows["n"])
    combined_lv  = ar_rows["avg_land_value"].iloc[0]
    nb_df = nb_df[~ar_mask]
    nb_df = pd.concat([nb_df, pd.DataFrame([{
        "localarea": "Arbutus Ridge",
        "n": combined_n,
        "median_survival": combined_med,
        "sf5": combined_sf5,
        "avg_land_value": combined_lv,
    }])], ignore_index=True)

# Pearson correlation
r, p = scipy_stats.pearsonr(nb_df["avg_land_value"], nb_df["median_survival"])
print(f"  Pearson r = {r:.3f}, p = {p:.4f}")

# Colors by survival tercile
tercile_33 = np.percentile(nb_df["median_survival"], 33)
tercile_66 = np.percentile(nb_df["median_survival"], 66)

def point_color(med):
    if med >= tercile_66:
        return "#2a9d5c"
    elif med <= tercile_33:
        return "#e63946"
    else:
        return "#f4a261"

colors4 = nb_df["median_survival"].apply(point_color)

fig, ax = plt.subplots(figsize=(11, 7.5))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

ax.scatter(
    nb_df["avg_land_value"] / 1e6,
    nb_df["median_survival"],
    c=colors4,
    s=nb_df["n"] / nb_df["n"].max() * 400 + 60,
    alpha=0.80,
    edgecolors=ANNO_COLOR,
    linewidth=0.5,
    zorder=5,
)

# Regression line
x_vals = nb_df["avg_land_value"].values
y_vals = nb_df["median_survival"].values
slope, intercept, *_ = scipy_stats.linregress(x_vals, y_vals)
x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
y_line = slope * x_line + intercept
ax.plot(x_line / 1e6, y_line, color="#888888", linewidth=1.2, linestyle="--",
        alpha=0.6, zorder=3, label=f"Trend (r={r:.2f}, p={p:.3f})")

# Mount Pleasant highlight
mp_row = nb_df[nb_df["localarea"] == "Mount Pleasant"]

# --- Labels with adjustText ---
texts = []
for _, row in nb_df.iterrows():
    # Skip Mount Pleasant — handled separately below with annotation
    if row["localarea"] == "Mount Pleasant":
        continue
    txt = ax.text(
        row["avg_land_value"] / 1e6,
        row["median_survival"],
        row["localarea"],
        fontsize=7.0,
        color=ANNO_COLOR,
        alpha=0.88,
    )
    texts.append(txt)

if HAS_ADJUST_TEXT:
    adjust_text(
        texts,
        ax=ax,
        expand=(1.3, 1.5),
        arrowprops=dict(arrowstyle="-", color="#aaaaaa", lw=0.6),
        force_text=(0.5, 0.8),
        force_points=(0.3, 0.5),
        only_move={"text": "xy", "points": ""},
    )
else:
    # Manual offsets for worst cluster: Downtown, West End, Strathcona, Renfrew, Hastings
    MANUAL_OFFSETS = {
        "Downtown":             (5, -18),
        "West End":             (5, 12),
        "Strathcona":           (-60, -15),
        "Renfrew-Collingwood":  (5, 10),
        "Hastings-Sunrise":     (5, -14),
    }
    for txt in texts:
        label = txt.get_text()
        if label in MANUAL_OFFSETS:
            dx, dy = MANUAL_OFFSETS[label]
            orig_x, orig_y = txt.get_position()
            ax.annotate(
                label,
                xy=(orig_x, orig_y),
                xytext=(dx, dy),
                textcoords="offset points",
                fontsize=7.0,
                color=ANNO_COLOR,
                arrowprops=dict(arrowstyle="-", color="#aaaaaa", lw=0.6),
            )
            txt.set_visible(False)

# Mount Pleasant with arrow annotation (prominent)
if not mp_row.empty:
    mp_lv  = mp_row["avg_land_value"].values[0]
    mp_med = mp_row["median_survival"].values[0]
    ax.scatter([mp_lv / 1e6], [mp_med], s=200, color="#e63946",
               edgecolors=ANNO_COLOR, linewidth=1.5, zorder=8, marker="*")
    ax.annotate(
        "Mount Pleasant",
        xy=(mp_lv / 1e6, mp_med),
        xytext=(12, -22),
        textcoords="offset points",
        fontsize=8.5, color="#e63946", fontweight="bold",
        arrowprops=dict(arrowstyle="->", color="#e63946", lw=1.0),
        zorder=9,
    )

ax.set_xlabel("Average Median Land Value ($M)", fontsize=11, color=ANNO_COLOR)
ax.set_ylabel("Neighbourhood Median Business Survival (years)", fontsize=11, color=ANNO_COLOR)
ax.set_title("Neighbourhood Land Value vs Business Survival (2013–2025)",
             fontsize=13, fontweight="bold", color=ANNO_COLOR, pad=12)

style_ax(ax)
ax.grid(axis="y", color=GRID_GREY, linewidth=0.7, zorder=1)
ax.grid(axis="x", color=GRID_GREY, linewidth=0.7, zorder=1)
ax.legend(loc="upper left", fontsize=9, frameon=True, framealpha=0.92, edgecolor=SPINE_GREY)
ax.annotate("Bubble size = number of businesses", xy=(0.98, 0.02),
            xycoords="axes fraction", fontsize=7.5, color=SOURCE_GREY, ha="right", va="bottom")

source_note(fig, SOURCE_TAX, y=0.01)
plt.tight_layout(rect=[0, 0.05, 1, 1])
out = os.path.join(PLOTS, "step4_land_value_vs_survival_scatter.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white", edgecolor="none")
plt.close()
print(f"  Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 4 — STEP 5: Forest plot (grouped, renamed duplicates)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Plot 4: Step 5 — Forest plot (grouped, no duplicate 'Other')")
print("=" * 70)

summary = cph3.summary.copy()

# ── Rename all coefficients ──────────────────────────────────────────────────
rename_map = {}
for col in summary.index:
    if col == "type_Other":
        rename_map[col] = "Other types"
    elif col.startswith("type_"):
        rename_map[col] = col.replace("type_", "").replace("_", " ")
    elif col == "area_Other":
        rename_map[col] = "Other areas"
    elif col.startswith("area_"):
        rename_map[col] = col.replace("area_", "").replace("_", " ")
    elif col == "log_land_value":
        rename_map[col] = "Log Land Value"
    elif col == "entry_year_centered":
        rename_map[col] = "Entry Year (from 2013)"
    elif col == "n_employees":
        rename_map[col] = "Number of Employees"

summary = summary.rename(index=rename_map)

# ── Classify each covariate into a group ────────────────────────────────────
# Map original index to group
TYPE_COLOR  = "#2166ac"   # blue
AREA_COLOR  = "#2a9d5c"   # green
CONT_COLOR  = "#e07b39"   # orange

group_map = {}
group_color_map = {}

for orig_col in list(cph3.params_.index):
    new_name = rename_map.get(orig_col, orig_col)
    if orig_col.startswith("type_"):
        group_map[new_name] = "Business Type"
        group_color_map[new_name] = TYPE_COLOR
    elif orig_col.startswith("area_"):
        group_map[new_name] = "Neighbourhood"
        group_color_map[new_name] = AREA_COLOR
    else:
        group_map[new_name] = "Continuous"
        group_color_map[new_name] = CONT_COLOR

# ── Sort within each group by HR ────────────────────────────────────────────
GROUP_ORDER = ["Business Type", "Neighbourhood", "Continuous"]

sorted_rows = []
for grp in GROUP_ORDER:
    grp_rows = [(name, row) for name, row in summary.iterrows()
                if group_map.get(name) == grp]
    grp_rows_sorted = sorted(grp_rows, key=lambda x: x[1]["exp(coef)"])
    sorted_rows.extend(grp_rows_sorted)

names_sorted   = [r[0] for r in sorted_rows]
summary_sorted = summary.loc[names_sorted]

hr     = summary_sorted["exp(coef)"]
ci_lo  = summary_sorted["exp(coef) lower 95%"]
ci_hi  = summary_sorted["exp(coef) upper 95%"]
pvals  = summary_sorted["p"]

# Colors: blue if sig (by group), grey if not sig
bar_colors = []
for name in names_sorted:
    grp_color = group_color_map.get(name, "#999999")
    p = pvals[name]
    bar_colors.append(grp_color if p < 0.05 else "#cccccc")

n_rows = len(names_sorted)
y_pos = list(range(n_rows))

# ── Build group separators and labels ───────────────────────────────────────
# Find y positions of group boundaries
group_ranges = {}
for grp in GROUP_ORDER:
    idxs = [i for i, name in enumerate(names_sorted)
             if group_map.get(name) == grp]
    if idxs:
        group_ranges[grp] = (min(idxs), max(idxs))

fig, ax = plt.subplots(figsize=(10, 12))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Horizontal bars + CIs
ax.barh(y_pos, hr - 1, left=1, height=0.6, color=bar_colors, alpha=0.8, edgecolor="none")
ax.errorbar(hr, y_pos, xerr=[hr - ci_lo, ci_hi - hr], fmt="none",
            ecolor="#444444", elinewidth=0.9, capsize=3, capthick=0.9)

# Reference line
ax.axvline(x=1.0, color=REF_RED, linewidth=1.5, linestyle="--", alpha=0.8, zorder=10)
ax.annotate("No effect", xy=(1.01, n_rows - 0.5), fontsize=8, color=REF_RED)

# ── Group dividers and section labels ────────────────────────────────────────
GROUP_LABELS = {
    "Business Type": ("Business Types", TYPE_COLOR),
    "Neighbourhood": ("Neighbourhoods", AREA_COLOR),
    "Continuous": ("Continuous Variables", CONT_COLOR),
}

for grp in GROUP_ORDER:
    if grp not in group_ranges:
        continue
    lo_i, hi_i = group_ranges[grp]
    label, color = GROUP_LABELS[grp]

    # Thin separator line between groups
    if lo_i > 0:
        sep_y = lo_i - 0.5
        ax.axhline(y=sep_y, color=SPINE_GREY, linewidth=1.2, linestyle="-", zorder=2, alpha=0.8)

    # Light background band for each group
    from matplotlib.patches import FancyBboxPatch
    ax.axhspan(lo_i - 0.5, hi_i + 0.5, alpha=0.04, color=color, zorder=0)

ax.set_yticks(y_pos)
ax.set_yticklabels(names_sorted, fontsize=8.5)
ax.set_xlabel("Hazard Ratio (exp(β))", fontsize=11, labelpad=8)
ax.set_title(
    "Cox Regression — Hazard Ratios (Model 3: Full Model)\n"
    "HR > 1 = higher risk of closure, HR < 1 = more durable",
    fontsize=12, fontweight="bold", pad=14,
)

style_ax(ax)
ax.grid(axis="x", color=GRID_GREY, linewidth=0.7)

# Legend for color coding
legend_handles = [
    Line2D([0], [0], marker="s", color="w", markerfacecolor=TYPE_COLOR,
           markersize=10, label="Business type (sig, p<0.05)"),
    Line2D([0], [0], marker="s", color="w", markerfacecolor=AREA_COLOR,
           markersize=10, label="Neighbourhood (sig, p<0.05)"),
    Line2D([0], [0], marker="s", color="w", markerfacecolor=CONT_COLOR,
           markersize=10, label="Continuous var (sig, p<0.05)"),
    Line2D([0], [0], marker="s", color="w", markerfacecolor="#cccccc",
           markersize=10, label="Not significant (p≥0.05)"),
]
ax.legend(handles=legend_handles, loc="lower right", fontsize=8,
          frameon=True, framealpha=0.92, edgecolor=SPINE_GREY)

source_note(fig, SOURCE_COX, y=0.005)
plt.tight_layout(rect=[0, 0.03, 1, 1])
out = os.path.join(PLOTS, "step5_cox_forest_plot.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white", edgecolor="none")
plt.close()
print(f"  Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
# PLOT 5 — STEP 5: Model comparison (fix AIC axis + delta annotations)
# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("Plot 5: Step 5 — Model comparison (fixed AIC axis + delta annotations)")
print("=" * 70)

models      = ["Type only", "Type + Area", "Full model"]
concordances = [cph1.concordance_index_, cph2.concordance_index_, cph3.concordance_index_]
aics        = [cph1.AIC_partial_, cph2.AIC_partial_, cph3.AIC_partial_]

print(f"  Concordances: {[f'{c:.4f}' for c in concordances]}")
print(f"  AICs:         {[f'{a:,.1f}' for a in aics]}")

colors_m = ["#457b9d", "#e9c46a", "#2a9d8f"]

fig, axes = plt.subplots(1, 2, figsize=(11, 5))
fig.patch.set_facecolor("white")

# ── Concordance panel ────────────────────────────────────────────────────────
ax = axes[0]
ax.set_facecolor("white")
bars = ax.bar(models, concordances, color=colors_m, edgecolor="none", width=0.6)

# FIX: y-axis starts at 0.55 to show differences clearly
c_min = min(concordances)
c_max = max(concordances)
y_lo = max(0.55, c_min - 0.005)
y_hi = c_max + 0.012
ax.set_ylim(y_lo, y_hi)

# coin flip reference only shown if visible in axis range
if y_lo <= 0.5:
    ax.axhline(y=0.5, color="#999999", linewidth=0.8, linestyle="--", alpha=0.6)
    ax.annotate("coin flip (0.5)", xy=(0.01, 0.501), xycoords=("axes fraction", "data"),
                fontsize=7, color="#999999", va="bottom")

# Value labels on bars
for bar, val in zip(bars, concordances):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.0005,
            f"{val:.4f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

# Delta annotations between bars (M1→M2, M2→M3)
for i in range(len(concordances) - 1):
    delta = concordances[i + 1] - concordances[i]
    x_mid = i + 0.5
    y_mid = (concordances[i] + concordances[i + 1]) / 2
    ax.annotate(
        f"Δ={delta:+.4f}",
        xy=(x_mid, y_mid + (y_hi - y_lo) * 0.04),
        fontsize=7.5, color="#555555", ha="center", va="bottom",
        fontweight="bold",
    )

ax.set_ylabel("Concordance Index (C-statistic)", fontsize=10)
ax.set_title("Discrimination\n(higher = better)", fontsize=11, fontweight="bold")
style_ax(ax)
ax.tick_params(axis="x", labelsize=9)

# ── AIC panel ────────────────────────────────────────────────────────────────
ax = axes[1]
ax.set_facecolor("white")
bars = ax.bar(models, aics, color=colors_m, edgecolor="none", width=0.6)

# FIX: y-axis starts near min AIC so differences are visible
aic_min = min(aics)
aic_max = max(aics)
aic_range = aic_max - aic_min
# Start axis just below the smallest bar
y_lo_aic = aic_min - aic_range * 0.4
y_hi_aic = aic_max + aic_range * 0.35
ax.set_ylim(y_lo_aic, y_hi_aic)

# Value labels on bars
for bar, val in zip(bars, aics):
    ax.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + aic_range * 0.03,
            f"{val:,.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")

# Delta annotations between bars (M1→M2, M2→M3)
for i in range(len(aics) - 1):
    delta = aics[i + 1] - aics[i]
    x_mid = i + 0.5
    y_mid = (aics[i] + aics[i + 1]) / 2
    ax.annotate(
        f"Δ={delta:+,.0f}",
        xy=(x_mid, y_mid + aic_range * 0.08),
        fontsize=7.5, color="#555555", ha="center", va="bottom",
        fontweight="bold",
    )

ax.set_ylabel("AIC (partial)", fontsize=10)
ax.set_title("Information Criterion\n(lower = better)", fontsize=11, fontweight="bold")

# Format y-axis with comma thousands separator
ax.yaxis.set_major_formatter(mticker.FuncFormatter(lambda x, _: f"{x:,.0f}"))
style_ax(ax)
ax.tick_params(axis="x", labelsize=9)

fig.suptitle("Cox Model Comparison — Adding Variables Improves Fit",
             fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
source_note(fig, SOURCE_COX, y=-0.03)
out = os.path.join(PLOTS, "step5_model_comparison.png")
plt.savefig(out, dpi=150, bbox_inches="tight", facecolor="white", edgecolor="none")
plt.close()
print(f"  Saved: {out}")


# ═══════════════════════════════════════════════════════════════════════════════
print("\n" + "=" * 70)
print("ALL PLOTS REGENERATED SUCCESSFULLY")
print("=" * 70)
print(f"\nOutput directory: {PLOTS}")
print("\nFiles written:")
for fname in [
    "step1_baseline_survival.png",
    "step3_survival_by_neighbourhood.png",
    "step4_land_value_vs_survival_scatter.png",
    "step5_cox_forest_plot.png",
    "step5_model_comparison.png",
]:
    fpath = os.path.join(PLOTS, fname)
    size_kb = os.path.getsize(fpath) / 1024 if os.path.exists(fpath) else 0
    print(f"  {fname:<45}  {size_kb:>7.1f} KB")

print("\nDone.")
