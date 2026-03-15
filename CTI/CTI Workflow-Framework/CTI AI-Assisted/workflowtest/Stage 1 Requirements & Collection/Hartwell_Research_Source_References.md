# Source References: Ransomware Threat Landscape Report (March 2026)

Organized by report section. Each claim maps to 1-2 primary sources.

---

## Section 1: Active Ransomware Groups Targeting Financial Services

| Claim | Source(s) |
|---|---|
| 126-141 active ransomware groups in 2025 | Emsisoft, "State of Ransomware in the U.S. 2025"; Picus Security, "Top 10 Ransomware Groups of 2025" |
| 451 ransomware cases in financial sector, 2025 | Check Point, "2025 Finance Sector Landscape Report" |
| $365.6M in reported ransom payments (2022-2024) from 432 FS incidents | FinCEN, "Financial Trend Analysis on Ransomware," December 2025 |
| 23% increase in extortion attacks to 6,182 globally | Symantec/Broadcom Threat Hunter Team, "Ransomware 2026" report, January 2026 |
| 406 publicly disclosed FS ransomware victims (Apr 2024-Apr 2025) | Flashpoint, "Top Threat Actor Groups Targeting Financial Sector," 2025 |
| Qilin: 946 victims by year-end 2025, 69 confirmed finance targets | Comparitech data via Industrial Cyber, October 2025; Picus Security, 2025 |
| Qilin "Korean Leaks" — 28 South Korean asset management firms via MSP GJTec | The Hacker News, November 2025; Korea JoongAng Daily, September 23, 2025 |
| Qilin stole 2.5 TB from Habib Bank AG Zurich | Breached.company, late 2025 |
| Akira: 717-740 leak site postings, $244M estimated revenue | Symantec/Broadcom, 2026; Picus Security, 2025 |
| Akira attack on Marquis Software Solutions — 400K+ consumers, 74+ banks | American Banker, "Seven Largest Banking Data Breaches of 2025" |
| Akira: 34 financial sector victims (Apr 2024-Apr 2025) | Flashpoint, "Top Threat Actor Groups Targeting Financial Sector," 2025 |
| Clop: 500+ victims via Cleo and Oracle EBS zero-days | SOCRadar, "Top 10 CVEs of 2025"; BankInfoSecurity, October 7, 2025 |
| Clop: Western Alliance Bank breach (21,899 customers) | SOCRadar, "Top 10 CVEs of 2025" |
| Clop demanded up to $50M per organization (Oracle campaign) | BlackFog, November 2025; Breached.company, "State of Ransomware 2026" |
| RansomHub: 38 confirmed financial victims before April 2025 shutdown | Flashpoint, 2025; Bitsight, 2025 |
| Medusa: CISA/FBI advisory AA25-071A, 300+ victims, $100K-$15M demands | CISA Advisory AA25-071A, March 12, 2025; Symantec, 2025 |
| Lazarus Group deploying Medusa against Middle Eastern financial institutions | Symantec/Security.com, "North Korean Lazarus Group Now Working With Medusa" |
| Play: ~900 entities compromised since mid-2022 | The Hacker News, June 2025 |
| LockBit 4.0/5.0 attempts, May 2025 infrastructure breach, $500 affiliate fees | Acronis TRU; Wikipedia; Breached.company |
| LockBit developer Panev extradited to U.S. | S-RM Intelligence, March 2025; U.S. DOJ |
| Black Basta collapse, 200K messages leaked Feb 11, 2025 | Intel 471; ReliaQuest |
| Black Basta leader Nefedov identified | Barracuda Networks, February 2026 |
| DragonForce cartel model, 200+ victims | Symantec, 2026; SOCRadar |
| SafePay: 58 claimed victims in May 2025 alone | Cyble, May 2025 |
| Hunters International → World Leaks rebrand, UBS data published | Infosecurity Magazine, July 2025; Group-IB, April 2025 |
| 57 new ransomware groups, 27 new extortion groups in 2025 | Cyble, "10 New Ransomware Groups of 2025" |

---

## Section 2: TTPs at Procedure-Level Detail

| Claim | Source(s) |
|---|---|
| Vulnerability exploitation: 33% of initial access cases | Mandiant M-Trends 2025, Google Cloud Blog, April 2025 |
| Compromised credentials: 41% of root causes | Sophos, "2025 Active Adversary Report," April 2025 |
| Edge/VPN exploitation jumped from 3% to 22% (2023-2024) | Verizon DBIR 2025 |
| 90% of ransomware incidents exploited firewalls; fastest chain 3 hours | Barracuda Managed XDR 2025 Threat Report, via Help Net Security, February 2026 |
| MFA absent in 59% of cases; 67.32% identity-related root causes | Sophos, "2026 Active Adversary Report" |
| 75% of initial access attempts are malware-free | CrowdStrike, 2025 Global Threat Report |
| ClickFix surged 517% in 2025 | ESET H1 2025 Threat Report; Infosecurity Magazine, 2025 |
| ClickFix targeting Portuguese financial services (Lampion) | Microsoft Security Blog, August 2025 |
| ClickFix → StealC → Qilin ransomware chain documented | Sophos, "I am not a robot" blog, 2025 |
| Nation-state ClickFix adoption (MuddyWater, APT28) | Logpoint; Proofpoint, 2025 |
| RMM tool abuse in 36% of IR cases; 32 different RMM tools | Arctic Wolf 2025 Threat Report, via eSecurity Planet |
| ScreenConnect signed malicious droppers targeting financial orgs (UNC5952) | CyberProof, May 2025 |
| AnyDesk used by Mad Liberator, Medusa, Rhysida, Cactus | Intel 471, 2025 |
| Black Basta chat leaks confirmed systematic RMM abuse | Intel 471, February 2025 |
| Akira installed Datto RMM on domain controllers | Barracuda, 2025 |
| Median time to AD compromise: 11 hours | Sophos, 2025 Active Adversary Report |
| 62% of compromised AD servers ran out-of-support OS | Sophos, 2025 |
| Rclone in 57% of ransomware incidents | ReliaQuest; Symantec/Broadcom; Infosecurity Magazine |
| Exfiltration median 72.98 hours; 83% of ransomware deployed off-hours | Sophos, 2025 |
| 96% of ransomware attacks involved data exfiltration | BlackFog Q3 2025, via Vectra AI |
| 2,500+ BYOVD driver variants in single campaign | Vectra AI, 2025 |
| EDRKillShifter used by 8+ groups | ESET, March 2025; Arete; The Hacker News, March 2025 |
| Reynolds ransomware embedded driver in payload (Feb 2026) | Vectra AI; Huntress, February 2026 |
| Akira pivoted to unmonitored Linux webcam after EDR quarantine | Vectra AI |

---

## Section 3: Vulnerabilities with CISA KEV Status

| CVE / Product | Claim | Source(s) |
|---|---|---|
| Fortinet general | 14 zero-day advisories in under 4 years | Coalition Insurance |
| CVE-2024-55591 (FortiGate) | CVSS 9.6, ~48K devices vulnerable, CISA KEV Jan 14, 2025 | Shadowserver; Corvus Insurance advisory, February 2025 |
| CVE-2025-59718/59719 (FortiGate) | FortiCloud SSO bypass, intrusions within 3 days | Arctic Wolf; Huntress; The Hacker News, December 2025 |
| CVE-2026-24858 (FortiGate) | Cross-account SSO bypass, ~10K instances | CyberScoop, January 2026; CISA advisory, January 28, 2026 |
| CVE-2025-0108 (Palo Alto) | CVSS 8.8, confirmed exploitation Feb 18, 2025 | Palo Alto Networks advisory; CSO Online, February 2025 |
| CVE-2025-0108 chained with Emperor Dragonfly | Chinese group used for RA World ransomware | Symantec/Broadcom, February 2025 |
| CVE-2024-40711 (Veeam) | CVSS 9.8, used by Akira/Fog/Frag; 20%+ of Rapid7 IR cases | Sophos X-Ops, October 2024; Rapid7, 2024 |
| CVE-2025-23120 (Veeam) | CVSS 9.9, domain user RCE | watchTowr; CSO Online, March 2025 |
| CVE-2025-10035 (GoAnywhere MFT) | CVSS 10.0, exploited by Medusa affiliate Storm-1175 | SOCRadar, "Top 10 CVEs of 2025"; Microsoft attribution |
| CVE-2025-5777 (Citrix NetScaler) | "CitrixBleed 2," 40% of exploitation targeting financial services | Imperva; Arctic Wolf; Cybersecurity Dive |
| CVE-2025-22224/22225/22226 (VMware ESXi) | VM escape chain, CISA confirmed ransomware use | CISA KEV, February 2026; Broadcom advisory VMSA-2025-0004 |
| CVE-2025-29824 (Windows CLFS) | Exploited by Storm-2460 against Venezuelan financial entity | Microsoft Security Blog, April 8, 2025; Symantec/Security.com |

---

## Section 4: Supply Chain Compromises

| Claim | Source(s) |
|---|---|
| Supply chain attacks: 30-60% of all incidents | Verizon DBIR 2025; SecurityScorecard, "2025 Global Third-Party Breach Report," March 26, 2025 |
| 41.4% of ransomware attacks start through third parties | SecurityScorecard, 2025 |
| Fintech: 41.8% of breaches from third-party vendors | SecurityScorecard, "Defending the Financial Supply Chain," May 21, 2025 |
| Clop Oracle EBS campaign — 100+ organizations, payroll/financial data | Google Cloud Blog, October 2025; BlackFog, November 2025 |
| Salesforce breach wave (Allianz, TransUnion, Farmers) | TechTarget, 2025; Proven Data, "Biggest Data Breaches of 2025" |
| Salesloft/Drift OAuth compromise — 700+ organizations | Google Cloud Blog, August 2025 |
| Marquis Software Solutions — 400K+ consumers, 74+ banks | American Banker, "Seven Largest Banking Data Breaches of 2025" |
| SitusAMC breach affecting JPMorgan, Citi, Morgan Stanley | CSO Online, November 2025; Cybernews |
| Prosper Marketplace — 17.6M customers | Centraleyes, October 2025 |
| Insight Partners — $90B+ AUM, 83-day dwell time | GBHackers, September 2025 |
| Financial firms monitor only 36.3% of supply chain for cyber risk | BitSight, November 2025; Help Net Security, November 11, 2025 |
| Financial services breach cost: $5.56M per incident | IBM Cost of a Data Breach Report 2025, August 2025 |

---

## Section 5: Infostealers and Initial Access Brokers

| Claim | Source(s) |
|---|---|
| 47% YoY increase in infostealer attacks on financial institutions | DeepStrike, "Stealer Log Statistics 2025" |
| 54% of ransomware victims had prior infostealer exposure | Verizon DBIR 2025 |
| Lumma: 51% of all logs on Russian dark web markets | Check Point, "2025 State of Cyber Security Report" |
| Lumma: ~92% of credential log alerts on Russian Market | Bitsight, "2025 State of the Underground Report"; ReliaQuest |
| Microsoft identified 394K infected computers; seized 2,300+ domains | Microsoft Security Blog, May 21, 2025 |
| Lumma activity resumed within weeks of takedown | Trend Micro, July 22, 2025 |
| Ransomware groups using Lumma-harvested credentials (Octo Tempest et al.) | Microsoft Security Blog, May 2025 |
| Vidar 2.0: C++ to C rewrite, Azure credential targeting, $300/month | Trend Micro, October 21, 2025; Ontinue; SC Media |
| StealC V2 linked to ClickFix → Qilin ransomware chain | Sophos; Zscaler ThreatLabz, May 2025 |
| Rhadamanthys: AI-powered OCR for seed phrases | Recorded Future, September 2024; Check Point Research, October 2025 |
| Operation Endgame Phase 2: 1,025 servers seized | SpyCloud; Europol, November 2025 |
| Acreed: 118K+ logs to Russian Market by June 2025; targeting SSO tokens | Bitsight; GBHackers; Intrinsec |
| RedLine/META: 64% of infected devices, 451M credentials before takedown | Flashpoint; The Hacker News, October 2024 |
| IAB financial services access: $500-$3,000 per listing | Cyberint/Check Point, IAB Report, April 2025 |
| 6,406 financial sector access posts (Apr 2024-Apr 2025) | Flashpoint, 2025 |
| Session token theft: 31% of M365 breaches, ~40K daily incidents | Obsidian Security, 2025 |
| AiTM phishing attacks increased 146% | Obsidian Security, 2025 |

---

## Section 6: Ransomware Economics

| Claim | Source(s) |
|---|---|
| Financial services median ransom: $2.0M | Sophos, "State of Ransomware in Financial Services 2024" |
| 51% of FS victims paid; 18% paid full demand; avg 75% of initial ask | Sophos Financial Services 2024 |
| Lowest FS encryption rate: 49% (down from 81% in 2023) | Sophos Financial Services 2024 |
| 28% of victims paying in 2025 (record low) | Chainalysis, "2026 Crypto Crime Report," February 2026 |
| Payment rates fell to ~20% by Q4 2025 | Coveware Q4 2025, via SOS Ransomware, February 2026 |
| 86% of businesses refused to pay in 2025 | Coalition 2026 Cyber Claims Report, March 2026 |
| Initial demands surged 47% YoY | Coalition, 2026 |
| Median on-chain payments jumped 368% to ~$59,556 | Chainalysis, 2026 Crypto Crime Report |
| Total on-chain payments: ~$820M in 2025 (8% decline from $892M) | Chainalysis, 2026 Crypto Crime Report |
| FinCEN: $2.1B+ in reported ransomware payments (2022-2024) | FinCEN, December 2025 |
| Mean FS recovery cost: $2.58M excluding ransom | Sophos Financial Services 2024 |
| Backup recovery: $375K avg vs $3M for payers | Invenio IT analysis, updated 2026 |
| Encryption in only 50% of attacks (six-year low) | Sophos, "State of Ransomware 2025" |
| Data-extortion-only payment rate: 19% | Coveware Q3 2025, via HIPAA Journal |
| Triple extortion includes SWATting, employee bribery | Coveware Q3 2025, via SOS Ransomware |
| Attackers stealing cyber insurance policies to calibrate demands | Resilience Midyear 2025 Cyber Risk Report, September 2025 |
| Bitcoin: 97% of FinCEN-reported payments | FinCEN, December 2025 |
| OFAC sanctions: Zservers (Feb), AEZA (Jul), Grinex (Aug), Media Land (Nov) | U.S. Treasury Press Releases, 2025 |

---

## Section 7: Regulatory Landscape

| Claim | Source(s) |
|---|---|
| SEC 8-K: 55 incidents reported by 54 companies in first year | Wilson Sonsini/Known Trends, February 2025 |
| Companies increasingly filing under 8.01 (immaterial) vs 1.05 | SEC Corp Fin Director Gerding statement, May 21, 2024 |
| SEC dismissed SolarWinds case (signal on enforcement posture) | Perkins Coie, 2025 |
| SEC 2026 Exam Priorities: cybersecurity governance, AI/polymorphic malware | SEC Press Release 2025-132, November 17, 2025 |
| FINRA 2026 Report: ransomware top risk, launched CORE program | FINRA 2026 Annual Regulatory Oversight Report, December 9, 2025 |
| FINRA added GenAI section for first time | McGuireWoods analysis, December 2025 |
| CIRCIA final rule delayed to May 2026 | Davis Wright Tremaine, September 2025 |
| CIRCIA FS-sector virtual town hall: March 18, 2026 | CISA.gov |
| CIRCIA: 72-hour incident reporting, 24-hour payment reporting | Congressional Research Service R48025 |
| NY DFS: 27 consent orders, $144M+ in fines | NY DFS Press Release, October 14, 2025 |
| NY DFS key actions: PayPal $2M, Block $40M | NY DFS, 2025 |
| NY DFS Nov 1, 2025 deadline: universal MFA, asset inventories | NY DFS Part 500 amendments |
| NY DFS Class A company criteria | NY DFS Part 500 |
| EU DORA effective January 17, 2025; penalties up to 2% turnover | ESMA/EIOPA/EBA implementation guides |
| OCC: 36-hour incident reporting requirement | ABA Banking Journal; OCC |
| FS-ISAC: financial sector ~8% of ransomware data leaks, 4th most affected | FS-ISAC, "Navigating Cyber 2025," May 19, 2025 |
