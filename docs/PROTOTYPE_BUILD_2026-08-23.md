# AINav Control Plane — working prototype build

**Build date:** 2026-08-23  
**Package:** `agent_gov` **2.1.0**  
**Gate:** `make gold` → **GOLD STANDARD: ALL PASS**  
**Gold path demo:** `GOLD PATH OK`  
**Repo:** https://github.com/AINav01/ainav-control-plane  

This is the **complete working lab prototype** as of today: dual-admitted effect authority end-to-end, offline Redis dual predicates, commercial ops docs, Cursor doctrine. Not a claim of LIVE_PIN_OK or multi-host HA in production.

---

## 1. What works (verified)

| Capability | How to run | Result |
|------------|------------|--------|
| Dual admit → gated SoR | `cd agent-governance && PYTHONPATH=. python3 examples/gold_path.py` | `GOLD PATH OK` |
| Offline dual predicates (Lua mirror) | `PYTHONPATH=. python3 tests/test_lua_simulator.py` | `ALL PASS` |
| Full offline suite | `make gold` (repo root) | `GOLD STANDARD: ALL PASS` |
| Action hash goldens | `tests/test_action_hash_golden.py` | PASS |
| Atomic dual (lab lock) | `tests/test_atomic_dual_consume.py` | PASS |
| Maximum product bar | `tests/test_maximum_product_bar.py` | PASS |
| Redis adapter (offline) | `tests/test_redis_consume_adapter.py` | PASS |
| Local pin health (strict) | `check_azure_swa_health --local --strict` | PASS |

---

## 2. Prototype architecture

```text
build_action / ActionMapper
        ↓
AdmitClient.begin(Action)
        ↓
DualSession  (required roles)
  approve(role_a, principal_a)
  approve(role_b, principal_b)
  execute  →  AdmitLock (lab) | RedisDualConsume (multi-host path)
        ↓
ok → DecisionRecord → apply_effect(idempotency_key)
err → fail-closed, no SoR
```

| Layer | Module |
|-------|--------|
| Client API | `agent_gov/client.py` |
| Action + hash | `action.py` · `action_map.py` |
| Lab atomic dual | `admit_lock.py` · tokens |
| Redis multi-host | `redis_consume.py` · `scripts/redis/dual_consume.lua` |
| Offline Lua mirror | `lua_simulator.py` |
| Effect gate | `effect.py` |

**HA rule:** Engineering ready; **product claim only after Redis fixtures green.**

---

## 3. Minimal reproduce

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
make gold
cd agent-governance && PYTHONPATH=. python3 examples/gold_path.py
```

```python
from agent_gov import AdmitClient, DualSession, build_action

action = build_action(
    resource_type="bank.payment",
    resource_id="pay_1",
    verb="post",
    params={"amount": 2500, "currency": "USD", "beneficiary": "acct_9"},
    evidence={"payment_batch_id": "batch_1"},
)
client = AdmitClient.in_memory()
session = client.begin(action)
receipt = session.run_and_apply(
    [("payments_ops", "ops@co"), ("payments_risk", "risk@co")],
    connector.apply,
)
assert receipt.admit_ok
```

---

## 4. Commercial / ops docs (bundled)

| Doc | Role |
|------|------|
| `BEST_OF_INTEGRATED.md` | Spine map |
| `P_ADM_ATTACH_SCRIPT.md` | Attach after kit PASS |
| `U_DUAL_REDIS_ATOMIC.md` | Multi-host atomicity |
| `MODEL_CUTOVER.md` | Grok 4.5 → 4.6 protect |
| `GAP_CLOSURE_REGISTER.md` | Honest OPEN/CLOSED |
| `PROTOTYPE_REVIEW_GROK46.md` | Deep review brief for Cursor |

SKU spine: **L1 $28–40k → P-ADM $40–60k/yr → U-DUAL $20–35k/yr (never free).**

---

## 5. Explicit non-claims

```text
✗ LIVE_PIN_OK — ops OPEN
✗ Multi-host HA dual in production — Redis fixtures first
✗ Signed L1 / revenue — commercial OPEN
✗ Live Dynamics/BC without unlock
```

---

## 6. Cursor deep review (Grok 4.6)

1. `git pull` · Open Folder  
2. Read `docs/PROTOTYPE_REVIEW_GROK46.md`  
3. Follow `.cursorrules`  
4. Run `make gold`  
5. Deliver review in the format in that brief  

**Related:** `MODEL_CUTOVER.md` · `BEST_OF_INTEGRATED.md`
