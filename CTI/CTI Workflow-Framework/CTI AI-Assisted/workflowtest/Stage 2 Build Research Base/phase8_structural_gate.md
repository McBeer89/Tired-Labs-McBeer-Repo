# Phase 8: Structural Gate
## CTI Research Base: Ransomware Groups Targeting Financial Services
## IR-01 / PIR-01.1, PIR-01.2, PIR-01.3

**Analyst:** Junior Analyst 1
**Date:** March 15, 2026
**Research Base Version:** 1.0

---

## Structural Gate Evaluation

The structural gate checks the research base as a whole against seven questions. Issues are flagged with specific recommendations.

---

### 1. Does this research base answer the intelligence requirement?

**PIR-01.1 (Groups + initial access): YES.**

The base identifies Qilin, Akira, Clop, Medusa, Play, and LockBit as actively targeting financial services with confirmed intrusions. Initial access methods are documented across three categories: edge device CVE exploitation (Fortinet, SonicWall, Palo Alto, Veeam, GoAnywhere, Citrix, VMware), credential-based access via the infostealer pipeline, and ClickFix social engineering. Specific financial sector incidents are named with dates, impact figures, and attributed threat actors.

**PIR-01.2 (TTPs at procedure level, including EDR evasion): YES — scoped to CTI lane.**

The base covers C2 frameworks, RMM tool abuse, credential harvesting tools and techniques, exfiltration tools and operational timing, and BYOVD/EDR evasion at the tool and technique level with group-specific procedures where available. Procedure-to-detection translation (log sources, event IDs, detection queries) is the Detection Engineering team's responsibility during TRR research, not the CTI analyst's. The research base provides the TTP foundation from which detection-ready output is derived. GAP-005 (CTI does not produce detection-ready output) is an organizational workflow gap addressed by the derivative production framework, not a research base deficiency.

**PIR-01.3 (Demand ranges, payment rates, extortion models): YES.**

Demand ranges documented from CISA advisory data ($100K–$15M for Medusa), vendor reporting ($2.0M median for FS), and incident data ($25.66M BlackCat payment, $50M Clop demands). Payment rate decline well-supported across Chainalysis, Coveware, and Coalition. Extortion model evolution — encryption-first to data-theft-first, triple extortion, insurance policy theft, cold-calling — documented with sources.

**Status: PASS (all three PIRs answered)**

---

### 2. Are key judgments clearly separated from supporting evidence?

**⚠️ FLAG — ADDRESSED IN PHASE 9**

Key judgments were not yet drafted at the time of structural gate evaluation. Phase 9 drafted five key judgments, each clearly stated as an assessment with confidence level, supporting evidence references, and caveats. These will be inserted into Section 1 of the research base in the final compilation.

**Status: PASS (after Phase 9 completion)**

---

### 3. Are there competing hypotheses?

**⚠️ FLAG — IDENTIFIED AND DOCUMENTED**

The research base initially adopted a single implicit hypothesis: the primary threat to Hartwell comes from ransomware groups targeting financial services via edge device exploitation and credential theft.

Three competing hypotheses were identified during structural review:

**Hypothesis A (Default):** The primary threat is direct compromise of Hartwell's perimeter via edge device/VPN exploitation by groups like Akira, Qilin, and Medusa using documented CVEs.

- *Supporting evidence:* CVE-2024-55591, CVE-2025-59718/59719, CVE-2026-24858 (Fortinet — Hartwell stack); CVE-2024-40766 (SonicWall — Akira/Marquis vector); CVE-2025-10035 (GoAnywhere — Hartwell stack); 33% of initial access via vulnerability exploitation (Mandiant); 90% of ransomware incidents exploited firewalls (Barracuda).
- *Weakening evidence:* Majority of confirmed FS incidents in this base involved vendor compromise, not direct targeting.

**Hypothesis B (Supply Chain):** The primary threat is supply-chain compromise through third-party vendors, not direct intrusion against Hartwell's perimeter.

- *Supporting evidence:* Marquis (74+ banks), DBS/Toppan (brokerage), SitusAMC (JPMorgan/Citi/Morgan Stanley), Qilin/GJTec (28 firms), Betterment (CRM vendor), Western Alliance Bank (Cleo) — the majority of confirmed FS incidents in the base involved vendor compromise. 41.4% of ransomware attacks start through third parties (SecurityScorecard). With 14,500 branch offices, Hartwell's vendor surface area is substantial.
- *Weakening evidence:* This hypothesis addresses exposure, not targeting. Direct exploitation CVEs are also confirmed active against FS. Supply chain risk may be an amplifier of Hypothesis A rather than an alternative.

**Hypothesis C (Credential Pipeline):** The primary threat is credential-based access via the infostealer pipeline, not vulnerability exploitation.

- *Supporting evidence:* 41% of root causes are compromised credentials (Sophos); 75% of initial access is malware-free (CrowdStrike); documented ClickFix → StealC → Qilin chain; 59% of cases lacked MFA (Sophos); 67.32% identity-related root causes.
- *Weakening evidence:* ClickFix → StealC → Qilin is a single documented chain. Infostealer-to-IAB pipeline is better addressed under PIR-04 (Analyst 3 / Dana Mercer's assignment). The credential vector may be an enabler of Hypothesis A (credentials used to access edge devices without MFA) rather than a separate path.

**Analyst Assessment:** These hypotheses are not mutually exclusive. In practice, all three vectors are active simultaneously, and a sophisticated intrusion may chain multiple vectors (e.g., infostealers harvest VPN credentials → IAB sells access → ransomware affiliate exploits unpatched edge device using stolen credentials). The key analytic question for Hartwell is which vector represents the greatest *unmitigated* risk given current defensive posture — which requires input from Vulnerability Management (patch state) and Security Operations (detection coverage) that CTI does not currently have.

**Status: PASS (hypotheses documented; analyst accepted)**

---

### 4. Are the sources diverse?

**⚠️ FLAG — STRUCTURAL WEAKNESS ACKNOWLEDGED**

The entire research base flows through a single AI-synthesized document. While that document references diverse source categories, the analyst has not independently accessed any of them.

**Source categories referenced (not verified):**

| Category | Examples | Claim Coverage |
|---|---|---|
| Government advisories | CISA, FBI, FinCEN, OFAC, DOJ | ~15 claims |
| Vendor threat reports | Sophos, CrowdStrike, ESET, Mandiant, Symantec, Vectra AI, Arctic Wolf, Intel 471 | ~50 claims |
| Industry reports | Chainalysis, Verizon DBIR, Coveware | ~15 claims |
| Insurance reports | Coalition, Resilience, Corvus | ~8 claims |
| News/trade publications | American Banker, The Hacker News, CSO Online | ~12 claims |
| Leak site/dark web reporting | Breached.company, Flashpoint | ~10 claims |
| Academic/research | Picus Security, Comparitech, Cyble | ~8 claims |

**Referenced diversity: GOOD — seven source categories represented.**
**Actual diversity: POOR — single intermediary source.**

**Recommendation (production environment):** Process at minimum three primary sources directly before finalizing: (1) CISA Advisory AA25-071A (Medusa), (2) one Sophos Active Adversary or FS report, (3) Chainalysis Crypto Crime Report. Each would upgrade multiple claims from LOW to MODERATE confidence and break the single-source dependency.

**For this exercise:** Documented as GAP-R01 in the research base. Accepted as a known limitation.

**Status: FLAG ACKNOWLEDGED — proceed with documented limitation**

---

### 5. Are collection gaps documented?

**YES — 8 gaps documented across two categories.**

**Gaps inherited from the collection plan (3):**

| Gap ID | PIR Affected | Description |
|---|---|---|
| GAP-003 | PIR-01.1, PIR-01.2 | CTI lacks version/patch data for Veeam and GoAnywhere MFT |
| GAP-005 | PIR-01.2 | CTI does not produce detection-ready output |
| GAP-006 | PIR-01.1, PIR-01.2 | No dedicated threat hunting capability |

**Gaps identified during research (5):**

| Gap ID | PIR Affected | Description |
|---|---|---|
| GAP-R01 | All | No primary sources independently verified; all claims through AI intermediary |
| GAP-R02 | PIR-01.1 | Several FS incidents lack named primary sources |
| GAP-R03 | PIR-01.2 | Several TTP claims undated and unsourced |
| GAP-R04 | PIR-01.3 | Sector-specific economics data relies on Sophos 2024 report |
| GAP-R05 | PIR-01.1 | Several CVE numbers unverified against CISA KEV/NVD |

**Status: PASS**

---

### 6. Is anything included that the analyst can't defend?

**No indefensible claims identified.**

Marginal claims reviewed:

| Claim | Assessment |
|---|---|
| 2.2.6b (Qilin 80–85% affiliate split) | Classified as ASSUMPTION with explicit verification requirement. Defensible as context. |
| 2.10.7 (Wealth management firms on leak sites) | Retained as PARTIALLY RELEVANT. Defensible as pattern evidence. |
| 2.7.5, 2.7.6 (DragonForce, SafePay) | Retained as PARTIALLY RELEVANT emerging groups with no confirmed FS targeting. Defensible as watchlist items. Could be cut without weakening the base. |

All PARTIALLY RELEVANT claims are labeled as such and would not be presented as primary evidence in derivatives.

**Status: PASS**

---

### 7. Are all assumptions explicit?

**YES — 5 assumptions documented in Section 5 of the research base.**

| Assumption ID | Description |
|---|---|
| ASMP-01 | Hartwell's technology stack matches collection plan (Fortinet, Palo Alto, Veeam, GoAnywhere, CrowdStrike Falcon, etc.) |
| ASMP-02 | Hartwell's risk profile is comparable to targeted wealth management firms |
| ASMP-03 | Hartwell's EDR is CrowdStrike Falcon (Reynolds ransomware directly relevant) |
| ASMP-04 | Hartwell's edge devices may be vulnerable; patch levels unconfirmed |
| ASMP-05 | Qilin's self-reported affiliate split (80–85%) is unverifiable |

**Additional implicit assumptions noted:** Several ASSESSMENT claims about affiliate migration assume timing correlation equals causation. This is reasonable analytical inference but acknowledged.

**Status: PASS**

---

## Structural Gate Summary

| # | Question | Status | Action |
|---|---|---|---|
| 1 | Answers the requirement? | ✅ PASS | PIR-01.2 scoped to CTI lane; detection translation is downstream |
| 2 | Key judgments separated? | ✅ PASS | Addressed in Phase 9 |
| 3 | Competing hypotheses? | ✅ PASS | Three hypotheses documented and accepted |
| 4 | Sources diverse? | ⚠️ FLAGGED | Single intermediary; documented as GAP-R01; accepted for exercise |
| 5 | Gaps documented? | ✅ PASS | 8 gaps across two categories |
| 6 | Anything indefensible? | ✅ PASS | No indefensible claims |
| 7 | Assumptions explicit? | ✅ PASS | 5 assumptions documented |

**Overall: PASS with one acknowledged structural weakness (source diversity).**

**The research base is cleared for key judgment drafting (Phase 9) and final compilation (Phase 10).**
