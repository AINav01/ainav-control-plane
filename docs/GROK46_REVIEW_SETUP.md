# Cursor + Grok 4.6 review (26 Aug 2026)

## 1. Clone and gate

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
git pull origin main
cd agent-governance && PYTHONPATH=. python3 tests/test_plane_major.py
```

Need: `plane MAJOR tests passed`.

If `scripts/review_sandbox.sh` exists, run it too. If it is missing, the plane-major test is the gate.

## 2. Open the right folder

Cursor **File → Open Folder** → `ainav-control-plane`
(the folder with `.cursorrules`, `.cursor/rules/`, `agent-governance/`).

Wrong: New Project / empty `/workspace`.

## 3. Model

Cursor model picker → **Grok 4.6**.

Rules that auto-load:
- `.cursorrules`
- `.cursor/rules/plane-major.mdc`
- `.cursor/rules/ainav-doctrine.mdc`

## 4. New chat — paste

Open `docs/PASTE_GROK46_REVIEW.md`. Copy **BEGIN PASTE → END PASTE**.
Paste the `test_plane_major.py` terminal output under it.

Do not start the review until the folder is this repo and the test printed `passed`.
