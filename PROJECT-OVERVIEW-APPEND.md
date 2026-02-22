# TIRED Labs — Expanded Scope & Discipline-Neutral Framing

> **Note:** This document supplements the existing `PROJECT-OVERVIEW.md` file.
> It does not replace it. `PROJECT-OVERVIEW.md` covers the analytical
> methodology (DDMs, procedures, compound probability, identification vs.
> classification). This addendum captures the broader organizational vision
> of TIRED Labs that is not yet reflected in published materials.

---

## Purpose of This Document

This briefing captures the broader organizational vision of TIRED Labs beyond
what is currently available in the published article series. The published
Threat Detection Engineering series by Andrew VanVleet focuses heavily on
detection strategy and detection engineering applications, which reflects the
author's professional background — but the TIRED Labs project itself has a
wider scope that is not yet fully documented in public materials.

This information was provided through direct communication with one of the
TIRED Labs founders and should be used to contextualize any work involving
TRRs, DDMs, or the TIRED Labs methodology.

---

## What TIRED Stands For

**T**hreat **I**ntelligence, **R**esponse, **E**mulation, and **D**etection.

These four disciplines represent the full scope of the project. TIRED Labs is
not a detection engineering project — it is a **purple team collaboration
framework** where all security disciplines work from shared source material.

---

## The Core Insight: TRRs Are Discipline-Neutral

A Technique Research Report (TRR) documents how an attack technique works at
the essential operation level. It captures the technical background, the
Detection Data Model (DDM), and the distinct procedures — nothing more.

A TRR does **not** contain:
- Detection strategy or detection recommendations
- Hunt hypotheses or hunt playbooks
- Emulation scripts or red team guidance
- Incident response procedures or forensic artifact analysis
- Threat intelligence assessments or attribution

A TRR is **source material**. Each team produces their own discipline-specific
documents from it:

| Team | Derivative Document | What It Contains |
|------|-------------------|------------------|
| Detection Engineering | Detection Methods | Detection specifications, telemetry selection, classification guidance, coverage matrix, blind spot analysis |
| Threat Hunting | Hunt Playbook | Hypothesis-driven hunt procedures derived from DDM operations |
| Red Team / Emulation | Emulation Plan | Per-procedure execution steps, tooling, expected artifacts |
| Incident Response | IR Runbook | Forensic artifacts, investigation steps, containment guidance |
| Threat Intelligence | Threat Brief | Technique context, actor usage, campaign relevance |

This separation is fundamental to the methodology. When detection
considerations were merged into a TRR during development of TRR0000, the
founders' feedback was clear: detection belongs as its own derivative
document. The TRR stays general and direct; teams build out from it.

---

## Why This Matters for AI-Assisted Research

The published article series establishes the analytical foundations — DDM
inclusion test, procedure vs. instance distinction, compound probability,
identification vs. classification, incremental coverage — but frames nearly
everything through a detection engineering lens. An AI model reading only the
published articles would reasonably conclude that TRRs are detection
documents. They are not.

When producing or reviewing TRRs, apply these rules:

1. **No detection-oriented language in TRR prose.** Do not write "detection
   opportunity," "high-fidelity signal," or "detection gold mine." State
   technical facts and let teams draw their own conclusions.

2. **No team-specific recommendations.** Do not suggest what to monitor, what
   to hunt for, what to emulate, or how to respond. Document the technique.

3. **Technical Background serves all readers equally.** An intelligence
   analyst, a red teamer, a detection engineer, and an incident responder
   should all find the information they need in the same document.

4. **Procedure narratives describe what happens, not what to do about it.**
   State the essential operations, the technical mechanics, and what makes
   each procedure distinct. Stop there.

5. **Derivative documents are separate files.** They reference the TRR as
   their source. They are not appendices or sections within the TRR.

---

## Current State of the Project

The public TRR Library (https://library.tired-labs.org) contains published
TRRs contributed by VanVleet and community members. The published methodology
articles cover the strategic framework and detection-focused applications. The
broader TIRED Labs organizational documentation — covering the full
intelligence/response/emulation/detection workflow and inter-team
collaboration model — is not yet publicly available. The project is actively
developing toward this fuller vision.


