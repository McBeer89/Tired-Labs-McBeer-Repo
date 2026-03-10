# KQL Coverage & Query Reference — TRR0013 (Forge a Kerberos TGT, T1558.001)

## Procedure Coverage

| Procedure | Operations Covered | Operations Without Sentinel/Defender Telemetry |
|---|---|---|
| TRR0013.AD.A | n1 Receive Network Request / TGS-REQ (Event 4769, correlation) | n16 Forge TGT (none), n0 Send Network Request / TGS-REQ (none), n2 Send TCP Packet (IDS only), n3 Receive TCP Packet (none), n4 Send Network Response / TGS-REP (none), n5 Send TCP Packet (none), n6 Receive TCP Packet (none), n7 Receive Network Response / TGS-REP (none), n12 Send Network Request / AP-REQ (none), n14 Send TCP Packet (IDS only), n15 Receive TCP Packet (none), n13 Receive Network Request / AP-REQ (Event 4624, too generic) |
| TRR0013.AD.B | n1 Receive Network Request / U2U+S4U2Self TGS-REQ (Event 4769), n22 Receive Network Request / TGS-REQ (Event 4769, correlation) | n8 Send Network Request / AS-REQ (none), n9 Receive Network Request / AS-REQ (Event 4768, not distinctive alone), n17 Send Network Response / AS-REP (none), n20 Receive Network Response / AS-REP (none), n0 Send Network Request / U2U TGS-REQ (none), n4 Send Network Response / TGS-REP (none), n7 Receive Network Response / TGS-REP (none), n16 Forge TGT (none), n21 Send Network Request / TGS-REQ (none), n23 Send Network Response / TGS-REP (none), n24 Receive Network Response / TGS-REP (none), n12 Send Network Request / AP-REQ (none), n13 Receive Network Request / AP-REQ (Event 4624, too generic) |

## Table Dependencies

| Table | Platform | Required For |
|---|---|---|
| SecurityEvent | Microsoft Sentinel | Procedures A, B — Event 4769 (TGS-REQ), Event 4768 (TGT request, correlation baseline) |
| IdentityLogonEvents | Microsoft Defender for Identity | Procedures A, B — Kerberos authentication events (baseline) |

## Blind Spots

| Operation | DDM Node | Procedure | Telemetry Status |
|---|---|---|---|
| Forge TGT | n16 (A), n16 (B) | A, B | Offline local operation. No telemetry exists for the forging itself. |
| Send Network Request (TGS-REQ) | n0 (A, B), n21 (B) | A, B | Client-side send. No DC telemetry — the DC logs the receive side (n1, n22). |
| Send/Receive Network Response (TGS-REP) | n4, n7 (A); n4, n7, n23, n24 (B) | A, B | DC response delivery. No distinct telemetry beyond the Event 4769 logged at the TGS-REQ receive. |
| Send Network Request (AP-REQ) | n12 (A, B) | A, B | Client-side send. No telemetry — the service logs the receive side (n13). |
| Receive Network Request (AP-REQ) | n13 (A, B) | A, B | Event 4624 fires here, but it is indistinguishable from any legitimate Kerberos logon. No DDM-based immutable filter separates a forged-ticket logon from a legitimate one at this node. |
| Send/Receive TCP Packets | n2, n14 (A) | A | Network IDS only. Not queryable in Sentinel/Defender. |
| Send/Receive Network Request (AS-REQ/AS-REP) | n8, n9, n17, n20 (B) | B | Event 4768 fires at n9 for the LowPrivUser's legitimate TGT request. This event is expected and not anomalous — the low-priv user is a legitimate account. Queried only as correlation baseline, not as a standalone detection. |

## Telemetry Constraints

1. **Golden Ticket detection depends on attacker mistakes.** The TRR states: "If an attacker is careful to forge a ticket with all the details in a legitimate TGT issued by the domain's KDC, a Golden Ticket attack is likely impossible to detect." The correlation query (Event 4769 without preceding Event 4768) relies on the fundamental fact that the TGT was never issued, but this gap is only visible if the lookback window captures the absence. TGTs issued before the lookback window will produce false positives.

2. **Event 4769 for U2U+S4U2Self misrepresents the delegation.** The TRR documents that Windows event logging "fails to recognize the S4U delegation. The resulting log simply has the low privilege user as both the TargetUserName and the ServiceName, and the targeted higher privilege user fails to appear in the log at all." The high-privilege target is invisible in Event 4769.

3. **ENC-TKT-IN-SKEY (TicketOptions bit 0x8) is immutable for U2U.** Any U2U authentication exchange requires this flag. It is the only immutable, observable property that distinguishes the Sapphire Ticket's PAC acquisition TGS-REQ from a normal TGS-REQ.

4. **TargetUserName == ServiceName is immutable for S4U2Self.** The S4U2Self extension requests a ticket from a service to itself. Combined with ENC-TKT-IN-SKEY, this pattern is highly specific to U2U+S4U2Self and rare in legitimate environments.

5. **Event 4624 is not actionable for this technique.** Every Kerberos service ticket presentation produces Event 4624. There are no DDM-based immutable properties to distinguish a forged-ticket logon from a legitimate one at the AP-REQ receive node. Event 4624 is excluded from the query set.

6. **Lookback window limitations.** The correlation queries use `leftanti` joins to find Event 4769 without Event 4768 for the same user. A TGT issued before the lookback window will not appear in the `tgt_issuances` set, producing a false positive. The default domain TGT lifetime is 10 hours; a 24-hour lookback covers most cases but is not guaranteed. The detection team determines the appropriate window for their environment.

7. **Machine account volume.** Domain controllers and other machine accounts regularly request service tickets using TGTs that may have been issued by inter-DC replication or other background processes. The correlation query computes an `IsMachineAccount` flag for analysis without excluding results — the detection team determines exclusion policy.

8. **IdentityLogonEvents field granularity.** The Defender queries surface Kerberos events from Microsoft Defender for Identity but cannot replicate the Sentinel correlation (absent Event 4768) or Procedure B's TicketOptions parsing because these details may be embedded in `AdditionalFields` as a dynamic JSON column. The queries project `AdditionalFields` for manual inspection.

9. **TicketOptions hex parsing.** Procedure B Query 1 converts the TicketOptions hex string to an integer via `tolong()` for bitwise comparison. Azure Data Explorer's `tolong()` supports "0x"-prefixed hex strings, but behavior may vary across Sentinel workspace versions. If the query returns no results in a specific environment, verify that `tolong("0x40810008")` produces a non-null value. If it does not, extract the last character of the TicketOptions string and check for "8" as a fallback.

## Vendor-Specific Telemetry (Not Queried)

The following telemetry sources are documented in the DDM but are not queryable through Microsoft Sentinel or Defender. They are noted here for teams operating those platforms.

| Telemetry | DDM Node | Procedure | Platform | Notes |
|---|---|---|---|---|
| CS ActiveDirectoryServiceAccessRequest | n1 (A, B), n22 (B) | A, B | CrowdStrike Falcon IDP | Fires when a TGT is submitted to request a service ticket. For Procedure B, CrowdStrike properly identifies the S4U delegation and records the high-privilege user as the client. The `DelegatorAccountUserPrincipal` field shows `krbtgt` because the additional-ticket in U2U is a TGT — the TRR identifies this as a strong indicator of U2U+S4U2Self and therefore a Sapphire Ticket attack. |
| CS ActiveDirectoryAuthentication | n9 (B) | B | CrowdStrike Falcon IDP | Fires when a user authenticates and is granted a TGT. In Procedure B, this captures the low-privilege user's legitimate AS-REQ. |
| IDS Rule | n2, n14 (A) | A | Network IDS (Snort, Suricata, etc.) | Kerberos traffic to port 88. Procedure A's DDM includes TCP-layer nodes with IDS labels. The Kerberos protocol is mostly unencrypted at the message level, making IDS inspection feasible for message-type identification, though encrypted ticket contents are not inspectable. |
| Event 4768 | n9 (A, gray/skipped) | A | Windows Security Events | Event 4768 on Procedure A's DDM is on a gray (skipped) node — it represents the TGT request that does NOT occur in a Golden Ticket attack. Its absence is the detection signal used in the correlation query, not a directly observable event. |

## Query File Inventory

| File | Procedure | Query Count | Tables Used |
|---|---|---|---|
| `trr0013_ad_a.kql` | TRR0013.AD.A | 2 (1 Sentinel, 1 Defender) | SecurityEvent, IdentityLogonEvents |
| `trr0013_ad_b.kql` | TRR0013.AD.B | 3 (2 Sentinel, 1 Defender) | SecurityEvent, IdentityLogonEvents |

---

## Query Annotations

### trr0013_ad_a.kql — Query 1: Sentinel SecurityEvent (Event 4769 without preceding Event 4768)

**DDM Operation:** n1 "Receive Network Request" (TGS-REQ), correlated with absence of skipped n9 (AS-REQ)

**Telemetry:** Windows Security Event 4769 ("A Kerberos service ticket was requested"), correlated with absence of Event 4768 ("A Kerberos authentication ticket (TGT) was requested")

**Detection Rationale:** In a Golden Ticket attack, the attacker forges a TGT locally and skips the AS-REQ entirely. The DDM shows the AS-REQ path (n8, n9) in gray to indicate it is skipped. Event 4768 is never generated for the impersonated user. A TGS-REQ (Event 4769) for a user who has no corresponding TGT issuance (Event 4768) in the lookback period is the primary detection signal.

| Filter | DDM Trace | Rationale |
|---|---|---|
| `EventID == 4769` | Telemetry label on n1 | Event 4769: "A Kerberos service ticket was requested." This is the telemetry source tagged on the active path's TGS-REQ receive node. |
| `Status == "0x0"` | n1 receives a valid TGS-REQ | Successful service ticket issuance. A well-crafted Golden Ticket will pass KDC validation and produce a successful TGS-REP. |
| `join kind=leftanti ... EventID == 4768` | Absence of n9 (skipped AS-REQ) | Removes users who have a successful TGT issuance (Event 4768) in the lookback period. The remaining users received a service ticket without ever requesting a TGT — consistent with a forged TGT. |
| `extend IsMachineAccount = ...endswith "$"` | Baseline context (not a filter) | Machine accounts regularly request service tickets. Computed as a flag for analysis but does NOT exclude results — the detection team decides exclusion policy. |

**Tangential elements deliberately NOT filtered:**

| Element | Why Excluded |
|---|---|
| TargetUserName | Attacker-controlled — any user can be impersonated with a Golden Ticket |
| ServiceName | Attacker-controlled — any service can be targeted |
| TicketEncryptionType | The TRR notes RC4 (0x17) as a common tool default, but the technique succeeds with any encryption type. Projected as informational column only. |
| IpAddress | Attacker-controlled source; projected for triage, not filtered |
| Tool name (Mimikatz, Rubeus, Impacket, etc.) | Tangential; the TGS-REQ is a protocol-level operation |

### trr0013_ad_a.kql — Query 2: Defender for Identity IdentityLogonEvents

**DDM Operation:** n1 "Receive Network Request" (TGS-REQ)

**Telemetry:** Microsoft Defender for Identity Kerberos authentication events

**Prerequisite:** Requires Microsoft Defender for Identity sensor deployed on Domain Controllers.

| Filter | DDM Trace | Rationale |
|---|---|---|
| `Protocol == "Kerberos"` | n1 receives a Kerberos TGS-REQ | Limits to Kerberos protocol events. |

**Limitations:** The correlation pattern (absent Event 4768 for the same user) cannot be reliably replicated in IdentityLogonEvents because AS and TGS events may not be separately identifiable without parsing `AdditionalFields`. The query surfaces all Kerberos events as a baseline; the detection team applies additional filtering based on their MDI deployment.

### trr0013_ad_b.kql — Query 1: Sentinel SecurityEvent (Event 4769 with ENC-TKT-IN-SKEY)

**DDM Operation:** n1 "Receive Network Request" (U2U+S4U2Self TGS-REQ)

**Telemetry:** Windows Security Event 4769 ("A Kerberos service ticket was requested")

**Detection Rationale:** The Sapphire Ticket's PAC acquisition step requires a U2U+S4U2Self TGS-REQ. U2U is signaled by the ENC-TKT-IN-SKEY flag in KDCOptions, which is observable in Event 4769's TicketOptions field (bit 0x8). S4U2Self causes the low-privilege user to appear as both TargetUserName and ServiceName. This combination is rare in legitimate environments.

| Filter | DDM Trace | Rationale |
|---|---|---|
| `EventID == 4769` | Telemetry label on n1 | Event 4769: "A Kerberos service ticket was requested." |
| `Status == "0x0"` | n1 receives a valid TGS-REQ | Successful service ticket issuance. The KDC processes the U2U+S4U2Self request and returns a service ticket containing the target user's PAC. |
| `binary_and(TicketOptionsInt, 8) != 0` | n0 property: KDCOptions = ENC-TKT-IN-SKEY (U2U) | Immutable: U2U authentication requires the ENC-TKT-IN-SKEY flag. Bit 0x8 in TicketOptions corresponds to this flag. Any U2U exchange must set it. |
| `TargetUserName == ServiceName` | n0 properties: Service (sname) = LowPrivUser, combined with S4U2Self | Immutable: S4U2Self requests a ticket from the service to itself. The low-privilege user is both the TGT holder (TargetUserName) and the service (ServiceName). |

**Tangential elements deliberately NOT filtered:**

| Element | Why Excluded |
|---|---|
| TargetUserName (specific value) | Attacker-controlled — any compromised account can serve as the low-privilege user |
| IpAddress | Attacker-controlled source; projected for triage, not filtered |
| TicketEncryptionType | Not relevant to the U2U+S4U2Self mechanism |
| High-privilege user identity | Does not appear in Event 4769 at all — Windows logging fails to capture the PA-FOR-USER target |

### trr0013_ad_b.kql — Query 2: Sentinel SecurityEvent (Event 4769 without preceding Event 4768)

**DDM Operation:** n22 "Receive Network Request" (TGS-REQ with forged TGT)

**Telemetry:** Windows Security Event 4769, correlated with absence of Event 4768

**Detection Rationale:** After extracting the high-privilege user's PAC and forging the TGT, the attacker submits a TGS-REQ as the high-privilege user. This is functionally the same detection challenge as Procedure A — no Event 4768 exists for the impersonated user because the TGT was forged, not issued by the KDC. The query is identical to Procedure A Query 1.

| Filter | DDM Trace | Rationale |
|---|---|---|
| `EventID == 4769` | Telemetry label on n22 | Same as Procedure A — TGS-REQ receive on the DC. |
| `Status == "0x0"` | n22 receives a valid TGS-REQ | Sapphire Tickets are designed to pass KDC validation by using legitimate PAC elements. |
| `join kind=leftanti ... EventID == 4768` | Absence of AS-REQ for the high-privilege user | The high-privilege user never requested a TGT — the forged TGT contains a legitimate PAC but was never issued by the KDC. |

**Note:** This query is identical to Procedure A Query 1. The Sapphire Ticket's advantage over the Golden Ticket is that the forged TGT contains a legitimate PAC, making PAC-based anomaly detection ineffective. However, the fundamental absence of Event 4768 for the impersonated user remains.

### trr0013_ad_b.kql — Query 3: Defender for Identity IdentityLogonEvents

**DDM Operations:** n1 "Receive Network Request" (U2U+S4U2Self TGS-REQ), n22 "Receive Network Request" (TGS-REQ with forged TGT)

**Telemetry:** Microsoft Defender for Identity Kerberos authentication events

**Prerequisite:** Requires Microsoft Defender for Identity sensor deployed on Domain Controllers.

| Filter | DDM Trace | Rationale |
|---|---|---|
| `Protocol == "Kerberos"` | n1 and n22 receive Kerberos TGS-REQs | Limits to Kerberos protocol events. |

**Limitations:** TicketOptions parsing (for ENC-TKT-IN-SKEY detection) and TargetUserName/ServiceName comparison are not available as top-level columns in IdentityLogonEvents. These may be embedded in `AdditionalFields`. The query surfaces all Kerberos events as a baseline.
