# Open AINav in Cursor

## Clone

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
cursor .
```

Or: **Command Palette → Git: Clone** → `https://github.com/AINav01/ainav-control-plane.git`

## Rules (auto-loaded)

- `.cursorrules`
- `.cursor/rules/ainav-doctrine.mdc`

## Pin edge (Azure)

```bash
# Requires: az login + Node (swa CLI)
bash mothership/azure/deploy-swa.sh
```

Repo secret for CI: `AZURE_STATIC_WEB_APPS_API_TOKEN`  
Workflow: `.github/workflows/azure-static-web-apps.yml`

DNS: `docs/DNS_PROPAGATION_TROUBLESHOOTING.md`  
Critical path: `docs/DO_THESE_NOW.md`

## Fixtures

```bash
cd agent-governance
bash scripts/run_gap_closure_fixtures.sh
```

If `agent-governance/` is missing from clone, overlay `dist/ainav-build-2026-08-20.zip`.

## Naming

- **AINav, Inc.** — legal  
- **AINav.Institute** — public pin  
- **AINav Control Plane** — product  

## Doctrine

Job C only · fail-closed · fixtures-first · dual + DecisionRecords · no Aether SKUs
