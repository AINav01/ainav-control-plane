# Microsoft 365 + Grok Build (AINav)

**Status:** 27 Aug 2026  
**Audience:** AINav operators using Grok Build / Cursor Grok 4.6 on `AINav01/ainav-control-plane`  
**Rule:** Grok and Cursor ship **code and documents**. They do **not** occupy a dual seat. Dynamics writes go through AINav admit.

This file does **not** complete Entra consent. An admin must click Connect in the tenant.

---

## 1. Three layers (do not mix them)

```text
Layer 1  grok.com/connectors     Outlook, Teams, OneDrive, SharePoint, GitHub
Layer 2  Grok Build MCP          Azure (+ optional PnP admin CLI)
Layer 3  Office add-ins          Word / Excel / PowerPoint / Outlook sidebars
         ── separate ──
Job C    AINav plane             propose → dual consume → BC / Sales
```

| Surface | Job | Admits a BC journal? |
|---------|-----|----------------------|
| Grok connectors | Context for specs, mail, files | No |
| Grok Build MCP | Code + Azure landing | No |
| Office add-ins | Draft L1 / AE docs in Office | No |
| Cursor `@Cursor` in Teams | Cloud Agent on a **repo** | No |
| AINav Adaptive Card | Two humans consume a ticket | **Yes** |

A Grok Build or Cursor session that talks to Business Central MCP **directly** is a bypass. Do not install it in this workspace.

---

## 2. Layer 1 — Grok connectors

Same SuperGrok / Business / Enterprise account you use for the `grok` CLI.

Open: [https://grok.com/connectors](https://grok.com/connectors)

Catalog and built-ins: [https://docs.x.ai/docs/grok/connectors](https://docs.x.ai/docs/grok/connectors)

### Connect in this order

1. **Outlook Mail & Calendar** — all Grok users. Mail + calendar context.
2. **Microsoft Teams** — all Grok users. Channels and chats. Can send messages; keep that on **engineering** teams only.
3. **OneDrive** — personal / shared files.
4. **SharePoint** — **Grok Business and Enterprise only.** Admin setup first (below).
5. **GitHub** — selected repos: `AINav01/ainav-control-plane` (and later `DayTradingMarkets`). Not “all repos.”

Personal `@outlook.com` is not Microsoft 365 Business. Use a work Entra account.

### SharePoint (admin, once)

Docs: [https://docs.x.ai/docs/grok/connectors/sharepoint](https://docs.x.ai/docs/grok/connectors/sharepoint)

1. Team admin opens the xAI console and adds the SharePoint connector.
2. Access mode: **delegated** (recommended). `Sites.Read.All` is bounded by what the connecting account can see.
3. Create a **dedicated Entra user** with access only to the AINav / engineering sites. Connect Grok as that user. Do not connect as Global Admin.
4. Enter the Entra tenant ID (GUID or `contoso.onmicrosoft.com`).
5. **Approve as admin** (one-time org consent).
6. Each operator then: grok.com/connectors → SharePoint → Connect → work account → Accept.
7. Write access is a separate admin flag. Leave **off** unless you have a written reason. Operators still opt in individually.

Application permissions that can see every site are not the default. Do not turn them on for the plane workspace.

### Teams connector scopes (expect these)

`Team.ReadBasic.All`, `Channel.ReadBasic.All`, `ChannelMessage.Read.All`, `ChannelMessage.Send`, `Chat.Read`, `Chat.Create`, `ChatMessage.Send`, `User.Read`, plus membership reads.

Sending mail or Teams messages from Grok is **not** an AINav admit. Do not use it as the $48,250 approval path.

---

## 3. Layer 2 — Grok Build MCP

Grok Build is the terminal agent (`grok` CLI). Default model since mid-Aug 2026: **Grok 4.6**.

Install:

```bash
# macOS / Linux
curl -fsSL https://x.ai/cli/install.sh | bash

# Windows PowerShell
irm https://x.ai/cli/install.ps1 | iex

grok --version
```

First launch opens a browser. Headless / CI: `XAI_API_KEY` from [https://console.x.ai](https://console.x.ai).

MCP is native: `grok mcp add`, in-session `/mcps`, `~/.grok/config.toml`, or a Claude-style `.mcp.json`. Build also reads `AGENTS.md` / `CLAUDE.md`.

```bash
grok inspect    # shows MCP, skills, plugins, hooks
```

### Allowed in the plane workspace

```bash
# Azure resource tools (read / landing). Not production Key Vault dump.
grok mcp add azure -- npx -y @azure/mcp@latest server start
```

GitHub: use the **Grok GitHub connector** (layer 1) or Cursor’s official GitHub app. Do not commit PATs.

### Forbidden in this workspace

| MCP | Why |
|-----|-----|
| Business Central (`mcp.businesscentral.dynamics.com`) | Direct SoR write |
| Dataverse / Sales write | Same |
| Graph `Mail.Send` / site write | Privileged effector |
| Any MCP that posts without `propose()` | Bypass |

### Optional: PnP CLI (tenant admin chores only)

Manages lists and sites. Not Job C.

```bash
npm i -g @pnp/cli-microsoft365 @pnp/cli-microsoft365-mcp-server
m365 login
grok mcp add m365-cli -- npx -y @pnp/cli-microsoft365-mcp-server
```

Auth is **your** `m365 login`, not Grok’s.

---

## 4. Layer 3 — Office add-ins

Install from Microsoft Marketplace while signed into the **work** tenant. Admins can deploy in Integrated Apps.

| Add-in | Notes |
|--------|--------|
| Grok for Word | Free Marketplace add-in; drafts from notes / connectors |
| Grok for Excel | Free; formulas and ranges in-sheet |
| Grok for PowerPoint | Free; decks from outlines |
| Grok for Outlook | Paid X / SuperGrok |

Add-ins can use the **same** Grok connectors (SharePoint, Outlook, Drive). Use them for L1 eval reports, AE one-pagers, Sentinel workbooks.

They do not hash tickets and they are not a dual seat.

---

## 5. Cursor on the same tenant

Cursor has **no** first-party “Connect Microsoft 365 Business.”

Official Microsoft links:

- **Teams `@Cursor`** — Cloud Agent on a Git repo (needs Cursor GitHub app + usage-based pricing)
- **Azure DevOps** — repos / PRs
- **Azure MCP** — same allowlist as Build
- **Dataverse plugin** — Marketplace; do **not** enable write in the plane folder

Mail / OneDrive / SharePoint inside Cursor = extra Graph MCP + Entra app + admin consent. Prefer Grok connectors for that context. Keep Cursor MCP = GitHub + Azure only.

```text
Cursor  File → Open Folder = ainav-control-plane clone only
Model   Grok 4.6 for reviews
MCP     GitHub + Azure
Not     BC / Sales / Graph-write
```

Two Teams surfaces:

| App | Channel | Purpose |
|-----|---------|---------|
| Cursor | Engineering | `@Cursor` fix a test |
| AINav Adaptive Card | Controllers | Approve ticket T |

Do not mix them.

---

## 6. How this sits on the Microsoft stack

```text
Human in Grok Build / Cursor
    → GitHub AINav01/ainav-control-plane
    → Actions OIDC → Azure (plane + pin)

Grok connectors (Outlook / Teams / SharePoint / OneDrive)
    → context for specs and decks
    → NOT a dual seat

Customer E7 tenant
    Entra Agent ID + Agent 365 inventory
    Copilot Studio ──propose──► AINav
    Teams Enterprise card ──two OIDs + acrs──► AINav
    Teams Premium meeting ──hygiene around ticket T
    AINav ──admit──► BC Premium / Sales Enterprise
    AINav ──record──► their Sentinel
```

E7 is the ICP **signal** (Copilot + Entra Suite + Agent 365). It is not a product to clone.

---

## 7. Operator checklist

```text
Grok account
  ☐ Same login for grok.com and grok CLI
  ☐ grok.com/connectors: Outlook, Teams, OneDrive
  ☐ GitHub connector: selected repos only
  ☐ SharePoint: admin consent + site-scoped account (Business/Enterprise)

Grok Build
  ☐ grok --version
  ☐ grok inspect → Azure MCP present
  ☐ grok inspect → no BC / Sales / Mail.Send MCP

Office
  ☐ Word / Excel / PowerPoint add-ins (optional Outlook)
  ☐ Work tenant, not personal Microsoft account

Cursor
  ☐ Open Folder = this repo only
  ☐ GitHub app + Bugbot
  ☐ MCP = GitHub + Azure
  ☐ Grok 4.6 review pack: docs/PASTE_GROK46_REVIEW.md

Entra / E7 (customer or lab tenant)
  ☐ Allow Grok / SpaceXAI publisher apps or your own Graph app
  ☐ PIM role "AINav Approver" ≠ GitHub CODEOWNER (same human, different seat)
  ☐ Teams Premium licenses on the two controllers only
  ☐ Separate AINav card app for admit
```

---

## 8. What this file is not

- Not Entra consent (you click that)
- Not LIVE_PIN_OK
- Not U-DUAL Redis
- Not a Grok / Cursor SKU
- Not permission to put BC MCP in this repo

Cursor and Grok Build ship code. AINav admits the write.

---

## 9. Links

| What | URL |
|------|-----|
| Grok connectors | https://grok.com/connectors |
| Connector docs | https://docs.x.ai/docs/grok/connectors |
| SharePoint connector | https://docs.x.ai/docs/grok/connectors/sharepoint |
| Grok Build install | https://x.ai/cli |
| Grok Build source | https://github.com/xai-org/grok-build |
| Cursor GitHub / Teams | https://cursor.com/dashboard/integrations |
| This repo | https://github.com/AINav01/ainav-control-plane |
| Grok 4.6 review paste | docs/PASTE_GROK46_REVIEW.md |
