#!/usr/bin/env bash
# Fail fast if this is not the ainav-control-plane tree (e.g. empty Cursor New Project).
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

ok=1
for p in \
  scripts/review_sandbox.sh \
  scripts/check_gold_standard.py \
  agent-governance \
  docs/MASTER_AS_OF_2026-08-23.md \
  docs/PASTE_GROK46_REVIEW.md \
  .cursorrules
do
  if [[ ! -e "$p" ]]; then
    echo "MISSING: $p"
    ok=0
  else
    echo "OK: $p"
  fi
done

echo "ROOT=$ROOT"

if [[ "$ok" -ne 1 ]]; then
  echo ""
  echo "RESULT: FAIL — wrong or incomplete workspace"
  echo "Clone https://github.com/AINav01/ainav-control-plane.git"
  echo "Cursor: File → Open Folder → ainav-control-plane (repo root)"
  exit 1
fi

echo "RESULT: PASS — Cursor workspace looks like ainav-control-plane"
exit 0
