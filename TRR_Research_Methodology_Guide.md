# TRR Research Methodology — A Practical Guide

**Based on:** VanVleet's Detection Engineering Methodology (TIRED Labs)  
**Purpose:** A step-by-step process for researching an attack technique and
producing a submission-quality Technique Research Report (TRR) with Detection
Data Models (DDMs).  
**Audience:** Entry-level detection engineers or anyone new to the methodology.

---

## Before You Start

### What You Need

- A technique to research (e.g., a MITRE ATT&CK ID, a known attack name, or a
  behavior you've observed)
- Access to the [TIRED Labs TRR spec] for format requirements
- Access to the [Arrows App] for building DDMs
- A text editor for your research notes and TRR draft
- Time and patience — depth matters more than speed

### Mindset

The single most important thing to remember: **you are not trying to catalog
tools or commands. You are trying to understand the essential operations that
MUST happen for a technique to work.** Tools change. Commands change. File
names change. The underlying operations do not.

Every time you're about to write something down, ask: "Is this something the
attacker MUST do, or is this something the attacker CHOSE to do?" If they
chose it, it's tangential. If they must do it, it might belong in your model.

---

## Phase 1: Build Your Understanding

**Goal:** Understand the technique well enough to explain it simply and
accurately. Do NOT touch the DDM yet.

### Step 1: Answer the Basic Questions

Write down answers to these questions. If you can't answer one, that's your
first research task.

```
□ What is this technique called?
□ What tactic does it accomplish? (Persistence? Credential Access? etc.)
□ What platform(s) does it affect?
□ What is the attacker trying to achieve?
□ Why do attackers use this technique instead of alternatives?
□ What are the prerequisites? (What must already be true for this to work?)
```

**Checkpoint:** Can you explain this technique to a non-technical person in
2-3 sentences? If not, keep researching.

### Step 2: Understand the Underlying Technology

Before you can model an attack, you need to understand the system being
attacked. This is the part most people skip, and it's why their models have
gaps.

```
□ What system components does this technique interact with?
□ What processes, services, or protocols are involved?
□ How does the legitimate version of this activity work?
□ What security controls exist that this technique exploits or bypasses?
□ What permissions or access does the attacker need?
```

**How to research this:**
1. Start with Microsoft Learn / vendor documentation for the technology
2. Read the MITRE ATT&CK page for the technique
3. Search for conference talks or blog posts from researchers who've analyzed
   the technique (look for names like SpecterOps, Red Canary, CrowdStrike,
   Elastic, Microsoft Threat Intelligence)
4. If the technique involves Windows internals, Sysinternals documentation
   and Mark Russinovich's resources are invaluable

**Checkpoint:** Do you understand WHY the technique works, not just WHAT it
does? Can you trace the path from the attacker's action to the effect on the
system?

### Step 3: Write It Down

Create a research notes file (markdown works great). Document everything you've
learned so far, organized by topic. Include:

- Technique summary
- Architecture of the affected system
- Key components and how they interact
- Security-relevant details (processes, permissions, file paths, APIs)
- References with links for everything you cite

**This file is your working memory.** You'll come back to it constantly. Keep
it updated as you learn more.

**Checkpoint:** Could another researcher read your notes and understand the
technique without needing to do their own research? If not, fill in the gaps.

---

## Phase 2: Build the Detection Data Model

**Goal:** Map out every essential operation in the technique and identify where
those operations can be observed.

### Step 4: Map Your Initial Understanding

Open the [Arrows App] and start placing operations.

**Rules for operations:**
- Each operation is a **circle**
- Name them using **"Action Object"** format (verb + noun):
  Good: "Write File", "Send Request", "Spawn Process"
  Bad: "The attacker uploads a web shell to the server"
- Use **arrows** to show flow from one operation to the next
- Use **downward arrows** for lower layers of abstraction (implementation
  details of the operation above)
- Use **green circles** for source/attacker machine operations
- Use **blue circles** for target machine operations
- Add **tags** for specific details (process names, APIs, file paths, ports)

**Don't worry about getting it perfect.** The whole point of the next step is
to refine it.

**Checkpoint:** Does your diagram have at least the major operations you
currently understand? Are there any you're unsure about? Mark those with "??".

### Step 5: Iterative Deepening (The Most Important Step)

For EVERY operation in your DDM, ask yourself these questions:

```
1. Do I understand what's actually happening here?
   → If no: research deeper, break it into sub-operations

2. What specific processes, APIs, or network connections are involved?
   → If you don't know: add tags with "?" and research

3. Is this ONE operation, or am I summarizing MULTIPLE operations?
   → If summarizing: split it into its component operations

4. Is this operation ESSENTIAL? Could the attacker skip it?
   → If optional: REMOVE IT from the DDM

5. Is this operation IMMUTABLE? Can the attacker change how it works?
   → If attacker-controlled: mark it as tangential or remove it

6. How does this operation cause or lead to the next operation?
   → If you can't explain the connection: there's a gap in your
     understanding. Research it.
```

**Repeat this for every operation until there are no more "??" marks.**

This is where most of your research time will be spent. It's normal for this
step to take hours or even days for a complex technique. Don't rush it.

**Checkpoint:** Can you explain every operation in your DDM in detail? Are
there any question marks left? If yes, keep going.

### Step 6: Classify Every Element

Go through your entire DDM and classify each element:

| Classification | Definition | In DDM? |
|---|---|---|
| **Essential** | Must happen for the technique to work | ✅ Yes |
| **Immutable** | Attacker cannot change this | ✅ Yes |
| **Observable** | Can theoretically be detected | ✅ Yes |
| **Optional** | Can be skipped without breaking the technique | ❌ Remove |
| **Tangential** | Attacker-controlled (tools, filenames, flags) | ❌ Remove |

**Common mistakes at this step:**
- Including specific tool names as operations (tangential)
- Including command-line parameters (tangential)
- Including specific file names the attacker chose (tangential)
- Keeping optional steps because they're "interesting" (remove them — they
  make it harder to identify distinct procedures later)

### Step 7: Add Telemetry

For each remaining operation, identify what could observe it:

```
□ Does this operation generate any Windows Event Log entries?
□ Does Sysmon capture this? (Check the Sysmon event ID list)
□ Would this appear in application-specific logs? (IIS logs, SQL logs, etc.)
□ Would this be visible in network traffic?
□ Would an EDR tool capture this?
□ Is there a file system artifact?
□ Is there a registry artifact?
```

Add telemetry as tags on the relevant operation nodes. If an operation has NO
known telemetry, tag it "No direct telemetry" — that's a detection gap worth
documenting.

**Important:** Put telemetry on the operation it DIRECTLY observes, not on a
nearby operation. Sysmon 1 (Process Create) goes on the "Spawn Process" node,
not on the "Execute Code" node.

### Step 8: Find Alternate Paths

For EVERY operation, ask: **"Is there another way to do this?"**

```
□ Can this operation be accomplished via a different API?
□ Can this operation be accomplished via a different protocol?
□ Can this operation be skipped entirely while still achieving the technique?
□ Can the attacker reach the same outcome through a completely different
  chain of operations?
```

If you find an alternate path:
- Add it to the DDM as a branch
- Follow it through to the end
- Apply Steps 5-7 to the new operations

**Checkpoint:** Have you explored every realistic alternate path? Have you
asked "is there another way?" for every single operation?

---

## Phase 3: Identify Procedures

**Goal:** Determine how many distinct execution paths exist in your DDM.

### Step 9: Trace the Paths

Look at your DDM and trace every possible path from start to finish.

**Key principle:** A procedure is a distinct execution path. Two different
tools that execute the same operations = SAME procedure. Two different
operation paths = DIFFERENT procedures.

For each path:
1. Trace it from the first operation to the last
2. Write down the sequence of operations
3. Compare it to every other path
4. If two paths share every essential operation, they're the same procedure
5. If two paths diverge at any essential operation, they're different
   procedures

### Step 10: Assign Procedure IDs

For each distinct procedure:

```
Format: TRR####.PLATFORM.LETTER
Example: TRR0000.WIN.A

Where:
  TRR#### = TRR ID (placeholder until assigned)
  PLATFORM = WIN, LNX, MAC, AZR, etc.
  LETTER = A, B, C, etc. (one per procedure)
```

Create a procedure table:

```markdown
| ID | Name | Summary |
|----|------|---------|
| TRR0000.WIN.A | Descriptive Name | One-sentence summary |
| TRR0000.WIN.B | Descriptive Name | One-sentence summary |
```

---

## Phase 4: Validate Everything

**Goal:** Make sure your model is complete, accurate, and useful before writing
the TRR.

### Step 11: Run the Checklists

**Completeness Check:**
```
□ All operations in the DDM are essential (none are optional or tangential)
□ All operations are well-understood (no "??" marks remain)
□ All realistic alternate paths have been explored
□ Telemetry has been identified for each operation
□ Procedures are distinct (different essential operations, not just different
  tools)
```

**Accuracy Check:**
```
□ Technical details are correct (verified against documentation)
□ No assumptions are hiding in the model
□ The model matches real-world implementations
□ References are cited for technical claims
□ DDM follows naming and formatting conventions
```

**Utility Check:**
```
□ A detection engineer could build detections from this
□ A red teamer could understand how to execute the technique
□ No environment-specific assumptions are baked in
□ Both common and uncommon procedures are covered
```

If any check fails, go back and fix it before proceeding.

### Step 12: Get a Second Opinion

If possible, have someone else review your DDM and research notes. Fresh eyes
catch things you've become blind to. Ask them:

- "Does this make sense?"
- "Do you see any paths I missed?"
- "Is there anything here that seems wrong or unclear?"

---

## Phase 5: Write the TRR

**Goal:** Produce a submission-quality TRR that follows the TIRED Labs format.

### Step 13: Write the Metadata

```markdown
# Technique Name

## Metadata

| Key          | Value              |
|--------------|--------------------|
| ID           | TRR0000            |
| External IDs | [T####.###]        |
| Tactics      | Tactic Name        |
| Platforms    | Windows            |
| Contributors | Your Name          |
```

Add a **Scope Statement** if your TRR doesn't cover the entire technique
(e.g., only one platform, only one variant). Be explicit about what's in
scope and what's out.

### Step 14: Write the Technique Overview

This is the **leadership-readable summary.** 1-2 paragraphs. No jargon.
Anyone in cybersecurity should be able to understand it.

After reading this section, the reader should know:
- What the technique is
- How it's generally used
- Why adversaries use it

### Step 15: Write the Technical Background

This is the **bulk of the report.** It should contain everything a reader
needs to understand the technique without going to external sources.

Use subheadings. Cover:
- The technology being abused (architecture, components, protocols)
- How the legitimate system works
- What security controls exist
- Why the technique is effective
- Any technical details common to multiple procedures

**Important:** This section does NOT contain execution steps. Those go in the
procedure narratives.

### Step 16: Write the Procedure Narratives

For each procedure, write a **narrative** (not a step-by-step list). Cover:
- Prerequisites
- How the execution works (trace through the DDM in prose)
- What makes this procedure distinct
- Key detection opportunities
- Any variations or edge cases

After each narrative, include:
- The DDM image (exported from Arrows app)
- A short paragraph describing what the DDM shows, calling out interesting
  nodes, detection opportunities, and gaps

### Step 17: Complete the Remaining Sections

```markdown
## Available Emulation Tests

| ID | Link |
|----|------|
| TRR0000.WIN.A | [Link if known] |

## References

- [Reference Name]: URL
```

### Step 18: Final Review

Read the entire TRR from start to finish as if you've never seen it before.
Ask yourself:

```
□ Is the Technique Overview clear enough to email to leadership?
□ Is the Technical Background complete enough to stand alone?
□ Are the procedure narratives accurate and match the DDMs?
□ Are all references cited?
□ Does the format match existing TRRs in the repository?
□ Would I be confident submitting this?
```

---

## Quick Reference: Common Pitfalls

| Pitfall | How to Avoid It |
|---------|----------------|
| **Tool-focused analysis** | Ask "what operation is this tool performing?" and model the operation, not the tool |
| **Including optional operations** | For every operation ask "can the attacker skip this and still succeed?" If yes, remove it |
| **Tangential elements in DDM** | If the attacker controls it (filenames, flags, tools), it's tangential — don't model it |
| **Incomplete alternate paths** | For every operation ask "is there another way to do this?" |
| **Assumptions hiding as facts** | If you can't cite a source for a technical claim, it might be an assumption. Verify it. |
| **Rushing to the TRR** | The DDM must be solid before you write. A good DDM makes the TRR easy. A bad DDM makes it wrong. |
| **Confusing procedures** | Same operations + different tools = same procedure. Different operations = different procedures. |
| **Skipping the technology research** | You can't model what you don't understand. Phase 1 is the foundation for everything. |

---

## Quick Reference: DDM Conventions

| Element | Convention |
|---------|-----------|
| Operations | Circles with "Action Object" naming |
| Flow | Horizontal arrows (left to right) |
| Abstraction layers | Downward arrows (higher to lower) |
| Source machine ops | Green circles |
| Target machine ops | Blue circles |
| Shared ops | Black circles |
| Details | Tags (process names, APIs, file paths, etc.) |
| Telemetry | Tags on the operation they observe |
| Unknowns | "??" marks (must be resolved before finalizing) |
| Branch points | Multiple arrows leaving one operation |

---

## Quick Reference: Classification Rules

```
ESSENTIAL + IMMUTABLE + OBSERVABLE = Include in DDM
ESSENTIAL + IMMUTABLE + NOT Observable = Include (and note the gap)
OPTIONAL (any combination) = Exclude from DDM
TANGENTIAL (attacker-controlled) = Exclude from DDM
```

---

## References for the Methodology

- [Improving Threat Identification with Detection Modeling — VanVleet]:
  https://medium.com/@vanvleet/improving-threat-identification-with-detection-data-models-1cad2f8ce051
- [Technique Analysis and Modeling — VanVleet]:
  https://medium.com/@vanvleet/technique-analysis-and-modeling-b95f48b0214c
- [Technique Research Reports: Capturing and Sharing Threat Research — VanVleet]:
  https://medium.com/@vanvleet/technique-research-reports-capturing-and-sharing-threat-research-9512f36dcf5c
- [What is a Procedure? — Jared Atkinson]:
  https://posts.specterops.io/on-detection-tactical-to-function-810c14798f63
- [Thoughts on Detection — Jared Atkinson]:
  https://posts.specterops.io/thoughts-on-detection-3c5cab66f511
- [TIRED Labs TRR Specification]:
  https://library.tired-labs.org
- [TIRED Labs TRR Library]:
  https://library.tired-labs.org
- [Arrows App]:
  https://arrows.app/

[TIRED Labs TRR spec]: https://library.tired-labs.org
[Arrows App]: https://arrows.app/
