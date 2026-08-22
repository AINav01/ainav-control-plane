# Execute all recommendations — operator runbook

**Generated:** 2026-08-21  
**Repo:** https://github.com/AINav01/ainav-control-plane

Automation cannot run `az login` or edit your Cloudflare DNS.  
**You** complete LIVE_PIN_OK on a machine with Azure access.

---

## A. Azure pin (required)

```powershell
az login
az account set --subscription "<id>"

git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane

bash mothership/azure/deploy-swa.sh
```

Then:

1. Portal → Static Web App **ainav-institute** → Custom domains → **ainav.institute**
2. Cloudflare DNS → records Azure shows; **delete Squarespace** targets
3. Grey-cloud during cert validation

```bash
curl -sS https://ainav.institute/health.json
# PASS = JSON with policy_digest
```

Optional after pin: Front Door rules + WAF Detection (`mothership/azure/`).

GitHub Actions: secret `AZURE_STATIC_WEB_APPS_API_TOKEN` → workflow **Deploy AINav.Institute**.

---

## B. Cursor

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane && cursor .
```

---

## C. Pilot outreach (this week)

1. Fill table in `docs/PILOT_OUTREACH_THIS_WEEK.md` (5 ICPs)
2. Send L1-FIX **$28k** email
3. Demo dual under 10 minutes

After green L1 → **P-ADM $40–60k/yr** within 90 days.

---

## D. Lab verify

```bash
cd agent-governance && bash scripts/run_gap_closure_fixtures.sh
```

```text
SUCCESS = LIVE_PIN_OK × proof day × signed L1 FIRST_OFFER
```
