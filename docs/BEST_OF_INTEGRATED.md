# Best-of integrated spine

**Date:** 2026-08-23  
**Gate:** `make gold` → GOLD STANDARD: ALL PASS  
**Package:** `agent_gov` 2.1.x  

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
| Dual consume Lua | `scripts/redis/dual_consume.lua` (+ agent-governance copy) |
| Redis client | `agent_gov/redis_consume.py` |
| Error map | `agent_gov/redis_errors.py` |
| Offline Lua predicates | `agent_gov/lua_simulator.py` |
| One-shot admit→effect | `DualSession.run_and_apply` / `AdmitClient.admit_and_apply` |
| Demo | `agent-governance/examples/gold_path.py` |

**HA rule:** Multi-host dual only after Redis fixtures green. Lab = AdmitLock.

---

## 3. Commercial (go-to-market)

| Asset | Path |
|-------|------|
| **Three ops docs** | `docs/COMMERCIAL_OPS_THREE.md` |
| Availability + repo ACL | `docs/COMMERCIAL_AVAILABILITY_AND_ENTITLEMENT.md` |
| Sales & purchase | `docs/SALES_PURCHASE_PROCESS.md` |
| Implementation + upsells | `docs/IMPLEMENTATION_AND_UPSELL_INTEGRATION.md` |
| L1 land | `docs/FIRST_OFFER.md` |
| P-ADM attach playbook | `docs/P_ADM_ATTACH_PLAYBOOK.md` |
| **P-ADM attach script** | `docs/P_ADM_ATTACH_SCRIPT.md` |
| Must-have offering | `docs/MUST_HAVE_OFFERING.md` · `docs/OFFERING.md` |

```text
L1 $28–40k → kit PASS → P-ADM $40–60k/yr ≤90 days → U-DUAL $20–35k/yr (never free)
```

---

## 4. U-DUAL + Redis atomic

| Asset | Path |
|-------|------|
| Pack specifics | Rate card / dual control pack · this spine §4 |
| Redis atomic deep dive | `docs/U_DUAL_REDIS_ATOMIC.md` |
| Dual index | `docs/DUAL_INDEX.md` |
| Canonical dual doctrine | `docs/AINav_Dual_Admission_Canonical_v1.md` |

**Promise:** N-role, hash-bound, both-or-neither, single-use, fail-closed.  
**Multi-host:** `EVALSHA dual_consume.lua` on `{request_id}`-tagged keys.

---

## 5. Cursor

| Asset | Path |
|-------|------|
| Project rules | `.cursorrules` |
| Open guide | `CURSOR.md` · `OPEN_IN_CURSOR.md` |
| Azure pin rule | `.cursor/rules/azure-pin-edge.mdc` |
| Redis dual rule | `.cursor/rules/redis-lua-dual-admit.mdc` |

Clone: `https://github.com/AINav01/ainav-control-plane.git` → Open Folder in Cursor.

---

## 6. Company gates (still outside code)

```text
LIVE_PIN_OK  ×  signed L1 FIRST_OFFER  ×  P-ADM attach
```

Code can be gold while the pin is still wrong DNS or L1 is unsigned.

---

## 7. Verify

```bash
make gold
# or
python3 scripts/check_gold_standard.py
```

**Bottom line:** Best-of is one **admit plane**, one **commercial sequence**, one **U-DUAL Redis burn**, and one **Cursor doctrine**—not a pile of essays.
