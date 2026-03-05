# CT → Local Area Concordance

**File**: `data/processed/ct_local_area_concordance.csv`
**Built**: 2026-03-03
**Script**: `scripts/build_ct_concordance.py`

---

## Purpose

Maps Statistics Canada Census Tract (CT) identifiers to City of Vancouver
local area names for census years 2006, 2011, 2016, and 2021. Enables
joining census demographic data (which is at the CT level) to the business
panel (which uses CoV local area names).

---

## Output Schema

| Column | Type | Example | Description |
|--------|------|---------|-------------|
| `ct_id` | string | `9330014.01` | StatCan CTUID, always 10 chars with dot (e.g. `9330014.01`). CMA prefix `933` = Vancouver. |
| `census_year` | int | `2021` | Census year: 2006, 2011, 2016, or 2021 |
| `local_area` | string | `Killarney` | CoV local area name from `data/raw/local-area-boundary.geojson` |
| `overlap_fraction` | float | `0.746` | Fraction of CT area falling within this local area. Sums to 1.0 per (ct_id, census_year). |

---

## Coverage Summary

| Year | CTs in Vancouver CMA | CTs overlapping CoV (matched) | CoV local areas covered |
|------|---------------------|-------------------------------|------------------------|
| 2006 | 410 | 115 | 22/22 |
| 2011 | 457 | 123 | 22/22 |
| 2016 | 478 | 125 | 22/22 |
| 2021 | 535 | 133 | 22/22 |

**Why so few CTs matched?** The Vancouver CMA boundary (CMA code 933) covers
the entire Metro Vancouver region — Burnaby, Richmond, Surrey, Coquitlam, etc.
Only ~25-28% of CMA CTs fall within the City of Vancouver's 22 local areas.
All 22 local areas have CT coverage in every census year. This is correct and
expected.

**Sliver threshold**: CTs with <0.1% overlap with any local area are excluded.
Typically 4-6 CTs per year have minimal boundary grazing (e.g. a CT in Burnaby
whose western edge just touches the Vancouver boundary) and are correctly
excluded.

---

## Methodology

### Boundary Sources

**CT boundaries** (national shapefiles from Statistics Canada):

| Year | File | URL |
|------|------|-----|
| 2006 | `data/raw/census/boundaries/2006/gct_000b06a_e.shp` | `https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gct_000b06a_e.zip` |
| 2011 | `data/raw/census/boundaries/2011/gct_000b11a_e.shp` | `https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/gct_000b11a_e.zip` |
| 2016 | `data/raw/census/boundaries/2016/lct_000b16a_e.shp` | `https://www12.statcan.gc.ca/census-recensement/2011/geo/bound-limit/files-fichiers/2016/lct_000b16a_e.zip` |
| 2021 | `data/raw/census/boundaries/2021/lct_000b21a_e.shp` | `https://www12.statcan.gc.ca/census-recensement/2021/geo/sip-pis/boundary-limites/files-fichiers/lct_000b21a_e.zip` |

**Local area boundaries**: `data/raw/local-area-boundary.geojson` — 22 CoV polygons
(source: CoV open data catalog, dataset `local-area-boundary`).

### Projection

All geometries are reprojected to **BC Albers (EPSG:3005)**, an equal-area
projection appropriate for BC, before computing areas. The input CT shapefiles
use EPSG:4269 (2006, 2011) or EPSG:3347 (2021) or Lambert Conformal Conic
(2016); the local area GeoJSON uses EPSG:4326.

### Spatial Join

For each census year:
1. Filter national CT shapefile to Vancouver CMA (CMAUID = `'933'`, or
   CTUID prefix `'933'` for 2021 which has no CMAUID column)
2. Compute CT polygon area in BC Albers metres²
3. Spatial intersection (`gpd.overlay(..., how='intersection')`) of CT polygons
   with local area polygons
4. For each intersection fragment: `overlap_fraction = fragment_area / ct_area`
5. Filter out slivers: drop rows where `overlap_fraction < 0.001` (< 0.1%)
6. Normalize fractions per CT so they sum to 1.0 (handles floating-point drift)

### Multi-Area CTs

CTs that straddle local area boundaries are assigned fractional weights.
Approximately 60-65% of matched CTs fall entirely within one local area
(overlap_fraction = 1.0). The remainder span 2-4 local areas.

| Year | Single-area CTs | Multi-area CTs | Max areas per CT |
|------|----------------|----------------|-----------------|
| 2006 | 41 | 74 | 4 |
| 2011 | 50 | 73 | 4 |
| 2016 | 52 | 73 | 4 |
| 2021 | 58 | 75 | 4 |

---

## CT Identifier Formats

### The CTUID Format (concordance)

The concordance uses StatCan's canonical CTUID format: `{CMA}{CTNUM}.{SUFFIX}`

- CMA: 3-digit CMA code (`933` for Vancouver)
- CTNUM: 4-digit CT number (zero-padded)
- SUFFIX: 2-digit suffix (always 2 decimal places)

Examples: `9330001.01`, `9330025.00`, `9330187.11`

This format comes directly from the boundary shapefile CTUID attribute.

### Census Data Key Formats

When joining census data to this concordance, normalize the CT key:

| Year | Census data key | Format | How to join |
|------|----------------|--------|-------------|
| 2006 | `GEO_CODE` (numeric) | `933000101` (9 digits, no dot) | `code[:7] + '.' + code[7:]` |
| 2011 | `CTUID` (string) | `9330001.01` OR `9330025.0` (inconsistent!) | Pad `.0` suffix to `.00` |
| 2016 | `ALT_GEO_CODE` (numeric) | `933000101` (9 digits, no dot) | `code[:7] + '.' + code[7:]` |
| 2021 | `ALT_GEO_CODE` (string) | `9330001.01` OR `9330025.0` (inconsistent!) | Pad `.0` suffix to `.00` |

**Important note**: The 2011 and 2021 census data files inconsistently format
integer-suffix CTs (`x.00` type) as `x.0` (single decimal) vs the shapefile's
`x.00` (two decimal). Apply this normalization before joining:

```python
def normalize_ctuid(ctuid: str) -> str:
    """Normalize CTUID to always have 2 decimal places."""
    if '.' in ctuid:
        base, dec = ctuid.rsplit('.', 1)
        return f"{base}.{dec.zfill(2)}"
    return ctuid  # should not occur in Vancouver CMA CTs
```

Approximately 25-37 CTs per year are affected (those with `.00` suffix
= whole CT numbers like `9330025.00`).

---

## CT Boundary Changes Between Census Years

CT boundaries are revised between census cycles to reflect population growth
and geographic changes. Vancouver CMA CT counts grew from 410 (2006) to 535
(2021) — a 30% increase — due to CT splits in growing areas.

**Implication for longitudinal analysis**: The same geographic area will have
different CTs (different CTUID values) in different census years. The local
area concordance handles this per-year, so temporal comparisons should:
1. Join each year's census data to the concordance using that year's ct_id
2. Aggregate to local area level before comparing across years
3. Do not attempt to match CTs directly across years without a StatCan
   CT concordance table (e.g., the 2021 CT correspondence file)

---

## Edge Cases

### CTs spanning the CoV boundary

Several CTs in Burnaby, Richmond, or other municipalities have a small sliver
of area inside CoV. These are excluded by the 0.1% threshold. If needed for
edge-neighbourhood analysis, lower the threshold in the script.

### Water-covered CTs

The CoV boundary includes False Creek, Burrard Inlet water portions, and
English Bay. CT boundaries may include water areas. BC Albers area calculations
include water, which is correct for our proportional allocation purpose.

### CT 9330059

CT `9330059` appears in multiple variants (e.g., `9330059.07` through
`9330059.18` in 2021 census data). These are distinct split CTs, all within
Vancouver's Downtown/West End. All are correctly mapped.

---

## Usage Example

```python
import pandas as pd

concordance = pd.read_csv('data/processed/ct_local_area_concordance.csv',
                          dtype={'ct_id': str})

def normalize_ctuid(ctuid: str) -> str:
    if '.' in ctuid:
        base, dec = ctuid.rsplit('.', 1)
        return f"{base}.{dec.zfill(2)}"
    return ctuid

# 2021 census data (example: population by CT)
df21 = pd.read_csv('data/raw/census/2021_CT/vancouver_CMA_2021.csv',
                   encoding='latin-1', low_memory=False)
pop21 = df21[
    (df21['GEO_LEVEL'] == 'Census tract') &
    (df21['CHARACTERISTIC_NAME'] == 'Population, 2021')
][['ALT_GEO_CODE', 'C1_COUNT_TOTAL']].copy()
pop21['ct_id'] = pop21['ALT_GEO_CODE'].astype(str).apply(normalize_ctuid)

# Join to concordance
joined = pop21.merge(
    concordance[concordance['census_year'] == 2021],
    on='ct_id',
    how='inner'
)

# Weighted aggregation to local area
joined['pop_allocated'] = joined['C1_COUNT_TOTAL'].astype(float) * joined['overlap_fraction']
local_pop = joined.groupby('local_area')['pop_allocated'].sum().reset_index()
local_pop.columns = ['local_area', 'population_2021']
```
