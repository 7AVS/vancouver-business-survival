# Related Datasets — Vancouver Open Data Portal Catalog Search

**Project**: Business Survival Analysis — do business closure rates correlate with land value appreciation?
**Catalog searched**: https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets
**Total catalog size**: 194 datasets
**Search date**: 2026-03-03
**Method**: Full catalog pull (2 pages, limit=100 each) + individual dataset metadata API calls for all relevant entries

## Already Acquired (baseline)

| Dataset | ID | Notes |
|---|---|---|
| Business licences (current) | `business-licences` | In hand |
| Business licences 1997-2012 | `business-licences-1997-to-2012` | In hand |
| Business licences 2013-2024 | `business-licences-2013-to-2024` | In hand |
| Property tax report (2020+) | `property-tax-report` | In hand |
| Local area boundary GeoJSON | `local-area-boundary` | In hand |
| Census 2001/2006/2011/2016/2021 | Multiple | Downloaded separately (4+ waves) |

---

## Priority 1: High Value — Acquire

### 1. Issued Building Permits
- **Dataset ID**: `issued-building-permits`
- **API**: `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/issued-building-permits`
- **Records**: 49,849
- **Date range**: 2017–2026 (current; updated daily as of 2026-03-02)
- **Update frequency**: Daily
- **Fields**: `permitnumber`, `permitnumbercreateddate`, `issuedate`, `permitelapseddays`, `projectvalue`, `typeofwork`, `address`, `projectdescription`, `permitcategory`, `applicant`, `propertyuse`, `specificusecategory`, `buildingcontractor`, `issueyear`, `geolocalarea`, `geo_point_2d`
- **Why valuable**: Direct signal of construction/redevelopment pressure. High permit volume + large project values in a neighbourhood indicate development intensity. Can correlate demolition/new construction permits with business closure rates in the same area. `typeofwork` includes New Building, Addition/Alteration, Demolition, Salvage & Abatement. `specificusecategory` breaks out commercial vs residential. `projectvalue` is a proxy for capital flow. **The displacement mechanism hypothesis lives here**: rising permits → rising land values → rising commercial rents → business closures.
- **Note**: Only goes back to 2017 — limited historical depth but covers the key post-2015 acceleration period.

---

### 2. Storefronts Inventory
- **Dataset ID**: `storefronts-inventory`
- **API**: `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/storefronts-inventory`
- **Records**: 33,983
- **Date range**: 2020–2023 (annual spring surveys; records stack across years in one layer)
- **Update frequency**: Annual (refreshed over summer after spring survey)
- **Fields**: `id`, `unit`, `civic_number_parcel`, `street_name_parcel`, `business_name`, `retail_category`, `year_recorded`, `geo_local_area`, `geom`, `geo_point_2d`
- **Why valuable**: This is a **direct vacancy and retail health indicator**. The annual storefronts inventory explicitly tracks "change and conditions of storefronts to monitor retail health." It captures which storefronts are occupied vs vacant, what category they are (Food & Beverage, Comparison Goods, Convenience Goods, etc.), and can be trended year-over-year by neighbourhood. **This is the closest proxy to commercial vacancy rates available in the portal**. Joining to business licences by address can validate licence cancellations against physical vacancy. Limitations: only covers 2020–2023 (4 years), and only street-level retail, not all commercial.

---

### 3. Zoning Districts and Labels
- **Dataset ID**: `zoning-districts-and-labels`
- **API**: `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/zoning-districts-and-labels`
- **Records**: 1,611
- **Date range**: Current (updated 2026-03-02; reflects current zoning only, not historical)
- **Update frequency**: As required (zoning changes trigger updates)
- **Fields**: `object_id`, `zoning_classification`, `zoning_category`, `zoning_district`, `cd_1_number`, `geom`, `geo_point_2d`
- **Why valuable**: Zoning is the regulatory framework that permits or blocks development. Commercial zones (C-1, C-2, C-3A, FC-1, MC, etc.) are directly relevant to business survival: rezoning from commercial to residential/mixed removes the land base for businesses. Can spatially join businesses to their zoning district to flag businesses operating in zones with redevelopment pressure. Limitation: snapshot only — no historical zoning data available on portal (historical zoning requires archive research).

---

### 4. Property Tax Reports (Historical Panels)
- **Dataset ID**: `property-tax-report-2006-2010`
- **Records**: 892,028
- **Date range**: 2006–2010
- **Fields**: Same schema as current (`current_land_value`, `previous_land_value`, `current_improvement_value`, `tax_assessment_year`, `neighbourhood_code`, `zoning_district`, `year_built`, `report_year`)

- **Dataset ID**: `property-tax-report-2011-2015`
- **Records**: 976,762
- **Date range**: 2011–2015
- **Fields**: Same schema

- **Dataset ID**: `property-tax-report-2016-2019`
- **Records**: 832,969
- **Date range**: 2016–2019
- **Fields**: Same schema

- **Why valuable**: The current property tax report we have covers 2020+. These three datasets extend the land value time series back to 2006, enabling a full 20-year panel. The `current_land_value` and `previous_land_value` fields capture year-over-year land value changes at parcel level, which is the core independent variable in the business survival hypothesis. The `neighbourhood_code` field enables neighbourhood-level aggregation. Together with the current dataset, we get: 2006 → 2026 annual land values for every taxable parcel in Vancouver. **This is essential for the core analysis.**
- **Note**: We already have `property-tax-report` (2020+). These three panels fill the historical gap.

---

### 5. Business Improvement Areas (BIA)
- **Dataset ID**: `business-improvement-areas-bia`
- **API**: `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-improvement-areas-bia`
- **Records**: 24
- **Date range**: Current (updated 2025-04-07)
- **Update frequency**: As required
- **Fields**: `mapid`, `name`, `geom`, `geo_point_2d`
- **Why valuable**: BIAs are boundary polygons for Vancouver's 22 business improvement areas (e.g., Robson Street, Granville, Commercial Drive, Gastown, Chinatown, Hastings-Sunrise, etc.). These are the key commercial corridors under study. Spatially joining businesses to BIA membership adds an important geographic dimension beyond the 22 local area boundaries — BIAs are more granular and represent areas where commercial activity is concentrated and organised. Business survival may vary significantly within a local area depending on whether a business is in a BIA. Also useful as a covariate: BIA membership may be protective (collective advocacy, shared marketing) or may proxy for higher-profile commercial real estate subject to gentrification pressure.

---

### 6. 3-1-1 Service Requests (2009–2021 archive + current)
- **Dataset ID**: `3-1-1-service-requests-2009-2021`
- **Records**: 2,083,091
- **Date range**: 2009–2021
- **Fields**: `department`, `service_request_type`, `status`, `closure_reason`, `service_request_open_timestamp`, `local_area`, `channel`, `latitude`, `longitude`, `geom`

- **Dataset ID**: `3-1-1-service-requests`
- **Records**: 897,035
- **Date range**: 2022–current (updated daily)
- **Fields**: Same schema

- **Why valuable**: The 311 data contains service request types that are proxies for neighbourhood conditions affecting business survival: `Graffiti Removal`, `Abandoned Vehicle`, `Private Property Construction Concern`, `Noise Complaint`, `Illegal Dumping`. High rates of construction-related complaints (`Private Property Construction Noise`, `Construction Concern`) in a local area signal active redevelopment pressure. Neighbourhood disorder complaints (graffiti, dumping, abandoned vehicles) correlate with declining commercial vitality. Together the two datasets span 2009–2026 (~17 years), aligning with the full business licence + property tax window. **Use case**: neighbourhood-year fixed effects using construction complaint counts as an additional displacement pressure proxy.
- **Caution**: Large files (2M + 900K records). Would need to filter to construction/development-related service types before use.

---

## Priority 2: Useful Supplementary Data

### 7. Rapid Transit Stations
- **Dataset ID**: `rapid-transit-stations`
- **API**: `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/rapid-transit-stations`
- **Records**: 22
- **Date range**: Current (reflects existing Expo/Millennium/Canada Lines; updated 2023-02-22)
- **Update frequency**: As required
- **Fields**: `station`, `geom`, `geo_local_area`, `geo_point_2d`
- **Why valuable**: Transit proximity is a known driver of commercial real estate pressure. Businesses near SkyTrain stations may face higher rents and displacement. The Broadway Subway (Millennium Line extension to Arbutus, opened 2024) is a natural experiment: businesses in Mount Pleasant, Fairview, Kitsilano near new stations should show detectable effects in the 2022–2026 licence data. Compute distance from each business address to nearest SkyTrain station as a covariate.

- **Dataset ID**: `rapid-transit-lines`
- **Records**: 3 (Expo, Millennium, Canada Line geometry)
- **Fields**: `line`, `geom`
- **Why valuable**: Companion geometry for transit corridor buffers. Together with stations, enables construction of 400m / 800m catchment zones around transit infrastructure.

---

### 8. Heritage Sites
- **Dataset ID**: `heritage-sites`
- **API**: `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/heritage-sites`
- **Records**: 2,495
- **Date range**: Current (updated 2023-03-23)
- **Fields**: `id`, `streetnumber`, `streetname`, `category`, `buildingnamespecifics`, `evaluationgroup`, `municipaldesignationm`, `provincialdesignationp`, `heritagerevitalizationagreementh`
- **Why valuable**: Heritage designation protects buildings from demolition/redevelopment. A business in a heritage-protected building is partially insulated from the land value → redevelopment → displacement pathway. Heritage status can be used as a quasi-instrumental variable or protective covariate. Also: historic commercial areas (Gastown, Chinatown, Strathcona) have high heritage density, and these overlap with gentrification hotspots — creating interesting interaction effects.

---

### 9. Non-Market Housing
- **Dataset ID**: `non-market-housing`
- **API**: `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/non-market-housing`
- **Records**: 641
- **Date range**: Includes `occupancy_year` field; updated 2026-01-01
- **Fields**: `name`, `address`, `project_status`, `occupancy_year`, `operator`, `clientele_families`, `clientele_seniors`, `design_accessible_*`, `design_adaptable_*`, `design_standard_*` (unit counts by bedroom type), `geom`
- **Why valuable**: Non-market housing concentrations shape the commercial tenant base. Neighbourhoods with high social housing density have different business survival dynamics (less disposable income, different retail mix). Also, new non-market housing developments often co-locate with commercial ground-floor space, which affects vacancy and business mix. Use as a neighbourhood-level demographic/economic control.

---

### 10. Property Parcel Polygons
- **Dataset ID**: `property-parcel-polygons`
- **API**: `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/property-parcel-polygons`
- **Records**: 99,744
- **Date range**: Current (updated 2026-03-02; updated frequently)
- **Fields**: `civic_number`, `streetname`, `tax_coord`, `site_id`, `geom`, `geo_point_2d`
- **Why valuable**: Parcel polygons enable precise spatial joins between business addresses, property tax records, zoning, building permits, and other spatial datasets. The `tax_coord` field should link directly to the `land_coordinate` field in the property tax report. This is the spatial backbone for joining all property-based data. Without it, address matching is string-based and error-prone.

---

### 11. Property Addresses
- **Dataset ID**: `property-addresses`
- **API**: `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/property-addresses`
- **Records**: 99,787
- **Date range**: Current (updated 2026-03-02)
- **Fields**: `civic_number`, `std_street`, `geo_local_area`, `p_parcel_id`, `pcoord`, `site_id`, `geom`, `geo_point_2d`
- **Why valuable**: Authoritative address-to-parcel lookup table. Business licences use address strings — this dataset provides a clean civic-number + street → parcel ID mapping. Essential for geocoding business addresses that don't have lat/long, and for linking business licences to property tax records via parcel.

---

### 12. City-Owned Properties
- **Dataset ID**: `city-owned-properties`
- **API**: `https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/city-owned-properties`
- **Records**: 4,455
- **Date range**: Current (updated 2026-03-02)
- **Fields**: `building_no`, `sap_address`, `type`, `geo_local_area`, `land_coord`, `geom`, `geo_point_2d`
- **Why valuable**: City-owned land is not subject to the same speculative land value dynamics as private land. Businesses on city-owned land (leased sites) may have different survival rates. Also identifies parks, community centres, social facilities — which are effectively non-commercial land uses that shape neighbourhood retail catchments.

---

### 13. Census Local Area Profiles (Portal Versions)
- **Dataset ID**: `census-local-area-profiles-2001`
- **Records**: (not retrieved — API intermittent)
- **Dataset ID**: `census-local-area-profiles-2006`
- **Dataset ID**: `census-local-area-profiles-2011`
- **Dataset ID**: `census-local-area-profiles-2016`
- **Date range**: 2001, 2006, 2011, 2016 respectively
- **Update frequency**: Census cycle (5-year)
- **Why valuable**: We already have census data downloaded separately (4 waves). These portal versions may offer pre-cleaned local area aggregations vs raw PUMF. Check if they add anything over what we already have. The local area profiles (22 Vancouver neighbourhoods) are already aggregated to the same geographic units as our business licence data. Fields typically include: population, age distribution, income distribution, housing tenure, dwelling type — all relevant controls for business survival analysis.
- **Note**: Portal only goes to 2016; 2021 census was downloaded separately. Likely redundant with existing census downloads but worth confirming schema compatibility.

---

## Priority 3: Interesting but Lower Priority

### 14. Development Cost Levy (DCL) Areas
- **Dataset ID**: `development-cost-levy-dcl-areas`
- **Records**: 6
- **Date range**: Current (updated 2020-02-10)
- **Fields**: `description`, `geom`, `geo_point_2d`
- **Why valuable**: DCL zones indicate where the city is actively planning for growth and charging developers levies for infrastructure. The 8 DCL districts (including citywide, public bike share, childcare, social housing, parks, transportation) define the geographic scope of active development policy. May be a useful proxy for areas under planned intensification pressure.

### 15. 3-1-1 Inquiry Volume
- **Dataset ID**: `3-1-1-inquiry-volume`
- **Records**: (not retrieved)
- **Why valuable**: Aggregate call volume by topic can indicate neighbourhood concern trends. Lower priority than the full service requests data.

### 16. Indicator Data (VanDashboard)
- **Dataset ID**: `indicator-data`
- **Records**: 2,280
- **Date range**: 2016–present (quarterly/annual)
- **Fields**: `indicatorid`, `indicatorname`, `granularity`, `periodlabel`, `periodend`, `actualvalue`, `geolevelname`, `disaggregationcategory`
- **Sample indicators relevant to this project**:
  - "Property tax increase (10 year rolling average)"
  - "Time to process an affordable housing development permit application"
  - "Time to process a minor commercial renovation permit application"
  - "People experiencing homelessness"
  - "Mode share (trips made by foot, bike, or transit)"
  - "Net debt per capita"
- **Why potentially useful**: Pre-aggregated city-level economic and social indicators with time series. Limited geographic granularity (city-wide, not neighbourhood). Could be useful as macro controls (e.g., city-wide homelessness trends, transit mode share trajectory). Low priority given granularity limitations.

### 17. Council Voting Records
- **Dataset ID**: `council-voting-records`
- **Records**: 79,446
- **Date range**: 2016–current (updated daily)
- **Fields**: `meeting_type`, `vote_date`, `agenda_description`, `council_member`, `vote`, `decision`
- **Why potentially useful**: Rezoning applications go to council for vote. Searching for rezoning-related agenda items in council votes could provide a dataset of approved rezonings by date and location. **This is a workaround for the absence of a dedicated rezoning applications dataset on the portal.** Would require text parsing of `agenda_description` to identify rezoning votes. Complex extraction but potentially high value.

### 18. Rental Standards — Current Issues
- **Dataset ID**: `rental-standards-current-issues`
- **Records**: 466
- **Date range**: Current only (unresolved issues; updated 2026-03-01)
- **Fields**: `businessoperator`, `detailurl`, `streetnumber`, `street`, `totaloutstanding`, `totalunits`, `geo_local_area`, `geom`
- **Why lower priority**: Only shows current unresolved issues for rental properties with 5+ units. No historical data. Limited to residential rental, not commercial. Not directly relevant unless studying residential vacancy → commercial impact.

### 19. Heritage Sites
- Already listed in Priority 2 above.

### 20. Road Ahead Projects Under Construction
- **Dataset ID**: `road-ahead-projects-under-construction`
- **Records**: 74
- **Date range**: Current snapshot only
- **Fields**: `project`, `street`, `location`, `comp_date`, `url_link`, `geom`
- **Why lower priority**: Current snapshot only — no history. Useful for understanding *current* construction disruption but can't be used for retrospective analysis.

---

## Notable Absences — Not Found in Catalog

The following categories were searched for and are **not present** in the City of Vancouver Open Data Portal:

| Gap | Notes |
|---|---|
| **Development permits** | No standalone development permit dataset exists. Building permits (`issued-building-permits`) cover construction/demolition but not pre-construction development approvals. Council voting records may be a workaround for rezoning decisions. |
| **Commercial vacancy rates** | No official commercial vacancy dataset. Storefronts inventory (2020–2023) is the best available proxy. CBRE/Avison Young/JLL publish commercial vacancy reports but not as open data. |
| **Rezoning applications** | No dataset. Historical rezonings are embedded in council minutes and voting records. The City's online rezoning tracker is a web application, not structured open data. |
| **Property assessment data (separate from tax)** | BC Assessment Authority (BCAA) data is the authoritative source but is provincial, not municipal. The property tax report *includes* BCAA assessment values, so this is partially covered. BCAA's own open data portal (`assessmentbc.ca`) is separate and may have additional granularity. |
| **Commercial real estate transaction data** | Not available as open data. Would require BC Land Title data (Landcor, Teranet) — paid sources. |
| **Business closures (direct)** | No dataset. Closures are inferred from business licence non-renewal (our existing methodology). |
| **Demographic change by neighbourhood over time** | Census profiles cover this but only every 5 years. No annual estimate data on the portal. |
| **Broadway Subway construction timeline** | No structured dataset for the project's neighbourhood-level construction impact. Would need external sources (TransLink, Broadway Project). |
| **Ground floor commercial space inventory** | No parcel-level dataset of commercial floor area or ground-floor retail zoning. Storefronts inventory is point-based, not area-based. |
| **Vacancy tax (empty homes)** | City's Empty Homes Tax data exists as reports but not as a downloadable open dataset on the portal as of search date. |

---

## Acquisition Priority Summary

| Priority | Dataset ID | Rationale | Est. Download Size |
|---|---|---|---|
| **P1 — Acquire now** | `issued-building-permits` | Core displacement mechanism signal | ~50K rows |
| **P1 — Acquire now** | `storefronts-inventory` | Best vacancy proxy available | ~34K rows |
| **P1 — Acquire now** | `property-tax-report-2006-2010` | Historical land values (fills gap) | ~900K rows |
| **P1 — Acquire now** | `property-tax-report-2011-2015` | Historical land values (fills gap) | ~977K rows |
| **P1 — Acquire now** | `property-tax-report-2016-2019` | Historical land values (fills gap) | ~833K rows |
| **P2 — Acquire soon** | `zoning-districts-and-labels` | Zoning type covariate | ~1.6K rows |
| **P2 — Acquire soon** | `business-improvement-areas-bia` | BIA membership covariate | 24 polygons |
| **P2 — Acquire soon** | `property-parcel-polygons` | Spatial join backbone | ~100K rows |
| **P2 — Acquire soon** | `property-addresses` | Address → parcel lookup | ~100K rows |
| **P2 — Acquire soon** | `rapid-transit-stations` | Transit proximity covariate | 22 points |
| **P3 — Consider** | `3-1-1-service-requests-2009-2021` | Construction pressure proxy | 2M rows, large |
| **P3 — Consider** | `3-1-1-service-requests` | Construction pressure proxy (recent) | 900K rows |
| **P3 — Consider** | `heritage-sites` | Heritage protection covariate | 2.5K rows |
| **P3 — Consider** | `non-market-housing` | Social housing density covariate | 641 rows |
| **P3 — Consider** | `city-owned-properties` | Non-private land exclusion | 4.5K rows |
| **P4 — Low priority** | `council-voting-records` | Rezoning vote extraction (complex) | 79K rows |
| **P4 — Low priority** | `indicator-data` | Macro controls only | 2.3K rows |

---

## API Access Pattern

All datasets accessible via:
```
# Metadata
https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/{dataset_id}

# Records (paginated)
https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/{dataset_id}/records?limit=100&offset=0

# Export (CSV)
https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/{dataset_id}/exports/csv

# Export (GeoJSON)
https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/{dataset_id}/exports/geojson
```

Rate limit: 15,000 requests/day per IP. The records API returns max 100 per call; large datasets require pagination.

---

*Last updated: 2026-03-03*
