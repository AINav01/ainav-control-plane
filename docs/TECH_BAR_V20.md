# Tech bar v2.0 — gold-standard integration

**Package:** `agent_gov` **2.0.0**  
**Spine:** `docs/GOLD_STANDARD.md`

## What v2.0 adds

| Module | Role |
|--------|------|
| **`redis_consume.py`** | `RedisDualConsume` — EVALSHA + NOSCRIPT retry + same-slot KEYS |
| **`redis_errors.py`** | Full Lua err catalog aligned with `dual_consume.lua` |
| **`scripts/redis/dual_consume.lua`** | In agent-governance tree |
| **`check_gold_standard.py`** | Excellence gate |

## Claim gate

Lab AdmitLock → fixtures / L1. RedisDualConsume → engineering-ready. HA claims → Redis fixtures green only.
