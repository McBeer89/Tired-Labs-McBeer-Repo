# Phase 9: Key Judgments
## CTI Research Base: Ransomware Groups Targeting Financial Services
## IR-01 / PIR-01.1, PIR-01.2, PIR-01.3

**Analyst:** Junior Analyst 1
**Date:** March 15, 2026
**Research Base Version:** 1.0
**Status:** Accepted by analyst — pending primary source verification for confidence upgrades

---

## Confidence Level Note

All key judgments carry LOW confidence. This reflects the single-source dependency (all claims flow through an AI-synthesized intermediary document without independent primary source verification), not the quality of the underlying evidence. Multiple judgments — particularly KJ4 — reference findings corroborated by three or more named sources and would likely reach MODERATE confidence upon independent verification. The analyst acknowledges confidence ratings are conservative for this exercise and appropriate given the source limitation.

---

## Key Judgment 1 (PIR-01.1: Primary Threat Groups)

**We assess with LOW confidence that Qilin, Akira, and Clop represent the most significant ransomware threats to financial services firms with Hartwell's profile in early 2026.**

Qilin leads in overall volume (946 victims, 69 confirmed FS targets) and demonstrated the ability to cascade through a single MSP to compromise 28 financial firms simultaneously (Korean Leaks campaign, September 2025). Akira has the most confirmed FS victim count from a single tracking source (34 per Flashpoint, April 2024–April 2025) and a documented attack pattern exploiting VPN infrastructure directly relevant to Hartwell's technology stack (SonicWall CVE-2024-40766 in the Marquis attack affecting 74+ banks). Clop's mass zero-day exploitation of shared platforms (Cleo file transfer, Oracle E-Business Suite) creates outsized supply-chain exposure for financial firms reliant on common technology vendors.

Medusa, Play, and DragonForce represent secondary but active threats. Medusa received a joint CISA/FBI/MS-ISAC advisory (AA25-071A) in March 2025 and has a confirmed Lazarus Group (North Korean) nexus. Play has remained consistently active among top five groups throughout 2025. DragonForce's cartel model has attracted Scattered Spider affiliates for social engineering campaigns against financial targets.

**Supporting Evidence:** Claims 2.2.1–2.2.5 (Qilin), 2.3.1–2.3.5 (Akira), 2.4.1–2.4.4 (Clop), 2.6.1–2.6.2 (Medusa), 2.7.1 (Play), 2.7.5 (DragonForce)

**Confidence Reasoning:** LOW — based on single AI-synthesized source. Would upgrade to MODERATE upon independent verification of Flashpoint FS targeting data and CISA advisories.

**Caveat:** This judgment reflects confirmed targeting of the financial services sector broadly, not confirmed targeting of Hartwell specifically.

---

## Key Judgment 2 (PIR-01.1: Initial Access — Direct vs. Supply Chain)

**We assess with LOW confidence that edge device and VPN exploitation is the primary direct-entry initial access vector, but supply-chain compromise through third-party vendors may represent greater organizational risk for a firm with Hartwell's branch footprint and vendor ecosystem.**

The majority of confirmed financial services incidents in this research base involved vendor compromise rather than direct targeting of the victim's perimeter:

- Marquis Software Solutions → 74+ banks via SonicWall compromise of vendor (Akira, August 2025)
- DBS Bank/Bank of China Singapore → via printing vendor Toppan Next Tech (April 2025)
- SitusAMC → JPMorgan Chase, Citigroup, Morgan Stanley via mortgage tech vendor (November 2025)
- Qilin/GJTec → 28 South Korean asset management firms via MSP compromise (September 2025)
- Betterment → 1.4 million customers via CRM vendor social engineering (January 2026)
- Western Alliance Bank → 21,899 customers via Clop's Cleo MFT exploitation

This pattern is consistent with industry data showing 41.4% of ransomware attacks start through third parties (SecurityScorecard). With 14,500 branch offices, Hartwell's vendor surface area is substantial.

**Supporting Evidence:** Claims 2.10.1–2.10.8 (confirmed FS incidents), 2.8.2–2.8.16 (CVEs), 2.9.1–2.9.9 (initial access vectors)

**Confidence Reasoning:** LOW — single-source dependency. The supply-chain pattern is the strongest finding in the incident data, but no primary sources have been independently verified.

**Caveat:** This judgment bridges PIR-01.1 and PIR-03 (supply chain risk, assigned to Dana Mercer). Coordination with Dana's research base is recommended to avoid duplication and ensure consistent treatment of supply-chain threat assessment.

---

## Key Judgment 3 (PIR-01.2: EDR Evasion as Critical TTP Shift)

**We assess with LOW confidence that BYOVD-based EDR evasion — specifically EDRKillShifter and its derivatives — represents the most significant procedural shift in the ransomware kill chain for 2025, with direct implications for Hartwell's CrowdStrike Falcon deployment.**

EDRKillShifter, originally developed by RansomHub, has been adopted by at least 8 groups including several targeting financial services: Medusa, Play, Qilin, DragonForce, and INC Ransom. ESET identified a threat actor ("QuadSwitcher") orchestrating cross-group sharing, suggesting active collaboration among typically closed RaaS operations.

Reynolds ransomware (February 2026) represents the next evolution: embedding a vulnerable driver directly in the ransomware payload — eliminating the staging step — and specifically terminating CrowdStrike Falcon, Cortex XDR, Sophos, and Symantec. This falls within the reporting window and directly threatens Hartwell's assumed EDR deployment.

Additionally, Akira demonstrated the ability to pivot to unmonitored IoT devices (a Linux-based webcam) after EDR quarantined the initial payload, encrypting the network from an agentless device. This confirms that groups are actively adapting when endpoint detection succeeds.

These findings collectively suggest that EDR alone is insufficient for ransomware defense. Defense-in-depth including network segmentation, identity-based detection, and non-traditional endpoint coverage is necessary.

**Supporting Evidence:** Claims 2.15.1–2.15.5 (BYOVD/EDR evasion), 2.3.6 (Akira IoT webcam pivot)

**Confidence Reasoning:** LOW — single-source dependency. EDRKillShifter cross-group sharing is corroborated by ESET, Arete, and The Hacker News (three named sources), trending toward MODERATE.

**Caveat:** This judgment assumes Hartwell deploys CrowdStrike Falcon as primary EDR (ASMP-03). If incorrect, the direct organizational relevance of Reynolds ransomware changes, though the broader EDR evasion trend remains applicable to any EDR platform.

---

## Key Judgment 4 (PIR-01.3: Payment Model Structural Change)

**We assess with LOW confidence that the ransomware payment model is undergoing structural change: payment rates have collapsed to historic lows (20–28% across sectors) while demands against financial services firms remain the highest of any sector ($2.0M median), creating pressure for increasingly aggressive extortion tactics.**

Three independent named sources corroborate the payment decline trend:
- Chainalysis: 28% of victims paid in 2025 (record low)
- Coveware: Payment rates fell from 25% (Q4 2024) to ~20% by Q4 2025
- Coalition: 86% of businesses refused to pay in 2025

Groups are compensating with escalating pressure tactics:
- Triple extortion: SWATting executives' homes, attempting to bribe employees (Coveware Q3 2025)
- Insurance policy theft: Stealing victims' cyber insurance policies to calibrate demands just below policy payout limits (Resilience Midyear 2025)
- Cold-calling: Akira contacting employees and clients of victim companies directly
- Data-theft-first: Encryption occurring in only 49–50% of FS attacks (six-year low), reflecting recognition that data exposure carries greater leverage against financial firms holding sensitive client information

The shift from encryption-first to data-theft-first extortion is particularly dangerous for firms holding sensitive client financial data — PII, account numbers, equity holdings, and trading histories carry premium value regardless of whether a ransom is paid.

**Supporting Evidence:** Claims 2.17.1–2.17.6 (demand ranges), 2.18.1–2.18.4 (payment rates), 2.19.1–2.19.3 (revenue), 2.21.1–2.21.6 (extortion model evolution)

**Confidence Reasoning:** LOW — single-source dependency, but this is the most corroborated finding in the research base. Three named sources independently confirm the payment rate decline. The Sophos FS-specific data is from a 2024 report (outside 90-day window). Would likely reach MODERATE upon independent verification of Chainalysis and Coveware data.

**Caveat:** Financial services-specific payment and demand data relies on the Sophos "State of Ransomware in Financial Services 2024" report — the most recent sector-specific data available but outside the 90-day reporting window. More current sector-specific data may alter the picture. Cross-sector payment data (Chainalysis, Coveware, Coalition) is current.

---

## Key Judgment 5 (PIR-01.1: Active Fortinet Threat — Time-Sensitive)

**We assess with LOW confidence that three Fortinet FortiGate vulnerabilities disclosed between December 2025 and January 2026, combined with observed pre-ransomware activity via FortiGate entry points as of March 2026, represent an active and current threat to Hartwell's perimeter.**

The specific vulnerabilities are:
- CVE-2025-59718/59719 (FortiCloud SSO bypass, CVSS 9.8): CISA KEV December 16, 2025. Active intrusions documented within three days of disclosure. Huntress reported 11 instances in 30 days.
- CVE-2026-24858 (Cross-account SSO bypass): CISA advisory January 28, 2026. Approximately 10,000 instances affected.
- SentinelOne documented campaigns using FortiGate as entry points with pre-ransomware activity observed as of March 2026.

These fall squarely within the 90-day reporting window. Fortinet FortiGate has accumulated 14 zero-day advisories in under four years, establishing a pattern of recurring critical vulnerabilities. The January 2025 CVE-2024-55591 (approximately 48,000 vulnerable devices) was already being exploited by multiple ransomware groups.

**Supporting Evidence:** Claims 2.8.1–2.8.5 (Fortinet CVEs and exploitation)

**Confidence Reasoning:** LOW — single-source dependency. CISA KEV entries and advisories are binary-verifiable and would immediately upgrade to MODERATE or HIGH upon direct verification. This is the fastest confidence upgrade available to the analyst.

**Caveat:** This judgment assumes Hartwell deploys FortiGate (ASMP-01) and that devices may not be fully patched (ASMP-04). Verification of patch levels with Vulnerability Management would either confirm this as an active organizational risk requiring immediate action or eliminate it. Given the time-sensitive nature of this finding, verification should not wait for the next quarterly PIR review cycle.

---

## Key Judgment Summary Table

| KJ | PIR | Core Assessment | Confidence | Upgrade Path |
|---|---|---|---|---|
| KJ-1 | PIR-01.1 | Qilin, Akira, Clop are top FS threats | LOW | Verify Flashpoint data + CISA advisories |
| KJ-2 | PIR-01.1 | Supply chain may exceed direct entry as organizational risk | LOW | Verify SecurityScorecard data; coordinate with PIR-03 research |
| KJ-3 | PIR-01.2 | BYOVD/EDRKillShifter is the critical TTP shift; Falcon specifically targeted | LOW | Verify ESET reporting + Huntress/Vectra AI on Reynolds |
| KJ-4 | PIR-01.3 | Payment model structural change; aggressive tactics compensating | LOW (trending MOD) | Verify Chainalysis + Coveware independently |
| KJ-5 | PIR-01.1 | Three Fortinet CVEs (Dec 2025–Jan 2026) are active, current threats | LOW | Verify CISA KEV directly (fastest upgrade) |
