# Section 3: ATT&CK Coverage Map

This map shows what the detections in this brief cover, what they partially cover, and what they cannot cover — organized by kill chain phase. Each gap states whether it is closable (missing telemetry or configuration) or inherent (behavior indistinguishable from legitimate activity without additional context).

## Full Coverage (detection tables above provide sufficient observable behavior and telemetry)

| Kill Chain Phase | ATT&CK ID | Technique | Detection Table | Coverage Notes |
|---|---|---|---|---|
| Defense Evasion | T1562.001 | Impair Defenses: BYOVD | P1-1 | Covered via driver load events and EDR process termination monitoring. Coverage is independent of EDR — designed to detect the attack that kills the EDR. |
| Credential Access | T1003.001 | LSASS Memory Dumping | P1-2 | Covered via Sysmon 10 ProcessAccess targeting lsass.exe. Well-established detection pattern with known GrantedAccess bitmasks. |
| Credential Access | T1558.003 | Kerberoasting | P2-1 | Covered via Windows 4769 with RC4 encryption filter. High fidelity in modern environments where AES is standard. |
| Credential Access | T1003.006 | DCSync | P2-2 | Covered via Windows 4662 directory replication requests from non-DC sources. Clear separation between legitimate (DC-to-DC) and malicious (non-DC source) replication. |
| Defense Evasion | T1112 | Modify Registry: WDigest | P2-3 | Covered via Sysmon 13 / Windows 4657 on specific registry key. Near-zero false positive rate. |
| Credential Access | T1555 | Veeam Credential Dumping | P2-5 | Covered via PowerShell Script Block Logging on Veeam servers. Dependent on logging being enabled (telemetry dependency — Section 5). |

## Partial Coverage (detectable but with significant caveats)

| Kill Chain Phase | ATT&CK ID | Technique | Detection Table | Coverage Limitation |
|---|---|---|---|---|
| Exfiltration | T1567.002 | Exfiltration to Cloud Storage | P1-3 | **Closable gap.** Detection depends on proxy/firewall logs capturing outbound connections to cloud storage providers. If branches route traffic locally rather than through central proxy, exfiltration from branch endpoints may not be visible. Confirm whether SD-WAN configuration routes all branch egress through centrally monitored infrastructure. |
| Persistence / C2 | T1219 | RMM Abuse | P1-4 | **Closable gap.** Behavioral detection requires a baseline of approved RMM tools, approved installer accounts, and approved target systems. Without this baseline, the detection cannot distinguish malicious RMM installation from legitimate IT activity. Requires coordination with IT operations to define the approved RMM whitelist. |
| Command & Control | T1102 | C2 via Trusted Platforms | P2-4 | **Closable gap.** Detecting Graph API or Google Sheets C2 requires process-level visibility into which applications make cloud API calls. Standard proxy logs show the domain but not the calling process. Requires endpoint-level network correlation (Sysmon 3 paired with process tree context). |
| Lateral Movement | T1021.001/.002 | RDP / SMB Admin Shares | P3-1 | **Inherent limitation.** RDP and SMB are legitimate enterprise protocols. Detection requires per-environment baselining of normal source-destination pairs, account types, and time-of-day patterns. False positive rate will remain elevated in a 14,500-branch environment until baselining is complete. |
| Initial Access | T1204.001 | ClickFix Social Engineering | P3-2 | **Partial — endpoint only.** Detection covers the browser-to-PowerShell handoff on the endpoint. Does not cover the social engineering delivery mechanism (email, web, ad) — that is email gateway and web proxy territory. Validate existing email/endpoint coverage before building additional rules. |

## No Coverage (not detectable with current approach or outside detection engineering scope)

| Kill Chain Phase | Gap | Reason | Closable? |
|---|---|---|---|
| Lateral Movement | Unmonitored device pivot (P3-3) | Akira pivoted to a Linux webcam with no EDR agent. Detection coverage ends at the agent boundary. No endpoint telemetry exists for agentless devices. | **Partially closable.** Network-layer anomaly detection (SMB traffic from IoT IP ranges) could provide partial coverage. Full mitigation requires network segmentation and asset inventory — infrastructure scope, not detection engineering. |
| Initial Access | Edge device / VPN exploitation | Fortinet FortiGate, Palo Alto PAN-OS, and SonicWall CVEs are the primary direct-entry vector. Exploitation of edge devices occurs outside endpoint telemetry. | **Not closable by detection engineering.** This is vulnerability management scope (patching) and network security scope (firewall log monitoring, anomalous admin sessions). Detection engineering's role begins at post-exploitation: the first detectable action after perimeter compromise feeds into P1-2 (LSASS), P1-4 (RMM installation), and P2-1 through P2-5. |
| Initial Access | Credential purchase from IAB | The ClickFix → StealC → IAB → Qilin pipeline means stolen credentials may be used weeks after initial theft. No detection fires at the point of credential sale. | **Not closable by detection engineering.** Detection opportunity is at credential use, not credential sale. Identity-based detections (impossible travel, anomalous logon patterns, MFA challenge failures) are the relevant control — owned by IAM and SOC, not detection engineering. Dark web monitoring (not currently available per company profile) would provide early warning. |
| Exfiltration | Data staging before exfiltration | Research base documents median 72.98 hours between initial access and exfiltration, but does not detail staging TTPs (compression, encryption, staging directories) at procedure level. | **Gap in research base (GAP-R03).** Staging detection is feasible if procedure-level detail is available. Recommend requesting staging TTP detail from DFIR reports or vendor case studies for the next research base update. |
| All Phases | Validation of detection efficacy | No threat hunting capability exists (GAP-006). Detections built from this brief cannot be validated against Hartwell's live environment through proactive hunting. | **Closable — organizational.** Requires either a dedicated threat hunting function or structured validation engagement with NCC Group during the annual red team exercise. |
