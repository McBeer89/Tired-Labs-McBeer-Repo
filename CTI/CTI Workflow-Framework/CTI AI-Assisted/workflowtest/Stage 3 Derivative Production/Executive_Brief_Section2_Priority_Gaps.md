# Executive Threat Brief — Section 2: Priority Gaps

**Derived From:** Research Base — Ransomware Threat to Financial Services (Q1 2026) / IR-01  
**Date:** March 15, 2026  
**Consumer:** Karen Whitfield, CISO  
**Question Answered:** What is the current ransomware threat to Hartwell, and what should we prioritize for budget/resource allocation and patching escalation?  
**Classification:** INTERNAL  

---

**Gap 1: Unknown patch status for backup and file transfer systems.**  
Our threat intelligence team has identified critical vulnerabilities with confirmed ransomware exploitation in our backup platform (CVSS 9.8) and managed file transfer system (CVSS 10.0), but cannot confirm whether we are exposed because version and patch data is unavailable to them. **To close:** Direct vulnerability management to provide current version and patch status for both systems. This is a coordination task, not a budget item — it requires a standing data-sharing agreement between vulnerability management and the threat intelligence team to prevent recurrence.

**Gap 2: No threat hunting capability to validate whether active threats are already present.**  
Our threat intelligence can identify the techniques ransomware groups are using against financial services firms, but we have no dedicated capability to search our environment for evidence of those techniques. Threat hunting is currently ad-hoc, performed by senior SOC analysts when time permits. **To close:** Establish a dedicated threat hunting function — minimum two FTEs with access to our security telemetry and endpoint detection platform. Alternatively, contract a managed threat hunting service at approximately $15,000–$30,000/month, which could be operational within 30 days versus 3–6 months for hiring.

**Gap 3: No dark web monitoring to detect stolen credentials or leaked data.**  
Our January 2025 infostealer incident confirmed credential harvesting from a branch workstation, but we have no capability to determine whether those credentials appeared in criminal marketplaces. Compromised credentials account for 41% of ransomware root causes (Sophos, 2025 Active Adversary Report). **To close:** Approve the previously requested dark web monitoring budget. This closes both a detection gap (stolen credentials before they are used) and an incident response gap (confirming data exposure after a breach).

**Gap 4: Vendor notification timelines are not contractually enforced.**  
Our April 2025 printing vendor breach demonstrated the problem: 18 days elapsed between the vendor discovering the breach and notifying Hartwell, with no contractual requirement for faster notification. Six of eight confirmed financial services incidents in this research involved vendor compromise. **To close:** Direct the legal and procurement teams to add mandatory breach notification timelines (48–72 hours) and security attestation requirements to all vendor contracts handling client data. This is a legal and procurement workstream, not a technology investment — but it requires CISO sponsorship to prioritize.

**Gap 5: All findings in this brief carry low confidence due to source verification limitations.**  
The underlying research has not yet been independently verified against primary sources. Multiple findings — particularly the ransom economics data — are corroborated by three or more named sources and are strong candidates for confidence upgrade upon verification. **To close:** The threat intelligence team needs 5–7 business days to verify priority claims against primary sources (CISA advisories, vendor reports, Chainalysis data). No additional budget required — this is an analyst workflow item. Patching escalation actions in this brief (Priorities 1 and 4) should not wait for confidence upgrades; the Fortinet vulnerabilities are binary-verifiable against the CISA Known Exploited Vulnerabilities catalog.

---

*CTI Team Contact: Dana Mercer, Senior Analyst — Cyber Threat Intelligence*
