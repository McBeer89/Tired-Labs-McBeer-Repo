# TRR Research Notes: File-Based Web Shell Execution via IIS

**Working TRR ID:** TRR0000 (assigned on PR acceptance)  
**Technique:** File-Based Web Shell Execution via IIS  
**External IDs:** [T1505.003], [A02:2025 – OWASP]  
**Platform:** Windows (IIS)  
**Scope:** File-based web shells (fileless/memory-based to be documented in a
separate TRR)  
**Researcher:** John  
**Status:** Phase 4 Complete — DDM Finalized, TRR Submission-Ready

---

## 1. Technique Summary

A web shell is a malicious script placed on a web server that gives an attacker
remote command execution through the server's normal HTTP request-handling
mechanisms. The attacker interacts with the shell by sending crafted HTTP
requests to the shell's URL. The web server processes the request like any
legitimate page, but the shell's code executes the attacker's commands and
returns the output in the HTTP response.

**Tactic(s):** Persistence  
**Attacker Objective:** Maintain persistent remote access and command execution
via a web server.

---

## 2. Why Attackers Use Web Shells

| Benefit           | Explanation |
|-------------------|-------------|
| Persistence       | The shell survives reboots — it's just a file on disk. |
| Stealth           | Traffic blends with normal web traffic (HTTP/HTTPS on 80/443). |
| Firewall Bypass   | Web traffic is almost always allowed through perimeter firewalls. |
| Flexibility       | Can run commands, upload/download files, browse the filesystem, interact with databases, pivot to internal systems. |
| Low Footprint     | No new processes or services are installed — the existing web server does all the work. |

---

## 3. IIS Architecture — Key Components

Understanding IIS architecture is foundational to building an accurate DDM.
Every operation in the model must map to a real component in this architecture.

### 3.1 HTTP.sys (Kernel-Mode Listener)

HTTP.sys is a **kernel-mode driver** that listens for incoming HTTP/HTTPS
requests on configured ports (typically 80 and 443). It handles basic tasks
like caching and routing at the kernel level. When a request needs actual
processing, HTTP.sys routes it to the appropriate **application pool**.

**Detection relevance:** HTTP.sys is the entry point. All web shell traffic
passes through it, but it operates at too low a level for most detection
strategies.

**Reference:** [HTTP.sys — Microsoft Docs]

### 3.2 Application Pools (App Pools)

An application pool is an **isolation boundary**. Each app pool runs as its own
`w3wp.exe` process (the IIS Worker Process). Different websites or applications
on the same server can run in different app pools, meaning different `w3wp.exe`
processes with potentially different permissions.

**Detection relevance:** The app pool identity determines the security context
of the web shell. Misconfigured pools running as high-privilege accounts
significantly increase impact.

**Reference:** [Application Pools in IIS — Microsoft Docs]

### 3.3 w3wp.exe (The Worker Process) ⭐

This is the most important component for detection. When HTTP.sys routes a
request to an app pool, `w3wp.exe` handles it. This process:

- Loads and executes the requested file (ASPX, ASP, PHP, etc.)
- Runs under the app pool's identity (default: `IIS AppPool\DefaultAppPool`)
- Has access to whatever resources that identity has permissions for
- **Can spawn child processes** — critical for detection

**Detection relevance:** `w3wp.exe` is the process that executes web shell
code. Any commands the web shell runs via `Process.Start()` (cmd.exe,
powershell.exe, etc.) will be **child processes of w3wp.exe**. This
parent-child relationship is one of the strongest detection signals.

**IMPORTANT:** w3wp.exe does NOT spawn a child process for all web shell
activity. It only spawns a child process when the web shell code explicitly
starts a new process. Actions performed through .NET framework APIs (file I/O,
database queries, network requests) execute inside w3wp.exe and produce no
child process.

**Reference:** [IIS Worker Process (w3wp.exe) — Microsoft Docs]

### 3.4 The IIS Request Pipeline

When a request arrives for a web shell (e.g., `/uploads/shell.aspx`):

```
Client (attacker) sends HTTP request
        │
        ▼
   ┌──────────┐
   │ HTTP.sys  │  Kernel-mode listener receives request
   └────┬─────┘
        │  Routes to correct app pool based on site bindings
        ▼
   ┌──────────┐
   │ w3wp.exe  │  IIS Worker Process picks up the request
   └────┬─────┘
        │  Checks handler mapping based on file extension
        ▼
   ┌──────────────┐
   │ Handler Match │  Determines ASP.NET, Classic ASP, Static, etc.
   └────┬─────────┘
        │  If executable handler, processes the file
        ▼
   ┌──────────────┐
   │ Execute Code  │  Handler compiles/interprets and runs the code
   └────┬─────────┘
        │  Web shell code runs
        ▼
   HTTP response returned to attacker via HTTP.sys
```

### 3.5 Handler Mappings — Why File Extension Matters

IIS uses **handler mappings** to determine how to process a requested file.
Only files with mapped handlers get executed — everything else is served as
static content.

| Extension | Handler | Executed? |
|-----------|---------|-----------|
| `.aspx`   | ASP.NET Engine | ✅ Yes |
| `.asp`    | Classic ASP Engine | ✅ Yes |
| `.ashx`   | ASP.NET Generic Handler | ✅ Yes |
| `.asmx`   | ASP.NET Web Service | ✅ Yes |
| `.shtml`, `.stm`, `.shtm` | Server-Side Includes (ssinc.dll) | ✅ Yes (if SSI enabled) |
| `.php`    | PHP-CGI / FastCGI (if installed) | ✅ Yes (if configured) |
| `.html`, `.css`, `.js`, `.jpg` | Static File Handler | ❌ No (served as-is) |

**Key takeaway for DDM:** The web shell MUST use a file extension that IIS is
configured to execute — unless the attacker modifies handler mappings via
web.config (see Section 3.8). On a default IIS/.NET server, the attacker needs
ASP or ASPX.

**Reference:** [Handler Mappings in IIS — Microsoft Docs]

### 3.5.1 ASP vs ASPX Execution Mechanics

Although both .asp and .aspx files are "executed" by IIS, the execution
mechanics differ in ways that matter for detection:

**Classic ASP (.asp):** The ASP engine (`asp.dll`) **interprets** the script
code directly inside the w3wp.exe process. No compilation step, no artifacts
on disk beyond the original .asp file.

**ASP.NET (.aspx):** On the **first request**, the ASP.NET engine **compiles**
the .aspx file into a .NET assembly (DLL). This compiled DLL is stored in:
`C:\Windows\Microsoft.NET\Framework64\<version>\Temporary ASP.NET Files\`

The compiled DLL is then loaded into the w3wp.exe process for execution.
Subsequent requests reuse the already-compiled DLL (no recompilation). On
older versions of ASP.NET, this compilation may spawn `csc.exe` (the C#
compiler) as a child process of w3wp.exe; on newer versions using the Roslyn
compiler, the compilation may occur in-process.

**Key takeaway for DDM:** The ASP.NET compilation step is:
- **Essential** (must happen for .aspx execution)
- **Immutable** (the attacker cannot skip it)
- **Observable** (DLL creation in Temp ASP.NET Files directory — Sysmon 11)

This is modeled in the DDM as a lower-abstraction sub-operation of Execute
Code (downward arrow).

### 3.5.2 Child Process Clarification

w3wp.exe does NOT spawn a child process for all web shell activity. The
behavior depends on what the web shell code does:

**Spawns a child process (detectable):**
- `System.Diagnostics.Process.Start("cmd.exe", "/c whoami")` → child process
- Any call that explicitly launches an external program

**Does NOT spawn a child process (harder to detect):**
- `System.IO.File.ReadAllText("C:\\secret.txt")` → no child process
- `System.IO.Directory.GetFiles()` → no child process
- `System.Net.WebClient` → no child process
- `System.Data.SqlClient` → no child process

This distinction is fundamental to why Procedures A and B are separate.

### 3.6 The Web Root Directory

Every IIS site has a **physical path** — a directory on the file system where
content lives. Default: `C:\inetpub\wwwroot\`.

For a web shell to be accessible via HTTP, the file must be placed somewhere
within this directory structure or within a **virtual directory** configured in
IIS. Virtual directories can map to physical paths anywhere on the file system
(e.g., `D:\shared\uploads\`), extending the web-accessible area beyond the
default web root. Files placed outside of any web-accessible path cannot be
triggered by an HTTP request.

**Key takeaway for DDM:** File placement in a web-accessible directory is an
**essential** operation. The specific path is broader than just `wwwroot` due
to virtual directories.

### 3.7 Security Context

`w3wp.exe` runs under the app pool's configured identity:

| Identity Type | Default? | Risk Level |
|---------------|----------|------------|
| `IIS AppPool\<PoolName>` (Virtual Account) | ✅ Default | Low — limited permissions |
| `NetworkService` | Sometimes configured | Medium |
| Domain service account | Misconfiguration | High |
| `LocalSystem` | Misconfiguration | Critical — full system access |

The web shell inherits whatever permissions this identity has. This determines
what the attacker can do post-execution.

**Key takeaway for DDM:** Security context is important for impact analysis,
but it's not an operation in the DDM — it's a property of the execution
environment.

### 3.8 web.config and Handler Manipulation

IIS configuration can be modified at the directory level via `web.config` files.
An attacker who can write a `web.config` file to a web-accessible directory can:

**Variant 1 — Custom handler mapping:** Add a handler mapping that tells IIS to
process an unusual file extension (like `.jpg` or `.txt`) through the ASP.NET
engine. The attacker then drops a web shell with that innocuous extension.
The web.config makes Match Handler match an extension it normally wouldn't.

**Variant 2 — Inline handler:** Define an `IHttpHandler` directly in the
web.config XML. The web.config file itself contains the web shell code. No
separate script file is needed at all.

Both variants share a critical operation: writing or modifying a `web.config`
file in a web-accessible directory. When a web.config is placed in a
subdirectory, IIS dynamically reloads that directory's configuration.

**Additional note:** IIS supports an Application Initialization feature that
can preload pages when an app pool starts. If an attacker can configure this
(via web.config), IIS itself would automatically trigger the web shell on
restart or app pool recycle, eliminating the need for the attacker to send
their own HTTP request.

**Key takeaway for DDM:** web.config manipulation constitutes a distinct
procedure (Procedure C) because it changes how Match Handler behaves and can
eliminate the need for a separate script file entirely.

**Telemetry:** Sysmon 11 (file creation), File Integrity Monitoring, IIS
configuration change logging.

### 3.9 Server-Side Includes (SSI)

IIS supports Server-Side Includes via `ssinc.dll`. Files with extensions
`.shtml`, `.stm`, and `.shtm` can execute directives like
`<!--#exec cmd="whoami"-->`. If SSI is enabled, these are additional
executable extensions an attacker could use. However, the essential operations
are identical to Procedures A/B — the only difference is the handler and
extension, which are tangential. SSI does not constitute a separate procedure.

---

## 4. Essential Constraints for DDM Construction

Based on Phase 1 and 2 research, these are the constraints that MUST be true
for a file-based web shell to execute on IIS:

| # | Constraint | Essential? | Immutable? | Observable? |
|---|-----------|------------|------------|-------------|
| 1 | A file must be written to disk (new or modified) OR a web.config with inline handler must exist in a web-accessible directory | ✅ | ✅ | ✅ (Sysmon 11, Sysmon 2, FIM) |
| 2 | The file must have an extension mapped to an executable handler (default or via custom web.config) | ✅ | ✅ | ✅ (file extension is visible) |
| 3 | An HTTP request must be sent to the file's URL (or IIS must auto-trigger via Application Initialization) | ✅ | ✅ | ✅ (IIS W3C logs) |
| 4 | IIS (w3wp.exe) must process and execute the file's code | ✅ | ✅ | ✅ (ASP.NET compilation artifacts for .aspx) |
| 5 | The web shell must perform an action: spawn a process OR call .NET APIs | ✅ | ✅ | Varies (Sysmon 1 / Event 4688 for process spawn; no direct telemetry for .NET API calls) |

**What is NOT essential (tangential/optional):**

- Specific tool used to upload the file (exploit, RDP, WebDAV, compromised
  creds, etc.)
- Specific web shell tool or framework (China Chopper, ASPX Spy, etc.)
- Specific commands the attacker runs through the shell
- Specific file name chosen by the attacker
- Encoding or obfuscation techniques used in the shell code
- One-liner vs full-featured web shell (same operations regardless)

---

## 5. Validated Procedures

Based on DDM analysis and multiple validation passes, three distinct procedures
were identified for file-based web shell execution on IIS:

| ID | Name | Summary | Distinguishing Operations |
|----|------|---------|--------------------------|
| TRR0000.WIN.A | Web Shell with OS Command Execution | Web shell spawns child processes from w3wp.exe to run OS commands | Process Spawn (parent: w3wp.exe) |
| TRR0000.WIN.B | Web Shell with In-Process Execution | Web shell uses .NET APIs directly within w3wp.exe, no child process | Call .NET API (no process spawn) |
| TRR0000.WIN.C | Web Shell via web.config Handler Manipulation | Attacker modifies IIS handler config via web.config to enable execution of unusual extensions or define inline handlers | Write Config (modifies Match Handler behavior) |

**Procedures A and B** share the same prerequisite chain: file on disk → HTTP
request → Route Request → Match Handler → Execute Code. They diverge at what
happens after code execution.

**Procedure C** diverges earlier: it introduces a Write Config operation that
modifies how Match Handler behaves. In Procedure C, Match Handler operates
against the attacker-defined handler mappings rather than the server defaults.
In the inline handler variant, Write Config eliminates the need for a separate
script file altogether. Post-execution behavior (process spawn or .NET API
call) depends on the web shell's code, not on how the handler was configured,
so Procedure C can lead to either endpoint.

### Noted but Out of Scope

| Item | Status | Rationale |
|------|--------|-----------|
| PHP via FastCGI on IIS | Noted on DDM, out of scope | Different execution model (php-cgi.exe); better suited to a platform-agnostic TRR |
| Fileless/memory web shells | Separate TRR | Fundamentally different essential operations (IIS modules, reflection, pipeline injection) |
| ISAPI filter/extension web shells | Separate TRR | Falls under fileless/module category |

---

## 6. DDM Summary

The validated DDM contains the following operations:

### Prerequisite Operations (feed into Match Handler)

| Operation | Type | Telemetry | Notes |
|-----------|------|-----------|-------|
| Modify Existing File | Prerequisite | FIM, Sysmon 2 (limited) | Stealthier than new file; Sysmon 11 does NOT fire for modifications |
| Create New File | Prerequisite | Sysmon 11 | Most common delivery method |
| Write Config | Prerequisite | Sysmon 11, FIM, IIS Config Change | Modifies Match Handler behavior; can be sole prerequisite for inline handler variant |

### Pipeline Operations (sequential flow)

| Operation | Telemetry | Notes |
|-----------|-----------|-------|
| Send HTTP Request | None (attacker-side) | Source/attacker machine (green node); server-side logging occurs at Route Request |
| Route Request | IIS W3C Logs | Component: HTTP.sys, Process: w3wp.exe |
| Match Handler | No direct telemetry | Handler: ASP.NET/ASP; behavior modified by Write Config in Procedure C |
| Execute Code | ASP.NET Compilation Artifacts | Process: w3wp.exe, Engine: ASP.NET |

### Post-Execution Branches

| Operation | Telemetry | Notes |
|-----------|-----------|-------|
| Process Spawn | Sysmon 1, Event 4688 | Parent: w3wp.exe; API: System.Diagnostics.Process.Start() or CreateProcess (native); strongest detection signal |
| Call .NET API | No direct telemetry | Side effects may produce telemetry; API calls are attacker-controlled (tangential) |
| Invoke FastCGI | (Out of scope) | Process: php-cgi, Parent: w3wp.exe |

### Sub-Operations (lower abstraction)

| Operation | Parent | Telemetry | Notes |
|-----------|--------|-----------|-------|
| Compile ASPX | Execute Code | Sysmon 11 (DLL in Temp ASP.NET Files) | API: System.CodeDom.Compiler; Output: Temporary ASP.NET Files\<app>\<hash>\<hash>.dll; Compiler: csc.exe (may be in-process on newer versions) |

---

## 7. DDM Structural Notes

**File placement is a prerequisite, not inline with the request flow:**
File operations (Modify Existing File, Create New File, Write Config) are
independent prerequisites. The file could be written days or weeks before the
first HTTP request. They feed into Match Handler, not into the sequential
request pipeline.

**Minor technical note:** Strictly speaking, file prerequisite operations are
prerequisites for Execute Code to succeed (Match Handler checks the extension
in the request URL, not the file on disk). However, modeling them as feeding
into Match Handler clearly communicates the essential relationship and is
appropriate for a DDM.

**Telemetry placement:** Each telemetry source is tagged on the operation it
directly observes, not grouped on a single node.

**The branch point is post-execution behavior:** After Execute Code, the DDM
branches based on what the web shell does (spawn process vs. call API vs.
invoke FastCGI). Each branch arrow is labeled with a conditional description:
- Execute Code → Process Spawn: "If shell calls OS command"
- Execute Code → Call .NET API: "If in process API"
- Execute Code → Invoke FastCGI: "If PHP"

**Per-procedure exports use red-highlighted arrows:** Following the convention
established in TRR0016, each procedure's DDM export uses red arrows to
highlight the active path for that procedure. Non-active paths remain in black
for context. All three exports use the same master DDM layout.

**Compile ASPX is a lower-abstraction sub-operation:** Shown with a downward
arrow from Execute Code, not as a branch alternative.

---

## 8. Scoping Decisions

Items explicitly excluded from this TRR and rationale:

| Excluded Item | Rationale |
|---|---|
| Fileless/memory web shells (IIS modules, reflection) | Different essential operations; fundamentally different prerequisite chain; separate TRR |
| ISAPI filter/extension web shells | Falls under fileless/module category; compiled DLL, not script file |
| PHP on IIS (FastCGI) | Noted on DDM as out of scope; different execution model (php-cgi.exe) better suited to platform-agnostic TRR |
| Specific delivery methods (exploit, RDP, WebDAV, etc.) | Tangential — attacker controls the method |
| Specific web shell tools (China Chopper, ASPX Spy, etc.) | Tangential — same operations regardless of tool |
| Obfuscation/encoding techniques | Tangential — doesn't change essential operations |
| Linux/macOS web servers (Apache, Nginx) | Different platforms with different architectures; separate TRR |
| Post-exploitation beyond initial execution | Different techniques entirely |
| One-liner vs full-featured shells | Same procedure per TIRED Labs definition |
| Server-Side Includes (SSI) | Same essential operations as Procedures A/B; only handler/extension differ (tangential) |
| WebDAV PUT delivery | Tangential delivery method for Write File operation |

---

## 9. References

### Primary References

- [T1505.003 — MITRE ATT&CK]: https://attack.mitre.org/techniques/T1505/003/
- [A02:2025 Security Misconfiguration — OWASP]: https://owasp.org/Top10/A05_2021-Security_Misconfiguration/
- [Improving Threat Identification with Detection Modeling — VanVleet]: https://medium.com/@vanvleet/improving-threat-identification-with-detection-data-models-1cad2f8ce051
- [Arrows App (DDM tool)]: https://arrows.app/

### IIS Architecture References

- [Introduction to IIS Architecture — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/get-started/introduction-to-iis/introduction-to-iis-architecture
- [HTTP.sys Web Server — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/get-started/introduction-to-iis/introduction-to-iis-architecture#httpsys
- [Application Pools in IIS — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/applicationpools/
- [IIS Worker Process and WAS — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/manage/provisioning-and-managing-iis/features-of-the-windows-process-activation-service-was
- [Handler Mappings in IIS — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/configuration/system.webserver/handlers/
- [IIS Modules Overview — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/get-started/introduction-to-iis/iis-modules-overview
- [Virtual Directories in IIS — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/configuration/system.applicationhost/sites/site/application/virtualdirectory
- [web.config Reference — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/configuration/
- [IIS Application Initialization — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/configuration/system.webserver/applicationinitialization/
- [Server-Side Includes (SSI) in IIS — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/configuration/system.webserver/serversideinclude

### ASP / ASP.NET References

- [ASP.NET Compilation Overview — Microsoft Learn]: https://learn.microsoft.com/en-us/previous-versions/aspnet/ms178466(v=vs.100)
- [ASP.NET Temporary Files — Microsoft Learn]: https://learn.microsoft.com/en-us/previous-versions/aspnet/ms366723(v=vs.100)
- [IHttpHandler Interface — Microsoft Learn]: https://learn.microsoft.com/en-us/dotnet/api/system.web.ihttphandler
- [System.Diagnostics.Process Class — Microsoft Learn]: https://learn.microsoft.com/en-us/dotnet/api/system.diagnostics.process
- [Classic ASP Overview — Microsoft Learn]: https://learn.microsoft.com/en-us/previous-versions/iis/6.0-sdk/ms524929(v=vs.90)
- [FastCGI on IIS — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/configuration/system.webserver/fastcgi/

### Telemetry and Detection References

- [Sysmon — Microsoft Sysinternals]: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon
- [Sysmon Event ID 1 — Process Creation]: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon#event-id-1-process-creation
- [Sysmon Event ID 11 — File Create]: https://learn.microsoft.com/en-us/sysinternals/downloads/sysmon#event-id-11-filecreate
- [Windows Security Event 4688 — Process Creation]: https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4688
- [Windows Security Event 4663 — Object Access]: https://learn.microsoft.com/en-us/windows/security/threat-protection/auditing/event-4663
- [IIS W3C Logging — Microsoft Learn]: https://learn.microsoft.com/en-us/iis/configuration/system.webserver/httplogging

### TIRED Labs Methodology References

- [Threat Detection Engineering: The Series — VanVleet]: https://medium.com/@vanvleet/threat-detection-engineering-the-series-7fe818fdfe62
- [TIRED Labs TRR Library]: https://library.tired-labs.org
- [Identifying and Classifying Attack Techniques — VanVleet]: https://medium.com/@vanvleet/identifying-and-classifying-attack-techniques-002c0c4cd595
- [Creating Resilient Detections — VanVleet]: https://medium.com/@vanvleet/creating-resilient-detections-db648a352854
- [Technique Analysis and Modeling — VanVleet]: https://medium.com/@vanvleet/technique-analysis-and-modeling-b95f48b0214c
- [Technique Research Reports: Capturing and Sharing Threat Research — VanVleet]: https://medium.com/@vanvleet/technique-research-reports-capturing-and-sharing-threat-research-9512f36dcf5c
- [What is a Procedure? — Jared Atkinson]: https://posts.specterops.io/on-detection-tactical-to-function-810c14798f63
- [Capability Abstraction — Jared Atkinson]: https://posts.specterops.io/capability-abstraction-fbeaeeb26384
- [Thoughts on Detection — Jared Atkinson]: https://posts.specterops.io/thoughts-on-detection-3c5cab66f511
- [Understanding the Function Call Stack — Jared Atkinson]: https://posts.specterops.io/understanding-the-function-call-stack-f08b5341efa4

### Additional Reading

**Government Advisories and Guidance:**

- [NSA/CISA: Detect and Prevent Web Shell Malware (2020)]: https://media.defense.gov/2020/Jun/09/2002313081/-1/-1/0/CSI-DETECT-AND-PREVENT-WEB-SHELL-MALWARE-20200422.PDF
- [ACSC: Web Shell Threat Advisory]: https://www.cyber.gov.au/resources-business-and-government/maintaining-devices-and-systems/system-hardening-and-administration/web-hardening/web-shells

**Microsoft Threat Research:**

- [Web Shell Attacks Continue to Rise — Microsoft Security Blog (2021)]: https://www.microsoft.com/en-us/security/blog/2021/02/11/web-shell-attacks-continue-to-rise/
- [HAFNIUM Targeting Exchange Servers with 0-Day Exploits — Microsoft (2021)]: https://www.microsoft.com/en-us/security/blog/2021/03/02/hafnium-targeting-exchange-servers/
- [Web Shell Threat Hunting with Azure Sentinel — Microsoft (2021)]: https://www.microsoft.com/en-us/security/blog/2021/09/15/analyzing-attacks-that-exploit-the-mshtml-cve-2021-40444-vulnerability/

**Industry Research:**

- [An Introduction to Web Shells — SANS (2018)]: https://www.sans.org/white-papers/39260/
- [Anatomy of a Web Shell — Volexity]: https://www.volexity.com/blog/
- [Red Canary Threat Detection Report — Web Shells]: https://redcanary.com/threat-detection-report/
- [Atomic Red Team Tests for T1505.003]: https://github.com/redcanaryco/atomic-red-team/blob/master/atomics/T1505.003/T1505.003.md

**Detection Engineering and Sysmon:**

- [Sysmon Configuration Guide — SwiftOnSecurity]: https://github.com/SwiftOnSecurity/sysmon-config
- [Sysmon Modular Configuration — olafhartong]: https://github.com/olafhartong/sysmon-modular
- [OSSEM Detection Model — Roberto Rodriguez]: https://ossemproject.com/dm/intro.html
