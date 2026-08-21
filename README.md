# AINav Control Plane

**Company:** AINav, Inc. · **Public edge:** [AINav.Institute](https://ainav.institute) · **Product:** AINav Control Plane

Runtime **authority coverage** for privileged AI agent actions — dual human admit, hash-bound Actions, DecisionRecords, fail-closed.

```text
SUCCESS = LIVE_PIN_OK × proof day × signed L1 FIRST_OFFER
```

## Open in Cursor

1. Install [Cursor](https://cursor.com)
2. **File → Open Folder** after clone, or Command palette → **Git: Clone**
3. Clone URL: `https://github.com/AINav01/ainav-control-plane.git`
4. Project rules load from `.cursor/rules/ainav-doctrine.mdc` and `.cursorrules`

```bash
git clone https://github.com/AINav01/ainav-control-plane.git
cd ainav-control-plane
cursor .
```

## Verify admit plane (local)

```bash
cd agent-governance
bash scripts/run_gap_closure_fixtures.sh
# Expect: ALL PASS
```

## Key paths

| Path | Role |
|------|------|
| `docs/NAMING.md` | Brand / product hierarchy |
| `docs/BUSINESS_MODEL.md` | Commercial model |
| `docs/DUAL_INDEX.md` | Dual admission entry |
| `docs/PRODUCT_BAR_MAXIMUM.md` | Maximum product bar |
| `docs/CURSOR_SETUP.md` | Cursor IDE setup |
| `docs/TARBALL_DOWNLOAD.md` | Offline archive |
| `agent-governance/` | Admit plane + fixtures |
| `mothership/www/` | Public pin / site source |

## Doctrine (short)

- **Job C only** — effect authority, not inventory or IdP
- Dual: SoD roles · `action_hash` · single-use · both-or-neither · named principals
- Land: FIRST_OFFER L1 $28–40k → attach P-ADM $40–60k/yr
- No second brand · no fail-open · no fake compliance labels

Private company repository. Lab dual suite is green on single-host atomicity.
