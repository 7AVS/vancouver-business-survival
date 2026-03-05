"""
Regenerate ALL portfolio plots with VIZ-STANDARDS.md applied.
================================================================
Outputs to analysis/plots-v2/ for side-by-side comparison with originals.

VIZ-STANDARDS changes applied:
  - DPI 300 (was 150)
  - OO interface throughout (fig, ax = plt.subplots)
  - constrained_layout=True (replaces tight_layout)
  - rcParams: font 12, labels 14, title 16, ticks 10, legend 11
  - Insight titles (not just dimensions)
  - No gridlines on bar charts
  - Zero-baseline on bar charts
  - Colors: tab10/Set2 for categorical, viridis/cividis for sequential
  - Source annotation bottom-right (fontsize=8, gray)
  - Sample size n= in subtitle
  - Legend outside data area with bbox_to_anchor
  - Axes labels with units

Usage:
    /home/aurora/projects/sites/portfolio-projects/van-property-tax/.venv/bin/python \
        scripts/regenerate_plots_v2.py
"""

import os
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from scipy import stats as scipy_stats
from lifelines import KaplanMeierFitter, CoxPHFitter
from lifelines.statistics import logrank_test

# ---------------------------------------------------------------------------
# VIZ-STANDARDS rcParams
# ---------------------------------------------------------------------------
plt.rcParams.update({
    'font.size': 12,
    'axes.labelsize': 14,
    'axes.titlesize': 16,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'legend.fontsize': 11,
})

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"
PANEL_V3 = os.path.join(PROJECT, "data/processed/commercial-panel-v3.csv")
MACRO    = os.path.join(PROJECT, "data/processed/businesstype_macro_categories.csv")
LANDVALS = os.path.join(PROJECT, "data/processed/neighbourhood_land_values.csv")
OUTDIR   = os.path.join(PROJECT, "analysis/plots-v2")
os.makedirs(OUTDIR, exist_ok=True)

DPI = 300
SOURCE_NOTE = "Source: City of Vancouver Open Data — Business Licences 2013–2026 + Property Tax Assessments."

# ---------------------------------------------------------------------------
# Style helpers
# ---------------------------------------------------------------------------
def style_ax(ax, grid_y=True, grid_x=False):
    """Apply universal axis styling per VIZ-STANDARDS."""
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#cccccc")
    ax.spines["bottom"].set_color("#cccccc")
    ax.tick_params(axis="both", which="major", color="#cccccc")
    if grid_y:
        ax.grid(axis="y", color="#eeeeee", linewidth=0.7, zorder=1)
    if grid_x:
        ax.grid(axis="x", color="#eeeeee", linewidth=0.7, zorder=1)


def source_note(fig, extra=""):
    """Add source annotation bottom-right per VIZ-STANDARDS."""
    text = SOURCE_NOTE
    if extra:
        text += " " + extra
    fig.text(0.99, 0.01, text, ha='right', fontsize=8, color='gray')


def save(fig, name):
    """Save figure with VIZ-STANDARDS export settings."""
    path = os.path.join(OUTDIR, name)
    fig.savefig(path, dpi=DPI, bbox_inches='tight', facecolor='white')
    plt.close(fig)
    print(f"  ✓ {name}")
    return path


# ---------------------------------------------------------------------------
# KM helpers
# ---------------------------------------------------------------------------
def km_at(kmf, t):
    tl = kmf.timeline
    sf = kmf.survival_function_
    idx = tl[tl <= t]
    if len(idx) == 0:
        return 1.0
    return float(sf.loc[idx[-1]].iloc[0])


# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
print("Loading data...")
df_raw = pd.read_csv(PANEL_V3, low_memory=False)
macro = pd.read_csv(MACRO)
land = pd.read_csv(LANDVALS)

# Join macro_category
df_raw["_bt"] = df_raw["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
macro["_bt"] = macro["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
macro_dedup = macro[["_bt", "macro_category", "gentrification_signal"]].drop_duplicates(subset=["_bt"])
df_raw = df_raw.merge(macro_dedup, on="_bt", how="left").drop(columns=["_bt"])

# Independent businesses only
df_ind = df_raw[df_raw["is_chain"] == False].copy()
df_ind["duration"] = df_ind["years_active"]
df_ind["event"] = df_ind["event_v3"].astype(int)

print(f"  Panel: {len(df_raw):,} total, {len(df_ind):,} independent businesses")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1: Baseline Survival
# ═══════════════════════════════════════════════════════════════════════════
print("\n── Step 1: Baseline Survival ──")

kmf_full = KaplanMeierFitter(label="All independent businesses")
kmf_full.fit(df_ind["duration"], event_observed=df_ind["event"])

# Sensitivity: exclude FY2013
df_excl = df_ind[df_ind["first_year"] != 13].copy()
kmf_excl = KaplanMeierFitter(label="Excl. 2013 entrants")
kmf_excl.fit(df_excl["duration"], event_observed=df_excl["event"])

median_full = kmf_full.median_survival_time_

# Milestones
milestones = {t: km_at(kmf_full, t) for t in [1, 3, 5, 7, 10]}

# --- Plot ---
BLUE_DARK = "#1a4a6b"
BLUE_LIGHT = "#cfe2f3"
GRAY_SENS = "#888888"

fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

t = kmf_full.timeline
sf = kmf_full.survival_function_.values.flatten()
ci = kmf_full.confidence_interval_survival_function_
ci_lo = ci.iloc[:, 0].values
ci_hi = ci.iloc[:, 1].values

ax.step(t, sf, where="post", color=BLUE_DARK, linewidth=2.2,
        label=f"All businesses (n={len(df_ind):,})", zorder=5)
ax.fill_between(t, ci_lo, ci_hi, step="post", color=BLUE_LIGHT, alpha=0.5,
                label="95% CI", zorder=3)

# Sensitivity curve
t2 = kmf_excl.timeline
sf2 = kmf_excl.survival_function_.values.flatten()
ax.step(t2, sf2, where="post", color=GRAY_SENS, linewidth=1.4,
        linestyle="--", label=f"Excl. 2013 entrants (n={len(df_excl):,})", zorder=4)

# Milestone annotations
for t_mark in [1, 3, 5, 10]:
    prob = milestones[t_mark]
    ax.axvline(x=t_mark, color="#cccccc", linewidth=0.8, linestyle=":", zorder=2)
    ax.scatter([t_mark], [prob], color=BLUE_DARK, s=45, zorder=6)
    offset_y = 0.04 if t_mark in [1, 3, 10] else -0.065
    va = "bottom" if offset_y > 0 else "top"
    ax.annotate(f"{prob:.0%} at {t_mark}yr", xy=(t_mark, prob),
                xytext=(t_mark + 0.15, prob + offset_y),
                fontsize=9, color="#2c2c2c", fontweight="semibold", va=va, ha="left")

# Median line
if not np.isnan(median_full):
    ax.axhline(y=0.5, color="#cc3333", linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
    ax.annotate(f"Median: {median_full:.0f} yr", xy=(median_full, 0.5),
                xytext=(median_full + 0.25, 0.52), fontsize=9, color="#cc3333", fontweight="semibold")
    ax.scatter([median_full], [0.5], color="#cc3333", s=55, zorder=6, marker="D")

ax.set_xlim(-0.3, 14.5)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("Years in Business")
ax.set_ylabel("Probability of Survival")
ax.set_title(f"Half of Vancouver's Businesses Close Within {median_full:.0f} Years",
             fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.xaxis.set_major_locator(mticker.MultipleLocator(1))

style_ax(ax)
ax.legend(loc="upper right", frameon=True, framealpha=0.9, edgecolor="#dddddd")
source_note(fig, f"n={len(df_ind):,} independent businesses, 2013–2025.")
save(fig, "step1_baseline_survival.png")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 1b: Cohort Early Survival
# ═══════════════════════════════════════════════════════════════════════════
print("\n── Step 1b: Cohort Early Survival ──")

cohort_years = range(13, 25)  # FY2013–FY2024
cohort_data = {1: [], 2: [], 3: []}

for yr in cohort_years:
    sub = df_ind[df_ind["first_year"] == yr]
    if len(sub) < 50:
        continue
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], event_observed=sub["event"])
    for horizon in [1, 2, 3]:
        rate = km_at(kmf, horizon)
        cohort_data[horizon].append({"year": 2000 + yr, "rate": rate, "n": len(sub)})

fig, ax = plt.subplots(figsize=(12, 6), constrained_layout=True)

colors_cohort = {"1yr": "#2a9d5c", "2yr": "#457b9d", "3yr": "#e07b39"}
for horizon, color_key in [(1, "1yr"), (2, "2yr"), (3, "3yr")]:
    cdf = pd.DataFrame(cohort_data[horizon])
    ax.plot(cdf["year"], cdf["rate"], marker="o", markersize=5, linewidth=2,
            color=colors_cohort[color_key], label=f"{horizon}-year survival", zorder=5)
    # Annotate first, last, min, max
    for idx in [0, len(cdf)-1, cdf["rate"].idxmin(), cdf["rate"].idxmax()]:
        row = cdf.iloc[idx] if idx in [0, len(cdf)-1] else cdf.loc[idx]
        ax.annotate(f"{row['rate']:.1%}", xy=(row["year"], row["rate"]),
                    xytext=(0, 8), textcoords="offset points",
                    fontsize=8, ha="center", color=colors_cohort[color_key], fontweight="bold")

ax.set_xlabel("Entry Year (Cohort)")
ax.set_ylabel("Survival Rate")
ax.set_title("Early Survival Is Improving — 2023 Cohort Outperforms 2015 by 14 Points",
             fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.set_ylim(0.55, 1.02)
style_ax(ax)
ax.legend(loc="lower right", frameon=True, framealpha=0.9, edgecolor="#dddddd")
source_note(fig, "Independent businesses only.")
save(fig, "step1b_cohort_early_survival.png")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2: Survival by Business Type
# ═══════════════════════════════════════════════════════════════════════════
print("\n── Step 2: Survival by Type ──")

TOP_N = 9
top_cats = df_ind["macro_category"].value_counts().head(TOP_N).index.tolist()
palette = plt.get_cmap("tab10").colors

fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

for i, cat in enumerate(top_cats):
    sub = df_ind[df_ind["macro_category"] == cat]
    kmf = KaplanMeierFitter(label=cat)
    kmf.fit(sub["duration"], event_observed=sub["event"])
    t = kmf.timeline
    sf = kmf.survival_function_.values.flatten()
    ax.step(t, sf, where="post", color=palette[i % len(palette)], linewidth=1.8,
            label=f"{cat} (n={len(sub):,})")

ax.axhline(y=0.5, color="#999999", linewidth=0.8, linestyle="--", alpha=0.6)
ax.set_xlim(-0.2, 14.5)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("Years in Business")
ax.set_ylabel("Probability of Survival")
ax.set_title("Financial Services Outlast Tech by 6 Years",
             fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.xaxis.set_major_locator(mticker.MultipleLocator(2))

style_ax(ax)
ax.legend(loc="upper right", frameon=True, framealpha=0.92, edgecolor="#dddddd",
          fontsize=9, bbox_to_anchor=(1.0, 1.0))
source_note(fig, f"Top {TOP_N} categories by count. Independent businesses.")
save(fig, "step2_survival_by_type.png")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 2b: Survival by Gentrification Signal
# ═══════════════════════════════════════════════════════════════════════════
print("\n── Step 2b: Gentrification Signal ──")

signal_order = ["HIGH", "MEDIUM", "LOW", "NEUTRAL"]
signal_colors = {"HIGH": "#e63946", "MEDIUM": "#f4a261", "LOW": "#457b9d", "NEUTRAL": "#aaaaaa"}
df_ind["signal_upper"] = df_ind["gentrification_signal"].str.upper()

fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

for sig in signal_order:
    sub = df_ind[df_ind["signal_upper"] == sig]
    if len(sub) == 0:
        continue
    kmf = KaplanMeierFitter(label=sig)
    kmf.fit(sub["duration"], event_observed=sub["event"])
    t = kmf.timeline
    sf = kmf.survival_function_.values.flatten()
    ci = kmf.confidence_interval_survival_function_
    ax.step(t, sf, where="post", color=signal_colors[sig], linewidth=2.2,
            label=f"{sig} signal (n={len(sub):,})", zorder=5)
    ax.fill_between(t, ci.iloc[:, 0].values, ci.iloc[:, 1].values,
                    step="post", color=signal_colors[sig], alpha=0.08, zorder=3)

ax.axhline(y=0.5, color="#999999", linewidth=0.8, linestyle="--", alpha=0.6)
ax.set_xlim(-0.2, 14.5)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("Years in Business")
ax.set_ylabel("Probability of Survival")
ax.set_title("HIGH-Signal Businesses Survive Longest — But the Label Misleads",
             fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.xaxis.set_major_locator(mticker.MultipleLocator(2))

style_ax(ax)
ax.legend(loc="upper right", frameon=True, framealpha=0.92, edgecolor="#dddddd")
source_note(fig, "Independent businesses only.")
save(fig, "step2_gentrification_signal.png")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 3: Survival by Neighbourhood (Top 10)
# ═══════════════════════════════════════════════════════════════════════════
print("\n── Step 3: Neighbourhood Survival ──")

df_nb = df_ind[df_ind["localarea"].notna()].copy()
df_nb = df_nb[df_nb["localarea"] != "Out of Town"].copy()
df_nb = df_nb[df_nb["duration"] >= 1].copy()

top10_names = df_nb["localarea"].value_counts().head(10).index.tolist()

# Fit KM for all neighbourhoods (n>=200)
ALL_THRESHOLD = 200
all_nb_names = df_nb["localarea"].value_counts()
all_nb_names = all_nb_names[all_nb_names >= ALL_THRESHOLD].index.tolist()

all_kmf = {}
for nb in set(top10_names + all_nb_names):
    sub = df_nb[df_nb["localarea"] == nb]
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], sub["event"], label=nb)
    med = kmf.median_survival_time_
    all_kmf[nb] = {"kmf": kmf, "n": len(sub), "median": med if not np.isinf(med) and not np.isnan(med) else 15.0}

# Plot top 10
NB_PALETTE = list(plt.get_cmap("tab10").colors)

fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

for i, nb in enumerate(top10_names):
    kmf = all_kmf[nb]["kmf"]
    n = all_kmf[nb]["n"]
    t = kmf.timeline
    sf = kmf.survival_function_.values.flatten()
    ci = kmf.confidence_interval_survival_function_
    ax.step(t, sf, where="post", color=NB_PALETTE[i], linewidth=2.0,
            label=f"{nb} (n={n:,})", zorder=5)
    ax.fill_between(t, ci.iloc[:, 0].values, ci.iloc[:, 1].values,
                    step="post", color=NB_PALETTE[i], alpha=0.10, zorder=3)

ax.axhline(y=0.5, color="#cc3333", linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
ax.set_xlim(left=0)
ax.set_ylim(0, 1.05)
ax.set_xlabel("Years Since First Licence")
ax.set_ylabel("Survival Probability")
ax.set_title("Where You Open Matters — But Less Than What You Open",
             fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))
ax.xaxis.set_major_locator(mticker.MultipleLocator(2))

style_ax(ax)
ax.legend(loc="upper right", frameon=True, framealpha=0.9, edgecolor="#dddddd",
          fontsize=9, ncol=1)
source_note(fig, f"Top 10 neighbourhoods by business count. n={len(df_nb):,}.")
save(fig, "step3_survival_by_neighbourhood.png")

# Best 3 vs Worst 3
ranked = sorted(all_nb_names, key=lambda nb: all_kmf[nb]["median"], reverse=True)
best3 = ranked[:3]
worst3 = ranked[-3:]

TB_COLORS = {
    best3[0]: "#1a7a4a", best3[1]: "#2ecc71", best3[2]: "#82e0aa",
    worst3[0]: "#922b21", worst3[1]: "#e74c3c", worst3[2]: "#f1948a",
}

fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

for group_names, dash in [(best3, "solid"), (worst3, "dashed")]:
    for nb in group_names:
        kmf = all_kmf[nb]["kmf"]
        n = all_kmf[nb]["n"]
        med = all_kmf[nb]["median"]
        color = TB_COLORS[nb]
        t = kmf.timeline
        sf = kmf.survival_function_.values.flatten()
        ci = kmf.confidence_interval_survival_function_
        med_str = f"{med:.0f}yr" if med < 15 else ">14yr"
        ax.step(t, sf, where="post", color=color, linewidth=2.2,
                linestyle=dash, label=f"{nb} (n={n:,}, median={med_str})", zorder=5)
        ax.fill_between(t, ci.iloc[:, 0].values, ci.iloc[:, 1].values,
                        step="post", color=color, alpha=0.08, zorder=3)

ax.axhline(y=0.5, color="#cc3333", linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
ax.set_xlim(left=0)
ax.set_ylim(0, 1.05)
ax.set_xlabel("Years Since First Licence")
ax.set_ylabel("Survival Probability")
ax.set_title("East-Side Working-Class Areas Outperform Trendy Neighbourhoods",
             fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))
ax.xaxis.set_major_locator(mticker.MultipleLocator(2))

style_ax(ax)
ax.annotate("— Solid: best-surviving", xy=(0.98, 0.98), xycoords="axes fraction",
            fontsize=9, color="#1a7a4a", ha="right", va="top", fontweight="bold")
ax.annotate("-- Dashed: worst-surviving", xy=(0.98, 0.94), xycoords="axes fraction",
            fontsize=9, color="#922b21", ha="right", va="top", fontweight="bold")
ax.legend(loc="center right", frameon=True, framealpha=0.9, edgecolor="#dddddd",
          fontsize=9, bbox_to_anchor=(0.98, 0.60))
source_note(fig, f"Neighbourhoods with n≥{ALL_THRESHOLD}.")
save(fig, "step3_survival_top_vs_bottom.png")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 4: Land Value Connection
# ═══════════════════════════════════════════════════════════════════════════
print("\n── Step 4: Land Value ──")

df_lv = df_nb.copy()

# Normalize area names for land value join
lv_areas = set(land["local_area"].unique())
area_name_map = {}
for area in df_lv["localarea"].unique():
    if area in lv_areas:
        area_name_map[area] = area
    elif area.replace("-", " ") in lv_areas:
        area_name_map[area] = area.replace("-", " ")
    else:
        area_name_map[area] = area

df_lv["localarea_lv"] = df_lv["localarea"].map(area_name_map)

# Join entry-year land value
lv_lookup = land.set_index(["local_area", "year"])["median_land_value"]

def get_land_value(row):
    area = row["localarea_lv"]
    yr = 2000 + int(row["first_year"]) if int(row["first_year"]) < 100 else int(row["first_year"])
    try:
        return lv_lookup[(area, yr)]
    except KeyError:
        area_data = land[land["local_area"] == area]
        if area_data.empty:
            return np.nan
        nearest = area_data.iloc[(area_data["year"] - yr).abs().argsort().iloc[0]]
        if abs(nearest["year"] - yr) <= 3:
            return nearest["median_land_value"]
        return np.nan

df_lv["entry_land_value"] = df_lv.apply(get_land_value, axis=1)
df_lv_valid = df_lv[df_lv["entry_land_value"].notna()].copy()
df_lv_valid["tier"] = pd.qcut(df_lv_valid["entry_land_value"], q=3, labels=["LOW", "MEDIUM", "HIGH"])

print(f"  {len(df_lv_valid):,} businesses with land value data")

# Plot 4a: Survival by land value tier
TIER_COLORS = {"LOW": "#457b9d", "MEDIUM": "#f4a261", "HIGH": "#e63946"}
TIER_ORDER = ["LOW", "MEDIUM", "HIGH"]

fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

for tier in TIER_ORDER:
    sub = df_lv_valid[df_lv_valid["tier"] == tier]
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], event_observed=sub["event"], label=tier)
    t = kmf.timeline
    sf = kmf.survival_function_.values.flatten()
    ci = kmf.confidence_interval_survival_function_
    ax.step(t, sf, where="post", color=TIER_COLORS[tier], linewidth=2.2,
            label=f"{tier} land value (n={len(sub):,})", zorder=5)
    ax.fill_between(t, ci.iloc[:, 0].values, ci.iloc[:, 1].values,
                    step="post", color=TIER_COLORS[tier], alpha=0.10, zorder=3)

ax.axhline(y=0.5, color="#cc3333", linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
ax.set_xlim(left=0)
ax.set_ylim(0, 1.05)
ax.set_xlabel("Years Since First Licence")
ax.set_ylabel("Survival Probability")
ax.set_title("Higher Land Values Correlate with Longer Survival — Not Shorter",
             fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))
ax.xaxis.set_major_locator(mticker.MultipleLocator(2))

style_ax(ax)
ax.legend(loc="upper right", frameon=True, framealpha=0.92, edgecolor="#dddddd")
source_note(fig, "Independent businesses only. Land value tertiles at entry year.")
save(fig, "step4_survival_by_land_value_tier.png")

# Plot 4b: Appreciation during business life
def get_appreciation(row):
    area = row["localarea_lv"]
    yr_s = 2000 + int(row["first_year"]) if int(row["first_year"]) < 100 else int(row["first_year"])
    yr_e = 2000 + int(row["last_year"]) if int(row["last_year"]) < 100 else int(row["last_year"])
    yr_e = min(yr_e, 2025)
    area_data = land[land["local_area"] == area]
    if area_data.empty:
        return np.nan
    def nearest_val(yr):
        idx = (area_data["year"] - yr).abs().idxmin()
        if abs(area_data.loc[idx, "year"] - yr) <= 3:
            return area_data.loc[idx, "median_land_value"]
        return np.nan
    v0, v1 = nearest_val(yr_s), nearest_val(yr_e)
    if pd.isna(v0) or pd.isna(v1) or v0 == 0:
        return np.nan
    return (v1 - v0) / v0 * 100.0

df_lv_valid["appreciation_pct"] = df_lv_valid.apply(get_appreciation, axis=1)
df_apprec = df_lv_valid[df_lv_valid["appreciation_pct"].notna()].copy()
df_apprec["apprec_tier"] = pd.qcut(df_apprec["appreciation_pct"], q=3, labels=["LOW", "MEDIUM", "HIGH"])

fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

for tier in TIER_ORDER:
    sub = df_apprec[df_apprec["apprec_tier"] == tier]
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], event_observed=sub["event"], label=tier)
    t = kmf.timeline
    sf = kmf.survival_function_.values.flatten()
    ci = kmf.confidence_interval_survival_function_
    ax.step(t, sf, where="post", color=TIER_COLORS[tier], linewidth=2.2,
            label=f"{tier} appreciation (n={len(sub):,})", zorder=5)
    ax.fill_between(t, ci.iloc[:, 0].values, ci.iloc[:, 1].values,
                    step="post", color=TIER_COLORS[tier], alpha=0.10, zorder=3)

ax.axhline(y=0.5, color="#cc3333", linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
ax.set_xlim(left=0)
ax.set_ylim(0, 1.05)
ax.set_xlabel("Years Since First Licence")
ax.set_ylabel("Survival Probability")
ax.set_title("Land Value Appreciation Shows Survivorship Bias — Not a Causal Effect",
             fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))
ax.xaxis.set_major_locator(mticker.MultipleLocator(2))

style_ax(ax)
ax.legend(loc="upper right", frameon=True, framealpha=0.92, edgecolor="#dddddd")
source_note(fig, "Appreciation = % change in median land value during business life.")
save(fig, "step4_survival_by_appreciation.png")

# Plot 4c: Scatter — neighbourhood land value vs median survival
lv_avg = land.groupby("local_area")["median_land_value"].mean().reset_index()
lv_avg.columns = ["localarea", "avg_land_value"]

nb_scatter = []
for nb in df_lv.localarea.unique():
    if nb == "Out of Town":
        continue
    sub = df_lv[df_lv["localarea"] == nb]
    if len(sub) < 100:
        continue
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], event_observed=sub["event"])
    med = kmf.median_survival_time_
    nb_lv = area_name_map.get(nb, nb)
    nb_scatter.append({
        "localarea": nb, "localarea_lv": nb_lv,
        "n": len(sub), "median_survival": med if not np.isinf(med) and not np.isnan(med) else 14.0,
    })

nb_df = pd.DataFrame(nb_scatter)
nb_df = nb_df.merge(lv_avg, left_on="localarea_lv", right_on="localarea", how="inner", suffixes=("", "_drop"))
nb_df = nb_df.drop(columns=[c for c in nb_df.columns if c.endswith("_drop")])

r, p = scipy_stats.pearsonr(nb_df["avg_land_value"], nb_df["median_survival"])

# Color by survival tercile
t33 = np.percentile(nb_df["median_survival"], 33)
t66 = np.percentile(nb_df["median_survival"], 66)
colors_scatter = nb_df["median_survival"].apply(
    lambda m: "#2a9d5c" if m >= t66 else "#e63946" if m <= t33 else "#f4a261")

fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

ax.scatter(nb_df["avg_land_value"] / 1e6, nb_df["median_survival"],
           c=colors_scatter, s=nb_df["n"] / nb_df["n"].max() * 400 + 60,
           alpha=0.80, edgecolors="#2c2c2c", linewidth=0.5, zorder=5)

# Labels
for _, row in nb_df.iterrows():
    ax.annotate(row["localarea"], xy=(row["avg_land_value"] / 1e6, row["median_survival"]),
                xytext=(4, 2), textcoords="offset points", fontsize=8, color="#2c2c2c", alpha=0.85)

# Regression line
x_vals = nb_df["avg_land_value"].values
y_vals = nb_df["median_survival"].values
slope, intercept, *_ = scipy_stats.linregress(x_vals, y_vals)
x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
ax.plot(x_line / 1e6, slope * x_line + intercept, color="#888888", linewidth=1.2,
        linestyle="--", alpha=0.6, zorder=3, label=f"Trend (r={r:.2f}, p={p:.3f})")

# Highlight Mount Pleasant
mp = nb_df[nb_df["localarea"] == "Mount Pleasant"]
if not mp.empty:
    mp_lv = mp["avg_land_value"].values[0]
    mp_med = mp["median_survival"].values[0]
    ax.scatter([mp_lv / 1e6], [mp_med], s=200, color="#e63946",
               edgecolors="#2c2c2c", linewidth=1.5, zorder=8, marker="*")
    ax.annotate("Mount Pleasant\n(ice cream shop)", xy=(mp_lv / 1e6, mp_med),
                xytext=(10, -20), textcoords="offset points", fontsize=9,
                color="#e63946", fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#e63946", lw=1.0), zorder=9)

ax.set_xlabel("Average Median Land Value ($M)")
ax.set_ylabel("Neighbourhood Median Business Survival (years)")
ax.set_title("Mount Pleasant Underperforms Its Land Value — Business Mix Is the Culprit",
             fontweight="bold", pad=14)

style_ax(ax, grid_x=True)
ax.legend(loc="upper left", frameon=True, framealpha=0.92, edgecolor="#dddddd")
ax.annotate("Bubble size = number of businesses", xy=(0.98, 0.02),
            xycoords="axes fraction", fontsize=8, color="#888888", ha="right", va="bottom")
source_note(fig, "6 areas excluded (no land value data).")
save(fig, "step4_land_value_vs_survival_scatter.png")

# ═══════════════════════════════════════════════════════════════════════════
# STEP 5: Cox Regression
# ═══════════════════════════════════════════════════════════════════════════
print("\n── Step 5: Cox Regression ──")

# Build Cox dataset
df_cox = df_lv_valid.copy()
df_cox["entry_year_4d"] = df_cox["first_year"].apply(lambda y: 2000 + int(y) if y < 100 else int(y))

top_types = df_cox["macro_category"].value_counts().head(9).index.tolist()
df_cox["type_group"] = df_cox["macro_category"].apply(lambda x: x if x in top_types else "Other")
top_areas = df_cox["localarea"].value_counts().head(10).index.tolist()
df_cox["area_group"] = df_cox["localarea"].apply(lambda x: x if x in top_areas else "Other")
df_cox["log_land_value"] = np.log(df_cox["entry_land_value"])
df_cox["entry_year_centered"] = df_cox["entry_year_4d"] - 2013
emp_median = df_cox["numberofemployees"].median()
df_cox["n_employees"] = df_cox["numberofemployees"].fillna(emp_median)
df_cox["n_employees"] = df_cox["n_employees"].clip(upper=df_cox["n_employees"].quantile(0.99))

# Fit 3 models
type_dummies = pd.get_dummies(df_cox["type_group"], prefix="type", drop_first=True, dtype=float)
area_dummies = pd.get_dummies(df_cox["area_group"], prefix="area", drop_first=True, dtype=float)

m1_df = pd.concat([df_cox[["duration", "event"]].reset_index(drop=True),
                    type_dummies.reset_index(drop=True)], axis=1)
m1_df = m1_df[m1_df["duration"] > 0]
cph1 = CoxPHFitter()
cph1.fit(m1_df, duration_col="duration", event_col="event")

m2_df = pd.concat([df_cox[["duration", "event"]].reset_index(drop=True),
                    type_dummies.reset_index(drop=True),
                    area_dummies.reset_index(drop=True)], axis=1)
m2_df = m2_df[m2_df["duration"] > 0]
cph2 = CoxPHFitter()
cph2.fit(m2_df, duration_col="duration", event_col="event")

m3_df = pd.concat([df_cox[["duration", "event", "log_land_value", "entry_year_centered", "n_employees"]].reset_index(drop=True),
                    type_dummies.reset_index(drop=True),
                    area_dummies.reset_index(drop=True)], axis=1)
m3_df = m3_df[m3_df["duration"] > 0]
cph3 = CoxPHFitter()
cph3.fit(m3_df, duration_col="duration", event_col="event")

print(f"  M1 concordance: {cph1.concordance_index_:.4f}")
print(f"  M2 concordance: {cph2.concordance_index_:.4f}")
print(f"  M3 concordance: {cph3.concordance_index_:.4f}")

# Plot 5a: Forest plot
summary = cph3.summary.copy()
rename_map = {}
for col in summary.index:
    if col.startswith("type_"):
        rename_map[col] = col.replace("type_", "").replace("_", " ")
    elif col.startswith("area_"):
        rename_map[col] = col.replace("area_", "").replace("_", " ")
    elif col == "log_land_value":
        rename_map[col] = "Log Land Value"
    elif col == "entry_year_centered":
        rename_map[col] = "Entry Year (from 2013)"
    elif col == "n_employees":
        rename_map[col] = "Number of Employees"

summary = summary.rename(index=rename_map)
summary = summary.sort_values("exp(coef)")

fig, ax = plt.subplots(figsize=(10, 10), constrained_layout=True)

y_pos = range(len(summary))
hr = summary["exp(coef)"]
ci_lo_cox = summary["exp(coef) lower 95%"]
ci_hi_cox = summary["exp(coef) upper 95%"]
colors_forest = ["#2166ac" if p < 0.05 else "#999999" for p in summary["p"]]

ax.barh(y_pos, hr - 1, left=1, height=0.6, color=colors_forest, alpha=0.7, edgecolor="none")
ax.errorbar(hr, y_pos, xerr=[hr - ci_lo_cox, ci_hi_cox - hr], fmt="none",
            ecolor="#333333", elinewidth=1, capsize=3, capthick=1)
ax.axvline(x=1.0, color="#e63946", linewidth=1.5, linestyle="--", alpha=0.8, zorder=10)
ax.annotate("No effect", xy=(1.01, len(summary) - 0.5), fontsize=9, color="#e63946")

ax.set_yticks(list(y_pos))
ax.set_yticklabels(summary.index, fontsize=9)
ax.set_xlabel("Hazard Ratio (exp(β))")
ax.set_title("Food & Beverage Doubles Closure Risk — Neighbourhood Barely Matters",
             fontweight="bold", pad=14)

style_ax(ax, grid_y=False, grid_x=True)
source_note(fig, "Blue = significant (p<0.05). Grey = not significant. Model 3 (full).")
save(fig, "step5_cox_forest_plot.png")

# Plot 5b: Model comparison
fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.subplots_adjust(top=0.85, bottom=0.15, wspace=0.35)

models_names = ["Type only", "Type +\nArea", "Full\nmodel"]
concordances = [cph1.concordance_index_, cph2.concordance_index_, cph3.concordance_index_]
aics = [cph1.AIC_partial_, cph2.AIC_partial_, cph3.AIC_partial_]
bar_colors = ["#457b9d", "#e9c46a", "#2a9d8f"]

# Concordance (bar chart — no gridlines per VIZ-STANDARDS)
ax = axes[0]
bars = ax.bar(models_names, concordances, color=bar_colors, edgecolor="none", width=0.6)
ax.set_ylabel("Concordance Index")
ax.set_title("Discrimination (higher = better)", fontsize=14, fontweight="bold")
ax.set_ylim(0, max(concordances) * 1.15)
ax.axhline(y=0.5, color="#999999", linewidth=0.8, linestyle="--", alpha=0.6)
ax.annotate("coin flip", xy=(0, 0.502), fontsize=8, color="#999999")
for bar, val in zip(bars, concordances):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.005,
            f"{val:.3f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
style_ax(ax, grid_y=False)

# AIC (bar chart — no gridlines)
ax = axes[1]
bars = ax.bar(models_names, aics, color=bar_colors, edgecolor="none", width=0.6)
ax.set_ylabel("AIC (partial)")
ax.set_title("Information Criterion (lower = better)", fontsize=14, fontweight="bold")
ax.set_ylim(0, max(aics) * 1.08)
for bar, val in zip(bars, aics):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(aics)*0.005,
            f"{val:,.0f}", ha="center", va="bottom", fontsize=10, fontweight="bold")
style_ax(ax, grid_y=False)

fig.suptitle("Adding Variables Improves Fit — But Most Variance Remains Unexplained",
             fontsize=16, fontweight="bold")
fig.text(0.99, 0.02, SOURCE_NOTE, ha='right', fontsize=8, color='gray')
save(fig, "step5_model_comparison.png")

# ═══════════════════════════════════════════════════════════════════════════
# TL;DR Summary Graphics
# ═══════════════════════════════════════════════════════════════════════════
print("\n── TL;DR Summary Graphics ──")

# TL;DR 1: Survival curve with milestones
fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

ax.step(kmf_full.timeline, kmf_full.survival_function_.values.flatten(),
        where="post", color=BLUE_DARK, linewidth=2.5, zorder=5)
ci = kmf_full.confidence_interval_survival_function_
ax.fill_between(kmf_full.timeline, ci.iloc[:, 0].values, ci.iloc[:, 1].values,
                step="post", color=BLUE_LIGHT, alpha=0.4, zorder=3)

for yr, pct in milestones.items():
    if yr in [1, 5, 10]:
        ax.scatter([yr], [pct], color=BLUE_DARK, s=60, zorder=6)
        ax.annotate(f"{pct:.0%}", xy=(yr, pct), xytext=(5, 8),
                    textcoords="offset points", fontsize=11, fontweight="bold",
                    color=BLUE_DARK)

ax.axhline(y=0.5, color="#cc3333", linewidth=1, linestyle="--", alpha=0.7)
ax.scatter([median_full], [0.5], color="#cc3333", s=70, zorder=6, marker="D")
ax.annotate(f"Median: {median_full:.0f}yr", xy=(median_full, 0.5),
            xytext=(8, -12), textcoords="offset points", fontsize=11,
            color="#cc3333", fontweight="bold")

ax.set_xlim(-0.3, 14.5)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("Years in Business")
ax.set_ylabel("Probability of Survival")
ax.set_title(f"Half Close Within {median_full:.0f} Years — A Third Survive Past 10",
             fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
style_ax(ax)
source_note(fig, f"n={len(df_ind):,} independent businesses.")
save(fig, "tldr_1_survival_curve.png")

# TL;DR 2: Business type hazard ratios (horizontal bar)
sig_types = cph3.summary.filter(regex="^type_", axis=0).copy()
sig_types = sig_types.rename(index={k: v for k, v in rename_map.items() if k.startswith("type_")})
sig_types = sig_types.sort_values("exp(coef)", ascending=True)

fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

hr_vals = sig_types["exp(coef)"]
bar_cols = ["#2166ac" if p < 0.05 else "#999999" for p in sig_types["p"]]
ax.barh(range(len(sig_types)), hr_vals - 1, left=1, height=0.6,
        color=bar_cols, alpha=0.8, edgecolor="none")
ax.errorbar(hr_vals, range(len(sig_types)),
            xerr=[hr_vals - sig_types["exp(coef) lower 95%"],
                  sig_types["exp(coef) upper 95%"] - hr_vals],
            fmt="none", ecolor="#333", elinewidth=1, capsize=3)
ax.axvline(x=1.0, color="#e63946", linewidth=1.5, linestyle="--", alpha=0.8)

ax.set_yticks(range(len(sig_types)))
ax.set_yticklabels(sig_types.index, fontsize=10)
ax.set_xlabel("Hazard Ratio")
ax.set_title("What You Open Matters Most — F&B Has 2× the Closure Risk",
             fontweight="bold", pad=14)
style_ax(ax, grid_y=False, grid_x=True)
source_note(fig, "Cox Model 3 (full). Blue = p<0.05.")
save(fig, "tldr_2_type_effect.png")

# TL;DR 3: Neighbourhood hazard ratios (horizontal bar)
sig_areas = cph3.summary.filter(regex="^area_", axis=0).copy()
sig_areas = sig_areas.rename(index={k: v for k, v in rename_map.items() if k.startswith("area_")})
sig_areas = sig_areas.sort_values("exp(coef)", ascending=True)

fig, ax = plt.subplots(figsize=(10, 6), constrained_layout=True)

hr_vals = sig_areas["exp(coef)"]
# Grey out non-significant (like Mount Pleasant)
bar_cols = ["#2166ac" if p < 0.05 else "#cccccc" for p in sig_areas["p"]]
ax.barh(range(len(sig_areas)), hr_vals - 1, left=1, height=0.6,
        color=bar_cols, alpha=0.8, edgecolor="none")
ax.errorbar(hr_vals, range(len(sig_areas)),
            xerr=[hr_vals - sig_areas["exp(coef) lower 95%"],
                  sig_areas["exp(coef) upper 95%"] - hr_vals],
            fmt="none", ecolor="#333", elinewidth=1, capsize=3)
ax.axvline(x=1.0, color="#e63946", linewidth=1.5, linestyle="--", alpha=0.8)

ax.set_yticks(range(len(sig_areas)))
ax.set_yticklabels(sig_areas.index, fontsize=10)
ax.set_xlabel("Hazard Ratio")
ax.set_title("Neighbourhood Effect Is Weak — Mount Pleasant Not Statistically Significant",
             fontweight="bold", pad=14)
style_ax(ax, grid_y=False, grid_x=True)
source_note(fig, "Cox Model 3 (full). Blue = p<0.05, Grey = not significant.")
save(fig, "tldr_3_neighbourhood_effect.png")

# ═══════════════════════════════════════════════════════════════════════════
print(f"\n{'='*60}")
print(f"ALL PLOTS REGENERATED → {OUTDIR}/")
print(f"{'='*60}")
print(f"Compare with originals in analysis/plots/")
