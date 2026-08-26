# Implementation of the 26 Aug 2026 review

**Repo target:** `AINav01/ainav-control-plane`
**Doctrine lock:** Job C only. No new SKUs. Institute = pin face, not a school.

This pass implements the review gaps as artifacts. DNS cutover still needs human Azure clicks.

## Still needs a human

- `bash mothership/azure/deploy-swa.sh` then custom domain + delete Squarespace
- `curl https://ainav.institute/health.json` must return JSON with policy_digest
- Partner Center seller + first design-partner emails

## Do not claim

LIVE_PIN_OK until public health.json is JSON. HA until Redis fixtures pass. SOC2 until the letter exists.
