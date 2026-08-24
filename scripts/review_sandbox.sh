#!/usr/bin/env bash
# AINav review sandbox — gold + gold_path + pointer to Cursor prompt
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
FAIL=0

echo "=============================================="
echo " AINav REVIEW SANDBOX"
echo "=============================================="

echo ""
echo "[1/2] Gold gate"
if [[ -f Makefile ]] && grep -qE '^gold:' Makefile 2>/dev/null; then
  if ! make gold; then FAIL=1; fi
else
  if ! python3 scripts/check_gold_standard.py; then FAIL=1; fi
fi

echo ""
echo "[2/2] Gold path (admit → effect)"
if ! (cd agent-governance && PYTHONPATH=. python3 examples/gold_path.py); then
  FAIL=1
fi

echo ""
if [[ "$FAIL" -ne 0 ]]; then
  echo "RESULT: FAIL — fix gates before Cursor review"
  exit 1
fi

echo "RESULT: PASS — gold + gold_path green"
echo ""
echo "Cursor + Grok 4.6:"
echo "  1. File → Open Folder → this repo"
echo "  2. Model → Grok 4.6"
echo "  3. New chat → open docs/CURSOR_DEEP_REVIEW_PROMPT.md and send the prompt block"
echo "  Or paste from: docs/SETUP_GITHUB_CURSOR_REVIEW.md"
echo ""
echo "Master: docs/MASTER_AS_OF_2026-08-23.md"
exit 0
