# KQL Coverage & Query Reference — TRR0011 (DCSync)

## Procedure Coverage

| Procedure | Operations Covered | Operations Without Sentinel/Defender Telemetry |
|---|---|---|
| TRR0011.AD.A | n6 Access AD Object (Event 4662) | n0 Send Network Request (none), n2 Call RPC (CS only), n3 Send TCP Packet (IDS only), n4 Receive TCP Packet (none), n5 Receive RPC (CS only), n1 Receive Network Request (none) |

## Table Dependencies

| Table | Platform | Required For |
|---|---|---|
| SecurityEvent | Microsoft Sentinel | Procedure A — n6 Access AD Object (Event 4662) |
| IdentityDirectoryEvents | Microsoft Defender for Identity | Procedure A — n6 Access AD Object (DCSync ActionType) |

## Blind Spots

The DDM pipeline has 7 operations. Only 1 (n6 "Access AD Object") produces telemetry queryable in Microsoft Sentinel or Defender for Identity. The remaining 6 operations are either unobservable or observable only through vendor-specific or network-based tools:

| Operation | DDM Node | Telemetry Status |
|---|---|---|
| Send Network Request | n0 | No known telemetry |
| Call RPC | n2 | CrowdStrike only (DCSyncAttempted?) — not available in Sentinel/Defender |
| Send TCP Packet | n3 | Network IDS only — requires IDS with MS-DRSR/drsuapi rules |
| Receive TCP Packet | n4 | No known telemetry |
| Receive RPC | n5 | CrowdStrike only (ActiveDirectoryIncomingDceRpcRequest) — not available in Sentinel/Defender |
| Receive Network Request | n1 | No known telemetry |
| Access AD Object | n6 | Event 4662 — covered by queries in this set |

## Telemetry Constraints

- **Event 4662 requires audit policy configuration.** The "Audit Directory Service Access" advanced audit policy must be enabled on Domain Controllers for Event 4662 to be generated. Without this policy, the SecurityEvent query will return no results. This is a deployment prerequisite, not a query limitation.

- **AccessMask format varies.** Event 4662 may record the AccessMask as hex (`0x100`) or decimal (`256`) depending on the log collection pipeline. The Sentinel query checks for both forms.

- **DC machine account exclusion is not applied in the queries.** Normal replication originates from DC machine accounts (ending in `$`), but not all `$` accounts are DCs, and compromised DC machine accounts could perform malicious replication. The Sentinel query computes an `IsMachineAccount` flag for analysis without excluding any results. The detection team determines exclusion policy for their environment.

## Vendor-Specific Telemetry (Not Queried)

The following telemetry sources are documented in the DDM but are not queryable through Microsoft Sentinel or Defender. They are noted here for teams operating those platforms:

| Telemetry | DDM Node | Platform | Notes |
|---|---|---|---|
| DCSyncAttempted? | n2 Call RPC | CrowdStrike Falcon | Fires on the attacker-side host when an MS-DRSR RPC call is initiated. Requires Falcon sensor on the source machine. |
| ActiveDirectoryIncomingDceRpcRequest | n5 Receive RPC | CrowdStrike Falcon | Fires on the DC when it receives the drsuapi RPC call. Requires Falcon sensor on the DC. |
| IDS Rule | n3 Send TCP Packet | Network IDS (Snort, Suricata, etc.) | Detects the DCE/RPC bind to the drsuapi interface UUID `{e3514235-4b06-11d1-ab04-00c04fc2dcd2}` on the wire. Requires IDS deployment with appropriate rules. |

## Query File Inventory

| File | Contents |
|---|---|
| `trr0011_ad_a.kql` | Query 1: Sentinel SecurityEvent (Event 4662); Query 2: Defender for Identity IdentityDirectoryEvents (DCSync ActionType) |

---

## Query Annotations

Line-by-line rationale for each filter in the query set. Each annotation traces back to the DDM operation or property that justifies the filter's inclusion.

### Query 1 — Microsoft Sentinel: SecurityEvent (Event 4662)

**DDM Operation:** n6 "Access AD Object" — Properties: Object = Domain-DNS Class, Host = DC

**Telemetry:** Windows Security Event 4662 ("An operation was performed on an object")

**Prerequisite:** Event 4662 requires the "Audit Directory Service Access" advanced audit policy to be enabled on Domain Controllers. If this policy is not configured, no events will be generated and this query will return no results.

| Filter | DDM Trace | Rationale |
|---|---|---|
| `EventID == 4662` | Telemetry label on n6 | Event 4662: "An operation was performed on an object." This is the telemetry source tagged on the DDM node. |
| `ObjectServer == "DS"` | n6 targets an AD object | ObjectServer "DS" = Directory Services. Immutable for AD object access events. |
| `ObjectType has "19195a5b-..."` | n6 property: Object = Domain-DNS Class | Schema GUID for the DomainDNS class — the root object of the directory partition. Replication is always performed against this object class. Immutable to the technique. |
| `OperationType == "Object Access"` | n6 is "Access AD Object" | Confirms this is an object access event, not a schema or property set operation. |
| `AccessMask == "0x100" or "256"` | RIGHT_DS_CONTROL_ACCESS (CR) bit | AccessMask 0x100 (decimal 256) = RIGHT_DS_CONTROL_ACCESS. Immutable access mask for control access right operations including replication. May appear as hex or decimal depending on log format — both forms are checked. |
| `Properties has_any (ReplicationPermissionGUIDs)` | n0 property: Permissions = DS-Replication-Get-Changes* | The Properties field contains the control access right GUID exercised. At least one of the three replication GUIDs must be present. These GUIDs are immutable — defined by the AD schema. |
| `extend IsMachineAccount = ...endswith "$"` | Baseline context (not a filter) | Normal replication originates from DC machine accounts (ending in `$`). Computed as a flag for analysis but does NOT exclude results — not all `$` accounts are DCs, and compromised DC accounts could perform malicious replication. The detection team decides exclusion policy. |

**Tangential elements deliberately NOT filtered:** SubjectUserName (attacker-controlled), tool names (Mimikatz, Impacket, etc.), and source hostname/IP are all tangential and excluded from query filters per DDM methodology.

### Query 2 — Microsoft Defender for Identity: IdentityDirectoryEvents

**DDM Operation:** n6 "Access AD Object" — Properties: Object = Domain-DNS Class, Host = DC

**Telemetry:** Event 4662 (underlying source), surfaced via Defender for Identity

**Prerequisite:** Requires Microsoft Defender for Identity sensor deployed on Domain Controllers.

| Filter | DDM Trace | Rationale |
|---|---|---|
| `ActionType == "DCSync"` | n6 "Access AD Object" with replication permissions | Defender for Identity classifies replication requests from non-DC sources under the "DCSync" ActionType. This is the MDI abstraction of the same underlying Event 4662 telemetry with replication GUIDs. If your MDI version uses a different ActionType string, adjust this filter accordingly. |

**Tangential elements deliberately NOT filtered:** AccountName (attacker-controlled), tool names are tangential and excluded from query filters per DDM methodology.
