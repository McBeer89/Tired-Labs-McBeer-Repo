# Claim Extraction — PIR-01.1, 01.2, 01.3
## Source: AI-Synthesized Research Document (March 2026) with Source References File
## Analyst: Junior Analyst 1
## Date: March 15, 2026
## Reporting Period: Past 90 days (mid-December 2025 – mid-March 2026)

---

## PIR-01.1 — Which ransomware groups have conducted confirmed intrusions against financial services firms in the past 90 days, and what initial access methods did they use?

### Ecosystem-Level Claims

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 1 | 126–141 active ransomware groups operated in 2025, up from ~70 in 2023. | Emsisoft, "State of Ransomware in the U.S. 2025"; Picus Security, "Top 10 Ransomware Groups of 2025" | Yes — 2025 full-year data |
| 2 | Financial sector recorded 451 ransomware cases in 2025. | Check Point, "2025 Finance Sector Landscape Report" | Yes |
| 3 | 23% increase in extortion attacks to 6,182 globally in 2025. | Symantec/Broadcom, "Ransomware 2026," January 2026 | Yes |
| 4 | 406 publicly disclosed financial sector ransomware victims from April 2024–April 2025 (~7% of all listings). | Flashpoint, "Top Threat Actor Groups Targeting Financial Sector," 2025 | Yes — date range specified |
| 5 | RansomHub, Black Basta, 8Base, BianLian, and Cactus all ceased operations between January and April 2025; displaced affiliates migrated to surviving and new operations. | Malwarebytes/ThreatDown, April 2025; Intel 471; ReliaQuest; Bitsight, 2025 | Yes |
| 6 | 57 new ransomware groups and 27 new extortion groups emerged in 2025. | Cyble, "10 New Ransomware Groups of 2025" | Yes |

### Group-Specific Claims — Qilin

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 7 | Qilin had 946 victims by year-end 2025, including 69 confirmed finance-sector targets among 590 business attacks by October 2025. | Comparitech via Industrial Cyber, October 2025; Picus Security, 2025 | Yes |
| 8 | Qilin's September 2025 "Korean Leaks" campaign compromised MSP GJTec to breach 28 South Korean asset management firms, exfiltrating over 1 million files. | The Hacker News, November 2025; Bitdefender; Korea JoongAng Daily, September 23, 2025 | Yes |
| 9 | Bitdefender linked the Qilin Korean campaign to potential North Korean state-affiliated involvement via Moonstone Sleet. | Bitdefender research (referenced in synthesis) | Yes |
| 10 | Qilin absorbed affiliates from defunct RansomHub after RansomHub ceased operations April 2025, significantly increasing its attack volume. | Malwarebytes/ThreatDown, April 2025; Bitsight, 2025 | Yes |
| 11 | Qilin stole 2.5 TB from Habib Bank AG Zurich. | Breached.company, late 2025 | Yes |
| 12 | Qilin's Rust-based payload targets Windows, Linux, and VMware ESXi; its RaaS model offers affiliates 80–85% of ransom proceeds. | AI synthesis; no named primary source in references file | Uncertain — undated capability claim |

### Group-Specific Claims — Akira

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 13 | Akira had approximately 717–740 leak site postings and an estimated $244 million in total extortion revenue since launch. | Symantec/Broadcom, "Ransomware 2026," 2026; Picus Security, 2025 | Yes |
| 14 | Akira's August 14, 2025, attack on Marquis Software Solutions (vendor to 700+ banks) compromised over 400,000 consumers across 74+ institutions via CVE-2024-40766 (SonicWall VPN). | American Banker, "Seven Largest Banking Data Breaches of 2025" | Yes |
| 15 | Flashpoint attributed 34 financial sector victims to Akira from April 2024 to April 2025. | Flashpoint, "Top Threat Actor Groups Targeting Financial Sector," 2025 | Yes |
| 16 | CISA/FBI advisory (updated November 2025) confirmed Akira's continued targeting of financial institutions. | CISA/FBI advisory (November 2025) | Yes |
| 17 | Akira exploits VPN infrastructure without MFA — particularly Cisco and SonicWall appliances. | CISA/FBI advisory (implied); Sophos X-Ops | Yes |
| 18 | In March 2025, Akira bypassed EDR by encrypting a network from an unsecured IoT webcam after EDR quarantined the initial payload. | Vectra AI | Yes |

### Group-Specific Claims — Clop

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 19 | Clop added 500+ victims in 2025 through campaigns against Cleo file transfer products (CVE-2024-50623/CVE-2024-55956, December 2024 onward) and Oracle E-Business Suite (CVE-2025-61882, July–November 2025). | SOCRadar, "Top 10 CVEs of 2025"; Google Cloud Blog, October 2025; BankInfoSecurity, October 7, 2025 | Yes |
| 20 | Clop's Cleo campaign included Western Alliance Bank (21,899 customers, SSNs stolen). | SOCRadar, "Top 10 CVEs of 2025" | Yes |
| 21 | Clop demanded up to $50 million from individual organizations in the Oracle EBS campaign. | BlackFog, November 2025; Breached.company, "State of Ransomware 2026" | Yes |
| 22 | Clop operates as a pure data-extortion group (no encryption); its supply-chain methodology creates outsized exposure for financial firms reliant on shared technology platforms. | AI synthesis; analytical assertion supported by incident pattern | Yes |

### Group-Specific Claims — RansomHub

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 23 | RansomHub led all groups in financial sector targeting with 38 confirmed financial victims from April 2024–April 2025 before ceasing operations April 1, 2025. | Flashpoint, 2025; Bitsight, 2025 | Yes — but group is now defunct |
| 24 | DragonForce claimed RansomHub migrated to its infrastructure. | Malwarebytes/ThreatDown, April 2025 | Yes |

### Group-Specific Claims — Medusa

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 25 | Medusa received joint CISA/FBI/MS-ISAC advisory AA25-071A (March 12, 2025) after exceeding 300 victims, with demands ranging from $100,000 to $15 million. | CISA Advisory AA25-071A, March 12, 2025; Symantec, 2025 | Yes |
| 26 | North Korean Lazarus Group actors were discovered deploying Medusa ransomware against Middle Eastern financial institutions. | Symantec/Security.com, "North Korean Lazarus Group Now Working With Medusa" | Yes |

### Group-Specific Claims — Play

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 27 | Play has compromised approximately 900 entities since mid-2022 and remained consistently active throughout 2025 among top five groups. | The Hacker News, June 2025 | Yes |

### Group-Specific Claims — LockBit

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 28 | LockBit attempted recovery with LockBit 4.0 (February 2025) and 5.0 (September 2025) but suffered a second infrastructure breach in May 2025 exposing affiliate details. | Acronis TRU; Wikipedia | Yes |
| 29 | LockBit affiliate fees dropped to $500 to compete. | Breached.company, "State of Ransomware 2026" | Yes |
| 30 | Key LockBit developer Rostislav Panev was extradited to the U.S. after arrest in Israel. | S-RM Intelligence, March 2025; U.S. DOJ | Yes |

### Group-Specific Claims — Black Basta

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 31 | Black Basta collapsed in January 2025, with 200,000 internal messages leaked on February 11, 2025. | Intel 471; ReliaQuest | Yes |
| 32 | German federal police identified Oleg Evgenievich Nefedov as key Black Basta leader "GG." | Barracuda Networks, February 2026 | Yes |
| 33 | Former Black Basta members migrated to Cactus and SafePay groups. | AI synthesis; implied by Intel 471/ReliaQuest | Yes |

### Group-Specific Claims — Emerging Groups

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 34 | DragonForce introduced a "cartel model" in April 2025 allowing affiliates to operate under their own branding, claiming 200+ victims. | Symantec, 2026; SOCRadar | Yes |
| 35 | SafePay surged to 58 claimed victims in May 2025. | Cyble, May 2025 | Yes |
| 36 | Hunters International rebranded as World Leaks (data-theft-only), targeting a third-party supplier of UBS in June 2025 and publishing data on 130,000 UBS employees. | Infosecurity Magazine, July 2025; Group-IB, April 2025 | Yes |

### Initial Access — CVEs Actively Exploited Against Financial Services

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 37 | Fortinet FortiGate has had 14 zero-day advisories in under 4 years. | Coalition Insurance | Yes |
| 38 | CVE-2024-55591 (FortiOS): CVSS 9.6, authentication bypass via Node.js websocket, ~48,000 internet-facing devices vulnerable. Exploited as zero-day since November 2024. CISA KEV January 14, 2025. Multiple ransomware groups actively exploiting. | Shadowserver; Corvus Insurance advisory, February 2025; CISA KEV | Yes |
| 39 | CVE-2025-59718/59719 (FortiCloud SSO bypass): CVSS 9.8, active intrusions within 3 days of disclosure. Huntress reported 11 instances in 30 days. CISA KEV December 16, 2025. | Arctic Wolf; Huntress; The Hacker News, December 2025; Help Net Security, January 2026 | Yes — within reporting window |
| 40 | CVE-2026-24858 (FortiGate cross-account SSO bypass): ~10,000 instances affected. CISA advisory January 28, 2026. | CyberScoop, January 2026; CISA advisory, January 28, 2026; Shadowserver | Yes — within reporting window |
| 41 | SentinelOne documented campaigns using FortiGate as entry points with pre-ransomware activity observed as of March 2026. | SentinelOne (referenced in synthesis) | Yes — within reporting window |
| 42 | CVE-2025-0108 (Palo Alto PAN-OS): CVSS 8.8, authentication bypass, confirmed exploitation from February 18, 2025. Chained with CVE-2024-9474 and CVE-2025-0111 for root-level access. CISA KEV February 2025. | Palo Alto Networks advisory; CSO Online, February 2025 | Yes |
| 43 | Chinese cyber-espionage group Emperor Dragonfly used Palo Alto exploits for RA World ransomware deployment. | Symantec/Broadcom, February 2025 | Yes |
| 44 | CVE-2024-40766 (SonicWall SSL VPN): Akira's primary exploitation target; the vector in the Marquis Software Solutions attack (74+ banks). | American Banker; AI synthesis | Yes |
| 45 | CVE-2024-40711 (Veeam Backup): CVSS 9.8, deserialization RCE, exploited by Akira, Fog, and Frag ransomware. Sophos X-Ops tracked 4+ incidents in October 2024 combining VPN compromise + Veeam exploitation. CISA KEV October 17, 2024. Marked "Known" for ransomware use. | Sophos X-Ops, October 2024; Cybersecurity Dive; CISA KEV | Yes — ongoing exploitation |
| 46 | Rapid7 noted 20%+ of their 2024 IR cases involved Veeam exploitation. | Rapid7, 2024 | Yes — data from 2024, most recent available |
| 47 | CVE-2025-23120 (Veeam): CVSS 9.9, allows any authenticated domain user to execute code when backup server is domain-joined. Disclosed March 2025. | watchTowr; CSO Online, March 2025 | Yes |
| 48 | CVE-2025-10035 (GoAnywhere MFT): CVSS 10.0, command injection, exploited by Storm-1175 (Medusa affiliate) since at least September 11, 2025. CISA KEV. | SOCRadar, "Top 10 CVEs of 2025"; Microsoft attribution | Yes |
| 49 | CVE-2025-5777 (Citrix NetScaler, "CitrixBleed 2"): CVSS 9.3, 11.5 million exploitation attempts, 40% targeting financial services. One attacking IP linked to RansomHub by CISA. CISA KEV July 10, 2025. | Imperva; Arctic Wolf; Cybersecurity Dive; CISA | Yes |
| 50 | CVE-2025-22224/22225/22226 (VMware ESXi): VM escape chain, CVSS up to 9.3, exploited as zero-days since at least February 2024. CISA confirmed CVE-2025-22225 "Known To Be Used in Ransomware Campaigns." February 2026 KEV update. | CISA KEV, February 2026; Broadcom advisory VMSA-2025-0004; Help Net Security; BleepingComputer | Yes — within reporting window |
| 51 | CVE-2025-29824 (Windows CLFS): Exploited by Storm-2460 targeting a Venezuelan financial sector entity; also used by Play ransomware-linked Balloonfly group. CISA KEV April 2025. | Microsoft Security Blog, April 8, 2025; Symantec/Security.com | Yes |
| 52 | CVE-2025-61882 (Oracle E-Business Suite): SSRF/XSL RCE exploited by Clop for mass financial data theft (July–November 2025). | Google Cloud Blog, October 2025; BlackFog, November 2025 | Yes |

### Initial Access — Credential-Based Vectors

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 53 | Vulnerability exploitation accounts for 33% of initial access cases. | Mandiant M-Trends 2025, Google Cloud Blog, April 2025 | Yes |
| 54 | Compromised credentials account for 41% of root causes. | Sophos, "2025 Active Adversary Report," April 2025 | Yes |
| 55 | Edge/VPN device exploitation jumped from 3% to 22% of all exploitation cases between 2023 and 2024. | Verizon DBIR 2025 | Yes |
| 56 | 90% of ransomware incidents exploited firewalls via CVE or vulnerable account; fastest observed chain completed breach-to-encryption in 3 hours and lateral movement in 10 minutes. | Barracuda Managed XDR 2025 Threat Report, Help Net Security, February 2026 | Yes |
| 57 | MFA was absent in 59% of cases; 67.32% of root causes were identity-related. | Sophos, "2026 Active Adversary Report" (covering Nov 2024–Oct 2025) | Yes |
| 58 | 75% of initial access attempts are malware-free, relying on credentials and identity misuse. | CrowdStrike, 2025 Global Threat Report | Yes |
| 59 | ClickFix social engineering surged 517% in 2025, becoming the second most common attack vector behind traditional phishing. | ESET H1 2025 Threat Report; Infosecurity Magazine, 2025 | Yes |
| 60 | Microsoft identified a May 2025 ClickFix campaign specifically targeting Portuguese financial services organizations with Lampion banking malware. | Microsoft Security Blog, August 2025 | Yes |
| 61 | Sophos documented a complete ClickFix → StealC → Qilin ransomware attack chain where stolen VPN credentials were sold by an IAB approximately one month later. | Sophos, "I am not a robot" blog, 2025 | Yes |
| 62 | Nation-state actors including Iran's MuddyWater and Russia's APT28 adopted ClickFix. | Logpoint; Proofpoint, 2025 | Yes |

### Financial Sector Incidents (PIR-01.1 — Confirmed Intrusions)

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 63 | Marquis Software Solutions (August 2025): Akira compromised vendor to 700+ banks via SonicWall CVE-2024-40766, exfiltrating data on 400,000+ consumers across 74+ institutions including SSNs and financial account data. Marquis paid ransom but data appeared on criminal marketplaces. Two-month notification delay triggered state AG filings. | American Banker, "Seven Largest Banking Data Breaches of 2025" | Yes |
| 64 | DBS Bank/Bank of China Singapore (April 2025): Ransomware attack on printing vendor Toppan Next Tech exposed data on 8,200 DBS customers (mostly DBS Vickers brokerage users) and 3,000 BOC Singapore customers. | AI synthesis; no named primary source in references file | Yes |
| 65 | SitusAMC breach (November 2025): Affected JPMorgan Chase, Citigroup, and Morgan Stanley via mortgage tech vendor. | CSO Online, November 2025; NYT/Bloomberg/CNN (referenced in synthesis) | Yes — within reporting window |
| 66 | Prosper Marketplace breach: 17.6 million customers — the largest single FS breach of 2025 by record count. | Centraleyes, October 2025 | Yes |
| 67 | Insight Partners ransomware attack: $90+ billion AUM PE firm, 83-day dwell time. | GBHackers, September 2025 | Yes |
| 68 | Betterment disclosed a breach in January 2026 exposing 1.4 million customers via a social engineering attack on a CRM vendor. | AI synthesis; no named primary source in references file | Yes — within reporting window |
| 69 | Multiple wealth management firms appeared on ransomware leak sites in 2025: Tufton Capital Management ($810M AUM), FAS Wealth Partners, Hudson Executive Capital LP, Duff Capital Investors. | AI synthesis; no named primary source in references file | Yes |
| 70 | A financial services firm paid a $25.66 million ransom to BlackCat/ALPHV affiliates (October 2025 federal indictment); two affiliates were a ransomware negotiator at DigitalMint and an IR manager at Sygnia Cybersecurity. | Federal indictment, October 2025 (referenced in synthesis) | Yes |
| 71 | Western Alliance Bank: 21,899 customers had SSNs stolen via Clop's Cleo exploitation. | SOCRadar, "Top 10 CVEs of 2025" | Yes |

---

## PIR-01.2 — What specific tools, techniques, and procedures — at the procedure level — are these groups using in current campaigns, including evasion techniques targeting EDR platforms?

### Command and Control

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 72 | Cobalt Strike remains the most frequently observed C2 framework, supplemented by Sliver (used by DEV-0237/FIN12 and APT29), Brute Ratel C4 (cracked versions at $2,500/license), and Havoc with Demon agent supporting Microsoft Graph API integration. | Microsoft/GCHQ (Sliver); BleepingComputer/AdvIntel (Brute Ratel); AlphaHunt, 2025–2026 (Havoc) | Yes |
| 73 | Emerging C2 tools include GC2 (abusing Google Sheets, observed in Fog ransomware) and Adaptix. | Picus Security, 2025 (Adaptix); AI synthesis (GC2/Fog) | Yes |

### Remote Management Tool Abuse

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 74 | RMM tool abuse appeared in 36% of IR cases, with 32 different RMM tools documented. | Arctic Wolf 2025 Threat Report, via eSecurity Planet | Yes |
| 75 | UNC5952 used signed malicious ConnectWise ScreenConnect droppers targeting global financial organizations. | CyberProof, May 2025 | Yes |
| 76 | AnyDesk featured in ransomware activity by Mad Liberator, Medusa, Rhysida, and Cactus. | Intel 471, 2025 | Yes |
| 77 | Black Basta's 197,000 leaked chat messages confirmed systematic RMM abuse. | Intel 471, February 2025 | Yes |
| 78 | Akira installed Datto RMM on domain controllers to blend into routine IT automation. | Barracuda, 2025 | Yes |

### Credential Harvesting and Lateral Movement

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 79 | Mimikatz for LSASS dumping (sekurlsa::logonpasswords is the most-used module). | Red Canary (referenced in synthesis) | Uncertain — no publication date for Red Canary data |
| 80 | Rubeus for Kerberoasting documented in Akira's attack chain. | Security Boulevard, November 2025 | Yes |
| 81 | DCSync attacks for KRBTGT hash extraction enabling Golden Ticket creation. | Qualys ETM Defense Guide, February 2026 | Yes |
| 82 | Median time from initial access to Active Directory compromise: 11 hours. | Sophos, 2025 Active Adversary Report | Yes |
| 83 | 62% of compromised AD servers ran out-of-support operating systems. | Sophos, 2025 Active Adversary Report | Yes |
| 84 | Qilin affiliates modify the WDigest registry key to force plaintext credential storage. | AI synthesis; no named primary source | Uncertain — undated |
| 85 | Akira dumps Veeam backup credentials via PowerShell. | AI synthesis; no named primary source | Uncertain — undated |
| 86 | Lateral movement relies on RDP (T1021.001), PsExec/PAExec over SMB admin shares (T1021.002), WMI (T1047), and Impacket; primary target is VMware ESXi hypervisors. | AI synthesis; general TTP description supported by multiple vendor reports | Uncertain — undated composite |

### Exfiltration

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 87 | Rclone is the dominant exfiltration tool, present in 57% of ransomware incidents, used by LockBit, Black Basta, BlackSuit, Medusa; typically uploading to MEGA.io. | ReliaQuest; Symantec/Broadcom; Infosecurity Magazine | Yes |
| 88 | WinSCP ranks second for exfiltration, followed by cURL; FileZilla used by INC Ransom for FTP-based exfiltration. | ReliaQuest (referenced in synthesis) | Yes |
| 89 | Exfiltration occurs at a median of 72.98 hours after attack initiation. | Sophos, 2025 Active Adversary Report | Yes |
| 90 | 83% of ransomware binaries deployed outside business hours; 79% of exfiltration also occurs off-hours. | Sophos, 2025 Active Adversary Report | Yes |
| 91 | 96% of ransomware attacks in 2025 involved data exfiltration alongside encryption. | BlackFog Q3 2025, via Vectra AI | Yes |
| 92 | Cyberduck used by Qilin affiliates for multipart uploads to Backblaze. | AI synthesis; no named primary source | Uncertain — undated |

### BYOVD and EDR Evasion

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 93 | Over 2,500 BYOVD driver variants used in a single campaign targeting the TrueSight driver. | Vectra AI, 2025 | Yes |
| 94 | EDRKillShifter (developed by RansomHub) is now used by at least 8 distinct groups: RansomHub, Medusa, BianLian, Play, BlackSuit, Qilin, DragonForce, and INC Ransom. | ESET, March 2025; Arete; The Hacker News, March 2025 | Yes |
| 95 | ESET identified threat actor "QuadSwitcher" orchestrating cross-group EDRKillShifter attacks; cross-group sharing suggests active collaboration among typically closed RaaS operations. | ESET, March 2025 | Yes |
| 96 | Reynolds ransomware (February 2026) embedded a vulnerable driver directly in its payload, terminating CrowdStrike Falcon, Cortex XDR, Sophos, and Symantec. | Vectra AI; Huntress, February 2026 | Yes — within reporting window |
| 97 | Akira pivoted to an unmonitored Linux-based webcam on the same network after EDR quarantined the initial payload, encrypting the network from an agentless device. | Vectra AI | Yes |
| 98 | Process injection (T1055) is the #1 most prevalent technique overall. | Picus Security, 2025 | Yes |

### MITRE ATT&CK Mapping (Composite — procedure-level context)

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 99 | T1190 (Exploit Public-Facing Application) is the primary initial access technique, targeting edge devices: Fortinet, Ivanti, Citrix, SonicWall, Palo Alto. | Composite: Mandiant M-Trends 2025; Verizon DBIR 2025; Barracuda 2025 | Yes |
| 100 | T1078 (Valid Accounts) accounts for 33–41% of initial access depending on source. | Mandiant M-Trends 2025; Sophos 2025 Active Adversary | Yes |
| 101 | T1562.001 (Disable Security Tools) via BYOVD/EDRKillShifter is the dominant defense evasion technique of 2025. | ESET, March 2025; Vectra AI, 2025 | Yes |
| 102 | T1567 (Exfiltration to Cloud Storage) via Rclone is present in 57% of incidents. | ReliaQuest; Symantec/Broadcom | Yes |
| 103 | T1486 (Data Encrypted for Impact) declining — encryption occurred in only 50% of attacks in 2025, a six-year low. | Sophos, "State of Ransomware 2025" | Yes |

---

## PIR-01.3 — What is the current ransom demand range, payment rate, and double-extortion model for groups actively targeting financial services?

### Demand Ranges

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 104 | Financial services faces the highest median ransom payment of any sector at $2.0 million. | Sophos, "State of Ransomware in Financial Services 2024" | Uncertain — 2024 report; most recent available but outside 90-day window |
| 105 | 51% of financial services victims paid a ransom; only 18% paid the full initial demand; firms paid an average of 75% of the initial ask. | Sophos, "State of Ransomware in Financial Services 2024" | Uncertain — same as above |
| 106 | Initial ransom demands surged 47% year-over-year in 2025. | Coalition 2026 Cyber Claims Report, March 2026 | Yes — within reporting window |
| 107 | Medusa demands range from $100,000 to $15 million. | CISA Advisory AA25-071A, March 12, 2025 | Yes |
| 108 | Clop demanded up to $50 million from individual organizations in the Oracle EBS campaign. | BlackFog, November 2025; Breached.company, "State of Ransomware 2026" | Yes |
| 109 | A financial services firm paid $25.66 million to BlackCat/ALPHV affiliates. | Federal indictment, October 2025 | Yes |

### Payment Rates

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 110 | 28% of victims paid ransoms across all sectors in 2025 — a record low. | Chainalysis, "2026 Crypto Crime Report," February 2026 | Yes |
| 111 | Payment rates fell from 25% (Q4 2024) to approximately 20% by Q4 2025. | Coveware Q4 2024/Q4 2025, via SOS Ransomware, February 2026 | Yes |
| 112 | 86% of businesses refused to pay in 2025. | Coalition 2026 Cyber Claims Report, March 2026 | Yes — within reporting window |
| 113 | Data-extortion-only attack payment rate dropped to 19% — victims increasingly doubt attackers will delete data. | Coveware Q3 2025, via HIPAA Journal | Yes |

### Revenue and Financial Flows

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 114 | Total on-chain ransomware payments reached approximately $820 million in 2025, an 8% decline from 2024's revised $892 million. | Chainalysis, "2026 Crypto Crime Report," February 2026 | Yes |
| 115 | Median on-chain payments jumped 368% to ~$59,556, reflecting concentration on higher-value victims. | Chainalysis, "2026 Crypto Crime Report," February 2026 | Yes |
| 116 | FinCEN documented over $2.1 billion in reported ransomware payments in BSA filings from 2022–2024; $365.6 million from 432 financial services incidents. | FinCEN, "Financial Trend Analysis on Ransomware," December 2025 | Yes |
| 117 | 97% of FinCEN-reported ransomware payments are in Bitcoin. | FinCEN, December 2025 | Yes |
| 118 | Bridge-related laundering growing 66% while mixer activity declined 37% as actors prefer cross-chain movement. | TRM Labs, 2026 Crypto Crime Report | Yes |
| 119 | OFAC designations in 2025: Zservers (February), AEZA Group (July), Garantex successor Grinex (August, $100M+ illicit transactions), Media Land LLC (November). | U.S. Treasury Press Releases, 2025 | Yes |

### Recovery Costs

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 120 | Mean recovery cost for financial services: $2.58 million excluding ransom. | Sophos, "State of Ransomware in Financial Services 2024" | Uncertain — 2024 report |
| 121 | IBM placed average financial services breach cost at $5.56 million per incident (second highest after healthcare). | IBM Cost of a Data Breach Report 2025, August 2025 | Yes |
| 122 | Financial firms with functional backups recovered for $375,000 average vs. $3 million for those who paid. | Invenio IT analysis, updated 2026 | Yes |

### Extortion Model Evolution

| # | Claim | Gate 1: Source | Gate 2: Current? |
|---|---|---|---|
| 123 | Encryption occurred in only 50% of ransomware attacks in 2025 — a six-year low, down from 70% in 2024. | Sophos, "State of Ransomware 2025" | Yes |
| 124 | Financial services has the lowest encryption rate of any sector at 49%, down from 81% in 2023. | Sophos, "State of Ransomware in Financial Services 2024" | Uncertain — 2024 report |
| 125 | Groups like Clop and World Leaks skip encryption entirely; Qilin, Akira, and Play favor double extortion. | AI synthesis; supported by incident-level data across multiple sources | Yes |
| 126 | Triple extortion now includes SWATting executives' homes and attempting to bribe employees. | Coveware Q3 2025, via SOS Ransomware; HIPAA Journal | Yes |
| 127 | Attackers are stealing organizations' cyber insurance policies to calibrate ransom demands just below policy payout limits. | Resilience Midyear 2025 Cyber Risk Report, September 2025 | Yes |
| 128 | Akira has begun cold-calling employees and clients of victim companies as a pressure tactic. | AI synthesis; no named primary source | Uncertain — undated |

---

## Summary Statistics

- **Total claims extracted:** 128
- **PIR-01.1 (Groups, intrusions, initial access):** Claims 1–71
- **PIR-01.2 (TTPs, procedure-level detail, EDR evasion):** Claims 72–103
- **PIR-01.3 (Economics, payment rates, extortion models):** Claims 104–128
- **Gate 1 — Claims with named primary sources:** ~110 of 128 (~86%)
- **Gate 1 — Claims attributed only to AI synthesis:** ~18 of 128 (~14%)
- **Gate 2 — Marked "Yes" (current):** ~113 of 128
- **Gate 2 — Marked "Uncertain":** ~15 of 128
