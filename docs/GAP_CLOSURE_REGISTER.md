# Gap closure register — AINav

**As of:** 2026-08-20 (pass 3 — maximum product bar)  
**Bar:** [`PRODUCT_BAR_MAXIMUM.md`](PRODUCT_BAR_MAXIMUM.md)  
**Purpose:** Track every gap from the “make better” upgrade path. Close in-repo items; name external blockers without fake-closing them.

```text
SUCCESS = LIVE_PIN_OK × proof day × signed L1 FIRST_OFFER
```

---

## Register

| ID | Gap | Status | Evidence / action |
|----|-----|--------|-------------------|
| **G1** | Public **LIVE_PIN_OK** | **OPEN (ops)** | Site source ready (`mothership/www`). Deploy cutover required. |
| **G2** | Atomic dual consume (single-host) | **CLOSED+** | AdmitLock + FileStore/MemoryStore; principal on issue; self-approve blocked. |
| **G3** | Atomic dual consume (multi-host HA) | **SPEC COMPLETE / RUNTIME NOT WIRED** | Redis Lua in snippets/token_consume_redis_lua.md |
| **G4** | Fixture battery CI | **CLOSED** | scripts/run_gap_closure_fixtures.sh |
| **G5** | DecisionRecord Acceptance Kit | **CLOSED (artifact)** | docs/AINav_DecisionRecord_Acceptance_Kit.md |
| **G6** | Dual Control Pack + failure matrix | **CLOSED (artifact)** | Dual Control Pack, Failure Matrix, DUAL_INDEX |
| **G7** | RFP Job C evaluation criteria | **CLOSED** | docs/RFP_EVALUATION_CRITERIA_JOB_C.md |
| **G8** | Mothership / client IP metadata policy | **CLOSED** | docs/MOTHERSHIP_METADATA_POLICY.md |
| **G9** | Institute product pages (source) | **CLOSED (source)** | mothership/www/ |
| **G10** | Public edge = source | **OPEN (ops)** | Cloudflare cutover |
| **G11** | Language discipline | **CLOSED (guidance)** | No unearned gold/SOTA |
| **G12** | Delaware entity + bank | **OPEN (legal)** | Formation |
| **G13** | Signed L1 / first revenue | **OPEN (commercial)** | FIRST_OFFER |
| **G14** | Commercial unlock / live SoR claims | **OPEN (gated)** | Pin + proof day |

---

## Tiers

| Tier | Meaning |
|------|---------|
| **Repo-complete** | G2, G4–G9, G11 |
| **Ops-complete** | + G1, G10 |
| **Company-complete** | + G12, G13, G14 |
