# Gate 3 — Relevance Evaluation
## Analyst: Junior Analyst 1
## Date: March 15, 2026

For each claim below, evaluate: does this help answer the intelligence requirement?

Your stated requirements:
- **PIR-01.1:** Which ransomware groups have conducted confirmed intrusions against financial services firms in the past 90 days, and what initial access methods did they use?
- **PIR-01.2:** What specific tools, techniques, and procedures — at the procedure level — are these groups using in current campaigns, including evasion techniques targeting EDR platforms?
- **PIR-01.3:** What is the current ransom demand range, payment rate, and double-extortion model for groups actively targeting financial services?

For each claim, respond with:
- **RELEVANT** — directly helps answer the requirement
- **PARTIALLY RELEVANT** — tangentially related; may support context but doesn't directly answer the requirement
- **NOT RELEVANT** — does not help answer the requirement
- **UNSURE** — you need to think about it or discuss

**Be aggressive with NOT RELEVANT.** If a claim is interesting but doesn't serve PIR-01.1, 01.2, or 01.3, it doesn't belong in this research base. It may belong in a different research base under a different PIR.

---

## PIR-01.1 Claims — Groups and Confirmed Intrusions

### Ecosystem-Level (Claims 1–6)

1. 126–141 active ransomware groups operated in 2025, up from ~70 in 2023.
2. Financial sector recorded 451 ransomware cases in 2025.
3. 23% increase in extortion attacks to 6,182 globally in 2025.
4. 406 publicly disclosed financial sector ransomware victims from April 2024–April 2025 (~7% of all listings).
5. RansomHub, Black Basta, 8Base, BianLian, and Cactus all ceased operations between January and April 2025; displaced affiliates migrated to surviving and new operations.
6. 57 new ransomware groups and 27 new extortion groups emerged in 2025.

### Qilin (Claims 7–12)

7. Qilin had 946 victims by year-end 2025, including 69 confirmed finance-sector targets among 590 business attacks by October 2025.
8. Qilin's September 2025 "Korean Leaks" campaign compromised MSP GJTec to breach 28 South Korean asset management firms, exfiltrating over 1 million files.
9. Bitdefender linked the Qilin Korean campaign to potential North Korean state-affiliated involvement via Moonstone Sleet.
10. Qilin absorbed affiliates from defunct RansomHub after RansomHub ceased operations April 2025, significantly increasing its attack volume.
11. Qilin stole 2.5 TB from Habib Bank AG Zurich.
12. Qilin's Rust-based payload targets Windows, Linux, and VMware ESXi; its RaaS model offers affiliates 80–85% of ransom proceeds.

### Akira (Claims 13–18)

13. Akira had approximately 717–740 leak site postings and an estimated $244 million in total extortion revenue since launch.
14. Akira's August 14, 2025, attack on Marquis Software Solutions (vendor to 700+ banks) compromised over 400,000 consumers across 74+ institutions via CVE-2024-40766 (SonicWall VPN).
15. Flashpoint attributed 34 financial sector victims to Akira from April 2024 to April 2025.
16. CISA/FBI advisory (updated November 2025) confirmed Akira's continued targeting of financial institutions.
17. Akira exploits VPN infrastructure without MFA — particularly Cisco and SonicWall appliances.
18. In March 2025, Akira bypassed EDR by encrypting a network from an unsecured IoT webcam after EDR quarantined the initial payload.

### Clop (Claims 19–22)

19. Clop added 500+ victims in 2025 through campaigns against Cleo MFT (CVE-2024-50623/CVE-2024-55956) and Oracle EBS (CVE-2025-61882).
20. Clop's Cleo campaign included Western Alliance Bank (21,899 customers, SSNs stolen).
21. Clop demanded up to $50 million from individual organizations in the Oracle EBS campaign.
22. Clop operates as a pure data-extortion group (no encryption); its supply-chain methodology creates outsized exposure for financial firms reliant on shared technology platforms.

### RansomHub (Claims 23–24)

23. RansomHub led all groups in financial sector targeting with 38 confirmed financial victims from April 2024–April 2025 before ceasing operations April 1, 2025.
24. DragonForce claimed RansomHub migrated to its infrastructure.

### Medusa (Claims 25–26)

25. Medusa received joint CISA/FBI/MS-ISAC advisory AA25-071A (March 12, 2025) after exceeding 300 victims, with demands ranging from $100,000 to $15 million.
26. North Korean Lazarus Group actors were discovered deploying Medusa ransomware against Middle Eastern financial institutions.

### Play (Claim 27)

27. Play has compromised approximately 900 entities since mid-2022 and remained consistently active throughout 2025 among top five groups.

### LockBit (Claims 28–30)

28. LockBit attempted recovery with LockBit 4.0 (February 2025) and 5.0 (September 2025) but suffered a second infrastructure breach in May 2025 exposing affiliate details.
29. LockBit affiliate fees dropped to $500 to compete.
30. Key LockBit developer Rostislav Panev was extradited to the U.S. after arrest in Israel.

### Black Basta (Claims 31–33)

31. Black Basta collapsed in January 2025, with 200,000 internal messages leaked on February 11, 2025.
32. German federal police identified Oleg Evgenievich Nefedov as key Black Basta leader "GG."
33. Former Black Basta members migrated to Cactus and SafePay groups.

### Emerging Groups (Claims 34–36)

34. DragonForce introduced a "cartel model" in April 2025 allowing affiliates to operate under their own branding, claiming 200+ victims.
35. SafePay surged to 58 claimed victims in May 2025.
36. Hunters International rebranded as World Leaks (data-theft-only), targeting a third-party supplier of UBS in June 2025 and publishing data on 130,000 UBS employees.

### CVEs Actively Exploited (Claims 37–52)

37. Fortinet FortiGate has had 14 zero-day advisories in under 4 years.
38. CVE-2024-55591 (FortiOS): CVSS 9.6, auth bypass, ~48K devices vulnerable. CISA KEV Jan 2025. Multiple ransomware groups exploiting.
39. CVE-2025-59718/59719 (FortiCloud SSO bypass): CVSS 9.8, active intrusions within 3 days. CISA KEV Dec 2025.
40. CVE-2026-24858 (FortiGate cross-account SSO bypass): ~10K instances. CISA advisory Jan 2026.
41. SentinelOne documented campaigns using FortiGate as entry points with pre-ransomware activity as of March 2026.
42. CVE-2025-0108 (Palo Alto PAN-OS): CVSS 8.8, auth bypass, confirmed exploitation Feb 2025. CISA KEV.
43. Chinese group Emperor Dragonfly used Palo Alto exploits for RA World ransomware deployment.
44. CVE-2024-40766 (SonicWall SSL VPN): Akira's primary target; vector in Marquis attack (74+ banks).
45. CVE-2024-40711 (Veeam Backup): CVSS 9.8, exploited by Akira/Fog/Frag. CISA KEV Oct 2024. Marked "Known" for ransomware use.
46. Rapid7: 20%+ of 2024 IR cases involved Veeam exploitation.
47. CVE-2025-23120 (Veeam): CVSS 9.9, domain user RCE when backup server is domain-joined.
48. CVE-2025-10035 (GoAnywhere MFT): CVSS 10.0, exploited by Storm-1175/Medusa since Sep 2025. CISA KEV.
49. CVE-2025-5777 (Citrix NetScaler "CitrixBleed 2"): CVSS 9.3, 11.5M exploitation attempts, 40% targeting financial services. CISA KEV.
50. CVE-2025-22224/22225/22226 (VMware ESXi): VM escape chain, confirmed ransomware use. CISA KEV Feb 2026.
51. CVE-2025-29824 (Windows CLFS): Exploited by Storm-2460 targeting Venezuelan financial entity; used by Play-linked Balloonfly. CISA KEV.
52. CVE-2025-61882 (Oracle EBS): SSRF/XSL RCE exploited by Clop for mass financial data theft.

### Credential-Based Initial Access (Claims 53–62)

53. Vulnerability exploitation accounts for 33% of initial access cases.
54. Compromised credentials account for 41% of root causes.
55. Edge/VPN device exploitation jumped from 3% to 22% between 2023–2024.
56. 90% of ransomware incidents exploited firewalls; fastest chain: breach-to-encryption in 3 hours, lateral movement in 10 minutes.
57. MFA absent in 59% of cases; 67.32% of root causes identity-related.
58. 75% of initial access attempts are malware-free, relying on credentials and identity misuse.
59. ClickFix surged 517% in 2025, becoming second most common attack vector.
60. Microsoft identified May 2025 ClickFix campaign targeting Portuguese financial services with Lampion.
61. Sophos documented complete ClickFix → StealC → Qilin ransomware chain.
62. Nation-state actors (MuddyWater, APT28) adopted ClickFix.

### Confirmed Financial Sector Incidents (Claims 63–71)

63. Marquis Software Solutions (Aug 2025): Akira via SonicWall, 400K+ consumers, 74+ banks, SSNs, two-month notification delay.
64. DBS Bank/Bank of China Singapore (Apr 2025): Vendor Toppan Next Tech, 8,200 DBS customers (brokerage), 3,000 BOC.
65. SitusAMC (Nov 2025): Affected JPMorgan, Citi, Morgan Stanley via mortgage tech vendor.
66. Prosper Marketplace: 17.6M customers — largest single FS breach of 2025.
67. Insight Partners: $90B+ AUM PE firm, 83-day dwell time.
68. Betterment (Jan 2026): 1.4M customers via social engineering on CRM vendor.
69. Multiple wealth management firms on leak sites: Tufton Capital ($810M AUM), FAS Wealth Partners, Hudson Executive Capital, Duff Capital Investors.
70. FS firm paid $25.66M to BlackCat/ALPHV affiliates; two affiliates were a ransomware negotiator and IR manager.
71. Western Alliance Bank: 21,899 customers, SSNs stolen via Clop/Cleo.

---

## PIR-01.2 Claims — TTPs at Procedure Level

### C2 (Claims 72–73)

72. Cobalt Strike dominant C2; supplemented by Sliver, Brute Ratel C4, Havoc with Graph API integration.
73. Emerging C2: GC2 (Google Sheets, Fog ransomware), Adaptix.

### RMM Abuse (Claims 74–78)

74. RMM abuse in 36% of IR cases; 32 different RMM tools documented.
75. UNC5952 used signed ScreenConnect droppers targeting financial organizations.
76. AnyDesk used by Mad Liberator, Medusa, Rhysida, Cactus.
77. Black Basta leaked chats confirmed systematic RMM abuse.
78. Akira installed Datto RMM on domain controllers.

### Credential Harvesting and Lateral Movement (Claims 79–86)

79. Mimikatz for LSASS dumping (sekurlsa::logonpasswords most-used module).
80. Rubeus for Kerberoasting documented in Akira's attack chain.
81. DCSync for KRBTGT hash extraction enabling Golden Ticket creation.
82. Median time to AD compromise: 11 hours.
83. 62% of compromised AD servers ran out-of-support OS.
84. Qilin modifies WDigest registry key to force plaintext credential storage.
85. Akira dumps Veeam backup credentials via PowerShell.
86. Lateral movement: RDP, PsExec/PAExec, WMI, Impacket; primary target VMware ESXi hypervisors.

### Exfiltration (Claims 87–92)

87. Rclone in 57% of incidents; LockBit, Black Basta, BlackSuit, Medusa; uploads to MEGA.io.
88. WinSCP second; cURL third; FileZilla by INC Ransom for FTP.
89. Exfiltration median 72.98 hours after attack initiation.
90. 83% of ransomware deployed off-hours; 79% of exfiltration off-hours.
91. 96% of attacks involved data exfiltration.
92. Cyberduck used by Qilin for multipart uploads to Backblaze.

### BYOVD and EDR Evasion (Claims 93–98)

93. 2,500+ BYOVD driver variants in single campaign targeting TrueSight driver.
94. EDRKillShifter used by 8+ groups: RansomHub, Medusa, BianLian, Play, BlackSuit, Qilin, DragonForce, INC Ransom.
95. ESET identified "QuadSwitcher" orchestrating cross-group EDRKillShifter use.
96. Reynolds ransomware (Feb 2026) embedded vulnerable driver in payload, terminating Falcon, Cortex XDR, Sophos, Symantec.
97. Akira pivoted to unmonitored Linux webcam after EDR quarantine.
98. Process injection (T1055) is #1 most prevalent technique overall.

### MITRE ATT&CK Composite (Claims 99–103)

99. T1190 primary initial access; edge devices: Fortinet, Ivanti, Citrix, SonicWall, Palo Alto.
100. T1078 (Valid Accounts): 33–41% of initial access.
101. T1562.001 (Disable Security Tools) via BYOVD is dominant defense evasion of 2025.
102. T1567 (Exfiltration to Cloud Storage) via Rclone in 57% of incidents.
103. T1486 (Data Encrypted for Impact) declining — only 50% of attacks in 2025.

---

## PIR-01.3 Claims — Economics, Payment Rates, Extortion Models

### Demand Ranges (Claims 104–109)

104. FS highest median ransom: $2.0 million.
105. 51% of FS victims paid; 18% paid full demand; avg 75% of initial ask.
106. Initial demands surged 47% YoY in 2025.
107. Medusa demands: $100K–$15M.
108. Clop demanded up to $50M per org (Oracle campaign).
109. FS firm paid $25.66M to BlackCat/ALPHV affiliates.

### Payment Rates (Claims 110–113)

110. 28% of victims paid in 2025 — record low.
111. Payment rates fell from 25% (Q4 2024) to ~20% by Q4 2025.
112. 86% of businesses refused to pay in 2025.
113. Data-extortion-only payment rate: 19%.

### Revenue and Flows (Claims 114–119)

114. Total on-chain payments: ~$820M in 2025 (8% decline from $892M).
115. Median on-chain payments jumped 368% to ~$59,556.
116. FinCEN: $2.1B+ reported 2022–2024; $365.6M from 432 FS incidents.
117. 97% of payments in Bitcoin.
118. Bridge-related laundering up 66%; mixer use down 37%.
119. OFAC designations 2025: Zservers, AEZA, Grinex, Media Land LLC.

### Recovery Costs (Claims 120–122)

120. Mean FS recovery cost: $2.58M excluding ransom.
121. IBM: FS breach cost $5.56M per incident.
122. Backup recovery: $375K avg vs $3M for payers.

### Extortion Model Evolution (Claims 123–128)

123. Encryption in only 50% of attacks in 2025 — six-year low.
124. FS lowest encryption rate: 49%, down from 81% in 2023.
125. Clop and World Leaks skip encryption; Qilin, Akira, Play favor double extortion.
126. Triple extortion: SWATting executives, bribing employees.
127. Attackers stealing cyber insurance policies to calibrate demands below policy limits.
128. Akira cold-calling employees and clients of victim companies as pressure tactic.
