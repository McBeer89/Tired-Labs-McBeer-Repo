# CTI Research Base: Ransomware Groups Targeting Financial Services
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
**Version:** 1.0 — Initial build from AI-synthesized source material
**Status:** DRAFT — Pending primary source verification

---

## SECTION 1: KEY JUDGMENTS

*[PLACEHOLDER — To be developed in Phase 9 after all sources are processed and structural gate is applied. Key judgments will be drafted based on the evidence below and reviewed by the analyst.]*

---

## SECTION 2: SUPPORTING EVIDENCE

### 2.1 — Ransomware Ecosystem: Scale and Fragmentation (Context for PIR-01.1)

**[2.1.1]** 126–141 active ransomware groups operated in 2025, up from approximately 70 in 2023.
Source: Emsisoft, "State of Ransomware in the U.S. 2025"; Picus Security, "Top 10 Ransomware Groups of 2025"
Current as of: 2025 full-year data
Relevance: PIR-01.1 (PARTIALLY RELEVANT — ecosystem scale context)
Confidence: N/A
Type: FACT

**[2.1.2]** The financial sector recorded 451 ransomware cases in 2025.
Source: Check Point, "2025 Finance Sector Landscape Report"
Current as of: 2025 full-year data
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.1.3]** Extortion attacks increased 23% to 6,182 globally in 2025.
Source: Symantec/Broadcom Threat Hunter Team, "Ransomware 2026," January 2026
Current as of: January 2026
Relevance: PIR-01.1 (PARTIALLY RELEVANT — global trend context)
Confidence: N/A
Type: FACT

**[2.1.4]** 406 publicly disclosed financial sector ransomware victims from April 2024–April 2025, approximately 7% of all ransomware listings.
Source: Flashpoint, "Top Threat Actor Groups Targeting Financial Sector," 2025
Current as of: April 2025 (date range specified)
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.1.5a]** RansomHub, Black Basta, 8Base, BianLian, and Cactus all ceased operations between January and April 2025.
Source: Malwarebytes/ThreatDown, April 2025; Intel 471; ReliaQuest; Bitsight, 2025
Current as of: April 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.1.5b]** Displaced affiliates from defunct groups migrated to surviving and new operations, driving volume increases at receiving groups.
Source: Malwarebytes/ThreatDown, April 2025; Intel 471; ReliaQuest; Bitsight, 2025
Current as of: April 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: LOW — Analytical inference from timing and volume correlation
Type: ASSESSMENT

**[2.1.6]** 57 new ransomware groups and 27 new extortion groups emerged in 2025.
Source: Cyble, "10 New Ransomware Groups of 2025"
Current as of: 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — ecosystem fragmentation context)
Confidence: N/A
Type: FACT

---

### 2.2 — Qilin (PIR-01.1: Confirmed FS Targeting + Initial Access)

**[2.2.1]** Qilin had 946 victims by year-end 2025, including 69 confirmed finance-sector targets among 590 business attacks by October 2025.
Source: Comparitech data via Industrial Cyber, October 2025; Picus Security, 2025
Current as of: October/December 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.2.2]** Qilin's September 2025 "Korean Leaks" campaign compromised MSP GJTec to breach 28 South Korean asset management firms, exfiltrating over 1 million files.
Source: The Hacker News, November 2025; Bitdefender research; Korea JoongAng Daily, September 23, 2025
Current as of: September 2025
Relevance: PIR-01.1 (RELEVANT — confirmed FS intrusion via supply chain/MSP)
Confidence: N/A
Type: FACT

**[2.2.3]** Bitdefender linked the Qilin Korean campaign to potential North Korean state-affiliated involvement via Moonstone Sleet.
Source: Bitdefender research (referenced in synthesis)
Current as of: Late 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — attribution context)
Confidence: LOW — Single-source attribution assessment
Type: ASSESSMENT

**[2.2.4]** Qilin absorbed affiliates from defunct RansomHub after RansomHub ceased operations April 2025, significantly increasing its attack volume.
Source: Malwarebytes/ThreatDown, April 2025; Bitsight, 2025
Current as of: April 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: LOW — Inferred from timing and volume correlation
Type: ASSESSMENT

**[2.2.5]** Qilin stole 2.5 TB from Habib Bank AG Zurich.
Source: Breached.company, late 2025
Current as of: Late 2025
Relevance: PIR-01.1 (RELEVANT — confirmed FS victim)
Confidence: N/A
Type: FACT

**[2.2.6a]** Qilin's Rust-based payload targets Windows, Linux, and VMware ESXi.
Source: AI synthesis; no named primary source
Current as of: Uncertain — undated capability claim
Relevance: PIR-01.1 (PARTIALLY RELEVANT — operational model context)
Confidence: N/A
Type: FACT

**[2.2.6b]** Qilin's RaaS model offers affiliates 80–85% of ransom proceeds.
Source: AI synthesis; no named primary source
Current as of: Uncertain — undated
Relevance: PIR-01.1 (PARTIALLY RELEVANT — operational model context)
Confidence: N/A
Type: ASSUMPTION — Self-reported by criminal group. Verification: Would require direct observation of affiliate agreements or corroboration from multiple affiliate debriefs/leaks.

---

### 2.3 — Akira (PIR-01.1: Confirmed FS Targeting + Initial Access)

**[2.3.1a]** Akira had approximately 717–740 leak site postings in 2025.
Source: Symantec/Broadcom, "Ransomware 2026," 2026; Picus Security, 2025
Current as of: 2025/2026
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.3.1b]** Akira has an estimated $244 million in total extortion revenue since launch.
Source: Symantec/Broadcom, "Ransomware 2026," 2026; Picus Security, 2025
Current as of: 2025/2026
Relevance: PIR-01.1 (RELEVANT)
Confidence: LOW — Revenue is an estimate based on blockchain analysis and victim reporting; true figure unknowable
Type: ASSESSMENT

**[2.3.2]** Akira's August 14, 2025, attack on Marquis Software Solutions (vendor to 700+ banks) compromised over 400,000 consumers across 74+ institutions via CVE-2024-40766 (SonicWall VPN).
Source: American Banker, "Seven Largest Banking Data Breaches of 2025"
Current as of: August 2025
Relevance: PIR-01.1 (RELEVANT — confirmed FS supply chain intrusion with named CVE)
Confidence: N/A
Type: FACT

**[2.3.3]** Flashpoint attributed 34 financial sector victims to Akira from April 2024 to April 2025.
Source: Flashpoint, "Top Threat Actor Groups Targeting Financial Sector," 2025
Current as of: April 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.3.4]** A joint CISA/FBI advisory (updated November 2025) confirmed Akira's continued targeting of financial institutions.
Source: CISA/FBI advisory, November 2025
Current as of: November 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.3.5]** Akira exploits VPN infrastructure without MFA — particularly Cisco and SonicWall appliances.
Source: CISA/FBI advisory (implied); Sophos X-Ops
Current as of: November 2025
Relevance: PIR-01.1 (RELEVANT — initial access method)
Confidence: N/A
Type: FACT

**[2.3.6]** In March 2025, Akira bypassed EDR by encrypting a network from an unsecured IoT webcam after EDR quarantined the initial payload.
Source: Vectra AI
Current as of: March 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — evasion during confirmed intrusion; also serves PIR-01.2)
Confidence: N/A
Type: FACT

---

### 2.4 — Clop (PIR-01.1: Confirmed FS Targeting + Initial Access)

**[2.4.1]** Clop added 500+ victims in 2025 through campaigns against Cleo file transfer products (CVE-2024-50623/CVE-2024-55956, December 2024 onward) and Oracle E-Business Suite (CVE-2025-61882, July–November 2025).
Source: SOCRadar, "Top 10 CVEs of 2025"; Google Cloud Blog, October 2025; BankInfoSecurity, October 7, 2025
Current as of: November 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.4.2]** Clop's Cleo campaign included Western Alliance Bank (21,899 customers, SSNs stolen).
Source: SOCRadar, "Top 10 CVEs of 2025"
Current as of: 2025
Relevance: PIR-01.1 (RELEVANT — confirmed FS victim)
Confidence: N/A
Type: FACT

**[2.4.3]** Clop demanded up to $50 million from individual organizations in the Oracle EBS campaign.
Source: BlackFog, November 2025; Breached.company, "State of Ransomware 2026"
Current as of: November 2025
Relevance: PIR-01.1 (RELEVANT); also PIR-01.3
Confidence: N/A
Type: FACT

**[2.4.4a]** Clop operates as a pure data-extortion group — no encryption.
Source: AI synthesis; supported by observable operational pattern across Cleo and Oracle campaigns
Current as of: 2025
Relevance: PIR-01.1 (RELEVANT — operational model)
Confidence: N/A
Type: FACT

**[2.4.4b]** Clop's supply-chain methodology creates outsized exposure for financial firms reliant on shared technology platforms.
Source: AI synthesis; analytical assertion
Current as of: 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: LOW — Analytical judgment about relative risk
Type: ASSESSMENT

---

### 2.5 — RansomHub (PIR-01.1: Confirmed FS Targeting — Now Defunct)

**[2.5.1]** RansomHub led all groups in financial sector targeting with 38 confirmed financial victims from April 2024–April 2025 before ceasing operations April 1, 2025.
Source: Flashpoint, 2025; Bitsight, 2025
Current as of: April 2025 (group defunct)
Relevance: PIR-01.1 (RELEVANT — highest FS victim count before shutdown; affiliates redistributed)
Confidence: N/A
Type: FACT

**[2.5.2]** DragonForce claimed RansomHub migrated to its infrastructure.
Source: Malwarebytes/ThreatDown, April 2025
Current as of: April 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — infrastructure migration context)
Confidence: N/A
Type: FACT (DragonForce made this claim; whether the claim is accurate is a separate question)

---

### 2.6 — Medusa (PIR-01.1: Confirmed FS Targeting)

**[2.6.1]** Medusa received joint CISA/FBI/MS-ISAC advisory AA25-071A (March 12, 2025) after exceeding 300 victims, with demands ranging from $100,000 to $15 million.
Source: CISA Advisory AA25-071A, March 12, 2025; Symantec, 2025
Current as of: March 2025
Relevance: PIR-01.1 (RELEVANT); also PIR-01.3
Confidence: N/A
Type: FACT

**[2.6.2]** North Korean Lazarus Group actors were discovered deploying Medusa ransomware against Middle Eastern financial institutions.
Source: Symantec/Security.com, "North Korean Lazarus Group Now Working With Medusa"
Current as of: 2025
Relevance: PIR-01.1 (RELEVANT — nation-state nexus with ransomware targeting FS)
Confidence: LOW — Single-source attribution assessment
Type: ASSESSMENT

---

### 2.7 — Other Active Groups (PIR-01.1)

**[2.7.1a]** Play has compromised approximately 900 entities since mid-2022.
Source: The Hacker News, June 2025
Current as of: June 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — active group, limited FS-specific confirmation)
Confidence: N/A
Type: FACT

**[2.7.1b]** Play remained consistently active throughout 2025 among top five groups.
Source: The Hacker News, June 2025
Current as of: June 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT)
Confidence: LOW — Ranking is an editorial/analytical judgment
Type: ASSESSMENT

**[2.7.2]** LockBit attempted recovery with LockBit 4.0 (February 2025) and 5.0 (September 2025) but suffered a second infrastructure breach in May 2025 exposing affiliate details.
Source: Acronis TRU; Wikipedia
Current as of: September 2025
Relevance: PIR-01.1 (RELEVANT — group status assessment)
Confidence: N/A
Type: FACT

**[2.7.3]** Black Basta collapsed in January 2025, with 200,000 internal messages leaked on February 11, 2025.
Source: Intel 471; ReliaQuest
Current as of: February 2025
Relevance: PIR-01.1 (RELEVANT — group cessation)
Confidence: N/A
Type: FACT

**[2.7.4]** Former Black Basta members migrated to Cactus and SafePay groups.
Source: AI synthesis; implied by Intel 471/ReliaQuest
Current as of: 2025
Relevance: PIR-01.1 (RELEVANT — affiliate redistribution)
Confidence: LOW — Inferred from affiliate tracking
Type: ASSESSMENT

**[2.7.5]** DragonForce introduced a "cartel model" in April 2025 allowing affiliates to operate under their own branding, claiming 200+ victims.
Source: Symantec, 2026; SOCRadar
Current as of: 2025/2026
Relevance: PIR-01.1 (PARTIALLY RELEVANT — emerging group, no confirmed FS targeting yet)
Confidence: N/A
Type: FACT

**[2.7.6]** SafePay surged to 58 claimed victims in May 2025.
Source: Cyble, May 2025
Current as of: May 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — emerging group, no confirmed FS targeting yet)
Confidence: N/A
Type: FACT

**[2.7.7]** Hunters International rebranded as World Leaks (data-theft-only), targeting a third-party supplier of UBS in June 2025 and publishing data on 130,000 UBS employees.
Source: Infosecurity Magazine, July 2025; Group-IB, April 2025
Current as of: July 2025
Relevance: PIR-01.1 (RELEVANT — confirmed FS targeting via supply chain)
Confidence: N/A
Type: FACT

---

### 2.8 — CVEs Actively Exploited Against Financial Services (PIR-01.1: Initial Access Methods)

**[2.8.1]** Fortinet FortiGate has had 14 zero-day advisories in under 4 years.
Source: Coalition Insurance
Current as of: 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — Fortinet risk context)
Confidence: N/A
Type: FACT

**[2.8.2]** CVE-2024-55591 (FortiOS): CVSS 9.6, authentication bypass via Node.js websocket, approximately 48,000 internet-facing devices vulnerable. Exploited as zero-day since November 2024. CISA KEV January 14, 2025. Multiple ransomware groups actively exploiting.
Source: Shadowserver; Corvus Insurance advisory, February 2025; CISA KEV
Current as of: January 2025
Relevance: PIR-01.1 (RELEVANT — active exploitation, Hartwell stack)
Confidence: N/A
Type: FACT

**[2.8.3]** CVE-2025-59718/59719 (FortiCloud SSO bypass): CVSS 9.8, active intrusions within 3 days of disclosure. Huntress reported 11 instances in 30 days. CISA KEV December 16, 2025.
Source: Arctic Wolf; Huntress; The Hacker News, December 2025; Help Net Security, January 2026
Current as of: December 2025 — within reporting window
Relevance: PIR-01.1 (RELEVANT — active exploitation, Hartwell stack, within reporting window)
Confidence: N/A
Type: FACT

**[2.8.4]** CVE-2026-24858 (FortiGate cross-account SSO bypass): approximately 10,000 instances affected. CISA advisory January 28, 2026.
Source: CyberScoop, January 2026; CISA advisory, January 28, 2026; Shadowserver
Current as of: January 2026 — within reporting window
Relevance: PIR-01.1 (RELEVANT — active exploitation, Hartwell stack, within reporting window)
Confidence: N/A
Type: FACT

**[2.8.5]** SentinelOne documented campaigns using FortiGate as entry points with pre-ransomware activity observed as of March 2026.
Source: SentinelOne (referenced in synthesis)
Current as of: March 2026 — within reporting window
Relevance: PIR-01.1 (RELEVANT — current pre-ransomware activity via Hartwell stack)
Confidence: N/A
Type: FACT

**[2.8.6]** CVE-2025-0108 (Palo Alto PAN-OS): CVSS 8.8, authentication bypass, confirmed exploitation from February 18, 2025. Chained with CVE-2024-9474 and CVE-2025-0111 for root-level access. CISA KEV February 2025.
Source: Palo Alto Networks advisory; CSO Online, February 2025
Current as of: February 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — confirmed exploitation, not explicitly FS-tied)
Confidence: N/A
Type: FACT

**[2.8.7]** Chinese cyber-espionage group Emperor Dragonfly used Palo Alto exploits for RA World ransomware deployment.
Source: Symantec/Broadcom, February 2025
Current as of: February 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — group-CVE mapping)
Confidence: LOW — Single-source attribution
Type: ASSESSMENT

**[2.8.8]** CVE-2024-40766 (SonicWall SSL VPN): Exploited by Akira; the vector in the Marquis Software Solutions attack affecting 74+ banks.
Source: American Banker; AI synthesis
Current as of: August 2025
Relevance: PIR-01.1 (RELEVANT — confirmed FS attack vector, Hartwell stack)
Confidence: N/A
Type: FACT

**[2.8.9]** CVE-2024-40711 (Veeam Backup & Replication): CVSS 9.8, deserialization RCE, exploited by Akira, Fog, and Frag ransomware variants. Sophos X-Ops tracked 4+ incidents combining VPN compromise + Veeam exploitation. CISA KEV October 17, 2024. Marked "Known" for ransomware use.
Source: Sophos X-Ops, October 2024; Cybersecurity Dive; CISA KEV
Current as of: October 2024 — ongoing exploitation
Relevance: PIR-01.1 (RELEVANT — active exploitation, Hartwell stack, confirmed ransomware use)
Confidence: N/A
Type: FACT

**[2.8.10]** Rapid7 noted 20%+ of their 2024 IR cases involved Veeam exploitation.
Source: Rapid7, 2024
Current as of: 2024
Relevance: PIR-01.1 (RELEVANT — prevalence of Veeam as attack vector)
Confidence: N/A
Type: FACT

**[2.8.11]** CVE-2025-23120 (Veeam): CVSS 9.9, allows any authenticated domain user to execute code when backup server is domain-joined. Disclosed March 2025.
Source: watchTowr; CSO Online, March 2025
Current as of: March 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — new Veeam vuln, no confirmed ransomware exploitation yet)
Confidence: N/A
Type: FACT

**[2.8.12]** CVE-2025-10035 (GoAnywhere MFT): CVSS 10.0, command injection, exploited as zero-day by Storm-1175 (Medusa affiliate) since at least September 11, 2025. CISA KEV.
Source: SOCRadar, "Top 10 CVEs of 2025"; Microsoft attribution
Current as of: September 2025
Relevance: PIR-01.1 (RELEVANT — active exploitation, Hartwell stack, confirmed ransomware use)
Confidence: N/A
Type: FACT

**[2.8.13]** CVE-2025-5777 (Citrix NetScaler, "CitrixBleed 2"): CVSS 9.3, 11.5 million exploitation attempts, 40% targeting financial services. One attacking IP linked to RansomHub by CISA. CISA KEV July 10, 2025.
Source: Imperva; Arctic Wolf; Cybersecurity Dive; CISA
Current as of: July 2025
Relevance: PIR-01.1 (RELEVANT — active exploitation with FS-specific targeting data)
Confidence: N/A
Type: FACT

**[2.8.14]** CVE-2025-22224/22225/22226 (VMware ESXi): VM escape chain, CVSS up to 9.3, exploited as zero-days since at least February 2024 by Chinese-speaking threat actors. CISA confirmed CVE-2025-22225 "Known To Be Used in Ransomware Campaigns." February 2026 KEV update.
Source: CISA KEV, February 2026; Broadcom advisory VMSA-2025-0004; Help Net Security; BleepingComputer
Current as of: February 2026 — within reporting window
Relevance: PIR-01.1 (RELEVANT — confirmed ransomware use, VMware is common in enterprise)
Confidence: N/A
Type: FACT

**[2.8.15]** CVE-2025-29824 (Windows CLFS): Exploited by Storm-2460 targeting a Venezuelan financial sector entity; also used by Play ransomware-linked Balloonfly group. CISA KEV April 2025.
Source: Microsoft Security Blog, April 8, 2025; Symantec/Security.com
Current as of: April 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — FS targeting, secondary group)
Confidence: N/A
Type: FACT

**[2.8.16]** CVE-2025-61882 (Oracle E-Business Suite): SSRF/XSL RCE exploited by Clop for mass financial data theft (July–November 2025).
Source: Google Cloud Blog, October 2025; BlackFog, November 2025
Current as of: November 2025
Relevance: PIR-01.1 (RELEVANT — Clop's primary 2025 campaign vector)
Confidence: N/A
Type: FACT

---

### 2.9 — Credential-Based Initial Access Vectors (PIR-01.1 + PIR-01.2 Cross-Reference)

**[2.9.1]** Vulnerability exploitation accounts for 33% of initial access cases.
Source: Mandiant M-Trends 2025, Google Cloud Blog, April 2025
Current as of: April 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.9.2]** Compromised credentials account for 41% of root causes.
Source: Sophos, "2025 Active Adversary Report," April 2025
Current as of: April 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.9.3]** Edge/VPN device exploitation jumped from 3% to 22% of all exploitation cases between 2023 and 2024.
Source: Verizon DBIR 2025
Current as of: 2025
Relevance: PIR-01.1 (RELEVANT — trend data on attack vector shift)
Confidence: N/A
Type: FACT

**[2.9.4]** 90% of ransomware incidents exploited firewalls via CVE or vulnerable account; fastest observed attack chain completed breach-to-encryption in 3 hours and lateral movement in 10 minutes.
Source: Barracuda Managed XDR 2025 Threat Report, Help Net Security, February 2026
Current as of: February 2026
Relevance: PIR-01.1 (RELEVANT — speed of exploitation)
Confidence: N/A
Type: FACT

**[2.9.5]** MFA was absent in 59% of cases; 67.32% of root causes were identity-related.
Source: Sophos, "2026 Active Adversary Report" (covering November 2024–October 2025)
Current as of: 2025/2026
Relevance: PIR-01.1 (RELEVANT — defensive gap enabling initial access)
Confidence: N/A
Type: FACT

**[2.9.6]** 75% of initial access attempts are malware-free, relying on credentials and identity misuse.
Source: CrowdStrike, 2025 Global Threat Report
Current as of: 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.9.7]** ClickFix social engineering surged 517% in 2025, becoming the second most common attack vector behind traditional phishing.
Source: ESET H1 2025 Threat Report; Infosecurity Magazine, 2025
Current as of: H1 2025
Relevance: PIR-01.1 (RELEVANT — emerging initial access technique)
Confidence: N/A
Type: FACT

**[2.9.8]** Microsoft identified a May 2025 ClickFix campaign specifically targeting Portuguese financial services organizations with Lampion banking malware.
Source: Microsoft Security Blog, August 2025
Current as of: August 2025
Relevance: PIR-01.1 (RELEVANT — FS-specific ClickFix targeting)
Confidence: N/A
Type: FACT

**[2.9.9]** Sophos documented a complete ClickFix → StealC → Qilin ransomware attack chain where stolen VPN credentials were sold by an IAB approximately one month later.
Source: Sophos, "I am not a robot" blog, 2025
Current as of: 2025
Relevance: PIR-01.1 (RELEVANT — documented infostealer-to-ransomware pipeline)
Confidence: N/A
Type: FACT

**[2.9.10]** Nation-state actors including Iran's MuddyWater and Russia's APT28 adopted ClickFix.
Source: Logpoint; Proofpoint, 2025
Current as of: 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — nation-state adoption context)
Confidence: LOW — Attribution of technique adoption to specific nation-state groups is analytical
Type: ASSESSMENT

---

### 2.10 — Confirmed Financial Sector Incidents (PIR-01.1)

**[2.10.1]** Marquis Software Solutions (August 2025): Akira compromised vendor serving 700+ banks via SonicWall CVE-2024-40766, exfiltrating data on 400,000+ consumers across 74+ institutions including SSNs and financial account data. Marquis paid ransom but data appeared on criminal marketplaces. Two-month notification delay triggered state AG filings.
Source: American Banker, "Seven Largest Banking Data Breaches of 2025"
Current as of: August 2025
Relevance: PIR-01.1 (RELEVANT — confirmed FS supply chain intrusion)
Confidence: N/A
Type: FACT

**[2.10.2]** DBS Bank/Bank of China Singapore (April 2025): Ransomware attack on printing vendor Toppan Next Tech exposed data on 8,200 DBS customers (mostly DBS Vickers brokerage users) and 3,000 BOC Singapore customers.
Source: AI synthesis; no named primary source in references file
Current as of: April 2025
Relevance: PIR-01.1 (RELEVANT — confirmed FS vendor attack, brokerage impact)
Confidence: N/A
Type: FACT

**[2.10.3]** SitusAMC breach (November 2025): Affected JPMorgan Chase, Citigroup, and Morgan Stanley via mortgage technology vendor.
Source: CSO Online, November 2025; NYT/Bloomberg/CNN (referenced in synthesis)
Current as of: November 2025
Relevance: PIR-01.1 (RELEVANT — major FS supply chain breach)
Confidence: N/A
Type: FACT

**[2.10.4]** Prosper Marketplace breach: 17.6 million customers — the largest single financial services breach of 2025 by record count.
Source: Centraleyes, October 2025
Current as of: October 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.10.5a]** Insight Partners ransomware attack ($90+ billion AUM PE firm).
Source: GBHackers, September 2025
Current as of: September 2025
Relevance: PIR-01.1 (RELEVANT — confirmed FS intrusion)
Confidence: N/A
Type: FACT

**[2.10.5b]** Insight Partners breach involved an 83-day dwell time.
Source: GBHackers, September 2025
Current as of: September 2025
Relevance: PIR-01.1 (RELEVANT)
Confidence: LOW — Dwell time is an analytical estimate from IR investigation
Type: ASSESSMENT

**[2.10.6]** Betterment disclosed a breach in January 2026 exposing 1.4 million customers via a social engineering attack on a CRM vendor.
Source: AI synthesis; no named primary source in references file
Current as of: January 2026 — within reporting window
Relevance: PIR-01.1 (RELEVANT — confirmed FS vendor attack)
Confidence: N/A
Type: FACT

**[2.10.7]** Multiple wealth management firms appeared on ransomware leak sites in 2025: Tufton Capital Management ($810M AUM), FAS Wealth Partners, Hudson Executive Capital LP, Duff Capital Investors.
Source: AI synthesis; no named primary source
Current as of: 2025
Relevance: PIR-01.1 (PARTIALLY RELEVANT — leak site appearances, limited detail)
Confidence: N/A
Type: FACT

**[2.10.8]** Western Alliance Bank: 21,899 customers had SSNs stolen via Clop's Cleo exploitation.
Source: SOCRadar, "Top 10 CVEs of 2025"
Current as of: 2025
Relevance: PIR-01.1 (RELEVANT — confirmed FS victim of named group/CVE)
Confidence: N/A
Type: FACT

---

### 2.11 — Command and Control (PIR-01.2)

**[2.11.1]** Cobalt Strike remains the most frequently observed C2 framework, supplemented by Sliver (used by DEV-0237/FIN12 and APT29), Brute Ratel C4 (cracked versions at $2,500/license), and Havoc with Demon agent supporting Microsoft Graph API integration for covert C2.
Source: Microsoft/GCHQ (Sliver); BleepingComputer/AdvIntel (Brute Ratel); AlphaHunt, 2025–2026 (Havoc)
Current as of: 2025–2026
Relevance: PIR-01.2 (RELEVANT)
Confidence: LOW — "Most frequently observed" and "supplemented by" are analytical rankings
Type: ASSESSMENT

**[2.11.2]** Emerging C2 tools include GC2 (abusing Google Sheets as C2, observed in Fog ransomware operations) and Adaptix.
Source: Picus Security, 2025 (Adaptix); AI synthesis (GC2/Fog)
Current as of: 2025
Relevance: PIR-01.2 (PARTIALLY RELEVANT — emerging tools, limited FS confirmation)
Confidence: N/A (GC2 observation) / N/A (Adaptix)
Type: FACT (tools exist and were observed) + ASSESSMENT ("emerging" characterization)

---

### 2.12 — Remote Management Tool Abuse (PIR-01.2)

**[2.12.1]** RMM tool abuse appeared in 36% of incident response cases, with 32 different RMM tools documented in malicious use.
Source: Arctic Wolf 2025 Threat Report, via eSecurity Planet
Current as of: 2025
Relevance: PIR-01.2 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.12.2]** UNC5952 used signed malicious ConnectWise ScreenConnect droppers targeting global financial organizations.
Source: CyberProof, May 2025
Current as of: May 2025
Relevance: PIR-01.2 (RELEVANT — FS-specific RMM abuse)
Confidence: N/A
Type: FACT

**[2.12.3]** AnyDesk featured in ransomware activity by Mad Liberator, Medusa, Rhysida, and Cactus.
Source: Intel 471, 2025
Current as of: 2025
Relevance: PIR-01.2 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.12.4]** Black Basta's 197,000 leaked chat messages confirmed systematic RMM abuse.
Source: Intel 471, February 2025
Current as of: February 2025
Relevance: PIR-01.2 (RELEVANT — procedural confirmation from primary source)
Confidence: N/A
Type: FACT

**[2.12.5]** Akira installed Datto RMM on domain controllers to blend into routine IT automation.
Source: Barracuda, 2025
Current as of: 2025
Relevance: PIR-01.2 (RELEVANT — specific procedure-level TTP)
Confidence: N/A
Type: FACT

---

### 2.13 — Credential Harvesting and Lateral Movement (PIR-01.2)

**[2.13.1]** Mimikatz for LSASS dumping; sekurlsa::logonpasswords is the most-used module.
Source: Red Canary (referenced in synthesis)
Current as of: Uncertain — no publication date
Relevance: PIR-01.2 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.13.2]** Rubeus for Kerberoasting documented in Akira's attack chain.
Source: Security Boulevard, November 2025
Current as of: November 2025
Relevance: PIR-01.2 (RELEVANT — group-specific procedure)
Confidence: N/A
Type: FACT

**[2.13.3]** DCSync attacks for KRBTGT hash extraction enabling Golden Ticket creation.
Source: Qualys ETM Defense Guide, February 2026
Current as of: February 2026
Relevance: PIR-01.2 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.13.4]** Median time from initial access to Active Directory compromise: 11 hours.
Source: Sophos, 2025 Active Adversary Report
Current as of: 2025
Relevance: PIR-01.2 (RELEVANT — operational tempo)
Confidence: N/A
Type: FACT

**[2.13.5]** 62% of compromised AD servers ran out-of-support operating systems.
Source: Sophos, 2025 Active Adversary Report
Current as of: 2025
Relevance: PIR-01.2 (PARTIALLY RELEVANT — victim environment condition, not attacker TTP)
Confidence: N/A
Type: FACT

**[2.13.6]** Qilin affiliates modify the WDigest registry key to force plaintext credential storage.
Source: AI synthesis; no named primary source
Current as of: Uncertain — undated
Relevance: PIR-01.2 (RELEVANT — specific procedure)
Confidence: N/A
Type: FACT

**[2.13.7]** Akira dumps Veeam backup credentials via PowerShell.
Source: AI synthesis; no named primary source
Current as of: Uncertain — undated
Relevance: PIR-01.2 (RELEVANT — specific procedure targeting Hartwell stack)
Confidence: N/A
Type: FACT

**[2.13.8]** Lateral movement relies on RDP (T1021.001), PsExec/PAExec over SMB admin shares (T1021.002), WMI (T1047), and Impacket for SMB/WMI abuse; primary target is VMware ESXi hypervisors.
Source: AI synthesis; composite TTP description supported by multiple vendor reports
Current as of: Uncertain — undated composite
Relevance: PIR-01.2 (RELEVANT)
Confidence: N/A
Type: FACT

---

### 2.14 — Exfiltration (PIR-01.2)

**[2.14.1]** Rclone is the dominant exfiltration tool, present in 57% of ransomware incidents, used by LockBit, Black Basta, BlackSuit, Medusa; typically uploading to MEGA.io accounts.
Source: ReliaQuest; Symantec/Broadcom; Infosecurity Magazine
Current as of: 2025
Relevance: PIR-01.2 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.14.2]** WinSCP ranks second for exfiltration, followed by cURL (native to Windows 10 1803+); FileZilla used by INC Ransom for FTP-based exfiltration.
Source: ReliaQuest (referenced in synthesis)
Current as of: 2025
Relevance: PIR-01.2 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.14.3]** Exfiltration occurs at a median of 72.98 hours after attack initiation.
Source: Sophos, 2025 Active Adversary Report
Current as of: 2025
Relevance: PIR-01.2 (RELEVANT — operational tempo)
Confidence: N/A
Type: FACT

**[2.14.4]** 83% of ransomware binaries deployed outside business hours; 79% of exfiltration also occurs off-hours.
Source: Sophos, 2025 Active Adversary Report
Current as of: 2025
Relevance: PIR-01.2 (RELEVANT — operational pattern)
Confidence: N/A
Type: FACT

**[2.14.5]** 96% of ransomware attacks in 2025 involved data exfiltration alongside encryption.
Source: BlackFog Q3 2025, via Vectra AI
Current as of: Q3 2025
Relevance: PIR-01.2 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.14.6]** Cyberduck used by Qilin affiliates for multipart uploads to Backblaze.
Source: AI synthesis; no named primary source
Current as of: Uncertain — undated
Relevance: PIR-01.2 (RELEVANT — group-specific exfiltration tool)
Confidence: N/A
Type: FACT

---

### 2.15 — BYOVD and EDR Evasion (PIR-01.2)

**[2.15.1]** Over 2,500 BYOVD driver variants used in a single campaign targeting the TrueSight driver.
Source: Vectra AI, 2025
Current as of: 2025
Relevance: PIR-01.2 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.15.2]** EDRKillShifter (developed by RansomHub) is now used by at least 8 distinct groups: RansomHub, Medusa, BianLian, Play, BlackSuit, Qilin, DragonForce, and INC Ransom.
Source: ESET, March 2025; Arete; The Hacker News, March 2025
Current as of: March 2025
Relevance: PIR-01.2 (RELEVANT — cross-group EDR evasion tool)
Confidence: N/A
Type: FACT

**[2.15.3]** ESET identified threat actor "QuadSwitcher" orchestrating cross-group EDRKillShifter attacks; cross-group sharing suggests active collaboration among typically closed RaaS operations.
Source: ESET, March 2025
Current as of: March 2025
Relevance: PIR-01.2 (RELEVANT)
Confidence: LOW — Actor identification and collaboration inference are analytical
Type: ASSESSMENT

**[2.15.4]** Reynolds ransomware (February 2026) embedded a vulnerable driver directly in its payload, terminating CrowdStrike Falcon, Cortex XDR, Sophos, and Symantec.
Source: Vectra AI; Huntress, February 2026
Current as of: February 2026 — within reporting window
Relevance: PIR-01.2 (RELEVANT — directly targets Hartwell's EDR per assumed stack)
Confidence: N/A
Type: FACT

**[2.15.5]** Akira pivoted to an unmonitored Linux-based webcam on the same network after EDR quarantined the initial payload, encrypting the network from an agentless device.
Source: Vectra AI
Current as of: March 2025
Relevance: PIR-01.2 (RELEVANT — EDR evasion via agentless device)
Confidence: N/A
Type: FACT

---

### 2.16 — ATT&CK Summary (PIR-01.2)

**[2.16.1]** T1486 (Data Encrypted for Impact) is declining — encryption occurred in only 50% of ransomware attacks in 2025, a six-year low.
Source: Sophos, "State of Ransomware 2025"
Current as of: 2025
Relevance: PIR-01.2 (RELEVANT — shift in operational objective); also PIR-01.3
Confidence: N/A
Type: FACT

---

### 2.17 — Ransom Demand Ranges (PIR-01.3)

**[2.17.1]** Financial services faces the highest median ransom payment of any sector at $2.0 million.
Source: Sophos, "State of Ransomware in Financial Services 2024"
Current as of: 2024 report — most recent sector-specific data available
Relevance: PIR-01.3 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.17.2]** 51% of financial services victims paid a ransom; only 18% paid the full initial demand; firms paid an average of 75% of the initial ask.
Source: Sophos, "State of Ransomware in Financial Services 2024"
Current as of: 2024 report
Relevance: PIR-01.3 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.17.3]** Initial ransom demands surged 47% year-over-year in 2025.
Source: Coalition 2026 Cyber Claims Report, March 2026
Current as of: March 2026 — within reporting window
Relevance: PIR-01.3 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.17.4]** Medusa demands range from $100,000 to $15 million.
Source: CISA Advisory AA25-071A, March 12, 2025
Current as of: March 2025
Relevance: PIR-01.3 (RELEVANT — group-specific demand range)
Confidence: N/A
Type: FACT

**[2.17.5]** Clop demanded up to $50 million from individual organizations in the Oracle EBS campaign.
Source: BlackFog, November 2025; Breached.company, "State of Ransomware 2026"
Current as of: November 2025
Relevance: PIR-01.3 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.17.6]** A financial services firm paid $25.66 million to BlackCat/ALPHV affiliates (October 2025 federal indictment).
Source: Federal indictment, October 2025
Current as of: October 2025
Relevance: PIR-01.3 (RELEVANT — upper bound of observed FS payments)
Confidence: N/A
Type: FACT

---

### 2.18 — Payment Rates (PIR-01.3)

**[2.18.1]** 28% of victims paid ransoms across all sectors in 2025 — a record low.
Source: Chainalysis, "2026 Crypto Crime Report," February 2026
Current as of: February 2026
Relevance: PIR-01.3 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.18.2]** Payment rates fell from 25% (Q4 2024) to approximately 20% by Q4 2025.
Source: Coveware Q4 2024/Q4 2025, via SOS Ransomware, February 2026
Current as of: February 2026
Relevance: PIR-01.3 (RELEVANT — quarterly trend)
Confidence: N/A
Type: FACT

**[2.18.3]** 86% of businesses refused to pay in 2025.
Source: Coalition 2026 Cyber Claims Report, March 2026
Current as of: March 2026 — within reporting window
Relevance: PIR-01.3 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.18.4]** Data-extortion-only attack payment rate dropped to 19% — victims increasingly doubt attackers will delete data.
Source: Coveware Q3 2025, via HIPAA Journal
Current as of: Q3 2025
Relevance: PIR-01.3 (RELEVANT — extortion model effectiveness)
Confidence: N/A
Type: FACT

---

### 2.19 — Revenue and Financial Flows (PIR-01.3)

**[2.19.1]** Total on-chain ransomware payments reached approximately $820 million in 2025, an 8% decline from 2024's revised $892 million.
Source: Chainalysis, "2026 Crypto Crime Report," February 2026
Current as of: February 2026
Relevance: PIR-01.3 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.19.2]** Median on-chain payments jumped 368% to approximately $59,556, reflecting concentration on higher-value victims.
Source: Chainalysis, "2026 Crypto Crime Report," February 2026
Current as of: February 2026
Relevance: PIR-01.3 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.19.3]** FinCEN documented over $2.1 billion in reported ransomware payments in BSA filings from 2022–2024; $365.6 million from 432 financial services incidents.
Source: FinCEN, "Financial Trend Analysis on Ransomware," December 2025
Current as of: December 2025
Relevance: PIR-01.3 (RELEVANT — FS-specific financial impact)
Confidence: N/A
Type: FACT

**[2.19.4]** 97% of FinCEN-reported ransomware payments are in Bitcoin.
Source: FinCEN, December 2025
Current as of: December 2025
Relevance: PIR-01.3 (PARTIALLY RELEVANT — payment rail context)
Confidence: N/A
Type: FACT

**[2.19.5]** OFAC designations in 2025: Zservers (February), AEZA Group (July), Garantex successor Grinex ($100M+ illicit transactions, August), Media Land LLC (November, supporting LockBit, BlackSuit, Play).
Source: U.S. Treasury Press Releases, 2025
Current as of: November 2025
Relevance: PIR-01.3 (PARTIALLY RELEVANT — OFAC designations affect payment decisions)
Confidence: N/A
Type: FACT

---

### 2.20 — Recovery Costs (PIR-01.3)

**[2.20.1]** Mean recovery cost for financial services: $2.58 million excluding ransom.
Source: Sophos, "State of Ransomware in Financial Services 2024"
Current as of: 2024 report
Relevance: PIR-01.3 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.20.2]** IBM placed the average financial services breach cost at $5.56 million per incident (second highest after healthcare at $7.42M).
Source: IBM Cost of a Data Breach Report 2025, August 2025
Current as of: August 2025
Relevance: PIR-01.3 (RELEVANT)
Confidence: N/A
Type: FACT

**[2.20.3]** Financial firms with functional backups recovered for an average of $375,000 versus $3 million for those who paid — an 8x differential.
Source: Invenio IT analysis, updated 2026
Current as of: 2026
Relevance: PIR-01.3 (RELEVANT — cost differential driving payment decisions)
Confidence: N/A
Type: FACT

---

### 2.21 — Extortion Model Evolution (PIR-01.3)

**[2.21.1]** Encryption occurred in only 50% of ransomware attacks in 2025 — a six-year low, down from 70% in 2024.
Source: Sophos, "State of Ransomware 2025"
Current as of: 2025
Relevance: PIR-01.3 (RELEVANT — shift in extortion model)
Confidence: N/A
Type: FACT

**[2.21.2]** Financial services has the lowest encryption rate of any sector at 49%, down from 81% in 2023.
Source: Sophos, "State of Ransomware in Financial Services 2024"
Current as of: 2024 report
Relevance: PIR-01.3 (RELEVANT — sector-specific trend)
Confidence: N/A
Type: FACT

**[2.21.3]** Clop and World Leaks (formerly Hunters International) skip encryption entirely; Qilin, Akira, and Play favor double extortion.
Source: AI synthesis; supported by observable operational patterns across incident data
Current as of: 2025
Relevance: PIR-01.3 (RELEVANT — group-specific extortion models)
Confidence: N/A
Type: FACT

**[2.21.4]** Triple extortion now includes SWATting executives' homes and attempting to bribe employees.
Source: Coveware Q3 2025, via SOS Ransomware; HIPAA Journal
Current as of: Q3 2025
Relevance: PIR-01.3 (RELEVANT — escalation of pressure tactics)
Confidence: N/A
Type: FACT

**[2.21.5]** Attackers are stealing organizations' cyber insurance policies to calibrate ransom demands just below policy payout limits.
Source: Resilience Midyear 2025 Cyber Risk Report, September 2025
Current as of: September 2025
Relevance: PIR-01.3 (RELEVANT — novel extortion tactic)
Confidence: N/A
Type: FACT

**[2.21.6]** Akira has begun cold-calling employees and clients of victim companies as a pressure tactic.
Source: AI synthesis; no named primary source
Current as of: Uncertain — undated
Relevance: PIR-01.3 (RELEVANT — group-specific pressure tactic)
Confidence: N/A
Type: FACT

---

## SECTION 3: COMPETING HYPOTHESES

*[PLACEHOLDER — To be developed in Phase 8 structural gate.]*

---

## SECTION 4: COLLECTION GAPS

### Gaps Inherited from Collection Plan

| Gap ID | PIR Affected | Description | Impact |
|---|---|---|---|
| GAP-003 | PIR-01.1, PIR-01.2 | CTI team lacks version/patch data for Veeam and GoAnywhere MFT | Can identify exploited CVEs (claims 2.8.9–2.8.12) but cannot confirm organizational exposure |
| GAP-005 | PIR-01.2 | CTI does not currently produce detection-ready output | Consumer need (Detection Engineering) unmet |
| GAP-006 | PIR-01.1, PIR-01.2 | No dedicated threat hunting capability | Cannot validate whether identified TTPs are present in Hartwell's environment |

### Gaps Identified During Research

| Gap ID | PIR Affected | Description | Impact |
|---|---|---|---|
| GAP-R01 | PIR-01.1 | No primary sources independently verified. All claims flow through a single AI-synthesized intermediary document. | All confidence levels capped at LOW until primary sources are processed directly. |
| GAP-R02 | PIR-01.1 | Several confirmed FS incidents (DBS Bank, Betterment, wealth management leak site listings) lack named primary sources. | Incident claims are plausible but unverifiable from current source material. |
| GAP-R03 | PIR-01.2 | Several procedure-level TTP claims (Qilin WDigest modification, Akira Veeam PowerShell dumping, Cyberduck/Backblaze exfiltration) are undated and unsourced. | Cannot confirm these TTPs are current; may reflect historical rather than active tradecraft. |
| GAP-R04 | PIR-01.3 | Sector-specific ransom economics data (median payment, payment rate, recovery cost) relies on Sophos 2024 report — outside the 90-day reporting window. | Most recent available, but may not reflect Q4 2025/Q1 2026 conditions. |
| GAP-R05 | PIR-01.1 | CVE numbers with high sequence values (CVE-2025-61882, CVE-2025-68947, CVE-2025-61155, CVE-2025-10035) have not been verified against CISA KEV or NVD. | Possible AI hallucination; CVE details may be fabricated. |

---

## SECTION 5: ASSUMPTIONS

**Note:** The following assumptions are being treated as true for the purposes of this exercise. In a production environment, each would require verification.

| Assumption ID | Assumption | What Would Verify It | PIRs Affected |
|---|---|---|---|
| ASMP-01 | Hartwell's technology stack includes Fortinet FortiGate, Cisco AnyConnect, Palo Alto Networks, Veeam Backup, GoAnywhere MFT, Microsoft Exchange Online, Entra ID, and CrowdStrike Falcon as stated in the collection plan. | Verified asset inventory from IT/Infrastructure team; confirmed by Vulnerability Management. | PIR-01.1, PIR-01.2 |
| ASMP-02 | Hartwell's risk profile is comparable to the wealth management and financial services firms being targeted by the groups documented in this research base (52,000 employees, 14,500 branches, $1.8T AUM). | Confirmation from CISO or risk management that Hartwell's profile matches the targeting criteria described in source material. | PIR-01.1 |
| ASMP-03 | Hartwell's detection capability relies on CrowdStrike Falcon as primary EDR. Reynolds ransomware (claim 2.15.4) specifically targets Falcon. If this assumption is incorrect, the direct organizational relevance of that claim changes. | Confirmed EDR deployment from Security Operations. | PIR-01.2 |
| ASMP-04 | Hartwell's edge devices (Fortinet, Palo Alto, SonicWall) may be vulnerable to the CVEs documented in Section 2.8. Patch levels have not been confirmed. GAP-003 already flags missing Veeam and GoAnywhere MFT version data. | Patch/version data from Vulnerability Management for all edge devices and backup infrastructure. | PIR-01.1, PIR-01.2 |
| ASMP-05 | Qilin's RaaS affiliate split is 80–85% (claim 2.2.6b). This is self-reported by a criminal organization and cannot be independently verified. | Would require affiliate debriefs, law enforcement data, or corroboration from multiple leak/chat analyses. | PIR-01.1 |

---

## SECTION 6: SOURCE LIST

| # | Source | Date | Type | Claims Supported |
|---|---|---|---|---|
| 1 | AI-synthesized research document (commissioned by analyst) | March 2026 | Secondary synthesis | All claims (primary intermediary) |
| 2 | AI-compiled source references file | March 2026 | Reference index | Source attributions for ~86% of claims |

### Named Primary Sources Referenced (Not Independently Verified)

| Source | Category | Claims Referencing |
|---|---|---|
| CISA Advisory AA25-071A (Medusa) | Government advisory | 2.6.1 |
| CISA KEV Catalog | Government database | 2.8.2–2.8.16 (multiple CVEs) |
| Sophos, "State of Ransomware 2025" / "2025 Active Adversary Report" / "Financial Services 2024" | Vendor report | 2.9.2, 2.9.5, 2.13.4, 2.13.5, 2.14.3, 2.14.4, 2.17.1, 2.17.2, 2.20.1, 2.21.1, 2.21.2 |
| Chainalysis, "2026 Crypto Crime Report" | Industry report | 2.18.1, 2.19.1, 2.19.2 |
| Flashpoint, "Top Threat Actor Groups Targeting Financial Sector" | Vendor report | 2.1.4, 2.3.3, 2.5.1 |
| Mandiant M-Trends 2025 | Vendor report | 2.9.1 |
| CrowdStrike, 2025 Global Threat Report | Vendor report | 2.9.6 |
| Verizon DBIR 2025 | Industry report | 2.9.3 |
| ESET, H1 2025 Threat Report / March 2025 | Vendor report | 2.9.7, 2.15.2, 2.15.3 |
| Coalition, 2026 Cyber Claims Report | Insurance report | 2.17.3, 2.18.3 |
| Coveware Q3/Q4 2025 | Industry report | 2.18.2, 2.18.4, 2.21.4 |
| FinCEN, December 2025 | Government report | 2.19.3, 2.19.4 |
| Symantec/Broadcom, "Ransomware 2026" | Vendor report | 2.1.3, 2.3.1a |
| Check Point, "2025 Finance Sector Landscape Report" | Vendor report | 2.1.2 |
| IBM, Cost of a Data Breach Report 2025 | Industry report | 2.20.2 |
| Barracuda Managed XDR 2025 | Vendor report | 2.9.4 |
| American Banker | News/trade publication | 2.3.2, 2.10.1 |
| Vectra AI | Vendor report | 2.15.1, 2.15.4, 2.15.5 |
| Arctic Wolf 2025 Threat Report | Vendor report | 2.12.1 |
| Intel 471 | Vendor report | 2.12.3, 2.12.4 |
| Resilience Midyear 2025 Cyber Risk Report | Insurance report | 2.21.5 |
| U.S. Treasury / OFAC | Government press releases | 2.19.5 |
| Microsoft Security Blog | Vendor blog | 2.9.8 |
| Picus Security, "Top 10 Ransomware Groups of 2025" | Vendor report | 2.1.1, 2.2.1 |
