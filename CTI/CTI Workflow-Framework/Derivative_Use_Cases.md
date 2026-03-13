# Derivative Use Cases by Discipline

Why Detection Engineering, Incident Response, and Red Team / Emulation need dedicated CTI derivatives — and what breaks when they don't have them.

---

## Detection Engineering

### The Problem Without a Dedicated Derivative

Detection engineers today get one of two things from CTI: nothing (they read public threat reports themselves and translate on their own), or a general-purpose threat report that buries the three things they need inside twelve pages of context they don't. Either way, the detection engineer is doing CTI's job for them — extracting the detection-relevant content, mapping it to telemetry, figuring out priority, and discovering halfway through that the telemetry they need isn't being collected.

### Use Cases

**Use Case 1: Prioritized Detection Backlog**

The detection team has limited engineering hours. They can't build detections for every technique in the ATT&CK matrix simultaneously. The Detection Brief gives them a ranked backlog driven by actual threat intelligence — what's being used against organizations like ours, by which groups, right now. Without this, the detection team either builds based on what's technically interesting (not necessarily what's relevant) or defaults to whatever the last conference talk was about.

*What this replaces:* The detection engineer reading five vendor blogs, mentally ranking the techniques, and hoping they picked the right priority. The CTI team has already done the cross-source analysis — the Detection Brief delivers the conclusion.

**Use Case 2: Telemetry Gap Discovery Before Query Development**

Every detection depends on telemetry that may or may not exist in the environment. The Detection Brief includes a telemetry dependency checklist that forces the question "is this data actually being collected?" before the engineer writes a single line of KQL. Without this, the engineer discovers the gap after investing hours in a query that returns zero results — then has to go back to the infrastructure team, wait for log forwarding to be configured, and start over.

*What this replaces:* Trial and error. The Detection Brief front-loads the infrastructure dependencies so the engineer knows what's buildable today and what requires a prerequisite conversation with another team.

**Use Case 3: Behavioral Detection Over Signature Detection**

Generic threat reports describe attacks in terms of tools: "the attacker used Mimikatz." The Detection Brief describes attacks in terms of observable behaviors: "LSASS process access from a non-standard parent process." The behavioral framing is what the detection engineer actually needs — it produces detections that survive tool changes, binary renaming, and packing. A detection for "Mimikatz.exe" breaks the moment the attacker renames the binary. A detection for "unexpected LSASS access" catches Mimikatz, Nanodump, ProcDump, and the next tool that doesn't exist yet.

*What this replaces:* The engineer translating tool-centric reporting into behavioral detections on their own, which requires the engineer to understand the underlying technique deeply enough to abstract away from the tool. The CTI team has already done this abstraction in the research base — the Detection Brief delivers it in detection-ready form.

**Use Case 4: Group-Specific High-Fidelity Detections**

Some threat groups have behavioral signatures that are more specific than the generic ATT&CK technique — a group that always creates a local account with a specific username, a group that always modifies a specific registry key, a group that chains specific tools in a specific order. These are high-fidelity detection opportunities with very low false positive rates. They don't appear in generic ATT&CK coverage because they're group-specific. The Detection Brief surfaces them because the CTI team tracks group-level behavior, not just technique-level behavior.

*What this replaces:* Nothing — this intelligence doesn't exist in any public report in a detection-ready format. The CTI team's research base is the only place where group-specific behavioral patterns are tracked, correlated, and delivered as detection opportunities.

**Use Case 5: Detection Coverage Mapping**

The Detection Brief includes an ATT&CK coverage map that shows not just what's covered but what's *not* covered and why. This gives the detection team a clear picture of where they have coverage, where they have gaps, and whether those gaps are closable (missing telemetry) or inherent (technique is indistinguishable from legitimate activity). Without this, the detection team's coverage map is based on what they've built, not on what the threat landscape requires — they know what they've done but not what they're missing.

*What this replaces:* The detection team building their own coverage assessment by reverse-engineering threat reports. The CTI team has already mapped the threat landscape to techniques; the Detection Brief delivers the gap analysis.

---

## Incident Response

### The Problem Without a Dedicated Derivative

When an incident hits, the IR team needs to know what the attack looks like — fast. If the only CTI product available is a general threat report, the IR lead has to read through pages of strategic context, threat actor history, and detection guidance to extract the forensic artifacts and kill chain detail they need in the first hour of response. Worse, the general report may not organize information by attack phase, may not call out specific artifacts by log source and event ID, and almost certainly doesn't include a containment priority sequence specific to this threat.

### Use Cases

**Use Case 1: Rapid Incident Scoping**

The IR team confirms a ransomware intrusion is underway. The first question is: "what are we dealing with?" If they can identify the threat group (from a ransom note filename, a specific local account, a specific file extension), the IR Preparedness Brief for that group tells them the full kill chain — what happened before the phase they're seeing, what's likely coming next, and what artifacts to look for at each phase. This turns a reactive investigation into a structured response within the first hour.

*What this replaces:* The IR lead Googling the ransom note text, reading three vendor blog posts during an active incident, and assembling a mental model of the kill chain on the fly. The IR Brief delivers that model pre-built, with artifacts already mapped to phases.

**Use Case 2: Blast Radius Determination**

The IR team needs to determine which systems the attacker accessed. The IR Brief includes a high-value target list informed by the specific group's known preferences — if this group targets ESXi hypervisors and Veeam backup servers, the IR team checks those first. Without this, the IR team checks everything equally, which means the systems the attacker most likely compromised get the same forensic priority as systems the attacker probably ignored.

*What this replaces:* Generic "check your domain controllers" guidance that doesn't account for what this specific adversary actually does. The IR Brief tailors the investigation priorities to the threat.

**Use Case 3: Containment Sequencing**

Containment actions have an order. Isolating hosts before disabling accounts may leave the attacker with valid credentials on systems you haven't found yet. Disabling accounts before blocking C2 may trigger the attacker to accelerate encryption. Patching the initial access vector before removing persistence is wasted effort if the attacker has four other ways in. The IR Brief provides a containment priority sequence specific to the threat — informed by the group's known persistence mechanisms, credential exposure patterns, and exfiltration channels.

*What this replaces:* The IR team following a generic playbook that isn't informed by the specific adversary's behavior. Generic playbooks cover the steps; the IR Brief tells you the order and the threat-specific considerations at each step.

**Use Case 4: Evidence Preservation Under Pressure**

During an active incident, the pressure to rebuild and restore is intense. Business leadership wants systems back online. The IR Brief includes an evidence preservation checklist — specific artifacts to capture before systems are reimaged. This includes non-obvious items that matter for this specific threat: Rclone configuration files that may contain the attacker's cloud storage credentials, specific log windows that cover the intrusion timeline, volatile memory that must be captured before reboot. Without this checklist, critical evidence gets destroyed in the rush to restore.

*What this replaces:* The IR team relying on memory and experience under pressure. The checklist is a safety net — it catches the evidence that gets overlooked when the team is moving fast.

**Use Case 5: Regulatory Escalation Triggers**

The IR team doesn't make the notification decision — Legal does. But the IR team needs to know *when* to escalate to Legal and *what information Legal will need*. The IR Brief includes regulatory trigger points with specific timelines: SEC 8-K (4 business days for material incidents), CIRCIA (24 hours for ransomware payment reporting), state AG breach notification, FINRA obligations. Without this, the IR team either escalates too late (missing a regulatory deadline) or doesn't escalate at all because they didn't realize a reporting obligation was triggered.

*What this replaces:* The IR lead calling Legal to ask "do we need to report this?" without knowing what the reporting thresholds are. The IR Brief gives the IR team the context to escalate with the right information at the right time.

**Use Case 6: Tabletop Exercise Design**

Outside of active incidents, the IR Brief serves as the foundation for realistic tabletop exercises. The kill chain, artifacts, containment sequence, and regulatory triggers are the exercise scenario — built from real threat intelligence, not hypothetical scenarios. This produces exercises that test the team against the threats they're most likely to face, with realistic decision points.

*What this replaces:* Generic tabletop scenarios that don't reflect the current threat landscape. The IR Brief provides a ready-made, intelligence-informed exercise scenario.

---

## Red Team / Emulation

### The Problem Without a Dedicated Derivative

Red teams that don't receive structured CTI derivatives default to one of two approaches: they emulate whatever they find interesting (which may not reflect the actual threat to the organization), or they build emulation plans from public threat reports (which requires them to do their own CTI analysis to extract procedure-level detail). Both approaches waste the red team's time on work the CTI team has already done, and neither guarantees that the emulation reflects the adversaries most likely to target the organization.

### Use Cases

**Use Case 1: Threat-Informed Emulation Planning**

The red team's engagement should emulate the adversaries most likely to target the organization — not a generic "advanced attacker" or whatever framework happens to ship with their C2 tool. The Emulation Brief provides the full attack chain for a specific threat group at procedure-level detail: which CVEs they exploit for initial access, which tools they use for C2, how they harvest credentials, what order they operate in, and how long the typical intrusion takes. This lets the red team design an engagement that produces a realistic test of the organization's defenses against its actual threat landscape.

*What this replaces:* The red team lead reading vendor reports, extracting TTP detail, mapping it to their tooling, and building an emulation plan — work the CTI team has already done. The Emulation Brief delivers the plan inputs.

**Use Case 2: Detection Validation (Purple Team Loop)**

The Emulation Brief explicitly cross-references the Detection Brief — mapping each emulation phase to the detection that should fire. This turns the red team engagement into a detection validation exercise: execute the adversary's TTPs, check whether each expected detection triggers. Phases where no detection fires are confirmed gaps. This is the highest-value output of the red team/CTI partnership — it closes the loop between "what we think we can detect" and "what we actually detect."

*What this replaces:* Red team engagements where the findings are "we got domain admin" without telling the blue team *which specific detections failed and why*. The cross-reference table makes detection validation systematic rather than anecdotal.

**Use Case 3: Realistic Evasion Testing**

The adversary doesn't just run tools — they evade defenses. The Emulation Brief includes the specific evasion techniques the group uses: binary renaming, packing, BYOVD driver loading, specific vulnerable drivers, LOLBin usage. The red team replicates these techniques so the blue team can validate whether their detections survive the adversary's actual evasion approach — not just whether they detect the clean, unmodified tool in a lab environment.

*What this replaces:* Red team engagements that use default tool configurations, which don't test whether detections survive evasion. The Emulation Brief tells the red team exactly how to make their tools look like the real adversary's tools.

**Use Case 4: Scoping Emulation Environments**

The Emulation Brief includes environmental prerequisites — what needs to exist in the emulation environment for the test to be realistic. If the adversary targets Veeam backup servers, the emulation environment needs Veeam. If the adversary harvests Kerberos service tickets, the environment needs service accounts with SPNs. If the adversary uses BYOVD, the blue team's driver-load monitoring needs to be active or the test is meaningless. Without this section, the red team discovers mid-engagement that the environment doesn't support the emulation they planned.

*What this replaces:* Engagement scoping meetings where the red team and blue team negotiate what's in scope without CTI input on what the adversary actually targets. The Emulation Brief provides the threat-informed scoping requirements.

**Use Case 5: Measuring Defensive Progress Over Time**

When the emulation is repeated quarterly or semi-annually against updated CTI, the results form a time series: which detections fired in Q1, which new detections fired in Q2 after the Detection Brief was updated, which gaps persisted. This is the most concrete measure of detection program maturity available — it's not a theoretical coverage percentage, it's empirical data on whether the organization can detect the adversaries targeting it.

*What this replaces:* Abstract maturity assessments based on framework coverage percentages. Repeated emulations with CTI-informed success criteria produce empirical, defensible measurements of defensive improvement.

**Use Case 6: Engagement Reporting That Maps to Detections**

Standard red team reports describe what the red team did and what worked. Emulation reports informed by the CTI derivative describe what the *adversary* does, what the red team replicated, and which *specific detections* succeeded or failed. This reframes the red team report from "here's what we broke" to "here's what the adversary would get away with and here's what the blue team needs to fix." The audience shifts from "look how good the red team is" to "here's the detection engineering backlog, prioritized by confirmed gap."

*What this replaces:* Red team reports that list findings without mapping them to the detection program. The Emulation Brief's cross-reference table turns red team findings into detection engineering work items.

---

## The Common Thread

Every use case above has the same underlying structure: a discipline needs specific CTI output, formatted for their workflow, delivered before they need it. Without dedicated derivatives:

- **Detection engineers** do their own threat intelligence analysis to figure out what to build. They're good at writing queries, not at cross-source threat analysis. Their time is misallocated.
- **IR teams** read general threat reports during active incidents to extract the forensic detail they need right now. They're good at investigating, not at parsing strategic assessments under pressure. Their response is slower.
- **Red teams** build emulation plans from public reporting without knowing which adversaries are most relevant to the organization. They're good at breaking things, not at determining what to break. Their engagements may not test the right threats.

The CTI team has already done the research. The derivative model delivers the right slice of that research to each discipline in the format they can act on — before they need it, not after.
