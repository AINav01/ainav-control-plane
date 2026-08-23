# Dual admission — index
### Canonical entry point · August 23, 2026

**Preferred name:** **dual admission** (product) · **U-DUAL** (SKU) · **Dual Control Pack** (demo/SOW bundle)

| Priority | Doc | Use when |
|----------|-----|----------|
| **0** | **`GOLD_STANDARD.md`** | **Deep review + integrated business/tech spine** |
| **1** | `AINav_Dual_Admission_Canonical_v1.md` | Default doctrine + lifecycle |
| **2** | `AINav_Dual_Control_Pack.md` | Demo script + SOW paste |
| **3** | `AINav_Dual_Failure_Matrix.md` | Fail-closed outcomes |
| **4** | `AINav_DecisionRecord_Acceptance_Kit.md` | Pilot exit / reconstruct |
| **5** | `PRODUCT_BAR_MAXIMUM.md` | Maximum bar + fixture suite |
| **6** | `GAP_CLOSURE_REGISTER.md` | What is closed vs open |
| **7** | **`REDIS_LUA_DUAL_ADMIT.md`** | **Multi-host Redis Lua consume (v2)** |
| **8** | `TECH_BAR_V20.md` | Client + Redis adapter + effect bar |

**Code (lab):** `agent-governance/agent_gov/tokens.py` · `admit_lock.py`  
**Code (client):** `client.py` · `action_map.py` · `effect.py`  
**Redis:** `scripts/redis/dual_consume.lua` · `agent_gov/redis_consume.py` · `redis_errors.py`  
**Tests:** `scripts/run_gap_closure_fixtures.sh` · `scripts/check_gold_standard.py`  
**Cursor:** `.cursor/rules/redis-lua-dual-admit.mdc`

**Rule:** Dual admission is **effect authority**, not agent-security intent-block.  
**Multi-host:** Redis Lua + `RedisDualConsume` are engineering-ready; **product HA claims only after Redis fixtures green**.
