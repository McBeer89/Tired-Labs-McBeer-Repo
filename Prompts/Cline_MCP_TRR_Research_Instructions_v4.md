# TRR & DDM Research Protocol for Cline
*Based on the TIRED Labs methodology by Andrew VanVleet*

---

## Session Startup (RUN THIS BEFORE ANYTHING ELSE — EVERY SESSION)

You have no memory of previous sessions. Every chat starts blank. The file system is your memory. Before doing anything else, execute this startup routine in order:

**Step 1 — Scan for active TRR work**

Use `filesystem` to list the contents of `./research_notes/` and `./TRRs/` and `./DDMs/`.

If files exist:
- Read every file in `./research_notes/` that matches the current TRR ID
- Read the current TRR draft in `./TRRs/` if one exists
- Build a mental summary of: what technique is being researched, what phase was last completed, what files exist, and what unresolved `[?]` markers remain

If no files exist:
- This is a new TRR. Proceed to Phase 1: Strategic Planning.

**Step 2 — Report current state to the user**

Before doing anything else, output a structured status report in this format:

```
SESSION STARTUP REPORT
======================
TRR ID:          [e.g., TRR0001 or "Not yet assigned"]
Technique:       [e.g., T1059.001 - PowerShell]
Platform:        [e.g., Windows]
Last Completed:  [e.g., Phase 2 — Technical Background]
Next Phase:      [e.g., Phase 3 — DDM Construction]
Files Found:     [list all files in research_notes/ for this TRR]
Open Questions:  [any [?] markers found in existing files]
Ready to proceed: [Yes / No — if No, explain what is missing]
```

**Step 3 — Wait for user confirmation**

Do not proceed to any research phase until the user confirms the status report is accurate and gives the go-ahead. The user may correct the state, redirect to a different TRR, or provide additional context that is not in the files.

**Rule**: This startup routine is mandatory. Even if the user's first message jumps straight to a task, run the startup routine first. A session that skips this will be working blind from prior phases.

---

## Phase 1: Strategic Planning (ALWAYS START HERE FOR NEW TRRs)

Before executing any command or writing any content, use the `sequential_thinking` tool to:

1. Identify the ATT&CK technique ID and name being researched.
2. State the platform(s) in scope (e.g., Windows, Linux, macOS, Azure).
3. Outline a research hypothesis — what procedures do you expect to find, and why?
4. List the phases you plan to execute in this session.

**Rule**: Do not write a single line of TRR content until the hypothesis and plan are documented. This prevents scope creep and tool-focused analysis.

---

## Phase 2: Technique Research (Phase 1 of TRR Methodology)

### Step 1 — High-Level Understanding
Use `fetch` to retrieve:
- The official ATT&CK technique page: `https://attack.mitre.org/techniques/TXXXX/`
- Any relevant sub-technique pages
- The TIRED Labs library for related TRRs: `https://library.tired-labs.org`

**Write to file**: `./research_notes/TRRXXXX_phase1_overview.md`

Document:
- Technique name, ID, tactic(s), and platform(s)
- Attacker objective (what does success look like?)
- Why attackers use this technique (what advantage does it provide?)

**Stop check**: Can you explain this technique in 2–3 sentences without referencing a specific tool? If not, research further before proceeding.

### Step 2 — Technical Background
Use `fetch` to retrieve Microsoft documentation, RFCs, or relevant technical references for the underlying technology (e.g., Windows APIs, protocols, services involved).

**Write to file**: `./research_notes/TRRXXXX_phase1_technical_background.md`

Document:
- System components, APIs, or protocols involved
- Prerequisites the attacker must satisfy
- Security controls that exist (and that this technique bypasses or abuses)
- Any relevant Windows internals or OS-level mechanics

**Stop check**: Do you understand the *why* behind how this technique works? If there are open questions, mark them with `[?]` and research them before moving on.

---

## Phase 3: Detection Data Model (DDM) Construction

### Step 3 — Initial Operation Mapping
Begin building the DDM. Use `filesystem` to create:

`./research_notes/TRRXXXX_ddm_draft.md`

Rules for operations:
- Name every operation as **Action Object** (e.g., "Open Process Handle", "Write File to Disk", "Call API")
- Classify each operation:
  - `[E]` Essential — must happen for the technique to work
  - `[I]` Immutable — cannot be changed by the attacker
  - `[O]` Observable — can be detected through some telemetry
- Do **not** include tool names, command-line flags, or file names — these are attacker-controlled (tangential) and do not belong in the DDM

**Color convention for DDM JSON exports** (Arrows.app):
- Green nodes: source/attacker machine operations
- Blue nodes: target machine operations
- Black: shared or ambiguous

### Step 4 — Iterative Deepening
For every operation in the current DDM, ask:

1. Do I fully understand what is happening here?
2. Does this operation summarize multiple sub-operations that should be split out?
3. Is this operation truly essential, or could the attacker skip it?
4. What causes this operation to occur, and what does it cause next?

If any answer is uncertain, mark the operation `[?]`, research deeper using `fetch`, and return to resolve it before continuing.

**Do not proceed with unresolved question marks.**

### Step 5 — Telemetry Identification
For each essential operation, document:
- Available telemetry sources (Sysmon event IDs, Windows Event Log channels, ETW providers, IIS logs, network captures, etc.)
- Whether the telemetry is commonly available or environment-specific
- Which side of the transaction the telemetry lives on (attacker vs. target)

**Write to file**: `./research_notes/TRRXXXX_telemetry_map.md`

**IIS-specific reminder**: IIS W3C logs belong on the *server/target side*, not the attacker side. Place telemetry annotations on the correct node in the DDM.

### Step 6 — Alternate Path Discovery
For each operation, ask:
- Is there another API, protocol, or mechanism that accomplishes the same thing?
- Can this operation be bypassed entirely?

If alternate paths exist, add branches to the DDM. Each unique execution path from start to finish is a candidate procedure.

---

## Phase 4: Procedure Identification

### Step 7 — Trace and Name Distinct Procedures
Examine the completed DDM and trace every unique path from start to finish.

Rules:
- Paths that diverge at any point = distinct procedures, even if they converge later
- Different tools executing the same operations = the *same* procedure
- Different operation paths = different procedures

Assign IDs using the convention: `TRRXXXX.PLATFORM.A`, `.B`, `.C`, etc.

**Write to file**: `./research_notes/TRRXXXX_procedures.md`

Include a procedure table:

```markdown
| ID               | Name                        | Summary                                      |
|------------------|-----------------------------|----------------------------------------------|
| TRRXXXX.WIN.A    | [Descriptive procedure name] | [One sentence summary of the unique path]   |
| TRRXXXX.WIN.B    | [Descriptive procedure name] | [One sentence summary of the unique path]   |
```

### Step 8 — Validate the Model
Before writing any TRR prose, answer these validation questions:

1. Can an attacker execute this technique using *only* the operations in the DDM?
2. Are all operations essential — could any be skipped?
3. Does the model cover the known real-world tooling and methods for this technique?
4. Are there any tangential elements (tool names, flags, file paths) that snuck in?
5. Does the model match real-world implementations?

If the answer to any question is "no," revise the model before proceeding.

---

## Phase 5: TRR Documentation

### Step 9 — Write Procedure Descriptions
For each procedure, write a narrative description (not a numbered step list) that covers:
- Prerequisites
- Execution mechanics
- Why it works (the underlying technical reason)
- Any notable variations or edge cases

**Quality check**: Could a detection engineer build a detection from this? Could a red teamer execute it? If not, go deeper.

### Step 10 — Assemble the Full TRR
Use `filesystem` to write the completed TRR to:

`./TRRs/TRRXXXX_TXXXX_Technique_Name.md`

Follow this structure exactly:

```
1. Metadata
   - TRR ID, external mappings (ATT&CK, etc.), tactics, platforms, contributors

2. Technique Overview
   - Executive summary accessible to non-technical readers
   - What, how, and why

3. Technical Background
   - Foundational knowledge sufficient to stand alone
   - Relevant technologies, APIs, services
   - Security controls involved

4. Procedures
   - Procedure table with IDs
   - For each procedure: narrative description + DDM diagram

5. Available Emulation Tests
   - Links to Atomic Red Team tests or equivalent

6. References
   - All sources used + additional reading
```

---

## File & Directory Structure

```
./research_notes/
    TRRXXXX_phase1_overview.md
    TRRXXXX_phase1_technical_background.md
    TRRXXXX_ddm_draft.md
    TRRXXXX_telemetry_map.md
    TRRXXXX_procedures.md

./TRRs/
    TRRXXXX_TXXXX_Technique_Name.md

./DDMs/
    TRRXXXX_ddm_master.json         ← Full DDM (Arrows.app format)
    TRRXXXX_ddm_proc_A.json         ← Procedure-specific DDM
    TRRXXXX_ddm_proc_B.json
```

---

## Version Control — Git Tools

All TRR work is committed to the following repository:

```
https://github.com/McBeer89/Tired-Labs-McBeer-Repo.git
```

### Commit Rules

Use `git_tools` to commit after completing each phase. Do not batch multiple phases into one commit. TRRs are versioned research artifacts — each commit should represent a discrete, reviewable unit of work.

**Commit message convention:**

```
TRR####: [Phase] — [brief description]

Examples:
TRR0001: Phase 1 — Initial technique overview and technical background
TRR0001: Phase 2 — DDM draft with telemetry map
TRR0001: Phase 3 — Procedures identified (WIN.A, WIN.B)
TRR0001: Phase 4 — DDM validated, tangential elements removed
TRR0001: Phase 5 — TRR document complete
TRR0001: DDM — Master and per-procedure exports added
```

### What to Commit and When

| Trigger | Files to Commit |
|---|---|
| After Phase 2 (research complete) | `research_notes/TRRXXXX_phase1_*.md` |
| After Phase 3 (DDM draft complete) | `research_notes/TRRXXXX_ddm_draft.md`, `TRRXXXX_telemetry_map.md` |
| After Phase 4 (procedures identified) | `research_notes/TRRXXXX_procedures.md` |
| After Phase 4 (DDM validated) | `DDMs/TRRXXXX_ddm_master.json` |
| After Phase 5 (TRR complete) | `TRRs/TRRXXXX_TXXXX_Technique_Name.md` |
| After per-procedure DDM exports | `DDMs/TRRXXXX_ddm_proc_*.json` |

**Rule**: Never commit files with unresolved `[?]` markers. If a question mark remains, it means the phase is not complete.

---

## General Principles

- **No tool-focused analysis**: Never write "Mimikatz does X." Write "Reading process memory of LSASS.exe accomplishes X." Tools are instances; procedures are recipes.
- **No assumptions**: If you are uncertain whether an operation is essential or how a mechanism works, mark it `[?]` and research it. Do not guess.
- **No hallucinations**: If `fetch` returns no results, document the intelligence gap. Do not invent data.
- **Essential operations only**: Tangential, attacker-controlled elements (tool names, file names, command-line arguments) do not belong in a DDM.
- **Least privilege on filesystem**: Only read/write to the directories listed above.
- **Validate before advancing**: Every phase ends with an explicit stop check. Do not skip them.
- **Commit after every phase**: TRRs are versioned artifacts. Use `git_tools` with descriptive commit messages. Never commit with unresolved `[?]` markers.
