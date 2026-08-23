# AINav gold standard — deep review & integrated spine

**Date:** 2026-08-23  
**Purpose:** First-principles review of the whole build, then the single spine that makes business + tech best-in-class.

---

## 1. First principles (non-negotiable)

```text
1. Agents propose writes. Unadmitted effects = open-loop authority = control failure.
2. Dual admission binds humans to an exact Action (action_hash), not a ticket.
3. Tokens are single-use; consume is both-or-neither; deny paths write nothing.
4. SoR effects run only after admit ok — fail-closed, idempotent.
5. Prove with fixtures before production. Cover with annual P-ADM.
6. The public pin is JSON truth, not marketing HTML.
7. Job C only — effect authority. Not inventory (A), not IdP (B).
```

Everything else is packaging, ops, or implementation detail.

---

## 2. Deep review — what is already gold

| Layer | Assessment |
|-------|------------|
| **Doctrine** | Clear, examiner-testable, refuse list is real |
| **Dual predicates** | Principals, SoD, hash triple-lock, single-use — correct |
| **`dual_consume.lua` v2** | Validate-all-then-write-all; stable `{ok|err}`; Cluster tags |
| **`AdmitClient` / `DualSession`** | Envelope + next_step + effect gates |
| **`action_map` / hash** | Deterministic mapping + golden vectors |
| **`redis_errors` + `effect`** | Transport vs business; SoR only after ok |
| **Lab fixtures** | MAXIMUM BAR / atomic dual / client / tech bar — **PASS** |
| **Must-have offering** | L1 → P-ADM sequence; walk conditions |
| **Azure pin ops** | healthz + health.json + FD probe/alerts + KQL selectivity |
| **Cursor rules** | Doctrine + Redis + Azure pin |

---

## 3. Deep review — gaps (honest)

| Gap | Severity | Status after this pass |
|-----|----------|------------------------|
| Redis consume **not wired** into TokenService product path | High for HA claims | **Adapter shipped**; lab still AdmitLock until HA SOW + fixtures |
| Error-code drift (Lua vs Python map) | Medium | **Aligned** |
| Doc sprawl (many Redis essays) | Low | **This spine + REDIS_LUA_DUAL_ADMIT** are canonical |
| **LIVE_PIN_OK** still Squarespace HTML | **Company-critical** | Ops: Azure SWA + DNS — not a code gap |
| No single excellence gate | Medium | **`check_gold_standard.py`** |
| Script only under top-level `scripts/redis` | Medium | **Also under `agent-governance/scripts/redis`** |

---

## 4. Integrated architecture (gold)

```text
Agents / tools → ActionMapper → AdmitClient / DualSession
  → approve × N → execute
  → lab: AdmitLock | multi-host: RedisDualConsume + dual_consume.lua
  → DecisionRecord → apply_effect (ok only) → SoR

Public edge (no admit): SWA /healthz.json + /health.json
```

---

## 5. Business gold path

```text
LIVE_PIN_OK → L1 FIRST_OFFER $28–40k → Kit PASS → P-ADM $40–60k/yr ≤ 90 days
```

**Walk:** inventory RFPs, soft HITL, fail-open, approve without hash.

---

## 6. Verify

```bash
python3 scripts/check_gold_standard.py
cd agent-governance && PYTHONPATH=. python3 tests/test_redis_consume_adapter.py
```

---

**Bottom line:** Engineering-gold on admit doctrine and lab proof. Company-gold when **LIVE_PIN_OK × signed L1 → P-ADM** land.
