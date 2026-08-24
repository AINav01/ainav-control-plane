# Open this folder in Cursor

**This directory is the project.** Do not use Cursor “New Project” or an empty `/workspace`.

## 1. Clone (if needed)

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
git pull
```

## 2. Prove fixtures

```bash
bash scripts/check_cursor_workspace.sh
bash scripts/review_sandbox.sh
```

Both must PASS.

## 3. Cursor

**File → Open Folder** → select **`ainav-control-plane`** (the folder that contains this file, `scripts/`, `docs/`, `agent-governance/`).

Model: **Grok 4.6**

## 4. Deep review

Paste from: https://github.com/AINav01/ainav-control-plane/blob/main/docs/PASTE_GROK46_REVIEW.md  

Include sandbox output in the same chat.

If Cursor path is `/workspace` with no `scripts/review_sandbox.sh` → wrong folder; close and open this repo.
