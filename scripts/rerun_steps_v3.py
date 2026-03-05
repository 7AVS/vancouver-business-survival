"""
Rerun Steps 1, 2a, 2b, 3 — using panel v3 corrected data
=========================================================
- event_v3 as the event indicator (includes silent exits reclassified as deaths)
- is_chain == False filter (independent businesses only)
- Same plot styling as prior scripts

Usage:
    /home/aurora/projects/sites/portfolio-projects/van-property-tax/.venv/bin/python \
        scripts/rerun_steps_v3.py
"""

import os
import sys
import warnings
import json

import numpy as np
import pandas as pd
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from lifelines import KaplanMeierFitter

warnings.filterwarnings("ignore")

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"
PANEL   = os.path.join(PROJECT, "data/processed/commercial-panel-v3.csv")
MACRO   = os.path.join(PROJECT, "data/processed/businesstype_macro_categories.csv")
PLOTS   = os.path.join(PROJECT, "analysis/plots")

os.makedirs(PLOTS, exist_ok=True)

# ---------------------------------------------------------------------------
# Load data
# ---------------------------------------------------------------------------
print("=" * 65)
print("Loading panel v3…")
df_raw = pd.read_csv(PANEL, low_memory=False)
print(f"  Total rows: {len(df_raw):,}")

# Join macro categories
macro = pd.read_csv(MACRO)
df_raw["_bt_clean"] = df_raw["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
macro["_bt_clean"] = macro["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
macro_dedup = macro[["_bt_clean", "macro_category", "gentrification_signal"]].drop_duplicates(subset=["_bt_clean"])
df_raw = df_raw.merge(macro_dedup, on="_bt_clean", how="left")
df_raw.drop(columns=["_bt_clean"], inplace=True)
print(f"  macro_category joined: {df_raw['macro_category'].notna().sum():,} rows matched")

# Filter to independent businesses only
df = df_raw[df_raw["is_chain"] == False].copy()
print(f"  After is_chain==False filter: {len(df):,} rows")

# Survival variables — use event_v3
df["duration"] = df["years_active"]
df["event"]    = df["event_v3"].astype(int)

n_total    = len(df)
n_events   = int(df["event"].sum())
n_censored = n_total - n_events
pct_events = 100 * n_events / n_total
silent_exits = int(df["silent_exit"].sum())

print(f"\n  Total (independent): {n_total:,}")
print(f"  Events (event_v3=1): {n_events:,}  ({pct_events:.1f}%)")
print(f"    of which silent exits reclassified: {silent_exits:,}")
print(f"  Censored: {n_censored:,}  ({100-pct_events:.1f}%)")

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
def km_at(kmf, t):
    """Return (survival_prob, lower_ci, upper_ci) at time t."""
    tl = kmf.timeline
    sf = kmf.survival_function_
    ci = kmf.confidence_interval_survival_function_
    idx = tl[tl <= t]
    if len(idx) == 0:
        return (1.0, 1.0, 1.0)
    t_use = idx[-1]
    prob = float(sf.loc[t_use].iloc[0])
    lo   = float(ci.loc[t_use].iloc[0])
    hi   = float(ci.loc[t_use].iloc[1])
    return (prob, lo, hi)


def km_median_ci(kmf):
    ci    = kmf.confidence_interval_survival_function_
    t     = kmf.timeline
    ci_lo = ci.iloc[:, 0].values
    ci_hi = ci.iloc[:, 1].values
    idx_lo = np.where(ci_hi < 0.5)[0]
    lo = float(t[idx_lo[0]]) if len(idx_lo) > 0 else np.nan
    idx_hi = np.where(ci_lo >= 0.5)[0]
    hi = float(t[idx_hi[-1]]) if len(idx_hi) > 0 else np.nan
    return lo, hi


# ---------------------------------------------------------------------------
# STEP 1 — Baseline Survival (independent businesses, event_v3)
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("STEP 1: Baseline Survival")
print("=" * 65)

BLUE_DARK  = "#1a4a6b"
BLUE_LIGHT = "#cfe2f3"
GRAY_SENS  = "#888888"
ANNO_COLOR = "#2c2c2c"

# Full independent cohort
kmf_full = KaplanMeierFitter(label="Independent businesses")
kmf_full.fit(df["duration"], event_observed=df["event"])

# Restricted cohort (first_year > 2013)
df_excl = df[df["first_year"] != 13].copy()
kmf_excl = KaplanMeierFitter(label="Excl. 2013 entrants")
kmf_excl.fit(df_excl["duration"], event_observed=df_excl["event"])

# Key stats
milestones = [1, 3, 5, 7, 10]
milestone_stats = {}
print("\nFull cohort milestones:")
for t in milestones:
    prob, lo, hi = km_at(kmf_full, t)
    milestone_stats[t] = {"prob": prob, "lo": lo, "hi": hi}
    print(f"  S({t:2d}yr) = {prob:.3f}  [{lo:.3f}, {hi:.3f}]")

median_full = kmf_full.median_survival_time_
median_lo, median_hi = km_median_ci(kmf_full)
if not np.isnan(median_lo) and not np.isnan(median_hi) and median_lo > median_hi:
    median_lo, median_hi = median_hi, median_lo
print(f"\nMedian survival: {median_full:.1f} yrs  CI [{median_lo}, {median_hi}]")

# RMST
tau = 14
timeline = kmf_full.timeline
t_clip  = timeline[timeline <= tau]
sf_clip = kmf_full.survival_function_.loc[t_clip].values.flatten()
if t_clip[-1] < tau:
    t_clip  = np.append(t_clip, tau)
    sf_clip = np.append(sf_clip, sf_clip[-1])
rmst = np.trapezoid(sf_clip, t_clip)
print(f"RMST (tau={tau}): {rmst:.2f} yrs")

# Restricted cohort stats
milestone_stats_excl = {}
for t in milestones:
    prob, lo, hi = km_at(kmf_excl, t)
    milestone_stats_excl[t] = {"prob": prob, "lo": lo, "hi": hi}
median_excl = kmf_excl.median_survival_time_
print(f"\nRestricted cohort (n={len(df_excl):,}):")
print(f"  Median: {median_excl:.1f} yrs")

# Build plot
print("\nBuilding Step 1 plot…")
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

t  = kmf_full.timeline
sf = kmf_full.survival_function_.values.flatten()
ci = kmf_full.confidence_interval_survival_function_
ci_lo = ci.iloc[:, 0].values
ci_hi = ci.iloc[:, 1].values

ax.step(t, sf, where="post", color=BLUE_DARK, linewidth=2.2,
        label=f"Independent businesses (n={n_total:,})", zorder=5)
ax.fill_between(t, ci_lo, ci_hi, step="post", color=BLUE_LIGHT, alpha=0.5,
                label="95% CI", zorder=3)

t2  = kmf_excl.timeline
sf2 = kmf_excl.survival_function_.values.flatten()
ax.step(t2, sf2, where="post", color=GRAY_SENS, linewidth=1.4,
        linestyle="--", label=f"Excl. 2013 entrants (n={len(df_excl):,})", zorder=4)

anno_milestones = [1, 3, 5, 10]
for t_mark in anno_milestones:
    prob = milestone_stats[t_mark]["prob"]
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

if not np.isnan(median_full):
    ax.axhline(y=0.5, color="#cc3333", linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
    ax.annotate(
        f"Median: {median_full:.0f} yr",
        xy=(median_full, 0.5),
        xytext=(median_full + 0.25, 0.52),
        fontsize=8.5, color="#cc3333", fontweight="semibold",
    )
    ax.scatter([median_full], [0.5], color="#cc3333", s=55, zorder=6, marker="D")

# Number at risk table
event_table = kmf_full.event_table
risk_times  = [0, 1, 2, 3, 4, 5, 7, 10, 14]
at_risk_vals = []
for rt in risk_times:
    et_idx = event_table.index[event_table.index <= rt]
    if len(et_idx) == 0:
        at_risk_vals.append(n_total)
    else:
        at_risk_vals.append(int(event_table.loc[et_idx[-1], "at_risk"]))

table_y = -0.14
ax.annotate("At risk:", xy=(0, table_y), xycoords=("data", "axes fraction"),
            fontsize=7.5, color="#555555", ha="left", va="top")
for i, (rt, ar) in enumerate(zip(risk_times, at_risk_vals)):
    ax.annotate(f"{ar:,}", xy=(rt, table_y), xycoords=("data", "axes fraction"),
                fontsize=7.5, color="#555555", ha="center", va="top")

ax.annotate("Year:", xy=(0, table_y - 0.06), xycoords=("data", "axes fraction"),
            fontsize=7.5, color="#555555", ha="left", va="top")
for rt in risk_times:
    ax.annotate(str(int(2013 + rt - 1)) if rt > 0 else "2013",
                xy=(rt, table_y - 0.06), xycoords=("data", "axes fraction"),
                fontsize=7.5, color="#555555", ha="center", va="top")

ax.set_xlim(-0.3, 14.5)
ax.set_ylim(-0.02, 1.05)
ax.set_xlabel("Years in business", fontsize=11, labelpad=8)
ax.set_ylabel("Probability of survival", fontsize=11, labelpad=8)
ax.set_title("Business Survival in Vancouver — Independent Businesses (2013–2025)", fontsize=14, fontweight="bold", pad=14)
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax.xaxis.set_major_locator(mticker.MultipleLocator(1))
ax.xaxis.set_minor_locator(mticker.MultipleLocator(1))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#dddddd")
ax.spines["bottom"].set_color("#dddddd")
ax.tick_params(axis="both", which="major", labelsize=9, color="#dddddd")
ax.grid(axis="y", color="#eeeeee", linewidth=0.7, zorder=1)
handles, labels = ax.get_legend_handles_labels()
ax.legend(handles, labels, loc="upper right", fontsize=9, frameon=True, framealpha=0.9, edgecolor="#dddddd")
fig.text(0.01, 0.01,
         "Source: City of Vancouver Open Data — Business Licences 2013–2026. "
         "Independent businesses only (chains excluded). event_v3 corrected.",
         fontsize=7, color="#888888", ha="left")

plt.tight_layout(rect=[0, 0.1, 1, 1])
PLOT1 = os.path.join(PLOTS, "step1_baseline_survival.png")
plt.savefig(PLOT1, dpi=150, bbox_inches="tight", facecolor="white")
print(f"Step 1 plot saved → {PLOT1}")
plt.close()

# Collect step 1 stats for notebook update
step1_stats = {
    "n_total": n_total,
    "n_events": n_events,
    "n_censored": n_censored,
    "pct_events": pct_events,
    "silent_exits": silent_exits,
    "milestones": milestone_stats,
    "milestones_excl": milestone_stats_excl,
    "median_full": float(median_full),
    "median_lo": float(median_lo) if not np.isnan(median_lo) else None,
    "median_hi": float(median_hi) if not np.isnan(median_hi) else None,
    "median_excl": float(median_excl),
    "rmst": float(rmst),
}


# ---------------------------------------------------------------------------
# STEP 2a — Survival by Business Type (independent, event_v3)
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("STEP 2a: Survival by Business Type")
print("=" * 65)

TOP_N = 9
cat_counts = df["macro_category"].value_counts()
top_cats   = cat_counts.head(TOP_N).index.tolist()

print(f"\nFitting KM by macro_category (top {TOP_N})…")
palette = plt.get_cmap("tab10").colors

fig1, ax1 = plt.subplots(figsize=(10, 7))
fig1.patch.set_facecolor("white")
ax1.set_facecolor("white")

type_stats = []
for i, cat in enumerate(top_cats):
    sub = df[df["macro_category"] == cat]
    n   = len(sub)
    kmf = KaplanMeierFitter(label=cat)
    kmf.fit(sub["duration"], event_observed=sub["event"])

    t  = kmf.timeline
    sf = kmf.survival_function_.values.flatten()
    color = palette[i % len(palette)]
    ax1.step(t, sf, where="post", color=color, linewidth=1.8,
             label=f"{cat} (n={n:,})")

    med = kmf.median_survival_time_
    s3  = float(kmf.survival_function_at_times([3]).values[0])
    s5  = float(kmf.survival_function_at_times([5]).values[0])
    type_stats.append({"macro_category": cat, "n": n, "median": med, "s3": s3, "s5": s5})
    med_str = f"{med:.1f}" if not (np.isnan(med) or np.isinf(med)) else ">14"
    print(f"  {cat:<35}  n={n:6,}  median={med_str:>5}yr  S(3)={s3:.2%}  S(5)={s5:.2%}")

ax1.axhline(y=0.5, color="#999999", linewidth=0.8, linestyle="--", alpha=0.6)
ax1.annotate("50%", xy=(0.1, 0.51), fontsize=7.5, color="#777777")
ax1.set_xlim(-0.2, 14.5)
ax1.set_ylim(-0.02, 1.05)
ax1.set_xlabel("Years in business", fontsize=11, labelpad=8)
ax1.set_ylabel("Probability of survival", fontsize=11, labelpad=8)
ax1.set_title("Business Survival by Type — Independent Businesses (2013–2025)", fontsize=13, fontweight="bold", pad=14)
ax1.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax1.xaxis.set_major_locator(mticker.MultipleLocator(2))
ax1.xaxis.set_minor_locator(mticker.MultipleLocator(1))
ax1.spines["top"].set_visible(False)
ax1.spines["right"].set_visible(False)
ax1.spines["left"].set_color("#dddddd")
ax1.spines["bottom"].set_color("#dddddd")
ax1.tick_params(axis="both", which="major", labelsize=9, color="#dddddd")
ax1.grid(axis="y", color="#eeeeee", linewidth=0.7, zorder=1)
ax1.legend(loc="upper right", fontsize=8.5, frameon=True, framealpha=0.92, edgecolor="#dddddd",
           bbox_to_anchor=(1.0, 1.0))
fig1.text(0.01, 0.01,
          "Source: City of Vancouver Open Data — Business Licences 2013–2026. "
          "Independent businesses only. event_v3 corrected.",
          fontsize=7, color="#888888", ha="left")
plt.tight_layout(rect=[0, 0.04, 1, 1])
PLOT2a = os.path.join(PLOTS, "step2_survival_by_type.png")
plt.savefig(PLOT2a, dpi=150, bbox_inches="tight", facecolor="white")
print(f"\nStep 2a plot saved → {PLOT2a}")
plt.close()

# Key findings
type_df = pd.DataFrame(type_stats)
longest  = type_df.dropna(subset=["median"]).nlargest(1, "median").iloc[0]
shortest = type_df.dropna(subset=["median"]).nsmallest(1, "median").iloc[0]
spread   = longest["median"] - shortest["median"]
print(f"\nLongest-surviving : {longest['macro_category']} (median {longest['median']:.1f} yr)")
print(f"Shortest-surviving: {shortest['macro_category']} (median {shortest['median']:.1f} yr)")
print(f"Spread            : {spread:.1f} years")


# ---------------------------------------------------------------------------
# STEP 2b — Survival by Gentrification Signal (independent, event_v3)
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("STEP 2b: Survival by Gentrification Signal")
print("=" * 65)

signal_order  = ["HIGH", "MEDIUM", "LOW", "NEUTRAL"]
signal_colors = {
    "HIGH":    "#e63946",
    "MEDIUM":  "#f4a261",
    "LOW":     "#457b9d",
    "NEUTRAL": "#aaaaaa",
}

df["signal_upper"] = df["gentrification_signal"].str.upper()

fig2, ax2 = plt.subplots(figsize=(10, 7))
fig2.patch.set_facecolor("white")
ax2.set_facecolor("white")

signal_stats = []
print("\nFitting KM by gentrification signal…")
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

    ax2.step(t, sf, where="post", color=color, linewidth=2.2,
             label=f"{sig} signal (n={n:,})", zorder=5)
    ax2.fill_between(t, ci_lo, ci_hi, step="post", color=color, alpha=0.08, zorder=3)

    med = kmf.median_survival_time_
    s3  = float(kmf.survival_function_at_times([3]).values[0])
    s5  = float(kmf.survival_function_at_times([5]).values[0])
    signal_stats.append({"signal": sig, "n": n, "median": med, "s3": s3, "s5": s5})
    med_str = f"{med:.1f}" if not (np.isnan(med) or np.isinf(med)) else ">14"
    print(f"  {sig:<8}  n={n:6,}  median={med_str:>5}yr  S(3)={s3:.2%}  S(5)={s5:.2%}")

ax2.axhline(y=0.5, color="#999999", linewidth=0.8, linestyle="--", alpha=0.6)
ax2.annotate("50%", xy=(0.1, 0.51), fontsize=7.5, color="#777777")
ax2.set_xlim(-0.2, 14.5)
ax2.set_ylim(-0.02, 1.05)
ax2.set_xlabel("Years in business", fontsize=11, labelpad=8)
ax2.set_ylabel("Probability of survival", fontsize=11, labelpad=8)
ax2.set_title("Business Survival by Gentrification Signal — Independent Businesses (2013–2025)",
              fontsize=12, fontweight="bold", pad=14)
ax2.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1, decimals=0))
ax2.xaxis.set_major_locator(mticker.MultipleLocator(2))
ax2.xaxis.set_minor_locator(mticker.MultipleLocator(1))
ax2.spines["top"].set_visible(False)
ax2.spines["right"].set_visible(False)
ax2.spines["left"].set_color("#dddddd")
ax2.spines["bottom"].set_color("#dddddd")
ax2.tick_params(axis="both", which="major", labelsize=9, color="#dddddd")
ax2.grid(axis="y", color="#eeeeee", linewidth=0.7, zorder=1)
ax2.legend(loc="upper right", fontsize=9, frameon=True, framealpha=0.92, edgecolor="#dddddd")
fig2.text(0.01, 0.01,
          "Source: City of Vancouver Open Data — Business Licences 2013–2026. "
          "Independent businesses only. event_v3 corrected.",
          fontsize=7, color="#888888", ha="left")
plt.tight_layout(rect=[0, 0.04, 1, 1])
PLOT2b = os.path.join(PLOTS, "step2_survival_by_signal.png")
plt.savefig(PLOT2b, dpi=150, bbox_inches="tight", facecolor="white")
print(f"\nStep 2b plot saved → {PLOT2b}")
plt.close()


# ---------------------------------------------------------------------------
# STEP 3 — Survival by Neighbourhood (independent, has localarea, event_v3)
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("STEP 3: Survival by Neighbourhood")
print("=" * 65)

# Filter to businesses with localarea, not "Out of Town"
df3 = df[df["localarea"].notna()].copy()
df3 = df3[df3["localarea"] != "Out of Town"]
print(f"\nAfter localarea filter: {len(df3):,} rows")

n3_total  = len(df3)
n3_events = int(df3["event"].sum())
print(f"  Events: {n3_events:,}  ({100*n3_events/n3_total:.1f}%)")

PALETTE = [
    "#1a4a6b", "#e07b39", "#2a9d5c", "#9b59b6", "#d4a017",
    "#c0392b", "#16a085", "#7f8c8d", "#2980b9", "#884ea0",
]
REF_RED = "#cc3333"

# Fit top 10 by count
top10_names = df3["localarea"].value_counts().head(10).index.tolist()
print(f"\nTop 10 neighbourhoods: {top10_names}")

kmf_fits   = {}
summary_rows = []

for nb in top10_names:
    sub = df3[df3["localarea"] == nb]
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], sub["event"], label=nb)
    kmf_fits[nb] = {"kmf": kmf, "n": len(sub)}

    med    = kmf.median_survival_time_
    med_str = f"{med:.0f}" if not (np.isinf(med) or np.isnan(med)) else ">14"
    sf5    = float(kmf.survival_function_at_times([5]).values[0])
    summary_rows.append({
        "Neighbourhood": nb,
        "Count": len(sub),
        "Median (yr)": med_str,
        "5-yr Rate": f"{sf5:.1%}",
    })
    print(f"  {nb:<28}  n={len(sub):>6,}  median={med_str:>4}yr  5yr={sf5:.1%}")


def draw_km_plot(neighbourhood_list, kmf_fits, title, outpath, figsize=(10, 7)):
    fig, ax = plt.subplots(figsize=figsize)
    fig.patch.set_facecolor("white")
    ax.set_facecolor("white")

    for i, nb in enumerate(neighbourhood_list):
        kmf   = kmf_fits[nb]["kmf"]
        n     = kmf_fits[nb]["n"]
        color = PALETTE[i % len(PALETTE)]
        t  = kmf.timeline
        sf = kmf.survival_function_.values.flatten()
        ci = kmf.confidence_interval_survival_function_
        ci_lo = ci.iloc[:, 0].values
        ci_hi = ci.iloc[:, 1].values
        label = f"{nb} (n={n:,})"
        ax.step(t, sf, where="post", color=color, linewidth=2.0, label=label, zorder=5)
        ax.fill_between(t, ci_lo, ci_hi, step="post", color=color, alpha=0.10, zorder=3)

    ax.axhline(y=0.5, color=REF_RED, linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
    ax.annotate("50% survival", xy=(0.02, 0.505), xycoords=("axes fraction", "data"),
                fontsize=8, color=REF_RED, va="bottom")

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
    ax.legend(loc="upper right", fontsize=9, frameon=True, framealpha=0.9,
              edgecolor="#dddddd", ncol=1)
    fig.text(0.01, 0.01,
             "Source: City of Vancouver Business Licence Registry (2013–2025). "
             "Independent businesses only. event_v3 corrected.",
             fontsize=7, color="#888888", ha="left", va="bottom")
    plt.tight_layout()
    plt.savefig(outpath, dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Saved: {outpath}")


print("\nGenerating Step 3 plot (top 10)…")
draw_km_plot(
    neighbourhood_list=top10_names,
    kmf_fits=kmf_fits,
    title="Business Survival by Neighbourhood — Independent Businesses (2013–2025)",
    outpath=os.path.join(PLOTS, "step3_survival_by_neighbourhood.png"),
    figsize=(10, 7),
)

# Fit all neighbourhoods (n >= 200) for top vs bottom
ALL_THRESHOLD = 200
print(f"\nFitting all neighbourhoods (n≥{ALL_THRESHOLD}) for top/bottom ranking…")
all_names = df3["localarea"].value_counts()
all_names = all_names[all_names >= ALL_THRESHOLD].index.tolist()
print(f"  Eligible neighbourhoods: {len(all_names)}")

all_stats = []
for nb in all_names:
    sub = df3[df3["localarea"] == nb]
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], sub["event"], label=nb)
    med = kmf.median_survival_time_
    med_rank = med if (not np.isinf(med) and not np.isnan(med)) else 15.0
    sf5 = float(kmf.survival_function_at_times([5]).values[0])
    all_stats.append({"neighbourhood": nb, "n": len(sub),
                      "median": med, "median_rank": med_rank, "sf5": sf5, "kmf": kmf})

all_stats_df = pd.DataFrame(all_stats).sort_values("median_rank", ascending=False)
best3  = all_stats_df.head(3)["neighbourhood"].tolist()
worst3 = all_stats_df.tail(3)["neighbourhood"].tolist()
print(f"  Best 3 : {best3}")
print(f"  Worst 3: {worst3}")

all_kmf_fits = {row["neighbourhood"]: {"kmf": row["kmf"], "n": row["n"]}
                for _, row in all_stats_df.iterrows()}

# Build top vs bottom palette
TB_PALETTE = {
    best3[0]: "#1a7a4a",
    best3[1]: "#2ecc71",
    best3[2]: "#82e0aa",
    worst3[0]: "#922b21",
    worst3[1]: "#e74c3c",
    worst3[2]: "#f1948a",
}

print("\nGenerating Step 3 top vs bottom plot…")
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

for group_label, group_names, dash in [("Best", best3, "solid"), ("Worst", worst3, "dashed")]:
    for nb in group_names:
        kmf   = all_kmf_fits[nb]["kmf"]
        n     = all_kmf_fits[nb]["n"]
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

ax.axhline(y=0.5, color=REF_RED, linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
ax.annotate("50% survival", xy=(0.02, 0.505), xycoords=("axes fraction", "data"),
            fontsize=8, color=REF_RED, va="bottom")
ax.set_xlim(left=0)
ax.set_ylim(0, 1.05)
ax.set_xlabel("Years Since First Licence", fontsize=11, color=ANNO_COLOR)
ax.set_ylabel("Survival Probability", fontsize=11, color=ANNO_COLOR)
ax.set_title("Business Survival — Best vs Worst Neighbourhoods (2013–2025)",
             fontsize=12, fontweight="bold", color=ANNO_COLOR, pad=12)
ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(mticker.MultipleLocator(1))
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#dddddd")
ax.spines["bottom"].set_color("#dddddd")
ax.tick_params(axis="both", which="major", labelsize=9, color="#dddddd")
ax.grid(axis="y", color="#eeeeee", linewidth=0.7, zorder=1)
ax.annotate("— Solid: best-surviving", xy=(0.98, 0.98), xycoords="axes fraction",
            fontsize=8, color="#1a7a4a", ha="right", va="top", fontweight="bold")
ax.annotate("-- Dashed: worst-surviving", xy=(0.98, 0.94), xycoords="axes fraction",
            fontsize=8, color="#922b21", ha="right", va="top", fontweight="bold")
ax.legend(loc="center right", fontsize=8.5, frameon=True, framealpha=0.9,
          edgecolor="#dddddd", ncol=1, bbox_to_anchor=(0.98, 0.60))
fig.text(0.01, 0.01,
         "Source: City of Vancouver Business Licence Registry (2013–2025). "
         "Independent businesses only. event_v3 corrected.",
         fontsize=7, color="#888888", ha="left", va="bottom")
plt.tight_layout()
PLOTTB = os.path.join(PLOTS, "step3_survival_top_vs_bottom.png")
plt.savefig(PLOTTB, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"  Saved: {PLOTTB}")

# Summary table
print("\n" + "=" * 65)
print("STEP 3 SUMMARY TABLE")
print("=" * 65)
summary_df = pd.DataFrame(summary_rows)
print(summary_df.to_string(index=False))

# ---------------------------------------------------------------------------
# Final summary of all key numbers
# ---------------------------------------------------------------------------
print("\n" + "=" * 65)
print("SUMMARY OF KEY NUMBERS FOR NOTEBOOK UPDATE")
print("=" * 65)
print(f"\nSTEP 1:")
print(f"  n_total (independent): {n_total:,}")
print(f"  n_events (event_v3)  : {n_events:,}  ({pct_events:.1f}%)")
print(f"  silent_exits         : {silent_exits:,}")
for t in [1, 3, 5, 7, 10]:
    s = milestone_stats[t]
    print(f"  S({t:2d}yr) = {s['prob']:.3f}  [{s['lo']:.3f}, {s['hi']:.3f}]")
print(f"  Median (full)        : {median_full:.1f} yr  CI [{median_lo:.0f}, {median_hi:.0f}]")
print(f"  Median (restricted)  : {median_excl:.1f} yr")
print(f"  RMST                 : {rmst:.2f} yr")

print(f"\nSTEP 2 (type stats):")
for row in type_stats:
    med_str = f"{row['median']:.1f}" if not (np.isnan(row['median']) or np.isinf(row['median'])) else ">14"
    print(f"  {row['macro_category']:<35}  median={med_str:>5}yr  S(5)={row['s5']:.2%}")

print(f"\nSTEP 2 (signal stats):")
for row in signal_stats:
    med_str = f"{row['median']:.1f}" if not (np.isnan(row['median']) or np.isinf(row['median'])) else ">14"
    print(f"  {row['signal']:<10}  n={row['n']:>7,}  median={med_str:>5}yr  S(5)={row['s5']:.2%}")

print("\nAll steps complete.")
