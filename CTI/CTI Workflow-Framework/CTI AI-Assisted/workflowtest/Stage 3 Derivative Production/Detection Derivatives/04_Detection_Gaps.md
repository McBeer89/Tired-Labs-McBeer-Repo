# Section 4: Detection Gaps

These are techniques or attack phases that cannot be detected with current telemetry or are outside detection engineering's scope. Each gap names what's missing and what would close it. These become requests from detection engineering to other teams.

---

## Gap 1: Branch Egress Visibility for Exfiltration Detection (P1-3)

**Affects:** P1-3 (Exfiltration to Cloud Storage)

**What's missing:** Unknown whether Hartwell's SD-WAN configuration routes all branch internet traffic through centrally monitored proxy/firewall infrastructure, or whether branches have local internet breakout. If branches break out locally, exfiltration from branch endpoints to MEGA.io, Backblaze, or other cloud storage destinations will not appear in central proxy logs.

**What would close it:** Confirmation from network engineering that all branch egress is centrally inspected — or, if local breakout exists, deployment of cloud access security broker (CASB) or branch-level proxy logging forwarded to Sentinel. This is an infrastructure request, not a detection engineering deliverable.

**Request to:** Network Engineering / Infrastructure

---

## Gap 2: Approved RMM Tool Baseline (P1-4)

**Affects:** P1-4 (Remote Management Tool Abuse)

**What's missing:** No approved RMM tool whitelist exists for detection engineering to reference. Without knowing which RMM tools are authorized, which accounts are approved to install them, and which target systems are legitimate management targets, any behavioral detection for unauthorized RMM installation will either generate excessive false positives (if too broad) or miss malicious activity (if tuned too aggressively to reduce noise).

**What would close it:** A documented whitelist from IT operations specifying: (1) approved RMM tools by product name, (2) approved installer accounts, (3) approved target system types. This is a policy/documentation request, not a technology deployment.

**Request to:** IT Operations / Endpoint Management

---

## Gap 3: Veeam and GoAnywhere MFT Version and Patch Status (P2-5, inherited GAP-003)

**Affects:** P2-5 (Veeam Credential Dumping) and potential GoAnywhere MFT detections

**What's missing:** CTI cannot confirm whether Hartwell's Veeam Backup & Replication or GoAnywhere MFT deployments are running versions vulnerable to actively exploited CVEs (Veeam CVE-2024-40711, CVE-2025-23120; GoAnywhere CVE-2025-10035). Detection engineering can build detections for post-exploitation behavior, but cannot assess whether the exploitation path is open without version data.

**What would close it:** Version and patch status from Vulnerability Management for all Veeam and GoAnywhere MFT instances. If vulnerable versions are confirmed, P2-5 should be elevated to P1.

**Request to:** Vulnerability Management (Sarah Cho)

---

## Gap 4: Process-Level Network Correlation for C2 Detection (P2-4)

**Affects:** P2-4 (C2 via Trusted Platforms)

**What's missing:** Detecting C2 over Microsoft Graph API or Google Sheets requires correlating the calling process with the network destination. Standard proxy logs show domain-level connections but not which process initiated the connection. Without Sysmon 3 (NetworkConnect) deployed broadly enough to correlate process-to-connection, C2 via trusted platforms is detectable only at the domain level — which generates unacceptable false positives against legitimate M365 and Google Workspace usage.

**What would close it:** Confirm Sysmon deployment scope includes NetworkConnect (Event ID 3) logging on endpoints likely to be early-stage compromise targets (branch workstations, VPN endpoints, servers). If Sysmon 3 is disabled due to volume concerns, evaluate enabling it on a targeted subset.

**Request to:** Security Operations (Trevor Blake) / Endpoint Engineering

---

## Gap 5: No Detection Validation Capability (inherited GAP-006)

**Affects:** All detections in this brief

**What's missing:** Hartwell has no dedicated threat hunting function. Detections built from this brief cannot be validated against the live environment through proactive hunting. There is no mechanism to confirm whether the TTPs described in this brief are already present in Hartwell's environment or whether newly built detections fire correctly against realistic attack simulations.

**What would close it:** Two options (not mutually exclusive): (1) Dedicate senior SOC analyst time to structured validation of P1 detections using the technique descriptions in this brief as hunt hypotheses. (2) Provide this brief to NCC Group before the next annual red team engagement and request they include P1 techniques in their emulation plan, validating detection coverage as part of the exercise.

**Request to:** SOC Manager (Trevor Blake) for option 1; CISO Office for option 2 (NCC Group scoping)

---

## Gap 6: Data Staging TTP Detail (Research Base Gap)

**Affects:** Pre-exfiltration detection (between lateral movement and exfiltration phases)

**What's missing:** The research base documents exfiltration tools and timing (median 72.98 hours, 79% off-hours) but does not detail staging procedures — compression tools, encryption of staged data, staging directories, or staging volume patterns. This phase is a detection opportunity between lateral movement (detectable) and exfiltration (detectable) that is currently blind.

**What would close it:** Procedure-level staging TTP data from DFIR case reports or vendor incident analyses. This is a research base gap — request CTI team update the research base with staging detail from Sophos, CrowdStrike, or Rapid7 case studies.

**Request to:** CTI Team (Dana Mercer) — research base update for next cycle
