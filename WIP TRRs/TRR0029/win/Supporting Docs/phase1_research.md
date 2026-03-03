# Research Notes: T1505.004 IIS Components — Telemetry Gap Resolution

**Resolves open questions from:** `phase1_scoping.md` items 1, 2, 3, 4, 5, 6, 7
**Date researched:** 2026-03-02

---

## Question 1: Microsoft-IIS-Configuration/Operational — EID 29 vs. EID 50

### Finding: Both exist; they cover different operations

| Event ID | Trigger | Scope |
|---|---|---|
| 29 | Module added or removed from IIS configuration | Global (`applicationHost.config`) and site-level (`web.config`) module sections |
| 50 | Modification made to a website configuration | Site-level configuration changes (web.config / site-level settings) |

**Log channel:** `Microsoft-IIS-Configuration/Operational` — confirmed.

**Enablement command:**
```
wevtutil sl /e:true Microsoft-IIS-Configuration/Operational
```

**Critical constraint — direct file edits are NOT captured:**

The official IIS support blog (blogs.iis.net) states: "Manual changes to the configuration store are not audited. If someone modifies the value of a section in the applicationHost.config directly such as by opening it in Notepad.exe, that won't be recorded in the audit logs."

IIS configuration auditing captures only operations that flow through the IIS configuration API layer (appcmd, PowerShell, IIS Manager). Direct text-editor modifications bypass the API and produce no EID 29 or EID 50.

**Coverage by path:**

- **Path A (appcmd/PowerShell registration):** EID 29 fires. Confirmed by Sigma rule `win_iis_module_added`.
- **Path A (direct `applicationHost.config` file edit):** EID 29 does NOT fire. Only Sysmon 11 applies.
- **Path B (web.config modification via API):** EID 29 likely fires for module section changes; EID 50 fires for general site-level changes. [?] Lab confirmation recommended for web.config `<modules>` specifically.
- **Path B (direct `web.config` file edit):** EID 29 does NOT fire.

**Sigma rule `win_iis_module_added`:** EventID 29, detection filter contains `/system.webServer/modules/add`.

---

## Question 2: Sysmon 7 (ImageLoad) for .NET Managed Assemblies

### Finding: Fires for disk-backed CLR loads; does NOT fire for reflective in-memory loads

Sysmon 7 hooks via `PsSetLoadImageNotifyRoutine`, triggered from `NtMapViewOfSection` (kernel callback).

- **Disk-backed .NET assemblies (Path B):** CLR calls `NtMapViewOfSection` to map the PE file. **Sysmon 7 fires.**
- **Reflective in-memory loads (Path C — `Assembly.Load(byte[])`):** CLR allocates from heap memory, no `NtMapViewOfSection` call. **Sysmon 7 does NOT fire.**

Confirmed by the `CLR-Unhook` project which documents that EDRs hook `nLoadImage` inside `clr.dll` specifically because the OS-level path is not traversed for byte-array loads.

---

## Question 3: IceApple Initial Loading Mechanism

### Finding: Hybrid model — registered base module + reflective capability modules

IceApple is NOT purely Path C. It uses a hybrid approach:
- A registered base module (Path A or B) provides the initial foothold
- The base module then reflectively loads 18+ capability modules (Path C behavior)
- The base module mimics IIS temporary file naming to blend in

This means IceApple has disk artifacts for its base module registration, but its capability modules are memory-only reflective loads.

---

## Question 4: Praying Mantis/TG1021 Persistence

### Finding: Genuinely volatile; re-entry via stolen machine key VIEWSTATE exploitation

NodeIISWeb is confirmed volatile — lost on w3wp.exe termination. TG1021 maintained access by:
- Stealing ASP.NET machine keys during initial exploitation
- Using stolen keys to craft malicious VIEWSTATE payloads
- Re-exploiting deserialization vulnerabilities at will to re-inject

This is not a persistence mechanism but a re-exploitation capability. Path C is correctly classified as non-persistent.

---

## Question 5: SUPERNOVA Classification

### Finding: SUPERNOVA is T1505.003, not T1505.004

SUPERNOVA implements `IHttpHandler` (responds only to specific URL pattern), not `IHttpModule` (server-wide pipeline interception). Per ATT&CK S0578 and CISA AR21-112A, it is classified as T1505.003. It modified an existing legitimate DLL rather than registering a new component.

**Action:** Remove from Path B known implementations. Already documented as excluded boundary case in Exclusion Table.

---

## Question 6: applicationHost.config Direct Edit Detection

### Finding: Sysmon 11 fires on overwrite; IIS auto-reloads; no default SACL

- **IIS auto-reload:** WAS monitors `applicationHost.config` via file change notification. Direct edits cause automatic config reload without iisreset.
- **Sysmon 11:** Fires on file overwrite. Saving modified `applicationHost.config` triggers Sysmon 11.
- **EID 4663:** Requires manual SACL configuration on the file. No default SACL exists.
- **EID 29/50:** Do NOT fire on direct file edits.

Sysmon 11 is the only reliable default-available telemetry for direct config file edits.

---

## Question 7: `<modules>` Section Lock State

### Finding: Default unlocked; CIS Benchmark does not recommend locking

The `<modules>` section has `overrideMode="Allow"` by default when ASP.NET is installed. The CIS Benchmark for IIS does not include a recommendation to lock this section. Path B's non-admin registration capability is available in default configurations.

---

## ETW Event ID Correction

### Finding: EID 154 is assembly load; EID 155 is unload/rundown

| Event | Event ID | Provider | Description |
|---|---|---|---|
| `AssemblyLoad_V1` | **154** | Microsoft-Windows-DotNETRuntime (runtime) | Real-time assembly load |
| `AssemblyUnload_V1` | **155** | Microsoft-Windows-DotNETRuntime (runtime) | Assembly unload |
| `AssemblyDCStart_V1` | **155** | Microsoft-Windows-DotNETRuntimeRundown (rundown) | Enumeration of loaded assemblies |

The scoping document's Constraint #6 cites EID 155 — this should be EID 154 (`AssemblyLoad_V1`) from the runtime provider with `LoaderKeyword (0x8)`.

Neither provider is enabled as a persistent Windows Event Log by default. Requires active ETW consumer session.

**ETW suppression risk:** CLR ETW events are emitted via `ntdll!EtwEventWrite` in userland. An attacker controlling `w3wp.exe` can patch this function (T1562.006). EDR CLR hooks on `nLoadImage` inside `clr.dll` are more resistant.

---

## Sources

- [Splunk: Fantastic IIS Modules and How to Find Them](https://www.splunk.com/en_us/blog/security/fantastic-iis-modules-and-how-to-find-them.html)
- [IIS Support Blog: IIS 7.5 Configuration Auditing](https://blogs.iis.net/webtopics/iis-7-5-how-to-enable-iis-configuration-auditing/)
- [Microsoft Learn: Loader ETW Events](https://learn.microsoft.com/en-us/dotnet/framework/performance/loader-etw-events)
- [Microsoft Learn: CLR ETW Providers](https://learn.microsoft.com/en-us/dotnet/framework/performance/clr-etw-providers)
- [MDSec: Bypassing Image Load Kernel Callbacks](https://www.mdsec.co.uk/2021/06/bypassing-image-load-kernel-callbacks/)
- [GitHub: CLR-Unhook](https://github.com/hwbp/CLR-Unhook)
- [XPN InfoSec: Hiding your .NET - ETW](https://blog.xpnsec.com/hiding-your-dotnet-etw/)
- [CrowdStrike: Falcon OverWatch Detects IceApple](https://www.crowdstrike.com/en-us/blog/falcon-overwatch-detects-iceapple-framework/)
- [TrustedSec SysmonCommunityGuide: file-create.md](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/file-create.md)
- [TrustedSec SysmonCommunityGuide: image-loading.md](https://github.com/trustedsec/SysmonCommunityGuide/blob/master/chapters/image-loading.md)
- [Microsoft Learn: Event 4663](https://learn.microsoft.com/en-us/previous-versions/windows/it-pro/windows-10/security/threat-protection/auditing/event-4663)
- [Detection.FYI: win_iis_module_added Sigma rule](https://detection.fyi/sigmahq/sigma/windows/builtin/iis-configuration/win_iis_module_added/)
- [Sigma: win_iis_module_added](https://detection.fyi/sigmahq/sigma/windows/builtin/iis-configuration/win_iis_module_added/)
- [Microsoft TechCommunity: IIS Configuration Auditing](https://techcommunity.microsoft.com/t5/iis-support-blog/iis-7-5-how-to-enable-iis-configuration-auditing/ba-p/347239)
- [Sygnia: Praying Mantis](https://www.sygnia.co/praying-mantis-detecting-and-hunting)
- [CISA: AR21-112A SUPERNOVA Analysis](https://www.cisa.gov/news-events/analysis-reports/ar21-112a)
