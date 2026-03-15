# Gate 3 — Analyst Relevance Decisions

## Disposition Summary

- **RELEVANT claims retained:** All claims marked RELEVANT below proceed to Gate 4.
- **PARTIALLY RELEVANT retained (essential context):** 1, 3, 6, 9, 12, 24, 27, 34, 35, 37, 42, 43, 47, 51, 62, 69, 73, 83, 117, 119
- **PARTIALLY RELEVANT cut (redundant with more detailed claims):** 99, 100, 101, 102 — these are ATT&CK summary stats that duplicate claims 53-54, 87-92, and 93-96 respectively. Remove from research base.
- **NOT RELEVANT — remove:** 30, 70, 118

---

## PIR-01.1 Claims

| # | Verdict |
|---|---|
| 1 | PARTIALLY RELEVANT — retain (ecosystem scale context) |
| 2 | RELEVANT |
| 3 | PARTIALLY RELEVANT — retain (global trend context) |
| 4 | RELEVANT |
| 5 | RELEVANT |
| 6 | PARTIALLY RELEVANT — retain (ecosystem fragmentation context) |
| 7 | RELEVANT |
| 8 | RELEVANT |
| 9 | PARTIALLY RELEVANT — retain (attribution context) |
| 10 | RELEVANT |
| 11 | RELEVANT |
| 12 | PARTIALLY RELEVANT — retain (operational model context) |
| 13 | RELEVANT |
| 14 | RELEVANT |
| 15 | RELEVANT |
| 16 | RELEVANT |
| 17 | RELEVANT |
| 18 | PARTIALLY RELEVANT — retain (evasion during confirmed intrusion) |
| 19 | RELEVANT |
| 20 | RELEVANT |
| 21 | RELEVANT |
| 22 | RELEVANT |
| 23 | RELEVANT |
| 24 | PARTIALLY RELEVANT — retain (infrastructure migration context) |
| 25 | RELEVANT |
| 26 | RELEVANT |
| 27 | PARTIALLY RELEVANT — retain (active group, limited FS-specific confirmation) |
| 28 | RELEVANT |
| 29 | PARTIALLY RELEVANT — cut (business model detail, not an intrusion) |
| 30 | NOT RELEVANT — remove |
| 31 | RELEVANT |
| 32 | NOT RELEVANT — remove |
| 33 | RELEVANT |
| 34 | PARTIALLY RELEVANT — retain (emerging group, no confirmed FS targeting yet) |
| 35 | PARTIALLY RELEVANT — retain (same) |
| 36 | RELEVANT |
| 37 | PARTIALLY RELEVANT — retain (Fortinet risk context) |
| 38 | RELEVANT |
| 39 | RELEVANT |
| 40 | RELEVANT |
| 41 | RELEVANT |
| 42 | PARTIALLY RELEVANT — retain (confirmed exploitation, not explicitly FS-tied) |
| 43 | PARTIALLY RELEVANT — retain (group-CVE mapping) |
| 44 | RELEVANT |
| 45 | RELEVANT |
| 46 | RELEVANT |
| 47 | PARTIALLY RELEVANT — retain (no confirmed ransomware exploitation yet, but Veeam risk) |
| 48 | RELEVANT |
| 49 | RELEVANT |
| 50 | RELEVANT |
| 51 | PARTIALLY RELEVANT — retain (FS targeting, secondary group) |
| 52 | RELEVANT |
| 53 | RELEVANT |
| 54 | RELEVANT |
| 55 | RELEVANT |
| 56 | RELEVANT |
| 57 | RELEVANT |
| 58 | RELEVANT |
| 59 | RELEVANT |
| 60 | RELEVANT |
| 61 | RELEVANT |
| 62 | PARTIALLY RELEVANT — retain (nation-state ClickFix adoption, context) |
| 63 | RELEVANT |
| 64 | RELEVANT |
| 65 | RELEVANT |
| 66 | RELEVANT |
| 67 | RELEVANT |
| 68 | RELEVANT |
| 69 | PARTIALLY RELEVANT — retain (leak site appearances, limited detail) |
| 70 | NOT RELEVANT — remove |
| 71 | RELEVANT |

## PIR-01.2 Claims

| # | Verdict |
|---|---|
| 72 | RELEVANT |
| 73 | PARTIALLY RELEVANT — retain (emerging C2, limited FS confirmation) |
| 74 | RELEVANT |
| 75 | RELEVANT |
| 76 | RELEVANT |
| 77 | RELEVANT |
| 78 | RELEVANT |
| 79 | RELEVANT |
| 80 | RELEVANT |
| 81 | RELEVANT |
| 82 | RELEVANT |
| 83 | PARTIALLY RELEVANT — retain (victim environment condition, not attacker TTP) |
| 84 | RELEVANT |
| 85 | RELEVANT |
| 86 | RELEVANT |
| 87 | RELEVANT |
| 88 | RELEVANT |
| 89 | RELEVANT |
| 90 | RELEVANT |
| 91 | RELEVANT |
| 92 | RELEVANT |
| 93 | RELEVANT |
| 94 | RELEVANT |
| 95 | RELEVANT |
| 96 | RELEVANT |
| 97 | RELEVANT |
| 98 | PARTIALLY RELEVANT — cut (generic prevalence stat, not procedure-level) |
| 99 | PARTIALLY RELEVANT — cut (redundant with claims 53-54) |
| 100 | PARTIALLY RELEVANT — cut (redundant with claims 53-54) |
| 101 | PARTIALLY RELEVANT — cut (redundant with claims 93-96) |
| 102 | PARTIALLY RELEVANT — cut (redundant with claims 87-92) |
| 103 | RELEVANT |

## PIR-01.3 Claims

| # | Verdict |
|---|---|
| 104 | RELEVANT |
| 105 | RELEVANT |
| 106 | RELEVANT |
| 107 | RELEVANT |
| 108 | RELEVANT |
| 109 | RELEVANT |
| 110 | RELEVANT |
| 111 | RELEVANT |
| 112 | RELEVANT |
| 113 | RELEVANT |
| 114 | RELEVANT |
| 115 | RELEVANT |
| 116 | RELEVANT |
| 117 | PARTIALLY RELEVANT — retain (payment rail context for CISO decisions) |
| 118 | NOT RELEVANT — remove |
| 119 | PARTIALLY RELEVANT — retain (OFAC designations affect payment decisions) |
| 120 | RELEVANT |
| 121 | RELEVANT |
| 122 | RELEVANT |
| 123 | RELEVANT |
| 124 | RELEVANT |
| 125 | RELEVANT |
| 126 | RELEVANT |
| 127 | RELEVANT |
| 128 | RELEVANT |

---

## Claims Removed (7 total)

| # | Reason |
|---|---|
| 30 | NOT RELEVANT — law enforcement action against developer, doesn't answer 01.1 |
| 32 | NOT RELEVANT — leadership attribution, intel community interest only |
| 70 | NOT RELEVANT — affiliate identity anecdote |
| 98 | Redundant — generic prevalence stat, not procedure-level |
| 99 | Redundant — summary of claims 53-54 |
| 100 | Redundant — summary of claims 53-54 |
| 101 | Redundant — summary of claims 93-96 |
| 102 | Redundant — summary of claims 87-92 |
| 118 | NOT RELEVANT — cryptocurrency laundering methodology |

**Note:** Claim 29 (LockBit $500 affiliate fees) was also cut as PARTIALLY RELEVANT with insufficient value — business model detail, not an intrusion.

**Total claims proceeding to Gate 4:** 118 (128 original minus 10 removed)
