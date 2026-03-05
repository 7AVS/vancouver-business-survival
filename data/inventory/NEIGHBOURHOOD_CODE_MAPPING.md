# Vancouver Neighbourhood Code Mapping
**Generated**: 2026-03-03 14:50
**Method**: Bulk spatial join — stratified sample of 50 addresses per code, BC Geocoder API, Shapely point-in-polygon
**Status**: DEFINITIVE (replaces coin-flip 2-sample approach)

---

## 1. Executive Summary

| Metric | Value |
|--------|-------|
| Total addresses sampled | 1461 |
| Successfully geocoded | 1461 (100.0%) |
| Clean pip assignments (used in distribution) | 1264 (86.5% of geocoded) |
| Nearest-centroid fallbacks (excluded from distribution) | 197 |
| Failed geocoding | 0 |
| HIGH confidence codes (≥80% in primary area) | 3/30 |
| MEDIUM confidence codes (60-79%) | 9/30 |
| LOW confidence codes (<60%, genuinely multi-area) | 18/30 |
| INSUFFICIENT pip sample (<5 clean results) | 0/30 |
| NO_DATA codes | 0/30 |
| CoV areas covered (appear as primary or secondary) | 22/22 |
| CoV areas with zero codes assigned | 0 |

✓ All 22 CoV local areas are represented in the mapping.

---

## 2. Neighbourhood Code Lookup Table

| Code | Primary Area | Pct | Secondary Area | Pct | PIP/Geocoded/Sampled | Confidence |
|------|-------------|-----|----------------|-----|----------------------|------------|
| 001 | Mount Pleasant | 54.0% | Dunbar-Southlands | 32.0% | 50/50/50 | LOW |
| 002 | Mount Pleasant | 65.9% | Arbutus Ridge | 12.2% | 41/50/50 | MEDIUM |
| 003 | Riley Park | 90.0% | Dunbar-Southlands | 5.0% | 40/50/50 | HIGH |
| 004 | Arbutus Ridge | 65.6% | Riley Park | 28.1% | 32/50/50 | MEDIUM |
| 005 | Oakridge | 38.3% | Riley Park | 25.5% | 47/50/50 | LOW |
| 006 | Marpole | 44.4% | Dunbar-Southlands | 22.2% | 9/11/11 | LOW |
| 007 | Mount Pleasant | 47.7% | Fairview | 36.4% | 44/50/50 | LOW |
| 008 | Oakridge | 61.0% | Shaughnessy | 26.8% | 41/50/50 | MEDIUM |
| 009 | Riley Park | 48.9% | Downtown | 40.4% | 47/50/50 | LOW |
| 010 | Kerrisdale | 50.0% | Oakridge | 37.0% | 46/50/50 | LOW |
| 011 | Marpole | 31.7% | Oakridge | 29.3% | 41/50/50 | LOW |
| 012 | Marpole | 44.7% | Downtown | 14.9% | 47/50/50 | LOW |
| 013 | Mount Pleasant | 48.8% | Strathcona | 16.3% | 43/50/50 | LOW |
| 014 | Mount Pleasant | 31.2% | Hastings-Sunrise | 29.2% | 48/50/50 | LOW |
| 015 | Riley Park | 37.5% | Mount Pleasant | 22.5% | 40/50/50 | LOW |
| 016 | Riley Park | 65.2% | Sunset | 23.9% | 46/50/50 | MEDIUM |
| 017 | Sunset | 42.3% | Riley Park | 26.9% | 26/50/50 | LOW |
| 018 | Killarney | 82.1% | Marpole | 10.7% | 28/50/50 | HIGH |
| 019 | Sunset | 30.6% | Riley Park | 30.6% | 49/50/50 | LOW |
| 020 | Hastings-Sunrise | 71.4% | Strathcona | 24.5% | 49/50/50 | MEDIUM |
| 021 | Mount Pleasant | 44.9% | Hastings-Sunrise | 26.5% | 49/50/50 | LOW |
| 022 | Riley Park | 52.0% | Renfrew-Collingwood | 20.0% | 50/50/50 | LOW |
| 023 | Renfrew-Collingwood | 36.4% | Killarney | 27.3% | 44/50/50 | LOW |
| 024 | Sunset | 38.8% | Killarney | 26.5% | 49/50/50 | LOW |
| 025 | Sunset | 72.5% | Killarney | 20.0% | 40/50/50 | MEDIUM |
| 026 | Downtown | 60.0% | Strathcona | 13.3% | 45/50/50 | MEDIUM |
| 027 | West End | 58.5% | Downtown | 39.0% | 41/50/50 | LOW |
| 028 | Downtown | 66.7% | West End | 20.0% | 45/50/50 | MEDIUM |
| 029 | Downtown | 97.7% | West End | 2.3% | 44/50/50 | HIGH |
| 030 | Downtown | 76.7% | Mount Pleasant | 9.3% | 43/50/50 | MEDIUM |

---

## 3. Methodology

### 3.1 Data Sources
- **Property tax data**: 4 CSV files, 4.25M rows total (2006–present)
- **Boundary polygons**: CoV local area boundary GeoJSON (22 features)
- **Geocoding service**: BC Geocoder API (geocoder.api.gov.bc.ca) — provincial government, no auth, excellent BC coverage

### 3.2 Sampling Strategy
With ~126,000 unique civic addresses across 30 codes, full geocoding would take ~10 hours. Stratified sample:
1. Extract all unique (from_civic_number, street_name, property_postal_code) per code
2. Sample up to 50 per code (stratified random, seed=42)
3. Total sample: ~1461 addresses (~0.3 sec/request ≈ 7 minutes)

### 3.3 Point-in-Polygon Test
- Shapely v2.x `contains()` on each of 22 CoV boundary polygons
- Coordinates: (lon, lat) in WGS84 (BC Geocoder returns WGS84)
- Fallback for points outside all polygons: nearest centroid — **EXCLUDED from code distributions** because the fallback is unreliable (a point slightly outside the Downtown polygon may get assigned to Hastings-Sunrise whose centroid is closest geometrically but semantically wrong). Only pip-confirmed assignments are used for code-to-area distributions.

### 3.4 Confidence Levels
- **HIGH**: Primary area captures ≥80% of geocoded addresses in that code
- **MEDIUM**: Primary area captures 60–79%
- **LOW**: Primary area captures <60% — code genuinely spans multiple areas, fractional assignment appropriate
- **NO_DATA**: Zero successful geocodes for this code

### 3.5 What This Means for Analysis
- HIGH confidence codes: safe to use as a proxy for a single CoV area
- LOW confidence codes: do NOT treat as a single area. Weight by percentage or stratify separately.
- Missing areas: if all 22 areas are covered, the mapping is complete. If any are missing, properties in those areas will be misclassified.

---

## 4. Distribution by Code

#### Code 001
Sampled: 50 | Geocoded: 50 | PIP (used): 50 | Centroid-fallback (excluded): 0 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Mount Pleasant | 27 | 54.0% |
| Dunbar-Southlands | 16 | 32.0% |
| West Point Grey | 6 | 12.0% |
| Riley Park | 1 | 2.0% |
#### Code 002
Sampled: 50 | Geocoded: 50 | PIP (used): 41 | Centroid-fallback (excluded): 9 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Mount Pleasant | 27 | 65.9% |
| Arbutus Ridge | 5 | 12.2% |
| Kitsilano | 4 | 9.8% |
| Fairview | 3 | 7.3% |
| Dunbar-Southlands | 1 | 2.4% |
| Shaughnessy | 1 | 2.4% |
#### Code 003
Sampled: 50 | Geocoded: 50 | PIP (used): 40 | Centroid-fallback (excluded): 10 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Riley Park | 36 | 90.0% |
| Dunbar-Southlands | 2 | 5.0% |
| South Cambie | 1 | 2.5% |
| Oakridge | 1 | 2.5% |
#### Code 004
Sampled: 50 | Geocoded: 50 | PIP (used): 32 | Centroid-fallback (excluded): 18 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Arbutus Ridge | 21 | 65.6% |
| Riley Park | 9 | 28.1% |
| Strathcona | 1 | 3.1% |
| Downtown | 1 | 3.1% |
#### Code 005
Sampled: 50 | Geocoded: 50 | PIP (used): 47 | Centroid-fallback (excluded): 3 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Oakridge | 18 | 38.3% |
| Riley Park | 12 | 25.5% |
| Arbutus Ridge | 9 | 19.1% |
| Sunset | 2 | 4.3% |
| South Cambie | 2 | 4.3% |
| Kensington-Cedar Cottage | 1 | 2.1% |
| Mount Pleasant | 1 | 2.1% |
| Marpole | 1 | 2.1% |
| Shaughnessy | 1 | 2.1% |
#### Code 006
Sampled: 11 | Geocoded: 11 | PIP (used): 9 | Centroid-fallback (excluded): 2 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Marpole | 4 | 44.4% |
| Dunbar-Southlands | 2 | 22.2% |
| Kerrisdale | 2 | 22.2% |
| Sunset | 1 | 11.1% |
#### Code 007
Sampled: 50 | Geocoded: 50 | PIP (used): 44 | Centroid-fallback (excluded): 6 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Mount Pleasant | 21 | 47.7% |
| Fairview | 16 | 36.4% |
| Strathcona | 2 | 4.5% |
| South Cambie | 2 | 4.5% |
| Riley Park | 1 | 2.3% |
| Marpole | 1 | 2.3% |
| Shaughnessy | 1 | 2.3% |
#### Code 008
Sampled: 50 | Geocoded: 50 | PIP (used): 41 | Centroid-fallback (excluded): 9 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Oakridge | 25 | 61.0% |
| Shaughnessy | 11 | 26.8% |
| Riley Park | 5 | 12.2% |
#### Code 009
Sampled: 50 | Geocoded: 50 | PIP (used): 47 | Centroid-fallback (excluded): 3 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Riley Park | 23 | 48.9% |
| Downtown | 19 | 40.4% |
| South Cambie | 3 | 6.4% |
| Strathcona | 2 | 4.3% |
#### Code 010
Sampled: 50 | Geocoded: 50 | PIP (used): 46 | Centroid-fallback (excluded): 4 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Kerrisdale | 23 | 50.0% |
| Oakridge | 17 | 37.0% |
| Sunset | 5 | 10.9% |
| Shaughnessy | 1 | 2.2% |
#### Code 011
Sampled: 50 | Geocoded: 50 | PIP (used): 41 | Centroid-fallback (excluded): 9 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Marpole | 13 | 31.7% |
| Oakridge | 12 | 29.3% |
| Downtown | 8 | 19.5% |
| Fairview | 4 | 9.8% |
| Mount Pleasant | 2 | 4.9% |
| Sunset | 2 | 4.9% |
#### Code 012
Sampled: 50 | Geocoded: 50 | PIP (used): 47 | Centroid-fallback (excluded): 3 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Marpole | 21 | 44.7% |
| Downtown | 7 | 14.9% |
| Fairview | 6 | 12.8% |
| Oakridge | 3 | 6.4% |
| Kerrisdale | 3 | 6.4% |
| Mount Pleasant | 2 | 4.3% |
| Shaughnessy | 2 | 4.3% |
| Grandview-Woodland | 1 | 2.1% |
| Riley Park | 1 | 2.1% |
| Sunset | 1 | 2.1% |
#### Code 013
Sampled: 50 | Geocoded: 50 | PIP (used): 43 | Centroid-fallback (excluded): 7 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Mount Pleasant | 21 | 48.8% |
| Strathcona | 7 | 16.3% |
| Downtown | 5 | 11.6% |
| Riley Park | 4 | 9.3% |
| Fairview | 3 | 7.0% |
| Sunset | 2 | 4.7% |
| Grandview-Woodland | 1 | 2.3% |
#### Code 014
Sampled: 50 | Geocoded: 50 | PIP (used): 48 | Centroid-fallback (excluded): 2 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Mount Pleasant | 15 | 31.2% |
| Hastings-Sunrise | 14 | 29.2% |
| Grandview-Woodland | 12 | 25.0% |
| Strathcona | 4 | 8.3% |
| Downtown | 3 | 6.2% |
#### Code 015
Sampled: 50 | Geocoded: 50 | PIP (used): 40 | Centroid-fallback (excluded): 10 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Riley Park | 15 | 37.5% |
| Mount Pleasant | 9 | 22.5% |
| Kensington-Cedar Cottage | 8 | 20.0% |
| Grandview-Woodland | 4 | 10.0% |
| Strathcona | 2 | 5.0% |
| Sunset | 1 | 2.5% |
| Downtown | 1 | 2.5% |
#### Code 016
Sampled: 50 | Geocoded: 50 | PIP (used): 46 | Centroid-fallback (excluded): 4 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Riley Park | 30 | 65.2% |
| Sunset | 11 | 23.9% |
| Strathcona | 2 | 4.3% |
| Kensington-Cedar Cottage | 1 | 2.2% |
| Downtown | 1 | 2.2% |
| Mount Pleasant | 1 | 2.2% |
#### Code 017
Sampled: 50 | Geocoded: 50 | PIP (used): 26 | Centroid-fallback (excluded): 24 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Sunset | 11 | 42.3% |
| Riley Park | 7 | 26.9% |
| Grandview-Woodland | 6 | 23.1% |
| Mount Pleasant | 1 | 3.8% |
| Downtown | 1 | 3.8% |
#### Code 018
Sampled: 50 | Geocoded: 50 | PIP (used): 28 | Centroid-fallback (excluded): 22 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Killarney | 23 | 82.1% |
| Marpole | 3 | 10.7% |
| Sunset | 1 | 3.6% |
| Riley Park | 1 | 3.6% |
#### Code 019
Sampled: 50 | Geocoded: 50 | PIP (used): 49 | Centroid-fallback (excluded): 1 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Sunset | 15 | 30.6% |
| Riley Park | 15 | 30.6% |
| Grandview-Woodland | 14 | 28.6% |
| Kensington-Cedar Cottage | 4 | 8.2% |
| Victoria-Fraserview | 1 | 2.0% |
#### Code 020
Sampled: 50 | Geocoded: 50 | PIP (used): 49 | Centroid-fallback (excluded): 1 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Hastings-Sunrise | 35 | 71.4% |
| Strathcona | 12 | 24.5% |
| Downtown | 2 | 4.1% |
#### Code 021
Sampled: 50 | Geocoded: 50 | PIP (used): 49 | Centroid-fallback (excluded): 1 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Mount Pleasant | 22 | 44.9% |
| Hastings-Sunrise | 13 | 26.5% |
| Grandview-Woodland | 7 | 14.3% |
| Strathcona | 5 | 10.2% |
| Fairview | 2 | 4.1% |
#### Code 022
Sampled: 50 | Geocoded: 50 | PIP (used): 50 | Centroid-fallback (excluded): 0 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Riley Park | 26 | 52.0% |
| Renfrew-Collingwood | 10 | 20.0% |
| Hastings-Sunrise | 8 | 16.0% |
| Mount Pleasant | 5 | 10.0% |
| Strathcona | 1 | 2.0% |
#### Code 023
Sampled: 50 | Geocoded: 50 | PIP (used): 44 | Centroid-fallback (excluded): 6 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Renfrew-Collingwood | 16 | 36.4% |
| Killarney | 12 | 27.3% |
| Mount Pleasant | 5 | 11.4% |
| Hastings-Sunrise | 3 | 6.8% |
| Riley Park | 3 | 6.8% |
| Victoria-Fraserview | 2 | 4.5% |
| Kensington-Cedar Cottage | 2 | 4.5% |
| Shaughnessy | 1 | 2.3% |
#### Code 024
Sampled: 50 | Geocoded: 50 | PIP (used): 49 | Centroid-fallback (excluded): 1 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Sunset | 19 | 38.8% |
| Killarney | 13 | 26.5% |
| Mount Pleasant | 9 | 18.4% |
| Renfrew-Collingwood | 4 | 8.2% |
| Victoria-Fraserview | 3 | 6.1% |
| Grandview-Woodland | 1 | 2.0% |
#### Code 025
Sampled: 50 | Geocoded: 50 | PIP (used): 40 | Centroid-fallback (excluded): 10 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Sunset | 29 | 72.5% |
| Killarney | 8 | 20.0% |
| Grandview-Woodland | 2 | 5.0% |
| Victoria-Fraserview | 1 | 2.5% |
#### Code 026
Sampled: 50 | Geocoded: 50 | PIP (used): 45 | Centroid-fallback (excluded): 5 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Downtown | 27 | 60.0% |
| Strathcona | 6 | 13.3% |
| West End | 6 | 13.3% |
| Hastings-Sunrise | 3 | 6.7% |
| Grandview-Woodland | 2 | 4.4% |
| Fairview | 1 | 2.2% |
#### Code 027
Sampled: 50 | Geocoded: 50 | PIP (used): 41 | Centroid-fallback (excluded): 9 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| West End | 24 | 58.5% |
| Downtown | 16 | 39.0% |
| Mount Pleasant | 1 | 2.4% |
#### Code 028
Sampled: 50 | Geocoded: 50 | PIP (used): 45 | Centroid-fallback (excluded): 5 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Downtown | 30 | 66.7% |
| West End | 9 | 20.0% |
| Grandview-Woodland | 4 | 8.9% |
| Hastings-Sunrise | 2 | 4.4% |
#### Code 029
Sampled: 50 | Geocoded: 50 | PIP (used): 44 | Centroid-fallback (excluded): 6 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Downtown | 43 | 97.7% |
| West End | 1 | 2.3% |
#### Code 030
Sampled: 50 | Geocoded: 50 | PIP (used): 43 | Centroid-fallback (excluded): 7 | Geocode failures: 0
*(Percentages are of PIP-confirmed assignments only)*

| Local Area | Count | Pct of PIP |
|-----------|-------|------------|
| Downtown | 33 | 76.7% |
| Mount Pleasant | 4 | 9.3% |
| West End | 2 | 4.7% |
| Renfrew-Collingwood | 1 | 2.3% |
| Riley Park | 1 | 2.3% |
| Shaughnessy | 1 | 2.3% |
| Fairview | 1 | 2.3% |

---

## 5. Temporal Stability Check

Sampled **200** PIDs from **231,483** total multi-year PIDs.

| Metric | Value |
|--------|-------|
| PIDs stable (same code all years) | 200 (100.0%) |
| PIDs with code changes | 0 |

*All sampled PIDs had stable neighbourhood codes across years.*


---

## 6. Area Name Normalization

| GeoJSON Name | Business Licence Name | Canonical | Notes |
|-------------|----------------------|-----------|-------|
| Arbutus Ridge | Arbutus-Ridge | Arbutus Ridge | hyphen_diff |
| Downtown | Downtown | Downtown |  |
| Dunbar-Southlands | Dunbar-Southlands | Dunbar-Southlands |  |
| Fairview | Fairview | Fairview |  |
| Grandview-Woodland | Grandview-Woodland | Grandview-Woodland |  |
| Hastings-Sunrise | Hastings-Sunrise | Hastings-Sunrise |  |
| Kensington-Cedar Cottage | Kensington-Cedar Cottage | Kensington-Cedar Cottage |  |
| Kerrisdale | Kerrisdale | Kerrisdale |  |
| Killarney | Killarney | Killarney |  |
| Kitsilano | Kitsilano | Kitsilano |  |
| Marpole | Marpole | Marpole |  |
| Mount Pleasant | Mount Pleasant | Mount Pleasant |  |
| Oakridge | Oakridge | Oakridge |  |
| Renfrew-Collingwood | Renfrew-Collingwood | Renfrew-Collingwood |  |
| Riley Park | Riley Park | Riley Park |  |
| Shaughnessy | Shaughnessy | Shaughnessy |  |
| South Cambie | South Cambie | South Cambie |  |
| Strathcona | Strathcona | Strathcona |  |
| Sunset | Sunset | Sunset |  |
| Victoria-Fraserview | Victoria-Fraserview | Victoria-Fraserview |  |
| West End | West End | West End |  |
| West Point Grey | West Point Grey | West Point Grey |  |

---

## 7. Limitations and Future Work

1. **Sample size**: 50 samples per code. For codes with LOW confidence, increasing to 50–100 samples would give tighter percentage estimates.
2. **Null civic numbers**: 52.9% of rows have no civic number and cannot be geocoded by this method. Street-level geocoding (street + postal only) would give lower-confidence assignments for these.
3. **Temporal coverage**: Sampled addresses include all years (2006–present). Earlier years may have fewer unique addresses in some codes.
4. **BC Geocoder accuracy**: The BC Geocoder returns coordinates for all queried addresses (100% geocode success), but ~13.5% of returned coordinates fell outside all 22 CoV polygon boundaries and were excluded from distributions via the nearest-centroid fallback.
5. **Full geocoding**: For production use with >1000 samples per code, consider Canada Post AddressComplete API (paid) or Natural Resources Canada (free but rate-limited).

---

*Generated by geocode_bulk.py on 2026-03-03 14:50.*
*Replaces the 2-sample coin-flip approach reviewed in A1_APPROACH_REVIEW.md.*
