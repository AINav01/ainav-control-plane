# AINav — maximum product bar

**As of:** 2026-08-20  
**Meaning:** The highest bar we will **implement and test** for dual admission — not marketing superlatives.

```text
MAXIMUM BAR =
  hash-bound dual
  × distinct named principals
  × atomic single-host consume
  × fail-closed on every failure mode below
  × DecisionRecord reconstructable
  × runnable fixture suite (CI)
```

---

## Non-negotiable product rules

| # | Rule |
|---|------|
| 1 | Explicit SoD roles on dual-class verbs |
| 2 | Tokens bound to request_id + action_hash |
| 3 | Triple hash at execute |
| 4 | All tokens burned together or none |
| 5 | Single-use; replay fails |
| 6 | Dual requires named principal per token |
| 7 | Same principal cannot fill two roles |
| 8 | Partial dual / expiry / revoke / hash mismatch → no effect |
| 9 | evaluate never consumes |
| 10 | DecisionRecord on allow and deny paths |

---

## Runnable proof suite

```bash
cd agent-governance
bash scripts/run_gap_closure_fixtures.sh
python3 tests/test_maximum_product_bar.py
```

| Test | Pass condition |
|------|----------------|
| Happy dual | executed; 2 tokens used |
| Replay | Second consume fails |
| Partial dual | Fail; zero tokens used |
| Hash mutation | Fail |
| Concurrent ×8 | Exactly one success |
| Self-approve | Fail |
| Missing principal | Fail |
| Revoke / expired | Fail |

---

## Host tiers

| Tier | Claim |
|------|-------|
| L1 / fixtures | Single-host AdmitLock |
| Production single host | + principals always set |
| Production multi-host | Redis Lua / SQL required before HA marketing |
