# External Triangulation — Survival Rate Validation

**Date**: 2026-03-03
**Project**: Vancouver Business Survival Analysis
**Analyst**: Claude Code (Desk-Mode Agent)
**Purpose**: Validate KM survival estimates against independent third-party sources

---

## Overview

The Kaplan-Meier survival analysis (Step 1 and Step 2) produced the following key estimates from the Vancouver business licence panel (101,471 commercial businesses, 2013–2025):

- Year-1 survival: 92%
- Year-5 survival: 60%
- Year-10 survival: 41%
- Overall median survival: 8 years
- Food & Beverage median: 6 years
- Technology median: 6 years
- Finance & Insurance median: 14 years

This report triangulates those estimates against six independent external sources to assess whether the figures are plausible, inflated, or deflated — and to identify any sector-level findings that require additional scrutiny.

---

## Sources Used

| ID | Source | Tier | URL |
|----|--------|------|-----|
| S-T1 | ISED Key Small Business Statistics 2024 | T1 | https://ised-isde.canada.ca/site/sme-research-statistics/en/key-small-business-statistics/key-small-business-statistics-2024 |
| S-T2 | ISED Canadian New Firms: Birth and Survival Rates 2002–2014 (May 2018) | T1 | https://ised-isde.canada.ca/site/sme-research-statistics/en/research-reports/canadian-new-firms-birth-and-survival-rates-over-period-2002-2014-may-2018/ |
| S-T3 | StatCan: Long-run evolution of business entry and exit rates (2025) | T1 | https://www150.statcan.gc.ca/n1/pub/36-28-0001/2025009/article/00001-eng.htm |
| S-T4 | StatCan: Firm Dynamics — Death of New Canadian Firms (2012) | T1 | https://www150.statcan.gc.ca/n1/pub/11-622-m/2012028/part-partie1-eng.htm |
| S-T5 | BLS Business Employment Dynamics (US comparison) | T1 | https://www.bls.gov/bdm/bdmage.htm |
| S-T6 | IRS "Tale of Two Datasets" study (administrative vs survey data) | T2 | https://www.irs.gov/pub/irs-soi/16rptwodatasets.pdf |

**Source tiers per DATA-PROJECT-RIGOR.md:**
- T1: Government statistics, primary data producers
- T2: Peer-reviewed academic research or equivalent government working papers

---

## Comparison Table

| Finding | Our Estimate | External Benchmark | Source | Verdict |
|---|---|---|---|---|
| Year-1 survival | 92% | 94.7% (national employer firms) | ISED 2024 (S-T1) | CONFIRMED — slightly below national baseline, consistent with urban high-cost market |
| Year-5 survival | 60% | 67.4% (national) | ISED 2024 (S-T1) | CONFIRMED — 7 percentage points below national; consistent with high-cost urban market dynamics |
| Year-10 survival | 41% | 41.0% (BC-specific) | ISED 2024 (S-T1) | EXACT MATCH — strongest single corroboration point in this analysis |
| Median survival (all sectors) | 7–8 years | ~6–8 years implied by ISED survival curves | ISED 2024 (S-T1) | CONFIRMED |
| Food & Beverage median | 6 years | 31% at 10yr → ~5–6yr median implied | ISED 2018 (S-T2) | CONFIRMED |
| Technology median | 6 years | Prof/Sci/Tech: 56% at 10yr → >10yr median implied | ISED 2018 (S-T2) | SCRUTINIZE — composition-dependent; see notes |
| Finance & Insurance median | 14 years | No benchmark supports >10yr median for any sector | Multiple (S-T1, S-T2, S-T3) | LIKELY ARTEFACT — institutional branch effect; see notes |

---

## Finding-Level Notes

### Year-1 and Year-5 (CONFIRMED)

Our Year-1 estimate (92%) falls 2.7 percentage points below the ISED 2024 national figure for employer firms (94.7%). This gap is expected: national averages include lower-cost markets (Prairie cities, smaller centres) where business formation barriers are lower. Vancouver's cost structure — among the highest commercial rents in Canada — produces incrementally higher early-stage attrition. The direction and magnitude of the gap are consistent with high-cost urban markets documented in the ISED provincial breakdowns.

Year-5 survival (60% vs 67.4% national) shows the same pattern at a wider spread. The 7 percentage point gap at Year 5 is larger than at Year 1, suggesting cumulative disadvantage rather than a one-time selection effect. This is consistent with the hypothesis that property cost pressure compounds over time.

### Year-10 (EXACT MATCH)

Our Year-10 estimate (41%) matches the ISED 2024 BC-specific figure exactly. This is the strongest corroboration in the validation exercise. The match is notable because it is a province-specific benchmark (not national), applied to a single-city dataset. If the licence-based tracking methodology introduced systematic bias, we would expect a consistent directional deviation. The exact match at Year 10 suggests the aggregate methodology is sound.

This finding should be used as the confidence anchor in the notebook narrative.

### Food & Beverage (CONFIRMED)

ISED 2018 reports approximately 31% of food & beverage businesses survive to Year 10, implying a median survival time in the 5–6 year range (the median is where the KM curve crosses 50%, which occurs before Year 10 if Year-10 survival is 31%). Our Food & Beverage median of 6 years is consistent with this implied range.

### Technology (SCRUTINIZE)

ISED 2018 reports that Professional, Scientific and Technical Services firms have approximately 56% survival at Year 10 — a figure that implies a median survival well above 10 years (the KM curve crosses 50% after Year 10). Our Technology median of 6 years is substantially lower than what the benchmark suggests for professional/tech services.

The likely explanation is composition: our "Technology" macro-category (derived from the businesstype crosswalk) aggregates ICT firms with broader "tech-adjacent" businesses that have higher failure rates. The ISED Accommodation & Food Services benchmark covers a more homogeneous category. This warrants a review of what specific business types fall into the Technology macro-category to determine whether the 6-year figure reflects the full category or a subset.

This is not necessarily an error in the data — it may reflect that Vancouver's technology sector includes many small early-stage startups and IT contractors with genuinely high turnover. However the finding should not be stated without this qualification.

### Finance & Insurance (LIKELY ARTEFACT)

No external benchmark supports a 14-year median survival for any sector in a licence-based dataset. The ISED sector-level data shows Finance, Insurance, Real Estate & Leasing firms at roughly 50–55% at Year 10, implying a median around 10–12 years at most.

The most likely explanation is the institutional branch effect: bank branches, insurance company offices, credit unions, and other institutional financial services locations are each issued individual business licences but represent operations of entities with indefinite lifespan. These are not "businesses" in the SME sense — they are branch locations of large institutions. A single bank with 10 Vancouver branches contributes 10 licence records, each of which will survive as long as the branch remains open. This inflates the Finance & Insurance KM curve.

An audit of Finance & Insurance records to quantify the share of institutional branch licences vs independently operated financial businesses is required before this finding can be published.

---

## Methodological Bias: Licence Data vs Economic Activity

The IRS "Tale of Two Datasets" study (S-T6) compares administrative business records (analogous to municipal licence data) against survey-based business survival data. The core finding: administrative records undercount exits by approximately 37% relative to surveys. Three mechanisms apply specifically to the Vancouver licence dataset:

### 1. Self-Employed Inclusion

The Vancouver business licence dataset includes sole proprietors and self-employed individuals who are required to hold a City licence. The ISED and StatCan benchmarks are primarily based on employer firms (those with at least one employee beyond the owner, registered for payroll). This means our population is broader — we include micro-businesses and solo operators who the national benchmarks exclude. These micro-businesses typically have higher failure rates, which should push our estimates downward relative to benchmarks. That our Year-10 estimate matches BC benchmarks despite including this broader population suggests our methodology is not systematically inflating survival.

### 2. Lapse Without Death Coding

A business that stops renewing its licence is coded as having exited in the year of last renewal. However, some businesses continue operating without a valid licence (non-compliance), while others cease operations but simply do not actively cancel — they lapse silently. In our panel construction, we applied gap-filling for 1-year lapses (treating them as administrative non-renewals rather than deaths). However, multi-year non-renewals are treated as exits even if the business continues operating informally. This creates a structural upward bias in measured exits from the licence data relative to actual business closures.

### 3. Finance & Insurance Branch Effect

As described above: institutional branches are registered as individual licence holders. This creates records with effective lifespans tied to institutional permanence rather than entrepreneurial survival. The effect is concentrated in Finance & Insurance but may also affect portions of Real Estate and Corporate/Professional Services.

---

## Recommended Actions

The following actions are flagged for before Step 3 (survival by neighbourhood) proceeds and before any of these findings are published:

1. **Audit Finance & Insurance records**: Sample the Finance & Insurance licence records; identify institutional branch locations (bank branches, insurance offices, credit union branches). Recompute the Finance & Insurance KM curve excluding institutional branches. Compare median survival before and after.

2. **Check exit status distribution**: Pull the breakdown of `status` values (e.g., "Gone Out of Business", "Inactive", silent non-renewal) for exited businesses. If a large share of exits are silent non-renewals rather than explicit GOB codes, document this as a source of upward bias in measured survival times.

3. **Document self-employed vs employer-firm distinction**: Any published write-up of survival rates should explicitly state that the population includes sole proprietors and self-employed licence holders, not only employer firms. This is the single most important disclosure for readers comparing against ISED/StatCan benchmarks.

4. **Use Year-10 = 41% BC match as confidence anchor**: This exact match is the strongest validation point. Reference it explicitly in the notebook narrative when presenting the overall survival curves.

5. **Technology macro-category composition review**: Before publishing the Technology 6-year median, audit which business types fall into the Technology macro-category. Consider whether a sub-split (e.g., ICT vs tech-adjacent services) would produce more interpretable results.

---

## Overall Verdict

**Aggregate survival rates (Year-1, Year-5, Year-10, overall median) are CONFIRMED** against national and BC-specific government statistics. The Year-10 exact match against the BC-specific ISED 2024 benchmark is the strongest single corroboration in this exercise. The directional pattern of Vancouver rates falling below national averages is consistent with documented high-cost urban market dynamics.

**Food & Beverage sector median is CONFIRMED** against ISED 2018 sector-level implied values.

**Finance & Insurance 14-year median is FLAGGED** as a likely artefact of institutional branch registration. This finding should not be published without the recommended audit. The current best characterization is: "14-year median likely reflects institutional branch longevity rather than independent business survival."

**Technology sector requires composition review** before the 6-year median can be interpreted. The figure may be accurate for Vancouver's tech startup population but diverges from what national professional/scientific services benchmarks would predict.

---

## Source Register

| ID | Source | Tier | URL | Notes |
|----|--------|------|-----|-------|
| S-T1 | ISED Key Small Business Statistics 2024 | T1 | https://ised-isde.canada.ca/site/sme-research-statistics/en/key-small-business-statistics/key-small-business-statistics-2024 | Used for Year-1, Year-5, Year-10 benchmarks (national and BC-specific) |
| S-T2 | ISED Canadian New Firms: Birth and Survival Rates 2002–2014 (May 2018) | T1 | https://ised-isde.canada.ca/site/sme-research-statistics/en/research-reports/canadian-new-firms-birth-and-survival-rates-over-period-2002-2014-may-2018/ | Used for sector-level survival benchmarks (Food & Bev, Tech, Finance) |
| S-T3 | StatCan: Long-run evolution of business entry and exit rates (2025) | T1 | https://www150.statcan.gc.ca/n1/pub/36-28-0001/2025009/article/00001-eng.htm | Used for cross-validation of exit rate trends |
| S-T4 | StatCan: Firm Dynamics — Death of New Canadian Firms (2012) | T1 | https://www150.statcan.gc.ca/n1/pub/11-622-m/2012028/part-partie1-eng.htm | Used for corroboration of early-year survival patterns |
| S-T5 | BLS Business Employment Dynamics (US) | T1 | https://www.bls.gov/bdm/bdmage.htm | Used as cross-national reference for Year-1 and Year-5 comparisons |
| S-T6 | IRS "Tale of Two Datasets" study | T2 | https://www.irs.gov/pub/irs-soi/16rptwodatasets.pdf | Used for methodological bias assessment (administrative data undercount of exits) |

---

*Report produced by Claude Code (Desk-Mode Agent) on 2026-03-03.*
*Framework: DATA-PROJECT-RIGOR.md v1.1. Source tiers per rigor framework definition.*
*See also: ASSUMPTION_VERIFICATION.md (A19), analysis/business-survival-vancouver.ipynb (Step 1 and Step 2 results)*
