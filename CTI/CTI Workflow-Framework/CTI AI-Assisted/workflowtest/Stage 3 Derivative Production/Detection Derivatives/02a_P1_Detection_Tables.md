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
