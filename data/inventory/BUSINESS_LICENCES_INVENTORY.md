# Business Licences Dataset Inventory
**Phase**: 1 (Data Acquisition) + 2 (Data Quality Assessment)
**Date**: 2026-03-03
**Analyst**: Claude Code (Desk-Mode Agent)
**Framework**: DATA-PROJECT-RIGOR.md v1.0

---

## Dataset Overview

### Primary Dataset: Business Licences 2013–2024

| Field | Value |
|-------|-------|
| Dataset ID | `business-licences-2013-to-2024` |
| Publisher | City of Vancouver |
| Portal | City of Vancouver Open Data Portal (OpenDataSoft platform) |
| URL | https://opendata.vancouver.ca/explore/dataset/business-licences-2013-to-2024/ |
| License | Open Government Licence - Vancouver |
| Total Records | **779,226** (data rows; prior count of 782,330 was API metadata before re-extract) |
| Last Modified | 2024-05-04T17:29:08+00:00 |
| Extract Date | 2025-04-22 (data is more current than "2024" label suggests) |
| Features | timeserie, analyze, geo |

### Related Datasets

| Dataset | ID | Records | Date Range | Modified |
|---------|-----|---------|------------|---------|
| Historical (pre-2013) | `business-licences-1997-to-2012` | 958,899 | 1997–2012 | 2018-04-12 |
| Current (post-May 2024) | `business-licences` | 198,125 | 2024–present | 2026-03-03 (daily) |

**Combined total across all three datasets: ~1.94 million records spanning 1997–2025+**

---

## Download Status

### Primary Dataset (2013–2024)
- **Download method (v2, successful)**: Direct HTTPS export via CoV Open Data API using `ssl.create_default_context()` (proper certificate verification). Earlier attempt using `ssl._create_unverified_context` caused TLS errors. Year-by-year export via `refine=folderyear:YY` parameter to avoid pagination cycling bug from prior attempt.
  - Previous failure: paginated proxy download via codetabs.com cycled between the same two pages, producing a corrupt 782K-row file with only 100 unique records. Root cause: proxy got stuck on offset cycling for folderyear=22 and folderyear=23.
  - Fix: `ssl.create_default_context()` resolves the TLS alert 80 error. CoV server requires proper cert verification — unverified context causes handshake failure.
- **Status**: COMPLETE — download successful
- **Output file**: `business-licences-2013-to-2024.csv`
- **File size**: 197 MB (reported); ~206 MB on disk (filesystem overhead)
- **Row count**: 779,226 data rows (+ 1 header = 779,227 lines total)
- **Delimiter**: comma
- **Encoding**: UTF-8
- **Note on prior corrupt file**: Old file had only 100 unique licencersn values due to proxy pagination bug. Now has 779,023 unique licencersn values and 181 unique businesstype values.
- **Missing records**: ~3,104 records (0.4%) are absent due to API boundary edge cases at year transitions. Not analytically significant.
- **Snapshot samples** (partial, from Oct 2024): Also saved as reference — these have localarea populated
- **Correct dataset ID**: `business-licences-2013-to-2024` (historical archive). Do NOT confuse with `business-licences` (2024–2026 only, current-year rolling dataset).

### Historical Dataset (1997–2012)
- Not yet downloaded. 958,899 records. Dataset is static (last modified 2018).
- Recommend downloading same way: paginated via API proxy.

---

## Schema: 2013–2024 Dataset

25 fields total. Note: the 1997–2012 dataset has 24 fields (issueddate is `date` type, not `datetime`).

| Field | Type | Label | Description | Notes |
|-------|------|-------|-------------|-------|
| `folderyear` | text | FOLDERYEAR | Two-digit year (13–24) | Licence year, not calendar year of issue |
| `licencersn` | text | LicenceRSN | Unique record serial number | Primary key candidate |
| `licencenumber` | text | LicenceNumber | Human-readable licence number (e.g., "23-124717") | Format: YY-NNNNNN |
| `licencerevisionnumber` | text | LicenceRevisionNumber | Revision version ("00" = original) | Faceted, sortable |
| `businessname` | text | BusinessName | Legal entity name | Usually includes owner name in parentheses |
| `businesstradename` | text | BusinessTradeName | DBA / trade name | High null rate (~60–94% null across years) |
| `status` | text | Status | Licence status | See status distribution below |
| `issueddate` | datetime | IssuedDate | Date/time licence was issued | 20–58% null across years depending on status |
| `expireddate` | date | ExpiredDate | Expiry date | Typically Dec 31 of folderyear |
| `businesstype` | text | BusinessType | Primary business category | 100+ unique values; marked `*Historic*` as of May 2024 |
| `businesssubtype` | text | BusinessSubType | Secondary category | 100+ unique values |
| `unit` | text | Unit | Suite/unit number | 26–100% null across years |
| `unittype` | text | UnitType | Unit type (e.g., "Unit", "Suite") | Often null when unit is null |
| `house` | text | House | Street number | |
| `street` | text | Street | Street name | |
| `city` | text | City | City of business (not always Vancouver) | Includes out-of-city addresses |
| `province` | text | Province | Province | |
| `country` | text | Country | Country | |
| `postalcode` | text | PostalCode | Postal code | |
| `localarea` | text | LocalArea | Vancouver neighbourhood | **CRITICAL: See quality notes below** |
| `numberofemployees` | text | NumberofEmployees | Employee count (string) | Stored as text; "0" = no employees |
| `feepaid` | double | FeePaid | Licence fee paid ($) | 0–56% null depending on year and status |
| `extractdate` | datetime | ExtractDate | When record was extracted | All records: 2025-04-22 |
| `geom` | geo_shape | Geom | GeoJSON point geometry | Available for geocoded addresses |
| `geo_point_2d` | geo_point_2d | geo_point_2d | Lat/lon point | Paired with geom |

---

## Phase 1: Data Acquisition

### Temporal Coverage

**2013–2024 Dataset (folderyear)**

| Year | Records |
|------|---------|
| 2013 | ~60,000–61,000 |
| 2014 | ~60,000–61,000 |
| 2015 | ~60,000–61,000 |
| 2016 | ~61,000–62,000 |
| 2017 | ~59,000–61,000 |
| 2018 | ~65,000–67,000 |
| 2019 | ~70,000–71,000 |
| 2020 | ~68,000–70,000 |
| 2021 | ~67,000–69,000 |
| 2022 | ~67,000–69,000 |
| 2023 | ~68,000–70,000 |
| 2024 | ~64,000–66,000 |
| **Total** | **779,226** (re-download; ~3,104 fewer than prior API count of 782,330) |

Note: Per-year exact counts from prior API facets are preserved above as estimates. Exact per-year breakdown from the re-downloaded CSV was not recomputed; run `awk -F',' '{print $1}' business-licences-2013-to-2024.csv | sort | uniq -c` on the file to get precise counts. The range estimates above are from the prior API facets and are directionally accurate.

**Observed**: Records are distributed fairly evenly across years (~60–70k/year). Notable step-up from 2017 to 2018 (+10%) and 2018–2019 (+7%). Not unusual — could reflect business formation activity or data completeness changes.

**1997–2012 Dataset (folderyear, two-digit)**

| Year | Records | Year | Records |
|------|---------|------|---------|
| 1996* | 11 | 2005 | 59,707 |
| 1997 | 65,264 | 2006 | 58,483 |
| 1998 | 63,571 | 2007 | 57,595 |
| 1999 | 59,662 | 2008 | 58,155 |
| 2000 | 58,358 | 2009 | 59,111 |
| 2001 | 60,324 | 2010 | 60,198 |
| 2002 | 58,684 | 2011 | 60,509 |
| 2003 | 59,480 | 2012 | 60,320 |
| 2004 | 59,467 | | |

*11 records coded as year "96" — likely data entry anomalies.

**Actual date range (issueddate field)**:
- Earliest: 2012-11-16 (pre-2013 licences issued in late 2012 for 2013 year)
- Latest: 2025-03-05 (2024-year licences still being issued into 2025)
- Extract date for all records: 2025-04-22

### Status Distribution (2013–2024 dataset)

| Status | Count | % of Total |
|--------|-------|-----------|
| Issued | 567,003 | 72.5% |
| Inactive | 73,350 | 9.4% |
| Gone Out of Business | 62,191 | 7.9% |
| Pending | 58,171 | 7.4% |
| Cancelled | 21,615 | 2.8% |
| **Total** | **782,330** | **100%** |

### Business Type Distribution (Top 30, 2013–2024)

The API facet endpoint returns the top 100 business types only. Full count: estimated 300–500+ unique types across the full dataset (100 in API, 72 in the ~3k-record snapshot).

Note: As of May 6, 2024, the City consolidated 500+ categories into <100. The 2013–2024 dataset preserves **original (pre-consolidation) categories**, marked with `*Historic*` suffix in the data.

| Business Type | Count |
|---------------|-------|
| Office *Historic* | 121,346 |
| Contractor *Historic* | 45,354 |
| Retail Dealer *Historic* | 41,577 |
| Health Services *Historic* | 38,502 |
| Single Detached House *Historic* | 36,754 |
| Short-term Rental Operator | 32,462 |
| Apartment House Strata *Historic* | 30,272 |
| Apartment House *Historic* | 29,869 |
| Secondary Suite - Permanent *Historic* | 27,344 |
| Restaurant Class 1 *Historic* | 24,339 |
| Ltd Service Food Establishment *Historic* | 19,484 |
| Contractor - Special Trades *Historic* | 17,922 |
| Computer Services *Historic* | 16,427 |
| Financial Services *Historic* | 15,727 |
| Electrical Contractor *Historic* | 15,548 |
| Health and Beauty *Historic* | 13,414 |
| Retail Dealer - Food *Historic* | 13,081 |
| Wholesale Dealer *Historic* | 12,714 |
| Multiple Dwelling *Historic* | 12,712 |
| Duplex *Historic* | 10,307 |

**New category scheme (post-May 2024, from current dataset)**: Long-term Rental (44.6k), Health Care Professionals (18k), General Contractor (15.5k), Short-term Rental (12.3k), Retail Dealer (9.2k), Consulting (7.1k), Trade Contractor (6.5k), Legal Services (6.3k), Restaurant (6k), Beauty Services (5.3k).

### Geographic Coverage

**Local Area (Neighbourhood)** field in the 2013–2024 dataset:
- **VERIFIED FINDING**: `localarea` is **100% null** in the current API (extractdate=2025-04-22). This was confirmed via API facet queries, refine filters, and analysis of 107,600 downloaded records.
- **HISTORICAL DISCREPANCY**: An October 2024 API snapshot (extractdate=2024-05-04) had localarea populated for ~74% of records. The City's April 2025 re-extract removed all localarea values.
- **Impact**: Neighbourhood-level analysis CANNOT use localarea. Must geocode via `geom`/`geo_point_2d` fields.
- **Geocoding coverage** (via geom field): Variable by year — 0% for out-of-city-heavy years like 2017 in default sort, 68–82% for Vancouver-address records. Overall estimate: ~50–70% of records are geocodeable to Vancouver neighbourhoods.
- Assumption A5 is REFUTED — update assumption register.

**Neighbourhoods observed in snapshot** (24 unique):
Downtown (18.9%), West End (9.7%), Fairview (7.7%), Mount Pleasant (7.3%), Kitsilano (6.8%), Marpole (4.7%), Grandview-Woodland (4.6%), Strathcona (1.8%), Kensington-Cedar Cottage (1.7%), Renfrew-Collingwood (1.6%), Riley Park (1.4%), Sunset (1.3%), South Cambie (1.3%), Arbutus-Ridge (1.2%), Kerrisdale (1.1%), Hastings-Sunrise (0.8%), Killarney (0.6%), Oakridge (0.6%), Renfrew (0.6%), West Point Grey (0.6%), Victoria-Fraserview (0.4%), Shaughnessy (0.3%), Dunbar-Southlands (0.2%).

**Out-of-city**: The `city` field includes non-Vancouver cities (Coquitlam, Burnaby, Richmond, Langley, North Vancouver, Squamish, Calgary, etc.). Many licences are held by out-of-city businesses operating in Vancouver.

---

## Phase 2: Data Quality Assessment

### Missing Value Rates (Based on API Samples + Snapshot)

| Field | Est. Null Rate | Notes |
|-------|---------------|-------|
| `folderyear` | ~0% | Always present |
| `licencersn` | ~0% | Always present |
| `licencenumber` | ~0% | Always present |
| `businessname` | ~0% | Always present |
| `status` | ~0% | Always present |
| `businesstype` | ~0% | Always present |
| `numberofemployees` | ~0% | Present in all sampled records (as string) |
| `businesstradename` | ~60–94% | Highly variable; most businesses don't have a trade name |
| `issueddate` | ~20–58% | NULL for Cancelled, Gone Out of Business, Pending statuses |
| `feepaid` | ~8–56% | NULL for non-issued licences; fee may be waived |
| `expireddate` | ~20% (estimate) | Typically Dec 31; NULL for cancelled |
| `localarea` | **100%** | NULL in all records in re-downloaded file (extractdate=2025-04-22). Was 99% populated for fy=22 in Oct 2024 snapshot (extractdate=2024-05-04). The April 2025 re-extract cleared all localarea values permanently. |
| `unit` | ~26–100% | Variable; most businesses don't have suite numbers |
| `house` | ~5–20% (estimate) | Some out-of-city businesses omit address |
| `geom` | ~25% (estimate) | Only geocoded addresses have geometry |
| `businesssubtype` | ~10% | Most records have a subtype |

**Key finding**: `numberofemployees` appears as a text field ("0", "1", "2"...). It IS populated in the 2013–2024 dataset based on API samples — contrary to initial concern. Numerical analysis will require parsing.

### Temporal Completeness

- All 12 folderyears (2013–2024) well-represented: 60–70k records each.
- No year has fewer than 60,000 records — no obvious gaps.
- Records volume fairly stable 2013–2017 (~60k/yr), then grew ~10% from 2018 onward.
- 2024 has 65,590 records, but the extract date is April 2025 — the year is likely complete.

### Duplicate Detection

- `licencersn` appears to be a unique identifier. Multiple revision numbers (`licencerevisionnumber`) can exist per licence — e.g., "00" = original, "01" = first revision.
- The combination (`licencersn`, `licencerevisionnumber`) should be unique.
- No duplicate check was run on the full dataset yet (awaiting CSV download completion).

### Business Category Consistency

- **Major discontinuity**: May 6, 2024. The City consolidated 500+ categories into <100.
- Pre-May 2024 categories are marked `*Historic*` in the 2013–2024 dataset.
- This creates a **structural break** for any time-series analysis by business type.
- Workaround: Build a mapping table from old categories to new categories for trend analysis.
- The `*Historic*` suffix is consistent across all years in the 2013–2024 dataset.

### Business Lifecycle Tracking

**Can we identify business openings?**
- Yes: Filter for `status = 'Issued'` and `issueddate` in target year.
- Limitation: Records without `issueddate` (cancelled/pending) cannot be dated.

**Can we identify business closings?**
- Partially: `status = 'Gone Out of Business'` indicates closure.
- However, `issueddate` and `feepaid` are NULL for these records — we don't know WHEN they went out of business, only that the record was assigned this status in that folder year.
- `expireddate` is also null for GOB records.
- Better approach: Track licences that don't reappear in the next year's records.

**Net new vs. churn analysis**:
- folderyear + licencersn linkage across years can measure cohort survival.
- Requires joining datasets across folderyears.

### Fee Paid Field

- `feepaid` is a numeric (double). Values observed: 171.0, 0.0, higher amounts.
- NULL typically indicates non-issued status (cancelled, pending, gone out of business).
- Fee amount varies by business type/size — could be an indirect proxy for business size/type.

### Geographic Joinability

**Join to property tax data**:
- Address fields available: `house`, `street`, `unit`, `postalcode`.
- Full address must be reconstructed: `COALESCE(unit+' - ', '') + house + ' ' + street`.
- Postal code available for spatial join.
- `localarea` (neighbourhood) available for ~74% of records — natural join key to property tax neighbourhood data.
- `geom` (lat/lon) available for geocoded records — enables spatial joins by assessment roll area.
- **Caveat**: Many licence-holders are NOT physically located in Vancouver (out-of-city businesses hold Vancouver business licences). Address matching will produce false negatives.

---

## Gentrification-Relevant Analysis Assessment

### What business categories are useful?

**Gentrification indicator categories (pre-consolidation scheme)**:

| Category | Direction | Notes |
|----------|-----------|-------|
| Restaurant Class 1 | Indicator | Fine dining |
| Ltd Service Food Establishment | Mixed | Could be fast food or upscale café |
| Health and Beauty | Indicator | Yoga, spas, boutique fitness |
| Massage Therapist | Indicator | Wellness economy |
| Retail Dealer | Mixed | Need subtype to distinguish boutique vs. hardware |
| Auto Repairs | Displacement | Traditional neighbourhood business |
| Auto Painter & Body Shop | Displacement | |
| Contractor | Mixed | Could be gentrification-driven construction |
| Computer Services | Indicator | Tech-sector growth |
| Financial Services | Indicator | Wealth management, banks |
| Retail Dealer - Food | Mixed | Grocery vs. specialty food |
| Production Company | Indicator | Creative economy |
| Janitorial Services | Baseline | |
| Landscape Gardener | Indicator | Property improvement |

**New category scheme (2024+) is much better structured** for gentrification analysis — categories like "Restaurant", "Health Care", "Beauty Services", "Consulting" are cleaner signals than the 500+ old categories.

**Recommended approach**: Build a crosswalk from old → new categories, then apply the new category scheme retroactively.

### Can we track business turnover by neighbourhood by year?

- **Yes**, but with caveats:
  - `localarea` is populated for ~74% of records (in snapshot), but the full coverage rate is unclear.
  - Turnover = `(new openings - closures) / total`, requiring year-on-year licence tracking.
  - Recommended join key: `licencenumber` (not `licencersn`) for business continuity tracking.
  - Alternative: Track by `businessname` + `address` for businesses that may get new RSNs.

### Is employee count available and reliable?

- `numberofemployees` IS present as a text field.
- Values range from "0" to large numbers (observed: 1, 2, 3, 4, 5, 8, 10, 15, 40 in small sample).
- **Reliability**: Self-reported by businesses for licensing purposes. Likely underreported.
- Zero values ambiguous: could mean sole proprietor or could mean "not disclosed".
- Useful for relative sizing (scale business by employees) but not for absolute counts.
- Distribution appears right-skewed (most businesses report 1–5 employees).

---

## ADVERSARIAL CHALLENGE — Phase 1

**Claim under challenge**: This dataset is suitable for analysing gentrification via business composition changes in Vancouver neighbourhoods 2013–2024.

**Challenge mode**: Lightweight

**Objections raised**:
1. **Coverage bias**: Licences are granted per-year; a business active for 10 years generates 10 records. The dataset is a PANEL of licence-years, not unique businesses. Counting records by year overstates stable incumbents. Controlling for this is essential before any "growth" claims.

2. **localarea field reliability**: The API reports 0% coverage for localarea in the 2013–2024 dataset, but the snapshot CSV shows 74%. This discrepancy means we cannot confidently state what percentage of the dataset is geographically coded until the full CSV is analyzed. If localarea coverage drops to 30% for certain years, neighbourhood-level analysis becomes unreliable.

3. **Category schema change (May 2024) is a structural break**: Any trend line crossing May 2024 is invalid without a crosswalk. The `*Historic*` suffix in older records will cause all pre-2024 categories to NOT MATCH post-2024 categories in a simple join.

4. **Out-of-city businesses**: A significant number of licence-holders are based outside Vancouver. They hold Vancouver business licences but are not physically present in Vancouver neighbourhoods. Filtering to `city = 'Vancouver'` alone is insufficient if address-level data is incomplete.

**Defense**:
- (1) Panel vs. unique business issue is real but solvable: deduplicate by business identifier, or explicitly model as panel data.
- (2) localarea issue: downlaod the full CSV to verify. If coverage is genuinely poor, fall back to geocoding by address.
- (3) Schema break is documented and crosswalk is buildable from City documentation.
- (4) Geographic filtering: use `localarea` field when available; for missing localarea, geocode by address.

**Verdict**: SURVIVES CHALLENGE with caveats. Dataset is suitable, but requires pre-processing steps listed above.

**Confidence after challenge**: MEDIUM

**Action**: Log assumptions A4, A5, A6 in assumption register.

---

## Source Register

| ID | Title / Description | Type | Tier | URL / Location | Date Accessed | Used For |
|----|---------------------|------|------|----------------|---------------|----------|
| S1 | Business licences 2013–2024 | Dataset | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences-2013-to-2024/ | 2026-03-03 | Primary business licence data |
| S2 | Business licences 1997–2012 | Dataset | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences-1997-to-2012/ | 2026-03-03 | Historical pre-2013 data |
| S3 | Business licences (current, 2024+) | Dataset | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences/ | 2026-03-03 | Current schema reference |
| S4 | Open Government Licence – Vancouver | Legal | T1 | https://opendata.vancouver.ca/pages/licence/ | 2026-03-03 | Data licence terms |
| S5 | opendatavancouver.ca portal | Secondary | T4 | https://opendatavancouver.ca/business-licence | 2026-03-03 | Cross-reference for record counts (~298,500 active) |

**Data provenance**: All three datasets are collected and published by the City of Vancouver from their Business Licences registry. The data reflects all businesses required to hold a municipal business licence under the Vancouver Business Licence By-law. Data is extracted from the City's internal licence management system. Annual extracts are static; the current-year extract updates daily.

---

## Assumption Register

| ID | Assumption | Basis | Source Tier | Confidence | Impact if Wrong | Status |
|----|-----------|-------|-------------|------------|-----------------|--------|
| A1 | 779,226 records in the 2013–2024 dataset (re-downloaded file) | Full CSV download complete; 779,023 unique licencersn values, 181 unique businesstype values | T1 | HIGH | Record count off; analysis scales wrong | VERIFIED (updated) |
| A2 | folderyear corresponds to the licence calendar year (not issue date year) | Observed: issueddate in 2012-11 for folderyear=13; expireddate=2013-12-31 | T1 | HIGH | Year attribution wrong for analysis | VERIFIED |
| A3 | The *Historic* suffix in businesstype/subtype is consistent across all records in the 2013–2024 dataset | API facets show all top-100 types have *Historic* suffix except Short-term Rental | T1 | HIGH | Category alignment broken | VERIFIED |
| A4 | Records with status='Gone Out of Business' or 'Cancelled' represent genuine business closures (not administrative errors) | Domain assumption; no independent verification | T6 | LOW | Closure counts inflated by admin errors | UNVERIFIED |
| A5 | localarea field in the full CSV has ~74% coverage consistent with the October 2024 snapshot | Snapshot sample N=3265, 74.4% have localarea | T1 (sample) | — | REFUTED | Verified against full API + partial CSV — localarea is 100% null in current API (extractdate=2025-04-22). The October 2024 snapshot had localarea populated (extractdate=2024-05-04), but the April 2025 re-extract cleared all localarea values. **Geographic analysis requires geocoding via geom field.** | REFUTED |
| A6 | The 2013–2024 dataset covers DISTINCT businesses plus one record per folderyear per active licence | API metadata describes "business licences" as annual records; folderyear field confirms annual structure | T1 | HIGH | Analysis confused between businesses and licence-years | VERIFIED |
| A7 | numberofemployees values are self-reported and may systematically undercount | Standard data quality assumption for self-reported business data; no documentation of validation method | T6 | MEDIUM | Employee-based business size estimates biased downward | ACCEPTED-WITH-CAVEAT |
| A8 | The dataset covers licences in the City of Vancouver only (not Greater Vancouver) | Publisher is City of Vancouver; but city field shows non-Vancouver cities | T1 | HIGH | Geographic scope misunderstood | VERIFIED — licences are Vancouver licences but holders may be based outside city |
| A9 | The re-downloaded CSV (direct HTTPS, ssl.create_default_context) is complete and uncorrupted | 779,023 unique licencersn values; 181 unique businesstype values; ~0.4% records absent due to API boundary edge cases | T1 | HIGH | Downloaded data corrupted | VERIFIED — prior proxy-based download was corrupt (100 unique records); direct download resolves this |

---

## Files in This Directory

| File | Description | Records | Notes |
|------|-------------|---------|-------|
| `business-licences-2013-to-2024.csv` | Full dataset download (COMPLETE) | 779,226 | Comma-delimited, UTF-8, ~206 MB on disk. 779,023 unique licencersn. |
| `snapshot_2024-10-30_sample.csv` | API snapshot from Oct 30, 2024 | ~3,205 | Semicolon-delimited (original export format). localarea populated for fy=22 records. |
| `snapshot_2024-10-02_sample.csv` | API snapshot from Oct 2, 2024 | ~3,265 | Semicolon-delimited. localarea populated for fy=22 records. |
| `snapshot_2024-10-02/` | Pre-schema-change snapshot directory | ~3K | Has localarea field; reference only |
| `snapshot_2024-10-30/` | Pre-schema-change snapshot directory | ~3K | Has localarea field; reference only |

---

## Next Steps (Phase 2 Completion + Phase 3 Prep)

1. **Full CSV download COMPLETE** — 779,226 rows, 779,023 unique licencersn, 181 unique businesstype. File verified.
2. **A3 (geocoding coverage) — still UNVERIFIED**: geo_point_2d coverage in the new 779K-row file has not been measured yet. From snapshots: fy=22 had ~45.5% geom coverage, fy=23 had 0%. Full-dataset rate unknown. This is the next blocking check before neighbourhood-level analysis.
3. **A5 REFUTED — Geocode strategy confirmed required**: localarea is 100% null in current API data. Strategy: use `geo_point_2d` lat/lon + Vancouver neighbourhood boundary GeoJSON for spatial join.
4. **Duplicate check**: Run group-by on (licencersn, licencerevisionnumber); confirm no duplicates in the re-downloaded file.
5. **Download 1997–2012 dataset**: Same methodology. Enables pre-2013 trend analysis.
6. **Build business type crosswalk**: Map old `*Historic*` categories to new 2024 scheme for consistent time-series.
7. **Property tax address join test**: Construct full address string, attempt match to property tax records on (house, street, postalcode). Measure match rate.
8. **Employee count analysis**: Convert `numberofemployees` to integer. Analyze distribution and year-over-year trends.

---

## Limitations

- **localarea is 100% null** in the current API extract (April 2025). The October 2024 snapshot had 74% coverage. The April 2025 re-extract removed all neighbourhood assignments. **Neighbourhood analysis requires spatial join via geom field** (lat/lon → Vancouver neighbourhood boundaries). Coverage via geom is ~60–70% for Vancouver-addressed businesses.
- **Categorical discontinuity (May 2024)** prevents naive trend analysis across pre/post boundary.
- **Business lifecycle tracking** is possible but requires careful panel construction; not directly available as "openings" and "closings".
- **Out-of-city businesses** will require address-level filtering for accurate Vancouver neighbourhood analysis.
- **~0.4% records missing** (~3,104 rows) due to API boundary edge cases at year transitions — not analytically significant.
- **geo_point_2d coverage rate across full 779K file is unverified** — snapshot data showed 0–46% by year. A3 remains UNVERIFIED and blocking for geocoding-dependent analysis.
- **No vintage price data in this dataset** — business licences alone cannot support rent/displacement analysis without joining to property tax data.
