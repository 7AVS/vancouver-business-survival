# Step 1: Baseline Business Survival in Vancouver
*Analysis date: 2026-03-03 | Data: City of Vancouver Business Licences 2013–2026*

---

## Overview

The question at the heart of this project is whether Vancouver's commercial property tax burden is making it harder for businesses to survive. Before we can answer that, we need to understand the baseline: how long do Vancouver businesses last in the first place?

This step fits a Kaplan-Meier survival curve to the full commercial panel (101,471 businesses observed over 2013–2025) to establish that baseline. Kaplan-Meier is the standard non-parametric method for survival analysis — it estimates the probability that a business survives past any given year, correctly accounting for businesses we've lost track of (right-censored observations).

---

## Cohort Definition

| Metric | Value |
|--------|-------|
| Total businesses in panel | 101,471 |
| Observed exits (Gone Out of Business + Inactive) | 49,331 (48.6%) |
| Censored (still active at last observation) | 52,140 (51.4%) |
| Left-truncated (entered 2013, pre-date data start) | 40,620 (40.0%) |

**Event definition**: A business is considered to have experienced an event (exit) if its final recorded status is "Gone Out of Business" or "Inactive". Businesses whose last recorded status is "Issued" are treated as right-censored — we observed them active to the end of the data window but do not know their ultimate fate.

**Duration**: `years_active` = `last_year − first_year + 1`, ranging from 1 to 14 years.

---

## Survival Rates

### Kaplan-Meier Estimates at Key Milestones

| Year | Survival Probability | 95% Confidence Interval |
|------|---------------------|------------------------|
| 1 yr | 91.9% | [91.8%, 92.1%] |
| 3 yr | 74.3% | [74.0%, 74.5%] |
| 5 yr | 59.5% | [59.2%, 59.8%] |
| 7 yr | 50.4% | [50.0%, 50.7%] |
| 10 yr | 40.8% | [40.4%, 41.1%] |

### Summary Statistics

| Statistic | Value |
|-----------|-------|
| Median survival time | 8.0 years (95% CI: 6.0–8.0) |
| Restricted mean survival time (tau=14 yr) | 7.86 years |

---

## What This Means

### The headline: half of Vancouver businesses don't make it past 8 years.

The median survival time is **8.0 years**. That's the point at which exactly half the businesses in our panel had exited — gone, inactive, or dissolved. The curve drops steeply in the early years: by year three, roughly 25.7% of businesses that entered the panel have already exited. The attrition slows after year five, and the tail of the curve flattens — but those long survivors are a minority.

The restricted mean survival time of **7.9 years** (averaged over the full 14-year window) is pulled down by the heavy early exit rate. In plain terms: the average business in Vancouver generates just over 8 years of economic activity before disappearing from the licence registry.

These numbers are not catastrophic by global standards — roughly half of all new businesses fail within five years across most developed economies — but they set the baseline against which we'll evaluate whether property tax stress accelerates that curve.

### The survival cliff: year one to three

The steepest drop in the survival curve happens in the first three years. About 8.1% of businesses exit within their first year, and nearly 25.7% are gone within three. This is consistent with well-documented patterns in business demography: the first few years carry the highest hazard as businesses test whether their model is viable. After year five, hazard rates fall — the businesses that survived the early gauntlet are systematically more robust.

### The long survivors

By year 10, **40.8%** of businesses are still active. This is a small but meaningful cohort — and disproportionately, these will be businesses with strong locations, stable demand, or some form of competitive moat. Whether those characteristics correlate with lower property tax exposure (e.g., ownership vs. tenancy) is a question later steps of this analysis will examine.

---

## Caveat: Left Truncation

**40,620 businesses (40.0%) entered the panel in 2013** — the first year of our data. These businesses existed *before* our observation window opened. We don't know when they were founded; we know only that they were alive in 2013. This is the left-truncation problem: these businesses have already survived some unknown period before we started watching.

The practical effect is that businesses with `first_year=2013` look artificially durable in our dataset — we observe them only after they've already passed some unobserved survival test. A cohort of 40,620 businesses is large enough that this biases the early part of the survival curve upward. The true early-exit rate for Vancouver businesses is likely *higher* than what we estimate.

### Sensitivity check: excluding 2013 entrants

When we exclude the 2013 cohort and re-fit on the 60,851 businesses that entered 2014–2026 (whose full birth-to-death span is observable), the median survival shifts to **7.0 years**. The curves are similar in shape but the restricted cohort shows a modestly lower survival rate in the early years, consistent with the truncation bias described above.

All subsequent steps in this analysis will flag which results are sensitive to the inclusion of 2013 entrants.

---

## Milestone Comparison: Full vs. Restricted Cohort

| Year | Full Cohort | Excl. 2013 Entrants |
|------|-------------|---------------------|
| 1 yr | 91.9% | 93.6% |
| 3 yr | 74.3% | 74.1% |
| 5 yr | 59.5% | 58.6% |
| 10 yr | 40.8% | 38.9% |
| Median | 8.0 yr | 7.0 yr |

---

## Output Files

| File | Description |
|------|-------------|
| `analysis/plots/step1_baseline_survival.png` | Kaplan-Meier survival curve with CI and milestone annotations |
| `analysis/STEP1_BASELINE_SURVIVAL.md` | This report |

---

## Next Steps

With the baseline survival curve established, Step 2 will stratify survival by business sector (`macro_category`) and neighbourhood (`localarea`) to identify where attrition is most concentrated. Step 3 will introduce the property tax data and test whether assessed land value correlates with accelerated exit rates.

---

*Data source: City of Vancouver Open Data Portal — Business Licences 2013–2026. Panel construction described in `PANEL_V2_CHANGELOG.md`.*
