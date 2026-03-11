# Census Data Quality Assessment — Vancouver CMA Census Tract Profiles

**Project**: Vancouver Property Tax Analysis
**Stage**: 1 — Inventory and Quality Assessment (do NOT extract variables yet)
**Author**: Andre Santos
**Date**: 2026-03-03
**Input files audited**:
- `data/raw/census/2006_CT/vancouver_CMA_2006.csv`
- `data/raw/census/2011_CT/vancouver_CMA_2011.csv`
- `data/raw/census/2016_CT_correct/vancouver_CMA_2016.csv`
- `data/raw/census/2021_CT/vancouver_CMA_2021.csv`

**Warning**: `data/raw/census/2016_CT/` contains DESIGNATED PLACES data (98-401-X2016007), NOT census tracts. Do not use this directory. All 2016 references in this document use `2016_CT_correct/`.

---

## Table of Contents

1. [File Format Inventory (per wave)](#1-file-format-inventory)
2. [Row Structure and Coverage](#2-row-structure-and-coverage)
3. [Geographic Identifier Formats](#3-geographic-identifier-formats)
4. [Variable Lists by Wave](#4-variable-lists-by-wave)
5. [Key Variable Deep Dive](#5-key-variable-deep-dive)
6. [Cross-Wave Comparability Matrix](#6-cross-wave-comparability-matrix)
7. [Data Quality Flags and Suppression](#7-data-quality-flags-and-suppression)
8. [Critical Issues and Caveats](#8-critical-issues-and-caveats)
9. [Recommended Variables for Extraction](#9-recommended-variables-for-extraction)

---

## 1. File Format Inventory

### 2006 — `vancouver_CMA_2006.csv`

| Property | Value |
|----------|-------|
| Source product | 94-581-XCB2006005 (SDMX-ML XML, converted to CSV) |
| File size | 45 MB |
| Encoding | Latin-1 (ASCII-compatible) |
| Delimiter | Comma |
| Header row | Row 0 (standard) |
| BOM | None |
| Line endings | CRLF (`\r\n`) |
| Columns | 5 |
| Column names | `GEO_CODE`, `GEO_NAME`, `CHARACTERISTIC_ID`, `CHARACTERISTIC_NAME`, `VALUE` |
| VALUE dtype | float64 (all numeric — zero non-numeric values confirmed) |
| Missing values | 0 (0.0%) |

**Column descriptions**:
- `GEO_CODE`: Numeric CT identifier. 9-digit integer, no dot separator (e.g., `933000101`). The CMA-level row uses code `933`.
- `GEO_NAME`: Geographic name string (e.g., `"Vancouver"`).
- `CHARACTERISTIC_ID`: Integer ID (1–2175) indexing the variable within a CT.
- `CHARACTERISTIC_NAME`: Human-readable variable label.
- `VALUE`: Numeric value. Zero missing values — no suppression codes were used (or suppressed values became 0 during XML conversion).

---

### 2011 — `vancouver_CMA_2011.csv`

| Property | Value |
|----------|-------|
| Source product | 98-316-XWE2011001-401 (2011 Census Profile, short-form) |
| File size | 25 MB |
| Encoding | Latin-1 |
| Delimiter | Comma |
| Header row | Row 0 is a TITLE ROW (`"Census Profile - Census Tracts (CTs),,,,..."`), NOT column names |
| BOM | None |
| Line endings | LF |
| Actual column count | 13 |
| Column names | None (must be supplied manually — see below) |
| Missing values | 0 in the Total column; suppression indicated via `Total_flag` column |

**Correct column names to apply when reading** (skiprows=1, no header):
```
CTUID, Province, CMA_name, CT_local_code, Topic, Characteristic,
Note_ID, Total, Total_flag, Male, Male_flag, Female, Female_flag
```

**Column descriptions**:
- `CTUID`: Full CTUID string (e.g., `9330187.11`). Parsed as float64 by pandas due to decimal. Treat as float or convert to normalized string.
- `Province`: Province name (`"British Columbia"`).
- `CMA_name`: CMA name (`"Vancouver"`).
- `CT_local_code`: Local CT suffix without CMA prefix (e.g., `"0187.11"`).
- `Topic`: Category grouping (e.g., `"Age characteristics"`).
- `Characteristic`: Variable name (e.g., `"Median age of the population"`).
- `Note_ID`: Note reference number (float, often blank).
- `Total`: Numeric value — total population (both sexes). Always numeric; suppression shown via flag not value replacement.
- `Total_flag`: String flag — `"x"` (suppressed, n=465), `".."` (not available, n=465), `"A"` (use with caution, n=89).
- `Male`, `Female`: Sex-disaggregated values.

**CRITICAL ISSUE — 2011 DATA CONTENT**: This file contains ONLY **short-form mandatory census** variables:
- Population and dwelling counts
- Age characteristics
- Marital status
- Family characteristics
- Household and dwelling characteristics (structure only — counts, not costs)
- Language (detailed mother tongue, knowledge of official languages, home language)

**The following variable categories are ABSENT from the 2011 file**:
- Income (household, individual, median, average)
- Housing costs (shelter costs, rent, mortgage payments, % spending 30%+)
- Education (highest certificate/degree)
- Immigration status and period
- Visible minority status
- Employment and unemployment rates
- Dwelling value

These belong to the **2011 National Household Survey (NHS)**, product 99-004-XWE2011001, which is a **separate** StatCan product that has NOT been downloaded. The national file `98-316-XWE2011001-401.CSV` (276 MB) contains identical topic coverage to the Vancouver extract — it is also short-form only.

This contradicts the note in the prior `CENSUS_INVENTORY.md` (line 36: "Includes NHS data"). That note is **incorrect**. The 2011 file has no NHS income or housing data.

---

### 2016 — `vancouver_CMA_2016.csv` (in `2016_CT_correct/`)

| Property | Value |
|----------|-------|
| Source product | 98-401-X2016043 (2016 Census Profile, CTs) |
| File size | 104 MB |
| Encoding | **UTF-8 with BOM** (`\xef\xbb\xbf`) — use `encoding='utf-8-sig'` |
| Delimiter | Comma |
| Header row | Row 0 (standard) |
| BOM | YES — `\xef\xbb\xbf` byte prefix |
| Line endings | CRLF |
| Columns | 14 |
| Missing values (Total col) | 0.0% — all numeric; suppression shown via string codes in value cols |

**Column names** (14 total):
```
CENSUS_YEAR, GEO_CODE (POR), GEO_LEVEL, GEO_NAME, GNR, GNR_LF,
DATA_QUALITY_FLAG, ALT_GEO_CODE,
DIM: Profile of Census Tracts (2247),
Member ID: Profile of Census Tracts (2247),
Notes: Profile of Census Tracts (2247),
Dim: Sex (3): Member ID: [1]: Total - Sex,
Dim: Sex (3): Member ID: [2]: Male,
Dim: Sex (3): Member ID: [3]: Female
```

**Column descriptions**:
- `GEO_CODE (POR)`: CT identifier with dot separator (e.g., `9330001.01`). Float or string.
- `GEO_LEVEL`: Integer — `1` = CMA level, `2` = CT level.
- `ALT_GEO_CODE`: 9-digit integer without dot (e.g., `933000101`). Numeric. Must be normalized for joining.
- `GNR`: Short-form Global Non-Response rate (%). Key data quality indicator.
- `GNR_LF`: Long-form Global Non-Response rate (%). Applies to 25%-sample variables.
- `DATA_QUALITY_FLAG`: 5-digit composite flag (see metadata for digit-by-digit interpretation).
- `DIM: Profile of Census Tracts (2247)`: Variable name string.
- `Member ID: Profile of Census Tracts (2247)`: Integer variable ID (1–2247).
- `Dim: Sex (3): Member ID: [1]: Total - Sex`: Total value. May contain suppression codes: `"x"` (confidential), `"F"` (unreliable), `"..."` (not applicable).

**Suppression in Total-Sex column**:
- `"x"` (suppressed): 12,659 rows (1.2%)
- `"F"` (unreliable): 2,240 rows (0.2%)
- `"..."` (not applicable): 73 rows (<0.01%)
- **Total suppressed**: ~14,972 rows (1.4% of CT rows)

---

### 2021 — `vancouver_CMA_2021.csv`

| Property | Value |
|----------|-------|
| Source product | 98-401-X2021007 (2021 Census Profile, CTs) |
| File size | 215 MB |
| Encoding | Latin-1 (no BOM) |
| Delimiter | Comma |
| Header row | Row 0 (standard) |
| BOM | None |
| Line endings | CRLF |
| Columns | 22 |
| Missing values (C1_COUNT_TOTAL) | 19,451 (1.4%) |

**Column names** (22 total):
```
CENSUS_YEAR, DGUID, ALT_GEO_CODE, GEO_LEVEL, GEO_NAME,
TNR_SF, TNR_LF, DATA_QUALITY_FLAG, CHARACTERISTIC_ID, CHARACTERISTIC_NAME,
CHARACTERISTIC_NOTE, C1_COUNT_TOTAL, SYMBOL,
C2_COUNT_MEN+, SYMBOL.1, C3_COUNT_WOMEN+, SYMBOL.2,
C10_RATE_TOTAL, SYMBOL.3, C11_RATE_MEN+, SYMBOL.4, C12_RATE_WOMEN+, SYMBOL.5
```

**Column descriptions**:
- `DGUID`: Dissemination geography unique identifier (e.g., `"2021S0503933"`). String.
- `ALT_GEO_CODE`: Numeric CTUID (e.g., `9330001.01` stored as float). Requires normalization.
- `GEO_LEVEL`: String — `"Census metropolitan area"` or `"Census tract"`.
- `TNR_SF`: Total Non-Response rate, short form (%). Replaces 2016's GNR.
- `TNR_LF`: Total Non-Response rate, long form (%). Applies to 25%-sample variables.
- `DATA_QUALITY_FLAG`: 5-digit composite flag (same structure as 2016).
- `CHARACTERISTIC_ID`: Integer variable ID (1–2631).
- `CHARACTERISTIC_NAME`: Variable label. May include leading spaces for hierarchy indentation.
- `C1_COUNT_TOTAL`: Primary numeric value (both sexes / total). NaN if suppressed.
- `SYMBOL`: Suppression/quality indicator for C1_COUNT_TOTAL — values: `"x"` (17,752 rows), `"..."` (1,694 rows), `" r"` (revised, 109 rows), `".."` (5 rows).
- `C10_RATE_TOTAL`: Rate version of the characteristic (% or per-unit) where applicable.

**Key difference from 2016**: 2021 separates suppression into a dedicated `SYMBOL` column rather than replacing the value with a code string. This makes parsing cleaner.

---

## 2. Row Structure and Coverage

All four files use **long format**: one row per CT per variable.

| Year | Total rows | CMA-level rows | CT-level rows | CT count | Variables per CT |
|------|-----------|----------------|---------------|----------|-----------------|
| 2006 | 891,750 | 2,175 | 889,575 | **409** | **2,175** |
| 2011 | 215,704 | — (no CMA row) | 215,704 | **457** | **472** |
| 2016 | 1,076,315 | 2,248 | 1,074,066 | **478** | **2,247** |
| 2021 | 1,410,220 | 2,634 | 1,407,585 | **535** | **2,631** |

**Notes**:
- 2006: The CMA-level row uses `GEO_CODE = 933`; the 409 CTs use 9-digit codes. One extra GEO_CODE appears in the raw count (410 unique GEO_CODEs) because the CMA code `933` is included. True CT count = 409.
- 2011: No CMA-level row present in the extract. All 215,704 rows are CT-level. Each CT has exactly 472 rows (confirmed via `groupby().size()` — zero variance).
- 2016: GEO_LEVEL = 1 (2,248 rows = CMA), GEO_LEVEL = 2 (1,074,066 rows = CT). Each CT = exactly 2,247 rows.
- 2021: GEO_LEVEL = "Census metropolitan area" (2,634 rows), "Census tract" (1,407,585 rows). Each CT = exactly 2,631 rows.

**Growth in variable count**: 472 (2011 short-form) → 2,175 (2006) → 2,247 (2016) → 2,631 (2021). The 2011 count is low because it captures short-form census only. The growth from 2016 to 2021 reflects expanded topic coverage (additional ethnocultural, gender, housing adequacy indicators).

**CT count growth** (409 → 457 → 478 → 535) reflects population growth in Greater Vancouver and associated CT boundary redesigns. CT boundaries are not stable across years — see Section 3.

---

## 3. Geographic Identifier Formats

### Summary Table

| Year | Primary key column | Key format | Example | Normalization needed |
|------|-------------------|------------|---------|---------------------|
| 2006 | `GEO_CODE` | 9-digit integer, no dot | `933000101` | `str(code)[:7] + '.' + str(code)[7:]` |
| 2011 | `CTUID` | Float64 with decimal | `9330187.11` | Convert to str, pad decimal to 2 places |
| 2016 | `ALT_GEO_CODE` | 9-digit integer, no dot | `933000101` | `str(code)[:7] + '.' + str(code)[7:]` |
| 2021 | `ALT_GEO_CODE` | Float64 with decimal | `9330001.01` | Convert to str, pad decimal to 2 places |

### CTUID Normalization Function

The concordance file (`ct_local_area_concordance.csv`) uses the canonical CTUID format: `{CMA_3digit}{CTNUM_4digit}.{SUFFIX_2digit}` (always 2 decimal places). Apply this normalization before joining:

```python
def normalize_ctuid(raw_code) -> str:
    """Convert any raw census CT identifier to canonical CTUID format."""
    s = str(raw_code)
    if '.' in s:
        base, dec = s.rsplit('.', 1)
        return f"{base}.{dec.zfill(2)}"
    else:
        # 9-digit integer format (2006, 2016 ALT_GEO_CODE as integer)
        s = s.split('.')[0]  # remove any float trailing .0
        return f"{s[:7]}.{s[7:]}"
```

### .00-Suffix Issue (2011 and 2021)

In 2011 and 2021, CTs with a zero decimal suffix (i.e., `9330025.00` in canonical form) are stored as `9330025.0` when pandas reads the CTUID as float64. The `.zfill(2)` normalization above corrects this. Approximately 76 of 457 CTs (2011) and a similar proportion in 2021 are affected.

### CT Boundary Changes Across Years

CT boundaries are redesigned every census cycle. The Vancouver CMA CT count grew from 409 (2006) to 535 (2021) — a 30.8% increase. Individual CT codes do NOT persist across years. Temporal analysis must:

1. Join each year's data to the year-specific concordance (`ct_id` + `census_year`)
2. Aggregate to local area level before comparing across years
3. Never attempt direct CT-to-CT matching across census years

The concordance file handles this per-year correctly:
- 2006: 409 CMA CTs → 115 CoV CTs matched
- 2011: 457 CMA CTs → 123 CoV CTs matched
- 2016: 478 CMA CTs → 125 CoV CTs matched
- 2021: 535 CMA CTs → 133 CoV CTs matched

---

## 4. Variable Lists by Wave

### 2006 — 2,175 Variables

**Topic groups** (inferred from structure):
- Population and dwelling counts (IDs 1–4)
- Age by sex in 5-year bands (IDs 5–43) — NO pre-calculated median age
- Marital and common-law status (IDs 44–52)
- Census family structure and size (IDs 53–100)
- Dwelling characteristics: tenure, condition, period of construction, structural type (IDs 101–130)
- Household size and type (IDs 131–142)
- Detailed mother tongue (IDs 143–245)
- Knowledge and use of official languages (IDs 246–360)
- Mobility (IDs 361–476)
- Immigrant status, place of birth, period of immigration, age at immigration (IDs 477–580)
- Labour force activity by age/sex (IDs 580–800+)
- Occupation (IDs 830–980)
- Industry (IDs 1000–1080)
- Mode of transportation / place of work (IDs 1080–1140)
- Education / highest degree (IDs 1200–1290)
- Visible minority groups (IDs 1305–1320)
- Income: individual, family, household — before and after tax (IDs 1567–1990)
- Housing: shelter costs, spending 30%+, dwelling value (IDs 1991–2175)

**Sample basis for key variables**:
- Population counts, dwelling type: 100% data
- Income, education, immigration, housing costs, occupation: **20% sample data**

**Key observation**: 2006 has NO pre-calculated median age or population density. These must be derived:
- Population density = Population / land area (IDs 2 and 4)
- Median age = requires interpolation from 5-year age bands (IDs 5–43)

### 2011 — 472 Variables (SHORT-FORM ONLY)

**Topic groups** (confirmed from file):
- Population and dwelling counts (7 variables): Population 2011, Population 2006, change %, private dwellings, occupied dwellings, density, land area
- Age characteristics (26 variables): 5-year bands from 0–4 to 85+, median age, % aged 15+
- Marital status (9 variables)
- Family characteristics (35 variables): census family structure, children, persons in households
- Household and dwelling characteristics (49 variables): household type, dwelling structural type, household size
- Detailed mother tongue (111 variables)
- Knowledge of official languages (5 variables)
- First official language spoken (7 variables)
- Detailed language spoken most often at home (111 variables)
- Detailed other language spoken regularly at home (112 variables)

**Variables CONFIRMED ABSENT** (all belong to 2011 NHS, not downloaded):
- Median household income
- Median shelter costs (rent, owner payments)
- % spending 30%+ on shelter
- Dwelling value
- Highest certificate/diploma/degree
- Immigrant status
- Visible minority status
- Employment / unemployment rates
- Occupation, industry

**2011 short-form variables that ARE available** (for comparability):
- Population count, population density, median age
- Dwelling type (single-detached, apartment, etc.)
- Owner / renter counts (from household type data — but NOT directly as tenure: household type provides family/non-family breakdown, NOT owner/renter)

**CORRECTION**: The 2011 file does NOT include owner/renter counts. "Household and dwelling characteristics" covers household *type* (census family, lone parent, non-family) and dwelling *structural type* (apartment, house, etc.) but NOT tenure (owned vs. rented). Tenure belongs to NHS.

### 2016 — 2,247 Variables

**Topic groups** (from 98-401-X2016043 product):
- Population, dwellings, age: IDs 1–60 (100% data)
- Families and households: IDs 61–110 (100% data)
- Income — individual, family, household (100% + 25% sample): IDs 111–900
- Ethnocultural diversity and immigration (25% sample): IDs 1100–1340
- Education (25% sample): IDs 1680–1860
- Labour (25% sample): IDs 1860–1960
- Dwelling type and tenure (100% data): IDs 41–50, 1615–1680
- Housing costs and affordability (25% sample): IDs 1660–1685

**Sample basis**: 100% (mandatory short-form) + 25% sample (reinstated long-form census). 2016 was the first census after the 2011 long-form cancellation — mandatory long form restored, so all income/education/immigration variables are from a proper probability sample.

### 2021 — 2,631 Variables

**Topic groups** (from 98-401-X2021007 product):
- Population, dwellings, age: IDs 1–60 (100% data)
- Families and households: IDs 61–110 (100% data)
- Income — 2020 reference year (100% + 25% sample): IDs 111–400
- Income — 2019 reference year (100% + 25% sample): IDs 204–241 (individual only, NOT household)
- Housing: IDs 1400–1500 (100% + 25% sample)
- Ethnocultural diversity and immigration (25% sample): IDs 1520–1680
- Visible minority and ethnic origin (25% sample): IDs 1683–1800
- Education (25% sample): IDs 1990–2100
- Labour (25% sample): IDs 2200–2300

**New in 2021 vs 2016**:
- Gender diversity categories (men+/women+ notation replacing male/female)
- Additional housing adequacy indicators (suitability, major repairs needed + spending 30% combinations)
- Expanded ethnocultural origin categories
- 2019 reference year income (individual only) as alternative to pandemic-year 2020 data

---

## 5. Key Variable Deep Dive

For each target variable: availability, characteristic ID, exact name, definition notes, and comparability caveats.

### 5.1 Population / Population Density

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Population count | ID 2: "Population, 2006 - 100% data" | "Population in 2011" (Characteristic) | ID 1: "Population, 2016" | ID 1: "Population, 2021" |
| Land area (sq km) | ID 4: "Land area in square kilometres, 2006" | "Land area (square km)" | — | — |
| Population density | **DERIVED** (pop / land area) | "Population density per square kilometre" | ID 6: "Population density per square kilometre" | ID 6: "Population density per square kilometre" |

**2006 caveat**: No pre-calculated density. Must compute: `VALUE[ID=2] / VALUE[ID=4]`.

**Definition consistency**: Population counts are always as of census day (May in each census year). Density is population per km² of land area. Comparable across all 4 years.

---

### 5.2 Median Age

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Median age | **NOT AVAILABLE** | "Median age of the population" | ID 40: "Median age of the population" | ID 40: "Median age of the population" |

**2006 caveat**: Median age is not a pre-calculated characteristic. The 2006 file provides 5-year age group counts by sex (IDs 6–43) from which median age can be approximated via interpolation. However, this introduces estimation error and is methodologically inconsistent with 2011/2016/2021 direct values. **Treat 2006 median age as derived/approximate only.**

**Age group availability in 2006 for 25–44 cohort**: Age bands 25–29, 30–34, 35–39, 40–44 are available separately for male and female populations, enabling calculation of the gentrification-cohort (25–44) total count.

---

### 5.3 Median Household Income (Before-Tax and After-Tax)

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Median household income (total/before-tax) | ID 2003 (income year 2005, 20% sample) | **NOT IN FILE** | ID 742 (income year 2015, 100% data) | ID 243 (income year 2020, 100% data) |
| Median after-tax household income | ID 2033 (income year 2005, 20% sample) | **NOT IN FILE** | ID 743 (income year 2015, 100% data) | ID 244 (income year 2020, 100% data) |

**Exact variable names**:
- 2006: `"Median household income $"` (parent: `"Household income in 2005 of private households - 20% sample data"`)
- 2016: `"Median total income of households in 2015 ($)"` / `"Median after-tax income of households in 2015 ($)"`
- 2021: `"Median total income of household in 2020 ($)"` / `"Median after-tax income of household in 2020 ($)"`

**CRITICAL COMPARABILITY ISSUE — INCOME YEAR**:
- 2006 census: income reference year = **2005**
- 2016 census: income reference year = **2015**
- 2021 census: income reference year = **2020** (COVID pandemic year)

**2021 COVID problem**: The 2020 income data includes CERB ($2,000/month for ~8.9M Canadians), CRB, and other emergency transfers. Many employment income earners had $0 in 2020 due to layoffs. Median household income in 2021 census is therefore NOT directly comparable to 2016 or 2006 income figures.

**Partial mitigation**: The 2021 file contains **individual-level** income for 2019 (IDs 204–241) as an alternative pre-COVID reference. However, **household-level 2019 income is NOT available** in the 2021 CT profile — only 2020 household income is provided. This means no direct pre-COVID household income comparison exists at CT level.

**2011 gap**: Median household income is entirely absent from the 2011 extract. The 2011 NHS would be required (separate download). **This wave must be treated as missing for all income variables.**

**Sample basis change**: 2006 income = 20% sample. 2016/2021 income = 100% data (derived from administrative tax records merged with census, for the first time in 2016). This methodology change may create small systematic differences independent of actual income changes.

---

### 5.4 Housing Costs — Median Rent and Median Owner Payments

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Median monthly rent | **NOT AVAILABLE** | **NOT IN FILE** | ID 1681: "Median monthly shelter costs for rented dwellings ($)" | ID 1494: "Median monthly shelter costs for rented dwellings ($)" |
| Average gross rent | ID 2053 (20% sample) | **NOT IN FILE** | ID 1682: "Average monthly shelter costs for rented dwellings ($)" | ID 1495: "Average monthly shelter costs for rented dwellings ($)" |
| Median monthly owner costs | **NOT AVAILABLE** | **NOT IN FILE** | ID 1674: "Median monthly shelter costs for owned dwellings ($)" | ID 1486: "Median monthly shelter costs for owned dwellings ($)" |
| Average owner major payments | ID 2058 (20% sample) | **NOT IN FILE** | ID 1675: "Average monthly shelter costs for owned dwellings ($)" | ID 1487: "Average monthly shelter costs for owned dwellings ($)" |

**2006 definition difference**: 2006 uses "average gross rent" and "average owner major payments" — these are AVERAGES, not MEDIANS. 2016 and 2021 provide median shelter costs. Averages and medians are not interchangeable, particularly in skewed distributions. **Do not compare 2006 housing cost figures to 2016/2021 median figures as if they are equivalent metrics.**

**2011 gap**: All housing cost variables absent (NHS territory).

---

### 5.5 % Spending 30%+ on Shelter (Affordability Indicator)

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Renters spending 30%+ | ID 2054 (COUNT, 20% sample) | **NOT IN FILE** | ID 1680: "% of tenant households spending 30% or more of its income on shelter costs" (RATE) | ID 1492: "% of tenant households spending 30% or more of its income on shelter costs" (RATE) |
| Owners spending 30%+ | ID 2059 (COUNT, 20% sample) | **NOT IN FILE** | ID 1673: "% of owner households spending 30% or more of its income on shelter costs" (RATE) | ID 1484: "% of owner households spending 30% or more of its income on shelter costs" (RATE) |

**CRITICAL FORMAT CHANGE**: 2006 provides COUNTS (e.g., "240 tenant households"), while 2016 and 2021 provide RATES (e.g., "24.3%"). To create a comparable series, the 2006 rate must be derived:

```
2006 renter rate = ID_2054 / ID_2052   [tenant spending 30%+ / total tenant dwellings]
2006 owner rate  = ID_2059 / ID_2056   [owner spending 30%+ / total owner dwellings]
```

Denominators:
- ID 2052: `"Tenant-occupied private non-farm, non-reserve dwellings"`
- ID 2056: `"Owner-occupied private non-farm, non-reserve dwellings"`

**Definition consistency**: The underlying concept ("housing core need threshold") is consistent across all years. The 30%-of-income threshold on shelter costs is a stable StatCan definition.

**2011 gap**: Absent (NHS territory).

---

### 5.6 Owner / Renter Ratio

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Owner households | ID 105: "Owned" (20% sample) | **NOT IN FILE** (tenure not in short-form) | ID 1618: "Owner" | ID 1415: "Owner" |
| Renter households | ID 106: "Rented" (20% sample) | **NOT IN FILE** | ID 1619: "Renter" | ID 1416: "Renter" |
| Total tenure denominator | ID 104 (20% sample) | — | Computed from 1618+1619 | Computed from 1415+1416 |

**2011 gap**: Dwelling tenure (owner vs. renter) is classified as a long-form/NHS variable in 2011. The 2011 short-form household dwelling characteristics file covers structural type (apartment vs. house) but NOT tenure.

---

### 5.7 Education (% University Degree)

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Population 25–64 (denominator) | ID 1251: "Total population 25 to 64 years by highest cert..." (20% sample) | **NOT IN FILE** | ID 1698: "Total - Highest certificate... aged 25 to 64" (25% sample) | ID 2014: "Total - Highest certificate... aged 25 to 64" (25% sample) |
| Bachelor's degree (25–64) | ID 1260: "Bachelor's degree" (within 25–64 group) | **NOT IN FILE** | ID 1708: "Bachelor's degree" (within 25–64 group) | ID 2025: "Bachelor's degree" (within 25–64 group) |
| Bachelor's degree or higher (25–64) | Computed: IDs 1260+1262+1263+1264 | **NOT IN FILE** | ID 1707: "University certificate, diploma or degree at bachelor level or above" | ID 2024: "Bachelor's degree or higher" |

**Definition change 2016→2021**: 2021 introduces the single aggregate `"Bachelor's degree or higher"` (ID 2024) which directly corresponds to 2016's `"University certificate, diploma or degree at bachelor level or above"` (ID 1707). Use these.

**2006 computation**: Sum IDs 1260 (Bachelor's) + 1262 (Medicine/dentistry/etc.) + 1263 (Master's) + 1264 (PhD) within the 25–64 age group subsection.

**2011 gap**: Absent (NHS territory).

---

### 5.8 Immigration (% Immigrant, % Recent Immigrant)

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Total for immigration status | ID 477 (20% sample) | **NOT IN FILE** | ID 1140 (25% sample) | ID 1527 (25% sample) |
| Immigrants | ID 481: "Immigrants" | **NOT IN FILE** | ID 1142: "Immigrants" | ID 1529: "Immigrants" |
| Recent immigrants (last 5 years) | IDs 515–547: "Total recent immigrants" (2001–2006) | **NOT IN FILE** | ID 1149: "2011 to 2016" | ID 1536: "2016 to 2021" |
| Non-permanent residents | ID 514 | **NOT IN FILE** | ID 1150 | ID 1537 |

**Definition consistent**: "Immigrants" = persons who are, or have been, landed immigrants (permanent residents). Consistent across 2006, 2016, 2021.

**2011 gap**: Absent (NHS territory).

---

### 5.9 Visible Minority %

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Total population (denominator) | ID 1305 (20% sample) | **NOT IN FILE** | ID 1323 (25% sample) | ID 1683 (25% sample) |
| Total visible minority | ID 1306 | **NOT IN FILE** | ID 1324 | ID 1684 |
| Not a visible minority | ID 1319 | **NOT IN FILE** | ID 1337 | ID 1697 |

**Definition note**: "Visible minority" is a Canadian Employment Equity Act category. The definition is consistent across 2006, 2016, 2021. The denominator is persons in private households (20%/25% sample base), not total population.

**2011 gap**: Absent (NHS territory).

---

### 5.10 Age Distribution (25–44 Gentrification Cohort)

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Total population (base) | ID 5 | "Total population by age groups" | ID 8 | ID 8 |
| 25–29 years | IDs 12+31 (M+F) | "25 to 29 years" | ID 16 | ID 16 |
| 30–34 years | IDs 13+32 (M+F) | "30 to 34 years" | ID 17 | ID 17 |
| 35–39 years | IDs 14+33 (M+F) | "35 to 39 years" | ID 18 | ID 18 |
| 40–44 years | IDs 15+34 (M+F) | "40 to 44 years" | ID 19 | ID 19 |
| **25–44 total** | Sum of above M+F | Sum of above | Sum IDs 16+17+18+19 | Sum IDs 16+17+18+19 |

**2006 structure**: Age groups are reported SEPARATELY for male (IDs 6–24) and female (IDs 25–43). There is no combined 25–44 aggregate. Must sum: Male 25–29 (ID 12) + Male 30–34 (ID 13) + Male 35–39 (ID 14) + Male 40–44 (ID 15) + Female 25–29 (ID 31) + Female 30–34 (ID 32) + Female 35–39 (ID 33) + Female 40–44 (ID 34).

**2011/2016/2021**: Age groups are provided as totals (both sexes combined). Consistent across these three years.

---

### 5.11 Employment / Unemployment Rate

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Unemployment rate | ID 585 (20% sample, multiple by age/sex breakdowns) | **NOT IN FILE** | ID 1872 (25% sample) | ID 2230 (25% sample) |
| Employment rate | ID 584 | **NOT IN FILE** | ID 1871 | ID 2229 |

**2006 note**: Unemployment rate appears many times (IDs 585, 593, 601, ...) for different age/sex subgroups. The overall unemployment rate for the population 15+ is ID 585.

**2011 gap**: Absent (NHS territory).

---

### 5.12 Dwelling Type

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Total occupied dwellings | ID 122 (100%) | "Total number of occupied private dwellings by structural type of dwelling" | ID 41 (100%) | ID 41 (100%) |
| Single-detached house | ID 123 | "Single-detached house" | ID 42 | ID 42 |
| Apartment, 5+ storeys | ID 127 | "Apartment, building that has five or more storeys" | ID 43 | ID 47 |
| Apartment, <5 storeys | ID 128 | "Apartment, building that has fewer than five storeys" | ID 48 | ID 46 |
| Apartment, duplex | ID 126 | "Apartment, duplex" | ID 47 | ID 45 |
| Row house | ID 125 | "Row house" | ID 46 | ID 44 |
| Semi-detached | ID 124 | "Semi-detached house" | ID 44 | ID 43 |

**IMPORTANT**: The Member ID numbering shifted between 2016 and 2021 for dwelling type. "Apartment, 5+ storeys" is ID 43 in 2016 but ID 47 in 2021. Always match by characteristic name, not by ID, when bridging years.

**Definition consistent**: The structural type categories are consistent across all four years. "Apartment in a building that has five or more storeys" is the same concept in all waves.

**2011 availability**: Dwelling type IS in the 2011 short-form data. This is one of the few variables available in 2011 alongside 2006/2016/2021.

---

### 5.13 Median Dwelling Value

| Variable | 2006 | 2011 | 2016 | 2021 |
|----------|------|------|------|------|
| Median dwelling value | **NOT AVAILABLE** | **NOT IN FILE** | ID 1676: "Median value of dwellings ($)" | ID 1488: "Median value of dwellings ($)" |
| Average dwelling value | ID 2057: "Average value of dwelling $" (20% sample) | **NOT IN FILE** | ID 1677: "Average value of dwellings ($)" | ID 1489: "Average value of dwellings ($)" |

**2006 definition**: Average (not median) value. Comparable to 2016/2021 average value only.

---

## 6. Cross-Wave Comparability Matrix

### Legend
- **FULL**: Same concept, same metric type, same sample base — directly comparable
- **DERIVED**: Available but requires calculation or normalization
- **DIFF**: Methodological or definitional difference — compare with caution
- **MISS**: Data not present in this year
- **APPROX**: Available but estimation required (e.g., median from grouped data)

| Variable | 2006 | 2011 | 2016 | 2021 | Comparability Notes |
|----------|------|------|------|------|---------------------|
| Population count | FULL | FULL | FULL | FULL | Identical concept, 100% data all years |
| Population density | DERIVED | FULL | FULL | FULL | 2006 must compute; 2011–2021 pre-calculated |
| Median age | APPROX | FULL | FULL | FULL | 2006 requires interpolation from 5-yr bands |
| Age 25–44 count | DERIVED | FULL | FULL | FULL | 2006 must sum M+F bands separately |
| Dwelling type (% apartment, % single) | FULL | FULL | FULL | FULL | Consistent definition all years |
| Owner/renter ratio | FULL | **MISS** | FULL | FULL | 2011: tenure is NHS variable |
| Median household income | DIFF | **MISS** | FULL | DIFF | Income year varies; 2021=2020 COVID year; 2011 absent |
| Median after-tax household income | DIFF | **MISS** | FULL | DIFF | Same caveats as above |
| Median monthly rent | MISS | **MISS** | FULL | FULL | 2006: average only; 2011 absent; 2016–2021 median |
| Average gross rent / shelter (rented) | DIFF | **MISS** | FULL | FULL | 2006: average; 2016–2021: average comparable |
| Median monthly owner costs | MISS | **MISS** | FULL | FULL | 2006: average only; 2011 absent |
| % renter spending 30%+ | DERIVED | **MISS** | FULL | FULL | 2006: must derive rate from counts; 2011 absent |
| % owner spending 30%+ | DERIVED | **MISS** | FULL | FULL | 2006: must derive rate from counts; 2011 absent |
| Median dwelling value | MISS | **MISS** | FULL | FULL | 2006: average only; 2011 absent |
| % bachelor degree (25–64) | DERIVED | **MISS** | FULL | FULL | 2006: must sum subcomponents; 2011 absent |
| % visible minority | FULL | **MISS** | FULL | FULL | 2011 absent (NHS); 2006/2016/2021 comparable |
| % immigrants | FULL | **MISS** | FULL | FULL | 2011 absent; definition consistent |
| % recent immigrants (5-yr) | DIFF | **MISS** | FULL | FULL | 2006: 2001–2006; 2016: 2011–2016; 2021: 2016–2021 (consistent windows, different periods) |
| Unemployment rate | FULL | **MISS** | FULL | FULL | 2011 absent; definition consistent |
| Employment rate | FULL | **MISS** | FULL | FULL | 2011 absent |

### Definition Changes to Flag at Extraction Time

1. **Income reference years**: 2005 (2006 census), 2015 (2016), 2020 (2021). Do not merge into a single column without marking the year. The 2021 individual income for 2019 (IDs 204–241) is available as a partial pre-COVID alternative.

2. **Bachelor's degree label**: 2021 uses "Bachelor's degree or higher" as a single bucket; 2016 uses "University certificate, diploma or degree at bachelor level or above." These are equivalent in meaning.

3. **Dwelling ID numbering**: IDs for apartment types shifted between 2016 and 2021. Extract by name, not by ID.

4. **Sex terminology**: 2021 uses "Men+" and "Women+" column labels (inclusive of non-binary). 2016 and earlier use "Male" and "Female." For total (both sexes combined) analysis, this has no impact — the `C1_COUNT_TOTAL` / `Dim: Sex (3): Member ID: [1]: Total - Sex` is unaffected.

5. **Housing methodology in 2016**: Shelter cost data in 2016 is based on the reinstated long-form census (mandatory 25% sample), replacing the 2011 NHS. The 2006 data uses a 20% sample (equivalent in mandatory status but slightly different sample size).

---

## 7. Data Quality Flags and Suppression

### 2006

- **Suppression rate**: 0% — zero suppressed or missing values in the VALUE column.
- **No quality flag column**: There is no GNR or DQ flag column in the 2006 extract.
- **Note on XML conversion**: The original 2006 data was SDMX-ML XML format. The CSV conversion shows no suppression codes (no "N", "D", or "x" values found in any VALUE field). Whether originally suppressed values were zeroed during conversion or were genuinely absent from the XML is unknown. This is a latent data quality risk.
- **Sample confidence**: Income/education/immigration variables are 20% sample data with standard errors provided (e.g., ID 1588 "Standard error of average income"). These standard errors can be used to assess precision at CT level.

### 2011

- **Total_flag column**: Present. Values observed: `"x"` (n=465), `".."` (n=465), `"A"` (n=89).
  - `"x"`: Suppressed for confidentiality
  - `".."`: Not available for this reference period
  - `"A"`: Use with caution (some unreliability)
- **DQ file available**: `98-316-XWE2011001-401-DQ.CSV` contains CT-level 5-digit data quality flags. This should be merged before analysis.
- **Applies only to short-form variables**: Since all 2011 income/NHS variables are absent anyway, the DQ flags affect only population/age/language/household structure variables.

### 2016

- **GNR (Global Non-Response rate)**: Short-form quality indicator. Mean GNR for Vancouver CTs = 4.8% (very good). Only **3 CTs have GNR > 25%** (high non-response):
  - CT `9330181.15` (GNR 40.5%, GNR_LF 25.8%) — population ~49 (extremely small CT)
  - CT `9330251.01` (GNR 73.7%, GNR_LF 63.5%) — population ~49 (extremely small CT)
  - CT `9330251.02` (GNR 25.3%, GNR_LF 30.3%) — border case
- **Suppression in Total column**: 12,659 rows suppressed as `"x"` (1.2%), 2,240 as `"F"` (0.2%), 73 as `"..."` (0.01%). Total 1.4% suppressed.
- **DATA_QUALITY_FLAG**: 5-digit code, digit 4 (long-form DQ) is the key flag for 25%-sample variables. Flag value 0 = good quality.
- **Top suppressed characteristics in 2016**: Income bracket groups ($50K–$59K, etc.) and language-specific variables. Key analytical variables (median income, % spending 30%) are NOT among the most suppressed — they are aggregate measures less likely to be suppressed.

### 2021

- **TNR_SF (Total Non-Response rate, short form)**: Mean for Vancouver CTs = 3.5%. **6 CTs have TNR_SF > 25%**:
  - CT `9330400.08` (TNR 100%, population = 5) — **DATA_QUALITY_FLAG = 9999** — fully suppressed. Only population count is available; everything else is NaN.
  - CTs `9330102.01`, `9330111.06`, `9330280.01`, `9330403.06`, `9330505.03` — moderate suppression (27–81% TNR)
- **SYMBOL column**: Dedicated suppression flag column. `"x"` = suppressed (17,752 rows = 1.3%); `"..."` = not applicable (1,694 rows = 0.1%). Missing C1_COUNT_TOTAL = 1.4%.
- **DATA_QUALITY_FLAG = 9999**: Indicates data has been completely suppressed due to very small CT populations (fewer than ~15 persons at DA level). The CT `9330400.08` with 5 persons is a newly created or institutional-area CT.

### Suppression Rate Summary

| Year | Suppressed cells | % | Primary suppression cause |
|------|-----------------|---|--------------------------|
| 2006 | 0 | 0.0% | None (no suppression codes found) |
| 2011 | 465 (x flag) | ~0.2% | Small CT populations |
| 2016 | ~14,972 | 1.4% | Small CT/income bracket confidentiality |
| 2021 | ~19,451 | 1.4% | Small CT populations, including one fully suppressed CT |

**Key finding**: Suppression rates are low and stable (0–1.4%). The 2006 rate of 0% is suspicious and may reflect conversion artifacts rather than genuine completeness — flag for verification. The 3 high-GNR CTs in 2016 and 6 high-TNR CTs in 2021 all have extremely small populations (< 100 persons) and should be excluded from analysis or treated as unreliable.

---

## 8. Critical Issues and Caveats

### Issue 1: 2011 Has NO Income, Housing Cost, Education, or Immigration Data

**Severity**: HIGH

The 2011 extract (`vancouver_CMA_2011.csv`, sourced from `98-316-XWE2011001-401.CSV`) is the **short-form census profile only**. It contains 472 variables covering population, age, marital status, family structure, household/dwelling type, and language. ALL income/housing/education/immigration variables require the **2011 National Household Survey (NHS)**, product 99-004-XWE2011001, which has NOT been downloaded.

The previous `CENSUS_INVENTORY.md` incorrectly stated the file "Includes NHS data." This is wrong.

**Implication**: For any longitudinal analysis of income, affordability, education, or immigration variables across all 4 waves, 2011 will be a gap. The series will effectively be 3-wave: 2006, 2016, 2021. For population, age, and dwelling type, 2011 is fully available and can extend the series to 4 waves.

**Action for Stage 2**: Either (a) download the 2011 NHS product and integrate it, or (b) design the extraction schema with an explicit 2011 gap for NHS variables, or (c) proceed with 3-wave analysis (2006/2016/2021) and note the gap.

### Issue 2: 2021 Income References 2020 COVID Pandemic Year

**Severity**: HIGH for income comparisons

The 2021 census income data (household-level IDs 242+) uses 2020 as the reference year. CERB and other COVID emergency transfers significantly altered income distributions in 2020. Median household income in 2020 includes government transfer income that is structurally different from employment-driven income in other years.

**Partial mitigation**: Individual-level 2019 income data (pre-COVID) is available in the 2021 file (IDs 204–241) but covers INDIVIDUALS only, not households. There is no pre-COVID household income available in the 2021 CT profile.

**Recommendation**: For any income trend analysis, clearly label 2021 income as "2020 reference year (COVID)." Consider flagging this as a structural break in the time series rather than a comparable data point.

### Issue 3: 2006 Housing Cost Metrics Are Averages, Not Medians

**Severity**: MEDIUM

2006 provides:
- Average gross rent (IDs 2053, 2062)
- Average owner major payments (IDs 2058, 2065)
- Average dwelling value (ID 2057)

2016 and 2021 provide both average AND median for all three. Averages are more sensitive to outliers. In high-cost Vancouver, a few very expensive units can shift averages significantly. **Do not treat 2006 average gross rent as equivalent to 2016/2021 median monthly shelter costs.**

### Issue 4: 2006 Spending 30%+ Is a Count, Not a Rate

**Severity**: MEDIUM

2006 IDs 2054 (renters spending 30%+) and 2059 (owners spending 30%+) are COUNTS of households. A CT with 500 tenant households where 150 spend 30%+ has the same raw count as a CT with 200 households where all 150 spend 30%+ — but very different affordability profiles. The rate must be derived from denominators (IDs 2052 and 2056 respectively).

### Issue 5: 2006 Has No Pre-Calculated Median Age or Population Density

**Severity**: LOW-MEDIUM

Both can be derived:
- Density = ID 2 / ID 4
- Median age = interpolation from 5-year age band counts (IDs 5–43)

Median age interpolation has estimation error of ±0.5–1 year typically. Document this approximation.

### Issue 6: The 2016 Wrong-Directory Risk

**Severity**: HIGH (if overlooked)

`data/raw/census/2016_CT/` contains the Designated Places profile (98-401-X2016007), NOT census tracts. Using this directory would silently return wrong geographic units (small municipalities, not CTs). Always use `2016_CT_correct/` which contains 98-401-X2016043.

### Issue 7: Member ID (Variable ID) Numbers Shift Between Years

**Severity**: MEDIUM

The same concept may have different CHARACTERISTIC_ID values across years:
- "Apartment, 5+ storeys": ID 127 (2006), not separate (2011), ID 43 (2016), ID 47 (2021)
- "Median after-tax household income": IDs 2033/2048 (2006), ID 743 (2016), ID 244 (2021)

**Always extract by matching on CHARACTERISTIC_NAME (case-insensitive, partial match), not by hardcoded ID.** IDs change between census years and are not canonical across waves.

### Issue 8: 2006 VALUE Suppression May Be Hidden

**Severity**: LOW (but worth noting)

The 2006 extract has 0 missing values. The original XML format used codes for suppressed/unavailable values. If these were converted to 0.0 instead of NaN during XML-to-CSV conversion, suppressed cells would appear as valid zeros — which could bias analysis (e.g., a CT where "Median household income" = 0 is unlikely to be real). This needs verification against the original StatCan website for a few sample CTs.

---

## 9. Recommended Variables for Extraction

### Tier 1: Available in All 4 Waves (Use in All Analyses)

| Variable | 2006 extract | 2011 extract | 2016 extract | 2021 extract | Notes |
|----------|-------------|-------------|-------------|-------------|-------|
| Population count | ID 2 | "Population in 2011" | ID 1 | ID 1 | FULL comparability |
| Population density | DERIVED (ID2/ID4) | "Population density per sq km" | ID 6 | ID 6 | 2006 derived |
| Age 25–44 count | DERIVED (sum M+F bands) | Sum bands | Sum IDs 16+17+18+19 | Sum IDs 16+17+18+19 | 2006 sum M+F separately |
| % single-detached dwelling | ID 123 / ID 122 | "Single-detached house" / total | ID 42 / ID 41 | ID 42 / ID 41 | FULL |
| % apartment 5+ storeys | ID 127 / ID 122 | "Apartment 5+ storeys" / total | ID 43 / ID 41 | ID 47 / ID 41 | FULL |
| % apartment <5 storeys | ID 128 / ID 122 | "Apartment <5 storeys" / total | ID 48 / ID 41 | ID 46 / ID 41 | FULL |

### Tier 2: Available in 3 Waves (2006 + 2016 + 2021), Absent in 2011

| Variable | 2006 extract | 2016 extract | 2021 extract | Caveats |
|----------|-------------|-------------|-------------|---------|
| Median household income | ID 2003 (2005$, 20% samp) | ID 742 (2015$, 100%) | ID 243 (2020$, COVID) | Income year varies; 2021 COVID-inflated |
| Median after-tax household income | ID 2033 (2005$, 20% samp) | ID 743 (2015$, 100%) | ID 244 (2020$, COVID) | Same as above |
| Owner households (count) | ID 105 (20% samp) | ID 1618 | ID 1415 | FULL concept |
| Renter households (count) | ID 106 (20% samp) | ID 1619 | ID 1416 | FULL concept |
| % renter spending 30%+ | DERIVED (ID2054/ID2052) | ID 1680 | ID 1492 | 2006 derived |
| % owner spending 30%+ | DERIVED (ID2059/ID2056) | ID 1673 | ID 1484 | 2006 derived |
| % visible minority | ID 1306 / ID 1305 | ID 1324 / ID 1323 | ID 1684 / ID 1683 | FULL concept |
| % immigrants | ID 481 / ID 477 | ID 1142 / ID 1140 | ID 1529 / ID 1527 | FULL concept |
| Unemployment rate | ID 585 (20% samp) | ID 1872 (25% samp) | ID 2230 (25% samp) | FULL concept |
| % bachelor degree or higher (25–64) | DERIVED (sum / ID1251) | ID 1707 / ID 1698 | ID 2024 / ID 2014 | 2006 derived |

### Tier 3: Available in 2 Waves (2016 + 2021 Only) — Best Comparability

These variables have the cleanest comparability: same methodology (long-form census), same metric type (medians), same sample basis (25%). Use these when possible.

| Variable | 2016 ID | 2021 ID |
|----------|---------|---------|
| Median monthly shelter costs — rented | 1681 | 1494 |
| Average monthly shelter costs — rented | 1682 | 1495 |
| Median monthly shelter costs — owned | 1674 | 1486 |
| % with mortgage | 1672 | 1483 |
| Median dwelling value | 1676 | 1488 |
| Average dwelling value | 1677 | 1489 |

### Variables Recommended for EXCLUSION from Extraction

| Variable | Reason |
|----------|--------|
| 2011 income variables | Not in file |
| 2021 household income (ID 243) as primary trend point | COVID year — structural break |
| 2006 average gross rent as substitute for median rent | Average ≠ median in skewed distributions |
| 2006 VALUE = 0 for income variables | Potential suppression-to-zero artifact — verify first |
| CT `9330400.08` (2021) | DATA_QUALITY_FLAG 9999, population = 5, nearly fully suppressed |
| CTs `9330251.01`, `9330251.02`, `9330181.15` (2016) | GNR > 25%, sample data unreliable |

---

## Appendix A: Reading Code Templates

### 2006

```python
import pandas as pd

df06 = pd.read_csv(
    'data/raw/census/2006_CT/vancouver_CMA_2006.csv',
    encoding='latin-1',
    dtype={'GEO_CODE': str, 'CHARACTERISTIC_ID': int},
    low_memory=False
)

# Separate CT from CMA level
df06_ct = df06[df06['GEO_CODE'] != '933'].copy()

# Normalize CTUID for join
def normalize_ctuid(code: str) -> str:
    code = code.split('.')[0]  # remove any float suffix
    return f"{code[:7]}.{code[7:]}"

df06_ct['ct_id'] = df06_ct['GEO_CODE'].apply(normalize_ctuid)
```

### 2011

```python
col_names = ['CTUID', 'Province', 'CMA_name', 'CT_local_code', 'Topic',
             'Characteristic', 'Note_ID', 'Total', 'Total_flag',
             'Male', 'Male_flag', 'Female', 'Female_flag']

df11 = pd.read_csv(
    'data/raw/census/2011_CT/vancouver_CMA_2011.csv',
    encoding='latin-1',
    skiprows=1,          # skip the title row
    names=col_names,
    index_col=False,
    low_memory=False
)

df11['Characteristic'] = df11['Characteristic'].str.strip()

def normalize_ctuid(ctuid: float) -> str:
    s = f"{ctuid:.2f}"   # float → "9330187.11"
    base, dec = s.rsplit('.', 1)
    return f"{base}.{dec.zfill(2)}"

df11['ct_id'] = df11['CTUID'].apply(normalize_ctuid)
```

### 2016

```python
df16 = pd.read_csv(
    'data/raw/census/2016_CT_correct/vancouver_CMA_2016.csv',
    encoding='utf-8-sig',   # handles UTF-8 BOM
    low_memory=False
)

df16_ct = df16[df16['GEO_LEVEL'] == 2].copy()

def normalize_ctuid_16(code) -> str:
    s = str(int(code))   # 933000101
    return f"{s[:7]}.{s[7:]}"

df16_ct['ct_id'] = df16_ct['ALT_GEO_CODE'].apply(normalize_ctuid_16)

# Rename variable columns for clarity
df16_ct = df16_ct.rename(columns={
    'DIM: Profile of Census Tracts (2247)': 'CHARACTERISTIC_NAME',
    'Member ID: Profile of Census Tracts (2247)': 'CHARACTERISTIC_ID',
    'Dim: Sex (3): Member ID: [1]: Total - Sex': 'VALUE'
})
```

### 2021

```python
df21 = pd.read_csv(
    'data/raw/census/2021_CT/vancouver_CMA_2021.csv',
    encoding='latin-1',
    low_memory=False
)

df21_ct = df21[df21['GEO_LEVEL'] == 'Census tract'].copy()
df21_ct['CHARACTERISTIC_NAME'] = df21_ct['CHARACTERISTIC_NAME'].str.strip()

def normalize_ctuid_21(code) -> str:
    s = str(code)
    if '.' in s:
        base, dec = s.rsplit('.', 1)
        return f"{base}.{dec.zfill(2)}"
    return s

df21_ct['ct_id'] = df21_ct['ALT_GEO_CODE'].astype(str).apply(normalize_ctuid_21)
```

---

*Stage 1 complete. Do NOT proceed to variable extraction until this assessment has been reviewed.*
*Stage 2 (extraction) should use the Tier 1/2/3 variable lists above, applying the reading templates and normalization functions.*
*Output file: `data/inventory/CENSUS_QUALITY_ASSESSMENT.md`*
*Generated: 2026-03-03*
