# Phase 0 — Research Question Candidates
**Project**: Vancouver Property Tax / Gentrification Analysis
**Phase**: 0 (Problem Framing)
**Date**: 2026-03-03
**Framework**: DATA-PROJECT-RIGOR.md v1.0
**Author**: Claude Code Desk-Mode Agent

---

## Preamble: What This Phase Is Not

The DiD angle on assessed values as an outcome for the Foreign Buyer Tax (2016) or Empty Homes Tax (2017) is closed. The adversarial review (`ADVERSARIAL_REVIEW.md`) documented why:

1. BC Assessment uses a July 1 valuation date. The FBT shock (August 2, 2016) cannot appear in assessment data until January 2018. This is a 17-month lag before the first affected valuation — making assessed values poorly suited for event-study identification.
2. Attenuation bias from this lag is documented in peer-reviewed literature (Fischer, Hauf, Stehle — *Journal of Banking & Finance*, 2026 from SSRN working paper; Berlin School of Economics working paper "When Housing Price Data Lag Behind the Market"). Researchers avoid assessed values for event studies for published methodological reasons — not oversight.
3. The only credible treatment proxy (pre-policy foreign buyer share from PTT records) is restricted to researchers with Ministry of Finance data agreements. The Census immigrant-share fallback conflates ethnicity with legal status, producing known-direction attenuation.
4. The EHT control group (Burnaby, Richmond, North Vancouver) is contaminated by SVT anticipation from the February 20, 2018 BC Budget announcement — 10 months before the regulation came into force.

None of these problems are overcome by a portfolio analyst without data agreements. Moving on.

What follows are three candidate questions that use the same three datasets but take different approaches — each with an inferential or predictive method at its core.

---

## Candidate 1: Neighbourhood Trajectory Typology

### 1. The Question

Can we classify Vancouver's 30 neighbourhoods into statistically distinct gentrification trajectory types using 20 years of assessed value growth, four waves of census demographic shift, and business licence composition change — and does the typology match what residents and urbanists describe informally?

### 2. Why It's Interesting

Vancouver residents talk about neighbourhood change in vivid qualitative terms: "Strathcona is the new Gastown," "Commercial Drive is holding," "Marpole feels next." These intuitions rarely get quantified. A data-driven typology that names and separates neighbourhood trajectories — and can say "these three neighbourhoods are on the same trajectory as Gastown was in 2006" — is immediately legible to anyone who lives here. It also has policy relevance: neighbourhoods in early-stage gentrification may benefit from different interventions than those mid-cycle.

The question is community-relevant at the household level. It also sidesteps the politically charged "did the foreign buyer tax work?" framing in favour of "here is what the data says about where your neighbourhood is headed."

### 3. Statistical Methods Required

**Primary method: Longitudinal clustering (K-means or hierarchical clustering on a trajectory feature matrix)**

Rather than clustering raw cross-sections (which ignores change over time), the approach builds a feature matrix where each row is a neighbourhood and each column is a trajectory metric — the *rate and pattern of change* over the observation window, not the current level. Examples: CAGR of assessed land value 2006–2026, change in renter share 2006–2021, net business licence churn in "gentrification-signal" categories 2013–2024, change in median household income 2006–2021. K-means or Ward's hierarchical clustering on this standardised feature matrix groups neighbourhoods by how they moved, not where they started.

**Secondary method: Silhouette analysis and cluster validation**

Clustering produces groups, but you must justify k (the number of clusters). Silhouette scores measure how similar each observation is to its own cluster relative to the nearest other cluster (range -1 to +1; higher is better). Elbow plots on within-cluster sum of squares provide a second diagnostic. Together these give a defensible answer to "why three clusters and not five?"

**Supporting method: Principal Component Analysis (PCA) for dimensionality reduction and visualisation**

If the feature matrix has 15–20 metrics, PCA reduces these to 2–3 components for visualisation while preserving most variance. The PC biplot shows which features drive the separation and allows scatterplot visualisation of the cluster structure. This is not the core inference — it supports interpretation.

**Inferential check: ANOVA / Kruskal-Wallis on cluster-level outcome differences**

After clustering, test whether the groups are statistically distinguishable on key outcome variables (e.g., mean assessed value growth rate, mean income change, mean business churn). This makes the clustering result falsifiable — if clusters are not statistically different on the outcome variables that motivated the clustering, the exercise is pattern-matching, not discovery.

### 4. Which Datasets Are Used and How

**Property tax data** (`current_land_value`, `neighbourhood_code`, `report_year`, `zoning_classification`, `legal_type`):
- Aggregate to 30 neighbourhoods × 21 years panel
- Compute: median assessed land value per neighbourhood-year (deflated to constant 2006 dollars), CAGR over 2006–2026, CAGR over 2006–2015 vs. 2015–2026 (two-period slope), share of STRATA vs. LAND legal type change
- Note: neighbourhood_code must be decoded using the City of Vancouver neighbourhood boundary dataset (not yet acquired — see assumption register A1 below)

**Census data** (income variables by CT, dwelling type, tenure, immigration):
- Aggregate CT-level data to the 30 CoV neighbourhood areas (requires spatial join of census tract boundaries to CoV neighbourhood polygons — CT boundary shapefiles identified but not downloaded, see A2)
- Extract: change in median household income (2006→2021), change in renter share, change in recent immigrant share, change in bachelor's degree attainment rate, change in % spending 30%+ on shelter
- Use 2016 and 2021 as the two primary census snapshots for the trajectory calculation (2011 NHS caveats apply; 2006 available as baseline)

**Business licences** (`businesstype`, `localarea`, `folderyear`, `status`, `licencersn`):
- Construct a "gentrification signal index" per neighbourhood-year: ratio of "signal" business types (fine dining, boutique fitness, wellness, tech/consulting) to "displacement" types (auto repair, light industrial, laundromat, pawn). Requires building a business type crosswalk from the 500+ historic categories to a simplified classification.
- Track net change in this ratio 2013–2024 (business licence data does not start until 1997, but the localarea and geom fields needed for neighbourhood attribution are most reliable post-2013)
- Note: localarea is 100% null in the current API extract; geocoding via geom field required (see A3)

### 5. What the Deliverable Looks Like

The reader sees:
- A dendrogram or k-means cluster map of the 30 neighbourhoods, coloured by cluster assignment
- A "cluster profile table" showing each cluster's mean values on 6–8 key features (e.g., "Cluster 1: High value, high appreciation, declining renter share, high gentrification signal business churn — *established gentrification zone*")
- A map of Vancouver with neighbourhoods colour-coded by cluster — the visual anchor for anyone who knows the city
- A cluster-by-cluster narrative: which neighbourhoods are in each group, what makes them similar, what distinguishes them from other groups
- Silhouette scores and the elbow plot justifying k
- A closing challenge: "Which neighbourhoods are early-stage today what Gastown was in 2006?" (using the cluster membership at early vs. late windows to identify trajectory similarity)

### 6. Feasibility Assessment

**Can this be done with our data?** Yes, with some pre-processing work.

**What we have that works:**
- Property tax panel is ideal: 30 neighbourhoods, 21 years, complete. Aggregating to neighbourhood-year medians is a standard operation.
- Census data covers the 15-year window with 4 snapshots. Change variables are constructable even without CT concordance (if we work at the CoV neighbourhood level rather than CT level, boundary stability is higher).
- Business licence data (2013–2024) gives 12 years of business composition data. Sufficient for a trend measure.

**Hardest parts:**
1. **Business type classification**: The 500+ historic `*Historic*` business type categories must be manually (or semi-automatically) classified into signal/neutral/displacement types. This is judgement work, not code. The classification decisions will be the most challengeable part of the analysis. Mitigation: publish the crosswalk and invite critique.
2. **Spatial join of census tracts to CoV neighbourhoods**: The 30 CoV neighbourhoods don't align perfectly with census tract boundaries. CT shapefiles must be downloaded and a weighted-area crosswalk built. This is solvable but requires GIS work (geopandas or equivalent).
3. **The 2011 NHS caveat**: Income and immigration variables from 2011 are NHS-based with known bias. For a 4-point trend (2006, 2011, 2016, 2021), using 2011 as one of the four points introduces measurement noise. Mitigation: run the clustering on 2006/2016/2021 only (skipping 2011 for income variables) and check robustness.

**What this CANNOT do:** Identify causal drivers of clustering. The analysis describes trajectory types — it cannot say why Strathcona moved into Cluster X and Marpole did not. The language must stay in the descriptive-with-inference zone, not slide into causal claims.

### 7. Learning Value for Andre

**Primary concept: Unsupervised machine learning (clustering)**

Andre works with A/B testing and cohort analysis — supervised-adjacent frameworks where the outcome is defined. Clustering is the first genuinely unsupervised method in his toolkit. It teaches: how to represent time-series change as a feature, why standardisation matters, how to choose k, and how to validate that the clusters are real rather than artefacts of the algorithm. These are transferable to customer segmentation, channel mix typology, and any scenario where you need to group things without a predefined label.

**Secondary concept: Dimensionality reduction (PCA)**

PCA shows how to compress many correlated variables into fewer uncorrelated components without losing most of the information. Useful for any high-dimensional data problem. The biplot interpretation — which variables load heavily on which components — is a thinking tool that applies everywhere.

### 8. Adversarial Pre-Challenge

**Challenge 1 — Clustering is not inference, it is pattern imposition.**
K-means will always produce k clusters regardless of whether k clusters actually exist in the data. The algorithm will group things even if the underlying distribution is uniform. Silhouette analysis and elbow plots are diagnostic tools, not proofs of cluster existence. A sceptic will say: "you drew lines in a continuous space and named them."

Defense: The clustering is a descriptive framework, not a causal claim. The ANOVA test on cluster-level outcome differences provides a post-hoc check that the groups are statistically distinguishable. If they are not, the clustering is abandoned. The deliverable is transparent about this.

**Challenge 2 — 30 neighbourhoods is a very small N.**
With only 30 data points (neighbourhoods), clustering is statistically fragile. A single outlier (e.g., Downtown/Central Business District, which has a fundamentally different property mix) can dominate the centroid calculation. With K=4, you effectively have 7-8 observations per cluster — small enough that results are sensitive to the choice of distance metric and initialisation seed.

Defense: This is real. Mitigation: run k-means 100 times with different seeds and report the most stable solution (highest average silhouette). Consider hierarchical clustering (Ward's method) which does not require initialisation and is more stable at low N. Report results for k=3, 4, 5 to show robustness. Consider excluding Downtown as a sui generis case.

**Challenge 3 — The business licence data starts in 2013 but the census and property data start in 2006. Splicing these windows creates a inconsistency.**
The clustering feature matrix will cover different time windows for different data sources. Property value CAGR is computed 2006–2026. Census change is 2006–2021. Business composition change is 2013–2024. These are not the same window. A neighbourhood that gentrified 2006–2012 (pre-business-licence window) would appear less gentrified in the business metric than in the property metric.

Defense: This is a known limitation. Mitigation: limit the property value trend metric to 2013–2026 as well, keeping windows aligned. Some power is lost (7 fewer years of property data as a trend metric) but the cross-dataset consistency is better. Alternatively, use the 1997–2012 business licence dataset (available but not yet fully processed) to extend the window. Document the limitation explicitly.

---

## Candidate 2: Bill 44 Upzoning Capitalization into Assessed Land Values

### 1. The Question

Did the 2023 Bill 44 / Vancouver R1-1 rezoning — which granted blanket multiplex rights to all formerly single-family-only lots in Vancouver — produce a measurable increase in assessed land values for affected properties relative to already-multifamily-zoned properties in the same neighbourhood, controlling for property characteristics and neighbourhood effects?

### 2. Why It's Interesting

Bill 44 is the biggest zoning change in Vancouver's history. City Council adopted R1-1 in October 2023, converting all RS-1 through RS-7 single-family zones to Residential Inclusive — permitting up to 6 units where previously only 1 was allowed. Every homeowner on a formerly-RS street in Vancouver now holds a lot with development rights they didn't have in 2022.

The question "how much is that worth?" is literally on the minds of everyone who owns a house in East Van, Kitsilano, or Dunbar. The economic theory (zoning capitalization) says density rights should be capitalised into land value — more permitted use = higher land value, all else equal. But by how much? Does $500K in new density rights show up as $500K in the assessment? Less? More? This is quantifiable with the data we have, and the answer matters to policy: if capitalization is high, upzoning benefits existing landowners; if low, the market doesn't believe the density rights will be exercised.

This is also what the adversarial review identified as the genuinely novel use case for assessed values: "Using BC Assessment data for a long-run capitalization study (e.g., measuring the permanent component of policy effects 5–10 years post-treatment) is genuinely underexplored." We have 2023, 2024, 2025, and 2026 assessments — 3 post-treatment years.

### 3. Statistical Methods Required

**Primary method: Two-way fixed effects panel regression (property FE + year FE)**

The dataset is a property-level panel: 170K–226K properties × 21 years. The estimating equation is:

`log(land_value_per_sqft)_it = α_i + γ_t + β × (Treated_i × Post2023_t) + ε_it`

Where:
- `α_i` = property fixed effect (absorbs all time-invariant property characteristics: lot size, location, structure age)
- `γ_t` = year fixed effect (absorbs economy-wide shocks common to all properties: interest rates, overall market conditions)
- `Treated_i` = 1 if the property was in an RS zone as of 2022 (now R1-1), 0 if already zoned for multi-family (RM, C zones, etc.)
- `Post2023_t` = 1 for report years 2024, 2025, 2026 (assessments reflecting market conditions after October 2023 rezoning)
- `β` = the capitalization coefficient — the percentage premium in land value attributable to the upzoning

The log specification is standard for land values (right-skewed distribution) and produces a coefficient interpretable as a percentage effect.

**Secondary method: Parallel trends pre-test**

Before trusting β, verify that treated and control properties followed parallel trends in assessed land value before October 2023. Plot year fixed effects for the two groups from 2006 to 2022. If they were co-moving prior to treatment, the post-2023 divergence is attributable to the rezoning. If they were already diverging, the DiD is invalid.

**Supporting method: Heterogeneity analysis (interaction terms)**

Does capitalization vary by neighbourhood? By lot size (larger lots gain more from multiplex rights)? By year_built (tear-down-candidate old structures vs. newer houses)? Interaction terms added to the base regression test these. Example: `β × Treated × Post2023 × LargeLot_i` tests whether the premium is larger for bigger lots.

### 4. Which Datasets Are Used and How

**Property tax data** (primary):
- `current_land_value`: outcome variable (per square metre, estimated from lot dimensions — see A4)
- `zoning_district` (2022 values): treatment assignment — RS-1 through RS-7 properties are Treated=1; RM, C, CD zones are control=0
- `neighbourhood_code`: fixed effect grouping (or neighbourhood-year controls)
- `report_year`: time dimension; Post2023=1 for 2024, 2025, 2026 assessments
- `year_built`, `current_improvement_value`: controls for property characteristics
- `legal_type` (LAND vs. STRATA): filter to LAND type for the primary analysis (strata is a different market with different capitalization dynamics)

Treatment assignment note: `zoning_district` field in the property tax data contains the specific zone code (e.g., "RS-1", "RS-7", "RM-3"). The R1-1 adoption on October 17, 2023 effectively means any property coded RS-1 through RS-7 in the 2022 or 2023 data is in the treated group. The 2024 assessment (reflecting July 1, 2024 market conditions) is the first assessment made with full knowledge of R1-1 being in effect for nearly a year.

**Census data** (control variables only):
- Neighbourhood-level income, education, and demographic controls to account for the possibility that upzoned areas are systematically different in ways that affect land value growth independently of the zoning change
- 2021 census is the last available snapshot — use as pre-treatment neighbourhood controls

**Business licences**: Not directly used in this analysis (zoning capitalization is a property-level question).

### 5. What the Deliverable Looks Like

The reader sees:
- A coefficient table from the two-way FE regression: the estimated β (percentage premium), its 95% confidence interval, and the sample size
- A parallel trends plot: two lines (treated/control) from 2006 to 2026, with a vertical line at October 2023. If the lines were parallel before and diverge after, the design is credible.
- A map of Vancouver showing which properties are treated (formerly RS) vs. control, coloured by whether they show above-average appreciation post-2023
- Heterogeneity table: does the premium differ by neighbourhood, lot size, or property age?
- An honest limitations section: "This design identifies the capitalization effect of the R1-1 rezoning, conditional on the parallel trends assumption holding. It cannot identify whether the effect comes from actual multiplex construction, speculative land value expectations, or a combination. We have only 3 post-treatment years — effects may not be fully capitalised yet."
- A plain-language summary: "A formerly-single-family lot in Vancouver gained approximately X% in assessed land value after the rezoning, compared to lots that were already zoned multi-family. At the median land value of $Y, this is approximately $Z per lot."

### 6. Feasibility Assessment

**Can this be done with our data?** Yes. This is the most technically feasible of the three candidates.

**What we have that works:**
- The property tax panel has excellent longitudinal coverage with 98%+ PID retention year-over-year. Two-way FE requires a panel — we have one.
- `zoning_district` is populated for 98%+ of records, and the RS zone codes are identifiable as text patterns.
- We have 3 post-treatment years (assessments for 2024, 2025, 2026). The 2024 assessment is the cleanest (July 1, 2024 market conditions; R1-1 was in effect from October 2023). The 2025 and 2026 assessments add additional post-treatment observations.
- The control group is internal to Vancouver — already-multifamily-zoned lots in the same city. This is a clean comparison because they share the same macro environment (interest rates, city-level demand).

**What's missing:**
- Lot square footage is NOT in the property tax dataset. To compute land value per square metre, we either (a) join to the CoV parcel shapefile (available from City Open Data) to get lot area, or (b) restrict the analysis to median-assessed-value comparisons rather than per-sqft metrics. Option (a) is preferred but requires a spatial join step.
- The zoning classification schema shifted circa 2020 in the dataset ("Residential Inclusive" appears as a new category). This means some R1-1 conversions may show up in `zoning_classification` but not in `zoning_district` depending on how the city updated the data. Requires careful inspection of the 2023–2026 records to confirm treatment assignment is stable.
- Pre-treatment parallel trends is the key assumption and must be checked. High-income RS neighbourhoods (Shaughnessy, Dunbar, Kitsilano) may have been on different value trajectories than multi-family inner-city neighbourhoods even before 2023. If parallel trends fails, the whole design fails.

**Hardest part:** The parallel trends test. If RS-zoned properties were already appreciating faster than RM-zoned properties before 2023 (due to land banking or teardown expectations), the comparison is invalid. Mitigation: restrict to neighbourhoods that have both RS and RM properties (most do), so the comparison is within-neighbourhood. The neighbourhood fixed effect handles this if the trend differences are neighbourhood-level; if they are property-type-level within the same neighbourhood, additional controls are needed.

### 7. Learning Value for Andre

**Primary concept: Two-way fixed effects (TWFE) panel regression**

This is the industry-standard method for before/after comparisons with panel data. Andre knows A/B testing (randomised treatment) and can extend that mental model to quasi-experiments: what happens when treatment is not randomised but you have panel data to control for unit-level fixed effects? TWFE teaches: why fixed effects absorb confounding better than OLS controls, what the Frisch-Waugh-Lovell theorem means in practice, and how to test the parallel trends assumption that makes the design credible. These are directly applicable to his work: cohort analysis, campaign measurement, and any marketing attribution problem where pre-treatment trends matter.

**Secondary concept: Log-linear regression and coefficient interpretation**

The log specification of the outcome (log land value) is standard in economics and frequently misunderstood by people trained in marketing analytics. Andre learns: why we log-transform skewed outcomes, how to interpret a coefficient in a log-level regression as an approximate percentage effect, and when this approximation breaks down. Transferable to conversion rate modelling, LTV analysis, and any outcome with a heavy right tail.

### 8. Adversarial Pre-Challenge

**Challenge 1 — The 2024/2025/2026 assessments reflect a confounded period (interest rate cuts + zoning change simultaneously).**
The Bank of Canada began cutting rates in June 2024, lowering the overnight rate from 5.00% to 2.75% by March 2025. This rate cutting cycle would independently increase land values across Vancouver regardless of zoning. A simple comparison of pre/post 2023 assessed values would attribute some of the rate-cut-driven appreciation to the R1-1 rezoning.

Defense: Two-way fixed effects with year fixed effects absorbs economy-wide shocks common to all properties in a given year — including interest rate effects. If BoC rate cuts raised all Vancouver land values equally in 2024, the year FE captures this and β estimates the *differential* effect on RS-zoned properties relative to already-RM-zoned properties. The design is not immune, however: if rate cuts disproportionately benefit single-family land (because lower rates increase feasibility of multiplex development), the year FE does not fully absorb this. A robustness check: run the same regression on Toronto (which has similar SSMU legislation under Ontario's More Homes Built Faster Act, Bill 23, November 2022) to compare. If Toronto shows similar coefficients for a similar rezoning, confidence in the Vancouver estimate increases. This would require sourcing Toronto assessment data — add to project scope only if needed.

**Challenge 2 — BC Assessment may not quickly reflect the value of new zoning rights if assessors are conservative.**
BC Assessment is mandated to reflect July 1 market value. But assessors may not immediately capitalise uncertain future density rights — especially if multiplex construction in practice is slow (permit bottlenecks, construction cost constraints). If assessors observe that few multiplex permits are being pulled, they may not mark up land values to reflect theoretical density rights.

Defense: This is real and is itself a finding. If β is not statistically significant or is small, one interpretation is "the market (as reflected in assessments) does not yet price in the upzoning." This is not a failure of the study — it is the answer to the question. The correct framing is: "We test whether upzoning has capitalised into assessed values, not whether it 'should have' capitalised." If assessors are lagging the market, a secondary analysis using permit data (multiplex applications post-2023) could test whether areas with higher permit activity show higher assessed value growth — but this requires permit data not currently in our inventory.

**Challenge 3 — The control group (already-RM-zoned properties) may receive their own policy shocks in 2023–2026 that contaminate the comparison.**
The Broadway Plan (approved June 2022, implementation ongoing) dramatically upzoned Broadway corridor properties. Some of these were already-RM-zoned properties. If the control group receives its own density boost from the Broadway Plan, the control group's land values rise for their own treatment reason, compressing the estimated β for R1-1.

Defense: Valid. Mitigation: explicitly exclude properties within the Broadway Plan boundary from the control group. The Broadway Plan geographic boundary is publicly available. This makes the control group "already-RM-zoned properties outside the Broadway Plan area" — a cleaner comparison. Log the exclusion as an assumption in the register (A5 below).

---

## Candidate 3: Business Survival Analysis by Neighbourhood Type

### 1. The Question

Does the probability that a business licence survives to a second year — and a fifth year — differ systematically by neighbourhood and business type in Vancouver, and has this survival probability changed over the 2013–2024 period in ways that correspond to observed neighbourhood change?

### 2. Why It's Interesting

"Small businesses are being pushed out" is one of the most common complaints in Vancouver's gentrification discourse. Rents go up, landlords redevelop, long-running independent shops close. But "how quickly?" and "where?" have no numerical answer attached to them in public discourse. Survival analysis puts a number on it: the median survival time for an independent restaurant in Mount Pleasant vs. in Downtown vs. in Strathcona. The Kaplan-Meier curve is immediately legible — a downward-sloping line showing what share of businesses are still operating at Year 1, 2, 3, 4, 5.

The question also inverts the usual perspective: rather than looking at who is moving in (gentrification signal businesses), it asks how long the existing ones last. Survival time is a proxy for the stability and economic health of a commercial ecosystem.

### 3. Statistical Methods Required

**Primary method: Kaplan-Meier survival estimation**

For each business licence cohort (e.g., all restaurants that first received a licence in 2013), track what fraction renew in each subsequent year. The Kaplan-Meier estimator produces a survival curve S(t) = probability of survival beyond time t, adjusting for right-censoring (businesses still active at the end of the observation window haven't failed — they are censored at their last observed year).

Key outputs: median survival time (the year by which 50% of a cohort has closed), 1-year, 3-year, and 5-year survival rates.

**Secondary method: Log-rank test**

Compare survival curves between groups: "Does the survival curve for restaurants in East Van differ statistically from restaurants in Downtown?" The log-rank test is a nonparametric test of whether two Kaplan-Meier curves are drawn from the same underlying distribution. It is the standard way to compare survival between groups in the absence of covariates.

**Extension method: Cox Proportional Hazards regression**

The Cox model estimates the hazard ratio — the multiplicative effect of a covariate on the instantaneous failure rate. Covariates: neighbourhood (categorical), business type (categorical), year of first licence (cohort), neighbourhood assessed value growth rate (from property tax data), presence of major nearby construction/redevelopment (derived from permit data or zoning changes). This extends the Kaplan-Meier analysis by allowing multiple covariates and producing interpretable effect sizes: "An independent restaurant in a neighbourhood with 10% higher land value appreciation has a X% higher hazard of closure, all else equal."

The Cox model is semi-parametric: it assumes the proportional hazards (PH) assumption (the hazard ratio between groups is constant over time) but does not assume a specific baseline hazard shape. The PH assumption is testable (Schoenfeld residuals test).

### 4. Which Datasets Are Used and How

**Business licences** (primary):
- Construct a survival dataset: one row per unique business (identified by `licencersn` or `licencenumber`), with `entry_year` (first folderyear), `exit_year` (last folderyear before status changed to "Gone Out of Business" or "Inactive"), and `censored` flag (if still "Issued" at end of observation window)
- `businesstype` (after building the old→new crosswalk): stratify survival analysis by business type category
- Neighbourhood assignment: via geom lat/lon → CoV neighbourhood boundary spatial join (A3). Records without geocoordinates are excluded from neighbourhood-stratified analysis.
- Time window: 2013–2024 for the primary analysis (12 years, maximum observed lifetime = 12 years). The 1997–2012 dataset could be combined to extend the observation window but requires harmonising the slightly different schema.
- Caveat: A business that closes and reopens under a new licence number will look like two separate short-tenure businesses rather than one long-running one. This is a known limitation of using licence records as a proxy for business survival (see A6).

**Property tax data** (covariate in Cox model):
- Neighbourhood-level median assessed land value growth rate per year (pre-computed from the 30-neighbourhood panel)
- Join to the survival dataset by neighbourhood + year
- This tests the hypothesis: "In neighbourhoods where land values are rising faster, businesses close sooner." If the Cox coefficient on land value growth is positive (higher growth = higher hazard = shorter survival), this is quantitative evidence for the rent-pressure hypothesis.

**Census data** (covariate in Cox model):
- Neighbourhood income level (2016 or 2021 census, depending on vintage of the survival window)
- Neighbourhood renter share
- These control for the possibility that businesses in higher-income areas close faster because the resident customer base is more transient (not because of rent pressure), which is a confound.

### 5. What the Deliverable Looks Like

The reader sees:
- A set of Kaplan-Meier curves: one per neighbourhood (or selected neighbourhoods for readability), showing survival probability over 10 years for a given business type (e.g., independent restaurants). The visual is immediately interpretable: a curve that falls sharply in year 1–2 means fast churn; a curve that holds through year 5 means stability.
- A table of median survival times: "Median survival for a Restaurant in Downtown: 3.2 years. In Kitsilano: 5.1 years. In Strathcona: 2.8 years." (These are example numbers, not predictions.)
- Log-rank test results: which neighbourhood pairs have statistically different survival distributions?
- Cox model coefficient table: which covariates (neighbourhood type, assessed value growth rate, income level) significantly predict hazard of closure? What is the estimated hazard ratio?
- A plain-language interpretation: "For every 10% increase in a neighbourhood's annual land value appreciation, businesses in that neighbourhood face a X% higher annual closure rate, after accounting for business type and neighbourhood income."
- Honest limitations section: the measurement-of-closure problem (businesses that quietly stop renewing may continue operating informally for some time), the licence RSN continuity problem, and the geocoding coverage gap.

### 6. Feasibility Assessment

**Can this be done with our data?** Yes, with significant pre-processing.

**What we have that works:**
- 12 years of business licence records (2013–2024) with stable `licencersn` identifiers
- Status field distinguishes "Issued" (active), "Inactive", "Gone Out of Business", "Cancelled"
- folderyear provides the temporal structure needed for cohort construction
- The property tax panel provides neighbourhood-level land value growth as a covariate
- Survival analysis is computationally straightforward in Python (lifelines library) or R (survival package)

**Hardest parts:**
1. **Defining an "event"**: The dataset does not directly record date of closure. The event must be inferred: a business that had "Issued" status in year t and does not appear (or appears with "Gone Out of Business" status) in year t+1 has exited. This requires building a panel from the cross-sectional licence records — tracking each business across years. The code logic is manageable but the business identity matching (same business, different RSN) is genuinely hard.
2. **Geocoding for neighbourhood assignment**: The `localarea` field is 100% null in the current extract. Neighbourhood assignment requires the geom lat/lon → CoV neighbourhood spatial join. Geocoding coverage is estimated at 60–70% for Vancouver-address records. Businesses that cannot be geocoded must be excluded from neighbourhood-stratified analyses. If non-geocodeable businesses are systematically different (e.g., out-of-city businesses, new businesses with provisional addresses), this is MNAR missingness and the exclusion is not neutral.
3. **The business identity problem**: A restaurant that closes and reopens 6 months later under a new licence number (new RSN) will look like two separate businesses with short tenure. Chains that open a new location each year under separate RSNs will look like many short-tenure businesses. Mitigation: use `businessname` + `street` + `house` to fuzzy-match potential re-licences. This adds engineering effort.
4. **Business type crosswalk**: The 500+ historic categories must be manually classified before survival can be stratified by business type. This is the same crosswalk needed for Candidate 1.

### 7. Learning Value for Andre

**Primary concept: Survival analysis / time-to-event analysis**

This is a method Andre has not used professionally. It teaches: what right-censoring is and why ignoring it biases naive duration estimates downward, how to estimate a non-parametric survival function, what the hazard function means (instantaneous failure rate), and how the Cox model turns survival into a regression problem. Survival analysis is used in: customer churn modelling (extremely common in banking and telco), clinical trials, equipment failure, and employee attrition analysis. Learning it adds a genuinely valuable tool to Andre's analytics toolkit — one that has direct applicability at RBC (customer lifecycle, retention modelling).

**Secondary concept: Semi-parametric regression (Cox model)**

The Cox model is a regression whose outcome is a hazard rate rather than a continuous or binary variable. It introduces the concept of semi-parametric estimation (flexible baseline hazard, parametric covariate effects) — a generalisation beyond the linear/logistic models Andre likely uses. The proportional hazards assumption (and its testability) teaches model diagnostics in a new context.

### 8. Adversarial Pre-Challenge

**Challenge 1 — The licence renewal process is a proxy for survival, not actual survival.**
A business that stops renewing its licence may have closed, or may be operating without a licence (illegal but common in small service businesses), or may have been absorbed into a different licence category (e.g., a coffee shop that also started selling food applied for a separate Food Establishment licence). Conversely, a licence may be renewed administratively even if the business is effectively dormant. This means "licence not renewed" ≠ "business closed" with perfect reliability.

Defense: This is a known limitation of administrative data for business survival measurement. The literature on business demographics (Statistics Canada LEAP database, US Longitudinal Business Database) documents this issue. The mitigation is to use "Gone Out of Business" status as the primary failure indicator (not just lapse in renewal) and to note in the limitations section that the survival curves are lower bounds on actual business longevity (because some "closed" businesses continue without a licence). The finding is still useful — licence survival is the measure, and it has its own policy relevance (compliance with licence requirements is itself a business indicator).

**Challenge 2 — The observation window (2013–2024) is too short for long-lived businesses.**
Many businesses established before 2013 enter the observation window already at tenure > 0 — they are left-truncated. A restaurant that opened in 2003 and is still operating in 2013 has survived at least 10 years before we observe it. The Kaplan-Meier estimator for survival beyond 10 years will be unreliable because most of the observed events (closures) happen in the first 5–7 years of the licence. Only businesses opened 2013 onward can be tracked from their origin.

Defense: Restrict the primary survival analysis to cohorts entering 2013 or later. This gives clean entry dates and avoids left-truncation bias. The trade-off is that we only observe at most 12 years of follow-up. If true median survival is 15 years, we will not observe it — 50% of the cohort will still be alive at the right-censoring date. Report the survival probability at 5 years and 10 years as the primary outputs; median survival is available only for business types where more than 50% have closed within the 12-year window. The 1997–2012 dataset could extend the origin window but creates harmonisation complexity.

**Challenge 3 — Neighbourhood survival differences may reflect business type composition, not neighbourhood effects.**
Downtown has a high concentration of restaurants and retail, which have naturally shorter survival curves than professional offices or contractors. If Downtown has lower survival rates, it may be because it has more restaurants, not because of anything specific to Downtown. A naive comparison of Kaplan-Meier curves by neighbourhood is confounded by business type.

Defense: This is why the Cox model is needed. By controlling for `businesstype` in the Cox model, the neighbourhood coefficient estimates the hazard ratio *after removing business type composition differences*. The Kaplan-Meier curves should be presented separately by business type, not pooled. The headline analysis is: "Within the same business type, do neighbourhood survival curves differ?" — which controls for this confound.

---

## Phase 0 Registers

### Source Register

| ID | Title / Description | Type | Tier | URL or Location | Date Accessed | Used For | Notes |
|----|---------------------|------|------|-----------------|---------------|----------|-------|
| S1 | Vancouver Property Tax Report (2006–2026) | Dataset | T1 | https://opendata.vancouver.ca/explore/dataset/property-tax-report/ | 2026-03-03 | Property value panel, zoning, neighbourhood | 4.25M rows across 4 files; inventory in DATA_INVENTORY.md |
| S2 | Statistics Canada Census Profile 2021 (98-401-X2021007) | Dataset | T1 | https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/... | 2026-03-03 | Demographics, income, housing tenure | 535 CTs, Vancouver CMA. Full details in CENSUS_INVENTORY.md |
| S3 | Statistics Canada Census Profile 2016 (98-401-X2016043) | Dataset | T1 | https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/... | 2026-03-03 | Demographics, income, housing tenure | 478 CTs. Full details in CENSUS_INVENTORY.md |
| S4 | Statistics Canada Census Profile 2011 (98-316-XWE2011001) | Dataset | T1 | https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/... | 2026-03-03 | Demographics (NHS-based for income/education) | 457 CTs. NHS caveats documented in CENSUS_INVENTORY.md |
| S5 | Statistics Canada Census Profile 2006 (94-581-XCB2006005) | Dataset | T1 | https://www12.statcan.gc.ca/open-gc-ouvert/2006/94-581-XCB2006005.ZIP | 2026-03-03 | Demographics baseline | 409 CTs. SDMX-ML format, converted to CSV |
| S6 | City of Vancouver Business Licences 2013–2024 | Dataset | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences-2013-to-2024/ | 2026-03-03 | Business survival, type composition | 782,330 records. Full details in BUSINESS_LICENCES_INVENTORY.md |
| S7 | City of Vancouver Business Licences 1997–2012 | Dataset | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences-1997-to-2012/ | 2026-03-03 | Historical business baseline | 958,899 records. Not yet processed for analysis. |
| S8 | BC Bill 44 — Housing Statutes (Residential Development) Amendment Act, 2023 | Legislation | T1 | https://www.bclaws.gov.bc.ca/civix/document/id/bills/billsprevious/4th42nd:gov44-3 | 2026-03-03 | Upzoning treatment definition (Candidate 2) | Royal assent November 30, 2023 |
| S9 | Vancouver R1-1 Residential Inclusive Zone adoption | Government record | T1 | Vancouver City Council records, October 17, 2023 | 2026-03-03 | Upzoning treatment date (Candidate 2) | Pre-dates provincial Bill 44 deadline |
| S10 | Fischer, Hauf, Stehle — assessed values and DiD attenuation bias | Journal article | T2 | Journal of Banking & Finance (2026); earlier SSRN working paper | 2026-03-03 | Justification for why DiD on assessed values for event studies is problematic | Confirmed existence in adversarial review. Verify DOI before citing. |
| S11 | Caracciolo & Miglino (2024) — "Ripple Effects: The Impact of an Empty-Homes Tax" | Working paper | T3 | SSRN 4919236; C.D. Howe Institute | 2026-03-03 | Background on EHT effects | Verified in ADVERSARIAL_REVIEW.md. 800-meter border design. |
| S12 | Pavlov, Somerville, Wetzel (2024) — "Foreign buyer taxes and housing affordability" | Journal article | T2 | Real Estate Economics 52(3): 928–950 | 2026-03-03 | Background on FBT literature, why our DiD is blocked | Verified in ADVERSARIAL_REVIEW.md. Third author Jake Wetzel noted. |
| S13 | Vancouver Broadway Plan (June 2022) | Government plan | T2 | https://vancouver.ca/home-property-development/broadway-plan.aspx | 2026-03-03 | Exclusion zone for Candidate 2 control group | Boundary: Clark Drive to Vine Street, 1st to 16th Avenues |
| S14 | ADVERSARIAL_REVIEW.md (this project) | Internal document | — | `/home/aurora/projects/sites/portfolio-projects/van-property-tax/ADVERSARIAL_REVIEW.md` | 2026-03-03 | DiD elimination rationale; gap claim verification | Generated 2026-03-03. Not an external source — summarises verification of external sources. |

---

### Assumption Register

| ID | Assumption | Basis | Source Tier | Confidence | Impact if Wrong | Verification Method | Status |
|----|------------|-------|-------------|------------|-----------------|---------------------|--------|
| A1 | The `neighbourhood_code` field (30 codes, 001–030) in the property tax data maps to the 22 City of Vancouver named local areas via a publicly available lookup table | City of Vancouver Open Data Portal publishes a neighbourhood boundary dataset; the 30-code schema is referenced in the data documentation | T4 (documentation reference, not verified) | MEDIUM | Neighbourhood-level aggregation is impossible without the mapping; neighbourhood-stratified analyses fail | Download CoV Local Area Boundary dataset and neighbourhood code lookup; verify all 30 codes match named areas | UNVERIFIED — must resolve before Phase 3 for Candidates 1 and 2 |
| A2 | Census tract boundaries can be spatially joined to CoV neighbourhood boundaries with acceptable accuracy for neighbourhood-level aggregation | Standard GIS operation; CT and neighbourhood boundary shapefiles are publicly available | T1 (StatCan CT shapefiles confirmed available) | HIGH that the join is achievable; MEDIUM on whether CT-to-neighbourhood aggregation introduces significant area-boundary mismatch error | Neighbourhood-level census aggregates will be misaligned with property tax neighbourhood codes if boundaries don't match | Download CT and CoV neighbourhood shapefiles; measure areal overlap; document mismatch rate | UNVERIFIED — required for all three candidates |
| A3 | The `geom` (lat/lon) field in the business licence dataset covers approximately 60–70% of Vancouver-address records after filtering to city=Vancouver | Estimated from snapshot samples in BUSINESS_LICENCES_INVENTORY.md; full CSV not fully analysed | T1 (sample-based estimate) | MEDIUM | If coverage is <40%, neighbourhood-stratified business survival analysis is underpowered and potentially unrepresentative; MNAR exclusion risk | Analyse the full downloaded CSV to compute exact geocoding coverage by folderyear and neighbourhood | UNVERIFIED — blocks Candidate 3 neighbourhood stratification until resolved |
| A4 | Lot square footage can be reliably derived by joining property tax PID to the City of Vancouver parcel shapefile (land area per parcel) | CoV publishes parcel boundary shapefiles; PID is the join key | T1 (CoV Open Data confirmed to publish parcel data) | HIGH | Land value per sqft metric is unavailable; must use total assessed land value without size normalisation | Download CoV parcel shapefile; join to property tax data by PID; measure join rate | UNVERIFIED — needed for Candidate 2 to normalise by lot size |
| A5 | Properties in the Broadway Plan boundary should be excluded from the control group in Candidate 2 because they received their own density upzoning from the Broadway Plan (June 2022) | Broadway Plan is confirmed; its geographic boundary is available | T2 (government plan, confirmed) | HIGH | Including Broadway Plan properties in the control group contaminates the comparison; β will be underestimated | Download Broadway Plan boundary shapefile; flag properties within the boundary | ACCEPTED-WITH-CAVEAT — action required in Phase 4 |
| A6 | A business licence RSN (`licencersn`) that does not appear in year t+1 (or appears with status "Gone Out of Business" or "Inactive") represents a true business exit, not an administrative reclassification or licence splitting | Domain assumption; no documentation of licence system reclassification rules | T6 | MEDIUM | Closure rates overstated if administrative reclassifications are common; survivor bias if businesses reopen under new RSNs | Cross-check a sample of "closed" businesses against the City of Vancouver licence search portal to verify actual closure | UNVERIFIED — load-bearing for Candidate 3 event definition |
| A7 | The `zoning_district` field in the 2022 and 2023 property tax records accurately reflects the RS zone classification for properties that became R1-1 in October 2023 | The property tax data reflects BC Assessment roll data, which reflects CoV zoning; the data should lag actual rezoning by at most one assessment cycle | T4 (inferred from data documentation) | MEDIUM | Treatment assignment may be noisy if the dataset does not consistently reflect mid-year zoning changes | Inspect the 2023 vs. 2024 property tax records for a sample of known RS properties; confirm `zoning_district` reflects R1-1 in the 2024 data | UNVERIFIED — load-bearing for Candidate 2 treatment assignment |
| A8 | BC Assessment values (July 1 valuation date) in the 2024, 2025, and 2026 assessments are the appropriate outcome for measuring zoning capitalization from the October 2023 R1-1 rezoning | The adversarial review confirmed that assessed values are NOT appropriate for event-study identification of short-run policy shocks (due to lag and attenuation). However, for capitalization over 12+ months, the lag is acceptable — the 2024 July 1 valuation is 8.5 months post-rezoning, 2025 is 20.5 months, 2026 is 32.5 months | T2 (Fischer et al. documents the limitation; the long-run capitalization use case is identified by the adversarial review as valid) | MEDIUM | If BC Assessment assessors are conservative and do not fully capitalise zoning rights into land values within 3 years, β will be attenuated below the true economic value of the density rights | Compare assessed value changes in the Broadway Plan boundary (where upzoning effect is longer-running) to test whether BC Assessment does capitalise zoning changes over time | ACCEPTED-WITH-CAVEAT — the lag problem is documented and disclosed; long-run capitalization is the framing, not event-study |
| A9 | The business type crosswalk (mapping 500+ historic categories to signal/neutral/displacement classification for Candidate 1, and to survival analysis strata for Candidate 3) will be consistent and replicable if built using documented rules | Standard data engineering assumption | T6 | LOW | Classification errors in the crosswalk propagate into all downstream analyses; "gentrification signal index" is only as valid as its input categories | Build the crosswalk table in a versioned file with explicit rules; have another person (or adversarial agent review) audit a 20% sample of category assignments | UNVERIFIED — not yet built; must be done before Phase 3 |
| A10 | The 2021 census income data (reference year 2020, pandemic year) is usable as the 2021 control variable in a property value regression if supplemented with the 2016 census income for comparisons that require pre-pandemic baseline income | Documented in CENSUS_INVENTORY.md as A3. 2021 data file also contains 2019 reference-year income as an alternate (Char IDs 204–216). | T1 (known COVID policy context) | HIGH | Using 2020 pandemic income directly in models would understate normal income levels and introduce measurement error correlated with CERB receipt | Use 2019 reference-year income (from 2021 census file) as the income control for post-2020 regressions | ACCEPTED-WITH-CAVEAT — mitigation available; use 2019 reference year |
| A11 | Major infrastructure projects (Broadway Subway / Millennium Line extension, construction ~2019-2025) independently affect localized business survival through reduced foot traffic, road closures, and construction disruption — separate from gentrification dynamics | Broadway Subway is a confirmed $2.83B project with construction along Broadway corridor including stations at Main St–Science World, Mount Pleasant, and others. Construction timelines confirmed via TransLink/BC government announcements. | T1 (government infrastructure project, publicly documented) | HIGH | If not modeled as a covariate, Main Street and Broadway corridor business survival estimates are biased downward during construction period (2019-2025). Post-opening (2026+), the effect reverses as transit access increases foot traffic and land values. | Include distance-to-station and construction-period indicator as covariates in Cox model. Compare survival rates for businesses within 400m of station sites vs. controls further away. | UNVERIFIED — need station locations geocoded and construction timeline confirmed with exact dates |
| A12 | COVID-19 pandemic effects (2020-2022) on business survival can be separated from Broadway Subway construction effects and from neighbourhood gentrification effects | COVID and construction overlap in time (2020-2022). Both suppress business activity but through different mechanisms: COVID is city-wide, construction is localized. | T6 (analytical assumption — no source confirms separability) | LOW | If effects cannot be separated, the Cox model coefficients for neighbourhood and construction are biased. The three shocks (COVID, construction, gentrification) are confounded during 2020-2022. | Use city-wide COVID effect as a baseline (all neighborhoods equally affected) and measure construction as a DIFFERENTIAL effect within the COVID period. Test with neighbourhood-level COVID restriction data if available. | UNVERIFIED — load-bearing for any Candidate 3 analysis covering 2020-2022 window |
| A13 | Business licence expiry or non-renewal represents true business closure, not seasonal lapse or administrative reclassification | Extends A6. Seasonal businesses (ice cream shops, patios) may let licences lapse over winter and renew in spring. This creates false death-and-rebirth events in the data. | T6 (domain inference — no documentation of seasonal licence patterns) | MEDIUM | Closure rates overstated for seasonal business types. Survival curves for food/beverage category are biased downward if seasonal lapses are counted as exits. | Check for RSNs that "die" and reappear within 6 months. If prevalent, define "death" as non-renewal for 12+ consecutive months instead of any lapse. | UNVERIFIED — must resolve before defining the survival event for Candidate 3 |
| A14 | Lease terms and rent levels are not observable in our data, and business closure is used as a proxy for economic displacement | Business licence data shows when a business closes but not why. A business may close due to: rent increase (displacement), poor management, market shift, retirement, etc. We cannot distinguish these causes. | T6 (structural data limitation) | HIGH | We cannot claim "gentrification killed this business" — only "this business closed in a gentrifying neighbourhood." Causal language must be avoided. | Acknowledged limitation. Mitigate by controlling for business type and age. Disclose prominently in Phase 8 communication. | ACCEPTED-WITH-CAVEAT — fundamental data limitation, must be disclosed in all outputs |

---

## Scope Boundaries

What this project will NOT address, regardless of which candidate question is selected:

1. **Causal identification of the Foreign Buyer Tax, Empty Homes Tax, or Speculation and Vacancy Tax effects on assessed property values.** The adversarial review documented why this is not feasible with publicly available data and the BC Assessment lag structure.
2. **Individual-level displacement outcomes.** We do not have data on tenants, evictions, or individual household moves. The analysis operates at property and neighbourhood level.
3. **Transaction prices or MLS data.** All analysis uses assessed values, not sale prices. The two are related but not identical. We will not claim to measure "what people paid" — only "what BC Assessment says the property is worth."
4. **Foreign buyer identity or beneficial ownership.** The Land Owner Transparency Registry (launched 2021) is not in our dataset inventory and is not required for any of the three candidate questions.
5. **Affordability outcomes for renters.** Rents, rental availability, and tenant affordability are not measurable from our three datasets. The analysis covers the supply side (properties, assessments, business licences) and the neighbourhood demographic side (census), not individual affordability.
6. **Metro Vancouver municipalities outside the City of Vancouver.** The property tax dataset and business licence dataset cover only the City of Vancouver. Census data covers the CMA but will be filtered to the City boundary for consistency.

---

## Phase 0 Gate Checklist

Per DATA-PROJECT-RIGOR.md, the gate to Phase 1 requires:

- [x] Research question candidates are crisp (one sentence each — see Section headings above)
- [x] Assumption register started — 10 entries, all with confidence and status
- [x] Source register started — 14 entries, all with tier and provenance
- [x] Adversarial pre-challenge run on all three candidates (Section 8 of each candidate)
- [x] Scope boundaries explicitly documented (what this analysis will NOT address)
- [ ] At least one T1-T2 source supports the feasibility of answering each question — **PARTIAL**
  - Candidate 1 (clustering): FEASIBLE — property and census data are T1; method is standard; no blocking constraint identified
  - Candidate 2 (upzoning capitalization): FEASIBLE — property data is T1; TWFE method is established for this use case; adversarial review explicitly identifies long-run capitalization as the valid use of assessed values
  - Candidate 3 (business survival): FEASIBLE — business licence data is T1; survival analysis is well-established; geocoding gap is the primary risk to neighbourhood stratification

**Gate status**: CONDITIONAL PASS. Proceed to selection of one candidate. Before Phase 1 work begins on the selected candidate, A1 (neighbourhood code lookup) and A3 (geocoding coverage in business licences) must be verified — they are blocking for Candidates 1 and 3 respectively.

---

## Recommendation on Candidate Selection

This is not a decision the framework makes — Andre selects. But here is the honest assessment of the tradeoffs:

**Candidate 1 (Trajectory Clustering)** is the most interesting to a Vancouver audience and the most novel combination of data sources. It requires the most pre-processing work (business type crosswalk, spatial joins, feature engineering) and teaches clustering — a genuinely new skill. The N=30 sample size is its structural weakness.

**Candidate 2 (Upzoning Capitalization)** is the most methodologically rigorous, the most directly relevant to ongoing Vancouver policy debate, and the most teachable single-method project. TWFE panel regression is a foundational skill with direct career applicability. The parallel trends assumption is the primary risk and is testable. The adversarial review explicitly identified this as the valid use case for BC Assessment data.

**Candidate 3 (Business Survival)** is the most original in terms of method (survival analysis is rarely applied to business licence data at this geographic granularity). It teaches the most transferable skill for banking analytics (customer churn / survival modelling). The event definition and geocoding challenges are manageable but real. It is the least connected to housing policy specifically and the most connected to commercial ecosystem health.

If the goal is one strong portfolio project with a clean method, a defensible design, and direct Vancouver relevance: **Candidate 2** is the most publication-ready. If the goal is to build a richer descriptive story that people in Vancouver will immediately relate to: **Candidate 1**. If the goal is to learn a new method with the most career transferability: **Candidate 3**.

All three are feasible with the data we have. None require data we don't have.

---

*Document generated 2026-03-03. Rigor controls applied per DATA-PROJECT-RIGOR.md v1.0.*
*Next document: `PHASE0_SELECTED.md` — after candidate is chosen, record the selection rationale and begin Phase 1 with the selected question.*
