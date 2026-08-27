# Plane 2.2

Same Job C. Same V1 digest. Tickets TTL-bound. Replay via in-process ledger. `admit()` → DecisionRecord.

```python
from agent_gov import admit, ConsumeLedger, default_lockfile, propose, admit_ticket

lock = default_lockfile()
book = ConsumeLedger()
ticket = propose(action, lock)
admit_ticket(ticket, lock, action=action)  # action, expires_at, digest required
rec = admit(action, lock, ledger=book)     # ledger required
```

Missing action / expires_at / policy_digest / ledger → `ticket_incomplete`.
Ledger is not U-DUAL.

V1: `sha256:8d4a295b1dfb76f4169193012fdb7666fb199df66f45fe94c0bfe247648f4e10`

Gate: `cd agent-governance && PYTHONPATH=. python3 tests/test_plane_major.py`
