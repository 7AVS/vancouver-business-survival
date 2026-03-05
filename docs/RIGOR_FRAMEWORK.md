# Research + Data Project Rigor Framework

**Version**: 1.1 | **Created**: 2026-03-03 | **Updated**: 2026-03-03
**Canonical location**: `/home/aurora/projects/research-skill/DATA-PROJECT-RIGOR.md`

A rigor protocol for data projects where AI agents produce research at speed. It adds structured source scoring, assumption tracking, adversarial challenge checkpoints, and agent delegation controls to every phase of the project lifecycle.

Use this document when a project involves both research (finding and evaluating external information) AND data analysis (building datasets, running models, producing quantitative conclusions).

---

## Lineage and Adaptations

This framework draws from established methodologies but departs from them significantly. Crediting what we took, naming what we changed, and why.

### What we drew from

| Source | What we took | Year |
|--------|-------------|------|
| CRISP-DM (Chapman et al.) | Phase sequencing concept (problem → data → analysis → communication) | 1999 |
| Tukey, *Exploratory Data Analysis* | EDA-first principle — let data speak before modeling | 1977 |
| Universal Research Skill (internal) | 5-layer quality model, adversarial challenge concept | 2026 |
| Practical experience with AI agents | Everything in Parts 1, 2, 3, 6 | 2026 |

### What we changed and why

**Source scoring (Part 1) — new, no precedent in CRISP-DM.**
CRISP-DM assumes the analyst knows where their facts came from. When AI agents produce research, the provenance of any claim is unknown by default. The 6-tier system with T6 (LLM inference) as the default exists because agents sound confident regardless of accuracy. This control didn't need to exist in 1999.

**Assumption register (Part 2) — extends CRISP-DM's "document assumptions" into an auditable system.**
CRISP-DM says "document assumptions." That's a sentence in a 60-page guide. In practice, assumptions are implicit, forgotten, and never revisited. The register forces them into a structured, append-only log with confidence scoring and verification status. The trigger: an AI agent produced 6 hallucinated citations in a housing policy research brief and every downstream conclusion inherited the error.

**Adversarial challenge (Part 3) — new, adapted from adversarial ML evaluation.**
CRISP-DM has no mechanism for challenging findings before communicating them. The assumption is that the analyst is self-critical. With AI agents, the output is optimized to sound correct, not to be correct. The adversarial protocol forces explicit disconfirmation attempts at every decision point. The three-mode structure (lightweight → standard → full) prevents this from being all-or-nothing.

**Agent delegation protocol (Part 6) — entirely new.**
Did not exist in any data science methodology before 2024. The core problem: AI agents produce deliverables that look complete but may contain fabricated sources, mischaracterized findings, and unverifiable claims. The 20% spot-check rule, the T6 auto-classify default, and the requirement to separate facts from inferences are all responses to observed failures.

**Data acquisition protocol (Part 8) — new, from observed failure.**
An agent given a narrow task ("download business licences 2013-2024") finds the archive dataset and stops. A separate current dataset with 2025-2026 data exists on the same portal and goes unnoticed. The project runs on stale data for weeks. CRISP-DM's Phase 1 says "collect data" — it has no mechanism to prevent narrow fetching. The catalog-first rule and the requirement to enumerate all available datasets before downloading any of them close this gap.

**Scope control — addressed but could be stronger.**
CRISP-DM assumes a well-defined business problem. Exploratory and hobby projects drift. Phase 0 now requires an explicit scope boundary ("what this analysis will NOT address"), but scope creep during execution remains a human discipline problem, not a framework-solvable one. Flag it when you see it.

### What we kept as-is

- The phase sequence (0-8) is sound. Skipping to modeling without understanding data is still the #1 failure mode.
- "Problem framing determines everything" — timeless.
- Train/test split before preprocessing — still a hard rule, still violated constantly.
- Baseline model first — still the right discipline.

### What's missing (known gaps)

- **Reproducibility protocol**: No current mechanism for ensuring another person can re-run the analysis and get the same results. Future version should address environment management, random seeds, and pipeline documentation.
- **Collaboration controls**: This framework assumes a single analyst (or analyst + AI agents). Multi-person projects need merge protocols for the assumption and source registers.
- **Cost-benefit on rigor**: Not every project needs full rigor. A quick analysis for personal curiosity doesn't need three appendices. The framework should eventually include a "rigor level" selector (light / standard / full) matched to project stakes.

---

## Part 1: Source Scoring System

Every factual claim in a research or data project must carry a source tier. Tier assignment determines how much analytical weight the claim can carry before needing verification.

### Tier Definitions

| Tier | Weight | Examples | Default Trust |
|------|--------|----------|---------------|
| **T1** | 1.0 | Government databases, Statistics Canada microdata, legislation text, court rulings, official statistical releases | Trust the data; verify interpretation |
| **T2** | 0.9 | Peer-reviewed journal articles (published in recognized journals, post-review) | Trust established; check methods section |
| **T3** | 0.7 | Working papers (NBER, SSRN), institutional reports (C.D. Howe, Fraser Institute, CMHC, IMF, World Bank), conference proceedings | Trust findings; note not peer-reviewed |
| **T4** | 0.5 | News articles from major outlets (Globe & Mail, Reuters, FT), government press releases, official blog posts from institutions | Trust for events/dates; verify stats they cite |
| **T5** | 0.3 | Opinion pieces, non-peer-reviewed analysis, think tank commentary, personal finance sites | Corroborate with higher tier before using |
| **T6** | 0.1 | LLM inference — model "just knows it", no external source cited | Must verify before building on it |

**T6 is the default** when an agent makes a claim without citing a retrievable source. If you cannot produce a URL, document title, or dataset name, it's T6.

### How to Apply Weights

A finding's **effective confidence** is a function of the highest tier source that supports it and how many independent sources corroborate it:

- **T1 or T2, single source**: Treat as established. Note the source. Adversarial challenge still applies for causal claims.
- **T3, 2+ sources**: Treat as established for analytical purposes. Flag in appendix.
- **T3, single source**: Treat as working assumption. Log in assumption register. Verify if it's load-bearing.
- **T4-T5, any count**: Do not treat as established fact. Use as leads to find T1-T3 sources. Never let T4-T5 be the primary basis of a quantitative claim.
- **T6, any claim**: Must be verified before building on it. If the analysis proceeds with unverified T6 claims, every downstream conclusion inherits T6 status.

**Compounding rule**: If Claim B depends on Claim A, and Claim A is T6, then Claim B is also T6 regardless of its own sourcing.

### Source Register Template

Maintain a source register for every project. One row per source consulted.

| ID | Title / Description | Type | Tier | URL or Location | Date Accessed | Used For | Notes |
|----|---------------------|------|------|-----------------|---------------|----------|-------|
| S1 | Statistics Canada Table 18-10-0056-01 (CPI) | Dataset | T1 | statcan.gc.ca/... | 2026-03-03 | Inflation adjustment | Annual, 2023 latest |
| S2 | Sims (2023) "Property Tax Incidence in Canada" | Journal article | T2 | DOI: 10.xxxx | 2026-03-03 | Tax shifting hypothesis | Published in Canadian Journal of Economics |
| S3 | CMHC Housing Market Outlook Q4 2025 | Institutional report | T3 | cmhc-schl.gc.ca/... | 2026-03-03 | Vacancy trends | Not peer-reviewed |
| S4 | Globe & Mail article on BC Assessment 2025 | News | T4 | globe... | 2026-03-03 | Policy context | Cites BC Assessment directly — find primary |

---

## Part 2: Assumption Register

Every analytical project makes assumptions. Most failures happen because assumptions were implicit. The assumption register makes them explicit, scored, and trackable.

**Rule**: If you would have to defend a choice in front of a skeptical peer, log it as an assumption.

### Assumption Register Template

| ID | Assumption | Basis | Source Tier | Confidence | Impact if Wrong | Verification Method | Status | Notes |
|----|------------|-------|-------------|------------|-----------------|---------------------|--------|-------|
| A1 | BC Assessment rolls are an accurate proxy for market value at time of assessment | BC Assessment mandate under Assessment Act; prior academic use in Andrle et al. (2022) | T1 / T2 | HIGH | Assessment-sale gaps would bias all price analysis | Compare to MLS transaction data for same period | VERIFIED | Gap is ~5-10% per literature |
| A2 | Properties with missing mill rate data are missing at random (MCAR) | Visual inspection — no obvious geographic clustering | T6 | LOW | Systematic missingness would bias geographic comparisons | Chi-squared test of missingness by neighborhood | UNVERIFIED | Load-bearing — must verify before Phase 3 |
| A3 | 2023 was not a structural break year for the property tax mill rate | Reviewed BC government budget statements; no announced structural change | T4 | MEDIUM | Pre/post comparisons invalid; difference-in-differences design breaks | Search BC Municipal Finance gazette for rate change announcements | ACCEPTED-WITH-CAVEAT | Budget statements are T4; need T1 confirmation |

### Status Definitions

| Status | Meaning |
|--------|---------|
| **UNVERIFIED** | Logged but not yet checked. Cannot be load-bearing. |
| **VERIFIED** | Checked against T1-T2 source. Can be load-bearing. |
| **REFUTED** | Evidence shows assumption is false. Analysis must be revised. |
| **ACCEPTED-WITH-CAVEAT** | Cannot be fully verified; proceeding with disclosed uncertainty. Must appear in limitations section. |

### Rules for the Assumption Register

1. Every assumption gets an ID. Once assigned, IDs do not change.
2. The register is append-only during active analysis. Do not delete refuted assumptions — mark them REFUTED and note what changed.
3. Any assumption with Confidence = LOW that is load-bearing for a conclusion must be verified before that conclusion is reported.
4. The register is included as an appendix in the final deliverable.

---

## Part 3: Adversarial Challenge Protocol

An adversarial challenge is a deliberate attempt to disprove the analysis before anyone else does. It is not pessimism — it is quality control. A finding that survives adversarial challenge is stronger. A finding that doesn't must be downgraded or revised.

### When a Challenge is Required (Non-Negotiable)

- [ ] Before choosing the primary dataset for the project
- [ ] Before finalizing the analytical approach or identification strategy
- [ ] Before accepting any "gap in literature" or "nobody has done X" claim
- [ ] Before treating any EDA finding as a hypothesis worth modeling
- [ ] Before presenting conclusions to any external audience
- [ ] Any time a finding feels too clean, too convenient, or too confirmatory

### Challenge Protocol — Three Modes

**Mode 1: Lightweight (routine analysis)**
After every major finding, ask explicitly:
- "Why might this be wrong?"
- "What's the alternative explanation?"
- "Who would disagree with this, and what would they say?"

Document answers in a `CHALLENGE:` block beneath the finding. Minimum two objections per key claim.

**Mode 2: Standard (load-bearing claims)**
- Run targeted searches specifically designed to disprove the claim
- Search for "criticism of [method]", "[finding] contradicted by", "[dataset] problems", "[assumption] violation"
- Log search queries and what was found (including null results)
- Produce a brief challenge report (3-5 sentences per challenged claim)

**Mode 3: Full (high-stakes conclusions, published work)**
Assign three roles explicitly:
- **Prosecutor**: Argues the findings are wrong. Searches for every counterpoint. Produces a brief for the opposition.
- **Defender**: Steelmans the findings. Argues why each objection fails. Produces a rebuttal.
- **Arbiter**: Reads both briefs, makes a final judgment on confidence. Can require additional evidence before proceeding.

This three-role structure can be run by a single agent switching modes, or delegated to subagents.

### Challenge Documentation Format

```
## ADVERSARIAL CHALLENGE — [Claim or Finding]

**Claim under challenge**: [exact claim]
**Challenge mode**: Lightweight / Standard / Full
**Date**: YYYY-MM-DD

**Objections raised**:
1. [Objection]: [Argument]. [Evidence searched for: query, result]
2. [Objection]: [Argument]. [Evidence searched for: query, result]

**Defense**:
- [Why objection 1 fails or is mitigated]
- [Why objection 2 fails or is mitigated]

**Verdict**: [SURVIVES CHALLENGE / DOWNGRADED / REQUIRES MORE EVIDENCE]
**Confidence after challenge**: HIGH / MEDIUM / LOW / UNCERTAIN
**Action**: [None / Caveat added / Assumption logged / Finding revised]
```

---

## Part 4: Verification Protocol by Claim Type

Not all claims require the same verification procedure. Use the appropriate protocol for the type of claim being made.

### Academic Papers
1. Search Google Scholar for exact title + lead author + year
2. Confirm the paper exists at the cited journal/venue
3. Read the abstract; confirm the finding described matches what's actually in the paper (agents regularly mischaracterize findings)
4. If access is paywalled, check SSRN, arXiv, or author's institutional page for preprint
5. If still inaccessible, downgrade to T3 and note "abstract only"

### Policy Dates and Legal Events
1. Cross-reference with: government gazette, official legislation text, or official government announcement page
2. Require two independent sources (e.g., legislation text + news report of enactment)
3. For BC-specific policy: check BC Laws (bclaws.gov.bc.ca) as T1 source
4. Do not use Wikipedia or news articles as sole source for legal effective dates

### Statistics and Numbers
1. Trace the number to its primary source (Statistics Canada table ID, BC Assessment data release, etc.)
2. If primary source is accessible: reproduce the number directly from the source
3. If not reproducible from primary source: require at minimum a T2 source with explicit methodology
4. Watch for: base year differences, geographic scope differences, rounding, and definition differences across sources that appear to report the same number

### "Nobody Has Done X" / Gap Claims
1. These claims are almost always wrong or imprecise. Treat as T6 until proven otherwise.
2. Search: Google Scholar for [method] + [domain], SSRN for working papers, web for grey literature
3. If literature search finds nothing: narrow the claim to "I found no published work on [specific combination] using [specific method] as of [date accessed]"
4. Absence of evidence is not evidence of absence. Use this formulation: "No peer-reviewed literature was identified" — not "no literature exists"

### Causal Claims
1. Any claim of the form "X causes Y" or "X leads to Y" or "X is driven by" requires:
   - Explicit identification strategy (what makes this causal rather than correlational?)
   - Stated assumptions of the identification strategy
   - List of potential confounds and how they are addressed
2. Observational data cannot support causal claims without explicit methodology (RD, IV, DiD, matching, etc.)
3. If the identification strategy cannot be stated, downgrade to "X is associated with Y"

---

## Part 5: Integrated Project Lifecycle

The project lifecycle with rigor checkpoints at every phase gate. Each phase has mandatory controls before proceeding to the next.

### Phase 0: Problem Framing

**Goal**: Translate research/business question into a precise analytical question.

**Standard steps**:
- Define target variable precisely
- Define success criteria before touching data
- Document constraints

**Rigor controls**:
- [ ] Write the research question in one sentence. If you can't, the framing is not done.
- [ ] Start the assumption register. Minimum 3 entries at this stage (scope, data availability, approach).
- [ ] Start the source register.
- [ ] Run adversarial challenge on the research question itself: "Is this the right question? Is this question answerable?"
- [ ] Explicitly state what this analysis will NOT address (scope boundary).

**Gate to Phase 1**: Research question is crisp. At least one T1-T2 source supports the feasibility of answering it. Adversarial challenge on framing is documented.

---

### Phase 1: Data Acquisition

**Goal**: Collect and ingest data. Document what you have.

**Standard steps**:
- Data inventory: source, format, row/column counts, update frequency
- Document provenance

**Rigor controls**:
- [ ] **Apply the Data Acquisition Protocol (Part 8) before downloading anything.** Enumerate first; download second.
- [ ] For each dataset: record source tier (T1-T4 at minimum for primary datasets — T5 or T6 data is suspect)
- [ ] Document data provenance: who collected it, when, using what method?
- [ ] Run adversarial challenge: "Is this the right dataset for this question? What's missing?"
- [ ] Log assumptions about data currency: "We assume this dataset reflects conditions as of [date]" (A-ID)
- [ ] If using a secondary dataset (someone else processed it), find and document the primary source

**Gate to Phase 2**: Every dataset in the project has a source register entry with tier, provenance, and currency note. Data catalog saved to project inventory before any downloads occurred.

---

### Phase 2: Data Quality Assessment

**Goal**: Know what you actually have before analyzing it.

**Standard steps**:
- Schema validation: types, ranges, allowed values
- Completeness: missing value rates, patterns (MCAR/MAR/MNAR)
- Consistency: cross-field logic checks
- Uniqueness: duplicate detection
- Timeliness: is data current enough?
- **Produce Data Quality Report**

**Rigor controls**:
- [ ] Every quality finding must reference the dataset's own documentation. If BC Assessment says mill rate should never be null and you find nulls — that is a finding, not a normal variation.
- [ ] Log every assumption about missing data patterns as an assumption register entry (what pattern, what assumption, what's the impact if wrong).
- [ ] MCAR/MAR/MNAR classification must be tested, not assumed. Log the test.
- [ ] If data quality is worse than expected: run adversarial challenge — "Does this quality issue invalidate the study?"

**Gate to Phase 3**: Data Quality Report exists. Missing data assumptions are logged and classified. No silent ignoring of quality issues.

---

### Phase 3: Exploratory Data Analysis

**Goal**: Understand the data before modeling.

**Standard steps**:
1. Univariate — distributions, central tendency, spread, outliers
2. Target variable — distribution, balance, skew
3. Bivariate — each feature vs target
4. Multivariate — correlations, pair plots
5. Temporal — trends, seasonality, breaks (if time-indexed)
6. Outlier investigation — document, don't silently remove
7. Missing value patterns — heatmaps, correlations of missingness
8. Hypothesis generation

**Rigor controls**:
- [ ] Every hypothesis generated in EDA must be logged with: what you observed, what it suggests, what the alternative explanation is.
- [ ] Every visual pattern must be supported by a statistical check (not just "the chart looks like").
- [ ] Run adversarial challenge on the 2-3 most important EDA findings before proceeding.
- [ ] Outliers: each one gets a disposition note in the assumption register. Removing an outlier is an assumption.
- [ ] If a pattern "confirms" your prior belief: flag it for adversarial challenge. Confirmation feels good; that's when bias sneaks in.

**Gate to Phase 4**: Hypothesis list with source basis for each. EDA findings that will drive modeling decisions have survived lightweight adversarial challenge.

---

### Phase 4: Data Preparation

**Goal**: Transform raw data into analysis-ready form.

**Standard steps**:
- Train/val/test split BEFORE imputation/scaling (prevent leakage)
- Imputation justified by MCAR/MAR/MNAR classification
- Outlier handling (document decision)
- Encoding, normalization

**Rigor controls**:
- [ ] Log every imputation choice as an assumption. "We imputed with median" = assumption that MCAR holds + that median is appropriate estimator.
- [ ] Log every encoding decision. Ordinal encoding of a nominal variable is an assumption about ordinality.
- [ ] Data leakage check: confirm split happened before preprocessing. This is a hard rule — leakage is a research integrity issue, not just a modeling mistake.
- [ ] If any transformation "fixes" a quality issue found in Phase 2: document the fix, log the assumption about its validity.

**Gate to Phase 5**: Transformation log exists. Every preprocessing choice is logged in the assumption register.

---

### Phase 5: Feature Engineering

**Goal**: Create the best analytical inputs for modeling.

**Standard steps**:
- Domain knowledge features
- Interaction terms, ratios, lags/windows for time series
- Feature selection

**Rigor controls**:
- [ ] Every domain-knowledge feature must be grounded in a source (T1-T3 preferred). "I added this feature because intuitively..." is a T6 assumption.
- [ ] Log all interaction terms as assumptions: "We assume the effect of X on Y varies by Z."
- [ ] Feature selection decisions must be documented. Dropped features are not just gone — they represent assumptions about what matters.
- [ ] Run adversarial challenge on feature set: "What important variable is missing? Why?"

**Gate to Phase 6**: Feature decisions logged. No undocumented choices.

---

### Phase 6: Modeling

**Goal**: Build and evaluate candidate models.

**Standard steps**:
- Baseline first (simplest model)
- Multiple algorithm families
- Hyperparameter tuning via CV on train only
- Document every run

**Rigor controls**:
- [ ] Model choice is an assumption. Log why this family of models was chosen over alternatives.
- [ ] Baseline must be reported alongside all results. Complexity must beat baseline to be justified.
- [ ] For causal models: identification strategy must be stated (see Verification Protocol — Causal Claims).
- [ ] Run adversarial challenge on results: "Why might this performance be misleading? What would make these results fail to generalize?"
- [ ] If results are suspiciously good: trigger adversarial challenge immediately. A model that perfectly fits training data is not a finding — it's a warning.

**Gate to Phase 7**: All model runs logged. Model choice assumption logged. Adversarial challenge on key results documented.

---

### Phase 7: Evaluation

**Goal**: Test on held-out data. Make honest claims about performance.

**Standard steps**:
- Holdout test set evaluated ONCE at the end
- Metrics aligned with business question
- Error analysis: where does the model fail?

**Rigor controls**:
- [ ] Metrics must be defined in Phase 0 and not changed here. Changing metrics post-hoc to make results look better is p-hacking.
- [ ] Report error analysis — not just overall metrics. Where does the model fail? Which subgroups?
- [ ] Run full adversarial challenge (Mode 2) on conclusions before finalizing.
- [ ] Verify that test set was never touched before this step (data hygiene audit).
- [ ] Produce honest limitations statement: what does this model not do well, and why?

**Gate to Phase 8**: Test set was used exactly once. Conclusions have survived adversarial challenge. Limitations are documented.

---

### Phase 8: Communication

**Goal**: Produce findings in a form others can use and scrutinize.

**Standard steps**:
- Translate to audience language
- Document limitations
- Monitoring/drift strategy (for production models)

**Rigor controls**:
- [ ] **Appendix A — Source Register**: Full source register compiled and included.
- [ ] **Appendix B — Assumption Register**: Full assumption register compiled. Status of each logged.
- [ ] **Appendix C — Adversarial Challenge Log**: Summary of all challenges run and their verdicts.
- [ ] Every confidence claim in the main body maps to a specific register entry.
- [ ] Claims that are ACCEPTED-WITH-CAVEAT or have Confidence = LOW must be disclosed as such in the body (not buried in the appendix).
- [ ] No conclusions are presented as stronger than the evidence supports.

---

## Part 6: Agent Delegation Protocol

When delegating research or data tasks to AI agents, the following rules apply to all outputs returned.

### What Agents Must Return

Every agent output must include:
1. **Main deliverable** (findings, data, analysis)
2. **Source register entries** for every claim in the deliverable
3. **Explicit separation** of "verified facts" (retrieved from an external source) vs. "inferences" (derived from model reasoning)
4. **Failed searches** — queries that were run but returned no useful results

If an agent returns findings without source citations, every claim is automatically classified T6 until verified.

### Orchestrator Responsibilities

The orchestrating agent (or Andre, when reviewing agent outputs) must:

- [ ] Spot-check at minimum **20% of T6 claims** before proceeding. Sample randomly, not by convenience.
- [ ] Verify any T6 claim that is **load-bearing** for the analysis (if the project conclusion rests on it, 100% verification required).
- [ ] Reject agent outputs that do not distinguish facts from inferences. Return for revision.
- [ ] When an agent cites a source, verify at least one cited source per major claim section (not just one per output).

### Delegation Request Format

When sending a research task to an agent, always include:

```
Task: [description]
Required output format:
- Section 1: [deliverable type]
- Source register: One row per claim — ID, claim, source title, URL, tier
- Inferences section: List all claims derived from model reasoning (no external source)
- Failed searches: List queries attempted that returned no useful results
Quality bar: T3 or higher required for [specific claims]. T6 claims require explicit flagging.
```

---

## Part 7: Quick-Reference Checklist

For any project that combines research and data analysis, run this checklist at each gate.

### Before You Start
- [ ] Research question is one clear sentence
- [ ] Source register created
- [ ] Assumption register created
- [ ] Success criteria defined

### Before Building on Any Claim
- [ ] Source tier assigned
- [ ] If T6: flagged for verification
- [ ] If load-bearing: verified (T1-T3 required)

### Before Each Phase Transition
- [ ] Phase-specific rigor controls checked off
- [ ] New assumptions logged
- [ ] New sources logged

### Before Any Adversarial Challenge
- [ ] Trigger condition met (see Part 3)
- [ ] Mode selected (Lightweight / Standard / Full)
- [ ] Challenge documented in standard format

### Before Final Deliverable
- [ ] All three appendices compiled (Sources, Assumptions, Challenges)
- [ ] No UNVERIFIED assumptions in load-bearing positions
- [ ] Limitations section is honest (not optimistic)
- [ ] Confidence levels on all key claims are disclosed

---

## Part 8: Data Acquisition Protocol

Before downloading any dataset, enumerate what the source offers. Narrow fetching — grabbing the first relevant file and stopping — is how projects end up running on incomplete data for weeks without knowing it.

**The rule: catalog first, download second.**

### Steps

**1. Catalog the source.**
Before downloading anything, list ALL datasets available from the data source. Use the API catalog endpoint, portal search, or directory listing — whatever the source exposes. For each dataset, record: name, description, temporal coverage, last updated date, record count if available.

**2. Check temporal coverage.**
What is the most recent data available? Does it extend beyond what was initially assumed? If the project scope is 2013-2024 and data through 2025-2026 exists, flag it immediately. Do not assume the dataset you found first is the most current.

**3. Flag adjacent datasets.**
If the source has related datasets — a historical archive AND a current feed, separate tables by geography or category, versioned releases — report ALL of them even if only one was explicitly requested. The requester may not know what exists. One query to the catalog costs nothing. Missing a complementary dataset costs weeks.

**4. Compare schemas before downloading multiple datasets.**
If you will combine datasets from the same source (or different releases of the same dataset), compare schemas first. Note differences in column names, data types, delimiter conventions, character encoding, and null representations. Schema mismatches discovered after download waste time and introduce silent merge errors.

**5. Save the catalog before downloading.**
Write the full catalog results to the project's data inventory file before any downloads start. This creates a record of what was available at the time of acquisition. If the source changes later — datasets removed, coverage extended, schema updated — you have a baseline to diff against.

### Catalog Documentation Format

```
## Data Catalog — [Source Name]
**Catalog date**: YYYY-MM-DD
**Source URL / API endpoint**: [url]
**Enumeration method**: [API catalog / portal search / directory listing / manual browse]

| Dataset | Description | Temporal Coverage | Last Updated | Records | Selected? | Notes |
|---------|-------------|-------------------|--------------|---------|-----------|-------|
| [name]  | [desc]      | [start–end]       | YYYY-MM-DD   | [n]     | YES / NO  | [notes] |

**Adjacent datasets noted**: [list any related datasets not selected, with reason]
**Schema comparison**: [if multiple datasets selected, note any schema differences]
**Decision**: [which datasets were downloaded and why]
```

### The Principle

Data acquisition is not "fetch this file." It is "understand what this source offers, then fetch what we need." The catalog step takes five minutes. Missing a dataset that was sitting on the same portal takes weeks to discover.

An agent given a narrow task will execute that task narrowly. The catalog step exists because task descriptions are written by people who don't yet know the full shape of what's available. The agent's job is to surface that shape before committing to a download path.

---

## Known Failure Modes (This Framework Prevents)

| Failure | How This Framework Catches It |
|---------|-------------------------------|
| LLM hallucination presented as fact | T6 default; spot-check requirement; source register |
| Assumption drift (forgot we assumed X) | Assumption register; append-only; appendix in deliverable |
| Confirmation bias in EDA | Adversarial challenge triggered on confirmatory findings |
| Causal claims from observational data | Verification protocol — causal claims require identification strategy |
| Data leakage | Phase 4 hard rule; Phase 7 data hygiene audit |
| "Gap in literature" overclaiming | Verification protocol — absence of evidence is not evidence of absence |
| Bad agent output incorporated silently | Delegation protocol; 20% spot-check; T6 auto-classify |
| Metrics changed post-hoc | Phase 0 defines metrics; Phase 7 cannot change them |
| Single-source reliance | Triangulation rule; confidence scoring |
| Narrow data fetching misses adjacent/newer datasets | Data acquisition protocol (Part 8); catalog-first rule; Phase 1 gate |

---

## Relationship to Other Documents

- **RESEARCH-SKILL.md** (5-layer quality model): The adversarial challenge in Part 3 operationalizes Layer 5. The source scoring in Part 1 replaces the informal source hierarchy in Layer 3. Use RESEARCH-SKILL.md for standalone research tasks; use this document when research feeds into a data project.
- **data-project-methodology.md** (project lifecycle): Part 5 adds rigor checkpoints to each phase. Use that file as a quick sequence reference; use this document when source verification and assumption tracking are required.

When in doubt: this document is the stricter standard.

---

*Living document. Version when methodology changes. Challenge it — that's the point.*
