# ONE PASTE — Cursor + Grok 4.6

## Folder

**WRONG:** New Project / empty `/workspace`.
**RIGHT:** Open Folder = clone of **ainav-control-plane** (has `.cursorrules`, `agent-governance/`, `.cursor/rules/plane-major.mdc`).

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane && git pull
cd agent-governance && PYTHONPATH=. python3 tests/test_plane_major.py
```

Need: `plane MAJOR tests passed`.

Then: **File → Open Folder → ainav-control-plane** → model **Grok 4.6** → new chat → paste BEGIN–END **and** the test output.

Setup: `docs/GROK46_REVIEW_SETUP.md`

--- BEGIN PASTE ---
Deep review of AINav Control Plane as of 2026-08-26. Job C only.

**Workspace check first:**
- If this workspace has no `agent-governance/agent_gov/hasher.py`, no `.cursorrules`, no `.cursor/rules/plane-major.mdc` → FAIL — wrong folder. Tell the user to clone AINav01/ainav-control-plane and Open Folder on that root.
- If the user pasted `plane MAJOR tests passed`, treat that as evidence.

## Product
Dual-admitted effect authority before privileged SoR writes.
Not inventory (Job A). Not IdP replacement (Job B).
Agent proposes Action → two distinct humans → action_hash bound → single-use consume → DecisionRecord → SoR only if admit ok → fail-closed otherwise.

## Plane MAJOR on main (review this)
- One hasher: agent_gov.hasher. Tagged digests only (`sha256:<64 hex>`).
- Tickets from propose() only. Immutable. admit_ticket(..., action=) denies flip, digest move, mutate.
- Lockfile flags fail-closed. Unknown flags and half-open cutover windows deny.
- Dual-write is a dated window on NEW rows. Expire leftover tickets. Do not re-hash history.
- Default hash_alg=sha256, canonical_ver=v1, sig_alg=none.
- V1 locked: sha256:8d4a295b1dfb76f4169193012fdb7666fb199df66f45fe94c0bfe247648f4e10
- Gate: cd agent-governance && PYTHONPATH=. python3 tests/test_plane_major.py
- CI: .github/workflows/plane-major.yml

## Commercial spine
- L1 $28–40k prove with fixtures zip. Green eval ≠ production license.
- P-ADM $40–60k/yr the plane.
- U-DUAL $20–35k/yr never free with P-ADM or U-SOR.
- Packs attach. No second control product. No invented SKUs.

## OPEN (do not fake-close)
- G1/G10 LIVE_PIN_OK — ops (ainav.institute still parking until DNS cut)
- G12 entity/bank — legal
- G13 signed L1 — commercial
- G14 live SoR — gated
- Product HA — only after live Redis H1–H12

## Must-not-change
Job C only · dual distinct principals · tagged action_hash · single-use · fail-closed · SoR only after ok · expire-not-convert · no soft HITL · no free U-DUAL · no LIVE_PIN_OK without curl evidence

## Deliver exactly
1. Verdict — PASS | PASS WITH NOTES | FAIL (FAIL only for wrong workspace or red tests)
2. Evidence — path check + pasted test lines
3. Solid
4. Thin / over-claimed
5. Top 5 improvements (S/M/L; ops|eng|commercial)
6. Must-not-change (confirm)
7. Next 7 days — ONE primary action only

Be strict. Prefer this brief + pasted fixtures over confidence.
--- END PASTE ---
