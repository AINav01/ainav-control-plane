# Model cutover — document & protect

**Purpose:** Model version may change (e.g. Grok 4.5 → 4.6). **AINav doctrine, SKUs, and dual bar do not.**

```text
Repo truth > chat memory > model confidence
```

---

## Non-negotiables (never “improve away”)

| Rule | Source |
|------|--------|
| Job C only (effect authority) | `.cursorrules` |
| Dual: distinct principals, action_hash, single-use, fail-closed | Dual canonical + Lua |
| L1 → P-ADM → packs; **U-DUAL never free** | OFFERING / rate card |
| HA claim only after Redis fixtures green | G3 / `U_DUAL_REDIS_ATOMIC.md` |
| LIVE_PIN_OK = real `health.json`, not HTML | Pin ops |
| Soft HITL is not dual | RFP criteria |

---

## Cutover log (fill on switch)

| Field | Value |
|-------|--------|
| From | Grok 4.5 (prior team sessions) |
| To | Grok 4.6 (when default) |
| Cutover date | _YYYY-MM-DD_ |
| Owner | _name_ |
| Repo SHA at cutover | _commit on main_ |
| Gold before | `make gold` → ALL PASS |
| Gold after | `make gold` → ALL PASS |

---

## Checklist

**Before**

- [ ] Note `main` commit SHA on GitHub
- [ ] `make gold` PASS
- [ ] Cursor opens repo with current `.cursorrules`

**Day of**

- [ ] New chat cites `.cursorrules` + `docs/BEST_OF_INTEGRATED.md`
- [ ] `make gold` again
- [ ] Spot-check: dual language, P-ADM attach script, no free U-DUAL
- [ ] GitHub read/write still works if used

**After 48h**

- [ ] Record quirks below
- [ ] Tighten rules if model ignores a line — **do not dilute the bar**

### Known quirks (post-cutover)

```text
(none yet — fill after 4.6 default)
```

---

## Protection map

| Layer | Path |
|-------|------|
| Cursor always-on | `.cursorrules` · `.cursor/rules/*.mdc` |
| Spine | `docs/BEST_OF_INTEGRATED.md` · `GOLD_STANDARD.md` |
| Gaps honesty | `docs/GAP_CLOSURE_REGISTER.md` |
| Dual / Redis | `U_DUAL_REDIS_ATOMIC.md` · `dual_consume.lua` |
| Commercial lock | `P_ADM_ATTACH_SCRIPT.md` · commercial ops three |
| Machine gate | `make gold` |

---

## Forbidden at cutover

- Rewrite dual or pricing because the model is “smarter”
- Claim LIVE_PIN_OK or multi-host HA without evidence
- Invent SKUs or soft-approve paths
- Skip `make gold`

**Related:** `BEST_OF_INTEGRATED.md` · `GAP_CLOSURE_REGISTER.md` · `.cursorrules`
