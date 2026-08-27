# Plane MAJOR / 2.2

Tagged `action_hash`. Tickets from `propose()`. TTL + replay ledger. `admit()` → DecisionRecord.

```bash
cd agent-governance
PYTHONPATH=. python3 tests/test_plane_major.py
```

```python
from agent_gov import admit, ConsumeLedger, default_lockfile, propose, admit_ticket

lock = default_lockfile()
ticket = propose(action, lock)
admit_ticket(ticket, lock, action=action)
rec = admit(action, lock, ledger=ConsumeLedger())
```

V1: `sha256:8d4a295b1dfb76f4169193012fdb7666fb199df66f45fe94c0bfe247648f4e10`

See `docs/PLANE_2_2.md`. Review paste: `docs/PASTE_GROK46_REVIEW.md`.
