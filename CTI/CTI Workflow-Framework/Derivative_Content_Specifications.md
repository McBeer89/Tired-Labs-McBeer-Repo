# Derivative Content Specifications by Discipline

What Detection Engineering, Incident Response, and Red Team / Emulation need the CTI team to include in their derivative deliverables — and why each element matters to the consuming discipline.

---

## Detection Engineering Brief

**Consumer:** Detection engineers, SOC engineering, SIEM/EDR query developers  
**Question answered:** What should we build detections against, in what priority order, and with what telemetry?

### Required Content

**1. Detection Priority Ranking**

Every technique or behavior in the brief must be ranked. Detection engineers operate under resource constraints — they can't build everything at once, so the CTI team needs to tell them what matters most. Priority should be driven by prevalence across active threat groups relevant to the organization, not by abstract severity.

| Priority | Criteria |
|---|---|
| P1 | Observed across multiple active groups targeting our sector; high likelihood of encounter |
| P2 | Group-specific but high-impact if encountered; or emerging TTP with increasing adoption |
| P3 | Late-stage indicators (encryption, destruction) — the attack is advanced, but detection still enables containment |

**2. Per-Technique Detection Table**

For each prioritized technique, the brief must include a table with three columns: what to detect, which telemetry source observes it, and operational notes.

- **What to Detect**: The observable behavior, not the tool name. "LSASS process access from non-standard parent process" — not "Mimikatz execution." The detection engineer needs to know what the system does, not what the attacker calls their tool.
- **Telemetry Source**: The specific log source and event. Use descriptive labels: `Sysmon 1 (ProcessCreate)`, `Windows 4769 (Kerberos TGS Request)`, `IIS W3C Extended Log`. Not just "Sysmon" or "Windows event logs." The detection engineer needs to know exactly which event ID to query.
- **Notes**: Tuning context — known false positive sources, baselining requirements, renamed binary considerations, environmental prerequisites. This is where the CTI team saves the detection engineer hours of trial and error.

**3. Group-Specific Behavioral Indicators**

When a threat group has a signature behavior that differs from the generic technique, call it out separately. These are not IOCs (which rotate) — they're behavioral patterns that persist across campaigns. Examples: a group that always creates a local account with a specific username, a group that always modifies a specific registry key, a group that chains multiple RMM tools on a single host. These are high-fidelity detection opportunities that the detection engineer won't find in a generic ATT&CK write-up.

**4. ATT&CK Coverage Map**

A summary table mapping every technique from the research base to whether the brief covers it, detection feasibility (High / Medium / Low), and the assigned priority. This gives the detection engineer the full picture — not just what to build, but what's not covered and why. Techniques with no feasible detection should still appear in the table with an explanation (e.g., "depends on edge device vendor logging" or "indistinguishable from legitimate use without additional context").

**5. Detection Gaps**

Explicit identification of techniques or behaviors that cannot be detected with available telemetry. Each gap should state: what's missing, why it's a gap (telemetry not collected, no distinguishing observable, requires correlation across sources not currently joined), and what would close it. This feeds directly into the detection engineer's backlog and into requests to the infrastructure team for additional log sources.

**6. Telemetry Dependency Checklist**

A table listing every telemetry source the detections depend on, what it's required for, and a confirmation status field. The detection engineer needs to validate that the data is actually being collected and forwarded to the SIEM before building queries against it. Without this checklist, the engineer discovers missing telemetry after spending hours writing a query that returns zero results.

**7. Detection Classification (When Applicable)**

If the environment context is known, classify each detection:

| Classification | Meaning |
|---|---|
| Inherently Suspicious | Almost always malicious regardless of environment |
| Suspicious Here | No legitimate use in this specific environment |
| Suspicious in Context | Has legitimate uses; requires additional context or correlation |

This classification tells the detection engineer how much tuning to expect and whether the detection can stand alone or needs enrichment.

### What Does NOT Belong

- IOCs (IP addresses, domain names, file hashes) — these rotate and belong in the Tactical IOC Package, not the detection brief
- Threat actor background narrative — the detection engineer doesn't need three paragraphs on the group's history to write a query
- Remediation guidance — that's the IR brief's job
- Regulatory context — that's the compliance brief's job
- Confidence levels on individual detections — the detection either works technically or it doesn't; confidence applies to the threat assessment, not the detection logic

---

## IR Preparedness Brief

**Consumer:** Incident response team, IR lead, forensic analysts  
**Question answered:** What does the attack look like end-to-end, what artifacts should we expect at each phase, and what are our containment priorities?

### Required Content

**1. Kill Chain Summary**

A visual or structured overview of the complete attack lifecycle for the threat in question. This should show the full chain from initial access through impact, with group-specific variations noted. The IR team uses this as a mental model when they're in the middle of an incident — it tells them what happened before the phase they're currently investigating, and what's likely coming next.

The summary should include a critical timing note for any phase where the sequence matters for response decisions. Example: if exfiltration completes before encryption, the IR team needs to know that detecting encryption means exfiltration already happened.

**2. Phase-by-Phase Artifact Tables**

For each phase of the kill chain, the brief must include:

- **What happened**: A plain-language description of what the attacker did in this phase. One to two sentences.
- **Pathway variants**: If there are multiple methods for the same phase (e.g., three different initial access vectors), present them as rows in a table with distinct artifact signatures for each.
- **Artifacts to look for**: Specific, concrete forensic artifacts — not "check the logs" but "Windows Event 4720 (User Account Created) with username `itadm`" or "Rclone config file in `C:\ProgramData\` containing attacker cloud storage credentials." The IR analyst needs to know exactly what to search for, in what log or file system location.
- **Investigative question**: One question per phase that captures the critical unknown the IR team needs to resolve before moving on. "How did the attacker get in?" "What credentials were compromised?" "Which systems did the attacker access?" "What data was exfiltrated?" These questions drive the investigation's structure.

**3. Group-Specific Indicators**

When a threat group leaves a signature artifact (a specific username, a specific ransom note filename, a specific file extension, a specific tool or tool configuration), the brief should call it out at the relevant phase. These let the IR team identify which group they're dealing with during a live incident, which informs what to expect in subsequent phases.

**4. High-Value Target List**

Which systems the attacker is likely targeting for access: domain controllers, hypervisors, backup servers, file servers, database servers. This isn't generic — it should be informed by the specific threat group's known preferences and the attack's objectives. The IR team uses this list to prioritize which systems get forensic review first.

**5. Containment Priority Sequence**

A numbered, time-critical sequence of containment actions. This is not a general incident response playbook — it's specific to the threat being briefed. The sequence should account for the attacker's likely persistence mechanisms, the credential exposure scope, and the exfiltration channels in use. Each step should be actionable without requiring further research.

Key elements the sequence must address in order:
- Network isolation of compromised hosts (with note to preserve volatile memory)
- Account disablement and credential reset scope (including KRBTGT double-reset if domain compromise is confirmed)
- C2 and exfiltration channel blocking (specific protocols, domains, cloud storage providers)
- Persistence mechanism removal (specific mechanisms to search for, informed by the group's known TTPs)
- Initial access vector remediation (patch or disable before restoring services)
- Legal and compliance notification triggers (with specific timelines — SEC 8-K, CIRCIA, state AG)

**6. Evidence Preservation Checklist**

A checkbox-style list of evidence to preserve before systems are rebuilt or reimaged. This is the IR team's "don't forget" list under pressure. It should include: memory images, configuration files that may contain attacker data (e.g., Rclone configs with cloud credentials), ransom notes, appliance logs covering the intrusion window, Windows event logs from all systems in the blast radius, EDR telemetry exports, network flow logs for the exfiltration window, copies of attacker tools and scripts, and any email gateway logs if phishing was the vector.

**7. Regulatory and Notification Triggers**

The IR team needs to know what triggers mandatory reporting, with specific timelines. This isn't legal advice — it's the factual context the IR team needs to escalate appropriately. Include the relevant regulatory frameworks (SEC, FINRA, NYDFS, CIRCIA, state AG breach notification), the triggering conditions, and the clock (e.g., 4 business days for SEC 8-K, 24 hours for CIRCIA ransomware payment reporting). The IR team doesn't make the notification decision — Legal does — but IR needs to know when to escalate to Legal and what information Legal will need.

### What Does NOT Belong

- Detection logic or SIEM queries — that's the detection brief's job
- Strategic risk assessment or prioritization guidance — that's the executive brief's job
- Full threat actor profiles or historical campaign summaries — the IR team needs to know what this group does, not where they came from
- Generic incident response procedures that aren't specific to this threat — the IR team already has playbooks; this brief supplements them with threat-specific detail

---

## Red Team / Emulation Brief

**Consumer:** Red team, purple team, adversary emulation leads  
**Question answered:** How does this adversary actually operate, in what sequence, and what should a realistic emulation look like?

### Required Content

**1. Adversary Profile (Operational, Not Strategic)**

A concise operational profile of the threat group being emulated. This is not a strategic intelligence summary — it's the information the red team needs to build a realistic emulation plan. Include: the group's typical targets and objectives, their known operational tempo (hours to days? weeks?), whether they operate as a RaaS with affiliates (which means TTP variation across campaigns), and any known constraints or preferences that affect emulation design.

**2. Attack Chain Sequence**

The full attack lifecycle in operational order, with enough detail for the red team to design an emulation plan. For each phase:

- **Technique and sub-technique IDs**: ATT&CK mapping for each step.
- **Procedure-level detail**: Not just "credential access" but "Mimikatz `sekurlsa::logonpasswords` against LSASS, followed by Kerberoasting targeting service accounts with SPNs." The red team needs to know *how* the adversary does it, not just *what* they do.
- **Tool-to-technique mapping**: What tools the adversary uses for each step, and what open-source or commercial alternatives the red team can substitute. Example: "Akira uses Mimikatz for credential harvesting. Emulation alternatives: Rubeus (Kerberoasting), Nanodump (LSASS dump), or direct LSASS access via ProcDump." The red team may not have (or want to use) the exact tool, but they need to produce the same telemetry footprint.
- **Sequencing notes**: What must happen before what. "Credential harvest happens after foothold but before lateral movement" is obvious. "BYOVD driver load happens immediately before encryption, not during initial foothold" is not obvious and affects emulation timing.

**3. Initial Access Specifics**

Detail on the adversary's preferred initial access methods with enough specificity for the red team to replicate or simulate. Include: the specific CVEs exploited (with affected products and versions), whether the adversary uses purchased credentials from IABs (and if so, what kind — VPN creds, RDP creds, SSO tokens), and any social engineering methods observed. The red team uses this to design realistic initial access scenarios for the engagement, or to agree with the blue team on an assumed breach starting point that matches the adversary's actual behavior.

**4. C2 and Infrastructure Patterns**

How the adversary maintains command and control, with enough detail for the red team to replicate the network footprint:

- C2 frameworks used (Cobalt Strike, Sliver, Brute Ratel, etc.)
- Communication protocols and ports (HTTPS on 443, DNS tunneling, mTLS)
- Beaconing patterns (jitter, sleep intervals if known)
- RMM tools used for redundant access (AnyDesk, ScreenConnect, MeshAgent)
- Whether the adversary uses legitimate cloud infrastructure for C2 (Azure, AWS, Cloudflare tunnels)

The red team needs this to generate realistic C2 traffic that the blue team's network monitoring should detect.

**5. Evasion Techniques**

What the adversary does to avoid detection, in enough detail for the red team to replicate:

- Binary renaming (e.g., Rclone renamed to `svchost.exe`)
- Packing or obfuscation (Themida packing on Mimikatz)
- BYOVD / EDR tampering (specific vulnerable drivers used, specific kill tool)
- Living-off-the-land binaries (LOLBins) used
- Log clearing or timestamp manipulation

This is critical for purple team exercises — the red team needs to use the same evasion techniques so the blue team can validate whether their detections survive the adversary's actual evasion approach.

**6. Detection Brief Cross-Reference**

The emulation brief should explicitly reference the corresponding Detection Engineering Brief and identify which detections should fire at each phase of the emulation. This turns the emulation into a validation exercise: the red team executes the adversary's TTPs, and the blue team verifies that the detections in the Detection Brief actually trigger.

Format this as a mapping table:

| Emulation Phase | Technique | Expected Detection | Detection Brief Reference |
|---|---|---|---|
| Foothold | T1219 — RMM tool install | Unauthorized RMM tool execution | DET-####, Priority 1 |
| Credential Harvest | T1003 — LSASS access | Sysmon 10 alert on LSASS access | DET-####, Priority 1 |
| Exfiltration | T1567 — Rclone to cloud | Rclone CLI args + outbound to MEGA | DET-####, Priority 1 |

The red team uses this table to confirm that every emulation step has a corresponding detection expectation. Phases where no detection exists are the gaps — and those gaps are the most valuable finding of the exercise.

**7. Environmental Prerequisites**

What needs to be true in the emulation environment for the test to be realistic:

- Target systems that match the adversary's known preferences (e.g., if the group targets ESXi, the emulation needs a hypervisor in scope)
- Credential types the adversary harvests (domain admin, service accounts, Veeam credentials) — the emulation environment needs these to exist
- Network segmentation assumptions (can the red team reach backup infrastructure? Domain controllers? The DMZ?)
- Telemetry that must be active for the detection validation to work (Sysmon, specific Windows audit policies, network flow logging)

Without this section, the red team may design an emulation that doesn't match the adversary's actual operating conditions, or the blue team may not have the right telemetry enabled to validate the detections.

**8. Success Criteria**

What "successful emulation" means for each phase. This isn't "did the red team get domain admin" — it's "did the emulation produce the same artifacts and telemetry footprint that the real adversary would produce?" The red team and blue team should agree on success criteria before the exercise starts. Include:

- Per-phase: "This phase is successfully emulated when [specific artifact] is generated and [specific detection] either fires or demonstrably fails."
- Overall: "The emulation is complete when all phases have been executed and the detection coverage map has been validated or updated with confirmed gaps."

### What Does NOT Belong

- Strategic threat assessment or risk prioritization — the red team needs operational detail, not business context
- IOCs from past campaigns — the red team generates their own infrastructure; they don't reuse attacker IOCs
- Compliance or regulatory context — irrelevant to emulation design
- Detection tuning guidance — that's feedback the blue team produces after the exercise, not input the red team needs before it
- Generic red team methodology — the emulation team already knows how to run an engagement; this brief tells them how *this specific adversary* operates

---

## Cross-Derivative Dependencies

The three derivatives are not independent — they form a validation loop:

```
CTI Research Base
       │
       ├──→ Detection Brief ──────────────────────┐
       │     (what to detect)                      │
       │                                           ▼
       ├──→ Emulation Brief ──→ Red Team ──→ Did detections fire?
       │     (how to emulate)    executes      │
       │                                       │ Yes → Detection validated
       │                                       │ No  → Gap identified
       │                                           │
       └──→ IR Brief ◄────────────────────────────┘
              (what the attack looks like)     Gaps feed back into
              Updated with findings from       detection engineering
              emulation and real incidents      and IR preparedness
```

The Detection Brief tells the blue team what to build. The Emulation Brief tells the red team how to test it. The IR Brief tells the response team what to expect when it's real. Findings from emulation exercises and real incidents feed back into all three. This loop only works if the derivatives reference each other — the emulation brief must cite the detection brief, and findings from exercises must update the IR brief.
