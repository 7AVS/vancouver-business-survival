# Phase 0 — Selection Rationale
**Project**: Vancouver Business Survival / Gentrification Analysis
**Selected Question**: Candidate 3 — Business Survival Analysis
**Date**: 2026-03-03
**Framework**: DATA-PROJECT-RIGOR.md v1.1
**Author**: Andre Santos

---

## The Selected Research Question

> Does business survival depend on neighbourhood, and does it correlate with land value appreciation? Specifically: do businesses in higher-appreciation neighbourhoods face systematically higher closure hazards, after controlling for business type and neighbourhood composition?

---

## 1. Why This Question

### The Personal Hook

A friend of mine owns an ice cream shop on Main Street, near the Broadway Subway construction site. For the past few years he has been watching his neighbourhood change: storefronts turning over, rents rising, familiar faces disappearing. He is not sure whether his lease renewal in 2027 will reflect what the block looks like today or what a developer thinks it could be worth.

That question — "what are my odds?" — is not hypothetical to him. It is the thing he thinks about at the end of a slow Tuesday in January. And there is no publicly available answer. No one has put a number on it.

I live in Vancouver. I have watched Strathcona shift, watched Mount Pleasant price out the people who made it interesting, watched the machine print "For Lease" signs faster than new tenants can fill them. The discourse around gentrification here is vivid and opinionated and almost entirely without data. People say "small businesses are being pushed out" — but how quickly? Where? Is it getting worse? Nobody knows, because nobody has looked at the full 12-year licence record and done the survival math.

That is what this project does.

### The Professional Hook

I have spent 10 years in banking analytics. The technical core of this project — survival analysis, right-censoring, Cox proportional hazards regression — is the same mathematics that runs underneath customer churn modelling, credit risk, and employee attrition. At RBC, I built the Vintage Engine: a cohort-based measurement system that tracks performance curves over time. That is survival analysis with different language on top of it.

The Cox model is essentially a churn model where the "customer" is a business licence and the "event" is not a cancelled credit card but a "Gone Out of Business" status update in the City of Vancouver's open data portal. The mathematics transfer directly. What this project adds is that I will finally learn to call it by its correct name and use the full toolbox: Kaplan-Meier estimators, log-rank tests, Schoenfeld residual diagnostics, time-varying covariates.

That combination — genuine personal motivation plus direct professional relevance — is what made Candidate 3 the right choice.

---

## 2. What Was Considered and Why Candidate 3 Won

Three candidate questions were evaluated against the same three datasets (City of Vancouver property tax records 2006–2026, business licences 2013–2026, and Statistics Canada census profiles 2006–2021). All three were assessed for methodological feasibility, data availability, adversarial challenges, and portfolio value. Full evaluation is documented in `docs/PHASE0_CANDIDATES.md`.

### Candidate 1 — Neighbourhood Trajectory Typology

**The question**: Can we classify Vancouver's 30 neighbourhoods into statistically distinct gentrification trajectory types using 20 years of assessed land value growth, census demographic shift, and business composition change?

**Why it was appealing**: This is the question most legible to a general Vancouver audience. A map showing "your neighbourhood is in the same trajectory cluster as Gastown was in 2006" would be immediately shareable. Clustering also teaches genuinely new skills: unsupervised machine learning, PCA, silhouette analysis.

**Why it did not win**: The method has a fundamental N=30 problem. With 30 neighbourhoods and 3–5 clusters, you are working with 6–10 observations per group. K-means at that scale is sensitive to outliers and initialisation. The result is a descriptive typology that cannot support strong inferential claims. The analysis describes patterns; it cannot test hypotheses. For a portfolio piece, that is a limitation — there is no p-value to hang a conclusion on.

### Candidate 2 — Bill 44 Upzoning Capitalization

**The question**: Did the 2023 R1-1 rezoning produce a measurable premium in assessed land values for formerly-single-family-zoned properties relative to already-multifamily properties?

**Why it was appealing**: Two-way fixed effects panel regression is the gold standard for before/after quasi-experiments with panel data. The adversarial review explicitly identified long-run capitalization as the valid use case for BC Assessment data (after closing the DiD-on-assessed-values angle for event studies). The question is directly relevant to anyone who owns property in Vancouver — a large audience.

**Why it did not win**: The parallel trends assumption is the load-bearing claim, and it is fragile. Single-family neighbourhoods (Shaughnessy, Dunbar, Kerrisdale) were already on different value trajectories than inner-city multi-family areas before 2023. The within-neighbourhood restriction helps but does not fully resolve this. Additionally, the October 2023 rezoning is simultaneous with a Bank of Canada rate-cutting cycle beginning June 2024 — two confounds happening close in time make clean identification difficult with only 3 post-treatment years of data. Candidate 2 is arguably the most methodologically demanding to execute *correctly*, and the risk of producing a result with a fatal identification flaw is higher here than in the other two candidates.

### Candidate 3 — Business Survival Analysis (Selected)

**The question wins on four dimensions:**

1. **Methodological fit**: Survival analysis is the right tool for this question in a way the other methods are right tools for their questions. Right-censoring is not a workaround — it is the correct treatment of businesses that are still active at the end of the observation window. The data structure (business enters, business exits or is censored) matches the method (Kaplan-Meier, Cox) almost exactly.

2. **Learning value**: Of the three candidates, Candidate 3 teaches the method with the highest direct transferability to banking analytics. Cox proportional hazards is churn modelling. I already understand the domain problem (customer lifecycle, cohort analysis) — this project extends that into the formal statistical framework I have not used professionally. The other two candidates teach important skills, but they teach them at lower intensity of professional relevance.

3. **The natural experiment**: The Broadway Subway construction (2019–2025) passes directly through the neighbourhood where my friend's shop operates. It creates a quasi-natural experiment embedded within the analysis: do businesses within 400 metres of a station site face elevated closure hazards during the construction period, and does that reverse post-opening? This is a specific, testable hypothesis inside the broader survival analysis that the other candidates do not have.

4. **Honest deliverable**: A Kaplan-Meier survival curve is immediately interpretable to a non-technical reader. A line that shows "by year 5, only 46% of restaurants in Mount Pleasant are still operating" is legible to anyone. The deliverable communicates directly, without requiring the reader to understand fixed effects or cluster validation.

---

## 3. Feasibility Assessment

The EDA confirmed that this analysis is tractable with the data available.

### Business Licence Panel

From 638,646 commercial licence records spanning FY2013–FY2026, the commercial pipeline identified:

- **127,255 unique trackable businesses** (85.2% trackable across 2+ years)
- **Median survival: 5 years** (KM estimate on the full commercial panel)
- **1-year survival: 87.4%** — roughly 1 in 8 businesses does not make it through its first full year
- **5-year survival: 46.4%** — the majority of businesses are gone within 5 years
- **10-year survival: 26.8%** — the long-term picture is stark

The survival curves are clean and right-censored appropriately. FY2026 records are mid-cycle and treated as censored in all KM estimates. The data volume is sufficient for neighbourhood-stratified and business-type-stratified analyses.

Survival rates differ meaningfully by business type:

| Business Type | 1yr | 3yr | 5yr |
|---|---|---|---|
| Long-term Rental | 95% | 88% | 87% |
| Health Services | 82% | 45% | 26% |
| Restaurant Class 1 | 85% | 50% | 29% |
| Retail Dealer | 76% | 38% | 19% |
| Contractor | 77% | 34% | 17% |

The spread across business types confirms that business-type stratification is essential before making any neighbourhood comparisons. This is exactly what the Cox model handles.

### Land Value Panel

The property tax panel covers 16 named local areas with 21 years of complete annual data (2006–2026), yielding 4,201,387 property-year records. Cumulative land value appreciation from 2007 varies enormously across neighbourhoods:

- **Highest**: Sunset (+222.6%), Riley Park (+219.6%), Shaughnessy (+211.3%)
- **Lowest**: Killarney (+59.4%), Strathcona (+90.2%), Marpole (+116.9%)

This spread — a 3.5x difference between Sunset and Killarney — gives the Cox model real variation to work with when testing whether neighbourhood land value growth predicts closure hazard. The variation is not subtle; if the effect exists, the data should find it.

Annual median land values are available as time-varying covariates, which is the correct treatment for a factor that changes year by year throughout each business's observation window.

### Coverage Gap

Six of the City of Vancouver's 22 named local areas are absent from the property tax panel: Grandview-Woodland, Kensington-Cedar Cottage, Kitsilano, South Cambie, Victoria-Fraserview, and West Point Grey. These areas do not appear in the neighbourhood code mapping used by BC Assessment. For the Cox model, businesses located in these 6 areas will not receive a land value covariate and will need to be handled separately (either excluded from the time-varying covariate analysis, or assigned the city-wide median as a fallback). This is a known limitation documented in the assumption register (A1).

---

## 4. Methodological Fit

The business survival question is structurally well-matched to survival analysis in ways worth stating explicitly.

### Right-Censoring Is the Correct Treatment

At the end of our observation window (FY2025 as the reliable endpoint, FY2026 treated as mid-cycle), many businesses are still active. A naive approach would either exclude them (throwing away valid data) or treat them as failed (biasing survival rates downward). Kaplan-Meier handles this correctly: businesses that are still "Issued" at the end of the window are right-censored — they contribute information about having survived to their last observed year but do not count as failures. This is not a workaround; it is the correct model of the data-generating process.

### Time-Varying Covariates

Land values change every year. A restaurant operating in Mount Pleasant in 2013 faces a different land value environment than the same restaurant in 2019, even if it has never moved. The Cox model with time-varying covariates accommodates this directly: each business-year row carries the neighbourhood median land value for that year, and the model estimates the effect of current land value growth on the instantaneous closure hazard. This is more accurate than assigning each business a single neighbourhood land value score at entry.

### Multiple Covariates Without Stratification Explosion

The natural alternative to Cox regression is to stratify Kaplan-Meier curves by every combination of neighbourhood × business type × period. With 20 neighbourhoods, 6 major business type categories, and 3 time periods, that produces 360 cells — most of which are too small for reliable KM estimation. The Cox model handles this through regression: it estimates a single hazard ratio for each covariate while conditioning on the others. The result is interpretable at the covariate level ("neighbourhood with 10% higher land appreciation has X% higher hazard") rather than requiring the reader to compare 360 survival curves.

### The Broadway Subway as Natural Experiment

A12 in the assumption register documents the challenge: COVID-19 (2020–2022) and Broadway Subway construction (2019–2025) are confounded in time. Both suppress business activity through different mechanisms. The survival analysis can partially address this by including both as covariates: a city-wide COVID-period indicator (common to all businesses) and a construction-zone indicator (businesses within 400 metres of a station site on the Broadway corridor). If the construction effect is real and separable, we would expect elevated closure hazards in the construction zone during 2019–2025 that narrow after the line opens. This is testable.

It is also personally relevant: my friend's shop on Main Street near Broadway is squarely inside this zone.

---

## 5. Known Limitations

Documenting these upfront is not pessimism — it is methodology. Every one of these appears in the assumption register with a verification status.

### Correlation, Not Causation (A14)

Business licence data shows when a business closes. It does not show why. A restaurant that closes in a neighbourhood with rapidly appreciating land values may have closed due to a rent increase, or due to poor management, or because the owner retired, or because the demographic mix of the neighbourhood no longer matched the menu. We cannot distinguish these causes from licence records alone.

The correct language throughout this project is: "businesses in high-appreciation neighbourhoods face higher hazards of closure, after controlling for business type and neighbourhood composition." Not: "gentrification killed this business." The Cox coefficient on land value growth is an association measure, not a causal estimate. This distinction is explicit in the deliverable.

### COVID Confounding (A12)

The observation window includes 2020–2022, during which pandemic-related closures were city-wide and mandatory. The closure hazard during this period reflects government health orders, not underlying neighbourhood economics. The Cox model will include a COVID-period indicator as a covariate, and survival curves will be presented separately for pre-COVID and post-COVID periods. However, the 2020–2022 period cannot be fully cleaned of pandemic effects. Any claim about business closure rates during that window carries this caveat.

### 6 Missing Areas in Land Value Data (A1)

Grandview-Woodland, Kensington-Cedar Cottage, Kitsilano, South Cambie, Victoria-Fraserview, and West Point Grey are not in the property tax neighbourhood panel. Businesses in these areas will not receive a neighbourhood land value covariate in the Cox model. This is a source data limitation, not an analytical choice. The survival curves for these neighbourhoods will be KM-only (no Cox covariate available). The effect is that our Cox estimates represent 16 of 22 neighbourhoods, with the missing 6 disproportionately in west-side and east-side residential corridors.

### Schema Break at FY2024 (A6, A13)

The business licence data has a documented schema discontinuity between the archive extract (FY2013–FY2023) and the current extract (FY2024–FY2026). The most significant difference is the `localarea` field, which is blank for all pre-2024 records. For the years 2013–2023, neighbourhood assignment must rely on geocoordinates (`geo_point_2d`), which have 59–65% coverage in those years. Businesses without geocoordinates cannot be assigned to a neighbourhood and must be excluded from neighbourhood-stratified analyses.

This is not a minor footnote: approximately 35–40% of the pre-2024 records may not be assignable to a neighbourhood. The survival curves presented with neighbourhood stratification represent the geocoded subsample, not the full population. The assumption that the non-geocoded records are MCAR (missing completely at random) is logged as A3 and must be verified before the neighbourhood-stratified analysis is treated as representative.

### Home-Based Business Address Issue (A15, not yet in register)

The business licence address field captures the licence address, not necessarily the physical operating location. Home-based businesses registered to a residential address in an affluent neighbourhood may not belong to the commercial ecosystem of that neighbourhood. This introduces noise in the neighbourhood assignment for businesses that operate remotely or out of a residential location. For the survival analysis, the bias is likely small (home-based businesses have different survival profiles than street-facing commercial tenants, and the Cox model controls for business type), but it is worth flagging.

---

## 6. Portfolio Value

This project exists for one purpose: to demonstrate what I can do to a hiring manager in data science or analytics. Here is what it demonstrates.

### End-to-End Data Science Pipeline

This is not a Kaggle notebook with a pre-cleaned CSV. The data came from a government open data portal, required merging four separate property tax files with mismatched schemas, required commercial filtering from a 638K-row business licence dataset, and required building a business-level panel from cross-sectional annual records. The pipeline is documented, reproducible, and auditable. That is the actual work of applied data science: most of the effort is in the data, not in the model.

### Working With Messy Real-World Government Data

Government administrative data is structured for administrative purposes, not analytical ones. The business licence dataset has a `localarea` field that is blank for 11 of 14 years of data. The property tax dataset maps neighbourhoods through a 30-code lookup with confidence weights, not a clean foreign key. The schema changes between the archive extract and the current extract. Dealing with these problems competently — documenting them, making principled decisions about how to handle them, and disclosing limitations honestly — is what separates a professional data scientist from someone who can only work with clean data.

### Survival Analysis and Cox PH

Survival analysis is used in customer churn (banking, telecom), clinical trials, credit risk modelling, and equipment failure. The Cox proportional hazards model is the standard method for multi-covariate time-to-event analysis across all of these domains. Demonstrating it on a novel application — business licence survival — shows the ability to apply the method in a new context. For any role in banking analytics, retention modelling, or risk, the underlying technique is directly transferable.

### Rigorous Methodology With Documented Assumptions

Every analytical decision in this project is logged in the assumption register with a source tier, confidence level, and verification status. Every claim is traceable to its source. Limitations are disclosed in the body, not buried in a footnote. The adversarial pre-challenge was run before any modelling began. This is the framework (DATA-PROJECT-RIGOR.md v1.1) applied to a real project — not as a compliance exercise but as a genuine quality control mechanism. An employer reviewing this project can trace any number in the deliverable back to the raw data and the decisions made along the way.

### Domain Knowledge — Vancouver Real Estate and Municipal Data

I live here. I understand the difference between Killarney and Kitsilano, between a heritage district's business mix and a Broadway corridor's. I know what the Broadway Subway construction looks like from street level because I have been walking past it for five years. Domain knowledge is underrated in data science; it determines what questions are interesting and which results make sense. This project is not generic survival analysis applied to an arbitrary dataset — it is a specific question about a city I know, applied to data I have verified, in service of an answer that matters to people who live here.

---

## Phase 0 Gate Status

Per DATA-PROJECT-RIGOR.md v1.1, the gate to Phase 1 requires the research question to be crisp, the assumption register to be started, the source register to be started, and an adversarial pre-challenge on the framing to be documented.

- [x] Research question is one clear sentence
- [x] Assumption register — 14 entries at Phase 0 (A1–A14), including A12 (COVID confounding) and A13 (seasonal lapse) which are Candidate 3-specific
- [x] Source register — 14 entries, all T1 or T2 primary datasets
- [x] Adversarial pre-challenge on Candidate 3 documented in `PHASE0_CANDIDATES.md`, Section 8 (three challenges, three defenses)
- [x] Scope boundaries documented (what this analysis will NOT address)
- [ ] A3 (geocoding coverage verification) — BLOCKING for neighbourhood stratification. Must be quantified before the neighbourhood-stratified survival curves are treated as representative.
- [ ] A6/A13 (event definition validation — lapse vs. closure) — BLOCKING for the survival event definition. A sample check against the CoV licence portal is required before the KM estimator is finalized.

**Gate status**: CONDITIONAL PASS. Selected question proceeds to Phase 1. A3 and A6/A13 are the two blocking assumptions — they must be verified before Phase 3 analysis begins on the neighbourhood-stratified outputs.

---

## What This Is Not

For the record: this analysis will not produce a causal estimate of "how much gentrification kills small businesses." The data does not support that claim and no amount of methodological sophistication would change that. We cannot observe lease terms, we cannot observe reasons for closure, and we cannot randomise which neighbourhoods appreciate faster.

What this analysis will produce is a precise, defensible, quantified description of how business survival hazards vary across Vancouver's neighbourhoods and whether that variation correlates with assessed land value appreciation. That is enough to be interesting. It is also, importantly, honest — which is more than most of the discourse on this topic manages to be.

---

*Selection rationale finalized 2026-03-03. Rigor controls applied per DATA-PROJECT-RIGOR.md v1.1.*
*Proceed to: `Phase 1 — Data Acquisition` for the selected candidate.*
