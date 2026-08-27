# ONE PASTE — Cursor + Grok 4.6 (plane 2.3)

## Folder

**WRONG:** New Project / empty `/workspace`.
**RIGHT:** Open Folder = clone of **ainav-control-plane**.

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane && git pull origin main
cd agent-governance && PYTHONPATH=. python3 tests/test_plane_major.py
```

Need: `plane MAJOR tests passed`.

Then: **File → Open Folder → ainav-control-plane** → **Grok 4.6** → new chat → paste BEGIN–END **and** the test output.

--- BEGIN PASTE ---
Deep review of AINav Control Plane 2.3 as of 2026-08-26. Job C only.

**Workspace check first:**
- Need agent-governance/agent_gov/plane.py, gates.py, ledger.py, .cursorrules, .cursor/rules/plane-major.mdc. Else FAIL — wrong folder.
- If the user pasted `plane MAJOR tests passed`, treat that as evidence.

## Product
Dual-admitted effect authority before privileged SoR writes. Not Job A inventory. Not Job B IdP.

## Plane 2.3 on main (review this)
- hasher — tagged only. V1 locked: sha256:8d4a295b1dfb76f4169193012fdb7666fb199df66f45fe94c0bfe247648f4e10
- propose() — immutable ticket + request_id + issued_at + expires_at
- admit_ticket requires action, expires_at, policy_digest
- gates.py — halt_api → halt_engaged; nonempty allowlist must hit resource.id or params token/token_id/asset
- ConsumeLedger — in-process replay only, not U-DUAL / Redis
- plane.admit() — hold or deny DecisionRecord; ledger required
- Dual-write dated window. Expire leftover tickets. Do not re-hash history.
- Default hash_alg=sha256, sig_alg=none, plane 2.3.0
- Gate: cd agent-governance && PYTHONPATH=. python3 tests/test_plane_major.py

## Commercial
L1 $28–40k · P-ADM $40–60k/yr · U-DUAL $20–35k/yr never free. No invented SKUs.

## OPEN
LIVE_PIN_OK · signed L1 · live SoR · Redis dual HA

## Must-not-change
Job C · dual · tagged action_hash · fail-closed · expire-not-convert · no LIVE_PIN_OK without curl

## Deliver exactly
1. Verdict PASS | PASS WITH NOTES | FAIL
2. Evidence
3. Solid
4. Thin / over-claimed
5. Top 5 (S/M/L; ops|eng|commercial)
6. Must-not-change
7. Next 7 days — ONE action
--- END PASTE ---
