# Do these now — AINav critical path

**Date:** 2026-08-21  
**Company:** AINav, Inc. · **Edge:** AINav.Institute · **Product:** AINav Control Plane

```text
SUCCESS = LIVE_PIN_OK × proof day × signed L1 FIRST_OFFER
```

---

## 1. LIVE_PIN_OK (Azure Static Web Apps)

**Blocker today:** `ainav.institute` still returns Squarespace "Coming Soon" HTML.  
**Local pin is ready:** `mothership/www/health.json` is valid JSON with `policy_digest`.

```bash
# From artifacts / clone root
az login
export AZURE_SWA_RG=rg-ainav-edge
export AZURE_SWA_NAME=ainav-institute

bash mothership/azure/deploy-swa.sh
```

Then:

1. Portal → Static Web App → **Custom domains** → `ainav.institute`  
2. DNS: records Azure shows · **delete Squarespace** parking  
3. Verify:

```bash
curl -sS https://ainav.institute/health.json | head
# PASS = JSON + policy_digest
# FAIL = Coming Soon HTML
```

Optional later: Front Door pin no-store + WAF Detection  
(`mothership/azure/CDN_FRONT_DOOR_RULES.md`, `FRONT_DOOR_WAF.md`).

---

## 2. GitHub + Cursor

Repo: https://github.com/AINav01/ainav-control-plane

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
# Overlay full build: dist/ainav-build-2026-08-20.zip

export GITHUB_TOKEN=ghp_xxx
bash scripts/github_push_batches.sh
```

Fixtures:

```bash
cd agent-governance && bash scripts/run_gap_closure_fixtures.sh
# → MAXIMUM BAR: ALL PASS
```

---

## 3. Pilot outreach (this week)

See **`docs/PILOT_OUTREACH_THIS_WEEK.md`**.

1. Fill **5 ICP rows** (Risk/Ops/Treasury where agents write)  
2. Send L1-FIX **$28k** email  
3. Demo dual <10 min  

---

## 4. After signed L1

**P-ADM $40–60k/yr** within 90 days · U-DUAL if high-blast.

---

## Explicit non-work

- Multi-host Redis until HA SOW  
- Job A inventory features  
- "Gold standard" / GENIUS-certified labels  
- Fail-open dual for logos  

**Right now:** run `deploy-swa.sh` → fix DNS → curl health.json.
