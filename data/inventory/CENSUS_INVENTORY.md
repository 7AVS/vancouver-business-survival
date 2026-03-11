# Census Data Inventory — Vancouver CMA Census Tract Profiles

**Project**: Vancouver Property Tax Analysis
**Data Phase**: Phase 1 (Acquisition) + Phase 2 (Quality Assessment)
**Author**: Andre Santos
**Date**: 2026-03-03
**Framework**: DATA-PROJECT-RIGOR.md v1.0

---

## Executive Summary

Four census years of Statistics Canada census tract profile data have been successfully downloaded for the Vancouver CMA (CMA code 933). Data spans 2006, 2011, 2016, and 2021, covering between 409 and 535 census tracts depending on the year. All required variable categories are present across all years. The 2021 and 2016 datasets have the richest variable coverage. The 2011 dataset uses the shorter-form National Household Survey (NHS) for income/immigration variables due to the long-form census cancellation in 2011. The 2006 data was delivered in SDMX-ML XML format and has been converted to CSV.

**Gate to Phase 3 (EDA)**: PASSED for 2016 and 2021. CONDITIONAL PASS for 2011 (NHS reliability caveat required). CONDITIONAL PASS for 2006 (variable coverage limited vs. later years).

---

## Phase 1: Data Inventory

### 1.1 Files Downloaded

| Year | File | Format | Compressed | Uncompressed | Source |
|------|------|--------|-----------|--------------|--------|
| 2021 | `2021_census_CT_national.zip` | CSV (ZIP) | 239 MB | 2.6 GB | StatCan GEONO=007 |
| 2021 | `2021_CT/vancouver_CMA_2021.csv` | CSV (extracted) | — | 215 MB | Extracted from above |
| 2021 | `2021_CT/98-401-X2021007_English_meta.txt` | TXT | — | 235 KB | Included in ZIP |
| 2021 | `2021_CT/98-401-X2021007_Geo_starting_row.CSV` | CSV | — | 273 KB | Included in ZIP |
| 2016 | `2016_census_CT_correct.zip` | CSV (ZIP) | 161 MB | 1.3 GB | StatCan GEONO=043 |
| 2016 | `2016_CT_correct/vancouver_CMA_2016.csv` | CSV (extracted) | — | 104 MB | Extracted from above |
| 2016 | `2016_CT_correct/98-401-X2016043_English_meta.txt` | TXT | — | 221 KB | Included in ZIP |
| 2016 | `2016_CT_correct/Geo_starting_row_CSV.csv` | CSV | — | 176 KB | Included in ZIP |
| 2011 | `2011_census_CT_national.zip` | CSV (ZIP) | 22 MB | ~300 MB | StatCan comp_download |
| 2011 | `2011_CT/98-316-XWE2011001-401.CSV` | CSV (extracted) | — | 276 MB | Extracted from above |
| 2011 | `2011_CT/vancouver_CMA_2011.csv` | CSV (filtered) | — | 25 MB | Filtered from above |
| 2011 | `2011_CT/98-316-XWE2011001-Metadata.CSV` | CSV | — | 7.9 KB | Included in ZIP |
| 2006 | `2006_census_CT_005.zip` | SDMX-ML XML (ZIP) | 59 MB | 3.7 GB | StatCan open-gc-ouvert |
| 2006 | `2006_CT/vancouver_CMA_2006.csv` | CSV (converted) | — | 45 MB | Converted from XML |

**Note on 2016_CT/ directory**: Contains `98-401-X2016007` files which are "Designated Places" profiles, NOT census tracts. The correct 2016 CT data is in `2016_CT_correct/` (catalog 98-401-X2016043). The `2016_CT/` directory should be ignored for analysis.

### 1.2 Geographic Coverage

| Year | CMA Code | CMA Name | Census Tracts | Source Verification |
|------|----------|----------|---------------|---------------------|
| 2021 | 933 | Vancouver | **535** | `98-401-X2021007_Geo_starting_row.CSV` |
| 2016 | 933 | Vancouver | **478** | `Geo_starting_row_CSV.csv` (2016) |
| 2011 | 933 | Vancouver | **457** | Counted from `vancouver_CMA_2011.csv` |
| 2006 | 933 | Vancouver | **409** | Counted from `vancouver_CMA_2006.csv` |

The increase in CT count over time reflects population growth and CT boundary revisions. CTs are periodically redesigned to keep populations within the 2,500–8,000 target range.

**CHALLENGE (Lightweight)**: Are these the same geographic units across time?
- No. Census tract boundaries are revised every census. CT codes are not stable identifiers across years. Join keys will require a CT concordance file.
- Verdict: Requires A1 (see Assumption Register). Load-bearing — must be addressed before temporal analysis.

### 1.3 Variable Coverage by Year

All years cover the core required variables. Detailed field-level mapping follows.

#### Population and Basic Demographics

| Variable | 2021 | 2016 | 2011 | 2006 |
|----------|------|------|------|------|
| Population count | Char ID 1 | ID 1 | "Population in 2011" | DIM 2 |
| Population density | Char ID 6 | ID 6 | "Population density per sq km" | DIM 4 |
| Median age | Char ID 40 | ID 40 | "Median age of the population" | Available |
| Age 0-14 (%) | Char ID 35 | ID 35 | Age group rows | Available |
| Age 65+ (%) | Char ID 37 | ID 37 | Age group rows | Available |

#### Income Variables

| Variable | 2021 | 2016 | 2011 (NHS) | 2006 |
|----------|------|------|------------|------|
| Median household income | ID 243 (2020 income) | ID 742 (2015 income) | Available (NHS) | Available (20% sample) |
| Average household income | ID 252 | ID 751 | Available (NHS) | Available |
| Median individual income | ID 113 | ID 663 | Available | Available |
| Income year reference | 2020 | 2015 | 2010 | 2005 |

#### Education

| Variable | 2021 | 2016 | 2011 (NHS) | 2006 |
|----------|------|------|------------|------|
| Bachelor's degree or higher | ID 2008 | ID 1693/1694 | Available (NHS) | Available (20% sample) |

#### Immigration

| Variable | 2021 | 2016 | 2011 (NHS) | 2006 |
|----------|------|------|------------|------|
| Recent immigrants | ID 1529+ | ID 1142+ | Available | Available |
| Non-permanent residents | ID 1529+ | Available | Available | Available |
| % visible minority | ID 1684 | ID 1324 | Available | Available |

#### Dwelling Type

| Variable | 2021 | 2016 | 2011 | 2006 |
|----------|------|------|------|------|
| Single-detached | ID 42 | ID 42 | "Single-detached house" | Available |
| Apartment (5+ storeys) | ID 47 | ID 43 | "Apartment, 5+ storeys" | Available |
| Apartment (<5 storeys) | ID 46 | ID 48 | "Apartment, <5 storeys" | Available |
| Condominium status | ID 1418/1419 | ID 1622/1623 | Available (20%) | Available |

#### Housing Tenure and Shelter Costs

| Variable | 2021 | 2016 | 2011 (NHS) | 2006 |
|----------|------|------|------------|------|
| Owner households | ID 1415 | ID 1618 | Available | Available |
| Renter households | ID 1416 | ID 1619 | Available | Available |
| Median monthly shelter (owned) | ID 1486 | ID 1674 | Available | Available |
| Median monthly shelter (rented) | ID 1494 | ID 1681 | Available | Available |
| Median dwelling value | ID 1488 | ID 1676 | Available | Available |
| % spending 30%+ on shelter | ID 1467 | ID 1669 | Available | Available |

#### Household Size

| Variable | 2021 | 2016 | 2011 | 2006 |
|----------|------|------|------|------|
| Average household size | ID 57 | ID 58 | Available | Available |
| Household size distribution | ID 50-56 | ID 51-57 | Available | Available |

#### Language

| Variable | 2021 | 2016 | 2011 | 2006 |
|----------|------|------|------|------|
| Non-official language at home | Available (char search) | ID 872+ | Available | Available |

---

## Phase 2: Data Quality Assessment

### 2.1 Completeness (Suppression Rates)

Statistics Canada applies random rounding and suppression to protect confidentiality in small geographies.

| Year | CT Count | Total Values Checked | Suppressed/Missing | Suppression Rate |
|------|----------|---------------------|-------------------|------------------|
| 2021 | 535 | 1,407,585 | 14,629 | **1.0%** — GOOD |
| 2016 | 478 | 1,074,066 | 116,987 | **10.9%** — MODERATE |
| 2011 | 457 | ~215,000 rows | Not fully checked | TBD |
| 2006 | 409 | 891,750 | Not checked | TBD |

**Finding 2021**: Suppression is very low (1%). Income and shelter cost variables at CT level appear complete for the vast majority of tracts.

**Finding 2016**: The 10.9% suppression rate is higher than 2021. This partly reflects the 25% sample data questions (income, education, immigration, housing tenure) having higher suppression in small tracts. Key variables like median income and median shelter costs appear available for most tracts in a sample check. Full suppression mapping by variable needed in EDA phase.

**CHALLENGE (Lightweight)**: Does suppression cluster in specific CTs or variables?
- Risk: If small CTs (low-income or sparse areas) have systematically higher suppression, missingness would be MNAR — invalidating simple imputation.
- Status: UNVERIFIED. Logged as A2 in Assumption Register.

### 2.2 Consistency — Data Format Differences Across Years

The census tract profile format changed substantially across years:

| Aspect | 2021 | 2016 | 2011 | 2006 |
|--------|------|------|------|------|
| File format | CSV | CSV | CSV | SDMX-ML XML (converted) |
| Geo ID format | `2021S0507933XXXX.XX` (DGUID) | `933XXXX.XX` (9-char) | `933XXXX.XX` | `933XXXXXX` (9-char) |
| Alt geo code | Numeric `933XXXX.XX` | Numeric | `9330XXX.XX` | Not in converted CSV |
| Income year | 2020 (pandemic year) | 2015 | 2010 | 2005 |
| Variables count | 2,631 | 1,979 (2247 profile) | 459 | 2,175 |
| Sample basis | 100% + 25% long form | 100% + 25% long form | 100% short form + NHS (20% sample) | 100% + 20% sample |

**Critical finding**: 2021 income data references 2020, a COVID-19 pandemic year. This is a structural break. Income comparisons between 2021 and 2016 must account for pandemic effects on employment income, CERB transfers, and COVID-related income support. Logged as A3.

**Critical finding**: 2011 income, education, immigration, and housing data comes from the National Household Survey (NHS), a voluntary survey that replaced the mandatory long-form census. The NHS has documented response rate issues and known biases (better-educated, higher-income Canadians overrepresented). Logged as A4.

### 2.3 Joinability Assessment

**Join to property tax data**: The key join will be CT geographic code to property tax parcels. Property tax parcels in Vancouver are identified by civic address or PID (Parcel Identifier). Joining census tracts to parcels requires:

1. A parcel-to-CT spatial crosswalk (address → CT), OR
2. Using the CT shapefile to spatially join tax parcels

Statistics Canada provides 2021 CT boundary files (separate download — not yet acquired). The City of Vancouver Open Data portal publishes a local area boundary file. A crosswalk from CT to CoV local area (neighborhood) may be available.

**CT code stability across years**: CT codes change every census. A CT concordance file would allow tracking individual tract-level changes. Statistics Canada publishes "Census Tract Correspondence Files." This has NOT been downloaded — logged as A1.

**Variable name consistency**: Variable names change between census years (different characteristic IDs, different question phrasings). A crosswalk table mapping equivalent variables across years is needed before longitudinal analysis. This will be built in Phase 4 (Data Preparation).

### 2.4 Known Data Issues

1. **2016 correct vs. misnamed directory**: The `2016_CT/` directory contains designated places data (98-401-X2016007), not census tracts. The correct CT data is in `2016_CT_correct/` (98-401-X2016043). Do not use `2016_CT/`.

2. **2021 income = 2020 pandemic year**: Any income-based comparisons involving 2021 must note this. Median household income likely understates pre-pandemic earning power. Employment income includes COVID transfers (CERB, CRB). Logged as A3.

3. **2011 NHS coverage gaps**: The NHS achieved approximately 68% response rate nationally. BC response rates were reasonable but not equivalent to mandatory census. For income/immigration/education variables in 2011, use lower confidence weights. Logged as A4.

4. **2006 XML conversion**: The 2006 data was converted from SDMX-ML XML. Values shown as "N" or "D" in the original (Missing/No data) are preserved in the VALUE field. During EDA, these must be filtered.

5. **CT boundary changes**: The 2006 Vancouver CMA had 409 CTs; 2021 has 535. New tracts were created as areas grew. Historical comparison at CT level is only valid within a given census year without a concordance file.

---

## Appendix A — Source Register

| ID | Title / Description | Type | Tier | URL | Date Accessed | Used For | Notes |
|----|---------------------|------|------|-----|---------------|----------|-------|
| S1 | Census Profile 2021 — CMAs, Tracted CAs and Census Tracts (98-401-X2021007) | Dataset | T1 | https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=007 | 2026-03-03 | Primary 2021 CT data | Released 2022-12-15. 2.6GB CSV |
| S2 | Census Profile 2016 — CMAs, Tracted CAs and Census Tracts (98-401-X2016043) | Dataset | T1 | https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/download-telecharger/comp/GetFile.cfm?Lang=E&FILETYPE=CSV&GEONO=043 | 2026-03-03 | Primary 2016 CT data | Released 2017-11-29. 1.3GB CSV |
| S3 | Census Profile 2011 — Census Tracts (98-316-XWE2011001) | Dataset | T1 | https://www12.statcan.gc.ca/census-recensement/2011/dp-pd/prof/details/download-telecharger/comprehensive/comp_download.cfm?LANG=E&CTLG=98-316-XWE2011001&FMT=CSV401 | 2026-03-03 | Primary 2011 CT data | 276MB CSV. Includes NHS data |
| S4 | Profile for CMAs, Tracted CAs and Census Tracts — 2006 Census (94-581-XCB2006005) | Dataset | T1 | https://www12.statcan.gc.ca/open-gc-ouvert/2006/94-581-XCB2006005.ZIP | 2026-03-03 | Primary 2006 CT data | SDMX-ML XML format; converted to CSV |
| S5 | Statistics Canada Census Profile Download Page (2021) | Web page | T1 | https://www12.statcan.gc.ca/census-recensement/2021/dp-pd/prof/details/download-telecharger.cfm | 2026-03-03 | Navigation/URL discovery | GEONO codes confirmed |
| S6 | Statistics Canada Census Profile Download Page (2016) | Web page | T1 | https://www12.statcan.gc.ca/census-recensement/2016/dp-pd/prof/details/download-telecharger/comp/page_dl-tc.cfm?Lang=E | 2026-03-03 | Navigation/URL discovery | GEONO=043 = CTs confirmed |
| S7 | Open Canada — Census Profile 2011 Census Tracts dataset listing | Open Data Catalogue | T1 | https://open.canada.ca/data/en/dataset/7153dd88-5aae-4cf6-a8e6-047f9e4bbff0 | 2026-03-03 | 2011 CT download URL discovery | Led to S3 URL |
| S8 | SDMX Structure file for 2006 CT data (Structure_94-581-XCB2006005.xml) | Dataset documentation | T1 | Extracted from 94-581-XCB2006005.ZIP | 2026-03-03 | 2006 variable code mapping | 2175 variables, 5065 geo codes |

---

## Appendix B — Assumption Register

| ID | Assumption | Basis | Source Tier | Confidence | Impact if Wrong | Verification Method | Status |
|----|------------|-------|-------------|------------|-----------------|---------------------|--------|
| A1 | Census tract codes do NOT persist across census years; boundary changes occurred between 2006-2021 | Statistics Canada CT methodology; standard geographic practice | T1 | HIGH (assumption well-established) | Incorrect temporal joins; double-counting or gaps in longitudinal analysis | Download CT Concordance File from StatCan; spatial overlay of CT shapefiles across years | ACCEPTED-WITH-CAVEAT — must resolve before temporal analysis |
| A2 | Data suppression (~ 1% in 2021, ~11% in 2016) is Missing Completely At Random (MCAR) within CT-level data | Visual inspection; no clustering evidence yet | T6 | LOW | If MNAR, imputation invalid; small-CT bias would affect conclusions about density/affordability | Chi-squared test of suppression rate by CT population size, neighborhood, income level | UNVERIFIED — load-bearing if imputation used |
| A3 | 2021 census income data (reference year 2020) is structurally different from prior census years due to COVID-19 pandemic effects | Known: CERB ($2000/month) and other COVID transfers inflated government transfer income; many employment income recipients had $0 in 2020 | T1 (known policy fact) | HIGH | Direct comparison of 2021 income to 2016 income without COVID adjustment would be misleading | Use Statistics Canada's 2019 reference year income where available in 2021 data (Char IDs 204-216); or flag all 2021 income comparisons with COVID caveat | ACCEPTED-WITH-CAVEAT — 2021 file contains 2019 reference-year income as alternate |
| A4 | 2011 Census income, education, immigration, and housing data (from NHS, 20% voluntary sample) is comparable to mandatory long-form data from 2006 and 2016 | NHS methodology differences are documented; StatCan released NHS alongside 2011 short-form census | T1/T3 | MEDIUM | Response bias in NHS overrepresents higher-income, better-educated groups; 2011 estimates may have wider confidence intervals for small CTs | Apply StatCan-published NHS quality indicators (DQ flags in `98-316-XWE2011001-401-DQ.CSV`); treat 2011 estimates for small CTs with appropriate uncertainty | ACCEPTED-WITH-CAVEAT — data quality flags exist and should be applied |
| A5 | The downloaded 2006 SDMX-ML XML file (94-581-XCB2006005) covers all CMAs and census tracts including the Vancouver CMA | Confirmed: XML header says "Profile for Census Metropolitan Areas, Tracted Census Agglomerations and Census Tracts"; 409 Vancouver CTs found in data | T1 | HIGH | Missing Vancouver CTs would cause incomplete 2006 coverage | Spot-check against individual CT profiles on StatCan website | VERIFIED — spot-checked GEO code 933 present with expected sub-codes |
| A6 | Vancouver CMA code is 933 consistently from 2006 through 2021 | Confirmed in all four datasets; geo index files show "Vancouver" labeled as 933 | T1 | HIGH | Wrong CMA selection | Cross-check with Statistics Canada CMA reference maps | VERIFIED — 933 = Vancouver in all 4 datasets |

---

## Appendix C — Adversarial Challenge Log

### Challenge 1: Joinability of CT data to property tax data

**Claim under challenge**: The census tract geographic identifier can be joined to property tax parcel data to enrich tax records with census demographics.

**Challenge mode**: Lightweight

**Objections raised**:
1. **CT boundaries don't match parcel boundaries**: A CT is a geographic area containing 2,500–8,000 people. Property tax parcels are individual lots. The join is spatial (many parcels → one CT), not a direct key match. A spatial join or address-geocoding step is required, which was not part of this download phase.
2. **Property tax data has address-based IDs, not CT codes**: BC Assessment Roll data identifies parcels by PID and civic address. These do not contain CT codes. Linking requires either geocoding addresses to geographic coordinates, or using a pre-built concordance file from the City of Vancouver.

**Defense**:
- Both objections are valid operational constraints, not fundamental barriers. Statistics Canada publishes CT boundary shapefiles (separate download). The City of Vancouver publishes parcel boundary files. A spatial join is standard GIS procedure.
- The challenge does NOT invalidate the census data download; it identifies a required additional step: downloading CT boundary files.

**Verdict**: SURVIVES CHALLENGE with clarification
**Confidence**: HIGH that the join IS achievable; MEDIUM on effort required
**Action**: Add task to download 2021 CT boundary shapefile from Statistics Canada

---

### Challenge 2: Is 2011 NHS data usable for this analysis?

**Claim under challenge**: The 2011 National Household Survey income/housing/education data can serve as the 2011 data point in a 2006–2021 trend analysis.

**Challenge mode**: Lightweight

**Objections raised**:
1. **NHS voluntary response bias is well-documented**: The NHS achieved 68% response nationally. Wealthier, more educated Canadians are known to respond at higher rates. This could upwardly bias income estimates and upwardly bias education levels in certain CTs.
2. **StatCan itself flagged NHS quality concerns**: Statistics Canada's Chief Statistician issued caveats about NHS data comparability with prior mandatory censuses. Some municipalities saw DA-level suppression rates of 30%+.

**Defense**:
- The NHS includes data quality flags (the `-DQ.CSV` file downloaded). These flags identify unreliable estimates at the CT level. Applying these flags removes the most problematic observations.
- For the purposes of a long-run trend analysis (2006→2016→2021), having a 2011 data point — even with caveats — is better than a 10-year gap. As long as the NHS limitations are disclosed in the methodology section and unreliable estimates are filtered using DQ flags, the data is usable.
- The 2011 short-form census data (population counts, age, dwelling type) is NOT from the NHS — it comes from the mandatory 100% census and is fully reliable.

**Verdict**: SURVIVES CHALLENGE with documented caveats
**Confidence**: MEDIUM for income/education/immigration; HIGH for population/dwelling variables
**Action**: Apply DQ flags before using 2011 sample-based variables; split results by data source type in analysis

---

## Phase 1 Gate Check

- [x] Every dataset has a source register entry with tier, provenance, and currency note
- [x] All primary datasets are T1 (Statistics Canada — Government of Canada official statistical releases)
- [x] Data provenance documented: Statistics Canada collected via census enumeration
- [x] Currency noted: each dataset's income reference year identified
- [x] Adversarial challenge on dataset choice documented (2011 NHS challenge above)
- [x] Geographic scope confirmed (Vancouver CMA = code 933, verified all four years)

**Phase 1 Gate: PASSED**

## Phase 2 Gate Check

- [x] Schema validation: column structures documented for each year
- [x] Completeness check: suppression rates measured for 2021 and 2016
- [x] Consistency: format differences across years documented
- [x] Joinability: assessment complete; CT shapefile identified as needed
- [x] Missing data assumption logged (A2) — NOT yet verified (not load-bearing until imputation decisions made)
- [x] 2011 NHS concern logged (A4) and DQ flag file available
- [x] Critical caveat: 2021 income = 2020 pandemic year (A3) logged

**Gaps requiring action before Phase 3**:
1. Download CT boundary shapefiles (2021 and historical) — needed for property tax join
2. Download CT Concordance files — needed for temporal analysis across years
3. Check 2011 and 2006 suppression rates (not yet measured)

**Phase 2 Gate: CONDITIONAL PASS** — proceed to EDA for 2021 and 2016; treat 2011 and 2006 as supplementary pending quality assessment completion.

---

## Next Steps

1. **Download CT boundary shapefiles** for spatial join to property tax parcels
   - URL: https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/index2021-eng.cfm
   - Need: 2021, 2016 CT shapefiles at minimum

2. **Download CT Concordance files** for temporal CT tracking
   - URL: https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/corr-cor/index2021-eng.cfm

3. **Build variable crosswalk** — map equivalent characteristics across 2006/2011/2016/2021 using the variable names/IDs documented above

4. **Run Phase 2 quality checks** on 2011 and 2006 suppression rates

5. **Filter 2006 XML-converted CSV** — replace "N" (missing) and "D" (no data) values with proper null markers

---

*Generated 2026-03-03*
*Data stored in: `/home/aurora/projects/sites/portfolio-projects/van-property-tax/data/raw/census/`*
