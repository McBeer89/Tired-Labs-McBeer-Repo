# Cyber Threat Intelligence Report: Ransomware Threat Assessment for Edward Jones

**Report ID:** CTI-2026-0047  
**Classification:** TLP:AMBER  
**Date:** March 10, 2026  
**Prepared By:** [Analyst Name], Cyber Threat Intelligence Team  
**Distribution:** CISO, VP Information Security, Security Operations Center, Incident Response Team, Risk Management, Compliance, IT Infrastructure, Executive Leadership Team

---

## Table of Contents

1. Executive Summary
2. Background on Ransomware
3. The Current Ransomware Landscape
4. Threat Actor Profiles
5. Initial Access Vectors
6. Post-Exploitation Tooling and Kill Chain
7. Financial Sector Targeting Trends
8. Recent Incidents Relevant to Edward Jones
9. MITRE ATT&CK Mapping
10. Indicators of Compromise
11. Regulatory and Compliance Considerations
12. Recommendations
13. Conclusion
14. References

---

## 1. Executive Summary

Ransomware continues to be a significant and evolving threat to financial services organizations globally, including firms with a profile similar to Edward Jones. In 2025, the ransomware ecosystem experienced significant changes, including the fragmentation of major groups following law enforcement operations, the emergence of new threat actors, and a continued shift toward data exfiltration-based extortion models. This report provides a comprehensive overview of the current ransomware threat landscape as it pertains to the financial services sector and specifically to our organization's risk profile as a wealth management and brokerage firm with over 20,000 financial advisors, approximately 9 million clients, and operations across the United States and Canada. The purpose of this report is to ensure that all stakeholders across the organization have a thorough understanding of the threat environment and can make informed decisions about security investments, controls, and risk acceptance. The threat is assessed as HIGH based on our analysis.

---

## 2. Background on Ransomware

### 2.1 What is Ransomware?

Ransomware is a type of malicious software (malware) that is designed to deny access to a computer system or data, typically by encrypting the victim's files, until a ransom is paid. The concept of ransomware dates back to 1989 with the AIDS Trojan (also known as the PC Cyborg virus), which was distributed via floppy disks and demanded payment be sent to a P.O. box in Panama. Since then, ransomware has evolved dramatically, particularly with the advent of cryptocurrency which enables anonymous payments, and the development of the Ransomware-as-a-Service (RaaS) business model.

Modern ransomware typically falls into one of several categories:

- **Crypto ransomware**: Encrypts files and demands payment for the decryption key. This is the most common variant.
- **Locker ransomware**: Locks the user out of their operating system entirely, preventing access to the desktop, applications, and files.
- **Double extortion ransomware**: Combines encryption with data theft. The threat actor threatens to publish stolen data if the ransom is not paid, even if the victim can restore from backups.
- **Triple extortion ransomware**: Adds a third pressure mechanism, such as DDoS attacks against the victim's infrastructure, contacting the victim's customers or partners directly, or threatening to report the victim to regulatory authorities.
- **Data extortion only (no encryption)**: Some groups, such as Clop, have moved entirely to data theft without deploying encryption payloads. This model is faster to execute and avoids detection mechanisms focused on encryption behaviors.

### 2.2 The Ransomware-as-a-Service (RaaS) Model

The modern ransomware ecosystem operates primarily through a Ransomware-as-a-Service (RaaS) model, which mirrors legitimate software-as-a-service business models. In a RaaS operation, the core developers create and maintain the ransomware payload, the command-and-control infrastructure, the negotiation portal, and the data leak site. They then recruit affiliates — independent operators who carry out the actual intrusions — and provide them with access to these tools in exchange for a percentage of any ransom payments collected.

The typical revenue split in a RaaS operation ranges from 70/30 to 85/15 in favor of the affiliate, with the core developers taking the smaller share. Some groups, such as Qilin, offer affiliates up to 80-85% of ransom proceeds, making them among the most competitive operations in the current market. This model has dramatically lowered the barrier to entry for conducting ransomware attacks, as affiliates do not need to develop their own malware, infrastructure, or negotiation capabilities.

The RaaS model also creates a significant challenge for attribution and law enforcement. Because affiliates may work with multiple RaaS operators simultaneously, or switch between them, taking down a single operation does not necessarily remove the affiliates from the ecosystem. This was clearly demonstrated when the LockBit operation was disrupted by Operation Cronos in February 2024 — many of its affiliates simply migrated to other RaaS platforms, including RansomHub, Akira, and Qilin.

### 2.3 The Evolution of Extortion Tactics

The extortion tactics employed by ransomware groups have evolved significantly over the past several years. Initially, the threat was limited to data encryption — pay the ransom or lose your data. However, as organizations improved their backup strategies and disaster recovery capabilities, threat actors adapted by adding data exfiltration as a secondary extortion lever.

Today, the trend is moving further away from encryption entirely. According to BlackFog's Q3 2025 data, data exfiltration occurred in 96% of ransomware attacks, and organizations were able to prevent only 3% of exfiltration attempts. This suggests that the primary value proposition for threat actors has shifted from denying access to threatening exposure. This evolution is particularly concerning for financial services organizations, which hold large volumes of personally identifiable information (PII), financial account data, and proprietary business information that could cause significant harm if exposed.

---

## 3. The Current Ransomware Landscape

### 3.1 Overall Volume and Trends

The ransomware threat landscape in 2025 was characterized by a significant increase in overall attack volume combined with a paradoxical decline in ransom payment rates. According to Check Point Research, Q3 2025 saw more than 85 distinct ransomware groups operating simultaneously — a significant increase from prior periods when the market was dominated by a handful of major operators. This fragmentation was driven in part by the disruption of major operations like LockBit and ALPHV/BlackCat, which created opportunities for smaller groups to recruit displaced affiliates and capture market share.

Attack volumes increased approximately 45-50% year-over-year in 2025. However, the overall ransom payment rate dropped to approximately 23% in Q3 2025, down from an estimated 28% for the full year and a high of roughly 79% in 2022. This creates a perverse incentive: as fewer victims pay, attackers must increase volume and intensity to maintain revenue, leading to more aggressive tactics and more frequent attacks.

Total ransomware payments for 2025 held roughly flat at an estimated $820-900 million despite the dramatic increase in attack volume, indicating that the average value per successful attack is declining. However, the median ransom payment for financial services specifically remained at approximately $2.0 million, with a mean of $3.3 million among firms that actually paid.

### 3.2 Ecosystem Fragmentation

Several significant events reshaped the ransomware ecosystem in 2025:

- **LockBit's attempted recovery and LockBit 5.0**: Following the February 2024 Operation Cronos takedown and the May 2024 identification of administrator Dmitry Khoroshev (LockBitSupp), the group struggled to rebuild credibility and affiliate trust. LockBit 5.0 was launched in September 2025 and posted 90 victims in January 2026, but the group has not recovered its pre-disruption market position.
- **ALPHV/BlackCat's exit scam**: After receiving a reported $22 million payment from Change Healthcare, ALPHV/BlackCat conducted an apparent exit scam in March 2024, absconding with affiliate funds and shutting down operations. This displaced a significant number of experienced affiliates into the broader ecosystem.
- **RansomHub's rise and fall**: RansomHub rapidly grew to become the most active group in H2 2024 by offering favorable affiliate terms (90/10 split) and absorbing displaced ALPHV affiliates. However, the group's infrastructure went offline in April 2025 amid internal disputes, causing another wave of affiliate displacement — many of whom migrated to Qilin.
- **The emergence of DragonForce's "cartel" model**: DragonForce launched a white-label RaaS platform allowing affiliates to operate under their own branding while using DragonForce's infrastructure. This model has been adopted by Scattered Spider affiliates for social engineering-led campaigns against financial targets.

---

## 4. Threat Actor Profiles

### 4.1 Qilin (a.k.a. Agenda)

**Overview**: Qilin is currently the most prolific ransomware operation globally, having surpassed 1,000 leak-site victims and averaging 75 attacks per month by Q3 2025. The group experienced a 280% jump in attack claims after absorbing affiliates from the defunct RansomHub operation.

**History**: Qilin first emerged in July 2022 and initially operated under the name "Agenda." The group rebranded to Qilin (named after a mythical creature from Chinese mythology) and has steadily grown its operations over the past three years. Qilin is believed to be a Russian-speaking operation based on language analysis of its communications and its policy of not attacking targets in CIS (Commonwealth of Independent States) countries.

**Technical Capabilities**: Qilin's ransomware payload is written in Rust, a programming language that provides cross-platform compatibility and makes reverse engineering more difficult. The payload targets Windows, Linux, and VMware ESXi environments. Qilin affiliates have been observed modifying the WDigest registry key (HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest\UseLogonCredential) to force plaintext credential storage in memory, facilitating credential harvesting using tools like Mimikatz.

**Financial Sector Targeting**: In August-September 2025, Qilin executed a focused campaign against South Korea's financial sector, compromising 23 financial services organizations — many of them mid-sized private equity funds — through a single cloud server operated by a shared IT contractor. This demonstrated the group's willingness and ability to target financial services specifically.

**RaaS Model**: Qilin offers affiliates 80-85% of ransom proceeds, making it one of the most competitive programs in the current market.

### 4.2 Akira

**Overview**: Akira is the second most prolific ransomware group, with approximately 740 victims in 2025 and an estimated $244 million in total extortion revenue since launch.

**History**: Akira first appeared in March 2023 and is believed to have connections to the disbanded Conti ransomware group based on code similarities, shared Bitcoin wallets, and overlapping infrastructure. The group is tracked by CrowdStrike as PUNK SPIDER, by Microsoft as Storm-1567, by Palo Alto as Howling Scorpius, and by other vendors under various designations.

**Technical Capabilities**: Akira primarily targets VPN infrastructure lacking multi-factor authentication, particularly Cisco ASA/AnyConnect (CVE-2023-20269) and SonicWall SSL VPN (CVE-2024-40766) appliances. The group is also known for exploiting Veeam Backup & Replication vulnerabilities (CVE-2023-27532, CVE-2024-40711) to compromise backup servers and harvest stored credentials. In a notable incident in March 2025, Akira affiliates bypassed an organization's EDR solution by pivoting to an unsecured IoT webcam on the network and encrypting files from that device, demonstrating creative lateral movement tactics.

**Financial Sector Activity**: A joint CISA/FBI advisory updated in November 2025 (AA24-109A) confirmed Akira's continued targeting of financial institutions, with 34 confirmed financial sector victims between April 2024 and April 2025. The group has expanded its extortion tactics to include cold-calling employees and clients of victim companies as a pressure mechanism.

**Ransom Demands**: Akira's ransom demands for financial institutions typically range from $200,000 to several million dollars, with the group showing willingness to negotiate. They typically create a local admin account named "itadm" for persistence.

### 4.3 Clop (a.k.a. Cl0p)

**Overview**: Clop operates a specialized mass-exploitation model that distinguishes it from most other ransomware groups. Rather than conducting individual intrusions, Clop identifies and exploits zero-day vulnerabilities in widely-deployed enterprise software platforms, then simultaneously exfiltrates data from hundreds of organizations.

**History**: Clop has been active since 2019 and is believed to be associated with the FIN11/TA505 threat group. The group gained significant notoriety through its exploitation of the MOVEit Transfer vulnerability (CVE-2023-34362) in 2023, which impacted over 2,600 organizations and 95 million individuals globally. Clop operates as a pure data-extortion group — it does not deploy encryption payloads, instead relying entirely on the threat of publishing stolen data to compel payment.

**2025 Activity**: In Q1 2025, Clop exploited vulnerabilities in the Cleo managed file transfer platform (CVE-2024-50623 and CVE-2024-55956), publishing nearly 400 victims from this single campaign. The group subsequently pivoted to an Oracle E-Business Suite zero-day (CVE-2025-61882) targeting payroll, HR, and finance databases.

**Relevance to Edward Jones**: Clop's supply-chain exploitation model creates risk for any organization that uses widely-deployed enterprise software platforms, particularly managed file transfer solutions and ERP systems. Even if Edward Jones is not directly vulnerable to Clop's currently-exploited platforms, the group's methodology could be applied to other software in our technology stack.

### 4.4 Medusa

**Overview**: Medusa operates as a RaaS and has been active since mid-2021, with significant growth in 2024-2025.

**History**: It is important to distinguish Medusa ransomware from MedusaLocker, which is a separate operation. Medusa operates its own data leak site under the name "Medusa Blog" and uses a Tor-based negotiation portal. The group was the subject of a joint CISA/FBI/MS-ISAC advisory (AA25-071A) issued in March 2025, which specifically listed financial services among its targeted critical infrastructure sectors.

**Technical Capabilities**: Medusa affiliates are known for their use of remote monitoring and management (RMM) tools for persistence and lateral movement. Darktrace has reported that Medusa affiliates frequently abuse legitimate RMM tools including AnyDesk, ScreenConnect, and MeshAgent, and confirmed that financial services was the most impacted sector among its customer base for Medusa-related activity.

**Extortion Model**: Medusa employs a triple extortion model, demanding ransom for decryption, threatening to publish stolen data, and in some cases conducting DDoS attacks against victims or contacting their customers directly.

### 4.5 Play (a.k.a. Playcrypt)

**Overview**: Play maintains a steady operational tempo of approximately 28-33 victims per month throughout 2025.

**Technical Capabilities**: Play is known for its use of custom tooling and its targeting of Microsoft Exchange vulnerabilities. The group has been observed exploiting ProxyNotShell vulnerabilities and using a custom network scanning tool called Grixba.

**Financial Sector Activity**: Play has targeted financial services companies including title and settlement firms. The group was the subject of an updated joint CISA/FBI advisory in 2025 confirming its continued targeting of diverse businesses and critical infrastructure across North America and Europe.

### 4.6 INC Ransom

**Overview**: INC Ransom has been active since mid-2023 and explicitly targets organizations with "substantial financial resources."

**Technical Capabilities**: INC Ransom affiliates use spear-phishing emails, exploitation of Citrix NetScaler vulnerabilities (CVE-2023-3519), and compromised credentials obtained from initial access brokers. The group uses a combination of commercial and open-source tools for post-exploitation, including Cobalt Strike, Impacket, and MegaSync for data exfiltration.

**Financial Sector Activity**: INC Ransom has claimed responsibility for attacks on financial services organizations including Howard Financial Corp. The group's explicit targeting of organizations with financial resources makes wealth management and brokerage firms high-priority targets.

### 4.7 DragonForce

**Overview**: DragonForce launched a novel "cartel" model RaaS platform in 2025, allowing affiliates to operate under their own branding while using DragonForce's infrastructure.

**Recent Activity**: DragonForce attacked German insurer HanseMerkur in early 2026 and has been adopted by Scattered Spider affiliates for social engineering-led campaigns against financial targets. The white-label model makes attribution more difficult and allows the group to scale operations more rapidly than traditional RaaS operations.

### 4.8 LockBit

**Overview**: Despite the significant disruption of Operation Cronos in February 2024, LockBit attempted to reconstitute with LockBit 5.0 in September 2025.

**Current Status**: The group posted 90 victims in January 2026, indicating some degree of recovery, but has not regained its pre-disruption dominance. The identification of administrator Dmitry Khoroshev and the loss of affiliate trust have permanently degraded the group's capabilities, though it remains a credible threat.

---

## 5. Initial Access Vectors

### 5.1 Edge Device Exploitation

The exploitation of internet-facing network devices — particularly VPN appliances, firewalls, and remote access gateways — is the primary technical initial access vector for ransomware targeting financial services. The following vulnerabilities were actively exploited against financial services targets in 2025:

| CVE | Product | Type | CVSS | Used By |
|-----|---------|------|------|---------|
| CVE-2024-55591 | Fortinet FortiOS | Auth bypass | 9.8 | Mora_001 / LockBit |
| CVE-2025-24472 | Fortinet FortiProxy | Auth bypass | 9.8 | Mora_001 / LockBit |
| CVE-2025-0282 | Ivanti Connect Secure | Buffer overflow | 9.0 | UNC5221 / Multiple |
| CVE-2025-22457 | Ivanti Connect Secure | Buffer overflow | 9.0 | UNC5221 / Multiple |
| CVE-2025-5777 | Citrix NetScaler | Zero-day | 9.8 | Multiple |
| CVE-2025-7775 | Citrix NetScaler | Zero-day | 9.1 | Multiple |
| CVE-2025-6543 | Citrix NetScaler | Zero-day | 9.4 | Multiple |
| CVE-2024-40766 | SonicWall SSL VPN | Auth bypass | 9.3 | Akira |
| CVE-2025-10035 | Fortra GoAnywhere MFT | Deserialization RCE | 10.0 | Medusa |
| CVE-2025-61882 | Oracle E-Business Suite | SSRF/XSL RCE | 9.8 | Clop |
| CVE-2023-27532 | Veeam Backup | Credential leak | 7.5 | Akira |
| CVE-2024-40711 | Veeam Backup | RCE | 9.8 | Akira |

The Citrix NetScaler vulnerabilities, collectively referred to as "CitrixBleed 2," have been associated with over 11.5 million recorded attack attempts since mid-2025.

### 5.2 The Infostealer-to-IAB-to-Ransomware Pipeline

The second major initial access pathway is the credential theft pipeline, which operates through a series of distinct steps. First, infostealer malware — most commonly Lumma Stealer (LummaC2), RedLine, and Raccoon — is distributed to large numbers of users through malicious advertisements, fake software downloads, and phishing campaigns. These infostealers harvest saved credentials, session tokens, and other sensitive data from infected machines. The stolen credentials are then packaged and sold to initial access brokers (IABs) on dark web forums.

According to Flashpoint, there were 6,406 dark web forum posts offering access to financial sector networks between April 2024 and April 2025. The average price for corporate network access is approximately $2,700, with 71% of available accesses including elevated privileges. Mandiant's 2025 M-Trends report places valid accounts (MITRE ATT&CK T1078) as the source of 21% of all ransomware initial access events.

This pipeline is particularly concerning for financial services organizations because it represents a continuous, scalable threat that is independent of the organization's perimeter defenses. Even if our network appliances are fully patched and properly configured, credentials stolen from employees' personal devices or compromised through phishing could provide attackers with valid access.

### 5.3 Phishing and Social Engineering

Phishing remains a universal initial access vector across all ransomware operations. However, the nature of phishing attacks has changed significantly with the adoption of generative AI. According to KnowBe4, AI-generated phishing emails now constitute approximately 83% of phishing traffic and achieve a 54% success rate compared to just 12% for traditional phishing campaigns.

A specific social engineering technique that gained widespread adoption among ransomware actors in H1 2025 is the "ClickFix" technique, which involves tricking users into pasting malicious commands into the Windows Run dialog or a PowerShell console. This technique has been used by multiple ransomware groups and bypasses many traditional email security controls because the actual malware execution occurs through user action rather than through malicious attachments or links.

Additionally, several ransomware groups — notably Scattered Spider affiliates operating under the DragonForce cartel model — have been observed conducting telephone-oriented social engineering (vishing) attacks targeting help desk personnel. These attacks typically involve the attacker impersonating an employee and requesting a password reset or MFA bypass, granting them initial access to the corporate network.

---

## 6. Post-Exploitation Tooling and Kill Chain

### 6.1 Command and Control

Once initial access is achieved, ransomware affiliates establish persistent command and control (C2) communications using a variety of frameworks:

- **Cobalt Strike**: Remains the dominant C2 framework in the ransomware ecosystem, despite Fortra's Operation Morpheus reducing unauthorized copies by approximately 80%. Cobalt Strike provides encrypted C2 communications, in-memory payload execution, credential harvesting modules, lateral movement capabilities, and file management tools. Many affiliates use "cracked" or pirated versions of Cobalt Strike.
- **Sliver**: An open-source, Go-based C2 framework developed by BishopFox that is increasingly adopted as an alternative to Cobalt Strike. Sliver supports multiple communication protocols (mTLS, HTTP, HTTPS, DNS) and provides cross-platform implants for Windows, Linux, and macOS.
- **Brute Ratel C4**: A commercial adversary simulation framework designed specifically for EDR evasion. Brute Ratel uses features such as direct syscalls, indirect syscalls, and reflective DLL loading to avoid detection by endpoint security solutions.
- **Havoc**: An open-source C2 framework that has gained popularity among ransomware affiliates due to its modular architecture and active development community.

### 6.2 Remote Access and Persistence

In addition to dedicated C2 frameworks, ransomware affiliates extensively abuse legitimate remote monitoring and management (RMM) tools for persistence and remote access. According to Microsoft's incident response data, RMM tools appeared in 79% of ransomware incidents in 2025. The most commonly abused tools include:

- AnyDesk
- ScreenConnect (ConnectWise Control)
- MeshAgent / MeshCentral
- Splashtop
- TeamViewer
- Atera

These tools are particularly effective for maintaining persistence because they are legitimate software with valid code signatures, making them difficult to distinguish from authorized IT administration tools in many environments. Ransomware affiliates may also create new user accounts for persistence — Akira, for example, typically creates a local administrator account named "itadm."

### 6.3 Credential Access

Credential harvesting is a critical phase of the ransomware kill chain, as it enables lateral movement and privilege escalation. Common credential access tools and techniques observed in 2025 include:

- **Mimikatz**: The most widely-used credential harvesting tool, often packed with Themida or other protectors to evade detection. Mimikatz can extract plaintext passwords, NTLM hashes, and Kerberos tickets from LSASS process memory.
- **DonPAPI**: A tool for extracting Windows credentials from DPAPI (Data Protection API) protected stores, including saved browser passwords, Wi-Fi keys, and Windows Credential Manager entries.
- **NetExec**: A Swiss Army knife for Windows network exploitation that supports credential spraying, pass-the-hash attacks, command execution over SMB/WMI, and credential extraction from remote systems.
- **LaZagne**: An open-source credential recovery tool that supports extraction from dozens of applications including browsers, email clients, databases, and system credentials.
- **Kerberoasting (T1558.003)**: A technique for extracting service account credentials by requesting Kerberos service tickets and cracking them offline. Akira has been specifically observed using this technique for service account credential extraction.

Qilin affiliates have been observed modifying the WDigest registry key to force Windows to store plaintext credentials in LSASS memory, a technique that has been largely mitigated in modern Windows versions but remains effective when registry protections are not in place.

### 6.4 Lateral Movement

Lateral movement in ransomware attacks typically relies on a combination of built-in Windows administration tools and offensive security frameworks:

- **Remote Desktop Protocol (RDP)** (T1021.001): The most common lateral movement protocol, often used in combination with stolen credentials or pass-the-hash attacks.
- **PsExec / PAExec over SMB Admin Shares** (T1021.002): Used for remote command execution on systems where SMB is accessible. PAExec is an open-source alternative to the Sysinternals PsExec tool.
- **Windows Management Instrumentation (WMI)** (T1047): Used for remote process execution and system enumeration.
- **Impacket**: A Python library providing implementations of various Windows networking protocols, commonly used for SMB/WMI-based lateral movement, credential relaying, and Kerberos attacks.

The ultimate target for lateral movement in many ransomware attacks is the VMware ESXi hypervisor environment, where encrypting a single host can disable an entire virtualized infrastructure.

### 6.5 Defense Evasion

The dominant defense evasion technique in 2025 is Bring Your Own Vulnerable Driver (BYOVD), in which attackers load a known-vulnerable kernel driver onto the target system and exploit it to terminate endpoint security processes. The most prominent tool in this category is **EDRKillShifter**, originally developed by RansomHub affiliates but now shared across at least eight rival ransomware groups including Play, Medusa, and BianLian. ESET has described this cross-group sharing as an "EDRKillShifter-as-a-Service ecosystem."

Specific vulnerable drivers observed in active ransomware campaigns include:

- Intel's `rwdrv.sys` (used by Akira)
- `NSecKrnl.sys` / CVE-2025-68947 (used by Reynolds ransomware)
- `BdApiUtil.sys` / CVE-2024-51324 (used by DeadLock ransomware)
- `GameDriverx64.sys` / CVE-2025-61155 (used by Interlock ransomware)

Reynolds ransomware, first observed in February 2026, embeds the vulnerable driver directly inside the ransomware payload, eliminating the staging step entirely and making detection more difficult.

### 6.6 Data Exfiltration

Data exfiltration occurs in 96% of ransomware attacks according to BlackFog's Q3 2025 data. The most commonly used exfiltration tools include:

- **Rclone**: Appears in 57% of ransomware incidents. Typically configured to sync data to cloud storage services including Google Drive, Amazon S3, MEGA, and Backblaze B2. Affiliates often rename the rclone binary to system process names such as `svchost.exe` to evade detection.
- **WinSCP**: Used for SFTP-based exfiltration to attacker-controlled servers.
- **FileZilla**: Another SFTP/FTP client used for data exfiltration.
- **MEGAsync**: The MEGA cloud storage desktop client, used for rapid exfiltration to MEGA accounts.
- **AzCopy**: Microsoft's Azure storage command-line utility, used for exfiltration to attacker-controlled Azure Blob storage containers.
- **Cyberduck**: Used by Qilin affiliates for multipart uploads to Backblaze B2 storage.
- **cURL**: Used in some cases for HTTP-based exfiltration to custom endpoints.

Organizations were able to successfully prevent only 3% of exfiltration attempts (Vectra AI), highlighting the difficulty of detecting and blocking data exfiltration once an attacker has established a foothold.

---

## 7. Financial Sector Targeting Trends

### 7.1 Why Financial Services is a Priority Target

The financial services sector is the highest-value ransomware target for several interconnected reasons:

1. **Data sensitivity**: Financial firms hold large volumes of PII, financial account data, trading histories, and proprietary business information. This data commands premium prices on criminal marketplaces and creates maximum extortion leverage.
2. **Regulatory pressure**: Financial services firms operate under stringent regulatory requirements (SEC, FINRA, state regulators, OCC, FFIEC) that impose significant consequences for data breaches, creating additional incentive to pay ransoms to avoid regulatory scrutiny.
3. **Operational criticality**: Downtime in financial services can result in direct financial losses, missed trading windows, failed settlements, and client impact that compounds rapidly.
4. **Payment capacity**: Financial services firms are perceived (often correctly) as having the financial resources to pay significant ransoms.
5. **Insurance coverage**: Many financial services firms carry substantial cyber insurance policies, which threat actors are increasingly aware of. Interlock ransomware has been observed stealing victims' cyber insurance policies and using them to calibrate ransom demands just below policy payout limits.
6. **Third-party ecosystem**: Financial services firms rely on extensive networks of third-party vendors, service providers, and technology platforms, creating numerous supply-chain attack vectors.

### 7.2 Industry Statistics

Financial services firms face the highest median ransom payments of any sector at approximately $2.0 million, with a mean payment of $3.3 million among firms that actually paid. 58% of demands to financial firms exceed $1 million, and 38% exceed $5 million.

A notable economic finding: firms that pay ransoms spend an average of $3 million on total recovery costs, while those that restore from backups average $375,000 — an 8x cost differential that increasingly drives the decision not to pay.

93% of investment management executives reported at least one cyber incident in 2025, yet only 24% use dedicated cybersecurity solutions — representing the widest gap between exposure and protection in any financial sub-sector.

### 7.3 Supply Chain Risk

The supply chain is an increasingly critical attack vector for financial services ransomware. Rather than attacking a well-defended financial institution directly, threat actors target smaller, less secure vendors and service providers that have access to the financial institution's data or network.

This pattern was clearly demonstrated in the Marquis Software Solutions attack (discussed in detail in Section 8), where the compromise of a single marketing and analytics vendor exposed data on over 1.4 million consumers across 74+ banking institutions. Similarly, the DBS/Toppan Next Tech incident involved a ransomware attack on a printing vendor that exposed brokerage customer data.

For Edward Jones, this risk is particularly relevant given our reliance on numerous third-party vendors for functions including technology infrastructure, marketing, compliance, data analytics, printing, and various back-office operations.

---

## 8. Recent Incidents Relevant to Edward Jones

### 8.1 Marquis Software Solutions (August 2025)

The Marquis Software Solutions attack is the most consequential financial sector supply-chain incident of 2025 and carries direct relevance to Edward Jones.

**Background**: Marquis is a Texas-based vendor providing marketing, compliance, and data analytics services to over 700 banking institutions across the United States. The company's services involve handling sensitive customer data on behalf of its financial services clients.

**Incident Details**: In August 2025, Marquis was compromised, likely via exploitation of a SonicWall SSL VPN vulnerability (CVE-2024-40766). The attackers exfiltrated data on more than 1.4 million consumers across 74+ banks and credit unions. The exposed data included names, Social Security numbers, financial account information, and debit/credit card numbers.

**Aftermath**: Marquis reportedly paid the ransom, but data still appeared on criminal marketplaces. A two-month gap between the breach and client notification (August to late October) has triggered multiple state Attorney General filings and class action investigations. The incident demonstrated that even when a vendor pays the ransom, there is no guarantee that stolen data will not be further distributed or sold.

**Relevance**: Edward Jones utilizes numerous third-party vendors that handle client data. An attack on any of these vendors could result in a similar outcome, with our clients' data being exposed regardless of the strength of our own security controls.

### 8.2 DBS Bank / Bank of China Singapore (April 2025)

**Background**: In April 2025, Toppan Next Tech, a printing vendor used by DBS Bank and Bank of China Singapore, was compromised in a ransomware attack.

**Incident Details**: The attack exposed data on approximately 8,200 DBS customers, most of whom were users of DBS Vickers — the bank's brokerage arm. The exposed data included names, addresses, and equity holdings details. An additional 3,000 Bank of China Singapore customers were affected.

**Relevance**: This incident is directly relevant to Edward Jones because it involved a brokerage operation and exposed the types of data that our firm holds — client names, addresses, and investment portfolio information. The attack vector was a printing vendor, a type of third party that many financial services firms would not consider a high-priority cybersecurity risk.

### 8.3 Wealth Management and Investment Firm Targeting

Several wealth management and investment firms appeared on ransomware leak sites in 2025:

- **Tufton Capital Management** ($810M AUM, Hunt Valley, Maryland) — a registered investment advisor with a profile very similar to an Edward Jones branch office.
- **FAS Wealth Partners** (Kansas City, Missouri) — a financial advisory firm.
- **Hudson Executive Capital LP** (New York City) — an SEC-registered investment advisor.
- **Duff Capital Investors** — an investment firm.
- **Betterment** — the major robo-advisor platform disclosed a breach in January 2026 exposing 1.4 million customers via a social engineering attack on a CRM vendor.

These incidents demonstrate that wealth management and investment advisory firms are actively being targeted by ransomware groups, and that firms of all sizes — from small independent advisors to major platforms — are at risk.

### 8.4 The $25.66 Million Ransom Case

A particularly noteworthy development from an October 2025 federal indictment: a financial services firm paid a $25.66 million ransom to BlackCat/ALPHV affiliates — two of whom turned out to be a ransomware negotiator at DigitalMint and an incident response manager at Sygnia Cybersecurity, operating as rogue affiliates. This case highlights the complex and sometimes corrupt ecosystem surrounding ransomware payments and negotiations.

---

## 9. MITRE ATT&CK Mapping

The following MITRE ATT&CK techniques are most commonly associated with the ransomware threat actors discussed in this report:

| Tactic | Technique ID | Technique Name | Description |
|--------|-------------|---------------|-------------|
| Initial Access | T1190 | Exploit Public-Facing Application | Exploitation of VPN, firewall, and web application vulnerabilities |
| Initial Access | T1078 | Valid Accounts | Use of stolen credentials from infostealers and IABs |
| Initial Access | T1566.001 | Spearphishing Attachment | Malicious email attachments |
| Initial Access | T1566.002 | Spearphishing Link | Malicious email links including ClickFix technique |
| Execution | T1059.001 | PowerShell | Post-exploitation scripting, UAC bypass, Defender disabling |
| Execution | T1059.003 | Windows Command Shell | General command execution |
| Execution | T1047 | WMI | Remote execution via Windows Management Instrumentation |
| Persistence | T1219 | Remote Access Software | AnyDesk, ScreenConnect, MeshAgent |
| Persistence | T1136.002 | Create Domain Account | Akira creates "itadm" account |
| Persistence | T1098 | Account Manipulation | Modification of existing accounts for persistence |
| Privilege Escalation | T1068 | Exploitation for Privilege Escalation | Veeam, SonicWall vulnerabilities |
| Privilege Escalation | T1558.003 | Kerberoasting | Service account credential extraction |
| Privilege Escalation | T1134 | Access Token Manipulation | Token impersonation and theft |
| Defense Evasion | T1562.001 | Disable or Modify Tools | BYOVD/EDRKillShifter to terminate security tools |
| Defense Evasion | T1055 | Process Injection | Most prevalent ATT&CK technique overall per Picus 2025 |
| Defense Evasion | T1036 | Masquerading | Renaming tools (e.g., rclone to svchost.exe) |
| Defense Evasion | T1112 | Modify Registry | WDigest credential storage modification |
| Credential Access | T1003 | OS Credential Dumping | Mimikatz, LSASS, DonPAPI |
| Credential Access | T1003.001 | LSASS Memory | Direct LSASS process memory access |
| Credential Access | T1555 | Credentials from Password Stores | Browser credential extraction |
| Discovery | T1018 | Remote System Discovery | Network scanning and enumeration |
| Discovery | T1082 | System Information Discovery | Host and domain enumeration |
| Discovery | T1069 | Permission Groups Discovery | Domain admin and privileged group identification |
| Lateral Movement | T1021.001 | Remote Desktop Protocol | Primary lateral movement method |
| Lateral Movement | T1021.002 | SMB/Windows Admin Shares | PsExec, Impacket-based execution |
| Collection | T1560 | Archive Collected Data | WinRAR, 7-Zip staging |
| Exfiltration | T1567 | Exfiltration Over Web Service | Rclone, MEGAsync, cloud storage |
| Exfiltration | T1048 | Exfiltration Over Alternative Protocol | SFTP via WinSCP, FileZilla |
| Impact | T1486 | Data Encrypted for Impact | File encryption (declining in prevalence) |
| Impact | T1490 | Inhibit System Recovery | Shadow copy deletion, backup destruction |
| Impact | T1489 | Service Stop | Termination of backup and security services |

---

## 10. Indicators of Compromise

### 10.1 Network Indicators

The following network-based indicators are associated with the threat actors discussed in this report. Note that threat actors frequently rotate their infrastructure, so these indicators may have limited shelf life.

**Qilin Associated Domains** (observed Q3-Q4 2025):
- Various .onion domains for negotiation and leak site (available upon request from CTI team)

**Akira Associated Infrastructure**:
- Akira negotiation portal accessible via Tor
- Known to use Cloudflare tunnels for C2 communications

**Common C2 Infrastructure Patterns**:
- Cobalt Strike Beacons using HTTPS on ports 443, 8443, and 8080
- Sliver implants communicating via mTLS or DNS
- RMM tools communicating to legitimate vendor infrastructure (AnyDesk relay servers, ScreenConnect cloud instances)

### 10.2 Host-Based Indicators

**Common File Artifacts**:
- Rclone binary renamed as `svchost.exe`, `svhost.exe`, or `explorer.exe`
- Akira ransomware extensions: `.akira`
- Qilin ransomware extensions: `.MmXReVIxLV` (varies per victim)
- Ransom notes: `akira_readme.txt`, `README-WARNING.txt` (Qilin)
- Registry modification: `HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest\UseLogonCredential` set to `1`
- New local admin accounts, particularly `itadm` (Akira)

**Common Process Artifacts**:
- Mimikatz execution (various process names, often packed)
- Lateral movement tools: psexec.exe, paexec.exe
- Network reconnaissance: Advanced IP Scanner, SoftPerfect Network Scanner
- Data staging: 7-Zip or WinRAR with command-line parameters indicating archiving of specific directories

---

## 11. Regulatory and Compliance Considerations

### 11.1 SEC Cybersecurity Disclosure Rules

The SEC's cybersecurity disclosure rules, which took effect in December 2023, require public companies to report material cybersecurity incidents within four business days via Form 8-K. For financial services firms, this creates a complex decision-making environment during a ransomware incident: the firm must simultaneously manage incident response, business continuity, client communications, regulatory notifications, and potential ransom negotiations, all under significant time pressure.

A coalition of financial trade associations including the Bank Policy Institute (BPI), American Bankers Association (ABA), and Securities Industry and Financial Markets Association (SIFMA) petitioned in May 2025 to rescind the rule, arguing it has been "weaponized as an extortion method" because threat actors can threaten to escalate publicity if the victim does not pay before the disclosure deadline. Under new SEC Chair Paul Atkins, the rule's future is uncertain, but organizations should continue to plan for compliance until any formal changes are made.

### 11.2 OFAC Sanctions Compliance

The Office of Foreign Assets Control (OFAC) maintains strict liability for payments to sanctioned entities, which creates significant legal risk for organizations considering ransomware payments. In 2025, OFAC expanded its sanctions designations relevant to the ransomware ecosystem, including sanctions against Zservers (a bulletproof hosting provider used by LockBit), Media Land LLC, and the Garantex cryptocurrency exchange network (which processed over $100 million in ransomware-linked transactions before being shut down and reconstituting as Grinex).

97% of ransomware payments continue to be made in Bitcoin (FinCEN data), and the laundering of these funds is becoming increasingly difficult due to enhanced blockchain analysis capabilities and international sanctions enforcement. However, the reconstitution of sanctioned services under new names (e.g., Garantex → Grinex) demonstrates that the cryptocurrency laundering infrastructure remains resilient.

For Edward Jones, any consideration of a ransom payment must include a thorough OFAC sanctions screening process, which adds complexity and time to an already time-pressured decision.

### 11.3 CISA CIRCIA Rule

CISA's Cyber Incident Reporting for Critical Infrastructure Act (CIRCIA) rule, expected to be finalized by October 2025, will require critical infrastructure entities (which includes financial services under the Financial Services Sector) to report ransomware payments within 24 hours. This represents a significant new compliance obligation that the Compliance and Legal teams should be tracking.

### 11.4 FINRA and State Regulatory Requirements

Financial services firms regulated by FINRA are subject to various cybersecurity-related requirements including Regulation S-P (safeguarding customer information), Regulation S-ID (identity theft prevention), and FINRA Rule 4370 (business continuity planning). A ransomware incident that impacts client data or operations could trigger multiple regulatory obligations simultaneously.

State regulators may impose additional requirements. Several states have enacted specific cybersecurity regulations for financial services firms, including the New York Department of Financial Services (NYDFS) Cybersecurity Regulation (23 NYCRR 500), which includes specific incident notification requirements and cybersecurity program mandates.

---

## 12. Recommendations

Based on the analysis presented in this report, the following recommendations are provided to reduce Edward Jones' exposure to the ransomware threats described:

### 12.1 Perimeter Hardening
- Ensure all internet-facing devices (VPN concentrators, firewalls, web application firewalls, load balancers) are patched against all known vulnerabilities, with priority given to the CVEs listed in Section 5.1.
- Implement multi-factor authentication on all VPN and remote access solutions.
- Conduct a review of all internet-facing assets using an external attack surface management (EASM) tool to identify and remediate any unauthorized or unknown internet-facing services.

### 12.2 Identity and Access Management
- Implement FIDO2-compliant multi-factor authentication across all user accounts, with priority given to privileged accounts.
- Deploy an advanced identity threat detection and response (ITDR) solution to detect credential abuse, Kerberoasting, pass-the-hash attacks, and other identity-based attack techniques.
- Implement privileged access management (PAM) controls for domain administrator and other high-privilege accounts.
- Review and restrict the use of service accounts, ensuring that service accounts have the minimum necessary privileges and use managed service accounts (gMSAs) where possible.

### 12.3 Endpoint Security
- Ensure endpoint detection and response (EDR) is deployed on all endpoints, including servers, with tamper protection enabled.
- Implement kernel-level driver loading restrictions to prevent BYOVD attacks. Consider implementing a driver allowlist policy.
- Block the execution of unauthorized RMM tools through application control policies.
- Monitor for signs of credential dumping, including LSASS process access and WDigest registry modifications.

### 12.4 Network Security
- Implement network segmentation to limit lateral movement opportunities.
- Monitor for unusual SMB traffic, RDP connections, and WMI activity between endpoints and servers.
- Deploy network detection and response (NDR) capabilities to detect C2 communications and data exfiltration.
- Block or alert on outbound connections to cloud storage services (MEGA, Backblaze, etc.) from servers and non-standard endpoints.

### 12.5 Data Protection and Backup
- Maintain offline (air-gapped) backups of critical systems and data.
- Test backup restoration procedures regularly to ensure recovery capabilities are functional.
- Implement data loss prevention (DLP) controls to detect and prevent large-scale data exfiltration.
- Consider deploying data classification tools to identify and protect the most sensitive data assets.

### 12.6 Third-Party Risk Management
- Review the cybersecurity posture of all critical third-party vendors, with particular attention to those handling client PII and financial data.
- Require third-party vendors to demonstrate adequate security controls, including patching programs, MFA, EDR, and incident response capabilities.
- Consider implementing contractual requirements for prompt breach notification from vendors.
- Monitor dark web forums and marketplaces for mentions of Edward Jones vendors.

### 12.7 Incident Response Preparedness
- Update the ransomware incident response playbook to reflect the current threat landscape, including data extortion-only scenarios.
- Conduct tabletop exercises involving ransomware scenarios, ensuring that key stakeholders (Legal, Compliance, Communications, Executive Leadership) are included.
- Establish relationships with external incident response firms, legal counsel, and ransomware negotiation services in advance of any incident.
- Pre-establish a decision framework for ransom payment decisions, including OFAC screening procedures and executive authorization requirements.

### 12.8 Security Awareness
- Conduct regular phishing simulation exercises, including AI-generated phishing templates, ClickFix scenarios, and vishing (voice phishing) scenarios targeting help desk personnel.
- Educate employees about the threat of infostealer malware, including risks associated with downloading software from unofficial sources, using personal devices for work-related activities, and saving corporate credentials in browsers.

---

## 13. Conclusion

The ransomware threat to Edward Jones is assessed as HIGH based on the analysis presented in this report. The financial services sector is the highest-value target for ransomware operators, and the specific characteristics of our organization — including our large client base, distributed branch network, extensive third-party vendor ecosystem, and the sensitivity of the client data we hold — make us a particularly attractive target.

The most likely threat actors to target a firm with our profile in early 2026 are Qilin (which has demonstrated financial sector focus and is the highest-volume operator), Akira (which has consistent financial sector targeting and is the subject of a CISA advisory), and Medusa (which explicitly listed financial services in its CISA advisory and is known for aggressive triple extortion tactics). The risk of supply-chain compromise through a third-party vendor is also elevated based on the Marquis and DBS/Toppan incidents.

The shift from encryption-first to data-theft-first extortion is particularly concerning for our organization, as client financial data carries premium value on criminal marketplaces regardless of whether a ransom is paid. The emergence of insurance policy theft as a negotiation weapon (as demonstrated by Interlock) suggests that attackers are becoming increasingly sophisticated in understanding the financial dynamics of their targets.

It is imperative that the organization continue to invest in the security controls and capabilities recommended in Section 12, with particular urgency around perimeter hardening, identity security, and third-party risk management.

---

## 14. References

1. Check Point Research, "The State of Ransomware – Q3 2025"
2. Check Point Research, "The State of Ransomware – Q2 2025"
3. Nordstellar, "Ransomware Stats 2025: A Year-End Review of Global Threats"
4. Cybersecurity News, "Ransomware Attack 2025 Recap"
5. Flashpoint, "The Top Threat Actor Groups Targeting the Financial Sector"
6. SOCRadar, "Top 10 Ransomware Groups of 2025"
7. SOCRadar, "Top 10 Ransomware Attacks of 2025"
8. Cyble, "Ransomware Attacks Surge 30% In October 2025"
9. Cyberint (Check Point), "Qilin Ransomware: Get the 2025 Lowdown"
10. Darktrace, "Qilin RaaS: Darktrace Detection Insights"
11. CISA Advisory AA24-109A, "#StopRansomware: Akira Ransomware" (Updated November 2025)
12. CISA Advisory AA25-071A, "#StopRansomware: Medusa Ransomware" (March 2025)
13. Halcyon, "Power Rankings: Ransomware Malicious Quartile Q2-2025"
14. MOXFIVE, "Threat Actor Spotlight: INC Ransom"
15. Picus Security, "The Top Ten MITRE ATT&CK Techniques"
16. KELA Cyber, "Ransomware Threat Actor Profile: Qilin"
17. Mandiant / Google Cloud, "M-Trends 2025"
18. BlackFog, "The State of Ransomware 2026"
19. CYFIRMA, "Tracking Ransomware: January 2026"
20. Chainalysis, "Crypto Ransomware: 2026 Crypto Crime Report"
21. Bleeping Computer, "Marquis data breach impacts over 74 US banks, credit unions"
22. TechCrunch, "Fintech firm Marquis alerts dozens of US banks and credit unions of a data breach after ransomware attack"
23. BankInfoSecurity, "More Banks Issue Breach Notifications Over Supplier Breach"
24. SOCRadar, "Dark Web Profile: Medusa Ransomware (MedusaLocker)"
25. Blackpoint, "Clop Ransomware" Threat Profile
26. Infosecurity Magazine, "Threat Actors Favor Rclone, WinSCP and cURL as Data Exfiltration Tools"
27. DeepStrike, "Data Breach in Financial Institutions 2025: A CISO's Guide"
28. DeepStrike, "Compromised Credential Statistics 2025"
29. Invenio IT, "Ransomware attacks in finance hit new high (Updated for 2026)"
30. Kiteworks, "Wealth Management Cybersecurity: Protecting Assets From Cyber Threats"
31. HIPAA Journal, "Cyber Insurance Claims Fall But Ransomware Losses Increase"

---

*This report will be updated as new intelligence becomes available. For questions regarding this report, contact the Cyber Threat Intelligence team.*

*© 2026 Edward Jones. Internal Use Only. Distribution restricted per TLP:AMBER guidelines.*
