# Dual admission — index
### Canonical entry point · August 22, 2026

**Preferred name:** **dual admission** (product) · **U-DUAL** (SKU) · **Dual Control Pack** (demo/SOW bundle)

| Priority | Doc | Use when |
|----------|-----|----------|
| **1** | `AINav_Dual_Admission_Canonical_v1.md` | Default doctrine + lifecycle |
| **2** | `AINav_Dual_Control_Pack.md` | Demo script + SOW paste |
| **3** | `AINav_Dual_Failure_Matrix.md` | Fail-closed outcomes |
| **4** | `AINav_DecisionRecord_Acceptance_Kit.md` | Pilot exit / reconstruct |
| **5** | `PRODUCT_BAR_MAXIMUM.md` | Maximum bar + fixture suite |
| **6** | `GAP_CLOSURE_REGISTER.md` | What is closed vs open |
| **7** | **`REDIS_LUA_DUAL_ADMIT.md`** | **Multi-host Redis Lua consume playbook** |

**Code:** `agent-governance/agent_gov/tokens.py` · `admit_lock.py`  
**Redis script:** `scripts/redis/dual_consume.lua`  
**Tests:** `scripts/run_gap_closure_fixtures.sh`  
**Cursor:** `.cursor/rules/redis-lua-dual-admit.mdc`

**Rule:** Dual admission is **effect authority**, not agent-security intent-block.  
**Multi-host:** Redis Lua path is engineering-ready; product claims only after fixtures green.
