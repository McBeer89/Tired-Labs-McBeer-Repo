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
