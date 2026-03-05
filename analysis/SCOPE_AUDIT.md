# Vancouver Business Licence Dataset — Scope Audit for Commercial Survival Analysis

**Dataset:** `business-licences-2013-to-2024.csv`
**Raw row count:** 779,226
**Analysis date:** 2026-03-03
**Purpose:** Identify all rows that do not belong in a commercial business survival analysis and quantify their impact.

---

## Table of Contents
1. [Variable Audit Results](#1-variable-audit-results)
   - 1.1 businesstype
   - 1.2 status
   - 1.3 businesssubtype
   - 1.4 city
   - 1.5 country / province
   - 1.6 numberofemployees
   - 1.7 feepaid
   - 1.8 licencerevisionnumber
   - 1.9 businessname
   - 1.10 localarea / geospatial
2. [Exclusion Recommendations](#2-exclusion-recommendations)
3. [Impact Assessment](#3-impact-assessment)
4. [Cumulative Impact](#4-cumulative-impact)
5. [Edge Cases](#5-edge-cases)
6. [Recommended Scope Definition](#6-recommended-scope-definition)

---

## 1. Variable Audit Results

### 1.1 `businesstype`

The dataset contains 173 unique businesstype values. They fall into six broad categories:

#### A. Pure Residential — DEFINITE EXCLUSION

These are dwelling licences, not business licences. The City of Vancouver requires permits for rental properties; these records ended up in the business licence database as an administrative artefact. They have no relevance to commercial survival.

| businesstype | Count | % of total |
|---|---|---|
| Single Detached House *Historic* | 36,642 | 4.7% |
| Apartment House Strata *Historic* | 30,082 | 3.9% |
| Apartment House *Historic* | 29,787 | 3.8% |
| Secondary Suite - Permanent *Historic* | 27,298 | 3.5% |
| Multiple Dwelling *Historic* | 12,676 | 1.6% |
| Duplex *Historic* | 10,273 | 1.3% |
| Pre-1956 Dwelling *Historic* | 2,835 | 0.4% |
| Live-aboards *Historic* | 1,137 | 0.1% |
| Rooming House *Historic* | 269 | 0.0% |
| Apartment House-99 Year Lease *Historic* | 118 | 0.0% |
| **SUBTOTAL** | **151,117** | **19.4%** |

**Reasoning:** These are residential property classifications. None of these entities "fail" as a commercial enterprise. A Single Detached House licence expiring does not represent a business death — it represents a landlord choosing not to renew a rental permit, or a property being owner-occupied again. Including these in a survival curve would make the analysis measure something undefined.

#### B. Short-Term Rental Operator — STRONG EXCLUSION RECOMMENDATION

| businesstype | Count | % of total |
|---|---|---|
| Short-term Rental Operator | 32,452 | 4.2% |

**Reasoning:** This is a residential property regulatory licence, not a commercial business licence. STR operators are homeowners or tenants renting out their primary residence (Airbnb-style). The licence was introduced around 2018 by the City of Vancouver specifically to regulate short-term residential rentals. Key evidence:
- No businesssubtype values at all (100% blank) — no commercial categorisation was even attempted
- Status breakdown: 21,191 Issued, 4,716 Gone Out of Business, 4,213 Cancelled, 2,134 Pending
- The high Cancelled count (13.0% of all STR records) reflects policy enforcement (the City actively cancels non-compliant STR licences), not business failure
- High-fee examples don't appear for this type — fees are flat and low
- "Gone Out of Business" for an STR operator means the homeowner stopped renting their spare bedroom, not that a commercial enterprise failed

**Verdict:** EXCLUDE. A survival analysis of STR licences would measure housing policy enforcement, not commercial gentrification dynamics.

#### C. Administrative and Regulatory Entries — DEFINITE EXCLUSION

These businesstypes are not businesses at all — they are administrative processes within the City's licensing system.

| businesstype | Count | % of total |
|---|---|---|
| Temp Liquor Licence Amendment | 1,516 | 0.2% |
| Liquor License Application | 213 | 0.0% |
| Soliciting For Charity | 133 | 0.0% |
| **SUBTOTAL** | **1,862** | **0.2%** |

**Temp Liquor Licence Amendment:** A modification to an existing liquor licence for a specific event or period. It is not a business entity — it is a paperwork row attached to a business that already has its own licence record. Status breakdown: 1,434 Issued, 36 Inactive, 27 Pending, 19 Cancelled. These are process records, not business records.

**Liquor License Application:** Pre-approval stage of a liquor licence. 44 are still Pending. These are not operating businesses. A Pending application that never gets approved would look like a "death" — but the business in question may still be operating under a different licence type.

**Soliciting For Charity:** A charitable fundraising permit, not a business licence. Charities solicit donations; they do not operate the same way a for-profit enterprise does and do not "fail" commercially.

#### D. Temporary and Event-Based — EXCLUDE

| businesstype | Count | % of total |
|---|---|---|
| Temporary Filming Company | 1,464 | 0.2% |
| Christmas Tree Lot *Historic* | 29 | 0.0% |
| **SUBTOTAL** | **1,493** | **0.2%** |

**Reasoning:** Temporary Filming Companies get a licence for a specific production. The licence expires when filming ends — this is the designed outcome, not business failure. Survival analysis of these would simply measure production schedules. Christmas Tree Lot licences are seasonal by definition; they are supposed to expire after the season. Neither type constitutes a persistent commercial enterprise.

Note: **Exhibitions/Shows/Concerts *Historic*** (1,798 records) is a borderline case — see Edge Cases section. It has been left in the core dataset here because exhibition venues and recurring concert promoters are persistent commercial entities even if individual events are temporary.

#### E. Commercially Operated Businesses — INCLUDE

The following types are clearly legitimate commercial businesses and must be retained:

- Restaurant Class 1 / Class 2 *Historic*: Food service establishments (24,213 + 294 rows)
- Ltd Service Food Establishment *Historic*: Cafes, fast food (19,406)
- Retail Dealer *Historic* and variants: Shops, stores (41,383 + sub-types ~18,000)
- Contractor / Electrical Contractor / Plumber *Historic* etc: Trades businesses (45,224 + ~70,000 sub-types)
- Office *Historic*: Professional services — lawyers, consultants, architects (120,826) — SEE NOTE BELOW
- Health Services *Historic*: Medical, dental, therapy practices (38,318)
- Computer Services *Historic*: Software, IT firms (16,313)
- Financial Services *Historic*: Advisors, accountants (15,601)
- Hotel or Motel: Lodging businesses (1,402)
- Liquor Establishment Extended/Standard *Historic*: Bars, clubs (1,593 + 1,425)
- Fitness Centre: Gyms (2,447)
- Manufacturer *Historic* and variants: Production businesses (5,885 + sub-types)
- Wholesale Dealer *Historic* and variants: Distribution businesses
- All other trade, service, retail classifications not covered by exclusion categories

**Note on Office *Historic* (120,826 rows, 15.5% of data):**

This is the largest single businesstype. Concern was raised that it might include home offices that should be excluded. Analysis shows:

- The top subtypes are: Consultant (26,513), Barrister & Solicitor (25,275), Administration (11,202), Architect (4,536), Mining Exploration (3,718)
- These are legitimate commercial professional services, not residential licences
- Home-based professionals (lawyers, consultants, architects) working from home ARE commercial businesses — they generate revenue, employ people, and can fail commercially
- The City of Vancouver classifies these as business licences, not dwelling licences
- A home-based lawyer's practice CAN fail: they lose clients, retire, leave the city
- **INCLUDE in analysis** — but flag that this category conflates solo practitioners with multi-person offices, which affects the employee count interpretation

The `*Historic*` suffix appearing on most businesstypes is a City data label indicating the classification comes from the legacy licensing system, not a residential designation.

#### F. Non-Profit Housing — EDGE CASE (see Section 5)

| businesstype | Count |
|---|---|
| Non-profit Housing *Historic* | 3,186 |

---

### 1.2 `status`

Five status values exist:

| Status | Count | % of total | Treatment |
|---|---|---|---|
| Issued | 566,994 | 72.8% | INCLUDE — active licence |
| Inactive | 70,255 | 9.0% | INCLUDE with nuance (see below) |
| Gone Out of Business | 62,191 | 8.0% | INCLUDE — primary death event |
| Pending | 58,171 | 7.5% | EXCLUDE — not yet operating |
| Cancelled | 21,615 | 2.8% | EXCLUDE — never operated commercially |

**Issued:** Active licence. The business is operating. Core inclusion.

**Gone Out of Business:** The primary death signal for survival analysis. Business confirmed closed. 79.7% of these rows have no fee data (feepaid is blank), which is consistent with how the City records closures — the fee was paid for the year the licence was active, but there's no fee for the year they reported closing.

**Inactive:** Requires year-specific interpretation:
- **Years 13–23:** 1,400–2,800 Inactive per year (2.2%–4.0% of year total). These are businesses that became inactive mid-year — meaningful data. Could represent seasonal businesses, businesses between owners, or early-stage closures not yet formally reported as Gone Out of Business. **INCLUDE** in analysis but treat as censored/ambiguous status.
- **Year 24:** 50,083 Inactive out of 62,495 total (80.1% of year 24). This is a snapshot timing artefact. The extract was taken October 2024; annual licences expire December 31. Businesses that had valid 2024 licences which expired before October but hadn't renewed yet show as Inactive — they are still operating, just mid-renewal-cycle. These are NOT deaths. **TREAT YEAR 24 AS RIGHT-CENSORED** — businesses observed as Inactive in year 24 should be coded as alive/censored as of the observation date, not as failures.

**Pending:** Licence applied for but not yet approved. The business may not have opened yet. Including Pending records would inject fictitious "near-zero duration" businesses (applied → never approved → looks like instant death). **EXCLUDE.**

Status x Year 24 further detail:
- Year 24 Issued: 4,069 (6.5%) — these are the small fraction that renewed early
- Year 24 Gone Out of Business: 6,151 (9.8%) — legitimate deaths still occurring
- Year 24 Pending: 513 (0.8%) — new applications late 2024
- Year 24 Cancelled: 1,679 (2.7%)

**Cancelled:** Means the licence was cancelled before or shortly after opening. Key evidence:
- Short-term Rental Operators account for 4,213 of 21,615 cancellations (19.5%) — driven by City policy enforcement, not commercial failure
- Median fee for Cancelled: $60 (vs $155 for Issued), suggesting many were cancelled very early
- Cancelled ≠ business failure. Cancellation can mean: the applicant withdrew the application, the City denied the licence, the business changed owners before even opening, regulatory non-compliance. None of these are the same as "a business started and then failed due to market forces." **EXCLUDE.**

---

### 1.3 `businesssubtype`

357 unique subtype values. 46.7% of rows have no subtype (blank). The subtype field adds granularity within businesstype but does not reveal additional residential/commercial misclassification issues beyond what businesstype already surfaces.

Key observations:
- Community Association *Historic* is 100% blank subtype (8,618 rows) — no commercial classification was ever assigned to this type
- Non-profit Housing *Historic* is 100% blank subtype (3,186 rows) — same
- Educational *Historic* subtypes are: Tutor (1,432), Interpreter/Translator (488), Other (274), Student Placement (177), etc. — all legitimate commercial services
- STR Operator is 100% blank subtype — confirms it's a regulatory class, not a commercial category

The subtype does not provide grounds for additional exclusions beyond businesstype-level exclusions already identified.

---

### 1.4 `city`

**This field records the mailing/business address of the licence holder, NOT the site where the business operates.**

| Value | Count | % |
|---|---|---|
| VANCOUVER | 694,778 | 89.2% |
| Blank | 1,046 | 0.1% |
| Non-Vancouver (527 unique values) | 83,402 | 10.7% |

The 10.7% non-Vancouver entries are NOT out-of-scope businesses. A contractor licensed by the City of Vancouver to operate in Vancouver may be headquartered in Burnaby. A retail chain may use its head office address (Toronto) on the licence application while the storefront is on Robson Street.

Evidence: The top businesstypes for non-Vancouver city entries are Contractor *Historic* (19,762), Electrical Contractor (11,398), Contractor - Special Trades (10,471), and Office *Historic* (8,098). These are tradespeople and professionals who live in suburbs and commute to work in Vancouver. The City of Vancouver is the licensing authority — by definition, a Vancouver licence is for a business that operates in Vancouver.

**Decision: Do NOT exclude based on city field.** The city field is mailing address, not operational location. Excluding non-Vancouver city entries would disproportionately remove contractors and trades businesses, biasing the study population toward retail.

However: City values like 'TEHRAN', 'DUBAI', 'RIO DE JANEIRO', 'DENMARK', 'NEW SOUTH WALES' (total ~20 records) likely represent data entry errors in address fields. Too small to affect analysis (<0.01%) but worth flagging as data quality noise.

---

### 1.5 `country` / `province`

| Country | Count | % |
|---|---|---|
| CA | 742,448 | 95.3% |
| Blank | 36,778 | 4.7% |

The 4.7% blank country is a data quality gap, not a misclassification issue. Blank country does not mean the business is foreign — it almost certainly means the field wasn't required when the record was created.

Province distribution:
- BC: 774,169 (99.4%)
- ON: 1,374 (0.2%) — Toronto-based companies with Vancouver locations
- Blank: 1,117 (0.1%)
- AB: 888 (0.1%) — Alberta companies
- US states (WA, NY, FL, etc.): ~700 total
- Other international: <20 total

**Decision: No exclusions based on country/province.** The out-of-province entries are legitimate businesses (e.g., national chains, franchisor head offices) with Vancouver operating locations. Excluding them would remove large retailers and hospitality chains.

---

### 1.6 `numberofemployees`

| Range | Count | Notes |
|---|---|---|
| Missing/blank | 271,301 (34.8%) | Not reported |
| 0 employees | 48,368 (6.2%) | Solo operators, reporting errors |
| 1–5 | 317,761 (40.8%) | Small businesses |
| 6–20 | 100,345 (12.9%) | Medium-small |
| 21–100 | 33,329 (4.3%) | Medium |
| 101–1,000 | 7,924 (1.0%) | Large |
| >1,000 | 198 (0.0%) | Major employers |

Summary statistics: Median = 2 employees, Mean = 11.2. The 34.8% missing rate makes this field unreliable for filtering. Max value is 5,876 (City Vaper Inc — likely a data entry error; a vape shop doesn't employ 5,876 people). Devret Bosch appears 5 times with 5,437 employees — a repeated data quality issue for that specific entity.

**Key findings:**
- 0-employee businesses (48,368 rows) are legitimate for inclusion. Many are sole proprietors (e.g., "Homecraft" cottage businesses, freelance contractors) who correctly report 0 employees because they have no W-2 employees — they ARE the business. Excluding 0-employee businesses would remove a large fraction of the small-business economy that is most relevant to gentrification dynamics.
- Unrealistically high values (>1,000) are data quality issues in specific records, not systematic misclassification. Top examples: City Vaper Inc (5,876), Devret Bosch (5,437 × 5 records), Open Text Corporation (4,500), Pacific National Exhibition (4,000). These 198 outlier records should be flagged but not excluded on type grounds.
- The employee field is not a reliable basis for scope filtering.

---

### 1.7 `feepaid`

| Metric | Value |
|---|---|
| Missing | 124,826 (16.0%) |
| Negative values | 6 total (3 Live-aboards, 1 Gas Contractor, 1 Office, 1 STR) |
| Zero fees | 0 rows |
| > $10,000 | 1,126 rows |
| Median (Issued) | $155 |
| Mean (Issued) | $329 |
| Max | $63,281 |

**Key findings:**

Missing fees by status: 0.5% of Issued rows have missing fees (data entry gaps). 79.7% of Gone Out of Business rows have missing fees — this is structural: businesses that close mid-year don't always have a fee recorded for the closing year, as they may have paid for the year of operation and then simply not renewed. This is expected behaviour and NOT an exclusion criterion.

Negative fees (6 rows) are almost certainly correction/refund entries. Negligible count, not worth excluding.

High fees (>$10K) are concentrated in Hotel or Motel (208 rows), Apartment House *Historic* (603 rows), and Liquor Establishment Extended (27 rows). These are legitimate large commercial entities; a hotel with 500 rooms pays a substantial licensing fee. No exclusions warranted.

Community Association *Historic* shows 6,653 Issued licences with fee < $50 — one of the highest counts in the low-fee bucket. This is consistent with non-profits and community groups receiving concessionary licensing rates, which supports the edge case for considering their exclusion (they are treated differently by the licensing system).

**Decision: No exclusions based on feepaid.** Fee patterns are informative for understanding business size but do not identify misclassified records.

---

### 1.8 `licencerevisionnumber`

| Revision | Count | % |
|---|---|---|
| 0 | 758,261 | 97.3% |
| 1 | 20,184 | 2.6% |
| 2 | 732 | 0.1% |
| 3 | 43 | 0.0% |
| 4 | 5 | 0.0% |
| 10 | 1 | 0.0% |

**What this means:** A revision number > 0 indicates the licence record was amended after initial issuance in that folderyear. Common causes: address change, ownership transfer, licence scope change, or correction. This does NOT represent a renewal — annual renewals create new rows with a new folderyear, not a revised row.

**Implications for survival analysis:**
- Revision 1+ rows are for the SAME licence-year as their revision 0 counterpart. They represent modifications, not new events.
- If two rows share the same `licencersn` and `folderyear` with different `licencerevisionnumber` values, only the highest revision number should be used (it represents the current state of the licence for that year).
- **Action required:** Deduplicate on (licencersn, folderyear) keeping max revision before survival analysis. 20,965 rows (2.7%) are revision 1+ and may have a corresponding revision 0 row.

---

### 1.9 `businessname`

Systematic scan for government entities and institutions:

**City of Vancouver itself:** "City of Vancouver" appears as a business licensee — the City holds its own licences for some operations (e.g., municipal facilities that serve the public). A very small count (< 10 unique instances, ~30–50 licence-years). These are institutional entities that cannot fail commercially.

**Province of BC:** "Province of BC Liquor Distribution Branch" appears in the Liquor Retail Store / Liquor Establishment categories. BC Liquor Stores are government-operated — they are not at risk of commercial failure. However, the count is small enough (~10–15 records) that it has negligible analytical impact.

**Vancouver School Board:** 3 unique records. Public institution, cannot fail commercially.

**Salvation Army:** ~10 records across various licence types. Charitable institution.

**YMCA / YWCA:** ~15–20 records. Non-profit community service organizations.

**Universities / Colleges:** Many hits in "COLLEGE" keyword are private colleges (Waterfront Business College, MTI Community College, etc.) which ARE commercial enterprises and should be included. Public universities (Simon Fraser University, UBC) hold a very small number of licences in the dataset for specific commercial-adjacent operations.

**Societies (*Society, *Foundation, *Association):** Approximately 15,325 rows match keywords associated with registered societies and non-profits. However, these span the full range of businesstypes including Office *Historic*, Restaurant *Historic*, and Retail — many are social enterprises, co-ops, or non-profits operating commercial spaces. The businesstype-level exclusions (Community Association) already capture the most clearly non-commercial entities.

**Verdict on businessname filtering:** The purely governmental entities (City of Vancouver, Province of BC Liquor Distribution, Vancouver School Board) are too small in number (~50–100 rows total) to materially affect analysis. Attempting to filter by businessname for non-profits or institutions would be error-prone: "Canadian Ports Clearance Association" sounds institutional but is a business service; "Metro Vancouver Roller Hockey League Ltd" sounds like a recreational club but holds a legitimate commercial venue licence. **Do not implement businessname-based exclusions** beyond the businesstype-level exclusions already defined.

---

### 1.10 `localarea` and Geospatial

**Critical finding: `localarea` is 100% blank across all 779,226 rows.**

This field, which should contain the Vancouver neighbourhood name (Downtown, Mount Pleasant, Kitsilano, etc.), is completely empty. This is a significant data quality issue for a spatial survival analysis of commercial gentrification.

The `geom` and `geo_point_2d` fields contain data for **403,610 rows (51.8%)**. The remaining 48.2% have no geographic coordinates.

**Implications:**
- Neighbourhood assignment must be derived from the coordinate fields, not from localarea
- The 48.2% without coordinates cannot be geographically placed without geocoding the street address fields (house + street + postalcode)
- Rows missing both geom/geo_point_2d AND localarea will need to be either geocoded or excluded from the spatial component of the analysis
- This is a data preparation task distinct from the scope audit, but it is significant: nearly half the dataset lacks neighbourhood information in any direct form

---

## 2. Exclusion Recommendations

### Definite Exclusions (apply unconditionally)

**Exclusion 1: Residential businesstypes**
```
businesstype IN (
  'Single Detached House *Historic*',
  'Apartment House Strata *Historic*',
  'Apartment House *Historic*',
  'Multiple Dwelling *Historic*',
  'Duplex *Historic*',
  'Rooming House *Historic*',
  'Pre-1956 Dwelling *Historic*',
  'Apartment House-99 Year Lease *Historic*',
  'Secondary Suite - Permanent *Historic*',
  'Live-aboards *Historic*'
)
```
Rationale: Residential property licences, not commercial businesses. These entities cannot "fail" as commercial enterprises.

**Exclusion 2: Short-Term Rental Operator**
```
businesstype = 'Short-term Rental Operator'
```
Rationale: Residential regulatory licence for homeowners renting via Airbnb. Not a commercial business. Deaths in this category reflect housing policy enforcement, not market dynamics.

**Exclusion 3: Pending status**
```
status = 'Pending'
```
Rationale: Business has applied for a licence but is not yet operating. Including these creates phantom ultra-short-duration records that corrupt survival curves. A Pending application that is rejected or withdrawn would look like a business death at age zero.

**Exclusion 4: Cancelled status**
```
status = 'Cancelled'
```
Rationale: Cancelled licences were cancelled before the business commenced normal operations, or represent enforcement actions (especially STR operators). Cancellation ≠ commercial failure. Including these mixes regulatory enforcement records with genuine business closures.

**Exclusion 5: Administrative licence types**
```
businesstype IN (
  'Temp Liquor Licence Amendment',
  'Liquor License Application',
  'Soliciting For Charity'
)
```
Rationale: These are process records within the City's licensing system, not records of operating businesses. A Temp Liquor Licence Amendment is a modification to an existing licence; the underlying business already has its own licence record.

**Exclusion 6: Temporary / event-based businesses**
```
businesstype IN (
  'Temporary Filming Company',
  'Christmas Tree Lot *Historic*'
)
```
Rationale: Designed to expire after their purpose is complete. Licence expiry is the intended outcome, not a business failure signal.

### Strongly Recommended Pre-Processing Step (not an exclusion but required for correctness)

**Deduplication on (licencersn, folderyear), keeping max licencerevisionnumber:**
20,965 rows carry revision numbers > 0 and may have an earlier revision row in the same (business, year) pair. The highest revision represents the current authoritative state of the licence. Failing to deduplicate will double-count licence-years for ~2.7% of records.

### Status Handling for Year 24

**Do NOT exclude year 24 Inactive records** — exclude or right-censor them differently. Year 24 has 50,083 Inactive records (80.1% of year 24 total) as a direct result of the mid-cycle extract. These businesses had 2024 licences that expired October–December 2024 and hadn't renewed yet at the extract date. They should be treated as **right-censored observations** (alive as of the extract date, follow-up ended), not as business failures.

---

## 3. Impact Assessment

### By Exclusion Category

| Exclusion | Rows Removed | % of Total |
|---|---|---|
| Residential types (10 types) | 151,117 | 19.4% |
| Short-Term Rental Operator | 32,452 | 4.2% |
| Pending status | 58,171 | 7.5% |
| Cancelled status | 21,615 | 2.8% |
| Administrative types (3 types) | 1,862 | 0.2% |
| Temporary types (2 types) | 1,493 | 0.2% |

**Overlap corrections (status × type):**
The Pending and Cancelled exclusions overlap with some residential and STR records already excluded by type. Overlap-corrected new removals:
- Residential already removed: 151,117
- STR (new, no prior overlap): 32,452
- Pending (new rows only, after removing residential and STR): 49,190
- Cancelled (new rows only): 15,435
- Administrative types (new): 1,739
- Temporary types (new): 1,399

### Debatable Categories (if also excluded)

| Category | Rows (in remaining) | % of remaining |
|---|---|---|
| Community Association *Historic* | 8,023 | 1.5% |
| Non-profit Housing *Historic* | 3,068 | 0.6% |
| Educational *Historic* | 2,305 | 0.4% |
| School (Business & Trade) *Historic* | 1,110 | 0.2% |
| Private School or College | 906 | 0.2% |
| ESL Instruction *Historic* | 826 | 0.2% |
| **Total debatable** | **16,238** | **3.1%** |

---

## 4. Cumulative Impact

Exclusions applied sequentially (most impactful first, overlap-corrected):

| Step | Action | Rows Removed | Cumulative Remaining | % of Original |
|---|---|---|---|---|
| — | Raw dataset | — | 779,226 | 100.0% |
| 1 | Remove residential types | 151,117 | 628,109 | 80.6% |
| 2 | Remove Short-Term Rental | 32,452 | 595,657 | 76.4% |
| 3 | Remove Pending status | 49,190 | 546,467 | 70.1% |
| 4 | Remove Cancelled status | 15,435 | 531,032 | 68.1% |
| 5 | Remove administrative types | 1,739 | 529,293 | 67.9% |
| 6 | Remove temporary/event types | 1,399 | 527,894 | 67.7% |
| **Final (core)** | | **251,332 removed** | **527,894** | **67.7%** |

**If debatable institutional categories are also excluded:**

| Action | Additional Removed | Final Remaining | % of Original |
|---|---|---|---|
| + Remove debatable institutional | 16,238 | 511,656 | 65.7% |

### Summary
- Core definite exclusions remove **251,332 rows (32.3%)** from the raw dataset
- The study population after core exclusions is **527,894 rows (67.7%)**
- Including the debatable institutional exclusions reduces this further to **511,656 rows (65.7%)**
- The original "16.2% residential" finding was an undercount — the correct residential figure is **19.4%** (including Live-aboards and all residential subtypes). When Short-Term Rentals are added, the residential/quasi-residential exclusion alone is **23.5%** of the raw data.

---

## 5. Edge Cases

### Edge Case 1: Short-Term Rental Operators as "the new commercial"

**Arguments to INCLUDE:** STR operators represent a form of commercial activity enabled by digital platforms; their entry and exit dynamics may be directly relevant to gentrification (STR growth displaces long-term residential stock, which changes neighbourhood commercial composition). Their survival patterns could be a predictor variable rather than an outcome.

**Arguments to EXCLUDE (recommended):** The study is commercial business survival, not housing economics. STR operators do not face commercial rent pressure, do not occupy commercial units, and their mortality is largely policy-driven (City enforcement campaigns). Mixing their survival curves with restaurant closures would be analytically meaningless.

**Recommendation:** Exclude from the survival model, but use as a contextual variable. STR density per neighbourhood per year could be a covariate in the Cox model.

### Edge Case 2: Community Association *Historic* (8,618 rows in remaining)

**Arguments to EXCLUDE:** These are non-profit associations, charities, mutual aid societies, and hobby clubs. They receive concessionary licensing rates (median fee < $50). They don't pay commercial rent, don't compete for market share, and don't "fail" in the same economic sense a restaurant does. Their mortality reflects loss of membership/funding, not market forces. Sample names: Heart & Stroke Foundation, Taoist Tai Chi Society, Bus Riders Union Society.

**Arguments to INCLUDE:** Some community associations operate commercial spaces (fitness classes, community halls for rent, food services). They occupy commercial space and contribute to neighbourhood vitality. Their closure may indicate neighbourhood decline as much as any restaurant closure.

**Recommendation:** EXCLUDE from survival analysis as the primary outcome, but potentially include as a control category. Community associations are so different in their economics that pooling their survival rates with commercial businesses would bias the baseline hazard.

### Edge Case 3: Non-Profit Housing *Historic* (3,068 in remaining after core exclusions)

**Arguments to EXCLUDE:** Non-profit housing operators (BC Housing, Atira, etc.) are subsidized institutional entities. They are not subject to market rent pressure and essentially cannot fail commercially — they have government backstops. Their "closures" reflect policy changes or portfolio reorganizations, not market dynamics.

**Arguments to INCLUDE:** They operate as businesses in the sense they have employees, pay operating costs, and manage commercial-scale operations. Their presence affects neighbourhood land use and commercial competition for space.

**Recommendation:** EXCLUDE. Government-backstopped entities are categorically different from market-dependent businesses. Their inclusion would flatten survival curves in neighbourhoods with heavy social housing presence.

### Edge Case 4: Educational *Historic* and Schools (4,147 rows in remaining)

**Arguments to INCLUDE:** Private tutoring businesses, ESL schools, trade schools, and private colleges are market-dependent businesses. An ESL school that loses students fails commercially just like a restaurant. They pay commercial rent. Examples include MTI Community College, Alexander College — real private educational enterprises. The Educational *Historic* subtype breakdown shows: Tutor (55%), Interpreter/Translator (21%), Training Facilities (3%). These are legitimate small businesses.

**Arguments to EXCLUDE:** Private schools have different failure modes (regulatory approval, immigration policy changes affecting student visas, public school competition). They are partially sheltered from pure market dynamics.

**Recommendation:** INCLUDE educational types. Private tutoring, language schools, and trade schools are unambiguously market-dependent commercial businesses. Public schools are too small in count to materially affect results and would only appear under School Board name patterns (which we've identified as ~3 records total).

### Edge Case 5: Exhibitions/Shows/Concerts *Historic* (1,798 rows)

**Arguments to EXCLUDE:** Individual events are temporary by design; their licence expires when the event ends. This is structurally similar to Temporary Filming Company which we excluded.

**Arguments to INCLUDE:** Many records under this type represent recurring annual events, permanent venue operators, and established promoters (e.g., Pacific National Exhibition appears repeatedly). These are persistent commercial entities.

**Recommendation:** INCLUDE, but acknowledge the type conflates persistent businesses with one-off events. The survival analysis will naturally handle recurring operators (they appear in multiple folderyears) versus one-off events (single appearance). A one-off concert promoter appearing once is not a "death" — they just stopped applying for licences as their activity scaled up or moved.

### Edge Case 6: Residential/Commercial *Historic* (2,704 rows in remaining)

**Arguments to EXCLUDE:** Hybrid use properties are ambiguous — they are partly residential, partly commercial. Including them may contaminate the commercial signal.

**Arguments to INCLUDE:** The commercial component of these properties is exactly what survival analysis should capture. Mixed-use properties are the front line of gentrification. Their persistence or failure is analytically meaningful.

**Recommendation:** INCLUDE, flagged as mixed-use. Sample names suggest these are investment holding companies and developers operating mixed-use properties (residential above, commercial below), not pure residential.

### Edge Case 7: Homecraft *Historic* (2,450 rows)

Home-based cottage businesses: hand-crafted goods, home baking, home-based services. Status breakdown: 1,540 Issued, 338 Gone Out of Business, 302 Pending, 188 Inactive, 82 Cancelled. These are genuinely commercial in that they generate revenue, but they operate from residential premises.

**Recommendation:** INCLUDE after removing Pending/Cancelled (already handled by status exclusions). Home-based businesses are commercial entities that pay taxes and can fail. Their survival dynamics differ from storefront businesses but they are within scope of "commercial business survival."

### Edge Case 8: Inactive status in years 13–23

In years 13–23, Inactive represents 2.2%–4.0% of records per year. Unlike year 24's timing artefact, these are genuine mid-year lapses. Three possible interpretations:
1. Business on hiatus (seasonal, ownership transition) — will renew next year
2. Business effectively dead but not yet formally reported as Gone Out of Business
3. Administrative error

**Recommendation:** Treat as censored rather than as a death event. Sensitivity analysis could also treat Inactive as a death proxy, particularly for years 13–23 where a business shows Inactive and then never reappears in subsequent years.

---

## 6. Recommended Scope Definition

**Recommended scope after applying all definite exclusions:**

The survival analysis covers **527,894 licence-year observations** representing commercial businesses licensed by the City of Vancouver between 2013 and 2024, after removing: (1) all residential property licences (dwelling types including Single Detached House, Apartment House, Multiple Dwelling, Duplex, Secondary Suite, Pre-1956 Dwelling, Apartment House Strata, Live-aboards, and 99-year Lease variants); (2) Short-Term Rental Operator licences, which are residential regulatory permits for Airbnb-style activity, not commercial businesses; (3) Pending status records, representing applications not yet approved; (4) Cancelled status records, representing licences cancelled before or during early operation; (5) purely administrative process entries (Temp Liquor Licence Amendments, Liquor License Applications, Charity Solicitation permits); and (6) inherently temporary licences designed to expire (Temporary Filming Company, Christmas Tree Lot). The remaining dataset represents persistent commercial enterprises — retailers, food service operators, contractors, professional service firms, health practitioners, hospitality businesses, and other market-dependent entities — whose entry, survival, and exit in Vancouver neighbourhoods constitute the phenomenon under study. Year 2024 records with Inactive status should be treated as right-censored observations due to the mid-cycle extract timing. Neighbourhood assignment requires derivation from the geom/geo_point_2d coordinates (available for 51.8% of remaining records) or geocoding of street addresses, as the localarea column is entirely blank across the full dataset.

**If a stricter scope is desired** (excluding institutionally-backed entities that do not compete in open markets), an additional 16,238 records can be removed by excluding Community Association *Historic*, Non-profit Housing *Historic*, and the four educational institution types, yielding a final dataset of **511,656 rows (65.7% of raw total)**.

---

## Appendix: Quick Reference — Exclusion Filter

### Pandas filter (definite exclusions)

```python
RESIDENTIAL_TYPES = {
    'Single Detached House *Historic*',
    'Apartment House Strata *Historic*',
    'Apartment House *Historic*',
    'Multiple Dwelling *Historic*',
    'Duplex *Historic*',
    'Rooming House *Historic*',
    'Pre-1956 Dwelling *Historic*',
    'Apartment House-99 Year Lease *Historic*',
    'Secondary Suite - Permanent *Historic*',
    'Live-aboards *Historic*',
}

ADMIN_TYPES = {
    'Temp Liquor Licence Amendment',
    'Liquor License Application',
    'Soliciting For Charity',
    'Temporary Filming Company',
    'Christmas Tree Lot *Historic*',
    'Short-term Rental Operator',
}

EXCLUDED_STATUSES = {'Pending', 'Cancelled'}

df_commercial = df[
    ~df['businesstype'].isin(RESIDENTIAL_TYPES) &
    ~df['businesstype'].isin(ADMIN_TYPES) &
    ~df['status'].isin(EXCLUDED_STATUSES)
].copy()

# Result: 527,894 rows (67.7% of raw 779,226)
```

### Additional deduplication (required for correct survival analysis)

```python
# Keep highest revision per (business, year) pair
df_commercial = (
    df_commercial
    .sort_values('licencerevisionnumber', ascending=False)
    .drop_duplicates(subset=['licencersn', 'folderyear'], keep='first')
)
```

### Year 24 treatment

```python
# Flag year 24 Inactive as right-censored (not death events)
df_commercial['is_right_censored'] = (
    (df_commercial['folderyear'] == '24') &
    (df_commercial['status'] == 'Inactive')
)
# These rows: 50,083 after applying commercial filter
```

---

*Audit produced: 2026-03-03*
*Data source: City of Vancouver Open Data — Business Licences 2013–2024*
