# Gap closure register — AINav

**As of:** 2026-08-23 (pass 5 — repo-complete + model cutover protect)  
**Bar:** [`PRODUCT_BAR_MAXIMUM.md`](PRODUCT_BAR_MAXIMUM.md) · [`BEST_OF_INTEGRATED.md`](BEST_OF_INTEGRATED.md)  
**Purpose:** Close every **in-repo** gap. Name external blockers without fake-closing them.

```text
SUCCESS = LIVE_PIN_OK × proof day × signed L1 FIRST_OFFER × P-ADM attach
```

---

## Register

| ID | Gap | Status | Evidence / action |
|----|-----|--------|-------------------|
| **G1** | Public **LIVE_PIN_OK** | **OPEN (ops)** | Source ready (`mothership/www`). Needs Azure SWA deploy + DNS off Squarespace. |
| **G2** | Atomic dual consume (single-host) | **CLOSED+** | `AdmitLock` + fixture matrix green. |
| **G3** | Atomic dual consume (multi-host) | **ENGINEERING READY** | `dual_consume.lua` + `RedisDualConsume` + simulator. **HA claim only after Redis fixtures green.** |
| **G4** | Fixture battery / gold gate | **CLOSED** | `make gold` · `check_gold_standard.py`. |
| **G5** | DecisionRecord Acceptance Kit | **CLOSED** | Pilot exit = reconstruct. |
| **G6** | Dual Control Pack + failure matrix | **CLOSED** | Pack + matrix + `DUAL_INDEX.md`. |
| **G7** | RFP Job C evaluation criteria | **CLOSED** | Soft HITL fails. |
| **G8** | Mothership metadata policy | **CLOSED** | |
| **G9** | Institute product pages (source) | **CLOSED (source)** | `mothership/www/`. |
| **G10** | Public edge = source | **OPEN (ops)** | Same cutover as G1. |
| **G11** | Language discipline | **CLOSED** | Guidance in rules + business model. |
| **G12** | Delaware entity + bank | **OPEN (legal)** | Not a repo task. |
| **G13** | Signed L1 / first revenue | **OPEN (commercial)** | FIRST_OFFER motion. |
| **G14** | Live SoR unlock claims | **OPEN (gated)** | Requires pin + proof day. |
| **G15** | Commercial ops three + attach script | **CLOSED** | Ops three + `P_ADM_ATTACH_SCRIPT.md` on `main`. |
| **G16** | Best-of spine + Cursor rules | **CLOSED** | `BEST_OF_INTEGRATED.md` · `.cursorrules` · `CURSOR.md`. |
| **G17** | GitHub ↔ local best-of sync | **CLOSED** | Gap-fill commit on `main`. |
| **G18** | Model cutover protect (→ 4.6) | **CLOSED** | `docs/MODEL_CUTOVER.md` + Cursor pointer. |

---

## Completion tiers

| Tier | Status | Meaning |
|------|--------|--------|
| **Repo-complete** | **YES** | G2–G9, G11, G15–G18 closed or engineering-ready as documented |
| **Ops-complete** | **NO** | Needs G1 + G10 |
| **Company-complete** | **NO** | Needs G12 + G13 (+ G14 gated) |

---

## Do not claim

```text
✗ LIVE_PIN_OK without health.json proof
✗ Multi-host HA dual without Redis fixtures green
✗ Market-proven / first revenue without signed L1
✗ Live SoR authority without commercial unlock
```

**Related:** `MODEL_CUTOVER.md` · `BEST_OF_INTEGRATED.md` · `GOLD_STANDARD.md`
