# KQL Query Set — TRR0012 (AS-REP Roasting, T1558.004)

## Procedure Coverage

| Procedure | Operations Covered | Operations Without Queryable Telemetry |
|---|---|---|
| TRR0012.AD.A | n7 "Send AS-REP" (Event 4768) | n0, n2, n4 (CS-only), n5, n11, n6, n12, n8 |
| TRR0012.AD.B | n7 "Send AS-REP" (Event 4768) | n0, n1, n3, n5, n11, n6, n12, n8 |
| TRR0012.AD.C | n7 "Send AS-REP" (Event 4771, Event 4768) | n9, n11, n6, n12, n8 |
| TRR0012.AD.D | None | n10, n8 (complete blind spot) |

Procedures A, B, and C share the TGT request pipeline from n11 onward. The only differentiation is the enumeration phase: A uses LDAP (n0, n2, n4), B uses ADWS (n0, n1, n3), and C skips enumeration entirely (n9 feeds directly into n11). As a result, Procedures A and B produce identical Sentinel/Defender queries because the only telemetry-bearing operation on their paths is the shared n7 node.

Procedure C is distinguished by the volume pattern: testing every account produces many Event 4771 (KDC_ERR_PREAUTH_REQUIRED) failures from a single source, whereas Procedures A and B target only known-vulnerable accounts and primarily produce Event 4768 successes. The summarize query in `trr0012_ad_c.kql` supports volume-based triage, but no thresholds are prescribed -- baselines are environment-specific.

## Table Dependencies

| Table | Platform | Required For |
|---|---|---|
| SecurityEvent | Microsoft Sentinel | Procedures A, B, C (Event 4768, Event 4771) |
| IdentityQueryEvents | Microsoft Defender for Identity | Procedures A, B, C (Kerberos AS events) |

## Blind Spots

| Operation | Node | Reason | Affected Procedures |
|---|---|---|---|
| Enumerate Users w/o Pre-Auth | n0 | Decision node; no telemetry | A, B |
| Send LDAP Search Request | n2 | No Sentinel/Defender telemetry for LDAP queries | A |
| Receive LDAP Search Request | n4 | CrowdStrike-only (see Vendor-Specific Telemetry) | A |
| Send ADWS Request | n1 | No known telemetry for ADWS queries | B |
| Receive ADWS Request | n3 | No known telemetry for ADWS queries | B |
| Send AD Data | n5 | No telemetry on DC response | A, B |
| Request TGT | n11 | Client-side action; no DC telemetry | A, B, C |
| Send AS-REQ | n6 | Client-side action; no DC telemetry (the DC logs the response, not the request) | A, B, C |
| Send TGT | n12 | DC response delivery; no distinct telemetry beyond n7 | A, B, C |
| Crack Hash | n8 | Offline activity; no telemetry | A, B, C, D |
| Test Every Account | n9 | Procedure entry point; no telemetry | C |
| Intercept Auth Server Messages | n10 | Passive network interception; no host/AD telemetry | D |

## Telemetry Constraints

1. **Event 4771** fires only on pre-authentication failure. It does not fire when a TGT is successfully issued without pre-auth. Therefore, Event 4771 is most relevant to Procedure C (where the attacker tests accounts that DO require pre-auth and receives failures) and less relevant to Procedures A and B (where the attacker already knows which accounts lack pre-auth).

2. **Event 4768** fires on both success and failure of TGT requests. For AS-REP roasting, the relevant pattern is a successful TGT issuance (Status `0x0`) where PreAuthType is `0` (no pre-authentication data provided).

3. **PreAuthType = 0** is the immutable indicator. A value of `0` means no pre-authentication data was provided in the AS-REQ. This is the essential attribute of the technique -- requesting a TGT without proving identity first.

4. **FailureCode / ResultCode `0x19`** (decimal 25) corresponds to `KDC_ERR_PREAUTH_REQUIRED`. This error code appears in Event 4771 when the KDC rejects a request because pre-auth was required but not provided. This is the distinguishing telemetry for Procedure C.

5. **EncryptionType** is informational, not a required filter. The DDM marks encryption downgrade as "Optional" on n6. The technique succeeds with any encryption type (RC4, AES, etc.). EncryptionType is projected as a column for analysis but is deliberately excluded from filter logic.

6. **Environment baseline matters.** Windows clients provide pre-authentication by default. Linux clients may or may not. In mixed environments, `KDC_ERR_PREAUTH_REQUIRED` errors (Event 4771 with FailureCode `0x19`) may be common and require baselining. In Windows-only environments, these events may be rare and more immediately noteworthy.

7. **Microsoft Defender for Identity (IdentityQueryEvents)** exposes Kerberos AS events, but field-level filtering for PreAuthType and Status depends on how these values are surfaced in AdditionalFields. The Defender queries project AdditionalFields for manual inspection. Extracting PreAuthType and Status from AdditionalFields requires environment-specific parsing of the dynamic JSON column.

## Vendor-Specific Telemetry (Not Queried)

The following CrowdStrike telemetry sources appear in the DDM but have no Sentinel or Defender table mapping. They are documented here for teams using CrowdStrike Falcon.

| DDM Label | Node | Notes |
|---|---|---|
| CS ActiveDirectoryIncomingLdapSearchRequest | n4 "Receive LDAP Search Request" | Fires when the DC receives an LDAP search. Procedure A only. Could surface the LDAP filter targeting `userAccountControl` with `ADS_UF_DONT_REQUIRE_PREAUTH` (0x400000). |
| CS ActiveDirectoryAuthenticationFailure | n7 "Send AS-REP" | Contains `KerberosErrorCode` in decimal (25 = `KDC_ERR_PREAUTH_REQUIRED`). `ActiveDirectoryAuthenticationMethod` = `0` for Kerberos. Relevant to Procedure C. |

Additionally, CrowdStrike's `ActiveDirectoryAuthentication` event covers successful authentications but lacks a pre-authentication indicator field, making it less useful than Event 4768 for this technique.

## Source Issues

**Event ID correction on DDM node n7.** The DDM label reads "Event 4678" but this event ID does not exist in Windows security auditing. The correct event is **Event 4768** ("A Kerberos authentication ticket (TGT) was requested"). The TRR's own References section links to "Event 4768 - Microsoft Learn," and the TRR prose in the Logging section describes the event as "Event 4678 - A Kerberos authentication ticket (TGT) was requested" -- the description matches Event 4768, confirming the label is a typo. All queries in this set use the corrected Event ID 4768.

## Query File Inventory

| File | Procedure | Query Count | Tables Used |
|---|---|---|---|
| `trr0012_ad_a.kql` | TRR0012.AD.A | 2 (1 Sentinel, 1 Defender) | SecurityEvent, IdentityQueryEvents |
| `trr0012_ad_b.kql` | TRR0012.AD.B | 2 (1 Sentinel, 1 Defender) | SecurityEvent, IdentityQueryEvents |
| `trr0012_ad_c.kql` | TRR0012.AD.C | 5 (3 Sentinel, 2 Defender) | SecurityEvent, IdentityQueryEvents |
| `trr0012_ad_d.kql` | TRR0012.AD.D | 0 (blind spot documented) | None |

## Query Annotations

### trr0012_ad_a.kql / trr0012_ad_b.kql — Event 4768 (Sentinel)

These files contain identical queries because Procedures A and B share the same telemetry-bearing operation (n7). They differ only in the enumeration method (LDAP vs. ADWS), which is upstream of the shared pipeline and has no Sentinel/Defender telemetry.

| Filter | DDM Trace | Rationale |
|---|---|---|
| `EventID == 4768` | n7 "Send AS-REP", label "Event 4678" (corrected to 4768) | TGT request event; fires on both success and failure |
| `PreAuthType == "0"` | n7 property `PreAuthType: 0` | Immutable: value 0 means no pre-auth data was provided. This is the essential indicator of the technique. |
| `Status == "0x0"` | n7 property `ResultCode_Success: 0x0` | Successful TGT issuance. For Procedures A/B, the attacker targets known-vulnerable accounts, so successes are the expected outcome. |

**Tangential Elements NOT Filtered:**

| Element | Why Excluded |
|---|---|
| TargetUserName | Attacker-controlled; any account lacking pre-auth could be targeted |
| IpAddress | Attacker-controlled; requests can originate from any host |
| TicketEncryptionType | DDM marks encryption downgrade as "Optional" on n6; technique succeeds with any encryption type. Projected as informational column only. |
| Tool name (Rubeus, GetNPUsers.py, etc.) | Tangential; the TGT request is a protocol-level operation, not tool-specific |
| LDAP filter string | Upstream of n7; no Sentinel/Defender telemetry for LDAP queries |

### trr0012_ad_c.kql — Event 4771 (Sentinel)

| Filter | DDM Trace | Rationale |
|---|---|---|
| `EventID == 4771` | n7 "Send AS-REP", label "Event 4771" | Pre-authentication failure event; fires only on failure |
| `FailureCode == "0x19"` | n7 property `ResultCode_Failure: 0x19` | Immutable: `KDC_ERR_PREAUTH_REQUIRED` is the specific error returned when pre-auth is required but not provided |
| `PreAuthType == "0"` | n7 property `PreAuthType: 0` | Immutable: no pre-auth data was provided in the request |

**Tangential Elements NOT Filtered:**

| Element | Why Excluded |
|---|---|
| TargetUserName | Attacker tests all accounts; filtering on specific names would miss the pattern |
| IpAddress | Attacker-controlled source; projected for triage, not filtered |
| Volume threshold | The high volume of 4771 events is the distinguishing characteristic of Procedure C, but thresholds are environment-specific. The summarize query supports volume triage without prescribing a count. |
| TicketEncryptionType | Optional per DDM; projected as informational column only |

### trr0012_ad_c.kql — Event 4771 Summarize (Sentinel)

| Filter | DDM Trace | Rationale |
|---|---|---|
| `EventID == 4771` | n7 "Send AS-REP", label "Event 4771" | Same as above |
| `FailureCode == "0x19"` | n7 property `ResultCode_Failure: 0x19` | Same as above |
| `PreAuthType == "0"` | n7 property `PreAuthType: 0` | Same as above |
| `summarize by IpAddress` | n6 property `Host: Any` | Groups failures by source to identify a single host testing many accounts |

### trr0012_ad_c.kql — Event 4768 (Sentinel)

Identical to the Procedure A/B query. For Procedure C, this captures the accounts that passed the test (i.e., accounts that do not require pre-auth). The attacker receives both 4771 failures (most accounts) and 4768 successes (vulnerable accounts).

### trr0012_ad_a.kql / trr0012_ad_b.kql / trr0012_ad_c.kql — Defender Variants

The Defender queries target `IdentityQueryEvents` and filter on `ActionType` for Kerberos AS events. Field-level filtering for PreAuthType and Status is not applied because these values may be embedded in `AdditionalFields` (a dynamic JSON column) rather than exposed as top-level columns. The queries project `AdditionalFields` for manual inspection and parsing by the detection team.

| Filter | DDM Trace | Rationale |
|---|---|---|
| `ActionType == "Kerberos authentication (AS)"` | n7 "Send AS-REP" | Maps to successful TGT issuance |
| `ActionType == "Kerberos authentication failed (AS)"` | n7 "Send AS-REP", label "Event 4771" | Maps to pre-authentication failure |
