# CTI AI-Assisted Workflow Guide

## What This Is

This guide describes a structured workflow for using AI assistants in the CTI intelligence production pipeline. It covers three stages — requirements formalization, research base construction, and derivative production — each with a dedicated prompt and explicit human checkpoints.

The workflow is platform-agnostic. The prompts work with any capable AI assistant (Claude, ChatGPT, Copilot, Gemini, or others). The design does not depend on any platform-specific feature.

## What AI Does vs. What the Analyst Does

This is the most important section in this document.

### AI Accelerates

- **Structuring raw input.** The analyst provides messy notes from a consumer meeting; AI helps organize them into the IR/PIR hierarchy format.
- **Extracting claims from source material.** The analyst provides a vendor report or advisory; AI helps pull out the factual claims and organize them.
- **Drafting prose.** AI writes initial drafts of research base entries, key judgments, and derivative sections — all subject to analyst review and revision.
- **Formatting and consistency.** Tables, ATT&CK mappings, telemetry labels, structural templates — mechanical formatting work.
- **Identifying structural gaps.** AI can flag missing elements: "Your research base has no competing hypotheses section" or "This PIR has no collection sources assigned."

### The Analyst Decides

- **What the organization needs to know.** Intelligence requirements come from consumer conversations. AI was not in the room. The analyst provides the raw input; AI helps structure it, but the requirements themselves are human-originated.
- **Whether a claim is relevant (Gate 3).** Relevance is judgment about what matters to *this organization* against *this requirement*. AI doesn't know the organization's threat profile, technology stack, or business context well enough to make this call.
- **What confidence level to assign and why (Gate 4).** Confidence is analytical judgment about source quality, corroboration, and gaps. AI can suggest, but the analyst must evaluate and own the rating.
- **Whether something is a fact, assessment, or assumption (Gate 5).** This requires the analyst to examine their own reasoning — specifically whether they're stating something verifiable, making an analytical judgment, or treating an unverified belief as true.
- **What the consumer needs.** The derivative inclusion test ("does this help this consumer make this decision?") requires knowing the consumer's role, responsibilities, and decision context. AI doesn't attend staff meetings.
- **What to cut.** The hardest editorial decision in intelligence writing is what to leave out. AI defaults to inclusion. The analyst must enforce exclusion.

### The Rule

**If the analyst could be replaced by a copy-paste into the AI prompt and a copy-paste out, the workflow has failed.** Every stage has checkpoints where the analyst must provide input that requires domain knowledge, organizational context, or analytical judgment. If the analyst is approving every AI suggestion without modification, they are not doing analysis — they are rubber-stamping.

---

## Workflow Overview

The pipeline has three stages, each with its own prompt. The output of each stage feeds the next.

```
Stage 1                    Stage 2                    Stage 3
Requirements &         →   Research Base           →   Derivative
Collection                 Construction                Production
(Prompt 1)                 (Prompt 2)                  (Prompt 3)

Input: Consumer            Input: Source material      Input: Completed
meeting notes OR           (reports, advisories,       research base +
analyst knowledge          ISAC alerts, etc.)          derivative type
of consumers

Human checkpoints:         Human checkpoints:          Human checkpoints:
- Validate each IR         - Gate 3 (Relevance)        - Confirm audience
- Validate each PIR        - Gate 4 (Confidence)       - Confirm question
- Confirm collection       - Gate 5 (Fact/Assess/      - Validate filtering
  sources                    Assumption)                 decisions
- Confirm gap register     - Structural gate review    - Review before
                                                         distribution

Output: Structured         Output: Structured          Output: Audience-
requirements doc           research base with          specific derivative
with collection            key judgments               document
matrix
```

### Stage Dependencies

- **Stage 2 requires Stage 1.** The research base is built against defined PIRs. Without requirements, the analyst has no filter for what's relevant — which is exactly the problem the framework solves.
- **Stage 3 requires Stage 2.** Derivatives are produced from the research base. Without a quality-gated research base, the derivative is just reformatted raw research — which is exactly the problem the framework solves.
- **Skipping stages reproduces the original problem.** If an analyst jumps straight to Stage 3 with raw source material and no requirements or gates, the output is an AI-generated report with no analytical rigor. The stages exist to prevent this.

---

## Prompt Design Principles

### Hard Stops

Each prompt includes explicit hard stops — points where the AI must pause and wait for analyst input before continuing. These are not suggestions. The AI is instructed not to proceed past a hard stop until the analyst provides the required input.

Hard stops exist at every point where the analyst must exercise judgment:
- "Is this requirement actually what the consumer asked for?"
- "Is this claim relevant to our specific intelligence requirement?"
- "What is your confidence level, and what supports it?"
- "Is this a fact, an assessment, or an assumption?"
- "Does this section help the consumer make their specific decision?"

### Progressive Construction

Each prompt builds output incrementally, not all at once. The AI does not generate a complete document and hand it to the analyst for review. Instead, it constructs the output section by section, with the analyst validating each section before the next one begins. This prevents the "wall of text" problem where the analyst receives a finished product and rubber-stamps it because revising 15 pages feels like starting over.

### Analyst-Originated Input

Every prompt begins by requiring the analyst to provide something AI cannot generate: raw notes from a consumer meeting, a specific source document, or working knowledge of their consumers and organization. When formal consumer meetings aren't available, the requirements prompt (Prompt 1) offers a guided elicitation path — but the analyst still provides all the substance. The AI asks structured questions; the analyst answers from their domain knowledge. If the analyst has truly nothing to provide — no consumer context, no organizational knowledge — the prompt cannot proceed. This prevents the "empty prompt" pattern where the analyst types a topic and expects the AI to produce intelligence from nothing.

### Explicit Provenance

Every claim, judgment, and recommendation in the output is traceable to either a source document (provided by the analyst) or an analyst decision (made at a hard stop). Nothing in the output should be untraceable — if a reviewer asks "where did this come from?" the answer is always either "this source" or "the analyst decided this at this checkpoint."

---

## When to Use Each Prompt

| Situation | Prompt | Prerequisites |
|---|---|---|
| Starting a new topic with consumer input available | Prompt 1 (path a) → 2 → 3 | Consumer meeting notes, emails, or Slack messages |
| Starting a new topic without formal consumer meetings | Prompt 1 (path b) → 2 → 3 | Analyst's working knowledge of consumers and organization |
| Updating an existing research base with new sources | Prompt 2 | Existing requirements; new source material |
| Producing a new derivative from an existing research base | Prompt 3 | Completed research base |
| Quarterly PIR review | Prompt 1 | Previous requirements doc; consumer feedback |
| Responding to an ad-hoc SIR | Prompt 2 → 3 | Defined SIR; source material; target consumer |

---

## Quality Assurance

### The Senior Analyst's Role

The senior analyst (team lead, reviewer) reviews output at two points:
1. **After Stage 2** — Is the research base analytically sound? Key judgments separated from evidence? Competing hypotheses? Confidence levels justified? Gaps documented?
2. **After Stage 3** — Does the derivative answer the consumer's question and only that question? Is it filtered correctly? Is it concise enough?

The reviewer does not review Stage 1 output in detail unless requirements are being established for the first time. Once requirements are set, they change semi-annually (IRs) or quarterly (PIRs).

### Red Flags

Signs that the workflow is being misused:
- **Every gate is approved without modification.** If the analyst never disagrees with the AI's suggestion, they're not applying judgment.
- **No claims are cut for relevance.** If everything the AI extracts passes Gate 3, the analyst isn't filtering.
- **All confidence levels are "Moderate."** If nothing is Low or High, the analyst is defaulting rather than evaluating.
- **No assumptions are identified.** Every research base has assumptions. If Gate 5 never surfaces one, the analyst isn't looking.
- **Derivatives are as long as the research base.** If the derivative isn't substantially shorter than the source material, the inclusion test isn't being applied.

---

## The Analyst's Own Files: AI Is a Session Tool, Not a Knowledge Base

AI assistants operate in sessions. When the conversation ends, the context is gone. Some platforms offer project folders or memory systems, but these are supplementary features — not reliable long-term storage, not portable across platforms, and not something every team member can access.

The analyst must maintain their own reference files outside the AI. These files serve three purposes: they persist between sessions, they're shareable with the team, and they provide the input that makes AI sessions productive rather than cold-start.

### What the Analyst Should Maintain

**Requirements Document (from Prompt 1).** The finalized IR/PIR hierarchy, collection matrix, cadence schedule, and gap register. This is the team's standing reference — it tells every analyst what to look for and where. It gets updated semi-annually (IRs) and quarterly (PIRs). Save it as a living document the team can access.

**Research Bases (from Prompt 2).** Each completed research base — one per topic or PIR cluster — with full gate metadata, key judgments, gaps, and assumptions. These are the source layer. They accumulate over time as new sources are processed. When starting a new AI session to add sources to an existing research base, the analyst pastes or uploads the current version so the AI has context. Without the file, the AI starts from zero.

**Completed Derivatives (from Prompt 3).** Each derivative produced, filed by type and date. These are the team's deliverable archive. They also serve as templates — when producing the next quarter's Detection Brief, the analyst can reference the previous one for format consistency.

**Source Library.** The raw source material the analyst has collected — vendor reports, CISA advisories, ISAC alerts, news articles, internal incident summaries. Organized by PIR or topic. When starting a Prompt 2 session, the analyst pulls from this library rather than searching from scratch. This is the analyst's collection, not the AI's.

**Threat Actor / Topic Folders.** Running files on threat actors, vulnerability clusters, or campaign tracking that the analyst updates as new information arrives. These don't have to follow the formal research base structure — they're working notes. But they're what the analyst brings into the AI session as raw material. The richer the working notes, the more productive the session.

### How This Works in Practice

```
Analyst's Files (persistent)          AI Session (temporary)
─────────────────────────────         ─────────────────────────
Requirements doc                 →    Pasted into Prompt 1 for
                                      quarterly review

Source library (reports,         →    Fed into Prompt 2 one
advisories, ISAC alerts)              source at a time

Existing research base           →    Pasted into Prompt 2 when
                                      adding new sources

Completed research base          →    Pasted into Prompt 3 to
                                      produce derivatives

Completed derivatives            ←    Saved from Prompt 3 output
Updated research base            ←    Saved from Prompt 2 output
Updated requirements             ←    Saved from Prompt 1 output
```

The arrows go both directions. The analyst's files feed into AI sessions, and AI session outputs get saved back to the analyst's files. The AI accelerates the work within a session; the analyst's files are the persistent record that survives between sessions.

### The Rule

**If the analyst loses access to their AI platform tomorrow, they should still have every requirements document, research base, and derivative they've ever produced.** The AI is a tool for building these artifacts faster — it is not the storage system. If the analyst's work only exists inside AI conversation histories, it's one platform change away from disappearing.

---

## Platform Compatibility Notes

These prompts are designed to be platform-agnostic, but AI assistants vary in their ability to handle complex system prompts. Here's what to expect.

### Fully Compatible

**Claude (Opus, Sonnet)** — Handles all three prompts as designed. Strong instruction following, reliable hard stop compliance, good at pushing back when the analyst rubber-stamps. Large context window handles multi-source research bases well.

**GPT-4o / GPT-4.5** — Handles all three prompts as designed. Comparable instruction following and hard stop compliance. Large context window. May be slightly more verbose in drafting than Claude — watch derivative length in Prompt 3.

### Compatible with Caveats

**Gemini (Pro, Ultra)** — Follows the structure but tends to be overly agreeable. The pushback mechanisms in Prompt 2 (flagging when the analyst marks everything relevant, noting when all confidence levels are accepted unchanged, challenging zero assumptions) may fire less reliably. Gemini also tends toward verbosity, which works against the filtering discipline in Prompt 3. The analyst may need to be more self-disciplined about cutting content if the AI doesn't push back.

**Qwen (72B+)** — Larger models handle the structured instructions and conditional branching well. Hard stop compliance is generally reliable at 72B+. Smaller models (14B, 32B) will struggle with the three-way intake path in Prompt 1 and the seven derivative type branches in Prompt 3. If using smaller Qwen models, consider breaking the prompts into per-phase conversations rather than relying on one long system prompt.

### May Require Adaptation

**Copilot (Enterprise)** — The GPT-4-backed enterprise version works. The free consumer version truncates long system prompts and loses instruction fidelity. These are long prompts — Prompt 3 in particular has significant branching logic. If the system prompt is being truncated, the derivative type specifications will be incomplete and the output quality will drop. Test by checking whether the AI acknowledges all seven derivative types in the setup phase. If it only lists four or five, the prompt is truncated.

**Copilot (Free / Consumer)** — Not recommended for these prompts without breaking them into smaller per-phase prompts. Context window and system prompt length limitations will degrade performance.

**Smaller Open-Source Models (<30B parameters)** — Not recommended. Hard stop compliance breaks down — the model will acknowledge the instruction to stop and then continue generating in the same message. The conditional branching in Prompt 1 and Prompt 3 requires instruction-following capability that smaller models lack. The five-gate enforcement in Prompt 2 requires the model to track state across multiple phases, which degrades quickly in smaller context windows.

### Common Issues Across Platforms

**Hard stop non-compliance.** The most common failure mode. The AI acknowledges that it should stop and wait, then generates the next phase anyway. If this happens consistently on a platform, the fix is to break the system prompt into smaller per-phase prompts — one prompt per phase, with the analyst manually moving to the next prompt after completing each phase. More manual, but it forces the stop mechanically.

**Context window overflow.** Prompt 2 accumulates content across multiple sources — extracted claims, gate metadata, corroboration tracking, compiled research base entries. On models with smaller context windows (under 32K tokens), the research base construction will degrade around source 4-5 as earlier claims fall out of context. The fix is to compile and save the research base entry after every 2-3 sources, then paste the compiled version back into a fresh session before processing additional sources.

**Verbosity creep.** Most AI assistants default to inclusion and length. Over the course of a Prompt 3 session, derivative sections tend to get longer as the AI tries to be thorough. The analyst must actively enforce conciseness — the final review checkpoint ("is it short enough that the consumer will actually read it?") exists specifically for this reason. If the AI consistently produces verbose output, add "keep this section under [N] words" to the section-level hard stop reviews.

**Pushback erosion.** Some models start strong on enforcement (challenging all-relevant markings, flagging zero assumptions) but stop pushing back after the analyst overrides them 2-3 times. The model learns within the session that the analyst doesn't want to be challenged. This is a feature of the model's helpfulness training, not a bug the analyst can fix. The senior analyst reviewer is the backstop — the red flags section of this guide exists to catch the patterns that eroded pushback would have caught.

---

## Influences

- **TIRED Labs TRR Methodology (Andrew VanVleet)** — The source-to-derivative model, the principle that research and deliverables are different things, and the DDM inclusion test as structural inspiration for the five-gate filter.
- **Robert M. Lee** — Confidence level framework and the principle that intelligence serves the consumer's requirement.
- **Michael Rea** — Intelligence requirements as the foundation of CTI program success.
- **Lenny Zeltser** — Consumer-focused inclusion test for reports, writing discipline principles.
- **SANS FOR578** — Intelligence cycle, structured analytic techniques.
