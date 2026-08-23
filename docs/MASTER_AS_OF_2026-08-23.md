# AINav — master status as of 2026-08-23 19:52 EDT

**UTC:** 2026-08-23 23:52  
**Repo:** https://github.com/AINav01/ainav-control-plane  
**Package:** `agent_gov` 2.1.0  
**Gate:** `make gold` → **GOLD STANDARD: ALL PASS**  
**Tier:** **REPO-COMPLETE** · ops/company **not** complete

This is the single stay-on-track document for business model, plan, build, and next moves.

---

## 1. Business model (Job C only)

```text
Problem:  Agents write to money / ledgers / access without dual-admitted authority
Product:  Dual humans + action_hash + single-use consume + fail-closed + DecisionRecord
SoR:      Only after admit ok (idempotent)
Not:      Agent inventory, IdP replacement, soft HITL theater
```

| SKU | Band | Role |
|-----|------|------|
| **L1** (FIX/SALES/FULL) | $28–40k | Prove dual in 2–4 weeks |
| **P-ADM** | $40–60k/yr | Keep the loop covered |
| **U-DUAL** | $20–35k/yr | Depth (SoD / high-blast); **never free** |
| **P-REC / U-SIEM / P-DEP / U-SOR-*** | Quoted | Export, SIEM, change gates, one SoR |
| **L2** | Quoted | One production verb |

**Motion:** L1 → kit PASS → P-ADM attach ≤14 days / convert ≤90 days → packs.

**Success equation:**

```text
LIVE_PIN_OK × proof day × signed L1 × P-ADM attach
```

---

## 2. Why must-have

Privileged agent writes without dual, hash-bound, fail-closed authority = **open-loop power**.  
Logs and IdP do not answer: *Who dual-admitted this exact effect?*

---

## 3. Build status (lab prototype)

| Capability | Status | Evidence |
|------------|--------|----------|
| Dual admit → gated effect | **Working** | `examples/gold_path.py` → GOLD PATH OK |
| Lab atomic dual | **Working** | AdmitLock + fixture matrix |
| Offline Lua predicates | **Working** | `lua_simulator` + tests |
| Redis dual adapter + Lua | **Engineering ready** | `redis_consume.py` · `dual_consume.lua` |
| H9 concurrent (offline) | **Working** | 16 workers → exactly one ok |
| H9 concurrent (live Redis) | **Skipped until REDIS_URL** | `@pytest.mark.redis_ha` |
| Gold gate | **PASS** | `make gold` |
| Commercial ops docs | **On main** | Ops three + attach script |
| Cursor doctrine | **On main** | `.cursorrules` · `CURSOR.md` |

**Explicit non-claims:** LIVE_PIN_OK · product multi-host HA · signed L1 · live SoR unlock.

---

## 4. Architecture (one plane)

```text
ActionMapper / build_action
  → AdmitClient.begin
  → DualSession approve × N (distinct principals)
  → execute:
        lab:      AdmitLock
        multi-host: RedisDualConsume + dual_consume.lua
  → ok → DecisionRecord → apply_effect(idempotency_key)
  → err → fail-closed
```

Redis: same-slot `{request_id}` · validate-all-then-write-all · NOSCRIPT→LOAD once.

HA claim gate: full matrix in `REDIS_HA_FIXTURES.md` (H1–H12) green on target Redis.

---

## 5. Gaps (honest)

| Status | IDs |
|--------|-----|
| **CLOSED / eng-ready** | G2–G9, G11, G15–G19; G3 engineering ready |
| **OPEN ops** | G1, G10 — LIVE_PIN_OK / public edge |
| **OPEN legal** | G12 — entity + bank |
| **OPEN commercial** | G13 — signed L1 |
| **OPEN gated** | G14 — live SoR unlock |

See `GAP_CLOSURE_REGISTER.md` · `COMPLETION_STATUS.md`.

---

## 6. Plan — next 7–30 days

| Priority | Action | Owner |
|----------|--------|--------|
| **1** | LIVE_PIN_OK (Azure SWA + DNS) | Ops |
| **2** | FIRST_OFFER → signed L1 | Commercial |
| **3** | On kit PASS: P-ADM attach script | Sales |
| **4** | Optional: REDIS_URL + H1–H12 for HA claim | Eng |
| **5** | No new doctrine docs unless blocked | All |

**Do not:** soft dual, free U-DUAL, invent SKUs, claim HA/pin without evidence.

---

## 7. Stay on track (Cursor + GitHub)

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane && git pull
make gold
```

**Cursor:** File → Open Folder → this repo (loads `.cursorrules`).

| Read first | Path |
|------------|------|
| **This master** | `docs/MASTER_AS_OF_2026-08-23.md` |
| Best-of map | `docs/BEST_OF_INTEGRATED.md` |
| Completion | `docs/COMPLETION_STATUS.md` |
| Prototype | `docs/PROTOTYPE_BUILD_2026-08-23.md` |
| Attach | `docs/P_ADM_ATTACH_SCRIPT.md` |
| Redis HA | `docs/REDIS_HA_FIXTURES.md` |
| Gaps | `docs/GAP_CLOSURE_REGISTER.md` |
| Model cutover | `docs/MODEL_CUTOVER.md` |

**Chat starter:**

```text
Follow .cursorrules and docs/MASTER_AS_OF_2026-08-23.md.
Job C only. Dual fail-closed. Repo truth > chat memory.
Do not invent SKUs or claim LIVE_PIN_OK / HA without evidence.
```

---

## 8. Industries (context, not new SKUs)

Stablecoin / tokenization / crypto asset ops / payments — same Job C.  
GENIUS raises urgency for issuer ops; do not claim regulatory certification.

---

## 9. Bottom line

**Repo and lab prototype are done and gated.**  
**Company progress = pin live + paid L1 + P-ADM.**  
Everything else is optional depth on the same admit plane.
