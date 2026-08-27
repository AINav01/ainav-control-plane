# Plane 2.4

On 2.3: in-process dual seats (A ≠ B) and effector idempotency.
Still not Redis. Still not a live SoR. V1 digest unchanged.

```python
from agent_gov import admit, ConsumeLedger, default_lockfile, EffectLedger, idempotency_key

rec = admit(action, default_lockfile(), ledger=ConsumeLedger())           # hold, no seats
rec = admit(action, lock, ledger=book, seat_a="oid-1", seat_b="oid-2")  # dual consumed
rec = admit(action, lock, ledger=book, seat_a="oid-1", seat_b="oid-1")  # sod_denied

key = idempotency_key(rec["request_id"], rec["action_hash"])
EffectLedger().effect(rec["request_id"], rec["action_hash"])
```

Omit both seats → 2.3 `hold_pending_approval`.
Pass one seat → `ticket_incomplete`.
Same seat twice → `sod_denied`.
Both distinct → `dual_consumed_pending_effector` (still not an SoR post).
