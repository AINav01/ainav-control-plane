# AINav Azure pin edge — ops build

Public **AINav.Institute** edge only. **Does not admit.** Dual admission is a separate plane.

```text
SWA (mothership/www)
  → healthz.json / health.json
  → optional Front Door (probe 30s, WAF AllowPinJson)
  → Log Analytics (Access + WAF)
  → Metric alerts (origin health + latency)
  → KQL (probe latency, WAF pin hits)
```

## Quick path

| Step | Command |
|------|---------|
| Local health | `python3 scripts/check_azure_swa_health.py --local --strict` |
| Deploy SWA | `bash mothership/azure/deploy-swa.sh` |
| FD probe 30s | `bash mothership/azure/configure-front-door-probe.sh --profile balanced` |
| LAW diagnostics | `bash mothership/azure/configure-log-analytics-diagnostics.sh --create-workspace` |
| Alerts | `ALERT_EMAIL=you@co.com bash mothership/azure/configure-front-door-alerts.sh` |
| Latency KQL | `bash mothership/azure/query-front-door-probe-latency.sh` |
| LIVE_PIN_OK | `python3 scripts/check_azure_swa_health.py --public --require-live` |

## Defaults

| Setting | Value |
|---------|--------|
| Probe path | `/healthz.json` |
| Probe interval | **30s** (balanced) |
| Health alert | OriginHealthPercentage < 100% / 15m |
| Latency alert | OriginLatency > 2000 ms / 15m |
| KQL | summary/fast: time → Category → path |

Index: this file. Cursor: `.cursor/rules/azure-pin-edge.mdc`.
