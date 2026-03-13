# Detection Engineering Brief: Ransomware TTPs Targeting Financial Services

**Derived From:** RB-2026-003 — Ransomware Threat to Financial Services  
**Date:** March 10, 2026  
**Consumer:** Detection Engineering, SOC Engineering, SIEM/EDR Query Developers  
**Question Answered:** What should we build detections against, and in what priority order?  
**Classification:** TLP:AMBER

---

## Detection Priorities

Ranked by prevalence across active financial sector ransomware groups (Qilin, Akira, Medusa) and likelihood of producing actionable telemetry. Priority 1 items appear across all three groups. Priority 2 items are group-specific but high-impact.

---

### Priority 1: Universal Across Target Groups

**Defense Evasion — BYOVD / EDRKillShifter (T1562.001)**

This is the single most critical detection gap. EDRKillShifter is shared across 8+ groups and directly terminates endpoint security processes by loading a vulnerable kernel driver.

| What to Detect | Telemetry Source | Notes |
|---|---|---|
| Vulnerable driver loading: `rwdrv.sys` (Akira), `NSecKrnl.sys`, `BdApiUtil.sys`, `GameDriverx64.sys` | Sysmon 6 (DriverLoad), EDR driver-load events | Reynolds (Feb 2026) embeds the driver in the payload — no separate staging step |
| Unsigned or known-vulnerable drivers loaded outside normal boot sequence | Sysmon 6, Windows CodeIntegrity logs | Allowlist-based detection is strongest; alert on any driver not in baseline |
| EDR service termination or tampering | EDR tamper protection alerts, Windows 7045 (ServiceInstall) | If your EDR offers tamper protection, verify it's enabled and monitored |

**Exfiltration — Rclone and Cloud Storage Tools (T1567)**

Rclone appears in 57% of ransomware incidents. Affiliates rename it to blend in.

| What to Detect | Telemetry Source | Notes |
|---|---|---|
| Rclone execution (any binary name) — detect by command-line args: `sync`, `copy`, `--transfers`, `--config`, `--bwlimit` | Sysmon 1 (ProcessCreate), EDR process telemetry | Commonly renamed to `svchost.exe`, `svhost.exe`, `explorer.exe` — command-line args are the reliable signal |
| Outbound connections to MEGA (`mega.nz`, `mega.co.nz`), Backblaze B2 (`backblazeb2.com`), unusual S3 endpoints | Network/proxy logs, DNS logs, firewall logs | From servers or non-standard endpoints = high signal |
| MEGAsync, AzCopy, Cyberduck, WinSCP execution on servers | Sysmon 1, application allowlist alerts | These tools have no legitimate use on most server infrastructure |
| Large outbound data transfers (>100MB) to cloud storage IPs during off-hours | NDR, firewall flow logs | Baseline normal transfer patterns first; alert on deviations |

**Persistence — RMM Tool Abuse (T1219)**

AnyDesk, ScreenConnect, MeshAgent, and Splashtop appeared in 79% of ransomware IR engagements in 2025.

| What to Detect | Telemetry Source | Notes |
|---|---|---|
| Unauthorized RMM tool installation or execution | Sysmon 1, application allowlist, EDR | Maintain a list of authorized RMM tools; alert on anything else |
| ScreenConnect, AnyDesk, MeshAgent connecting to non-corporate relay infrastructure | Network/proxy logs | If your org uses ScreenConnect legitimately, alert on connections to relay servers you don't control |
| New Windows services for RMM tools (e.g., `ScreenConnect Client`) | Windows 7045 (ServiceInstall), Sysmon 12/13 (Registry) | Installation creates services and registry entries |

**Credential Access — LSASS and Credential Dumping (T1003)**

| What to Detect | Telemetry Source | Notes |
|---|---|---|
| LSASS process access from non-standard processes | Sysmon 10 (ProcessAccess) with TargetImage `lsass.exe` | High-value but noisy — tune by excluding known legitimate callers |
| Mimikatz indicators: process names, command-line patterns (`sekurlsa::`, `kerberos::`) | Sysmon 1, EDR | Often Themida-packed; behavioral detection (LSASS access patterns) more reliable than signature |
| WDigest registry modification: `UseLogonCredential` set to `1` | Sysmon 13 (RegistrySetValue) at `HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest` | Qilin-specific TTP; forces plaintext credential storage in LSASS |
| Kerberoasting: high volume of TGS requests (T1558.003) | Windows 4769 (Kerberos Service Ticket Request) with encryption type `0x17` (RC4) | Akira uses this for service account credential extraction; correlate with non-service accounts requesting service tickets |

**Lateral Movement — RDP and SMB (T1021.001, T1021.002)**

| What to Detect | Telemetry Source | Notes |
|---|---|---|
| RDP connections from unexpected source hosts | Windows 4624 (Logon Type 10), network flow logs | Baseline normal RDP patterns; alert on new source→destination pairs |
| PsExec / PAExec service creation on remote hosts | Windows 7045 (ServiceInstall) with service names like `PSEXESVC`, `PAExec-*` | Short-lived services — detect on creation, not running state |
| Impacket-based WMI/SMB execution | Windows 4648 (Explicit Credential Logon), Sysmon 1 with unusual parent processes for `cmd.exe` or `powershell.exe` | Impacket WMI execution often spawns `cmd.exe` under `WmiPrvSE.exe` with encoded commands |

---

### Priority 2: Group-Specific High-Value Detections

**Akira-Specific**

| What to Detect | Telemetry Source | Notes |
|---|---|---|
| Local account creation: username `itadm` | Windows 4720 (User Account Created), Sysmon 1 if `net user` used | Akira's consistent persistence pattern |
| Veeam credential extraction via PowerShell | Sysmon 1 with PowerShell accessing Veeam credential stores; Veeam logs | Targets backup server credentials specifically |
| File extension `.akira` on encrypted files | EDR file-write telemetry, Sysmon 11 (FileCreate) | Late-stage indicator — encryption already underway |
| Ransom note creation: `akira_readme.txt` | Sysmon 11 (FileCreate) | Same — late-stage but useful for automated alerting |

**Qilin-Specific**

| What to Detect | Telemetry Source | Notes |
|---|---|---|
| Cyberduck execution (multipart uploads to Backblaze B2) | Sysmon 1, network logs to `backblazeb2.com` | Qilin affiliate exfiltration tool of choice |
| Ransom note: `README-WARNING.txt` | Sysmon 11 (FileCreate) | File extension varies per victim (e.g., `.MmXReVIxLV`) |

**Medusa-Specific**

| What to Detect | Telemetry Source | Notes |
|---|---|---|
| GoAnywhere MFT exploitation (CVE-2025-10035) | GoAnywhere application logs, WAF/IDS | Deserialization RCE, CVSS 10.0 — if your org runs GoAnywhere, this is critical |
| Heavy RMM tool chaining (multiple RMM tools on single host) | Sysmon 1, service creation logs | Medusa affiliates use multiple RMM tools for redundant persistence |

---

### Priority 3: Pre-Encryption / Impact Stage

These are late-stage indicators. If you're seeing these, the attack is well advanced — but detection here still enables containment.

| What to Detect | Telemetry Source | Notes |
|---|---|---|
| Shadow copy deletion: `vssadmin delete shadows /all /quiet` | Sysmon 1 (ProcessCreate), Windows VSS logs | T1490 — near-universal pre-encryption step |
| Backup service termination: stopping Veeam, SQL Server, backup agents | Windows 7036 (Service Status Change), Sysmon 1 | T1489 — disables recovery before encryption |
| WinRAR/7-Zip staging: command-line archiving of specific directories | Sysmon 1 with command-line args referencing `a -r`, specific directory paths | T1560 — data staging for exfiltration; look for archiving of `C:\Users`, shared drives, database directories |

---

## ATT&CK Coverage Map

Summary of techniques covered by the detections above, mapped to the research base's full ATT&CK table.

| Technique | Covered Above | Detection Feasibility | Priority |
|---|---|---|---|
| T1562.001 — Disable Security Tools (BYOVD) | Yes | Medium — requires driver-load monitoring | 1 |
| T1567 — Exfiltration to Cloud Storage | Yes | High — command-line and network signals | 1 |
| T1219 — Remote Access Software | Yes | High — allowlist-based | 1 |
| T1003 — OS Credential Dumping | Yes | Medium — noisy, needs tuning | 1 |
| T1558.003 — Kerberoasting | Yes | Medium — requires 4769 correlation | 1 |
| T1021.001/.002 — RDP/SMB Lateral Movement | Yes | Medium — requires baselining | 1 |
| T1490 — Inhibit System Recovery | Yes | High — distinct command-line | 3 |
| T1489 — Service Stop | Yes | High — service status telemetry | 3 |
| T1560 — Archive Collected Data | Yes | Medium — command-line pattern | 3 |
| T1190 — Exploit Public-Facing Application | Not covered here | Depends on edge device vendor logging | — |
| T1078 — Valid Accounts | Partially (via credential monitoring) | Low — hard to distinguish from legitimate use | — |
| T1055 — Process Injection | Not covered here | Varies by injection method | — |

**[GAP]:** T1190 detection depends entirely on edge device vendor logging (Fortinet, SonicWall, Ivanti, Citrix). Detection engineering for initial access requires coordination with the network/infrastructure team to confirm log availability and forwarding to SIEM.

---

## Telemetry Dependencies

The detections above require the following telemetry sources to be active and forwarding to the SIEM:

| Source | Required For | Status |
|---|---|---|
| Sysmon (or equivalent EDR process telemetry) | Process creation, driver loads, registry changes, LSASS access, file creation | **[CONFIRM]** |
| Windows Security Event Log (4624, 4648, 4720, 4769, 7036, 7045) | Logon events, account creation, Kerberos, service changes | **[CONFIRM]** |
| Network/proxy/firewall logs | Outbound cloud storage connections, RMM relay traffic, large transfers | **[CONFIRM]** |
| DNS logs | Cloud storage domain resolution from unusual sources | **[CONFIRM]** |
| Application-specific logs (Veeam, GoAnywhere, VPN appliance) | Backup credential access, MFT exploitation, initial access | **[CONFIRM]** |

Items marked **[CONFIRM]** require validation that the telemetry is being collected and forwarded before building detections against it.

---

*Source: RB-2026-003 | Contact: [Analyst Name], CTI — [contact info]*
