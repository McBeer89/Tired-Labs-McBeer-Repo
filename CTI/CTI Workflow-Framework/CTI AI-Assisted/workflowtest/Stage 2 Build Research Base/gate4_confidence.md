# Gate 4 — Confidence Assessment
## Analyst: Junior Analyst 1
## Date: March 15, 2026
## Claims Evaluated: 118 (after Gate 3 removals)

---

## Critical Context for This Assessment

**Every claim in this research base currently flows through a single AI-synthesized document.** While the synthesis cites named primary sources (~86% of claims), the analyst has not independently verified any of those citations against the actual primary sources. This creates a ceiling on confidence:

- A claim attributed to "Sophos, 2025 Active Adversary Report" in the synthesis is **not the same** as a claim the analyst extracted directly from the Sophos report.
- The synthesis may have misquoted, misattributed, or fabricated source references.
- Until primary sources are independently processed, all confidence levels carry the caveat: **"pending primary source verification."**

This is not a reason to discard the research base — it's a reason to treat it as a first draft that improves as primary sources are added.

**Confidence Criteria (reference):**
- **LOW:** Single-sourced or limited corroboration. Known gaps exist. Useful but should not be the sole basis for a decision.
- **MODERATE:** Supported by 2–3 independent pieces of information. Gaps significantly reduced. Multiple data points from at least two source categories.
- **HIGH:** Supported by predominant available data across multiple independent sources. Collection gaps accounted for and unlikely to change the assessment.

---

## Suggested Confidence Levels by Category

### Category A: LOW — Single-sourced through synthesis only, no named primary source
**Claims:** 12, 33, 64, 68, 69, 73, 84, 85, 86, 92, 128

**Reasoning:** These 11 claims have no traceable primary source in the references file. They exist only in the AI synthesis. They may be accurate, but they cannot be verified from this source material alone. They should be treated as leads requiring corroboration, not as established claims.

| # | Claim (abbreviated) | Suggested | Reasoning |
|---|---|---|---|
| 12 | Qilin Rust payload targets Win/Linux/ESXi; 80-85% affiliate split | LOW | No primary source; operational detail unverifiable from synthesis |
| 33 | Black Basta members migrated to Cactus and SafePay | LOW | Implied by Intel 471/ReliaQuest but not directly attributed |
| 64 | DBS Bank/BOC Singapore via Toppan Next Tech | LOW | No primary source in references file |
| 68 | Betterment breach Jan 2026, 1.4M customers | LOW | No primary source in references file |
| 69 | Wealth management firms on leak sites (Tufton, FAS, Hudson, Duff) | LOW | No primary source; leak site observation without verification |
| 73 | GC2 (Google Sheets C2) in Fog ransomware; Adaptix emerging | LOW | Picus cited for Adaptix only; GC2/Fog unsourced |
| 84 | Qilin modifies WDigest registry key | LOW | No primary source; undated |
| 85 | Akira dumps Veeam credentials via PowerShell | LOW | No primary source; undated |
| 86 | Lateral movement: RDP, PsExec, WMI, Impacket; target ESXi | LOW | Composite TTP description, no single source |
| 92 | Cyberduck used by Qilin for Backblaze uploads | LOW | No primary source |
| 128 | Akira cold-calling employees/clients as pressure tactic | LOW | No primary source; undated |

---

### Category B: LOW — Named primary source in references, but single-sourced and unverified
**Claims:** 1, 3, 6, 7, 9, 10, 11, 15, 20, 21, 23, 24, 26, 27, 28, 31, 34, 35, 36, 37, 40, 41, 43, 46, 47, 51, 52, 55, 58, 59, 60, 62, 65, 66, 67, 71, 73 (Adaptix portion), 75, 76, 77, 78, 80, 81, 83, 95, 98 (cut), 103, 106, 108, 115, 116, 117, 119, 120, 121, 122, 124, 127

**Reasoning:** Each of these cites a single named primary source via the synthesis — Flashpoint, Comparitech, Symantec, Coalition, Chainalysis, Sophos, etc. The source is identified and datable, but the analyst has not independently accessed or verified the source. This is better than Category A (at least you know where to check), but it's still single-sourced through an AI intermediary.

**There are 57 claims in this category.** Rather than list all individually, here are representative examples:

| # | Claim (abbreviated) | Suggested | Reasoning |
|---|---|---|---|
| 1 | 126–141 active groups in 2025 | LOW | Emsisoft + Picus cited, but accessed only through synthesis |
| 7 | Qilin 946 victims, 69 finance targets | LOW | Comparitech/Picus cited; single synthesis pathway |
| 15 | Akira 34 FS victims Apr 2024–Apr 2025 | LOW | Flashpoint cited; unverified |
| 23 | RansomHub 38 FS victims before shutdown | LOW | Flashpoint/Bitsight cited; unverified |
| 55 | Edge/VPN exploitation 3% to 22% (2023–2024) | LOW | Verizon DBIR 2025 cited; unverified |
| 106 | Demands surged 47% YoY | LOW | Coalition 2026 cited; unverified |
| 115 | Median on-chain payments jumped 368% | LOW | Chainalysis cited; unverified |
| 127 | Attackers stealing cyber insurance policies | LOW | Resilience Midyear 2025 cited; unverified |

---

### Category C: LOW trending MODERATE — Named primary source is a government advisory or CISA KEV
**Claims:** 16, 25, 38, 39, 42, 44, 45, 48, 49, 50, 107

**Reasoning:** These claims cite CISA advisories, CISA KEV entries, or joint CISA/FBI advisories — sources that are publicly accessible, well-indexed, and straightforward to verify. Government advisories are among the most reliable sources in CTI. These trend toward MODERATE because:
1. The source is authoritative (government, multi-agency)
2. The source is easily verifiable (CISA.gov, KEV catalog)
3. The claims are factual (advisory published, CVE added to KEV) rather than analytical

However, they remain LOW until the analyst independently verifies the citations. Once you pull up the actual CISA advisory and confirm the synthesis accurately represents it, these jump to MODERATE or HIGH immediately.

| # | Claim (abbreviated) | Suggested | Reasoning |
|---|---|---|---|
| 16 | CISA/FBI advisory confirmed Akira targeting FS (Nov 2025) | LOW → MODERATE on verification | Government advisory; easily verifiable |
| 25 | Medusa CISA/FBI advisory AA25-071A, 300+ victims, $100K–$15M | LOW → MODERATE on verification | Government advisory with specific ID |
| 38 | CVE-2024-55591 FortiOS CISA KEV Jan 2025 | LOW → MODERATE on verification | KEV entry; binary verifiable |
| 39 | CVE-2025-59718/59719 FortiCloud CISA KEV Dec 2025 | LOW → MODERATE on verification | KEV entry |
| 42 | CVE-2025-0108 Palo Alto CISA KEV Feb 2025 | LOW → MODERATE on verification | KEV entry |
| 44 | CVE-2024-40766 SonicWall — Akira/Marquis vector | LOW → MODERATE on verification | KEV + incident correlation |
| 45 | CVE-2024-40711 Veeam CISA KEV Oct 2024, ransomware confirmed | LOW → MODERATE on verification | KEV marked "Known" ransomware use |
| 48 | CVE-2025-10035 GoAnywhere CISA KEV, Medusa/Storm-1175 | LOW → MODERATE on verification | KEV + Microsoft attribution |
| 49 | CVE-2025-5777 CitrixBleed 2 CISA KEV Jul 2025, 40% targeting FS | LOW → MODERATE on verification | KEV + Imperva FS-specific data |
| 50 | CVE-2025-22224/22225/22226 VMware ESXi CISA KEV Feb 2026 | LOW → MODERATE on verification | KEV confirmed ransomware use |
| 107 | Medusa demands $100K–$15M | LOW → MODERATE on verification | From CISA advisory AA25-071A |

---

### Category D: LOW trending MODERATE — Multiple named sources in references file
**Claims:** 2, 4, 5, 8, 13, 14, 17, 19, 22, 53, 54, 56, 57, 61, 63, 72, 74, 79, 82, 87, 89, 90, 91, 93, 94, 96, 97, 104, 105, 109, 110, 111, 112, 113, 114, 123, 125, 126

**Reasoning:** These claims have multiple named sources in the references file, suggesting corroboration across independent reporting. For example:

- Claim 53 (vulnerability exploitation 33% of initial access): Mandiant M-Trends 2025
- Claim 54 (compromised credentials 41%): Sophos 2025 Active Adversary
- Together, claims 53+54 paint a corroborated picture of initial access vectors from two independent vendor sources.

Similarly:
- Claim 110 (28% payment rate): Chainalysis
- Claim 111 (20% by Q4 2025): Coveware
- Claim 112 (86% refused to pay): Coalition
- Three independent sources corroborating declining payment rates.

These trend MODERATE because source diversity exists, but remain technically LOW until the analyst independently verifies at least two of the named sources per claim.

| # | Claim (abbreviated) | Suggested | Reasoning |
|---|---|---|---|
| 5 | Multiple groups ceased operations Jan–Apr 2025 | LOW → MOD | Intel 471 + ReliaQuest + Malwarebytes + Bitsight |
| 8 | Qilin Korean Leaks — 28 firms via MSP GJTec | LOW → MOD | Hacker News + Bitdefender + Korea JoongAng Daily |
| 13 | Akira 717-740 victims, $244M revenue | LOW → MOD | Symantec + Picus |
| 14 | Akira/Marquis — 400K consumers, 74+ banks | LOW → MOD | American Banker (single but high-quality source) |
| 19 | Clop 500+ victims via Cleo + Oracle EBS | LOW → MOD | SOCRadar + Google Cloud Blog + BankInfoSecurity |
| 87 | Rclone in 57% of incidents | LOW → MOD | ReliaQuest + Symantec + Infosecurity Magazine |
| 94 | EDRKillShifter used by 8+ groups | LOW → MOD | ESET + Arete + The Hacker News |
| 110 | 28% payment rate 2025 | LOW → MOD | Chainalysis + corroborated by Coveware (claim 111) + Coalition (claim 112) |
| 123 | Encryption in only 50% of attacks | LOW → MOD | Sophos + corroborated by sector-specific data (claim 124) |

---

### Category E: No claims assessed at MODERATE or HIGH

**No claim in this research base currently qualifies for MODERATE or HIGH confidence.**

This is not a quality failure — it's an accurate reflection of the source situation. You have one AI-synthesized document that references many primary sources, but you haven't independently verified any of those references. The entire research base is effectively single-sourced through one intermediary.

**How to upgrade confidence:**
- Process one CISA advisory directly → all claims citing that advisory move to MODERATE
- Process one Sophos/Mandiant/CrowdStrike report directly → claims citing it gain independent corroboration
- Process an FS-ISAC alert that corroborates synthesis claims → those claims move toward MODERATE
- Two independent primary sources confirming a claim = MODERATE
- Three+ independent primary sources across different source categories = HIGH

---

## Summary Table

| Confidence Level | Claim Count | Description |
|---|---|---|
| LOW (no named source) | 11 | AI synthesis only; no traceable primary source |
| LOW (named source, unverified) | 57 | Single named source, not independently confirmed |
| LOW → MODERATE (government advisory) | 11 | CISA/FBI advisory or KEV; easily verifiable |
| LOW → MODERATE (multiple named sources) | 39 | 2+ named sources suggesting corroboration |
| MODERATE | 0 | None — requires independent source verification |
| HIGH | 0 | None — requires multiple independent verified sources |

---

## What I Need From You

For each claim (or category of claims), confirm or override the suggested confidence level:

1. **Do you agree with the overall assessment that everything is LOW pending verification?** This is the technically correct position given the source situation. If you disagree, explain why — you may have analyst knowledge that changes the picture.

2. **For Category C (government advisories) — have you independently accessed any of these CISA advisories?** If you've read AA25-071A (Medusa) or checked CISA KEV entries directly, those claims can upgrade immediately.

3. **For Category D (multiple named sources) — do you have independent knowledge that corroborates any of these claims?** For example, if you've seen the Chainalysis payment rate data reported independently in FS-ISAC products, that's corroboration.

4. **Are there any claims where you think LOW is too generous?** Some Category A claims (no named source, undated) might warrant flagging as "LOW — weak" or even reconsideration for removal.

5. **What primary sources do you plan to process next?** This will tell me which confidence upgrades to anticipate.

State your confidence level and one sentence of reasoning for each claim or category where you disagree with my suggestion. For categories where you agree, a simple "confirmed" is sufficient.
