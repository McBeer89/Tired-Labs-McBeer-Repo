# Phase 1 Scoping: IIS Components — Malicious IIS Modules and ISAPI Backdoors (T1505.004)

**Scope Status:** CONFIRMED — 2026-03-02

## Scope Statement

Persistent and in-memory IIS module and ISAPI backdoors on Windows — covering native module registration via `applicationHost.config`, managed module registration via `web.config`, and reflective in-memory assembly loading into `w3wp.exe` — where the malicious component integrates into the IIS HTTP request pipeline to intercept server-wide traffic rather than responding to requests at a specific URL.

## Scope Confirmation Notes

- Scope statement is specific and defensible — clearly distinguishes T1505.004 (pipeline module, server-wide interception) from T1505.003 (handler/script, URL-specific response).
- All major exclusions captured with correct rationale. SUPERNOVA boundary case is explicitly documented and excluded (T1505.003 per ATT&CK S0578 / CISA AR21-112A).
- 7 of 7 original open questions resolved or partially resolved. Two new lab-verification questions (Q8, Q9) identified — neither blocks DDM construction; both can be confirmed during Phase 3 procedure lab work.
- Three procedure paths confirmed: Path A (native module), Path B (managed module), Path C (reflective in-memory). ISAPI variant maps to Path A essential operations.
- IceApple reclassified as hybrid (Path A/B base + Path C capabilities). NodeIISWeb/Praying Mantis confirmed as pure Path C (volatile, re-exploitation model).
- ETW event ID corrected: EID 154 (`AssemblyLoad_V1`) is the real-time load event, not EID 155.
- Ready for Phase 2 DDM construction.

## Exclusion Table

| Excluded Item | Rationale |
|---|---|
| File-based web shells (.aspx, .asp, .ashx, .php) in web root (T1505.003) | Different essential operations — persistence is a script file at a web-accessible URL executed via handler mapping, not a DLL registered in IIS configuration. Covered by TRR0000. |
| SQL Stored Procedures (T1505.001) | Different essential operations — database engine execution, not HTTP pipeline. Warrants separate TRR. |
| Transport Agent (T1505.002) | Different essential operations — Exchange mail transport pipeline, not IIS HTTP pipeline. Warrants separate TRR. |
| Terminal Services DLL (T1505.005) | Different essential operations — RDP service context, not IIS. Warrants separate TRR. |
| vSphere Installation Bundles (T1505.006) | Different essential operations — VMware ESXi boot mechanism. Warrants separate TRR. |
| PHP web shells on Linux (Apache/Nginx) | Different essential operations — different process lineage (`httpd`/`php-fpm` parent), different telemetry (auditd), different platform. Warrants separate TRR. |
| JSP web shells on Tomcat | Different essential operations — JVM process context, Jasper compilation model. Warrants separate TRR. |
| Web shells on network appliances (Ivanti, FortiGate) | Different essential operations — hardened filesystem, appliance-specific persistence. Warrants separate TRR. |
| Delivery mechanism (T1190 Exploit Public-Facing Application, T1078 Valid Accounts) | Tangential — attacker-controlled prerequisite. How the DLL reaches the server is variable; the IIS component registration is the essential operation. |
| Post-exploitation commands executed through the module | Tangential — separate techniques (T1059, T1033, T1087, etc.) using the module as a channel. |
| Specific DLL file names, module names, registration tool (appcmd vs. PowerShell vs. direct edit) | Tangential — attacker-controlled. All registration methods converge on the same configuration file write. |
| C2 trigger mechanism (Cookie, header, URL parameter, POST body) | Tangential — attacker-controlled. The delivery field varies per malware family. |
| C2 encryption/encoding (AES, XOR, base64, dynamic compile) | Tangential — attacker-controlled. Does not change the essential pipeline interception operation. |
| Anti-log tampering via `OnLogRequest` hook | Tangential — optional evasion layer present in only some families (IISpy). Not essential to the technique. |
| IIS HTTP handlers (`IHttpHandler` in `<handlers>`) registered via DLL | Boundary case — handlers respond only to URL-matched requests (like T1505.003), not server-wide interception. Closer to T1505.003 execution model despite DLL implementation. SUPERNOVA is the notable example; it implements `IHttpHandler`, not `IHttpModule`. Excluded from this TRR's DDM but documented in Technical Background as a boundary case. |
| ASP.NET Core on IIS (Kestrel reverse proxy model) | Different architecture — IIS acts as proxy, not execution engine. Out of platform scope. |

## Essential Constraints Table

| # | Constraint | Essential? | Immutable? | Observable? | Telemetry |
|---|-----------|------------|------------|-------------|-----------|
| 1 | Malicious DLL must be written to the IIS server filesystem (Paths A/B) | ✅ | ✅ | ✅ | Sysmon 11 (FileCreate) |
| 2 | IIS configuration file must be modified to register the component — `applicationHost.config` for native modules/ISAPI, `web.config` for managed modules (Paths A/B) | ✅ | ✅ | ✅ | Sysmon 11 (FileCreate on config file overwrite); Microsoft-IIS-Configuration/Operational EID 29 (module add/remove, API-mediated changes only — requires manual enablement). **Note:** Direct file edits to `applicationHost.config` or `web.config` bypass the IIS configuration API and do NOT trigger EID 29 or EID 50. Sysmon 11 is the only reliable telemetry for direct-edit paths. |
| 3 | Module DLL must be loaded into `w3wp.exe` worker process — via `LoadLibrary` (native) or CLR assembly loader from disk (managed) | ✅ | ✅ | ✅ | Sysmon 7 (ImageLoad) — fires for both native DLLs (`LoadLibrary` → `NtMapViewOfSection`) and disk-backed .NET assemblies (CLR maps PE via same kernel path). Does NOT fire for reflective in-memory loads via `Assembly.Load(byte[])` (see Constraint #6). |
| 4 | Module must register HTTP pipeline event hooks — `RegisterModule` + `SetRequestNotifications` (native) or `IHttpModule.Init()` (managed) | ✅ | ✅ | ❌ | No direct telemetry; inferred from DLL load (Constraint #3) |
| 5 | HTTP request must be received and processed by the module within `w3wp.exe` | ✅ | ✅ | ✅ | IIS W3C access logs (partial — module can tamper); network capture |
| 6 | Reflective assembly loading into `w3wp.exe` memory — no DLL on disk, no config modification (Path C only) | ✅ | ✅ | ✅ | ETW Microsoft-Windows-DotNETRuntime EID 154 (`AssemblyLoad_V1`, runtime provider, `LoaderKeyword 0x8`) — fires in real-time when any assembly is loaded including in-memory. Requires active ETW consumer session. Not enabled by default. Sysmon 7 does NOT fire for `Assembly.Load(byte[])`. Note: ETW events are userland-sourced and can be suppressed by attacker patching `ntdll!EtwEventWrite` (T1562.006). |
| 7 | Pre-existing code execution within `w3wp.exe` as prerequisite for reflective loading (Path C only) | ✅ | ✅ | ✅ | IIS access logs (exploit request); EDR behavioral telemetry |

## Procedure Paths Identified

Three execution paths differ at the essential operation level — specifically in the installation/registration mechanism and persistence profile:

### Path A — Persistent Native Module (C++ DLL + applicationHost.config)

A C++ DLL exporting `RegisterModule` is written to disk and registered in `applicationHost.config` under `<globalModules>` and `<modules>`. Requires administrator access. IIS loads the DLL into every subsequent `w3wp.exe` process at worker startup. The module registers `CHttpModule` or `CGlobalModule` event handlers covering all HTTP requests. Survives reboots and worker process recycles.

**Essential operations:** DLL write to disk (Constraint #1) → `applicationHost.config` modification (Constraint #2) → `w3wp.exe` start → DLL load via `LoadLibrary` (Constraint #3) → `RegisterModule` called (Constraint #4) → HTTP request intercepted (Constraint #5)

**Known implementations:** RGDoor (OilRig/APT34), IISpy (unknown actor), SessionManager (possibly GELSEMIUM), IIS-Raid (MDSec red team tool), Larva-25003 (Chinese-speaking APT, 2025)

### Path B — Persistent Managed Module (.NET IHttpModule + web.config)

A .NET assembly implementing `IHttpModule` is placed in the application's `/bin` directory (or GAC) and registered in `web.config` under `<system.webServer><modules>`. Does NOT require administrator access when the `<modules>` configuration section is unlocked (default when ASP.NET is installed). The CLR within `w3wp.exe` loads the assembly on first request. Persists across reboots via configuration file.

**Essential operations:** Assembly write to `/bin` (Constraint #1) → `web.config` modification (Constraint #2) → first HTTP request → CLR init in `w3wp.exe` → assembly load (Constraint #3) → `IHttpModule.Init()` registers event handlers (Constraint #4) → subsequent HTTP requests intercepted (Constraint #5)

**Distinguished from Path A by:** managed (.NET) vs. native (C++); potentially no administrator required; `web.config` vs. `applicationHost.config`; CLR assembly loader vs. `LoadLibrary`; loads on first request (not at process start).

**Known implementations:** IceApple base module (registered module that serves as loader for reflective capability modules — hybrid model, see Path C)

### Path C — Reflective In-Memory Loading (No Disk DLL, No Config Entry)

A pre-existing foothold within `w3wp.exe` (web application exploitation, deserialization RCE) is used to reflectively load a malicious .NET assembly into process memory via `Assembly.Load(byte[])`. No DLL written to disk. No `applicationHost.config` or `web.config` modification. The assembly hooks the IIS HTTP pipeline from memory. **Not persistent** — lost when `w3wp.exe` terminates or recycles.

**Essential operations:** Web application exploitation (Constraint #7) → reflective assembly load into `w3wp.exe` memory (Constraint #6) → HTTP pipeline hooks registered in-memory (Constraint #4) → HTTP request intercepted (Constraint #5)

**Distinguished from Paths A/B by:** no file write to disk; no configuration file modification; detected only through ETW assembly load events (EID 154) and behavioral analysis; volatile (non-persistent).

**Known implementations:** IceApple capability modules (China-nexus — the 18+ reflective modules loaded by the registered base module; the base itself is Path A/B), NodeIISWeb/Praying Mantis (TG1021/Sygnia — genuinely volatile; TG1021 maintained access by stealing ASP.NET machine keys and re-exploiting VIEWSTATE deserialization to re-inject after worker process recycles)

### ISAPI Filter/Extension Variant (Legacy — Maps to Path A)

ISAPI filters (`GetFilterVersion`/`HttpFilterProc`) and extensions (`GetExtensionVersion`/`HttpExtensionProc`) are the IIS 4–6 predecessors to native modules. They are still supported in IIS 7+ via `IsapiModule` and `IsapiFilterModule`. The essential operations are identical to Path A: DLL write → config registration → DLL load into `w3wp.exe` → request interception. The registration target differs (`<isapiFilters>` section instead of `<globalModules>`), but the telemetry profile is the same. OwaAuth (TG-3390) used this model.

This variant does not warrant a separate procedure path in the DDM — the essential operations converge with Path A. The ISAPI-specific API is a tangential implementation detail.

## Technical Background Notes

### IIS Request Pipeline Architecture

IIS 7.0+ uses a unified integrated pipeline replacing the older ISAPI model. All HTTP requests traverse the same pipeline within `w3wp.exe`:

1. `HTTP.sys` (kernel-mode driver) receives the TCP connection and parses the HTTP request
2. Windows Process Activation Service (WAS) routes the request to the appropriate application pool's `w3wp.exe`
3. Inside `w3wp.exe`, the request passes through an ordered list of native and managed modules at each pipeline stage:
   - `RQ_BEGIN_REQUEST` → `RQ_AUTHENTICATE_REQUEST` → `RQ_AUTHORIZE_REQUEST` → `RQ_RESOLVE_REQUEST_CACHE` → `RQ_MAP_REQUEST_HANDLER` → `RQ_ACQUIRE_REQUEST_STATE` → `RQ_PRE_EXECUTE_REQUEST_HANDLER` → `RQ_EXECUTE_REQUEST_HANDLER` → `RQ_RELEASE_REQUEST_STATE` → `RQ_UPDATE_REQUEST_CACHE` → `RQ_LOG_REQUEST` → `RQ_END_REQUEST`
4. At each stage, every registered module that subscribed to that event is invoked in priority order

A malicious module registered for `RQ_BEGIN_REQUEST` executes on **every request** before any handler mapping, authentication, or logging — giving it first access to all HTTP traffic.

### Module Registration and Loading

**Native modules** require two configuration entries:
- `<globalModules>` in `applicationHost.config`: installs the DLL server-wide (admin-only)
- `<modules>`: enables the module for specific applications

**Managed modules** require only a `<modules>` entry, which can be in application-level `web.config`. The `<modules>` section is **unlocked by default** when ASP.NET is installed, meaning application-level operators can add managed modules without administrator rights.

**All persistent registration paths write to `applicationHost.config` or `web.config`.** No registry-only or in-memory-only persistent registration path has been identified for IIS 7+.

### Process Context and Lineage

All IIS module types execute within `w3wp.exe` under the application pool identity (default: `IIS APPPOOL\{PoolName}`, a low-privilege virtual account). This is the same process that executes file-based web shells.

**Critical difference from T1505.003:** A malicious IIS module can execute commands entirely in-process using .NET APIs — no child process spawn required. When no `cmd.exe` or `powershell.exe` child appears, the process-tree-based detection that catches file-based web shells does not fire. Microsoft DART explicitly notes this: "monitoring for w3wp.exe spawning cmd.exe should not be considered a strong detection method for IIS modules."

### IIS Log Suppression Capability

Modules registered for the `RQ_LOG_REQUEST` event can modify or suppress HTTP log entries before IIS commits them. IISpy demonstrates this by rewriting the HTTP method to GET, changing the URL to `/`, and stripping Cookie/Referer/Content-Type headers on its own traffic. This is an inherent capability of the IIS module pipeline — any module can subscribe to the logging event. File-based web shells cannot suppress their own log entries.

### Telemetry Enablement Requirements

| Telemetry Source | Default State | Enablement |
|---|---|---|
| Sysmon 11 (FileCreate) | Requires Sysmon installation | Sysmon config with file-create rules |
| Sysmon 7 (ImageLoad) | Requires Sysmon installation | Sysmon config with image-load rules for `w3wp.exe` |
| Microsoft-IIS-Configuration/Operational | **Disabled by default** | `wevtutil sl /e:true Microsoft-IIS-Configuration/Operational` |
| Windows Security EID 4663 | Requires SACL on target file | SACL on `applicationHost.config` + Object Access audit policy |
| Windows Security EID 4688 | Requires audit policy | Process Creation audit policy (Advanced Audit Configuration) |
| ETW Microsoft-Windows-DotNETRuntime EID 154 (`AssemblyLoad_V1`) | Requires ETW consumer | Not collected by default; requires active ETW session subscribing to runtime provider with `LoaderKeyword (0x8)`. EID 155 is the unload/rundown enumeration event, not the load event. |
| IIS W3C Access Logs | Enabled by default | Default fields log URI, method, status — Cookie and POST body not logged |

### Key Malware Families Documented

| Family | Type | Threat Group | C2 Mechanism | Notable Characteristic |
|---|---|---|---|---|
| RGDoor | Native module | OilRig/APT34 | HTTP Cookie field | Secondary backdoor; installed via TwoFace web shell |
| IISpy | Native module | Unknown | MD5(Host+URL) verification; AES-CBC | Anti-forensic log rewriting via `OnLogRequest` |
| SessionManager | Native module | Possibly GELSEMIUM | `SM_SESSION` Cookie; XOR | SOCKS5 proxy capability; post-ProxyLogon |
| IIS-Raid | Native module | MDSec (red team) | `X-Password` header | Credential dumping; open-source |
| Larva-25003 | Native module | Chinese-speaking APT | All requests intercepted | Associated with Gh0st RAT; Feb 2025 |
| IceApple | Hybrid — registered base (Path A/B) + reflective capability modules (Path C) | China-nexus | Reflective .NET assembly loading from base module | 18+ capability modules; base module mimics IIS temp file naming; CrowdStrike detected via proprietary CLR hook |
| SUPERNOVA | Managed (`IHttpHandler`) — **excluded, T1505.003** | Unknown (not SUNBURST) | GET parameters | Implements `IHttpHandler` (URL-specific), not `IHttpModule` (pipeline). Modified existing DLL. Per ATT&CK S0578 / CISA AR21-112A, classified as T1505.003. |
| NodeIISWeb | Managed (in-memory) | TG1021/Praying Mantis | Reflective load via deser exploit | Volatile; memory-only; strong OPSEC |
| OwaAuth | ISAPI filter | TG-3390/APT27 | Z1/Z2 HTTP parameters | Credential capture; masquerades as OWA component |

## Open Questions [?]

### Resolved

1. **~~[?]~~ RESOLVED — Microsoft-IIS-Configuration/Operational EID 29 vs. 50 scope**: Both events exist in the same channel — EID 29 fires on module add/remove, EID 50 fires on site-level configuration changes. Confirmed via Sigma rule `win_iis_module_added` (EID 29, filter `/system.webServer/modules/add`). **Critical finding:** Neither EID 29 nor EID 50 fires on direct file edits — only API-mediated changes (appcmd, PowerShell, IIS Manager) are captured. Direct `applicationHost.config` or `web.config` edits bypass the IIS configuration API entirely. Constraint #2 telemetry annotation updated.

2. **~~[?]~~ RESOLVED — Sysmon 7 (ImageLoad) for managed (.NET) assemblies**: Sysmon 7 hooks via `PsSetLoadImageNotifyRoutine` (kernel callback on `NtMapViewOfSection`). **Fires for disk-backed .NET assemblies** (CLR maps PE via same kernel path as native DLLs). **Does NOT fire for `Assembly.Load(byte[])` reflective in-memory loads** (CLR allocates from heap, no `NtMapViewOfSection` call). Constraint #3 annotation updated. Path B retains Sysmon 7 as a valid observable; Path C does not.

3. **~~[?]~~ PARTIALLY RESOLVED — IceApple initial loading mechanism**: IceApple uses a **hybrid model** — a registered base module (Path A or B, with disk artifact) that then reflectively loads 18+ capability modules into memory (Path C behavior). The base module mimics IIS temporary file naming to blend in. CrowdStrike detected via proprietary EDR CLR hook on `nLoadImage` inside `clr.dll`, not via standard Windows telemetry. **Remaining gap:** The exact registration method of the base module (native vs. managed, applicationHost.config vs. web.config) is not detailed in public CrowdStrike reporting. Lab reconstruction not possible from public sources alone.

4. **~~[?]~~ RESOLVED — Praying Mantis/TG1021 persistence**: NodeIISWeb is confirmed genuinely volatile — lost on `w3wp.exe` termination. TG1021 maintained access not through persistence but through **re-exploitation**: they stole ASP.NET machine keys during initial compromise and used them to craft malicious VIEWSTATE payloads, re-exploiting deserialization vulnerabilities at will to re-inject. This confirms Path C as non-persistent.

5. **~~[?]~~ RESOLVED — SUPERNOVA classification**: SUPERNOVA is T1505.003, not T1505.004. Per ATT&CK S0578 and CISA AR21-112A, SUPERNOVA implements `IHttpHandler` (responds only to specific URL pattern), not `IHttpModule` (server-wide pipeline interception). It modified an existing legitimate DLL rather than registering a new component. **Removed from Path B known implementations.** Retained in Exclusion Table and malware families table as annotated boundary case.

6. **~~[?]~~ RESOLVED — IIS configuration file change detection via Sysmon 11**: Three sub-findings: (a) WAS monitors `applicationHost.config` via file change notification — direct edits cause automatic config reload without iisreset; (b) Sysmon 11 fires on file overwrite, so saving a modified `applicationHost.config` triggers Sysmon 11 (FileCreate); (c) Windows Security EID 4663 requires manual SACL configuration on the file — no default SACL exists on `applicationHost.config`. **Sysmon 11 is the only reliable default-available telemetry for direct config file edits.**

7. **~~[?]~~ PARTIALLY RESOLVED — `<modules>` section lock state**: Default IIS installation with ASP.NET has `<modules>` section set to `overrideMode="Allow"` (unlocked). The CIS Benchmark for IIS does not include a recommendation to lock this section. Path B's non-admin registration capability is available in default configurations. **Remaining gap:** Prevalence of locked configurations in enterprise Exchange/IIS environments is unknown — this is an environmental variable, not a researchable technical question. Noted as DDM scope assumption.

### Remaining Open

8. **[?] EID 29 for `web.config`-level `<modules>` additions via API**: Community sources state EID 29 covers "global and site level" module additions, which would include `web.config` entries added via appcmd or PowerShell. No primary-source lab confirmation exists for this specific path. Lab test needed: register a managed module via `appcmd` targeting `web.config` and observe whether EID 29 or EID 50 fires.

9. **[?] MDE ETW collection of EID 154**: Whether Microsoft Defender for Endpoint subscribes to the `Microsoft-Windows-DotNETRuntime` provider with `LoaderKeyword` and surfaces EID 154 assembly load events in its telemetry tables is not confirmed from public sources.

## Atomic Red Team Test Mapping

| Path | ART Tests | Notes |
|---|---|---|
| **Path A** (native module) | 2 tests — `53adbdfa` (AppCmd), `cc3381fb` (PowerShell New-WebGlobalModule) | Both use benign existing DLL (`defdoc.dll`). Cover only the registration operation. Do not test functional backdoor behavior, HTTP interception, or command execution. |
| **Path B** (managed module) | None | No ART test covers managed module registration via `web.config` or `/bin` deployment. Intelligence gap. |
| **Path C** (reflective in-memory) | None | No ART test covers reflective assembly loading into `w3wp.exe`. Intelligence gap. |
| **ISAPI filter** | None | No ART test covers ISAPI filter registration. Intelligence gap. |

ART coverage is minimal — the two existing tests are variants of one essential operation (config file write) via two tangential installation tools. No execution-phase testing exists.

## Sources

### MITRE ATT&CK
- [T1505.004 — Server Software Component: IIS Components](https://attack.mitre.org/techniques/T1505/004/)
- [T1505.003 — Server Software Component: Web Shell](https://attack.mitre.org/techniques/T1505/003/)
- [T1505 — Server Software Component (parent)](https://attack.mitre.org/techniques/T1505/)

### Atomic Red Team
- [T1505.004 Atomic Tests](https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1505.004/T1505.004.md)

### Microsoft Documentation
- [IIS Modules Overview](https://learn.microsoft.com/en-us/iis/get-started/introduction-to-iis/iis-modules-overview)
- [Developing a Module Using .NET](https://learn.microsoft.com/en-us/iis/develop/runtime-extensibility/developing-a-module-using-net)
- [Develop a Native C/C++ Module for IIS 7.0](https://learn.microsoft.com/en-us/iis/develop/runtime-extensibility/develop-a-native-cc-module-for-iis)
- [Designing Native-Code HTTP Modules](https://learn.microsoft.com/en-us/iis/web-development-reference/native-code-development-overview/designing-native-code-http-modules)
- [Global Modules `<globalModules>` Configuration](https://learn.microsoft.com/en-us/iis/configuration/system.webserver/globalmodules/)
- [Modules `<modules>` Configuration](https://learn.microsoft.com/en-us/iis/configuration/system.webserver/modules/)
- [ISAPI Filters `<isapiFilters>` Configuration](https://learn.microsoft.com/en-us/iis/configuration/system.webserver/isapifilters/)
- [Introduction to applicationHost.config](https://learn.microsoft.com/en-us/iis/get-started/planning-your-iis-architecture/introduction-to-applicationhostconfig)
- [How to Use Locking in IIS 7.0 Configuration](https://learn.microsoft.com/en-us/iis/get-started/planning-for-security/how-to-use-locking-in-iis-configuration)
- [ASP.NET Application Life Cycle Overview for IIS 7.0](https://learn.microsoft.com/en-us/previous-versions/aspnet/bb470252(v=vs.100))
- [CHttpModule Class](https://learn.microsoft.com/en-us/iis/web-development-reference/native-code-api-reference/chttpmodule-class)
- [CGlobalModule Class](https://learn.microsoft.com/en-us/iis/web-development-reference/native-code-api-reference/cglobalmodule-class)

### Microsoft Security Blog
- [IIS modules: The evolution of web shells and how to detect them (December 2022)](https://www.microsoft.com/en-us/security/blog/2022/12/12/iis-modules-the-evolution-of-web-shells-and-how-to-detect-them/)
- [Malicious IIS extensions quietly open persistent backdoors into servers (July 2022)](https://www.microsoft.com/en-us/security/blog/2022/07/26/malicious-iis-extensions-quietly-open-persistent-backdoors-into-servers/)

### Threat Intelligence
- [Unit 42: OilRig uses RGDoor IIS Backdoor on Targets in the Middle East](https://unit42.paloaltonetworks.com/unit42-oilrig-uses-rgdoor-iis-backdoor-targets-middle-east/)
- [Kaspersky Securelist: The SessionManager IIS backdoor](https://securelist.com/the-sessionmanager-iis-backdoor/106868/)
- [Secureworks: Threat Group-3390 Targets Organizations for Cyberespionage (OwaAuth)](https://www.secureworks.com/research/threat-group-3390-targets-organizations-for-cyberespionage)
- [CrowdStrike: Falcon OverWatch Detects Novel IceApple Framework](https://www.crowdstrike.com/en-us/blog/falcon-overwatch-detects-iceapple-framework/)
- [CrowdStrike: IceApple White Paper (PDF)](https://www.crowdstrike.com/wp-content/uploads/2022/05/crowdstrike-iceapple-a-novel-internet-information-services-post-exploitation-framework-1.pdf)
- [Unit 42: SUPERNOVA .NET Webshell Analysis](https://unit42.paloaltonetworks.com/solarstorm-supernova/)
- [MDSec: IIS-Raid — Backdooring IIS Using Native Modules](https://www.mdsec.co.uk/2020/02/iis-raid-backdooring-iis-using-native-modules/)
- [Sygnia: Praying Mantis (TG1021)](https://www.sygnia.co/praying-mantis-detecting-and-hunting)
- [AhnLab ASEC: Distribution of IIS Malware — Larva-25003 (February 2025)](https://asec.ahnlab.com/en/87804/)
- [ESET: Anatomy of native IIS malware (August 2021)](https://www.welivesecurity.com/2021/08/06/anatomy-native-iis-malware/)
- [ESET: IISpy anti-forensic IIS backdoor (August 2021)](https://www.welivesecurity.com/2021/08/09/iispy-complex-server-side-backdoor-antiforensic-features/)
- [ESET: Anatomy of Native IIS Malware — Black Hat USA 2021 White Paper](https://i.blackhat.com/USA21/Wednesday-Handouts/us-21-Anatomy-Of-Native-Iis-Malware-wp.pdf)

### Detection Rules
- [Sigma: win_iis_module_added — SigmaHQ](https://detection.fyi/sigmahq/sigma/windows/builtin/iis-configuration/win_iis_module_added/)
- [Splunk: Windows IIS Components New Module Added](https://research.splunk.com/endpoint/55f22929-cfd3-4388-ba5c-4d01fac7ee7e/)
- [Splunk: Windows IIS Components Add New Module (process-based)](https://research.splunk.com/endpoint/38fe731c-1f13-43d4-b878-a5bbe44807e3/)
- [Splunk: Windows PowerShell IIS Components WebGlobalModule Usage](https://research.splunk.com/endpoint/33fc9f6f-0ce7-4696-924e-a69ec61a3d57/)
- [Splunk: Fantastic IIS Modules and How to Find Them (blog + SPL)](https://www.splunk.com/en_us/blog/security/fantastic-iis-modules-and-how-to-find-them.html)
- [Splunk: IIS Components Analytics Story](https://research.splunk.com/stories/iis_components/)
- [WA Cyber Security Unit: T1505.004 Suspicious IIS Module Registration](https://soc.cyber.wa.gov.au/guidelines/TTP_Hunt/ADS_forms/T1505.004-Suspicious-IIS-Module-Registration/)
- [GitHub: IIS-Raid (0x09AL)](https://github.com/0x09AL/IIS-Raid)

### Telemetry Research (Phase 1 Resolution)
- [IIS Support Blog: IIS 7.5 — How to enable IIS Configuration Auditing](https://blogs.iis.net/webtopics/iis-7-5-how-to-enable-iis-configuration-auditing/)
- [Microsoft TechCommunity: IIS 7.5 Configuration Auditing](https://techcommunity.microsoft.com/t5/iis-support-blog/iis-7-5-how-to-enable-iis-configuration-auditing/ba-p/347239)
- [Microsoft Learn: Loader ETW Events — .NET Framework](https://learn.microsoft.com/en-us/dotnet/framework/performance/loader-etw-events)
- [Microsoft Learn: CLR ETW Providers — .NET Framework](https://learn.microsoft.com/en-us/dotnet/framework/performance/clr-etw-providers)
- [MDSec: Bypassing Image Load Kernel Callbacks](https://www.mdsec.co.uk/2021/06/bypassing-image-load-kernel-callbacks/)
- [GitHub: CLR-Unhook (hwbp)](https://github.com/hwbp/CLR-Unhook)
- [XPN InfoSec: Hiding your .NET - ETW](https://blog.xpnsec.com/hiding-your-dotnet-etw/)
- [TrustedSec SysmonCommunityGuide: image-loading.md](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/image-loading.md)
- [TrustedSec SysmonCommunityGuide: file-create.md](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/file-create.md)
- [Microsoft Learn: Event 4663 — Object Access](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4663)
- [CISA: AR21-112A — SUPERNOVA Malware Analysis](https://www.cisa.gov/news-events/analysis-reports/ar21-112a)
