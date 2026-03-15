# CTI Research Quality Framework: Inclusion Tests and Structural Gates

## The Problem

Analysts produce long reports that lack analytical rigor. The length comes not from thorough research but from uncritical accumulation — everything found gets included regardless of relevance, confidence, sourcing, or timeliness. The result is a report that is simultaneously too long and too shallow.

## Why This Happens

Junior analysts often lack a filter for what belongs in a finished intelligence product. Without one, the default behavior is to include everything — because cutting feels like losing work, and because the analyst doesn't yet have the judgment to distinguish intelligence from noise. The fix is to give them an explicit, repeatable filter they can apply to every claim before it enters the research base.

---

## Part 1: The Claim-Level Inclusion Test

Before any piece of information enters the research base, the analyst should run it through five gateway questions. Every claim must pass all five. If it fails any one, it either gets cut, reworked, or flagged for further research.

### The Five Gates

**Gate 1: Is this sourced?**

Can I point to where this came from? A specific report, advisory, vendor publication, or primary data source? If the answer is "I think I read it somewhere" or "this is common knowledge," it fails. Common knowledge still needs a source — the analyst's job is to show their work.

- Pass: "Akira exploited CVE-2024-40766 in SonicWall appliances (CISA Advisory AA24-109A, November 2025)"
- Fail: "Akira is known to exploit VPN vulnerabilities"

**Gate 2: Is this current?**

Is this information still accurate as of the reporting period? Threat intelligence has a shelf life. IOCs rotate, groups rebrand, TTPs evolve. A technique documented in 2022 may no longer be in active use. If the analyst can't confirm the information reflects the current threat environment, it fails or gets flagged with a staleness caveat.

- Pass: "Qilin averaged 75 attacks per month in Q3 2025 (Check Point Research, Q3 2025)"
- Fail: "RansomHub is the most active ransomware group" (ceased operations April 2025)

**Gate 3: Is this relevant to the intelligence requirement?**

Does this information help answer the question the consumer asked? If no one asked "how does ransomware work," then a section explaining the RaaS model doesn't belong — no matter how accurate it is. The intelligence requirement is the scope statement. Everything that doesn't serve it is research the analyst did for their own understanding, not intelligence for the consumer.

- Pass: Consumer asked "what ransomware groups target financial services?" → Qilin's campaign against 23 South Korean financial firms is relevant.
- Fail: Consumer asked the same question → A history of the AIDS Trojan from 1989 is not relevant.

**Gate 4: How confident am I, and why?**

Can the analyst state a confidence level (Low, Moderate, High) and articulate what supports it? This forces the analyst to evaluate their own claims rather than presenting everything with equal weight. The confidence level is based on source count, source quality, corroboration, and known collection gaps.

| Level | Criteria |
|---|---|
| Low | Hypothesis supported by available information. Likely single-sourced. Known gaps exist. May not be sufficient as the sole factor in a decision. |
| Moderate | Supported by multiple pieces of information. Gaps significantly reduced. May still be single-sourced but with multiple data points. |
| High | Supported by predominant available data across multiple independent sources. Collection gaps accounted for and unlikely to change the assessment. |

- Pass: "We assess with moderate confidence that supply-chain compromise is the most likely vector, based on three independent incidents in 2025 (Marquis, DBS/Toppan, Betterment) and Flashpoint reporting on IAB activity targeting financial sector vendors."
- Fail: "Supply-chain attacks are a major threat." (No confidence level, no supporting evidence, no specificity.)

**Gate 5: Am I stating a fact, an assessment, or an assumption?**

The analyst must know which one they're writing. Facts are verifiable. Assessments are analytical judgments that go beyond the evidence (and require confidence levels). Assumptions are unstated beliefs the analyst is treating as true. Assumptions are the most dangerous — they hide in the prose and never get challenged.

- Fact: "CISA published advisory AA25-071A on Medusa ransomware in March 2025."
- Assessment: "We assess with moderate confidence that Medusa poses a credible threat to firms in our sector."
- Assumption (hidden): "[Organization] uses SonicWall appliances." (Do they? Has the analyst verified this? If not, recommendations based on SonicWall CVEs are built on an assumption the consumer may not share.)

**If a claim fails any gate:** it doesn't go in as-is. The analyst either finds a source (Gate 1), verifies currency (Gate 2), ties it to the requirement (Gate 3), assigns a confidence level with reasoning (Gate 4), or makes the assumption explicit (Gate 5).

---

## Part 2: The Research Base Structural Gate

Once the analyst has built a research base using the claim-level test, the base itself needs a structural review before any derivatives are produced from it. This is the "is the whole greater than the sum of its parts" check.

### Seven Questions for the Research Base

**1. Does this research base answer the intelligence requirement?**

State the requirement in one sentence. Read the research base. Does it answer the question? If the analyst can't summarize the answer in 2-3 sentences after completing their research, the base isn't ready — it's a collection of facts, not intelligence.

**2. Are the key judgments clearly separated from the supporting evidence?**

The analyst should be able to point to their assessments (analytical judgments with confidence levels) as distinct from the facts that support them. If the assessments are buried inside long narrative paragraphs, they need to be extracted and stated explicitly.

**3. Are there competing hypotheses?**

Has the analyst considered alternative explanations? If the assessment is "supply-chain compromise is the most likely vector," has the analyst considered direct exploitation and credential theft as alternatives? What evidence supports or weakens each? If only one hypothesis was considered, the analysis is incomplete.

**4. Are the sources diverse?**

Is the analyst relying on a single vendor's reporting? A research base built entirely from CrowdStrike reports will reflect CrowdStrike's visibility and biases. Multiple independent sources (government advisories, multiple vendor reports, dark web monitoring, incident data) produce more reliable assessments.

**5. Are collection gaps documented?**

What couldn't the analyst find? What questions remain unanswered? What sources were unavailable? Documenting gaps is not a weakness — it's a sign of analytical maturity. It tells the consumer where the uncertainty lives and what additional collection might improve the assessment.

**6. Is anything included that the analyst can't defend?**

If a senior reviewer asked "why is this in here?" about any section, could the analyst answer with a specific reason tied to the intelligence requirement? If not, the section doesn't belong.

**7. Are all assumptions explicit?**

Read the research base looking specifically for unstated assumptions. Common hiding places: assumed technology stack ("our VPN appliances"), assumed threat actor motivation ("financially motivated"), assumed organizational exposure ("we are a high-value target"), assumed defensive posture ("our EDR would detect this"). Every assumption should be stated and, where possible, verified.

---

## Part 3: Applying This in Practice

### For the Analyst

Before writing anything, state the intelligence requirement in one sentence. Write it at the top of the research document. Every claim that enters the base should visibly serve that requirement.

As you research, tag each claim:

- **[SOURCED]** — includes specific attribution
- **[CURRENT]** — verified against reporting period
- **[RELEVANT]** — tied to the intelligence requirement
- **[CONFIDENCE: L/M/H]** — with stated reasoning
- **[FACT / ASSESSMENT / ASSUMPTION]** — explicitly labeled

This tagging is internal discipline, not formatting for the final product. It forces the analyst to evaluate every claim as it enters the base rather than evaluating the whole report after it's written (by which point they're invested in keeping everything).

### For the Reviewer

The reviewer's job is not to rewrite the analyst's work. It's to challenge the analysis using the structural gate questions. A useful review format:

- Does this answer the requirement? (Yes/No — if No, stop here)
- What are the key judgments? Can I find them quickly?
- What's the confidence level and do I agree with the reasoning?
- What alternatives were considered?
- What assumptions am I being asked to accept?
- What gaps should the consumer know about?

If the reviewer can answer these questions from the research base, the base is ready for derivatives. If not, it goes back to the analyst with specific questions — not "make it shorter" but "what's your confidence level on this claim and what supports it?"

---

## How This Relates to the Source-to-Derivative Model

This framework solves a different problem than the source-to-derivative workflow proposal. They work together:

| Problem | Solution |
|---|---|
| Good research, bad delivery | Source-to-derivative model (workflow fix) |
| Bad research, long reports | This framework (analytical tradecraft fix) |

If the research base is poor, no amount of derivative formatting will fix it. This framework ensures the source layer is worth deriving from. Once it is, the source-to-derivative model ensures the right intelligence reaches the right consumer in the right form.

---

## Influences and References

- **Lenny Zeltser** — *Rating Sheet for the Right Information: Threat Reports* (SEC402). The question-based inclusion approach for threat report content directly influenced the claim-level gate structure. [zeltser.com](https://zeltser.com)
- **Lenny Zeltser** — *Top 10 Writing Mistakes in Cybersecurity* (SANS Webcast). Mistake #9 (including details most readers don't need) and Mistake #10 (not giving credit) inform Gates 3 and 1 respectively. [youtube.com/watch?v=V7lO7UgxQV4](https://www.youtube.com/watch?v=V7lO7UgxQV4)
- **Robert M. Lee** — *Structuring Cyber Threat Intelligence Assessments*. The confidence level framework (Low/Moderate/High) and the principle that low confidence assessments are valid and useful directly inform Gate 4. The inverted pyramid model of assessment distribution is a useful benchmark for reviewer calibration. [robertmlee.org](https://www.robertmlee.org/structuring-cyber-threat-intelligence-assessments-musings-and-recommendations/)
- **Andrew VanVleet / TIRED Labs** — The DDM inclusion test (Essential + Immutable + Observable) provided the structural model for a compound gateway filter where a claim must pass all gates, not just some. The Phase 1 vs. Phase 4 distinction and Pitfall #11 (Phase 1 Artifact Leakage) reinforce the separation between research and deliverables. [library.tired-labs.org](https://library.tired-labs.org)
- **SANS FOR578: Cyber Threat Intelligence** — Intelligence cycle concepts, structured analytic techniques, and the principle that intelligence exists to serve the consumer's requirement, not the analyst's curiosity. [sans.org/cyber-security-courses/cyber-threat-intelligence](https://www.sans.org/cyber-security-courses/cyber-threat-intelligence)
