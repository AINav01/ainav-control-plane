# U-DUAL Redis atomic implementation

**SKU:** U-DUAL ($20–35k/yr) · **Multi-host burn:** `dual_consume.lua`  
**Client:** `agent_gov.redis_consume.RedisDualConsume`  
**Errors:** `agent_gov.redis_errors`

---

## Why

Lab AdmitLock proves dual. Multi-writer production needs **one atomic consume** so concurrent executes yield exactly one `ok`.

---

## Keys (Cluster-safe)

```text
ainav:req:{request_id}
ainav:tok:{request_id}:{token_id}
```

All KEYS share `{request_id}` → one slot → multi-key Lua allowed.

---

## Contract

```text
EVALSHA <sha> N+1  req tok…  expected_hash now

1. Validate request (exists, not consumed/revoked/expired, hash match)
2. Validate every token (used, expiry, hash, request_id, unique role, unique principal)
3. On any fail → {err=code} with **zero** writes
4. Else mark all tokens used + request consumed → {ok=executed, n=…}
```

Hash is computed in the **app**; Lua only compares.

---

## Client

```text
SCRIPT LOAD → sticky SHA
EVALSHA on execute
NOSCRIPT → LOAD once → retry once
Map err → reason_code → fail-closed (no SoR)
```

---

## U-DUAL mapping

| Promise | Implementation |
|---------|----------------|
| N roles / SoD | Unique `role` + `principal` in script |
| Hash-bound | ARGV + request + token `action_hash` |
| Both-or-neither | Validate-all-then-write-all |
| Single-use | `consumed` / `used` flags |
| Fail-closed | `{err}` → no effect |
| Multi-host | Lua atomicity on slot owner |

**Never claim HA** until Redis fixture matrix is green. Effect stays outside Redis with idempotency key.

**Related:** `scripts/redis/dual_consume.lua` · `docs/BEST_OF_INTEGRATED.md` · `docs/GOLD_STANDARD.md`
