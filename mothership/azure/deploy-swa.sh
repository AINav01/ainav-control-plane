#!/usr/bin/env bash
# Deploy AINav.Institute pin edge to Azure Static Web Apps.
# Does NOT admit dual tokens — pin edge only.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/../.." && pwd)"
WWW="${ROOT}/mothership/www"
RG="${AZURE_SWA_RG:-rg-ainav-edge}"
NAME="${AZURE_SWA_NAME:-ainav-institute}"
LOC="${AZURE_SWA_LOCATION:-eastus2}"

if [[ ! -f "${WWW}/health.json" ]]; then
  echo "ERROR: missing ${WWW}/health.json" >&2
  exit 1
fi
python3 -c "import json; json.load(open('${WWW}/health.json'))" || {
  echo "ERROR: health.json is not valid JSON" >&2
  exit 1
}

if [[ -z "${AZURE_STATIC_WEB_APPS_API_TOKEN:-}" ]]; then
  echo "=== No AZURE_STATIC_WEB_APPS_API_TOKEN — creating / looking up SWA ==="
  command -v az >/dev/null || { echo "Install Azure CLI: https://aka.ms/azcli"; exit 1; }
  az account show >/dev/null 2>&1 || { echo "Run: az login"; exit 1; }

  az group create -n "$RG" -l eastus --output none 2>/dev/null || true
  if ! az staticwebapp show -n "$NAME" -g "$RG" >/dev/null 2>&1; then
    echo "Creating Static Web App ${NAME}..."
    az staticwebapp create -n "$NAME" -g "$RG" -l "$LOC" --sku Free -o jsonc
  fi
  export AZURE_STATIC_WEB_APPS_API_TOKEN
  AZURE_STATIC_WEB_APPS_API_TOKEN="$(az staticwebapp secrets list -n "$NAME" -g "$RG" --query 'properties.apiKey' -o tsv)"
  echo "Token acquired (not printed)."
fi

command -v swa >/dev/null 2>&1 || npm i -g @azure/static-web-apps-cli

echo "Deploying ${WWW} → ${NAME}..."
swa deploy "$WWW" \
  --deployment-token "$AZURE_STATIC_WEB_APPS_API_TOKEN" \
  --env production

HOST="$(az staticwebapp show -n "$NAME" -g "$RG" --query 'defaultHostname' -o tsv 2>/dev/null || true)"
echo ""
echo "=== Deployed ==="
echo "Default host: https://${HOST:-<check portal>}"
echo ""
echo "Next:"
echo "  1. Portal → Custom domains → add ainav.institute"
echo "  2. DNS: set records Azure shows; REMOVE Squarespace Coming Soon"
echo "  3. curl -sS https://ainav.institute/health.json | head"
echo "     Expect: JSON with policy_digest — not HTML"
echo ""
if [[ -n "${HOST:-}" ]]; then
  echo "Smoke test default host:"
  curl -sS --max-time 20 "https://${HOST}/health.json" | head -20 || true
fi
