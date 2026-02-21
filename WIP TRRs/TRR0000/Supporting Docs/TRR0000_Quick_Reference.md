# TRR0000 Quick Reference

## 30-Second Pitch

File-based web shell execution on IIS. Three distinct procedures, not just the
obvious cmd.exe spawn. Full DDM with telemetry mapping. Lab-validated. Honest
about blind spots. Any detection engineer can pick it up and build detections
for their environment.

---

## What Are the Two Deliverables?

### TRR (Technique Research Report)
- **Environment-independent** research document
- Contains: scoping, technical background, procedures, DDMs, detection
  considerations, blind spots
- **Lossless** — preserves all reasoning so any DE can build detections
- A detection query is **lossy** — it bakes in SIEM, log source, tuning
  decisions and throws away the "why"

### DDM (Detection Data Model)
- Diagram of **essential, immutable, observable** operations
- Structured analytic technique (borrowed from intel analysis)
- Forces you to verify understanding instead of assuming
- Telemetry tagged on the specific operation each source observes
- **Master DDM** = all paths in black; **per-procedure exports** = active
  path in red arrows

---

## The DDM Inclusion Test

> Does this operation belong in the model?

| Test | Question | If No... |
|------|----------|----------|
| **Essential** | Must this happen for the technique to work? | It's optional — remove it |
| **Immutable** | Can the attacker change or avoid this? | It's tangential — remove it |
| **Observable** | Can any telemetry source see this? | Note the gap, keep if E+I pass |

**All three must pass.** Fail any one → doesn't belong.

### Tangential Examples (fails immutable)
- Specific tool (China Chopper, custom shell)
- Filename, extension choice, delivery method
- Specific .NET APIs called (Proc B)
- Encoding, obfuscation, language variant

---

## IIS Pipeline — The Shared Backbone

```
HTTP.sys (kernel) → App Pool → w3wp.exe → Handler Mapping → Execute Code
```

- Every web shell on IIS transits this pipeline
- HTTP.sys is below most telemetry — can't detect there
- App pool identity = web shell's permissions (default: low-privilege
  `IIS AppPool\DefaultAppPool`)
- w3wp.exe is **the** process to watch

---

## Three Procedures at a Glance

| | A: OS Command | B: In-Process | C: web.config |
|---|---|---|---|
| **One-liner** | Shell spawns cmd.exe | Shell uses .NET APIs in-process | web.config changes handler mappings |
| **Distinguishing op** | Process Spawn | Call .NET API | Write Config |
| **Best detection** | w3wp.exe → cmd.exe (Sysmon 1) | File creation only (Sysmon 11) | .compiled for non-standard ext (Sysmon 11) |
| **Fidelity** | Very High | Low | Very High |
| **Blind spot?** | No | **Yes — biggest gap** | Partial (inline handler variant) |

---

## Procedure A: OS Command Execution

**Chain:** Create File → Send HTTP → Route Request → Match Handler → Execute
Code → **Process Spawn**

**Key facts:**
- w3wp.exe → cmd.exe / powershell.exe is rarely legitimate in production
- Sysmon 1 and Win 4688 both capture parent-child relationship
- Lab confirmed: full command line visible (`cmd.exe /c whoami`)
- .aspx shells also trigger csc.exe compilation (sub-operation)
- .asp shells are interpreted directly — no compilation artifacts

**If asked "what about tool X?":** The tool is tangential. Any shell that spawns
cmd.exe from w3wp.exe is this procedure. Same operations = same procedure.

---

## Procedure B: In-Process Execution

**Chain:** Create File → Send HTTP → Route Request → Match Handler → Execute
Code → **Call .NET API**

**Key facts:**
- No child process ever spawns — w3wp.exe looks normal
- Uses System.IO, System.Net, System.Data, etc. — all in-process
- Specific APIs are tangential (attacker-controlled, infinite variety)
- Lab confirmed: **zero Sysmon 1 events** — blind spot validated

**Why it's hard to detect:**
- No process spawn → no parent-child alert
- SACL tested: Proc B does **reads only** → Write audit doesn't fire
- ReadData audit would fire but generates massive noise in production
- Residual: Sysmon 11 (new file only), IIS logs (weak classification),
  compilation artifacts (first access only)

**Worst case:** Code injected into existing .aspx page + .NET APIs only =
no Sysmon 11, no process spawn, no useful SACL, no distinguishing compilation.
Only FIM and IIS log analysis remain.

---

## Procedure C: web.config Manipulation

**Chain:** **Write Config** → (opt. Create File) → Send HTTP → Route Request →
Match Handler → Execute Code → (Proc A or B ending)

**Why it's a separate procedure (expect this question):**
1. Introduces Write Config — an essential operation that doesn't exist in A/B
2. Removes the constraint that extension must match a default handler
3. Inline IHttpHandler variant: web.config IS the shell — no separate file

**Two variants:**

| | Custom Handler Mapping | Inline IHttpHandler |
|---|---|---|
| Files needed | web.config + shell file (.txt, .jpg, etc.) | web.config only |
| Config elements | `<handlers>` AND `<buildProviders>` | `<handlers>` with inline code |
| Scope constraint | buildProviders must be at IIS Application level | No restriction |
| Unique artifact | `.compiled` preserving original extension | None specific |

**Lab discovery:** Initial attempts returned HTTP 500. buildProviders element is
required AND must be at IIS Application level. Directories had to be converted
to IIS Applications. This refined the TRR.

**High-fidelity detection:** `readme.txt.cdcab7d2.compiled` — ASP.NET should
**never** compile .txt/.jpg/.info files. Zero false positives.

---

## Detection Coverage Matrix

| Detection | Telemetry | Fidelity | A | B | C |
|-----------|-----------|----------|---|---|---|
| w3wp.exe → cmd/powershell | Sysmon 1 / 4688 | **Very High** | ✅ | ❌ | ⚠️ |
| Non-standard ext .compiled | Sysmon 11 | **Very High** | — | — | ✅ |
| w3wp.exe → csc.exe | Sysmon 1 | **High** | ✅ | ✅ | ✅ |
| New web.config in web dir | Sysmon 11 | **High** | — | — | ✅ |
| New .aspx/.asp in web root | Sysmon 11 | **Medium** | ✅ | ✅ | — |
| BAM registry entries | Sysmon 13 | **Medium** | ✅ | — | ✅ |
| IIS log anomalies | W3C logs | **Low-Med** | ✅ | ✅ | ✅ |

⚠️ = only when shell spawns a process (Proc C can end like A or B)

**No single detection covers all three procedures.**

---

## ASP vs. ASP.NET — Why It Matters

| | Classic ASP (.asp) | ASP.NET (.aspx) |
|---|---|---|
| Engine | asp.dll (interpreted) | Compiled to DLL |
| Compilation | None | csc.exe spawn on .NET 4.8 |
| Disk artifacts | Original file only | .compiled, .dll, .cs, .cmdline |
| Temp ASP.NET Files | No | Yes |
| Detection implications | Fewer artifacts | More detection surface |

csc.exe compilation, .compiled metadata, Temp ASP.NET Files subdirectories
— all .aspx only. A strategy relying solely on compilation telemetry misses
.asp shells entirely.

---

## Forensic Artifacts

**BAM Registry:** w3wp.exe → cmd.exe writes to
`HKLM\...\bam\State\UserSettings\{SID}\`. Persists across reboots. Proves a
specific exe ran under the IIS app pool identity even after logs are cleared.

**IIS Log Timing:** First request to dynamically compiled page shows ~650ms
response time vs. single-digit ms for subsequent requests. First-seen URI with
anomalously high response time = likely new shell.

**500→200 in IIS Logs:** Attacker iterating on web.config config — failed
attempts (500) followed by success (200) is a forensic indicator.

---

## Scoping — What's In and Out

**In scope:** File-based web shells on IIS, Windows, ASP/ASP.NET pipeline

**Out of scope:**

| Excluded | Why |
|----------|-----|
| Fileless/memory web shells | Different essential operations |
| ASP.NET Core on IIS | Different execution model (Kestrel proxy) |
| PHP on IIS (FastCGI) | Different execution model (php-cgi.exe) |
| Non-Windows platforms | Different architecture entirely |
| SSI (ssinc.dll) | Same essential ops as A/B — not a separate procedure |

---

## Methodology Questions

**Q: Why this technique first?**
Well-documented enough to validate against, but most write-ups only cover Proc A.
Forced deep IIS internals work. Good proving ground for the full methodology.

**Q: How'd you build the DDM?**
Started with the IIS pipeline (shared backbone). Mapped each operation. Asked
"what are the possible paths?" at each step. Branch after Execute Code emerged
(process spawn vs. in-process). Prerequisites modeled separately because file
delivery can happen days before first request.

**Q: How'd you decide three procedures?**
"Do the essential operations change?" A→B: post-execution op changes. A/B→C:
Write Config introduces a new essential op AND changes what Match Handler
operates against. Inline variant eliminates the script file prerequisite
entirely.

**Q: Why no detection queries in the TRR?**
By design. Queries are environment-specific (SIEM, log source, noise). The TRR
gives you the research to build the right query for YOUR environment.

---

## Curveball Questions

**Q: How would you evade your own detections?**
Proc B via file modification into existing .aspx, .NET APIs only. Documented
blind spot. No process spawn, no Sysmon 11, no distinguishing compilation.
Need FIM or SACL on web root to catch it.

**Q: Could Proc B be split further by API type?**
No. API choice is tangential (attacker-controlled). What's essential is
in-process execution without a child process. System.IO vs. System.Net is an
implementation detail.

**Q: What about fileless web shells?**
Out of scope — different essential operations (no file on disk, different
injection mechanism). Separate TRR.

**Q: How's this different from ATT&CK T1505.003?**
ATT&CK describes the technique high-level and lists tools. Doesn't break into
procedures with operation-level models. The TRR identifies essential operations,
maps them, shows where detection is strong and where it's weak. ATT&CK =
taxonomy. TRR = analysis.

**Q: Difference from a threat intel report?**
Threat intel = event-focused (who used what tool in what campaign). TRR =
technique-focused (how does it work at the operation level regardless of actor).

---

## Lab Validation Highlights

| Finding | Significance |
|---------|-------------|
| Proc A: Full parent-child chain in Sysmon 1 + 4688 | Strongest single detection point confirmed |
| Proc B: Zero Sysmon 1 events | Blind spot empirically validated |
| Proc B: SACL didn't fire (reads only) | ReadData audit = too noisy for production |
| Proc C: Initial 500 errors | buildProviders requirement discovered; refined TRR |
| Proc C: `readme.txt.cdcab7d2.compiled` | Non-standard ext compilation = zero false positives |
| Proc C: buildProviders scope constraint | Must be at IIS Application level — narrows attack surface |
| IIS logs: 500→200 transition | Forensic indicator of attacker config iteration |
| First-request timing: ~650ms vs. <5ms | Compilation overhead visible in logs |

---

## Five Anchors — Always Come Back To These

1. **DDM Inclusion Test** — Essential + Immutable + Observable. Apply it to
   anything.
2. **Procedures vs. Instances** — Different essential ops = different procedure.
   Different tools, same ops = same procedure.
3. **Lossless vs. Lossy** — TRR preserves everything. Query discards context.
4. **Know Your Blind Spots** — Proc B via file mod is the gap. Saying so is a
   strength.
5. **The IIS Pipeline** — HTTP.sys → app pool → w3wp.exe → handler → execute.
   You understand the technology, not just the attack.
