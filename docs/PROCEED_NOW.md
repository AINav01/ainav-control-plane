# Proceed now — operator checklist

**Date:** 2026-08-21  
**Goal:** `LIVE_PIN_OK × proof day × signed L1`

```text
Public edge today: ainav.institute = Squarespace "Coming Soon" (not mothership/www)
Lab release:       agent-gov-1.9.0
Repo:              https://github.com/AINav01/ainav-control-plane
```

---

## 1. LIVE_PIN_OK (you must run — needs Cloudflare)

### A. Cloudflare API token
1. Cloudflare Dashboard → My Profile → API Tokens → Create Token  
2. Permissions: **Account → Cloudflare Pages → Edit**  
3. On the machine that deploys:

```bash
export CLOUDFLARE_API_TOKEN=...
npm i -g wrangler   # if needed
```

### B. Deploy Pages

```bash
cd /path/to/artifacts   # or clone + overlay tarball
bash mothership/cloudflare/deploy.sh --require
```

Project default: **`ainav-institute`**.

### C. DNS (critical)

Today **ainav.institute** resolves to **Squarespace** parking — not Pages.

1. Cloudflare DNS for `ainav.institute`  
2. Point apex to **Cloudflare Pages** project `ainav-institute`  
3. Remove Squarespace A/CNAME for "Coming Soon"  
4. Wait for propagation  

See `mothership/cloudflare/DNS.md`.

### D. Verify LIVE_PIN_OK

```bash
curl -sS https://ainav.institute/health.json | jq .
# Must be real JSON with policy_digest — NOT HTML Coming Soon
```

Also open: `https://ainav.institute/` → product homepage from `mothership/www/`, not Squarespace.

---

## 2. GitHub + Cursor

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
cursor .
```

If `agent-governance/` missing, overlay `ainav-build-2026-08-20.tar.gz` or run `scripts/github_push_batches.sh` with `GITHUB_TOKEN`.

---

## 3. Proof day (fixtures)

```bash
cd agent-governance
bash scripts/run_gap_closure_fixtures.sh
# MAXIMUM BAR fixtures: ALL PASS
```

---

## 4. First commercial motion (this week)

| Step | Action |
|------|--------|
| 1 | List **3–5** FIRST_OFFER targets |
| 2 | Offer L1-FIX **$28k** fixtures dual |
| 3 | 10-minute dual demo |
| 4 | SOW = FIRST_OFFER only |
| 5 | Attach **P-ADM** within 90 days after accept |

---

## Done when

```text
□ health.json is JSON + digests match lab
□ apex serves mothership product pages
□ GitHub has agent-governance + mothership www
□ Fixture suite green
□ ≥1 active FIRST_OFFER conversation
```
