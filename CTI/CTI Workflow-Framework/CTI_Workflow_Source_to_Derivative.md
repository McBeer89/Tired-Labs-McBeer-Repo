# CTI Workflow Proposal: Source-to-Derivative Model

## The Problem

Analysts produce thorough, well-researched reports — but deliver the raw research as the finished product. The result is 10+ page documents that contain good intelligence buried in more detail than any single consumer needs. Leadership stops reading. The analyst's work goes underutilized.

## The Root Cause

Research and deliverables are different things. The analyst's job doesn't end when the research is complete — it ends when the right intelligence reaches the right consumer in a form they can act on.

## The Model

### Layer 1: CTI Research Base (Source Layer)

The team's shared, lossless source of truth. One per topic (threat actor, campaign, vulnerability cluster, sector trend — whatever the team tracks).

**Characteristics:**
- Captures everything: threat actor profiles, full ATT&CK mapping, kill chain detail, IOCs, incident case studies, regulatory context, source evaluation
- Full sourcing and confidence levels on every claim
- Any analyst can contribute; the base grows over time
- Never sent outside the CTI team as-is
- Analogous to Phase 1 research in the TIRED Labs TRR methodology — exhaustive by design

### Layer 2: Derivative Products (Deliverables)

Audience-specific outputs produced from the research base. Each derivative has a defined consumer, a defined question it answers, and an inclusion test that determines what belongs.

| Derivative | Consumer | Question It Answers |
|---|---|---|
| Executive Threat Brief | CISO, security leadership | What should we prioritize and why? |
| Tactical IOC Package | SOC analysts, SIEM operators | What should we watch for right now? |
| Detection Engineering Brief | Detection/query developers | What should we build detections against? |
| IR Preparedness Brief | Incident response team | What does the kill chain look like and what artifacts should we expect? |
| Compliance Brief | Legal, compliance, risk | What are our reporting obligations and payment risks? |

**Not every topic requires every derivative.** Produce what's needed, when it's needed, for whoever is asking.

### The Inclusion Test for Derivatives

Before including any section in a derivative, ask:

1. **Who is reading this?** — Name the consumer.
2. **What decision are they making?** — Name the decision or action.
3. **Does this section help them make that decision?** — If no, it stays in the research base.

This is the CTI equivalent of Zeltser's rating sheet: every section must answer a question the reader actually has.

## Analyst Rotation

Rotate which analyst writes which derivative product each cycle (quarterly, per-campaign, however the team operates).

**What rotation accomplishes:**
- Analysts learn what each consumer cares about by writing for them directly
- Cross-trains the team across CTI, detection, IR, and executive communication
- Prevents analysts from getting siloed into one output type
- Research quality improves naturally — analysts start collecting with derivatives in mind, not just collecting everything

**Example rotation:**

| Cycle | Analyst A | Analyst B | Analyst C |
|---|---|---|---|
| Q1 | Executive Brief | Detection Brief | IOC Package |
| Q2 | IR Brief | Executive Brief | Detection Brief |
| Q3 | IOC Package | IR Brief | Executive Brief |
| Q4 | Detection Brief | IOC Package | IR Brief |

## Quality Control

The senior analyst reviews all derivatives before distribution. This is where editorial judgment lives — not in the research phase (where thoroughness is the goal), but in the derivative phase (where filtering and conciseness are the goal).

The review checks:
- Does this answer the consumer's question and only that question?
- Is the main point up front, not buried?
- Are confidence levels stated?
- Is it concise enough that the consumer will actually read it?
- Are sources attributed?

## What This Looks Like in Practice

```
Analyst does research
        │
        ▼
┌─────────────────────┐
│  CTI Research Base   │  ← Lossless, exhaustive, internal only
│  (Source Layer)      │
└────────┬────────────┘
         │
         │  Filter by consumer + question
         │
    ┌────┼────┬─────────┬──────────┐
    ▼    ▼    ▼         ▼          ▼
  Exec  IOC  Detection  IR      Compliance
  Brief Pack  Brief    Brief     Brief
    │    │      │        │          │
    ▼    ▼      ▼        ▼          ▼
  CISO  SOC   DetEng    IR Team   Legal
```

Each arrow is a filtering step. Information flows down only if it answers a question the consumer has.

## Key Principle

> The analyst who does the most research is not the one who writes the longest report. They're the one who can produce five different deliverables from one body of work — each one exactly as long as it needs to be and no longer.

## Influences and References

The inclusion test, quality control criteria, and overall philosophy of filtering research into consumer-focused deliverables draw from several sources:

- **Lenny Zeltser** — *Rating Sheet for the Right Information: Threat Reports* (SEC402: Cybersecurity Writing: Hack the Reader). The rating sheet's question-based framework directly informs the derivative inclusion test above. [zeltser.com](https://zeltser.com)
- **Lenny Zeltser** — *Writing Tips for IT Professionals*, v1.1. General writing discipline principles (lead with the point, cut 20%, write for skimmers) applied to derivative formatting. [zeltser.com/writing-tips-for-it-professionals](https://zeltser.com/writing-tips-for-it-professionals)
- **Lenny Zeltser** — *Top 10 Writing Mistakes in Cybersecurity and How You Can Avoid Them* (SANS Webcast / YouTube). The five golden elements (structure, look, words, tone, information) and the specific anti-patterns — particularly burying the main point, overstuffing paragraphs, including details most readers don't need, and using FUD — informed the quality review checklist. [youtube.com/watch?v=V7lO7UgxQV4](https://www.youtube.com/watch?v=V7lO7UgxQV4)
- **Andrew VanVleet / TIRED Labs** — The source-to-derivative model is adapted from the TRR methodology, where discipline-neutral Technique Research Reports serve as lossless source material from which team-specific derivative documents (Detection Methods, Lab Recreation Guides, Hunt Playbooks, IR Runbooks) are produced. The Phase 1 research vs. Phase 4 publication distinction and Pitfall #11 (Phase 1 Artifact Leakage) directly parallel the CTI research base vs. derivative product separation. [library.tired-labs.org](https://library.tired-labs.org)
- **Robert M. Lee** — *Structuring Cyber Threat Intelligence Assessments: Musings and Recommendations*. Confidence levels (Low/Moderate/High) and the principle that intelligence exists to serve the consumer's requirement, not to showcase the analyst's research. [robertmlee.org](https://www.robertmlee.org/structuring-cyber-threat-intelligence-assessments-musings-and-recommendations/)
