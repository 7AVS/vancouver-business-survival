"""
Step 2: Business Survival by Type — Vancouver Commercial Businesses
======================================================================
Kaplan-Meier survival curves broken down by:
  1. macro_category (top 8 categories by count)
  2. gentrification_signal (HIGH / MEDIUM / LOW / NEUTRAL)

Produces two plots + prints key statistics to stdout.

Usage:
    python3.12 scripts/step2_survival_by_type.py
"""

import os
import warnings

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from matplotlib.lines import Line2D

from lifelines import KaplanMeierFitter

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"
DATA    = os.path.join(PROJECT, "data/processed/commercial-panel-v2.csv")
MACRO   = os.path.join(PROJECT, "data/processed/businesstype_macro_categories.csv")
PLOT1   = os.path.join(PROJECT, "analysis/plots/step2_survival_by_type.png")
PLOT2   = os.path.join(PROJECT, "analysis/plots/step2_survival_by_signal.png")

# ---------------------------------------------------------------------------
# Load & join
# ---------------------------------------------------------------------------
print("Loading panel…")
df = pd.read_csv(DATA, low_memory=False)
print(f"  {len(df):,} rows loaded")

macro = pd.read_csv(MACRO)

# Normalise businesstype for join (strip *Historic* suffix)
df["_bt_clean"] = df["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
macro["_bt_clean"] = macro["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()

macro_dedup = macro[["_bt_clean", "macro_category", "gentrification_signal"]].drop_duplicates(subset=["_bt_clean"])
df = df.merge(macro_dedup, on="_bt_clean", how="left")
df.drop(columns=["_bt_clean"], inplace=True)

matched = df["macro_category"].notna().sum()
print(f"  macro_category joined: {matched:,} / {len(df):,} rows matched")

# ---------------------------------------------------------------------------
# Survival variables
# ---------------------------------------------------------------------------
df["duration"] = df["years_active"]
df["event"]    = df["status_last_year"].isin(["Gone Out of Business", "Inactive"]).astype(int)

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def km_median(kmf):
    """Return median survival time (NaN if curve doesn't reach 0.5)."""
    return kmf.median_survival_time_


def km_at(kmf, t):
    """Return survival probability at time t (closest time <= t)."""
    tl = kmf.timeline
    sf = kmf.survival_function_
    idx = tl[tl <= t]
    if len(idx) == 0:
        return 1.0
    return float(sf.loc[idx[-1]].iloc[0])


# ---------------------------------------------------------------------------
# Plot 1: Survival by macro_category (top N categories)
# ---------------------------------------------------------------------------
TOP_N = 9

cat_counts = df["macro_category"].value_counts()
top_cats   = cat_counts.head(TOP_N).index.tolist()

print(f"\nFitting KM by macro_category (top {TOP_N})…")

# Colour palette — tab10 gives 10 well-separated colours
palette = plt.get_cmap("tab10").colors

fig1, ax1 = plt.subplots(figsize=(10, 7))
fig1.patch.set_facecolor("white")
ax1.set_facecolor("white")

median_table = []

for i, cat in enumerate(top_cats):
    sub = df[df["macro_category"] == cat]
    n   = len(sub)
    kmf = KaplanMeierFitter(label=cat)
    kmf.fit(sub["duration"], event_observed=sub["event"])

    t  = kmf.timeline
    sf = kmf.survival_function_.values.flatten()
    color = palette[i % len(palette)]

    ax1.step(t, sf, where="post", color=color, linewidth=1.8, label=f"{cat} (n={n:,})")

    med = km_median(kmf)
    s3  = km_at(kmf, 3)
    s5  = km_at(kmf, 5)
    median_table.append({
        "macro_category":        cat,
        "n":                     n,
        "median_survival":       med,
        "survival_3yr":          s3,
        "survival_5yr":          s5,
        "gentrification_signal": macro_dedup.loc[macro_dedup["macro_category"] == cat, "gentrification_signal"].mode().iloc[0]
                                 if not macro_dedup.loc[macro_dedup["macro_category"] == cat].empty else "—",
    })
    print(f"  {cat:<35}  n={n:6,}  median={med:5.1f}yr  S(3)={s3:.2%}  S(5)={s5:.2%}")

# Formatting
ax1.axhline(y=0.5, color="#999999", linewidth=0.8, linestyle="--", alpha=0.6)
ax1.annotate("50%", xy=(0.1, 0.51), fontsize=7.5, color="#777777")

ax1.set_xlim(-0.2, 14.5)
ax1.set_ylim(-0.02, 1.05)
ax1.set_xlabel("Years in business", fontsize=11, labelpad=8)
ax1.set_ylabel("Probability of survival", fontsize=11, labelpad=8)
ax1.set_title("Business Survival by Type in Vancouver (2013–2025)", fontsize=13, fontweight="bold", pad=14)

ax1.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax1.xaxis.set_major_locator(mticker.MultipleLocator(2))
ax1.xaxis.set_minor_locator(mticker.MultipleLocator(1))

ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_color("#dddddd")
ax1.spines["bottom"].set_color("#dddddd")
ax1.tick_params(axis="both", which="major", labelsize=9, color="#dddddd")
ax1.grid(axis="y", color="#eeeeee", linewidth=0.7, zorder=1)

ax1.legend(
    loc="upper right",
    fontsize=8.5,
    frameon=True,
    framealpha=0.92,
    edgecolor="#dddddd",
    bbox_to_anchor=(1.0, 1.0),
)

fig1.text(
    0.01, 0.01,
    "Source: City of Vancouver Open Data — Business Licences 2013–2026. Analysis: van-property-tax project.",
    fontsize=7, color="#888888", ha="left",
)

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig(PLOT1, dpi=150, bbox_inches="tight", facecolor="white")
print(f"\nPlot 1 saved → {PLOT1}")
plt.close()

# ---------------------------------------------------------------------------
# Plot 2: Survival by gentrification_signal
# ---------------------------------------------------------------------------
print("\nFitting KM by gentrification_signal…")

# Normalise signal to uppercase for display; preserve count ordering
signal_order   = ["HIGH", "MEDIUM", "LOW", "NEUTRAL"]
signal_colors  = {
    "HIGH":    "#e63946",
    "MEDIUM":  "#f4a261",
    "LOW":     "#457b9d",
    "NEUTRAL": "#aaaaaa",
}

# Normalise signal column
df["signal_upper"] = df["gentrification_signal"].str.upper()

fig2, ax2 = plt.subplots(figsize=(10, 7))
fig2.patch.set_facecolor("white")
ax2.set_facecolor("white")

signal_stats = []

for sig in signal_order:
    sub = df[df["signal_upper"] == sig]
    if len(sub) == 0:
        print(f"  {sig}: no rows, skipping")
        continue
    n   = len(sub)
    kmf = KaplanMeierFitter(label=sig)
    kmf.fit(sub["duration"], event_observed=sub["event"])

    t  = kmf.timeline
    sf = kmf.survival_function_.values.flatten()
    ci = kmf.confidence_interval_survival_function_
    ci_lo = ci.iloc[:, 0].values
    ci_hi = ci.iloc[:, 1].values

    color = signal_colors[sig]

    ax2.step(t, sf, where="post", color=color, linewidth=2.2, label=f"{sig} signal (n={n:,})", zorder=5)
    ax2.fill_between(t, ci_lo, ci_hi, step="post", color=color, alpha=0.08, zorder=3)

    med = km_median(kmf)
    s3  = km_at(kmf, 3)
    s5  = km_at(kmf, 5)
    signal_stats.append({
        "signal": sig,
        "n": n,
        "median_survival": med,
        "survival_3yr": s3,
        "survival_5yr": s5,
    })
    print(f"  {sig:<8}  n={n:6,}  median={med:5.1f}yr  S(3)={s3:.2%}  S(5)={s5:.2%}")

ax2.axhline(y=0.5, color="#999999", linewidth=0.8, linestyle="--", alpha=0.6)
ax2.annotate("50%", xy=(0.1, 0.51), fontsize=7.5, color="#777777")

ax2.set_xlim(-0.2, 14.5)
ax2.set_ylim(-0.02, 1.05)
ax2.set_xlabel("Years in business", fontsize=11, labelpad=8)
ax2.set_ylabel("Probability of survival", fontsize=11, labelpad=8)
ax2.set_title("Business Survival by Gentrification Signal", fontsize=13, fontweight="bold", pad=14)

ax2.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax2.xaxis.set_major_locator(mticker.MultipleLocator(2))
ax2.xaxis.set_minor_locator(mticker.MultipleLocator(1))

ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_color("#dddddd")
ax2.spines["bottom"].set_color("#dddddd")
ax2.tick_params(axis="both", which="major", labelsize=9, color="#dddddd")
ax2.grid(axis="y", color="#eeeeee", linewidth=0.7, zorder=1)

ax2.legend(
    loc="upper right",
    fontsize=9,
    frameon=True,
    framealpha=0.92,
    edgecolor="#dddddd",
)

fig2.text(
    0.01, 0.01,
    "Source: City of Vancouver Open Data — Business Licences 2013–2026. Analysis: van-property-tax project.",
    fontsize=7, color="#888888", ha="left",
)

plt.tight_layout(rect=[0, 0.04, 1, 1])
plt.savefig(PLOT2, dpi=150, bbox_inches="tight", facecolor="white")
print(f"\nPlot 2 saved → {PLOT2}")
plt.close()

# ---------------------------------------------------------------------------
# Key statistics printout
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("MEDIAN SURVIVAL BY MACRO-CATEGORY (sorted)")
print("=" * 65)
med_df = pd.DataFrame(median_table).sort_values("median_survival", ascending=False)

# Get dominant signal per category from the already-merged panel
cat_signal_map = (
    df.groupby("macro_category")["gentrification_signal"]
    .agg(lambda x: x.mode().iloc[0] if len(x) > 0 else "—")
    .to_dict()
)

print(f"\n{'Category':<35} {'n':>7} {'Median':>7} {'S(3yr)':>7} {'S(5yr)':>7} {'Signal'}")
print("-" * 75)
for _, row in med_df.iterrows():
    cat    = row["macro_category"]
    sig    = cat_signal_map.get(cat, "—").upper()
    med    = f"{row['median_survival']:.1f}" if not (isinstance(row['median_survival'], float) and np.isnan(row['median_survival'])) else "N/A"
    print(f"{cat:<35} {row['n']:>7,} {med:>7} {row['survival_3yr']:>7.1%} {row['survival_5yr']:>7.1%} {sig}")

print("\n" + "=" * 65)
print("SURVIVAL BY GENTRIFICATION SIGNAL")
print("=" * 65)
print(f"\n{'Signal':<10} {'n':>7} {'Median':>7} {'S(3yr)':>7} {'S(5yr)':>7}")
print("-" * 45)
for row in sorted(signal_stats, key=lambda x: x["median_survival"], reverse=True):
    med = f"{row['median_survival']:.1f}" if not (isinstance(row['median_survival'], float) and np.isnan(row['median_survival'])) else "N/A"
    print(f"{row['signal']:<10} {row['n']:>7,} {med:>7} {row['survival_3yr']:>7.1%} {row['survival_5yr']:>7.1%}")

print("\n" + "=" * 65)
print("KEY FINDINGS")
print("=" * 65)

longest  = med_df.iloc[0]
shortest = med_df.iloc[-1]
print(f"\nLongest-surviving type : {longest['macro_category']} (median {longest['median_survival']:.1f} yr)")
print(f"Shortest-surviving type: {shortest['macro_category']} (median {shortest['median_survival']:.1f} yr)")

spread = longest["median_survival"] - shortest["median_survival"]
print(f"Spread (median max-min): {spread:.1f} years")

# HIGH signal vs overall baseline
baseline_median = 8.0  # from Step 1
high_stat = next((x for x in signal_stats if x["signal"] == "HIGH"), None)
low_stat  = next((x for x in signal_stats if x["signal"] == "LOW"), None)
if high_stat and low_stat:
    print(f"\nHIGH-signal businesses  : median {high_stat['median_survival']:.1f} yr  (baseline: {baseline_median} yr)")
    print(f"LOW-signal businesses   : median {low_stat['median_survival']:.1f} yr")
    direction = "FASTER" if high_stat["median_survival"] < baseline_median else "SLOWER"
    print(f"HIGH vs baseline        : {direction} ({baseline_median - high_stat['median_survival']:+.1f} yr delta from baseline)")

print("\nDone.")
