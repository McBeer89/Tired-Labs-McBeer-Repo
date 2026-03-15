# Filtering Decisions — Executive Threat Brief (CISO)

**Derived From:** Research Base — Ransomware Threat to Financial Services (Q1 2026) / IR-01  
**Derivative Type:** Executive Threat Brief  
**Consumer:** Karen Whitfield, CISO  
**Decisions Informed:** (1) Budget and resource allocation, (2) Patching escalation  
**Date:** March 15, 2026  

---

## Inclusion Test Applied

For every element in the research base:

1. **Who is reading this?** → Karen Whitfield, CISO  
2. **What decisions are they making?** → Budget and resource allocation; Patching escalation  
3. **Does this element help her make those decisions?**

---

## INCLUDED

### Key Judgments

| Element | Reason for Inclusion |
|---|---|
| **KJ-1 (Primary Threat Groups)** | The CISO needs to know who is actively targeting firms like Hartwell to justify where budget goes. The Qilin MSP cascade (28 firms) and Akira/Marquis incident (74+ banks) frame the scale of threat for budget conversations. |
| **KJ-2 (Supply Chain vs. Direct Entry)** | Directly informs resource allocation: should budget prioritize perimeter hardening or third-party risk management? The finding that 6 of 8 confirmed FS incidents came through vendors, plus the 14,500-branch vendor surface area, is a resource allocation argument. |
| **KJ-3 (EDR Evasion / BYOVD)** | Directly informs budget: EDR alone is insufficient. Reynolds ransomware specifically terminates CrowdStrike Falcon (Hartwell's primary EDR). Justifies investment in defense-in-depth — network segmentation, identity-based detection, non-traditional endpoint coverage. |
| **KJ-4 (Payment Model Structural Change)** | Informs budget context for incident planning: payment rates collapsing while demands against FS remain highest ($2.0M median). Data-theft-first extortion means Hartwell's client PII is the target regardless of whether a ransom is paid. Shapes board-level risk framing. |
| **KJ-5 (Active Fortinet Threat)** | Highest-priority patching escalation item. Three Fortinet CVEs in the reporting window, pre-ransomware activity via FortiGate confirmed March 2026. This is the "act now" item. |

### Supporting Evidence (Selective)

| Element | Reason for Inclusion |
|---|---|
| **Section 2.8 — Fortinet CVEs (2.8.1–2.8.5)** | Directly supports the patching escalation decision. Three CVEs, CISA KEV entries, confirmed active exploitation. |
| **Section 2.8 — Veeam CVEs (2.8.9–2.8.11)** | Hartwell runs Veeam; CVE-2024-40711 is CVSS 9.8 with confirmed ransomware exploitation by Akira, Fog, and Frag. Patch status unknown (GAP-003). Patching escalation item. |
| **Section 2.8 — GoAnywhere MFT (2.8.12)** | Hartwell runs GoAnywhere; CVE-2025-10035 is CVSS 10.0, exploited by Medusa affiliate. Patch status unknown (GAP-003). Patching escalation item. |
| **Section 2.8 — Palo Alto (2.8.6)** | Hartwell runs Palo Alto in data centers. CVE-2025-0108 with confirmed exploitation. Patching escalation item. |
| **Section 2.10 — Marquis and DBS/Toppan incidents** | Both are supply-chain incidents involving vendors comparable to Hartwell's ecosystem. DBS/Toppan mirrors Hartwell's own April 2025 printing vendor breach. Powerful budget justification. |
| **Section 2.17/2.18/2.20 — Ransom economics summary** | $2.0M median demand, $2.58M mean recovery cost, $5.56M per-incident breach cost (IBM). Budget justification context — the cost of inaction. |
| **Section 2.21 — Extortion model evolution** | Data-theft-first (encryption in only 49% of FS attacks), insurance policy theft, SWATting, cold-calling clients. Shapes the CISO's understanding of what a realistic incident looks like now. |

### Gaps and Assumptions

| Element | Reason for Inclusion |
|---|---|
| **GAP-003 (missing Veeam/GoAnywhere version data)** | Directly actionable: the CISO can direct Vuln Mgmt to provide this data. Patching escalation can't be completed without it. |
| **GAP-R01 (all confidence LOW due to source limitation)** | The CISO needs to know the confidence basis for these findings. |
| **GAP-006 (no threat hunting capability)** | Resource allocation item — cannot validate whether identified TTPs are present in Hartwell's environment without this capability. |

### Analytical Framework

| Element | Reason for Inclusion |
|---|---|
| **Competing Hypotheses (summary only)** | Frames the "where to invest" question: all three vectors are active simultaneously; the key question is which represents the greatest unmitigated risk. |

---

## EXCLUDED

### Key Judgment Detail

| Element | Reason for Exclusion |
|---|---|
| **KJ-1 detail on Qilin affiliate split percentages (2.2.6b)** | Criminal business model internals don't inform CISO budget or patching decisions. |

### Sections Excluded in Full (Claim-Level Detail)

| Element | Reason for Exclusion |
|---|---|
| **Section 2.1 (Ecosystem Scale/Fragmentation detail)** | Background context for analysts, not decision-useful for the CISO. Headline numbers (126–141 groups, 451 FS cases) appear as contextual framing only. |
| **Sections 2.2–2.7 (Individual group profiles at claim level)** | The CISO needs to know the top groups and why they matter to Hartwell (covered in KJ-1), not the claim-by-claim evidence trail. |
| **Section 2.9 (Credential-based initial access detail)** | The ClickFix stat and credential pipeline concept are noted in KJ context, but the full evidence chain (Mimikatz modules, Rubeus procedures, WDigest registry keys) is detection/IR-level detail. |
| **Sections 2.11–2.14 (C2, RMM abuse, lateral movement, exfiltration — procedure-level detail)** | Detection Engineering and IR brief material. The CISO doesn't need Rclone percentages or Mimikatz module names. |
| **Section 2.15 (BYOVD claim-level detail)** | EDR evasion trend captured in KJ-3; per-claim evidence (2,500 driver variants, QuadSwitcher identity) stays in the research base. |
| **Section 2.16 (ATT&CK Summary)** | Technical framework reference, not executive-level. |
| **Section 2.19 (Revenue/Financial Flows detail)** | Compliance brief material. The CISO needs the demand/cost numbers (included via 2.17/2.20), not on-chain payment flow detail. |

### CVEs Not in Hartwell's Stack

| Element | Reason for Exclusion |
|---|---|
| **Citrix NetScaler (2.8.13)** | Not in Hartwell's technology stack. |
| **Oracle EBS (2.8.16)** | Not in Hartwell's technology stack. |
| **VMware ESXi (2.8.14)** | Not confirmed in Hartwell's stack at executive decision level. |
| **Windows CLFS (2.8.15)** | OS-level vulnerability; not a perimeter patching escalation item. |
| **SonicWall (2.8.8)** | Appears via Marquis incident narrative but is not a Hartwell perimeter device. |

### Gaps and Assumptions (Analyst-Internal)

| Element | Reason for Exclusion |
|---|---|
| **ASMP-05 (Qilin affiliate split assumption)** | Internal analyst assumption about criminal economics. |
| **GAP-R02 through GAP-R05 (research-level source gaps)** | Analyst workflow items, not CISO decision items. GAP-R01 is included as the representative confidence caveat. |

### Research Base Internal Sections

| Element | Reason for Exclusion |
|---|---|
| **Section 6 (Full Source List)** | Internal documentation. |
| **Section 7 (Version History)** | Internal tracking. |
| **Section 8 (Next Actions for analysts)** | Analyst workflow. Some actions reframed as CISO-directed recommendations in the derivative. |

---

*This filtering record is retained as part of the derivative production audit trail.*
