#!/usr/bin/env bash
# Cursor / Grok 4.6 evidence gate: workspace + gold + gold_path
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== 0. Workspace (not empty New Project) ==="
bash "$ROOT/scripts/check_cursor_workspace.sh"

echo ""
echo "=== 1. make gold ==="
if [[ -f Makefile ]] && grep -q '^gold:' Makefile 2>/dev/null; then
  make gold
elif [[ -f scripts/check_gold_standard.py ]]; then
  python3 scripts/check_gold_standard.py
else
  echo "FAIL: no gold target"
  exit 1
fi

echo ""
echo "=== 2. gold_path ==="
if [[ -f agent-governance/examples/gold_path.py ]]; then
  (cd agent-governance && PYTHONPATH=. python3 examples/gold_path.py)
else
  echo "FAIL: gold_path missing"
  exit 1
fi

echo ""
echo "RESULT: PASS — gold + gold_path green"
echo ""
echo "Cursor: Open Folder = this repo root ($ROOT)"
echo "Grok 4.6 paste: docs/PASTE_GROK46_REVIEW.md (BEGIN→END) + this output"
exit 0
