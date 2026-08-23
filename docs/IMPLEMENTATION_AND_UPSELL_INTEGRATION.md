# Implementation & upsell integration

**Rule:** Fixtures before connectors. One admit plane for every pack. Effect only after admit ok.

## Implementation sequence

| Phase | Work | Exit |
|-------|------|------|
| 0 Kickoff | Verb lock, principals, env | Written scope |
| 1 Lab dual | Happy/deny/replay/hash paths | Customer re-runs tests |
| 2 Records | DecisionRecord + export | Reconstruct in minutes |
| 3 Optional sandbox | Dynamics cite / BC if sold | Sandbox demo only |
| 4 Readout | Risks + P-ADM proposal | Go / no-go |
| 5 P-ADM land | Prod wiring, support | Coverage live |
| 6 Packs | One at a time | Pack acceptance green |
| 7 L2 | One prod verb + monitoring | Prod admit; HA if proven |

Kickoff SLA: ≤5 business days after pilot signature.

## Technical spine

```text
Client → AdmitClient.begin → DualSession
  approve(role, principal) × N → execute
  lab AdmitLock | RedisDualConsume
  → DecisionRecord → apply_effect (ok only)
```

## Upsell integration map

| Pack | Hook | Acceptance |
|------|------|------------|
| U-DUAL | Policy + consume roles | Fixture matrix PASS |
| P-REC | After DecisionRecord | Examiner rebuild |
| U-SIEM | Sink after record | Sample events received |
| P-DEP | deploy.* Actions | Deploy fixture PASS |
| U-SOR-X | apply_effect only | Sandbox then prod |
| L2 | Prod verb | One verb live + evidence |

**Never:** second admit service per pack · soft-approve bypass · connector before kit PASS.

## Redis / multi-host (when sold)

SHA pinned · SCRIPT LOAD on primaries · `{request_id}` tags · NOSCRIPT → LOAD once · offline simulator/fixtures green before HA claim · effect idempotency outside Redis.

## Maintenance

Fixture regression every release · Lua SHA on script change · policy digests per customer release · quarterly verb scope review.

**Related:** `COMMERCIAL_OPS_THREE.md` · `U_DUAL_REDIS_ATOMIC.md` · `GOLD_STANDARD.md`
