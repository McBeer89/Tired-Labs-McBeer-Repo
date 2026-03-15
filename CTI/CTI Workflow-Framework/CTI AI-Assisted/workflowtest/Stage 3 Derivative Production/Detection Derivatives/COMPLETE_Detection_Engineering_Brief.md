# Detection Engineering Brief — Ransomware TTPs Targeting Financial Services (Q1 2026)

| Field | Detail |
|---|---|
| **Derived From** | Research Base — Ransomware Threat to Financial Services (Q1 2026), IR-01 / PIR-01.1, PIR-01.2, PIR-01.3, v1.0 |
| **Date** | March 15, 2026 |
| **Consumer** | Priya Nair, Detection Engineering Lead |
| **Question Answered** | What detection rules should detection engineering build next based on current ransomware TTPs targeting financial services? What telemetry must be confirmed or requested? Which existing detections should be rebuilt as behavioral detections? |
| **Classification** | INTERNAL — Hartwell & Associates |

## Confidence Note

All source material in this brief flows through a single AI-synthesized intermediary document. No primary sources have been independently verified. Confidence across the research base is rated LOW — reflecting source dependency, not evidence quality. Several claims (marked in individual tables) are undated or unsourced at procedure level. Treat priority rankings as directionally correct pending primary source verification. Do not delay P1 detection builds for verification — the techniques are well-documented in public literature regardless of this specific base's sourcing limitations.

---

# Section 1: Detection Priority Ranking

This table is the detection backlog. P1 techniques represent the highest-value detection builds based on confirmed active use against financial services, direct relevance to Hartwell's technology stack, and whether the technique requires behavioral detection to catch (because tool-signature detections are already being evaded).

| Priority | ATT&CK ID | Technique | Groups Using | Rationale |
|---|---|---|---|---|
| **P1** | T1562.001 | Impair Defenses: Disable or Modify Tools (BYOVD) | Medusa, Play, Qilin, DragonForce, INC Ransom + 3 others; Reynolds ransomware | 8+ groups sharing EDRKillShifter. Reynolds (Feb 2026) embeds vulnerable driver in payload and specifically terminates CrowdStrike Falcon. Hartwell's primary EDR is the named target. |
| **P1** | T1003.001 | OS Credential Dumping: LSASS Memory | Cross-group (Akira, Qilin, others) | Universal ransomware kill chain step. Mimikatz sekurlsa::logonpasswords is the most-used module (Red Canary). Precedes all lateral movement and privilege escalation. |
| **P1** | T1567.002 | Exfiltration to Cloud Storage | LockBit, Black Basta, BlackSuit, Medusa, Qilin, INC Ransom | Rclone present in 57% of ransomware incidents (ReliaQuest). 79% of exfiltration occurs off-hours (Sophos 2025). Tool-name detection is trivially evaded — requires behavioral rebuild targeting volume, timing, and destination. |
| **P1** | T1219 | Remote Access Software (RMM Abuse) | Medusa, Rhysida, Cactus, Akira, Black Basta | 36% of IR cases involved RMM abuse across 32 different tools (Arctic Wolf 2025). Legitimate tools used maliciously — signature detection is ineffective. Requires behavioral rules based on installation context, timing, and account association. |
| **P2** | T1558.003 | Steal or Forge Kerberos Tickets: Kerberoasting | Akira | Rubeus documented in Akira attack chain (Security Boulevard, Nov 2025). High-fidelity detection via service ticket request anomalies. |
| **P2** | T1003.006 | OS Credential Dumping: DCSync | Cross-group | KRBTGT hash extraction for Golden Ticket creation (Qualys ETM, Feb 2026). Precedes domain-wide persistence. Detectable via directory replication service requests from non-DC sources. |
| **P2** | T1112 | Modify Registry: WDigest Credential Caching | Qilin | Qilin affiliates modify WDigest UseLogonCredential to force plaintext credential storage before LSASS dumping. Near-zero false positive rate. Source is undated/unverified — but the technique itself is well-documented and detection is low-cost. |
| **P2** | T1102 | Web Service: C2 via Trusted Platforms | Fog (GC2), multiple groups (Havoc) | Havoc framework integrates Microsoft Graph API for C2. GC2 uses Google Sheets. Both abuse trusted cloud services to evade network-based detection. Requires monitoring API call patterns to M365 and Google services. |
| **P2** | T1555 | Credentials from Password Stores: Veeam Backup | Akira | Akira dumps Veeam backup credentials via PowerShell. Hartwell runs Veeam Backup & Replication. Source is undated/unverified, but Veeam exploitation is broadly documented (Sophos X-Ops, Rapid7). |
| **P3** | T1021.001/.002 | Remote Services: RDP / SMB Admin Shares | Cross-group | Standard lateral movement via RDP, PsExec/PAExec over SMB, WMI, Impacket. High false positive rate in enterprise environments with 14,500 branches. Requires baselining before deployment. |
| **P3** | T1204.001 | User Execution: ClickFix Social Engineering | Qilin (via StealC), Lampion (FS-targeted) | ClickFix surged 517% in 2025 (ESET H1 2025). Documented ClickFix → StealC → Qilin chain (Sophos). May overlap with existing email/endpoint controls — validate existing coverage before building new rules. |
| **P3** | — | Unmonitored Device Pivot (Architectural Gap) | Akira | Akira encrypted a network from an unmonitored Linux webcam after EDR quarantined the initial payload (Vectra AI). Not a detection rule — this is a network segmentation and asset inventory gap. Included for awareness: detection coverage has a physical boundary at the EDR agent. |

---

# Section 2: Per-Technique Detection Tables

## P1 — Priority 1 Techniques

These four techniques are ranked P1 because they are actively used by multiple groups targeting financial services, directly relevant to Hartwell's technology stack, and require behavioral detection approaches — tool-signature detections are already being evaded.

---

### P1-1: BYOVD / EDR Evasion (T1562.001 — Impair Defenses: Disable or Modify Tools)

| Field | Content |
|---|---|
| **Technique** | T1562.001 — Impair Defenses: Disable or Modify Tools (BYOVD variant) |
| **Priority** | P1 — 8+ groups actively sharing EDRKillShifter; Reynolds ransomware (Feb 2026) specifically terminates CrowdStrike Falcon. |
| **Observable Behavior** | A vulnerable signed driver is loaded into the kernel, then used to terminate or blind EDR processes. Reynolds embeds the driver directly in the ransomware payload, eliminating a separate staging step. |
| **Telemetry Source** | Sysmon 6 (DriverLoad) — driver loading events with signature metadata. Sysmon 1 (ProcessCreate) — process spawning the driver load. Windows 7045 (Service Installed) — new service registration for driver. Windows 4688 (Process Creation) — with command-line logging enabled. |
| **Known Indicators** | EDRKillShifter variants targeting TrueSight driver (2,500+ variants observed per Vectra AI). Reynolds terminates processes for CrowdStrike Falcon, Cortex XDR, Sophos, and Symantec by name. Newly installed kernel-mode drivers with revoked or expired signatures. |
| **Group-Specific** | EDRKillShifter shared across Medusa, Play, Qilin, DragonForce, INC Ransom, and others. ESET identified "QuadSwitcher" orchestrating cross-group sharing. Reynolds (Feb 2026) is the latest evolution — driver embedded in payload, no staging step. |
| **Why This Priority** | P1 — Hartwell's primary EDR (CrowdStrike Falcon) is explicitly named as a termination target. If BYOVD succeeds, all endpoint-dependent detections fail simultaneously. This detection must operate independently of the EDR it protects. |

---

### P1-2: LSASS Credential Dumping (T1003.001 — OS Credential Dumping: LSASS Memory)

| Field | Content |
|---|---|
| **Technique** | T1003.001 — OS Credential Dumping: LSASS Memory |
| **Priority** | P1 — Cross-group; universal ransomware kill chain step. Mimikatz sekurlsa::logonpasswords is the most-used credential dumping module (Red Canary). |
| **Observable Behavior** | A process opens a handle to lsass.exe with memory read permissions, then reads or dumps LSASS process memory to extract credentials. |
| **Telemetry Source** | Sysmon 10 (ProcessAccess) — TargetImage = lsass.exe with GrantedAccess values indicating memory read (0x1010, 0x1410, 0x1438). Windows 4656 / 4663 (Handle Request / Object Access) — on LSASS process object. |
| **Known Indicators** | Mimikatz module sekurlsa::logonpasswords. Non-standard parent processes accessing lsass.exe (anything other than csrss.exe, services.exe, wininit.exe, lsaiso.exe). GrantedAccess bitmasks associated with memory read operations. |
| **Group-Specific** | Akira documented using Mimikatz followed by Rubeus Kerberoasting (Security Boulevard, Nov 2025). Qilin affiliates modify WDigest registry before LSASS dumping to ensure plaintext credentials are present (see P2-3). |
| **Why This Priority** | P1 — Precedes all lateral movement and privilege escalation. Median time from initial access to AD compromise is 11 hours (Sophos 2025). Detecting LSASS access is the highest-value early-kill-chain detection available. |

---

### P1-3: Exfiltration to Cloud Storage (T1567.002 — Exfiltration Over Web Service: to Cloud Storage)

| Field | Content |
|---|---|
| **Technique** | T1567.002 — Exfiltration Over Web Service: Exfiltration to Cloud Storage |
| **Priority** | P1 — Rclone present in 57% of ransomware incidents (ReliaQuest). 96% of attacks in 2025 involved data exfiltration (BlackFog Q3 2025). Tool-name detection is trivially evaded; behavioral rebuild required. |
| **Observable Behavior** | Large-volume outbound transfers to cloud storage providers (MEGA.io, Backblaze, others), typically occurring off-hours. Rclone, WinSCP, cURL, or Cyberduck used as transfer tools — often renamed to avoid signature detection. |
| **Telemetry Source** | Sysmon 3 (NetworkConnect) — outbound connections to known cloud storage domains/IPs. Sysmon 1 (ProcessCreate) — process creation with command-line arguments referencing cloud storage configurations. Proxy/firewall logs — volume and destination analysis for MEGA.io, Backblaze B2, and similar services. |
| **Known Indicators** | Destinations: MEGA.io (Rclone default for LockBit, Black Basta, BlackSuit, Medusa), Backblaze B2 (Cyberduck, Qilin affiliates). Tools: Rclone (frequently renamed), WinSCP, cURL, FileZilla (INC Ransom). 79% of exfiltration occurs off-hours; median 72.98 hours after initial access (Sophos 2025). |
| **Group-Specific** | Qilin affiliates use Cyberduck for multipart uploads to Backblaze (source undated/unverified). INC Ransom uses FileZilla for FTP-based exfiltration (ReliaQuest). Rclone is cross-group standard. |
| **Why This Priority** | P1 — Exfiltration is the prerequisite for double/triple extortion, which is now the dominant ransomware model. Detecting Rclone by filename is a signature detection that current groups evade by renaming the binary. This must be rebuilt as a behavioral detection: anomalous volume + cloud storage destination + off-hours timing. |

---

### P1-4: Remote Management Tool Abuse (T1219 — Remote Access Software)

| Field | Content |
|---|---|
| **Technique** | T1219 — Remote Access Software (RMM Abuse) |
| **Priority** | P1 — 36% of IR cases, 32 different tools documented (Arctic Wolf 2025). Legitimate tools used maliciously — signature-based detection is fundamentally inadequate. |
| **Observable Behavior** | Installation or execution of a remote management tool outside of approved IT management channels — particularly on high-value targets (domain controllers, backup servers) or by accounts not associated with IT administration. |
| **Telemetry Source** | Sysmon 1 (ProcessCreate) — RMM tool process creation with parent process and user context. Windows 7045 (Service Installed) — new service registration for RMM agent. Windows 4688 (Process Creation) — with command-line logging. Proxy/firewall logs — outbound connections to RMM vendor infrastructure. |
| **Known Indicators** | Tools documented in ransomware chains: ConnectWise ScreenConnect (signed malicious droppers targeting FS, per CyberProof May 2025), AnyDesk (Medusa, Rhysida, Cactus), Datto RMM (Akira — installed on domain controllers). |
| **Group-Specific** | Akira installs Datto RMM on domain controllers specifically to blend into routine IT automation (Barracuda 2025). UNC5952 used signed malicious ConnectWise ScreenConnect droppers targeting global financial organizations (CyberProof, May 2025). Black Basta's leaked internal messages confirmed systematic RMM abuse as standard operating procedure (Intel 471, Feb 2025). |
| **Why This Priority** | P1 — These are legitimate tools, which means any detection based on tool name or binary hash will generate false positives against real IT use and false negatives against renamed/repackaged instances. Behavioral approach required: flag RMM installations by non-IT accounts, on non-standard targets (DCs, backup servers), or outside approved change windows. |

---

## P2 — Priority 2 Techniques

P2 techniques are actively used by groups targeting financial services and relevant to Hartwell's stack, but either have higher detection fidelity (lower build complexity), affect fewer groups, or have unverified source attribution. Build these after P1 detections are operational.

---

### P2-1: Kerberoasting (T1558.003 — Steal or Forge Kerberos Tickets: Kerberoasting)

| Field | Content |
|---|---|
| **Technique** | T1558.003 — Steal or Forge Kerberos Tickets: Kerberoasting |
| **Priority** | P2 — Akira-attributed; high detection fidelity via service ticket anomalies. |
| **Observable Behavior** | A single account requests TGS tickets for multiple service principal names (SPNs) in rapid succession, targeting accounts with weak or crackable passwords. Rubeus is the documented tool. |
| **Telemetry Source** | Windows 4769 (Kerberos Service Ticket Request) — filter for RC4 encryption (0x17) from accounts requesting tickets for multiple SPNs. Windows 4768 (Kerberos TGT Request) — for associated authentication context. |
| **Known Indicators** | Rubeus as Kerberoasting tool in Akira chain (Security Boulevard, Nov 2025). Anomalous volume of 4769 events from a single source account. Encryption type 0x17 (RC4) in ticket requests — legitimate services increasingly use AES. |
| **Group-Specific** | Akira uses Rubeus for Kerberoasting after initial Mimikatz credential dump, as a privilege escalation step before lateral movement (Security Boulevard, Nov 2025). |
| **Why This Priority** | P2 — High detection fidelity (RC4 ticket requests from a single account are anomalous in modern environments), but narrower group attribution than P1 techniques. |

---

### P2-2: DCSync (T1003.006 — OS Credential Dumping: DCSync)

| Field | Content |
|---|---|
| **Technique** | T1003.006 — OS Credential Dumping: DCSync |
| **Priority** | P2 — Cross-group; enables domain-wide persistence via Golden Ticket. |
| **Observable Behavior** | A non-domain-controller host initiates directory replication service (DRS) requests to a domain controller, extracting the KRBTGT hash or other credential material. |
| **Telemetry Source** | Windows 4662 (Directory Service Access) — operations on domain replication objects (DS-Replication-Get-Changes, DS-Replication-Get-Changes-All) from non-DC source addresses. Sysmon 3 (NetworkConnect) — RPC connections to DCs on replication ports from non-DC hosts. |
| **Known Indicators** | KRBTGT hash extraction as precursor to Golden Ticket creation (Qualys ETM Defense Guide, Feb 2026). Replication requests originating from workstations or member servers rather than domain controllers. |
| **Group-Specific** | Cross-group technique. Research base documents it as a standard post-credential-dump escalation step without single-group attribution. |
| **Why This Priority** | P2 — Domain-wide impact if successful (Golden Ticket grants persistent, unrestricted domain access). Ranked P2 rather than P1 because the prerequisite (LSASS dumping, P1-2) must succeed first — detecting the precursor is higher value. |

---

### P2-3: WDigest Registry Modification (T1112 — Modify Registry)

| Field | Content |
|---|---|
| **Technique** | T1112 — Modify Registry (WDigest credential caching) |
| **Priority** | P2 — Qilin-attributed; near-zero false positive rate. |
| **Observable Behavior** | WDigest `UseLogonCredential` registry value set to `1`, forcing plaintext credential storage in LSASS memory. This is a precursor to LSASS dumping (P1-2). |
| **Telemetry Source** | Sysmon 13 (RegistryEvent — Value Set). Windows 4657 (Registry Value Modified) — requires auditing enabled on the target key. |
| **Known Indicators** | Registry key: `HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest`, value `UseLogonCredential` = `1`. |
| **Group-Specific** | Qilin affiliates modify this key before LSASS dumping to ensure plaintext credentials are available. Source is undated/unverified (GAP-R03), but the technique itself is well-documented in public DFIR literature. |
| **Why This Priority** | P2 — Near-zero false positive rate (legitimate WDigest modification is rare in modern environments). Low build complexity. Paired with P1-2 (LSASS dumping), this creates a two-stage detection chain: WDigest modification as early warning, LSASS access as confirmation. |

---

### P2-4: C2 via Trusted Platforms (T1102 — Web Service)

| Field | Content |
|---|---|
| **Technique** | T1102 — Web Service (C2 via trusted cloud platforms) |
| **Priority** | P2 — Multiple groups; abuses trusted services that bypass traditional network-based detection. |
| **Observable Behavior** | Malware communicates with attacker-controlled infrastructure via legitimate cloud services — Microsoft Graph API (Havoc framework), Google Sheets (GC2 framework) — disguising C2 traffic as normal cloud API calls. |
| **Telemetry Source** | Proxy/firewall logs — API call patterns to Microsoft Graph and Google Sheets APIs from non-standard processes or endpoints. Sysmon 3 (NetworkConnect) — outbound connections to graph.microsoft.com or sheets.googleapis.com from processes not associated with legitimate M365/Google Workspace usage. Sysmon 1 (ProcessCreate) — parent-child process trees where unusual processes spawn cloud API connections. |
| **Known Indicators** | Havoc C2 with Microsoft Graph API integration (AlphaHunt, 2025–2026). GC2 (Google Sheets C2) observed in Fog ransomware (Picus Security, 2025). Non-browser, non-Office processes making API calls to graph.microsoft.com or sheets.googleapis.com. |
| **Group-Specific** | Fog ransomware used GC2 for Google Sheets-based C2 (Picus Security, 2025). Havoc with Graph API is an emerging cross-group capability. |
| **Why This Priority** | P2 — These C2 channels abuse services Hartwell uses legitimately (M365, potentially Google Workspace), making network-layer blocking impractical. Detection must be behavioral: which processes are calling these APIs, and do they match expected application behavior? Ranked P2 because the technique is emerging rather than dominant, and standard C2 (Cobalt Strike, Sliver, Brute Ratel) remains more prevalent. |

---

### P2-5: Veeam Backup Credential Dumping (T1555 — Credentials from Password Stores)

| Field | Content |
|---|---|
| **Technique** | T1555 — Credentials from Password Stores (Veeam Backup) |
| **Priority** | P2 — Akira-attributed; Hartwell runs Veeam Backup & Replication. |
| **Observable Behavior** | PowerShell commands query the Veeam credential store to extract stored backup credentials, which often include domain admin or service account passwords. |
| **Telemetry Source** | Windows 4104 (PowerShell Script Block Logging) — script blocks referencing Veeam credential retrieval functions. Sysmon 1 (ProcessCreate) — PowerShell execution with command-line arguments targeting Veeam APIs or database. Windows 4688 (Process Creation) — with command-line logging enabled. |
| **Known Indicators** | PowerShell commands targeting Veeam credential storage (specific commands undated/unverified per GAP-R03). Veeam Backup & Replication CVE-2024-40711 (CVSS 9.8, deserialization RCE) exploited by Akira, Fog, and Frag — Sophos X-Ops tracked 4+ incidents combining VPN + Veeam exploitation. CVE-2025-23120 (CVSS 9.9, domain-joined backup servers) disclosed March 2025. |
| **Group-Specific** | Akira dumps Veeam backup credentials via PowerShell (source undated/unverified). Broader Veeam exploitation is well-documented: 20%+ of Rapid7 2024 IR cases involved Veeam exploitation. |
| **Why This Priority** | P2 — Hartwell runs Veeam, making this directly relevant. Ranked P2 rather than P1 because the specific PowerShell-based credential dump procedure is unverified (GAP-R03), and version/patch status of Hartwell's Veeam deployment is unknown (GAP-003). Telemetry dependency: confirm PowerShell Script Block Logging is enabled on Veeam servers. |

---

## P3 — Priority 3 Techniques

P3 techniques are documented in the research base and relevant to financial services ransomware, but present higher false positive rates requiring significant baselining, overlap with likely existing coverage, or represent architectural gaps rather than detection rule opportunities. Build or revisit these after P1 and P2 detections are operational and tuned.

---

### P3-1: Lateral Movement via RDP and SMB (T1021.001 / T1021.002 — Remote Services)

| Field | Content |
|---|---|
| **Technique** | T1021.001 — Remote Services: RDP / T1021.002 — Remote Services: SMB/Windows Admin Shares |
| **Priority** | P3 — Cross-group standard; high false positive rate in large enterprise environments. |
| **Observable Behavior** | Lateral movement via RDP sessions, PsExec/PAExec execution over SMB admin shares (C$, ADMIN$), WMI remote execution, and Impacket-based SMB operations. Primary targets are VMware ESXi hypervisors and domain controllers. |
| **Telemetry Source** | Windows 4624 (Logon Type 10 for RDP, Type 3 for SMB). Windows 5140/5145 (Network Share Access) — access to admin shares from non-administrative workstations. Sysmon 1 (ProcessCreate) — PsExec/PAExec service binary creation on remote hosts. Windows 7045 (Service Installed) — PsExec service installation pattern. |
| **Known Indicators** | PsExec/PAExec service names (default: PSEXESVC). Impacket default named pipes and service names. RDP sessions originating from servers or service accounts that don't normally initiate interactive sessions. Admin share access patterns from non-IT accounts. |
| **Group-Specific** | Cross-group — RDP, PsExec, WMI, and Impacket are standard lateral movement tools across all documented groups. ESXi hypervisors are primary targets for encryption (multiple groups). |
| **Why This Priority** | P3 — RDP and SMB are legitimate enterprise protocols used heavily across 14,500 branches. False positive rate will be high without per-environment baselining. Validate existing coverage first — Hartwell's SOC likely has some lateral movement detection in place. Effective detection requires behavioral context: source-destination pairs, time-of-day, account type, and target system sensitivity. |

---

### P3-2: ClickFix Social Engineering (T1204.001 — User Execution: Malicious Link)

| Field | Content |
|---|---|
| **Technique** | T1204.001 — User Execution: Malicious Link (ClickFix variant) |
| **Priority** | P3 — 517% surge in 2025; documented FS-targeting campaign and Hartwell prior incident. Likely overlaps existing email/endpoint controls. |
| **Observable Behavior** | User is socially engineered into executing a PowerShell command or script via a fake CAPTCHA or browser prompt. The executed command downloads and runs an infostealer (StealC, Lumma) or banking malware (Lampion). |
| **Telemetry Source** | Sysmon 1 (ProcessCreate) — PowerShell or cmd.exe spawned by browser process (chrome.exe, msedge.exe, firefox.exe) with encoded or obfuscated command-line arguments. Windows 4104 (PowerShell Script Block Logging) — decoded script content from ClickFix payloads. Proxy logs — connections to ClickFix infrastructure following browser-spawned PowerShell execution. |
| **Known Indicators** | ClickFix → StealC → Qilin full attack chain documented by Sophos: stolen VPN credentials sold by IAB approximately one month post-compromise. Microsoft identified a May 2025 ClickFix campaign targeting Portuguese FS organizations with Lampion banking malware. Hartwell experienced a January 2025 ClickFix/Lumma incident at a branch workstation. |
| **Group-Specific** | Qilin (via StealC infostealer and IAB pipeline, per Sophos 2025). Lampion banking malware targeting FS organizations (Microsoft, Aug 2025). Nation-state adoption by MuddyWater (Iran) and APT28 (Russia) reported by Proofpoint. |
| **Why This Priority** | P3 — Hartwell has direct experience with this technique (Jan 2025 incident). Ranked P3 rather than higher because CrowdStrike Falcon likely detects the payload execution stage, and email gateway controls should catch distribution. Validate existing coverage before building new rules. The detection gap is more likely at the browser-to-PowerShell handoff than at the payload stage. |

---

### P3-3: Unmonitored Device Pivot (Architectural Gap — No ATT&CK ID)

| Field | Content |
|---|---|
| **Technique** | No direct ATT&CK mapping — Lateral movement to unmonitored/agentless devices |
| **Priority** | P3 — Akira-demonstrated; architectural gap, not a detection rule. |
| **Observable Behavior** | After EDR quarantines the initial payload on a monitored endpoint, the attacker pivots to an unmonitored device on the same network segment (in the documented case, a Linux-based webcam) and encrypts the network from that device. |
| **Telemetry Source** | Network-layer detection only — no endpoint telemetry available on agentless devices. NetFlow/firewall logs — anomalous SMB or encryption-related traffic originating from IoT/OT device IP ranges. DHCP/ARP logs — for device inventory correlation. |
| **Known Indicators** | SMB traffic or large-volume file operations originating from IP addresses assigned to IoT, printer, or other non-endpoint device ranges. Encryption activity (mass file rename patterns) observed on file servers where the source is not a managed endpoint. |
| **Group-Specific** | Akira pivoted to a Linux-based webcam on the same network after EDR quarantined the initial payload, encrypting from an agentless device (Vectra AI, March 2025). |
| **Why This Priority** | P3 — This is not a detection rule Priya's team can build in the traditional sense. It's an architectural gap: detection coverage ends at the EDR agent boundary. Mitigation requires network segmentation (isolating IoT/OT from production file servers) and asset inventory (identifying unmanaged devices). Included here for completeness — if Priya's team implements network-layer anomaly detection, this becomes detectable. Otherwise, this is a request to infrastructure and security architecture. |

---

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

---

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

---

# Section 5: Telemetry Dependency Checklist

Every detection in this brief depends on specific telemetry sources being active, configured correctly, and forwarding to Sentinel. This checklist is ordered by impact — sources supporting the most or most critical detections are listed first.

**Action required:** Priya's team should confirm each source's status before beginning detection builds. A detection built against a telemetry source that isn't active will never fire.

---

## Tier 1 — Required for P1 Detections (Do Not Build Without These)

| # | Telemetry Source | Specific Requirements | Detections Supported | Impact if Missing | Status |
|---|---|---|---|---|---|
| 1 | **Sysmon 1 (ProcessCreate)** | Sysmon installed and configured to log process creation with full command-line capture, parent process tracking, and user context. | P1-1 (BYOVD — process spawning driver load), P1-3 (exfil tool process creation), P1-4 (RMM tool installation), P2-4 (C2 process trees), P2-5 (PowerShell targeting Veeam), P3-1 (PsExec), P3-2 (ClickFix browser→PowerShell) | Loss of visibility into 10 of 12 detection tables. Sysmon 1 is the single most critical telemetry dependency in this brief. | ☐ Confirmed ☐ Unconfirmed |
| 2 | **Sysmon 10 (ProcessAccess)** | Sysmon configured to log process access events, specifically access to lsass.exe with GrantedAccess bitmask capture. | P1-2 (LSASS credential dumping) | P1-2 becomes undetectable. LSASS dumping is the highest-value early-kill-chain detection. | ☐ Confirmed ☐ Unconfirmed |
| 3 | **Sysmon 6 (DriverLoad)** | Sysmon configured to log kernel driver load events with driver signature metadata (signed/unsigned, signer name, hash). | P1-1 (BYOVD — vulnerable driver loading) | P1-1 loses its primary detection signal. BYOVD detection degrades to secondary indicators only (EDR process termination). | ☐ Confirmed ☐ Unconfirmed |
| 4 | **Proxy / Firewall Logs (Centralized)** | Outbound connection logs from centralized proxy or firewall infrastructure, forwarded to Sentinel. Must include destination domain/IP, source IP, volume, and timestamp. | P1-3 (exfil to cloud storage — destination and volume analysis), P1-4 (RMM — outbound connections to RMM vendor infrastructure), P2-4 (C2 — domain-level cloud API connections) | P1-3 exfiltration detection and P2-4 C2 detection both degrade significantly. Branch-level coverage depends on SD-WAN routing (Gap 1). | ☐ Confirmed ☐ Unconfirmed |
| 5 | **Windows 7045 (Service Installed)** | Windows Security event log forwarding to Sentinel with service installation events enabled. | P1-1 (BYOVD — driver service registration), P1-4 (RMM — RMM agent service installation), P3-1 (PsExec service pattern) | Loss of secondary detection signal for BYOVD and primary signal for PsExec lateral movement detection. | ☐ Confirmed ☐ Unconfirmed |
| 6 | **Windows 4688 (Process Creation)** | Windows Security event log with process creation auditing enabled and command-line logging enabled (requires GPO: "Include command line in process creation events"). | P1-1 (BYOVD), P1-4 (RMM), P2-5 (Veeam credential dump) | Fallback for environments where Sysmon is not deployed on all endpoints. If Sysmon 1 is confirmed across the estate, 4688 provides redundancy. If Sysmon is partial, 4688 fills the gap on non-Sysmon hosts. | ☐ Confirmed ☐ Unconfirmed |

---

## Tier 2 — Required for P2 Detections

| # | Telemetry Source | Specific Requirements | Detections Supported | Impact if Missing | Status |
|---|---|---|---|---|---|
| 7 | **Windows 4769 (Kerberos Service Ticket Request)** | Kerberos Service Ticket Operations audit policy enabled on domain controllers. Events forwarded to Sentinel. | P2-1 (Kerberoasting — RC4 ticket request anomalies) | P2-1 becomes undetectable. Kerberoasting has no alternative telemetry source. | ☐ Confirmed ☐ Unconfirmed |
| 8 | **Windows 4662 (Directory Service Access)** | Directory Service Access auditing enabled on domain controllers, specifically for DS-Replication-Get-Changes and DS-Replication-Get-Changes-All operations. | P2-2 (DCSync — replication requests from non-DC sources) | P2-2 becomes undetectable. DCSync has no alternative telemetry source. | ☐ Confirmed ☐ Unconfirmed |
| 9 | **Sysmon 13 (RegistryEvent — Value Set)** | Sysmon configured to log registry value modification events. Filter should include the WDigest registry path at minimum. | P2-3 (WDigest registry modification) | P2-3 loses its primary detection signal. Windows 4657 provides a fallback but requires Object Access auditing enabled on the specific registry key. | ☐ Confirmed ☐ Unconfirmed |
| 10 | **Windows 4104 (PowerShell Script Block Logging)** | PowerShell Script Block Logging enabled via GPO. Must be active on Veeam servers and branch workstations at minimum. | P2-5 (Veeam credential dump — PowerShell script content), P3-2 (ClickFix — decoded payload content) | P2-5 degrades to process-level detection only (Sysmon 1), losing visibility into script content. P3-2 loses decoded payload visibility. | ☐ Confirmed ☐ Unconfirmed |
| 11 | **Sysmon 3 (NetworkConnect)** | Sysmon configured to log outbound network connections with process-level attribution (process name, PID, destination IP/domain). Note: high-volume event — may require targeted deployment. | P2-4 (C2 via trusted platforms — process-to-connection correlation) | P2-4 degrades to domain-level detection only via proxy logs. Cannot distinguish legitimate M365 API usage from Havoc C2 without process context. | ☐ Confirmed ☐ Unconfirmed |

---

## Tier 3 — Required for P3 Detections and Coverage Expansion

| # | Telemetry Source | Specific Requirements | Detections Supported | Impact if Missing | Status |
|---|---|---|---|---|---|
| 12 | **Windows 4624 (Logon Events)** | Logon event auditing enabled across the estate. Type 10 (RDP) and Type 3 (Network/SMB) logons forwarded to Sentinel. | P3-1 (Lateral movement — RDP and SMB session tracking) | P3-1 becomes undetectable. Lateral movement via RDP/SMB has no alternative telemetry source without logon events. | ☐ Confirmed ☐ Unconfirmed |
| 13 | **Windows 5140/5145 (Network Share Access)** | Object Access auditing enabled for file shares, specifically admin shares (C$, ADMIN$). | P3-1 (Lateral movement — admin share access from non-administrative workstations) | Loses visibility into PsExec/Impacket-style lateral movement via admin shares. | ☐ Confirmed ☐ Unconfirmed |
| 14 | **NetFlow / Firewall Logs (Network Layer)** | NetFlow data or firewall session logs capturing internal east-west traffic, particularly SMB and file operation traffic between network segments. | P3-3 (Unmonitored device pivot — SMB traffic from IoT/OT IP ranges) | P3-3 architectural gap remains fully open. No detection of encryption activity originating from unmanaged devices. | ☐ Confirmed ☐ Unconfirmed |
| 15 | **Windows 4657 (Registry Value Modified)** | Object Access auditing enabled with SACL on WDigest registry key. Fallback for Sysmon 13. | P2-3 (WDigest — secondary source) | Redundancy loss only if Sysmon 13 is confirmed. Primary dependency if Sysmon 13 is unavailable. | ☐ Confirmed ☐ Unconfirmed |

---

## Summary: Minimum Viable Telemetry

To operationalize P1 detections, the following must be confirmed active and forwarding to Sentinel at minimum:

1. Sysmon 1 (ProcessCreate) with command-line capture
2. Sysmon 10 (ProcessAccess) targeting lsass.exe
3. Sysmon 6 (DriverLoad) with signature metadata
4. Centralized proxy/firewall logs with destination, volume, and timestamp
5. Windows 7045 (Service Installed)
6. Windows 4688 (Process Creation) with command-line logging — as fallback/redundancy for Sysmon 1

If any of items 1–4 are unconfirmed, the corresponding P1 detection cannot be built reliably. Confirm these before beginning P1 detection development.

---

*Questions or telemetry confirmation: Contact CTI team — Dana Mercer, Senior Analyst.*
