# CTI Pipeline Framework — Anticipated FAQ

Questions a CTI team lead is likely to ask when seeing this framework for the first time, with answers grounded in the three framework documents.

---

## Foundational Concepts

### "What exactly is an intelligence requirement?"

An intelligence requirement is a question the organization needs answered about the threat environment. It comes from consumers — the CISO, the SOC, IR, compliance — not from the CTI team's own interests. It's the difference between "what should we be researching?" (requirement-driven) and "what did we happen to find this week?" (curiosity-driven). Requirements exist at three levels: broad IRs (semi-annual), specific PIRs (quarterly), and granular SIRs (incident-driven, short-lived). The requirement is what makes everything downstream purposeful — without it, analysts collect without direction.

### "What's the difference between the research base and a report?"

The research base is the team's internal, lossless source of truth on a topic. It captures everything — threat actor profiles, full ATT&CK mapping, kill chain detail, IOCs, incident case studies, source evaluation, confidence levels. It's exhaustive by design and never sent outside the CTI team as-is. A report (what this framework calls a "derivative") is an audience-specific output produced *from* the research base. It contains only what a specific consumer needs to make a specific decision. The research base is the kitchen; the derivative is what gets plated and served.

### "What do you mean by 'derivative'?"

A derivative is any deliverable produced from the research base for a specific audience. Each one has a defined consumer and a defined question it answers. Examples: an Executive Brief for the CISO ("what should we prioritize?"), a Detection Engineering Brief for det eng ("what should we build?"), an IR Preparedness Brief for the IR team ("what does the attack look like?"). The term comes from the TIRED Labs methodology where discipline-neutral research produces team-specific outputs. The key property: one body of research, multiple deliverables, each filtered by audience and decision.

### "What's a confidence level and why does it matter?"

A confidence level (Low, Moderate, High) tells the consumer how much weight to put on an assessment. It's based on source count, source quality, corroboration, and known gaps. Low confidence means the assessment is supported by available information but may be single-sourced with known gaps. Moderate means multiple pieces of information support it with gaps significantly reduced. High means predominant available data across multiple independent sources with gaps accounted for. The important thing: low confidence is a valid, useful assessment — it tells the consumer "we think this, but here's what we don't know." Without confidence levels, everything reads as equally certain, which is misleading.

### "What's the difference between a fact, an assessment, and an assumption?"

A **fact** is verifiable — "CISA published advisory AA25-071A on Medusa ransomware in March 2025." An **assessment** is an analytical judgment that goes beyond the evidence — "We assess with moderate confidence that Medusa poses a credible threat to firms in our sector." It requires a confidence level. An **assumption** is an unstated belief the analyst is treating as true — "our organization uses SonicWall appliances." Assumptions are the most dangerous because they hide in the prose and never get challenged. The five gates force analysts to explicitly label which one they're writing.

---

## Implementation and Practicality

### "This looks like a lot of overhead. How much work is this to stand up?"

It's designed to be adopted incrementally, not all at once. The highest-value starting point is usually the requirements hierarchy — just getting IRs and PIRs defined with consumers. That alone focuses analyst effort and gives the team a way to say "we're working on this because leadership asked this question." The five gates can be introduced as a review checklist before anything gets published. The derivative model can start with just two outputs — an executive brief and one technical brief — and expand as the team builds the muscle. The framework documents are the reference; the team decides how fast to adopt.

### "We already produce reports. How is this different from what we do now?"

The framework doesn't assume your current reports are bad. The question is whether the same body of research could serve more consumers in less total effort. If your analysts are writing one long report that gets sent to everyone, the CISO skims the first page and the detection engineer hunts for the three IOCs buried on page 8. Both got the same document; neither got what they needed efficiently. The derivative model means you do the research once and produce targeted outputs. The total word count across all derivatives might actually be *less* than the single long report, because each one only includes what its consumer needs.

### "How do you define who the consumers are?"

You ask them. Meet with each group — security leadership, the SOC, detection engineering, IR, compliance, whoever consumes your output. Ask: "What do you need to know about the threat environment to do your job? What decisions do you make that threat intelligence could inform?" Their answers become your IRs. The CTI team doesn't invent requirements — they elicit and formalize them from consumers. If you don't know who your consumers are or what they need, that's the first problem to solve before anything else in this framework matters.

### "What if we don't have enough analysts to produce all these derivatives?"

Not every topic requires every derivative. Produce what's needed, when it's needed, for whoever is asking. If you have two analysts and the most impactful outputs are an executive brief and a detection brief, start there. The IOC package, IR brief, and compliance brief can be added when the team grows or when a specific consumer requests them. The framework is a menu, not a mandate. The rotation schedule also assumes a team of three or more — smaller teams can still use the model, they just produce fewer derivatives per cycle.

### "How does analyst rotation work in practice?"

Each production cycle (quarterly, per-campaign, however the team operates), you rotate which analyst writes which derivative. Analyst A writes the executive brief this quarter, the detection brief next quarter, the IR brief the quarter after. The rotation serves two purposes: it cross-trains the team so no one is siloed into one output type, and it builds consumer empathy — writing for the CISO teaches a fundamentally different discipline than writing for the SOC. The senior analyst reviews all derivatives before distribution regardless of who wrote them.

### "What tools do we need to implement this?"

The framework is tool-agnostic. It describes a workflow, not a platform. The research base can live in a wiki, a shared document, a TIP, or even a structured markdown repository. Derivatives can be Word docs, PDFs, emails, or whatever format your consumers prefer. The collection matrix can be a spreadsheet. The gap register can be a table in a shared doc. If you already have a TIP (Threat Intelligence Platform), the framework tells you how to structure what goes into it and what comes out of it. If you don't have a TIP, you can still run this workflow with basic tools.

---

## Quality and Process

### "What happens when a claim fails one of the five gates?"

It doesn't enter the research base as-is. Depending on which gate it fails, the analyst either finds a source (Gate 1), verifies currency (Gate 2), ties it to the requirement (Gate 3), assigns a confidence level with reasoning (Gate 4), or makes the assumption explicit (Gate 5). Some claims get cut entirely because they're not relevant to the requirement. Some get reworked with better sourcing. Some get flagged as low-confidence with known gaps documented. The gates aren't a pass/fail exam — they're a forcing function that improves the quality of what enters the base.

### "How do you handle disagreements about confidence levels?"

That's what the reviewer is for. The senior analyst reviews the research base and challenges the confidence reasoning. If an analyst rates something as moderate confidence but it's single-sourced from a vendor blog with no corroboration, the reviewer pushes back: "What's your second source? If you don't have one, this is low confidence." The confidence criteria are explicit (source count, source diversity, gap accounting), so disagreements can be resolved by pointing to the criteria rather than arguing about feelings. The review checks the reasoning, not just the label.

### "What's the gap register and why should I care about it?"

The gap register documents intelligence requirements the team *cannot* adequately answer with available sources. Each gap is tied to a specific PIR, describes the missing capability, states the impact on assessment quality, and tracks resolution status. This is the most honest part of the intelligence program — it tells leadership exactly what the team can and can't answer. More importantly, it turns resource requests into data-backed business cases. "We need a dark web monitoring subscription" is a vague ask. "We cannot answer PIR-04.1 (organizational credential exposure) because we lack dark web credential monitoring — here's what that means for our risk posture" is a funded request.

### "How do you prevent the research base from becoming its own bloated document?"

The research base is allowed to be exhaustive — that's by design. It's the lossless source layer. What prevents bloat from reaching consumers is the derivative filter. The research base can be 30 pages; the executive brief derived from it should be 2. The inclusion test ("who is reading this, what decision are they making, does this help") is what keeps derivatives lean. The research base itself stays clean because the five gates prevent low-quality claims from entering it in the first place — it's exhaustive but rigorous, not exhaustive and undisciplined.

### "Who reviews the derivatives before they go out?"

The senior analyst reviews all derivatives before distribution. The review checks: Does this answer the consumer's question and *only* that question? Is the main point up front, not buried? Are confidence levels stated? Is it concise enough that the consumer will actually read it? Are sources attributed? The reviewer's job is editorial judgment on the derivative — not rewriting it, but ensuring it's filtered correctly for the audience. The research phase values thoroughness; the derivative phase values filtering and conciseness. Different standards for different stages.

---

## Scope and Adaptability

### "Does this framework assume a specific team size?"

No. The examples use three analysts and five derivative types, but both scale up or down. A two-person team might produce two derivative types. A ten-person team might have dedicated analysts per IR and produce the full derivative suite. The structure scales — the IR/PIR hierarchy, the five gates, and the derivative model all work regardless of team size. What changes is how many PIRs you can actively collect against, how many derivatives you produce per cycle, and whether you rotate or specialize.

### "Can this work alongside our existing processes?"

Yes — it's designed to be adapted, not to replace everything. If you already have a requirements process, this framework gives you a structure to formalize it. If you already produce executive briefs, this gives you an inclusion test to sharpen them. If your research quality is already strong, the derivative model is the piece that adds the most immediate value. You don't adopt the whole pipeline on day one — you identify which stage of your current workflow would benefit most from structure and start there.

### "What if our consumers don't know what they need?"

That's common, especially early on. The framework accounts for this — the IR development process starts with open-ended conversations: "What decisions do you make that threat intelligence could inform?" Most consumers can answer that even if they can't articulate a formal intelligence requirement. The CTI team's job is to translate those answers into structured IRs and PIRs. Over time, as consumers see derivatives tailored to their needs, they get better at articulating what they want. The first cycle is the hardest; it gets easier.

### "How does this relate to the MITRE ATT&CK framework?"

ATT&CK is a taxonomy of adversary behavior — it tells you *what* attackers do. This framework tells you *how to structure your intelligence production* around threats that use those behaviors. They're complementary. ATT&CK techniques show up in the research base (mapped to threat actor TTPs), in the Detection Brief (prioritized for detection development), and in the IR Brief (mapped to kill chain phases). ATT&CK is the language; this framework is the workflow for producing intelligence about threats that speak that language.

### "Where did this come from? Is this a commercial product?"

No, it's not a product. It draws on three established bodies of work: the intelligence cycle (Rob Lee, Michael Rea, SANS FOR578), cybersecurity writing discipline (Lenny Zeltser, SEC402), and the TIRED Labs TRR methodology (Andrew VanVleet) — specifically the source-to-derivative model where discipline-neutral research serves as lossless source material for team-specific outputs. The framework documents are the deliverable. Everything is available for the team to review, adapt, and use.
