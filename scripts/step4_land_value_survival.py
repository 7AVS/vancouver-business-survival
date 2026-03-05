"""
Step 4: Business Survival vs Land Value — Vancouver Commercial Businesses
=========================================================================
Connects business survival to the property tax land value of the neighbourhood
where a business opened. Four analyses:

  1. Survival by entry-year land value tier (LOW / MEDIUM / HIGH tertile)
  2. Survival by cumulative land value appreciation during the business's life
  3. Scatter: avg neighbourhood land value vs neighbourhood median survival
  4. Log-rank pairwise tests between land value tiers

Produces:
  analysis/plots/step4_survival_by_land_value_tier.png
  analysis/plots/step4_survival_by_appreciation.png
  analysis/plots/step4_land_value_vs_survival_scatter.png

Usage:
    /home/aurora/projects/sites/portfolio-projects/van-property-tax/.venv/bin/python \
        scripts/step4_land_value_survival.py
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
from scipy import stats
from lifelines import KaplanMeierFitter
from lifelines.statistics import logrank_test

# ---------------------------------------------------------------------------
# Paths
# ---------------------------------------------------------------------------
PROJECT  = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"
PANEL    = os.path.join(PROJECT, "data/processed/commercial-panel-v3.csv")
LANDVALS = os.path.join(PROJECT, "data/processed/neighbourhood_land_values.csv")

PLOT_TIER   = os.path.join(PROJECT, "analysis/plots/step4_survival_by_land_value_tier.png")
PLOT_APPREC = os.path.join(PROJECT, "analysis/plots/step4_survival_by_appreciation.png")
PLOT_SCATTER= os.path.join(PROJECT, "analysis/plots/step4_land_value_vs_survival_scatter.png")

# ---------------------------------------------------------------------------
# Style constants (matching Steps 1–3)
# ---------------------------------------------------------------------------
ANNO_COLOR = "#2c2c2c"
REF_RED    = "#cc3333"

TIER_COLORS = {
    "LOW":    "#457b9d",   # blue
    "MEDIUM": "#f4a261",   # orange
    "HIGH":   "#e63946",   # red
}
TIER_ORDER = ["LOW", "MEDIUM", "HIGH"]

# ---------------------------------------------------------------------------
# 1. Load data
# ---------------------------------------------------------------------------
print("=" * 60)
print("Step 4: Business Survival vs Land Value")
print("=" * 60)

print("\nLoading panel v3…")
df = pd.read_csv(PANEL, low_memory=False)
print(f"  {len(df):,} rows loaded")

print("Loading land values…")
lv = pd.read_csv(LANDVALS)
print(f"  {len(lv):,} land value rows, {lv['local_area'].nunique()} areas covered")
print(f"  Areas in land values: {sorted(lv['local_area'].unique())}")

# ---------------------------------------------------------------------------
# 2. Filter panel: independent businesses with localarea
# ---------------------------------------------------------------------------
df = df[df["is_chain"] == False].copy()
df = df[df["localarea"].notna()].copy()
df = df[df["localarea"] != "Out of Town"].copy()
df["duration"] = df["years_active"]
df["event"]    = df["event_v3"].astype(int)

# Sanity: drop zero-duration rows
df = df[df["duration"] >= 1].copy()

# Normalize localarea to use spaces (the land value file uses spaces, not hyphens)
# e.g. "Arbutus-Ridge" -> "Arbutus Ridge"
df["localarea_norm"] = df["localarea"].str.replace("-", " ").str.strip()
# But preserve names that already have spaces + hyphens correctly
# (Renfrew-Collingwood, Dunbar-Southlands, etc. are correct in land values already)
# Build explicit map from observed panel values to land value names
area_name_map = {}
lv_areas = set(lv["local_area"].unique())
for area in df["localarea"].unique():
    if area in lv_areas:
        area_name_map[area] = area
    elif area.replace("-", " ") in lv_areas:
        area_name_map[area] = area.replace("-", " ")
    else:
        area_name_map[area] = area  # keep as-is (will produce NaN in join)

df["localarea_lv"] = df["localarea"].map(area_name_map)

print(f"\nAfter filtering (independent, has localarea, duration>=1):")
print(f"  {len(df):,} businesses")
print(f"  Events (exits): {df['event'].sum():,} ({100*df['event'].mean():.1f}%)")

# ---------------------------------------------------------------------------
# 3. Join land value at entry year
#    For each business: get median_land_value in localarea at first_year
# ---------------------------------------------------------------------------
lv_lookup = lv.set_index(["local_area", "year"])["median_land_value"]

covered_areas = set(lv["local_area"].unique())
panel_areas   = set(df["localarea_lv"].unique())
missing_areas = panel_areas - covered_areas

print(f"\nLand value coverage:")
print(f"  Panel has {len(panel_areas)} distinct local areas")
print(f"  Land values cover {len(covered_areas)} areas")
print(f"  Missing areas (no land value data): {sorted(missing_areas)}")

def get_land_value(row, lookup, lv_df):
    """Return median_land_value for a business's localarea in its first_year.
    Falls back to nearest available year if exact year is missing.
    NOTE: first_year is stored as 2-digit offset from 2000 (e.g. 13 = 2013)."""
    area = row["localarea_lv"]
    yr_raw = int(row["first_year"])
    # Convert 2-digit year to 4-digit (13 → 2013, 26 → 2026)
    year = 2000 + yr_raw if yr_raw < 100 else yr_raw
    try:
        return lookup[(area, year)]
    except KeyError:
        # Try nearby years (±3 years)
        area_data = lv_df[lv_df["local_area"] == area]
        if area_data.empty:
            return np.nan
        available_years = area_data["year"].values
        nearest = available_years[np.argmin(np.abs(available_years - year))]
        if abs(nearest - year) <= 3:
            return lv_df[(lv_df["local_area"] == area) & (lv_df["year"] == nearest)]["median_land_value"].values[0]
        return np.nan

print("\nJoining entry-year land values…")
df["entry_land_value"] = df.apply(lambda r: get_land_value(r, lv_lookup, lv), axis=1)

n_with_lv = df["entry_land_value"].notna().sum()
n_total   = len(df)
print(f"  Businesses with entry land value: {n_with_lv:,} of {n_total:,} ({100*n_with_lv/n_total:.1f}%)")

# Work with businesses that have land value data
df_lv = df[df["entry_land_value"].notna()].copy()

# ---------------------------------------------------------------------------
# 4. Analysis 1: Survival by Entry Land Value Tier
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("ANALYSIS 1: Survival by Entry Land Value Tier")
print("=" * 60)

# Assign tertiles
df_lv["tier"] = pd.qcut(df_lv["entry_land_value"], q=3,
                         labels=["LOW", "MEDIUM", "HIGH"])

tier_counts = df_lv["tier"].value_counts().sort_index()
print(f"\nTertile breakpoints:")
print(f"  LOW:    < ${df_lv[df_lv['tier']=='LOW']['entry_land_value'].max():,.0f}")
print(f"  MEDIUM: ${df_lv[df_lv['tier']=='MEDIUM']['entry_land_value'].min():,.0f} – ${df_lv[df_lv['tier']=='MEDIUM']['entry_land_value'].max():,.0f}")
print(f"  HIGH:   > ${df_lv[df_lv['tier']=='HIGH']['entry_land_value'].min():,.0f}")

print("\nFitting KM curves by land value tier…")
tier_kmf = {}
tier_stats = []

for tier in TIER_ORDER:
    sub = df_lv[df_lv["tier"] == tier]
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], event_observed=sub["event"], label=tier)
    tier_kmf[tier] = {"kmf": kmf, "n": len(sub)}

    med = kmf.median_survival_time_
    med_str = f"{med:.0f}" if (not np.isinf(med) and not np.isnan(med)) else ">14"
    sf5 = kmf.survival_function_at_times([5]).values[0]
    sf3 = kmf.survival_function_at_times([3]).values[0]
    tier_stats.append({
        "Tier": tier,
        "Count": len(sub),
        "Median Survival (yr)": med_str,
        "3-yr Rate": f"{sf3:.1%}",
        "5-yr Rate": f"{sf5:.1%}",
    })
    print(f"  {tier:<8}  n={len(sub):>6,}  median={med_str:>4}yr  3yr={sf3:.1%}  5yr={sf5:.1%}")

# Plot
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

for tier in TIER_ORDER:
    kmf = tier_kmf[tier]["kmf"]
    n   = tier_kmf[tier]["n"]
    color = TIER_COLORS[tier]
    t  = kmf.timeline
    sf = kmf.survival_function_.values.flatten()
    ci = kmf.confidence_interval_survival_function_
    ax.step(t, sf, where="post", color=color, linewidth=2.2,
            label=f"{tier} land value (n={n:,})", zorder=5)
    ax.fill_between(t, ci.iloc[:, 0].values, ci.iloc[:, 1].values,
                    step="post", color=color, alpha=0.10, zorder=3)

ax.axhline(y=0.5, color=REF_RED, linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
ax.annotate("50% survival", xy=(0.02, 0.505), xycoords=("axes fraction", "data"),
            fontsize=8, color=REF_RED, va="bottom")

ax.set_xlim(left=0)
ax.set_ylim(0, 1.05)
ax.set_xlabel("Years Since First Licence", fontsize=11, color=ANNO_COLOR)
ax.set_ylabel("Survival Probability", fontsize=11, color=ANNO_COLOR)
ax.set_title("Business Survival by Entry Land Value Tier (2013–2025)",
             fontsize=13, fontweight="bold", color=ANNO_COLOR, pad=12)
ax.xaxis.set_major_locator(mticker.MultipleLocator(2))
ax.xaxis.set_minor_locator(mticker.MultipleLocator(1))
ax.yaxis.set_major_formatter(mticker.PercentFormatter(xmax=1.0, decimals=0))
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#dddddd")
ax.spines["bottom"].set_color("#dddddd")
ax.tick_params(axis="both", which="major", labelsize=9, color="#dddddd")
ax.grid(axis="y", color="#eeeeee", linewidth=0.7, zorder=1)
ax.legend(loc="upper right", fontsize=9.5, frameon=True, framealpha=0.92, edgecolor="#dddddd")
fig.text(0.01, 0.01,
         "Source: City of Vancouver Open Data — Business Licences 2013–2026 + Property Tax Assessments. "
         "Independent businesses only. event_v3 corrected.",
         fontsize=7, color="#888888", ha="left", va="bottom")
plt.tight_layout()
plt.savefig(PLOT_TIER, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"\n  Saved: {PLOT_TIER}")

print("\nTier Stats Summary:")
tier_stats_df = pd.DataFrame(tier_stats)
print(tier_stats_df.to_string(index=False))

# ---------------------------------------------------------------------------
# 5. Analysis 2: Survival by Land Value Appreciation
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("ANALYSIS 2: Survival by Land Value Appreciation During Business Life")
print("=" * 60)

lv_by_area_year = lv.set_index(["local_area", "year"])["median_land_value"]

def get_appreciation(row, lv_df):
    """Compute cumulative_growth_pct from first_year to min(last_year, 2025) for the business's area.
    NOTE: first_year/last_year stored as 2-digit offsets from 2000."""
    area      = row["localarea_lv"]
    yr_start_raw = int(row["first_year"])
    yr_end_raw   = int(row["last_year"])
    yr_start = 2000 + yr_start_raw if yr_start_raw < 100 else yr_start_raw
    yr_end   = min((2000 + yr_end_raw if yr_end_raw < 100 else yr_end_raw), 2025)

    area_data = lv_df[lv_df["local_area"] == area]
    if area_data.empty:
        return np.nan

    # Get land value at start and end
    def nearest_val(yr):
        sub = area_data.copy()
        idx = (sub["year"] - yr).abs().idxmin()
        if abs(sub.loc[idx, "year"] - yr) <= 3:
            return sub.loc[idx, "median_land_value"]
        return np.nan

    val_start = nearest_val(yr_start)
    val_end   = nearest_val(yr_end)

    if pd.isna(val_start) or pd.isna(val_end) or val_start == 0:
        return np.nan

    return (val_end - val_start) / val_start * 100.0

print("\nComputing appreciation for each business…")
df_lv["appreciation_pct"] = df_lv.apply(lambda r: get_appreciation(r, lv), axis=1)

n_with_apprec = df_lv["appreciation_pct"].notna().sum()
print(f"  Businesses with appreciation data: {n_with_apprec:,}")

df_apprec = df_lv[df_lv["appreciation_pct"].notna()].copy()

# Tertiles
df_apprec["apprec_tier"] = pd.qcut(df_apprec["appreciation_pct"], q=3,
                                    labels=["LOW", "MEDIUM", "HIGH"])

print(f"\nAppreciation tertile breakpoints:")
print(f"  LOW:    < {df_apprec[df_apprec['apprec_tier']=='LOW']['appreciation_pct'].max():.1f}%")
print(f"  MEDIUM: {df_apprec[df_apprec['apprec_tier']=='MEDIUM']['appreciation_pct'].min():.1f}% – {df_apprec[df_apprec['apprec_tier']=='MEDIUM']['appreciation_pct'].max():.1f}%")
print(f"  HIGH:   > {df_apprec[df_apprec['apprec_tier']=='HIGH']['appreciation_pct'].min():.1f}%")

print("\nFitting KM curves by appreciation tier…")
apprec_kmf = {}
apprec_stats = []

for tier in TIER_ORDER:
    sub = df_apprec[df_apprec["apprec_tier"] == tier]
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], event_observed=sub["event"], label=tier)
    apprec_kmf[tier] = {"kmf": kmf, "n": len(sub)}

    med = kmf.median_survival_time_
    med_str = f"{med:.0f}" if (not np.isinf(med) and not np.isnan(med)) else ">14"
    sf5 = kmf.survival_function_at_times([5]).values[0]
    sf3 = kmf.survival_function_at_times([3]).values[0]
    apprec_stats.append({
        "Tier": tier,
        "Count": len(sub),
        "Median Survival (yr)": med_str,
        "3-yr Rate": f"{sf3:.1%}",
        "5-yr Rate": f"{sf5:.1%}",
    })
    print(f"  {tier:<8}  n={len(sub):>6,}  median={med_str:>4}yr  3yr={sf3:.1%}  5yr={sf5:.1%}")

# Plot
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

for tier in TIER_ORDER:
    kmf = apprec_kmf[tier]["kmf"]
    n   = apprec_kmf[tier]["n"]
    color = TIER_COLORS[tier]
    t  = kmf.timeline
    sf = kmf.survival_function_.values.flatten()
    ci = kmf.confidence_interval_survival_function_
    ax.step(t, sf, where="post", color=color, linewidth=2.2,
            label=f"{tier} appreciation (n={n:,})", zorder=5)
    ax.fill_between(t, ci.iloc[:, 0].values, ci.iloc[:, 1].values,
                    step="post", color=color, alpha=0.10, zorder=3)

ax.axhline(y=0.5, color=REF_RED, linewidth=1.0, linestyle="--", alpha=0.7, zorder=2)
ax.annotate("50% survival", xy=(0.02, 0.505), xycoords=("axes fraction", "data"),
            fontsize=8, color=REF_RED, va="bottom")

ax.set_xlim(left=0)
ax.set_ylim(0, 1.05)
ax.set_xlabel("Years Since First Licence", fontsize=11, color=ANNO_COLOR)
ax.set_ylabel("Survival Probability", fontsize=11, color=ANNO_COLOR)
ax.set_title("Business Survival by Land Value Appreciation During Business Life (2013–2025)",
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
ax.legend(loc="upper right", fontsize=9.5, frameon=True, framealpha=0.92, edgecolor="#dddddd")
fig.text(0.01, 0.01,
         "Source: City of Vancouver Open Data — Business Licences 2013–2026 + Property Tax Assessments. "
         "Independent businesses only. event_v3 corrected.",
         fontsize=7, color="#888888", ha="left", va="bottom")
plt.tight_layout()
plt.savefig(PLOT_APPREC, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"\n  Saved: {PLOT_APPREC}")

print("\nAppreciation Tier Stats Summary:")
apprec_stats_df = pd.DataFrame(apprec_stats)
print(apprec_stats_df.to_string(index=False))

# ---------------------------------------------------------------------------
# 6. Analysis 3: Scatter — avg neighbourhood land value vs median survival
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("ANALYSIS 3: Neighbourhood Land Value vs Median Survival (Scatter)")
print("=" * 60)

# Average median land value per neighbourhood across all available years
lv_avg = lv.groupby("local_area")["median_land_value"].mean().reset_index()
lv_avg.columns = ["localarea", "avg_land_value"]

# Neighbourhood median survival from Step 3 data (recompute here)
# Use the canonical localarea (original, not normalized) for display — but merge on lv name
print("\nFitting KM for each neighbourhood (n>=100)…")
nb_stats = []

for nb in df["localarea"].unique():
    if nb == "Out of Town":
        continue
    sub = df[df["localarea"] == nb]
    if len(sub) < 100:
        continue
    kmf = KaplanMeierFitter()
    kmf.fit(sub["duration"], event_observed=sub["event"])
    med = kmf.median_survival_time_
    sf5 = kmf.survival_function_at_times([5]).values[0]
    # map to lv area name for joining
    nb_lv = area_name_map.get(nb, nb)
    nb_stats.append({
        "localarea": nb,       # display name
        "localarea_lv": nb_lv, # join key
        "n": len(sub),
        "median_survival": med if (not np.isinf(med) and not np.isnan(med)) else 14.0,
        "sf5": sf5,
    })

nb_df = pd.DataFrame(nb_stats)
nb_df = nb_df.merge(lv_avg, left_on="localarea_lv", right_on="localarea", how="inner",
                    suffixes=("", "_lv"))
# Drop the extra columns from merge
for col in ["localarea_lv_lv", "localarea_lv"]:
    if col in nb_df.columns:
        nb_df = nb_df.drop(columns=[col])

# Merge Arbutus Ridge + Arbutus-Ridge: same neighbourhood, two naming variants in panel
# Combine them by taking the weighted average (by n) of survival stats
if nb_df["localarea_lv" if "localarea_lv" in nb_df.columns else "localarea"].isin(["Arbutus Ridge"]).any():
    ar_mask = nb_df["localarea"].isin(["Arbutus Ridge", "Arbutus-Ridge"])
    if ar_mask.sum() > 1:
        ar_rows = nb_df[ar_mask]
        combined_n = ar_rows["n"].sum()
        combined_med = np.average(ar_rows["median_survival"], weights=ar_rows["n"])
        combined_sf5 = np.average(ar_rows["sf5"], weights=ar_rows["n"])
        combined_lv  = ar_rows["avg_land_value"].iloc[0]
        nb_df = nb_df[~ar_mask]
        new_row = pd.DataFrame([{
            "localarea": "Arbutus Ridge",
            "n": combined_n,
            "median_survival": combined_med,
            "sf5": combined_sf5,
            "avg_land_value": combined_lv,
        }])
        nb_df = pd.concat([nb_df, new_row], ignore_index=True)
        print(f"  Merged 'Arbutus Ridge' + 'Arbutus-Ridge' → n={combined_n}, median={combined_med:.1f}yr")

print(f"  Neighbourhoods with land values + survival data: {len(nb_df)}")
print(f"\nNeighbourhood land value vs survival:")
print(nb_df[["localarea", "n", "avg_land_value", "median_survival", "sf5"]]
      .sort_values("avg_land_value")
      .to_string(index=False, float_format=lambda x: f"{x:,.0f}" if x > 100 else f"{x:.2f}"))

# Pearson correlation
r, p = stats.pearsonr(nb_df["avg_land_value"], nb_df["median_survival"])
print(f"\nPearson r = {r:.3f}, p = {p:.4f}")

# Where is Mount Pleasant?
mp_row = nb_df[nb_df["localarea"] == "Mount Pleasant"]
if not mp_row.empty:
    mp_lv  = mp_row["avg_land_value"].values[0]
    mp_med = mp_row["median_survival"].values[0]
    print(f"\nMount Pleasant: avg land value = ${mp_lv:,.0f}, median survival = {mp_med:.1f}yr")

# Plot
fig, ax = plt.subplots(figsize=(10, 7))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

# Color by survival tier (top third green, bottom third red, middle grey)
survival_sorted = nb_df["median_survival"].sort_values()
tercile_33 = np.percentile(nb_df["median_survival"], 33)
tercile_66 = np.percentile(nb_df["median_survival"], 66)

def point_color(med):
    if med >= tercile_66:
        return "#2a9d5c"   # green — high survival
    elif med <= tercile_33:
        return "#e63946"   # red — low survival
    else:
        return "#f4a261"   # orange — middle

colors = nb_df["median_survival"].apply(point_color)

scatter = ax.scatter(
    nb_df["avg_land_value"] / 1e6,   # display in $M
    nb_df["median_survival"],
    c=colors,
    s=nb_df["n"] / nb_df["n"].max() * 400 + 60,   # size ~ n
    alpha=0.80,
    edgecolors="#2c2c2c",
    linewidth=0.5,
    zorder=5,
)

# Label each point
for _, row in nb_df.iterrows():
    ax.annotate(
        row["localarea"],
        xy=(row["avg_land_value"] / 1e6, row["median_survival"]),
        xytext=(4, 2),
        textcoords="offset points",
        fontsize=7.5,
        color=ANNO_COLOR,
        alpha=0.85,
    )

# Regression line
x_vals = nb_df["avg_land_value"].values
y_vals = nb_df["median_survival"].values
slope, intercept, *_ = stats.linregress(x_vals, y_vals)
x_line = np.linspace(x_vals.min(), x_vals.max(), 100)
y_line = slope * x_line + intercept
ax.plot(x_line / 1e6, y_line, color="#888888", linewidth=1.2, linestyle="--",
        alpha=0.6, zorder=3, label=f"Trend (r={r:.2f}, p={p:.3f})")

# Highlight Mount Pleasant
if not mp_row.empty:
    ax.scatter([mp_lv / 1e6], [mp_med], s=200, color="#e63946",
               edgecolors="#2c2c2c", linewidth=1.5, zorder=8, marker="*")
    ax.annotate("Mount Pleasant\n(ice cream shop)",
                xy=(mp_lv / 1e6, mp_med),
                xytext=(10, -20),
                textcoords="offset points",
                fontsize=8.5,
                color="#e63946",
                fontweight="bold",
                arrowprops=dict(arrowstyle="->", color="#e63946", lw=1.0),
                zorder=9)

ax.set_xlabel("Average Median Land Value ($M)", fontsize=11, color=ANNO_COLOR)
ax.set_ylabel("Neighbourhood Median Business Survival (years)", fontsize=11, color=ANNO_COLOR)
ax.set_title("Neighbourhood Land Value vs Business Survival (2013–2025)",
             fontsize=13, fontweight="bold", color=ANNO_COLOR, pad=12)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#dddddd")
ax.spines["bottom"].set_color("#dddddd")
ax.tick_params(axis="both", which="major", labelsize=9, color="#dddddd")
ax.grid(axis="y", color="#eeeeee", linewidth=0.7, zorder=1)
ax.grid(axis="x", color="#eeeeee", linewidth=0.7, zorder=1)
ax.legend(loc="upper left", fontsize=9, frameon=True, framealpha=0.92, edgecolor="#dddddd")

# Bubble size note
ax.annotate("Bubble size = number of businesses", xy=(0.98, 0.02),
            xycoords="axes fraction", fontsize=7.5, color="#888888",
            ha="right", va="bottom")

fig.text(0.01, 0.01,
         "Source: City of Vancouver Open Data — Business Licences 2013–2026 + Property Tax Assessments. "
         "Independent businesses only. event_v3 corrected. 6 areas excluded (no land value data).",
         fontsize=7, color="#888888", ha="left", va="bottom")
plt.tight_layout()
plt.savefig(PLOT_SCATTER, dpi=150, bbox_inches="tight")
plt.close(fig)
print(f"\n  Saved: {PLOT_SCATTER}")

# ---------------------------------------------------------------------------
# 7. Analysis 4: Log-rank pairwise tests between land value tiers
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("ANALYSIS 4: Log-Rank Pairwise Tests — Land Value Tiers")
print("=" * 60)

pairs = [
    ("LOW",    "HIGH"),
    ("LOW",    "MEDIUM"),
    ("MEDIUM", "HIGH"),
]

print(f"\n{'Comparison':<20}  {'Test stat':>10}  {'p-value':>12}  {'Significant?':>14}")
print("-" * 62)

for t1, t2 in pairs:
    sub1 = df_lv[df_lv["tier"] == t1]
    sub2 = df_lv[df_lv["tier"] == t2]
    result = logrank_test(
        sub1["duration"], sub2["duration"],
        event_observed_A=sub1["event"],
        event_observed_B=sub2["event"],
    )
    sig = "YES (p<0.05)" if result.p_value < 0.05 else "no"
    print(f"  {t1} vs {t2:<12}  {result.test_statistic:>10.2f}  {result.p_value:>12.6f}  {sig:>14}")

# Also run for appreciation tiers
print(f"\nAppreciation Tiers:")
print(f"{'Comparison':<20}  {'Test stat':>10}  {'p-value':>12}  {'Significant?':>14}")
print("-" * 62)

for t1, t2 in pairs:
    sub1 = df_apprec[df_apprec["apprec_tier"] == t1]
    sub2 = df_apprec[df_apprec["apprec_tier"] == t2]
    result = logrank_test(
        sub1["duration"], sub2["duration"],
        event_observed_A=sub1["event"],
        event_observed_B=sub2["event"],
    )
    sig = "YES (p<0.05)" if result.p_value < 0.05 else "no"
    print(f"  {t1} vs {t2:<12}  {result.test_statistic:>10.2f}  {result.p_value:>12.6f}  {sig:>14}")

# ---------------------------------------------------------------------------
# 8. Final summary
# ---------------------------------------------------------------------------
print("\n" + "=" * 60)
print("STEP 4 COMPLETE")
print("=" * 60)
print(f"\nPlots saved:")
print(f"  {PLOT_TIER}")
print(f"  {PLOT_APPREC}")
print(f"  {PLOT_SCATTER}")
print(f"\nCoverage note:")
print(f"  Land value data covers {len(covered_areas)} of {len(panel_areas)} neighbourhoods.")
print(f"  Missing areas: {sorted(missing_areas)}")
print(f"  {n_with_lv:,} of {n_total:,} independent businesses matched to land value data ({100*n_with_lv/n_total:.1f}%).")
