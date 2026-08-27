# Microsoft 365 + Grok Build (AINav)

**Status:** 27 Aug 2026  
**Audience:** AINav operators using Grok Build / Cursor Grok 4.6 on `AINav01/ainav-control-plane`  
**Rule:** Grok and Cursor ship **code and documents**. They do **not** occupy a dual seat. Dynamics writes go through AINav admit.

This file does **not** complete Entra consent. An admin must click Connect in the tenant.

Official connector index: [docs.x.ai/grok/connectors](https://docs.x.ai/grok/connectors)

---

## 1. Three layers (do not mix them)

```text
Layer 1  grok.com/connectors     Outlook, Teams, OneDrive, SharePoint, GitHub
Layer 2  Grok Build MCP          Azure (+ optional PnP admin CLI)
Layer 3  Office add-ins          Word / Excel / PowerPoint / Outlook sidebars
         -- separate --
Job C    AINav plane             propose -> dual consume -> BC / Sales
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

## 2. Layer 1 -- Grok connectors

Same SuperGrok / Business / Enterprise account you use for the `grok` CLI.

Open: [https://grok.com/connectors](https://grok.com/connectors)

Three kinds:

- **Built-in** -- xAI-maintained OAuth (Outlook, Teams, OneDrive, SharePoint, plus Google / Salesforce)
- **Catalog** -- pre-configured OAuth (GitHub, Notion, Linear, Box, …)
- **Custom MCP** -- public HTTPS MCP URL at New Connector -> Custom

On **Grok Business / Enterprise**, a team admin must **provision** the connector in [console.x.ai](https://console.x.ai) (Team Read-Write) before members see it.

Personal `@outlook.com` is not Microsoft 365 Business. Use a work Entra account.

### Plan gates (trust the per-connector page)

The index says “all Grok users.” The individual pages win:

| Connector | Kind | Plan | Admin console first? |
|-----------|------|------|----------------------|
| Outlook Mail | Built-in | All Grok | Only if tenant shows “need admin approval” |
| Outlook Calendar | Built-in (separate OAuth) | All Grok | Same |
| Microsoft Teams | Built-in | All Grok | Same |
| OneDrive | Built-in | **Business / Enterprise only** | **Yes** -- tenant ID + admin consent |
| SharePoint | Built-in | **Business / Enterprise only** | **Yes** -- tenant ID + access mode + consent |
| GitHub | Catalog | All Grok | No |

Connect in this order: Outlook Mail -> Outlook Calendar -> Teams -> OneDrive -> SharePoint -> GitHub.

Disconnect: grok.com/connectors -> Disconnect, or revoke at [myapps.microsoft.com](https://myapps.microsoft.com).

xAI states it does not train on connector data and does not keep mailbox/calendar/file bytes after the turn. Treat that as their policy, not a substitute for tenant DLP.

---

### 2.1 Outlook Mail

Docs: [Outlook connector](https://docs.x.ai/grok/connectors/outlook)

Mail and Calendar are **two connectors**, two OAuth grants.

**Can:** search mailbox; read body, headers, attachments; compose drafts (To/Cc/Bcc/HTML); send, reply-all, forward; move / create folders; attach Grok artifacts to a draft.

**Scopes (delegated, signed-in user only):**

- `Mail.ReadWrite` -- read, create, update, delete mail and drafts
- `Mail.Send` -- send on behalf of the user
- `User.Read`
- `offline_access`

**Steps:** grok.com/connectors -> New Connector -> **Outlook** -> work account -> Accept.

If “need admin approval”: Entra admin consents the xAI Grok app under **Enterprise applications**.

**AINav:** drafts and research only. `Mail.Send` from Grok is **not** an admit. Do not send customer or regulator mail from this connector.

---

### 2.2 Outlook Calendar

Same docs page; pick **Outlook Calendar** as its own connector.

**Can:** search events by range/keyword; read attendees, location, body; check free/busy across attendees; create/update events (attendees, location, recurrence, reminders); RSVP accept / decline / tentative.

**Scopes:** `Calendars.ReadWrite`, `User.Read`, `offline_access`.

**AINav:** schedule the two-controller Teams Premium meeting. Creating the meeting is hygiene. It does not consume a ticket.

---

### 2.3 Microsoft Teams

Docs: [Teams connector](https://docs.x.ai/grok/connectors/microsoft-teams)

Not plan-gated. No tenant-ID field. Work or school account.

**Can:** search channels and chats; read threads, reactions, @mentions; send channel messages and thread replies; send 1:1 / group chat; create chats; browse teams/channels; list members and roles.

**Scopes (delegated):**

- `Team.ReadBasic.All` / `TeamMember.Read.All`
- `Channel.ReadBasic.All` / `ChannelMember.Read.All` / `ChannelMessage.Read.All` / `ChannelMessage.Send`
- `Chat.Read` / `Chat.Create` / `ChatMessage.Send`
- `User.Read` / `offline_access`

Grok only sees teams the signed-in user already belongs to.

**AINav:** engineering channels only. Do **not** use this send path as the $48,250 approval. That card is the AINav Adaptive Card app.

---

### 2.4 OneDrive

Docs: [OneDrive connector](https://docs.x.ai/grok/connectors/onedrive)

**Business / Enterprise only.** “Personal storage” means *your* OneDrive for Business, not a consumer Microsoft account.

**Admin (once), console.x.ai -> Grok Business -> Connectors -> Add OneDrive:**

1. Enter Entra tenant ID (GUID or `contoso.onmicrosoft.com`) from Entra **Overview**.
2. Consent: Approve as admin, copy link for IT, or skip and finish later.
3. Needs Team Read-Write on the xAI team.

**Member:** grok.com/connectors -> OneDrive -> work account -> Accept.

**Can:** browse nested folders; upload Grok-generated files (xlsx, pdf, reports).

**Cannot:** see other users’ drives. Full-text search of OneDrive *for Business* files needs the **SharePoint** connector as well (those files live on SharePoint infrastructure).

**Scopes:** `Files.ReadWrite`, `User.Read`, `offline_access` (delegated).

Disconnect deletes indexed data for that user. Admin removal deletes org-wide index.

**AINav:** drop L1 reports and AE drafts here. Not a DecisionRecord store.

---

### 2.5 SharePoint

Docs: [SharePoint connector](https://docs.x.ai/grok/connectors/sharepoint)

**Business / Enterprise only.**

**Access modes**

- **Delegated (default for AINav).** `Sites.Read.All` + `Files.Read.All` bounded by what the connecting account can see. Use a **dedicated Entra user** limited to AINav / engineering sites. Do not connect as Global Admin.
- **Application `Sites.Selected`.** After consent, admin picks sites in the console. Sync indexes only those sites.

**Admin**

1. console.x.ai -> add SharePoint.
2. Choose delegated (recommended) or Sites.Selected.
3. Enter tenant ID.
4. Admin consent (popup, copy link, or skip).
5. If application mode: pick allowed sites (editable later).
6. Write access is a **second** Entra app (`Files.ReadWrite.All`). Button **Enable Write Access**. Off by default. Members still opt in one by one.

**Read scopes:** `Sites.Read.All`, `Files.Read.All`, `User.Read`, `offline_access`.  
**Write (if enabled):** `Files.ReadWrite.All`.

Every query is access-checked as the asking user.

**Can:** search documents across allowed sites; read library files; browse folders/drives; upload artifacts if write is on.

**AINav:** keep write **off** unless you have a written reason. Application-wide site access is not the default for the plane workspace.

---

### 2.6 GitHub (catalog)

Not a built-in. Catalog OAuth at grok.com/connectors -> GitHub.

**Can (typical catalog grant):** search code, issues, PRs; summarize and review. Pin to **selected** repos: `AINav01/ainav-control-plane`, later `DayTradingMarkets`. Not all-org.

Prefer Cursor’s official GitHub app + Bugbot for merge gates. Grok GitHub is extra context in chat / Build.

Do not commit PATs. CODEOWNER review is still required on `agent-governance/agent_gov/**`.

---

### 2.7 Custom MCP from grok.com

New Connector -> **Custom** -> public HTTPS MCP URL. Local servers need a tunnel ([custom MCP tunneling](https://docs.x.ai/grok/connectors/custom-mcp-tunneling)).

Same forbid list as Grok Build MCP: no BC, no Sales write, no Graph `Mail.Send` / site write unless that path calls `propose()` first.

---

## 3. Layer 2 -- Grok Build MCP

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

Connectors on the Grok **account** (section 2) are visible to Build when the same login is used. MCP is the extra local/remote tool channel.

### Allowed in the plane workspace

```bash
# Azure resource tools (read / landing). Not production Key Vault dump.
grok mcp add azure -- npx -y @azure/mcp@latest server start
```

GitHub: Grok catalog connector or Cursor GitHub app. Not a PAT in git.

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

## 4. Layer 3 -- Office add-ins

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

- **Teams `@Cursor`** -- Cloud Agent on a Git repo (needs Cursor GitHub app + usage-based pricing)
- **Azure DevOps** -- repos / PRs
- **Azure MCP** -- same allowlist as Build
- **Dataverse plugin** -- Marketplace; do **not** enable write in the plane folder

Mail / OneDrive / SharePoint inside Cursor = extra Graph MCP + Entra app + admin consent. Prefer Grok connectors for that context. Keep Cursor MCP = GitHub + Azure only.

```text
Cursor  File -> Open Folder = ainav-control-plane clone only
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
    -> GitHub AINav01/ainav-control-plane
    -> Actions OIDC -> Azure (plane + pin)

Grok connectors (Outlook / Teams / SharePoint / OneDrive)
    -> context for specs and decks
    -> NOT a dual seat

Customer E7 tenant
    Entra Agent ID + Agent 365 inventory
    Copilot Studio --propose--> AINav
    Teams Enterprise card --two OIDs + acrs--> AINav
    Teams Premium meeting --hygiene around ticket T
    AINav --admit--> BC Premium / Sales Enterprise
    AINav --record--> their Sentinel
```

E7 is the ICP **signal** (Copilot + Entra Suite + Agent 365). It is not a product to clone.

---

## 7. Operator checklist

```text
Grok account
  [ ] Same login for grok.com and grok CLI
  [ ] Outlook Mail + Outlook Calendar (two grants)
  [ ] Teams (engineering only)
  [ ] OneDrive: Business/Enterprise + admin tenant ID + consent
  [ ] SharePoint: delegated + site-scoped account; write off
  [ ] GitHub catalog: selected repos only

Grok Build
  [ ] grok --version
  [ ] grok inspect -> Azure MCP present
  [ ] grok inspect -> no BC / Sales / Mail.Send MCP

Office
  [ ] Word / Excel / PowerPoint add-ins (optional Outlook)
  [ ] Work tenant, not personal Microsoft account

Cursor
  [ ] Open Folder = this repo only
  [ ] GitHub app + Bugbot
  [ ] MCP = GitHub + Azure
  [ ] Grok 4.6 review pack: docs/PASTE_GROK46_REVIEW.md

Entra / E7 (customer or lab tenant)
  [ ] Allow Grok / SpaceXAI publisher apps or your own Graph app
  [ ] PIM role "AINav Approver" != GitHub CODEOWNER (same human, different seat)
  [ ] Teams Premium licenses on the two controllers only
  [ ] Separate AINav card app for admit
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
| Connector index | https://docs.x.ai/grok/connectors |
| grok.com connectors | https://grok.com/connectors |
| Outlook Mail + Calendar | https://docs.x.ai/grok/connectors/outlook |
| OneDrive | https://docs.x.ai/grok/connectors/onedrive |
| SharePoint | https://docs.x.ai/grok/connectors/sharepoint |
| Microsoft Teams | https://docs.x.ai/grok/connectors/microsoft-teams |
| Custom MCP tunnel | https://docs.x.ai/grok/connectors/custom-mcp-tunneling |
| xAI console | https://console.x.ai |
| Revoke Microsoft apps | https://myapps.microsoft.com |
| Grok Build install | https://x.ai/cli |
| Grok Build source | https://github.com/xai-org/grok-build |
| Cursor integrations | https://cursor.com/dashboard/integrations |
| This repo | https://github.com/AINav01/ainav-control-plane |
| Grok 4.6 review paste | docs/PASTE_GROK46_REVIEW.md |
