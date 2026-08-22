# DNS propagation troubleshooting — ainav.institute

## Current observed state (2026-08-21)

| Check | Result |
|-------|--------|
| Resolves | Yes → Cloudflare anycast (`104.21.x`, `172.67.x`) |
| HTTPS | 200 |
| Body | **Squarespace Coming Soon** parking HTML |
| `/health.json` | Same HTML — **not** pin JSON |

**Conclusion:** DNS already hits Cloudflare. This is **not** a TTL wait problem. Fix **origin/records** (remove Squarespace, point at Azure SWA).

## Success test (LIVE_PIN_OK)

```bash
curl -sS https://ainav.institute/health.json | head
# PASS: JSON with policy_digest
# FAIL: Coming Soon / squarespace.com HTML
```

## Cutover order

1. Deploy `mothership/www` → Azure Static Web Apps (`bash mothership/azure/deploy-swa.sh`)
2. Azure Portal → Custom domain `ainav.institute` → copy required DNS records
3. Cloudflare DNS → set those records; **delete** Squarespace A/CNAME targets
4. Prefer **DNS only (grey cloud)** until Azure cert shows Ready
5. Re-test `health.json` from 8.8.8.8 / 1.1.1.1 / dnschecker.org

## Propagation vs wrong target

| Symptom | Cause |
|---------|--------|
| Everywhere sees Coming Soon | Records still Squarespace (fix origin) |
| Mixed old/new by region | Real TTL lag after record change |
| NXDOMAIN | Registrar NS not pointing at Cloudflare |
| SSL errors after switch | Cert pending on SWA / proxy mode |

Record changes on Cloudflare (NS already CF): usually **seconds–minutes**.  
Nameserver changes at registrar: **1–48h**.

## Commands

```powershell
nslookup ainav.institute 8.8.8.8
curl.exe -sS https://ainav.institute/health.json
```

```bash
dig A ainav.institute @8.8.8.8 +short
curl -sSI https://ainav.institute/ | head -20
```

## Pitfalls

- Apex `@` and `www` both need records
- Competing A + CNAME
- Orange-cloud during Azure domain validation → use grey-cloud first
- Expecting pin JSON while origin is still parking page

See also: `docs/DO_THESE_NOW.md`, `mothership/azure/deploy-swa.sh`
