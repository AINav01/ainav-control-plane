# Plane 2.3

On 2.2: halt gate, allowlist gate, `request_id` on every ticket.

```python
from agent_gov import admit, ConsumeLedger, default_lockfile, propose

lock = default_lockfile()          # halt_api False, allowlist []
rec = admit(action, lock, ledger=ConsumeLedger())
```

`flags.halt_api: true` → every admit is `halt_engaged`.
Non-empty `allowlist` → resource.id or params.token / token_id / asset must match.
Flip halt or allowlist → `policy_digest` moves → in-flight tickets deny.

Still hash layer. Not Redis dual. V1 digest unchanged.
