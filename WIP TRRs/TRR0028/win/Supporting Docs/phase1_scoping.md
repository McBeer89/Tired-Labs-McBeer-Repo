# Phase 1 Scoping: PowerShell Command and Script Execution (T1059.001)

## Scope Statement

PowerShell command and script execution on Windows via the System.Management.Automation runtime — covering standard host binary invocation, hosted runspace execution without powershell.exe, and PowerShell v2 engine downgrade.

## Exclusion Table

| Excluded Item | Rationale |
|---|---|
| PowerShell Remoting via WinRM (T1021.006) | Different essential operations — adds WS-Management network protocol, WinRM service processing, `wsmprovhost.exe` host context, and Type 3 remote logon event not present in local execution. Warrants separate TRR. |
| PowerShell Profile persistence (T1546.013) | Different essential operations — the technique is event-triggered persistence (file write to profile path + auto-execution on session start), not execution itself. Warrants separate TRR. |
| Command obfuscation / encoding (T1027.010) | Tangential — attacker-controlled. Base64 encoding, string manipulation, `Invoke-Obfuscation` output are all variable. The PowerShell engine decodes before execution; EID 4104 captures the decoded content. The encoding does not change the essential runtime operations. |
| Specific payloads executed via PowerShell | Tangential — attacker-controlled. Invoke-Mimikatz, BloodHound, etc. are subsequent techniques (T1003, T1087, etc.) that happen to use PowerShell as a delivery vehicle. |
| Download cradle method (Net.WebClient, MsXml2, IWR, etc.) | Tangential — attacker-controlled delivery mechanism. The network retrieval method varies; the PowerShell runtime operations after retrieval are identical. File-writing cradles belong under T1105 (Ingress Tool Transfer). |
| Command-line flags (-EncodedCommand, -NoProfile, -WindowStyle Hidden, etc.) | Tangential — attacker-controlled invocation parameters. Do not change the essential runtime operations. |
| Specific cmdlets or script content | Tangential — attacker-controlled. The script content is variable; the engine's parsing/compilation/execution pipeline is fixed. |
| AMSI bypass techniques | Different essential operations — these are evasion operations (T1562.001) layered on top of execution. AMSI itself is a security control, not an attacker operation. |
| PowerShell on Linux/macOS (pwsh cross-platform) | Out of platform scope — ATT&CK lists T1059.001 as Windows only. Cross-platform pwsh abuse would require a separate platform TRR. |
| Execution policy bypass methods | Tangential — execution policies are explicitly not a security boundary per Microsoft documentation. Bypass methods are attacker-controlled and do not change essential runtime operations. |

## Essential Constraints Table

| # | Constraint | Essential? | Immutable? | Observable? | Telemetry |
|---|-----------|------------|------------|-------------|-----------|
| 1 | `System.Management.Automation.dll` must load into the host process | ✅ | ✅ | ✅ | Sysmon 7 (ImageLoad) |
| 2 | .NET CLR must initialize in the host process (`clr.dll` for CLR v4, `coreclr.dll` for .NET Core, `mscorwks.dll` for CLR v2) | ✅ | ✅ | ✅ | Sysmon 7 (ImageLoad) |
| 3 | PowerShell engine must parse and compile script blocks into .NET IL | ✅ | ✅ | ✅ | EID 4104 (Script Block Logging) — captures decoded content post-deobfuscation |
| 4 | A Runspace must be created and initialized within the CLR | ✅ | ✅ | ✅ | EID 400 (EngineStart), ETW provider events |
| 5 | Process creation occurs when invoked via powershell.exe or pwsh.exe (Path A only) | ✅ | ✅ | ✅ | Sysmon 1 (ProcessCreate), Windows Security EID 4688 |
| 6 | CLR v2 (`mscorwks.dll`) loads instead of CLR v4 (`clr.dll`) when v2 engine is forced (Path C only) | ✅ | ✅ | ✅ | Sysmon 7 (ImageLoad) — distinguishes downgrade from standard execution |

## Procedure Paths Identified

Three distinct execution paths differ at the essential operation level:

### Path A — Standard Host Binary Execution
A known PowerShell host binary (`powershell.exe` or `pwsh.exe`) creates a process, loads `System.Management.Automation.dll`, and executes script blocks. This single path covers all command-line variations (`-Command`, `-File`, `-EncodedCommand`), all download cradle variants, fileless/in-memory execution, registry-sourced scripts, and NTFS ADS-sourced scripts — because the essential runtime operations are identical across all of these. The delivery mechanism and encoding are tangential.

**Essential operations**: Process creation (Constraint #5) → CLR init (Constraint #2) → SMA load (Constraint #1) → Runspace creation (Constraint #4) → Script block parse/compile (Constraint #3)

### Path B — Hosted Runspace (No powershell.exe)
A non-PowerShell process loads `System.Management.Automation.dll` via the .NET hosting API and executes PowerShell through `PowerShell.Create()` and `Runspace` objects. No `powershell.exe` or `pwsh.exe` process appears. The host binary is attacker-controlled and tangential — the SMA DLL load into an unexpected process is the distinguishing observable.

**Essential operations**: CLR init (Constraint #2) → SMA load into non-standard host (Constraint #1) → Runspace creation (Constraint #4) → Script block parse/compile (Constraint #3)

**Note**: Process creation still occurs for the host binary, but the host binary identity is attacker-controlled (tangential). The essential observable is SMA loading into a process that is not a known PowerShell host.

### Path C — PowerShell v2 Engine Downgrade
PowerShell is launched with `-Version 2`, forcing the v2 engine which loads CLR v2 (`mscorwks.dll`) instead of CLR v4 (`clr.dll`). This eliminates Script Block Logging (EID 4104), Module Logging (EID 4103), and AMSI — all of which require PowerShell 5.0+. The CLR version loaded is the distinguishing essential observable.

**Essential operations**: Process creation (Constraint #5) → CLR v2 init with `mscorwks.dll` (Constraint #6) → SMA v2 load (Constraint #1) → Runspace creation (Constraint #4) → Script block execution (Constraint #3, but no EID 4104)

**Prerequisite**: .NET Framework 2.0/3.5 optional feature must be installed. Removed from Windows 11 and Server 2025 shipping images.

## Technical Background Notes

### PowerShell Architecture
PowerShell is built on the .NET runtime. The core assembly `System.Management.Automation.dll` (SMA) contains the entire engine: parser, compiler, pipeline model, Extended Type System, cmdlet infrastructure, and provider model. Every PowerShell execution path — interactive console, ISE, hosted runspace, remoting — ultimately loads SMA and creates a Runspace.

A **Runspace** is the execution sandbox holding loaded modules, variables, providers, and session state. The `InitialSessionState` class controls what is loaded when a Runspace opens. `PowerShell.Create()` is the primary .NET API for instantiating the engine.

### Host Process Model
The console hosts (`powershell.exe` for 5.1, `pwsh.exe` for 7.x) are thin wrappers implementing `PSHost` (abstract I/O interface) that call into SMA. Any .NET application can host SMA identically by referencing the `Microsoft.PowerShell.SDK` NuGet package and implementing `PSHost`.

### Script Execution Pipeline
1. Source text received (from command line, file, or API call)
2. Parser converts source to Abstract Syntax Tree (AST)
3. Compiler transforms AST to .NET Intermediate Language (IL)
4. AMSI scans the decoded content (PowerShell 5.0+, Windows 10+)
5. IL executes within the Runspace
6. Script Block Logging (EID 4104) captures the decoded script block content (PowerShell 5.0+)

Key property: AMSI and SBL operate on the **decoded** content. Base64-encoded commands are decoded before scanning/logging. This makes encoding tangential from a telemetry perspective.

### Logging Infrastructure

| Layer | Event | Channel | Availability |
|---|---|---|---|
| Script Block Logging | EID 4104 | Microsoft-Windows-PowerShell/Operational | PS 5.0+ (requires GPO or registry enablement; auto-fires at Warning level for suspicious strings) |
| Module Logging | EID 4103 | Microsoft-Windows-PowerShell/Operational | PS 3.0+ (requires GPO enablement) |
| Engine Start/Stop | EID 400/403 | Windows PowerShell | PS 2.0+ |
| Transcription | Text file | Configurable path | PS 5.0+ (requires GPO enablement) |
| AMSI | amsi.dll load + scan | In-process | PS 5.0+ on Windows 10+ |

**ETW Provider difference**: Windows PowerShell 5.1 uses provider GUID `{A0C1853B-5C40-4B15-8766-3CF1C58F985A}` logging to `Microsoft-Windows-PowerShell/Operational`. PowerShell 7.x uses `{f90714a8-5509-434a-bf6d-b1624c8a19a2}` logging to `PowerShellCore/Operational`. These are distinct channels — a SIEM subscribed to only one will miss the other.

### Version Delta Summary

| Feature | PS 2.0 | PS 5.1 | PS 7.x |
|---|---|---|---|
| Runtime | .NET Framework 2.0/3.5 | .NET Framework 4.5 | .NET 6/7/8/9/10 |
| Executable | powershell.exe -Version 2 | powershell.exe | pwsh.exe |
| Script Block Logging | ❌ | ✅ | ✅ |
| Module Logging | ❌ | ✅ | ✅ |
| AMSI | ❌ | ✅ | ✅ |
| Constrained Language Mode | ❌ | ✅ | ✅ |
| Removed from OS | Win 11 / Server 2025 | Ships inbox | Side-by-side install |

### Execution Policies Are Not a Security Boundary
Microsoft explicitly states execution policies are not a security system. They can be bypassed via `-ExecutionPolicy Bypass`, stdin piping, direct SMA hosting, `Invoke-Expression`, or environment variable manipulation. They do not appear in the Essential Constraints Table because they fail the immutability test — they are trivially bypassed.

### Language Modes
Constrained Language Mode (CLM) restricts .NET type access when enforced by WDAC or AppLocker. It blocks `Add-Type` for unsigned assemblies and restricts `New-Object` to approved types. CLM is a security control when backed by application control policy — without WDAC/AppLocker, users can start a new FullLanguage session. CLM is relevant context but is not an essential operation of the technique itself.

## Open Questions [?]

1. **[?] EID 4104 in hosted runspaces (Path B)**: Does Script Block Logging fire when `System.Management.Automation.dll` is loaded by a custom host process that does not explicitly initialize the PowerShell ETW provider? Multiple sources indicate it should fire if the OS-level GPO is enabled, but this has not been confirmed against a primary Microsoft source or lab test. This directly affects whether Path B has the same telemetry profile as Path A.

2. **[?] AMSI behavior in custom host processes (Path B)**: Does AMSI activate when SMA is loaded by a process that never calls `AmsiInitialize()`? Security research suggests AMSI may not activate in this scenario, but Microsoft primary documentation has not confirmed. If AMSI does not fire, Path B has a reduced telemetry profile.

3. **[?] PowerShell 7 ETW provider consistency**: The PowerShell 7 ETW provider GUID differs from 5.1. Are the Event ID numbers (4104, 4103, 400, 403) consistent across both providers, or do they differ? This affects telemetry mapping in the DDM.

4. **[?] Automatic suspicious script block logging behavior**: Windows auto-logs EID 4104 at Warning level for "suspicious" strings even without SBL GPO enabled. The exact keyword list that triggers this behavior is not publicly documented by Microsoft. Need to determine if this is reliable enough to include in the DDM telemetry map.

5. **[?] PS v2 availability as prerequisite**: The v2 downgrade path (Path C) requires .NET Framework 2.0/3.5 to be installed. On Windows 11 and Server 2025 this feature is removed. Should Path C be scoped only to older Windows versions, or is the .NET 3.5 optional feature still installable on Win 11?

## Atomic Red Team Test Mapping

22 ART tests exist for T1059.001. Mapped to procedure paths:

| Path | ART Tests | Notes |
|---|---|---|
| **Path A** (standard host) | Tests 1-11, 13-22 | All use powershell.exe. Tests 1,3,6,7,8,9,19 differ only in download cradle method (tangential). Tests 10,11 differ in script storage location (tangential). Tests 13-17 differ in encoding (tangential). All share the same essential operations. |
| **Path B** (hosted runspace) | None | No ART test covers hosted runspace execution without powershell.exe. Intelligence gap — lab reproduction needed. |
| **Path C** (v2 downgrade) | None | No ART test covers `-Version 2` invocation for T1059.001. A Sigma detection rule exists. |
| **Boundary** (remoting) | Test 12 | PSSession/Invoke-Command via WinRM — excluded from this TRR scope per T1021.006. |

## Sources

### ATT&CK
- [T1059.001 — Command and Scripting Interpreter: PowerShell](https://attack.mitre.org/techniques/T1059/001/)
- [T1059 — Command and Scripting Interpreter (parent)](https://attack.mitre.org/techniques/T1059/)
- [T1021.006 — Remote Services: Windows Remote Management](https://attack.mitre.org/techniques/T1021/006/)
- [T1546.013 — Event Triggered Execution: PowerShell Profile](https://attack.mitre.org/techniques/T1546/013/)
- [T1620 — Reflective Code Loading](https://attack.mitre.org/techniques/T1620/)
- [T1106 — Native API](https://attack.mitre.org/techniques/T1106/)
- [T1027.010 — Command Obfuscation](https://attack.mitre.org/techniques/T1027/010/)
- [T1562.010 — Impair Defenses: Downgrade Attack](https://attack.mitre.org/techniques/T1562/010/)
- [DS0009 — Process](https://attack.mitre.org/datasources/DS0009/)
- [DS0011 — Module](https://attack.mitre.org/datasources/DS0011/)
- [DS0012 — Script](https://attack.mitre.org/datasources/DS0012/)

### Atomic Red Team
- [T1059.001 Atomic Tests](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1059.001/T1059.001.md)

### Microsoft Documentation
- [PowerShell Class — System.Management.Automation](https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.powershell?view=powershellsdk-7.4.0)
- [Runspace Class — System.Management.Automation.Runspaces](https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.runspaces.runspace?view=powershellsdk-7.2.0)
- [PSHost Class — System.Management.Automation.Host](https://learn.microsoft.com/en-us/dotnet/api/system.management.automation.host.pshost?view=powershellsdk-7.4.0)
- [about_Execution_Policies](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_execution_policies?view=powershell-7.5)
- [about_Language_Modes](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_language_modes?view=powershell-7.5)
- [about_Logging_Windows (PowerShell 7.5)](https://learn.microsoft.com/en-us/powershell/module/microsoft.powershell.core/about/about_logging_windows?view=powershell-7.5)
- [Antimalware Scan Interface (AMSI)](https://learn.microsoft.com/en-us/windows/win32/amsi/antimalware-scan-interface-portal)
- [Differences between Windows PowerShell 5.1 and PowerShell 7.x](https://learn.microsoft.com/en-us/powershell/scripting/whats-new/differences-from-windows-powershell?view=powershell-7.5)
- [WinRM Security Considerations](https://learn.microsoft.com/en-us/powershell/scripting/security/remoting/winrm-security?view=powershell-7.5)
- [Windows PowerShell Host Quickstart](https://learn.microsoft.com/en-us/powershell/scripting/developer/hosting/windows-powershell-host-quickstart?view=powershell-7.5)

### Security Research
- [Elastic: Suspicious PowerShell Engine ImageLoad Rule](https://www.elastic.co/docs/reference/security/prebuilt-rules/rules/windows/execution_suspicious_powershell_imgload)
- [Sigma: PowerShell Downgrade Attack Detection](https://github.com/SigmaHQ/sigma/blob/master/rules/windows/process_creation/proc_creation_win_powershell_downgrade_attack.yml)
- [Palantir: ADS-004 Unusual PowerShell Host Process](https://github.com/palantir/alerting-detection-strategy-framework/blob/master/ADS-Examples/004-Unusual-Powershell-Host-Process.md)
- [Lee Holmes: Detecting and Preventing PowerShell Downgrade Attacks](https://www.leeholmes.com/detecting-and-preventing-powershell-downgrade-attacks/)
- [NetSPI: 15 Ways to Bypass the PowerShell Execution Policy](https://www.netspi.com/blog/technical-blog/network-pentesting/15-ways-to-bypass-the-powershell-execution-policy/)
- [Red Canary: AMSI Data Source](https://redcanary.com/blog/threat-detection/better-know-a-data-source/amsi/)
- [Splunk: Hunting for Malicious PowerShell using Script Block Logging](https://www.splunk.com/en_us/blog/security/hunting-for-malicious-powershell-using-script-block-logging.html)
- [Palantir: Tampering with Windows Event Tracing](https://blog.palantir.com/tampering-with-windows-event-tracing-background-offense-and-defense-4be7ac62ac63)
