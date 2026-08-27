# ONE PASTE — Cursor + Grok 4.6 (plane 2.2)

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

Setup: `docs/GROK46_REVIEW_SETUP.md`

--- BEGIN PASTE ---
Deep review of AINav Control Plane 2.2 as of 2026-08-26. Job C only.

**Workspace check first:**
- Need `agent-governance/agent_gov/plane.py`, `ledger.py`, `.cursorrules`, `.cursor/rules/plane-major.mdc`. Else FAIL — wrong folder.
- If the user pasted `plane MAJOR tests passed`, treat that as evidence.

## Product
Dual-admitted effect authority before privileged SoR writes.
Not inventory (Job A). Not IdP replacement (Job B).

## Plane 2.2 on main (review this)
- hasher.py — tagged digests only. V1 locked: sha256:8d4a295b1dfb76f4169193012fdb7666fb199df66f45fe94c0bfe247648f4e10
- propose() — immutable ticket + issued_at + expires_at
- admit_ticket(..., action=) — mutate / digest flip / expired → HasherError
- ConsumeLedger — same action_hash twice → replay_denied
- plane.admit() — DecisionRecord hold or deny (hash layer, not Redis dual)
- lockfile ticket_ttl_seconds (default 3600). Unknown flags deny.
- Dual-write dated window. Expire leftover tickets. Do not re-hash history.
- Default hash_alg=sha256, sig_alg=none.
- Gate: cd agent-governance && PYTHONPATH=. python3 tests/test_plane_major.py

## Commercial
L1 $28–40k · P-ADM $40–60k/yr · U-DUAL $20–35k/yr never free. No invented SKUs.

## OPEN (do not fake-close)
G1/G10 LIVE_PIN_OK · G12 legal · G13 signed L1 · G14 live SoR · HA after Redis H1–H12

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
