## P2 — Priority 2 Techniques

P2 techniques are actively used by groups targeting financial services and relevant to Hartwell's stack, but either have higher detection fidelity (lower build complexity), affect fewer groups, or have unverified source attribution. Build these after P1 detections are operational.

---

### P2-1: Kerberoasting (T1558.003 — Steal or Forge Kerberos Tickets: Kerberoasting)

| Field | Content |
|---|---|
| **Technique** | T1558.003 — Steal or Forge Kerberos Tickets: Kerberoasting |
| **Priority** | P2 — Akira-attributed; high detection fidelity via service ticket anomalies. |
| **Observable Behavior** | A single account requests TGS tickets for multiple service principal names (SPNs) in rapid succession, targeting accounts with weak or crackable passwords. Rubeus is the documented tool. |
| **Telemetry Source** | Windows 4769 (Kerberos Service Ticket Request) — filter for RC4 encryption (0x17) from accounts requesting tickets for multiple SPNs. Windows 4768 (Kerberos TGT Request) — for associated authentication context. |
| **Known Indicators** | Rubeus as Kerberoasting tool in Akira chain (Security Boulevard, Nov 2025). Anomalous volume of 4769 events from a single source account. Encryption type 0x17 (RC4) in ticket requests — legitimate services increasingly use AES. |
| **Group-Specific** | Akira uses Rubeus for Kerberoasting after initial Mimikatz credential dump, as a privilege escalation step before lateral movement (Security Boulevard, Nov 2025). |
| **Why This Priority** | P2 — High detection fidelity (RC4 ticket requests from a single account are anomalous in modern environments), but narrower group attribution than P1 techniques. |

---

### P2-2: DCSync (T1003.006 — OS Credential Dumping: DCSync)

| Field | Content |
|---|---|
| **Technique** | T1003.006 — OS Credential Dumping: DCSync |
| **Priority** | P2 — Cross-group; enables domain-wide persistence via Golden Ticket. |
| **Observable Behavior** | A non-domain-controller host initiates directory replication service (DRS) requests to a domain controller, extracting the KRBTGT hash or other credential material. |
| **Telemetry Source** | Windows 4662 (Directory Service Access) — operations on domain replication objects (DS-Replication-Get-Changes, DS-Replication-Get-Changes-All) from non-DC source addresses. Sysmon 3 (NetworkConnect) — RPC connections to DCs on replication ports from non-DC hosts. |
| **Known Indicators** | KRBTGT hash extraction as precursor to Golden Ticket creation (Qualys ETM Defense Guide, Feb 2026). Replication requests originating from workstations or member servers rather than domain controllers. |
| **Group-Specific** | Cross-group technique. Research base documents it as a standard post-credential-dump escalation step without single-group attribution. |
| **Why This Priority** | P2 — Domain-wide impact if successful (Golden Ticket grants persistent, unrestricted domain access). Ranked P2 rather than P1 because the prerequisite (LSASS dumping, P1-2) must succeed first — detecting the precursor is higher value. |

---

### P2-3: WDigest Registry Modification (T1112 — Modify Registry)

| Field | Content |
|---|---|
| **Technique** | T1112 — Modify Registry (WDigest credential caching) |
| **Priority** | P2 — Qilin-attributed; near-zero false positive rate. |
| **Observable Behavior** | WDigest `UseLogonCredential` registry value set to `1`, forcing plaintext credential storage in LSASS memory. This is a precursor to LSASS dumping (P1-2). |
| **Telemetry Source** | Sysmon 13 (RegistryEvent — Value Set). Windows 4657 (Registry Value Modified) — requires auditing enabled on the target key. |
| **Known Indicators** | Registry key: `HKLM\SYSTEM\CurrentControlSet\Control\SecurityProviders\WDigest`, value `UseLogonCredential` = `1`. |
| **Group-Specific** | Qilin affiliates modify this key before LSASS dumping to ensure plaintext credentials are available. Source is undated/unverified (GAP-R03), but the technique itself is well-documented in public DFIR literature. |
| **Why This Priority** | P2 — Near-zero false positive rate (legitimate WDigest modification is rare in modern environments). Low build complexity. Paired with P1-2 (LSASS dumping), this creates a two-stage detection chain: WDigest modification as early warning, LSASS access as confirmation. |

---

### P2-4: C2 via Trusted Platforms (T1102 — Web Service)

| Field | Content |
|---|---|
| **Technique** | T1102 — Web Service (C2 via trusted cloud platforms) |
| **Priority** | P2 — Multiple groups; abuses trusted services that bypass traditional network-based detection. |
| **Observable Behavior** | Malware communicates with attacker-controlled infrastructure via legitimate cloud services — Microsoft Graph API (Havoc framework), Google Sheets (GC2 framework) — disguising C2 traffic as normal cloud API calls. |
| **Telemetry Source** | Proxy/firewall logs — API call patterns to Microsoft Graph and Google Sheets APIs from non-standard processes or endpoints. Sysmon 3 (NetworkConnect) — outbound connections to graph.microsoft.com or sheets.googleapis.com from processes not associated with legitimate M365/Google Workspace usage. Sysmon 1 (ProcessCreate) — parent-child process trees where unusual processes spawn cloud API connections. |
| **Known Indicators** | Havoc C2 with Microsoft Graph API integration (AlphaHunt, 2025–2026). GC2 (Google Sheets C2) observed in Fog ransomware (Picus Security, 2025). Non-browser, non-Office processes making API calls to graph.microsoft.com or sheets.googleapis.com. |
| **Group-Specific** | Fog ransomware used GC2 for Google Sheets-based C2 (Picus Security, 2025). Havoc with Graph API is an emerging cross-group capability. |
| **Why This Priority** | P2 — These C2 channels abuse services Hartwell uses legitimately (M365, potentially Google Workspace), making network-layer blocking impractical. Detection must be behavioral: which processes are calling these APIs, and do they match expected application behavior? Ranked P2 because the technique is emerging rather than dominant, and standard C2 (Cobalt Strike, Sliver, Brute Ratel) remains more prevalent. |

---

### P2-5: Veeam Backup Credential Dumping (T1555 — Credentials from Password Stores)

| Field | Content |
|---|---|
| **Technique** | T1555 — Credentials from Password Stores (Veeam Backup) |
| **Priority** | P2 — Akira-attributed; Hartwell runs Veeam Backup & Replication. |
| **Observable Behavior** | PowerShell commands query the Veeam credential store to extract stored backup credentials, which often include domain admin or service account passwords. |
| **Telemetry Source** | Windows 4104 (PowerShell Script Block Logging) — script blocks referencing Veeam credential retrieval functions. Sysmon 1 (ProcessCreate) — PowerShell execution with command-line arguments targeting Veeam APIs or database. Windows 4688 (Process Creation) — with command-line logging enabled. |
| **Known Indicators** | PowerShell commands targeting Veeam credential storage (specific commands undated/unverified per GAP-R03). Veeam Backup & Replication CVE-2024-40711 (CVSS 9.8, deserialization RCE) exploited by Akira, Fog, and Frag — Sophos X-Ops tracked 4+ incidents combining VPN + Veeam exploitation. CVE-2025-23120 (CVSS 9.9, domain-joined backup servers) disclosed March 2025. |
| **Group-Specific** | Akira dumps Veeam backup credentials via PowerShell (source undated/unverified). Broader Veeam exploitation is well-documented: 20%+ of Rapid7 2024 IR cases involved Veeam exploitation. |
| **Why This Priority** | P2 — Hartwell runs Veeam, making this directly relevant. Ranked P2 rather than P1 because the specific PowerShell-based credential dump procedure is unverified (GAP-R03), and version/patch status of Hartwell's Veeam deployment is unknown (GAP-003). Telemetry dependency: confirm PowerShell Script Block Logging is enabled on Veeam servers. |
