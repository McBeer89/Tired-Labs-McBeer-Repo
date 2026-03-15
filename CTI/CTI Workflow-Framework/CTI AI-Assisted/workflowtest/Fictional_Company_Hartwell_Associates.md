# Fictional Company Profile: Hartwell & Associates

## Overview

Hartwell & Associates is a mid-large financial services firm headquartered in Kansas City, Missouri. Founded in 1962, the firm provides wealth management, retirement planning, and brokerage services to individual investors and small business clients across the United States and Canada.

## Key Facts

| Attribute | Detail |
|---|---|
| Sector | Financial Services — Wealth Management & Brokerage |
| Headquarters | Kansas City, MO |
| Employees | ~52,000 |
| Branch Offices | ~14,500 across U.S. and Canada |
| Clients | ~8 million individual investor accounts |
| AUM | ~$1.8 trillion |
| Regulators | SEC, FINRA, NYDFS (NY-licensed), state insurance regulators, OSFI (Canada) |
| ISAC Membership | FS-ISAC (full member) |
| Fiscal Year | Calendar year |

## Business Model

Hartwell operates a decentralized branch model. Each branch is run by a financial advisor who is an independent contractor affiliated with the firm. Advisors manage client portfolios, execute trades, and provide retirement planning. The firm provides the platform, compliance, research, and technology infrastructure. Client PII — including SSNs, account numbers, portfolio holdings, and beneficiary information — is held centrally.

## Technology Stack

| Category | Products / Vendors |
|---|---|
| Edge Devices (VPN) | Fortinet FortiGate (primary), Cisco AnyConnect (legacy, being phased out) |
| Firewalls | Palo Alto Networks (data centers), Fortinet (branch offices) |
| Cloud | Microsoft Azure (primary), AWS (secondary — analytics workloads) |
| Identity | Microsoft Entra ID (Azure AD), Duo MFA |
| Endpoint | CrowdStrike Falcon (EDR), Microsoft Defender for Endpoint (secondary) |
| SIEM | Microsoft Sentinel |
| Email | Microsoft 365 / Exchange Online |
| Backup | Veeam Backup & Replication (on-prem), Azure Backup (cloud) |
| MFT | GoAnywhere MFT (for partner/vendor file transfers) |
| CRM | Salesforce Financial Services Cloud |
| Trading Platform | Proprietary (internally developed, Java-based) |
| Branch Connectivity | SD-WAN (Fortinet) with MPLS fallback |
| Collaboration | Microsoft Teams, SharePoint Online |

## Security Organization

| Team | Size | Lead |
|---|---|---|
| CISO Office | 3 (CISO + 2 deputies) | CISO: Karen Whitfield |
| Cyber Threat Intelligence | 4 (1 senior + 3 junior analysts) | Senior Analyst: Dana Mercer |
| Security Operations Center (SOC) | 18 (3 shifts, 24/7) | SOC Manager: Trevor Blake |
| Detection Engineering | 3 | Lead: Priya Nair |
| Incident Response | 5 | IR Lead: Marcus Holt |
| Vulnerability Management | 4 | Lead: Sarah Cho |
| Identity & Access Management | 6 | Lead: James Okafor |
| Compliance & Risk | 4 (security-focused subset of larger compliance org) | Lead: Rachel Dunn |
| Red Team | 0 (outsourced to NCC Group on annual engagements) | N/A |
| Threat Hunting | 0 (ad-hoc, performed by senior SOC analysts) | N/A |

## CTI Team Current State

Dana Mercer's team of four produces threat intelligence for the broader security organization. Current state:

- Reports are long (8-12 pages average), sent to a broad distribution list that includes the CISO, SOC, detection engineering, and compliance
- No formal intelligence requirements — topics are selected based on trending threats, FS-ISAC alerts, or ad-hoc requests from the CISO
- Junior analysts rely heavily on AI for drafting; output quality varies significantly
- No structured research base — analysts research and write in the same pass
- Consumers have complained informally that reports are "too long" and "hard to find the actionable parts"
- FS-ISAC membership is underutilized — the team monitors alerts but doesn't systematically collect against defined requirements
- No dark web monitoring capability (budget requested but not yet approved)
- Veeam and GoAnywhere MFT are in the technology stack but the CTI team is not aware of their specific versions or patch status

## Recent Incidents

- **September 2025:** Phishing campaign impersonating Hartwell's brand targeted clients via lookalike domain. Discovered by a client reporting a suspicious email, not by internal detection. Lookalike domain was active for 11 days before takedown.
- **April 2025:** A third-party printing vendor (used for client statements) disclosed a breach. Hartwell client names and account numbers were potentially exposed. Vendor notification came 18 days after the vendor discovered the breach. No contractual requirement for faster notification existed.
- **January 2025:** CrowdStrike Falcon flagged credential harvesting activity on a branch workstation. Investigation determined an infostealer (Lumma) had been delivered via a ClickFix social engineering technique targeting a financial advisor. Contained within 4 hours. Forced password reset for the advisor and 3 branch staff. Unknown whether harvested credentials appeared in dark web marketplaces (no monitoring capability).

## Consumer Landscape (Who Would Use CTI Derivatives)

| Consumer | What They Care About | Current Pain Point |
|---|---|---|
| Karen Whitfield (CISO) | Strategic risk, budget justification, board reporting | Gets 10-page reports, reads page 1 only |
| Trevor Blake (SOC Manager) | Actionable IOCs, current campaigns targeting FS sector | Extracts IOCs manually from CTI reports |
| Priya Nair (Detection Eng Lead) | TTPs to build detections against, telemetry gaps | Reads vendor blogs herself because CTI reports don't include event IDs or detection-ready detail |
| Marcus Holt (IR Lead) | Kill chain detail, expected artifacts, containment guidance | Uses CISA advisories directly because CTI reports don't organize by attack phase |
| Sarah Cho (Vuln Mgmt Lead) | Which CVEs are being actively exploited against FS sector | Gets CVE lists without exploitation context or priority |
| Rachel Dunn (Compliance Lead) | Regulatory obligations, reporting triggers, sanctions updates | Not currently receiving CTI products at all |
| NCC Group (Red Team, external) | Adversary TTPs for realistic emulation | Receives a generic threat briefing before annual engagement; no structured emulation brief |
