# Adversarial Review: Neighbourhood Code Mapping Approach
**Document**: Review of proposed geocoding-based approach for mapping BC Assessment neighbourhood codes (001–030) to City of Vancouver local area names (22 areas)
**Date**: 2026-03-03
**Reviewer**: Claude Code (Desk-Mode Agent)
**Status of proposed approach**: PARTIALLY EXECUTED — `geocode_neighbourhood_codes.py` has already run and produced `neighbourhood_code_lookup.csv` and `NEIGHBOURHOOD_CODE_MAPPING.md`. This review evaluates the outputs, not just the plan.

---

## Executive Summary

The geocoding approach has already been executed and has produced a mapping with **serious defects** that make it unsuitable for use as-is. The primary failure is that **6 of 22 official CoV local areas are absent from the mapping**, and **16 of 30 codes were assigned with LOW confidence (tied vote)**. These are not minor issues — they mean the mapping is wrong for a material fraction of properties in the dataset.

The geocoding approach was also the *wrong starting point*. The property tax dataset itself contains a `geo_local_area` field in the 2020-present segment, and two earlier independent geocoding attempts (in `ASSUMPTION_VERIFICATION.md`) already revealed contradictory results with the current mapping. The correct path was a bulk spatial join on all unique addresses, not a 2-sample-per-code approach.

---

## PART 1: Problems with the Executed Approach (Ranked by Severity)

---

### SEVERITY 1 (CRITICAL): Six of 22 Official CoV Areas Are Completely Missing From the Mapping

**Finding**: The current `neighbourhood_code_lookup.csv` assigns all 30 codes to only **16 of the 22 CoV local areas**. The following 6 areas have **zero neighbourhood codes assigned** to them:

- Arbutus Ridge
- Mount Pleasant
- Shaughnessy
- South Cambie
- Sunset
- West Point Grey

This means that any property tax record whose address falls in these 6 areas will be **silently misclassified** in downstream analysis. It will be assigned to a neighbouring area's code. There is no error or flag — the join will succeed with a wrong result.

**Why it happened**: The 2-samples-per-code approach used addresses that happened not to land in these 6 areas. With 30 codes and 60 total samples, the statistical likelihood of missing entire areas was high. Several of these areas (Shaughnessy, South Cambie, West Point Grey) contain relatively few properties compared to Downtown or Renfrew-Collingwood, making them underrepresented in any random sample.

**Verification from data**: These 6 areas appear in the business licence snapshot's `localarea` field and in the CoV boundary GeoJSON. They are real, populated areas. For example:
- The business licence snapshot shows 22 unique `localarea` values, all 6 missing areas are among them
- The GeoJSON boundary file contains polygon features for all 6 areas
- Shaughnessy postal codes (V6H) appear in code 007 and code 008 data — meaning those codes contain Shaughnessy properties that are currently mapped to "Fairview" and "Marpole" respectively

**Impact**: Every property in these 6 areas is misclassified. That is a known geographic bias — errors are not random, they are spatially concentrated, which can corrupt neighbourhood-level trend analysis exactly where the displacement signals are most interesting (e.g., Shaughnessy land values, South Cambie development pressure near the Broadway Subway corridor).

---

### SEVERITY 1 (CRITICAL): 16 of 30 Codes Were Assigned With LOW Confidence (50/50 Tie)

**Finding**: The summary table in `NEIGHBOURHOOD_CODE_MAPPING.md` shows **16 codes** assigned with `LOW` confidence, meaning every geocoded sample returned a *different* area — a 50/50 tie with 2 samples. The final assignment in these cases was arbitrary (Python's `Counter.most_common()` breaks ties by insertion order, which is effectively random for a `Counter` of two equal-count items).

```
001: tied Fairview / West Point Grey
004: tied Dunbar-Southlands / Arbutus Ridge
006: tied Kerrisdale / Arbutus Ridge
009: tied Riley Park / Dunbar-Southlands
010: tied Marpole / Kerrisdale
012: tied Marpole / Downtown
013: tied Strathcona / Mount Pleasant
014: tied Grandview-Woodland / Kensington-Cedar Cottage
015: tied Riley Park / Mount Pleasant
017: tied Victoria-Fraserview / Kensington-Cedar Cottage
019: tied Renfrew-Collingwood / Sunset
021: tied Grandview-Woodland / Hastings-Sunrise
022: tied Renfrew-Collingwood / Hastings-Sunrise
025: tied Victoria-Fraserview / Killarney
```

That is **14 explicitly tied codes** (plus codes 008, 016, 018, 026 where one sample failed geocoding entirely, leaving 1/1 "HIGH confidence" on a single data point).

**The root cause**: 2 samples per code is statistically insufficient. If a neighbourhood code spans a boundary between two CoV areas (which many do, given 30 codes → 22 areas), a 2-sample draw will tie or flip-coin the result. The confidence labels are misleading — "HIGH" on a 1-sample code (e.g., 008: Marpole from 1 successful geocode) is meaningless.

**What the ties are telling you**: Many of these codes genuinely straddle two CoV areas. For example, code 013 (covering V5T + V6A postal codes) spans both Strathcona and Mount Pleasant by design — it is a large code. Assigning it to just "Strathcona" loses the Mount Pleasant properties.

---

### SEVERITY 1 (CRITICAL): The geo_local_area Field Already Exists in the 2020-Present Dataset (But Was Not Used)

**Finding**: The `taxyvr` R package documentation explicitly lists `geo_local_area` as one of the 29 columns in the Vancouver property tax dataset with the description "geographical local area designation". Cross-referencing with the `DATA_INVENTORY.md`, the 2020-present file has 30 columns while the 2006-2019 files have 29. The extra column in the 2020-present file was documented as `note` — but the `taxyvr` documentation suggests some version of the dataset included `geo_local_area`.

**Confirmed**: Inspecting the actual 2020-present CSV header confirms the columns are:
`pid, legal_type, folio, land_coordinate, zoning_district, zoning_classification, lot, plan, block, district_lot, from_civic_number, to_civic_number, street_name, property_postal_code, narrative_legal_line1-5, current_land_value, current_improvement_value, tax_assessment_year, previous_land_value, previous_improvement_value, year_built, big_improvement_year, tax_levy, neighbourhood_code, report_year, note`

The `note` column (not `geo_local_area`) is the 30th column in the current download. However, the `taxyvr` documentation may reflect an earlier version of the dataset or the API vs. bulk-export discrepancy. This needs verification: query the CoV Open Data API for a few records from the 2020+ dataset and check if `geo_local_area` appears in the API response even if not in the bulk CSV export.

**Action required**: Run `curl "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/property-tax-report/records?limit=5"` and inspect all returned fields. If `geo_local_area` is present in the API response but absent from the bulk CSV, the City is providing the mapping for free via the API and we simply need to request it. This would make the entire geocoding exercise unnecessary for 2020+ data.

---

### SEVERITY 2 (HIGH): The Approach Assumes a Clean 1-to-1 Code-to-Area Mapping — But Codes Genuinely Span Areas

**Finding**: The `ASSUMPTION_VERIFICATION.md` contains an earlier independent geocoding attempt (single sample per code) that **contradicts** the current mapping for several codes:

| Code | Current mapping (NEIGHBOURHOOD_CODE_MAPPING.md) | Earlier result (ASSUMPTION_VERIFICATION.md) |
|------|-------------------------------------------------|--------------------------------------------|
| 001 | Fairview (LOW) | Kitsilano |
| 002 | Kitsilano (HIGH) | Fairview |
| 007 | Fairview (HIGH) | Unknown (South Cambie or Fairview) |
| 013 | Strathcona (LOW) | Hastings-Sunrise |
| 017 | Victoria-Fraserview (LOW) | Sunset |

The fact that two independent geocoding runs using different sample addresses from the same neighbourhood codes produce different results is not a methodology failure — it is the data telling you that **these codes contain properties from multiple CoV areas**. There is no single correct area to assign to codes 001, 002, 007, 013, or 017. They are spatially heterogeneous.

The right question is not "which area does code 013 map to?" but "what fraction of code 013 properties are in Strathcona vs. Mount Pleasant vs. Hastings-Sunrise?"

**Impact on analysis**: Any analysis that treats neighbourhood_code as a proxy for a single CoV local area will produce aggregation errors proportional to the cross-boundary fraction. For a business survival analysis stratified by neighbourhood, this can introduce systematic misclassification that is correlated with geography and property type.

---

### SEVERITY 2 (HIGH): Geocoding Sample Selection Was Not Random — Samples Were Pre-Selected

**Finding**: The `geocode_neighbourhood_codes.py` script contains a hardcoded `SAMPLES` dictionary with 2 manually chosen addresses per code. These were not drawn randomly from the property tax data — they were manually selected. This creates selection bias:

1. The selector may have unconsciously picked "representative" addresses (i.e., addresses they knew or guessed were in the expected area)
2. Many property tax records have `from_civic_number = null` (50–58% of rows per the DATA_INVENTORY). A random sample would include these and fail to geocode, but the hardcoded samples pre-selected non-null addresses
3. Street-only addresses (no house number) would return to the middle of the street, which can cross area boundaries — but these were avoided by pre-selection

**Confirmed**: The hardcoded SAMPLES include full civic addresses like "303 BAYSWATER ST" and "1003 ALBERNI ST" — not the sparse "MAIN ST" or "COLUMBIA ST" entries that dominate the actual data. This means the geocoding success rate in the sample (~90%) is higher than what a random draw from the actual data would achieve.

---

### SEVERITY 2 (HIGH): Geocoding Failure Modes Are Underreported

**Failures observed in the current output**:

1. **Code 008**: "PINE CRES, Vancouver, BC V6J 4K4" → GEOCODE_FAILED. Pine Crescent is a real street but Nominatim returned no result. Code 008 was then assigned "Marpole" based on a single successful geocode (Selkirk St). But Selkirk St in V6H 4E2 is in Marpole/South Granville — while Pine Crescent in V6J is in Kitsilano/Arbutus Ridge. Code 008 may span both Marpole and Kitsilano.

2. **Code 026**: "2007 CORDOVA ST W, Vancouver, BC V6B 0E6" → GEOCODE_FAILED. Code 026 was assigned "Downtown" from a single sample (401 Georgia St W). This is plausible but unverified for the rest of code 026's properties.

3. **Code 016**: "MAIN ST, Vancouver, BC V5W 2T7" → GEOCODE_FAILED. MAIN ST without a civic number is ambiguous — Nominatim may return the middle of the street, which crosses many CoV boundary polygons.

4. **Code 018**: "115 KENT AVENUE SOUTH E, Vancouver, BC V5P 4X1" → GEOCODE_FAILED. Non-standard street name format likely caused the failure.

**The "nearest centroid" fallback is geographically imprecise**: Code 005's second sample (BLENHEIM ST V6N 1P5) fell outside all 22 polygons and was assigned "NEAREST:Dunbar-Southlands". Points on the water, in parks, or on boundary lines will trigger this fallback and silently assign the nearest centroid, which may be correct by area but incorrect in practice.

---

### SEVERITY 3 (MEDIUM): Temporal Stability Assumption Is Untested

**The approach assumes the mapping is stable across 2006–2026.** This is unverified.

BC Assessment neighbourhood codes are administrative identifiers that CAN be reassigned when the City redraws assessment boundaries. Over a 20-year period (2006–2026), some codes may have shifted geographic coverage. The data shows:

- 30 unique codes appear in every year from 2006 to 2026 (confirmed in DATA_INVENTORY.md: "0% null; 30 unique values" consistent across all periods)
- But consistency in the NUMBER of codes does not mean consistency in geographic coverage

If code 013's boundaries shifted between 2006 and 2020 (covering different streets in different years), applying a 2020-geocoded mapping to 2006 records will produce errors that look like neighbourhood trends but are actually mapping artifacts.

**Workaround**: Check whether the same PID appears with the same neighbourhood_code across all years it's present. A property should have the same code every year unless it was reassessed. From the DATA_INVENTORY cross-year PID analysis, >99.8% of PIDs persist year-over-year — checking code consistency for those PIDs would validate or refute temporal stability.

---

### SEVERITY 3 (MEDIUM): Naming Inconsistency Will Cause Silent Join Failure Downstream

**Finding**: The CoV GeoJSON boundary file uses `"Arbutus Ridge"` (space, no hyphen). The business licence `localarea` field uses `"Arbutus-Ridge"` (hyphen). The current mapping uses GeoJSON names throughout.

When the property tax neighbourhood code lookup is joined to the business licence data on `local_area_name`, the join will silently drop all Arbutus Ridge records because `"Arbutus Ridge" != "Arbutus-Ridge"`.

This is a known issue (flagged in `ASSUMPTION_VERIFICATION.md`) but is not reflected in the current mapping documentation, which contains no normalization note.

**Additional inconsistency**: The `ASSUMPTION_VERIFICATION.md` notes that "Renfrew" appears as a standalone `localarea` value in the business licence snapshot, separate from "Renfrew-Collingwood". This would be a 23rd area name in the business licence data that doesn't exist in the 22-area CoV boundary GeoJSON. Needs investigation.

---

### SEVERITY 3 (MEDIUM): The land_coordinate Field Is Not a Geographic Coordinate

**The `land_coordinate` field was proposed as a potential direct geocoding source**. Investigation shows it is NOT geographic:

- `land_coordinate` = first 8 digits of the 12-digit `folio` number
- The `folio` number is a BC Assessment roll number (administrative ID)
- Confirmed: `folio[:8] == land_coordinate` for all sampled records
- Example: folio=`570271750000`, land_coordinate=`57027175`

`land_coordinate` encodes no latitude or longitude information. It cannot be used for spatial analysis without a BC Assessment parcel lookup database that maps folio numbers to coordinates — which is not publicly available in the CoV open data.

---

## PART 2: Better Alternatives

---

### Alternative 1 (STRONGLY RECOMMENDED): Bulk Spatial Join on All Unique Property Tax Addresses

Instead of 2 samples per code with geocoding, use **all unique (from_civic_number, street_name, property_postal_code) combinations** in the dataset and perform a bulk spatial join.

**Method**:
1. Extract all unique addresses from the full 4.25M-row dataset: `SELECT DISTINCT from_civic_number, street_name, property_postal_code FROM property_tax`. Expect ~5,000–15,000 unique addresses.
2. Geocode each unique address once using Nominatim (5,000–15,000 calls at 1/sec = 1.4–4 hours, feasible overnight).
3. Point-in-polygon test each geocoded coordinate against the 22 CoV boundary polygons using Shapely.
4. Store result as address → CoV_area lookup.
5. Join back to full property tax dataset on address fields.

**Advantage**: This directly assigns a CoV area to each individual property, not to each code. It sidesteps the "code-to-area" problem entirely. Multiple codes can map to the same area (correct), and properties within the same code that span two areas get correctly differentiated.

**Limitation**: 50–58% of rows have null `from_civic_number`. For these, only street-level geocoding is possible — which returns the midpoint of the street, which may be in a different area than the actual property. But 40–50% coverage on a first pass is better than 100% coverage with a wrong mapping.

---

### Alternative 2 (FAST, LOWER QUALITY): Check the CoV Open Data API for geo_local_area

The `taxyvr` R package documentation lists `geo_local_area` as a field in the property tax dataset. The bulk CSV download does not contain this field — but the API may return it.

**Test**:
```bash
curl "https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/property-tax-report/records?limit=5"
```

If `geo_local_area` is in the API response, the City is providing the mapping directly for 2020+ records. This would give a definitive code-to-area lookup for at least a subset of years. For 2006–2019, the bulk spatial join would still be needed.

---

### Alternative 3 (PARTIAL): Use Postal Code FSA as a Proxy for Large, Clean Codes

The postal code FSA analysis shows that many neighbourhood codes are dominated by 1–2 FSAs:

- Code 020 (Hastings-Sunrise): 96.2% V5K — very clean
- Code 023 (Renfrew-Collingwood): 80.4% V5R — very clean
- Code 024 (Killarney): 45.9% V5S + 31.9% V5R — predominantly southeast Vancouver
- Code 027 (West End): 48.0% V6E + 45.4% V6G — very clean

For these high-purity codes, postal code crosswalk tables (Statistics Canada or Canada Post) could provide area assignments without geocoding.

**Where this fails**: Multi-FSA codes where the FSA split reflects the actual cross-boundary nature of the code (e.g., code 007 spans V6H, V5Z, V6J — these are three distinct neighbourhoods). Postal codes are not CoV local area boundaries and don't align neatly.

**Use case**: A quick sanity check to validate geocoded results, not as the primary mapping method.

---

### Alternative 4: Check BC Assessment Data Catalogue for Official Code Definitions

BC Assessment publishes a Data Catalogue at `info.bcassessment.ca`. The `neighbourhood_code` field in the property tax data is described in `DATA_INVENTORY.md` as "3-digit number assigned by BCA which identifies the neighbourhood." BC Assessment likely has an official published description of what each code means.

**Action**: Download and read `https://info.bcassessment.ca/Shared%20Documents/Data-Catalogue.pdf` in a PDF reader. The file failed to fetch as readable text in this review session. A BC Assessment representative or the provincial open data helpdesk may also provide a formal jurisdiction-to-code lookup.

If BC Assessment publishes a code→area lookup table in any format, that is authoritative and supersedes all geocoding approaches.

---

### Alternative 5: Use Business Licence Cross-Reference as Validation (Not Primary)

The business licence `localarea` field (22 CoV area names, populated in the Oct 2024 snapshot) could serve as a ground-truth validator — but NOT as the primary mapping method.

**Reason it can't be primary**: The business licence data has `localarea` entirely stripped in the April 2025 API extract. It is now 100% null for newly downloaded data (see `BUSINESS_LICENCES_INVENTORY.md`, A5 REFUTED). The October 2024 snapshot is the only usable reference.

**How to use it for validation**: For businesses in the Oct 2024 snapshot where `localarea` is populated AND `geo_point_2d` is present:
1. Take the lat/lon from `geo_point_2d`
2. Point-in-polygon against property tax neighbourhood codes (by cross-referencing the business address to a property record)
3. This gives a code → area mapping from an independent source

This is valuable for cross-validation but labor-intensive to set up.

---

## PART 3: Recommended Approach

The following sequence replaces the current single-run geocoding approach:

**Step 1 (1 hour)**: Check the CoV Open Data API for `geo_local_area` in the 2020+ property tax records. If it exists, use it to build a definitive code-to-area lookup from the 2020 data, then validate against 2006–2019 via bulk spatial join.

**Step 2 (overnight)**: Run bulk spatial join on all unique (from_civic_number, street_name, property_postal_code) combinations. This replaces the 2-sample approach with full-coverage address-level assignment. Expected size: ~5,000–15,000 unique addresses. At 1 req/sec Nominatim rate: 1.4–4 hours.

**Step 3 (1 day)**: For the ~50% of properties with null `from_civic_number`, use a street-level geocode (just street_name + postal_code + "Vancouver, BC") and assign to the polygon containing the street's midpoint. Document these as lower-confidence assignments. Most street-only parcels are likely entire blocks or institutional properties with clear boundaries (parks, large developments).

**Step 4 (30 min)**: Build the final `neighbourhood_code_lookup.csv` from the bulk results. For each code, the area assignment is determined by majority vote across ALL properties in that code, not 2 samples. Codes that are genuinely split (e.g., 30% Strathcona / 70% Mount Pleasant) should be flagged as multi-area codes rather than forced into a single assignment.

**Step 5 (30 min)**: Normalize all area names to a single canonical spelling. Resolve the "Arbutus Ridge" vs. "Arbutus-Ridge" discrepancy and the "Renfrew" vs. "Renfrew-Collingwood" issue. Document the canonical name table used for all downstream joins.

---

## PART 4: Verification Strategy for the Current (Flawed) Mapping

If the current mapping is used as a first approximation before the bulk spatial join is complete, the following checks bound the error:

1. **Coverage check**: Count how many rows in the full dataset, when mapped through `neighbourhood_code_lookup.csv`, produce an area from the 6 missing areas list. Expected count: 0 (because those areas are absent). This confirms the gap is real.

2. **Postal code consistency check**: For each code-to-area assignment, verify that the assigned area's known postal codes are consistent with the code's dominant FSA from the frequency table. Example: code 020 → Hastings-Sunrise is HIGH confidence — Hastings-Sunrise is in V5K, and 96% of code 020 properties are V5K. Code 012 → Marpole is LOW confidence — code 012 properties are 73% V6P (which covers Marpole, Oakridge, and Kerrisdale) with no dominant single-area signal.

3. **Cross-validation with ASSUMPTION_VERIFICATION.md**: The earlier single-sample geocoding shows contradictions for codes 001, 002, 013. At minimum, these three codes should be re-geocoded with 5+ samples each before any analysis stratified by those areas is published.

4. **Temporal stability check**: For a sample of 100 PIDs tracked across 2006–2026, verify that `neighbourhood_code` does not change. If even 1% of PIDs switch codes across years, the mapping is not static and requires year-specific application.

---

## Summary Table

| Issue | Severity | Status | Action |
|-------|----------|--------|--------|
| 6 of 22 areas missing from mapping | CRITICAL | Confirmed defect | Bulk spatial join required |
| 16 of 30 codes assigned via 50/50 tie | CRITICAL | Confirmed defect | Bulk spatial join required |
| geo_local_area may exist in API | CRITICAL | Unverified | Query API endpoint immediately |
| Codes genuinely span multiple areas | HIGH | Confirmed | Redesign mapping as fractional, not 1-to-1 |
| Sample was non-random (handpicked) | HIGH | Confirmed defect | Bulk spatial join on random draws |
| land_coordinate is not a coordinate | MEDIUM | Confirmed finding | Do not use for geocoding |
| Naming inconsistency (Arbutus Ridge/-) | MEDIUM | Confirmed, unfixed | Add normalization step |
| Temporal stability untested | MEDIUM | Unverified | PID consistency check across years |
| Geocoding failures silently degraded quality | MEDIUM | Confirmed | Track failure rates in bulk join |

---

## Conclusion

The current `neighbourhood_code_lookup.csv` should **not** be used for production analysis. It is acceptable as a rough orientation map showing the general geography of each code, but it has known incorrect assignments (codes mapping to wrong areas due to tied votes) and structural gaps (6 areas completely unmapped). Any analysis stratified by neighbourhood that uses this lookup will have spatially correlated misclassification errors that can masquerade as real geographic trends.

The two highest-leverage immediate actions are:

1. Query the CoV Open Data API for `geo_local_area` — this costs 5 minutes and may make the entire geocoding exercise unnecessary for 2020+ data
2. Run the bulk spatial join on all unique addresses — this is an overnight job that definitively resolves the mapping with high coverage

Do not proceed to neighbourhood-level EDA until one of these two approaches is complete.

---

*Review performed by Claude Code (Desk-Mode Agent) on 2026-03-03.*
*Framework: DATA-PROJECT-RIGOR.md adversarial challenge protocol.*
*Evidence sources: actual CSV data, NEIGHBOURHOOD_CODE_MAPPING.md, DATA_INVENTORY.md, ASSUMPTION_VERIFICATION.md, BUSINESS_LICENCES_INVENTORY.md, business licence snapshot, local-area-boundary.geojson, web research.*
