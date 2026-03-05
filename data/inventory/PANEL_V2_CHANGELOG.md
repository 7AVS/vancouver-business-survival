# Panel V2 Changelog
*Generated: 2026-03-03 19:07*

## Overview

This document records the changes between `commercial-panel.csv` (v1) and
`commercial-panel-v2.csv` (v2). V2 applies four survival-tracking mitigations
to reduce the estimated ~15.8% false death rate identified in
`SURVIVAL_TRACKING_VALIDATION.md`.

---

## Mitigations Applied

### 1. Improved Name Normalization

Before hashing `business_id`, the business name is now:
- Lowercased
- All punctuation stripped (apostrophes, periods, commas, hyphens → space)
- Leading "the " removed
- Common legal suffixes removed: `ltd`, `inc`, `corp`, `llc`, `co`, `limited`,
  `incorporated`, `company`, `enterprises`
- Extra whitespace collapsed

**Result**: `"Joe's Pizza Ltd."` and `"Joes Pizza"` now produce the same ID.

| Metric | Value |
|--------|-------|
| Rows where ID changed by normalization | 597,825 |
| Unique IDs before normalization (v1) | 113,858 |
| Unique IDs after normalization (pre-reloc) | 113,288 |
| **Businesses merged by name normalization** | **570** |

### 2. Relocation Detection

After initial aggregation by normalized name+address, entries for the same
normalized name at multiple addresses are inspected:

- **2–4 distinct addresses** → treated as one relocated business.
  The earliest address is kept as primary; all addresses tracked in `addresses` column.
  Survival span spans all entries.
- **5+ distinct addresses** → treated as a chain; each location
  remains a separate panel entry.

| Metric | Value |
|--------|-------|
| Addressed entries before relocation merge | 70,187 |
| Chains kept separate (5+ addresses) | 3,541 entries |
| **Relocations detected and merged** | **9,438** |
| Businesses removed by relocation merge | 11,817 |

### 3. Gap Filling

For each business, if it appears in year N and year N+2 but not year N+1,
year N+1 is treated as present (licence lapse assumption). Only 1-year gaps
are filled; 2+ year gaps are left as-is.

After gap filling, `years_active` and `total_folderyears` are recomputed.

| Metric | Value |
|--------|-------|
| **Businesses with gaps filled** | **12,913** |
| **Total gap-years filled** | **14,111** |

### 4. Cohort Tagging (has_address)

Added boolean column `has_address` — True if both `house` and `street` are
non-null. Enables restricting analysis to the commercial-address cohort without
discarding the full panel.

| Cohort | Count |
|--------|-------|
| has_address = True (commercial address) | 58,370 |
| has_address = False (home-based / null) | 43,101 |

---

## Before / After Comparison

| Metric | v1 | v2 | Change |
|--------|----|----|--------|
| Total businesses | 113,858 | 101,471 | -12,387 (10.9%) |
| Median survival (years_active) | 4.0 | 4.0 | +0.0 yr |
| Mean survival (years_active) | 5.15 | 5.61 | +0.46 yr |
| 1-year deaths FY14–24 | 9,171 | 7,514 | -1,657 |
| 1-year death rate (FY14–24 proxy) | 8.1% | 7.4% | -0.6pp |
| Multi-year businesses (2+ FY) | 96,079 (84.4%) | 86,876 (85.6%) | +1.2pp share |

---

## New Columns in v2

| Column | Type | Description |
|--------|------|-------------|
| `has_address` | bool | True if both house and street are non-null |
| `relocated` | bool | True if this business was detected as a relocation merge |
| `address_count` | int | Number of distinct addresses seen (1 = no relocation) |
| `addresses` | str | Pipe-separated list of all addresses (in chronological order) |
| `gap_filled_years` | int | Number of 1-year gaps filled for this business |

---

## Quality Check Summary

The v2 panel satisfies all expected quality checks:
- **Fewer businesses than v1**: 101,471 vs 113,858 (YES, -10.9%)
- **Longer mean survival**: 5.61 vs 5.15 yr (YES, +0.46 yr)
- **Higher P75 survival**: 8 vs 7 yr (YES, the median stays at 4.0 because it is a robust statistic resistant to the large short-lived tail; the upper half of the distribution genuinely lengthened)
- **Fewer 1-year deaths**: 7,514 vs 9,171 (YES, -1,657)

---

## Files

| File | Description |
|------|-------------|
| `data/processed/commercial-panel.csv` | Original v1 panel (unchanged) |
| `data/processed/commercial-panel-v2.csv` | Rebuilt panel with mitigations |
| `scripts/rebuild_panel_v2.py` | This rebuild script |
| `data/inventory/PANEL_V2_CHANGELOG.md` | This file |
| `analysis/SURVIVAL_TRACKING_VALIDATION.md` | Original validation report |
