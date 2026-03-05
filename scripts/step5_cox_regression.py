#!/usr/bin/env python3
"""Step 5: Cox Proportional Hazards Regression — disentangle neighbourhood, type, and land value."""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker
from lifelines import CoxPHFitter, KaplanMeierFitter
from lifelines.statistics import proportional_hazard_test

PROJECT = "/home/aurora/projects/sites/portfolio-projects/van-property-tax"

# ── Load & join ──────────────────────────────────────────────────────────────
df = pd.read_csv(f"{PROJECT}/data/processed/commercial-panel-v3.csv", low_memory=False)
macro = pd.read_csv(f"{PROJECT}/data/processed/businesstype_macro_categories.csv")
land = pd.read_csv(f"{PROJECT}/data/processed/neighbourhood_land_values.csv")

# Strip *Historic* suffix before joining
df["_bt"] = df["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
macro["_bt"] = macro["businesstype"].str.replace(r"\s*\*Historic\*$", "", regex=True).str.strip()
macro_dedup = macro[["_bt", "macro_category", "gentrification_signal"]].drop_duplicates(subset=["_bt"])
df = df.merge(macro_dedup, on="_bt", how="left").drop(columns=["_bt"])

# Filter to independent businesses only
df = df[df["is_chain"] == False].copy()

# ── Join land value at entry year ────────────────────────────────────────────
# Normalise area names
area_map = {
    "Arbutus-Ridge": "Arbutus Ridge",
    "Kensington-Cedar Cottage": "Kensington-Cedar Cottage",
    "Hastings-Sunrise": "Hastings-Sunrise",
    "Riley Park": "Riley Park",
    "Renfrew-Collingwood": "Renfrew-Collingwood",
    "Dunbar-Southlands": "Dunbar-Southlands",
}
df["_area"] = df["localarea"].map(lambda x: area_map.get(x, x) if pd.notna(x) else x)

# Convert 2-digit years to 4-digit
df["entry_year_4d"] = df["first_year"].apply(lambda y: 2000 + int(y) if y < 100 else int(y))

land_entry = land[["local_area", "year", "median_land_value"]].copy()
land_entry.rename(columns={"local_area": "_area", "year": "entry_year_4d", "median_land_value": "entry_land_value"}, inplace=True)

df = df.merge(land_entry, on=["_area", "entry_year_4d"], how="left")

# ── Survival variables ───────────────────────────────────────────────────────
df["duration"] = df["years_active"]
df["event"] = df["event_v3"].astype(int)

# ── Build Cox dataset ────────────────────────────────────────────────────────
# Filter to businesses with all required fields
cox_df = df.dropna(subset=["macro_category", "localarea", "entry_land_value"]).copy()
print(f"Cox regression sample: {len(cox_df):,} businesses (of {len(df):,} independent)")

# Top 9 business types (others grouped as "Other")
top_types = cox_df["macro_category"].value_counts().head(9).index.tolist()
cox_df["type_group"] = cox_df["macro_category"].apply(lambda x: x if x in top_types else "Other")

# Top 10 neighbourhoods (others grouped as "Other")
top_areas = cox_df["localarea"].value_counts().head(10).index.tolist()
cox_df["area_group"] = cox_df["localarea"].apply(lambda x: x if x in top_areas else "Other")

# Log land value (better-behaved in regression)
cox_df["log_land_value"] = np.log(cox_df["entry_land_value"])

# Entry year as covariate (controls for cohort effects)
cox_df["entry_year_centered"] = cox_df["entry_year_4d"] - 2013  # center at 2013

# Number of employees (fill NaN with median, cap outliers)
emp_median = cox_df["numberofemployees"].median()
cox_df["n_employees"] = cox_df["numberofemployees"].fillna(emp_median)
cox_df["n_employees"] = cox_df["n_employees"].clip(upper=cox_df["n_employees"].quantile(0.99))

# ── Model 1: Type only ──────────────────────────────────────────────────────
print("\n" + "="*80)
print("MODEL 1: Business Type Only")
print("="*80)

type_dummies = pd.get_dummies(cox_df["type_group"], prefix="type", drop_first=True, dtype=float)
m1_df = pd.concat([cox_df[["duration", "event"]].reset_index(drop=True),
                    type_dummies.reset_index(drop=True)], axis=1)
m1_df = m1_df[m1_df["duration"] > 0]

cph1 = CoxPHFitter()
cph1.fit(m1_df, duration_col="duration", event_col="event")
print(f"\nConcordance: {cph1.concordance_index_:.4f}")
print(f"Log-likelihood ratio test p-value: {cph1.log_likelihood_ratio_test().p_value:.2e}")
cph1.print_summary(columns=["coef", "exp(coef)", "p", "exp(coef) lower 95%", "exp(coef) upper 95%"])

# ── Model 2: Type + Neighbourhood ────────────────────────────────────────────
print("\n" + "="*80)
print("MODEL 2: Business Type + Neighbourhood")
print("="*80)

area_dummies = pd.get_dummies(cox_df["area_group"], prefix="area", drop_first=True, dtype=float)
m2_df = pd.concat([cox_df[["duration", "event"]].reset_index(drop=True),
                    type_dummies.reset_index(drop=True),
                    area_dummies.reset_index(drop=True)], axis=1)
m2_df = m2_df[m2_df["duration"] > 0]

cph2 = CoxPHFitter()
cph2.fit(m2_df, duration_col="duration", event_col="event")
print(f"\nConcordance: {cph2.concordance_index_:.4f}")
print(f"Log-likelihood ratio test p-value: {cph2.log_likelihood_ratio_test().p_value:.2e}")
cph2.print_summary(columns=["coef", "exp(coef)", "p", "exp(coef) lower 95%", "exp(coef) upper 95%"])

# ── Model 3: Type + Neighbourhood + Land Value + Controls ────────────────────
print("\n" + "="*80)
print("MODEL 3: Full Model (Type + Neighbourhood + Land Value + Controls)")
print("="*80)

m3_df = pd.concat([cox_df[["duration", "event", "log_land_value", "entry_year_centered", "n_employees"]].reset_index(drop=True),
                    type_dummies.reset_index(drop=True),
                    area_dummies.reset_index(drop=True)], axis=1)
m3_df = m3_df[m3_df["duration"] > 0]

cph3 = CoxPHFitter()
cph3.fit(m3_df, duration_col="duration", event_col="event")
print(f"\nConcordance: {cph3.concordance_index_:.4f}")
print(f"Log-likelihood ratio test p-value: {cph3.log_likelihood_ratio_test().p_value:.2e}")
cph3.print_summary(columns=["coef", "exp(coef)", "p", "exp(coef) lower 95%", "exp(coef) upper 95%"])

# ── Proportional hazards test ────────────────────────────────────────────────
print("\n" + "="*80)
print("PROPORTIONAL HAZARDS TEST (Schoenfeld residuals)")
print("="*80)
try:
    ph_test = proportional_hazard_test(cph3, m3_df, time_transform="rank")
    print(ph_test.summary)
except Exception as e:
    print(f"PH test error: {e}")

# ── Model comparison ─────────────────────────────────────────────────────────
print("\n" + "="*80)
print("MODEL COMPARISON")
print("="*80)
print(f"{'Model':<45} {'Concordance':>12} {'AIC':>12} {'Params':>8}")
print("-" * 80)
print(f"{'M1: Type only':<45} {cph1.concordance_index_:>12.4f} {cph1.AIC_partial_:>12.1f} {len(cph1.params_):>8}")
print(f"{'M2: Type + Neighbourhood':<45} {cph2.concordance_index_:>12.4f} {cph2.AIC_partial_:>12.1f} {len(cph2.params_):>8}")
print(f"{'M3: Full (Type + Area + Land + Controls)':<45} {cph3.concordance_index_:>12.4f} {cph3.AIC_partial_:>12.1f} {len(cph3.params_):>8}")

# ── Plot 1: Hazard ratios forest plot ────────────────────────────────────────
print("\nGenerating plots...")

# Extract coefficients from Model 3 for the forest plot
summary = cph3.summary.copy()

# Rename for readability
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

# Sort by hazard ratio
summary = summary.sort_values("exp(coef)")

fig, ax = plt.subplots(figsize=(10, 10))
fig.patch.set_facecolor("white")
ax.set_facecolor("white")

y_pos = range(len(summary))
hr = summary["exp(coef)"]
ci_lo = summary["exp(coef) lower 95%"]
ci_hi = summary["exp(coef) upper 95%"]

# Color by significance
colors = ["#2166ac" if p < 0.05 else "#999999" for p in summary["p"]]

ax.barh(y_pos, hr - 1, left=1, height=0.6, color=colors, alpha=0.7, edgecolor="none")
ax.errorbar(hr, y_pos, xerr=[hr - ci_lo, ci_hi - hr], fmt="none", ecolor="#333333",
            elinewidth=1, capsize=3, capthick=1)

ax.axvline(x=1.0, color="#e63946", linewidth=1.5, linestyle="--", alpha=0.8, zorder=10)
ax.annotate("No effect", xy=(1.01, len(summary) - 0.5), fontsize=8, color="#e63946")

ax.set_yticks(list(y_pos))
ax.set_yticklabels(summary.index, fontsize=8.5)
ax.set_xlabel("Hazard Ratio (exp(β))", fontsize=11, labelpad=8)
ax.set_title("Cox Regression — Hazard Ratios (Model 3: Full Model)\n"
             "HR > 1 = higher risk of closure, HR < 1 = more durable",
             fontsize=12, fontweight="bold", pad=14)
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#dddddd")
ax.spines["bottom"].set_color("#dddddd")
ax.tick_params(axis="both", labelsize=9, color="#dddddd")
ax.grid(axis="x", color="#eeeeee", linewidth=0.7)

fig.text(0.01, 0.01,
         "Source: City of Vancouver Open Data — Business Licences + Property Tax Assessments 2013–2025. "
         "Blue = significant (p < 0.05). Grey = not significant.",
         fontsize=7, color="#888888")
plt.tight_layout(rect=[0, 0.03, 1, 1])
plt.savefig(f"{PROJECT}/analysis/plots/step5_cox_forest_plot.png", dpi=150, bbox_inches="tight",
            facecolor="white", edgecolor="none")
plt.close()
print("  → step5_cox_forest_plot.png saved")

# ── Plot 2: Model comparison ────────────────────────────────────────────────
fig, axes = plt.subplots(1, 2, figsize=(10, 4.5))
fig.patch.set_facecolor("white")

models = ["Type only", "Type + Area", "Full model"]
concordances = [cph1.concordance_index_, cph2.concordance_index_, cph3.concordance_index_]
aics = [cph1.AIC_partial_, cph2.AIC_partial_, cph3.AIC_partial_]

colors = ["#457b9d", "#e9c46a", "#2a9d8f"]

# Concordance
ax = axes[0]
ax.set_facecolor("white")
bars = ax.bar(models, concordances, color=colors, edgecolor="none", width=0.6)
ax.set_ylabel("Concordance Index", fontsize=10)
ax.set_title("Discrimination (higher = better)", fontsize=11, fontweight="bold")
ax.set_ylim(0.5, max(concordances) * 1.08)
ax.axhline(y=0.5, color="#999999", linewidth=0.8, linestyle="--", alpha=0.6)
ax.annotate("coin flip", xy=(0, 0.502), fontsize=7, color="#999999")
for bar, val in zip(bars, concordances):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.002,
            f"{val:.3f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#dddddd")
ax.spines["bottom"].set_color("#dddddd")
ax.tick_params(axis="both", labelsize=9, color="#dddddd")

# AIC
ax = axes[1]
ax.set_facecolor("white")
bars = ax.bar(models, aics, color=colors, edgecolor="none", width=0.6)
ax.set_ylabel("AIC (partial)", fontsize=10)
ax.set_title("Information Criterion (lower = better)", fontsize=11, fontweight="bold")
for bar, val in zip(bars, aics):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + max(aics)*0.005,
            f"{val:,.0f}", ha="center", va="bottom", fontsize=9, fontweight="bold")
ax.spines["top"].set_visible(False)
ax.spines["right"].set_visible(False)
ax.spines["left"].set_color("#dddddd")
ax.spines["bottom"].set_color("#dddddd")
ax.tick_params(axis="both", labelsize=9, color="#dddddd")

fig.suptitle("Cox Model Comparison — Adding Variables Improves Fit", fontsize=12, fontweight="bold", y=1.02)
plt.tight_layout()
plt.savefig(f"{PROJECT}/analysis/plots/step5_model_comparison.png", dpi=150, bbox_inches="tight",
            facecolor="white", edgecolor="none")
plt.close()
print("  → step5_model_comparison.png saved")

# ── Key findings summary ────────────────────────────────────────────────────
print("\n" + "="*80)
print("KEY FINDINGS FOR NOTEBOOK")
print("="*80)

# Top risk factors (highest HR)
sig_only = cph3.summary[cph3.summary["p"] < 0.05].sort_values("exp(coef)", ascending=False)
print("\nTop 5 risk factors (HR > 1, significant):")
for idx, row in sig_only.head(5).iterrows():
    name = rename_map.get(idx, idx)
    print(f"  {name}: HR={row['exp(coef)']:.3f} (p={row['p']:.2e})")

print("\nTop 5 protective factors (HR < 1, significant):")
protective = cph3.summary[cph3.summary["p"] < 0.05].sort_values("exp(coef)", ascending=True)
for idx, row in protective.head(5).iterrows():
    name = rename_map.get(idx, idx)
    print(f"  {name}: HR={row['exp(coef)']:.3f} (p={row['p']:.2e})")

# Land value effect
lv_row = cph3.summary.loc["log_land_value"]
print(f"\nLand value effect:")
print(f"  HR = {lv_row['exp(coef)']:.3f} per log-unit increase")
print(f"  p = {lv_row['p']:.2e}")
print(f"  Interpretation: doubling land value changes hazard by factor of {2**lv_row['coef']:.3f}")

# Entry year effect
ey_row = cph3.summary.loc["entry_year_centered"]
print(f"\nEntry year effect:")
print(f"  HR = {ey_row['exp(coef)']:.3f} per year later entry")
print(f"  p = {ey_row['p']:.2e}")

print("\nDone.")
