# AINav Control Plane

**AINav, Inc.** · **AINav.Institute** · Runtime admission for privileged AI agent actions

```text
SUCCESS = LIVE_PIN_OK × proof day × signed L1 FIRST_OFFER
```

## Open in Cursor

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
cursor .
```

Rules: `.cursorrules` · `.cursor/rules/ainav-doctrine.mdc`  
Guides: `OPEN_IN_CURSOR.md` · `docs/CURSOR_SETUP.md`

## LIVE_PIN_OK (Azure)

```bash
az login
bash mothership/azure/deploy-swa.sh
# Portal → custom domain ainav.institute
# Cloudflare DNS → Azure records; remove Squarespace
curl -sS https://ainav.institute/health.json
```

- `docs/DO_THESE_NOW.md` · `docs/DNS_PROPAGATION_TROUBLESHOOTING.md`
- CI secret: `AZURE_STATIC_WEB_APPS_API_TOKEN`
- Workflow: `.github/workflows/azure-static-web-apps.yml`

## Product

- **AINav Control Plane** — dual admit, DecisionRecords, fail-closed
- Land: L1 $28–40k · Attach: P-ADM $40–60k/yr
- Job C only · fixtures-first · complement Agent 365 / Okta / Zenity
