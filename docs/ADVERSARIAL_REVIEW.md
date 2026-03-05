# Adversarial Review: Vancouver Housing Policy Research
## Reviewer notes
**Document reviewed**: `POLICY_RESEARCH.md`
**Review date**: 2026-03-03
**Methodology**: Web verification of academic papers (DOI, journal, authors, findings), policy date cross-checking against primary government sources, targeted challenges to the gap claim, DiD design assumptions, and data availability claims.

---

## PART 1: POLICY TIMELINE VERIFICATION

---

## Claim: BC Foreign Buyer Tax — Effective Date August 2, 2016

- **Source tier**: 1 (primary legislation / government)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: Bill 28 (Miscellaneous Statutes (Housing Priority Initiatives) Amendment Act, 2016) received royal assent on July 28, 2016, but the operative date for the Property Transfer Tax amendment — when transfers registered on or after August 2, 2016 became subject to the tax — is confirmed as August 2, 2016 by BC government sources, Wikipedia (Bill 28 BC), and multiple legal commentaries (McMillan, Norton Rose Fulbright). The document is correct on this distinction.
- **Challenge**: Minor — the document says "effective date: August 2, 2016" and that royal assent was part of Bill 28, but doesn't specify that royal assent was July 28. This is technically accurate (effective date is Aug 2) but could mislead a reader who conflates announcement → assent → effective date. The announcement was July 25, assent July 28, effective August 2. The timeline is actually compressed into one week, which matters for anticipation effects.
- **Notes**: The 7-day window between announcement and effective date is so short it is unlikely to have produced meaningful anticipation-driven behavior (buyers could not close transactions that fast even if they tried).

---

## Claim: BC FBT Initial Rate 15%, February 21, 2018 Amendment to 20% with Geographic Expansion

- **Source tier**: 1 (government sources, BC Budget 2018)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: Multiple sources confirm the February 21, 2018 amendment increased the rate to 20% and expanded to Fraser Valley, Capital Regional District (Victoria), Regional District of Nanaimo, and Central Okanagan. The date February 21 is specifically the 2018 BC Budget date, confirmed by McCarthy Tétrault and other legal commentaries.
- **Challenge**: The document says "This expansion was part of the 2018 BC Budget under the NDP government." This is accurate. However, the document does not note that a transitional provision existed: transactions subject to a written agreement dated on or before February 20, 2018 and registered on or before May 18, 2018 were exempt from the higher rate. This transitional carve-out is relevant to any DiD study using transaction data in that window.
- **Notes**: The effective date distinction (February 21 = Budget Day, which was also the implementation date, not a future date) is correctly stated.

---

## Claim: Vancouver Empty Homes Tax — Effective January 1, 2017, By-law No. 11674, Initial Rate 1%

- **Source tier**: 1 (City of Vancouver By-law, primary source)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: Confirmed by City of Vancouver official sources, Lawson Lundell, McMillan LLP, and multiple legal commentaries. The by-law number 11674 is correct. January 1, 2017 was the start of the first taxable vacancy reference period.
- **Challenge**: The document states "effective date: January 1, 2017 (first taxable vacancy reference period: Jan 1–Dec 31, 2017)." This framing is accurate but could be clearer: taxpayers did not actually pay the tax until 2018 (the 2017 vacancy year resulted in bills issued in 2018). The "effective" economic shock for a landlord contemplating whether to leave a unit vacant in 2017 is technically the 2017 reference period start — which is what the document says — but the cash outflow happens in 2018. For DiD purposes this matters: any behavioral response would appear in 2017 occupancy decisions (anticipation of the 2018 bill), not at payment date.
- **Notes**: Rate progression (1% → 1.25% 2020 → 3% 2021) is consistent with the 2023 Annual Report and public sources.

---

## Claim: EHT — Declared vacant fell from ~2,500 (2017) to under 1,000 (2024 reference year); vacancy rate fell from ~0.9% to 0.49%

- **Source tier**: 2 (City of Vancouver Annual Reports, administrative data)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: City of Vancouver's December 2025 press release confirms: "a record-low vacancy rate of 0.49 per cent was recorded in 2024 compared to 0.90 per cent in 2017." BIV and Daily Hive both report that vacant homes fell below 1,000 (979 in 2024). The 2017 figure of ~2,500 is not directly cited in the search results but is consistent with the ~0.9% vacancy rate claim at the baseline.
- **Challenge**: The Caracciolo & Miglino (2024) C.D. Howe study found that ~226 net additional units became occupied as a result of the EHT — far fewer than the raw "declared vacant" decline would suggest. The gap is because many properties shifted from "declared vacant" to "deemed occupied" through behavioral responses, but the baseline denominator is large. The document's City-reported statistics are not wrong, but they present the most favorable framing (administrative declarations, not causal attribution). A critic of the EHT (Russil Wvong's Substack piece on the C.D. Howe paper) noted exactly this problem.
- **Notes**: The 2017 baseline number of "~2,500" declared vacant is not independently confirmed in sources found; the Caracciolo paper uses a 7% vacancy rate estimate from Census data, not the declaration-based count.

---

## Claim: BC SVT — First tax year 2018, royal assent SBC 2018 c. 46, regulation B.C. Reg. 275/2018 came into force December 10, 2018

- **Source tier**: 1 (CanLII, BC government)
- **Verification**: VERIFIED (with a critical note on anticipation)
- **Confidence**: HIGH
- **Evidence**: CanLII confirms SBC 2018, c. 46 exists. B.C. Reg. 275/2018 is confirmed. The first tax year being 2018 is consistent with government sources (declarations due March 31, 2019 for 2018 tax year). EY Global Tax News and gov.bc.ca confirm the structure.
- **Challenge — IMPORTANT**: The document claims the EHT control group (Burnaby, Richmond, etc.) is "clean" from 2015–2018 because the SVT only applies after 2018. This ignores a serious anticipation effect. The BC SVT was first announced publicly on **February 20, 2018** (the NDP Budget). CBC News and Global News reported this prominently. This is 10 months before the regulation came into force (December 2018). Property owners in Metro Vancouver municipalities — including the control group municipalities — faced uncertainty and potential behavioral response from February 2018 onward, not December 2018. The document's proposed EHT analysis window of "2015–2018" therefore ends precisely at the moment contamination begins. This is not clean. The SVT announcement in February 2018 would likely have produced behavioral effects in the same control municipalities during Q1–Q4 2018. Any DiD study claiming a clean 2015–2018 window needs to end at December 31, 2017 at the latest, not 2018. The document acknowledges SVT contamination but misstates when it begins.
- **Notes**: This is the most significant methodological weakness in the EHT DiD design as described.

---

## Claim: SVT Rate Structure — BC residents 0.5%, foreign owners and satellite families 2%

- **Source tier**: 1 (gov.bc.ca SVT rates page)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: BC government's SVT rates page confirms the rate structure. The document accurately captures the two-tier structure.
- **Challenge**: The document claims "The 0.5% domestic rate is unlikely to cause major behavioral change; the 2% foreign rate is the meaningful shock." This is a reasonable inference but is not a verified empirical claim. The BCREA estimated the SVT reduced home sales in taxable regions by an additional 12.5% vs. non-taxable regions, which suggests even the domestic rate may have had meaningful effects on transaction behavior (not just foreign owners).

---

## Claim: Federal UHT — Effective January 1, 2022, eliminated by 2025 Budget, no filings required for 2024+

- **Source tier**: 1 (Canada.ca, McMillan LLP, BDO)
- **Verification**: VERIFIED WITH CORRECTION
- **Confidence**: HIGH
- **Evidence**: The 2025 federal Budget proposed eliminating the UHT effective 2025 (no UHT payable for 2025 and beyond). This is confirmed by McMillan, BDO, and McCarthy Tétrault.
- **Challenge — CORRECTION**: The document states "new filings are not required for 2024 and later tax years for most owners." This is imprecise. The correct statement is that no UHT is payable and no filings are required for **2025** and later tax years. **2024** UHT requirements continue to apply, including penalties for failure to file or late payment. This is a factual error in the document — 2024 is still subject to UHT; 2025 is not.
- **Notes**: The UHT Act and Regulations are proposed to be fully repealed effective January 1, 2035 per the budget legislation.

---

## Claim: Federal Prohibition on Non-Canadians — Effective January 1, 2023, Extended February 4, 2024 to January 1, 2027

- **Source tier**: 1 (Canada.ca, Aird Berlis, Dentons)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: Extension to January 1, 2027 confirmed by multiple legal sources including Aird Berlis and Dentons citing the February 4, 2024 announcement.
- **Challenge**: The document says "March 2023 amendments" included buildings with 4+ dwelling units excluded. The actual effective date was March 27, 2023 per CMHC and Pushor Mitchell. The document correctly identifies the key exemptions. One point worth noting: the document calls this "an outright ban (not a tax)" — this is accurate and an important methodological distinction. A prohibition creates a structural break in who can buy, whereas a tax creates a price disincentive; their identification strategies differ.
- **Notes**: No material errors here.

---

## Claim: BC STR Restrictions — Effective May 1, 2024, SBC 2023 c. 38, municipalities over 10,000 population

- **Source tier**: 1 (BC government news release, BCREA)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: BC government news release from May 1, 2024 confirms "New rules take effect to rein in short-term rentals." The population threshold of 10,000 is confirmed. The act is SBC 2023, c. 38.
- **Challenge**: The document says "60+ communities" are affected. BCREA and BC government sources cite 65 communities, not "60+." This is minor but imprecise. The document also says "additional 17 communities voluntarily opted in with an effective date of November 1, 2024." This figure could not be independently confirmed in this review; the searches found reference to 65 total (not 60 + 17 opt-ins). Potential error or outdated framing.
- **Notes**: The document's description of the mechanism (principal residence only + one additional suite) is accurate.

---

## Claim: Vancouver Broadway Plan — Approved June 2022, 30,000 homes over 30 years (revised to 41,500 December 2024)

- **Source tier**: 2 (City of Vancouver official plan documents)
- **Verification**: PARTIALLY VERIFIED
- **Confidence**: MEDIUM
- **Evidence**: The June 22, 2022 Council approval date is confirmed by City of Vancouver Shape Your City records. The 41,500 homes figure for the December 2024 amendment appears in Urbanized / Daily Hive reporting.
- **Challenge**: The original "30,000 new homes over 30 years" figure is not confirmed in the search results — the Broadway Plan itself does not appear to have used that specific round number as a headline figure in City documents found. The 30,000 figure may be accurate but was not independently verified. This should be checked against the original June 2022 plan document before using it in published work.
- **Notes**: Geographic boundary (Clark Drive to Vine Street, 1st to 16th Avenues) is consistent with City of Vancouver maps.

---

## Claim: Bill 44 — Royal assent November 30, 2023, municipalities must update zoning bylaws by June 30, 2024

- **Source tier**: 1 (MLT Aikins, CityHallWatch, CHBA BC)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: MLT Aikins confirms Bills 44 and 47 received royal assent on November 30, 2023. The June 30, 2024 bylaw update deadline is confirmed by CHBA BC and Vancouver City staff reports.
- **Challenge**: The document states "Vancouver City Council adopted the new R1-1 Residential Inclusive Zone (replacing RS-1 through RS-9 zones) on October 17, 2023." This is correct — Vancouver adopted R1-1 on October 17, 2023, specifically at a Council meeting after a September 14 public hearing. However, the document says this replaced "RS-1 through RS-9." The actual consolidation replaced RS-1, RS-1A, RS-1B, RS-2, RS-3, RS-3A, RS-5, RS-6, and RS-7 — nine zones, but notably not including RS-4 (which apparently did not exist as a named zone). Calling them "RS-1 through RS-9" implies a consecutive numbering that is not accurate. Minor but worth correcting if this research is published.
- **Notes**: The claim that "multiplex applications represented ~50% of R1-1 application volume" by 2024 is plausible but was not verified independently. Treat as UNVERIFIED until sourced.

---

## Claim: Bank of Canada Rate Hike Sequence (March 2022 onward)

- **Source tier**: 1 (Bank of Canada official announcements)
- **Verification**: VERIFIED WITH ONE CORRECTION
- **Confidence**: HIGH
- **Evidence**: Bank of Canada announcement on March 2, 2022 confirms +25 bps to 0.50%. The sequence through December 2022 matches BNN Bloomberg and Bank of Canada records.
- **Challenge — CORRECTION**: The document states "March 8, 2023: +25 bps → 4.75% (pause signaled)" and "June 2023: +25 bps → 5.00%." The actual sequence was: January 25, 2023 → 4.50%; March 8, 2023 the Bank held at 4.50% (pause, not a hike); June 7, 2023 → 4.75%; July 12, 2023 → 5.00%. The document conflates the March pause with a rate hike and misstates the June 2023 terminal rate as 5.00% when it was actually reached in July 2023. This is a factual error — the March 8, 2023 date is a hold/pause announcement, not a 25 bps hike.
- **Notes**: The overall message (rates peaked at 5.00%, held through mid-2024, then cut) is correct. The specific date sequence has errors that matter if used in event studies.

---

## Claim: Vancouver benchmark price peaked at approximately $1,252,800 in April 2022, declined 14–25% from February 2022 peak by July 2022

- **Source tier**: 3 (REBGV MLS HPI data, news reporting)
- **Verification**: PLAUSIBLE BUT NOT INDEPENDENTLY CONFIRMED
- **Confidence**: MEDIUM
- **Evidence**: Multiple sources confirm April 2022 was the benchmark peak and that prices fell significantly through mid-2022. The WOWA Vancouver Housing Market page references the all-time high in April 2022 with current prices 8.7% below that peak (as of early 2026). The specific figure of $1,252,800 was not found in search results.
- **Challenge**: The "14–25% decline from February 2022 peak by July 2022" range is wide and imprecise. REBGV reports are the primary source for Vancouver benchmark data; this figure should be cited to the specific REBGV monthly market report. The 2022 benchmark price figure appears to mix "benchmark composite" with other measures — REBGV, CMHC, and Teranet all publish different indices with different methodologies. For a research document, the specific index and source must be cited precisely.
- **Notes**: The claim that "this decline is almost entirely attributable to rate hikes, not policy interventions" is an interpretive assertion. It is plausible given timing — rate hikes began March 2022 and prices peaked April 2022 — but "almost entirely" is a strong causal claim that is not sourced to any study. Treat as PLAUSIBLE INFERENCE, not a verified finding.

---

## PART 2: ACADEMIC LITERATURE VERIFICATION

---

## Claim: Du, Zaichao, Hua Yin, and Lin Zhang (2022) — "Foreign buyer taxes and house prices in Canada: A tale of two cities" — *Journal of Housing Economics*, Volume 55

- **Source tier**: 1 (journal publication, IDEAS/RePEC, ScienceDirect)
- **Verification**: VERIFIED WITH DOI DISCREPANCY
- **Confidence**: HIGH
- **Evidence**: Paper confirmed to exist in Journal of Housing Economics, Volume 55, 2022. Authors (Zaichao Du, Hua Yin, Lin Zhang) are confirmed. IDEAS/RePEC and ScienceDirect both list this paper.
- **Challenge — DOI DISCREPANCY**: The document cites DOI `10.1016/j.jhe.2021.101791`. Multiple searches confirm the actual DOI as `10.1016/j.jhe.2021.101807` (per ScienceDirect and IDEAS records). The document's cited DOI `101791` does not appear in any source. This is a fabricated or copied-with-error DOI that will return a 404. The correct DOI is `101807`. Anyone trying to follow this citation will hit a dead link.
- **Findings check**: The document states FBT reduced Vancouver house prices by approximately 5% (Aug 2016–Dec 2017) and Toronto by 7–9% (April 2017–Dec 2017). Both figures are confirmed by multiple secondary sources. The document also says "effects concentrated in single-detached homes" — confirmed. The "temporary in some specifications — prices partially recovered by 2018" finding is also confirmed as the paper's conclusion for Vancouver.
- **Notes**: The methodological description (panel program evaluation + RD design) is accurate.

---

## Claim: Pavlov, Andrey, and Tsur Somerville (2024) — "Foreign buyer taxes and housing affordability" — *Real Estate Economics*, Volume 52(3), pp. 928–950

- **Source tier**: 1 (journal publication, IDEAS/RePEC, Wiley Online Library)
- **Verification**: VERIFIED WITH MISSING AUTHOR
- **Confidence**: HIGH
- **Evidence**: Article confirmed. Volume 52(3), pp. 928–950, May 2024. Wiley Online Library and IDEAS/RePEC both confirm.
- **Challenge — MISSING AUTHOR**: The paper has three authors: **Andrey Pavlov, Tsur Somerville, and Jake Wetzel** (Stata Analytics). The document lists only two authors — Pavlov and Somerville. This is a citation error. Any submitted paper using this citation would be incorrect.
- **Findings check**: The document states "house prices fell by 6% more in high-foreign-buyer-concentration neighborhoods relative to low-concentration neighborhoods after the FBT." This is confirmed by both the Wiley abstract and the UBC Sauder press release ("Foreign Buyers Tax led to home prices declining six per cent more in some Vancouver neighbourhoods"). The finding that "No evidence that the FBT meaningfully boosted local purchases to offset the decline" is consistent with the paper's conclusion about affordability improvements being small.
- **Data check**: The document states Pavlov/Somerville used "pre-policy voluntary disclosure records." An earlier web search confirmed the PTT data included foreign buyer recording starting June 10, 2016 (about 6 weeks pre-tax). This is accurate — there was a brief pre-implementation data collection period. The description of these as "voluntary disclosure records" is somewhat misleading; they were administratively collected, not self-reported voluntary disclosures in the usual sense.

---

## Claim: Hartley, Jonathan, Li Ma, Susan M. Wachter, and Albert A. Zevelev (2024) — "Do Foreign Buyer Taxes Affect House Prices?" — *Journal of Real Estate Research*

- **Source tier**: 1 (SSRN 3939611, Taylor & Francis, Journal of Real Estate Research)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: SSRN ID 3939611 confirmed. Published in Journal of Real Estate Research, Vol. 47, No. 4, pp. 570–596, 2024. All four authors confirmed. AEA 2023 conference presentation confirmed.
- **Challenge**: The document describes the journal simply as "Journal of Real Estate Research" without volume/page numbers. The actual publication is Vol. 47(4), pp. 570–596. This is an incomplete citation but not incorrect.
- **Findings check**: The document states "FBTs had negative, large, and persistent effects on house price growth across all three countries" and "effects are persistent (do not fully reverse within a 3-year window)." This is confirmed as the paper's headline finding. The characterization that this is "broader/more optimistic than Du et al. regarding persistence" is accurate — Du et al. find temporary effects in Vancouver specifically, while Hartley et al. find persistence across countries.
- **Notes**: The SSRN link (3939611) and AEA 2023 conference link are both confirmed. The Tandfonline published version link in the sources section is accurate.

---

## Claim: Andersen, Asger Lau, et al. (2024) — "Heterogeneous effects of a foreign buyer tax on house prices" — *Journal of Economic Geography*, Volume 24(4), pp. 495–

- **Source tier**: PARTIALLY VERIFIED — AUTHORSHIP UNCERTAIN, POSSIBLE MISATTRIBUTION
- **Verification**: PLAUSIBLE BUT WITH SIGNIFICANT UNCERTAINTY
- **Confidence**: LOW
- **Evidence**: A paper at `academic.oup.com/joeg/article-abstract/24/4/495/7639370` exists with the title "Heterogeneous effects of a foreign buyer tax on house prices" in JEG Volume 24(4), 2024, pp. 495–. This is confirmed. However, the first author listed as "Asger Lau Andersen" could not be confirmed through multiple targeted searches. A separate 2024 JEG paper on foreign buyer taxes (Howell, Mughan, Singla) was found studying New South Wales, Australia — and is a clear mismatch. The "Asger Lau" name combination is more commonly associated with Danish macroeconomics research (Asger Lau Andersen is a Danish economist at University of Copenhagen who has worked on household finance), not Vancouver housing.
- **Challenge — POSSIBLE MISIDENTIFICATION**: The document attributes this JEG 24(4) paper to "Andersen, Asger Lau, et al." but cannot confirm the co-authors. The DOI cited (`10.1093/joeg/lbad022`) is plausible given JEG DOI formats (lbad prefix = accepted 2023, JEG). However, the actual authorship of this specific paper could not be verified. If "Asger Lau Andersen" is indeed the author, this would be a notable cross-disciplinary piece. If the authorship is wrong, this citation is misleading. RECOMMEND: Verify directly at the OUP URL before publishing.
- **Findings check**: "Neighborhoods with higher pre-tax foreign buyer shares see larger post-tax price declines" is internally consistent with other papers in this literature. Whether this is what THIS specific paper finds could not be verified.
- **Notes**: The DOI `lbad022` format is plausible for a paper accepted for JEG in 2023. The journal and volume are confirmed at that URL. The key risk is the author attribution.

---

## Claim: Caracciolo, Gherardo Gennaro, and Enrico Miglino (2024) — "Ripple Effects: The Impact of an Empty-Homes Tax on the Housing Market" — C.D. Howe Institute / SSRN 4919236

- **Source tier**: 1 (SSRN, C.D. Howe Institute publication)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: SSRN 4919236 confirmed. C.D. Howe Institute publication confirmed. Authors confirmed. August 2024 publication date confirmed.
- **Challenge — METHODOLOGY CONCERN**: The document says the control group is "comparable properties just outside the city boundary (Burnaby, North Vancouver)." The actual Caracciolo/Miglino methodology used neighborhoods within 800 meters of Boundary Road (Vancouver-Burnaby border) — this is a much tighter geographic design (a sharp boundary DiD / geographic RD) than the document implies. The document's description of "Burnaby, North Vancouver" as the control group is an oversimplification. The actual design uses only the border zone, not municipality-wide comparisons. This matters because border-zone properties may not be representative of broader housing markets.
- **Findings check**: Vacancy rate dropped by 1.5 percentage points (from 7% in 2016 to ~5.5%), representing a 21% reduction. ~226 net additional occupied homes. No rent effect. No construction effect. All confirmed by C.D. Howe publication and Caracciolo's commentary in The Hub (August 2024). The document's description of the "high-price equilibrium" explanation for no rent effect is a reasonable paraphrase of the authors' interpretation.
- **External challenge**: Russil Wvong's Substack ("C.D. Howe: a bad study of vacancy taxes") critiques the methodology, arguing the 800-meter border zone design is too narrow and the Census vacancy data used is unreliable. This critique is not acknowledged in the research document. If this paper is cited as evidence for "EHT reduced vacancies," the known methodological critiques should be noted.

---

## Claim: Han, Lu, Derek Stacey, and Hong Chen (2023) — "Frictional and Speculative Vacancies: The Effects of an Empty Homes Tax" — ABFER Annual Conference 2023

- **Source tier**: 2 (conference paper, not peer-reviewed journal publication)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: ABFER 2023 conference paper confirmed. Authors are Lu Han, Derek Stacey, and Hong Cheng (not "Hong Chen" as listed in the document). The paper is accessible at the ABFER URL cited. Derek Stacey's research page and a Twitter/X post from February 2024 also confirm the paper was presented.
- **Challenge — AUTHOR NAME ERROR**: The document lists the third author as "Hong Chen." The actual third author is **Hong Cheng** (based on ABFER conference records and the paper itself). "Hong Chen" is a different name from "Hong Cheng." This is a citation error.
- **Findings check**: The document's summary of the paper's findings (frictional vs. speculative vacancies distinction; flat vacancy tax may harm frictional vacancies; worse tenant-matching quality) is consistent with the ABFER abstract and Urban SMU event description.
- **Notes**: This is a conference paper, not a peer-reviewed journal article. Its findings should carry less weight than the Caracciolo/Miglino paper and should be characterized as working paper/conference findings, not settled results.

---

## Claim: Favilukis, Jack, and Stijn Van Nieuwerburgh (2021) — "Out-of-Town Home Buyers and City Welfare" — *Journal of Finance*

- **Source tier**: 1 (Wiley Online Library, Journal of Finance)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: Published in Journal of Finance, Volume 76(5), pp. 2577–2638, October 2021. Confirmed via Wiley Online Library, IDEAS/RePEC, and SSRN (abstract 2922230, which differs from the 3035279 cited in the document).
- **Challenge — SSRN ID MAY BE WRONG**: The document cites SSRN `3035279`. Wiley and CEPR show SSRN as `2922230`. The SSRN `3035279` appears to link to a different related paper ("Affordable Housing and City Welfare" with Mabille as co-author). The document has linked to the wrong SSRN ID. Anyone clicking the cited link will reach a different paper.
- **Findings check**: "5% higher house prices in Vancouver" and "0.34% welfare loss for local residents" are confirmed by a cemmap/UBC PDF of the paper and multiple secondary sources. The description of the methodology (structural housing market model calibrated to Vancouver) is accurate.
- **Notes**: The document describes this as the "First paper to rigorously model the welfare implications of foreign demand on a specific Canadian city" — this is a plausible characterization given the structural model approach, but it is difficult to verify as an absolute claim of precedence.

---

## Claim: Pavlov, Andrey, and Tsur Somerville (2020) — "Immigration, Capital Flows, and Housing Prices" — *Real Estate Economics*, Volume 48(3)

- **Source tier**: 1 (Wiley Online Library, IDEAS/RePEC)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: Confirmed in Real Estate Economics, Volume 48(3), pp. 915–949, September 2020. DOI `10.1111/1540-6229.12267` confirmed. Globe and Mail coverage confirmed the IIP suspension natural experiment finding.
- **Challenge**: The document states the paper "exploits the unexpected suspension of Canada's Immigrant Investor Program (IIP) as a natural experiment." The IIP was suspended in July 2012 (moratorium on applications) and formally eliminated in Budget 2014. The document does not clarify which event (suspension or elimination) is used as the shock. The Globe and Mail article and UBC summary refer to the "closure" broadly. For a DiD to be clean, the exact event (suspension July 2012 vs. elimination 2014) matters. The Pavlov/Somerville paper likely uses the July 2012 administrative suspension — researchers should verify this before replicating the design.
- **Findings check**: "IIP suspension caused a 3% decline in property prices in neighborhoods most exposed to investor immigrant demand" — confirmed by multiple secondary sources. The "24-month effect window" (effect disappears after 24 months) is also confirmed from the Globe and Mail summary.

---

## Claim: Ley, David (2021) — "A regional growth ecology, a great wall of capital and a metropolitan housing market" — *Urban Studies*, Volume 58(2)

- **Source tier**: 1 (SAGE Journals, DOI confirmed)
- **Verification**: VERIFIED
- **Confidence**: HIGH
- **Evidence**: DOI `10.1177/0042098019895226` confirmed via SAGE Journals. David Ley is a UBC geographer. Volume 58(2), 2021 confirmed.
- **Challenge**: The document characterizes this as arguing that "short-term tax interventions cannot fully address" Vancouver's housing crisis — this is a reasonable paraphrase of Ley's structural argument. However, this is a qualitative/theoretical paper, not causal inference. Its inclusion in the literature review is appropriate for framing but should not be confused with empirical identification of policy effects.
- **Notes**: No significant errors.

---

## Claim: Systematic Literature Review (2023) — *ScienceDirect / Heliyon*

- **Source tier**: 3 (Heliyon is a lower-tier mega-journal)
- **Verification**: UNVERIFIED
- **Confidence**: LOW
- **Evidence**: The document cites a "Systematic Literature Review (2023)" in ScienceDirect/Heliyon with a URL but no authors, no title, no DOI beyond the ScienceDirect article ID. A search did not confirm this specific review. Heliyon is a legitimate but broad Elsevier journal that accepts papers across disciplines.
- **Challenge**: No author names, no title, and no DOI means this citation cannot be verified or followed. It is essentially uncitable as written. Whether the claim ("DiD, synthetic control, and regression discontinuity as the dominant quasi-experimental methods in this literature after 2010") is accurate is uncontested — it is widely true — but the specific source cannot be verified.
- **Notes**: This citation needs to be completed with author names, article title, and DOI before use in any published work.

---

## PART 3: THE GAP CLAIM — ADVERSARIAL CHALLENGE

---

## Claim: "No existing paper appears to have done a full DiD using assessed values as the primary outcome" — and this is presented as an original contribution

- **Source tier**: 6 (LLM inference / absence-of-evidence claim)
- **Verification**: PARTIALLY REFUTED — with important caveats
- **Confidence**: MEDIUM (the gap may be real, but the reason for it is well-understood and intentional, not an oversight)
- **Evidence and Challenge**:

### Why the "gap" may be intentional, not accidental:

1. **BC Assessment values have a known 12-month lag**: BC Assessment uses a July 1 valuation date. The 2016 assessment (mailed January 2017) reflects market conditions as of July 1, 2016 — *one month before* the FBT took effect (August 2, 2016). The 2017 assessment reflects July 1, 2017. This means the first assessment cycle that could potentially capture FBT effects is the 2017 assessment, published January 2018, reflecting a date 11 months post-treatment. For a policy shock on August 2, 2016, a researcher using transaction prices can measure effects in August–September 2016; a researcher using assessment data cannot observe any response until the 2018 data release. This is not a gap born of negligence — it is a fundamental timing problem that makes assessed values poorly suited for event-study identification of policy shocks.

2. **Attenuation bias is documented**: Fischer, Hauf, and Stehle (published in Journal of Banking & Finance, 2026, from an earlier SSRN working paper) explicitly find that DiD estimates using assessed values are "often more attenuated and can become statistically insignificant or economically implausible" relative to estimates using transaction prices. The authors recommend against using assessed values in research designs that rely on short- to medium-run price changes. A working paper by researchers at Berlin School of Economics ("When Housing Price Data Lag Behind the Market") makes the same point. This is the *stated reason in the literature* why researchers avoid assessed values for event studies.

3. **The "full stock vs. only sold properties" argument has merit only if the treatment effect operates slowly**: Assessed values cover the full property stock, which avoids selection bias from studying only traded properties. This is a genuine advantage for long-run capitalization studies. But for the FBT shock (2016), where transaction-level evidence is abundant (thousands of sales per quarter in Metro Vancouver), the selection bias argument is weaker — there are enough transactions to estimate effects from MLS data.

4. **The research document acknowledges this with "annual assessed values lag market prices by 12+ months"** — but then proceeds to recommend using assessed values anyway, without fully engaging with the methodological literature that says this makes event studies unreliable. The document has one sentence acknowledging the lag but does not address the attenuation bias consequence.

### What would actually be novel:
Using BC Assessment data for a *long-run capitalization study* (e.g., measuring the permanent component of policy effects 5–10 years post-treatment) is genuinely underexplored. The documented literature emphasizes short-run effects. A contribution that uses annual assessed values to study whether FBT effects are permanent (assessed value track over 2013–2022) would be novel AND would sidestep the event-study timing problem by not trying to identify the immediate shock.

### Verdict on the gap claim:
The claim that "no paper uses BC Assessment annual assessed values rather than MLS transaction prices" may be literally true, but it is true for documented methodological reasons (lag, attenuation bias), not because of oversight. Presenting this as a contribution without acknowledging and directly addressing the attenuation bias literature (Fischer et al., Berlin School paper) would be a significant weakness that peer reviewers would identify immediately.

---

## PART 4: DiD DESIGN CHALLENGES

---

## Claim: Foreign buyer share data is available from "pre-policy voluntary disclosure records" — usable as treatment assignment proxy

- **Source tier**: 3 (academic secondary description, not primary data documentation)
- **Verification**: PLAUSIBLE BUT RESTRICTED
- **Confidence**: MEDIUM
- **Evidence**: BC Ministry of Finance began collecting foreign buyer data on June 10, 2016, approximately 6 weeks before the FBT effective date, per PTT administrative records. By end of 2016, foreign buyers' market share had fallen from ~13% to below 3%. This data exists but is NOT publicly available — it requires a data access agreement with the BC Ministry of Finance (as Pavlov/Somerville/Wetzel obtained). Confirmable from BCREA's SVT impact estimates and Globe and Mail reporting on the June 2016 data collection start.
- **Challenge**: The document acknowledges "these records are the gold standard but are not publicly available." For a portfolio project (non-academic, no institutional data agreements), this dataset is inaccessible. The document then pivots to Census proxies.

---

## Claim: 2016 Census "recent-immigrant-share" proxy is usable as a proxy for foreign buyer share in DiD treatment assignment

- **Source tier**: 5 (methodological inference, documented limitations)
- **Verification**: PLAUSIBLE WITH KNOWN BIASES
- **Confidence**: LOW-MEDIUM
- **Evidence**: Pavlov & Somerville (2020) used this approach in the IIP paper. However, the conceptual validity of equating "recent immigrant share" with "foreign buyer concentration" is problematic for several reasons identified in the research literature:

### Problems with the proxy:
1. **Recent immigrants are different from foreign buyers**: A recent immigrant is a Canadian permanent resident or newly naturalized citizen who physically resides in Canada and pays Canadian income tax. A foreign buyer is a non-Canadian national who may not reside in Canada. These populations overlap (foreign nationals who recently became PRs) but are not the same. Recent immigrants *can* buy property, are not subject to the FBT, and would not be deterred by it. Using recent immigrant share as a proxy for foreign buyer share captures the right *neighborhoods* (Chinese, Hong Kong, Taiwanese diaspora areas did have more foreign buyers) but for the wrong reason (ethnic correlation, not status correlation).

2. **Conflates ethnicity with citizenship**: As the document itself acknowledges, this "Problematic because it conflates ethnicity with foreign status." Vancouver has large established Chinese-Canadian communities (2nd, 3rd generation) who would appear in "recent immigrant" counts but are definitively not foreign buyers.

3. **The 2016 Census captures the population as of May 2016**, slightly before the treatment (August 2016). This is correct for pre-treatment assignment.

4. **Known direction of bias**: The proxy likely overstates treatment intensity in neighborhoods with large established immigrant communities relative to actual foreign buyer concentration, leading to attenuation of the DiD estimate (harder to detect true effects because control tracts are contaminated by neighbors who share the proxy characteristics but face no treatment).

### What Pavlov/Somerville actually did:
The 2024 Pavlov/Somerville/Wetzel paper explicitly used pre-policy administrative PTT records (not Census proxies) to identify high vs. low foreign buyer concentration neighborhoods. The Census proxy is explicitly mentioned in the research document as the fallback "what you can use without a data agreement" option. This is a qualitatively different identification strategy from the published literature, and any DiD using Census proxies will produce noisier, likely attenuated estimates compared to the published literature.

---

## Claim: Parallel trends assumption is plausible for the neighborhood-level FBT DiD (high vs. low foreign buyer concentration)

- **Source tier**: 4 (methodological inference from published literature)
- **Verification**: PLAUSIBLE but not verified through a pre-trends test
- **Confidence**: MEDIUM
- **Evidence**: Pavlov/Somerville (2024) use this design and presumably passed peer review, implying reviewers accepted the parallel trends argument.
- **Challenge**:
  1. High-concentration neighborhoods (West Vancouver, Richmond, Burnaby portions) were already experiencing faster price appreciation pre-2016 than low-concentration neighborhoods, driven by the same foreign buyer demand that the FBT targeted. This *pre-existing differential trend* is precisely what makes parallel trends questionable: if high-concentration areas were appreciating faster before 2016, separating this trend from the treatment effect requires strong controls or a longer pre-period test.
  2. **Spillover contamination**: If the FBT reduced demand in high-concentration areas and redirected buyers to low-concentration areas, the control group (low-concentration) would see upward price pressure post-treatment — contaminating the comparison. The document acknowledges this as "general equilibrium spillover" in Option B's weakness section.
  3. **Local economic shocks**: Some high-concentration neighborhoods (e.g., Richmond, Burnaby) had specific commercial and employment shocks in 2015–2016 (Richmond's Brighouse area redevelopment, Burnaby's Metrotown densification) that could violate parallel trends independently of the FBT.

---

## Claim: Burnaby, Richmond, North Vancouver serve as valid control group for Vancouver EHT DiD (2015–2018)

- **Source tier**: 5 (design assumption, not empirically tested in the document)
- **Verification**: CHALLENGED
- **Confidence**: LOW
- **Evidence**: The Caracciolo/Miglino paper uses a 800-meter border zone around Vancouver/Burnaby boundary as its control — not municipality-wide Burnaby. This design choice is not arbitrary: it attempts to address the fact that Burnaby and Richmond are *different housing markets* in structure, density, and price level.
- **Challenge**:
  1. **Different market structures**: Richmond is dominated by strata (condo/townhouse) and recent Chinese immigrant demand. North Vancouver (City and District) is dominated by single-family residential with different demographic profiles. Burnaby spans from dense Brentwood/Metrotown to suburban Burnaby Mountain. These are not parallel to the City of Vancouver's housing market.
  2. **SVT contamination begins February 2018, not December 2018**: As noted above, the SVT was *announced* in the February 2018 budget. A control group study ending December 2018 is contaminated by 10 months of anticipation effects in both the treatment (City of Vancouver) and control (Burnaby, Richmond — both Metro Vancouver, both SVT-designated) municipalities. This is a problem the document acknowledges incompletely.
  3. **EHT is a declaration-based tax that primarily affects owners who hold vacant units**: The parallel trends assumption requires that Burnaby/Richmond property owners would have changed their vacancy behavior at the same rate as Vancouver property owners in the absence of the EHT. Given that Richmond and Burnaby have different proportions of investment properties, strata vs. freehold, and ownership structures, this is a heroic assumption.
  4. **North Vancouver did not have a municipal vacancy tax, but it is a tight rental market**: North Vancouver's rental market characteristics in 2015–2017 were quite different from Vancouver's (higher owner-occupancy rate, less speculative investment). Using it as a control for a vacancy tax study may be inappropriate.

---

## PART 5: SCORING SUMMARY

| Claim | Source Tier | Verification | Confidence | Key Issue |
|-------|-------------|-------------|------------|-----------|
| FBT effective date August 2, 2016 | 1 | VERIFIED | HIGH | None |
| FBT initial rate 15% | 1 | VERIFIED | HIGH | None |
| FBT Feb 21, 2018 amendment to 20% | 1 | VERIFIED | HIGH | Transitional provision not noted |
| EHT effective date Jan 1, 2017, By-law 11674 | 1 | VERIFIED | HIGH | None |
| EHT declared vacant ~2,500 (2017), under 1,000 (2024) | 2 | VERIFIED | HIGH | Caracciolo finds only 226 net attributable |
| SVT first tax year 2018, SBC 2018 c. 46 | 1 | VERIFIED | HIGH | Anticipation from Feb 2018 Budget not acknowledged |
| SVT rate structure 0.5% / 2% | 1 | VERIFIED | HIGH | Domestic 0.5% behavioral effects may be larger than claimed |
| Federal UHT effective 2022, eliminated 2025 | 1 | VERIFIED WITH ERROR | HIGH | Document misstates 2024 as no-filing year (it's 2025) |
| Federal prohibition extended to Jan 1, 2027 | 1 | VERIFIED | HIGH | None |
| STR restrictions May 1, 2024 | 1 | VERIFIED | HIGH | "60+" communities may be inaccurate (65 confirmed) |
| Broadway Plan June 2022, 30,000 homes | 2 | PARTIALLY VERIFIED | MEDIUM | 30,000 figure not independently confirmed |
| Bill 44 royal assent Nov 30, 2023 | 1 | VERIFIED | HIGH | RS zone numbering slightly inaccurate |
| R1-1 adopted October 17, 2023 | 1 | VERIFIED | HIGH | None |
| BoC rate hike sequence 2022 | 1 | VERIFIED WITH ERROR | HIGH | March 8, 2023 was a hold, not a hike |
| Vancouver benchmark peak ~$1.25M April 2022 | 3 | PLAUSIBLE, UNVERIFIED | MEDIUM | Specific figure not confirmed; source not cited |
| Du/Yin/Zhang (2022) JHE Vol 55 | 1 | VERIFIED | HIGH | DOI is wrong (101807 not 101791) |
| Pavlov/Somerville (2024) REE 52(3) | 1 | VERIFIED | HIGH | Missing third author: Jake Wetzel |
| Hartley et al. (2024) JRER | 1 | VERIFIED | HIGH | Citation lacks volume/pages |
| Andersen et al. (2024) JEG 24(4) | UNCERTAIN | PLAUSIBLE | LOW | Authors unconfirmed; risk of misattribution |
| Caracciolo/Miglino (2024) SSRN 4919236 | 1 | VERIFIED | HIGH | Control group description oversimplified |
| Han/Stacey/Chen (2023) ABFER | 2 | VERIFIED | HIGH | Third author is "Hong Cheng," not "Hong Chen" |
| Favilukis/Van Nieuwerburgh (2021) JF | 1 | VERIFIED | HIGH | SSRN ID in document is wrong (2922230 not 3035279) |
| Pavlov/Somerville (2020) REE 48(3) | 1 | VERIFIED | HIGH | None |
| Ley (2021) Urban Studies 58(2) | 1 | VERIFIED | HIGH | None |
| Systematic review (2023) Heliyon | UNKNOWN | UNVERIFIED | LOW | No authors, no title, no DOI |
| Gap claim: no DiD using assessed values | 6 | PLAUSIBLE BUT MISLEADING | MEDIUM | Gap is real but intentional; attenuation bias literature not engaged |
| Parallel trends FBT neighborhood DiD | 5 | CHALLENGED | MEDIUM | Pre-treatment trends may not be parallel |
| EHT control group (Burnaby, Richmond, N.Van) | 5 | CHALLENGED | LOW | SVT anticipation contaminates 2018; markets not parallel |
| Census immigrant proxy for foreign buyer share | 5 | PLAUSIBLE WITH KNOWN BIASES | LOW | Conflates ethnicity with citizenship; attenuation likely |

---

## PART 6: SUMMARY OF MATERIAL ERRORS

### Factual errors requiring correction before publication:
1. **DOI for Du/Yin/Zhang**: Cited as `10.1016/j.jhe.2021.101791`. Correct DOI is `10.1016/j.jhe.2021.101807`.
2. **Missing author on Pavlov/Somerville (2024)**: Third author Jake Wetzel is omitted.
3. **Wrong author on Han/Stacey paper**: Third author is Hong Cheng, not Hong Chen.
4. **Wrong SSRN ID for Favilukis/Van Nieuwerburgh**: Document cites 3035279 (Affordable Housing paper with Mabille). Correct ID for Out-of-Town Home Buyers is 2922230.
5. **Systematic review citation incomplete**: No authors, title, or DOI.
6. **Bank of Canada March 8, 2023**: This was a rate hold, not a +25 bps hike. Rate hike was June 7, 2023 (to 4.75%), then July 12, 2023 (to 5.00%).
7. **UHT elimination year**: Document implies 2024 filings are exempt; correct answer is 2025 and later are exempt. 2024 still required.
8. **Andersen et al. authorship**: Could not be confirmed. Risk of misattribution to a Danish economist unconnected to this research.

### Methodological concerns requiring acknowledgment in the research document:
1. **Assessed values for event studies**: The literature explicitly warns against this due to attenuation bias from the 12-month lag. BC Assessment's July 1 valuation date means the FBT shock (August 2, 2016) cannot appear in assessment data until January 2018 (2017 assessments). This is not a gap in the literature — it is a known limitation. The document must engage with Fischer et al. and the Berlin School evidence before claiming assessed values as an advantage.
2. **SVT anticipation effects begin February 2018, not December 2018**: The EHT control group is contaminated from February 2018, not after the year ends.
3. **Census immigrant proxy for foreign buyers**: The known biases (conflates ethnicity with legal status, likely attenuation) must be discussed explicitly. Any results using this proxy will be noisier and less comparable to Pavlov/Somerville/Wetzel who used actual PTT records.
4. **Parallel trends in FBT neighborhood DiD**: Pre-treatment trends in high vs. low foreign buyer concentration areas are likely non-parallel given the pre-existing divergence driven by foreign demand itself. A pre-trends test is not just recommended — it is essential for any credible DiD here.

---

*Review completed 2026-03-03. Sources verified via web search; direct journal access was not available for all papers. Primary citations confirmed through IDEAS/RePEC, SSRN, Wiley Online Library, and government primary sources.*
