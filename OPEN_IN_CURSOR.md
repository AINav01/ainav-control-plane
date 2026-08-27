# Open this folder in Cursor

**This directory is the project.** Do not use Cursor “New Project” or an empty `/workspace`.

## 1. Clone

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
git pull origin main
```

## 2. Gate

```bash
cd agent-governance && PYTHONPATH=. python3 tests/test_plane_major.py
```

Need: `plane MAJOR tests passed`.

## 3. Cursor

**File → Open Folder** → **`ainav-control-plane`**

Model: **Grok 4.6**

## 4. Review

1. [docs/GROK46_REVIEW_SETUP.md](docs/GROK46_REVIEW_SETUP.md)
2. New chat → paste BEGIN–END from [docs/PASTE_GROK46_REVIEW.md](docs/PASTE_GROK46_REVIEW.md)
3. Paste the test output in the same chat

Wrong folder = no `agent-governance/agent_gov/hasher.py`.
