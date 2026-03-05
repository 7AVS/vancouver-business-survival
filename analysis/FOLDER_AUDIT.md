# Folder Audit — van-property-tax

**Audited by**: Claude Code (Desk-Mode Agent)
**Date**: 2026-03-03
**Scope**: Full recursive audit of `/home/aurora/projects/sites/portfolio-projects/van-property-tax/`
**Total files**: 120 regular files + 2 symlinks = 122 entries

---

## 1. Current File Tree

```
van-property-tax/                                          [3.1 GB total]
│
├── analysis/                                              [1012 KB]
│   ├── plots/
│   │   ├── geo_coverage.png                               315 KB  2026-03-03
│   │   ├── lifespan_distribution.png                       73 KB  2026-03-03
│   │   ├── population_by_year.png                         114 KB  2026-03-03
│   │   ├── status_distribution.png                         75 KB  2026-03-03
│   │   ├── step1_baseline_survival.png                    110 KB  2026-03-03
│   │   ├── survival_by_type.png                            79 KB  2026-03-03
│   │   └── survival_curve.png                              75 KB  2026-03-03
│   ├── A15_HOME_BASED_IMPACT.md                            15 KB  2026-03-03
│   ├── BUSINESS_LICENCE_EDA.md                             28 KB  2026-03-03
│   ├── COMMERCIAL_EDA.md                                    9 KB  2026-03-03
│   ├── LAND_VALUE_ANALYSIS.md                               8 KB  2026-03-03
│   ├── MISSING_AREAS_INVESTIGATION.md                      12 KB  2026-03-03
│   ├── PANEL_V2_CHANGELOG.md                                4 KB  2026-03-03  ⚠ SEE ISSUE 1
│   ├── SCOPE_AUDIT.md                                      39 KB  2026-03-03
│   ├── STEP1_BASELINE_SURVIVAL.md                           6 KB  2026-03-03
│   ├── SURVIVAL_TRACKING_VALIDATION.md                     12 KB  2026-03-03
│   ├── business-survival-vancouver.ipynb                   10 KB  2026-03-03
│   └── survival_tracking_validation_raw.json                9 KB  2026-03-03  ⚠ SEE ISSUE 2
│
├── data/
│   ├── inventory/
│   │   ├── BUSINESS_LICENCES_INVENTORY.md                  28 KB  2026-03-03
│   │   ├── BUSINESS_LICENCE_QUALITY.md                     19 KB  2026-03-03
│   │   ├── CENSUS_INVENTORY.md                             24 KB  2026-03-03
│   │   ├── CENSUS_QUALITY_ASSESSMENT.md                    51 KB  2026-03-03
│   │   ├── COV_CATALOG.md -> datasets/vancouver/           [symlink, target valid]
│   │   ├── CT_CONCORDANCE.md                                9 KB  2026-03-03
│   │   ├── DATA_INVENTORY.md                               16 KB  2026-03-03
│   │   ├── DATA_STATUS.md                                   6 KB  2026-03-03
│   │   ├── NEIGHBOURHOOD_CODE_MAPPING.md                   19 KB  2026-03-03
│   │   ├── RELATED_DATASETS.md                             23 KB  2026-03-03
│   │   └── SOURCE_DOCUMENTATION.md                         69 KB  2026-03-03
│   │
│   ├── processed/
│   │   ├── address_to_area.csv                            120 KB  2026-03-03
│   │   ├── area_name_normalization.csv                      1 KB  2026-03-03
│   │   ├── business_panel.csv                              14 MB  2026-03-03  ⚠ SEE ISSUE 3
│   │   ├── businesstype_crosswalk.csv                      44 KB  2026-03-03
│   │   ├── businesstype_macro_categories.csv               14 KB  2026-03-03
│   │   ├── commercial-licences-2013-to-2026.csv           172 MB  2026-03-03
│   │   ├── commercial-panel.csv                            16 MB  2026-03-03  ⚠ SEE ISSUE 4
│   │   ├── commercial-panel-v2.csv                         17 MB  2026-03-03
│   │   ├── ct_local_area_concordance.csv                   33 KB  2026-03-03
│   │   ├── neighbourhood_code_lookup.csv                    2 KB  2026-03-03
│   │   └── neighbourhood_land_values.csv                   23 KB  2026-03-03
│   │
│   └── raw/
│       ├── business-licences/
│       │   ├── business-licences-2013-to-2024.csv         206 MB  2026-03-03
│       │   ├── business-licences-current.csv               52 MB  2026-03-03
│       │   ├── business-licences-merged-2013-to-2026.csv  241 MB  2026-03-03  ⚠ SEE ISSUE 5
│       │   ├── snapshot_2024-10-02_sample.csv             753 KB  2026-03-03
│       │   └── snapshot_2024-10-30_sample.csv             735 KB  2026-03-03
│       ├── census/
│       │   ├── 2006_CT/
│       │   │   └── vancouver_CMA_2006.csv                  45 MB  2026-03-03
│       │   ├── 2006_census_CT_001.zip                      52 MB  2012-03-08  ⚠ SEE ISSUE 6
│       │   ├── 2006_census_CT_005.zip                      59 MB  2012-03-08
│       │   ├── 2006_census_CT_sample_004.zip                2 MB  2012-03-08  ⚠ SEE ISSUE 7
│       │   ├── 2011_CT/
│       │   │   ├── 98-316-XWE2011001-401-DQ.CSV           173 KB  2016-04-05
│       │   │   ├── 98-316-XWE2011001-401.CSV              276 MB  2014-08-22  ⚠ SEE ISSUE 8
│       │   │   ├── 98-316-XWE2011001-Metadata.CSV           8 KB  2014-09-24
│       │   │   └── vancouver_CMA_2011.csv                   25 MB  2026-03-03
│       │   ├── 2011_census_CT_national.zip                  21 MB  2026-03-03
│       │   ├── 2016_CT/                                                       ⚠ SEE ISSUE 9
│       │   │   ├── 98-401-X2016007_English_CSV_data.csv     8 MB  2017-09-20
│       │   │   ├── 98-401-X2016007_English_meta.txt         21 KB  2017-09-20
│       │   │   ├── Geo_starting_row_CSV.csv                 50 KB  2017-09-20
│       │   │   └── README_meta.txt                           1 KB  2017-09-20
│       │   ├── 2016_CT_correct/
│       │   │   ├── 98-401-X2016043_English_meta.txt        221 KB  2018-02-09
│       │   │   ├── Geo_starting_row_CSV.csv                 176 KB  2018-02-09
│       │   │   └── vancouver_CMA_2016.csv                  104 MB  2026-03-03
│       │   ├── 2016_census_CT_correct.zip                  161 MB  2026-03-03
│       │   ├── 2016_census_CT_national.zip                 652 KB  2026-03-03  ⚠ SEE ISSUE 10
│       │   ├── 2021_CT/
│       │   │   ├── 98-401-X2021007_English_meta.txt        235 KB  2022-12-07
│       │   │   ├── 98-401-X2021007_Geo_starting_row.CSV    272 KB  2022-12-07
│       │   │   ├── README_meta.txt                            1 KB  2022-07-30
│       │   │   └── vancouver_CMA_2021.csv                  215 MB  2026-03-03
│       │   ├── 2021_census_CT_national.zip                 238 MB  2026-03-03
│       │   └── boundaries/
│       │       ├── 2006/ [4 shapefiles: .dbf, .prj, .shp, .shx]                ⚠ SEE ISSUE 11
│       │       ├── 2011/ [4 shapefiles + 92-160-g2011001-eng.pdf]               ⚠ SEE ISSUE 11
│       │       ├── 2016/ [4 shapefiles + census_tract.html + 92-160-g2016002-eng.pdf] ⚠ SEE ISSUE 11
│       │       ├── 2021/ [4 shapefiles + .xml]                                  ⚠ SEE ISSUE 11
│       │       ├── gct_000b06a_e.zip                         8 MB  2026-03-03  ⚠ SEE ISSUE 11
│       │       ├── gct_000b11a_e.zip                        12 MB  2026-03-03  ⚠ SEE ISSUE 11
│       │       ├── lct_000b16a_e.zip                         8 MB  2026-03-03  ⚠ SEE ISSUE 11
│       │       └── lct_000b21a_e.zip                        13 MB  2026-03-03  ⚠ SEE ISSUE 11
│       ├── businesstype-crosswalk-official.pdf              243 KB  2026-03-03
│       ├── cov-open-data-catalog.csv -> datasets/vancouver/ [symlink, target valid]
│       ├── local-area-boundary.geojson                       91 KB  2026-03-03
│       ├── property-tax-report-2006-2010.csv               222 MB  2026-03-03
│       ├── property-tax-report-2011-2015.csv               254 MB  2026-03-03
│       ├── property-tax-report-2016-2019.csv               230 MB  2026-03-03
│       └── property-tax-report-2020-present.csv            443 MB  2026-03-03
│
├── docs/
│   ├── A1_APPROACH_REVIEW.md                               25 KB  2026-03-03
│   ├── ADVERSARIAL_REVIEW.md                               49 KB  2026-03-03
│   ├── ASSUMPTION_VERIFICATION.md                          46 KB  2026-03-03
│   ├── PHASE0_CANDIDATES.md                                61 KB  2026-03-03
│   ├── PHASE0_SELECTED.md                                  23 KB  2026-03-03
│   ├── POLICY_RESEARCH.md                                  44 KB  2026-03-03
│   └── RIGOR_FRAMEWORK.md                                  33 KB  2026-03-03
│
├── logs/
│   ├── download.log                                        14 KB  2026-03-03
│   ├── download_progress.json                              62 KB  2026-03-03
│   ├── geocode_progress.jsonl                             503 KB  2026-03-03
│   └── geocode_run.log                                    204 KB  2026-03-03
│
└── scripts/
    ├── biz_licence_eda.py                                  30 KB  2026-03-03  ⚠ SEE ISSUE 12
    ├── build_ct_concordance.py                              8 KB  2026-03-03
    ├── commercial_eda_plots.py                             13 KB  2026-03-03  ⚠ SEE ISSUE 13
    ├── commercial_pipeline.py                              54 KB  2026-03-03
    ├── compute_land_values.py                              24 KB  2026-03-03
    ├── eda_plots.py                                        15 KB  2026-03-03  ⚠ SEE ISSUE 14
    ├── geocode_bulk.py                                     36 KB  2026-03-03
    ├── geocode_neighbourhood_codes.py                      16 KB  2026-03-03  ⚠ SEE ISSUE 15
    ├── investigate_historic_businesstypes.py                8 KB  2026-03-03  ⚠ SEE ISSUE 16
    ├── rebuild_panel_v2.py                                 28 KB  2026-03-03
    ├── step1_baseline_survival.py                          22 KB  2026-03-03
    └── validate_survival_tracking.py                       31 KB  2026-03-03
```

**No files exist in the project root directory.** All content is in the correct top-level directories.

---

## 2. Issues Found

### Summary Table

| # | File | Current Location | Recommended Location | Type | Reason |
|---|------|-----------------|---------------------|------|--------|
| 1 | `PANEL_V2_CHANGELOG.md` | `analysis/` | `data/inventory/` | Misplacement | Documents a data transformation/panel version change — it is data documentation, not an analysis report |
| 2 | `survival_tracking_validation_raw.json` | `analysis/` | `logs/` | Misplacement | Raw JSON output from a validation script — a debug/intermediate artifact, not an analysis deliverable |
| 3 | `business_panel.csv` | `data/processed/` | Archive or delete | Duplicate/Superseded | Unscoped (all business types) first-pass panel from `biz_licence_eda.py`. Superseded by `commercial-panel.csv` and `commercial-panel-v2.csv`. `biz_licence_eda.py` also hardcodes the wrong path (`data/business_panel.csv` instead of `data/processed/business_panel.csv`) — the file ended up in `processed/` only because it was moved manually |
| 4 | `commercial-panel.csv` | `data/processed/` | Retain but mark superseded | Duplicate/Version | v1 panel, superseded by `commercial-panel-v2.csv` for all current analysis. Actively read by `validate_survival_tracking.py` (to compare v1 vs v2) and referenced in `A15_HOME_BASED_IMPACT.md`. Keep but document clearly as v1-archived |
| 5 | `business-licences-merged-2013-to-2026.csv` | `data/raw/business-licences/` | `data/processed/business-licences/` or `data/processed/` | Misplacement | This is a derived merge of `business-licences-2013-to-2024.csv` + `business-licences-current.csv`, produced by `commercial_pipeline.py`. It is NOT an untouched source — it is a processed/derived artifact. Raw directory should contain only downloaded originals |
| 6 | `2006_census_CT_001.zip` | `data/raw/census/` | Archive or delete | Orphan/Unused | Contains `Generic_94-581-XCB2006001.xml` (a different geographic breakdown than catalog 005). The project uses `2006_census_CT_005.zip` as confirmed in `CENSUS_INVENTORY.md` (Source S4). Catalog 001 was apparently downloaded as a candidate but not used. No extracted content from it exists |
| 7 | `2006_census_CT_sample_004.zip` | `data/raw/census/` | Archive or delete | Orphan/Unused | A 2 MB sample ZIP (catalog 94-581-XCB2006004). Not referenced in `CENSUS_INVENTORY.md` at all — appears to have been downloaded during initial exploration and abandoned. No extracted content from it exists |
| 8 | `2011_CT/98-316-XWE2011001-401.CSV` | `data/raw/census/2011_CT/` | Archive or delete | Redundant — original in zip | 276 MB full national CSV, extracted from `2011_census_CT_national.zip`. The `vancouver_CMA_2011.csv` filtered file is what's actually used. The full national CSV is identical to the zip's content (size-verified). The zip is retained, so the extracted national CSV is a redundant full extraction |
| 9 | `2016_CT/` (entire directory) | `data/raw/census/2016_CT/` | `data/raw/census/_wrong_downloads/2016_CT/` or delete | Misnamed/Wrong data | Contains catalog `98-401-X2016007` (Designated Places profiles), NOT census tracts. `DATA_STATUS.md` and `CENSUS_INVENTORY.md` both explicitly warn not to use this directory. It is a wrong download that was superseded by `2016_CT_correct/`. Risk of accidental use is real |
| 10 | `2016_census_CT_national.zip` | `data/raw/census/` | `data/raw/census/_wrong_downloads/` or delete | Misnamed/Wrong data | 652 KB ZIP containing `98-401-X2016007` files (same wrong data as `2016_CT/` directory). Its name suggests it is the national CT zip, but it is the Designated Places zip. Easily confused with `2016_census_CT_correct.zip` |
| 11 | Boundary zips vs extracted subdirs | `data/raw/census/boundaries/` | Consolidate — keep zips OR extracted subdirs, not both | Redundant duplication | All four boundary zip files (`gct_000b06a_e.zip`, `gct_000b11a_e.zip`, `lct_000b16a_e.zip`, `lct_000b21a_e.zip`) have been fully extracted into their `2006/`, `2011/`, `2016/`, `2021/` subdirectories. Byte-for-byte verified identical. Both copies exist, consuming ~83 MB in duplicate |
| 12 | `biz_licence_eda.py` | `scripts/` | `scripts/` (keep, but fix bug) | Bug / Orphan candidate | Script is partially superseded — it performs the old unscoped EDA on all business types, producing `business_panel.csv`. The commercial-scoped workflow (`commercial_pipeline.py`) replaced it. It also hardcodes `PANEL_PATH = ".../data/business_panel.csv"` (missing `/processed/`). Not actively called by any other script. Candidate for archival once `BUSINESS_LICENCE_EDA.md` no longer needs regeneration |
| 13 | `commercial_eda_plots.py` | `scripts/` | `scripts/generated/` or add header comment | Generated artifact | This file is programmatically generated by `commercial_pipeline.py` (line: `SCRIPT_OUT = f"{BASE}/scripts/commercial_eda_plots.py"`). It is not hand-authored. Currently lives alongside hand-authored scripts with no visual distinction |
| 14 | `eda_plots.py` | `scripts/` | `scripts/` (keep, but mark superseded) | Superseded | Produces the same 6 plot filenames as `commercial_eda_plots.py` but reads `business_panel.csv` (unscoped). Overwrites current plots if run accidentally. The current plots in `analysis/plots/` were generated by `commercial_eda_plots.py`. Running `eda_plots.py` would silently degrade plot quality |
| 15 | `geocode_neighbourhood_codes.py` | `scripts/` | `scripts/` (keep as historical) or archive | Superseded | First-pass geocoding approach: hardcoded 2-address-per-code manual samples. Explicitly identified as the wrong approach in `A1_APPROACH_REVIEW.md`. Replaced by `geocode_bulk.py`. Its outputs (`neighbourhood_code_lookup.csv`, `NEIGHBOURHOOD_CODE_MAPPING.md`) were overwritten by `geocode_bulk.py`. Also had a path bug writing to project root (`BASE / "neighbourhood_code_lookup.csv"`) |
| 16 | `investigate_historic_businesstypes.py` | `scripts/` | `scripts/` (keep) | Orphan/One-off | Prints-only investigation script, produces no file output. Answers a specific question about FY24-25 businesstype classification artifact. Legitimate investigative script, but has no corresponding output in `analysis/`. If the finding was absorbed into `COMMERCIAL_EDA.md` or `SCOPE_AUDIT.md`, it is effectively archived |

---

## 3. Detailed Issue Descriptions

### Issue 1 — `PANEL_V2_CHANGELOG.md` in `analysis/`

`PANEL_V2_CHANGELOG.md` documents what changed between `commercial-panel.csv` (v1) and `commercial-panel-v2.csv` (v2). This is data documentation — it describes the lineage and transformation applied to a processed dataset. It belongs in `data/inventory/` alongside `DATA_STATUS.md` and `BUSINESS_LICENCES_INVENTORY.md`.

### Issue 2 — `survival_tracking_validation_raw.json` in `analysis/`

Raw JSON output from `validate_survival_tracking.py` containing intermediate check statistics (e.g., `addr_pct_range`, `a15_flip_count`). This is a debug/intermediate artifact, not an analysis deliverable. The human-readable analysis is in `SURVIVAL_TRACKING_VALIDATION.md`. The JSON should be in `logs/` alongside other run output files.

### Issue 3 — `business_panel.csv` in `data/processed/`

This is the first-pass all-business-types panel generated by `biz_licence_eda.py`. It predates the commercial-scoped workflow. Key facts:
- 131,870 rows (all types), vs `commercial-panel.csv` which is scoped to commercial types only
- The script that creates it (`biz_licence_eda.py`) hardcodes path `data/business_panel.csv` (missing `/processed/`) — the file ended up in `processed/` only by manual correction after the script ran
- Not referenced by any active downstream script (only by the old `eda_plots.py`)
- Candidate for deletion; at minimum, should be renamed `business_panel_SUPERSEDED.csv` to prevent accidental use

### Issue 4 — `commercial-panel.csv` (v1) — Retain but document

v1 is actively read by `validate_survival_tracking.py` and `rebuild_panel_v2.py` for comparison purposes. It is NOT orphaned — it is the intentional baseline for the v2 rebuild. However, the filenames `commercial-panel.csv` and `commercial-panel-v2.csv` are easily confused. Recommend renaming to `commercial-panel-v1.csv` and updating all references. This would make the versioning explicit.

### Issue 5 — `business-licences-merged-2013-to-2026.csv` in `data/raw/`

This file is produced by `commercial_pipeline.py` as a merge of two raw source files (2013-to-2024 + current). It is a derived/processed artifact, not an untouched download. Convention is clear: `data/raw/` contains only files exactly as they came from external sources. This file should be in `data/processed/`.

Secondary note: if moved to `data/processed/`, the scripts referencing it (`commercial_pipeline.py`, `investigate_historic_businesstypes.py`) need path updates.

### Issue 6 & 7 — Unused 2006 census ZIPs

`2006_census_CT_001.zip` (catalog 94-581-XCB2006001) and `2006_census_CT_sample_004.zip` (catalog 94-581-XCB2006004) have no extracted files and are not referenced in `CENSUS_INVENTORY.md`. Only catalog 005 was used. These appear to be exploratory downloads that were abandoned. At 52 MB and 2 MB respectively, they are low-risk to delete.

### Issue 8 — `98-316-XWE2011001-401.CSV` full national extracted

The 276 MB full national 2011 census CSV was extracted from the zip and sits alongside `vancouver_CMA_2011.csv`. Since `2011_census_CT_national.zip` is retained and contains all three national files, the extracted 276 MB CSV is a redundant extraction. Only `vancouver_CMA_2011.csv`, the filtered Vancouver CMA file, is used by any scripts or referenced in inventory. The national CSV can be safely deleted (reextractable from the zip if ever needed).

### Issue 9 & 10 — Wrong 2016 census data

`data/raw/census/2016_CT/` and `data/raw/census/2016_census_CT_national.zip` both contain catalog `98-401-X2016007` (Designated Places profiles, not census tracts). Both `DATA_STATUS.md` and `CENSUS_INVENTORY.md` explicitly flag these with warnings. These wrong-download artifacts create ongoing confusion risk and should be moved to a clearly named `_wrong_downloads/` subdirectory or deleted.

### Issue 11 — Boundary shapefiles duplicated (zips + extracted)

All four boundary zip files have been fully extracted into subdirectories (`2006/`, `2011/`, `2016/`, `2021/`). Byte-for-byte verification confirms 100% match. Both copies exist consuming ~83 MB in duplication. Decision: keep zips as archives (they are the canonical download artifact from StatCan) and delete the extracted subdirectories, OR keep the extracted subdirectories and delete the zips. Do not keep both.

Recommendation: keep the extracted subdirectories (scripts can read shapefiles directly without unzipping) and delete the 4 zip files.

### Issue 12 — `biz_licence_eda.py` path bug + orphan status

The script has `PANEL_PATH = "/home/aurora/projects/sites/portfolio-projects/van-property-tax/data/business_panel.csv"` (missing `/processed/`). When run today it would write to a non-existent path. The script's main purpose — generating `BUSINESS_LICENCE_EDA.md` — was a one-time run. The commercial pipeline (`commercial_pipeline.py`) replaced it for ongoing work.

### Issue 13 — `commercial_eda_plots.py` is generated code

`commercial_pipeline.py` programmatically writes `commercial_eda_plots.py` to `scripts/`. It is not hand-authored. It lives alongside human-authored scripts with no distinguishing header. If the pipeline reruns, it overwrites the file. Recommend: move to a `scripts/generated/` subdirectory, or at minimum add a clearly visible `# AUTO-GENERATED BY commercial_pipeline.py — DO NOT EDIT BY HAND` header.

### Issue 14 — `eda_plots.py` will silently corrupt plots if run

`eda_plots.py` reads `business_panel.csv` (unscoped, 131K rows) and outputs the same 6 filenames as `commercial_eda_plots.py` (which reads the scoped commercial panel). If `eda_plots.py` is run accidentally, it silently overwrites the current plots with lower-quality unscoped data. Mark this clearly as superseded or rename it `eda_plots_SUPERSEDED.py`.

### Issue 15 — `geocode_neighbourhood_codes.py` is superseded

The script's 2-address-per-code manual approach was explicitly rejected in `A1_APPROACH_REVIEW.md` and replaced by `geocode_bulk.py`. Its outputs have been overwritten by the bulk geocoder. The script also had a path bug: writing to `BASE / "neighbourhood_code_lookup.csv"` (project root) instead of `data/processed/`. Files were not left in root (confirmed), but the path bug remains in the script. Mark as superseded or move to `scripts/archive/`.

### Issue 16 — `investigate_historic_businesstypes.py` — print-only orphan

Prints investigation results to stdout, produces no file output. Legitimate one-shot investigation script. If its finding (re: FY24-25 businesstype classification artifact) was absorbed into other docs, the script is historical only. Candidate for `scripts/archive/`.

---

## 4. Proposed Moves

The following table is ready for an execution agent. Each row is an independent operation.

| # | Action | Source | Destination | Notes |
|---|--------|--------|-------------|-------|
| M1 | `mv` | `analysis/PANEL_V2_CHANGELOG.md` | `data/inventory/PANEL_V2_CHANGELOG.md` | Data documentation, not analysis report |
| M2 | `mv` | `analysis/survival_tracking_validation_raw.json` | `logs/survival_tracking_validation_raw.json` | Debug artifact |
| M3 | `mv` | `data/raw/business-licences/business-licences-merged-2013-to-2026.csv` | `data/processed/business-licences-merged-2013-to-2026.csv` | Derived file; update paths in `commercial_pipeline.py` and `investigate_historic_businesstypes.py` |
| M4 | `mkdir` + `mv` | `data/raw/census/2016_CT/` | `data/raw/census/_wrong_downloads/2016_CT/` | Wrong download; prevents accidental use |
| M5 | `mv` | `data/raw/census/2016_census_CT_national.zip` | `data/raw/census/_wrong_downloads/2016_census_CT_national.zip` | Wrong download (same bad data as M4) |
| M6 | `rm` | `data/raw/census/boundaries/gct_000b06a_e.zip` | — | Extracted into `boundaries/2006/`; 100% duplicate |
| M7 | `rm` | `data/raw/census/boundaries/gct_000b11a_e.zip` | — | Extracted into `boundaries/2011/`; 100% duplicate |
| M8 | `rm` | `data/raw/census/boundaries/lct_000b16a_e.zip` | — | Extracted into `boundaries/2016/`; 100% duplicate |
| M9 | `rm` | `data/raw/census/boundaries/lct_000b21a_e.zip` | — | Extracted into `boundaries/2021/`; 100% duplicate |
| M10 | `rm` | `data/raw/census/2006_census_CT_001.zip` | — | Unused wrong-catalog download; 005 is the active one |
| M11 | `rm` | `data/raw/census/2006_census_CT_sample_004.zip` | — | Exploratory download; abandoned; not in CENSUS_INVENTORY |
| M12 | `rm` | `data/raw/census/2011_CT/98-316-XWE2011001-401.CSV` | — | 276 MB redundant full-national extraction; zip retained |
| M13 | `mv` | `data/processed/business_panel.csv` | `data/processed/business_panel_SUPERSEDED.csv` | Prevents accidental use; superseded by commercial-panel.csv |
| M14 | `mv` | `scripts/commercial_eda_plots.py` | `scripts/generated/commercial_eda_plots.py` | Auto-generated by `commercial_pipeline.py`; update SCRIPT_OUT path in pipeline |
| M15 | `mv` | `scripts/eda_plots.py` | `scripts/archive/eda_plots.py` | Superseded by commercial_eda_plots.py; dangerous if run |
| M16 | `mv` | `scripts/geocode_neighbourhood_codes.py` | `scripts/archive/geocode_neighbourhood_codes.py` | Superseded by geocode_bulk.py; approach rejected in A1_APPROACH_REVIEW |
| M17 | `mv` | `scripts/investigate_historic_businesstypes.py` | `scripts/archive/investigate_historic_businesstypes.py` | One-shot print-only investigation; no active role |

### Lower-priority / judgment calls

| # | Action | File | Recommendation | Reason |
|---|--------|------|----------------|--------|
| L1 | Consider rename | `data/processed/commercial-panel.csv` → `commercial-panel-v1.csv` | Optional | Reduces confusion with v2; requires updating paths in `biz_licence_eda.py`, `validate_survival_tracking.py`, `commercial_eda_plots.py`, `commercial_pipeline.py`, and `A15_HOME_BASED_IMPACT.md` |
| L2 | Fix bug | `scripts/biz_licence_eda.py` line 17 | `PANEL_PATH` should point to `data/processed/business_panel.csv` | Currently missing `/processed/` segment |
| L3 | Fix path | `scripts/commercial_pipeline.py` line 30 | `SCRIPT_OUT` needs updating if M14 is applied | Would write generated file to new `scripts/generated/` location |

---

## 5. What Is Clean

The following aspects of the project structure are correct and require no action:

- **Root directory**: No stray files. All content is in appropriate subdirectories.
- **`docs/`**: All seven files are methodology/assumption/policy documents. Correctly placed. `SOURCE_DOCUMENTATION.md` and `RELATED_DATASETS.md` are in `data/inventory/` (correct — they are data documentation, not methodology).
- **`data/inventory/`**: All files are data documentation. `COV_CATALOG.md` is a symlink to the shared datasets directory — correct per convention. `SOURCE_DOCUMENTATION.md` and `RELATED_DATASETS.md` are correctly placed here.
- **`analysis/plots/`**: All 7 PNG files are plots. Correctly placed.
- **`logs/`**: Four log files covering download and geocoding runs. All correctly placed.
- **`scripts/`**: Core active scripts (`commercial_pipeline.py`, `rebuild_panel_v2.py`, `step1_baseline_survival.py`, `validate_survival_tracking.py`, `compute_land_values.py`, `build_ct_concordance.py`, `geocode_bulk.py`) are correctly placed.
- **`data/raw/`**: Property tax CSVs, GeoJSON boundary, and the business licences source files are correctly placed as untouched downloads.
- **`data/processed/`**: Crosswalk files, concordance files, and lookup tables are correctly placed.
- **Census `2016_CT_correct/`, `2021_CT/`, `2006_CT/` directories**: Correctly contain filtered Vancouver-only extracts from national ZIPs.
- **`data/raw/cov-open-data-catalog.csv`**: Symlink to shared datasets directory — correct per convention.
- **Analysis reports** (`SCOPE_AUDIT.md`, `COMMERCIAL_EDA.md`, `LAND_VALUE_ANALYSIS.md`, `BUSINESS_LICENCE_EDA.md`, `STEP1_BASELINE_SURVIVAL.md`, `SURVIVAL_TRACKING_VALIDATION.md`, `MISSING_AREAS_INVESTIGATION.md`, `A15_HOME_BASED_IMPACT.md`): All EDA/step reports correctly in `analysis/`.
- **Notebook** (`business-survival-vancouver.ipynb`): Portfolio-facing notebook, correctly in `analysis/`.

---

## 6. Space Freed by Proposed Deletions

| Action | Space Freed |
|--------|------------|
| M6–M9 (boundary zip duplicates) | ~42 MB |
| M10 (2006_census_CT_001.zip) | ~52 MB |
| M11 (2006_census_CT_sample_004.zip) | ~2 MB |
| M12 (2011 full national CSV) | ~276 MB |
| **Total** | **~372 MB** |

---

*Audit complete. Execute M1–M17 above to resolve all confirmed issues. L1–L3 are optional improvements.*
