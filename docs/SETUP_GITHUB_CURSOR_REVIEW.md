# Setup: GitHub · Cursor · Grok 4.6 deep review

**As of:** 2026-08-23  
**Repo:** https://github.com/AINav01/ainav-control-plane

---

## 1. GitHub

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
git pull origin main
```

Source of truth: `main` (code, `.cursorrules`, master spine, review brief).

---

## 2. Local evidence (sandbox)

```bash
./scripts/review_sandbox.sh
# or: make gold && cd agent-governance && PYTHONPATH=. python3 examples/gold_path.py
```

Expect: **GOLD STANDARD: ALL PASS** and **GOLD PATH OK**.

---

## 3. Cursor + Grok 4.6

1. **File → Open Folder** → `ainav-control-plane`
2. Select model **Grok 4.6**
3. New chat — paste:

```text
Deep review of AINav Control Plane as of 2026-08-23.

Follow .cursorrules, docs/MASTER_AS_OF_2026-08-23.md, docs/PROTOTYPE_REVIEW_GROK46.md.

Run if needed: ./scripts/review_sandbox.sh
(or make gold + agent-governance gold_path.py)

Job C only. Dual fail-closed. Repo truth > assumptions.
No invented SKUs. No LIVE_PIN_OK / product HA / signed L1 without evidence.

Deliver:
1. Verdict (PASS / PASS WITH NOTES / FAIL)
2. What is solid
3. What is over-claimed or thin
4. Top 5 improvements (S/M/L)
5. Must-not-change
6. Next 7 days (ops / eng / commercial)
```

---

## 4. After review

- Real bugs → branch → `make gold` → push/PR
- Do not close G1 (pin) or G13 (L1) in git without evidence
- Company next: pin live OR signed L1

---

## 5. Key paths

| Item | Path |
|------|------|
| Master spine | `docs/MASTER_AS_OF_2026-08-23.md` |
| Review brief | `docs/PROTOTYPE_REVIEW_GROK46.md` |
| Cursor rules | `.cursorrules` · `CURSOR.md` |
| Sandbox script | `scripts/review_sandbox.sh` |
