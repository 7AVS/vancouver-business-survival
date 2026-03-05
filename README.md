# Does Your Neighbourhood Determine Your Business's Fate?

**Survival analysis of 97,915 Vancouver businesses (2013–2025)**

A friend on Main Street asked if his ice cream shop would survive the Broadway Subway construction. I pulled 13 years of City of Vancouver business licence data, joined it to property tax assessments, and ran the numbers.

## Key Findings

- **Median survival: 6 years.** Not a year-one cliff — a steady drain through year five.
- **Business type dominates.** Food & Beverage has 2x the closure risk. Construction & Trades is most durable.
- **Mount Pleasant is not the problem.** Once you control for business mix, it's statistically indistinguishable from Downtown.
- **Land value is a weak signal.** ~7% closure risk per doubling, but it's a residential property proxy.

## Methods

- **Kaplan-Meier** survival curves (baseline, by type, by neighbourhood, by land value tier)
- **Cox proportional hazards** regression (3 nested models, concordance = 0.62)
- **Panel construction**: 101,471 businesses → 97,915 independent (after chain detection, silent exit reclassification, gap filling)

## Data Sources

All data from [City of Vancouver Open Data Portal](https://opendata.vancouver.ca/):

- **Business Licences** (2013–2026): ~900K rows across archive + current datasets
- **Property Tax Assessments** (2006–2025): 4.25M rows
- **Census** (2006/2011/2016/2021): neighbourhood-level demographics
- **Local Area Boundaries**: 22 polygon GeoJSON

Raw data files are too large for GitHub. Download from the CoV portal and place in `data/raw/`.

## Project Structure

```
├── analysis/
│   ├── business-survival-vancouver.ipynb   # Main notebook (Steps 1-5)
│   ├── plots/                              # All generated figures
│   └── *.md                                # Step reports
├── scripts/
│   ├── step1_baseline_survival.py          # KM baseline
│   ├── step2_survival_by_type.py           # KM by macro-category
│   ├── step3_survival_by_neighbourhood.py  # KM by local area
│   ├── step4_land_value_survival.py        # Land value integration
│   └── step5_cox_regression.py             # Cox PH models
├── data/
│   ├── inventory/                          # Data documentation
│   └── processed/                          # Lookup tables & crosswalks
└── docs/                                   # Research & methodology
```

## Requirements

```
Python 3.12
pandas, numpy, matplotlib, lifelines, scipy, geopandas
```

## Author

Andre Santos — [andresantos.ca](https://andresantos.ca)
