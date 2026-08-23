# Sales & purchase process

**Motion:** Qualify → L1 SOW → Deliver → Readout → P-ADM attach → Packs / L2  
**Must-have rule:** Sell control, not catalog. L1 proves; P-ADM keeps; packs deepen.

## End-to-end flow

```text
1. Qualify (sponsor, verb, dual people, fixtures or sandbox)
2. Propose L1 (FIX / SALES / FULL)
3. Sign pilot SOW + verb-lock exhibit
4. Kickoff ≤5 business days
5. Deliver kit → customer re-runs gate
6. Readout (risks + attach proposal)
7. P-ADM proposal within 14 days of PASS
8. Sign coverage SOW (target ≤90 days from pilot start)
9. Optional: pack / L2 order lines
```

**Stop conditions:** inventory-only RFP, no dual appetite, must claim live ERP week one without tenant.

## Qualification

**Yes if:** named sponsor, high-blast or SoR-adjacent verb, two approvers, sandbox or fixtures-only acceptance.  
**Walk if:** shadow-AI inventory only, soft HITL end state, live production before fixtures.

## What to sell when

| Stage | SKU | Price band |
|-------|-----|------------|
| First 90 days | **L1** only | $28–40k fixed |
| After kit PASS | **P-ADM** | $40–60k/yr |
| With coverage | **U-DUAL / P-REC / U-SIEM / P-DEP** | Rate card |
| Named system | **U-SOR-*** | Quoted |
| Prod verb | **L2** | Separate SOW |

**Never:** lead with L3/L4, free U-DUAL to close P-ADM, seats/inventory.

## Purchase instruments

| Step | Document | Acceptance |
|------|----------|------------|
| Pilot | FIRST_OFFER_SOW + order form + verb-lock | Kit PASS / readout |
| Coverage | P-ADM SOW (coverage language) | Term start + support |
| Pack | Order line / change order | Pack acceptance |
| Connector | U-SOR SOW | Sandbox green → prod |

Order form: `python3 scripts/pilot_order_form.py`

## Attach (post-PASS)

> You proved dual-admitted control under fixtures.  
> **P-ADM** keeps that control covered for a year—not seats, **coverage**.  
> Declining P-ADM is choosing **open-loop** again.

Full script: `docs/P_ADM_ATTACH_SCRIPT.md`

## Metrics

| Metric | Target |
|--------|--------|
| L1 cycle | 2–4 weeks |
| Attach proposal latency | ≤14 days after PASS |
| L1 → P-ADM conversion | Primary KPI |
| Time to P-ADM signature | ≤90 days from pilot start |

**Related:** `FIRST_OFFER.md` · `P_ADM_ATTACH_PLAYBOOK.md` · `COMMERCIAL_OPS_THREE.md`
