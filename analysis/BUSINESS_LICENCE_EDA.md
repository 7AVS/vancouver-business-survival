# Vancouver Business Licence — Data Quality & EDA Report

**Data**: City of Vancouver Business Licences 2013–2024  

**Script**: `biz_licence_eda.py`  

**Generated**: 2026-03-03


## LOADING DATA

File: /home/aurora/projects/sites/portfolio-projects/van-property-tax/data/raw/business-licences/business-licences-2013-to-2024.csv
Loaded 779,226 rows x 25 columns
Columns: ['folderyear', 'licencersn', 'licencenumber', 'licencerevisionnumber', 'businessname', 'businesstradename', 'status', 'issueddate', 'expireddate', 'businesstype', 'businesssubtype', 'unit', 'unittype', 'house', 'street', 'city', 'province', 'country', 'postalcode', 'localarea', 'numberofemployees', 'feepaid', 'extractdate', 'geom', 'geo_point_2d']

**Rows**: 779,226  
**Columns**: 25  


## PHASE 2 — DATA QUALITY ASSESSMENT


### 2.1 Column Completeness


--- 2.1 COLUMN COMPLETENESS TABLE ---

**Column Completeness Table:**

| column                |   null_count | null_pct   |   unique_count |
|:----------------------|-------------:|:-----------|---------------:|
| folderyear            |            0 | 0.0%       |             12 |
| licencersn            |            0 | 0.0%       |         779023 |
| licencenumber         |            0 | 0.0%       |         758597 |
| licencerevisionnumber |            0 | 0.0%       |              6 |
| businessname          |        33421 | 4.3%       |         111853 |
| businesstradename     |       470467 | 60.4%      |          46636 |
| status                |            0 | 0.0%       |              5 |
| issueddate            |       131662 | 16.9%      |         546430 |
| expireddate           |       131979 | 16.9%      |           1762 |
| businesstype          |            0 | 0.0%       |            181 |
| businesssubtype       |       364049 | 46.7%      |            356 |
| unit                  |       583075 | 74.8%      |           2553 |
| unittype              |       583353 | 74.9%      |             41 |
| house                 |       359906 | 46.2%      |           5671 |
| street                |       359863 | 46.2%      |           1481 |
| city                  |         1046 | 0.1%       |            547 |
| province              |         1117 | 0.1%       |             75 |
| country               |        36778 | 4.7%       |              1 |
| postalcode            |       364926 | 46.8%      |           6939 |
| localarea             |       779226 | 100.0%     |              0 |
| numberofemployees     |            0 | 0.0%       |            464 |
| feepaid               |       124826 | 16.0%      |           6360 |
| extractdate           |            0 | 0.0%       |             50 |
| geom                  |       375616 | 48.2%      |           9061 |
| geo_point_2d          |       375616 | 48.2%      |           9061 |

### 2.2 geo_point_2d Coverage


--- 2.2 GEO_POINT_2D COVERAGE ---
Overall geo_point_2d coverage: 403,610 / 779,226 = 51.8%
Validating geo format and bounding box (Vancouver)...
Valid geo coordinates: 403,610 / 779,226 = 51.8%

Geo coverage by folderyear:

**geo_point_2d Coverage by Year:**

|   folderyear |   total |   has_geo |   coverage_pct |
|-------------:|--------:|----------:|---------------:|
|           13 |   60913 |     32217 |           52.9 |
|           14 |   60579 |     32319 |           53.4 |
|           15 |   60937 |     32687 |           53.6 |
|           16 |   61393 |     33575 |           54.7 |
|           17 |   60059 |     34173 |           56.9 |
|           18 |   66176 |     35877 |           54.2 |
|           19 |   70772 |     36865 |           52.1 |
|           20 |   69299 |     33164 |           47.9 |
|           21 |   68387 |     33962 |           49.7 |
|           22 |   68423 |     34303 |           50.1 |
|           23 |   69793 |     34372 |           49.2 |
|           24 |   62495 |     30096 |           48.2 |

Overall: 51.8% of rows have valid Vancouver coordinates

### 2.3 Business Tracking Feasibility (name+address)


--- 2.3 BUSINESS TRACKING FEASIBILITY ---
Building tracking key from businessname + house + street...
Rows with at least name or address data: 745,810 / 779,226 = 95.7%
Rows with complete (name+house+street): 419,315 / 779,226 = 53.8%

Unique (businessname, house, street) combinations: 131,871
Unique business-addresses appearing in 1 folderyear only: 18,656 (14.1%)
Unique business-addresses appearing in 2+ folderyears: 113,214 (85.9%)

Lifespan distribution (number of folderyears a business-address appears):
  1 year(s): 18,656 businesses (14.1%)
  2 year(s): 20,051 businesses (15.2%)
  3 year(s): 16,752 businesses (12.7%)
  4 year(s): 15,290 businesses (11.6%)
  5 year(s): 12,002 businesses (9.1%)
  6 year(s): 7,908 businesses (6.0%)
  7 year(s): 7,153 businesses (5.4%)
  8 year(s): 5,600 businesses (4.2%)
  9 year(s): 4,464 businesses (3.4%)
  10 year(s): 3,694 businesses (2.8%)
  11 year(s): 3,532 businesses (2.7%)
  12 year(s): 16,768 businesses (12.7%)

Building business panel (vectorized)...
Business panel: 131,870 unique business-addresses
Panel saved to: /home/aurora/projects/sites/portfolio-projects/van-property-tax/data/business_panel.csv

Survival rate estimates from panel:
Cohort (started <= 2023): 128,868 businesses
  1-year survival: 100.0% (n=128,868 eligible cohort)
  2-year survival: 87.9% (n=128,868 eligible cohort)
  3-year survival: 76.6% (n=121,836 eligible cohort)
  5-year survival: 56.7% (n=108,378 eligible cohort)
  7-year survival: 44.9% (n=92,714 eligible cohort)
  10-year survival: 35.1% (n=69,617 eligible cohort)
Median lifespan: 4.0 years

**Panel Summary:**

- Total unique business-addresses tracked: 131,870
- Businesses tracked across 2+ years: 113,214
- Median lifespan: 4.0 years

### 2.4 businesstype Analysis


--- 2.4 BUSINESSTYPE ANALYSIS ---
Total unique businesstype values: 181

Top 30 business types (all years):

**Top 30 Business Types (all years):**

| businesstype                              |   count |   pct |
|:------------------------------------------|--------:|------:|
| Office *Historic*                         |  120826 |  15.5 |
| Contractor *Historic*                     |   45224 |   5.8 |
| Retail Dealer *Historic*                  |   41383 |   5.3 |
| Health Services *Historic*                |   38318 |   4.9 |
| Single Detached House *Historic*          |   36642 |   4.7 |
| Short-term Rental Operator                |   32452 |   4.2 |
| Apartment House Strata *Historic*         |   30082 |   3.9 |
| Apartment House *Historic*                |   29787 |   3.8 |
| Secondary Suite - Permanent *Historic*    |   27298 |   3.5 |
| Restaurant Class 1 *Historic*             |   24213 |   3.1 |
| Ltd Service Food Establishment *Historic* |   19406 |   2.5 |
| Contractor - Special Trades *Historic*    |   17856 |   2.3 |
| Computer Services *Historic*              |   16313 |   2.1 |
| Financial Services *Historic*             |   15601 |   2   |
| Electrical Contractor *Historic*          |   15507 |   2   |
| Health and Beauty *Historic*              |   13340 |   1.7 |
| Retail Dealer - Food *Historic*           |   13034 |   1.7 |
| Wholesale  Dealer *Historic*              |   12681 |   1.6 |
| Multiple Dwelling *Historic*              |   12676 |   1.6 |
| Duplex *Historic*                         |   10273 |   1.3 |
| Community Association *Historic*          |    8618 |   1.1 |
| Instruction *Historic*                    |    7736 |   1   |
| Janitorial Services *Historic*            |    7281 |   0.9 |
| Massage Therapist *Historic*              |    6837 |   0.9 |
| Plumber & Gas Contractor *Historic*       |    6829 |   0.9 |
| Landscape Gardener *Historic*             |    6282 |   0.8 |
| Manufacturer *Historic*                   |    5885 |   0.8 |
| Personal Services *Historic*              |    5485 |   0.7 |
| Repair/ Service/Maintenance *Historic*    |    5379 |   0.7 |
| Production Company *Historic*             |    5214 |   0.7 |

Schema break analysis: folderyear <= 23 vs folderyear = 24
Unique types in folderyear <= 23: 181
Unique types in folderyear = 24: 172
Types in both: 172
Types ONLY in pre-2024: 9
Types ONLY in folderyear 24: 0

Sample types only in pre-2024 (first 20): ['Auto Wrecker *Historic*', 'Chimney Sweep *Historic*', 'Christmas Tree Lot *Historic*', 'Exotic Dancers *Historic*', 'Late Night Dance Event *Historic*', 'Peddler *Historic*', 'Specialized Services *Historic*', 'Transient Trader/Peddler-W *Historic*', 'Vending Machines *Historic*']

Sample types only in folderyear 24 (first 20): []

**Schema Break Summary:**

- Pre-2024 unique types: 181
- 2024 unique types: 172
- Types only in pre-2024: 9
- Types only in 2024: 0
- Types present in both: 172

### 2.5 status Field


--- 2.5 STATUS FIELD ---
Status distribution:

**Status Distribution:**

| status               |   count |   pct |
|:---------------------|--------:|------:|
| Issued               |  566994 |  72.8 |
| Inactive             |   70255 |   9   |
| Gone Out of Business |   62191 |   8   |
| Pending              |   58171 |   7.5 |
| Cancelled            |   21615 |   2.8 |

### 2.6 Date Fields


--- 2.6 DATE FIELDS ---

issueddate: 647,564 populated (83.1%), 131,662 null (16.9%)
  Parseable dates: 647,564 (83.1%)
  Min: 2012-11-16 17:08:35+00:00
  Max: 2025-03-05 22:26:44+00:00
  Future dates (>2025): 0
  Far past dates (<2000): 0

expireddate: 647,247 populated (83.1%), 131,979 null (16.9%)
  Parseable dates: 647,247 (83.1%)
  Min: 2013-01-13 00:00:00
  Max: 2024-12-31 00:00:00
  Future dates (>2025): 0
  Far past dates (<2000): 0

**issueddate by folderyear (issued month distribution for Seasonal):**
Month distribution of issueddate:

**Monthly Issue Distribution:**

| month_name   |   count |
|:-------------|--------:|
| January      |   96275 |
| February     |   49123 |
| March        |   22079 |
| April        |   13961 |
| May          |   12054 |
| June         |   10833 |
| July         |    9078 |
| August       |    9118 |
| September    |    8750 |
| October      |   10244 |
| November     |  139979 |
| December     |  266070 |

Expireddate month distribution:

**Monthly Expiry Distribution:**

| month_name   |   count |
|:-------------|--------:|
| January      |      93 |
| February     |     167 |
| March        |     215 |
| April        |     243 |
| May          |     256 |
| June         |     446 |
| July         |     404 |
| August       |     382 |
| September    |     372 |
| October      |     594 |
| November     |     249 |
| December     |  643826 |

### 2.7 Geographic Coverage


--- 2.7 GEOGRAPHIC COVERAGE ---
localarea: 0 populated (0.0%) — confirmed 100% null: True
postalcode: 414,300 populated (53.2%)
Rows with valid Vancouver FSA (V##): 414,115 (53.1%)

Top 20 FSAs (proxy for local area):

**Top 20 FSAs:**

| fsa   |   count |   pct |
|:------|--------:|------:|
| V6B   |   50304 |   6.5 |
| V6E   |   33379 |   4.3 |
| V6C   |   29818 |   3.8 |
| V6A   |   24511 |   3.1 |
| V5Z   |   24311 |   3.1 |
| V6Z   |   22810 |   2.9 |
| V6J   |   21920 |   2.8 |
| V6H   |   20495 |   2.6 |
| V5T   |   17198 |   2.2 |
| V5L   |   16944 |   2.2 |
| V6K   |   13960 |   1.8 |
| V6P   |   12829 |   1.6 |
| V6G   |   12574 |   1.6 |
| V5N   |   12554 |   1.6 |
| V5V   |   12121 |   1.6 |
| V5Y   |   11156 |   1.4 |
| V5X   |   10170 |   1.3 |
| V5R   |    9146 |   1.2 |
| V6M   |    8317 |   1.1 |
| V5P   |    7046 |   0.9 |

## PHASE 3 — EXPLORATORY DATA ANALYSIS


### 3.1 Business Population Over Time


--- 3.1 BUSINESS POPULATION OVER TIME ---

**Total Records by Folderyear:**

|   folderyear |   total_records |
|-------------:|----------------:|
|           13 |           60913 |
|           14 |           60579 |
|           15 |           60937 |
|           16 |           61393 |
|           17 |           60059 |
|           18 |           66176 |
|           19 |           70772 |
|           20 |           69299 |
|           21 |           68387 |
|           22 |           68423 |
|           23 |           69793 |
|           24 |           62495 |

Active (Issued) records by year:

**Active (Issued) by Folderyear:**

|   folderyear |   active_issued |
|-------------:|----------------:|
|           13 |           49661 |
|           14 |           48539 |
|           15 |           48133 |
|           16 |           48484 |
|           17 |           48795 |
|           18 |           53566 |
|           19 |           55512 |
|           20 |           51649 |
|           21 |           51412 |
|           22 |           52639 |
|           23 |           54535 |
|           24 |            4069 |

Status breakdown by year:

**Status Breakdown by Folderyear:**

|   folderyear |   Cancelled |   Gone Out of Business |   Inactive |   Issued |   Pending |
|-------------:|------------:|-----------------------:|-----------:|---------:|----------:|
|           13 |         841 |                   5329 |       1522 |    49661 |      3560 |
|           14 |         745 |                   4751 |       1416 |    48539 |      5128 |
|           15 |         858 |                   5481 |       1442 |    48133 |      5023 |
|           16 |         918 |                   6936 |       1825 |    48484 |      3230 |
|           17 |        1420 |                   3669 |       1722 |    48795 |      4453 |
|           18 |        1165 |                   3809 |       1461 |    53566 |      6175 |
|           19 |        1625 |                   5481 |       1395 |    55512 |      6759 |
|           20 |        4209 |                   5005 |       1496 |    51649 |      6940 |
|           21 |        3271 |                   4413 |       2749 |    51412 |      6542 |
|           22 |        2708 |                   4869 |       2334 |    52639 |      5873 |
|           23 |        2176 |                   6297 |       2810 |    54535 |      3975 |
|           24 |        1679 |                   6151 |      50083 |     4069 |       513 |

### 3.2 Business Type Concentration


--- 3.2 BUSINESS TYPE CONCENTRATION ---
Top 10 business types (all years):

**Top 10 Business Types:**

| businesstype                           |   count |   pct |
|:---------------------------------------|--------:|------:|
| Office *Historic*                      |  120826 |  15.5 |
| Contractor *Historic*                  |   45224 |   5.8 |
| Retail Dealer *Historic*               |   41383 |   5.3 |
| Health Services *Historic*             |   38318 |   4.9 |
| Single Detached House *Historic*       |   36642 |   4.7 |
| Short-term Rental Operator             |   32452 |   4.2 |
| Apartment House Strata *Historic*      |   30082 |   3.9 |
| Apartment House *Historic*             |   29787 |   3.8 |
| Secondary Suite - Permanent *Historic* |   27298 |   3.5 |
| Restaurant Class 1 *Historic*          |   24213 |   3.1 |

Tracking top types across years (pre-2024 only for consistency):

### 3.3 Geographic Concentration by FSA


--- 3.3 GEOGRAPHIC CONCENTRATION BY FSA ---
Top 10 FSA trend over years:

**Top FSAs Over Time:**

|   folderyear |   V6B |   V6E |   V6C |   V6A |   V5Z |   V6Z |   V6J |   V6H |   V5T |   V5L |
|-------------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|------:|
|           13 |  3849 |  2765 |  2484 |  2025 |  2004 |  1987 |  1816 |  1659 |  1428 |  1312 |
|           14 |  3932 |  2627 |  2392 |  2043 |  2001 |  1953 |  1837 |  1625 |  1419 |  1341 |
|           15 |  3994 |  2644 |  2408 |  2078 |  2041 |  1886 |  1862 |  1612 |  1402 |  1368 |
|           16 |  4089 |  2782 |  2404 |  2146 |  2059 |  1838 |  1822 |  1779 |  1410 |  1395 |
|           17 |  4228 |  2902 |  2473 |  2113 |  2078 |  1890 |  1817 |  1704 |  1443 |  1392 |
|           18 |  4612 |  3248 |  2518 |  2135 |  2166 |  2127 |  1884 |  1749 |  1469 |  1417 |
|           19 |  4873 |  3259 |  2597 |  2162 |  2255 |  2229 |  1909 |  1787 |  1516 |  1479 |
|           20 |  4129 |  2614 |  2487 |  1992 |  2005 |  1759 |  1777 |  1725 |  1368 |  1434 |
|           21 |  4173 |  2638 |  2539 |  2068 |  2002 |  1788 |  1806 |  1755 |  1403 |  1487 |
|           22 |  4328 |  2621 |  2563 |  2069 |  1908 |  1800 |  1807 |  1737 |  1472 |  1498 |
|           23 |  4347 |  2726 |  2650 |  1951 |  1963 |  1869 |  1867 |  1774 |  1501 |  1499 |
|           24 |  3750 |  2553 |  2303 |  1729 |  1829 |  1684 |  1716 |  1589 |  1367 |  1322 |

### 3.4 Survival Analysis from Panel


--- 3.4 SURVIVAL ANALYSIS ---
Panel size: 131,870 unique business-addresses

Lifespan distribution (years):
  1 year(s): 18,656 (14.1%)
  2 year(s): 19,867 (15.1%)
  3 year(s): 16,664 (12.6%)
  4 year(s): 15,253 (11.6%)
  5 year(s): 11,946 (9.1%)
  6 year(s): 7,883 (6.0%)
  7 year(s): 7,114 (5.4%)
  8 year(s): 5,608 (4.3%)
  9 year(s): 4,440 (3.4%)
  10 year(s): 3,678 (2.8%)
  11 year(s): 3,594 (2.7%)
  12 year(s): 17,167 (13.0%)

Cohort survival table (year of first appearance vs lifespan):

**Cohort Survival Summary:**

|   cohort_year |     n |   mean_lifespan |   median_lifespan |
|--------------:|------:|----------------:|------------------:|
|          2013 | 56239 |         6.85587 |                 6 |
|          2014 |  6722 |         5.81003 |                 5 |
|          2015 |  6656 |         5.62936 |                 5 |
|          2016 |  7155 |         5.33473 |                 5 |
|          2017 |  7238 |         5.08193 |                 5 |
|          2018 |  8704 |         4.33019 |                 4 |
|          2019 |  7343 |         4.07817 |                 5 |
|          2020 |  8321 |         4.00168 |                 5 |
|          2021 |  6985 |         3.2378  |                 4 |
|          2022 |  6473 |         2.59679 |                 3 |
|          2023 |  7032 |         1.84258 |                 2 |
|          2024 |  3002 |         1       |                 1 |

Median lifespan by top business types:

**Median Lifespan by Business Type (n>=100):**

| businesstype                                      |   count |   median_lifespan |
|:--------------------------------------------------|--------:|------------------:|
| Apartment House *Historic*                        |    3374 |              11   |
| Multiple Dwelling *Historic*                      |    1306 |              10   |
| Financial Institution *Historic*                  |     283 |              10   |
| Duplex *Historic*                                 |    1124 |               9   |
| Equipment Operator *Historic*                     |     100 |               9   |
| Liquor Retail Store *Historic*                    |     139 |               8   |
| Residential/Commercial *Historic*                 |     370 |               8   |
| Non-profit Housing *Historic*                     |     425 |               7   |
| Secondary Suite - Permanent *Historic*            |    3641 |               7   |
| Hotel or Motel                                    |     113 |               7   |
| Single Detached House *Historic*                  |    4190 |               7   |
| Auto Repairs *Historic*                           |     435 |               6   |
| Liquor Establishment Extended  *Historic*         |     168 |               6   |
| Retail Dealer - Grocery *Historic*                |     146 |               6   |
| Auto Parking Lot/Parkade *Historic*               |     669 |               6   |
| Electrical-Security Alarm Installation *Historic* |     342 |               6   |
| Sprinkler Contractor *Historic*                   |     154 |               5.5 |
| Dry Cleaner *Historic*                            |     122 |               5.5 |
| Manufacturer *Historic*                           |    1020 |               5   |
| Financial Services *Historic*                     |    2744 |               5   |

Median lifespan by FSA (top FSAs, n>=100):

**Median Lifespan by FSA:**

| fsa   |   count |   median_lifespan |
|:------|--------:|------------------:|
| V5Z   |    4162 |                 5 |
| V7Y   |    1046 |                 5 |
| V6M   |    1349 |                 5 |
| V6N   |     274 |                 5 |
| V6H   |    3222 |                 5 |
| V6K   |    2306 |                 5 |
| V7X   |     926 |                 5 |
| V5S   |     392 |                 4 |
| V5R   |    1656 |                 4 |
| V5K   |    1014 |                 4 |
| V5M   |     953 |                 4 |
| V5N   |    2073 |                 4 |
| V5P   |    1252 |                 4 |
| V5L   |    2949 |                 4 |
| V6A   |    4428 |                 4 |
| V5Y   |    2108 |                 4 |
| V5X   |    1829 |                 4 |
| V5W   |     857 |                 4 |
| V5T   |    3019 |                 4 |
| V5V   |    2093 |                 4 |

### 3.5 Fee (feepaid) Analysis


--- 3.5 FEE ANALYSIS ---
feepaid populated: 654,400 (84.0%)
Min: -1624.5
Max: 63281.0
Mean: 336.50
Median: 155.00

Median fee by top business types:

**Median Fee by Business Type (top 20):**

| businesstype                                    |   count |   median_fee |   mean_fee |
|:------------------------------------------------|--------:|-------------:|-----------:|
| Retail Dealer - Market Outlet *Historic*        |     126 |       4479   |   4491.73  |
| Hotel or Motel                                  |    1304 |       3513.5 |   5544.18  |
| Liquor Establishment Extended  *Historic*       |    1379 |       2421   |   3056.44  |
| Restaurant Class 2 *Historic*                   |     256 |       2284   |   2523.52  |
| Live-aboards *Historic*                         |    1047 |       2192   |   2334.16  |
| Personal Care Home *Historic*                   |     213 |       1620   |   2224.1   |
| Financial Institution *Historic*                |    2428 |       1535   |   1506.32  |
| Restaurant Class 1 *Historic*                   |   22145 |       1145   |   1324.9   |
| Apartment House *Historic*                      |   28076 |       1056   |   1899.35  |
| Manufacturer - Food with Anc. Retail *Historic* |     288 |        952   |    890.351 |
| Retail Dealer - Grocery *Historic*              |     822 |        919   |    865.831 |
| Manufacturer - Food *Historic*                  |    2425 |        770   |    722.343 |
| Rooming House *Historic*                        |     238 |        625.5 |    859.891 |
| Liquor Establishment Standard *Historic*        |    1298 |        575   |    749.187 |
| Ltd Service Food Establishment *Historic*       |   17457 |        525   |    510.66  |
| Venue *Historic*                                |     350 |        482   |    470.734 |
| Liquor Retail Store *Historic*                  |    1184 |        418   |    405.322 |
| Laundry-Coin Operated Services *Historic*       |     519 |        397   |    388.94  |
| Wholesale Dealer - Food *Historic*              |    2248 |        388   |    381.872 |
| Caterer                                         |    1803 |        387   |    354.539 |

Median fee by year:

**Median Fee by Year:**

|   folderyear |   median_fee |
|-------------:|-------------:|
|           13 |          129 |
|           14 |          130 |
|           15 |          133 |
|           16 |          136 |
|           17 |          139 |
|           18 |          145 |
|           19 |          151 |
|           20 |          155 |
|           21 |          155 |
|           22 |          163 |
|           23 |          171 |
|           24 |          250 |

### 3.6 Employee Count Analysis


--- 3.6 EMPLOYEE COUNT ---
numberofemployees populated: 779,226 (100.0%)
Min: 0.0
Max: 5876.0
Mean: 7.28
Median: 1.00

Employee count buckets:
  0 employees: 148,551 (19.1%)
  1 employees: 71,998 (9.2%)
  2-5 employees: 97,244 (12.5%)
  6-10 employees: 63,974 (8.2%)
  11-20 employees: 36,372 (4.7%)
  21-50 employees: 24,419 (3.1%)
  51-100 employees: 8,910 (1.1%)
  101-500 employees: 7,022 (0.9%)
  500+ employees: 1,100 (0.1%)

**Employee Count Distribution:**

| bucket   |   count |
|:---------|--------:|
| 0        |  148551 |
| 1        |   71998 |
| 2-5      |   97244 |
| 6-10     |   63974 |
| 11-20    |   36372 |
| 21-50    |   24419 |
| 51-100   |    8910 |
| 101-500  |    7022 |
| 500+     |    1100 |

### 3.7 Seasonal Patterns


--- 3.7 SEASONAL PATTERNS ---
Already computed above in 2.6. Key summary:
Most common issueddate month: 12.0 (December)
Most common expireddate month: 12.0 (December)

## SUMMARY & KEY FINDINGS

## Data Quality Summary

| Dimension | Finding | Impact |
|-----------|---------|--------|
| localarea | 100% null | Must use postalcode FSA as proxy |
| geo_point_2d | 51.8% coverage, consistent 48-57% across all years | Spatial analysis on a subset only — not representative |
| businessname | 4.3% null | Well-populated, usable for tracking |
| house + street | 46.2% null each | Only 53.8% of rows have complete name+house+street |
| postalcode | 46.8% null | 53.1% have valid Vancouver FSA |
| numberofemployees | 0% null (100% populated) | Usable covariate — median 1, mean 7 |
| feepaid | 16.0% null | Good covariate — median $155, range up to $63k |
| businesstype | 0% null, 181 unique types | Schema stability better than expected: only 9 types absent from 2024 |
| issueddate | 16.9% null | 83.1% populated, parseable, no anomalies |
| expireddate | 16.9% null | 99.8% expire in December — uniform annual cycle |
| folderyear 24 status anomaly | 50,083 Inactive vs ~1,400-2,800 in prior years | CRITICAL: year 24 data appears to be a mid-year snapshot, not year-end |

## Critical Findings for Survival Analysis

### What WORKS:
1. **Business tracking via name+address** is feasible — 131,870 unique business-addresses built, 85.9% appear in 2+ years
2. **feepaid** is a viable covariate (84% coverage, meaningful variation by type)
3. **postalcode FSA** is a viable geographic proxy for the null localarea (53.1% coverage)
4. **12 years of data** (2013–2024) allows meaningful multi-year survival analysis
5. **status field** provides a direct survival signal (Gone Out of Business, Cancelled)
6. **numberofemployees** is 100% populated — rare for a public dataset, strong covariate candidate
7. **Schema break is mild**: only 9 types dropped in 2024, 0 new types introduced — businesstype is stable
8. **Survival signal is clear**: median lifespan 4 years, 1-yr: 100%, 2-yr: 87.9%, 5-yr: 56.7%, 10-yr: 35.1%

### What DOESN'T WORK or NEEDS CARE:
1. **localarea is 100% null** — spatial analysis must use FSA proxies or geo coordinates
2. **geo_point_2d only ~50% coverage** — spatial analysis is possible but on a biased subset (which businesses have geocodes?)
3. **house + street 46% null** — only 53.8% of rows have all three tracking fields. The other 46.2% can only be tracked by name alone or not at all
4. **folderyear 24 is NOT a full year**: 50,083 rows show "Inactive" status vs 1,400-2,800 in all prior years. This strongly suggests folderyear 24 was extracted mid-cycle before year-end processing. Active count drops to 4,069 (vs 48k-55k normally). **Do not treat folderyear 24 as a complete observation year.**
5. **licencersn changes every year** — confirmed, cannot use for tracking (use name+address)
6. **Address null rate is the binding constraint**: only 53.8% of rows have complete tracking keys. Businesses with no address (often sole traders, home-based, or service businesses without a fixed location) are untrackable and excluded from the panel.

### Blocking Issues:
- **Folderyear 24 anomaly is the most significant issue**: It appears to be a snapshot extracted before the annual renewal cycle completed. The 50k "Inactive" records are likely businesses whose licences have lapsed but haven't been processed yet. This means 2024 cannot be used as a definitive endpoint for survival analysis — use 2023 as the last clean observation year.
- No other issues block survival analysis.

### Recommended Next Steps:
1. **Treat folderyear 24 as partial/unreliable** — use 2023 as the last clean year. Right-censor at 2023 for the survival model.
2. Build formal survival model (Cox PH or Kaplan-Meier) using `business_panel.csv`
3. Event definition: `status = "Gone Out of Business"` OR (last_year < 23 AND status != "Issued"). Right-censor if last_year = 23 and status = "Issued".
4. Covariates to test: feepaid, businesstype (using the stable 172-type taxonomy), FSA, numberofemployees
5. Validate name+address matching on a sample — false negatives (same business, slightly different address format) will undercount survival
6. The 46% address null rate means the panel covers ~54% of the population — investigate whether non-trackable businesses (no address) differ systematically from trackable ones before proceeding with survival estimates
7. If spatial analysis is needed: filter to rows with valid geo_point_2d (~51.8%) and join to CoV neighbourhood polygons via the geom field
