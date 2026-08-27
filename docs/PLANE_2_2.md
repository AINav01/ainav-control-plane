# Plane 2.2

Same Job C. Same V1 digest. New: ticket TTL, replay ledger, `admit()` → DecisionRecord.

```python
from agent_gov.plane import admit
from agent_gov.ledger import ConsumeLedger
from agent_gov.lockfile import default_lockfile

lock = default_lockfile()
book = ConsumeLedger()
rec = admit(action, lock, ledger=book)   # hold_pending_approval
again = admit(action, lock, ledger=book) # deny replay_denied if same ticket hash consumed
```

V1: `sha256:8d4a295b1dfb76f4169193012fdb7666fb199df66f45fe94c0bfe247648f4e10`

Gate: `cd agent-governance && PYTHONPATH=. python3 tests/test_plane_major.py`
Review: `docs/PASTE_GROK46_REVIEW.md` + Grok 4.6 in Cursor.
