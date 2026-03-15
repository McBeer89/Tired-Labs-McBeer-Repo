# Hartwell & Associates — CTI Intelligence Requirements & Collection Plan

**Date:** March 2026
**Prepared by:** CTI Team (Dana Mercer, Senior Analyst)
**Review cycle:** IRs semi-annually; PIRs quarterly
**Note:** These requirements are based on analyst knowledge of consumers, not direct consumer input. Validation with each consumer is recommended.

---

## 1. Intelligence Requirements

| IR ID | Intelligence Requirement | Consumer(s) | Review Cycle |
|---|---|---|---|
| IR-01 | What ransomware groups are actively targeting the financial services sector, and what are their current tactics, techniques, and procedures? | CISO, Detection Engineering, IR, Red Team (NCC Group) | Semi-annual |
| IR-02 | What vulnerabilities in Hartwell's deployed technology stack are being actively exploited in the wild? | CISO, Detection Engineering, IR | Semi-annual |
| IR-03 | What third-party and supply chain compromises pose a risk to Hartwell and its client data? | CISO, IR | Semi-annual |
| IR-04 | What credential theft, infostealer, and initial access broker activity targets or exposes Hartwell employees and systems? | CISO, Detection Engineering, IR | Semi-annual |
| IR-05 | What social engineering campaigns — including client-facing brand impersonation — are targeting Hartwell or the financial services sector? | CISO, Detection Engineering, IR | Semi-annual |

---

## 2. Priority Intelligence Requirements

**Default reporting period:** Past 90 days (extend further back when the 90-day window returns insufficient results).

### Under IR-01: Ransomware groups targeting financial services

| PIR ID | Priority Intelligence Requirement | Cadence |
|---|---|---|
| PIR-01.1 | Which ransomware groups have conducted confirmed intrusions against financial services firms in the past 90 days, and what initial access methods did they use? | Quarterly |
| PIR-01.2 | What specific tools, techniques, and procedures — at the procedure level — are these groups using in current campaigns, including evasion techniques targeting EDR platforms? | Quarterly |
| PIR-01.3 | What is the current ransom demand range, payment rate, and double-extortion model for groups actively targeting financial services? | Quarterly |

### Under IR-02: Vulnerability exploitation in Hartwell's stack

| PIR ID | Priority Intelligence Requirement | Cadence |
|---|---|---|
| PIR-02.1 | Which CVEs affecting Hartwell's deployed products (Fortinet FortiGate, Cisco AnyConnect, Palo Alto Networks, Veeam, GoAnywhere MFT, Microsoft Exchange Online, Entra ID, CrowdStrike Falcon) have been added to CISA KEV or observed in active exploitation in the past 90 days? | Quarterly |
| PIR-02.2 | For actively exploited CVEs affecting Hartwell's stack, what does exploitation look like in telemetry — what artifacts, log sources, and event IDs indicate successful or attempted exploitation? | Quarterly |
| PIR-02.3 | Are threat groups specifically chaining vulnerabilities in Hartwell's stack as part of broader intrusion campaigns? | Quarterly |

### Under IR-03: Third-party and supply chain risk

| PIR ID | Priority Intelligence Requirement | Cadence |
|---|---|---|
| PIR-03.1 | Which third-party products or service providers in Hartwell's vendor ecosystem have disclosed breaches or been identified as compromised in the past 90 days? | Quarterly |
| PIR-03.2 | What threat groups are conducting supply chain compromises against financial services firms or their vendors, and what is their operational pattern? | Quarterly |
| PIR-03.3 | What types of Hartwell client data are at risk through third-party exposure based on current supply chain compromise patterns targeting the financial services sector? | Quarterly |

### Under IR-04: Credential theft and initial access broker activity

| PIR ID | Priority Intelligence Requirement | Cadence |
|---|---|---|
| PIR-04.1 | Which infostealer families are currently active against the financial services sector, what are their delivery mechanisms, and what credentials or session tokens do they harvest? | Quarterly |
| PIR-04.2 | Are Hartwell employee credentials, session tokens, or internal system access appearing in dark web marketplaces, initial access broker listings, or credential dumps? | Quarterly |
| PIR-04.3 | What initial access broker activity is relevant to Hartwell — are brokers advertising access to financial services firms of similar size, geography, or technology stack? | Quarterly |

### Under IR-05: Social engineering and brand impersonation

| PIR ID | Priority Intelligence Requirement | Cadence |
|---|---|---|
| PIR-05.1 | What phishing, vishing, or social engineering campaigns have targeted Hartwell employees or clients in the past 90 days, and what delivery techniques were used? | Quarterly |
| PIR-05.2 | Are there active lookalike domains, brand impersonation sites, or fraudulent social media accounts using Hartwell's brand? | Quarterly |
| PIR-05.3 | What social engineering techniques are trending against the financial services sector in the current quarter? | Quarterly |

---

## 3. Collection Matrix

| PIR | Primary Sources | Secondary Sources | Min. Independent Sources |
|---|---|---|---|
| PIR-01.1 | FS-ISAC alerts; CrowdStrike threat reports; CISA advisories | Mandiant; The DFIR Report; Recorded Future (if available); OSINT | 2 |
| PIR-01.2 | The DFIR Report; CrowdStrike threat research; Elastic Security Labs | Red Canary; Sophos Active Adversary; FS-ISAC | 2 |
| PIR-01.3 | Coveware quarterly reports; Chainalysis; FS-ISAC | Mandiant M-Trends; OSINT/news | 2 |
| PIR-02.1 | CISA KEV; vendor security advisories (Fortinet, Palo Alto, Veeam, Fortra, Microsoft); NVD | FS-ISAC vulnerability alerts; CrowdStrike/Mandiant | 1 (KEV confirmed); 2 (non-KEV) |
| PIR-02.2 | Vendor advisories (detection sections); Elastic Security Labs; CrowdStrike blog | Sentinel community queries; DFIR Report; Red Canary | 2 |
| PIR-02.3 | CISA advisories; CrowdStrike campaign reporting; Mandiant | The DFIR Report; Sophos; FS-ISAC | 2 |
| PIR-03.1 | Vendor breach notifications; FS-ISAC; OSINT/news | SEC filings; state AG breach databases; internal procurement | 1 (vendor confirmed); 2 (unconfirmed) |
| PIR-03.2 | CrowdStrike; Mandiant; CISA advisories | FS-ISAC; The DFIR Report; ESET | 2 |
| PIR-03.3 | Internal data classification records; vendor data handling agreements; FS-ISAC | OSINT/news; Mandiant | 2 |
| PIR-04.1 | CrowdStrike; Flashpoint/Recorded Future (if available); FS-ISAC | SpamHaus/abuse.ch; Elastic Security Labs; Proofpoint | 2 |
| PIR-04.2 | **Dark web monitoring (NOT AVAILABLE)** | FS-ISAC credential sharing; Have I Been Pwned (limited) | 1 (confirmed match) |
| PIR-04.3 | **Dark web monitoring (NOT AVAILABLE)**; FS-ISAC | CrowdStrike access broker reporting; KELA/Recorded Future (if available) | 2 |
| PIR-05.1 | Internal telemetry (M365, Falcon, Sentinel); FS-ISAC | Proofpoint; Cofense; OSINT | 1 (Hartwell-targeted); 2 (sector trend) |
| PIR-05.2 | **Domain monitoring (NOT AVAILABLE)** | OSINT (passive DNS, cert transparency — manual); FS-ISAC | 1 (confirmed impersonation) |
| PIR-05.3 | Proofpoint; Cofense; FS-ISAC | CrowdStrike; OSINT; internal phishing trends | 2 |

---

## 4. Collection Cadence

| Cadence | What Gets Checked | Source |
|---|---|---|
| Daily | CISA KEV additions; CISA advisories; FS-ISAC alerts; vendor security advisories (Fortinet, Palo Alto, Microsoft, Veeam, Fortra); internal phishing reports and Falcon alerts | CISA, FS-ISAC, vendor portals, Sentinel, Falcon, M365 |
| Weekly | CrowdStrike blog; The DFIR Report; Elastic Security Labs; Proofpoint/Cofense; Red Canary; OSINT security news; FS-ISAC weekly digest | Vendor research blogs, FS-ISAC, OSINT |
| Monthly | Coveware ransomware trends; Mandiant/Google TAG; Sophos Active Adversary; state AG breach databases; certificate transparency log review (manual) | Vendor reports, regulatory databases, OSINT |
| Quarterly | PIR review and update; coverage gap assessment; research base currency review; derivative production cycle | All sources aggregated; consumer feedback |
| Semi-annual | IR review with consumers; collection plan review; gap register review with leadership | Consumer meetings, internal review |

---

## 5. Analyst Assignment

| Analyst | Assigned PIRs | Rationale |
|---|---|---|
| Junior Analyst 1 | PIR-01.1, PIR-01.2, PIR-01.3 | Ransomware — single IR, high source availability, serves all four consumers |
| Junior Analyst 2 | PIR-02.1, PIR-02.2, PIR-02.3 | Vulnerability exploitation — requires building relationship with Vuln Mgmt for version data |
| Junior Analyst 3 | PIR-04.1, PIR-05.1, PIR-05.2, PIR-05.3 | Infostealers and social engineering — natural overlap in delivery mechanisms |
| Dana Mercer (Senior) | PIR-03.1, PIR-03.2, PIR-03.3, PIR-04.2, PIR-04.3 + oversight of all PIRs | Supply chain (highest judgment required) + dark web/IAB gaps (owns budget justification relationship with CISO) |

---

## 6. Gap Register

| Gap ID | PIR Affected | Gap Description | Impact on Assessment | Resolution Status |
|---|---|---|---|---|
| GAP-001 | PIR-04.2, PIR-04.3 | No dark web monitoring capability. Budget requested, not approved. | Cannot determine credential exposure from January 2025 incident. PIR-04.2 and PIR-04.3 unanswerable. | Open — budget pending |
| GAP-002 | PIR-05.2 | No domain monitoring or brand protection service. | Lookalike domains detected reactively only. September 2025 domain active 11 days before client-reported discovery. | Open — no budget request submitted |
| GAP-003 | PIR-02.1, PIR-02.2, PIR-02.3 | CTI team lacks version/patch data for Veeam and GoAnywhere MFT. | Can identify exploited CVEs but cannot confirm organizational exposure for these products. | Open — requires internal coordination with IT ops/Vuln Mgmt |
| GAP-004 | PIR-03.1, PIR-03.3 | No contractual requirement for timely vendor breach notification. 18-day delay in April 2025. | Third-party breach intelligence will always lag vendor self-disclosure. | Open — contractual/legal issue, resolution sits with procurement/legal |
| GAP-005 | PIR-01.2, PIR-02.2 | CTI team does not currently produce detection-ready output. Detection engineering researches independently. | Consumer need unmet. Addressed by this framework and derivative production templates. | Open — addressed by workflow implementation |
| GAP-006 | PIR-01.1, PIR-01.2 | No dedicated threat hunting capability. Ad-hoc only via senior SOC analysts. | Cannot validate whether identified TTPs are present in Hartwell's environment. | Open — organizational capability gap |
