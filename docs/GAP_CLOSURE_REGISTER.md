# Gap closure register — AINav

**As of:** 2026-08-23 (pass 4 — best-of integrate + Redis adapter + commercial ops)  
**Bar:** [`PRODUCT_BAR_MAXIMUM.md`](PRODUCT_BAR_MAXIMUM.md) · [`BEST_OF_INTEGRATED.md`](BEST_OF_INTEGRATED.md)  
**Purpose:** Track every gap. Close in-repo items; name external blockers without fake-closing them.

```text
SUCCESS = LIVE_PIN_OK × proof day × signed L1 FIRST_OFFER × P-ADM attach
```

---

## Register

| ID | Gap | Status | Evidence / action |
|----|-----|--------|-------------------|
| **G1** | Public **LIVE_PIN_OK** | **OPEN (ops)** | Site source ready (`mothership/www`). Deploy Azure SWA + DNS off Squarespace. |
| **G2** | Atomic dual consume (single-host) | **CLOSED+** | `AdmitLock` + fixtures green. |
| **G3** | Atomic dual consume (multi-host HA) | **ENGINEERING READY** | `dual_consume.lua` + `RedisDualConsume` + `redis_errors` + lua_simulator. **Product HA claim only after Redis fixtures green.** `U_DUAL_REDIS_ATOMIC.md`. |
| **G4** | Fixture battery CI | **CLOSED** | `run_gap_closure_fixtures.sh` + `check_gold_standard.py` / `make gold`. |
| **G5** | DecisionRecord Acceptance Kit | **CLOSED** | Pilot exit = non-author reconstruct. |
| **G6** | Dual Control Pack + failure matrix | **CLOSED** | Pack + matrix + `DUAL_INDEX.md`. |
| **G7** | RFP Job C evaluation criteria | **CLOSED** | Soft HITL fails. |
| **G8** | Mothership metadata policy | **CLOSED** | |
| **G9** | Institute product pages (source) | **CLOSED (source)** | `mothership/www/`. |
| **G10** | Public edge = source | **OPEN (ops)** | Cutover so buyers do not hit construction-only. |
| **G11** | Language discipline | **CLOSED (guidance)** | |
| **G12** | Delaware entity + bank | **OPEN (legal)** | Not a repo task. |
| **G13** | Signed L1 / first revenue | **OPEN (commercial)** | FIRST_OFFER motion. |
| **G14** | Commercial unlock / live SoR claims | **OPEN (gated)** | Pin + proof day. |
| **G15** | Commercial ops three | **CLOSED (artifact)** | `COMMERCIAL_OPS_THREE.md` + availability/sales/impl + `P_ADM_ATTACH_SCRIPT.md`. |
| **G16** | Best-of spine + Cursor rules | **CLOSED (artifact)** | `BEST_OF_INTEGRATED.md` · `.cursorrules` · `CURSOR.md` · `make gold`. |
| **G17** | GitHub ↔ local sync of best-of | **CLOSED (this commit)** | Commercial detail + Cursor + gap register on `main`. |

---

## Tiers

| Tier | Meaning |
|------|--------|
| **Repo-complete** | G2–G9, G11, G15–G17 closed |
| **Ops-complete** | + G1, G10 (LIVE_PIN_OK) |
| **Company-complete** | + G12, G13, G14 |
