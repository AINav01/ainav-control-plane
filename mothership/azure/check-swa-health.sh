#!/usr/bin/env bash
# Azure SWA pin health checks — local artifacts + optional hosts.
# Usage:
#   bash mothership/azure/check-swa-health.sh
#   bash mothership/azure/check-swa-health.sh --local
#   bash mothership/azure/check-swa-health.sh --url https://xxx.azurestaticapps.net
#   bash mothership/azure/check-swa-health.sh --public --require-live
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
exec python3 "${ROOT}/scripts/check_azure_swa_health.py" "$@"
