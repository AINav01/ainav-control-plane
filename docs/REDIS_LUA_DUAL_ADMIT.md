# Redis Lua dual admit — canonical playbook

**AINav Control Plane · multi-host effect authority**  
**Status:** Engineering doctrine for Redis-backed dual consume (Job C).  
**Scope:** Atomic check-and-burn of dual (or N-role) tokens before privileged SoR writes.

Related: `docs/DUAL_INDEX.md` · product dual admission · DecisionRecords.

---

## 0. One-page summary

```text
App:  hash Action · policy (PDP) · build KEYS · EVALSHA · on ok → DecisionRecord → SoR (idempotent)
Redis Lua:  validate ALL predicates → then burn ALL tokens + request · return {ok|err}
Never:  policy-in-Lua · partial burn · effect before ok · fail-open on Redis errors
```

| Layer | Owns |
|-------|------|
| **App** | Canonical hash, PDP, orchestration, DecisionRecord, SoR effect |
| **Redis Lua** | Atomic dual predicates + single-use burn |
| **SoR** | Business write with idempotency key |

**Admit atomicity ≠ end-to-end transaction with Dynamics/BC.** Effect is always *after* `ok`, with idempotent apply.

---

## 1. When to use Lua

| Use Lua | Avoid in Lua |
|---------|----------------|
| Atomic check-then-act | Heavy policy / OPA trees |
| Multi-key updates in **one hash slot** | Cross-slot “transactions” |
| Dual token burn, CAS, short locks | HTTP, SoR, large JSON transforms |
| Short, deterministic state changes | Long loops / SCAN over big sets |

---

## 2. Atomicity guarantees

### Guaranteed (single node / slot owner)

While a script runs, Redis does **not** interleave other commands on that node:

| Guarantee | Meaning |
|-----------|---------|
| No interleaving | No other client runs mid-script on that node |
| Atomic visibility | Others never see half the script’s writes |
| Check-then-act | Reads + writes share one consistent view |
| Fail-closed structure | Validate all → return `err` with **zero** writes; else write all → `ok` |

`EVAL` and `EVALSHA` have the **same** atomicity.

### Not guaranteed

| Non-guarantee | Implication |
|---------------|-------------|
| Cross-slot atomicity | All KEYS must share one `{request_id}` hash tag |
| Durability | AOF/fsync is separate from “atomic” |
| External systems | SoR is outside the script |
| Correct business logic | A buggy script is still “atomic” |
| Multi-primary / active-active | Own consistency model required |

### Dual outcome under concurrency

```text
Two EVALSHA same request_id → exactly one ok; rest err
Partial dual / hash mismatch → err, no writes
```

---

## 3. Key layout (Cluster-safe)

```text
ainav:req:{request_id}
ainav:tok:{request_id}:{token_id}
```

| Rule | Why |
|------|-----|
| Same `{request_id}` on every key in the script | One slot → one primary |
| Every touched key listed in `KEYS` | Cluster routing + clarity |
| No `KEYS` / big `SCAN` inside consume | Bounded latency |

---

## 4. EVALSHA lifecycle

```text
SCRIPT LOAD <source>  →  sha
EVALSHA <sha> numkeys keys… args…
on NOSCRIPT           →  LOAD once + EVALSHA once (no tight loop)
```

| Prefer | Avoid |
|--------|--------|
| Sticky SHA in process memory | Full `EVAL` every request |
| Version script text in git | Silent prod body edits |
| LOAD before traffic / on boot | Rely only on first-hit recovery |
| Handle restart / failover `NOSCRIPT` | `SCRIPT FLUSH` on live traffic |

### EVAL vs EVALSHA performance

| | EVAL | EVALSHA (hit) |
|--|------|----------------|
| Wire payload | Full source | ~40-byte SHA |
| Compile path | Higher if cold | Cached body |
| **Execution / atomicity** | **Same** | **Same** |

Hot-path win is **bytes + cache**, not faster opcodes.

### NOSCRIPT retry overhead

| Path | Typical cost |
|------|----------------|
| Cache hit | 1 × RTT + sub-ms script |
| Miss recovery | ~3 × RTT (`EVALSHA` fail + `LOAD` + `EVALSHA`) |

Keep `NOSCRIPT` rate ≈ 0 in steady state. Use **single-flight LOAD** under herd after restart.

### Cluster script cache

| Fact | |
|------|-|
| Script cache is **per node** | Not cluster-global |
| Primary → its replicas | `SCRIPT LOAD` usually propagates; **effects** of writes replicate |
| Primary A → Primary B | **No** shared Lua cache |
| Slot owner must have SHA | Or `NOSCRIPT` → LOAD on that node |

---

## 5. Reference consume contract

```text
KEYS[1]     = request hash key
KEYS[2..N]  = token hash keys (N = number of roles, typically 2)
ARGV[1]     = expected action_hash (app-canonicalized)
ARGV[2]     = now (unix seconds) for expiry checks
```

### Predicates (all must pass before any write)

**Request:** exists · not consumed · not revoked · not expired · `action_hash` matches ARGV[1]  
**Each token:** exists · not used · not expired · hash matches · `request_id` binds · role distinct as required

### Returns

| Reply | Meaning |
|-------|---------|
| `{ok='executed'}` | All burned; client may DecisionRecord + effect |
| `{err='already_consumed'\|'token_used'\|'hash_mismatch'\|…}` | Business deny; **no** writes |

Use **return values** for dual denials. Reserve Lua `error()` for programmer misuse (wrong `numkeys`, invariants).

### Client

```text
result = EVALSHA(sha, keys, [hash, now])
if ok:
  DecisionRecord(executed_after_dual_admit)
  effect(SoR) with idempotency_key
else:
  fail-closed
on Timeout / uncertain:
  reconcile; never double-post SoR
on NOSCRIPT:
  LOAD once; EVALSHA once
on Redis down:
  fail-closed
```

---

## 6. Reference Lua (validate-all-then-write-all)

See also: `scripts/redis/dual_consume.lua`

```lua
-- KEYS[1]=request, KEYS[2..N]=tokens
-- ARGV[1]=expected_hash, ARGV[2]=now

local function hget(key, field, default)
  local v = redis.call('HGET', key, field)
  if v == false then return default end
  return v
end

if redis.call('EXISTS', KEYS[1]) == 0 then
  return {err='unknown_request'}
end

if hget(KEYS[1], 'consumed', '0') == '1' then
  return {err='already_consumed'}
end

if hget(KEYS[1], 'revoked', '0') == '1' then
  return {err='revoked'}
end

local exp = tonumber(hget(KEYS[1], 'expires', '0'))
if exp > 0 and tonumber(ARGV[2]) > exp then
  return {err='expired'}
end

if hget(KEYS[1], 'action_hash', '') ~= ARGV[1] then
  return {err='hash_mismatch'}
end

for i = 2, #KEYS do
  local tk = KEYS[i]
  if redis.call('EXISTS', tk) == 0 then
    return {err='missing_token'}
  end
  if hget(tk, 'used', '0') == '1' then
    return {err='token_used'}
  end
  local texp = tonumber(hget(tk, 'expires', '0'))
  if texp > 0 and tonumber(ARGV[2]) > texp then
    return {err='token_expired'}
  end
  if hget(tk, 'action_hash', '') ~= ARGV[1] then
    return {err='token_hash_mismatch'}
  end
end

-- All checks passed — burn
for i = 2, #KEYS do
  redis.call('HSET', KEYS[i], 'used', '1', 'used_at', ARGV[2])
end
redis.call('HSET', KEYS[1], 'consumed', '1', 'consumed_at', ARGV[2])

return {ok='executed'}
```

Keep out of Lua: canonical JSON, PDP, SoR HTTP, secrets, verbose success logging.

---

## 7. Performance optimization

Priority order:

| # | Technique | Gain |
|---|-----------|------|
| 1 | One `EVALSHA` check-and-act | 1 RTT vs N HGET/HSET + races |
| 2 | `SCRIPT LOAD` + sticky SHA | Less payload/compile |
| 3 | Hash-tagged same-slot keys | No cross-slot retries |
| 4 | Hash/policy in app | Lua compares short strings |
| 5 | Early exit + thin HGET/HSET | Less work on reject/success |
| 6 | Connection pooling | Lower RTT variance |

**Target:** sub-ms script time; one RTT for consume.

### Script length

Short scripts protect the event loop. Move hash/policy/effects to the app. Do **not** delete dual predicates to save lines. Aim ~30–80 lines for dual consume, not a policy engine.

---

## 8. Performance profiling

| Layer | Tool |
|-------|------|
| Server script time | `SLOWLOG`, `INFO commandstats` (`usec_per_call`) |
| Client RTT | Histogram around `EVALSHA` |
| Errors | `NOSCRIPT`, timeout, cross-slot counters |

```text
CONFIG SET slowlog-log-slower-than 1000
SLOWLOG GET 32
INFO commandstats
```

| Pattern | Action |
|---------|--------|
| High RTT, low slowlog | Network / pool / region |
| High RTT, high slowlog | Fat script / hot node |
| `NOSCRIPT` spikes | LOAD on deploy/restart |
| High business `err`, low duration | Contention — not CPU |

OSS Redis has no line-by-line Lua profiler; treat the script as one unit.

---

## 9. Debugging techniques

| Class | Example | Handle |
|-------|---------|--------|
| Business `err` | `already_consumed` | Metrics by code; fail-closed |
| Runtime error | nil index, bad call | Fix script |
| Transport | `NOSCRIPT`, timeout | Retry/load; never assume success |

**Reproduce with `redis-cli`:** seed HASHes → `EVALSHA` → matrix (happy, replay, bad hash, missing token, concurrent).

**Binary search:** read-only snapshot return → add checks → add writes last.

```lua
redis.log(redis.LOG_WARNING, "consume " .. KEYS[1])  -- staging; no secrets
```

**Nil guards:** `HGET` missing field returns `false` — default before compare.

**`SCRIPT DEBUG`:** staging only; `SYNC` can block the node — never routine prod.

### Dual-consume debug checklist

```text
□ KEYS count/order match script
□ All keys share {request_id}
□ Request fields: consumed, revoked, expires, action_hash
□ Token fields: used, expires, action_hash, request_id, role
□ ARGV hash format matches stored hash
□ 1st call ok; 2nd already_consumed
□ Parallel: exactly one ok
□ NOSCRIPT → LOAD → retry after restart
```

---

## 10. Fixture matrix (minimum)

| Case | Expect |
|------|--------|
| Happy dual | `ok`; both tokens used; request consumed |
| Replay | `already_consumed` / `token_used`; no double effect |
| Partial dual (one token only) | `err`; no writes |
| Hash mismatch | `err`; no writes |
| Concurrent double execute | One `ok`, one `err` |
| Expired / revoked | `err` |
| After Redis restart | `NOSCRIPT` recovered once; then normal |

---

## 11. Metrics

```text
redis_evalsha_duration_ms     (histogram)
redis_evalsha_ok_total
redis_evalsha_err_total{code=}
redis_evalsha_noscript_total
redis_evalsha_timeout_total
```

Alert on p99 budget, `NOSCRIPT` spikes, error-rate spikes — separate business `err` from infra failures.

---

## 12. Doctrine alignment (AINav)

| Rule | |
|------|-|
| Job C | Effect authority only |
| Fail-closed | Redis errors / denials → no SoR write |
| Dual | Named distinct principals; action_hash bind; single-use |
| DecisionRecord | After successful admit, before/with effect path |
| Not claimed until wired | Multi-host Redis must pass fixtures before product claims |

---

## 13. Anti-patterns

| Avoid | Why |
|-------|-----|
| Chatty HGET/HSET without Lua | Races + RTT × N |
| Policy engine inside Lua | Blocks Redis; hard to audit |
| Effect before `ok` | Dual bypass |
| Infinite `NOSCRIPT` retry | Amplifies outages |
| Cross-slot keys | Hard failures / wrong mental model |
| `SCRIPT FLUSH` in prod | Mass cache miss |
| Logging tokens / PII in `redis.log` | Leakage |

---

**Bottom line:** One short, versioned, `EVALSHA`-cached script on **same-slot keys**, **validate-all-then-write-all**, clear **ok/err**, **fail-closed** clients, **hash/policy/SoR outside Redis**. That is multi-host dual admit atomicity for AINav Control Plane.
