# Cursor deep-review prompt (Grok 4.6)

Copy everything below the line into a **new** Cursor chat with model **Grok 4.6**.

---

Deep review of AINav Control Plane (prototype as of 2026-08-23).

**Follow (in order):**
1. `.cursorrules`
2. `docs/MASTER_AS_OF_2026-08-23.md`
3. `docs/PROTOTYPE_REVIEW_GROK46.md`

**Evidence first — run in the terminal:**
```bash
./scripts/review_sandbox.sh
```
If that fails, stop and report the failure. Do not review on a red gate.

**Hard rules:**
- Job C only (dual-admitted effect authority)
- Dual: distinct principals, action_hash, single-use, fail-closed
- Repo and command output > prior chat memory
- Do not invent SKUs
- Do not claim LIVE_PIN_OK, product multi-host HA, or signed L1 without evidence in the repo or command output
- Redis dual = engineering ready until live H1–H12 green (`docs/REDIS_HA_FIXTURES.md`)

**Deliver exactly this structure:**
1. **Verdict** — PASS | PASS WITH NOTES | FAIL
2. **Evidence** — quote gold / gold_path result lines
3. **Solid** — what is proven
4. **Thin / over-claimed** — what is not proven
5. **Top 5 improvements** — ranked; effort S/M/L; owner ops|eng|commercial
6. **Must-not-change**
7. **Next 7 days** — one primary action only

Be strict. Prefer fixtures and docs over confidence.
