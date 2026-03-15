# CTI Pipeline Implementation Plan

A phased rollout for a team of four (1 senior lead + 3 analysts) adopting the structured CTI pipeline. Designed to be achievable alongside existing work — the team doesn't stop producing while they adopt the framework.

**Realistic timeline:** Basic operational capability in 6 months. Well-oiled in 12. The first three months are the hardest because you're building the foundation while still doing the old work. After Month 3, the framework starts reducing effort rather than adding it.

---

## Month 1: Requirements Foundation

**Goal:** Define what the team is supposed to be answering.

**Week 1-2: Consumer conversations.**
The lead schedules 30-minute conversations with each consumer (CISO, SOC, Detection Eng, IR, Vuln Mgmt, Compliance). One question per conversation: "What do you need to know about the threat environment to do your job?" These don't have to be formal. Slack, coffee, email — whatever works. The analysts don't participate yet — the lead owns this.

**Week 3-4: Draft requirements.**
The lead uses Prompt 1 to structure the consumer input into IRs and PIRs. Draft the collection matrix and gap register. This takes one focused day with the AI, plus a day of review and refinement.

**Deliverable by end of Month 1:**
- 6-8 IRs with consumer attribution
- PIRs under each IR with collection sources
- Initial gap register
- One-page summary sent to each consumer: "Here's what I heard. Does this match what you need?"

**Team impact:** Minimal. The lead does this work. Analysts continue existing production. The only visible change is the lead having conversations with consumers.

---

## Month 2: First Research Base

**Goal:** Produce one research base using the five gates. Prove the process works.

**Week 1: Pick the topic.**
The lead selects the single highest-priority PIR cluster — probably the one the CISO cares about most or the one with the most available source material. Don't pick something obscure. Pick the topic you'd be writing a report about anyway.

**Week 2-3: Build the research base.**
The lead and one analyst work through Prompt 2 together. Process 3-5 sources. The lead walks the analyst through the five gates on the first source, then the analyst runs gates on subsequent sources with the lead reviewing. This is training by doing, not training by presentation.

**Week 4: Structural gate and key judgments.**
The lead reviews the completed research base against the seven structural questions. Finalize key judgments.

**Deliverable by end of Month 2:**
- One completed research base with full gate metadata
- The analyst who participated understands the five gates from experience, not theory

**Team impact:** One analyst is partially dedicated to this. The other two continue existing work. The lead is spending roughly 30% of their time on implementation.

---

## Month 3: First Derivatives

**Goal:** Produce two derivatives from the Month 2 research base. Show consumers the difference.

**Week 1-2: Executive Brief.**
The lead uses Prompt 3 to produce an Executive Brief from the research base. Reviews with the CISO. The ask: "Is this more useful than what you've been getting? What would you change?"

**Week 2-3: One technical derivative.**
Pick the technical consumer who has been most vocal about the current reports not working — probably Detection Engineering or IR. The lead and a second analyst produce the Detection Brief or IR Brief together using Prompt 3. Same training-by-doing approach as Month 2.

**Week 4: Consumer feedback.**
The lead collects feedback from the two consumers who received derivatives. What worked? What didn't? What's missing?

**Deliverable by end of Month 3:**
- One Executive Brief delivered to CISO
- One Detection or IR Brief delivered to the technical consumer
- Consumer feedback documented
- Two analysts have now been through the process (one on research base, one on derivatives)

**Team impact:** Two analysts have hands-on experience. The third hasn't participated yet. Existing report production continues in parallel but the team is starting to see the contrast.

**This is the inflection point.** If the consumers respond positively — and they will, because a 2-page brief that answers their question is better than a 12-page report that doesn't — the team has proof that the framework works. The lead can use this to justify shifting more effort toward the new workflow.

---

## Month 4: Second Cycle and Third Analyst

**Goal:** Run the pipeline a second time. Bring the third analyst in. Start replacing old report production.

- Pick a second PIR cluster. The third analyst builds the research base with lead oversight.
- The first two analysts produce derivatives from the new research base — one each, different types.
- Begin phasing out the old report format. Instead of one long report, produce the research base internally and send derivatives to consumers.

**Deliverable by end of Month 4:**
- Second research base completed
- Two more derivatives produced
- All three analysts have been through the pipeline at least once
- At least one old-format report replaced by the new workflow

---

## Month 5: Rotation and Independence

**Goal:** Analysts produce with decreasing lead involvement. Start the rotation.

- Each analyst owns a research base update or derivative production with the lead reviewing output rather than co-producing.
- Introduce the rotation: Analyst A writes the Executive Brief, Analyst B writes the Detection Brief, Analyst C writes the IR Brief. Next cycle they rotate.
- The lead shifts from co-producer to reviewer — checking research bases against the structural gate and derivatives against the inclusion test.

**Deliverable by end of Month 5:**
- Three derivatives produced with lead reviewing, not co-writing
- Rotation schedule established
- Lead time per derivative is decreasing

---

## Month 6: Baseline Operational Capability

**Goal:** The pipeline runs without the lead doing the work. The lead reviews and the analysts produce.

- Quarterly PIR review with consumers (first one since Month 1)
- Gap register updated based on five months of collection experience
- Analysts can independently run Prompts 1-3 with lead review at structural gate (research base) and final review (derivatives)
- At least 2-3 research bases exist with derivatives produced from each

**What "operational" looks like at Month 6:**
- Requirements exist and are reviewed with consumers
- Research bases are built with five gates enforced
- Derivatives are produced for specific consumers in formats they can use
- The old 11-page report format is retired or reserved for topics that haven't been through the pipeline yet
- The lead spends most of their time reviewing, not producing

**What's probably still rough at Month 6:**
- The rotation isn't smooth yet — analysts are better at some derivative types than others
- Collection cadence may not be fully disciplined (daily/weekly/monthly schedule is aspirational)
- Not all PIRs have adequate source coverage — the gap register is honest about this
- AI-assisted workflow is functional but analysts are still learning when to push back versus accept suggestions
- Consumer feedback loop is informal, not systematic

---

## Months 7-9: Depth and Breadth

**Goal:** Expand coverage and increase quality.

- Add research bases for PIR clusters that haven't been addressed yet
- Produce additional derivative types (IOC Package for SOC, Compliance Brief for Legal, Emulation Brief for annual red team engagement)
- Formalize the collection cadence — daily and weekly checks become habit, not aspiration
- The lead starts tracking red flags from the AI workflow guide: are analysts rubber-stamping gates? Are all confidence levels moderate? Are assumptions being surfaced?
- Consumer feedback becomes structured: after each derivative, one question to the consumer — "did this help you make a decision?"

---

## Months 10-12: Well-Oiled

**Goal:** The pipeline is self-sustaining. The lead manages, the analysts produce, consumers receive.

- Full PIR coverage — every standing PIR has an active research base or is documented as a gap
- Rotation is smooth — every analyst has written every derivative type at least twice
- Collection cadence is disciplined and tracked
- Gap register is used in budget conversations ("we can't answer PIR-04.1 without dark web monitoring — here's the cost")
- Consumer feedback drives PIR updates — the semi-annual IR review with consumers is a real meeting, not a formality
- Emulation Brief produced for annual red team engagement, detection validation loop completed at least once
- Research bases are versioned and maintained — new sources are processed incrementally, not from scratch each cycle

**What "well-oiled" looks like at Month 12:**
- A consumer asks a question, the team checks whether an existing research base answers it, and if so produces a derivative in days not weeks
- New topics go through the full pipeline from requirements to derivative without the lead hand-holding
- The team can articulate why they're researching what they're researching — every topic traces to a consumer requirement
- Quality is consistent across analysts because the gates and review process enforce a standard regardless of individual motivation

---

## What This Requires From Leadership

The framework solves the methodology problem. It doesn't solve the capacity problem or the motivation problem. For this plan to work, leadership needs to:

- **Protect the lead's time in Months 1-3.** The lead is building the foundation, training analysts, and still reviewing existing work. If they're pulled into other projects, the timeline slips.
- **Accept reduced output volume in Months 2-4.** The team is learning a new process. They'll produce fewer total documents but the documents they produce will be better. This is a temporary dip.
- **Enforce the transition.** At some point (Month 4-5), the old report format has to stop being acceptable. If consumers still receive 11-page reports alongside the new derivatives, there's no pressure to complete the transition.
- **Fund the gaps the framework surfaces.** The gap register will identify specific capabilities the team lacks (dark web monitoring, vendor breach notification SLAs, etc.). If those gaps never get funded, the register becomes a list of things the team documented but leadership ignored — which kills morale faster than not having a framework at all.

---

## Quick Reference: What's Produced When

| Month | Research Bases | Derivatives | Analysts Trained | Lead Role |
|---|---|---|---|---|
| 1 | 0 | 0 | 0 | Build requirements |
| 2 | 1 | 0 | 1 | Co-produce |
| 3 | 1 | 2 | 2 | Co-produce |
| 4 | 2 | 4 | 3 | Co-produce / review |
| 5 | 2-3 | 5-6 | 3 | Review |
| 6 | 3+ | 6+ | 3 | Review |
| 7-12 | Expanding | Full suite | 3 (rotating) | Manage |
