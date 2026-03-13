# Ransomware threat landscape targeting financial services, 2025–2026

**Financial services is now the highest-value ransomware target sector globally, with firms paying a median $2.0 million per incident and facing record attack volumes.** The ecosystem has fractured dramatically: 85+ active extortion groups operated simultaneously in Q3 2025, up from a handful of dominant players two years ago. Despite this surge — attack volumes rose 45–50% year-over-year — payment rates collapsed to an all-time low of **23%** by Q3 2025. The result is a paradox: more attacks, less revenue per attack, and increasingly aggressive tactics as operators compensate for declining payouts. For a firm with the profile of a large retail brokerage or wealth management house, the most relevant threats are Qilin (which ran a targeted campaign against 23 South Korean financial firms in a single quarter), Akira (34 confirmed financial sector victims in 12 months), and supply-chain attacks via third-party vendors — the dominant intrusion pathway for financial institutions in 2025.

---

## The groups that matter most right now

**Qilin** (also known as Agenda) is the most prolific ransomware operation of 2025, surpassing 1,000 leak-site victims and averaging 75 attacks per month by Q3. It absorbed affiliates from defunct RansomHub (which ceased operations in April 2025), causing a **280% jump** in its attack claims. In August–September 2025, Qilin executed a focused campaign against South Korea's financial sector, compromising 23 financial services organizations — many of them mid-sized **private equity funds** — through a single cloud server operated by a shared IT contractor. The group's Rust-based payload targets Windows, Linux, and VMware ESXi, and its RaaS model offers affiliates **80–85%** of ransom proceeds, among the most competitive splits in the market.

**Akira** ranks second with approximately 740 victims in 2025 and an estimated **$244 million** in total extortion revenue since launch. A joint CISA/FBI advisory updated in November 2025 confirmed Akira's continued targeting of financial institutions, with **34 confirmed financial sector victims** between April 2024 and April 2025. Akira is notable for exploiting VPN infrastructure without MFA — particularly Cisco and SonicWall appliances — and for a March 2025 incident where it bypassed EDR entirely by encrypting a network from an unsecured IoT webcam. The group has begun cold-calling employees and clients of victim companies as a pressure tactic.

**Clop** remains dangerous despite lower overall victim counts because of its specialized mass-exploitation model. In Q1 2025, Clop published nearly 400 victims from its exploitation of the Cleo managed file transfer platform (CVE-2024-50623/CVE-2024-55956), then pivoted to an Oracle E-Business Suite zero-day (CVE-2025-61882) targeting payroll, HR, and finance databases. Clop operates as a pure data-extortion group — no encryption — and its supply-chain methodology creates outsized exposure for financial firms reliant on shared technology platforms.

**Play** maintains a steady **28–33 victims per month**, including confirmed attacks on financial services companies such as Lakeside Title Co. (a Maryland title/settlement firm). **INC Ransom** explicitly targets organizations with "substantial financial resources," including Howard Financial Corp. **Medusa** drew a joint CISA/FBI advisory in March 2025 specifically listing financial services among its targeted critical infrastructure sectors, with Darktrace confirming financial services as the most impacted sector among its customer base. **LockBit** returned with version 5.0 in September 2025, posting 90 victims in January 2026, though its pre-disruption dominance has not recovered. **DragonForce**, operating a white-label "cartel" RaaS model, attacked German insurer HanseMerkur in early 2026 and has been adopted by Scattered Spider affiliates for social engineering-led campaigns against financial targets.

---

## How they get in: initial access vectors and key CVEs

Edge device exploitation is the primary technical entry point. The following CVEs were actively exploited against financial services targets in 2025:

- **CVE-2024-55591 / CVE-2025-24472** (Fortinet FortiOS/FortiProxy): Authentication bypass vulnerabilities exploited by Mora_001, a LockBit-linked affiliate deploying "SuperBlack" ransomware. Zero-day exploitation began December 2024; added to CISA KEV March 2025.
- **CVE-2025-0282 / CVE-2025-22457** (Ivanti Connect Secure VPN): Stack-based buffer overflow enabling RCE, exploited by UNC5221 and ransomware affiliates from January 2025.
- **CVE-2025-5777 / CVE-2025-7775 / CVE-2025-6543** (Citrix NetScaler): Three separate zero-days since mid-2025, collectively dubbed "CitrixBleed 2," with **11.5 million+** recorded attack attempts.
- **CVE-2024-40766** (SonicWall SSL VPN): Akira's primary exploitation target; the likely vector in the Marquis Software Solutions attack affecting 74+ banks.
- **CVE-2025-10035** (Fortra GoAnywhere MFT): Deserialization RCE (CVSS 10.0) exploited by Medusa from September 2025.
- **CVE-2025-61882** (Oracle E-Business Suite): SSRF/XSL RCE exploited by Clop for mass financial data theft.
- **CVE-2023-27532 / CVE-2024-40711** (Veeam Backup): Exploited by Akira for backup server compromise and credential harvesting.

The **infostealer-to-IAB-to-ransomware pipeline** is now the dominant initial access path when credentials, not vulnerabilities, are the entry point. Mandiant's 2025 M-Trends report places valid accounts (T1078) at **21% of all ransomware initial access**. Lumma Stealer (LummaC2), RedLine, and Raccoon harvest credentials that are sold to initial access brokers (IABs) at an average price of **$2,700 per corporate network** — with 71% including elevated privileges. Flashpoint tracked **6,406 dark web forum posts** offering access to financial sector networks between April 2024 and April 2025.

Phishing remains universal. AI-generated phishing emails now constitute **83%** of phishing traffic (KnowBe4) and achieve a **54% success rate** versus 12% for traditional campaigns. The "ClickFix" social engineering technique — tricking users into pasting malicious commands — was adopted broadly by ransomware actors in H1 2025.

---

## The post-exploitation kill chain in detail

Once inside, the attack sequence follows a consistent pattern across major groups. **Cobalt Strike** remains the dominant C2 framework despite Operation Morpheus reducing unauthorized copies by 80%; alternatives include **Sliver** (Go-based, open-source), **Brute Ratel C4** (designed for EDR evasion), and **Havoc**. Remote management tools — **AnyDesk, ScreenConnect, MeshAgent, Splashtop** — appeared in **79%** of Microsoft incident response engagements in 2025.

For credential access, **Mimikatz** (often Themida-packed to evade detection) remains standard, supplemented by **DonPAPI**, **NetExec**, **LaZagne**, and Kerberoasting (T1558.003) for service account credentials. Qilin affiliates modify the WDigest registry key to force plaintext credential storage. Akira dumps Veeam backup credentials via PowerShell.

Lateral movement relies on **RDP** (T1021.001), **PsExec/PAExec** over SMB admin shares (T1021.002), **WMI** (T1047), and **Impacket** for SMB/WMI abuse. The target is typically VMware ESXi hypervisors, where a single encryption operation can disable an entire virtualized environment.

**BYOVD (Bring Your Own Vulnerable Driver)** is the dominant defense evasion technique of 2025. RansomHub's **EDRKillShifter** tool — which exploits vulnerable kernel drivers to terminate endpoint security processes — has been shared across at least **eight rival ransomware groups** including Play, Medusa, and BianLian, creating what ESET describes as an "EDRKillShifter-as-a-Service ecosystem." Specific vulnerable drivers in active use include Intel's rwdrv.sys (Akira), NSecKrnl.sys/CVE-2025-68947 (Reynolds), BdApiUtil.sys/CVE-2024-51324 (DeadLock), and GameDriverx64.sys/CVE-2025-61155 (Interlock). Reynolds ransomware, observed in February 2026, embeds the vulnerable driver directly inside the ransomware payload, eliminating the staging step entirely.

Data exfiltration occurs in **96% of ransomware attacks** (BlackFog Q3 2025), with organizations successfully preventing only **3%** of exfiltration attempts (Vectra AI). **Rclone** appears in **57% of ransomware incidents**, typically configured to sync to cloud storage (Google Drive, Amazon S3, MEGA, Backblaze) and often renamed to svchost.exe to evade detection. Other exfiltration tools include **WinSCP**, **FileZilla**, **MEGAsync**, **AzCopy** (to Azure Blob storage), and **Cyberduck** (used by Qilin affiliates for multipart uploads to Backblaze).

---

## 2025 incidents that hit closest to the wealth management sector

The **Marquis Software Solutions** attack in August 2025 is the most consequential financial sector supply-chain incident of the year. Marquis, a Texas-based vendor providing marketing, compliance, and data analytics to **700+ banking institutions**, was compromised likely via a SonicWall vulnerability (CVE-2024-40766). The attackers exfiltrated data on **1.4 million+ consumers** across 74+ banks and credit unions, including names, SSNs, financial account information, and debit/credit card numbers. Marquis paid the ransom, but data still appeared on criminal marketplaces. The two-month gap between breach and client notification (August to late October) has triggered multiple state AG filings and class action investigations.

The **DBS Bank/Bank of China Singapore** incident in April 2025 directly impacted a brokerage operation. A ransomware attack on printing vendor Toppan Next Tech exposed data on **8,200 DBS customers**, most of whom were users of **DBS Vickers** (the bank's brokerage arm), with data including names, addresses, and equity holdings details. An additional 3,000 Bank of China Singapore customers were affected.

Several wealth management and investment firms appeared on ransomware leak sites in 2025: **Tufton Capital Management** ($810M AUM, Hunt Valley, Maryland), **FAS Wealth Partners** (Kansas City), **Hudson Executive Capital LP** (NYC, SEC-registered investment advisor), and **Duff Capital Investors**. **Betterment**, the major robo-advisor platform, disclosed a breach in January 2026 exposing 1.4 million customers via a social engineering attack on a CRM vendor.

A particularly striking data point from an October 2025 federal indictment: a **financial services firm paid a $25.66 million ransom** to BlackCat/ALPHV affiliates — two of whom turned out to be a ransomware negotiator at DigitalMint and an incident response manager at Sygnia Cybersecurity, operating as rogue affiliates.

---

## MITRE ATT&CK techniques most relevant to financial sector ransomware

The following techniques map directly to the TTPs described above and should form the core of any financial sector CTI report:

| Phase | Technique ID | Technique | Context |
|---|---|---|---|
| Initial Access | T1190 | Exploit Public-Facing Application | Edge devices: Fortinet, Ivanti, Citrix, SonicWall |
| Initial Access | T1078 | Valid Accounts | Infostealer credentials; 21% of initial access |
| Initial Access | T1566.001/.002 | Phishing | AI-generated; ClickFix social engineering |
| Execution | T1059.001 | PowerShell | Universal post-exploitation; UAC bypass, Defender disabling |
| Persistence | T1219 | Remote Access Software | AnyDesk, ScreenConnect, MeshAgent in 79% of IR cases |
| Persistence | T1136.002 | Create Domain Account | Akira creates "itadm"; RansomHub re-enables disabled accounts |
| Privilege Escalation | T1068 | Exploitation for Privilege Escalation | Veeam, SonicWall vulnerabilities |
| Privilege Escalation | T1558.003 | Kerberoasting | Akira service account credential extraction |
| Defense Evasion | T1562.001 | Disable Security Tools | **BYOVD/EDRKillShifter — dominant evasion technique** |
| Defense Evasion | T1055 | Process Injection | **#1 most prevalent technique overall** (Picus 2025) |
| Credential Access | T1003 | OS Credential Dumping | Mimikatz, LSASS, DonPAPI |
| Lateral Movement | T1021.001/.002 | RDP / SMB Admin Shares | PsExec, Impacket for remote execution |
| Collection | T1560 | Archive Collected Data | WinRAR, 7-Zip staging before exfiltration |
| Exfiltration | T1567 | Exfiltration to Cloud Storage | Rclone in 57% of incidents; MEGA, S3, Backblaze |
| Impact | T1486 | Data Encrypted for Impact | Declining to 50% of attacks; data theft now primary |
| Impact | T1490 | Inhibit System Recovery | vssadmin shadow copy deletion; backup service termination |

---

## The money: ransom economics and regulatory pressure

Financial services firms face the **highest median ransom payments** of any sector at **$2.0 million**, with a mean payment of **$3.3 million** among firms that pay. **58% of demands** to financial firms exceed $1 million; **38% exceed $5 million**. Recovery costs diverge dramatically: firms that pay ransoms spend an average of **$3 million** on recovery, while those restoring from backups average **$375,000** — an 8x differential that increasingly drives the decision not to pay.

The payment rate collapse is the defining trend of 2025. Only **28% of victims** paid ransoms across all sectors (Chainalysis), down from 79% in 2022. For data-exfiltration-only attacks — the model Clop and others are shifting toward — the rate dropped to just **19%**. Total ransomware revenue held roughly flat at **~$820–900 million** despite the 50% increase in attacks, meaning operators are working significantly harder for diminishing returns.

One novel escalation: **Interlock ransomware has begun stealing victims' cyber insurance policies** and using them to calibrate ransom demands just below policy payout limits. This represents a direct weaponization of financial data against financial firms. Meanwhile, **97%** of ransoms are still paid in Bitcoin (FinCEN data), though laundering is increasingly difficult — sanctioned exchange Garantex processed $100M+ in ransomware-linked transactions before being shut down and reconstituting as Grinex.

The regulatory environment is in flux. SEC cybersecurity disclosure rules require material incident reporting within **four business days**, but a coalition of financial trade associations (BPI, ABA, SIFMA) petitioned in May 2025 to rescind the rule, arguing it has been "weaponized as an extortion method." Under new SEC Chair Paul Atkins, the rule's future is uncertain. OFAC maintains a strict liability regime on payments to sanctioned entities, and expanded sanctions designations in 2025 — including Zservers, Media Land LLC, and the Garantex network — create growing compliance risk for any firm considering payment. CISA's CIRCIA rule, expected finalized by October 2025, will require critical infrastructure entities to report ransomware payments within **24 hours**.

---

## Conclusion: what this means for a wealth management CTI posture

The threat to firms with a retail brokerage or wealth management profile is concrete and escalating. **93% of investment management executives** reported at least one cyber incident in 2025, yet only **24%** use dedicated cybersecurity solutions — the widest gap between exposure and protection in any financial sub-sector. The most likely attack scenarios are threefold: direct compromise via unpatched VPN/firewall appliances (Akira's preferred vector), supply-chain intrusion through a third-party vendor (the Marquis and DBS/Toppan pattern), or credential-based access via the infostealer pipeline.

The groups most likely to target such a firm in early 2026 are **Qilin** (demonstrated financial sector focus, highest volume), **Akira** (consistent financial targeting, CISA-advised), and **Medusa** (explicitly listed financial services in CISA advisory, known for aggressive triple extortion). The shift from encryption-first to data-theft-first extortion is particularly dangerous for firms holding sensitive client financial data — PII, account numbers, equity holdings, and trading histories carry premium value on criminal marketplaces regardless of whether a ransom is paid. The emergence of insurance policy theft as a negotiation weapon suggests that attackers are becoming increasingly sophisticated in understanding the financial dynamics of their targets.