# Best-of integrated spine

**Date:** 2026-08-23  
**Gate:** `make gold` → GOLD STANDARD: ALL PASS  
**Package:** `agent_gov` 2.1.0  
**Prototype:** `docs/PROTOTYPE_BUILD_2026-08-23.md`

## First principles

```text
Dual humans + action_hash + single-use + fail-closed
SoR only after admit ok · L1 → P-ADM → packs · Job C only
```

## Control plane

| Asset | Path |
|-------|------|
| Gold gate | `make gold` |
| Redis dual | `redis_consume.py` · `dual_consume.lua` |
| Gold demo | `agent-governance/examples/gold_path.py` |

## Commercial

| Asset | Path |
|-------|------|
| Ops three | `COMMERCIAL_OPS_THREE.md` |
| Attach | `P_ADM_ATTACH_SCRIPT.md` |

## Prototype & review

| Doc | Role |
|------|------|
| `PROTOTYPE_BUILD_2026-08-23.md` | Working build evidence |
| `PROTOTYPE_REVIEW_GROK46.md` | Cursor deep review for Grok 4.6 |
| `MODEL_CUTOVER.md` | Model version protect |
| `GAP_CLOSURE_REGISTER.md` | OPEN vs CLOSED |

## Company gates (outside code)

```text
LIVE_PIN_OK × signed L1 × P-ADM attach
```

```bash
make gold
```
