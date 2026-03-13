# CTI Intelligence Requirements and Collection Framework

## Purpose

This framework answers the question that sits upstream of everything else: **What should analysts be looking for, where should they look, and how do they know when they've found enough?**

Without defined intelligence requirements, analysts collect based on curiosity, trending topics, or whatever they stumble across. The result is unfocused research that produces long, inaccurate reports about whatever the analyst happened to find — not what the organization needs to know.

This framework provides the Planning & Direction layer of the intelligence cycle. It feeds into the Research Quality Framework (five gates) and the Source-to-Derivative workflow. Together, the three documents form the complete CTI pipeline:

```
Requirements & Collection  →  Quality Gates  →  Research Base  →  Derivatives
(this document)               (what passes)     (source layer)    (deliverables)
```

---

## Part 1: Intelligence Requirements Hierarchy

Intelligence requirements exist at three levels. Each level drives the one below it.

### Intelligence Requirements (IRs)

IRs are the broadest questions the organization needs answered. They come from consumers — security leadership, the SOC, IR, compliance — not from the CTI team's own interests. A financial services CTI program should have no more than 6–8 active IRs at any time. More than that means you haven't prioritized.

IRs are reviewed and updated **semi-annually** unless a significant change in the threat landscape or business operations forces an earlier review.

**Example IRs for a financial services firm:**

| IR ID | Intelligence Requirement | Consumer | Review Cycle |
|---|---|---|---|
| IR-01 | Which threat actors are actively targeting financial services firms with our profile, and what are their current TTPs? | CISO, Security Leadership | Semi-annual |
| IR-02 | What vulnerabilities in our technology stack are being actively exploited in the wild? | Vulnerability Management, Detection Eng | Semi-annual |
| IR-03 | What supply-chain and third-party risks could expose our client data or operations? | CISO, Third-Party Risk, Compliance | Semi-annual |
| IR-04 | What credential exposures affect our organization or our vendors? | SOC, Identity & Access Mgmt | Semi-annual |
| IR-05 | What phishing, social engineering, and fraud campaigns are targeting our sector or our brand? | SOC, Fraud, Communications | Semi-annual |
| IR-06 | What regulatory or legal developments affect our cybersecurity obligations? | Compliance, Legal, CISO | Semi-annual |

**How to develop IRs:** Meet with each consumer group. Ask: "What do you need to know about the threat environment to do your job? What decisions do you make that threat intelligence could inform?" Capture their answers. Consolidate overlapping needs. Prioritize by business impact. The CTI team does not invent requirements — they elicit and formalize them from consumers.

### Priority Intelligence Requirements (PIRs)

PIRs break each IR into specific, time-bound, actionable questions. They are more granular and change more frequently — reviewed **quarterly** or when the threat landscape shifts. PIRs are where most of the analyst's daily work is directed.

**Example PIRs under IR-01 (Threat Actors Targeting Financial Services):**

| PIR ID | Priority Intelligence Requirement | Derived From | Cadence |
|---|---|---|---|
| PIR-01.1 | Which ransomware groups have claimed financial sector victims in the past 90 days, and what initial access vectors did they use? | IR-01 | Quarterly |
| PIR-01.2 | Are any APT or espionage groups conducting campaigns against the wealth management or brokerage sub-sector? | IR-01 | Quarterly |
| PIR-01.3 | What BYOVD or EDR evasion techniques are being shared across ransomware groups? | IR-01 | Quarterly |

**Example PIRs under IR-02 (Vulnerability Exploitation):**

| PIR ID | Priority Intelligence Requirement | Derived From | Cadence |
|---|---|---|---|
| PIR-02.1 | Which CVEs affecting our edge devices (VPN, firewall, MFT) have been added to CISA KEV or observed in active exploitation in the past 30 days? | IR-02 | Monthly |
| PIR-02.2 | Are threat actors exploiting any vulnerabilities in our backup infrastructure (Veeam, Commvault, etc.)? | IR-02 | Quarterly |
| PIR-02.3 | What zero-days affecting enterprise software (MFT, ERP, CRM) are being exploited by data-extortion groups? | IR-02 | Quarterly |

**Example PIRs under IR-03 (Supply-Chain Risk):**

| PIR ID | Priority Intelligence Requirement | Derived From | Cadence |
|---|---|---|---|
| PIR-03.1 | Have any of our critical third-party vendors appeared in breach notifications, leak sites, or dark web marketplaces in the past 90 days? | IR-03 | Quarterly |
| PIR-03.2 | What vendor categories are being targeted in supply-chain ransomware campaigns (marketing, printing, CRM, payroll, etc.)? | IR-03 | Quarterly |

**Example PIRs under IR-04 (Credential Exposure):**

| PIR ID | Priority Intelligence Requirement | Derived From | Cadence |
|---|---|---|---|
| PIR-04.1 | Do any organization employee credentials appear in current infostealer logs or IAB marketplace listings? | IR-04 | Monthly |
| PIR-04.2 | What infostealer families are actively targeting financial services employees, and through what distribution methods? | IR-04 | Quarterly |

**Example PIRs under IR-05 (Phishing & Fraud):**

| PIR ID | Priority Intelligence Requirement | Derived From | Cadence |
|---|---|---|---|
| PIR-05.1 | Are there active phishing kits or lookalike domains impersonating our brand? | IR-05 | Monthly |
| PIR-05.2 | What social engineering techniques (vishing, ClickFix, AI-generated phishing) are being used against financial services help desks and employees? | IR-05 | Quarterly |

**Example PIRs under IR-06 (Regulatory):**

| PIR ID | Priority Intelligence Requirement | Derived From | Cadence |
|---|---|---|---|
| PIR-06.1 | Have SEC, FINRA, NYDFS, or CISA issued new cybersecurity guidance, rules, or enforcement actions in the past 90 days? | IR-06 | Quarterly |
| PIR-06.2 | Have OFAC sanctions designations changed in ways that affect ransomware payment decisions? | IR-06 | Quarterly |

### Specific Intelligence Requirements (SIRs)

SIRs are the most granular — specific facts, indicators, or attributes needed for immediate action. They are short-lived (days to weeks) and often triggered by incidents or emerging events.

**Examples:**

- "What are the IOCs associated with the Qilin campaign targeting South Korean financial firms in September 2025?"
- "What CVE is being exploited in the active Medusa campaign using GoAnywhere MFT?"
- "What domains are associated with the phishing kit impersonating our brand reported by FS-ISAC yesterday?"

SIRs don't need a standing table. They emerge from PIR research, incident response, or ad-hoc requests from consumers. They get answered and closed.

---

## Part 2: Collection Plan

Each PIR needs a collection plan — where does the analyst look to answer it? Without a collection plan, analysts either search everywhere (wasting time) or search the wrong places (missing critical information).

### Source Categories

| Category | What It Provides | Examples |
|---|---|---|
| **Government Advisories** | Confirmed TTPs, CVEs, attribution, mitigation guidance | CISA advisories, FBI flash alerts, NSA advisories, NCSC (UK), ASD (Australia) |
| **Sector ISAC** | Financial-sector-specific threat intel, peer incident sharing, IOCs | FS-ISAC (SHARE platform, CONNECT, weekly risk summaries, GIO alerts) |
| **Vendor Threat Research** | Threat actor profiles, campaign analysis, TTP deep-dives, detection guidance | CrowdStrike, Mandiant/Google, Microsoft, Recorded Future, Flashpoint, Palo Alto Unit 42, Elastic, Red Canary, SentinelOne, Darktrace, ESET, Sophos |
| **Intrusion Reports** | Real-world kill chain detail with telemetry and artifacts | The DFIR Report, Mandiant M-Trends, CrowdStrike Threat Hunting Report |
| **Vulnerability Intelligence** | Active exploitation data, CVE severity, patch status | CISA KEV, NVD, vendor security advisories, Qualys/Tenable research |
| **Dark Web / Underground** | Credential exposures, IAB listings, leak site monitoring, threat actor chatter | Flashpoint, Recorded Future, KELA, Intel 471, SpyCloud, Hudson Rock |
| **OSINT / News** | Breaking incidents, breach reporting, regulatory developments | BleepingComputer, The Record, Krebs on Security, BankInfoSecurity, Cybersecurity News, SecurityWeek |
| **Internal Telemetry** | Incidents, alerts, phishing reports, vulnerability scan results | SIEM, EDR, email gateway, phishing report inbox, vulnerability scanner |
| **Regulatory / Legal** | Rule changes, enforcement actions, sanctions updates | SEC.gov, FINRA.org, NYDFS, OFAC SDN list, CISA CIRCIA updates |

### Collection Matrix: PIR to Source Mapping

This is the operational heart of the collection plan. It tells the analyst exactly where to look for each PIR.

| PIR | Primary Sources | Secondary Sources | Min. Independent Sources Before Assessment |
|---|---|---|---|
| PIR-01.1 (Ransomware groups / FS victims) | CISA advisories, FS-ISAC alerts, vendor threat reports (Check Point, SOCRadar, Cyble) | Leak site monitoring, The DFIR Report, news (BleepingComputer) | 3 |
| PIR-01.2 (APT targeting wealth mgmt) | Mandiant M-Trends, CrowdStrike, FS-ISAC, government advisories | Recorded Future, ESET APT reports | 2 |
| PIR-01.3 (EDR evasion / BYOVD) | ESET, vendor detection research (Elastic, Picus), CISA | Infosecurity Magazine, The DFIR Report | 2 |
| PIR-02.1 (Edge device CVEs) | CISA KEV, vendor security advisories (Fortinet, Ivanti, SonicWall, Citrix) | NVD, FS-ISAC alerts | 2 |
| PIR-02.2 (Backup infra vulns) | Veeam security advisories, CISA KEV, vendor research | CISA advisories referencing backup exploitation | 2 |
| PIR-02.3 (Zero-days in enterprise SW) | CISA KEV, vendor advisories, Clop/data-extortion group analysis | Vendor threat research, news | 2 |
| PIR-03.1 (Vendor breach monitoring) | Dark web monitoring (Flashpoint, KELA), FS-ISAC, news | State AG breach notification databases, leak sites | 2 |
| PIR-03.2 (Supply-chain targeting patterns) | Vendor research, CISA, FS-ISAC, incident case studies | BankInfoSecurity, BleepingComputer | 3 |
| PIR-04.1 (Credential exposure) | Dark web monitoring (SpyCloud, Hudson Rock, Flashpoint), IAB marketplace monitoring | FS-ISAC, internal phishing/incident reports | 1 (verified match) |
| PIR-04.2 (Infostealer families) | Vendor research (Mandiant, Recorded Future), OSINT | Any.Run, VirusTotal, MalwareBazaar | 2 |
| PIR-05.1 (Brand impersonation) | Domain monitoring tools, FS-ISAC, phishing report inbox | OSINT (urlscan.io, PhishTank) | 1 (verified match) |
| PIR-05.2 (Social engineering techniques) | Vendor research, CISA, FS-ISAC | KnowBe4 research, internal phishing simulation data | 2 |
| PIR-06.1 (Regulatory developments) | SEC.gov, FINRA.org, NYDFS, CISA.gov | Legal counsel, industry associations (ABA, SIFMA), BankInfoSecurity | 1 (primary regulatory source) |
| PIR-06.2 (OFAC sanctions changes) | OFAC SDN list, Treasury.gov, Chainalysis | Legal counsel, news | 1 (primary regulatory source) |

### Minimum Source Thresholds

The "Min. Independent Sources" column is critical. It tells the analyst how many independent, corroborating sources are needed before they can make an assessment at a given confidence level. This directly prevents the accuracy problem — an analyst reading one blog post and treating it as fact.

| Confidence Level | Minimum Sources | Source Diversity Requirement |
|---|---|---|
| **Low** | 1 credible source | Single-sourced is acceptable; must be documented as low confidence with known gaps |
| **Moderate** | 2–3 independent sources | At least two different source categories (e.g., government advisory + vendor report) |
| **High** | 3+ independent sources across multiple categories | Must include at least one primary/authoritative source (CISA, ISAC, court filing, IR case data); collection gaps accounted for |

**"Independent" means:** Different organizations with different visibility. Two blog posts from the same vendor citing the same dataset are one source, not two. A CISA advisory and a vendor report that independently analyzed the same threat actor are two sources.

---

## Part 3: Collection Cadence and Analyst Assignment

### Standing Collection Schedule

Not everything needs to be checked daily. Match cadence to how fast the intelligence changes.

| Cadence | What Gets Checked | Source |
|---|---|---|
| **Daily** | CISA KEV additions, FS-ISAC alerts, credential exposure alerts | CISA KEV RSS, FS-ISAC SHARE, dark web monitoring dashboard |
| **Weekly** | FS-ISAC risk summary, new CISA advisories, ransomware leak site activity, OSINT news scan | FS-ISAC, CISA.gov, leak site monitoring, news aggregation |
| **Monthly** | Vendor threat reports, edge device CVE review against org inventory, brand impersonation review | Vendor blogs/reports, NVD, domain monitoring |
| **Quarterly** | Full PIR review and update, threat actor profile refresh, regulatory landscape review, collection gap assessment | Aggregated from all sources; produces quarterly research base update |
| **Semi-annual** | IR review with consumers, collection plan validation, source quality assessment | Consumer meetings, team retrospective |

### Analyst Assignment

Each PIR should have a named analyst responsible for collection against it. This prevents the "everyone looks at everything and no one owns anything" problem.

| Analyst | Assigned PIRs | Rationale |
|---|---|---|
| Analyst A | PIR-01.1, PIR-01.2, PIR-01.3 | Threat actor tracking — ransomware and APT focus |
| Analyst B | PIR-02.1, PIR-02.2, PIR-02.3 | Vulnerability intelligence — technical depth required |
| Analyst C | PIR-03.1, PIR-03.2, PIR-04.1, PIR-04.2 | Supply-chain and credential exposure — dark web monitoring focus |
| All / rotating | PIR-05.1, PIR-05.2, PIR-06.1, PIR-06.2 | Phishing/fraud and regulatory — lower research burden, good rotation candidates |

**PIR ownership doesn't mean isolation.** If Analyst B finds threat actor TTP information while researching a vulnerability, they pass it to Analyst A. The collection plan creates ownership, not silos.

---

## Part 4: From Collection to Research Base

When an analyst finds information relevant to a PIR, they don't write a report. They add a claim to the research base, tagged with the five gates from the Research Quality Framework:

1. **Sourced** — where it came from
2. **Current** — reporting period verified
3. **Relevant** — tied to the specific PIR
4. **Confidence-rated** — L/M/H with reasoning based on source count and diversity
5. **Typed** — Fact / Assessment / Assumption

The research base accumulates claims over time. When enough claims have accumulated to answer a PIR (meeting the minimum source threshold), the analyst can produce a key judgment. Key judgments are what drive derivative products.

```
PIR defines what to look for
        │
Collection plan defines where to look
        │
Five gates filter what enters the research base
        │
Minimum source thresholds determine when an assessment can be made
        │
Key judgments are formed from accumulated evidence
        │
Derivatives are produced for specific consumers from key judgments
```

---

## Part 5: Gap Management

When the collection plan reveals that a PIR cannot be adequately answered with available sources, that's a **collection gap**. Gaps are not failures — they're intelligence about the state of the intelligence program.

### Types of Gaps

| Gap Type | What It Means | Example | Resolution |
|---|---|---|---|
| **Source gap** | No available source provides this information | No dark web monitoring capability → can't answer PIR-04.1 | Acquire capability (vendor subscription, ISAC membership) or accept the gap and document it |
| **Access gap** | Source exists but we don't have access | FS-ISAC membership required for sector-specific alerts | Budget request for membership |
| **Visibility gap** | Source exists, we have access, but it doesn't cover our specific profile | Vendor threat reports cover banking but not wealth management specifically | Document as limitation on confidence; seek additional sources |
| **Timeliness gap** | Information arrives too late to be actionable | Quarterly vendor report arrives after the campaign is over | Supplement with real-time sources (ISAC alerts, news, internal telemetry) |
| **Internal gap** | We lack internal data needed to contextualize external intelligence | Don't know our own edge device inventory → can't assess CVE relevance | Coordinate with IT/infrastructure teams to close the gap |

### Gap Register

Maintain a running register of gaps tied to PIRs. Review quarterly.

| Gap ID | PIR Affected | Gap Description | Impact on Assessment | Resolution Status |
|---|---|---|---|---|
| GAP-001 | PIR-04.1 | No dark web credential monitoring capability | Cannot assess organizational credential exposure; PIR-04.1 unanswerable | Open — vendor evaluation in progress |
| GAP-002 | PIR-02.1 | Edge device inventory not confirmed with IT | Cannot map CVEs to actual organizational exposure | Open — requested from infrastructure team |
| GAP-003 | PIR-03.1 | No systematic vendor breach monitoring | Vendor compromises discovered reactively through news, not proactively | Open — evaluating Flashpoint/KELA |

**Gaps are the most honest part of any intelligence program.** They tell leadership exactly what the team can and cannot answer, and they provide the justification for resource requests (tool subscriptions, ISAC memberships, headcount) tied directly to unanswerable intelligence requirements.

---

## How This Connects to the Full Pipeline

| Pipeline Stage | Document | What It Does |
|---|---|---|
| **What to look for and where** | This document (Requirements & Collection Framework) | Defines IRs, PIRs, collection sources, cadence, analyst assignment, minimum source thresholds |
| **What qualifies as intelligence** | Research Quality Framework (Five Gates) | Filters each claim before it enters the research base |
| **Where intelligence accumulates** | Research Base (per-topic) | Structured, sourced, confidence-rated repository — the source layer |
| **Who gets what** | Source-to-Derivative Workflow | Produces audience-specific deliverables filtered by consumer and question |

If the team has all four layers, every piece of intelligence can be traced from the consumer's question (IR) through the collection that found it (PIR + source), through the quality filter that validated it (five gates), into the research base (with confidence level), and out to the derivative that delivered it (to the right consumer in the right form).

If anything breaks, you can diagnose where: bad requirements (wrong questions), bad collection (wrong sources or not enough sources), bad filtering (claims entering without sourcing or confidence), bad research base (no key judgments, no competing hypotheses), or bad derivatives (wrong audience, wrong format, too long).

---

## Influences and References

- **Robert M. Lee** — *Structuring Cyber Threat Intelligence Assessments*. The principle that intelligence exists to serve the consumer's requirement, confidence level framework, and the inverted pyramid distribution of assessment confidence. [robertmlee.org](https://www.robertmlee.org/structuring-cyber-threat-intelligence-assessments-musings-and-recommendations/)
- **Michael Rea** — *I Can Haz Requirements?* (SANS DFIR YouTube). The centrality of intelligence requirements to CTI program success. [youtube.com](https://www.youtube.com/watch?v=Aqo3IcVQs_M)
- **SANS FOR578: Cyber Threat Intelligence** — Intelligence cycle, planning & direction phase, collection management, structured analytic techniques. [sans.org](https://www.sans.org/cyber-security-courses/cyber-threat-intelligence)
- **Security Risk Advisors (TIGR Team)** — Threat Intelligence Requirements categorization and example requirements for organizations. [sra.io](https://sra.io/blog/threat-intelligence-requirements/)
- **ThreatConnect** — IR/PIR/SIR hierarchy best practices and implementation guidance. [knowledge.threatconnect.com](https://knowledge.threatconnect.com/docs/best-practices-intelligence-requirements)
- **Intel 471** — Collection requirements framework, attack surface vs. adversary focused requirements, external vs. internal collection. [intel471.com](https://www.intel471.com/blog/cyber-threat-intelligence-requirements-what-are-they-what-are-they-for-and-how-do-they-fit-in-the)
- **Kraven Security (Adam Goss)** — Intelligence requirements guide, PIR definition and lifecycle. [kravensecurity.com](https://kravensecurity.com/what-are-intelligence-requirements/)
- **Ondra Rojčík** — Developing Priority Intelligence Requirements, operational classification of attack types for CTI programs. [medium.com/@orojcik](https://medium.com/@orojcik/developing-priority-intelligence-requirements-for-your-cyber-threat-intelligence-program-fab25bf414ff)
- **Flashpoint** — Threat intelligence lifecycle, requirements & tasking phase. [flashpoint.io](https://flashpoint.io/blog/threat-intelligence-lifecycle/)
- **FS-ISAC** — Financial services threat intelligence sharing platform, Intelligence Exchange (SHARE/CONNECT), operating rules for member intelligence sharing. [fsisac.com](https://www.fsisac.com/intelligence)
- **Lenny Zeltser** — *Rating Sheet for the Right Information: Threat Reports* (SEC402). The consumer-question-based inclusion test that influences how PIRs are framed. [zeltser.com](https://zeltser.com)
- **Andrew VanVleet / TIRED Labs** — The source-to-derivative model and the principle that research and deliverables are different things. The DDM inclusion test as structural inspiration for the five-gate claim filter. [library.tired-labs.org](https://library.tired-labs.org)
