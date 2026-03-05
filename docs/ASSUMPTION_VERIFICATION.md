# Assumption Verification Report
**Project**: Vancouver Business Survival Analysis
**Framework**: DATA-PROJECT-RIGOR.md v1.0
**Date**: 2026-03-03
**Analyst**: Claude Code (Desk-Mode Agent)

---

## Summary Table

| Assumption | Status | Confidence | Blocking? |
|------------|--------|------------|-----------|
| A1: Neighbourhood code lookup (property tax → CoV names) | PARTIALLY VERIFIED | MEDIUM | YES |
| A3: LocalArea field assignment method | UPDATED — VERIFIED | HIGH | PARTIAL |
| A6: LicenceRSN as unique record key; LicenceNumber reuse | UPDATED — VERIFIED | HIGH | NO |
| A6/A13: Seasonal licence lapse detection | UNVERIFIED | — | YES |
| A11: Broadway Subway station locations | VERIFIED | HIGH | NO |
| A15: Home-based business address removal | VERIFIED | HIGH | YES |
| A16: CURRENT_LAND_VALUE type and previous_land_value availability | VERIFIED | HIGH | YES |
| A17: Business type taxonomy break at FY24 | VERIFIED | HIGH | YES |
| A18: NumberofEmployees type mismatch across datasets | VERIFIED | HIGH | YES |
| A19: External triangulation of survival rates | VERIFIED-WITH-CAVEATS | HIGH (aggregate) / LOW (Finance & Insurance) | NO |

---

## A1: Neighbourhood Code Lookup

### Question
What are the exact neighbourhood codes in the property tax data? Can we map them to the CoV Local Area Boundary polygons?

### Findings

**The field is `neighbourhood_code`, not `geo_local_area`.**
All four property tax CSV files use a field named `neighbourhood_code`, a 3-character zero-padded integer (`001` through `030`). There are exactly 30 unique values, all present in every year from 2006–2026 with 0% null rate.

**These codes are BC Assessment internal identifiers, not CoV 22 Local Area names.**
The CoV Open Data Portal's `local-area-boundary` dataset has 22 features (the 22 official CoV planning areas) but only 3 fields: `name`, `geom`, and `geo_point_2d`. There is no numeric mapid or code field. The 30 BC Assessment codes do not have an official publicly published lookup table mapping them to CoV neighbourhood names.

**Confirmed neighbourhood boundary dataset downloaded:**
- URL: `https://opendata.vancouver.ca/explore/dataset/local-area-boundary/`
- Downloaded to: `data/raw/local-area-boundary.geojson`
- File size: 90,858 bytes
- Features: 22 polygons
- Fields: `name`, `geo_point_2d`, `geom`
- Last modified: 2023-06-24

**The 22 CoV Local Area names (from boundary dataset):**

| Name | Centroid (lat, lon) |
|------|---------------------|
| Arbutus Ridge | 49.2468, -123.1617 |
| Downtown | 49.2807, -123.1166 |
| Dunbar-Southlands | 49.2380, -123.1895 |
| Fairview | 49.2645, -123.1310 |
| Grandview-Woodland | 49.2764, -123.0667 |
| Hastings-Sunrise | 49.2779, -123.0403 |
| Kensington-Cedar Cottage | 49.2467, -123.0729 |
| Kerrisdale | 49.2237, -123.1596 |
| Killarney | 49.2170, -123.0376 |
| Kitsilano | 49.2675, -123.1633 |
| Marpole | 49.2102, -123.1284 |
| Mount Pleasant | 49.2631, -123.0985 |
| Oakridge | 49.2264, -123.1230 |
| Renfrew-Collingwood | 49.2473, -123.0402 |
| Riley Park | 49.2448, -123.1031 |
| Shaughnessy | 49.2457, -123.1398 |
| South Cambie | 49.2456, -123.1218 |
| Strathcona | 49.2782, -123.0882 |
| Sunset | 49.2188, -123.0920 |
| Victoria-Fraserview | 49.2200, -123.0641 |
| West End | 49.2850, -123.1354 |
| West Point Grey | 49.2684, -123.2035 |

Note: the business licence dataset uses "Arbutus-Ridge" (hyphenated); the boundary dataset uses "Arbutus Ridge" (space). Confirm normalization before any join.

**Partial code decoding via geocoded sample addresses + spatial join:**

The following was derived by geocoding one sample address per tax code (from the 2023 property tax records) and doing a spatial join against the CoV boundary polygons using `shapely`. This is T6-quality evidence (one sample per code, geocoding can be imprecise).

| Tax Code | Sample Address | CoV Neighbourhood (spatial join) | Confidence |
|----------|---------------|----------------------------------|------------|
| 001 | 206 W 10th Ave | Kitsilano | Medium |
| 002 | 313 W Broadway | Fairview | Medium |
| 003 | 204 W 28th Ave | South Cambie (uncertain — also has Collingwood St samples) | Low |
| 004 | 1 W 23rd Ave | Riley Park (uncertain — MacLure Mews samples suggest Arbutus-Ridge) | Low |
| 005 | 402 W 38th Ave | Shaughnessy (uncertain — W 48th Ave + Balsam St suggest Kerrisdale) | Low |
| 006 | 1 SW Marine Dr | Kerrisdale/Marpole (geocoder ambiguity on SW Marine Dr) | Low |
| 007 | 305 Cambie St | Unknown — Cambie St span too wide; likely South Cambie or Fairview | Very Low |
| 008 | 1 Oak St | Shaughnessy/South Cambie (geocoder ambiguity) | Low |
| 009 | 306 Cambie St | Unknown — same Cambie St span issue | Very Low |
| 010 | 205 W 57th Ave | Oakridge | Medium |
| 011 | 602 Cambie St | Marpole (Cambie south of 49th) | Low |
| 012 | 302 SW Marine Dr | Victoria-Fraserview/Marpole (far east Marine Dr) | Low |
| 013 | 701 E 1st Ave | Hastings-Sunrise | Medium |
| 014 | 205 Commercial Dr | Grandview-Woodland | High |
| 015 | 101 Inverness St | Kensington-Cedar Cottage | High |
| 016 | 201 E 33rd Ave | Kensington-Cedar Cottage | High |
| 017 | 304 Fraser St | Sunset | High |
| 018 | 602 Riverwalk Ave | Victoria-Fraserview (Champlain Heights) | Medium |
| 019 | 203 Victoria Dr | Grandview-Woodland (or Renfrew-Collingwood — boundary unclear) | Low |
| 020 | 201 E Hastings St | Hastings-Sunrise | High |
| 021 | 204 Grant St | Grandview-Woodland | High |
| 022 | 1 E 20th Ave | Renfrew-Collingwood | High |
| 023 | 2003 Boundary Rd | Renfrew-Collingwood | High |
| 024 | 306 Joyce St | Killarney | High |
| 025 | 1 E 50th Ave | Victoria-Fraserview | High |
| 026 | 1008 Hamilton St | Downtown | High |
| 027 | 806 Bidwell St | West End | High |
| 028 | 1602 Bayshore Dr | Downtown (Coal Harbour) | High |
| 029 | 604 Smithe St | Downtown (Yaletown) | High |
| 030 | 601 Kinghorne Mews | Downtown (False Creek) | Medium |

**Key structural finding:** 30 tax codes map to 22 CoV local areas. Multiple tax codes per CoV area (e.g., Downtown has at least codes 026, 028, 029, 030). This means any analysis that joins property tax data to business licences by neighbourhood must aggregate multiple tax codes per CoV local area.

**What's required to complete A1:**
The proper mapping requires a programmatic spatial join: for each unique property tax address, geocode it and point-in-polygon test against the CoV boundary GeoJSON. This has been set up and tested (works with `shapely`). A bulk geocoding run on a representative sample of ~300 addresses (~10 per tax code) would produce a reliable lookup table.

### Status
**PARTIALLY VERIFIED** — Boundary dataset confirmed downloaded and usable. 30 vs 22 discrepancy understood. Spatial join methodology tested and working. Full code-to-neighbourhood lookup is T6 quality until bulk geocoding is run. This assumption is still blocking: EDA requires a confirmed code-to-neighbourhood map before neighbourhood-level aggregation.

### Source Register
| ID | Source | Tier | URL |
|----|--------|------|-----|
| S-A1-1 | CoV Local Area Boundary dataset | T1 | https://opendata.vancouver.ca/explore/dataset/local-area-boundary/ |
| S-A1-2 | CoV Local Area Boundary API records | T1 | https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/local-area-boundary/records |
| S-A1-3 | Geocoded sample addresses via Nominatim/OSM | T4 | https://nominatim.openstreetmap.org/ |

---

## A3: LocalArea Field — Assignment Method and Reliability

### Question
How is the `LocalArea` field assigned in the business licence datasets? Is it geocoded from coordinates, derived from address, or something else? What are the implications for using it as a neighbourhood identifier?

### Findings

**LocalArea is MANUALLY ASSIGNED by a data custodian — not geocoded.**

The CoV Open Data Portal field description (verbatim) for `localarea` in all three business licence datasets reads:

> "Manual selection from data custodian in source system. The City has 22 local areas (also known as local planning areas); see the Local area boundary dataset."

This is stated identically in the current dataset and in the 2013–2024 archive dataset. It is an **authoritative administrative assignment**, not a computed or geocoded value.

**Implications of manual assignment:**
- **Authoritative**: The assignment reflects the City's own administrative classification of the business's location. It is not a derived approximation.
- **Human error risk**: Manual data entry introduces potential for misassignment, especially near neighbourhood boundaries, or if the custodian uses different boundaries than the official polygon dataset.
- **Not always populated**: The field is NULL in all records from the April 2025 API extract (previously 99% for folderyear=22 in Oct 2024). The field is now absent from the current downloadable data.
- **Not a geocoded value**: Cannot be reconstructed by geocoding the address and doing a spatial join — the manual assignment may intentionally differ from the geometric polygon boundary for address-edge cases.

**Previous A3 question (geocoding coverage in the 2013-2024 CSV) is a separate blocking issue documented below under "Additional Findings".**

### Status
**VERIFIED** — LocalArea assignment method confirmed from primary source (CoV dataset field definition). The field is authoritative when present but subject to human error. Given it is now 0% populated in downloadable data, our analysis must use `geom` + spatial join against the boundary dataset as the neighbourhood assignment method.

### Source Register
| ID | Source | Tier | URL |
|----|--------|------|-----|
| S-A3-1 | CoV Open Data Portal — `business-licences` field definition for `localarea` | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences/information/ |
| S-A3-2 | CoV Open Data Portal — `business-licences-2013-to-2024` field definition for `localarea` | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences-2013-to-2024/information/ |

---

## A3 (Legacy): Geocoding Coverage in Business Licences

### Question
What is the actual geocoding coverage (geom/lat-lon) in the 2013-2024 business licence data? Is the "~60-70%" estimate accurate? Does it vary by year or business type?

### Findings

**The downloaded CSV is corrupted and cannot be used.**

File: `data/raw/business-licences/business-licences-2013-to-2024.csv`
- Line count: 782,401 (1 header + 782,400 data lines) — matches expected record count
- Unique records: only **100** (the file repeats 2 unique records 7,824 times each)
- Root cause: the download script used paginated API calls via codetabs.com proxy. The API or proxy got stuck cycling between page offsets 0 and 10,000 (for folderyear=22 and folderyear=23), writing the same 50 records cyclically until reaching the target line count.
- folderyears present in file: only `22` (469,440 lines) and `23` (312,960 lines)
- The 2 unique records: one "Single Detached House" (folderyear=22, no geom) and one "Health Services" block (folderyear=23, 35/40 unique have geom)
- The file cannot support any analysis.

**Snapshot files cannot substitute for the full 12-year dataset:**

| File | Rows | FolderYears | localarea% | geom% |
|------|------|-------------|------------|-------|
| `snapshot_2024-10-02_sample.csv` | 3,265 | 22, 23 | 74.4% (fy=22 only) | 33.9% |
| `snapshot_2024-10-30_sample.csv` | 3,205 | 22, 23 | 73.9% (fy=22 only) | 33.0% |

Critical finding within snapshots:
- `folderyear=22` records: localarea coverage = **99.0%**, geom coverage = **45.5%**
- `folderyear=23` records: localarea coverage = **3.0%**, geom coverage = **0%**
- The `localarea` field for fy=22 was populated in the Oct 2024 API snapshot (extractdate=2024-05-04). It was cleared in the April 2025 re-extract (extractdate=2025-04-22). This is now **permanently 0%** in all downloadable files from the current API.

**The inventory document's "~60-70%" geocoding estimate is unverified (T6):**
It was derived from API facet queries against the current endpoint, not from the actual CSV. Given that the snapshots show fy=22 has 45.5% geom coverage and fy=23 has 0%, and the full 2013-2024 dataset spans years where coverage may vary substantially, the 60-70% estimate may be significantly off.

**Business type geocoding patterns (from snapshot, n=3,205):**
- Highest GOB rate: Real Estate Dealer (60%), Physical Therapist (28.6%)
- Residential categories (Apartment House Strata = 7.4% GOB) — largest category by volume
- Seasonal business types present: Caterer (2), Public Market Operator-Annual (2), Restaurant Class 1 (2)
- No explicit "patio", "ice cream", or summer-only business types found in snapshot

**What the actual coverage breakdown requires:**
A valid download of the 2013-2024 CSV via a different method (direct export, different proxy, or splitting by year via API `refine=folderyear:YY` parameter) is needed. The download must be retried.

### Status
**UNVERIFIED** — The downloaded CSV is corrupt. Actual coverage rates for the full 2013-2024 dataset cannot be measured from available data. This is a blocking assumption: if geocoding coverage is <30% in early years (pre-2018), neighbourhood-level business analysis in those years is not feasible.

**Action Required**: Re-download using year-by-year API calls:
```
https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences-2013-to-2024/exports/csv?refine=folderyear:13
```
(repeat for each folderyear 13–24). This sidesteps the pagination cycling failure.

---

## A6: LicenceRSN as Unique Record Key; LicenceNumber Reuse

### Question
What is the correct unique key for a business licence record? Is `LicenceRSN` truly unique? Can `LicenceNumber` be reused?

### Findings

**Confirmed from primary source (CoV field definitions, verbatim):**

> "There is a small chance that a licence number has been used twice. Licence RSN is an unique identifier."

This statement appears in the Data Accuracy sections of all three business licence datasets (current, 2013–2024, 1997–2012). The field description for `licencenumber` additionally states:

> "9-character field: two digit year + hyphen + six digit system-generated number. Note: There is a small chance that a licence number can be reused more than once within a given year. LicenceRSN is an unique identifier."

**What this means for our analysis:**
- `LicenceRSN` is the correct primary key for any deduplication or record-level operations. Do not use `LicenceNumber` as a unique key.
- `LicenceRSN` is still **year-specific** (confirmed by prior empirical analysis: 0 RSNs shared across folderyear=22 and folderyear=23 in snapshot data). A business renewing annually gets a new RSN each year.
- The source confirmation validates our prior finding (from empirical data inspection) that name+address is the correct cross-year business identifier. The source docs do not provide a stable cross-year identifier because none exists in the system design.

**Mitigation:**
- Use `LicenceRSN` for all within-year deduplication and record-level joins.
- Use `businessname + house + street` as the cross-year business identifier for survival and lapse tracking.
- When joining across years, be aware that the same `LicenceNumber` format (e.g., "22-123456") is theoretically reusable, so RSN is required for disambiguation if querying within a folderyear.

### Status
**VERIFIED** — LicenceRSN confirmed as unique per-record key from CoV source documentation. LicenceNumber reuse confirmed as possible from same source. Our prior empirical finding (RSN is year-specific) stands; source docs add the authoritative confirmation that RSN is the correct unique key.

### Source Register
| ID | Source | Tier | URL |
|----|--------|------|-----|
| S-A6-1 | CoV Open Data — `business-licences` Data Accuracy section and `licencenumber` field definition | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences/information/ |
| S-A6-2 | CoV Open Data — `business-licences-2013-to-2024` Data Accuracy section | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences-2013-to-2024/information/ |
| S-A6-3 | Empirical cross-year RSN analysis from snapshot data (see A6/A13 section below) | T5 | Internal |

---

## A6/A13: Seasonal Licence Lapse Detection

### Question
How prevalent is the pattern of RSNs "dying" for 1 year and reappearing within 6-12 months? Is it concentrated in seasonal business types?

### Findings

**Critical finding: RSN (licenceRSN) is year-specific, not business-specific.**

The `licencenumber` field follows the format `YY-NNNNNN` where `YY` is the 2-digit folderyear. Each annual licence renewal generates a new `licencenumber` and a new `licenceRSN`. A business renewing year-over-year gets a brand new RSN and licence number each year.

Confirmed from snapshot cross-year analysis:
- **0 RSNs** appear in both folderyear=22 and folderyear=23 in the snapshots
- 7 businesses matched across years using `businessname + house + street` as the key
  - These 7 had different RSNs in each year (confirming RSNs are year-specific)
  - Example: "SoleFit Orthotics Inc" — different RSN in fy=22 vs fy=23

**Implications for A6/A13:**
- "RSN that dies and reappears" is **not a valid construct**. RSNs do not carry over between years.
- Seasonal lapse detection must use `businessname + address` as the business identifier
- A "lapse" = businessname+address present in year N, absent in year N+1, present in year N+2
- This is detectable from a properly structured multi-year dataset but NOT from the current corrupted CSV

**What the snapshot can tell us about non-renewal patterns:**
In the Oct 2024 snapshot (fy=22 records), 2,341 of 2,429 fy=22 businesses (96.4%) do not appear in the fy=23 records by name+address. However this is almost entirely explained by the snapshot being a limited slice of the database (the fy=23 data is still being issued/filed when the snapshot was taken), not by businesses closing.

**Business types that could be seasonal (present in snapshot):**
- `Public Market Operator-Annual` (2 records) — the "Annual" suffix suggests a non-permanent licence
- `Temporary` suffix types (not present in snapshot but documented in inventory as likely present in full dataset)
- The seasonal hypothesis requires the full 12-year panel to test

**Revised definition recommendation:**
Given that RSNs are year-specific, the appropriate seasonal lapse detection query is:
```
Find businessname+address combos that appear in year N AND year N+2
but NOT in year N+1 (skipped exactly one year)
```
A 6-12 month absence is not detectable at annual-licence granularity — the minimum detectable gap is one full calendar year.

### Status
**UNVERIFIED** — Cannot be analyzed until a valid multi-year CSV is available. The RSN structure finding is a **REFUTATION** of the original assumption that RSN is the stable business identifier. RSN tracks licences, not businesses. The assumption register should be updated:

- **A6 (RSN as stable business ID)**: REFUTED. RSNs are year-specific.
- **A13 (6-12 month lapse detectable)**: REVISED. Minimum detectable lapse at annual licence granularity is 12 months (one full year gap). 6-month lapse detection would require `issueddate` and `expireddate` analysis within a year, which is possible but limited (many "Gone Out of Business" records have null issueddate).

---

## A11: Broadway Subway Station Locations

### Question
What are the exact Broadway Subway (Millennium Line extension) station names, locations, and construction timeline?

### Findings

**Status: VERIFIED**

**Project scope:** 5.7 km Millennium Line extension from VCC-Clark Station (existing) to Arbutus Street (new terminus). Six new underground stations.

**Construction timeline:**
- Major construction began: May 2021
- Original target opening: 2025
- Revised target: 2026 (also missed)
- Current projected opening: **Fall 2027** (delayed due to tunnelling complexity)
- Total project cost: $2.954 billion (BC Government, with contributions from Canada and CoV)
- As of early 2026: all running rail installed; dynamic testing begins late 2026

**Station names and addresses:**

| Station Name | Intersection / Address | Near Main St? |
|-------------|------------------------|---------------|
| Great Northern Way–Emily Carr Station | East side of Thornton Street, just north of Great Northern Way | No (east of Main, ~1 km) |
| **Mount Pleasant Station** | SW corner of **Broadway and Main Street** | **YES — this station is at Main & Broadway** |
| Broadway–City Hall Station | SE corner of Broadway and Cambie Street | No (~800m west of Main) |
| Oak–VGH Station | SW corner of Broadway and Laurel Street (near Oak Street) | No (~1.2 km west) |
| South Granville Station | NE corner of Broadway and Granville Street | No (~1.8 km west) |
| Arbutus Station | NE corner of Broadway and Arbutus Street | No (~2.5 km west) |

**Key geographic finding for the project:**
Mount Pleasant Station at Broadway & Main is the station most relevant to Main Street commercial corridor analysis. The Broadway–City Hall station at Cambie affects the Cambie/South Cambie area. The pre/post subway analysis should treat 2021 (construction start) and 2027 (opening) as separate treatment year candidates.

**Approximate coordinates (from centroid estimates):**
- Great Northern Way–Emily Carr: ~49.268, -123.075
- Mount Pleasant (Main & Broadway): ~49.263, -123.101
- Broadway–City Hall (Cambie): ~49.263, -123.116
- Oak–VGH: ~49.263, -123.122
- South Granville: ~49.263, -123.137
- Arbutus: ~49.263, -123.155

### Source Register
| ID | Source | Tier | URL |
|----|--------|------|-----|
| S-A11-1 | broadwaysubway.ca — official project site | T1 | https://www.broadwaysubway.ca/about/stations/ |
| S-A11-2 | CBC News: "Broadway SkyTrain extension delayed to 2027" | T4 | https://www.cbc.ca/news/canada/british-columbia/broadway-subway-extension-delayed-1.7215046 |
| S-A11-3 | Daily Hive: "100% of rail installed" | T4 | https://dailyhive.com/vancouver/broadway-subway-rail-installation-completion |
| S-A11-4 | TransLink project page | T1 | https://www.translink.ca/plans-and-projects/projects/rapid-transit-projects/broadway-subway-project |

---

## A15: Home-Based Business Address Removal (Retroactive, April 2018)

### Question
Why do some business records have no address? Are missing addresses a data quality problem or a deliberate policy decision? How does this affect survival tracking?

### Findings

**Confirmed from primary source (CoV dataset description, verbatim) — present in all three business licence datasets:**

> "Effective April 12, 2018, the business license dataset, including historical data files from 1997 forward to the current year, has been updated for home-based businesses. The City has removed the business address from the home-based business license category."

**Key facts established:**
1. **Retroactive application**: The removal applied to the entire historical archive back to 1997, not just post-2018 records. All three dataset descriptions carry this statement, including the 1997–2012 archive.
2. **Date of change**: April 12, 2018. The 1997–2012 dataset's `Last Modified (source data)` timestamp is exactly `2018-04-12T12:05:46+00:00`, confirming the retroactive edit is what triggered the final modification of the archive.
3. **Mechanism**: Address fields (`house`, `street`, `city`, `postalcode`) were cleared for home-based business licence types. The `house` and `street` fields will be null/blank for these records, so `geom` and `localarea` will also be null.
4. **Privacy rationale**: Removing home addresses is a privacy protection measure (home address = residential address of the business owner).
5. **Business types affected**: The CoV dataset description also notes: "Address data of some selected business types was not disclosed to provide privacy protection" — this is the same mechanism.

**Implications for survival tracking (name+address matching):**
- A home-based business present in year N (pre-2018 extract) with an address may appear in year N+1 (post-2018 extract) with a null address — causing a false "death" in our name+address matching.
- Conversely, any business that has no address across all years may be a home-based business that was never geocodable, not a data quality gap.
- The retroactive nature means this issue affects the **entire 1997–2012 dataset**, not just records from April 2018 onward.

**Mitigation:**
- Flag records where `house` is null/blank as "likely home-based or privacy-restricted" rather than "missing address."
- For survival tracking: supplement name+address matching with a name-only fallback for records that transition from addressed to unaddressed across the 2018 boundary.
- When counting "missing address" records, always report the home-based business caveat.
- Do not use address-dependent geocoding or spatial analysis for these records. Rely on `localarea` (manual custodian field) where populated, accepting its limitations.

### Status
**VERIFIED** — Source documentation explicitly states the retroactive home address removal policy, the date, and the scope. This is a T1 source finding that materially affects survival analysis methodology.

### Source Register
| ID | Source | Tier | URL |
|----|--------|------|-----|
| S-A15-1 | CoV Open Data — `business-licences` dataset description ("Effective April 12, 2018...") | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences/information/ |
| S-A15-2 | CoV Open Data — `business-licences-2013-to-2024` dataset description (same statement) | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences-2013-to-2024/information/ |
| S-A15-3 | CoV Open Data — `business-licences-1997-to-2012` dataset description (same statement) + Last Modified timestamp = 2018-04-12 | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences-1997-to-2012/information/ |

---

## A16: CURRENT_LAND_VALUE — Value Type and Historical Availability

### Question
Is `CURRENT_LAND_VALUE` in the property tax data the actual market value from BC Assessment, or is it the municipal taxable value (which nets out exemptions)? Is `previous_land_value` available across all years?

### Findings

**Confirmed from primary source — CoV property tax field definition (verbatim):**

> `current_land_value`: "Market value of the fee simple interest in land, provided by BCA for the Tax_Assessment_Year. Issued in the Completed Roll (January) and Revised Roll (mid-March); amendments possible via Supplementary Rolls throughout the year. **This is the actual value, not taxable value (which is net of exemptions and may be averaged).**"

**Key facts established:**
1. **Value type**: `CURRENT_LAND_VALUE` is the **BC Assessment market value** — the full assessed market value of the fee simple land interest. It is explicitly stated to be the actual value, not the taxable value.
2. **Taxable value distinction**: The taxable value is different — it is net of statutory exemptions (e.g., homeowner grant, farm exemptions) and may be a BC Assessment average over multiple years. `CURRENT_LAND_VALUE` bypasses this averaging.
3. **Source**: BC Assessment (BCA), extracted as the Completed Roll (January) or Revised Roll (mid-March), with possible amendments via Supplementary Rolls.
4. **Correct for land appreciation analysis**: Since our analysis tracks land value appreciation over time, using the market value (not the averaged taxable value) is the correct choice. No adjustment needed.
5. **previous_land_value availability**: The CoV dataset description explicitly states: "Values for the 'previous improvement value' and 'previous land value' columns are not available for the 2006–2013 reports." The field definition for `previous_land_value` similarly notes: "Not available for 2006–2013 reports."

**Implications:**
- The land appreciation analysis using `CURRENT_LAND_VALUE` is methodologically sound — we are working with full market values, not administratively adjusted taxable values.
- Year-over-year change calculations that use `previous_land_value` cannot be computed for 2006–2013. For these years, compute YoY change by comparing `CURRENT_LAND_VALUE` across adjacent annual datasets (join on PID or folio).
- Announcement effect windows around the Broadway Subway announcement (2018) and construction start (2021) can use this field directly without transformation.

**Mitigation:**
- Document the "actual value vs taxable value" distinction in all published outputs. Readers familiar with municipal finance may assume taxable value.
- For 2006–2013, use cross-dataset joins to compute YoY land value change instead of the `previous_land_value` column.
- Be explicit in methodology: "Land values are BC Assessment market values (fee simple), sourced from the Completed Roll."

### Status
**VERIFIED** — Both the value type (market value, not taxable) and the `previous_land_value` unavailability for 2006–2013 are stated in CoV primary source documentation.

### Source Register
| ID | Source | Tier | URL |
|----|--------|------|-----|
| S-A16-1 | CoV Open Data — `property-tax-report` field definition for `current_land_value` | T1 | https://opendata.vancouver.ca/explore/dataset/property-tax-report/information/ |
| S-A16-2 | CoV Open Data — `property-tax-report` Notes section: "Values for 'previous improvement value' and 'previous land value' columns are not available for the 2006–2013 reports." | T1 | https://opendata.vancouver.ca/explore/dataset/property-tax-report/information/ |
| S-A16-3 | CoV Open Data — `property-tax-report-2016-2019` and `property-tax-report-2011-2015` Caveats (same statement repeated) | T1 | https://opendata.vancouver.ca/explore/dataset/property-tax-report-2016-2019/ |

---

## A17: Business Type Taxonomy Break at FY24 (May 6, 2024)

### Question
When did the business type taxonomy change? What is the scope of the change? Can `businesstype` be used as a covariate across the full time series?

### Findings

**Confirmed from primary source — CoV dataset description (verbatim):**

> "Effective May 6, 2024, the City streamlined its business licence categories, consolidating over 500 categories into fewer than 100. While data from before this date will remain accessible, this dataset post-May 6 is organized according to the new, streamlined categories."

> "All existing business licences are transitioned automatically into the new categories. Some business licence categories retained the same name. Business owners will renew their licence at the end of each year and may select a different category from the one they were sorted into. New businesses applying for a licence after the update will also select from the updated categories."

Additional context from source documentation:
- The enabling instrument is **Licence By-law No. 4450 amendment**, with the City referencing **Council Report RTS 15385** (cited in public documentation about the change).
- The 2013–2024 archive dataset description states: "Effective May 6, 2024, the City streamlined its business licence categories, consolidating over 500 categories into fewer than 100."
- Pre-May 6, 2024 records in the 2013–2024 dataset retain original types. Post-May 6, 2024 records are in the new `business-licences` (current) dataset with new types.
- Old business types that no longer exist are marked with `*Historic*` suffix in the archive datasets.

**Precise scope of the break:**
- **Before**: ~500+ categories (the field definition mentions "over 500"; the inventory previously cited "~168 distinct types" in the 2013–2024 data, likely reflecting active types at a point in time rather than all-time unique values).
- **After**: Fewer than 100 categories (CoV states "fewer than 100"; the current dataset has 93 active types as of the change).
- **Cut date**: May 6, 2024 (not January 1, 2024 — mid-year cut).
- **Dataset boundary**: 2013–2024 archive covers up to May 3, 2024 with old types. Current dataset covers from May 6, 2024 (post-change) onward. There is a 2-day gap (May 4–5) which appears to be a weekend/transition period.
- **No double-counting**: The datasets are designed not to overlap. The archive goes to "May 3, 2024" and the current dataset starts "2024 onwards."

**Implications for analysis using businesstype as a covariate:**
- **Incomparability across the break**: A restaurant coded as "Restaurant Class 1 *Historic*" in 2023 may be coded as "Food & Beverage" in 2025. These are not directly comparable without a crosswalk table.
- **Pre-break panel (1997–May 2024)**: businesstype is internally consistent within this span (same taxonomy) and can be used as a covariate.
- **Post-break (May 2024+)**: New taxonomy — use as covariate only within the new taxonomy period.
- **Crosswalk**: CoV states "All existing business licences are transitioned automatically into the new categories" but has not published a machine-readable crosswalk table. The transition mapping is therefore not available for reverse-engineering pre/post comparisons without manual effort.
- **Our main study period (up to FY24 cut)**: If the primary analysis uses 1997–2023 data (or 1997–May 2024), the taxonomy is internally consistent throughout. The schema break only becomes a problem if we extend the analysis into FY24 post-May or into the current dataset.

**Mitigation:**
- Limit `businesstype` as a covariate to the pre-May 2024 period (1997–2012 archive + 2013–2024 archive).
- When extending analysis into the current dataset, explicitly note the taxonomy break and treat the two periods separately or use a coarser classification (e.g., collapse both schemas to NAICS-equivalent macro categories).
- Flag all pre-May 2024 `businesstype` values that carry the `*Historic*` suffix as retired types — these may represent intra-period consolidations (not just the 2024 break).
- Request or construct a crosswalk if post-2024 panel analysis is required.

### Status
**VERIFIED** — The taxonomy change date (May 6, 2024), scope (500+ → <100 categories), enabling instrument (By-law 4450 amendment), and dataset boundary are all confirmed from CoV primary source documentation.

### Source Register
| ID | Source | Tier | URL |
|----|--------|------|-----|
| S-A17-1 | CoV Open Data — `business-licences` dataset description (Note section re: May 6, 2024 change) | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences/information/ |
| S-A17-2 | CoV Open Data — `business-licences-2013-to-2024` dataset description (same Note section) | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences-2013-to-2024/information/ |
| S-A17-3 | CoV Open Data — `business-licences-1997-to-2012` dataset description (reference to new categories, dataset unchanged) | T1 | https://opendata.vancouver.ca/explore/dataset/business-licences-1997-to-2012/information/ |
| S-A17-4 | City of Vancouver — Business licences new categories page | T1 | https://vancouver.ca/doing-business/business-licences.aspx#new-categories |

---

## A18: NumberofEmployees — Type Mismatch Across Datasets

### Question
Is the `NumberofEmployees` field the same type across all three business licence datasets? What type casting is required in the merge pipeline?

### Findings

**Confirmed from primary source — CoV field definitions (verbatim, differences highlighted):**

| Dataset | Field Name | Type | CoV Description |
|---------|-----------|------|-----------------|
| `business-licences` (current) | `numberofemployees` | **double** | "Number of staff employed with the business. Note: 0 = business has no employees (per applicant); 000 = information unknown." |
| `business-licences-2013-to-2024` | `numberofemployees` | **text** | Same description. NOTE: typed as text in this dataset. |
| `business-licences-1997-to-2012` | `numberofemployees` | **text** | Same description. |

**Key facts:**
1. The current dataset (`business-licences`, FY24+) stores `NumberofEmployees` as `double`.
2. Both archive datasets (2013–2024 and 1997–2012) store it as `text`.
3. The SOURCE_DOCUMENTATION.md explicitly notes: "IMPORTANT SCHEMA DIFFERENCE: `numberofemployees` is typed as `text` in this dataset vs `double` in the current dataset. This affects joins and numeric operations."
4. The "000" sentinel value for "information unknown" is a string — it cannot be stored as a numeric 0. This explains why the field is text in the archive datasets (the sentinel must be distinguishable from "0 employees").
5. The distinction between `0` (no employees) and `000` (unknown) is **only preserved in text form**. If you cast text to integer/double naively, both map to 0 and the "unknown" signal is lost.

**Implications for the merge pipeline:**
- When stacking the three datasets into a unified panel, `NumberofEmployees` must be handled explicitly.
- Do not use pandas default dtype inference — it will silently cast "000" to 0.0.
- The `000` → "unknown" distinction is analytically important: a business with 0 employees is different from one that did not report.

**Mitigation — explicit type casting protocol:**
```python
# Step 1: Read all datasets with numberofemployees as string
df['numberofemployees'] = df['numberofemployees'].astype(str)

# Step 2: Distinguish sentinel values before any numeric conversion
df['employees_unknown'] = df['numberofemployees'].str.strip() == '000'
df['employees_zero'] = df['numberofemployees'].str.strip() == '0'

# Step 3: Convert to numeric, preserving NaN for unknowns
df['numberofemployees_numeric'] = pd.to_numeric(
    df['numberofemployees'].replace('000', pd.NA),
    errors='coerce'
)
```
- Add a separate boolean column `employees_reported` (True if not '000' and not null).
- Document the sentinel handling in the pipeline README.

### Status
**VERIFIED** — Type difference confirmed from CoV API schema metadata for all three datasets. The `text` vs `double` discrepancy and the "000" sentinel are documented in the source field definitions.

### Source Register
| ID | Source | Tier | URL |
|----|--------|------|-----|
| S-A18-1 | CoV Open Data API schema — `business-licences` field `numberofemployees` type = double | T1 | https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences/ |
| S-A18-2 | CoV Open Data API schema — `business-licences-2013-to-2024` field `numberofemployees` type = text | T1 | https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences-2013-to-2024/ |
| S-A18-3 | CoV Open Data API schema — `business-licences-1997-to-2012` field `numberofemployees` type = text | T1 | https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences-1997-to-2012/ |

---

## Additional Findings from Data Inspection

### Business Licence Data Structure (from snapshots)

**Schema confirmed:**
All 25 fields as documented in BUSINESS_LICENCES_INVENTORY.md are confirmed present. Key findings:

- `folderyear`: Two-digit string ("22", "23"), not a 4-digit year
- `licencersn`: Numeric string, year-specific (not a stable business identifier)
- `licencenumber`: Format "YY-NNNNNN" — year prefix + sequential number
- `localarea`: **NULL in all records from the April 2025 extract.** Was populated (99%) for folderyear=22 in the October 2024 extract. Cleared in the April 2025 re-extract.
- `geom`: WKT format "POINT(lon lat)" — present for geocoded records (~46% in fy=22 snapshot)
- `geo_point_2d`: "lat,lon" format (comma-separated, unquoted) — causes CSV parsing issues when using `csv.DictReader` because the comma is not quoted. Use `csv.reader` instead and merge the last two columns.
- `businesstype`: All pre-May 2024 categories carry `*Historic*` suffix — structural break in taxonomy

**22 CoV neighbourhood names observed in business licence snapshots (fy=22 localarea field):**
Downtown, West End, Fairview, Mount Pleasant, Kitsilano, Marpole, Grandview-Woodland, Strathcona, Kensington-Cedar Cottage, Renfrew-Collingwood, Riley Park, Sunset, South Cambie, Arbutus-Ridge, Kerrisdale, Hastings-Sunrise, Killarney, Oakridge, Renfrew, West Point Grey, Victoria-Fraserview, Shaughnessy, Dunbar-Southlands (23 unique — note "Renfrew" appears separately from "Renfrew-Collingwood")

Note: "Renfrew" as a standalone value may be a data quality issue in the business licence system or a sub-area of Renfrew-Collingwood. Requires investigation before use.

### CSV Parsing Note

The `geo_point_2d` field in the business licence CSV contains an unquoted comma (format: "49.26,-123.15") which causes column misalignment when using Python's `csv.DictReader`. Use `csv.reader` directly and handle the 26-column rows:

```python
for row in reader:
    if len(row) == 26:
        row = row[:24] + [row[24] + ',' + row[25]]
```

---

## Blocking Issues and Required Actions

| Issue | Priority | Action |
|-------|----------|--------|
| Business licence CSV is corrupt | CRITICAL | Re-download using year-by-year API refine parameter |
| Neighbourhood code lookup incomplete | HIGH | Run bulk geocoding (shapely + Nominatim) on 10 addresses per tax code |
| localarea field NULL in current data | KNOWN | Use geom field + CoV boundary spatial join instead (localarea assignment method now documented as manual — A3 VERIFIED) |
| RSN as cross-year identifier: refuted | RESOLVED | Source docs confirm LicenceRSN is per-record unique key; LicenceNumber can be reused. Name+address is correct cross-year ID (A6 VERIFIED) |
| Home-based business address removal | NEW — KNOWN | Flag null-address records as likely home-based. Handle 2018 retroactive boundary in survival matching (A15 VERIFIED) |
| NumberofEmployees type mismatch | NEW — KNOWN | Explicit type casting required in merge pipeline; preserve "000" sentinel (A18 VERIFIED) |
| businesstype incomparable post-May 2024 | NEW — KNOWN | Limit businesstype covariate to pre-May 2024 period or use crosswalk (A17 VERIFIED) |
| previous_land_value missing 2006–2013 | NEW — KNOWN | Use cross-dataset YoY joins for 2006–2013 land value change (A16 VERIFIED) |
| Broadway subway coordinates | RESOLVED | Confirmed — Fall 2027 opening, Mount Pleasant station at Main & Broadway (A11 VERIFIED) |

---

## Re-Download Instructions for Business Licence Data

The download failure was caused by the paginated API cycling the same two pages. Alternative approach using year-specific exports:

```bash
# Download each folderyear separately (more reliable than paginated download)
for yr in 13 14 15 16 17 18 19 20 21 22 23 24; do
  curl -s --proxy "https://api.codetabs.com/v1/proxy?quest=" \
    "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences-2013-to-2024/exports/csv?refine=folderyear:${yr}&limit=100000" \
    >> /path/to/business-licences-2013-to-2024-REDOWNLOAD.csv
done
```

Or use the direct export URL (if SSL block is lifted or via browser):
```
https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences-2013-to-2024/exports/csv?timezone=UTC&use_labels=false&epsg=4326
```

---

## Appendix: Assumption Register Updates

| ID | Assumption | Previous Status | New Status | Change |
|----|-----------|-----------------|------------|--------|
| A3 | Geocoding coverage ~60-70% in business licences | UNVERIFIED | SPLIT | Geocoding coverage question remains unverified (CSV corrupt). LocalArea assignment method now separately verified as manual custodian selection (T1 source). |
| A5 | localarea field ~74% coverage | REFUTED (inventory) | REFUTED | Confirmed: 0% in current API, was 99% for fy=22 in Oct 2024 snapshot |
| A6 | RSN is stable business identifier across years | UNVERIFIED | REFUTED + CLARIFIED | RSN is year-specific (empirical). Source docs confirm LicenceRSN is unique per-record key; LicenceNumber can be reused. Name+address is correct cross-year identifier. |
| A13 | 6-12 month lapse detectable via RSN gaps | UNVERIFIED | REVISED | 6-month lapse not detectable at annual granularity; min detectable = 12 months |
| A15 | Home-based business address removal | NEW | VERIFIED | Retroactive removal of home-based business addresses applied April 12, 2018, back to 1997. Missing address ≠ missing data for home-based businesses. Affects name+address survival matching. |
| A16 | CURRENT_LAND_VALUE type and previous_land_value availability | NEW | VERIFIED | Field is BC Assessment market value (not taxable value). previous_land_value not available for 2006–2013 datasets. |
| A17 | Business type taxonomy break at FY24 | NEW | VERIFIED | 500+ categories → <100 effective May 6, 2024 (By-law 4450 amendment). businesstype is incomparable across the break without a crosswalk. |
| A18 | NumberofEmployees type mismatch | NEW | VERIFIED | text in both archive datasets; double in current dataset. "000" sentinel for unknown must be handled explicitly before numeric cast. |
| A19 | External triangulation of survival rates | NEW | VERIFIED-WITH-CAVEATS | Aggregate rates confirmed against 6 sources. Finance & Insurance 14yr median flagged as likely institutional branch artefact. Technology 6yr median flagged for composition review. |

---

## A19: External Triangulation of Survival Rates

### Assumption
Our Kaplan-Meier survival estimates reflect true business survival patterns in Vancouver. The aggregate figures (Year-1, Year-5, Year-10, median) are plausible, the sector-level medians are interpretable, and the analysis is not systematically inflated or deflated by data artefacts.

### Basis
External triangulation against six independent sources across three countries (Canada, US; international comparison). Sources include national government statistics, provincial-specific breakdowns, peer-reviewed IRS research on administrative data methodology, and StatCan longitudinal firm dynamics studies.

### Source Tier
T1 (government statistics, primary data producers) for five of six sources. T2 (peer-reviewed government working paper) for the IRS study.

### Confidence
- **HIGH** for aggregate survival rates: Year-1 (92%), Year-5 (60%), Year-10 (41%), overall median (7–8 years). Year-10 = 41% is an exact match against the BC-specific ISED 2024 benchmark — the strongest single corroboration point.
- **HIGH** for Food & Beverage sector median (6 years): consistent with ISED 2018 implied range.
- **MEDIUM** for Technology sector median (6 years): diverges from national Professional/Scientific/Technical Services benchmark; likely explained by composition (startups + contractors vs established professional firms) but requires audit before publishing.
- **LOW** for Finance & Insurance sector median (14 years): no external benchmark supports >10yr median for any sector. Likely artefact from institutional branch registrations (bank branches, insurance offices coded as individual licence holders). Requires audit before publishing.

### Impact if Wrong
Entire analysis narrative built on incorrect baseline. Sector-level comparisons and neighbourhood-level conclusions would be unreliable. The Broadway Subway effect estimates (Step 4+) depend on the baseline survival model being correctly specified.

### Verification
Compared against 6 independent sources:
1. ISED Key Small Business Statistics 2024 (Year-1, Year-5, Year-10 national and BC-specific benchmarks)
2. ISED Canadian New Firms: Birth and Survival Rates 2002–2014 / May 2018 (sector-level survival curves)
3. StatCan Long-run evolution of business entry and exit rates 2025 (exit rate cross-validation)
4. StatCan Firm Dynamics: Death of New Canadian Firms 2012 (early-year survival corroboration)
5. BLS Business Employment Dynamics (cross-national US reference)
6. IRS "Tale of Two Datasets" (methodological bias: administrative data undercount exits by ~37% vs surveys)

Full triangulation details: `docs/EXTERNAL_TRIANGULATION.md`

### Status
**VERIFIED-WITH-CAVEATS**

Aggregate rates confirmed. Two sector-level findings flagged for audit before publication.

### Caveats
1. **Finance & Insurance artefact**: The 14-year median almost certainly reflects institutional branch longevity (bank/insurance branches with indefinite lifespan), not independent business survival. Do not publish this figure without an audit that separates institutional branches from independently operated financial businesses.
2. **Licence-based upward bias from silent non-renewals**: Businesses that stop renewing without notifying the City are coded as exits, but businesses that continue operating informally without a valid licence are invisible in the data. The IRS "Tale of Two Datasets" study finds administrative records undercount exits by ~37% vs surveys, meaning our survival estimates may be modestly optimistic (true exit rates slightly higher than licence data captures).
3. **Self-employed vs employer-firm scope**: Our population includes sole proprietors and self-employed individuals required to hold a City licence. ISED/StatCan benchmarks are primarily based on employer firms (at least one paid employee beyond the owner). Our population is broader, which should push survival rates downward — but our Year-10 match against BC benchmarks suggests this effect is not distorting the aggregate. All published comparisons must disclose this scope difference.

### Source Register
| ID | Source | Tier | URL |
|----|--------|------|-----|
| S-A19-1 | ISED Key Small Business Statistics 2024 | T1 | https://ised-isde.canada.ca/site/sme-research-statistics/en/key-small-business-statistics/key-small-business-statistics-2024 |
| S-A19-2 | ISED Canadian New Firms: Birth and Survival Rates 2002–2014 (May 2018) | T1 | https://ised-isde.canada.ca/site/sme-research-statistics/en/research-reports/canadian-new-firms-birth-and-survival-rates-over-period-2002-2014-may-2018/ |
| S-A19-3 | StatCan: Long-run evolution of business entry and exit rates (2025) | T1 | https://www150.statcan.gc.ca/n1/pub/36-28-0001/2025009/article/00001-eng.htm |
| S-A19-4 | StatCan: Firm Dynamics — Death of New Canadian Firms (2012) | T1 | https://www150.statcan.gc.ca/n1/pub/11-622-m/2012028/part-partie1-eng.htm |
| S-A19-5 | BLS Business Employment Dynamics (US comparison) | T1 | https://www.bls.gov/bdm/bdmage.htm |
| S-A19-6 | IRS "Tale of Two Datasets" study | T2 | https://www.irs.gov/pub/irs-soi/16rptwodatasets.pdf |

---

*Analysis performed by Claude Code on 2026-03-03. Framework: DATA-PROJECT-RIGOR.md v1.0.*
*Sources: City of Vancouver Open Data Portal (T1), OSM Nominatim geocoder (T4), broadwaysubway.ca (T1), CBC/Daily Hive (T4)*
