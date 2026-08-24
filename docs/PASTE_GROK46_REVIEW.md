# ONE PASTE — Cursor + Grok 4.6 (self-contained)

## Critical: which folder Cursor opens

**WRONG:** Cursor “New Project” / empty initializer → review **must stop** (no fixtures).  
**RIGHT:** Open Folder = clone of **ainav-control-plane** (has `scripts/review_sandbox.sh`, `agent-governance/`, `.cursorrules`).

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
git pull
bash scripts/review_sandbox.sh    # must print RESULT: PASS
```

Then: **File → Open Folder → `ainav-control-plane`** (the folder that contains `scripts/` and `docs/`) → model **Grok 4.6** → new chat → paste between BEGIN and END → **also paste the sandbox terminal output**.

**GitHub:** https://github.com/AINav01/ainav-control-plane/blob/main/docs/PASTE_GROK46_REVIEW.md

--- BEGIN PASTE ---
Deep review of AINav Control Plane. Prototype as of 2026-08-23.

**Workspace check (do this first):**
- If this Cursor workspace has no `scripts/review_sandbox.sh`, no `agent-governance/`, and no `.cursorrules`, you are in the WRONG folder (empty New Project). Verdict: FAIL — wrong workspace. Tell the user: clone AINav01/ainav-control-plane, Open Folder on that root, re-run sandbox, re-paste.
- If user pastes sandbox output containing `RESULT: PASS` and `GOLD PATH OK`, treat that as evidence even if local tools are limited.
- All product context below is in this message. Do not refuse review only because you cannot open other docs—use this brief + pasted terminal output.

## Product (Job C only)
AINav Control Plane: dual-admitted effect authority before privileged system-of-record writes.
- NOT agent inventory (Job A). NOT IdP replacement (Job B).
- Agent proposes Action → two distinct humans approve (roles + principals) → action_hash bound → single-use atomic consume → DecisionRecord → SoR apply ONLY if admit ok → fail-closed otherwise.

## Commercial spine
- L1 FIRST_OFFER $28–40k (2–4 weeks) prove with Acceptance Kit
- P-ADM $40–60k/yr keep coverage (attach after kit PASS; never soft dual)
- U-DUAL $20–35k/yr depth pack — NEVER free with P-ADM or U-SOR
- Packs deepen same admit plane; no second control product
- Success equation: LIVE_PIN_OK × proof day × signed L1 × P-ADM attach

## Build status (lab — proven offline when sandbox PASS)
- agent_gov ~2.1.0: AdmitClient, DualSession, run_and_apply / admit_and_apply, effect gate, RedisDualConsume, lua_simulator
- dual_consume.lua: validate-all-then-write-all; same-slot keys; {ok}|{err}
- Gates: make gold / bash scripts/review_sandbox.sh → GOLD STANDARD ALL PASS + GOLD PATH OK
- H9 concurrent offline: exactly one ok (simulator)
- Live Redis H1–H12 required for PRODUCT multi-host HA; else G3 = engineering ready only

## OPEN gaps (do not mark closed)
- G1/G10 LIVE_PIN_OK — ops
- G12 entity/bank — legal
- G13 signed L1 — commercial
- G14 live SoR — gated
- Product HA — only after live Redis fixtures green

## Must-not-change
Job C only · dual distinct principals · action_hash · single-use · fail-closed · SoR only after ok · no free U-DUAL · no soft HITL as dual · no inventing SKUs · no LIVE_PIN_OK/HA/L1 without evidence

## Deliver exactly
1. Verdict — PASS | PASS WITH NOTES | FAIL (use FAIL only for wrong workspace or red sandbox; otherwise PASS WITH NOTES is normal without live pin)
2. Evidence — workspace path check + sandbox lines user pasted
3. Solid
4. Thin / over-claimed
5. Top 5 improvements (S/M/L; ops|eng|commercial)
6. Must-not-change (confirm)
7. Next 7 days — ONE primary action only

Be strict. Prefer this brief + pasted fixtures over confidence.
--- END PASTE ---
