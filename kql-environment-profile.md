# KQL Environment Profile

This file describes your environment's log sources, schema mappings, and known
baselines. The `kql-builder` agent reads this before generating queries and
adapts its output to match your actual environment.

**Location:** Repo root (`kql-environment-profile.md`). One per repository —
not per TRR.

**How to use:** Fill in the sections that apply to your environment. Leave
sections empty or remove them if they don't apply. The kql-builder will note
in query comments when a DDM operation can't be covered because the required
telemetry isn't declared here.

---

## 1. SIEM Platform

<!-- Which SIEM/query platform are you targeting? The kql-builder uses this to
     choose the correct base tables and syntax conventions. -->

| Setting | Value |
|---|---|
| Platform | <!-- Microsoft Sentinel / Microsoft Defender for Endpoint / Both / Other --> |
| Workspace | <!-- Log Analytics workspace name, if relevant --> |
| Default Lookback | <!-- e.g., 24h, 7d — used in `ago()` clauses --> |

---

## 2. Available Log Sources

<!-- Declare which telemetry sources are available in your environment.
     The kql-builder maps DDM telemetry labels to these entries.

     For each source: what's the actual table name, is it reliably ingested,
     and any notes about coverage gaps or configuration.

     If a source isn't listed here, the kql-builder will flag it as
     unavailable and skip queries that depend on it. -->

### Endpoint Telemetry

| DDM Telemetry Label | Available? | Table Name | Notes |
|---|---|---|---|
| Sysmon 1 (ProcessCreate) | <!-- Yes/No --> | <!-- e.g., SysmonEvent, Event --> | <!-- e.g., "Deployed to servers only" --> |
| Sysmon 3 (NetworkConnect) | | | |
| Sysmon 7 (ImageLoaded) | | | |
| Sysmon 8 (CreateRemoteThread) | | | |
| Sysmon 10 (ProcessAccess) | | | |
| Sysmon 11 (FileCreate) | | | |
| Sysmon 12/13/14 (Registry) | | | |
| Sysmon 17/18 (PipeEvent) | | | |
| Sysmon 19/20/21 (WMI) | | | |
| Sysmon 22 (DNSQuery) | | | |
| Sysmon 23 (FileDelete) | | | |
| Win 4624 (Logon) | | | |
| Win 4625 (FailedLogon) | | | |
| Win 4648 (ExplicitLogon) | | | |
| Win 4663 (SACL) | | | |
| Win 4688 (ProcessCreate) | | | |
| Win 4689 (ProcessExit) | | | |
| Win 4657 (RegistryValue) | | | |
| Win 4768 (TGT Request) | | | |
| Win 4769 (Service Ticket) | | | |
| Win 4771 (Kerberos PreAuth) | | | |

### Application / Infrastructure Telemetry

| DDM Telemetry Label | Available? | Table Name | Notes |
|---|---|---|---|
| IIS W3C | | | |
| DNS Debug Log | | | |
| DHCP Log | | | |
| <!-- Add rows as needed --> | | | |

### EDR / Vendor-Specific Telemetry

<!-- If you use Defender for Endpoint, CrowdStrike, or another EDR, map its
     tables here. The kql-builder will use these instead of or alongside
     the generic Sysmon/Windows event mappings. -->

| DDM Telemetry Label | Available? | Table Name | Notes |
|---|---|---|---|
| MDE ProcessCreate | <!-- Yes/No --> | <!-- DeviceProcessEvents --> | |
| MDE FileCreate | | <!-- DeviceFileEvents --> | |
| MDE RegistryEvent | | <!-- DeviceRegistryEvents --> | |
| MDE ImageLoad | | <!-- DeviceImageLoadEvents --> | |
| MDE NetworkConnect | | <!-- DeviceNetworkEvents --> | |
| MDE LogonEvent | | <!-- DeviceLogonEvents --> | |
| CS ProcessRollup2 | | | |
| CS / CrowdStrike (other) | | | |
| <!-- Add rows as needed --> | | | |

### Custom / ETW Sources

<!-- ETW providers, custom log ingestion, or any non-standard sources. -->

| Source Name | Table Name | What It Captures | Notes |
|---|---|---|---|
| <!-- e.g., IIS Config ETW EID 29 --> | | | |
| <!-- e.g., .NET CLR ETW --> | | | |

---

## 3. Field Name Mappings

<!-- Different ingestion pipelines rename fields. Declare your actual field
     names here so the kql-builder uses the right column references.

     Only fill in fields that differ from the defaults. If your environment
     uses the standard Sentinel or Defender schema, you can skip this section.

     The "Default Name" column shows what the kql-builder assumes if no
     override is provided. -->

### Process Events

| Concept | Default Name | Your Field Name |
|---|---|---|
| Process name | `NewProcessName` / `FileName` | <!-- e.g., Process_Name --> |
| Parent process name | `ParentProcessName` / `InitiatingProcessFileName` | |
| Command line | `CommandLine` / `ProcessCommandLine` | |
| Process ID | `NewProcessId` / `ProcessId` | |
| Parent process ID | `ProcessId` / `InitiatingProcessId` | |
| User / Account | `SubjectUserName` / `AccountName` | |
| Timestamp | `TimeGenerated` | |

### File Events

| Concept | Default Name | Your Field Name |
|---|---|---|
| File path | `TargetFilename` / `FolderPath` | |
| File name | `TargetFilename` / `FileName` | |
| Action type | `ActionType` | |

### Registry Events

| Concept | Default Name | Your Field Name |
|---|---|---|
| Registry key | `TargetObject` / `RegistryKey` | |
| Registry value name | `Details` / `RegistryValueName` | |
| Registry value data | `Details` / `RegistryValueData` | |

### Network Events

| Concept | Default Name | Your Field Name |
|---|---|---|
| Destination IP | `DestinationIp` / `RemoteIP` | |
| Destination port | `DestinationPort` / `RemotePort` | |
| Source IP | `SourceIp` / `LocalIP` | |

### Authentication Events

| Concept | Default Name | Your Field Name |
|---|---|---|
| Target account | `TargetUserName` / `AccountName` | |
| Source host | `WorkstationName` / `DeviceName` | |
| Logon type | `LogonType` | |
| Service name | `ServiceName` | |

---

## 4. Known Baselines

<!-- This is the hard part. Environmental noise — legitimate activity that
     produces the same telemetry as an attack — is unique to every environment.

     The kql-builder uses entries here to add exclusion clauses (`where not`)
     to queries. Without these, queries will fire on legitimate activity.

     Organize by operation type. Each entry should describe:
     - What the legitimate pattern looks like
     - Why it's legitimate (briefly)
     - How confident you are it's safe to exclude

     You don't need to fill this out exhaustively. Start with the patterns
     that generate the most noise and add more over time as you tune queries.
     The kql-builder will produce functional queries without any baselines —
     they'll just be noisier. -->

### Process Creation Baselines

<!-- Known-legitimate parent → child process relationships that should be
     excluded from process-spawn queries. -->

<!--
| Parent Process | Child Process | Context | Confidence |
|---|---|---|---|
| e.g., w3wp.exe | e.g., csc.exe | ASP.NET runtime compilation | High |
| e.g., svchost.exe | e.g., taskhostw.exe | Scheduled task execution | High |
-->

### Registry Modification Baselines

<!-- Known-legitimate registry writes that match DDM operations. -->

<!--
| Process | Registry Path Pattern | Context | Confidence |
|---|---|---|---|
| e.g., msiexec.exe | HKLM\SOFTWARE\Microsoft\... | Software installation | High |
-->

### File System Baselines

<!-- Known-legitimate file creation/modification in monitored paths. -->

<!--
| Process | Path Pattern | Context | Confidence |
|---|---|---|---|
| e.g., w3wp.exe | C:\inetpub\wwwroot\*.dll | IIS temp compilation | Medium |
-->

### Authentication Baselines

<!-- Known service accounts, scheduled logons, or patterns that generate
     legitimate Kerberos/NTLM events matching DDM operations. -->

<!--
| Account Pattern | Event Type | Context | Confidence |
|---|---|---|---|
| e.g., svc_backup$ | 4769 (Service Ticket) | Nightly backup job | High |
-->

### WMI Baselines

<!-- Known-legitimate WMI event subscriptions or WMI method calls. -->

<!--
| Filter/Consumer Name | Purpose | Confidence |
|---|---|---|
| e.g., BVTFilter | SCCM client health check | High |
-->

### Network Baselines

<!-- Known-legitimate network connections that match DDM operations. -->

<!--
| Process | Destination Pattern | Context | Confidence |
|---|---|---|---|
-->

---

## 5. Environment Notes

<!-- Anything else the kql-builder should know about your environment that
     affects query generation. Free-form. Examples:

     - "We run IIS on ports 8080 and 8443, not 80/443"
     - "Sysmon config excludes common noisy paths — see sysmon-config.xml"
     - "Domain controllers are in the 'DC' device group in MDE"
     - "We use Azure AD joined devices, no on-prem AD"
     - "Log retention is 90 days in Sentinel, 30 days in MDE"
-->

