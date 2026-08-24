#!/usr/bin/env bash
# AINav review sandbox — evidence before Cursor deep review
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
  make gold || FAIL=1
else
  python3 scripts/check_gold_standard.py || FAIL=1
fi

echo ""
echo "[2/2] Gold path"
(cd agent-governance && PYTHONPATH=. python3 examples/gold_path.py) || FAIL=1

echo ""
if [[ "$FAIL" -ne 0 ]]; then
  echo "RESULT: FAIL — fix before review"
  exit 1
fi

echo "RESULT: PASS"
echo ""
echo "Next: Cursor → Grok 4.6 → docs/CURSOR_DEEP_REVIEW_PROMPT.md"
echo "      (copy text below the --- line into a new chat)"
echo "Guide: docs/START.md"
exit 0
