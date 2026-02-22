# TRR0000 — Detection Methods

**Source TRR:** TRR0000 — File-Based Web Shell Execution via IIS  
**Technique:** T1505.003 — Server Software Component: Web Shell  
**Platform:** Windows (IIS)  
**Procedures:** A (OS Command Execution), B (In-Process Execution),
C (web.config Manipulation)

> This document is the detection team's derivative of TRR0000. It translates
> the DDM operations and telemetry into actionable detection specifications,
> incorporating findings from lab recreation testing. For the technique's
> technical background, procedures, and DDM diagrams, refer to TRR0000.

---

## DDM Analysis

The shared pipeline operations (Send HTTP Request → Route Request → Match
Handler → Execute Code) lack telemetry suitable for automated detection. Route
Request has no server-side telemetry. Match Handler has none. Execute Code has
none. Send HTTP Request is observable through IIS W3C logs, but classification
is extremely difficult — web shell requests are structurally identical to
legitimate requests.

Detection opportunities exist at three points in the DDM:

1. **Prerequisite operations** — file creation and web.config writes happen
   before the pipeline executes
2. **Post-execution divergence** — Process Spawn (Procedure A) produces
   high-fidelity process telemetry
3. **Compilation sub-operation** — Compile ASPX produces file creation events
   and, on .NET Framework, a `csc.exe` child process

No single detection point covers all three procedures. A layered approach is
required.

---

## Detection Specifications

Ordered by implementation priority. Deploy Specification 1 first for immediate
coverage of the highest-risk procedure path, then layer in the remaining
specifications to close gaps.

### Specification 1 — w3wp.exe Child Process Creation

| | |
|---|---|
| **DDM Operation** | Process Spawn |
| **Telemetry** | Sysmon 1 (ProcessCreate), Win 4688 (ProcessCreate) |
| **Procedures** | A ✅, B ❌, C ✅ (when shell spawns a process) |
| **Priority** | Deploy first |

**Logic:** Alert when `w3wp.exe` is the parent process of `cmd.exe`,
`powershell.exe`, `csc.exe`, or other command interpreters and system
utilities (`whoami.exe`, `net.exe`, `ipconfig.exe`, `systeminfo.exe`,
`net1.exe`, `nltest.exe`, etc.).

**Classification:** Inherently suspicious. Under normal IIS operations,
`w3wp.exe` rarely spawns command interpreters. The primary legitimate exception
is `csc.exe` during first-time ASP.NET page compilation — in pre-compiled
production environments this should not occur, but development servers will
produce benign `csc.exe` spawns.

**Lab evidence:** Confirmed across Procedure A (`cmd.exe /c whoami`,
`cmd.exe /c ipconfig`) and Procedure C1 (`cmd.exe /c whoami` through `.txt`
handler remapping). Full parent-child chain captured in both Sysmon 1 and
Win 4688 with complete command lines. The detection fires identically
regardless of file extension — the parent-child relationship is the same
whether the shell is `.aspx`, `.asp`, `.txt`, or `.info`.

**Key fields:**

| Field | Value |
|---|---|
| ParentImage | `C:\Windows\System32\inetsrv\w3wp.exe` |
| Image | `cmd.exe`, `powershell.exe`, etc. |
| User | `IIS APPPOOL\<PoolName>` |
| CommandLine | Attacker-controlled (tangential, but useful for triage) |

**Tuning notes:** Consider allowlisting specific scheduled tasks or known
management scripts that legitimately invoke `w3wp.exe` child processes.
`csc.exe` spawns can be handled as a separate, lower-severity rule (see
Specification 5).

---

### Specification 2 — Non-Standard Extension Compilation Artifacts

| | |
|---|---|
| **DDM Operation** | Compile ASPX (sub-operation of Execute Code) |
| **Telemetry** | Sysmon 11 (FileCreate) |
| **Procedures** | A ❌, B ❌, C ✅ (custom handler mapping variant only) |
| **Priority** | Deploy second — unique coverage for Procedure C |

**Logic:** Alert on file creation in `Temporary ASP.NET Files\` where the
filename contains a `.compiled` suffix and the source extension is NOT a
recognized ASP.NET script type (`.aspx`, `.ashx`, `.asmx`, `.cshtml`,
`.vbhtml`).

**Classification:** Inherently suspicious. There is no legitimate reason for
ASP.NET to compile `.txt`, `.jpg`, `.info`, `.log`, or other non-script
extensions. This detection has near-zero false positives.

**Lab evidence:** Confirmed with two variants:

| Variant | Artifact |
|---|---|
| C1 (`.txt`) | `readme.txt.cdcab7d2.compiled` |
| C2 (`.info`) | `status.info.cdcab7d2.compiled` |

Both appeared in `C:\Windows\Microsoft.NET\Framework64\v4.0.30319\Temporary
ASP.NET Files\<app_name>\` along with companion artifacts (`App_Web_*.dll`,
generated `.cs` source files, compiler I/O files).

**Key fields:**

| Field | Value |
|---|---|
| TargetFilename | `*\Temporary ASP.NET Files\*\*.compiled` |
| Exclusion | Source extension = `.aspx`, `.ashx`, `.asmx`, `.cshtml`, `.vbhtml` |

**Additional signal:** Each IIS Application gets its own subdirectory within
Temporary ASP.NET Files. The appearance of a new, unexpected subdirectory
name is itself an indicator that a new application path has been configured.

---

### Specification 3 — web.config Creation in Web Directories

| | |
|---|---|
| **DDM Operation** | Write Config |
| **Telemetry** | Sysmon 11 (FileCreate), FIM |
| **Procedures** | A ❌, B ❌, C ✅ (both variants) |
| **Priority** | Deploy third — covers both Procedure C variants |

**Logic:** Alert on creation of `web.config` files in IIS web root directories
or their subdirectories.

**Classification:** Suspicious in most production environments. Web.config
changes should be rare and controlled through change management. In development
or CMS environments, correlate with deployment processes to reduce noise.

**Lab evidence:** web.config creation captured by Sysmon 11 at file deployment
time and by Win 4663 (SACL) audit events.

**Key fields:**

| Field | Value |
|---|---|
| TargetFilename | `*\inetpub\wwwroot\*\web.config` (adjust to match your web roots) |

**Gap:** Sysmon 11 fires only on new file creation, not modification of an
existing `web.config`. Covering modifications requires FIM or SACL auditing
configured on the web root with write access monitoring.

---

### Specification 4 — Script File Creation in Web Root

| | |
|---|---|
| **DDM Operation** | Create New File |
| **Telemetry** | Sysmon 11 (FileCreate) |
| **Procedures** | A ⚠️, B ⚠️, C ⚠️ (custom handler variant) |
| **Priority** | Deploy fourth — broad but noisier coverage |

**Logic:** Alert on new files with executable extensions (`.aspx`, `.asp`,
`.ashx`, `.asmx`) created in IIS web root directories.

**Classification:** Context-dependent. On static content servers with no
deployment activity, any new script file is suspicious. On servers with active
CMS or CI/CD deployments, significant tuning is required. Investigate files
created by unexpected processes (anything other than the deployment pipeline).

**Lab evidence:** All Procedure A and B test shells triggered Sysmon 11 at
deployment time.

**Key fields:**

| Field | Value |
|---|---|
| TargetFilename | `*\inetpub\wwwroot\*.aspx`, `*.asp`, `*.ashx`, `*.asmx` |

**Gap:** Does not cover file modification (code injection into existing files).
Does not cover Procedure C's non-standard extensions — that's handled by
Specification 2.

---

### Specification 5 — Dynamic ASP.NET Compilation (csc.exe from w3wp.exe)

| | |
|---|---|
| **DDM Operation** | Compile ASPX (sub-operation of Execute Code) |
| **Telemetry** | Sysmon 1 (ProcessCreate), Win 4688 (ProcessCreate) |
| **Procedures** | A ⚠️, B ⚠️, C ⚠️ (`.aspx` and ASPX-compiled shells only) |
| **Priority** | Deploy fifth — corroborating signal |

**Logic:** Alert when `w3wp.exe` spawns `csc.exe`. On .NET Framework 4.8 (the
default ASP.NET runtime on Windows Server), every first-time ASPX compilation
triggers this. In pre-compiled production environments, this should not occur
outside of deployments.

**Classification:** Suspicious in context. Development servers will produce
legitimate `csc.exe` spawns. Best used as a corroborating signal rather than
standalone alerting — correlate with new file creation (Specification 4) or
non-standard extension artifacts (Specification 2).

**Lab evidence:** Confirmed across all procedures where ASPX compilation
occurred. Each variant (Procedure A shell, Procedure C1 `.txt`, Procedure C2
`.info`) produced a separate `csc.exe` spawn on first access.

**Note:** On ASP.NET Core or environments using the Roslyn in-process compiler,
compilation may occur entirely within `w3wp.exe` without spawning `csc.exe`.
This detection applies to the classic .NET Framework pipeline.

---

### Specification 6 — IIS Log Analysis (Hunt)

| | |
|---|---|
| **DDM Operation** | Send HTTP Request |
| **Telemetry** | IIS W3C Logs |
| **Procedures** | A ✅, B ✅, C ✅ |
| **Priority** | Ongoing hunt — not automated alerting |

**Logic:** Hunt for anomalous request patterns:

- POST requests to files that normally receive only GET
- Requests with suspicious query parameters (`cmd=`, `action=`, `exec=`)
- HTTP 200 responses for unusual file extensions (`.txt`, `.info`, `.log`)
- First-seen URIs with anomalously high response times (compilation overhead)
- Single-file access patterns from unusual source IPs
- The 500 → 200 transition pattern (attacker iterating on web.config)

**Classification:** Requires analyst judgment. Web shell requests are
structurally identical to legitimate traffic. This is the only telemetry with
100% identification across all three procedures, but classification difficulty
makes it unsuitable for automated alerting in most environments.

**Lab evidence:** IIS W3C logs captured all test activity across all
procedures. Key observations from lab testing:

- First-access response times showed clear compilation overhead (647ms vs
  subsequent 0-1ms) — a useful forensic indicator
- The `cmd=whoami` and `action=listdir` query parameters were visible in
  `cs-uri-query`
- The 500 → 200 transition for Procedure C (as the attacker refined their
  web.config) was clearly visible in the logs

---

## Procedure Coverage Matrix

|                    | Spec 1: Process Spawn | Spec 2: Non-Std Compile | Spec 3: web.config | Spec 4: File Create | Spec 5: csc.exe | Spec 6: IIS Logs |
|--------------------|:---:|:---:|:---:|:---:|:---:|:---:|
| **TRR0000.WIN.A**  | ✅  | —   | —   | ⚠️* | ⚠️** | ✅ (hunt) |
| **TRR0000.WIN.B**  | —   | —   | —   | ⚠️* | ⚠️** | ✅ (hunt) |
| **TRR0000.WIN.C**  | ⚠️***| ✅ | ✅  | —   | ⚠️** | ✅ (hunt) |

\* New file creation only — not file modification.  
\*\* ASPX shells only, first access only, .NET Framework only.  
\*\*\* Only when the Procedure C shell spawns a child process.

---

## Known Blind Spots

### Procedure B via file modification

An attacker injects web shell code into an existing legitimate `.aspx` page and
operates exclusively through .NET APIs. In this scenario:

- Specification 1 does not apply (no child process)
- Specification 2 does not apply (standard `.aspx` extension)
- Specification 3 does not apply (no web.config involved)
- Specification 4 does not apply (file modification, not creation)
- Specification 5 may fire on first recompilation, but recompilation of an
  existing page is not inherently suspicious
- Specification 6 (IIS logs) is the sole detection opportunity

**Lab validation:** Confirmed. Procedure B testing produced zero Sysmon 1
events. SACL auditing was tested but found insufficient — Procedure B performs
only read operations (`Directory.GetDirectories`, `File.ReadAllText`), and the
SACL was configured for write access. Adding `ReadData` auditing would catch
these operations but would generate unacceptable noise from every legitimate
page request.

**Mitigation options:** File Integrity Monitoring on web root directories
(detects the prerequisite file modification, not the execution). Content-aware
scanning for known web shell signatures. Network-level anomaly detection for
unusual `w3wp.exe` outbound connections (Sysmon 3).

### Application Initialization persistence

When an attacker configures IIS Application Initialization via web.config to
auto-trigger the web shell on app pool recycle, no attacker-initiated HTTP
request occurs. Specification 6 (IIS logs) may not show external attacker
requests. Specification 3 (web.config monitoring) remains fully effective for
this variant since the attacker must still write the web.config.

---

## Source References

- **TRR0000** — File-Based Web Shell Execution via IIS (technique research)
- **TRR0000 DDM** — Detection Data Model with telemetry mapping
- **TRR0000 Lab Recreation Guide** — Procedure execution and telemetry
  validation
