# CTI Pipeline Framework — Talking Points

## Slide 1: Title — "A Structured CTI Pipeline"

- This isn't a product pitch or a critique of how things work today. It's a framework I've been building that structures the CTI production pipeline into three connected pieces.
- The goal of this conversation is exploratory — I want to walk through how these three frameworks work together, and then talk about where something like this could add value in our environment.
- Everything I'm showing has full documentation behind it. The deck is the overview; the three framework documents go deep.

---

## Slide 2: The Pipeline at a Glance

- The pipeline has three frameworks, each solving one specific part of the intelligence production problem.
- **Framework 1** answers "what should we be looking for and where?" — this is the requirements and collection layer.
- **Framework 2** answers "what qualifies as intelligence?" — this is a quality filter that every claim has to pass before it enters the research base.
- **Framework 3** answers "who gets what and in what form?" — this is where a single body of research gets turned into audience-specific deliverables.
- The key idea: these aren't independent — they're a pipeline. Requirements drive collection, quality gates filter what enters the research base, and derivatives deliver the right intelligence to the right consumer. If you break one, the downstream stages feel it.

---

## Slide 3: Framework 1 — Requirements & Collection

- This is the upstream layer that everything else depends on. Without defined requirements, analysts collect based on curiosity or whatever's trending — not what the organization needs to know.
- The hierarchy has three levels. **IRs** are the broadest questions — "which threat actors target firms with our profile?" You should have 6–8 max, reviewed semi-annually. These come from consumers, not from the CTI team.
- **PIRs** break each IR into specific, time-bound questions — "which ransomware groups have claimed financial sector victims in the past 90 days?" These are reviewed quarterly and are where most of the analyst's daily work is directed.
- **SIRs** are granular, short-lived — triggered by incidents or emerging events. They get answered and closed.
- The key features that make this work: every PIR has a **collection matrix** mapping it to specific sources, so analysts know exactly where to look. There are **minimum source thresholds** — you can't make a moderate-confidence assessment from a single blog post. And the **gap register** documents what the team *can't* answer, which turns "we need more tools" into a data-backed business case tied to specific unanswerable questions.

---

## Slide 4: Framework 2 — Research Quality

- This is the filter between collection and the research base. Five gates, every claim must pass all five.
- **Sourced** — can you point to where this came from? "I think I read it somewhere" fails. Common knowledge still needs a citation.
- **Current** — is this still accurate? Threat intel has a shelf life. A technique documented in 2022 may not be in active use anymore.
- **Relevant** — does this help answer the intelligence requirement? If no one asked "how does ransomware work," a section explaining the RaaS model doesn't belong — no matter how accurate it is.
- **Confidence-Rated** — can you state Low, Moderate, or High and articulate *why*? This forces the analyst to evaluate their own claims rather than presenting everything with equal weight.
- **Typed** — is this a fact, an assessment, or an assumption? Assumptions are the most dangerous because they hide in the prose and never get challenged.
- If a claim fails any single gate, it doesn't enter the research base as-is. It gets cut, reworked, or flagged.
- There's also a structural gate that checks the research base as a whole — are key judgments separated from evidence? Are competing hypotheses considered? Are collection gaps documented? Are assumptions explicit?

---

## Slide 5: Framework 3 — Source-to-Derivative

- This is where research turns into deliverables. The core principle: one research base, multiple outputs, each filtered by audience and question.
- The **research base** is internal only — lossless, exhaustive, fully sourced. It never leaves the CTI team as-is.
- Each **derivative** has a defined consumer and a defined question. The Executive Brief answers "what should we prioritize?" for the CISO. The Detection Brief answers "what should we build?" for detection engineering. The IR Brief answers "what does the attack look like?" for incident response. And so on.
- The inclusion test for every section in a derivative is three questions: Who is reading this? What decision are they making? Does this section help them make that decision? If the answer to the third question is no, it stays in the research base.
- Not every topic requires every derivative. You produce what's needed, when it's needed, for whoever is asking.
- The result: instead of one 11-page report that nobody reads, you get a 2-page executive brief, a technical detection package, an IR preparedness doc — each one exactly as long as it needs to be.

---

## Slide 6: How the Frameworks Connect

- This is the end-to-end view. Requirements define what to look for. Quality gates filter what enters the base. The research base accumulates key judgments. Derivatives deliver to the right consumer.
- The important property is **full traceability**. Every piece of intelligence can be traced from the consumer's question (IR), through the collection that found it (PIR + source), through the quality filter that validated it (five gates), into the research base (with confidence level), and out to the derivative that delivered it.
- If a deliverable is wrong or a consumer isn't getting what they need, you trace backward to find where the chain broke. Was it bad requirements (wrong questions)? Bad collection (wrong sources)? Bad filtering (claims entering without sourcing)? Bad research base (no key judgments)? Or bad derivatives (wrong audience, wrong format)?
- That diagnostic capability is what makes this a pipeline rather than just a set of documents.

---

## Slide 7: Why This Produces Good Results

- **Analysts know what to look for.** IRs and PIRs replace open-ended research with defined questions from consumers. Collection plans map each PIR to specific sources. No more "search everywhere and include everything."
- **Every claim is quality-tested.** The five gates prevent unsourced, stale, irrelevant, or unconfident claims from entering the research base. Assumptions get surfaced, not hidden.
- **Consumers get exactly what they need.** A CISO gets a 2-page brief with prioritized actions. A detection engineer gets Sysmon EIDs and query priorities. Same research, right format. Nobody has to parse a full threat report to find the three things they care about.
- **Gaps are visible and actionable.** The gap register ties unanswerable questions directly to specific missing capabilities. This is the difference between "we need better tools" and "we cannot answer PIR-04.1 because we lack dark web credential monitoring — here's the cost and here's the impact."
- **The team cross-trains naturally.** Analyst rotation across derivative types builds consumer empathy. Writing for the CISO teaches a fundamentally different skill than writing for the SOC. Over time, every analyst understands what every consumer needs.

---

## Slide 8: Discipline Use Cases

- This slide shows how each security discipline consumes the pipeline's output differently.
- **Threat Intelligence** owns the pipeline. They build the research base, produce all derivatives, and maintain the requirements with consumers. They're the engine.
- **Detection Engineering** consumes the Detection Brief — prioritized ATT&CK techniques with specific telemetry sources and Sysmon EIDs. This feeds directly into query development and SIEM tuning. The detection engineer doesn't need to read a full threat report to know what to build next.
- **Incident Response** consumes the IR Preparedness Brief — phase-by-phase kill chain with expected artifacts, containment priorities, and evidence preservation checklists. This feeds playbook updates and tabletop exercise design. When an incident hits, the IR team already knows what the attack looks like.
- **Red Team / Emulation** uses the research base directly for realistic adversary emulation. They also use the Detection Brief as a validation target — testing whether the detections actually fire. This closes the loop between intelligence and defense.
- **Hunt** uses the Detection Brief and IR Brief together. The detection coverage map shows where detections exist and where blind spots remain — hunt operates in the blind spots. Kill chain detail from the IR Brief helps form hypotheses.
- The point: one body of research serves five different disciplines. Each gets what they need without the CTI team writing five different reports from scratch.

---

## Slide 9: Where This Comes From

- This isn't invented from scratch. It draws on three established bodies of work.
- The **intelligence cycle** — requirements-driven production, confidence levels, the principle that intelligence serves the consumer's requirement, not the analyst's curiosity. Rob Lee's confidence framework, Michael Rea's work on intelligence requirements, SANS FOR578.
- **Cybersecurity writing discipline** — Lenny Zeltser's consumer-focused inclusion test. Does this answer a question the reader actually has? Lead with the point. Cut 20%. Don't bury the main idea. His SEC402 rating sheet directly informed the derivative inclusion test.
- **TIRED Labs TRR methodology** — Andrew VanVleet's source-to-derivative model. The idea that discipline-neutral research serves as lossless source material from which team-specific outputs are produced. Research and deliverables are different things. That principle is the backbone of this whole framework.
- Full references and source material are in the framework documentation if anyone wants to go deeper.

---

## Slide 10: Let's Explore This Together

- This framework is designed to be adapted, not adopted wholesale. The structure is environment-agnostic — the specific IRs, PIRs, sources, and derivative types would all be tailored to how the team operates today.
- The conversation I'd like to have: what does your current workflow look like, and where could a structured pipeline like this add the most value?
- I have three full framework documents plus an example research base with derivatives available for review. Happy to walk through any of them in detail.
- This is an exploratory conversation — I'm not prescribing a solution, I'm presenting a framework and asking where it fits.
