# CTI Research Base: Ransomware Threat to Financial Services

**Research Base ID:** RB-2026-003  
**Topic:** Ransomware targeting financial services (wealth management / brokerage focus)  
**Reporting Period:** April 2025 – March 2026  
**Intelligence Requirement:** Which ransomware groups pose the most credible threat to a large retail brokerage and wealth management firm, what are their most likely attack vectors, and where are the critical exposure gaps?  
**Last Updated:** March 10, 2026  
**Analyst:** [Analyst Name]  
**Status:** Active — accepts ongoing contributions

---

## How to Use This Document

This is the team's lossless research base on this topic. **It is not a deliverable.** No one outside the CTI team should receive this document. It is the source layer from which audience-specific derivative products are produced.

Every claim is tagged with:
- **Source** — specific attribution
- **Confidence** — L (Low) / M (Moderate) / H (High)
- **Type** — FACT / ASSESSMENT / ASSUMPTION

Unresolved questions are tagged **[GAP]**. Competing hypotheses are explicitly documented.

---

## 1. Key Judgments

These are the analytical assessments derived from the research below. Each judgment has a stated confidence level and supporting basis.

**KJ-1: Qilin, Akira, and Medusa pose the most credible ransomware threat to firms with our profile in Q1 2026.**  
Confidence: **Moderate**  
Type: ASSESSMENT  
Basis: Qilin demonstrated financial sector focus via campaign against 23 South Korean financial firms (Check Point Q3 2025). Akira confirmed 34 financial sector victims in 12 months (CISA AA24-109A, Nov 2025). Medusa explicitly listed financial services in CISA advisory AA25-071A (March 2025) and confirmed by Darktrace as most-impacted sector in their customer base.  
Competing hypothesis: Clop's mass-exploitation model may pose equal or greater risk through supply-chain exposure, but Clop's targeting is platform-driven (MFT/ERP), not sector-driven — relevance depends on the organization's technology stack. **[GAP: Organization's MFT and ERP platforms not confirmed.]**

**KJ-2: Supply-chain compromise through a third-party vendor is the most likely attack scenario.**  
Confidence: **Moderate**  
Type: ASSESSMENT  
Basis: Three independent supply-chain incidents impacted financial services in 2025 (Marquis — 74+ banks via marketing vendor; DBS/Toppan — brokerage data via printing vendor; Betterment — 1.4M customers via CRM vendor). Flashpoint reports 6,400+ IAB posts offering financial sector access (Apr 2024–Apr 2025), many targeting vendor networks. Pattern is consistent across multiple independent sources.  
Competing hypothesis: Direct exploitation of the organization's own edge devices (VPN/firewall) is the primary vector in Akira's playbook specifically. If the organization runs unpatched SonicWall or Cisco appliances, this may be the more immediate risk. **[GAP: Organization's edge device inventory and patch status unknown.]**

**KJ-3: The BYOVD technique (EDRKillShifter) represents a likely detection gap for most financial services organizations.**  
Confidence: **Low-Moderate**  
Type: ASSESSMENT  
Basis: ESET reports EDRKillShifter shared across 8+ groups. Technique bypasses EDR solutions that don't monitor kernel driver loading. Reynolds ransomware (Feb 2026) embeds vulnerable driver directly in payload. However, assessment of organizational exposure depends on specific EDR product and configuration. **[GAP: Organization's EDR product, version, and driver-load monitoring capability unknown.]**

**KJ-4: Data theft has overtaken encryption as the primary extortion model for financial services targeting.**  
Confidence: **High**  
Type: ASSESSMENT  
Basis: BlackFog Q3 2025 reports exfiltration in 96% of ransomware attacks. Vectra AI confirms only 3% of exfiltration attempts blocked. Clop operates purely on data extortion (no encryption). Chainalysis reports data-extortion-only payment rate at 19% vs. 28% overall — lower payment rate but increasing adoption. Multiple independent sources confirm trend.

---

## 2. Threat Actor Profiles

### 2.1 Qilin (a.k.a. Agenda)

| Attribute | Detail | Source | Type |
|---|---|---|---|
| Status | Most prolific group globally, 1,000+ victims | Check Point Q3 2025 | FACT |
| Attack volume | ~75 attacks/month by Q3 2025 | Check Point Q3 2025 | FACT |
| Growth | 280% jump after absorbing RansomHub affiliates (Apr 2025) | Check Point Q3 2025, SOCRadar | FACT |
| Payload | Rust-based; targets Windows, Linux, VMware ESXi | Cyberint/Check Point, KELA Cyber | FACT |
| RaaS split | 80–85% to affiliates | SOCRadar, Cyberint | FACT |
| Financial targeting | 23 South Korean financial firms via shared IT contractor (Aug–Sep 2025) | Check Point Q3 2025 | FACT |
| Credential technique | Modifies WDigest registry key for plaintext credential storage | Darktrace, KELA Cyber | FACT |
| Exfiltration | Cyberduck for multipart uploads to Backblaze B2 | Darktrace | FACT |
| Attribution | Russian-speaking; does not target CIS countries | Multiple vendor reports | ASSESSMENT (M) |
| CIS country exclusion as attribution signal | Standard but not definitive — some non-Russian groups adopt the same policy for operational security | — | ASSUMPTION (documented) |

### 2.2 Akira

| Attribute | Detail | Source | Type |
|---|---|---|---|
| Status | ~740 victims in 2025; $244M total estimated revenue | CISA AA24-109A (Nov 2025), SOCRadar | FACT |
| Tracking names | PUNK SPIDER (CrowdStrike), Storm-1567 (Microsoft), Howling Scorpius (Palo Alto) | Multiple | FACT |
| Primary access vector | VPN without MFA — Cisco ASA/AnyConnect, SonicWall SSL VPN | CISA AA24-109A | FACT |
| Key CVEs | CVE-2024-40766 (SonicWall), CVE-2023-27532/CVE-2024-40711 (Veeam) | CISA AA24-109A | FACT |
| Financial sector victims | 34 confirmed between Apr 2024–Apr 2025 | CISA AA24-109A (Nov 2025) | FACT |
| Persistence technique | Creates local admin account "itadm" | CISA AA24-109A | FACT |
| EDR bypass | Encrypted network from unsecured IoT webcam (Mar 2025) | SOCRadar | FACT |
| Credential access | Kerberoasting (T1558.003); Veeam backup credential extraction via PowerShell | CISA AA24-109A | FACT |
| BYOVD driver | Intel rwdrv.sys | ESET | FACT |
| Pressure tactics | Cold-calling employees and clients of victim companies | SOCRadar | FACT |
| Conti connection | Code similarities, shared BTC wallets, overlapping infrastructure | Multiple vendor analyses | ASSESSMENT (M) |

### 2.3 Medusa

| Attribute | Detail | Source | Type |
|---|---|---|---|
| Status | Active since mid-2021; significant growth 2024–2025 | CISA AA25-071A | FACT |
| CISA advisory | AA25-071A (March 2025) — explicitly lists financial services as targeted sector | CISA/FBI/MS-ISAC | FACT |
| Sector impact | Financial services confirmed as most impacted in Darktrace customer base | Darktrace | FACT |
| RMM abuse | AnyDesk, ScreenConnect, MeshAgent for persistence | Darktrace | FACT |
| Extortion model | Triple extortion (encryption + data publication + client contact/DDoS) | CISA AA25-071A, SOCRadar | FACT |
| Key CVE | CVE-2025-10035 (Fortra GoAnywhere MFT, CVSS 10.0) from Sep 2025 | Multiple | FACT |
| Distinct from MedusaLocker | Separate operation despite name similarity | CISA AA25-071A, SOCRadar | FACT |

### 2.4 Clop

| Attribute | Detail | Source | Type |
|---|---|---|---|
| Model | Pure data extortion — no encryption payload | Multiple | FACT |
| 2025 campaigns | Cleo MFT (CVE-2024-50623/CVE-2024-55956) — ~400 victims; Oracle E-Business Suite (CVE-2025-61882) | Blackpoint, Cyber Security News | FACT |
| Association | FIN11/TA505 | Multiple vendor analyses | ASSESSMENT (M) |
| Relevance | Platform-driven not sector-driven — risk depends on org's tech stack | — | ASSESSMENT (M) |
| **[GAP]** | Organization's use of Cleo, GoAnywhere, Oracle EBS not confirmed | — | — |

### 2.5 Other Active Groups (Summary)

| Group | Key Detail | Financial Relevance | Source |
|---|---|---|---|
| Play | 28–33 victims/month; Lakeside Title Co. among victims | Title/settlement firms targeted | CISA updated advisory 2025 |
| INC Ransom | Explicitly targets orgs with "substantial financial resources" | Howard Financial Corp. claimed | MOXFIVE |
| LockBit 5.0 | Returned Sep 2025; 90 victims Jan 2026 | Diminished but credible | Check Point, Wikipedia/news |
| DragonForce | White-label "cartel" RaaS; adopted by Scattered Spider affiliates | HanseMerkur insurer attacked early 2026 | SOCRadar, Cyber Security News |

---

## 3. Initial Access Vectors

### 3.1 Edge Device Exploitation

| CVE | Product | CVSS | Exploited By | Source | Status |
|---|---|---|---|---|---|
| CVE-2024-55591 / CVE-2025-24472 | Fortinet FortiOS/FortiProxy | 9.8 | Mora_001 / LockBit | CISA KEV (Mar 2025) | FACT |
| CVE-2025-0282 / CVE-2025-22457 | Ivanti Connect Secure | 9.0 | UNC5221 / Multiple | Multiple | FACT |
| CVE-2025-5777 / -7775 / -6543 | Citrix NetScaler ("CitrixBleed 2") | 9.1–9.8 | Multiple | Multiple; 11.5M+ attack attempts | FACT |
| CVE-2024-40766 | SonicWall SSL VPN | 9.3 | Akira | CISA AA24-109A | FACT |
| CVE-2025-10035 | Fortra GoAnywhere MFT | 10.0 | Medusa | Multiple | FACT |
| CVE-2025-61882 | Oracle E-Business Suite | 9.8 | Clop | Cyber Security News | FACT |
| CVE-2023-27532 / CVE-2024-40711 | Veeam Backup | 7.5/9.8 | Akira | CISA AA24-109A | FACT |

**[GAP]:** Organization's edge device inventory (VPN vendor, firewall vendor, MFT platform) has not been confirmed. CVE relevance cannot be assessed without this information.

### 3.2 Credential Theft Pipeline

| Claim | Source | Type |
|---|---|---|
| Valid accounts (T1078) = 21% of ransomware initial access | Mandiant M-Trends 2025 | FACT |
| Top infostealers: Lumma (LummaC2), RedLine, Raccoon | Multiple | FACT |
| Average IAB price for corporate network access: $2,700; 71% include elevated privileges | Flashpoint | FACT |
| 6,406 dark web posts offering financial sector network access (Apr 2024–Apr 2025) | Flashpoint | FACT |
| AI-generated phishing = 83% of phishing traffic; 54% success rate vs. 12% traditional | KnowBe4 | FACT |
| ClickFix social engineering technique broadly adopted by ransomware actors H1 2025 | Multiple | FACT |

**[GAP]:** No visibility into whether organization credentials currently appear in infostealer logs or IAB marketplaces.

### 3.3 Supply-Chain Incidents (Financial Sector, 2025)

| Incident | Date | Vector | Impact | Source |
|---|---|---|---|---|
| Marquis Software Solutions | Aug 2025 | Likely CVE-2024-40766 (SonicWall) | 1.4M+ consumers across 74+ banks; SSNs, account data, card numbers | Bleeping Computer, TechCrunch, BankInfoSecurity |
| DBS/Toppan Next Tech | Apr 2025 | Ransomware on printing vendor | 8,200 DBS Vickers brokerage customers; names, addresses, equity holdings | SC Media |
| Betterment | Jan 2026 | Social engineering on CRM vendor | 1.4M customers | Multiple news sources |

**Pattern assessment:** Three independent incidents in 12 months, each via a different vendor category (marketing analytics, printing, CRM). **We assess with moderate confidence that supply-chain compromise through third-party vendors is the most likely attack pathway for financial services firms (see KJ-2).**

---

## 4. Post-Exploitation Kill Chain

### 4.1 Command & Control

| Tool | Role | Prevalence | Source |
|---|---|---|---|
| Cobalt Strike | Primary C2 framework | Dominant despite Operation Morpheus (-80% unauthorized copies) | Multiple |
| Sliver | Open-source C2 alternative (Go-based) | Growing adoption | Multiple |
| Brute Ratel C4 | EDR evasion-focused C2 | Used by advanced affiliates | Multiple |
| Havoc | Open-source C2 | Emerging | Multiple |
| AnyDesk, ScreenConnect, MeshAgent, Splashtop | RMM tools abused for persistence | 79% of Microsoft IR engagements (2025) | Microsoft |

### 4.2 Credential Access

| Tool/Technique | ATT&CK ID | Used By | Source |
|---|---|---|---|
| Mimikatz (Themida-packed) | T1003 | Universal | Multiple |
| DonPAPI | T1555 | Multiple groups | Multiple |
| NetExec | T1003, T1110 | Multiple groups | Multiple |
| LaZagne | T1555 | Multiple groups | Multiple |
| Kerberoasting | T1558.003 | Akira specifically | CISA AA24-109A |
| WDigest registry modification | T1112 | Qilin specifically | Darktrace, KELA |
| Veeam credential extraction (PowerShell) | T1003 | Akira specifically | CISA AA24-109A |

### 4.3 Lateral Movement

| Method | ATT&CK ID | Notes | Source |
|---|---|---|---|
| RDP | T1021.001 | Most common lateral movement protocol | Multiple |
| PsExec/PAExec over SMB admin shares | T1021.002 | Remote command execution | Multiple |
| WMI | T1047 | Remote process execution/enumeration | Multiple |
| Impacket | T1021.002, T1047 | Python library for SMB/WMI/Kerberos abuse | Multiple |

**Target:** VMware ESXi hypervisors — single encryption operation disables entire virtualized environment.

### 4.4 Defense Evasion — BYOVD

| Detail | Source | Type |
|---|---|---|
| EDRKillShifter shared across 8+ groups (Play, Medusa, BianLian, others) | ESET | FACT |
| ESET describes this as "EDRKillShifter-as-a-Service ecosystem" | ESET | FACT |
| Vulnerable drivers: Intel rwdrv.sys (Akira), NSecKrnl.sys/CVE-2025-68947 (Reynolds), BdApiUtil.sys/CVE-2024-51324 (DeadLock), GameDriverx64.sys/CVE-2025-61155 (Interlock) | ESET, Multiple | FACT |
| Reynolds (Feb 2026) embeds vulnerable driver directly in payload | Multiple | FACT |

**[GAP]:** Organization's EDR product and driver-load monitoring capability unknown. Cannot assess exposure without this.

### 4.5 Data Exfiltration

| Tool | Prevalence | Technique | Source |
|---|---|---|---|
| Rclone | 57% of incidents | Cloud sync (MEGA, S3, Backblaze); often renamed svchost.exe | Infosecurity Magazine |
| WinSCP | Common | SFTP to attacker servers | Infosecurity Magazine |
| MEGAsync | Common | Direct MEGA cloud upload | Multiple |
| AzCopy | Emerging | Azure Blob storage | Multiple |
| Cyberduck | Qilin-specific | Multipart uploads to Backblaze B2 | Darktrace |

Supporting data: Exfiltration in 96% of attacks (BlackFog Q3 2025). Only 3% of exfiltration attempts blocked (Vectra AI).

---

## 5. Financial Impact and Ransom Economics

| Metric | Value | Source | Type |
|---|---|---|---|
| Median ransom payment (financial services) | $2.0M | DeepStrike, Invenio IT | FACT |
| Mean ransom payment (financial services, among payers) | $3.3M | DeepStrike | FACT |
| Demands >$1M to financial firms | 58% | DeepStrike | FACT |
| Demands >$5M to financial firms | 38% | DeepStrike | FACT |
| Recovery cost (payers) | $3.0M average | Multiple | FACT |
| Recovery cost (backup restoration) | $375K average | Multiple | FACT |
| Cost differential | 8x | Derived from above | FACT |
| Overall payment rate (2025) | ~23% (Q3), ~28% (full year) | Check Point Q3 2025, Chainalysis | FACT |
| Payment rate for data-extortion-only | 19% | Chainalysis | FACT |
| Total ransomware revenue (2025) | ~$820–900M | Chainalysis | FACT |
| Insurance policy theft | Interlock steals cyber insurance policies to calibrate demands | Multiple | FACT |
| Payment method | 97% Bitcoin | FinCEN | FACT |

---

## 6. Regulatory Landscape

| Regulation | Requirement | Status | Source | Type |
|---|---|---|---|---|
| SEC 8-K disclosure | Material incident reporting within 4 business days | Active, but rescission petition filed May 2025 (BPI/ABA/SIFMA); future uncertain under SEC Chair Atkins | NetDiligence, Market Edge, SIFMA | FACT |
| OFAC sanctions | Strict liability for payments to sanctioned entities | Active; expanded designations in 2025 (Zservers, Media Land LLC, Garantex network) | Chainalysis, CoinDesk, Lewis Brisbois | FACT |
| CISA CIRCIA | Ransomware payment reporting within 24 hours | Expected finalized by Oct 2025 | Multiple | FACT |
| FINRA | Regulation S-P (safeguards), S-ID (identity theft), Rule 4370 (BCP) | Active | — | FACT |
| NYDFS 23 NYCRR 500 | Cybersecurity program mandates and incident notification | Active | — | FACT |

---

## 7. Collection Gaps

These are known gaps that limit the confidence of assessments in this research base. Each gap is tied to the judgment it affects.

| Gap | Affects | Priority |
|---|---|---|
| Organization's edge device inventory (VPN/firewall vendors, versions) | KJ-2, CVE relevance assessment | HIGH |
| Organization's MFT and ERP platforms | Clop exposure assessment (KJ-1 competing hypothesis) | HIGH |
| Organization's EDR product and driver-load monitoring config | KJ-3 (BYOVD gap assessment) | HIGH |
| Whether organization credentials appear in infostealer logs / IAB markets | KJ-2 (credential vector assessment) | HIGH |
| Organization's third-party vendor inventory and vendor security posture | KJ-2 (supply-chain exposure) | HIGH |
| Organization's cyber insurance policy details | Interlock insurance theft tactic relevance | MEDIUM |
| Organization's incident history (prior ransomware or related incidents) | Broader context | MEDIUM |
| Direct targeting intelligence (recon activity against org infrastructure) | All judgments | LOW (unlikely to obtain without internal telemetry) |

---

## 8. MITRE ATT&CK Reference Table

| Phase | Technique ID | Technique | Context | Used By |
|---|---|---|---|---|
| Initial Access | T1190 | Exploit Public-Facing Application | Edge devices: Fortinet, Ivanti, Citrix, SonicWall | Akira, Medusa, LockBit affiliates |
| Initial Access | T1078 | Valid Accounts | Infostealer credentials via IABs; 21% of initial access | All groups |
| Initial Access | T1566.001/.002 | Phishing | AI-generated; ClickFix social engineering | All groups |
| Execution | T1059.001 | PowerShell | UAC bypass, Defender disabling, credential extraction | All groups |
| Persistence | T1219 | Remote Access Software | AnyDesk, ScreenConnect, MeshAgent (79% of IR cases) | All groups, Medusa specifically |
| Persistence | T1136.002 | Create Domain Account | "itadm" account | Akira |
| Privilege Escalation | T1068 | Exploitation for Priv Esc | Veeam, SonicWall vulns | Akira |
| Privilege Escalation | T1558.003 | Kerberoasting | Service account credential extraction | Akira |
| Defense Evasion | T1562.001 | Disable Security Tools | BYOVD / EDRKillShifter | 8+ groups |
| Defense Evasion | T1055 | Process Injection | #1 most prevalent technique (Picus 2025) | Multiple |
| Credential Access | T1003 | OS Credential Dumping | Mimikatz, LSASS, DonPAPI | All groups |
| Lateral Movement | T1021.001/.002 | RDP / SMB Admin Shares | PsExec, Impacket | All groups |
| Collection | T1560 | Archive Collected Data | WinRAR, 7-Zip staging | All groups |
| Exfiltration | T1567 | Exfiltration to Cloud Storage | Rclone (57%), MEGA, S3, Backblaze | All groups, Qilin (Cyberduck) |
| Impact | T1486 | Data Encrypted for Impact | Declining — data theft now primary | Most groups |
| Impact | T1490 | Inhibit System Recovery | vssadmin shadow copy deletion | All groups |

---

## 9. Sources

| # | Source | Used For |
|---|---|---|
| 1 | CISA Advisory AA24-109A (Nov 2025) | Akira profile, CVEs, financial sector targeting |
| 2 | CISA Advisory AA25-071A (Mar 2025) | Medusa profile, financial services targeting |
| 3 | Check Point Research, Q3 2025 | Qilin profile, ecosystem fragmentation, attack volumes |
| 4 | Check Point Research, Q2 2025 | Supplementary volume/trend data |
| 5 | Mandiant / Google Cloud, M-Trends 2025 | Initial access statistics, credential theft pipeline |
| 6 | Flashpoint, "Top Threat Actor Groups Targeting Financial Sector" | IAB marketplace data, financial sector access posts |
| 7 | Chainalysis, Crypto Ransomware 2026 | Payment rates, revenue estimates, sanctions |
| 8 | BlackFog, State of Ransomware 2026 | Exfiltration prevalence (96%), prevention rate (3%) |
| 9 | Darktrace, Qilin RaaS Detection Insights | Qilin TTPs, credential techniques |
| 10 | Darktrace, Medusa RMM Abuse in Ransomware | Medusa TTPs, sector impact confirmation |
| 11 | SOCRadar, Top 10 Ransomware Groups 2025 | Group profiles, DragonForce cartel model |
| 12 | SOCRadar, Top 10 Ransomware Attacks 2025 | Incident case studies |
| 13 | Cyble, Ransomware Attacks Surge October 2025 | Volume trends |
| 14 | Cyberint/Check Point, Qilin Ransomware 2025 | Qilin technical details |
| 15 | KELA Cyber, Qilin Threat Actor Profile | Qilin RaaS model, credential techniques |
| 16 | ESET | EDRKillShifter ecosystem, BYOVD drivers |
| 17 | Picus Security, Top 10 MITRE ATT&CK Techniques | Technique prevalence data |
| 18 | Infosecurity Magazine | Exfiltration tool prevalence (Rclone 57%) |
| 19 | MOXFIVE, INC Ransom Threat Actor Spotlight | INC Ransom profile |
| 20 | Bleeping Computer | Marquis breach, supply-chain reporting |
| 21 | TechCrunch | Marquis breach details |
| 22 | BankInfoSecurity | Marquis breach, banking impact |
| 23 | SC Media | DBS/Toppan Next Tech incident |
| 24 | DeepStrike | Financial sector ransom economics, credential statistics |
| 25 | Invenio IT | Financial sector ransomware statistics (updated 2026) |
| 26 | Halcyon, Ransomware Malicious Quartile Q2-2025 | Group power rankings |
| 27 | CYFIRMA, Tracking Ransomware Jan 2026 | LockBit 5.0 data |
| 28 | Blackpoint, Clop Ransomware Profile | Clop technical details |
| 29 | KnowBe4 | AI phishing statistics |
| 30 | Microsoft IR data (via multiple vendor reports) | RMM tool prevalence (79%) |
| 31 | FinCEN | Payment method data (97% Bitcoin) |

---

*This research base is a living document. Contributions should follow the claim-level inclusion test (Sourced, Current, Relevant, Confidence-rated, Typed) defined in the CTI Research Quality Framework.*
