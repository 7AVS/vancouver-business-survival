# Survival Tracking Validation
*Generated: 2026-03-03 18:57*

## Summary

| Metric | Value |
|--------|-------|
| Total panel businesses | 113,858 |
| Estimated correctly tracked | ~104,900 (92%) |
| Estimated false entities | ~8,958 |
| Estimated false death rate | ~15.8% |
| Estimated false birth rate | ~15.8% |
| A15-specific address flips (FY17→FY18) | 2,956 names |
| Panel addr-split false entities | 2,760 (2.42%) |
| 1-year deaths (FY14–24) | 9,171 |
| False death rate in 1-yr sample | 21% |
| Multi-year businesses with timeline gaps | 16,670 (17.4%) |

---

## Check 1 — A15 / Home-Based Business Address Wipe

### Finding
A15 retroactive wipe appears already applied in source data: address presence rates are STABLE across all years (range 7.7pp, 61.9–69.6%). No FY17->FY18 spike in address loss. However, 2,756 business names appear in the panel BOTH with and without addresses (2,760 null-addr entries that share a name with an addr entry), representing ~2.4% of the panel as potential false identity splits.

### Address Presence by Year

| FY | Year | Rows | With Address | % |
|----|------|------|-------------|---|
| 13 | 2013 | 44,697 | 28,128 | 62.9% |
| 14 | 2014 | 43,122 | 27,853 | 64.6% |
| 15 | 2015 | 43,653 | 27,812 | 63.7% |
| 16 | 2016 | 45,493 | 28,167 | 61.9% |
| 17 | 2017 | 42,703 | 28,247 | 66.1% |
| 18 | 2018 | 42,653 | 28,274 | 66.3% |
| 19 | 2019 | 43,401 | 28,439 | 65.5% |
| 20 | 2020 | 40,296 | 26,523 | 65.8% |
| 21 | 2021 | 41,498 | 27,381 | 66.0% |
| 22 | 2022 | 42,248 | 28,198 | 66.7% |
| 23 | 2023 | 45,106 | 29,793 | 66.1% |
| 24 | 2024 | 42,230 | 29,238 | 69.2% |
| 25 | 2025 | 42,304 | 29,429 | 69.6% |
| 26 | 2026 | 38,499 | 26,679 | 69.3% |

### Interpretation

The City's April 2018 bylaw (A15) retroactively removed addresses for home-based businesses
back to 1997. However, because the source data was extracted in April 2025, this wipe was
**already applied** before we received the data. Address presence rates are stable across
all 14 fiscal years (61.9%–69.6%, a range of only
7.7 percentage points), confirming no FY17→FY18 structural break.

The residual problem is identity splitting: the panel key is `hash(name + house + street)`.
Home-based businesses have null addresses in all years, so they are consistently hashed as
`hash(name||)`. They track correctly within the null-address cohort. The **2,756 names**
that appear in the panel **both with and without addresses** represent the real risk —
these businesses likely changed from a commercial address to a home office (or vice versa)
and are recorded as two separate panel entities. This affects **2,760
null-addr panel entries** (2.42% of the panel).

---

## Check 2 — Name Matching Quality

### Finding
12,336 panel names have punctuation-only variants; 12,307 differ only by Ltd/Inc suffix; 11,682 differ only by 'The' prefix — but most of these represent genuine distinct businesses at different locations. In a 100-business sample of 1-year deaths (FY14-FY24), 21 (21%) appear in the licence data across multiple years under the same name, suggesting a matching failure rather than a true closure.

### One-Year Deaths by Fiscal Year

| FY | Year | 1-Year Deaths |
|----|------|--------------|
| 14 | 2014 | 1,181 |
| 15 | 2015 | 1,305 |
| 16 | 2016 | 969 |
| 17 | 2017 | 771 |
| 18 | 2018 | 593 |
| 19 | 2019 | 622 |
| 20 | 2020 | 271 |
| 21 | 2021 | 417 |
| 22 | 2022 | 626 |
| 23 | 2023 | 1,174 |
| 24 | 2024 | 1,242 |

Note: FY13 has 5,853 one-year entries — these are almost certainly businesses that existed
before FY13 but whose history is not in our dataset, not true one-year deaths.

### Sample: 1-Year Deaths That Reappear Elsewhere (21 of 100)

- **Barbara Elaine Janzen (Barbara Janzen)**
  - Panel: year=15, addr=900 HOWE ST
  - Licences: appears in years [15, 16, 17]
  - Streets seen: ['HOWE ST', 'W GEORGIA ST']
- **Kit and Ace Apparel Inc**
  - Panel: year=19, addr=165 WATER ST
  - Licences: appears in years [17, 18, 19]
  - Streets seen: ['ALEXANDER ST', 'W 4TH AV', 'W 7TH AV', 'WATER ST']
- **Wales Young Education Inc**
  - Panel: year=14, addr=938 HOWE ST
  - Licences: appears in years [14, 15, 16, 17, 18, 19, 20, 21, 23]
  - Streets seen: ['HOWE ST', 'TERMINAL AV', 'THURLOW ST']
- **(Jenny Wu)**
  - Panel: year=23, addr=4979 DUCHESS STREET
  - Licences: appears in years [19, 21, 23]
  - Streets seen: ['DUCHESS STREET']
- **Atkinson & Company CPA Inc**
  - Panel: year=18, addr=8167 MAIN ST
  - Licences: appears in years [18, 19, 20, 21, 22, 23, 24, 25]
  - Streets seen: ['MAIN ST', 'W 75TH AV']
- **Spawnlab Technologies Corp**
  - Panel: year=21, addr=nan nan
  - Licences: appears in years [21, 22, 23, 24]
  - Streets seen: ['SEYMOUR ST']
- **Alliance Facility Solutions Inc**
  - Panel: year=21, addr=nan nan
  - Licences: appears in years [21, 22, 23, 24, 25, 26]
  - Streets seen: ['W HASTINGS ST']
- **Asiana Trading Ltd**
  - Panel: year=17, addr=1155 W PENDER ST
  - Licences: appears in years [17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
  - Streets seen: ['W PENDER ST']
- **Royal Bank of Canada**
  - Panel: year=24, addr=4498 W 10TH AV
  - Licences: appears in years [13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26]
  - Streets seen: ['ARBUTUS ST', 'COMMERCIAL DR', 'DAVIE ST', 'DENMAN ST']
- **Shoreline Studios Inc & 0925395 BC Ltd**
  - Panel: year=16, addr=1425 CHARLES ST
  - Licences: appears in years [13, 14, 15, 16]
  - Streets seen: ['CHARLES ST', 'E 7TH AV']

### Near-Duplicate Name Counts in Panel

| Normalization Type | Names with Variants |
|-------------------|---------------------|
| Punctuation stripped | 12,336 |
| Ltd/Inc suffix removed | 12,307 |
| 'The' prefix removed | 11,682 |

These overlap heavily. Most represent genuine separate businesses at different locations
(e.g., multiple Tim Hortons franchises, different numbered BC corporations). The ~21%
false death rate in the sample is dominated by **address-change relocations**, not pure
name-variation failures. Name case and punctuation are normalized in the pipeline, so
`Joe's Pizza` vs `JOES PIZZA` would produce different IDs only due to the apostrophe,
which is a genuine normalization gap.

---

## Check 3 — Address Matching Quality

### Finding
9,197 business names have multiple panel entries across different addresses. 230 names with 5+ distinct street locations are likely chains (correctly split by location). 7,843 names with 2–4 distinct streets are likely relocations miscounted as new businesses. 1,124 names have multiple panel entries at the same address (likely duplicate licence years, not distinct entities).

### Address Multiplicity in Panel

| Category | Count |
|----------|-------|
| Names with multiple panel entries | 9,197 |
| Likely chains (5+ distinct streets) | 230 |
| Likely relocations (2–4 distinct streets) | 7,843 |
| Multiple entries at same address | 1,124 |

### Interpretation

Chains are **correctly handled** by the panel design — each location is a separate economic
unit, and the panel correctly gives each a unique entry. The relocation problem is more
significant: **7,843 businesses** appear to have moved addresses
and are counted as 2–4 distinct panel entities. Using a conservative 50% rate (many of these
may be deliberate multi-location expansions), this represents ~3,921
falsely-split entities, each generating one false death and one false birth.

---

## Check 4 — Temporal Consistency

### Finding
16,670 of 96,079 multi-year businesses (17.4%) have at least one gap in their timeline. 11,357 gaps are 1 year (likely data artifact or licence lapse), while 5,313 are 2+ years (more likely genuine closures/reopenings). Each gap represents a potential false death + false birth pair if treated as two entities.

### Gap Summary

| Metric | Value |
|--------|-------|
| Multi-year businesses | 96,079 |
| With at least one gap | 16,670 (17.4%) |
| 1-year gaps | 11,357 |
| 2+ year gaps | 5,313 |
| Average gap size | 1.5 years |

### Interpretation

A 17.4% gap rate is high but not alarming in isolation — licence data is administrative
and businesses routinely lapse for a year (renewal delay, temporary closure, address
change within same commercial block). The **1-year gap cohort (11,357 businesses)**
is the primary concern: these may represent valid businesses that missed one renewal
cycle rather than genuine closures. Treating them as died+reborn would inflate both
false death and false birth counts by up to 11,357 each.

The **2+ year gap cohort (5,313)** is more likely to contain genuine closures and
reopenings (or new businesses that happen to share a name+address with a prior one).

---

## Check 5 — Overall Panel Reliability

### False Entity Decomposition

| Source of Error | Estimated False Entities | % of Panel |
|----------------|--------------------------|-----------|
| Address splits (A15 / home-biz) | 2,760 | 2.4% |
| Relocation miscounts (conservative) | 3,921 | 3.4% |
| Name variation splits (conservative 2%) | 2,277 | 2.0% |
| **Total** | **8,958** | **7.9%** |

### Summary

- **Panel size**: 113,858 unique entities
- **Estimated correctly tracked**: ~104,900 (92%)
- **Estimated false death rate**: ~15.8%
- **Estimated false birth rate**: ~15.8%

### What This Means for the Analysis

The panel is **broadly reliable** for macro survival analysis (cohort trends, sector-level
survival curves, neighbourhood comparisons). The ~11% noise rate is concentrated in
specific failure modes:

1. **Home-based businesses** (null-address cohort, 38% of panel): internally consistent
   but isolated from the commercial-address cohort. Cross-cohort comparisons are unreliable.
   Restrict aggregate survival analysis to the **commercial-address cohort** (70,360 entries)
   where the false-split rate is lower.

2. **Relocating businesses** (~3,900 conservative estimate): inflate business birth counts
   and death counts simultaneously. For survival analysis, this biases the **hazard rate
   upward** (businesses appear to die sooner) and the **entry rate upward** (new entrants
   are partly relocated incumbents). Magnitude: ~3.4% of the commercial-address panel.

3. **1-year gap businesses** (11,357): these are at risk of being split into died+reborn
   pairs in cohort analysis. If gaps are ignored and only first/last year are used (as the
   current panel does via `first_year`/`last_year`), this problem is **mitigated** — the
   panel already treats them as continuous because it records the span endpoints, not year-by-year
   presence. The gap issue only matters if you rebuild year-by-year presence from the panel.

### Recommended Mitigations

1. **Restrict to commercial-address cohort** for primary survival analysis (exclude null-addr).
2. **Add a "relocation flag"**: for any business_id that `last_year < current_year`, check if
   the same name appears in a later year at a different address. Flag those as "possible
   relocation" rather than confirmed death.
3. **Treat 1-year gaps as continuous**: a business absent for exactly 1 year should not be
   split. Apply a gap-filling rule: if present in year N and year N+2, treat year N+1 as
   present (licence lapse assumption).
4. **Name normalization improvement**: strip punctuation AND suffixes from the hash key.
   `Joe's Pizza Ltd` and `Joes Pizza` would then hash identically, reducing false splits.

---

## Appendix: Data Quality by Dimension

| Dimension | Reliability | Notes |
|-----------|-------------|-------|
| Name matching (exact) | High | Pipeline uppercases and strips whitespace; punctuation not stripped |
| Address matching | Medium | ~34% null-address rate; null is stable (not a data error) |
| Year continuity | Medium-High | 17% gap rate; mostly 1-year lapses |
| Identity splitting (addr change) | Medium | Relocation creates false death+birth; no mitigation in pipeline |
| A15 retroactive wipe | Not a current problem | Wipe already applied in source data extract |
| Chain detection | Good | Each location correctly tracked separately |
| FY13 cohort completeness | Low | 5,853 one-year entries — likely truncation, not real 1-yr closures |
| FY26 cohort completeness | Low | Data extract mid-year; use with caution |

*Note: "Reliability" refers to the field's usefulness for survival tracking, not raw completeness.*
