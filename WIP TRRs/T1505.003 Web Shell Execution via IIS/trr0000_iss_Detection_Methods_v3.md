# TRR0000 Detection Strategy: File-Based Web Shell Execution via IIS

**TRR ID:** TRR0000  
**Technique:** T1505.003 — Server Software Component: Web Shell  
**Platform:** Windows (IIS)  
**Procedures:**

| ID             | Name                                    |
|----------------|-----------------------------------------|
| TRR0000.WIN.A  | Web Shell with OS Command Execution     |
| TRR0000.WIN.B  | Web Shell with In-Process Execution     |
| TRR0000.WIN.C  | Web Shell via web.config Manipulation   |

---

## DDM Walkthrough: Finding the Best Detection Point

Following VanVleet's methodology (A6, Step 9), the goal is to find the
operation in the DDM that is shared by the most procedures and has usable
telemetry. This is where we get the most identification coverage from a single
detection. If no single point covers all procedures, we need a group of
detections that collectively cover them.

### The Shared Pipeline

All three procedures share a common execution pipeline once the prerequisite
files are in place:

    Send HTTP Request → Route Request → Match Handler → Execute Code

This pipeline is the natural place to look first. If we could detect at a
single operation here, we'd have 100% identification across all procedures.
Unfortunately, the DDM shows that most of these operations lack usable
telemetry:

- **Send HTTP Request** — This occurs on the attacker's machine. No server-side
  telemetry.
- **Route Request** — Telemetry available via IIS W3C logs. Every HTTP request
  generates a log entry. However, a web shell request looks identical to a
  legitimate request in these logs, making classification extremely difficult.
  (More on this below.)
- **Match Handler** — Explicitly tagged "No direct telemetry" in the DDM. The
  handler matching process is internal to the IIS pipeline and produces no
  observable log entry.
- **Execute Code** — No direct telemetry for the execution itself. However,
  there is a sub-operation (Compile ASPX) that produces an observable artifact
  for `.aspx` files specifically. (More on this below.)

There is no single operation in the shared pipeline that offers both strong
identification *and* strong classification for all three procedures. This is
unlike VanVleet's T1543.003 example, where "Create Registry Key" provides a
bottleneck that covers 100% of procedures with available telemetry (Sysmon 12
or SACL). We do not have that luxury here.

### The Divergence Points

Since the shared pipeline doesn't give us a clean detection point, we have to
look at where the procedures diverge. The DDM shows two categories of
divergence:

**Prerequisite divergence (how the web shell gets on disk):**

- Procedures A and B: Create New File or Modify Existing File (traditional
  script in web root)
- Procedure C: Write Config (web.config manipulation), optionally accompanied
  by a file with an unusual extension

**Post-execution divergence (what the web shell does after code runs):**

- Procedure A (and C-with-spawn): Process Spawn from w3wp.exe
- Procedure B (and C-with-API): Call .NET API within w3wp.exe

These divergence points are where we must build our detection strategy. Because
no single operation covers everything, we need a **layered approach** — multiple
detections that collectively maximize procedure coverage.

---

## Detection Strategy

### Layer 1 (Primary): Process Spawn from w3wp.exe

**DDM Operation:** Process Spawn  
**Telemetry:** Sysmon Event ID 1 (Process Creation), Windows Security Event
4688 (Process Creation)  
**Key Fields:** Parent process = `w3wp.exe`, Child process = `cmd.exe`,
`powershell.exe`, `whoami.exe`, `net.exe`, `ipconfig.exe`, `systeminfo.exe`,
or other unexpected executables

**Procedure Coverage:**

| Procedure      | Covered? | Notes |
|----------------|----------|-------|
| TRR0000.WIN.A  | ✅ Full  | Process spawn is the distinguishing operation for this procedure |
| TRR0000.WIN.B  | ❌ No    | By definition, Procedure B never spawns a child process |
| TRR0000.WIN.C  | ⚠️ Partial | Covered only when the web.config-delivered shell spawns a process; not covered when it uses .NET APIs exclusively |

**Estimated Identification:** Covers Procedure A fully and Procedure C
partially. Roughly 1.5 of 3 procedures, depending on how frequently Procedure C
shells use process spawn vs. in-process APIs.

**Classification:** **Inherently Suspicious.** Under normal operations,
`w3wp.exe` should rarely, if ever, spawn command interpreters or system
utilities. The parent-child relationship between `w3wp.exe` and `cmd.exe` or
`powershell.exe` is almost never legitimate. This makes classification
straightforward — almost any alert can be treated as likely malicious without
requiring additional context.

**False Positive Considerations:** Very low. Possible exceptions include
legitimate CGI scripts or health monitoring tools that shell out from the web
server, but these are uncommon and can be baselined.

**Why this is Layer 1:** Despite not covering all procedures, the process spawn
detection provides the highest-fidelity signal in the entire DDM. The
combination of strong identification (the parent-child relationship is specific
and essential) with inherently suspicious classification makes it the most
reliable detection point. In VanVleet's terms, this is the detection with the
best ratio of incremental coverage to incremental cost.

---

### Layer 2 (Secondary): File Creation in Web-Accessible Directories

**DDM Operation:** Create New File  
**Telemetry:** Sysmon Event ID 11 (File Create)  
**Key Fields:** Target filename extensions (`.aspx`, `.asp`, `.ashx`, `.asmx`,
`.shtml`, `.stm`, `.shtm`), Target path within IIS web root or virtual
directories

**Procedure Coverage:**

| Procedure      | Covered? | Notes |
|----------------|----------|-------|
| TRR0000.WIN.A  | ⚠️ Partial | Covers only when a **new** file is created; does NOT cover injection into an existing file |
| TRR0000.WIN.B  | ⚠️ Partial | Same limitation as Procedure A |
| TRR0000.WIN.C  | ⚠️ Partial | Covers the custom handler mapping variant (where a web shell file with an unusual extension is created); does NOT cover the inline handler variant (where only web.config is written) |

**Critical Gap — Modify Existing File:** The TRR explicitly documents that
Sysmon Event ID 11 fires only on new file creation. Injecting web shell code
into an existing legitimate page (Modify Existing File in the DDM) does **not**
trigger Sysmon 11. Detection of file modifications requires File Integrity
Monitoring (FIM) or content-aware scanning, which are environment-dependent
capabilities. This is a meaningful identification gap within this layer.

An attacker who injects web shell code into an existing legitimate `.aspx` page
will bypass Sysmon 11-based file monitoring entirely, while still being able to
execute Procedures A or B through that modified file.

**Classification:** **Suspicious Here** or **Suspicious in Context**, depending
on the environment.

- **Suspicious Here** applies when the IIS server runs a static or rarely
  updated application. New `.aspx` or `.asp` files appearing in the web root
  are unusual and can be treated as likely malicious without additional context.
  This is the more common scenario for production servers.
- **Suspicious in Context** applies when the IIS server hosts a CMS, content
  management platform, or application that regularly creates or modifies
  `.aspx` files as part of normal operations. In this case, classification
  requires distinguishing between legitimate file deployments and malicious web
  shell drops, which may need additional context (e.g., correlating with
  deployment windows, CI/CD pipeline activity, or authorized change records).

The distinction matters because it determines whether this layer can function
as an automated detection rule (Suspicious Here) or must serve as a hunt lead
requiring human analysis (Suspicious in Context).

**False Positive Considerations:** Environment-dependent. Low for static
servers; moderate to high for servers with CMS deployments or active
development.

---

### Layer 3 (Tertiary): web.config Creation or Modification

**DDM Operation:** Write Config  
**Telemetry:** Sysmon Event ID 11 (for new web.config creation), File Integrity
Monitoring (for modifications to existing web.config), IIS configuration change
logging

**Procedure Coverage:**

| Procedure      | Covered? | Notes |
|----------------|----------|-------|
| TRR0000.WIN.A  | ❌ No    | Procedure A does not involve web.config manipulation |
| TRR0000.WIN.B  | ❌ No    | Procedure B does not involve web.config manipulation |
| TRR0000.WIN.C  | ✅ Full  | Write Config is the distinguishing prerequisite for Procedure C; covers both the custom handler mapping and inline handler variants |

**Classification:** **Suspicious Here** in most production environments. Changes
to `web.config` files in production IIS servers should be rare and tightly
controlled. The creation of a new `web.config` file in a subdirectory of the
web root is particularly suspicious, as this is a common Procedure C delivery
pattern. Subdirectory `web.config` files cause IIS to dynamically reload
configuration without a server restart, making them immediately effective.

**False Positive Considerations:** Low to moderate. Legitimate `web.config`
changes do occur during application deployments, configuration updates, and
troubleshooting, but these should correlate with authorized change windows. In
environments with mature change management, any `web.config` change outside a
change window can be treated as highly suspicious.

---

### Layer 4 (Supplementary): ASPX Compilation Artifacts

**DDM Operation:** Compile ASPX (sub-operation of Execute Code)  
**Telemetry:** Sysmon Event ID 11 (File Create)  
**Key Fields:** File path matching
`C:\Windows\Microsoft.NET\Framework64\<version>\Temporary ASP.NET Files\`,
file extension `.dll`

**Procedure Coverage:**

| Procedure      | Covered? | Notes |
|----------------|----------|-------|
| TRR0000.WIN.A  | ⚠️ Partial | Only fires for `.aspx` web shells, not `.asp` |
| TRR0000.WIN.B  | ⚠️ Partial | Same limitation — `.aspx` only |
| TRR0000.WIN.C  | ⚠️ Partial | Applies when Procedure C results in `.aspx` execution (inline handlers or custom-mapped extensions processed by ASP.NET) |

**When this fires:** On the first HTTP request to an `.aspx` web shell. The
ASP.NET engine compiles the source into a DLL and stores it in the Temporary
ASP.NET Files directory. This means the artifact appears during execution, not
at the prerequisite stage — it fires even if the web shell file was placed days
or weeks earlier.

**Classification:** **Suspicious in Context.** Every legitimate `.aspx` page
produces the same compilation artifact on its first request. Classification
requires correlating the new DLL with the source file it was compiled from. A
DLL compiled from a recently created or modified `.aspx` file in an unusual
location would be suspicious; a DLL compiled from a long-standing application
page would not.

**Value in layered strategy:** This layer adds detection depth at the execution
stage rather than the prerequisite stage. If an attacker's web shell file
evades Layer 2 (e.g., injected into an existing file, bypassing Sysmon 11), the
compilation artifact still fires when the shell is first triggered. This makes
it a useful supplementary signal, particularly in combination with other layers.

**Limitation:** Classic ASP files (`.asp`) are interpreted directly by the ASP
engine and do not produce compilation artifacts. This layer provides no coverage
for `.asp` web shells.

---

### Layer 5 (Hunt): IIS Log Analysis

**DDM Operation:** Route Request  
**Telemetry:** IIS W3C Logs  
**Key Fields:** Requested URL (cs-uri-stem), HTTP method (cs-method), source
IP (c-ip), response status code (sc-status), response time (time-taken),
user agent (cs(User-Agent))

**Procedure Coverage:**

| Procedure      | Covered? | Notes |
|----------------|----------|-------|
| TRR0000.WIN.A  | ✅ Full  | All HTTP requests to the web shell are logged |
| TRR0000.WIN.B  | ✅ Full  | All HTTP requests to the web shell are logged |
| TRR0000.WIN.C  | ✅ Full  | All HTTP requests are logged (unless triggered by Application Initialization, which generates internal requests that may be logged differently) |

**This is the only telemetry source with 100% identification coverage across
all three procedures.** Every HTTP request routed through IIS generates a W3C
log entry, regardless of how the web shell was deployed or what it does
post-execution. This makes Route Request the theoretical "ideal" detection
point in VanVleet's framework.

**Why it's Layer 5 and not Layer 1:** Despite 100% identification, IIS logs
present a severe classification challenge. A web shell request looks nearly
identical to a legitimate request in W3C logs. The URL, method, status code,
and user agent are all attacker-controlled (tangential), meaning the attacker
can craft requests that blend with normal traffic. Classification requires
looking for anomalous patterns rather than definitive indicators:

- POST requests to files that normally only receive GET requests
- Requests to files in unusual locations (e.g., deep subdirectories, temporary
  upload directories)
- Requests to recently created files (requires correlation with Layer 2)
- Requests from IP addresses not associated with normal user activity
- Single-file access patterns (repeated requests to one specific file from one
  source, with no other page navigation)
- Unusual response sizes or response times that suggest command execution

Because these indicators are probabilistic rather than deterministic, IIS log
analysis is best suited as a **hunt lead** rather than an automated detection
rule. An analyst can investigate suspicious patterns and correlate with other
layers to confirm or dismiss web shell activity. This is consistent with
VanVleet's S3 discussion of threat hunting's relative advantage for situations
where automated classification is not feasible.

**Special case — Procedure B fallback:** For Procedure B (in-process execution
with no process spawn), IIS log analysis is the **primary** detection method
available, since Layers 1, 3, and 4 provide limited or no coverage. This makes
Layer 5 the critical backstop for the hardest-to-detect procedure.

---

## Known Blind Spots

### Blind Spot 1: Procedure B via File Modification

**Scenario:** An attacker injects web shell code into an existing legitimate
`.aspx` page. The web shell uses only .NET APIs (no process spawn).

**What fails:**

- Layer 1 (Process Spawn): No child process to detect
- Layer 2 (File Creation): Sysmon 11 does not fire on file modification
- Layer 3 (web.config): No web.config involvement
- Layer 4 (Compile ASPX): The `.aspx` page already has a compiled DLL; a
  recompilation may occur but would replace an existing DLL rather than creating
  a new one, and the recompilation of a known page is not inherently suspicious
- Layer 5 (IIS Logs): Available but classification is extremely difficult

**Residual detection options:** File Integrity Monitoring that detects content
changes in web-accessible files. SACL auditing (Windows Event 4663) on web root
directories if configured. Behavioral analysis of outbound network connections
or file access from `w3wp.exe` (Sysmon Event 3 for network, Event 4663 for
object access).

**Assessment:** This is the lowest-visibility scenario in the DDM. It should be
documented as a known blind spot for automated detection and addressed through
periodic manual review or FIM-based hunting.

### Blind Spot 2: Procedure C with Application Initialization

**Scenario:** An attacker writes a web.config that configures IIS Application
Initialization to automatically trigger the web shell on app pool recycle or
server reboot. The attacker never sends their own HTTP request.

**What fails:**

- Layer 5 (IIS Logs): The triggering request is generated internally by IIS,
  not by the attacker. It may be logged differently or be harder to distinguish
  from legitimate warmup activity.

**What still works:**

- Layer 3 (web.config): The web.config creation/modification is still
  detectable

**Assessment:** Layer 3 remains effective for this variant. The IIS log
limitation is worth noting but does not represent a full blind spot.

---

## Procedure Coverage Matrix

|                  | Layer 1: Process Spawn | Layer 2: File Creation | Layer 3: web.config | Layer 4: Compile ASPX | Layer 5: IIS Logs |
|------------------|:-----:|:-----:|:-----:|:-----:|:-----:|
| **TRR0000.WIN.A** | ✅    | ⚠️*   | —     | ⚠️**  | ✅ (hunt) |
| **TRR0000.WIN.B** | —     | ⚠️*   | —     | ⚠️**  | ✅ (hunt) |
| **TRR0000.WIN.C** | ⚠️*** | —     | ✅    | ⚠️**  | ✅ (hunt) |

*\* Only covers new file creation, not modification of existing files.*  
*\*\* Only covers `.aspx` files, not `.asp`.*  
*\*\*\* Only when the Procedure C shell spawns a child process.*

---

## Recommended Implementation Priority

1. **Layer 1 — Process Spawn.** Deploy first. Highest fidelity, lowest false
   positive rate, inherently suspicious classification. This should be a
   production detection rule that generates alerts for immediate investigation.

2. **Layer 3 — web.config monitoring.** Deploy second. Low false positive rate
   in most production environments and covers a procedure (C) that Layer 1 may
   miss. Can be a production detection rule with change-window correlation to
   reduce false positives.

3. **Layer 2 — File creation monitoring.** Deploy third. Coverage across all
   procedures at the prerequisite stage, but requires environment-specific
   tuning to manage false positives. May function as a detection rule
   (Suspicious Here environments) or hunt lead (Suspicious in Context
   environments).

4. **Layer 4 — Compile ASPX artifacts.** Deploy as supplementary. Adds
   execution-stage depth, particularly useful when prerequisite-stage detections
   are evaded. Limited to `.aspx` shells. Best used as a corroborating signal
   rather than a standalone rule.

5. **Layer 5 — IIS log analysis.** Implement as a hunt workflow. Critical
   backstop for Procedure B and for any scenario that evades Layers 1–4. Define
   hunt queries for anomalous request patterns and schedule periodic reviews.

---

## Compound Probability Considerations

Following VanVleet's compound probability framework (S4), even incomplete
coverage of this technique contributes meaningfully to the overall detection
mesh. If we estimate that Layers 1 through 3 together cover roughly 2 of 3
procedures with high confidence (~67% identification), that coverage stacks
with detections at other points in the attacker's kill chain (initial access,
lateral movement, privilege escalation, etc.).

VanVleet demonstrates that with even 33% attack surface coverage per tactic and
a 5-step attack path, the probability of an attacker evading all detections
drops to roughly 13%. At 50% coverage, it drops to 3%. Our layered approach for
this single technique pushes our coverage well above 50% of this technique's
attack surface, which means its contribution to the compound probability mesh
is strong — even with the Procedure B blind spot.

The key insight: **do not anguish over the Procedure B gap.** Document it,
pursue FIM and hunt workflows to address it, and then move on to the next
technique. The compound probability math works in the defender's favor across
the full mesh of detections, not at any single technique.

---

## References

- [Technique Analysis and Modeling — VanVleet (A6)](https://medium.com/@vanvleet/technique-analysis-and-modeling-b95f48b0214c)
- [Identifying and Classifying Attack Techniques — VanVleet (S2)](https://medium.com/@vanvleet/identifying-and-classifying-attack-techniques-002c0c4cd595)
- [Compound Probability: You Don't Need 100% Coverage to Win — VanVleet (S4)](https://medium.com/@vanvleet/compound-probability-you-dont-need-100-coverage-to-win-a2e650da21a4)
- [The Threat Detection Balancing Act: Coverage vs Cost — VanVleet (A1)](https://medium.com/@vanvleet/the-threat-detection-balancing-act-coverage-vs-cost-cdb71d21412f)
- [The Relative Strengths of Threat (Detection|Hunting) — VanVleet (S3)](https://medium.com/@vanvleet/the-relative-strengths-of-threat-detection-hunting-777b03a89d15)
