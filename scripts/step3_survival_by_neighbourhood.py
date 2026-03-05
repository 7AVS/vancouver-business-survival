"""
Step 3: Survival Analysis by Neighbourhood — Vancouver Commercial Businesses
=============================================================================
Kaplan-Meier survival curves fitted per neighbourhood, using the backfilled
commercial-panel-v2.csv.

Produces:
  analysis/plots/step3_survival_by_neighbourhood.png  — top 10 neighbourhoods
  analysis/plots/step3_survival_top_vs_bottom.png      — 3 best vs 3 worst

Usage:
    /home/aurora/projects/sites/portfolio-projects/van-property-tax/.venv/bin/python \
        scripts/step3_survival_by_neighbourhood.py
"""

import os
import sys
import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from lifelines import KaplanMeierFitter

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"
PANEL   = os.path.join(PROJECT, "data/processed/commercial-panel-v2.csv")
PLOT10  = os.path.join(PROJECT, "analysis/plots/step3_survival_by_neighbourhood.png")
PLOTTB  = os.path.join(PROJECT, "analysis/plots/step3_survival_top_vs_bottom.png")

# ---------------------------------------------------------------------------
# Style constants (matching Step 1/2)
# ---------------------------------------------------------------------------
ANNO_COLOR = "#2c2c2c"
REF_RED    = "#cc3333"

# 10-colour palette — distinct enough for 10 lines
PALETTE = [
    "#1a4a6b",  # dark blue
    "#e07b39",  # orange
    "#2a9d5c",  # green
    "#9b59b6",  # purple
    "#d4a017",  # gold
    "#c0392b",  # red
    "#16a085",  # teal
    "#7f8c8d",  # grey
    "#2980b9",  # mid blue
    "#884ea0",  # violet
]

# ---------------------------------------------------------------------------
# 1. Load panel
# ---------------------------------------------------------------------------
print("=" * 60)
print("Step 3: Survival by Neighbourhood")
print("=" * 60)
print("\nLoading panel…")
df = pd.read_csv(PANEL, low_memory=False)
print(f"  {len(df):,} rows loaded")

# ---------------------------------------------------------------------------
# 2. Filter to businesses with a localarea
# ---------------------------------------------------------------------------
n_before = len(df)
df = df[df["localarea"].notna()].copy()
n_after = len(df)
print(f"  {n_before - n_after:,} dropped (no localarea) → {n_after:,} remaining")

# Exclude "Out of Town" — not a Vancouver neighbourhood
df = df[df["localarea"] != "Out of Town"]
print(f"  {n_after - len(df):,} 'Out of Town' excluded → {len(df):,} for analysis")

# ---------------------------------------------------------------------------
# 3. Define survival variables
# ---------------------------------------------------------------------------
df["duration"] = df["years_active"]
df["event"]    = df["status_last_year"].isin(["Gone Out of Business", "Inactive"]).astype(int)

n_total   = len(df)
n_events  = df["event"].sum()
n_censored = n_total - n_events
print(f"\nSurvival variables:")
print(f"  Total businesses  : {n_total:,}")
print(f"  Events (exits)    : {n_events:,}  ({100*n_events/n_total:.1f}%)")
print(f"  Censored (active) : {n_censored:,}  ({100*n_censored/n_total:.1f}%)")

# Sanity check: duration must be ≥ 1
bad_dur = (df["duration"] < 1).sum()
if bad_dur > 0:
    print(f"  WARNING: {bad_dur:,} rows have duration < 1 — dropping")
    df = df[df["duration"] >= 1]

# ---------------------------------------------------------------------------
# 4. Fit KM curves for top 10 neighbourhoods by business count
# ---------------------------------------------------------------------------
print("\nFitting KM curves…")
top10_names = df["localarea"].value_counts().head(10).index.tolist()
print(f"  Top 10 neighbourhoods: {top10_names}")

kmf_fits = {}
summary_rows = []

for nb in top10_names:
    sub = df[df["localarea"] == nb]
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], sub["event"], label=nb)
    kmf_fits[nb] = {"kmf": kmf, "n": len(sub)}

    med = kmf.median_survival_time_
    med_str = f"{med:.0f}" if not np.isinf(med) and not np.isnan(med) else ">14"
    sf5 = kmf.survival_function_at_times([5]).values[0]
    summary_rows.append({
        "Neighbourhood": nb,
        "Count": len(sub),
        "Median Survival (yr)": med_str,
        "5-yr Survival Rate": f"{sf5:.1%}",
    })
    print(f"    {nb:<28}  n={len(sub):>6,}  median={med_str:>4}yr  5yr={sf5:.1%}")

# ---------------------------------------------------------------------------
# 5. Helper: draw a KM plot
# ---------------------------------------------------------------------------
def draw_km_plot(neighbourhood_list, kmf_fits, title, outpath, figsize=(10, 7)):
    """Draw KM curves for the given list of neighbourhood names."""
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for i, nb in enumerate(neighbourhood_list):
        kmf = kmf_fits[nb]["kmf"]
        n   = kmf_fits[nb]["n"]
        color = PALETTE[i % len(PALETTE)]

        t  = kmf.timeline
        sf = kmf.survival_function_.values.flatten()
        ci = kmf.confidence_interval_survival_function_
        ci_lo = ci.iloc[:, 0].values
        ci_hi = ci.iloc[:, 1].values

        label = f"{nb} (n={n:,})"
        ax.step(t, sf, where="post", color=color, linewidth=2.0, label=label, zorder=5)
        ax.fill_between(t, ci_lo, ci_hi, step="post", color=color, alpha=0.10, zorder=3)

    # 50% reference line
    ax.axhline(y=0.5, color=REF_RED, linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
    ax.annotate("50% survival", xy=(0.02, 0.505), xycoords=("axes fraction", "data"),
                fontsize=8, color=REF_RED, va="bottom")

    # Axes formatting
    ax.set_xlim(left=0)
    ax.set_ylim(0, 1.05)
    ax.set_xlabel("Years Since First Licence", fontsize=11, color=ANNO_COLOR)
    ax.set_ylabel("Survival Probability", fontsize=11, color=ANNO_COLOR)
    ax.set_title(title, fontsize=13, fontweight="bold", color=ANNO_COLOR, pad=12)

    ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
    ax.xaxis.set_minor_locator(mticker.MultipleLocator(1))
    ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))

    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#dddddd")
    ax.spines["bottom"].set_color("#dddddd")
    ax.tick_params(axis="both", which="major", labelsize=9, color="#dddddd")
    ax.grid(axis="y", color="#eeeeee", linewidth=0.7, zorder=1)

    # Legend
    ax.legend(loc="upper right", fontsize=9, frameon=True, framealpha=0.9,
              edgecolor="#dddddd", ncol=1)

    # Source note
    fig.text(
        0.01, 0.01,
        "Source: City of Vancouver Business Licence Registry (2013–2025). "
        "Analysis: Andre Santos / Aurora.",
        fontsize=7, color="#888888", ha="left", va="bottom",
    )

    plt.tight_layout()
    plt.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {outpath}")

# ---------------------------------------------------------------------------
# 6. Plot 1 — Top 10 neighbourhoods
# ---------------------------------------------------------------------------
print("\nGenerating Plot 1: Top 10 neighbourhoods…")
draw_km_plot(
    neighbourhood_list=top10_names,
    kmf_fits=kmf_fits,
    title="Business Survival by Neighbourhood in Vancouver (2013–2025)",
    outpath=PLOT10,
    figsize=(10, 7),
)

# ---------------------------------------------------------------------------
# 7. Fit KM for ALL neighbourhoods to find best/worst 3 by median survival
# ---------------------------------------------------------------------------
print("\nFitting KM for all neighbourhoods to rank best vs worst…")
ALL_THRESHOLD = 200  # min businesses to be eligible for top/bottom ranking

all_names = df["localarea"].value_counts()
all_names = all_names[all_names >= ALL_THRESHOLD].index.tolist()
print(f"  Neighbourhoods with n≥{ALL_THRESHOLD}: {len(all_names)}")

all_stats = []
for nb in all_names:
    sub = df[df["localarea"] == nb]
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], sub["event"], label=nb)
    med = kmf.median_survival_time_
    # Treat inf median (>50% still alive at study end) as 14+ for ranking
    med_rank = med if (not np.isinf(med) and not np.isnan(med)) else 15.0
    sf5 = kmf.survival_function_at_times([5]).values[0]
    all_stats.append({
        "neighbourhood": nb,
        "n": len(sub),
        "median": med,
        "median_rank": med_rank,
        "sf5": sf5,
        "kmf": kmf,
    })

all_stats_df = pd.DataFrame(all_stats).sort_values("median_rank", ascending=False)

# Add any top10 entries not already in all_stats (those with n < 200 won't be there)
# We want best 3 and worst 3 by median survival among n>=200 neighbourhoods
best3  = all_stats_df.head(3)["neighbourhood"].tolist()
worst3 = all_stats_df.tail(3)["neighbourhood"].tolist()

print(f"  Best 3 (highest median): {best3}")
print(f"  Worst 3 (lowest median): {worst3}")

# Build kmf_fits dict for all neighbourhoods
all_kmf_fits = {row["neighbourhood"]: {"kmf": row["kmf"], "n": row["n"]}
                for _, row in all_stats_df.iterrows()}

# ---------------------------------------------------------------------------
# 8. Plot 2 — 3 best vs 3 worst
# ---------------------------------------------------------------------------
print("\nGenerating Plot 2: 3 best vs 3 worst neighbourhoods…")

# Use green shades for best, red/orange for worst
TB_PALETTE = {
    best3[0]: "#1a7a4a",   # dark green
    best3[1]: "#2ecc71",   # mid green
    best3[2]: "#82e0aa",   # light green
    worst3[0]: "#922b21",  # dark red
    worst3[1]: "#e74c3c",  # mid red
    worst3[2]: "#f1948a",  # light red
}

fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

for group_label, group_names, dash in [("Best", best3, "solid"), ("Worst", worst3, "dashed")]:
    for nb in group_names:
        kmf = all_kmf_fits[nb]["kmf"]
        n   = all_kmf_fits[nb]["n"]
        color = TB_PALETTE[nb]

        t  = kmf.timeline
        sf = kmf.survival_function_.values.flatten()
        ci = kmf.confidence_interval_survival_function_
        ci_lo = ci.iloc[:, 0].values
        ci_hi = ci.iloc[:, 1].values

        med = kmf.median_survival_time_
        med_str = f"{med:.0f}yr" if (not np.isinf(med) and not np.isnan(med)) else ">14yr"
        label = f"{nb} (n={n:,}, median={med_str})"
        ax.step(t, sf, where="post", color=color, linewidth=2.2,
                linestyle=dash, label=label, zorder=5)
        ax.fill_between(t, ci_lo, ci_hi, step="post", color=color, alpha=0.08, zorder=3)

# 50% reference line
ax.axhline(y=0.5, color=REF_RED, linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
ax.annotate("50% survival", xy=(0.02, 0.505), xycoords=("axes fraction", "data"),
            fontsize=8, color=REF_RED, va="bottom")

ax.set_xlim(left=0)
ax.set_ylim(0, 1.05)
ax.set_xlabel("Years Since First Licence", fontsize=11, color=ANNO_COLOR)
ax.set_ylabel("Survival Probability", fontsize=11, color=ANNO_COLOR)
ax.set_title(
    "Business Survival — Best vs Worst Neighbourhoods in Vancouver (2013–2025)",
    fontsize=12, fontweight="bold", color=ANNO_COLOR, pad=12,
)

ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(mticker.MultipleLocator(1))
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))

ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#dddddd")
ax.spines["bottom"].set_color("#dddddd")
ax.tick_params(axis="both", which="major", labelsize=9, color="#dddddd")
ax.grid(axis="y", color="#eeeeee", linewidth=0.7, zorder=1)

# Group legend annotations
ax.annotate("— Solid: best-surviving", xy=(0.98, 0.98), xycoords="axes fraction",
            fontsize=8, color="#1a7a4a", ha="right", va="top", fontweight="bold")
ax.annotate("-- Dashed: worst-surviving", xy=(0.98, 0.94), xycoords="axes fraction",
            fontsize=8, color="#922b21", ha="right", va="top", fontweight="bold")

ax.legend(loc="center right", fontsize=8.5, frameon=True, framealpha=0.9,
          edgecolor="#dddddd", ncol=1, bbox_to_anchor=(0.98, 0.60))

fig.text(
    0.01, 0.01,
    "Source: City of Vancouver Business Licence Registry (2013–2025). "
    "Analysis: Andre Santos / Aurora.",
    fontsize=7, color="#888888", ha="left", va="bottom",
)

plt.tight_layout()
plt.savefig(PLOTTB, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {PLOTTB}")

# ---------------------------------------------------------------------------
# 9. Summary table
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("SUMMARY TABLE — Top 10 Neighbourhoods by Business Count")
print("=" * 60)
summary_df = pd.DataFrame(summary_rows)
print(summary_df.to_string(index=False))

print("\n" + "=" * 60)
print(f"ALL NEIGHBOURHOODS RANKED BY MEDIAN SURVIVAL (n≥{ALL_THRESHOLD})")
print("=" * 60)
rank_df = all_stats_df[["neighbourhood", "n", "median", "sf5"]].copy()
rank_df["median_str"] = rank_df["median"].apply(
    lambda m: f"{m:.0f}" if (not np.isinf(m) and not np.isnan(m)) else ">14"
)
rank_df["sf5_str"] = rank_df["sf5"].apply(lambda x: f"{x:.1%}")
print(rank_df[["neighbourhood", "n", "median_str", "sf5_str"]].rename(columns={
    "neighbourhood": "Neighbourhood",
    "n": "Count",
    "median_str": "Median Survival (yr)",
    "sf5_str": "5-yr Survival",
}).to_string(index=False))

print("\nStep 3 complete.")
