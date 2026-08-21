# Open AINav in Cursor

**Repo (private):** https://github.com/AINav01/ainav-control-plane  
**Product:** AINav Control Plane · **Company:** AINav, Inc. · **Edge:** AINav.Institute

---

## 1. Clone into Cursor

### Option A — Cursor UI
1. Open **Cursor**
2. **File → Open Folder…** (or **Clone Repo**)
3. Sign in to GitHub if prompted (account that can access **AINav01**)
4. Clone: `https://github.com/AINav01/ainav-control-plane.git`
5. Open the cloned folder as the workspace

### Option B — Terminal

```bash
cd ~/Projects   # or any directory you prefer
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
```

Then in Cursor: **File → Open Folder…** → select `ainav-control-plane`.

### Option C — SSH

```bash
git clone git@github.com:AINav01/ainav-control-plane.git
```

---

## 2. After open

| Action | Why |
|--------|-----|
| Read `docs/NAMING.md` | Product hierarchy lock |
| Read `docs/BUSINESS_MODEL.md` | Canonical commercial model |
| Read `docs/DUAL_INDEX.md` | Dual admission entry |
| Read `docs/SESSION_FREEZE_2026-08-20.md` | Session freeze |

Optional: install Python 3.11+ if you work on `agent-governance/`.

```bash
cd agent-governance
bash scripts/run_gap_closure_fixtures.sh   # when full tree is present
```

---

## 3. Full tree vs GitHub freeze

GitHub may hold the **canonical docs batch** first. The **complete** build (tests, mothership www, full agent-governance) is also in:

```text
dist/ainav-build-2026-08-20.zip
dist/ainav-build-2026-08-20.tar.gz
```

To expand full tree into the clone:

```bash
# after downloading the zip from the project workspace or a Release asset
Expand-Archive ainav-build-2026-08-20.zip -DestinationPath .\ainav-full
# or: tar -xzf ainav-build-2026-08-20.tar.gz
```

Then open that folder in Cursor, or copy folders into the git clone and commit.

---

## 4. Cursor tips

- Use **Composer / Agent** with context: `@docs/BUSINESS_MODEL.md` `@docs/NAMING.md`
- Keep secrets out of the repo (no tokens, no customer data)
- Private repo: only collaborators with access can clone

---

**Bottom line:** Clone **AINav01/ainav-control-plane** → Open Folder in Cursor → start from `docs/NAMING.md` and `docs/BUSINESS_MODEL.md`.
