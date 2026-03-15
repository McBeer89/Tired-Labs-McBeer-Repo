# Gate 5 — Type Classification (FACT / ASSESSMENT / ASSUMPTION)
## Analyst: Junior Analyst 1
## Date: March 15, 2026
## Claims Evaluated: 118

---

## Instructions

For each claim, classify it as:

- **FACT:** Verifiable. Can be checked against a source. Does NOT carry a confidence level. If you classify something as FACT, the LOW confidence rating from Gate 4 is dropped — facts are either verified or unverified, not "low confidence."
  - Example: "CISA published advisory AA25-071A on Medusa ransomware in March 2025."

- **ASSESSMENT:** An analytical judgment that goes beyond the evidence. Requires a confidence level.
  - Example: "Qilin is the most likely group to target a wealth management firm in early 2026."

- **ASSUMPTION:** A belief being treated as true without verification. The most dangerous type. If you identify something as an ASSUMPTION, state what would need to be verified to convert it to a FACT.
  - Example: "Hartwell uses SonicWall VPN appliances." (Has this been verified with IT?)

**Be especially vigilant for hidden assumptions.** Common hiding places:
- Assumed technology stack ("our edge devices")
- Assumed threat actor motivation ("financially motivated")
- Assumed organizational exposure ("we are a high-value target")
- Assumed defensive posture ("our EDR would detect this")

**Note on FACTS and confidence:** Facts are verifiable and do not carry confidence levels. The LOW confidence you assigned in Gate 4 is dropped for any claim you now classify as FACT. Confidence levels only apply to ASSESSMENTS.

---

## My Pre-Classification With Reasoning

I've pre-classified each claim based on what I can observe. **You must review and override where your judgment differs.** I'm particularly likely to be wrong on claims that look like facts but contain hidden analytical judgments, or claims that look like assessments but are actually verifiable.

---

## PIR-01.1 — Groups, Intrusions, Initial Access

### Ecosystem-Level

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 1 | 126–141 active groups in 2025 | FACT | Verifiable count from named sources; can be checked |
| 2 | 451 FS ransomware cases in 2025 | FACT | Verifiable statistic from Check Point |
| 3 | 23% increase to 6,182 attacks globally | FACT | Verifiable statistic from Symantec/Broadcom |
| 4 | 406 publicly disclosed FS victims Apr 2024–Apr 2025 | FACT | Verifiable from Flashpoint data |
| 5 | Multiple groups ceased operations Jan–Apr 2025; affiliates migrated | FACT (cessation) + ASSESSMENT (migration) | Cessation is observable; migration patterns are analytical inference |
| 6 | 57 new ransomware groups, 27 new extortion groups in 2025 | FACT | Verifiable count from Cyble |

### Qilin

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 7 | 946 victims, 69 FS targets by Oct 2025 | FACT | Verifiable leak site count |
| 8 | Korean Leaks — 28 firms via MSP GJTec, 1M+ files | FACT | Verifiable incident with named victim, date, method |
| 9 | Bitdefender linked to North Korean Moonstone Sleet | ASSESSMENT | Attribution is analytical judgment, not verifiable fact |
| 10 | Absorbed RansomHub affiliates, increasing volume | ASSESSMENT | Affiliate migration is inferred from timing and volume; not directly observable |
| 11 | Stole 2.5 TB from Habib Bank AG Zurich | FACT | Verifiable incident — leak site claim with named victim |
| 12 | Rust payload targets Win/Linux/ESXi; 80–85% affiliate split | FACT (payload targets) + ASSUMPTION (affiliate split) | Payload capabilities are reversible; affiliate percentage is self-reported by criminal group and unverifiable |

### Akira

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 13 | 717–740 leak site postings, $244M revenue | FACT (postings) + ASSESSMENT (revenue) | Leak site count is observable; revenue is an estimate |
| 14 | Marquis attack Aug 2025, 400K+ consumers, 74+ banks via SonicWall | FACT | Verifiable incident with named victim, CVE, date, impact |
| 15 | 34 FS victims Apr 2024–Apr 2025 | FACT | Verifiable count from Flashpoint |
| 16 | CISA/FBI advisory Nov 2025 confirmed FS targeting | FACT | Advisory exists or doesn't; binary verifiable |
| 17 | Exploits VPN without MFA — Cisco and SonicWall | FACT | Documented in CISA advisory; verifiable TTP |
| 18 | Bypassed EDR via IoT webcam (March 2025) | FACT | Specific incident with date; verifiable against Vectra AI reporting |

### Clop

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 19 | 500+ victims via Cleo + Oracle EBS in 2025 | FACT | Verifiable victim count from named campaigns |
| 20 | Western Alliance Bank 21,899 customers via Cleo | FACT | Named victim, specific impact figure |
| 21 | Demanded up to $50M per org (Oracle campaign) | FACT | Verifiable demand amount from reporting |
| 22 | Pure data-extortion; supply-chain methodology creates outsized FS exposure | FACT (no encryption) + ASSESSMENT (outsized exposure) | Operational model is observable; "outsized exposure" is an analytical judgment |

### RansomHub

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 23 | 38 FS victims before Apr 2025 shutdown | FACT | Verifiable count from Flashpoint |
| 24 | DragonForce claimed RansomHub migrated to its infrastructure | FACT | DragonForce's claim is a verifiable statement (they said it); whether it's true is separate |

### Medusa

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 25 | CISA advisory AA25-071A, 300+ victims, $100K–$15M demands | FACT | Advisory with specific ID; verifiable |
| 26 | Lazarus Group deploying Medusa against Middle Eastern FS | ASSESSMENT | Attribution (Lazarus) is analytical; nation-state ransomware nexus is an inference |

### Play, LockBit, Black Basta, Emerging Groups

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 27 | Play ~900 entities since mid-2022, top five in 2025 | FACT (count) + ASSESSMENT (ranking) | Count verifiable; "top five" is a ranking judgment |
| 28 | LockBit 4.0/5.0 attempts; second infrastructure breach May 2025 | FACT | Verifiable events with dates |
| 31 | Black Basta collapsed Jan 2025; 200K messages leaked Feb 2025 | FACT | Verifiable events with dates |
| 33 | Former Black Basta members migrated to Cactus and SafePay | ASSESSMENT | Migration is inferred from affiliate tracking; not directly verifiable |
| 34 | DragonForce cartel model Apr 2025, 200+ victims | FACT | Verifiable operational model and count |
| 35 | SafePay 58 victims in May 2025 | FACT | Verifiable count |
| 36 | Hunters Intl → World Leaks; UBS supplier targeted, 130K employee records | FACT | Verifiable rebrand and incident |

### CVEs Actively Exploited

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 37 | Fortinet 14 zero-days in under 4 years | FACT | Verifiable count of advisories |
| 38 | CVE-2024-55591 FortiOS details + CISA KEV Jan 2025 | FACT | CVE + KEV status are binary verifiable |
| 39 | CVE-2025-59718/59719 FortiCloud + CISA KEV Dec 2025 | FACT | Same |
| 40 | CVE-2026-24858 FortiGate + CISA advisory Jan 2026 | FACT | Same |
| 41 | SentinelOne: FortiGate → pre-ransomware activity as of Mar 2026 | FACT | Verifiable vendor reporting with date |
| 42 | CVE-2025-0108 Palo Alto + CISA KEV Feb 2025 | FACT | CVE + KEV verifiable |
| 43 | Emperor Dragonfly used Palo Alto exploits for RA World ransomware | ASSESSMENT | Attribution of exploit use to specific group is analytical |
| 44 | CVE-2024-40766 SonicWall — Akira primary target, Marquis vector | FACT (CVE) + ASSESSMENT ("primary target") | CVE verifiable; characterization as "primary" is judgment |
| 45 | CVE-2024-40711 Veeam + CISA KEV + ransomware confirmed | FACT | KEV marked "Known" ransomware use |
| 46 | Rapid7: 20%+ of 2024 IR cases involved Veeam exploitation | FACT | Verifiable statistic from Rapid7 |
| 47 | CVE-2025-23120 Veeam CVSS 9.9, domain user RCE | FACT | CVE details verifiable |
| 48 | CVE-2025-10035 GoAnywhere + CISA KEV + Medusa/Storm-1175 | FACT (CVE/KEV) + ASSESSMENT (Storm-1175 attribution) | KEV verifiable; affiliate attribution is analytical |
| 49 | CVE-2025-5777 CitrixBleed 2 + 40% targeting FS + CISA KEV | FACT (CVE/KEV) + FACT (40% stat from Imperva) | Both verifiable |
| 50 | CVE-2025-22224/22225/22226 VMware ESXi + CISA KEV Feb 2026 | FACT | KEV entry verifiable |
| 51 | CVE-2025-29824 Windows CLFS + Storm-2460 + Venezuelan FS entity | FACT (CVE) + ASSESSMENT (Storm-2460 attribution) | CVE verifiable; group attribution is analytical |
| 52 | CVE-2025-61882 Oracle EBS — Clop mass financial data theft | FACT | CVE + campaign verifiable |

### Credential-Based Initial Access

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 53 | Vuln exploitation = 33% of initial access | FACT | Verifiable Mandiant statistic |
| 54 | Compromised credentials = 41% of root causes | FACT | Verifiable Sophos statistic |
| 55 | Edge/VPN exploitation 3% → 22% (2023–2024) | FACT | Verifiable Verizon DBIR statistic |
| 56 | 90% of ransomware exploited firewalls; fastest 3hr chain | FACT | Verifiable Barracuda statistic |
| 57 | MFA absent 59%; 67.32% identity-related root causes | FACT | Verifiable Sophos statistic |
| 58 | 75% of initial access malware-free | FACT | Verifiable CrowdStrike statistic |
| 59 | ClickFix surged 517% in 2025 | FACT | Verifiable ESET statistic |
| 60 | ClickFix targeting Portuguese FS with Lampion (May 2025) | FACT | Verifiable Microsoft blog post |
| 61 | ClickFix → StealC → Qilin chain documented | FACT | Verifiable Sophos case study |
| 62 | MuddyWater, APT28 adopted ClickFix | ASSESSMENT | Nation-state attribution is analytical judgment |

### Confirmed FS Incidents

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 63 | Marquis Software Solutions full incident details | FACT | Named victim, date, CVE, impact — all verifiable |
| 64 | DBS Bank/BOC Singapore via Toppan Next Tech | FACT | Named victims, dates, impact — verifiable |
| 65 | SitusAMC affecting JPMorgan, Citi, Morgan Stanley | FACT | Named victims — verifiable against news reporting |
| 66 | Prosper Marketplace 17.6M customers | FACT | Named victim, impact figure — verifiable |
| 67 | Insight Partners $90B+ AUM, 83-day dwell time | FACT (breach occurred) + ASSESSMENT (83-day dwell time) | Breach verifiable; dwell time is an analytical estimate |
| 68 | Betterment Jan 2026, 1.4M customers, CRM vendor attack | FACT | Named victim, date, vector — verifiable |
| 69 | Wealth mgmt firms on leak sites (Tufton, FAS, Hudson, Duff) | FACT | Leak site postings are observable events |
| 71 | Western Alliance Bank 21,899 customers via Clop/Cleo | FACT | Named victim, impact — verifiable |

---

## PIR-01.2 — TTPs at Procedure Level

### C2

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 72 | Cobalt Strike dominant; Sliver, Brute Ratel, Havoc supplements | ASSESSMENT | "Dominant" and "supplemented by" are analytical rankings of prevalence |
| 73 | GC2 (Google Sheets C2) in Fog; Adaptix emerging | FACT (tools exist/observed) + ASSESSMENT ("emerging") | Observation verifiable; characterization as "emerging" is judgment |

### RMM Abuse

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 74 | RMM abuse in 36% of IR cases; 32 tools | FACT | Verifiable Arctic Wolf statistic |
| 75 | UNC5952 signed ScreenConnect droppers targeting financial orgs | FACT | Verifiable CyberProof reporting |
| 76 | AnyDesk used by Mad Liberator, Medusa, Rhysida, Cactus | FACT | Verifiable Intel 471 reporting |
| 77 | Black Basta chats confirmed systematic RMM abuse | FACT | Verifiable from leaked chat analysis |
| 78 | Akira installed Datto RMM on domain controllers | FACT | Verifiable Barracuda case study |

### Credential Harvesting and Lateral Movement

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 79 | Mimikatz LSASS dumping, sekurlsa::logonpasswords most used | FACT | Verifiable from Red Canary telemetry |
| 80 | Rubeus Kerberoasting in Akira chain | FACT | Verifiable Security Boulevard case study |
| 81 | DCSync for KRBTGT → Golden Ticket | FACT | Documented technique; verifiable |
| 82 | Median time to AD compromise: 11 hours | FACT | Verifiable Sophos statistic |
| 83 | 62% of compromised AD servers ran out-of-support OS | FACT | Verifiable Sophos statistic |
| 84 | Qilin modifies WDigest registry key for plaintext creds | FACT | Technique is specific and verifiable if source is found |
| 85 | Akira dumps Veeam creds via PowerShell | FACT | Technique is specific and verifiable if source is found |
| 86 | Lateral movement: RDP, PsExec, WMI, Impacket; target ESXi | FACT | Standard documented TTPs; verifiable across multiple IR reports |

### Exfiltration

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 87 | Rclone in 57% of incidents; used by LockBit, Black Basta, etc. | FACT | Verifiable across ReliaQuest + Symantec |
| 88 | WinSCP second; cURL third; FileZilla by INC Ransom | FACT | Verifiable ReliaQuest reporting |
| 89 | Exfiltration median 72.98 hours | FACT | Verifiable Sophos statistic |
| 90 | 83% ransomware deployed off-hours; 79% exfil off-hours | FACT | Verifiable Sophos statistic |
| 91 | 96% of attacks involved data exfiltration | FACT | Verifiable BlackFog statistic |
| 92 | Cyberduck by Qilin for Backblaze uploads | FACT | Specific tool-group mapping; verifiable if source is found |

### BYOVD and EDR Evasion

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 93 | 2,500+ BYOVD driver variants in single campaign | FACT | Verifiable Vectra AI statistic |
| 94 | EDRKillShifter used by 8+ groups (named) | FACT | Verifiable ESET reporting with named groups |
| 95 | "QuadSwitcher" orchestrating cross-group use | ASSESSMENT | Threat actor identification and role characterization is analytical |
| 96 | Reynolds (Feb 2026) embedded driver in payload; terminates Falcon, Cortex, Sophos, Symantec | FACT | Verifiable Vectra AI/Huntress reporting |
| 97 | Akira pivoted to unmonitored Linux webcam after EDR quarantine | FACT | Verifiable Vectra AI case study |

### ATT&CK

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 103 | T1486 declining — encryption in 50% of attacks, six-year low | FACT | Verifiable Sophos statistic |

---

## PIR-01.3 — Economics, Payment Rates, Extortion Models

### Demand Ranges

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 104 | FS highest median ransom: $2.0M | FACT | Verifiable Sophos statistic |
| 105 | 51% paid; 18% full demand; avg 75% of ask | FACT | Verifiable Sophos statistic |
| 106 | Demands surged 47% YoY | FACT | Verifiable Coalition statistic |
| 107 | Medusa $100K–$15M | FACT | From CISA advisory — verifiable |
| 108 | Clop demanded up to $50M (Oracle campaign) | FACT | Verifiable from reporting |
| 109 | FS firm paid $25.66M to BlackCat/ALPHV | FACT | Federal indictment — verifiable |

### Payment Rates

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 110 | 28% paid in 2025 — record low | FACT | Verifiable Chainalysis statistic |
| 111 | Rates fell from 25% to ~20% (Q4 2024–Q4 2025) | FACT | Verifiable Coveware data |
| 112 | 86% refused to pay in 2025 | FACT | Verifiable Coalition statistic |
| 113 | Data-extortion-only rate: 19% | FACT | Verifiable Coveware statistic |

### Revenue and Flows

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 114 | Total on-chain: ~$820M in 2025, 8% decline | FACT | Verifiable Chainalysis statistic |
| 115 | Median on-chain jumped 368% to ~$59,556 | FACT | Verifiable Chainalysis statistic |
| 116 | FinCEN: $2.1B+ (2022–2024); $365.6M from 432 FS incidents | FACT | Verifiable FinCEN report |
| 117 | 97% of payments in Bitcoin | FACT | Verifiable FinCEN data |
| 119 | OFAC designations: Zservers, AEZA, Grinex, Media Land | FACT | Verifiable Treasury press releases |

### Recovery Costs

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 120 | Mean FS recovery: $2.58M excluding ransom | FACT | Verifiable Sophos statistic |
| 121 | IBM: FS breach cost $5.56M | FACT | Verifiable IBM report |
| 122 | Backup recovery $375K vs $3M for payers | FACT | Verifiable Invenio IT analysis |

### Extortion Model Evolution

| # | Claim (abbreviated) | Suggested Type | Reasoning |
|---|---|---|---|
| 123 | Encryption in 50% of attacks — six-year low | FACT | Verifiable Sophos statistic |
| 124 | FS lowest encryption rate: 49%, down from 81% | FACT | Verifiable Sophos statistic |
| 125 | Clop/World Leaks skip encryption; Qilin/Akira/Play double extortion | FACT | Observable operational models |
| 126 | Triple extortion: SWATting, employee bribery | FACT | Verifiable Coveware reporting |
| 127 | Attackers stealing cyber insurance policies to calibrate demands | FACT | Verifiable Resilience report |
| 128 | Akira cold-calling employees/clients | FACT | Technique is verifiable if source is found |

---

## Summary of Pre-Classification

| Type | Count | Notes |
|---|---|---|
| FACT | 96 | Verifiable claims — confidence level DROPPED per gate rules |
| ASSESSMENT | 15 | Analytical judgments — RETAIN confidence level (LOW) |
| Mixed FACT + ASSESSMENT | 7 | Claims containing both; needs analyst decision on how to split |
| ASSUMPTION | 0 | None identified — **SEE WARNING BELOW** |

### ⚠️ ZERO ASSUMPTIONS IDENTIFIED — WARNING

**You identified no assumptions in the source material, and neither did I in this pre-classification. Every research base contains assumptions — they may be hiding in claims you or I classified as facts.**

Common hiding places specific to THIS research base:

1. **Assumed Hartwell technology stack:** The CVE claims (37–52) are relevant because they affect products in Hartwell's stated technology stack (Fortinet FortiGate, Cisco AnyConnect, Palo Alto, Veeam, GoAnywhere MFT). But has anyone verified with IT/infrastructure that these products are actually deployed, at what versions, and in what configuration? If not, the relevance of every CVE claim rests on an **unstated assumption about the technology stack.**

2. **Assumed Hartwell exposure profile:** Claims about wealth management firm targeting (67, 69) and the conclusion that Hartwell matches the profile of firms being targeted assume Hartwell's risk profile is comparable. Is it?

3. **Assumed detection capability:** Claims about EDR evasion (93–97) assume Hartwell's detection stack is the one being evaded. Does Hartwell run CrowdStrike Falcon (which Reynolds specifically targets)? If so, claim 96 is directly relevant. If not, it's context but not an organizational threat.

4. **Assumed patch/configuration state:** Claims about VPN exploitation assume Hartwell's edge devices may be vulnerable. Has Vuln Mgmt confirmed patch levels? (Note: GAP-003 in the collection plan already flags that CTI lacks version/patch data for Veeam and GoAnywhere MFT.)

**These assumptions don't appear in the source material — they appear in the ANALYST'S APPLICATION of the source material to Hartwell.** That's exactly where assumptions hide.

Review these and decide: should any be added as explicit assumptions in the research base?
