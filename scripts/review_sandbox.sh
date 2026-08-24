#!/usr/bin/env bash
# AINav prototype deep-review sandbox — run before/during Cursor Grok 4.6 review
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=============================================="
echo "AINav REVIEW SANDBOX  (as of master spine)"
echo "=============================================="
echo ""

echo "[1/3] make gold / check_gold_standard.py"
if [[ -f Makefile ]] && grep -q '^gold:' Makefile 2>/dev/null; then
  make gold
else
  python3 scripts/check_gold_standard.py
fi

echo ""
echo "[2/3] gold_path.py"
cd agent-governance
PYTHONPATH=. python3 examples/gold_path.py
cd "$ROOT"

echo ""
echo "[3/3] Cursor + Grok 4.6 — paste this in a new chat:"
echo "----------------------------------------------"
cat << 'PROMPT'
Deep review of AINav Control Plane as of 2026-08-23.

Follow .cursorrules, docs/MASTER_AS_OF_2026-08-23.md, docs/PROTOTYPE_REVIEW_GROK46.md.

Evidence from review_sandbox.sh should already show gold + gold_path.
If not run: make gold && cd agent-governance && PYTHONPATH=. python3 examples/gold_path.py

Job C only. Dual fail-closed. Repo truth > assumptions.
No invented SKUs. No LIVE_PIN_OK / product HA / signed L1 without evidence.

Deliver:
1. Verdict (PASS / PASS WITH NOTES / FAIL)
2. What is solid
3. What is over-claimed or thin
4. Top 5 improvements (S/M/L)
5. Must-not-change
6. Next 7 days (ops / eng / commercial)
PROMPT
echo "----------------------------------------------"
echo ""
echo "Docs: docs/SETUP_GITHUB_CURSOR_REVIEW.md"
echo "Done."
