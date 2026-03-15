# Derivative Use Cases by Discipline

Why Detection Engineering, Incident Response, and Red Team / Emulation need dedicated CTI derivatives — and what breaks when they don't have them.

---

## Detection Engineering

**Without a dedicated derivative:** Detection engineers either get nothing from CTI and do their own research, or get a 12-page report and dig through it looking for the three things they need. Either way they're doing CTI's job for them.

**Prioritized Detection Backlog.** Limited engineering hours, unlimited techniques. The Detection Brief ranks what to build by what's actually being used against the organization's sector right now — not what's technically interesting or trending at conferences.

**Telemetry Gap Discovery.** The brief lists every log source the detections depend on with a confirmation status. The engineer knows what's buildable today versus what needs an infrastructure request first — before they waste hours on a query that returns nothing.

**Behavioral Detection Framing.** Reports say "the attacker used Mimikatz." The brief says "LSASS process access from a non-standard parent." Behavioral framing survives tool changes, renaming, and packing. The CTI team has already abstracted from tool to behavior — the brief delivers it detection-ready.

**Group-Specific High-Fidelity Detections.** Some groups always create the same local account name, always modify the same registry key, always chain tools the same way. These don't appear in generic ATT&CK write-ups. Low false positive, high signal — only available from CTI tracking group-level behavior.

**Coverage Mapping.** Shows what's covered, what's not, and whether gaps are closable (missing telemetry) or inherent (indistinguishable from legitimate). Without this, the detection team knows what they've built but not what they're missing.

---

## Incident Response

**Without a dedicated derivative:** When an incident hits, the IR lead reads through pages of strategic context and detection guidance to find the forensic artifacts they need in the first hour. The general report isn't organized by attack phase, doesn't call out specific artifacts by log location, and doesn't include a containment sequence.

**Rapid Incident Scoping.** IR identifies the threat group from a ransom note or file extension, pulls the IR Brief, and has the full kill chain — what happened before the phase they're seeing, what's coming next, what artifacts to check at each phase. Pre-built, not assembled mid-incident from Google searches.

**Blast Radius Determination.** The brief includes a high-value target list based on the specific group's preferences. If this group targets Veeam and ESXi, IR checks those first instead of treating every system equally.

**Containment Sequencing.** Containment has an order. Isolating hosts before disabling accounts leaves credentials active elsewhere. The brief provides a sequence specific to this threat's persistence mechanisms, credential patterns, and exfiltration channels.

**Evidence Preservation.** The business pushes to reimage fast. The brief includes a checklist of artifacts to capture before rebuild — including non-obvious items like Rclone config files with attacker cloud credentials. A safety net under pressure.

**Regulatory Escalation Triggers.** IR doesn't make the notification call — Legal does. But IR needs to know when to escalate and what Legal will need. The brief includes specific timelines: SEC 8-K (4 business days), CIRCIA (24 hours for payment reporting), state AG notification.

**Tabletop Exercise Design.** Outside incidents, the kill chain, artifacts, containment sequence, and regulatory triggers become a ready-made exercise scenario built from real intelligence instead of hypotheticals.

---

## Red Team / Emulation

**Without a dedicated derivative:** Red teams default to emulating whatever's interesting or building plans from public reporting — doing their own CTI analysis to extract procedure-level detail. Neither guarantees the emulation reflects the actual threat to the organization.

**Threat-Informed Emulation Planning.** The brief provides a specific adversary's full attack chain at procedure level — initial access, C2, credential harvesting, lateral movement, evasion, exfiltration. The red team designs the engagement around the adversary most likely to target the organization, not a generic attack chain.

**Detection Validation (Purple Team Loop).** The brief cross-references the Detection Brief — each emulation phase maps to the detection that should fire. Execute the TTPs, check what triggers, confirm what doesn't. This is the highest-value output: closing the loop between "what we think we detect" and "what we actually detect."

**Realistic Evasion Testing.** The brief includes the group's specific evasion techniques — binary renaming, packing, BYOVD with specific drivers, LOLBins. The red team replicates these so the blue team validates whether detections survive the adversary's actual evasion, not just clean tool execution in a lab.

**Scoping Emulation Environments.** If the adversary targets Veeam, the engagement needs Veeam in scope. If they Kerberoast, the environment needs service accounts with SPNs. The brief provides threat-informed scoping requirements so the red team doesn't discover mid-engagement that the environment doesn't support the emulation.

**Measuring Defensive Progress.** Repeated emulations against updated CTI produce a time series — which detections fired this quarter versus last, which gaps persisted. Empirical measurement of defensive improvement, not abstract maturity percentages.

**Engagement Reporting That Maps to Detections.** Reframes the report from "here's what we broke" to "here's what the adversary would get away with and here's what the blue team needs to fix." Red team findings become detection engineering work items.

---

## The Common Thread

Each discipline needs specific CTI output formatted for their workflow, delivered before they need it. Without dedicated derivatives, detection engineers do their own threat research, IR teams parse general reports during active incidents, and red teams emulate threats they picked themselves. The CTI team has already done the research — the derivative model delivers the right slice to each discipline in the format they can act on.
