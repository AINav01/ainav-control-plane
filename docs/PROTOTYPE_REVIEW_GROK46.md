# Deep review brief — Grok 4.6 in Cursor

**Prototype:** AINav Control Plane · build **2026-08-23** · `agent_gov` **2.1.0**  
**Audience:** Grok 4.6 reviewing this repo in Cursor  
**Rule:** Repo truth > chat memory. Do not soften dual or invent SKUs.

---

## Mission

Deep review of the working prototype: dual admission correctness, fail-closed behavior, Redis atomicity honesty, commercial consistency, and gaps.

---

## Required reading (in order)

1. `.cursorrules`
2. `docs/BEST_OF_INTEGRATED.md`
3. `docs/PROTOTYPE_BUILD_2026-08-23.md`
4. `docs/GOLD_STANDARD.md`
5. `docs/U_DUAL_REDIS_ATOMIC.md`
6. `docs/GAP_CLOSURE_REGISTER.md`
7. `docs/MODEL_CUTOVER.md`
8. `docs/P_ADM_ATTACH_SCRIPT.md`

Optional: `scripts/redis/dual_consume.lua` · `agent_gov/client.py` · `lua_simulator.py`

---

## Commands before opinions

```bash
make gold
cd agent-governance && PYTHONPATH=. python3 examples/gold_path.py
PYTHONPATH=. python3 tests/test_lua_simulator.py
```

---

## Review checklist

**A. Dual** — distinct principals; hash bind; single-use; partial dual no execute; SoR only after ok  
**B. Redis/HA** — lab vs Lua; same-slot tags; no HA claim without fixtures; effect outside Lua  
**C. Commercial** — L1→P-ADM→packs; U-DUAL never free; attach = coverage  
**D. Gaps** — G1/G10/G13 still OPEN; do not fake-close  
**E. Model** — no new SKUs; no soft HITL as dual  

---

## Output format

```text
1. Verdict: PASS / PASS WITH NOTES / FAIL
2. What is solid
3. What is over-claimed or thin
4. Top 5 improvements (ranked, effort S/M/L)
5. Must-not-change list
6. Suggested next 7-day plan
```

---

## Chat starter (paste in Cursor)

```text
You are reviewing AINav Control Plane prototype build 2026-08-23.
Follow .cursorrules and docs/PROTOTYPE_REVIEW_GROK46.md.
Run make gold and examples/gold_path.py before conclusions.
Job C only. Dual fail-closed. Do not invent SKUs or claim LIVE_PIN_OK/HA without evidence.
Deliver the review in the output format specified in PROTOTYPE_REVIEW_GROK46.md.
```

**Repo:** https://github.com/AINav01/ainav-control-plane
