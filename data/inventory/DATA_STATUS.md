# Data Status — Vancouver Property Tax / Business Survival Analysis
**Project**: Vancouver Business Survival Analysis
**Phase**: 0–1 (Data Acquisition + Initial Quality Assessment)
**Last updated**: 2026-03-03
**Analyst**: Claude Code (Desk-Mode Agent)

This file is the single source of truth for which data assets are ready for analysis and which have known issues. Update this file whenever a dataset's status changes.

---

## Data Asset Status Table

| Dataset | File(s) | Rows / Records | Status | Notes |
|---------|---------|---------------|--------|-------|
| Property Tax | `raw/property-tax-report-*.csv` (4 files) | 4.25M total | READY | 2006–2026, 30 cols in 2020+ files (29 in earlier). neighbourhood_code field (001–030). See `DATA_INVENTORY.md`. |
| Business Licences | `raw/business-licences/business-licences-2013-to-2024.csv` | 779,226 | READY | 2013–2024 (folderyears 13–24), ~60K–70K records/year, comma-delimited, UTF-8, ~206 MB on disk. 779,023 unique licencersn. 181 unique businesstype values. Re-downloaded 2026-03-03 using ssl.create_default_context(). |
| Census (2006) | `raw/census/2006_CT/` | ~409 census tracts | READY | XML-parsed. |
| Census (2011) | `raw/census/2011_CT/` | ~480 census tracts | READY | |
| Census (2016) | `raw/census/2016_CT_correct/` | ~520 census tracts | READY | **WARNING**: `raw/census/2016_CT/` contains WRONG data — do not use. Use `2016_CT_correct/` only. |
| Census (2021) | `raw/census/2021_CT/` | ~535 census tracts | READY | |
| CoV Boundaries | `raw/local-area-boundary.geojson` | 22 polygons | READY | 22 CoV local areas, WGS84. Last modified 2023-06-24. Field names: `name`, `geom`, `geo_point_2d`. |
| Neighbourhood Code Lookup | `neighbourhood_code_lookup.csv` | 30 codes | READY (with caveats) | Maps BC Assessment neighbourhood_code (001–030) to CoV local area names. Bulk spatial join on 1,461 stratified-sampled addresses. 18/30 codes are LOW confidence (genuinely span multiple areas). See `NEIGHBOURHOOD_CODE_MAPPING.md`. |
| Address-to-Area | `address_to_area.csv` | 1,461 addresses | READY | BC Geocoder API, 100% geocode success rate. Used to build neighbourhood_code_lookup.csv. |
| Name Normalization | `area_name_normalization.csv` | 22 areas | READY | One known discrepancy: GeoJSON uses "Arbutus Ridge" (space), business licences use "Arbutus-Ridge" (hyphen). Canonical form: "Arbutus Ridge". Normalize before any cross-dataset join on area name. |
| Business Licence Snapshots | `raw/business-licences/snapshot_2024-10-02/`, `snapshot_2024-10-30/` | ~3K each | REFERENCE ONLY | Pre-schema-change snapshots (extractdate=2024-05-04). The only copies with `localarea` populated. localarea coverage: fy=22 ~99%, fy=23 ~3%. Not representative of the full 2013–2024 dataset. |

---

## Key Data Quality Issues

### localarea Field — Permanently NULL in Downloaded Data
The `localarea` field in `business-licences-2013-to-2024.csv` is **100% null** in all records as of the April 2025 re-extract. The City's April 2025 extract cleared all neighbourhood assignments. The only records with localarea populated are in the Oct 2024 snapshots (reference only). **All neighbourhood-level analysis of business licences must use spatial join via `geo_point_2d` + `local-area-boundary.geojson`.**

### geo_point_2d Coverage — UNVERIFIED for Full File
Geocoding coverage rate across the full 779K-row file has not been measured. From snapshot data: fy=22 had ~45.5% coverage, fy=23 had ~0%. The full-dataset coverage rate is a blocking unknown for geocoding-dependent analysis. This must be measured before neighbourhood-level analysis proceeds (see A3 below).

### Neighbourhood Code Lookup — 18/30 Codes Are LOW Confidence
The `neighbourhood_code_lookup.csv` produced by bulk spatial join shows that 18 of 30 BC Assessment neighbourhood codes genuinely span multiple CoV local areas — they cannot be cleanly mapped to a single area. For analysis stratified by CoV local area, use fractional weighting rather than a hard 1-to-1 assignment for LOW confidence codes. See `NEIGHBOURHOOD_CODE_MAPPING.md` for the full distribution tables per code.

### Census 2016 Correct Directory
The `raw/census/2016_CT/` directory contains incorrect data. The correct data is in `raw/census/2016_CT_correct/`. Do not reference `2016_CT/` in any analysis.

---

## Assumption Status Summary

| Assumption | Status | Notes |
|------------|--------|-------|
| A1 (neighbourhood code lookup complete) | VERIFIED | Bulk spatial join complete (1,461 addresses, 100% geocode success). All 22 CoV areas covered. 18/30 codes LOW confidence (multi-area). See `NEIGHBOURHOOD_CODE_MAPPING.md`. |
| A3 (geocoding coverage in business licences) | UNVERIFIED — BLOCKING | geo_point_2d coverage in the 779K-row file has not been measured. Must be checked before geocoding-dependent neighbourhood analysis. |
| A5 (localarea field ~74% coverage) | REFUTED | localarea is 100% null in the April 2025 re-extract. Was populated in Oct 2024 snapshots only. |
| A6 (licenceRSN = stable business identifier) | REFUTED | RSN is year-specific; a new RSN is issued on each annual renewal. Business continuity must be tracked via businessname + address, not RSN. |

Note: PHASE0_CANDIDATES.md and ASSUMPTION_VERIFICATION.md are the authoritative assumption registers. This table reflects status as of 2026-03-03 and is for quick reference only. Do not modify PHASE0_CANDIDATES.md based solely on this file.

---

## Not Yet Acquired

| Dataset | Priority | Notes |
|---------|----------|-------|
| Business Licences 1997–2012 | LOW | 958,899 records. Static (last modified 2018). Extends coverage to pre-2013. Download same way as 2013–2024 file. |
| Property Tax (pre-2006) | LOW | Not available on CoV Open Data in current form. |
| BC Assessment Parcel Data | NOT PLANNED | Folio-to-coordinate lookup not publicly available. |

---

*Updated by Claude Code (Desk-Mode Agent) on 2026-03-03.*
*Framework: DATA-PROJECT-RIGOR.md v1.0.*
