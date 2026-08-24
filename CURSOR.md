# Open AINav Control Plane in Cursor

**Master (stay on track):** `docs/MASTER_AS_OF_2026-08-23.md`  
**As of:** 2026-08-23 19:52 EDT · **Repo-complete** · pin/L1 still OPEN

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane && git pull
make gold
```

**File → Open Folder** → loads `.cursorrules`.

## Chat starter

```text
Follow .cursorrules and docs/MASTER_AS_OF_2026-08-23.md.
Job C only. Dual fail-closed. Repo truth > chat memory.
Do not invent SKUs or claim LIVE_PIN_OK / HA without evidence.
Next priorities: pin live OR signed L1 — not more doctrine.
```

## Key paths

| Topic | Doc |
|-------|-----|
| Master status | `docs/MASTER_AS_OF_2026-08-23.md` |
| Gold / prototype | `make gold` · `docs/PROTOTYPE_BUILD_2026-08-23.md` |
| P-ADM attach | `docs/P_ADM_ATTACH_SCRIPT.md` |
| Redis HA / H9 | `docs/REDIS_HA_FIXTURES.md` · `tests/test_redis_ha_h9_concurrent.py` |
| Gaps | `docs/GAP_CLOSURE_REGISTER.md` |
| Completion | `docs/COMPLETION_STATUS.md` |

**Deep review setup:** `docs/SETUP_GITHUB_CURSOR_REVIEW.md` · `./scripts/review_sandbox.sh`

**Repo:** https://github.com/AINav01/ainav-control-plane
