# Best-of integrated spine

**Date:** 2026-08-23  
**Gate:** `make gold` → GOLD STANDARD: ALL PASS  
**Package:** `agent_gov` 2.1.x  
**Gaps:** Repo-complete — see `GAP_CLOSURE_REGISTER.md`

One place to find the best of control plane + commercial + U-DUAL Redis work.

---

## 1. First principles (non-negotiable)

```text
Agents propose privileged writes → dual humans + action_hash + single-use consume + fail-closed
SoR only after admit ok (idempotent)
Fixtures before production · L1 prove → P-ADM cover → packs deepen
Job C only (not inventory, not IdP)
```

---

## 2. Control plane (engineering)

| Asset | Path |
|-------|------|
| Gold gate | `scripts/check_gold_standard.py` · `make gold` |
| Gold doctrine | `docs/GOLD_STANDARD.md` |
| Dual consume Lua | `scripts/redis/dual_consume.lua` |
| Redis client | `agent_gov/redis_consume.py` |
| Error map | `agent_gov/redis_errors.py` |
| Offline Lua predicates | `agent_gov/lua_simulator.py` |
| One-shot admit→effect | `DualSession.run_and_apply` / `AdmitClient.admit_and_apply` |

**HA rule:** Multi-host dual only after Redis fixtures green. Lab = AdmitLock.

---

## 3. Commercial (go-to-market)

| Asset | Path |
|-------|------|
| Three ops docs | `docs/COMMERCIAL_OPS_THREE.md` |
| Availability + ACL | `docs/COMMERCIAL_AVAILABILITY_AND_ENTITLEMENT.md` |
| Sales & purchase | `docs/SALES_PURCHASE_PROCESS.md` |
| Implementation + upsells | `docs/IMPLEMENTATION_AND_UPSELL_INTEGRATION.md` |
| P-ADM attach script | `docs/P_ADM_ATTACH_SCRIPT.md` |

```text
L1 $28–40k → kit PASS → P-ADM $40–60k/yr ≤90 days → U-DUAL $20–35k/yr (never free)
```

---

## 4. U-DUAL + Redis atomic

| Asset | Path |
|-------|------|
| Redis atomic | `docs/U_DUAL_REDIS_ATOMIC.md` |
| Dual index | `docs/DUAL_INDEX.md` |

---

## 5. Cursor & model cutover

| Asset | Path |
|-------|------|
| Project rules | `.cursorrules` |
| Open guide | `CURSOR.md` |
| Model cutover | `docs/MODEL_CUTOVER.md` |
| Gap register | `docs/GAP_CLOSURE_REGISTER.md` |

Clone: `https://github.com/AINav01/ainav-control-plane.git` → Open Folder in Cursor.

---

## 6. Company gates (still outside code)

```text
LIVE_PIN_OK  ×  signed L1 FIRST_OFFER  ×  P-ADM attach
```

---

## 7. Verify

```bash
make gold
```

**Bottom line:** One admit plane, one commercial sequence, one U-DUAL Redis burn, one Cursor doctrine — model version does not rewrite the bar.
