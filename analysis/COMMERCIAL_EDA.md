# Vancouver Commercial Business Licences — EDA Report

**Generated:** 2026-03-03 16:48
**Data span:** FY2013–FY2026
**Source files:** Merged from archive (FY13-23) + current (FY24-26)

---

## 1. Data Quality Summary

**Scoped commercial dataset rows:** 638,646

### Column Completeness

| Column | % Non-null/Non-blank |
|---|---|
| folderyear | 100.0% |
| licencersn | 100.0% |
| licencenumber | 100.0% |
| licencerevisionnumber | 100.0% |
| businessname | 100.0% |
| businesstradename | 48.3% |
| status | 100.0% |
| issueddate | 92.9% |
| expireddate | 92.9% |
| businesstype | 100.0% |
| businesssubtype | 55.9% |
| unit | 30.6% |
| unittype | 30.5% |
| house | 63.4% |
| street | 63.4% |
| city | 100.0% |
| province | 100.0% |
| country | 95.9% |
| postalcode | 63.0% |
| localarea | 25.3% |
| numberofemployees | 100.0% |
| feepaid | 85.0% |
| extractdate | 100.0% |
| geo_point_2d | 60.7% |
| folderyear_4 | 100.0% |

**Notes:**
- `localarea` is blank for FY13-23 (expected — field only populated in current extract, FY24-26)
- `geo_point_2d` has partial coverage (~50%) across all years
- `feepaid` has ~16% missing (structural: Gone Out of Business records often lack fee for closing year)
- `numberofemployees` ~35% missing (self-reported, optional)

---

## 2. Population by Year

Active commercial businesses (Issued + Inactive) per folderyear:

| Year | Active Businesses |
|---|---|
| 2013 | 39,957 |
| 2014 | 38,918 |
| 2015 | 38,786 |
| 2016 | 39,317 |
| 2017 | 39,553 |
| 2018 | 39,382 |
| 2019 | 39,379 |
| 2020 | 36,924 |
| 2021 | 38,527 |
| 2022 | 38,911 |
| 2023 | 40,182 |
| 2024 | 54,624 |
| 2025 | 52,680 |
| 2026 | 49,802 *(mid-cycle)* |

**Notes:**
- FY2024 anomaly resolved: clean data from current extract (56K+ Issued vs poisoned 4K in archive)
- FY2026 is mid-cycle — count will grow as more licences are issued through year-end
- Steady growth 2013→2020, COVID dip, recovery 2022+

---

## 3. localarea Coverage by Folderyear

| Year | % with localarea |
|---|---|
| 2013 | 0.0% |
| 2014 | 0.0% |
| 2015 | 0.0% |
| 2016 | 0.0% |
| 2017 | 0.0% |
| 2018 | 0.0% |
| 2019 | 0.0% |
| 2020 | 0.0% |
| 2021 | 0.0% |
| 2022 | 0.0% |
| 2023 | 0.0% |
| 2024 | 97.4% |
| 2025 | 98.2% |
| 2026 | 100.0% |

**Notes:**
- FY13-23: ~0% (field was blank in archive extract)
- FY24-26: 97-100% (populated in current extract)
- This geographic coverage leap enables neighbourhood-level analysis for recent years
- For FY13-23, spatial analysis requires geocoding from geo_point_2d (51.8% coverage) or postal FSA approximation

---

## 4. geo_point_2d Coverage by Folderyear

| Year | % with geo_point_2d |
|---|---|
| 2013 | 59.1% |
| 2014 | 61.1% |
| 2015 | 60.6% |
| 2016 | 59.3% |
| 2017 | 63.7% |
| 2018 | 64.2% |
| 2019 | 63.8% |
| 2020 | 64.3% |
| 2021 | 64.7% |
| 2022 | 65.6% |
| 2023 | 63.8% |
| 2024 | 54.7% |
| 2025 | 55.9% |
| 2026 | 54.6% |

---

## 5. Business Tracking Statistics

**Unique businesses (panel):** 127,255
**% trackable across 2+ years:** 85.2%
**Median lifespan:** 3 year(s)
**Mean lifespan:** 4.9 years
**P25 / P75 lifespan:** 2 / 7 years
**Max lifespan:** 14 years

**Lifespan distribution (years_active):**

| Years Active | Count | % |
|---|---|---|
| 1 | 18,784 | 14.8% |
| 2 | 20,377 | 16.0% |
| 3 | 26,879 | 21.1% |
| 4 | 13,012 | 10.2% |
| 5 | 8,877 | 7.0% |
| 6 | 6,778 | 5.3% |
| 7 | 5,088 | 4.0% |
| 8 | 4,087 | 3.2% |
| 9 | 3,790 | 3.0% |
| 10 | 3,278 | 2.6% |
| 11 | 3,588 | 2.8% |
| 12 | 1,975 | 1.6% |
| 13 | 2,098 | 1.6% |
| 14 | 8,644 | 6.8% |

---

## 6. Survival Rates (Commercial Only)

KM survival analysis using business panel. Right-censored: businesses with last_year ∈ {25,26} and status = Issued.

| Milestone | Survival Rate |
|---|---|
| 1yr | 87.4% |
| 2yr | 73.0% |
| 3yr | 62.3% |
| 5yr | 46.4% |
| 7yr | 36.4% |
| 10yr | 26.8% |

**Median survival time:** 5 year(s)

**Methodology:**
- Duration = `total_folderyears` (actual count of years with a licence record)
- Event = business exits study (status != Issued in final observed year, OR never reappears)
- Right-censored = last_year ∈ {25,26} AND status_last_year = Issued (still active)
- FY26 is mid-cycle; used as informational only, treated as censored

---

## 7. Top 20 Business Types

| Rank | Business Type | Count |
|---|---|---|
| 1 | Office *Historic* | 100,940 |
| 2 | Long-term Rental | 40,743 |
| 3 | Retail Dealer *Historic* | 34,657 |
| 4 | Contractor *Historic* | 34,478 |
| 5 | Health Services *Historic* | 31,909 |
| 6 | Restaurant Class 1 *Historic* | 21,003 |
| 7 | Ltd Service Food Establishment *Historic* | 16,703 |
| 8 | Health Care Professionals and Services | 16,005 |
| 9 | Contractor - Special Trades *Historic* | 13,673 |
| 10 | Financial Services *Historic* | 13,227 |
| 11 | General Contractor | 13,039 |
| 12 | Computer Services *Historic* | 12,982 |
| 13 | Electrical Contractor *Historic* | 11,987 |
| 14 | Health and Beauty *Historic* | 11,261 |
| 15 | Retail Dealer - Food *Historic* | 11,150 |
| 16 | Wholesale  Dealer *Historic* | 10,494 |
| 17 | Retail Dealer | 7,932 |
| 18 | Consulting and Management Services | 6,062 |
| 19 | Instruction *Historic* | 6,041 |
| 20 | Legal Services | 5,880 |

*Residential types (Single Detached House, Apartment House, etc.) should be absent — exclusions applied correctly.*

---

## 8. Status Distribution by Year

| Year | Issued | Inactive | Gone Out of Business | Total |
|---|---|---|---|---|
| 2013 | 38499 | 1458 | 4740 | 44,697 |
| 2014 | 37563 | 1355 | 4204 | 43,122 |
| 2015 | 37420 | 1366 | 4867 | 43,653 |
| 2016 | 37563 | 1754 | 6176 | 45,493 |
| 2017 | 37904 | 1649 | 3150 | 42,703 |
| 2018 | 38017 | 1365 | 3271 | 42,653 |
| 2019 | 38106 | 1273 | 4022 | 43,401 |
| 2020 | 35620 | 1304 | 3372 | 40,296 |
| 2021 | 36027 | 2500 | 2971 | 41,498 |
| 2022 | 36841 | 2070 | 3337 | 42,248 |
| 2023 | 37700 | 2482 | 4924 | 45,106 |
| 2024 | 53284 | 1340 | 1369 | 55,993 |
| 2025 | 50090 | 2590 | 3034 | 55,714 |
| 2026 | 48458 | 1344 | 2267 | 52,069 |

**Notes:**
- FY2024 should now look normal (Inactive ~2-4% like other years, not 80%)
- Pending and Cancelled excluded from scoped dataset — should show 0 in this table
- Gone Out of Business represents primary death events for survival analysis

---

## 9. Survival by Business Type (Top 6 Commercial)

KM survival rates at 1yr, 3yr, 5yr for top 6 commercial types:

| Business Type | 1yr | 3yr | 5yr |
|---|---|---|---|
| Office *Historic* | 80% | 42% | 22% |
| Long-term Rental | 95% | 88% | 87% |
| Retail Dealer *Historic* | 76% | 38% | 19% |
| Contractor *Historic* | 77% | 34% | 17% |
| Health Services *Historic* | 82% | 45% | 26% |
| Restaurant Class 1 *Historic* | 85% | 50% | 29% |

---

## 10. Geographic Distribution

### By localarea (FY2024-2026, where field is populated)

| Neighbourhood | Business Count |
|---|---|
| Downtown | 39,035 |
| Fairview | 13,647 |
| Kitsilano | 10,738 |
| Out of Town | 10,542 |
| Mount Pleasant | 10,402 |
| West End | 9,075 |
| Kensington-Cedar Cottage | 8,206 |
| Grandview-Woodland | 6,931 |
| Renfrew-Collingwood | 6,704 |
| Sunset | 5,990 |
| Marpole | 5,674 |
| Hastings-Sunrise | 5,132 |
| Strathcona | 5,092 |
| Riley Park | 5,042 |
| Victoria-Fraserview | 3,186 |
| Killarney | 2,903 |
| Dunbar-Southlands | 2,502 |
| Kerrisdale | 2,130 |
| Arbutus-Ridge | 2,106 |
| West Point Grey | 1,906 |

### By Postal FSA (FY2013-2023)

| FSA | Business Licence Records |
|---|---|
| V6B | 38,836 |
| V6C | 24,955 |
| V6E | 24,490 |
| V5Z | 19,478 |
| V6A | 18,256 |
| V6Z | 17,559 |
| V6J | 15,674 |
| V6H | 14,066 |
| V5L | 11,554 |
| V5T | 11,279 |
| V5V | 9,118 |
| V6K | 8,971 |
| V5N | 8,779 |
| V6P | 8,379 |

---

## 11. Fee and Employee Distributions (Commercial Subset)

### Fee Paid (CAD)

| Metric | Value |
|---|---|
| Count (non-null) | 542,568 |
| Missing | 96,078 (15.0%) |
| Mean | $326.80 |
| Median | $165.00 |
| P25 | $139.00 |
| P75 | $268.00 |
| P95 | $934.00 |
| Max | $63722.00 |

### Number of Employees

| Metric | Value |
|---|---|
| Count (non-null) | 638,646 |
| Missing | 0 (0.0%) |
| Mean | 10.1 |
| Median | 2.0 |
| P25 | 1.0 |
| P75 | 5.0 |
| P95 | 30.0 |
| Max | 5876 |

---

## 12. FY2026 Mid-Cycle Caveat

FY2026 currently has **52,069** commercial licence records compared to FY2025's **55,714**.
The FY2026 extract was taken early in the licence year (March 2026 data).

**Implications for analysis:**
- Pending records are excluded (never operated), but Issued count is still growing
- FY2026 Issued = licences already renewed/issued for 2026; more will follow through December
- Gone Out of Business in FY2026 = genuine exits but not yet annualized
- **Treat FY2025 as the reliable endpoint for survival analysis**
- FY2026 is useful for directional signals only; do not extrapolate annual rates from it

For the KM curves in this report, FY2026 records are treated as right-censored (businesses still alive).

---

## 13. Scope Summary

| Stage | Rows |
|---|---|
| Merged FY13-26 raw | 914,856 |
| After scope exclusions | 638,646 |
| Removed | 276,210 (30.2%) |
| Unique commercial businesses (panel) | 127,255 |

**Exclusions applied:**
1. Residential businesstypes (10 types incl. Single Detached House, Apartment House variants, etc.)
2. Short-term Rental Operator
3. Community Association *Historic*
4. Non-Profit Housing *Historic*
5. Admin/temp types (Temp Liquor Amendment, Liquor License Application, Charity, Filming, Christmas Tree, Live-aboards)
6. Status = Pending
7. Status = Cancelled

---

*Report generated by commercial_pipeline.py*
*Date: 2026-03-03*