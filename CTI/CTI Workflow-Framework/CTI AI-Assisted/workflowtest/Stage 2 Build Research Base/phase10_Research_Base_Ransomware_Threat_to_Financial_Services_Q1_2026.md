# Research Base — Ransomware Threat to Financial Services (Q1 2026)
## IR-01 / PIR-01.1, PIR-01.2, PIR-01.3

---

**Intelligence Requirement:** IR-01 — What ransomware groups are actively targeting the financial services sector, and what are their current tactics, techniques, and procedures?

**Priority Intelligence Requirements Served:**
- PIR-01.1: Which ransomware groups have conducted confirmed intrusions against financial services firms in the past 90 days, and what initial access methods did they use?
- PIR-01.2: What specific tools, techniques, and procedures — at the procedure level — are these groups using in current campaigns, including evasion techniques targeting EDR platforms?
- PIR-01.3: What is the current ransom demand range, payment rate, and double-extortion model for groups actively targeting financial services?

**Reporting Period:** Past 90 days (mid-December 2025 – mid-March 2026); extended to full 2025 where 90-day window returns insufficient data per collection plan guidance.

**Date Compiled:** March 15, 2026
**Analyst:** Junior Analyst 1
**Reviewed by:** [Pending — Dana Mercer, Senior Analyst]
**Version:** 1.0 — Initial build from AI-synthesized source material
**Status:** DRAFT — Pending primary source verification

**Classification:** INTERNAL — CTI TEAM USE ONLY. This is the source layer research base. It is never sent to consumers as-is. Derivative products (executive briefs, detection briefs, IR briefs) are produced from this document using the derivative production workflow.

---

## SECTION 1: KEY JUDGMENTS

### Confidence Level Note

All key judgments carry LOW confidence. This reflects the single-source dependency (all claims flow through an AI-synthesized intermediary document without independent primary source verification), not the quality of the underlying evidence. Multiple judgments — particularly KJ-4 — reference findings corroborated by three or more named sources and would likely reach MODERATE confidence upon independent verification. The analyst acknowledges confidence ratings are conservative for this exercise and appropriate given the source limitation.

---

### KJ-1 — Primary Threat Groups (PIR-01.1)

**We assess with LOW confidence that Qilin, Akira, and Clop represent the most significant ransomware threats to financial services firms with Hartwell's profile in early 2026.**

Qilin leads in overall volume (946 victims, 69 confirmed FS targets) and demonstrated the ability to cascade through a single MSP to compromise 28 financial firms simultaneously (Korean Leaks campaign, September 2025). Akira has the most confirmed FS victim count from a single tracking source (34 per Flashpoint, April 2024–April 2025) and a documented attack pattern exploiting VPN infrastructure directly relevant to Hartwell's technology stack (SonicWall CVE-2024-40766 in the Marquis attack affecting 74+ banks). Clop's mass zero-day exploitation of shared platforms (Cleo file transfer, Oracle E-Business Suite) creates outsized supply-chain exposure for financial firms reliant on common technology vendors.

Medusa, Play, and DragonForce represent secondary but active threats. Medusa received a joint CISA/FBI/MS-ISAC advisory (AA25-071A) in March 2025 and has a confirmed Lazarus Group (North Korean) nexus. Play has remained consistently active among top five groups throughout 2025. DragonForce's cartel model has attracted Scattered Spider affiliates for social engineering campaigns against financial targets.

*Supporting Evidence:* Sections 2.2–2.7
*Confidence Upgrade Path:* Verify Flashpoint FS targeting data and CISA advisories independently.
*Caveat:* This judgment reflects confirmed targeting of the financial services sector broadly, not confirmed targeting of Hartwell specifically.

---

### KJ-2 — Supply Chain vs. Direct Entry Risk (PIR-01.1)

**We assess with LOW confidence that edge device and VPN exploitation is the primary direct-entry initial access vector, but supply-chain compromise through third-party vendors may represent greater organizational risk for a firm with Hartwell's branch footprint and vendor ecosystem.**

The majority of confirmed financial services incidents in this research base involved vendor compromise rather than direct targeting of the victim's perimeter:

- Marquis Software Solutions → 74+ banks via SonicWall compromise of vendor (Akira, August 2025)
- DBS Bank/Bank of China Singapore → via printing vendor Toppan Next Tech (April 2025)
- SitusAMC → JPMorgan Chase, Citigroup, Morgan Stanley via mortgage tech vendor (November 2025)
- Qilin/GJTec → 28 South Korean asset management firms via MSP compromise (September 2025)
- Betterment → 1.4 million customers via CRM vendor social engineering (January 2026)
- Western Alliance Bank → 21,899 customers via Clop's Cleo MFT exploitation

This pattern is consistent with industry data showing 41.4% of ransomware attacks start through third parties (SecurityScorecard). With 14,500 branch offices, Hartwell's vendor surface area is substantial.

*Supporting Evidence:* Sections 2.8–2.10
*Confidence Upgrade Path:* Verify SecurityScorecard data; coordinate with PIR-03 research (Dana Mercer).
*Caveat:* This judgment bridges PIR-01.1 and PIR-03 (supply chain risk, assigned to Dana Mercer). Coordination with Dana's research base is recommended to avoid duplication and ensure consistent treatment.

---

### KJ-3 — EDR Evasion as Critical TTP Shift (PIR-01.2)

**We assess with LOW confidence that BYOVD-based EDR evasion — specifically EDRKillShifter and its derivatives — represents the most significant procedural shift in the ransomware kill chain for 2025, with direct implications for Hartwell's CrowdStrike Falcon deployment.**

EDRKillShifter, originally developed by RansomHub, has been adopted by at least 8 groups including several targeting financial services: Medusa, Play, Qilin, DragonForce, and INC Ransom. ESET identified a threat actor ("QuadSwitcher") orchestrating cross-group sharing, suggesting active collaboration among typically closed RaaS operations.

Reynolds ransomware (February 2026) represents the next evolution: embedding a vulnerable driver directly in the ransomware payload — eliminating the staging step — and specifically terminating CrowdStrike Falcon, Cortex XDR, Sophos, and Symantec. This falls within the reporting window and directly threatens Hartwell's assumed EDR deployment.

Additionally, Akira demonstrated the ability to pivot to unmonitored IoT devices (a Linux-based webcam) after EDR quarantined the initial payload, encrypting the network from an agentless device. This confirms that groups are actively adapting when endpoint detection succeeds.

These findings collectively suggest that EDR alone is insufficient for ransomware defense. Defense-in-depth including network segmentation, identity-based detection, and non-traditional endpoint coverage is necessary.

*Supporting Evidence:* Section 2.15, Claim 2.3.6
*Confidence Upgrade Path:* Verify ESET reporting + Huntress/Vectra AI on Reynolds independently.
*Caveat:* Assumes Hartwell deploys CrowdStrike Falcon as primary EDR (ASMP-03). If incorrect, the direct organizational relevance of Reynolds ransomware changes, though the broader EDR evasion trend remains applicable.

---

### KJ-4 — Payment Model Structural Change (PIR-01.3)

**We assess with LOW confidence that the ransomware payment model is undergoing structural change: payment rates have collapsed to historic lows (20–28% across sectors) while demands against financial services firms remain the highest of any sector ($2.0M median), creating pressure for increasingly aggressive extortion tactics.**

Three independent named sources corroborate the payment decline trend:
- Chainalysis: 28% of victims paid in 2025 (record low)
- Coveware: Payment rates fell from 25% (Q4 2024) to ~20% by Q4 2025
- Coalition: 86% of businesses refused to pay in 2025

Groups are compensating with escalating pressure tactics: triple extortion including SWATting executives' homes and bribing employees; stealing cyber insurance policies to calibrate demands below policy limits; cold-calling victims' clients directly; and shifting from encryption-first to data-theft-first operations (encryption in only 49–50% of FS attacks, a six-year low).

The shift to data-theft-first extortion is particularly dangerous for firms holding sensitive client financial data — PII, account numbers, equity holdings, and trading histories carry premium value regardless of whether a ransom is paid.

*Supporting Evidence:* Sections 2.17–2.21
*Confidence Upgrade Path:* Verify Chainalysis + Coveware data independently. This is the most corroborated finding in the base and the strongest candidate for MODERATE confidence.
*Caveat:* FS-specific payment and demand data relies on Sophos 2024 report — most recent available but outside the 90-day window. Cross-sector data is current.

---

### KJ-5 — Active Fortinet Threat (PIR-01.1, Time-Sensitive)

**We assess with LOW confidence that three Fortinet FortiGate vulnerabilities disclosed between December 2025 and January 2026, combined with observed pre-ransomware activity via FortiGate entry points as of March 2026, represent an active and current threat to Hartwell's perimeter.**

The specific vulnerabilities are:
- CVE-2025-59718/59719 (FortiCloud SSO bypass, CVSS 9.8): CISA KEV December 16, 2025. Active intrusions within three days. Huntress: 11 instances in 30 days.
- CVE-2026-24858 (Cross-account SSO bypass): CISA advisory January 28, 2026. ~10,000 instances affected.
- SentinelOne: Pre-ransomware activity via FortiGate entry points observed as of March 2026.

Fortinet has accumulated 14 zero-day advisories in under four years. These CVEs fall within the reporting window with confirmed active exploitation.

*Supporting Evidence:* Section 2.8, Claims 2.8.1–2.8.5
*Confidence Upgrade Path:* Verify CISA KEV entries directly — this is binary-verifiable and the fastest confidence upgrade available.
*Caveat:* Assumes Hartwell deploys FortiGate (ASMP-01) and devices may not be fully patched (ASMP-04). Verification with Vulnerability Management should not wait for the next quarterly cycle.

---

### Key Judgment Summary

| KJ | PIR | Core Assessment | Confidence | Fastest Upgrade |
|---|---|---|---|---|
| KJ-1 | 01.1 | Qilin, Akira, Clop are top FS threats | LOW | Verify Flashpoint + CISA advisories |
| KJ-2 | 01.1 | Supply chain may exceed direct entry as org risk | LOW | Verify SecurityScorecard; coordinate PIR-03 |
| KJ-3 | 01.2 | BYOVD/EDRKillShifter is critical TTP shift; Falcon targeted | LOW | Verify ESET + Huntress/Vectra on Reynolds |
| KJ-4 | 01.3 | Payment model structural change; aggressive tactics compensating | LOW → MOD | Verify Chainalysis + Coveware |
| KJ-5 | 01.1 | Three Fortinet CVEs (Dec 2025–Jan 2026) active current threat | LOW | Verify CISA KEV (fastest) |

---

## SECTION 2: SUPPORTING EVIDENCE

### 2.1 — Ransomware Ecosystem: Scale and Fragmentation (Context for PIR-01.1)

**[2.1.1]** 126–141 active ransomware groups operated in 2025, up from approximately 70 in 2023.
Source: Emsisoft, "State of Ransomware in the U.S. 2025"; Picus Security, "Top 10 Ransomware Groups of 2025"
Current as of: 2025 full-year data | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Type: FACT

**[2.1.2]** The financial sector recorded 451 ransomware cases in 2025.
Source: Check Point, "2025 Finance Sector Landscape Report"
Current as of: 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.1.3]** Extortion attacks increased 23% to 6,182 globally in 2025.
Source: Symantec/Broadcom Threat Hunter Team, "Ransomware 2026," January 2026
Current as of: January 2026 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Type: FACT

**[2.1.4]** 406 publicly disclosed financial sector ransomware victims from April 2024–April 2025, approximately 7% of all ransomware listings.
Source: Flashpoint, "Top Threat Actor Groups Targeting Financial Sector," 2025
Current as of: April 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.1.5a]** RansomHub, Black Basta, 8Base, BianLian, and Cactus all ceased operations between January and April 2025.
Source: Malwarebytes/ThreatDown, April 2025; Intel 471; ReliaQuest; Bitsight, 2025
Current as of: April 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.1.5b]** Displaced affiliates from defunct groups migrated to surviving and new operations, driving volume increases at receiving groups.
Source: Malwarebytes/ThreatDown; Intel 471; ReliaQuest; Bitsight
Current as of: April 2025 | Relevance: PIR-01.1 (RELEVANT) | Confidence: LOW | Type: ASSESSMENT

**[2.1.6]** 57 new ransomware groups and 27 new extortion groups emerged in 2025.
Source: Cyble, "10 New Ransomware Groups of 2025"
Current as of: 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Type: FACT

---

### 2.2 — Qilin (PIR-01.1)

**[2.2.1]** Qilin had 946 victims by year-end 2025, including 69 confirmed finance-sector targets among 590 business attacks by October 2025.
Source: Comparitech via Industrial Cyber, October 2025; Picus Security, 2025
Current as of: October/December 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.2.2]** Qilin's September 2025 "Korean Leaks" campaign compromised MSP GJTec to breach 28 South Korean asset management firms, exfiltrating over 1 million files.
Source: The Hacker News, November 2025; Bitdefender; Korea JoongAng Daily, September 23, 2025
Current as of: September 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.2.3]** Bitdefender linked the Qilin Korean campaign to potential North Korean state-affiliated involvement via Moonstone Sleet.
Source: Bitdefender research
Current as of: Late 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Confidence: LOW | Type: ASSESSMENT

**[2.2.4]** Qilin absorbed affiliates from defunct RansomHub after RansomHub ceased operations April 2025, significantly increasing its attack volume.
Source: Malwarebytes/ThreatDown, April 2025; Bitsight, 2025
Current as of: April 2025 | Relevance: PIR-01.1 (RELEVANT) | Confidence: LOW | Type: ASSESSMENT

**[2.2.5]** Qilin stole 2.5 TB from Habib Bank AG Zurich.
Source: Breached.company, late 2025
Current as of: Late 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.2.6a]** Qilin's Rust-based payload targets Windows, Linux, and VMware ESXi.
Source: AI synthesis; no named primary source
Current as of: Uncertain | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Type: FACT

**[2.2.6b]** Qilin's RaaS model offers affiliates 80–85% of ransom proceeds.
Source: AI synthesis; no named primary source
Current as of: Uncertain | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Type: ASSUMPTION — Self-reported by criminal group. Verification would require affiliate debriefs/leaks.

---

### 2.3 — Akira (PIR-01.1)

**[2.3.1a]** Akira had approximately 717–740 leak site postings in 2025.
Source: Symantec/Broadcom, "Ransomware 2026"; Picus Security, 2025
Current as of: 2025/2026 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.3.1b]** Akira has an estimated $244 million in total extortion revenue since launch.
Source: Symantec/Broadcom, "Ransomware 2026"; Picus Security, 2025
Current as of: 2025/2026 | Relevance: PIR-01.1 (RELEVANT) | Confidence: LOW | Type: ASSESSMENT

**[2.3.2]** Akira's August 14, 2025, attack on Marquis Software Solutions (vendor to 700+ banks) compromised over 400,000 consumers across 74+ institutions via CVE-2024-40766 (SonicWall VPN).
Source: American Banker, "Seven Largest Banking Data Breaches of 2025"
Current as of: August 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.3.3]** Flashpoint attributed 34 financial sector victims to Akira from April 2024 to April 2025.
Source: Flashpoint, "Top Threat Actor Groups Targeting Financial Sector," 2025
Current as of: April 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.3.4]** A joint CISA/FBI advisory (updated November 2025) confirmed Akira's continued targeting of financial institutions.
Source: CISA/FBI advisory, November 2025
Current as of: November 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.3.5]** Akira exploits VPN infrastructure without MFA — particularly Cisco and SonicWall appliances.
Source: CISA/FBI advisory (implied); Sophos X-Ops
Current as of: November 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.3.6]** In March 2025, Akira bypassed EDR by encrypting a network from an unsecured IoT webcam after EDR quarantined the initial payload.
Source: Vectra AI
Current as of: March 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT); also PIR-01.2 | Type: FACT

---

### 2.4 — Clop (PIR-01.1)

**[2.4.1]** Clop added 500+ victims in 2025 through campaigns against Cleo file transfer products (CVE-2024-50623/CVE-2024-55956, December 2024 onward) and Oracle E-Business Suite (CVE-2025-61882, July–November 2025).
Source: SOCRadar, "Top 10 CVEs of 2025"; Google Cloud Blog, October 2025; BankInfoSecurity, October 7, 2025
Current as of: November 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.4.2]** Clop's Cleo campaign included Western Alliance Bank (21,899 customers, SSNs stolen).
Source: SOCRadar, "Top 10 CVEs of 2025"
Current as of: 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.4.3]** Clop demanded up to $50 million from individual organizations in the Oracle EBS campaign.
Source: BlackFog, November 2025; Breached.company, "State of Ransomware 2026"
Current as of: November 2025 | Relevance: PIR-01.1 + PIR-01.3 (RELEVANT) | Type: FACT

**[2.4.4a]** Clop operates as a pure data-extortion group — no encryption.
Source: Observable operational pattern across Cleo and Oracle campaigns
Current as of: 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.4.4b]** Clop's supply-chain methodology creates outsized exposure for financial firms reliant on shared technology platforms.
Source: AI synthesis; analytical assertion
Current as of: 2025 | Relevance: PIR-01.1 (RELEVANT) | Confidence: LOW | Type: ASSESSMENT

---

### 2.5 — RansomHub (PIR-01.1 — Defunct, Affiliates Redistributed)

**[2.5.1]** RansomHub led all groups in financial sector targeting with 38 confirmed financial victims from April 2024–April 2025 before ceasing operations April 1, 2025.
Source: Flashpoint, 2025; Bitsight, 2025
Current as of: April 2025 (group defunct) | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.5.2]** DragonForce claimed RansomHub migrated to its infrastructure.
Source: Malwarebytes/ThreatDown, April 2025
Current as of: April 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Type: FACT

---

### 2.6 — Medusa (PIR-01.1)

**[2.6.1]** Medusa received joint CISA/FBI/MS-ISAC advisory AA25-071A (March 12, 2025) after exceeding 300 victims, with demands ranging from $100,000 to $15 million.
Source: CISA Advisory AA25-071A, March 12, 2025; Symantec, 2025
Current as of: March 2025 | Relevance: PIR-01.1 + PIR-01.3 (RELEVANT) | Type: FACT

**[2.6.2]** North Korean Lazarus Group actors were discovered deploying Medusa ransomware against Middle Eastern financial institutions.
Source: Symantec/Security.com
Current as of: 2025 | Relevance: PIR-01.1 (RELEVANT) | Confidence: LOW | Type: ASSESSMENT

---

### 2.7 — Other Active Groups (PIR-01.1)

**[2.7.1a]** Play has compromised approximately 900 entities since mid-2022.
Source: The Hacker News, June 2025
Current as of: June 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Type: FACT

**[2.7.1b]** Play remained consistently active throughout 2025 among top five groups.
Source: The Hacker News, June 2025
Current as of: June 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Confidence: LOW | Type: ASSESSMENT

**[2.7.2]** LockBit attempted recovery with LockBit 4.0 (February 2025) and 5.0 (September 2025) but suffered a second infrastructure breach in May 2025 exposing affiliate details.
Source: Acronis TRU; Wikipedia
Current as of: September 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.7.3]** Black Basta collapsed in January 2025, with 200,000 internal messages leaked on February 11, 2025.
Source: Intel 471; ReliaQuest
Current as of: February 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.7.4]** Former Black Basta members migrated to Cactus and SafePay groups.
Source: AI synthesis; implied by Intel 471/ReliaQuest
Current as of: 2025 | Relevance: PIR-01.1 (RELEVANT) | Confidence: LOW | Type: ASSESSMENT

**[2.7.5]** DragonForce introduced a "cartel model" in April 2025 allowing affiliates to operate under their own branding, claiming 200+ victims.
Source: Symantec, 2026; SOCRadar
Current as of: 2025/2026 | Relevance: PIR-01.1 (PARTIALLY RELEVANT — no confirmed FS targeting) | Type: FACT

**[2.7.6]** SafePay surged to 58 claimed victims in May 2025.
Source: Cyble, May 2025
Current as of: May 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT — no confirmed FS targeting) | Type: FACT

**[2.7.7]** Hunters International rebranded as World Leaks (data-theft-only), targeting a third-party supplier of UBS in June 2025 and publishing data on 130,000 UBS employees.
Source: Infosecurity Magazine, July 2025; Group-IB, April 2025
Current as of: July 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

---

### 2.8 — CVEs Actively Exploited Against Financial Services (PIR-01.1)

**[2.8.1]** Fortinet FortiGate has had 14 zero-day advisories in under 4 years.
Source: Coalition Insurance
Current as of: 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Type: FACT

**[2.8.2]** CVE-2024-55591 (FortiOS): CVSS 9.6, authentication bypass via Node.js websocket, ~48,000 internet-facing devices vulnerable. Exploited as zero-day since November 2024. CISA KEV January 14, 2025. Multiple ransomware groups actively exploiting.
Source: Shadowserver; Corvus Insurance advisory, February 2025; CISA KEV
Current as of: January 2025 | Relevance: PIR-01.1 (RELEVANT — Hartwell stack) | Type: FACT

**[2.8.3]** CVE-2025-59718/59719 (FortiCloud SSO bypass): CVSS 9.8, active intrusions within 3 days of disclosure. Huntress reported 11 instances in 30 days. CISA KEV December 16, 2025.
Source: Arctic Wolf; Huntress; The Hacker News, December 2025; Help Net Security, January 2026
Current as of: December 2025 — within reporting window | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.8.4]** CVE-2026-24858 (FortiGate cross-account SSO bypass): ~10,000 instances affected. CISA advisory January 28, 2026.
Source: CyberScoop, January 2026; CISA advisory, January 28, 2026; Shadowserver
Current as of: January 2026 — within reporting window | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.8.5]** SentinelOne documented campaigns using FortiGate as entry points with pre-ransomware activity observed as of March 2026.
Source: SentinelOne (referenced in synthesis)
Current as of: March 2026 — within reporting window | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.8.6]** CVE-2025-0108 (Palo Alto PAN-OS): CVSS 8.8, authentication bypass, confirmed exploitation from February 18, 2025. Chained with CVE-2024-9474 and CVE-2025-0111 for root-level access. CISA KEV February 2025.
Source: Palo Alto Networks advisory; CSO Online, February 2025
Current as of: February 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Type: FACT

**[2.8.7]** Chinese cyber-espionage group Emperor Dragonfly used Palo Alto exploits for RA World ransomware deployment.
Source: Symantec/Broadcom, February 2025
Current as of: February 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Confidence: LOW | Type: ASSESSMENT

**[2.8.8]** CVE-2024-40766 (SonicWall SSL VPN): Exploited by Akira; the vector in the Marquis Software Solutions attack affecting 74+ banks.
Source: American Banker; AI synthesis
Current as of: August 2025 | Relevance: PIR-01.1 (RELEVANT — Hartwell stack) | Type: FACT

**[2.8.9]** CVE-2024-40711 (Veeam Backup & Replication): CVSS 9.8, deserialization RCE, exploited by Akira, Fog, and Frag. Sophos X-Ops tracked 4+ incidents combining VPN + Veeam exploitation. CISA KEV October 17, 2024. Marked "Known" ransomware use.
Source: Sophos X-Ops, October 2024; Cybersecurity Dive; CISA KEV
Current as of: Ongoing exploitation | Relevance: PIR-01.1 (RELEVANT — Hartwell stack) | Type: FACT

**[2.8.10]** Rapid7 noted 20%+ of their 2024 IR cases involved Veeam exploitation.
Source: Rapid7, 2024
Current as of: 2024 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.8.11]** CVE-2025-23120 (Veeam): CVSS 9.9, allows any authenticated domain user to execute code when backup server is domain-joined. Disclosed March 2025.
Source: watchTowr; CSO Online, March 2025
Current as of: March 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT — no confirmed ransomware exploitation yet) | Type: FACT

**[2.8.12]** CVE-2025-10035 (GoAnywhere MFT): CVSS 10.0, command injection, exploited by Storm-1175 (Medusa affiliate) since at least September 11, 2025. CISA KEV.
Source: SOCRadar, "Top 10 CVEs of 2025"; Microsoft attribution
Current as of: September 2025 | Relevance: PIR-01.1 (RELEVANT — Hartwell stack) | Type: FACT

**[2.8.13]** CVE-2025-5777 (Citrix NetScaler, "CitrixBleed 2"): CVSS 9.3, 11.5 million exploitation attempts, 40% targeting financial services. One attacking IP linked to RansomHub by CISA. CISA KEV July 10, 2025.
Source: Imperva; Arctic Wolf; Cybersecurity Dive; CISA
Current as of: July 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.8.14]** CVE-2025-22224/22225/22226 (VMware ESXi): VM escape chain, CVSS up to 9.3. CISA confirmed CVE-2025-22225 "Known To Be Used in Ransomware Campaigns." February 2026 KEV update.
Source: CISA KEV, February 2026; Broadcom advisory VMSA-2025-0004
Current as of: February 2026 — within reporting window | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.8.15]** CVE-2025-29824 (Windows CLFS): Exploited by Storm-2460 targeting a Venezuelan financial entity; used by Play-linked Balloonfly group. CISA KEV April 2025.
Source: Microsoft Security Blog, April 8, 2025; Symantec/Security.com
Current as of: April 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Type: FACT

**[2.8.16]** CVE-2025-61882 (Oracle E-Business Suite): SSRF/XSL RCE exploited by Clop for mass financial data theft (July–November 2025).
Source: Google Cloud Blog, October 2025; BlackFog, November 2025
Current as of: November 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

---

### 2.9 — Credential-Based Initial Access Vectors (PIR-01.1 + PIR-01.2)

**[2.9.1]** Vulnerability exploitation accounts for 33% of initial access cases.
Source: Mandiant M-Trends 2025, Google Cloud Blog, April 2025
Current as of: April 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.9.2]** Compromised credentials account for 41% of root causes.
Source: Sophos, "2025 Active Adversary Report," April 2025
Current as of: April 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.9.3]** Edge/VPN device exploitation jumped from 3% to 22% of all exploitation cases between 2023 and 2024.
Source: Verizon DBIR 2025
Current as of: 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.9.4]** 90% of ransomware incidents exploited firewalls via CVE or vulnerable account; fastest observed chain completed breach-to-encryption in 3 hours and lateral movement in 10 minutes.
Source: Barracuda Managed XDR 2025 Threat Report, Help Net Security, February 2026
Current as of: February 2026 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.9.5]** MFA was absent in 59% of cases; 67.32% of root causes were identity-related.
Source: Sophos, "2026 Active Adversary Report" (covering Nov 2024–Oct 2025)
Current as of: 2025/2026 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.9.6]** 75% of initial access attempts are malware-free, relying on credentials and identity misuse.
Source: CrowdStrike, 2025 Global Threat Report
Current as of: 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.9.7]** ClickFix social engineering surged 517% in 2025, becoming the second most common attack vector behind traditional phishing.
Source: ESET H1 2025 Threat Report; Infosecurity Magazine, 2025
Current as of: H1 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.9.8]** Microsoft identified a May 2025 ClickFix campaign specifically targeting Portuguese financial services organizations with Lampion banking malware.
Source: Microsoft Security Blog, August 2025
Current as of: August 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.9.9]** Sophos documented a complete ClickFix → StealC → Qilin ransomware attack chain where stolen VPN credentials were sold by an IAB approximately one month later.
Source: Sophos, "I am not a robot" blog, 2025
Current as of: 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.9.10]** Nation-state actors including Iran's MuddyWater and Russia's APT28 adopted ClickFix.
Source: Logpoint; Proofpoint, 2025
Current as of: 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Confidence: LOW | Type: ASSESSMENT

---

### 2.10 — Confirmed Financial Sector Incidents (PIR-01.1)

**[2.10.1]** Marquis Software Solutions (August 2025): Akira compromised vendor serving 700+ banks via SonicWall CVE-2024-40766, exfiltrating data on 400,000+ consumers across 74+ institutions including SSNs and financial account data. Marquis paid ransom but data appeared on criminal marketplaces. Two-month notification delay triggered state AG filings.
Source: American Banker, "Seven Largest Banking Data Breaches of 2025"
Current as of: August 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.10.2]** DBS Bank/Bank of China Singapore (April 2025): Ransomware attack on printing vendor Toppan Next Tech exposed data on 8,200 DBS customers (mostly DBS Vickers brokerage users) and 3,000 BOC Singapore customers.
Source: AI synthesis; no named primary source
Current as of: April 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.10.3]** SitusAMC breach (November 2025): Affected JPMorgan Chase, Citigroup, and Morgan Stanley via mortgage technology vendor.
Source: CSO Online, November 2025; NYT/Bloomberg/CNN
Current as of: November 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.10.4]** Prosper Marketplace breach: 17.6 million customers — the largest single financial services breach of 2025 by record count.
Source: Centraleyes, October 2025
Current as of: October 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.10.5a]** Insight Partners ransomware attack ($90+ billion AUM PE firm).
Source: GBHackers, September 2025
Current as of: September 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.10.5b]** Insight Partners breach involved an 83-day dwell time.
Source: GBHackers, September 2025
Current as of: September 2025 | Relevance: PIR-01.1 (RELEVANT) | Confidence: LOW | Type: ASSESSMENT

**[2.10.6]** Betterment disclosed a breach in January 2026 exposing 1.4 million customers via a social engineering attack on a CRM vendor.
Source: AI synthesis; no named primary source
Current as of: January 2026 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

**[2.10.7]** Multiple wealth management firms appeared on ransomware leak sites in 2025: Tufton Capital Management ($810M AUM), FAS Wealth Partners, Hudson Executive Capital LP, Duff Capital Investors.
Source: AI synthesis; no named primary source
Current as of: 2025 | Relevance: PIR-01.1 (PARTIALLY RELEVANT) | Type: FACT

**[2.10.8]** Western Alliance Bank: 21,899 customers had SSNs stolen via Clop's Cleo exploitation.
Source: SOCRadar, "Top 10 CVEs of 2025"
Current as of: 2025 | Relevance: PIR-01.1 (RELEVANT) | Type: FACT

---

### 2.11 — Command and Control (PIR-01.2)

**[2.11.1]** Cobalt Strike remains the most frequently observed C2 framework, supplemented by Sliver (DEV-0237/FIN12, APT29), Brute Ratel C4 ($2,500/license cracked versions), and Havoc with Microsoft Graph API integration.
Source: Microsoft/GCHQ; BleepingComputer/AdvIntel; AlphaHunt, 2025–2026
Current as of: 2025–2026 | Relevance: PIR-01.2 (RELEVANT) | Confidence: LOW | Type: ASSESSMENT

**[2.11.2]** Emerging C2: GC2 (Google Sheets C2, observed in Fog ransomware) and Adaptix.
Source: Picus Security, 2025; AI synthesis
Current as of: 2025 | Relevance: PIR-01.2 (PARTIALLY RELEVANT) | Type: FACT + ASSESSMENT

---

### 2.12 — Remote Management Tool Abuse (PIR-01.2)

**[2.12.1]** RMM tool abuse appeared in 36% of incident response cases, with 32 different tools documented.
Source: Arctic Wolf 2025 Threat Report
Current as of: 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.12.2]** UNC5952 used signed malicious ConnectWise ScreenConnect droppers targeting global financial organizations.
Source: CyberProof, May 2025
Current as of: May 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.12.3]** AnyDesk featured in ransomware activity by Mad Liberator, Medusa, Rhysida, and Cactus.
Source: Intel 471, 2025
Current as of: 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.12.4]** Black Basta's 197,000 leaked chat messages confirmed systematic RMM abuse.
Source: Intel 471, February 2025
Current as of: February 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.12.5]** Akira installed Datto RMM on domain controllers to blend into routine IT automation.
Source: Barracuda, 2025
Current as of: 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

---

### 2.13 — Credential Harvesting and Lateral Movement (PIR-01.2)

**[2.13.1]** Mimikatz for LSASS dumping; sekurlsa::logonpasswords is the most-used module.
Source: Red Canary
Current as of: Uncertain | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.13.2]** Rubeus for Kerberoasting documented in Akira's attack chain.
Source: Security Boulevard, November 2025
Current as of: November 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.13.3]** DCSync attacks for KRBTGT hash extraction enabling Golden Ticket creation.
Source: Qualys ETM Defense Guide, February 2026
Current as of: February 2026 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.13.4]** Median time from initial access to Active Directory compromise: 11 hours.
Source: Sophos, 2025 Active Adversary Report
Current as of: 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.13.5]** 62% of compromised AD servers ran out-of-support operating systems.
Source: Sophos, 2025 Active Adversary Report
Current as of: 2025 | Relevance: PIR-01.2 (PARTIALLY RELEVANT) | Type: FACT

**[2.13.6]** Qilin affiliates modify the WDigest registry key to force plaintext credential storage.
Source: AI synthesis; no named primary source
Current as of: Uncertain | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.13.7]** Akira dumps Veeam backup credentials via PowerShell.
Source: AI synthesis; no named primary source
Current as of: Uncertain | Relevance: PIR-01.2 (RELEVANT — Hartwell stack) | Type: FACT

**[2.13.8]** Lateral movement relies on RDP, PsExec/PAExec over SMB admin shares, WMI, and Impacket; primary target is VMware ESXi hypervisors.
Source: AI synthesis; composite TTP description
Current as of: Uncertain | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

---

### 2.14 — Exfiltration (PIR-01.2)

**[2.14.1]** Rclone present in 57% of ransomware incidents; used by LockBit, Black Basta, BlackSuit, Medusa; uploads to MEGA.io.
Source: ReliaQuest; Symantec/Broadcom; Infosecurity Magazine
Current as of: 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.14.2]** WinSCP second; cURL third; FileZilla by INC Ransom for FTP-based exfiltration.
Source: ReliaQuest
Current as of: 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.14.3]** Exfiltration occurs at a median of 72.98 hours after attack initiation.
Source: Sophos, 2025 Active Adversary Report
Current as of: 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.14.4]** 83% of ransomware binaries deployed outside business hours; 79% of exfiltration also off-hours.
Source: Sophos, 2025 Active Adversary Report
Current as of: 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.14.5]** 96% of ransomware attacks in 2025 involved data exfiltration.
Source: BlackFog Q3 2025, via Vectra AI
Current as of: Q3 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.14.6]** Cyberduck used by Qilin affiliates for multipart uploads to Backblaze.
Source: AI synthesis; no named primary source
Current as of: Uncertain | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

---

### 2.15 — BYOVD and EDR Evasion (PIR-01.2)

**[2.15.1]** Over 2,500 BYOVD driver variants used in a single campaign targeting the TrueSight driver.
Source: Vectra AI, 2025
Current as of: 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.15.2]** EDRKillShifter (RansomHub-developed) used by 8+ groups: RansomHub, Medusa, BianLian, Play, BlackSuit, Qilin, DragonForce, INC Ransom.
Source: ESET, March 2025; Arete; The Hacker News, March 2025
Current as of: March 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

**[2.15.3]** ESET identified "QuadSwitcher" orchestrating cross-group EDRKillShifter attacks; suggests active collaboration among typically closed RaaS operations.
Source: ESET, March 2025
Current as of: March 2025 | Relevance: PIR-01.2 (RELEVANT) | Confidence: LOW | Type: ASSESSMENT

**[2.15.4]** Reynolds ransomware (February 2026) embedded a vulnerable driver directly in its payload, terminating CrowdStrike Falcon, Cortex XDR, Sophos, and Symantec.
Source: Vectra AI; Huntress, February 2026
Current as of: February 2026 — within reporting window | Relevance: PIR-01.2 (RELEVANT — Hartwell stack) | Type: FACT

**[2.15.5]** Akira pivoted to an unmonitored Linux-based webcam on the same network after EDR quarantined the initial payload, encrypting from an agentless device.
Source: Vectra AI
Current as of: March 2025 | Relevance: PIR-01.2 (RELEVANT) | Type: FACT

---

### 2.16 — ATT&CK Summary (PIR-01.2)

**[2.16.1]** T1486 (Data Encrypted for Impact) declining — encryption in only 50% of attacks, six-year low.
Source: Sophos, "State of Ransomware 2025"
Current as of: 2025 | Relevance: PIR-01.2 + PIR-01.3 (RELEVANT) | Type: FACT

---

### 2.17 — Ransom Demand Ranges (PIR-01.3)

**[2.17.1]** Financial services: highest median ransom at $2.0 million.
Source: Sophos, "State of Ransomware in Financial Services 2024"
Current as of: 2024 report | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.17.2]** 51% of FS victims paid; 18% paid full demand; avg 75% of initial ask.
Source: Sophos, "State of Ransomware in Financial Services 2024"
Current as of: 2024 report | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.17.3]** Initial demands surged 47% year-over-year in 2025.
Source: Coalition 2026 Cyber Claims Report, March 2026
Current as of: March 2026 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.17.4]** Medusa demands: $100,000 to $15 million.
Source: CISA Advisory AA25-071A
Current as of: March 2025 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.17.5]** Clop demanded up to $50 million per org (Oracle EBS campaign).
Source: BlackFog, November 2025; Breached.company
Current as of: November 2025 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.17.6]** A financial services firm paid $25.66 million to BlackCat/ALPHV affiliates.
Source: Federal indictment, October 2025
Current as of: October 2025 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

---

### 2.18 — Payment Rates (PIR-01.3)

**[2.18.1]** 28% of victims paid in 2025 — record low.
Source: Chainalysis, "2026 Crypto Crime Report," February 2026
Current as of: February 2026 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.18.2]** Payment rates fell from 25% (Q4 2024) to ~20% by Q4 2025.
Source: Coveware Q4 2024/Q4 2025, via SOS Ransomware
Current as of: February 2026 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.18.3]** 86% of businesses refused to pay in 2025.
Source: Coalition 2026 Cyber Claims Report, March 2026
Current as of: March 2026 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.18.4]** Data-extortion-only payment rate: 19%.
Source: Coveware Q3 2025, via HIPAA Journal
Current as of: Q3 2025 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

---

### 2.19 — Revenue and Financial Flows (PIR-01.3)

**[2.19.1]** Total on-chain payments: ~$820 million in 2025, 8% decline from $892M in 2024.
Source: Chainalysis, "2026 Crypto Crime Report," February 2026
Current as of: February 2026 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.19.2]** Median on-chain payments jumped 368% to ~$59,556.
Source: Chainalysis, "2026 Crypto Crime Report," February 2026
Current as of: February 2026 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.19.3]** FinCEN: $2.1B+ reported 2022–2024; $365.6M from 432 FS incidents.
Source: FinCEN, "Financial Trend Analysis on Ransomware," December 2025
Current as of: December 2025 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.19.4]** 97% of FinCEN-reported payments in Bitcoin.
Source: FinCEN, December 2025
Current as of: December 2025 | Relevance: PIR-01.3 (PARTIALLY RELEVANT) | Type: FACT

**[2.19.5]** OFAC designations 2025: Zservers (Feb), AEZA Group (Jul), Grinex (Aug), Media Land LLC (Nov).
Source: U.S. Treasury Press Releases
Current as of: November 2025 | Relevance: PIR-01.3 (PARTIALLY RELEVANT) | Type: FACT

---

### 2.20 — Recovery Costs (PIR-01.3)

**[2.20.1]** Mean FS recovery cost: $2.58 million excluding ransom.
Source: Sophos, "State of Ransomware in Financial Services 2024"
Current as of: 2024 report | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.20.2]** IBM: FS breach cost $5.56 million per incident.
Source: IBM Cost of a Data Breach Report 2025, August 2025
Current as of: August 2025 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.20.3]** Backup recovery: $375,000 avg vs $3 million for payers — 8x differential.
Source: Invenio IT analysis, updated 2026
Current as of: 2026 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

---

### 2.21 — Extortion Model Evolution (PIR-01.3)

**[2.21.1]** Encryption in only 50% of attacks in 2025 — six-year low, down from 70% in 2024.
Source: Sophos, "State of Ransomware 2025"
Current as of: 2025 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.21.2]** FS lowest encryption rate: 49%, down from 81% in 2023.
Source: Sophos, "State of Ransomware in Financial Services 2024"
Current as of: 2024 report | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.21.3]** Clop and World Leaks skip encryption entirely; Qilin, Akira, Play favor double extortion.
Source: Observable operational patterns
Current as of: 2025 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.21.4]** Triple extortion: SWATting executives, bribing employees.
Source: Coveware Q3 2025, via SOS Ransomware; HIPAA Journal
Current as of: Q3 2025 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.21.5]** Attackers stealing cyber insurance policies to calibrate demands below policy limits.
Source: Resilience Midyear 2025 Cyber Risk Report, September 2025
Current as of: September 2025 | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

**[2.21.6]** Akira cold-calling employees and clients of victim companies as pressure tactic.
Source: AI synthesis; no named primary source
Current as of: Uncertain | Relevance: PIR-01.3 (RELEVANT) | Type: FACT

---

## SECTION 3: COMPETING HYPOTHESES

Three hypotheses were considered for the primary threat vector to a firm with Hartwell's profile:

### Hypothesis A: Direct Perimeter Compromise (Default)

The primary threat is direct compromise of Hartwell's perimeter via edge device/VPN exploitation.

**Supporting evidence:** 16 CVEs documented in Section 2.8 with active exploitation against financial services; 33% of initial access via vulnerability exploitation (Mandiant); 90% of ransomware incidents exploited firewalls (Barracuda); three Fortinet CVEs within reporting window with pre-ransomware activity confirmed (SentinelOne, March 2026).

**Weakening evidence:** Majority of confirmed FS incidents in Section 2.10 involved vendor compromise, not direct targeting of the victim's perimeter.

### Hypothesis B: Supply Chain Compromise

The primary threat is supply-chain compromise through third-party vendors, not direct intrusion.

**Supporting evidence:** 6 of 8 confirmed FS incidents in Section 2.10 involved vendor compromise (Marquis, DBS/Toppan, SitusAMC, Qilin/GJTec, Betterment, Western Alliance/Cleo). 41.4% of ransomware attacks start through third parties (SecurityScorecard). 14,500 branch offices create substantial vendor surface area.

**Weakening evidence:** Addresses exposure, not targeting intent. Supply chain risk may amplify Hypothesis A rather than replace it.

### Hypothesis C: Credential Pipeline

The primary threat is credential-based access via the infostealer-to-IAB-to-ransomware pipeline.

**Supporting evidence:** 41% of root causes are compromised credentials (Sophos); 75% of initial access malware-free (CrowdStrike); documented ClickFix → StealC → Qilin chain; MFA absent in 59% of cases.

**Weakening evidence:** Better addressed under PIR-04 (Analyst 3 / Dana Mercer). May be an enabler of Hypothesis A rather than a separate path.

### Analyst Assessment

These hypotheses are not mutually exclusive. All three vectors are active simultaneously, and sophisticated intrusions may chain multiple vectors. The key question for Hartwell is which vector represents the greatest *unmitigated* risk — which requires input from Vulnerability Management (patch state) and Security Operations (detection coverage) that CTI does not currently have.

---

## SECTION 4: COLLECTION GAPS

### Gaps Inherited from Collection Plan

| Gap ID | PIR Affected | Description | Impact | Status |
|---|---|---|---|---|
| GAP-003 | PIR-01.1, PIR-01.2 | CTI lacks version/patch data for Veeam and GoAnywhere MFT | Can identify exploited CVEs but cannot confirm organizational exposure | Open — requires coordination with IT ops/Vuln Mgmt |
| GAP-005 | PIR-01.2 | CTI does not produce detection-ready output; Detection Engineering researches independently | Consumer need unmet; addressed by derivative production workflow | Open — addressed by workflow implementation |
| GAP-006 | PIR-01.1, PIR-01.2 | No dedicated threat hunting capability; ad-hoc only via senior SOC analysts | Cannot validate whether identified TTPs are present in Hartwell's environment | Open — organizational capability gap |

### Gaps Identified During Research

| Gap ID | PIR Affected | Description | Impact | Status |
|---|---|---|---|---|
| GAP-R01 | All | No primary sources independently verified; all claims flow through single AI-synthesized intermediary | All confidence levels capped at LOW until primary sources processed directly | Open — highest priority for resolution |
| GAP-R02 | PIR-01.1 | Several confirmed FS incidents (DBS Bank, Betterment, wealth mgmt leak site listings) lack named primary sources | Incident claims plausible but unverifiable from current material | Open — requires primary source collection |
| GAP-R03 | PIR-01.2 | Several procedure-level TTP claims (Qilin WDigest, Akira Veeam PowerShell, Cyberduck/Backblaze) are undated and unsourced | Cannot confirm TTPs are current; may reflect historical tradecraft | Open — requires DFIR Report or vendor case studies |
| GAP-R04 | PIR-01.3 | Sector-specific ransom economics data relies on Sophos 2024 report — outside 90-day window | Most recent available; may not reflect Q4 2025/Q1 2026 conditions | Open — monitoring for Sophos 2025 FS report |
| GAP-R05 | PIR-01.1 | Several CVE numbers with high sequence values unverified against CISA KEV/NVD | Possible AI hallucination; CVE details may be fabricated | Open — verify against KEV catalog |

---

## SECTION 5: ASSUMPTIONS

| ID | Assumption | Verification Required | PIRs Affected | Status |
|---|---|---|---|---|
| ASMP-01 | Hartwell's technology stack includes Fortinet FortiGate, Cisco AnyConnect, Palo Alto Networks, Veeam Backup, GoAnywhere MFT, Microsoft Exchange Online, Entra ID, and CrowdStrike Falcon as stated in collection plan. | Verified asset inventory from IT/Infrastructure; confirmed by Vulnerability Management. | PIR-01.1, PIR-01.2 | Assumed true for exercise |
| ASMP-02 | Hartwell's risk profile (52,000 employees, 14,500 branches, $1.8T AUM) is comparable to targeted wealth management and financial services firms documented in this base. | Confirmation from CISO or risk management. | PIR-01.1 | Assumed true for exercise |
| ASMP-03 | Hartwell's primary EDR is CrowdStrike Falcon. Reynolds ransomware (claim 2.15.4) specifically terminates Falcon. | Confirmed EDR deployment from Security Operations. | PIR-01.2 | Assumed true for exercise |
| ASMP-04 | Hartwell's edge devices may be vulnerable to CVEs documented in Section 2.8. Patch levels unconfirmed. GAP-003 flags missing Veeam and GoAnywhere MFT version data. | Patch/version data from Vulnerability Management for all edge devices and backup infrastructure. | PIR-01.1, PIR-01.2 | Assumed true for exercise |
| ASMP-05 | Qilin's RaaS affiliate split is 80–85% (claim 2.2.6b). Self-reported by criminal organization. | Affiliate debriefs, law enforcement data, or corroboration from multiple leak/chat analyses. | PIR-01.1 | Assumed true for exercise |

---

## SECTION 6: SOURCE LIST

### Primary Source (Processed)

| # | Source | Date | Type | Notes |
|---|---|---|---|---|
| S-01 | AI-synthesized research document, commissioned by analyst | March 2026 | Secondary synthesis | Primary intermediary for all claims; moderate analyst trust |
| S-02 | AI-compiled source references file | March 2026 | Reference index | Maps claims to named primary sources; ~86% coverage |

### Named Primary Sources Referenced (Not Independently Verified)

| Category | Source | Claims Supported |
|---|---|---|
| Government | CISA Advisory AA25-071A (Medusa, March 2025) | 2.6.1, 2.17.4 |
| Government | CISA KEV Catalog (multiple CVE entries) | 2.8.2–2.8.16 |
| Government | FinCEN, "Financial Trend Analysis on Ransomware," December 2025 | 2.19.3, 2.19.4 |
| Government | U.S. Treasury/OFAC Press Releases, 2025 | 2.19.5 |
| Government | Federal indictment, October 2025 (BlackCat/ALPHV) | 2.17.6 |
| Vendor | Sophos, "State of Ransomware 2025" / "Active Adversary 2025/2026" / "Financial Services 2024" | 2.9.2, 2.9.5, 2.13.4–5, 2.14.3–4, 2.17.1–2, 2.20.1, 2.21.1–2 |
| Vendor | CrowdStrike, 2025 Global Threat Report | 2.9.6 |
| Vendor | ESET, H1 2025 Threat Report / March 2025 | 2.9.7, 2.15.2–3 |
| Vendor | Mandiant M-Trends 2025 | 2.9.1 |
| Vendor | Symantec/Broadcom, "Ransomware 2026" | 2.1.3, 2.3.1a, 2.6.2, 2.8.7 |
| Vendor | Vectra AI | 2.15.1, 2.15.4–5, 2.3.6 |
| Vendor | Arctic Wolf 2025 Threat Report | 2.12.1 |
| Vendor | Intel 471 | 2.12.3–4, 2.7.3 |
| Vendor | Flashpoint, "Top Threat Actor Groups Targeting FS," 2025 | 2.1.4, 2.3.3, 2.5.1 |
| Vendor | Check Point, "2025 Finance Sector Landscape Report" | 2.1.2 |
| Vendor | Barracuda Managed XDR 2025 | 2.9.4, 2.12.5 |
| Vendor | SentinelOne | 2.8.5 |
| Vendor | Microsoft Security Blog | 2.9.8 |
| Vendor | Picus Security, "Top 10 Ransomware Groups of 2025" | 2.1.1, 2.2.1 |
| Industry | Chainalysis, "2026 Crypto Crime Report," February 2026 | 2.18.1, 2.19.1–2 |
| Industry | Verizon DBIR 2025 | 2.9.3 |
| Industry | Coveware Q3/Q4 2025 | 2.18.2, 2.18.4, 2.21.4 |
| Industry | IBM Cost of a Data Breach Report 2025 | 2.20.2 |
| Insurance | Coalition 2026 Cyber Claims Report, March 2026 | 2.17.3, 2.18.3 |
| Insurance | Resilience Midyear 2025 Cyber Risk Report | 2.21.5 |
| Insurance | Corvus Insurance advisory, February 2025 | 2.8.2 |
| News/Trade | American Banker | 2.3.2, 2.10.1 |
| News/Trade | The Hacker News | 2.2.2, 2.7.1a |
| News/Trade | CSO Online | 2.10.3 |
| News/Trade | Korea JoongAng Daily | 2.2.2 |
| Dark Web/Leak | Breached.company | 2.2.5, 2.4.3 |
| Research | Cyble | 2.1.6, 2.7.6 |
| Research | Comparitech via Industrial Cyber | 2.2.1 |
| Research | SOCRadar | 2.4.2, 2.8.12, 2.10.8 |

---

## SECTION 7: VERSION HISTORY

| Version | Date | Author | Changes |
|---|---|---|---|
| 1.0 | March 15, 2026 | Junior Analyst 1 | Initial build from AI-synthesized source material. 118 claims across 3 PIRs. 5 key judgments drafted. All confidence LOW pending primary source verification. |

---

## SECTION 8: NEXT ACTIONS

| Priority | Action | Rationale |
|---|---|---|
| 1 | Verify CISA KEV entries for all CVEs in Section 2.8 | Binary-verifiable; fastest confidence upgrade path (KJ-5) |
| 2 | Process CISA Advisory AA25-071A (Medusa) as independent primary source | Government advisory; upgrades KJ-1 claims on Medusa |
| 3 | Process Chainalysis "2026 Crypto Crime Report" independently | Most corroborated finding (KJ-4); fastest path to MODERATE confidence |
| 4 | Coordinate with Dana Mercer on PIR-03 supply chain overlap | KJ-2 bridges PIR-01.1 and PIR-03; avoid duplication |
| 5 | Request patch/version data from Vulnerability Management for Fortinet, Veeam, GoAnywhere | Resolves ASMP-04 and GAP-003; determines if KJ-5 requires immediate action |
| 6 | Share Sections 4–5 of source synthesis (supply chain, infostealers) with Dana Mercer and Analyst 3 | Source material relevant to their PIR assignments |
| 7 | Flag KJ-5 (Fortinet) to Dana Mercer for potential escalation to CISO | Time-sensitive finding; should not wait for quarterly cycle |

---

*This document is the source layer — internal only, never sent to consumers as-is. Derivative products (executive briefs, detection briefs, IR briefs) are produced from this using the derivative production workflow (Prompt 3).*

*This document should be versioned and updated as new sources are processed.*
