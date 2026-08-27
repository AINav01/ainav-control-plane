# Plane 2.3

Hash layer. Not Redis dual. V1 digest unchanged.

```python
from agent_gov import admit, ConsumeLedger, default_lockfile, propose, admit_ticket

lock = default_lockfile()
book = ConsumeLedger("seen.json")   # optional persist; still not U-DUAL
ticket = propose(action, lock)      # gates run here too
admit_ticket(ticket, lock, action=action)  # request_id + expires_at + digest required
rec = admit(action, lock, ledger=book)
```

- `halt_api` → no ticket, no admit (`halt_engaged`)
- unimplemented flag True (`acrs_enforced`, `sentinel_export`, …) → `flag_not_implemented`
- nonempty allowlist → `resource.id` or params token/token_id/asset/instrument/coin/stablecoin
- replay keyed by `action_hash`; new `request_id` does not reset
- `extra=` cannot overwrite `request_id` or hash fields
