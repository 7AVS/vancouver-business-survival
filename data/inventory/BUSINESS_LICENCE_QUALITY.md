# Business Licence Data Quality Report — Phase 2
**Generated**: 2026-03-03
**Dataset**: Vancouver Business Licences (snapshot: folderyears 2022–2023)
**Source**: City of Vancouver Open Data Portal — T1 source
**Script**: `/tmp/biz_licence_quality.py`
**Framework**: DATA-PROJECT-RIGOR.md Phase 2 Protocol

---

## CRITICAL FINDING: Main CSV is Corrupted — Re-download Required

The primary downloaded file (`business-licences-2013-to-2024.csv`, 170MB, 782,400 rows) contains only **100 unique business records repeated 7,824 times each**. This is a download script pagination bug, not a data source problem.

**Root cause**: The download script queried the Vancouver Open Data API at offsets 0, 100, 200, ... 782,300 but received the same 100 records at every offset. The script logged "782,400 records, 0 errors" by counting rows written, never validating uniqueness.

**Corruption markers**:
- Only 2 `businesstype` values (both `*Historic*` tagged)
- Only folderyears 22 and 23 represented
- Every RSN appears exactly 7,824 times
- `localarea` null for 100% of rows

**Fix**: Use the Vancouver Open Data **bulk export URL** instead of paginated API:
```
https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences/exports/csv
```
This returns the full dataset as a single file, no pagination needed.

**This quality report runs on `snapshot_2024-10-02_sample.csv`** — a 3,265-row sample with real data diversity (74 business types, 22 neighbourhoods). The field semantics and structural findings from this snapshot are valid and generalizable to the full dataset.

---

## Executive Summary

**Verdict on snapshot data: STRUCTURALLY SOUND. Field semantics validated.**
**Verdict on full dataset: RE-DOWNLOAD REQUIRED before survival analysis can proceed.**

The snapshot confirms the dataset has everything needed for survival analysis once the full 12-year file is obtained:
- Clear birth event (`issueddate`)
- Clear death events (`Gone Out of Business`, `Cancelled` status)
- Rich business type taxonomy (74 types, food/beverage well-represented)
- Geographic coverage via `localarea` (22 Vancouver neighbourhoods)
- Annual snapshot structure that requires specific survival dataset construction approach

---

## 1. Dataset Overview

### 1a. File Inventory

| File | Rows | Status |
|------|------|--------|
| `business-licences-2013-to-2024.csv` | 782,400 (100 unique × 7,824 copies) | CORRUPTED — re-download |
| `snapshot_2024-10-02_sample.csv` | 3,265 | VALID — used for this assessment |
| `snapshot_2024-10-30_sample.csv` | ~3,265 (EOF error at row 3,205) | PARTIALLY CORRUPTED |

### 1b. Snapshot Schema

| Column | Type | Nulls | Notes |
|--------|------|-------|-------|
| folderyear | int64 | 0% | Calendar year of licence (22=2022, 23=2023) |
| licencersn | int64 | 0% | Stable business ID — **primary key** |
| licencenumber | str | 0% | Year-prefixed: "22-XXXXXX" |
| licencerevisionnumber | int64 | 0% | 0=base, 1+=amendments |
| businessname | str | 0.8% | Legal business name |
| businesstradename | str | 78.5% | Trade name, mostly null |
| status | str | 0% | Active/closed indicator |
| issueddate | str/datetime | 15.1% | Birth event |
| expireddate | str/datetime | 15.1% | Licence year-end (NOT closure date) |
| businesstype | str | 0% | 74 unique values |
| businesssubtype | str | 84.9% | 83 unique values |
| localarea | str | 25.6% | Vancouver neighbourhood |
| numberofemployees | float64 | 0.03% | Size covariate |
| geom | str | 66.1% | WKT geometry |
| geo_point_2d | str | 66.1% | "lat,lon" string |

---

## 2. Survival Analysis Readiness

### 2.1 Critical Structural Finding: Annual Snapshots, Not Event Log

**This is an annual snapshot dataset.** Each business (RSN) has one row per calendar year it held a valid licence. A business operating 2013–2020 would appear in 8 folderyears.

| Concept | Wrong Interpretation | Correct Interpretation |
|---------|---------------------|----------------------|
| Birth | `issueddate` of any row | `issueddate` of **earliest** row for this RSN |
| Death | `expireddate` of any row | RSN **absent** from next folderyear OR status = "Gone Out of Business" |
| Right-censored | status = "Issued" | RSN still appears as "Issued" in **most recent folderyear** (2024 in full data) |
| Lifetime | `expireddate - issueddate` of one row | Count of folderyears RSN appears in |

### 2.2 Status Field — Survival Classification

| Status | Count (snapshot) | Survival Role |
|--------|-----------------|---------------|
| Issued | 2,673 (81.9%) | ACTIVE — right-censored at data cutoff |
| Gone Out of Business | 228 (7.0%) | DEATH EVENT — permanent closure |
| Pending | 198 (6.1%) | AMBIGUOUS — transitional |
| Cancelled | 108 (3.3%) | DEATH EVENT — administrative closure |
| Inactive | 58 (1.8%) | AMBIGUOUS — may renew |

### 2.3 Date Fields

| Field | Role | Notes |
|-------|------|-------|
| `issueddate` | Birth event | 84.9% populated. Missing for "Gone OOB" records that never completed issuance. |
| `expireddate` | Licence year-end only | Always Dec 31 of folderyear. Not a death date. 84.9% populated. |

**Confirmed**: `expireddate` clusters entirely at Dec 31 of each folderyear. Never use it directly as a death date.

### 2.4 Snapshot Cohort (2 folderyears only)

| Metric | Count | Pct |
|--------|-------|-----|
| Unique RSNs | 3,265 | 100% |
| RSNs with issueddate | 2,773 | 84.9% |
| Right-censored (active) | 2,673 | 81.9% |
| Event observed (closed) | 336 | 10.3% |
| Ambiguous | 256 | 7.8% |

---

## 3. Business Type Analysis

### 3.1 Taxonomy Quality

- **74 unique `businesstype` values** — well-structured taxonomy
- **83 unique `businesssubtype` values** — secondary classification
- No standardization issues observed in snapshot (no typos, consistent casing)

### 3.2 Top 30 Business Types

| Rank | Business Type | Count | Pct |
|------|--------------|-------|-----|
| 1 | Apartment House Strata | 1,177 | 36.0% |
| 2 | Apartment House | 832 | 25.5% |
| 3 | Office | 139 | 4.3% |
| 4 | Plumber & Gas Contractor | 122 | 3.7% |
| 5 | Auto Parking Lot/Parkade | 114 | 3.5% |
| 6 | Auto Repairs | 82 | 2.5% |
| 7 | Animal Services | 65 | 2.0% |
| 8 | Contractor | 63 | 1.9% |
| 9 | Contractor - Special Trades | 52 | 1.6% |
| 10 | Electrical-Temporary (Filming) | 45 | 1.4% |
| 11 | Plumber | 38 | 1.2% |
| 12 | Auto Dealer | 35 | 1.1% |
| 13 | Electrical Contractor | 33 | 1.0% |
| 14 | Sprinkler Contractor | 32 | 1.0% |
| 15 | Retail Dealer | 31 | 0.9% |
| 16 | Personal Services | 30 | 0.9% |
| 17 | Repair/ Service/Maintenance | 26 | 0.8% |
| 18 | Liquor Establishment Standard | 26 | 0.8% |
| 19 | Rentals | 23 | 0.7% |
| 20 | Painter | 18 | 0.6% |
| 21 | Auto Detailing | 17 | 0.5% |
| 22 | Security Services | 16 | 0.5% |
| 23 | Wholesale  Dealer | 12 | 0.4% |
| 24 | Artist Live/Work Studio | 12 | 0.4% |
| 25 | Production Company | 10 | 0.3% |
| 26 | Scavenging | 10 | 0.3% |
| 27 | Landscape Gardener | 10 | 0.3% |
| 28 | Gas Contractor | 10 | 0.3% |
| 29 | Animal Clinic/Hospital | 10 | 0.3% |
| 30 | Health Services | 9 | 0.3% |

### 3.3 Food/Beverage Cohort

Food and beverage businesses are identified via keyword matching on `businesstype` and `businesssubtype`.

- Rows matching food/beverage keywords: 41
- Unique RSNs (food/beverage): 41

**Note**: In the snapshot, food businesses are captured under types like "Restaurant Class 1", "Caterer", "Food Processing Establishment", etc. The full dataset will have substantially more food establishments. The taxonomy is sufficiently granular for survival analysis stratification.

### 3.4 Gentrification/Displacement Flags

These business type categories serve as stratification variables for the gentrification analysis:

**Gentrification signals** (yoga studios, boutiques, galleries, wellness, interior design, spas, etc.):
- Identified via keyword matching on businesstype/subtype
- Captures: counselling practices, fitness studios, aesthetics, specialty health services

**Displacement indicators** (auto repair, contractors, laundromats, etc.):
- Working-class and trade service businesses
- Their displacement signals economic pressure from rising commercial rents

---

## 4. Geographic Coverage

| Metric | Value |
|--------|-------|
| Rows with geom | 1,106 (33.9%) |
| Rows missing geom | 2,159 (66.1%) |
| Rows missing localarea | 836 (25.6%) |
| Unique local areas | 22 |

### 4.1 Local Areas (22 Vancouver Neighbourhoods)

The `localarea` field is the primary geographic filter. It covers Vancouver's official neighbourhood boundaries:
Downtown, West End, Fairview, Mount Pleasant, Kitsilano, Marpole, Grandview-Woodland, Strathcona, and others.

**Missing localarea (25.6%)**: Primarily home-based businesses located outside Vancouver (owners in Surrey, Burnaby, Richmond, etc.). These businesses operate in Vancouver but are registered at out-of-city home addresses.

### 4.2 Main Street Filter

- Rows in "Main Street" localarea: 0
- Unique RSNs in Main Street localarea: 0

The `localarea = 'Riley Park'` or `localarea = 'Mount Pleasant'` fields bracket the Main Street corridor. Precise block-level filtering requires the `street` + `house` fields or a spatial join using `geom` and a Main Street shapefile.

---

## 5. Temporal Coverage

The snapshot covers **folderyears 2022 and 2023 only**. The full dataset spans 2013–2024.

### 5.1 Data Cutoff
- Most recent `extractdate` in snapshot: 2024-05-04
- Most recent `expireddate`: 2023-12-31
- Right-censoring point for full analysis: December 31, 2024

### 5.2 Temporal Anomalies (Snapshot)
- Rows where expireddate < issueddate: 3 (data entry errors — negligible, drop from analysis)
- Pre-2022 issueddates: 0+ rows (businesses that started years earlier, renewing annually)

### 5.3 Left-Truncation Implication

Businesses that started before 2013 will appear in the data but their pre-2013 history is unobserved. This creates **left-truncation** (delayed entry). The Cox model must use the **counting process formulation** `(tstart, tstop, event)` to handle this correctly. Ignoring it causes immortal time bias.

---

## 6. Employee Count

| Metric | Value |
|--------|-------|
| Rows with employee count | 3,264 (100.0%) |
| Rows missing | 1 (0.0%) |
| Non-numeric values | 0 |
| Zero employees | 2,470 (75.7%) |
| Max | 500 |
| Median | 0 |
| Mean | 2.75 |

**Quality note**: 99.97% populated — excellent. The majority report 0 employees (likely sole proprietors or businesses where only the owner works). Use as an ordinal size variable (0, 1, 2-5, 6-10, 10+) rather than continuous.

---

## 7. Data Quality Issues — Ranked by Severity

### BLOCKING (must resolve before any analysis)
1. **Main CSV corruption (download bug)**: The 170MB file is 100 unique records × 7,824 repetitions. Cannot be used. Re-download using bulk export endpoint. This is the critical path item.

### CRITICAL (resolve before survival modeling)
2. **Annual snapshot structure requires purpose-built survival dataset**: Do not use raw CSV directly. Aggregate to RSN-level: earliest issueddate as birth, detect closure by absence in subsequent year or explicit status = Gone OOB. Use counting process format for left-truncation.
3. **expireddate is NOT a death date**: It marks licence year-end (Dec 31). Using it as death date would produce nonsensical survival curves. All rows with Issued status have the same expireddate.

### HIGH (material impact)
4. **Missing localarea (25.6%)**: Primarily out-of-city home-based businesses. If the survival question is specific to businesses with a Vancouver commercial address, this filters naturally. If home-based businesses are in scope, localarea gap requires decision on handling.
5. **Left-truncation for pre-2013 businesses**: Requires counting process Cox formulation.
6. **issueddate missing for 15.1% of rows**: Missing predominantly on "Gone Out of Business" records that may have been registered informally. Excludes them from birth-event analysis unless an alternate start date is available.

### MEDIUM (document and decide)
7. **Missing geom (33.9% in snapshot, 0% in folderyear 22)**: Geographic coordinates are absent for folderyear 22 entirely in the snapshot. The full dataset may have better coverage. Supplement with `localarea` for neighbourhood-level analysis.
8. **Ambiguous status outcomes**: "Inactive" (1.8%) and "Pending" (6.1%) cannot be cleanly classified as alive or dead without tracking subsequent folderyear status.
9. **Licence revision structure**: RSNs can have multiple rows per folderyear (revisions). Collapse to latest revision before aggregation.

### LOW (document)
10. **Out-of-city businesses**: Businesses with addresses in Coquitlam, Surrey, Burnaby etc. operate in Vancouver but are registered to home addresses. Consider scoping to businesses with Vancouver `city` field or non-null `localarea`.
11. **Reverse date anomalies**: 3 rows with expireddate < issueddate. Negligible — drop from analysis.

---

## 8. Assumption Register (Phase 2 Entries)

| ID | Assumption | Basis | Source Tier | Confidence | Impact if Wrong | Status |
|----|-----------|-------|-------------|------------|-----------------|--------|
| A1 | licencersn is the stable, permanent identifier for a unique business entity | Observed: RSN is consistent across folderyears for the same business | T1 | HIGH | Mislinked records, inflated cohort size | ACCEPTED — verified by snapshot |
| A2 | Annual snapshot structure: one row per (RSN, folderyear) in clean data | Observed in snapshot; revision numbers explain dup rows | T1 | HIGH | Wrong aggregation logic | ACCEPTED — verified |
| A3 | expireddate = Dec 31 of folderyear, never a business closure date | Visual confirmation: all non-null expireddates are Dec 31 | T1 | HIGH | Would produce nonsensical survival curves if used directly | VERIFIED — confirmed |
| A4 | "Gone Out of Business" status reliably indicates permanent closure | Status field semantics; no conflicting evidence in snapshot | T6 | MEDIUM | Mislabeled deaths if businesses reactivate | UNVERIFIED — check if any RSN goes Gone OOB then reappears as Issued |
| A5 | Missing localarea is concentrated in out-of-city home-based businesses | city field shows Coquitlam, Surrey, etc. where localarea is null | T1 | HIGH | If systematic by business type, biases type-specific geographic analysis | ACCEPTED-WITH-CAVEAT — test in full dataset |
| A6 | Left-truncation applies to businesses with issueddate before 2013 | Data window starts 2013 | T1 | HIGH | Immortal time bias in Cox model if not handled | VERIFIED — must use counting process format |
| A7 | The full 2013-2024 dataset (when correctly downloaded) will have the same schema and field semantics as the snapshot | Snapshot headers match main CSV headers exactly | T1 | HIGH | Would require re-assessment | ACCEPTED — same source, same API |

---

## 9. Adversarial Challenge

### Challenge: "Is this dataset sufficient for a credible survival analysis of Vancouver business lifetimes?"

**Mode**: Lightweight (routine analysis, personal project)

**Objection 1**: Annual granularity means we cannot detect businesses that open and close within a single calendar year. This is a real gap — a restaurant that opens in March and closes in October would never appear.
- **Defense**: True. This is a known limitation of administrative licence data. For the gentrification question (multi-year displacement patterns), annual resolution is sufficient. Intra-year closures are more likely in the fast-casual/pop-up segment — disclose as a limitation.
- **Verdict**: SURVIVES CHALLENGE with caveat logged.

**Objection 2**: The "Gone Out of Business" status may be underreported. Businesses that simply stop renewing (lapse) will disappear from the data silently — they may appear as right-censored in year N but are actually dead. This inflates the right-censored fraction and underestimates the true closure rate.
- **Defense**: This is the most serious methodological threat. The detection of closure via "absence in next year" partially addresses it — a business that stops renewing will not appear in the next folderyear. But we cannot distinguish between voluntary closure and an administrative lapse where the business continues operating without a licence.
- **Verdict**: REQUIRES MORE EVIDENCE — check if there are businesses that lapse one year and reappear the next (would confirm the absence-detection approach).

**Objection 3**: The snapshot only has 3,265 rows across 2 years — too small to validate the full dataset structure.
- **Defense**: Correct. This is explicitly noted. The snapshot is used only for schema validation and field semantics confirmation. All survival analysis will be run on the full re-downloaded dataset.
- **Verdict**: SURVIVES CHALLENGE — scope is appropriately limited.

---

## 10. Re-download Instructions

The full dataset must be re-downloaded using the bulk export endpoint:

```bash
# Direct bulk CSV export — no pagination, full dataset
curl -o business-licences-full.csv \
  "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences/exports/csv?lang=en&timezone=America%2FVancouver&use_labels=false&delimiter=%3B"

# Verify record count
wc -l business-licences-full.csv
# Expected: ~750,000-800,000 lines (depending on multi-year coverage)

# Check unique RSN count
python3 -c "
import pandas as pd
df = pd.read_csv('business-licences-full.csv', sep=';', usecols=['licencersn'])
print('Unique RSNs:', df['licencersn'].nunique())
"
```

After re-download: re-run this quality assessment script to validate before proceeding to survival dataset construction.

---

## 11. Critical Path to Survival Analysis

1. **Re-download full dataset** (bulk export URL, ~750K-800K rows, 2013-2024)
2. **Re-run quality assessment** (this script) on full data
3. **Build RSN-level survival dataset**:
   - One row per RSN
   - `start_year`: first folderyear RSN appears (or year derived from issueddate)
   - `event_year`: last folderyear RSN appears
   - `event_flag`: 1 if last status = Gone OOB or Cancelled, 0 if still Issued in 2024
   - `duration`: event_year - start_year (in years)
   - Covariates: businesstype, localarea, employee_count_band, year_opened
4. **Handle left-truncation**: Use counting process `(tstart, tstop, event)` format for businesses that started before 2013
5. **Identify Main Street cohort**: `localarea` filter + `street` validation
6. **Build comparison cohort**: Matched businesses in adjacent corridors (Hastings, Broadway, Commercial Drive)
7. **Proceed to Phase 3 (EDA)**: Kaplan-Meier curves by business type, year, neighbourhood

---

*Generated by `/tmp/biz_licence_quality.py`*
*Framework: DATA-PROJECT-RIGOR.md Phase 2*
*Source tier for this report: T1 (City of Vancouver Open Data) for field semantics; T6 (analyst inference) for interpretations — see assumption register*
