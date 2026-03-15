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
