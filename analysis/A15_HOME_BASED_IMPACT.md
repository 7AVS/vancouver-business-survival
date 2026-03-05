# A15: Home-Based Business Address Removal — Impact Assessment

**Assumption being tested:** A15 — In April 2018, the City of Vancouver retroactively removed addresses from all home-based business licences back to 1997. Because our survival tracking uses a `business_id = hash(name + house + street)` key, a business that had a home address before the wipe but none after would produce two separate panel entities: one that "dies" when the address disappears, and a second that "starts" with a blank address. This would inject false deaths into the 2017–2018 window.

**Data source:** `data/processed/business-licences-merged-2013-to-2026.csv` (914,856 rows, FY13–FY26)
**Commercial scope:** `data/processed/commercial-licences-2013-to-2026.csv` (597,903 rows)
**Panel:** `data/processed/commercial-panel.csv` (113,858 unique businesses)
**Analysis date:** 2026-03-03

---

## Table of Contents

1. [What "Homecraft" Means in the Data](#1-what-homecraft-means-in-the-data)
2. [The Critical Finding: Wipe Pre-dates Our Dataset](#2-the-critical-finding-wipe-pre-dates-our-dataset)
3. [Homecraft in the Commercial Panel](#3-homecraft-in-the-commercial-panel)
4. [The business_id Key and Why It Matters](#4-the-business_id-key-and-why-it-matters)
5. [Non-Homecraft Home-Based Businesses (The Residual Risk)](#5-non-homecraft-home-based-businesses-the-residual-risk)
6. [Quantified False Death Estimate](#6-quantified-false-death-estimate)
7. [Summary Table](#7-summary-table)
8. [Conclusion and Recommendation](#8-conclusion-and-recommendation)

---

## 1. What "Homecraft" Means in the Data

In the City of Vancouver business licence schema, home-based cottage businesses are classified as **`Homecraft *Historic*`** under the `businesstype` field. These are small enterprises operated from a residential premises: home bakers, handcraft sellers, personal-service operators, and similar micro-businesses.

**Raw data counts:**

| Metric | Value |
|--------|-------|
| Total Homecraft rows (raw, all years) | 2,251 |
| Unique licencersn | 2,251 |
| Folderyear range | FY13 to FY23 |
| businesssubtype values | None — 100% blank |
| Status breakdown: Issued | 1,540 |
| Status breakdown: Pending | 300 |
| Status breakdown: Gone Out of Business | 288 |
| Status breakdown: Cancelled | 71 |
| Status breakdown: Inactive | 52 |

**Note on `*Historic*` suffix:** This label appears on most pre-2020 businesstypes and indicates the classification originated in the legacy licensing system. It does not mean the business is no longer operating — many Homecraft licences are Issued through FY23.

---

## 2. The Critical Finding: Wipe Pre-dates Our Dataset

The April 2018 retroactive wipe removed addresses from all home-based business licences back to 1997. Our dataset starts in FY13 (2013) — five years before the wipe.

**Address null rates for Homecraft, by year:**

| Year | Total rows | house null | house null % | street null % |
|------|-----------|-----------|-------------|--------------|
| 13 | 172 | 172 | 100% | 100% |
| 14 | 170 | 170 | 100% | 100% |
| 15 | 181 | 181 | 100% | 100% |
| 16 | 191 | 191 | 100% | 100% |
| 17 | 187 | 187 | 100% | 100% |
| 18 | 191 | 191 | 100% | 100% |
| 19 | 209 | 209 | 100% | 100% |
| 20 | 215 | 215 | 100% | 100% |
| 21 | 243 | 243 | 100% | 100% |
| 22 | 252 | 252 | 100% | 100% |
| 23 | 240 | 240 | 100% | 100% |

**Interpretation:** Addresses for Homecraft are 100% null in every year from FY13 through FY23 — including FY13 (2013), which predates the April 2018 wipe by five years. This means our data was either (a) extracted after the retroactive wipe was already applied to the historical records, or (b) the City's public Open Data portal always had Homecraft addresses scrubbed before our extraction period. Either way, the wipe is already a complete, uniform, pre-existing condition in our dataset.

**Corroborating evidence — address null rate across all commercial data by year:**

| Year | Total rows | Null address % |
|------|-----------|--------------|
| 13 | 44,697 | 37.1% |
| 14 | 43,122 | 35.4% |
| 15 | 43,653 | 36.3% |
| 16 | 45,493 | 38.1% |
| 17 | 42,703 | 33.8% |
| **18** | **42,653** | **33.7%** |
| 19 | 43,401 | 34.5% |
| 20 | 40,296 | 34.2% |
| 21 | 41,498 | 34.0% |
| 22 | 42,248 | 33.2% |
| 23 | 45,106 | 33.9% |
| 24 | 42,230 | 30.8% |

There is no spike in null address rates around FY17–18. If the wipe had occurred mid-dataset, we would see a jump. The flat distribution confirms the wipe was already applied uniformly to all years when our data was extracted.

**Critical verification:** A direct check for any `licencersn` that transitions from having an address to not having an address across years in our commercial dataset returns **zero results**. Not a single business licence went from addressed to unaddressed within our data period.

---

## 3. Homecraft in the Commercial Panel

After applying scope exclusions (removing Pending and Cancelled status, as per the SCOPE_AUDIT), Homecraft contributes:

| Stage | Count |
|-------|-------|
| Homecraft rows in raw data | 2,251 |
| Homecraft rows after scope exclusions (commercial licences) | 1,880 |
| Homecraft unique businesses in commercial panel | 366 |
| Homecraft with any address in panel | 0 (0%) |
| Homecraft with geo_point_2d in panel | 0 (0%) |

The 366 Homecraft businesses in the panel are tracked by **name only** — their `business_id` is `hash(businessname_norm + "||")` (house and street normalised to empty string). This is stable across all years.

**Panel characteristics:**

| Metric | Value |
|--------|-------|
| Businesses with total_folderyears ≥ 2 | 296 (80.9%) |
| Businesses with total_folderyears = 1 | 70 (19.1%) |
| Maximum folderyears observed | 11 |
| status_last_year = Issued | 89 (24.3%) |
| status_last_year = Gone Out of Business | 265 (72.4%) |
| status_last_year = Inactive | 12 (3.3%) |

The 265 "Gone Out of Business" represents organic commercial failure — not A15 artefact. These are legitimate closures, spread across all years (last_year runs from 13 to 23).

**Implication for survival analysis:** Homecraft businesses can be tracked consistently in the KM and Cox models. Their business_id is stable because the empty-address key was always their key. No continuity break exists. The 266 eventual deaths are real signal, not A15 noise.

---

## 4. The business_id Key and Why It Matters

The pipeline constructs identity as:

```python
key = f"{businessname_norm}|{house_norm}|{street_norm}"
business_id = hashlib.md5(key.encode()).hexdigest()[:12]
```

where `house_norm` and `street_norm` default to `""` when null.

For Homecraft (always null address):
```
business_id = hash("name||")    # stable for all years
```

For a business that had an address and then lost it:
```
year 13-17: business_id = hash("name|123|MAIN ST")
year 18+:   business_id = hash("name||")           ← different!
```

The second case would create a false death (the addressed entity "dies" at year 17) and a false birth (the unaddressed entity "starts" at year 18).

**Result from the data:** This second case does not occur in our dataset. As shown above, zero `licencersn` values transition from addressed to unaddressed. The wipe was applied before our extraction, so our data only ever contains the post-wipe state.

---

## 5. Non-Homecraft Home-Based Businesses (The Residual Risk)

The April 2018 policy change applied to all home-based businesses, not just those classified as `Homecraft *Historic*`. Businesses in categories such as `Office *Historic*`, `Health Services *Historic*`, `Computer Services *Historic*`, and others could operate from home without being labelled "Homecraft." These businesses would also have had their addresses wiped.

**However:** The same conclusion applies. Since our data extract reflects the post-wipe state uniformly, any business that operated from home and had its address wiped shows null addresses across all years. The transition from address → no address is not observable in our data because it happened before our first data point.

**The indirect risk:** A subtler concern is whether the same physical business appears in our panel under two different `business_id` values — once with an address (from some data source before the wipe) and once without. To test this, I searched for panel entities sharing the same business name but differing in address presence.

**Results:**

| Pattern | Count |
|---------|-------|
| Panel business names appearing 2+ times | 11,678 |
| Names appearing both WITH and WITHOUT address | 2,816 unique names (4,639 pair rows) |

Of these 2,816 split-name cases, the vast majority are explained by legitimate reasons:
- Same person's name appearing as different entities at different times or addresses
- Same franchise or chain name across multiple locations
- Business moving to a new address (new record) while the old record stays in the data
- Names with no address from FY13 (pre-wipe era, definitively not A15)

To isolate genuine A15 candidates, I applied strict criteria:
1. The addressed version last appears in FY16, FY17, or FY18
2. The unaddressed version first appears in FY17, FY18, or FY19
3. The transition is sequential (unaddressed starts after or when addressed ends — not overlapping)
4. The addressed version has status `Gone Out of Business` or `Inactive` at the transition

**A15 candidate businesstypes (no-address versions):**

| businesstype | Count |
|-------------|-------|
| Office *Historic* | 24 |
| Contractor *Historic* | 9 |
| General Contractor | 7 |
| Computer Services *Historic* | 7 |
| Architectural and Engineering Services | 6 |
| Business Support Services | 5 |
| Retail Dealer *Historic* | 4 |
| Production Company *Historic* | 4 |
| Other | 34 |

**Note on contractors:** Most `Contractor *Historic*` and similar types show 85–99% null address rates in the panel. This is because contractors routinely have no fixed business address (they operate from vehicles and client sites). Their null addresses are structural, not from A15. The A15 candidates identified above represent the subset where a contractor previously had a home address on file that was wiped.

---

## 6. Quantified False Death Estimate

| Scenario | Estimated False Deaths | % of Panel | % of All Deaths | % of YR17+18 Deaths |
|----------|----------------------|-----------|----------------|---------------------|
| **Strict** (sequential, FY17–18 break) | **~69** | **0.06%** | **0.15%** | **1.2%** |
| **Upper bound** (sequential, FY16–18 break) | **~87** | **0.08%** | **0.19%** | **1.5%** |
| Homecraft specifically | **0** | 0% | 0% | 0% |

**Reference totals:**

| Metric | Value |
|--------|-------|
| Total commercial panel businesses | 113,858 |
| Total Gone Out of Business | 45,583 |
| Deaths with last_year = 17 | 2,858 |
| Deaths with last_year = 18 | 2,950 |
| Combined year 17+18 deaths | 5,808 |

**Interpretation of the upper bound:**

The ~87 upper-bound figure is itself conservative in what it counts — these are split-name pairs with the right temporal structure AND a dead addressed version. But many of these likely have legitimate explanations (business moved, name coincidence between two individuals, businesstype change triggering re-registration). The true A15 false deaths are likely toward the lower end of this range or below it.

Even taking the full upper bound of 87 as real: this represents **0.19% of all deaths** and **0.08% of the panel**. It does not materially affect survival curves, KM estimates, or hazard ratios at any commercially meaningful scale.

---

## 7. Summary Table

| Question | Finding |
|----------|---------|
| What is "Homecraft"? | businesstype = `Homecraft *Historic*` — cottage businesses licensed under home-based rules |
| How many Homecraft rows in raw data? | 2,251 (unique licencersn: 2,251) |
| How many Homecraft in commercial panel? | 366 unique businesses |
| Do Homecraft businesses have any addresses? | No — 100% null addresses in all years (FY13–FY23) |
| Does the April 2018 wipe affect our data? | No — wipe was retroactive and pre-dates our entire dataset. All years in our data are already post-wipe. |
| Is there any address→null transition observable in our data? | No — zero licencersn show this transition. Confirmed by direct check. |
| Is there a null-address spike in FY18? | No — address null rates are flat at 33–38% throughout FY13–FY26 |
| Are Homecraft businesses tracked consistently in the panel? | Yes — business_id is stable (name-only key) throughout all years |
| False deaths for Homecraft from A15? | **Zero** |
| Non-Homecraft A15 false deaths (all types combined)? | **~69 (strict) to ~87 (upper bound)** |
| As % of total panel? | <0.08% |
| As % of all deaths? | <0.19% |
| Does this materially bias survival curves? | No — negligible at this magnitude |
| Bigger concern than A15 for spatial analysis? | Yes — 38.2% of panel businesses (43,498) have no address and cannot be geocoded |

---

## 8. Conclusion and Recommendation

### Conclusion

**A15 is a non-issue for the commercial panel as currently constructed.**

The concern was valid in principle — a retroactive address wipe could inject false deaths if our data spans the wipe event. But the empirical evidence is unambiguous: the City's retroactive wipe was complete before our dataset begins. Every year of our data (FY13–FY26) reflects the post-wipe state. No business in our commercial dataset ever transitioned from having an address to not having one.

For **Homecraft specifically**, there are zero false deaths. Homecraft has always been tracked by name-only in our data, the business_id key is stable, and the 265 Homecraft deaths recorded as "Gone Out of Business" represent genuine organic closures.

For **non-Homecraft home-based businesses**, the estimated false deaths from A15-style address splitting are **~69 to 87 businesses** — representing 0.06–0.08% of the commercial panel and 0.15–0.19% of all deaths. This is below the noise floor for KM or Cox estimates.

### Recommendation

**No mitigation required.** The assumption can be closed as a non-issue for this dataset.

**Optional sensitivity check (low priority):** If publishing, a footnote can acknowledge that the City of Vancouver retroactively removed home-based business addresses in April 2018, and that empirical testing found no observable address-to-null transitions in the FY2013–2026 extract, confirming the wipe is a uniform pre-existing condition rather than an event within the study window.

**Larger concern to address:** The 38.2% of panel businesses (43,498) with no address whatsoever — and the 41.7% with no geo_point_2d — represent the real limitation for spatial analysis. This is not A15-related; it is structural (contractors, mobile services, certain professional categories genuinely lack fixed addresses). Neighbourhood assignment for these businesses will require either geocoding via postal code centroids or exclusion from the spatial component of the Cox model, with careful documentation of the resulting population bias.

---

*Analysis produced: 2026-03-03*
*Data: City of Vancouver Open Data — Business Licences FY2013–FY2026 (merged)*
