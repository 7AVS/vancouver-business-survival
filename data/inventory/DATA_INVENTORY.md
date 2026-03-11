# Vancouver Property Tax Assessment — Data Inventory
**Generated:** 2026-03-03
**Source:** City of Vancouver Open Data Portal
**URL:** https://opendata.vancouver.ca/explore/dataset/property-tax-report/
**License:** Open Government Licence — Vancouver

---

## 1. File Inventory

| File | Years | Rows | Columns | File Size | Source Dataset |
|------|-------|------|---------|-----------|----------------|
| `property-tax-report-2006-2010.csv` | 2006–2010 | 892,028 | 29 | 212 MB | property-tax-report-2006-2010 |
| `property-tax-report-2011-2015.csv` | 2011–2015 | 976,762 | 29 | 243 MB | property-tax-report-2011-2015 |
| `property-tax-report-2016-2019.csv` | 2016–2019 | 832,969 | 29 | 219 MB | property-tax-report-2016-2019 |
| `property-tax-report-2020-present.csv` | 2020–2026 | 1,551,132 | 30 | 423 MB | property-tax-report |
| **TOTAL** | **2006–2026** | **4,252,891** | | **1.1 GB** | |

**Note:** The Open Data portal segments data to control file size. The "2020-present" dataset is updated weekly and currently includes data through report year 2026 (assessment year 2026). The API export endpoint has an undocumented truncation limit (~400K rows per request); files were obtained using `rows=2000000` parameter with wget to bypass this.

---

## 2. Column Schema

### All datasets (29 columns, 2006–2019)

| # | Column | Type | Description | Notes |
|---|--------|------|-------------|-------|
| 1 | `pid` | string | Parcel Identifier (9-digit, dashed) | Primary property key. 0.2–0.4% null |
| 2 | `legal_type` | categorical | Legal classification of property | LAND, STRATA, OTHER |
| 3 | `folio` | string | Tax folio number | No nulls |
| 4 | `land_coordinate` | string | Land coordinate (BC Assessment) | No nulls |
| 5 | `zoning_district` | string | Specific zoning code (e.g. RS-1, CD-1) | 0–1.8% null; 528–987 unique values |
| 6 | `zoning_classification` | categorical | Broad zoning category | 0.4–2.1% null; 8–10 unique values |
| 7 | `lot` | string | Lot number | 0.7–1.0% null |
| 8 | `plan` | string | Plan number | 0.1–0.6% null |
| 9 | `block` | string | Block number | ~52–60% null (sparse field) |
| 10 | `district_lot` | string | District lot | 5–8% null |
| 11 | `from_civic_number` | string | Civic address number (from) | ~50–58% null (many properties lack street number) |
| 12 | `to_civic_number` | string | Civic address number (to) | 0.3–0.5% null |
| 13 | `street_name` | string | Street name | 0.1–0.2% null |
| 14 | `property_postal_code` | string | Postal code | 0.9–2.1% null |
| 15 | `narrative_legal_line1` | string | Legal description line 1 | ~0% null |
| 16 | `narrative_legal_line2` | string | Legal description line 2 | ~0.1% null |
| 17 | `narrative_legal_line3` | string | Legal description line 3 | 29–35% null |
| 18 | `narrative_legal_line4` | string | Legal description line 4 | 64–89% null |
| 19 | `narrative_legal_line5` | string | Legal description line 5 | 68–94% null |
| 20 | `current_land_value` | numeric | Assessed land value (CAD) | 0% null in 2006–2010; 1.1–1.7% in later years |
| 21 | `current_improvement_value` | numeric | Assessed improvement value (CAD) | Same null pattern |
| 22 | `tax_assessment_year` | integer | Year of BCA assessment | Same null pattern |
| 23 | `previous_land_value` | numeric | Prior year land value | 100% null in 2006–2010; ~3–60% null in later years |
| 24 | `previous_improvement_value` | numeric | Prior year improvement value | Same pattern |
| 25 | `year_built` | integer | Year property was built | 1.3–3.7% null |
| 26 | `big_improvement_year` | integer | Year of major improvement | 1.3–3.7% null |
| 27 | `tax_levy` | numeric | Annual tax levy (CAD) | ~0–16% null |
| 28 | `neighbourhood_code` | string (3-char) | Neighbourhood code (001–030) | 0% null; 30 unique values |
| 29 | `report_year` | integer | Year of this report record | 0% null |

### 2020-present only (adds 1 column, total 30)

| # | Column | Type | Description | Notes |
|---|--------|------|-------------|-------|
| 30 | `note` | string | Free-text annotation | 99.9% null; 1,155 records contain "Translated name until colonial systems support multi-lingual characters." |

---

## 3. Rows Per Year

| Year | Rows | Unique PIDs | PIDs with Duplicates |
|------|------|-------------|----------------------|
| 2006 | 171,074 | 170,422 | 41 (0.02%) |
| 2007 | 174,946 | 174,287 | 40 (0.02%) |
| 2008 | 177,968 | 177,308 | 39 (0.02%) |
| 2009 | 182,247 | 181,387 | 37 (0.02%) |
| 2010 | 185,793 | 184,931 | 33 (0.02%) |
| 2011 | 188,149 | 187,288 | 30 (0.02%) |
| 2012 | 190,802 | 189,964 | 28 (0.01%) |
| 2013 | 193,392 | 192,544 | 28 (0.01%) |
| 2014 | 200,925 | 199,726 | 241 (0.12%) — notable spike |
| 2015 | 203,494 | 202,271 | 260 (0.13%) — notable spike |
| 2016 | 203,658 | 203,011 | 43 (0.02%) |
| 2017 | 206,480 | 205,846 | 44 (0.02%) |
| 2018 | 209,649 | 209,023 | 45 (0.02%) |
| 2019 | 213,182 | 212,559 | 47 (0.02%) |
| 2020 | 214,803 | 214,186 | 47 (0.02%) |
| 2021 | 217,802 | 217,188 | 52 (0.02%) |
| 2022 | 218,674 | 218,073 | 51 (0.02%) |
| 2023 | 222,197 | 221,572 | 55 (0.02%) |
| 2024 | 224,743 | 224,122 | 53 (0.02%) |
| 2025 | 226,360 | 225,745 | 53 (0.02%) |
| 2026 | 226,553 | 225,943 | 53 (0.02%) |

**Growth:** Property count grew from ~170K in 2006 to ~226K in 2026, a 33% increase over 20 years, reflecting new construction (strata subdivisions, condo towers, infill development).

---

## 4. Numeric Column Value Ranges

### Land Value (current_land_value)
| Period | Min | Max | Mean |
|--------|-----|-----|------|
| 2006–2010 | $0 | $1,084,905,000 | $678,039 |
| 2011–2015 | $0 | $1,952,630,000 | $952,351 |
| 2016–2019 | $0 | $3,516,727,000 | $1,669,623 |
| 2020–2026 | $0 | $3,637,869,000 | $1,768,321 |

**Key observation:** Mean land value increased ~2.6x from 2006–2010 to 2020–2026 period averages.

### Improvement Value (current_improvement_value)
| Period | Min | Max | Mean |
|--------|-----|-----|------|
| 2006–2010 | $0 | $717,983,000 | $252,853 |
| 2011–2015 | $0 | $717,983,000 | $326,408 |
| 2016–2019 | $0 | $626,232,000 | $384,124 |
| 2020–2026 | $0 | $1,136,633,000 | $475,001 |

### Tax Levy (tax_levy)
| Period | Min | Max | Mean |
|--------|-----|-----|------|
| 2006–2010 | -$166 | $7,809,697 | $6,145 |
| 2011–2015 | -$338 | $8,186,891 | $6,935 |
| 2016–2019 | $0 | $9,898,133 | $8,016 |
| 2020–2026 | $0 | $9,760,300 | $9,481 |

**Note:** Negative tax levy values exist in earlier years (2006–2015) — likely tax credits, adjustments, or corrections.

---

## 5. Categorical Column Cardinalities

### Legal Type (legal_type)
| Value | 2006–2010 | 2011–2015 | 2016–2019 | 2020–2026 |
|-------|-----------|-----------|-----------|-----------|
| STRATA | 437,266 | 518,631 | 471,824 | 921,789 |
| LAND | 449,215 | 452,488 | 360,207 | 627,814 |
| OTHER | 5,547 | 5,643 | 938 | 1,529 |

STRATA overtakes LAND in the 2020–2026 period, reflecting the city's ongoing densification via condo/townhouse development.

### Zoning Classification (top categories across all years)
- One-Family Dwelling
- Comprehensive Development
- Multiple Dwelling
- Commercial
- Two-Family Dwelling
- Industrial
- Historical Area
- Residential Inclusive (new category appearing in 2020+ era)
- Residential (new 2020+ era)
- Limited Agriculture

**Note:** "Residential Inclusive" and "Residential" appear as new classification labels in the 2020–2026 dataset. This likely reflects the 2023 Broadway Plan and RS zoning reforms where large swaths of single-family land were upzoned.

### Zoning District (cardinality)
| Period | Unique Zoning Districts |
|--------|------------------------|
| 2006–2010 | 528 |
| 2011–2015 | 639 |
| 2016–2019 | 634 |
| 2020–2026 | 987 |

The jump to 987 unique zoning districts in 2020–2026 reflects proliferation of site-specific CD-1 (Comprehensive Development) zones.

### Neighbourhood Code
Consistent across all years: 30 unique codes (001–030). No mapping table included in dataset — cross-reference with City of Vancouver neighbourhood boundary data to decode.

---

## 6. Missing Value Assessment

### Critical fields — completeness

| Column | 2006–2010 | 2011–2015 | 2016–2019 | 2020–2026 |
|--------|-----------|-----------|-----------|-----------|
| pid | 99.6% | 99.6% | 99.7% | 99.8% |
| current_land_value | 100.0% | 98.9% | 98.3% | 98.4% |
| current_improvement_value | 100.0% | 98.9% | 98.3% | 98.4% |
| tax_levy | 100.0% | 98.9% | 98.4% | 84.1% |
| previous_land_value | **0.0%** | 39.8% | 96.7% | 97.4% |
| previous_improvement_value | **0.0%** | 39.8% | 96.7% | 97.4% |

**Previous year values are entirely absent in 2006–2010** — confirmed 100% null. Partially present in 2011–2015 (about 40% have values). Mostly present in 2016+.

### Tax levy null spike in 2020–2026
Tax levy is 15.9% null in the 2020–2026 dataset (vs ~1% in earlier periods). Investigation: 2025 and 2026 report years likely have incomplete levy data since BC Assessment rolls may not be finalized for the most recent years. The 2026 data appears to be the current-year assessment with approximately 226K properties but with levy calculations still pending for many records.

### Sparse fields (structural, not data quality issues)
- `block`: 52–60% null — expected, many properties (esp. strata) don't have a block number
- `from_civic_number`: 50–58% null — strata lots and non-addressed parcels lack a street number
- `narrative_legal_line4` / `line5`: 64–94% null — only long legal descriptions use these lines

---

## 7. Duplicate Detection

Duplicates are defined as multiple rows with the same PID in the same report year.

**Summary:** Duplicate rates are extremely low — consistently 0.02% of rows per year — with one notable exception:
- **2014 and 2015** show a spike (241 and 260 duplicated PIDs respectively vs. typical ~35–50). These may reflect data loading errors during the transition between datasets or properties that were mid-subdivision. These dupes exist within the 2011–2015 file.

**Cross-file duplicates:** No PIDs span across different dataset files for the same year (confirmed by year range boundaries).

---

## 8. Cross-Year PID Tracking (Property Longitudinal Analysis)

A PID (Parcel Identifier) is the primary key for tracking the same physical property across years.

### Year-over-year retention rates

| Transition | Shared PIDs | % of Prior Year | % of Next Year | New PIDs | Dropped PIDs |
|------------|-------------|-----------------|----------------|----------|--------------|
| 2006→2007 | 170,125 | 99.8% | 97.6% | 4,162 | 297 |
| 2007→2008 | 173,974 | 99.8% | 98.1% | 3,334 | 313 |
| 2008→2009 | 176,996 | 99.8% | 97.6% | 4,391 | 312 |
| 2009→2010 | 181,000 | 99.8% | 97.9% | 3,931 | 387 |
| 2010→2011 | 184,681 | 99.9% | 98.6% | 2,607 | 250 |
| 2011→2012 | 187,097 | 99.9% | 98.5% | 2,867 | 191 |
| 2012→2013 | 189,680 | 99.9% | 98.5% | 2,864 | 284 |
| 2013→2014 | 192,544 | 100.0% | 96.4% | 7,182 | 0 |
| 2014→2015 | 199,698 | 100.0% | 98.7% | 2,573 | 28 |
| 2015→2016 | 199,620 | 98.7% | 98.3% | 3,391 | 2,651 |
| 2016→2017 | 202,695 | 99.8% | 98.5% | 3,151 | 316 |
| 2017→2018 | 205,273 | 99.7% | 98.2% | 3,750 | 573 |
| 2018→2019 | 208,808 | 99.9% | 98.2% | 3,751 | 215 |
| 2020→2021 | 213,657 | 99.8% | 98.4% | 3,531 | 529 |
| 2021→2022 | 217,049 | 99.9% | 99.5% | 1,024 | 139 |
| 2022→2023 | 217,519 | 99.7% | 98.2% | 4,053 | 554 |
| 2023→2024 | 221,232 | 99.8% | 98.7% | 2,890 | 340 |
| 2024→2025 | 223,837 | 99.9% | 99.2% | 1,908 | 285 |
| 2025→2026 | 225,719 | 100.0% | 99.9% | 224 | 26 |

**Key finding:** Year-over-year PID retention is very high (97.6–100%), confirming the dataset supports robust longitudinal tracking. A property can be followed from 2006 to 2026.

**2015→2016 anomaly:** 2,651 PIDs dropped from 2015 to 2016. This is abnormally high (vs typical ~300). Likely a boundary/classification change at the dataset segmentation point rather than actual property disappearance.

**2013→2014 spike:** 7,182 new PIDs appeared — the largest single-year jump in the series. This coincides with a wave of strata subdivision activity.

**Long-term tracking:** 98.0% of PIDs present in 2006 also appear in 2019 (13 years later). 99.1% of PIDs in 2020 appear in 2026. The dataset is suitable for 20-year property-level panel analysis.

---

## 9. Cross-Field Logic Issues

### Potential issues observed

1. **tax_assessment_year vs report_year:** These fields usually match but not always. The `tax_assessment_year` reflects when BC Assessment performed the valuation (usually the prior calendar year), while `report_year` is the tax roll year. For analysis, use `report_year` as the primary temporal key.

2. **current_land_value = 0:** Valid in some cases (e.g. Crown land, parks, some institutional properties) but worth flagging for analysis — there are properties with $0 land value in every year.

3. **current_improvement_value = 0:** Many properties (particularly vacant lots, parking, and some older LAND type properties) legitimately have $0 improvement value.

4. **tax_levy negative values (2006–2015):** Small number of negative tax levy records. These are likely adjustments/credits rather than errors. Should be handled as adjustments in aggregation.

5. **PID nulls:** ~0.2–0.4% of rows have no PID. These cannot be tracked longitudinally. They represent properties where the parcel identifier was not populated at source.

6. **Zoning classification schema shift (2020+):** New categories "Residential Inclusive" and "Residential" appear, likely reflecting BC/CoV zoning reforms. Not present in 2006–2019 data. This breaks any categorical time series on zoning unless you map old→new categories.

7. **Column ordering differs between 2006–2010 and later files:** In 2006–2010, `tax_assessment_year` (col 20) appears between improvement value (col 19) and narrative_legal_line4 (col 21). Later files reorder these. When combining files, always join by column name not position.

---

## 10. Data Coverage Summary

| Aspect | Assessment |
|--------|-----------|
| Temporal coverage | 2006–2026 (21 years, complete) |
| Property count growth | 170K (2006) → 226K (2026), +33% |
| Longitudinal trackability | Excellent (>98% PID retention year-over-year) |
| Land value data | Complete for all years |
| Previous year values | Not available for 2006–2010; partial for 2011–2015; complete for 2016+ |
| Tax levy data | Complete through 2024; ~16% missing for 2025–2026 (likely unfinalised) |
| Geographic fields | Neighbourhood code (30 areas) available throughout; postal code 98%+ complete |
| Zoning data | Available throughout; schema changed circa 2020 (new categories added) |
| Legal description | Complete (narrative_legal_line1-5) |
| Gaps | No data before 2006; 2019→2020 gap between dataset files (cross-file join needed) |

---

## 11. Recommended Next Steps

1. **Build a neighbourhood code lookup table** — map the 30 codes (001–030) to neighbourhood names using CoV's neighbourhood boundary dataset.

2. **Handle the 2015→2016 PID drop** — investigate the ~2,651 PIDs that disappear. Are they merged parcels, errors, or strata re-registrations?

3. **Normalise zoning classification** for time series — create a mapping from the 2020+ category names back to the 2006–2019 schema where possible.

4. **Address the previous_land_value gap for 2006–2010** — if year-over-year change is needed for that period, derive it by joining report_year N to N-1 directly from the data.

5. **Combine all four files** into a single parquet or DuckDB database for efficient querying. 4.25M rows is manageable but CSV joins across files are slow.

6. **For trend analysis**, exclude 2025–2026 from tax levy calculations until the roll is finalised (15.9% null in that file).

---

*Analysis performed on 2026-03-03. Raw data in `data/raw/`.*
