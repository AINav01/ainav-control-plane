# Setup: GitHub · Cursor · Grok 4.6 deep review

**One path. No doctrine rewrite.**

---

## A. Get `main`

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
git pull
```

---

## B. Prove the build (required)

```bash
./scripts/review_sandbox.sh
# same as: make review
```

**Must see:** `RESULT: PASS — gold + gold_path green`  
If FAIL → stop; do not review.

---

## C. Deep review in Cursor

1. **Open Folder** → `ainav-control-plane`
2. Model → **Grok 4.6**
3. New chat → open **`docs/CURSOR_DEEP_REVIEW_PROMPT.md`** → copy the prompt under the line → send

That file is the single review prompt (verdict format + hard rules).

---

## D. After

| Result | Action |
|--------|--------|
| Real defect | Fix → `./scripts/review_sandbox.sh` → commit/push |
| Doc nit | Small doc PR only |
| “Close pin/L1” | **Not** a git close — ops/commercial |

**Company next:** LIVE_PIN_OK or signed L1 — not another review.

---

## Files

| File | Role |
|------|------|
| `scripts/review_sandbox.sh` | Gold + gold_path |
| `docs/CURSOR_DEEP_REVIEW_PROMPT.md` | Paste into Grok 4.6 |
| `docs/MASTER_AS_OF_2026-08-23.md` | Business + build spine |
| `docs/PROTOTYPE_REVIEW_GROK46.md` | Longer brief |
| `.cursorrules` | Always-on doctrine |
