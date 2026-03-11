# Source Documentation — City of Vancouver Open Data Datasets

**Compiled**: 2026-03-03
**Method**: CoV Open Data Portal API (`/api/explore/v2.1/catalog/datasets/{id}`), portal information pages, Open Data Change Log dataset, web search for supplementary documents
**Purpose**: Single reference document capturing everything the data publisher says about their data — field definitions, known issues, schema changes, caveats, methodology, linked documents. For research rigor and reproducibility.

---

## Table of Contents

1. [Business Licences (Current) — `business-licences`](#1-business-licences-current)
2. [Business Licences 2013–2024 — `business-licences-2013-to-2024`](#2-business-licences-2013-to-2024)
3. [Business Licences 1997–2012 — `business-licences-1997-to-2012`](#3-business-licences-1997-to-2012)
4. [Property Tax Report (Current/2020+) — `property-tax-report`](#4-property-tax-report-current2020)
5. [Local Area Boundary — `local-area-boundary`](#5-local-area-boundary)
6. [Related / Supplementary Datasets](#6-related--supplementary-datasets)
   - 6a. Property Tax Report 2016–2019
   - 6b. Property Tax Report 2011–2015
   - 6c. Property Tax Report 2006–2010
   - 6d. Storefronts Inventory
   - 6e. Business Improvement Areas (BIA)
   - 6f. Zoning Districts and Labels
   - 6g. Open Data Change Log
7. [Licence — Open Government Licence – Vancouver](#7-licence--open-government-licence--vancouver)
8. [Open Data Change Log — Entries for Key Datasets](#8-open-data-change-log--entries-for-key-datasets)
9. [Supplementary Documents](#9-supplementary-documents)
10. [Portal Catalog — Dataset Inventory by Theme](#10-portal-catalog--dataset-inventory-by-theme)
11. [API Endpoints Reference](#11-api-endpoints-reference)
12. [Key Cross-Dataset Issues and Caveats](#12-key-cross-dataset-issues-and-caveats)

---

## 1. Business Licences (Current)

**Dataset ID**: `business-licences`
**Dataset UID**: `da_jm6e1w`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/business-licences/information/
**API Metadata**: https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences/

### Overview

| Attribute | Value |
|---|---|
| **Title** | Business licences |
| **Publisher** | City of Vancouver |
| **Data Owner** | City of Vancouver |
| **Data Team / Department** | Development, Buildings, and Licensing — Licence Office |
| **Theme** | Business and economy |
| **Keywords/Tags** | licence |
| **Licence** | Open Government Licence – Vancouver |
| **Licence URL** | https://opendata.vancouver.ca/pages/licence/ |
| **Record Count** | 198,125 (as of 2026-03-03) |
| **Last Modified / Data Processed** | 2026-03-03T14:49:25+00:00 |
| **Metadata Processed** | 2026-03-03T14:49:29 |
| **Update Frequency** | Daily (current year extract updated daily) |
| **Geometry Types** | Point |
| **Spatial Bounding Box** | -123.219 to -123.024 lon, 49.200 to 49.298 lat |
| **Features** | timeserie, analyze, geo |
| **Attachments** | None |
| **Export Formats** | CSV, JSON, Excel, GeoJSON |

### Full Description (verbatim from API)

> This dataset includes business licence records from 2024 onwards with the new categories (BusinessType).
>
> Under Licence By-Law No.4450, a valid business licence is required in order to operate a business in the City of Vancouver. A business licence can be obtained from the City's Licence Office and is valid for the remainder of the calendar year unless stated otherwise.

**Note section:**

> Effective May 6, 2024, the City streamlined its business licence categories, consolidating over 500 categories into fewer than 100. While data from before this date will remain accessible, this dataset post-May 6 is organized according to the new, streamlined categories. Learn more about this update at [Business licences | City of Vancouver](https://vancouver.ca/doing-business/business-licences.aspx#new-categories).
>
> All existing business licences are transitioned automatically into the new categories. Some business licence categories retained the same name. Business owners will renew their licence at the end of each year and may select a different category from the one they were sorted into. New businesses applying for a licence after the update will also select from the updated categories.
>
> Business licence records from 2013 to 2024, up to May 3, 2024, with their original categories (BusinessType) are found in [Business licences 2013 to 2024](https://opendata.vancouver.ca/explore/dataset/business-licences-2013-to-2024/) dataset.
>
> [Business licences 1997 to 2012](https://opendata.vancouver.ca/explore/dataset/business-licences-1997-to-2012/information/?disjunctive.status&disjunctive.businesssubtype) dataset remains the same.
>
> Effective April 12, 2018, the business license dataset, including historical data files from 1997 forward to the current year, has been updated for home-based businesses. The City has removed the business address from the home-based business license category.

**Data currency:**

> The extract for business licences of the current year is updated daily.

**Data accuracy:**

> There is a small chance that a licence number has been used twice. Licence RSN is an unique identifier.
>
> Business licences issued to out of town (outside of City of Vancouver) addresses do not have coordinates and will not show up on the map. Not all City of Vancouver addresses have coordinates.
>
> A small percentage of businesses are issued with a replacement licence in a displayed year due to changes or when business type names were retired during mid-year.
>
> Address data of some selected business types was not disclosed to provide privacy protection.
>
> There may be addresses that do not return coordinates in the geocoding process. These records will appear in the Table view but not on the Map.
>
> Liquor License Application business type does not have Issued Date or Expired Date information because it is interim application for a valid business licence.
>
> There may be some loss of quality from data entry errors.

**Websites for further information (from dataset page):**
- https://vancouver.ca/doing-business/licenses-and-permits.aspx
- https://vancouver.ca/doing-business/get-a-business-licence.aspx
- https://vancouver.ca/your-government/licence-bylaw.aspx
- https://vancouver.ca/doing-business/contact-business-licence-office.aspx

**Change log URL**: https://opendata.vancouver.ca/explore/dataset/open-data-change-log/log/?disjunctive.datasets&sort=logdate&refine.datasetids=business-licences

**Search terms (internal)**: licence, permit, license

### Field Definitions

| Field Name | Label | Type | Description |
|---|---|---|---|
| `folderyear` | FOLDERYEAR | text | First two characters of the Business Licence Number, representing the year issued |
| `licencersn` | LicenceRSN | text | Unique identifier for each business licence generated by the system |
| `licencenumber` | LicenceNumber | text | 9-character field: two digit year + hyphen + six digit system-generated number. Note: There is a small chance that a licence number can be reused more than once within a given year. LicenceRSN is an unique identifier. |
| `licencerevisionnumber` | LicenceRevisionNumber | text | 2-digit field representing the licence version. 00 = original version; increases as new revisions are created. |
| `businessname` | BusinessName | text | The ownership of the business |
| `businesstradename` | BusinessTradeName | text | Name under which business is usually conducted |
| `status` | Status | text | Current status: Cancelled (various reasons); GOB (Gone Out of Business, no longer operating); Inactive (no longer active); Issued (issued with no status change for the displayed year, or liquor licence review completed); Pending (application, incomplete, or under review stage for the displayed year) |
| `issueddate` | IssuedDate | datetime | The date when the business licence is issued and printed |
| `expireddate` | ExpiredDate | date | The date that the business licence expires. Most licences expire on December 31st. |
| `businesstype` | BusinessType | text | Description of the business activity, usually in accordance with the definition in Licence By-Law No. 4450. Note: Business type names with *Historic* at the end signify retired business licence types. Due to privacy concern, some business types do not have address data. |
| `businesssubtype` | BusinessSubType | text | Sub-category(s) of the main business type. Note: names with *Historic* signify retired sub types. |
| `unit` | Unit | text | Official space identifier for a building. Alphanumeric field. |
| `unittype` | UnitType | text | Description of a location other than a house or building with a simple street address where the business is located (Block, Suite, Apartment, etc.) |
| `house` | House | text | The number assigned to an address where the business is located |
| `street` | Street | text | The name of the street where the business is located |
| `city` | City | text | Name of the municipality where the business is located |
| `province` | Province | text | Name of the province or state where the business is located |
| `country` | Country | text | Two-character field for country (CA = Canada) |
| `postalcode` | PostalCode | text | A series of letters and/or digits attached to the business address |
| `localarea` | LocalArea | text | Manual selection from data custodian in source system. The City has 22 local areas (also known as local planning areas); see the Local area boundary dataset. |
| `numberofemployees` | NumberofEmployees | double | Number of staff employed with the business. Note: 0 = business has no employees (per applicant); 000 = information unknown. |
| `feepaid` | FeePaid | double | Total amount of licence fee paid in Canadian dollars. Blank if unavailable or unspecified. |
| `extractdate` | ExtractDate | datetime | Date when data was extracted from source data system |
| `geom` | Geom | geo_shape | Spatial representation of feature |
| `geo_point_2d` | geo_point_2d | geo_point_2d | Geographic point coordinates (no description provided) |

---

## 2. Business Licences 2013 to 2024

**Dataset ID**: `business-licences-2013-to-2024`
**Dataset UID**: `da_atbn4b`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/business-licences-2013-to-2024/information/
**API Metadata**: https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences-2013-to-2024/

### Overview

| Attribute | Value |
|---|---|
| **Title** | Business licences 2013 to 2024 |
| **Publisher** | City of Vancouver |
| **Data Owner** | City of Vancouver |
| **Data Team / Department** | Development, Buildings, and Licensing — Licence Office |
| **Theme** | Business and economy |
| **Keywords/Tags** | licence |
| **Licence** | Open Government Licence – Vancouver |
| **Licence URL** | https://opendata.vancouver.ca/pages/licence/ |
| **Record Count** | 782,330 (static) |
| **Last Modified (source data)** | 2024-05-04T17:29:08+00:00 |
| **Data Processed** | 2025-04-22T22:10:23+00:00 |
| **Update Frequency** | Static (frozen dataset — no further updates) |
| **Geometry Types** | Point |
| **Spatial Bounding Box** | -123.219 to -123.024 lon, 49.200 to 49.296 lat |
| **Features** | timeserie, analyze, geo |
| **Attachments** | None |
| **Export Formats** | CSV, JSON, Excel, GeoJSON |

### Full Description (verbatim)

> This dataset includes business licence records from 2013 to May 3, 2024 with original categories (BusinessType).
>
> Under Licence By-Law No.4450, a valid business licence is required in order to operate a business in the City of Vancouver. A business licence can be obtained from the City's Licence Office and is valid for the remainder of the calendar year unless stated otherwise.

**Note section:**

> This is a new dataset containing business licence records from 2013 to May 5, 2024 with original categories (BusinessType).
>
> [Business licences](https://opendata.vancouver.ca/explore/dataset/business-licences/) dataset includes business licence records from 2024 onwards with their new categories (BusinessType).
>
> [Business licences 1997 to 2012](https://opendata.vancouver.ca/explore/dataset/business-licences-1997-to-2012/information/) dataset remains the same.
>
> Effective May 6, 2024, the City streamlined its business licence categories, consolidating over 500 categories into fewer than 100. Learn more about this update at [Business licences | City of Vancouver](https://vancouver.ca/doing-business/business-licences.aspx#new-categories).
>
> Effective April 12, 2018, the business license dataset, including historical data files from 1997 forward to the current year, has been updated for home-based businesses. The City has removed the business address from the home-based business license category.

**Data currency:**

> This dataset is static.

**Data accuracy:**

> There is a small chance that a licence number has been used twice. Licence RSN is an unique identifier.
>
> Business licences issued to out of town (outside of City of Vancouver) addresses do not have coordinates and will not show up on the map. Not all City of Vancouver addresses have coordinates.
>
> A small percentage of businesses are issued with a replacement licence in a displayed year due to changes or when business type names were retired during mid-year.
>
> Address data of some selected business types was not disclosed to provide privacy protection.
>
> There may be addresses that do not return coordinates in the geocoding process. These records will appear in the Table view but not on the Map.
>
> Liquor License Application business type does not have Issued Date or Expired Date information because it is interim application for a valid business licence.
>
> There may be some loss of quality from data entry errors.

**Change log URL**: https://opendata.vancouver.ca/explore/dataset/open-data-change-log/log/?disjunctive.datasets&sort=logdate&refine.datasetids=business-licences-2013-to-2024

**Search terms (internal)**: permit, license, business, licence

### Field Definitions

All fields are identical to `business-licences` with one difference noted below:

| Field Name | Label | Type | Description / Notes |
|---|---|---|---|
| `folderyear` | FOLDERYEAR | text | First two characters of Business Licence Number, representing the year issued |
| `licencersn` | LicenceRSN | text | Unique identifier for each business licence |
| `licencenumber` | LicenceNumber | text | 9-character field (year + hyphen + 6-digit number). Possible reuse within a year; LicenceRSN is unique. |
| `licencerevisionnumber` | LicenceRevisionNumber | text | 2-digit version field. 00 = original. |
| `businessname` | BusinessName | text | Ownership of the business |
| `businesstradename` | BusinessTradeName | text | Name under which business is usually conducted |
| `status` | Status | text | Cancelled; GOB; Inactive; Issued; Pending (same definitions as current dataset) |
| `issueddate` | IssuedDate | datetime | Date licence issued and printed |
| `expireddate` | ExpiredDate | date | Licence expiry date. Most expire Dec 31. |
| `businesstype` | BusinessType | text | Business activity, per Licence By-Law No. 4450. *Historic* suffix = retired type. Privacy restriction: some types lack address data. |
| `businesssubtype` | BusinessSubType | text | Sub-category(s) of main business type. *Historic* suffix = retired sub type. |
| `unit` | Unit | text | Space identifier for a building (alphanumeric) |
| `unittype` | UnitType | text | Location descriptor (Block, Suite, Apt., etc.) |
| `house` | House | text | Address house number |
| `street` | Street | text | Street name |
| `city` | City | text | Municipality name |
| `province` | Province | text | Province or state |
| `country` | Country | text | Two-character country code (CA = Canada) |
| `postalcode` | PostalCode | text | Postal code |
| `localarea` | LocalArea | text | Manual selection from data custodian. City has 22 local areas. |
| `numberofemployees` | NumberofEmployees | **text** | NOTE: In this dataset the type is text (not double as in the current dataset). 0 = no employees; 000 = unknown. |
| `feepaid` | FeePaid | double | Total licence fee paid (CAD). Blank if unavailable. |
| `extractdate` | ExtractDate | datetime | Date of extraction from source system |
| `geom` | Geom | geo_shape | Spatial representation |
| `geo_point_2d` | geo_point_2d | geo_point_2d | Geographic point coordinates |

**IMPORTANT SCHEMA DIFFERENCE**: `numberofemployees` is typed as `text` in this dataset vs `double` in the current dataset. This affects joins and numeric operations.

---

## 3. Business Licences 1997 to 2012

**Dataset ID**: `business-licences-1997-to-2012`
**Dataset UID**: `da_blrqav`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/business-licences-1997-to-2012/information/
**API Metadata**: https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/business-licences-1997-to-2012/

### Overview

| Attribute | Value |
|---|---|
| **Title** | Business licences 1997 to 2012 |
| **Publisher** | City of Vancouver |
| **Data Owner** | City of Vancouver |
| **Data Team / Department** | Development, Buildings, and Licensing — Licence Office |
| **Theme** | Business and economy |
| **Keywords/Tags** | licence |
| **Licence** | Open Government Licence – Vancouver |
| **Licence URL** | https://opendata.vancouver.ca/pages/licence/ |
| **Record Count** | 958,899 (static) |
| **Last Modified (source data)** | 2018-04-12T12:05:46+00:00 |
| **Data Processed** | 2025-04-22T22:13:33+00:00 |
| **Update Frequency** | Static (frozen dataset — no further updates) |
| **Geometry Types** | Point |
| **Spatial Bounding Box** | -123.219 to -123.024 lon, 49.200 to 49.296 lat |
| **Features** | timeserie, analyze, geo |
| **Attachments** | None |
| **Export Formats** | CSV, JSON, Excel, GeoJSON |

### Full Description (verbatim)

> This dataset includes business licence records from 1997 to 2012 with original categories (BusinessType).
>
> Under Licence By-Law No.4450, a valid business licence is required in order to operate a business in the City of Vancouver. A business licence can be obtained from the City's Licence Office and is valid for the remainder of the calendar year unless stated otherwise.

**Note section:**

> Effective May 6, 2024, the City streamlined its business licence categories, consolidating over 500 categories into fewer than 100. While data from before this date will remain accessible, [Business licences](https://opendata.vancouver.ca/explore/dataset/business-licences/information/) dataset post-May 6 is organized according to the new, streamlined categories. Learn more about this update at [Business licences | City of Vancouver](https://vancouver.ca/doing-business/business-licences.aspx#new-categories).
>
> This dataset remains the same.
>
> [Business licences](https://opendata.vancouver.ca/explore/dataset/business-licences/) dataset includes business licence records from 2024 onwards according to the new categories (BusinessType).
>
> [Business licence records from 2013 to 2024](https://opendata.vancouver.ca/explore/dataset/business-licences-2013-to-2024/), up to May 3, 2024, with their original categories (BusinessType) are found in Business licences 2013 to 2024 dataset.
>
> Effective April 12, 2018, the business license dataset, including historical data files from 1997 forward to the current year, has been updated for home-based businesses. The City has removed the business address from the home-based business license category.

**Data currency:**

> This is a static dataset.

**Data accuracy:** (same as other business licence datasets — see section 1)

**Change log URL**: https://opendata.vancouver.ca/explore/dataset/open-data-change-log/log/?disjunctive.datasets&sort=logdate&refine.datasetids=business-licences-1997-to-2012

**Search terms (internal)**: permit, license

### Field Definitions

| Field Name | Label | Type | Description / Notes |
|---|---|---|---|
| `folderyear` | FOLDERYEAR | text | First two characters of Business Licence Number, representing the year issued |
| `licencersn` | LicenceRSN | text | Unique identifier |
| `licencenumber` | LicenceNumber | text | 9-character field. Possible reuse within year; LicenceRSN is unique. |
| `licencerevisionnumber` | LicenceRevisionNumber | text | 2-digit version. 00 = original. |
| `businessname` | BusinessName | text | Ownership of the business |
| `businesstradename` | BusinessTradeName | text | Trade name |
| `status` | Status | text | Cancelled; GOB; Inactive; Issued; Pending |
| `issueddate` | IssuedDate | **date** | NOTE: In this dataset IssuedDate is typed as `date` (not `datetime` as in the other two datasets). |
| `expireddate` | ExpiredDate | date | Licence expiry date |
| `businesstype` | BusinessType | text | Business activity per Licence By-Law No. 4450. *Historic* suffix = retired. |
| `businesssubtype` | BusinessSubType | text | Sub-category(s). *Historic* suffix = retired. |
| `unit` | Unit | text | Space identifier for building |
| `unittype` | UnitType | text | Location descriptor |
| `house` | House | text | Address house number |
| `street` | Street | text | Street name |
| `city` | City | text | Municipality |
| `province` | Province | text | Province or state |
| `country` | Country | text | Two-character country code |
| `postalcode` | PostalCode | text | Postal code |
| `localarea` | LocalArea | text | Manual selection from data custodian. 22 local areas. |
| `numberofemployees` | NumberofEmployees | **text** | Type is text in this dataset. 0 = no employees; 000 = unknown. |
| `feepaid` | FeePaid | **int** | NOTE: In this dataset FeePaid is typed as `int` (not `double`). Total licence fee paid (CAD). |
| `extractdate` | ExtractDate | datetime | Date of extraction |
| `geom` | Geom | geo_shape | Spatial representation |

**NOTE**: `geo_point_2d` field is NOT present in this dataset (present in the other two business licence datasets).

**IMPORTANT SCHEMA DIFFERENCES from other business licence datasets**:
- `issueddate`: `date` type here vs `datetime` in 2013-2024 and current
- `numberofemployees`: `text` here (same as 2013-2024, different from current which is `double`)
- `feepaid`: `int` here vs `double` in both other datasets
- No `geo_point_2d` field

---

## 4. Property Tax Report (Current/2020+)

**Dataset ID**: `property-tax-report`
**Dataset UID**: `da_34rtj6`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/property-tax-report/information/
**API Metadata**: https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/property-tax-report/

### Overview

| Attribute | Value |
|---|---|
| **Title** | Property tax report |
| **Publisher** | City of Vancouver |
| **Data Owner** | City of Vancouver; BC Assessment |
| **Data Team / Department** | Finance, Risk and Supply Chain Management — Revenue Services |
| **Theme** | Government and finance |
| **Keywords/Tags** | (none listed) |
| **Licence** | Open Government Licence – Vancouver |
| **Licence URL** | https://opendata.vancouver.ca/pages/licence/ |
| **Record Count** | 1,551,132 (as of 2026-03-03) |
| **Last Modified / Data Processed** | 2026-03-02T15:21:56+00:00 |
| **Metadata Processed** | 2026-03-03T14:50:00 |
| **Update Frequency** | Current year updated weekly; all other years static |
| **Geometry Types** | None (no geo fields) |
| **Features** | analyze |
| **Attachments** | None |
| **Export Formats** | CSV, JSON, Excel |
| **Search terms (internal)** | house |

### Full Description (verbatim)

> This dataset contains information on properties from BC Assessment (BCA) and City sources from 2020.
>
> To limit the size of individual datasets, we segmented the property tax data into multiple datasets. See all [property tax datasets](https://opendata.vancouver.ca/explore/?q=property+tax) for data since 2006.

**Note section:**

> - Tax coordinates and particularly the legal description information should not be viewed as definitive or legal.
> - For zoning data information please consult the City's zoning pages.
> - Zoning data is not available in historical property tax data sets.
> - Values for the "previous improvement value" and "previous land value" columns are not available for the 2006–2013 reports.

**Data currency:**

> This data in City systems is updated in the normal course of business, however priorities and resources determine how fast a change in reality is reflected in the database.
>
> Note: Only property tax data for the current year is updated weekly. All other data years contain static data.

**Data accuracy:**

> Accuracy is dependent on the matching of records between multiple agencies including non-City sources.

**Websites for further information:**
- http://vancouver.ca/home-property-development/property-tax.aspx
- http://www.bcassessment.ca/Pages/default.aspx
- https://vancouver.ca/home-property-development/zoning-and-development-bylaw.aspx
- https://vancouver.ca/home-property-development/zoning-and-land-use-policies-document-library.aspx

**Change log URL**: https://opendata.vancouver.ca/explore/dataset/open-data-change-log/log/?disjunctive.datasets&sort=logdate&refine.datasetids=property-tax-report

### Field Definitions

| Field Name | Label | Type | Description |
|---|---|---|---|
| `pid` | PID | text | Property identifier, assigned by Land Title Survey Authority, sourced from BC Assessment records |
| `legal_type` | LEGAL_TYPE | text | Values: 'STRATA' (part of a Strata Plan), 'LAND' (non-strata plan number), 'OTHER' (no plan number) |
| `folio` | FOLIO | text | 12-digit identifier for assessment purposes. Assigned by BC Assessment. All communication with BCA regarding folio numbers must be prefixed with Neighbourhood code. |
| `land_coordinate` | LAND_COORDINATE | text | First 8 digits of BC Assessment's folio number |
| `zoning_district` | ZONING_DISTRICT | text | Name of zoning district. Each has a corresponding district schedule in the Zoning and Development By-law. Not available in historical datasets. |
| `zoning_classification` | ZONING_CLASSIFICATION | text | Name of zoning classification. Not available in historical datasets. |
| `lot` | LOT | text | Component of legal description, assigned by Land Title Survey Authority, sourced from BC Assessment |
| `plan` | PLAN | text | Component of legal description, assigned by Land Title Survey Authority, sourced from BC Assessment |
| `block` | BLOCK | text | Component of legal description, assigned by Land Title Survey Authority, sourced from BC Assessment |
| `district_lot` | DISTRICT_LOT | text | Component of legal description, assigned by Land Title Survey Authority, sourced from BC Assessment |
| `from_civic_number` | FROM_CIVIC_NUMBER | text | House number; may be the first in a range. Assigned by the City, sourced from BCA records. |
| `to_civic_number` | TO_CIVIC_NUMBER | text | Blank unless it is the last house number in a range. Assigned by the City, sourced from BCA records. |
| `street_name` | STREET_NAME | text | Street name where property is located. Assigned by the City, sourced from BCA records. |
| `property_postal_code` | PROPERTY_POSTAL_CODE | text | Postal code for the property address |
| `narrative_legal_line1` | NARRATIVE_LEGAL_LINE1 | text | Property description for registration purposes; assigned by Land Title Survey Authority, sourced from BC Assessment |
| `narrative_legal_line2` | NARRATIVE_LEGAL_LINE2 | text | (same sourcing as line1) |
| `narrative_legal_line3` | NARRATIVE_LEGAL_LINE3 | text | (same sourcing as line1) |
| `narrative_legal_line4` | NARRATIVE_LEGAL_LINE4 | text | (same sourcing as line1) |
| `narrative_legal_line5` | NARRATIVE_LEGAL_LINE5 | text | (same sourcing as line1) |
| `current_land_value` | CURRENT_LAND_VALUE | int | Market value of the fee simple interest in land, provided by BCA for the Tax_Assessment_Year. Issued in the Completed Roll (January) and Revised Roll (mid-March); amendments possible via Supplementary Rolls throughout the year. This is the actual value, not taxable value (which is net of exemptions and may be averaged). |
| `current_improvement_value` | CURRENT_IMPROVEMENT_VALUE | int | Market value of improvements (buildings/structures), provided by BCA for the Tax_Assessment_Year. Same sourcing and caveats as current_land_value. |
| `tax_assessment_year` | TAX_ASSESSMENT_YEAR | text | Year in effect for Current_Land_Value, Current_Improvement_Value, and Tax_Levy. May be blank when the folio did not meet assessment criteria for the year (e.g., new construction not yet assessed, or property subdivided/consolidated). |
| `previous_land_value` | PREVIOUS_LAND_VALUE | int | Land value for the previous assessment year. Not available for 2006–2013 reports. |
| `previous_improvement_value` | PREVIOUS_IMPROVEMENT_VALUE | int | Improvement value for the previous assessment year. Not available for 2006–2013 reports. |
| `year_built` | YEAR_BUILT | text | Year the property was built. Assigned by BCA based on permit records. |
| `big_improvement_year` | BIG_IMPROVEMENT_YEAR | text | Year of major improvement to the property. Assigned by BCA based on permit records. |
| `tax_levy` | TAX_LEVY | double | Total taxes on the most recent tax notice. Includes the City's general levy, levies for all taxing authorities, utilities, local improvements, and miscellaneous charges. Note: (1) Main property tax notices mailed end of May each year — no value in this column until early June of TAX_ASSESSMENT_YEAR. (2) Advance tax amount is not shown separately but is included in the main tax levy. |
| `neighbourhood_code` | NEIGHBOURHOOD_CODE | text | 3-digit number assigned by BCA identifying the neighbourhood for the folio. All BCA communication must include this code. Note: BCA does not supply the City with neighbourhood name information — contact BCA for neighbourhood names. |
| `report_year` | REPORT_YEAR | text | Year when data was extracted from source data system |
| `note` | NOTE | text | (no description provided by publisher) |

---

## 5. Local Area Boundary

**Dataset ID**: `local-area-boundary`
**Dataset UID**: `da_jxjdo1`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/local-area-boundary/information/
**API Metadata**: https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/local-area-boundary/

### Overview

| Attribute | Value |
|---|---|
| **Title** | Local area boundary |
| **Publisher** | City of Vancouver |
| **Data Owner** | City of Vancouver |
| **Data Team / Department** | Technology Services — GIS and CADD Services; Planning, Urban Design & Sustainability — City-Wide & Regional Planning |
| **Theme** | Property and development |
| **Keywords/Tags** | (none listed) |
| **Licence** | Open Government Licence – Vancouver |
| **Licence URL** | https://opendata.vancouver.ca/pages/licence/ |
| **Record Count** | 22 (one record per local area) |
| **Last Modified** | 2023-06-24T12:22:11+00:00 |
| **Update Frequency** | Static — "These boundaries do not change." |
| **Geometry Types** | Polygon |
| **Spatial Bounding Box** | -123.225 to -123.023 lon, 49.199 to 49.296 lat |
| **Features** | analyze, geo |
| **Attachments** | None |
| **Export Formats** | CSV, JSON, Excel, GeoJSON |
| **Search terms (internal)** | neighbourhood, local planning area, boundaries, neighborhood |

### Full Description (verbatim)

> This data set contains the boundaries for the City's 22 local areas (also known as local planning areas).

**Data currency:**

> These boundaries do not change.

**Data accuracy:**

> Local area boundaries generally follow street centrelines; centrelines are in the approximate centre of streets.

**Change log URL**: https://opendata.vancouver.ca/explore/dataset/open-data-change-log/log/?disjunctive.datasets&sort=logdate&refine.datasetids=local-area-boundary

### Field Definitions

| Field Name | Label | Type | Description |
|---|---|---|---|
| `name` | Name | text | Official Name (of the local area) |
| `geom` | Geom | geo_shape | Spatial representation of Local Area |
| `geo_point_2d` | geo_point_2d | geo_point_2d | (no description provided) |

### Notes on the 22 Local Areas

The City of Vancouver has 22 local areas (also known as local planning areas). The dataset contains one polygon per area. From the change log (2023-06-20): the area previously named "Arbutus-Ridge" was renamed to "Arbutus Ridge" (hyphen removed). The field `localarea` in the business licence datasets uses manual custodian selection from the source system — it may not perfectly align with the polygon boundaries in this dataset for all records.

---

## 6. Related / Supplementary Datasets

### 6a. Property Tax Report 2016–2019

**Dataset ID**: `property-tax-report-2016-2019`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/property-tax-report-2016-2019/

| Attribute | Value |
|---|---|
| **Title** | Property tax report 2016-2019 |
| **Record Count** | 832,969 (static) |
| **Last Modified** | 2021-05-08 |
| **Data Owner** | City of Vancouver |
| **Data Team** | Finance, Risk and Supply Chain Management — Revenue Services |
| **Theme** | Government and finance |
| **Licence** | Open Government Licence – Vancouver |
| **Update Frequency** | Static |

**Description (verbatim):**
> This dataset contains information on properties from BC Assessment (BCA) and City sources from 2016 to 2019. To limit the size of individual datasets, we segmented the property tax data into multiple datasets.

**Caveats (verbatim):**
- Tax coordinates and legal descriptions are not definitive or legal
- For zoning data information, consult the City's zoning pages
- Zoning data not available in historical datasets
- Values for "previous improvement value" and "previous land value" not available for the 2006–2013 reports

**Data currency:**
> The data for past years is static.

**Fields**: Same schema as `property-tax-report`. All fields present except `note` field is absent. The `zoning_district` and `zoning_classification` fields are present in the schema but populated only for the 2016–2019 years which overlap the period when zoning data began to be included (approximately 2014+).

### 6b. Property Tax Report 2011–2015

**Dataset ID**: `property-tax-report-2011-2015`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/property-tax-report-2011-2015/

| Attribute | Value |
|---|---|
| **Title** | Property tax report 2011-2015 |
| **Record Count** | 976,762 (static) |
| **Last Modified** | 2021-05-08 |
| **Data Owner** | City of Vancouver |
| **Data Team** | Finance, Risk and Supply Chain Management — Revenue Services |
| **Theme** | Government and finance |
| **Licence** | Open Government Licence – Vancouver |
| **Update Frequency** | Static |

**Description (verbatim):**
> This dataset contains information on properties from BC Assessment (BCA) and City sources from 2011 to 2015. To limit the size of individual datasets, we segmented the property tax data into multiple datasets.

**Important caveat**: Values for "previous improvement value" and "previous land value" are not available for the 2006–2013 reports. Since this dataset spans 2011–2015, these fields are absent for 2011–2013 records but present for 2014 and 2015 records.

**Fields**: Same schema as `property-tax-report` (all same fields).

### 6c. Property Tax Report 2006–2010

**Dataset ID**: `property-tax-report-2006-2010`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/property-tax-report-2006-2010/

| Attribute | Value |
|---|---|
| **Title** | Property tax report 2006-2010 |
| **Record Count** | 892,028 (static) |
| **Last Modified** | 2021-05-08 |
| **Data Owner** | City of Vancouver; BC Assessment |
| **Data Team** | Finance, Risk and Supply Chain Management — Revenue Services |
| **Theme** | Government and finance |
| **Licence** | Open Government Licence – Vancouver |
| **Update Frequency** | Static |

**Description (verbatim):**
> This dataset contains information on properties from BC Assessment (BCA) and City sources from 2006 to 2010. To limit the size of individual datasets, we segmented the property tax data into multiple datasets.

**Caveats (verbatim):**
- Tax coordinates and legal descriptions are not definitive or legal
- For zoning data information, consult the City's zoning pages
- Zoning data is not available in historical property tax data sets
- Values for "previous improvement value" and "previous land value" columns are not available for the 2006–2013 reports

**Data currency:**
> The data for past years is static.

**Websites for further information (unique to this dataset — older URL format):**
- http://vancouver.ca/home-property-development/property-tax.aspx
- http://www.bcassessment.ca/Pages/default.aspx
- http://vancouver.ca/home-property-development/zoning-districts-maps-and-regulations.aspx
- http://vancouver.ca/home-property-development/descriptions-of-zoning-districts.aspx

**Schema note**: `previous_improvement_value` and `previous_land_value` are typed as `text` in the 2006–2010 dataset (vs `int` in 2011–2015 and 2016–2019). This is consistent with the values being absent — the type reflects the empty nature of the data in this era.

### 6d. Storefronts Inventory

**Dataset ID**: `storefronts-inventory`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/storefronts-inventory/

| Attribute | Value |
|---|---|
| **Title** | Storefronts inventory |
| **Record Count** | 33,983 |
| **Last Modified** | 2024-01-26 |
| **Data Owner** | City of Vancouver |
| **Data Team** | Planning, Urban Design & Sustainability — City-Wide & Regional Planning |
| **Theme** | Business and economy |
| **Licence** | Open Government Licence – Vancouver |
| **Update Frequency** | Annual (spring inventory conducted March/April; dataset refreshed over summer) |

**Description (verbatim):**
> The annual Storefronts inventory documents change and conditions of storefronts in the City of Vancouver to monitor retail health.

**Note (verbatim):**
> All inventory years are shown in one layer. To consider only the latest data, filter on the latest "Year Recorded" field.

**Data currency (verbatim):**
> The inventory is conducted annually in the springtime (March/April) and this dataset is refreshed over the summer.

**Data accuracy (verbatim):**
> The addresses are spatially accurate to the block level as each address is coded to the centre of the property parcel (not the business address). Multiple stores on a single larger parcel (such as in downtown and Yaletown) may have the same mapped location.

**Relevance to van-property-tax project**: Provides retail occupancy/vacancy data by local area and year — useful for correlating commercial activity with property values and business licence counts.

**Fields:**

| Field Name | Label | Type | Description |
|---|---|---|---|
| `id` | id | text | A unique number associated with each commercial retail space that stays the same from year to year |
| `unit` | unit | text | The unit number of a CRU |
| `civic_number_parcel` | civic_number_parcel | text | The civic number of the parcel that each CRU is geocoded to — a component of the full address. May not match business-posted addresses. |
| `street_name_parcel` | street_name_parcel | text | The street name of the parcel geocoded to — a component of the full address. May not match business-posted addresses. |
| `business_name` | business_name | text | The name of the occupant identified for each CRU |
| `retail_category` | retail_category | text | A coding system of broad categories of retail commercial uses |
| `year_recorded` | year_recorded | text | The year when the data was collected |
| `geo_local_area` | geo_local_area | text | The local area where the feature is found, derived from the feature's coordinates or address. The City has 22 local areas. For more details, see the Local area boundary dataset. |
| `geom` | geom | geo_shape | Spatial representation of feature |
| `geo_point_2d` | geo_point_2d | geo_point_2d | Geographic point coordinates |

### 6e. Business Improvement Areas (BIA)

**Dataset ID**: `business-improvement-areas-bia`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/business-improvement-areas-bia/

| Attribute | Value |
|---|---|
| **Title** | Business improvement areas (BIA) |
| **Record Count** | 24 |
| **Last Modified** | 2025-04-07 |
| **Data Owner** | City of Vancouver |
| **Data Team** | (not specified in API metadata) |
| **Theme** | Business and economy |
| **Licence** | Open Government Licence – Vancouver |
| **Update Frequency** | Updated in the normal course of business |

**Description (verbatim):**
> The Business Improvement Area layer includes the boundary areas for the City's BIAs. Business Improvement Areas or BIAs are non-profit associations of property owners and business tenants who join together to promote and improve the commercial viability of their business district.

**Data currency (verbatim):**
> This data in City systems is updated in the normal course of business, however priorities and resources determine how fast a change in reality is reflected in the database.

**Relevance to van-property-tax project**: BIA boundaries identify commercially managed zones within local areas; useful for distinguishing BIA vs non-BIA commercial areas in business density analysis.

**Fields:**

| Field Name | Label | Type | Description |
|---|---|---|---|
| `mapid` | mapid | text | (no description provided) |
| `name` | name | text | BIA Name |
| `geom` | geom | geo_shape | Spatial representation of BIA |
| `geo_point_2d` | geo_point_2d | geo_point_2d | (no description provided) |

### 6f. Zoning Districts and Labels

**Dataset ID**: `zoning-districts-and-labels`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/zoning-districts-and-labels/

| Attribute | Value |
|---|---|
| **Title** | Zoning districts and labels |
| **Record Count** | 1,611 |
| **Last Modified** | 2026-03-02 |
| **Data Owner** | City of Vancouver |
| **Data Team** | Planning, Urban Design & Sustainability — City-Wide & Regional Planning |
| **Theme** | Property and development |
| **Licence** | Open Government Licence – Vancouver |
| **Update Frequency** | Updated in the normal course of business |

**Description (verbatim):**
> This dataset consists of zoning polygons throughout the City and labels describing them.
>
> Zoning regulates the development of property in Vancouver by encouraging land use and building in accordance with community goals and visions for the future of Vancouver and its neighbourhoods. The city is divided into many development zones, with each zone further broken down into districts. The Zoning Development Bylaw describes each district and its list of permitted uses and regulations. Some districts are scattered across the city, while others are found only in a single neighbourhood.

**Relevance to van-property-tax project**: Provides the authoritative spatial zoning geometry. The property tax report links to zoning via `zoning_district` and `zoning_classification` fields (for 2014+ data). This dataset can be spatially joined to establish zoning context.

**Fields:**

| Field Name | Label | Type | Description |
|---|---|---|---|
| `geom` | geom | geo_shape | Spatial representation of feature |
| `object_id` | object_id | text | Unique feature number for data management purposes |
| `zoning_classification` | zoning_classification | text | Grouping of zoning districts based on land uses, as defined in Section 9 of the Zoning and Development By-law (e.g., "Commercial", "Multiple Dwelling") |
| `zoning_category` | zoning_category | text | Grouping of zoning districts that regulate similar land uses (e.g., "C", "RM") |
| `zoning_district` | zoning_district | text | Zoning district as listed in Section 9 of the Zoning and Development By-law (e.g., "C-2", "RM-5") |
| `cd_1_number` | cd_1_number | text | Specific CD-1 (Comprehensive Development) zoning district number, sometimes including a letter (e.g., "46", "3B") |
| `geo_point_2d` | geo_point_2d | geo_point_2d | Geographic point coordinates |

**Key reference**: Zoning and Development By-law Section 9 (https://bylaws.vancouver.ca/zoning/Sec09.pdf) defines the zoning classification vocabulary used in both this dataset and the property tax report.

### 6g. Open Data Change Log

**Dataset ID**: `open-data-change-log`
**Dataset UID**: `da_a17p19`
**Portal URL**: https://opendata.vancouver.ca/explore/dataset/open-data-change-log/information/
**API Metadata**: https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/open-data-change-log/

| Attribute | Value |
|---|---|
| **Title** | Open data change log |
| **Record Count** | 190 (as of 2026-02-24) |
| **Last Modified** | 2026-02-24 |
| **Data Team** | Technology Services — Enterprise Data and Analytics |
| **Theme** | Government and finance |
| **Licence** | Open Government Licence – Vancouver |
| **Update Frequency** | As-needed (whenever significant changes occur) |

**Description (verbatim):**
> Significant changes to the open data catalogue, including new datasets added, datasets renamed or retired, quarterly or annual updates to high-impact datasets, changes to data structure or definition. Smaller changes, such as adding or editing records or renaming a field in an existing dataset are not included.

**Note (verbatim):**
> This log is published in the interest of transparency into the work of the open data program.

**Exclusions from the log**: Record additions/edits, field renaming — only significant structural changes are logged.

**Fields:**

| Field Name | Label | Type | Description |
|---|---|---|---|
| `datasets` | Datasets | text | Dataset name(s) affected (human-readable) |
| `changetype` | ChangeType | text | Type of change (Added, Changed) |
| `title` | Title | text | Title of the change log entry |
| `datasetids` | DatasetIDs | text | Machine-readable dataset IDs affected (structured lookup list) |
| `details` | Details | text | Detailed description of the change |
| `logdate` | LogDate | date | Date of the change |

---

## 7. Licence — Open Government Licence – Vancouver

**Licence Name**: Open Government Licence – Vancouver
**Licence URL**: https://opendata.vancouver.ca/pages/licence/

All datasets on the City of Vancouver Open Data Portal are published under the Open Government Licence – Vancouver. This is a permissive open data licence modelled after similar Open Government Licences used by the Province of British Columbia and the Government of Canada.

**Key terms** (from portal documentation and standard OGL-Vancouver terms):
- Users may copy, modify, publish, translate, adapt, distribute, or use the information for any lawful purpose, including commercial purposes, free of charge
- Attribution required: "Contains information licensed under the Open Government Licence – Vancouver"
- The City makes no warranty regarding accuracy, completeness, or fitness for any particular purpose
- The licence does not grant rights to use any trade-marks or logos of the City of Vancouver
- If there is a conflict between this licence and the City's Terms of Use, the terms and conditions of the Open Government Licence – Vancouver prevail

**Applies to all 5 primary datasets and all supplementary datasets documented here.**

---

## 8. Open Data Change Log — Entries for Key Datasets

The following entries from the Open Data Change Log (190 total entries as of 2026-02-24) are relevant to the van-property-tax project datasets. Listed chronologically (newest first).

### Business Licences

**2024-05-05 | Changed | Updated Business Licences dataset**
Datasets: `business-licences`, `business-licences-2013-to-2024`
> Changes to this dataset were made to align with the changes made to the Business Licence By-law.
> Effective May 6, 2024, the City streamlined its business licence categories (BusinessType), consolidating over 500 categories into fewer than 100. While data from before this date remains accessible, records post-May 6 are organized according to the new, streamlined categories. A new dataset (business-licences-2013-to-2024) was created to preserve historical records with original categories.

**2019-07-12 | Changed | Updated business licence dataset**
Dataset: `business-licences`
> Updated data files starting from 2017 to remove the names of the licence holders from short term rental business licence category.

**2018-04-12 | Changed | Updated Council expenses, employee remuneration, and business licence datasets**
Datasets include: `business-licences` (historical)
> Updated business licence dataset. Historical data files from 1997 forward to current year has been updated for home-based businesses. The City has removed the business address from the home-based business license category.

**2015-10-29 | Added | Historical business licences and 2015 cultural spaces**
Dataset: `business-licences`
> In addition to publishing business licence data for the current year, we have added all business licences that were recorded since 1997. This data was extracted between October 19 to 20 and will remain static, except for the immediate past two years which will be updated monthly. Business licences in the current year will continue to be refreshed daily.

**2011-03-10 | Added | Business Licence data improved**
Dataset: `business-licences-1997-to-2012`
> The City has just improved the Business Licence data on the Open Data website to include latitude and longitude attributes. In addition, XML Document Type Definition (DTD) information is also made available.

**2010-09-28 | Added | Business License Data Added to Open Data Site**
Dataset: `business-licences-1997-to-2012`
> The City has just added Business Licenses data to the Open Data web site. Business licenses are required in order to operate a business in the City of Vancouver and are obtained from the City's License Office.

### Property Tax Report

**2021-05-12 | Changed | Updated Property tax report datasets**
Datasets: `property-tax-report`, `property-tax-report-2016-2019`, `property-tax-report-2011-2015`, `property-tax-report-2006-2010`
> To better align with the terminology used in the [Zoning and Development By-law (Section 9)](https://bylaws.vancouver.ca/zoning/Sec09.pdf), the following attribute name changes were made:
> - Attribute names for zoning-related fields updated to match zoning bylaw terminology
> Note: No change in the underlying data; only attribute naming alignment with the zoning bylaw vocabulary.

**2020-12-16 | Changed | Property tax data from 2006**
Datasets: `property-tax-report`, `property-tax-report-2006-2010`, `property-tax-report-2011-2015`, `property-tax-report-2016-2019`
> To limit the size of individual datasets to under 1 million records, we have re-segmented the property tax data from 2006 to 2020 into multiple datasets.
> Note: There is no change in the data published for each year. Only the specific dataset to find the property tax for a given year has changed.

**2015-03-02 | Added | Property tax data from 2006**
Datasets: `property-tax-report`, `property-tax-report-2006-2010`
> We enhanced the property tax dataset with data from 2006 to 2013. The data was extracted on January 31, 2015 and included all tax-roll revisions up to that date. We started capturing year-end data at the end of 2014 as a new annual process. Current year data is refreshed weekly but data published for previous years remains static.

**2014-09-03 | Added | Improved property tax report dataset**
Datasets: `property-tax-report`, `property-tax-report-2006-2010`
> Improved data and descriptions of the property tax report dataset with two new data fields.

### Local Area Boundary

**2023-06-20 | Changed | Updated Local area boundary dataset**
Dataset: `local-area-boundary`
> - Updated Name value of Arbutus-Ridge to Arbutus Ridge (hyphen removed)
> - Retired MapID field

### Storefronts Inventory

**2023-07-19 | Added | Updated Storefronts Inventory dataset**
Dataset: `storefronts-inventory`
> - Added 2022 data
> - Updated Name value of Arbutus-Ridge to Arbutus Ridge

**2022-04-19 | Added | Storefronts Inventory**
Dataset: `storefronts-inventory`
> Added data relates to the annual inventory of most of the city's ground-level storefronts (commercial retail spaces) and shopping malls.

### Census Data (for reference — not part of primary scope but relevant context)

**2018-02-08 | Added | Census local area profiles 2016**
Dataset: `census-local-area-profiles-2016`
> The 2016 Census provides statistical information about the population, age and sex, type of dwelling, families, households and marital status, language, income, immigration and ethnocultural diversity, housing, Aboriginal peoples, education, labour, journey to work, language of work and mobility, and migration, as measured in the census program. The data is provided by Statistics Canada as a custom profile for each of the City's 22 Local Areas.

**2013-03-26 | Added | 2001–2011 Census local area profiles**
Datasets: `census-local-area-profiles-2001`, `census-local-area-profiles-2006`, `census-local-area-profiles-2011`
> The census is Canada's largest and most comprehensive data source conducted by Statistics Canada every five years. Data provided as custom profile for each of the City's 22 local planning areas.

---

## 9. Supplementary Documents

### 9a. Business Licence Category Streamlining — Council Reports

**Council Report (May 10, 2023 — Finance and Services Committee)**
URL: https://council.vancouver.ca/20230510/documents/cfsc3_000.pdf
Status: Access restricted (403 Forbidden from automated request; requires browser session)

**Key content established through web search and change log:**
- Staff recommended reducing licence types from ~570 to 88 groupings (final count as implemented: <100 types)
- The 22 new main categories correspond to major economic areas (retail, manufacturing, food, etc.)
- Streamlining achieved by amalgamating similar activities and eliminating outdated types (e.g., "pen pal services")
- Staff worked with other City departments, the Vancouver Economic Commission (VEC), and Vancouver Police Department (VPD) to address potential unintended consequences including data loss risk
- No financial implications; no anticipated drop in licence revenue
- Implementation: initially targeted April 1, 2024; actual effective date was May 6, 2024
- All existing business licences were automatically transitioned into the new categories

**Council Report follow-up (August 1, 2023 / September 13, 2023 committee)**
URL: https://council.vancouver.ca/20230913/documents/cfsc2.pdf
Contact: Sarah Hicks

**2024 Fee Schedule for Streamlined Business Licence Types (February 27, 2024)**
URL: https://council.vancouver.ca/20240227/documents/r2revised.pdf
Status: Access restricted (403 Forbidden)

### 9b. Self-Serve Mapping Chart (Old → New Categories)

**Title**: "Table 1 Business Licence Types as of May 6, 2024 — Main category" (self-serve chart)
**URL**: https://vancouver.ca/files/cov/streamlining-of-business-licence-types-self-serve-chart.pdf
**Status**: Access restricted (403 Forbidden from automated requests — requires browser session with a specific session cookie or browser access)

**What it contains**: A mapping table showing old business licence category names mapped to the new streamlined categories effective May 6, 2024. This is the official category crosswalk — the document for understanding how 500+ pre-May 2024 categories (in `business-licences-2013-to-2024`) map to the <100 post-May 2024 categories (in `business-licences`).

**Referenced from**: The `businesstype` field notes in the business-licences dataset (the "new categories" link points to the Vancouver.ca page which links to this PDF). The Google search snippet confirms: "Table 1 Business Licence Types as of May 6, 2024 Main category."

### 9c. Zoning and Development By-law, Section 9

**URL**: https://bylaws.vancouver.ca/zoning/Sec09.pdf
**Referenced by**: 2021-05-12 change log entry for property tax datasets; zoning-districts-and-labels field descriptions
**Content**: Defines zoning classification vocabulary used in both `property-tax-report` and `zoning-districts-and-labels`. The 2021 property tax dataset update was made to align field names with this bylaw's terminology.

### 9d. Licence By-Law No. 4450

**URL**: https://vancouver.ca/your-government/licence-bylaw.aspx
**Referenced by**: All three business licence dataset descriptions
**Content**: The governing bylaw defining business licence requirements and category definitions. Business type descriptions in the `businesstype` field are "usually in accordance with the definition in Licence By-Law No. 4450."

---

## 10. Portal Catalog — Dataset Inventory by Theme

### Business and Economy Theme (complete list as of 2026-03-03)

| Dataset ID | Title | Records | Last Modified |
|---|---|---|---|
| `business-licences` | Business licences | 198,125 | 2026-03-03 |
| `business-licences-2013-to-2024` | Business licences 2013 to 2024 | 782,330 | 2024-05-04 |
| `business-licences-1997-to-2012` | Business licences 1997 to 2012 | 958,899 | 2018-04-12 |
| `storefronts-inventory` | Storefronts inventory | 33,983 | 2024-01-26 |
| `business-improvement-areas-bia` | Business improvement areas (BIA) | 24 | 2025-04-07 |
| `food-vendors` | Food Vendors | 91 | 2020-11-19 |
| `film-office-work-areas` | Film office work areas | 22 | 2021-09-27 |

### Property and Development Theme (relevant datasets)

| Dataset ID | Title | Records | Last Modified |
|---|---|---|---|
| `local-area-boundary` | Local area boundary | 22 | 2023-06-24 |
| `zoning-districts-and-labels` | Zoning districts and labels | 1,611 | 2026-03-02 |

### Government and Finance Theme — Property Tax Family (complete)

| Dataset ID | Title | Records | Last Modified |
|---|---|---|---|
| `property-tax-report` | Property tax report (2020+) | 1,551,132 | 2026-03-02 |
| `property-tax-report-2016-2019` | Property tax report 2016-2019 | 832,969 | 2021-05-08 |
| `property-tax-report-2011-2015` | Property tax report 2011-2015 | 976,762 | 2021-05-08 |
| `property-tax-report-2006-2010` | Property tax report 2006-2010 | 892,028 | 2021-05-08 |

**Total property tax records across all 4 datasets**: approximately 4,252,891 rows (covering 2006–present).

### Summary: All Property Tax Data Coverage

| Dataset | Years Covered | Records | Notes |
|---|---|---|---|
| `property-tax-report-2006-2010` | 2006–2010 | 892,028 | Static; `previous_*_value` fields typed as text (empty); no zoning fields populated |
| `property-tax-report-2011-2015` | 2011–2015 | 976,762 | Static; `previous_*_value` absent for 2011–2013, present for 2014–2015; no zoning fields |
| `property-tax-report-2016-2019` | 2016–2019 | 832,969 | Static; `previous_*_value` present; zoning fields populated for some years |
| `property-tax-report` | 2020–present | 1,551,132 | Weekly updates for current year; zoning fields populated |

### Summary: All Business Licence Data Coverage

| Dataset | Years Covered | Records | Status | Categories |
|---|---|---|---|---|
| `business-licences-1997-to-2012` | 1997–2012 | 958,899 | Static | Original (pre-streamlining) — 500+ types |
| `business-licences-2013-to-2024` | 2013–May 2024 | 782,330 | Static (frozen May 2024) | Original (pre-streamlining) — 500+ types |
| `business-licences` | May 2024–present | 198,125 | Daily updates | New streamlined categories (<100 types) |

---

## 11. API Endpoints Reference

### Metadata Endpoints (GET, no authentication required)

```
# Full dataset metadata (metas, fields, attachments)
GET https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/{dataset-id}/

# Dataset records
GET https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/{dataset-id}/records/
  ?limit=100
  &offset=0
  &order_by={field} DESC
  &where={field} like "{value}"
  &select={field1},{field2}

# Catalog search by theme
GET https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/?refine=theme:{theme-name}&limit=50

# Catalog text search
GET https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/?q={search-term}&limit=50

# Export as CSV (direct download)
GET https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/{dataset-id}/exports/csv
```

**Note on SSL**: The API has intermittent TLS handshake failures when accessed with default Python SSL settings. Using `ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)` with `ctx.minimum_version = ssl.TLSVersion.TLSv1_2` and disabling certificate verification resolves this. Retry logic (3–5 attempts with 3–5s delays) is needed for reliable access.

### Known Dataset IDs for API Access

```
business-licences
business-licences-2013-to-2024
business-licences-1997-to-2012
property-tax-report
property-tax-report-2016-2019
property-tax-report-2011-2015
property-tax-report-2006-2010
local-area-boundary
zoning-districts-and-labels
storefronts-inventory
business-improvement-areas-bia
open-data-change-log
census-local-area-profiles-2016
census-local-area-profiles-2011
census-local-area-profiles-2006
census-local-area-profiles-2001
```

### Change Log for Specific Dataset (via portal)

```
https://opendata.vancouver.ca/explore/dataset/open-data-change-log/log/?disjunctive.datasets&sort=logdate&refine.datasetids={dataset-id}
```

### Change Log API (records endpoint)

```
GET https://opendata.vancouver.ca/api/explore/v2.1/catalog/datasets/open-data-change-log/records/
  ?limit=50
  &order_by=logdate DESC
```

---

## 12. Key Cross-Dataset Issues and Caveats

### Schema Inconsistencies Across Business Licence Datasets

| Field | `business-licences` (current) | `business-licences-2013-to-2024` | `business-licences-1997-to-2012` |
|---|---|---|---|
| `issueddate` type | datetime | datetime | **date** |
| `numberofemployees` type | **double** | text | text |
| `feepaid` type | double | double | **int** |
| `geo_point_2d` field | present | present | **absent** |

Implication: Vertical stacking of all three datasets requires type-casting before concat. `numberofemployees` should be treated as text/nullable across all datasets due to the "000 = unknown" encoding; cast to numeric after filtering out "000" and "0" sentinel values.

### Home-Based Business Address Redaction (2018)

Effective April 12, 2018, the City removed business addresses from home-based business licence categories across ALL historical data files (1997 forward). This is a retroactive modification — historical records for home-based businesses across all years have addresses removed, not just post-2018 records.

### Short-Term Rental Privacy Redaction (2019)

Effective July 2019, data files starting from 2017 were updated to remove the names of licence holders from the short term rental business licence category.

### Business Type Category Discontinuity (May 6, 2024)

- Pre-May 2024: 500+ discrete licence types in `businesstype` field (across `business-licences-1997-to-2012` and `business-licences-2013-to-2024`)
- Post-May 2024: <100 streamlined types in `businesstype` field (in `business-licences`)
- The self-serve mapping chart provides the official category crosswalk (URL above — currently requires browser access)
- The `*Historic*` suffix on business types indicates retired categories — these can appear in historical data and represent types that were in use before the streamlining
- Any time-series analysis of business activity by type spanning the May 2024 boundary requires category harmonization using the crosswalk

### Property Tax Value Definitions

**Critical distinction**: The `current_land_value` and `current_improvement_value` fields represent the **actual assessed market value** (fee simple interest as per the Assessment Act), NOT the taxable value. The taxable value is net of exemptions and may also be averaged for certain property classes (farm land, managed forests, etc.). The portal does not publish the net taxable value separately.

**Assessment roll timing**: Values are sourced from three rolls:
1. Completed Roll (received January) — initial values for the tax year
2. Revised Roll (received mid-March) — amendments to the Completed Roll
3. Supplementary Rolls (throughout the year) — amendments to individual properties

The data published reflects values as of the extraction date (see `report_year`), meaning a given year's data may reflect Completed, Revised, or Supplementary roll values depending on when the extract was taken.

### Zoning Data Availability in Property Tax Reports

- `zoning_district` and `zoning_classification` fields are **present in all property tax dataset schemas** but populated **only for records from approximately 2014 onwards** (when the City began including zoning data)
- For pre-2014 data, these fields will be empty/null in the downloaded data
- For authoritative current zoning geometry, use `zoning-districts-and-labels` dataset with a spatial join on property address or coordinates
- The 2021 change log entry notes that field names were aligned to Zoning and Development By-law Section 9 terminology — if you have data extracted before 2021, field names or values may differ slightly

### BCA Neighbourhood Code

The `neighbourhood_code` in property tax datasets is a 3-digit BCA-assigned identifier. The City does not publish the corresponding neighbourhood name mapping — it must be obtained directly from BC Assessment. This code is NOT the same as the City's 22 local areas. All BCA communication referencing a folio number must include the neighbourhood code prefix.

### Coordinate Coverage Gaps (Business Licences)

Business licence records may lack coordinates for several reasons (all documented by the publisher):
- Out-of-town business addresses (outside City of Vancouver) have no coordinates
- Some City of Vancouver addresses fail the geocoding process
- Home-based businesses: addresses removed (no coordinates) — affects all data for home-based business types across all years
- Short-term rental licence holders: names removed (affects data from 2017+)
- Records without coordinates appear in table data exports but would not appear in any map/GIS analysis

### LocalArea Field — Business Licences

The `localarea` field in all business licence datasets is described as a "manual selection from data custodian in source system." This means:
- It is not derived computationally from coordinates — it is entered manually in the licensing system
- It may not perfectly match a spatial join to the `local-area-boundary` polygons
- It is consistent with the 22 official local area names but may have historical variants (see "Arbutus-Ridge" vs "Arbutus Ridge" noted in the 2023 change log)

### LicenceRSN vs LicenceNumber

- `licencenumber` is the user-facing identifier but can be reused within a year
- `licencersn` is the true unique identifier — always use RSN for joining and deduplication
- `licencerevisionnumber` tracks versions of the same licence; 00 = original; higher numbers = amendments — when analyzing current status, take the highest revision number per RSN

---

*Document compiled on 2026-03-03.*
*Data sources: City of Vancouver Open Data Portal API (v2.1), portal information pages, Open Data Change Log (all 190 entries reviewed), web searches for supplementary documents.*
*All metadata from API calls is authoritative; HTML-rendered page content may differ due to dynamic loading.*
*Supplementary PDFs (self-serve chart, council reports) were unavailable for direct content extraction due to 403 restrictions — content described from web search results and change log entries.*
