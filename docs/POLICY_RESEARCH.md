# Vancouver Housing Policy Research
## Policy Timeline, Academic Literature, and DiD Design Notes

**Project**: Vancouver property value trajectory analysis
**Purpose**: Research foundation for a difference-in-differences (DiD) portfolio project
**Date compiled**: 2026-03-03

---

## Part 1: Policy Timeline (2015–2025)

Each entry includes: effective date, mechanism, target, geographic scope, and amendments.

---

### 1. BC Foreign Buyer Tax (Additional Property Transfer Tax)

**Effective date**: August 2, 2016
**Legislative vehicle**: Bill 28 — Miscellaneous Statutes (Housing Priority Initiatives) Amendment Act, 2016; amends the Property Transfer Tax Act
**Initial rate**: 15% of fair market value on the proportionate share held by a foreign entity
**Mechanism**: A surcharge on top of the standard Property Transfer Tax (PTT), collected at time of registration of the property transfer. Applies to any purchase by a "foreign entity" (foreign nationals, foreign corporations, taxable trustees).
**Target**: Foreign buyers (non-Canadian nationals and controlled corporations) purchasing residential real estate
**Geographic scope**: Greater Vancouver Regional District only (Metro Vancouver), excluding treaty lands of Tsawwassen First Nation

**Amendment — February 21, 2018**:
- Rate increased from 15% to 20%
- Geographic scope dramatically expanded to include: Fraser Valley Regional District, Capital Regional District (Victoria), Regional District of Nanaimo, Central Okanagan Regional District
- This expansion was part of the 2018 BC Budget under the NDP government

**Notes for research design**: The August 2, 2016 date is a clean, hard shock applied only to Metro Vancouver. The February 2018 expansion to other regional districts creates a second quasi-experimental event. The 2016 shock is preferred for DiD because it is more geographically bounded and less anticipated. There was no COVID suspension of this tax — the federal Prohibition Act (see below) overlaps from Jan 2023.

---

### 2. Vancouver Empty Homes Tax (Vacancy Tax)

**Effective date**: January 1, 2017 (first taxable vacancy reference period: Jan 1–Dec 31, 2017)
**Legislative vehicle**: City of Vancouver Vacancy Tax By-law (By-law No. 11674)
**Initial rate**: 1% of assessed taxable value
**Mechanism**: Annual municipal tax levied on residential properties that are vacant for more than 6 months per year. Property owners must file an annual declaration. Failure to declare = deemed vacant = tax applies. Revenue directed to affordable housing initiatives.
**Target**: Property owners leaving homes vacant (speculators, absentee owners, non-primary-residence holders)
**Geographic scope**: City of Vancouver only (not Metro Vancouver, not other municipalities)

**Rate changes**:
- 2017 reference year: 1% (effective for 2018 tax payment)
- 2019 reference year: 1% (held flat)
- 2020 reference year: 1.25% (slight increase)
- 2021 reference year: 3% — **Council voted November 25, 2020** to triple the rate. Effective immediately for the 2021 vacancy period.
- 2022 onward: 3% (maintained)

**Results reported by the City**:
- Declared vacant properties fell from ~2,500 (2017) to under 1,000 (2024 reference year)
- Vacancy rate dropped from ~0.9% to 0.49% of total housing stock
- Revenue recycled into affordable housing programs

**Notes for research design**: The City of Vancouver boundary creates a natural treatment group. Surrounding Metro Vancouver municipalities (Burnaby, Richmond, New Westminster, North Vancouver, etc.) that do NOT have an equivalent municipal vacancy tax serve as a plausible control group pre-2018. After 2018 the BC SVT (below) complicates this because it applies province-wide in designated areas, affecting both treatment and control.

---

### 3. BC Speculation and Vacancy Tax (SVT)

**Effective date**: The Speculation and Vacancy Tax Act received royal assent as SBC 2018, c. 46. The first tax year was 2018. The regulation (B.C. Reg. 275/2018) came into force December 10, 2018.
**Legislative vehicle**: Speculation and Vacancy Tax Act, SBC 2018, c. 46
**Mechanism**: Annual provincial tax on residential property based on how the property was used. Owners must file an annual declaration. Properties that are rented for at least 6 months per year (to unrelated parties) are typically exempt. The tax rate varies by the owner's residency and citizenship status.
**Target**: Non-resident owners, satellite families (Canadian tax residents whose household income is primarily earned outside Canada), and domestic speculators holding vacant or underused residential property
**Geographic scope**: Designated taxable regions (not all of BC), covering:
- Metro Vancouver (excluding Bowen Island, Village of Lions Bay, Tsawwassen First Nation lands)
- Capital Regional District (excluding Salt Spring Island, Southern Gulf Islands, Juan de Fuca Electoral Area)
- District of Mission, City of Abbotsford, City of Chilliwack (Fraser Valley)
- City of Kelowna, West Kelowna (Central Okanagan)
- City of Nanaimo, District of Lantzville (Nanaimo area)

**Rate structure**:
- BC residents (Canadian citizens/PRs): 0.5% of assessed value
- Other Canadian citizens/PRs not in satellite family: 0.5%
- Foreign owners and satellite families: 2%

**Amendments**:
- 2019: Rental exemption clarified — property must be rented for at least 6 months to be exempt
- November 2023: BC government announced expansion to additional communities, with those new areas first declaring in January 2025 (for 2024 tax year)
- February 2026: Further amendments announced in the 2026 BC Budget (details emerging)

**Revenue**: Approximately $230M collected for 2018, 2019, and 2020 tax years combined. Government claims the SVT added over 20,000 units to long-term rental supply, though critics note attribution is difficult given simultaneous EHT and STR regulations.

**Notes for research design**: The SVT creates a complex treatment because it applies at differential rates to different ownership types within the same geographic area. This makes individual-level treatment intensity variable rather than a clean geographic cutoff. The 0.5% domestic rate is unlikely to cause major behavioral change; the 2% foreign rate is the meaningful shock.

---

### 4. Federal Underused Housing Tax (UHT)

**Effective date**: January 1, 2022
**Legislative vehicle**: Underused Housing Tax Act, SC 2022, c. 5
**Rate**: 1% annually of taxable value (assessed or fair market value, at owner's choice)
**Mechanism**: Annual federal tax on vacant or underused residential property. Most Canadian citizens and permanent residents are "excluded owners" and exempt from the tax itself, though they may still have a filing obligation. The tax falls primarily on non-resident, non-Canadian owners.
**Target**: Non-Canadian owners of residential property; also some Canadian partnerships, trusts, and private corporations (who must file even if ultimately exempt)
**Geographic scope**: All of Canada

**Elimination**: The 2025 federal Budget announced the UHT would be eliminated as "inefficient." As of early 2026 the elimination is in progress — new filings are not required for 2024 and later tax years for most owners.

**Notes for research design**: The UHT is a federal overlay on top of BC's existing foreign buyer and SVT regimes. At 1%, the rate is lower than either the PTT surcharge (20%) or the SVT (2%). Its primary effect may be on compliance and disclosure rather than on market prices. Likely a second-order factor in any DiD analysis of Vancouver property values.

---

### 5. Federal Prohibition on Purchase of Residential Property by Non-Canadians

**Effective date**: January 1, 2023
**Legislative vehicle**: Prohibition on the Purchase of Residential Property by Non-Canadians Act, SC 2022, c. 18
**Mechanism**: An outright ban (not a tax) on non-Canadians purchasing residential real estate in Canada. This is a prohibition, not a price disincentive — non-compliant transactions can face fines up to $10,000 and orders to sell the property.
**Target**: Non-Canadians (foreign nationals and controlled corporations). Permanent residents and temporary residents meeting specific criteria are exempt.
**Geographic scope**: All of Canada
**Duration**: Originally 2 years (Jan 2023–Dec 2024). Extended February 4, 2024 for an additional 2 years, to January 1, 2027.

**March 2023 amendments**:
- Buildings with 4+ dwelling units excluded (commercial investment exemption)
- Vacant land zoned residential or mixed-use excluded
- Non-Canadians permitted to purchase for development purposes

**Notes for research design**: This policy creates a hard break starting Jan 2023 that effectively prohibits the activity the 2016 Foreign Buyer Tax was trying to price-discriminate against. This means any DiD analysis looking at the 2016–2022 period using foreign buyer concentration as the treatment axis must account for this as a structural break at the end of the study window.

---

### 6. BC Short-Term Rental (STR) Restrictions

**Effective date**: May 1, 2024
**Legislative vehicle**: Short-Term Rental Accommodations Act, SBC 2023, c. 38
**Mechanism**: Restricts short-term rentals (platforms like Airbnb, VRBO) to the principal residence of the host plus one additional suite or laneway home on the same property. Effectively bans the use of investment properties as full-time STRs. Provincial Short-Term Rental Compliance Enforcement Unit established with authority to issue administrative monetary penalties.
**Target**: Property owners operating STRs in non-principal-residence properties (i.e., investment property owners converting long-term rental supply to Airbnb)
**Geographic scope**: Municipalities with populations over 10,000 across BC (60+ communities). An additional 17 communities voluntarily opted in with an effective date of November 1, 2024.

**Notes for research design**: This is a 2024 event, relatively recent, and its price effect would primarily operate through the conversion of former STR units back to long-term rental supply (increasing supply, softening rent levels). For property value DiD, the effect could be negative for properties in high-STR-density neighborhoods (e.g., Granville Island area, Coal Harbour, Gastown) as the rental income potential of those properties drops. Pre/post comparisons using STR listing density by neighborhood as the treatment proxy are plausible.

---

### 7. Vancouver Broadway Plan

**Effective date**: Approved by Vancouver City Council in June 2022. Implementation is ongoing and phased — rezoning applications began after approval.
**Geographic scope**: Broadway corridor from Clark Drive (east) to Vine Street (west), between 1st and 16th Avenues
**Mechanism**: A 30-year land use plan providing density allowances and zoning permissions for residential and commercial development along the Broadway Subway corridor. Allows mixed-use towers up to 40 storeys near new subway stations; residential towers up to 20 storeys for replacement of smaller aging rentals. Target of 30,000 new homes over 30 years.
**December 2024 update**: Council approved amendments to add 41,500 new homes over 30 years (revised upward from 30,000). October 2025 public hearing adopted new low-rise (R3), mid-rise (R4), and high-rise (R5) apartment zones in Broadway and Cambie Corridor areas.
**Target**: Density increases for market strata (34%), market rental (46%), social housing (12%), below-market rental (7%)

**Notes for research design**: The Broadway Plan creates geographically bounded upzoning treatment. Properties within the plan boundary gain significant density rights — this should capitalize into land values even before construction begins. Comparing Broadway-area properties to matched comparison neighborhoods outside the plan area before and after June 2022 is a clean DiD setup for measuring zoning capitalization.

---

### 8. BC Bill 44 — Small-Scale Multi-Unit Housing (SSMU)

**Effective date**: Royal assent November 30, 2023. Local governments required to update zoning bylaws by June 30, 2024.
**Legislative vehicle**: Housing Statutes (Residential Development) Amendment Act, 2023 (Bill 44)
**Mechanism**: Mandates that all BC municipalities allow 3–4 dwelling units on any single-family residential lot (up to 6 units for larger lots near transit). Eliminates single-family-only zoning as a class in municipalities over 5,000 population. Municipalities that do not comply by June 30, 2024 face provincial override.
**Target**: Local government exclusionary zoning — aimed at democratizing housing supply province-wide
**Geographic scope**: All municipalities in BC with population over 5,000

**Vancouver implementation**: Vancouver City Council adopted the new R1-1 Residential Inclusive Zone (replacing RS-1 through RS-9 zones) on October 17, 2023 (pre-dating the provincial Bill 44 requirement). The R1-1 zone permits multiplexes up to 6 units province-wide. By 2024, multiplex applications represented ~50% of R1-1 application volume.

**Notes for research design**: This is a province-wide supply shock. A DiD using pre/post would need to find a valid control group — possibly jurisdictions outside BC, or municipalities within BC that were already close to these density thresholds. The capitalization effect is ambiguous: in high-demand areas, more supply rights on a parcel may increase land value; in lower-demand areas the effect could be neutral or negative (if it signals the end of single-family exclusivity premiums).

---

### 9. Bank of Canada Interest Rate Cycle (Major Housing Market Driver)

These are not housing policies per se, but they are the dominant confound in any property value analysis spanning 2019–2023.

**COVID-19 emergency rate cuts**:
- March 2020: Bank of Canada cut overnight rate to 0.25% (emergency floor) in response to pandemic
- Rate held at 0.25% from March 2020 through early 2022
- Ultra-low rates drove a demand surge — Vancouver benchmark prices rose steeply through 2020–2022

**Rate hike cycle — 2022**:
- March 2, 2022: +25 bps → 0.50%
- April 13, 2022: +50 bps → 1.00%
- June 1, 2022: +50 bps → 1.50%
- July 13, 2022: +100 bps → 2.50% (largest single hike since 1998)
- September 7, 2022: +75 bps → 3.25%
- October 26, 2022: +50 bps → 3.75%
- December 7, 2022: +50 bps → 4.25%

**2023 additional hikes and hold**:
- January 25, 2023: +25 bps → 4.50%
- March 8, 2023: +25 bps → 4.75% (pause signaled)
- June 2023: +25 bps → 5.00%
- Rate held at 5.00% through June 2024, then began cutting

**Market price impact**: Vancouver benchmark home price peaked at approximately $1,252,800 in April 2022. By July 2022 median prices had fallen 14–25% from the February 2022 peak. This decline is almost entirely attributable to rate hikes, not policy interventions. Any DiD study that spans 2020–2023 must control aggressively for interest rate effects.

---

### 10. COVID-19 Housing Market Effects (2020–2021)

**BC eviction moratorium**: BC government issued Ministerial Orders in March 2020 restricting most evictions. The moratorium formally lifted August 18, 2020, though enhanced tenant protections continued under Bill 37 (Rental Amendment Act 2020).

**Foreign buyer activity**: Chinese buying of Vancouver real estate dropped sharply in early 2020 as borders closed. This created a temporary negative shock to foreign demand independent of the 2016 tax.

**Price behavior**: Despite foreign buyer reduction and initial demand shock in spring 2020, ultra-low interest rates drove prices to record highs by 2021. This counterintuitive pattern (lower foreign demand, higher prices) reflects the dominance of domestic financing conditions over foreign buyer flows.

**Notes for research design**: The 2020–2021 COVID period is a confounding minefield. The foreign buyer demand shock coincides with a domestic demand surge driven by rate cuts. Any study of the 2016–2022 period should either end the analysis window before March 2020 or explicitly model the COVID break as a structural shift.

---

## Part 2: Academic Literature Review

---

### 2.1 Primary Studies on the BC Foreign Buyer Tax (2016)

---

#### Du, Zaichao, Hua Yin, and Lin Zhang (2022)
**"Foreign buyer taxes and house prices in Canada: A tale of two cities"**
*Journal of Housing Economics*, Volume 55
DOI: https://doi.org/10.1016/j.jhe.2021.101791

**Methods**: Two complementary approaches:
1. Panel program evaluation variant (city-level aggregate data, synthetic control logic) — constructs a counterfactual Vancouver using a weighted combination of control cities
2. Regression discontinuity design at the transaction level — exploits the August 2, 2016 hard cutoff to compare properties purchased just before vs. just after the tax introduction

**Data**: House-level transaction data from MLS (Metro Vancouver). City-level panel for the SCM arm.

**Control group**: Other Canadian cities (Calgary, Edmonton, Toronto pre-tax) for the SCM arm. Transactions in a narrow window around August 2 for the RD arm.

**Key findings**:
- FBT reduced Vancouver house prices by approximately 5% over the period August 2016–December 2017
- Effects concentrated in the single-detached home segment (condos and townhomes showed smaller effects)
- Toronto FBT (April 2017) reduced prices by 7–9%
- Price effect is temporary in some specifications — prices partially recovered by 2018

**Methodological notes**: The SCM approach requires the treated unit (Vancouver) to be constructable as a convex combination of control units in the pre-treatment period. Du et al. explicitly allow for non-convex weights, nesting classical DiD as a special case. This is a major strength.

---

#### Pavlov, Andrey, and Tsur Somerville (2024)
**"Foreign buyer taxes and housing affordability"**
*Real Estate Economics*, Volume 52(3), pp. 928–950
DOI: https://doi.org/10.1111/1540-6229.12468
Also available: UBC Open Collections https://open.library.ubc.ca/media/stream/pdf/52383/1.0423854/5

**Methods**: Difference-in-differences at the census tract level within Metro Vancouver. Treatment defined by above-vs.-below median pre-tax concentration of foreign buyers (identified from actual transaction-level records where foreign buyer status was recorded prior to the tax). Comparison is high-concentration neighborhoods vs. low-concentration neighborhoods before and after August 2016.

**Data**: Transaction-level property data from BC, with direct identification of foreign buyer involvement from pre-policy records (before Aug 2016, disclosure was voluntary/partial; post-policy, the tax created administrative records). Also uses Census data for neighborhood characteristics.

**Control group (within-city)**: Census tracts with below-median foreign buyer concentration in the pre-period. The paper treats these as a within-metro control — plausible because they share the same macro environment (interest rates, city-level demand shocks) but differ in exposure to the tax shock.

**Key findings**:
- House prices fell by 6% more in high-foreign-buyer-concentration neighborhoods relative to low-concentration neighborhoods after the FBT
- Effect is statistically significant and robust to controls
- No evidence that the FBT meaningfully boosted local purchases to offset the decline — total transaction volume fell in high-concentration areas
- Conclusion: affordability improvements were small because price decline was not offset by volume of local purchases

**Key data innovation**: The paper uses pre-policy voluntary disclosure records to identify foreign buyer shares by neighborhood — this is the primary treatment proxy.

---

#### Hartley, Jonathan, Li Ma, Susan M. Wachter, and Albert A. Zevelev (2024)
**"Do Foreign Buyer Taxes Affect House Prices?"**
*Journal of Real Estate Research*
SSRN working paper: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3939611
AEA 2023 conference version: https://www.aeaweb.org/conference/2023/program/paper/kBBk4zQd

**Methods**: Machine learning prediction + synthetic control method. Studies foreign buyer tax regimes in Canada, Australia, and New Zealand simultaneously. Uses ML for variable selection in constructing the synthetic control counterfactual.

**Scope**: Cross-country comparative — not limited to Vancouver. Uses British Columbia, Ontario, Australian states, and New Zealand as treated units with non-taxing jurisdictions as controls.

**Key findings**:
- FBTs had negative, large, and persistent effects on house price growth across all three countries
- Larger effects in locations with higher tax rates and higher shares of immigrant buyers
- Effects are persistent (do not fully reverse within a 3-year window)
- This is broader/more optimistic than Du et al. regarding persistence

---

#### Andersen, Asger Lau, et al. — Oxford Journal of Economic Geography (2024)
**"Heterogeneous effects of a foreign buyer tax on house prices"**
*Journal of Economic Geography*, Volume 24(4), pp. 495–
DOI: https://doi.org/10.1093/joeg/lbad022

**Methods**: Within-Vancouver DiD exploiting heterogeneity in foreign buyer exposure across neighborhoods. Likely uses variation in the share of transactions involving foreign buyers as a continuous treatment intensity measure rather than a binary high/low split.

**Key findings**: Documents heterogeneous price effects — some neighborhoods experience much larger declines than others, consistent with the Pavlov/Somerville finding but with finer-grained spatial resolution. Neighborhoods with higher pre-tax foreign buyer shares see larger post-tax price declines.

---

### 2.2 Studies on the Empty Homes Tax

---

#### Caracciolo, Gherardo Gennaro, and Enrico Miglino (2024)
**"Ripple Effects: The Impact of an Empty-Homes Tax on the Housing Market"**
*C.D. Howe Institute*
SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4919236

**Methods**: Difference-in-differences exploiting the Vancouver City boundary. City of Vancouver properties are the treatment group; comparable properties just outside the city boundary (Burnaby, North Vancouver) are the control group. Pre-period is before the January 2017 implementation; post-period is after.

**Key findings**:
- Vacancy rate in treated areas dropped by 1.5 percentage points (a 21% reduction in vacant homes) — from ~7% to ~5.5%
- No statistically significant effect on average rent levels
- No effect on new housing construction
- The tax was effective at reducing vacancies but did not translate into affordability improvement

**Why no rent effect**: Authors suggest Vancouver and comparable markets may be in a "high-price equilibrium" where landlords can always find tenants at prevailing market rates regardless of marginal supply additions. The 226 net additional occupied homes (from 1,078 vacant) represents a small fraction of total rental stock.

---

#### Han, Lu, Derek Stacey, and Hong Chen (2023)
**"Frictional and Speculative Vacancies: The Effects of an Empty Homes Tax"**
Presented at ABFER Annual Conference, 2023
Available: https://abfer.org/media/abfer-events-2023/annual-conference/papers-realestate/AC23P6023-Frictional-and-Speculative-Vacancies-The-Effects-of-an-Empty-Homes-Tax.pdf

**Methods**: Distinguishes between two types of vacancies: frictional (natural search frictions — units temporarily vacant between tenants) vs. speculative (intentionally held vacant for capital gains). Argues that a flat vacancy tax collapses this distinction and may actually harm efficiency by taxing frictional vacancies.

**Key findings**: A vacancy tax reduces total vacancies but may have unintended distributional effects — it primarily affects owners who are speculating on capital gains, but it also catches some frictional vacancies and can reduce landlord willingness to leave units temporarily vacant during tenant turnover, leading to worse matching quality.

---

#### Anon — ResearchGate (2021)
**"Vancouver Empty Home Tax: An Analysis of Taxation as a Solution to a Housing Crunch"**
ResearchGate: https://www.researchgate.net/publication/349907426

**Notes**: A policy analysis paper (likely a working paper or graduate thesis) evaluating the EHT mechanism. Primarily descriptive — not causal inference. Useful for understanding the design and stated mechanisms.

---

### 2.3 Foundational Literature on Foreign Buyers and Housing Prices

---

#### Favilukis, Jack, and Stijn Van Nieuwerburgh (2021)
**"Out-of-Town Home Buyers and City Welfare"**
*Journal of Finance* (published version)
SSRN: https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3035279

**Methods**: Structural housing market model calibrated to Vancouver data. Uses a general equilibrium framework to quantify the welfare effects of out-of-town (primarily foreign) demand shocks.

**Key findings**: Observed increases in out-of-town purchases associated with 5% higher house prices in Vancouver and a 0.34% welfare loss for local residents. First paper to rigorously model the welfare implications of foreign demand on a specific Canadian city.

---

#### Pavlov, Andrey, and Tsur Somerville (2020)
**"Immigration, Capital Flows, and Housing Prices"**
*Real Estate Economics*, Volume 48(3)
DOI: https://doi.org/10.1111/1540-6229.12267
UBC Open Collections: https://open.library.ubc.ca/soa/cIRcle/collections/facultyresearchandpublications/52383/items/1.0357371

**Methods**: Exploits the unexpected suspension of Canada's Immigrant Investor Program (IIP) as a natural experiment. Compares neighborhoods in Greater Vancouver that were popular with investor immigrants (treatment) to those that were not (control), before and after the IIP suspension.

**Key findings**: IIP suspension caused a 3% decline in property prices in neighborhoods most exposed to investor immigrant demand. Demonstrates that capital flows (not just the physical relocation of people) are what drives the housing price premium.

**Relevance**: This is a predecessor paper to the FBT work by the same team and establishes the neighborhood-level variation in foreign buyer exposure as a valid treatment axis.

---

#### Ley, David (2021)
**"A regional growth ecology, a great wall of capital and a metropolitan housing market"**
*Urban Studies*, Volume 58(2)
DOI: https://doi.org/10.1177/0042098019895226

**Methods**: Qualitative case study and comparative urban analysis. Not causal inference. Reviews Vancouver's housing market in the context of global capital flows, Pacific Rim migration, and the regional political economy.

**Key findings**: Argues that Vancouver's housing crisis is fundamentally a product of its role as a gateway city for Pacific Rim capital and migration — a structural condition that short-term tax interventions cannot fully address. Provides historical context and frame for interpreting why the FBT price effects, while statistically significant, are modest relative to the underlying price level.

---

### 2.4 Broader Housing Policy Evaluation Methodology

---

#### Impact of Housing Policies on Real Estate Markets — Systematic Literature Review (2023)
*ScienceDirect / Heliyon*
https://www.sciencedirect.com/science/article/pii/S2405844023079124

A systematic review of empirical methods used to evaluate housing policy interventions globally. Documents the rise of DiD, synthetic control, and regression discontinuity as the dominant quasi-experimental methods in this literature after 2010.

---

### 2.5 Key Gaps in the Literature

Based on the above review, the following gaps are identifiable:

1. **Multi-policy simultaneity**: Most studies evaluate one policy at a time. No paper adequately models the compound effect of the FBT (2016) + EHT (2017) + SVT (2018) operating simultaneously in Metro Vancouver. These three policies are structurally collinear and researchers who study only the FBT cannot separate its effect from the EHT/SVT that followed 6–24 months later.

2. **Assessment value vs. transaction price**: Most studies use MLS transaction prices, which only capture properties that traded. BC Assessment values are annual, property-level, and cover the full stock (not just sales). Using assessment data avoids selection bias from studying only traded properties — but no published paper appears to have done a full DiD using assessed values as the primary outcome.

3. **Long-run persistence**: Du et al. (2022) find partial price recovery by 2018. Hartley et al. (2024) find persistent effects. There is no consensus on whether FBT price effects are permanent or temporary — and no paper carries the analysis past 2020.

4. **Property type heterogeneity**: Pavlov/Somerville and Du/Yin/Zhang both note that effects concentrate in single-detached homes. The condo market response is understudied, despite condos being the primary vehicle for foreign buyer investment in high-density inner-city neighborhoods.

5. **Zoning interaction**: None of the FBT literature examines whether the Broadway Plan upzoning (2022) or Bill 44 multiplex allowances (2023) dampened or amplified prior policy effects. A property initially subject to the FBT shock in 2016 may also receive upzoning rights in 2022 — the interaction has not been studied.

6. **STR-to-residential conversion effect**: The May 2024 STR restrictions are too recent for academic study. There is a measurable effect on assessed values of condo units formerly operating as Airbnb in high-tourist-density neighborhoods that remains unstudied.

---

## Part 3: Treatment and Control Group Design

---

### 3.1 DiD Design for the Foreign Buyer Tax (August 2016)

**Treatment definition options**:

**Option A — Geographic binary (coarse)**
Treatment = Metro Vancouver. Control = Calgary + Edmonton (or a synthetic combination of unaffected Canadian cities).
Strength: Clean geographic cutoff, easy to implement with city-level aggregate data.
Weakness: Calgary/Edmonton have very different economic structures (oil-dependent). Parallel trends assumption is fragile across the 2014–2016 oil price crash.

**Option B — Neighborhood foreign buyer concentration (within-city DiD, preferred)**
Treatment = census tracts in Metro Vancouver with above-median pre-tax foreign buyer share.
Control = census tracts with below-median pre-tax foreign buyer share.
Strength: Both groups share the same macro environment (interest rates, city economy, immigration policy). Parallel trends assumption is much more plausible. This is the approach used by Pavlov/Somerville (2024) and by the JEG (2024) heterogeneous effects paper.
Weakness: Spillover effects — if the FBT reduces prices in high-concentration tracts, it may attract local buyers who then bid up prices in adjacent low-concentration tracts, contaminating the control group (general equilibrium spillover).

**Option C — Property type within neighborhood**
Treatment = single-detached homes (more foreign buyer exposure). Control = condos or strata units in the same neighborhood (less foreign buyer exposure).
Strength: Controls for neighborhood-level shocks. Takes advantage of known property-type heterogeneity in the literature.
Weakness: Single-detached vs. condos are fundamentally different assets (different income profiles, different user types). Parallel trends requires heroic assumptions.

**Recommended**: Option B (neighborhood concentration) with a robustness check using Option A. Follow Pavlov/Somerville's tract-level design but extend the analysis window to 2020 (pre-COVID) and use assessed values rather than transaction prices.

---

### 3.2 DiD Design for the Empty Homes Tax (2017)

**Treatment definition options**:

**Option A — City boundary (City of Vancouver vs. adjacent municipalities)**
Treatment = properties within City of Vancouver boundaries.
Control = comparable residential properties in Burnaby, Richmond, New Westminster, North Vancouver City, North Vancouver District — municipalities adjacent to Vancouver that did NOT have a municipal vacancy tax.
Strength: This is the most natural control group — same Metro Vancouver market, same macro environment.
Weakness: After 2018, the BC SVT applies to both treatment and control areas (both are in Metro Vancouver). This contaminates the control group with a second policy shock that hits both groups.
Mitigation: End the study window at December 2017 (one year of the EHT only) or include SVT introduction as an explicit second treatment.

**Option B — Property use type within Vancouver**
Treatment = residential properties likely to be vacant (non-strata single-detached with no occupancy permit, or properties with high assessed land/improvement ratio suggesting older structures held for redevelopment).
Control = owner-occupied strata units (low vacancy probability).
Weakness: This is not a credible parallel trends design because the two groups differ on fundamentals.

**Recommended**: Option A (City boundary), study window 2015–2018. Include the SVT as a robustness check by re-running the analysis for 2015–2020 with a second treatment indicator for the SVT.

---

### 3.3 Data Sources for Treatment Intensity

**1. Pre-policy foreign buyer transaction records (the key dataset)**
- BC Ministry of Finance collected foreign buyer data at time of Property Transfer Tax registration starting August 2, 2016 (mandatory from that date). These records are the gold standard but are not publicly available.
- Pavlov/Somerville (2024) used pre-policy voluntary disclosure records — these would have been provided under a data access agreement with the province.
- For a portfolio project without data agreements: The City of Vancouver's Open Data Portal publishes annual property tax reports going back to 2006, with parcel-level assessed values. Foreign buyer identity is NOT in the open dataset.

**2. Proxy for foreign buyer concentration (what you can use without a data agreement)**

a. **Ethnic enclave proxies**: Statistics Canada 2016 Census data by census tract. Tracts with higher shares of recent immigrants from mainland China, Hong Kong, or Taiwan historically correlated with higher foreign buyer shares. Pavlov/Somerville (2020) used this approach in their IIP paper. Problematic because it conflates ethnicity with foreign status.

b. **Satellite imagery + permit data**: Properties with assessed land value >> improvement value may indicate land banking (foreign buyer behavior). Not validated in the literature but worth exploring.

c. **REBGV/BCREA aggregate statistics**: The Real Estate Board of Greater Vancouver publishes some neighborhood-level statistics, but foreign buyer share is not included at fine geographic resolution.

d. **Land Owner Transparency Registry (LOTR)**: Launched November 30, 2020; searchable publicly from April 30, 2021. Collects beneficial ownership including country of residence for all post-2020 transfers. Too late to use for 2016 treatment assignment, but useful for post-2020 analysis of residual foreign ownership patterns.

e. **BC Assessment open data via UBC Abacus**: BC Assessment Data Advice files (2016–2022) are available to university researchers via Abacus (restricted to SFU, UBC, UNBC, UVic). Contains property-level assessed values annually. This is the cleanest source for the outcome variable. URL: https://abacus.library.ubc.ca/dataset.xhtml?persistentId=hdl:11272.1/AB2/LAPUAB

f. **City of Vancouver Open Data — Property Tax Report**: Annual property-level data including assessed land value, assessed improvement value, tax levy, zoning, and legal description. Available from 2006 onward. Public, no restrictions. URL: https://opendata.vancouver.ca/explore/dataset/property-tax-report/ This is the most accessible data source for this project.

**3. Control variables**

- Property size (land area, gross floor area) — from City of Vancouver permit data and BC Assessment
- Distance to transit/SkyTrain stations — from Metro Vancouver GIS
- School district quality — BC Ministry of Education school catchment rankings
- Neighborhood income — Statistics Canada Census by CT, available 2006, 2011, 2016, 2021
- Heritage designation (limits redevelopment) — City of Vancouver heritage register

---

### 3.4 Recommended Analytical Framework for This Portfolio Project

**Primary analysis: FBT 2016 shock, neighborhood-level DiD**

- Unit of analysis: Census tract (or neighborhood area as defined by City of Vancouver)
- Outcome: Annual change in average assessed land value per square foot (City of Vancouver open data)
- Treatment: Continuous — pre-FBT proxy for foreign buyer intensity (e.g., 2016 Census share of recent non-permanent-resident population by CT; or simply use the same above/below median split that Pavlov/Somerville use)
- Time window: 2013–2019 (3 years pre-treatment, 3 years post-treatment, stops before COVID)
- Controls: Interest rate environment (national macro variable, same for all tracts), neighborhood income, distance to transit
- Regression: Two-way fixed effects (tract FE + year FE) with an interaction term for `Post_2016 × Foreign_Buyer_Intensity`

**Parallel trends test**: The key assumption is that high-concentration and low-concentration tracts would have trended similarly in the absence of the FBT. Test this by plotting pre-2016 trends separately for high and low tracts. If the trends are not parallel in 2013–2015, the DiD is not credible.

**Secondary analysis: EHT 2017 shock, city boundary DiD**

- Unit of analysis: Property-level from open data
- Outcome: Year-over-year change in assessed value
- Treatment: Indicator for City of Vancouver (vs. Burnaby, North Vancouver, Richmond)
- Time window: 2015–2018 (stops before SVT complicates the control group)
- Controls: Property type, land area, zoning

**Potential contribution over existing literature**:
- Using *assessed values* (full population) rather than *transaction prices* (selected sample) removes selection bias from studying only traded properties
- Extending any existing analysis to include the 2022 upzoning as a third treatment shock, creating a multi-treatment DiD across three distinct interventions
- Explicitly modeling the COVID period as a structural break rather than ignoring it or truncating the sample

---

## Sources

### Policy Sources
- [Bill 28 (British Columbia) — Wikipedia](https://en.wikipedia.org/wiki/Bill_28_(British_Columbia))
- [BC Additional Property Transfer Tax — Gov.bc.ca](https://www2.gov.bc.ca/gov/content/taxes/property-taxes/property-transfer-tax/additional-property-transfer-tax)
- [BC Speculation and Vacancy Tax — Gov.bc.ca](https://www2.gov.bc.ca/gov/content/taxes/speculation-vacancy-tax)
- [BC SVT Tax Rates — Gov.bc.ca](https://www2.gov.bc.ca/gov/content/taxes/speculation-vacancy-tax/how-tax-works/tax-rates)
- [Vancouver Empty Homes Tax — City of Vancouver](https://vancouver.ca/home-property-development/empty-homes-tax.aspx)
- [Empty Homes Tax FAQ — City of Vancouver](https://vancouver.ca/home-property-development/empty-homes-tax-frequently-asked-questions.aspx)
- [Empty Homes Tax Annual Report 2023 — City of Vancouver (PDF)](https://vancouver.ca/files/cov/empty-homes-tax-annual-report-2023.pdf)
- [2025 Empty Homes Tax Annual Report (PDF)](https://vancouver.ca/files/cov/2025-empty-homes-tax-annual-report.pdf)
- [Underused Housing Tax — Canada.ca](https://www.canada.ca/en/services/taxes/excise-taxes-duties-and-levies/underused-housing-tax.html)
- [UHT Eliminated — Budget 2025, McMillan LLP](https://mcmillan.ca/insights/publications/budget-2025-inefficient-underused-housing-tax-eliminated/)
- [Prohibition on Purchase of Residential Property by Non-Canadians — Federal Extension](https://www.canada.ca/en/department-finance/news/2024/02/government-announces-two-year-extension-to-ban-on-foreign-ownership-of-canadian-housing.html)
- [Short-Term Rental Restrictions — BC Gov News, May 2024](https://news.gov.bc.ca/releases/2024HOUS0020-000590)
- [BC Bill 44 — Housing Statutes (Residential Development) Amendment Act, 2023](https://www.bclaws.gov.bc.ca/civix/document/id/bills/billsprevious/4th42nd:gov44-3)
- [Vancouver Broadway Plan](https://vancouver.ca/home-property-development/broadway-plan.aspx)
- [Vancouver Multiplex / R1-1 Zone — CityHallWatch](https://cityhallwatch.wordpress.com/2023/09/05/issues-public-hearing-rs-rezoning-multiplexes-missing-middle/)
- [Bank of Canada Policy Rate History](https://www.bankofcanada.ca/core-functions/monetary-policy/key-interest-rate/)
- [Land Owner Transparency Registry](https://landtransparency.ca/)

### Academic Sources
- [Du, Yin, Zhang (2022) — Foreign buyer taxes and house prices: A tale of two cities. *Journal of Housing Economics*, Vol. 55](https://www.sciencedirect.com/science/article/abs/pii/S1051137721000620)
- [Pavlov & Somerville (2024) — Foreign buyer taxes and housing affordability. *Real Estate Economics*, 52(3)](https://onlinelibrary.wiley.com/doi/10.1111/1540-6229.12468)
- [Pavlov & Somerville (2024) — UBC Open Collections full text](https://open.library.ubc.ca/media/stream/pdf/52383/1.0423854/5)
- [Hartley, Ma, Wachter, Zevelev — Do Foreign Buyer Taxes Affect House Prices? SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3939611)
- [Hartley et al. — Journal of Real Estate Research (2024)](https://www.tandfonline.com/doi/full/10.1080/08965803.2024.2376955)
- [Andersen et al. (2024) — Heterogeneous effects of a foreign buyer tax. *Journal of Economic Geography*, 24(4)](https://academic.oup.com/joeg/article-abstract/24/4/495/7639370)
- [Caracciolo & Miglino (2024) — Ripple Effects: The Impact of an Empty-Homes Tax. C.D. Howe Institute / SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=4919236)
- [Han, Stacey, Chen (2023) — Frictional and Speculative Vacancies: Effects of an Empty Homes Tax](https://abfer.org/media/abfer-events-2023/annual-conference/papers-realestate/AC23P6023-Frictional-and-Speculative-Vacancies-The-Effects-of-an-Empty-Homes-Tax.pdf)
- [Favilukis & Van Nieuwerburgh — Out-of-Town Home Buyers and City Welfare. SSRN](https://papers.ssrn.com/sol3/papers.cfm?abstract_id=3035279)
- [Pavlov & Somerville (2020) — Immigration, Capital Flows, and Housing Prices. *Real Estate Economics*, 48(3)](https://onlinelibrary.wiley.com/doi/abs/10.1111/1540-6229.12267)
- [Ley (2021) — A regional growth ecology, a great wall of capital and a metropolitan housing market. *Urban Studies*](https://journals.sagepub.com/doi/abs/10.1177/0042098019895226)
- [NBER Working Paper w27370 — Global Capital and Local Assets](https://www.nber.org/papers/w27370)
- [Sauder UBC News — Foreign Buyers Tax led to home prices declining 6% in some Vancouver neighbourhoods](https://www.sauder.ubc.ca/news/insights/foreign-buyers-tax-led-home-prices-declining-six-cent-more-some-vancouver)

### Data Sources
- [City of Vancouver Open Data — Property Tax Report](https://opendata.vancouver.ca/explore/dataset/property-tax-report/)
- [BC Assessment Data Advice 2016–2022 (Restricted) — UBC Abacus](https://abacus.library.ubc.ca/dataset.xhtml?persistentId=hdl:11272.1/AB2/LAPUAB)
- [BC Assessment — Independent property assessment](https://www.bcassessment.ca/)
