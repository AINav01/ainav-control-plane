# Plane MAJOR (SchemaVer 1)

Tagged `action_hash`. One hasher. Tickets from `propose()`. Expire, do not convert.

```bash
cd agent-governance
PYTHONPATH=. python3 tests/test_plane_major.py
```

```python
from agent_gov import propose, admit_ticket, load_lockfile

lock = load_lockfile("agent-governance/data/lockfile.example.json")
ticket = propose(action, lock)
admit_ticket(ticket, lock, action=action)
```

V1: `sha256:8d4a295b1dfb76f4169193012fdb7666fb199df66f45fe94c0bfe247648f4e10`

Default `hash_alg=sha256`. SHA3-256 only inside a dated dual-write window. `sig_alg=none` until U-HSM.
