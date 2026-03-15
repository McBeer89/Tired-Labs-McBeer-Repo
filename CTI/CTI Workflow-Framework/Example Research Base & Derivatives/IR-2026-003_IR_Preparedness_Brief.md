# IR Preparedness Brief: Ransomware Kill Chain for Financial Services

**Derived From:** RB-2026-003 — Ransomware Threat to Financial Services  
**Date:** March 10, 2026  
**Consumer:** Incident Response Team, IR Lead  
**Question Answered:** What does the attack look like end-to-end, what artifacts should we expect, and what should our containment priorities be?  
**Classification:** TLP:AMBER

---

## Kill Chain Summary

The ransomware groups most likely to target financial services (Qilin, Akira, Medusa) follow a consistent kill chain with group-specific variations. The typical intrusion timeline from initial access to exfiltration/encryption ranges from hours to days — Akira in particular operates quickly once inside. The chain below represents the composite pattern across all three groups.

```
Initial Access          Establish Foothold       Credential Harvest
(Edge exploit or    →   (RMM tool + C2       →   (Mimikatz, LSASS,
 stolen creds)           framework)               Kerberoasting)
                                                        │
     ┌──────────────────────────────────────────────────┘
     ▼
Lateral Movement        Discovery & Staging      Exfiltration
(RDP, PsExec,       →   (Network enum,       →   (Rclone to cloud,
 WMI, Impacket)          archive with              WinSCP, MEGAsync)
                         WinRAR/7-Zip)
                                                        │
     ┌──────────────────────────────────────────────────┘
     ▼
Defense Evasion         Impact
(BYOVD/EDRKillShifter,  (Encryption and/or
 disable security)  →    extortion demand)
```

**Critical timing note:** Data exfiltration typically completes *before* encryption begins. In data-extortion-only attacks (Clop model, increasingly adopted by others), there is no encryption phase at all. If you detect the intrusion at the encryption stage, assume exfiltration already occurred.

---

## Phase-by-Phase: What to Expect

### Phase 1: Initial Access

**What happened:** The attacker gained entry through one of three pathways.

| Pathway | What It Looks Like | Artifacts |
|---|---|---|
| Edge device exploitation | Exploitation of VPN/firewall vulnerability (SonicWall CVE-2024-40766, Fortinet CVE-2024-55591, Ivanti CVE-2025-0282, GoAnywhere CVE-2025-10035) | VPN appliance logs showing anomalous authentication or command execution; IDS/WAF alerts; CISA KEV advisories for specific CVEs |
| Stolen credentials (IAB) | Login with valid credentials purchased from initial access broker; no exploit required | Successful authentication from unusual IP/geolocation; VPN login from unrecognized device; no corresponding MFA challenge if MFA not enforced |
| Phishing / social engineering | AI-generated phishing email, ClickFix technique (user pastes malicious command), or vishing targeting help desk | Email gateway logs; PowerShell execution from user context; help desk ticket for password reset from spoofed caller |

**Investigative question:** How did the attacker get in? This is the most critical gap in most ransomware investigations and the most valuable finding for post-incident remediation. Prioritize identifying the initial access vector.

### Phase 2: Establish Foothold

**What happened:** The attacker established persistent access using C2 frameworks and legitimate remote access tools.

| Tool | Artifacts to Look For |
|---|---|
| Cobalt Strike Beacon | Encoded PowerShell execution; HTTP/HTTPS beaconing on ports 443, 8443, 8080; named pipes (`\.\pipe\msagent_*`); malleable C2 profiles masquerading as legitimate traffic |
| Sliver implant | mTLS/DNS C2 traffic; Go-compiled binaries; unusual DNS TXT queries |
| Brute Ratel C4 | Designed for EDR evasion — may leave minimal endpoint artifacts; look for badger payloads, direct syscall patterns |
| AnyDesk | `AnyDesk.exe` execution; Windows service `AnyDesk`; connections to `*.net.anydesk.com` |
| ScreenConnect | `ScreenConnect.ClientService.exe`; service installation; connections to attacker-controlled relay (not corporate instance) |
| MeshAgent | `MeshAgent.exe` or renamed binary; service installation; WebSocket connections to MeshCentral server |

**Akira-specific:** Look for local account creation with username **`itadm`** (Windows Event 4720). This is a consistent Akira persistence indicator.

**Investigative question:** How many persistence mechanisms did the attacker install? Assume more than one. Failure to find all persistence before remediation leads to re-compromise.

### Phase 3: Credential Harvest

**What happened:** The attacker harvested credentials to enable lateral movement and privilege escalation.

| Technique | Artifacts |
|---|---|
| Mimikatz / LSASS dump | Process access to `lsass.exe` from unexpected parent (Sysmon EID 10); Mimikatz binary (often Themida-packed, random filename); `sekurlsa::logonpasswords` in command history |
| WDigest registry modification (Qilin) | Registry value `UseLogonCredential` set to `1` at `HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest` (Sysmon EID 13) |
| Kerberoasting (Akira) | High volume of Kerberos TGS requests (Windows 4769) with RC4 encryption type (`0x17`) from a single account; targeted service accounts |
| Veeam credential extraction (Akira) | PowerShell commands accessing Veeam credential stores; Veeam Backup & Replication logs showing unauthorized access |
| DonPAPI | DPAPI credential extraction — look for access to browser credential stores, Wi-Fi keys, Credential Manager entries |
| NetExec / LaZagne | Command-line execution with credential harvesting flags; results written to local files |

**Investigative question:** What credentials were compromised? This determines the scope of required password resets and whether domain-level compromise occurred (domain admin, service accounts, Kerberos TGT).

### Phase 4: Lateral Movement

**What happened:** The attacker moved through the network toward high-value targets (domain controllers, file servers, VMware ESXi hypervisors, backup servers).

| Method | Artifacts |
|---|---|
| RDP (T1021.001) | Windows 4624 (Logon Type 10) from unexpected source IPs; RDP bitmap cache on source machine; `mstsc.exe` execution |
| PsExec / PAExec (T1021.002) | Service creation on remote hosts: service names `PSEXESVC`, `PAExec-*` (Windows 7045); binary dropped to `ADMIN$` share |
| WMI (T1047) | `WmiPrvSE.exe` spawning `cmd.exe` or `powershell.exe`; Windows 4648 (Explicit Credential Logon); DCOM network traffic |
| Impacket | Python-based SMB/WMI execution; unusual `cmd.exe` command-line patterns with encoded commands; `smbexec`/`wmiexec` signatures |

**High-value targets to check for attacker access:**
- Domain controllers (credential harvesting, GPO modification)
- VMware ESXi hypervisors (single-point encryption of entire virtualized environment)
- Veeam / backup infrastructure (credential extraction, backup deletion)
- File servers / NAS (data staging for exfiltration)

**Investigative question:** Which systems did the attacker access? Lateral movement artifacts establish the blast radius and determine what systems need forensic review.

### Phase 5: Discovery, Staging, and Exfiltration

**What happened:** The attacker identified valuable data, staged it for exfiltration, and transferred it out.

| Step | Artifacts |
|---|---|
| Network discovery | Execution of `Advanced IP Scanner`, `SoftPerfect Network Scanner`, `nltest`, `net group "Domain Admins"`, `net share` |
| Data staging | WinRAR or 7-Zip command-line archiving: `rar a -r`, `7z a` with arguments referencing specific directories; archives appearing in staging directories (often `C:\Temp`, `C:\ProgramData`, user profile dirs) |
| Exfiltration via Rclone | Rclone binary (likely renamed to `svchost.exe`); command-line args: `sync`, `copy`, `--transfers`, `--config`; outbound connections to cloud storage (MEGA, Backblaze B2, S3); rclone config file (may contain attacker's cloud credentials) |
| Exfiltration via other tools | WinSCP (`WinSCP.exe`), MEGAsync (`MEGAsyncSetup.exe`), AzCopy, Cyberduck (Qilin); large outbound transfers (>100MB) to unusual destinations |

**Investigative question:** What data was exfiltrated, and how much? This determines breach notification obligations (SEC, FINRA, state AGs), client impact, and regulatory exposure. The Rclone config file, if recovered, may reveal the attacker's destination storage and account — preserve it.

### Phase 6: Defense Evasion and Impact

**What happened:** The attacker disabled security tools and deployed encryption (or issued extortion demand without encryption).

| Step | Artifacts |
|---|---|
| BYOVD / EDRKillShifter | Vulnerable driver loaded (`rwdrv.sys`, `NSecKrnl.sys`, `BdApiUtil.sys`, `GameDriverx64.sys`); EDR service stopped or crashed; Sysmon EID 6 (DriverLoad); Reynolds variant embeds driver in payload |
| Shadow copy deletion | `vssadmin delete shadows /all /quiet` in process creation logs; VSS event logs |
| Backup service termination | Veeam, SQL Server, backup agent services stopped (Windows 7036) |
| Encryption | File extension changes (`.akira` for Akira; variable for Qilin); ransom notes (`akira_readme.txt`, `README-WARNING.txt`); mass file-write activity |

**If no encryption occurs:** The attack is a data-extortion-only operation. The attacker will contact the organization (email, Tor portal, or direct phone call) with proof of stolen data and a payment demand. No ransom note may exist on disk.

---

## Containment Priorities (Time-Critical)

If an active ransomware intrusion is confirmed, execute in this order:

1. **Isolate confirmed compromised hosts** from the network. Do not power off — preserve volatile memory for forensics.
2. **Disable compromised accounts** — all credentials harvested by the attacker must be assumed compromised. If domain admin was compromised, initiate KRBTGT double-reset.
3. **Block attacker C2 and exfiltration channels.** Block known C2 IPs/domains at the firewall. Block outbound traffic to MEGA, Backblaze, and attacker-controlled cloud storage. Block unauthorized RMM tool traffic.
4. **Identify and remove all persistence mechanisms.** RMM tools, scheduled tasks, local accounts (check for `itadm`), services, registry run keys. Assume multiple persistence mechanisms.
5. **Patch the initial access vector** before restoring services. If the attacker got in via an unpatched VPN, restoring operations without patching guarantees re-compromise.
6. **Engage Legal and Compliance** for breach notification assessment — SEC 8-K (4 business days), CIRCIA (24 hours for payment), state AG notification, client notification obligations.

---

## Evidence Preservation Checklist

Preserve the following for forensic analysis and potential legal proceedings:

- [ ] Memory images from compromised hosts (before reboot/rebuild)
- [ ] Rclone configuration files (may contain attacker cloud storage credentials)
- [ ] Ransom notes
- [ ] VPN/firewall appliance logs covering the intrusion period
- [ ] Windows Event Logs (Security, System, PowerShell) from all systems in the blast radius
- [ ] Sysmon logs if deployed
- [ ] EDR telemetry/timeline exports
- [ ] Network flow logs and proxy logs for the exfiltration window
- [ ] Email gateway logs if phishing was the initial vector
- [ ] Copies of malicious binaries, scripts, and tools left by the attacker

---

*Source: RB-2026-003 | Contact: [Analyst Name], CTI — [contact info]*
