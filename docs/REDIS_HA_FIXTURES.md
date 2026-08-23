# Redis HA fixtures — dual consume (U-DUAL)

**Purpose:** Prove **multi-host atomic dual admission** against a real Redis (standalone or Cluster).  
**Until this matrix is green:** G3 = **ENGINEERING READY**, not product HA.  
**Implementation:** `scripts/redis/dual_consume.lua` · `agent_gov.redis_consume.RedisDualConsume`

```text
Product HA claim  ⇔  this fixture matrix PASS on the target topology
```

---

## 1. What “HA fixture” means here

| Not this | This |
|----------|------|
| Offline fake Redis (`test_redis_consume_adapter`) | Live `EVALSHA` against Redis |
| Lab `AdmitLock` file store | Concurrent clients, one slot owner |
| “Script exists in git” | One `ok`, rest `err` under parallel execute |

**Atomic unit under test:** validate-all-then-write-all consume of request + N tokens on **same hash slot**.

---

## 2. Environment

| Item | Requirement |
|------|-------------|
| Redis | 6.2+ (7.x preferred); Cluster if claiming Cluster HA |
| Client | Cluster-aware if Cluster (`MOVED`/`ASK`) |
| Script | Exact bytes of `dual_consume.lua` from git |
| SHA | `SCRIPT LOAD` result pinned; `NOSCRIPT` → LOAD once → retry once |
| Keys | Always `{request_id}` tagged |

```text
ainav:req:{request_id}
ainav:tok:{request_id}:{token_id}
```

---

## 3. Seed fields

**Request:** `request_id`, `action_hash`, `consumed=0`, `revoked=0`, `expires_at`, optional `required_n`  
**Token:** `request_id`, `action_hash`, `role`, `principal` (distinct), `used=0`, `expires_at`  

Helpers: `seed_request_hash_fields` / `seed_token_hash_fields` in `redis_consume.py`.

---

## 4. Fixture matrix (must PASS)

| ID | Setup | Expect |
|----|--------|--------|
| **H1** Happy | req + 2 tokens | `{ok=executed}`; consumed + both used |
| **H2** Replay | after H1 | `already_consumed` / `token_used` |
| **H3** Partial dual | one token only | err; **zero** writes |
| **H4** Self-admit | same principal | `self_admit`; zero writes |
| **H5** Duplicate role | same role twice | `duplicate_role`; zero writes |
| **H6** Hash mismatch | ARGV ≠ stored | hash mismatch; zero writes |
| **H7** Expired | past expires_at | expired; zero writes |
| **H8** Revoked | revoked=1 | `revoked`; zero writes |
| **H9** Concurrent | 8–32 parallel EVALSHA | **exactly one** ok; single burn |
| **H10** NOSCRIPT | empty script cache | LOAD retry; no double burn |
| **H11** Wrong slot | bad/missing hash tag | CROSSSLOT / error; not ok |
| **H12** Client map | each err | reason_code; no may_apply_effect |

---

## 5. Concurrent (H9)

```text
Seed → N workers same KEYS/ARGV → barrier → EVALSHA
ok_count == 1
Redis: consumed=1, all used=1, no partial burn
Prefer ≥2 processes / hosts
```

---

## 6. Cluster extras

Same KEYSLOT for all dual keys · NOSCRIPT after failover · MOVED-safe client · LOAD on primaries that own the slot.

---

## 7. Pass → product HA

H1–H12 green + H9 multi-process + (Cluster checks if used) + recorded log → G3 may move to **CLOSED (HA proven)**.

Until then: engineering ready only.

---

## 8. Offline vs HA

| Suite | Server | Proves |
|-------|--------|--------|
| `test_redis_consume_adapter` | No | Adapter / error map |
| `test_lua_simulator` | No | Predicates |
| **This matrix** | **Yes** | Real atomicity |

**Related:** `U_DUAL_REDIS_ATOMIC.md` · `GAP_CLOSURE_REGISTER.md` (G3)
