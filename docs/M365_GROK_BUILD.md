# Microsoft 365 + Grok Build (AINav)

**Status:** 27 Aug 2026  
**Audience:** AINav operators using Grok Build / Cursor Grok 4.6 on `AINav01/ainav-control-plane`  
**Rule:** Grok and Cursor ship **code and documents**. They do **not** occupy a dual seat. Dynamics writes go through AINav admit.

This file documents Entra consent. It does **not** click it for you.

Official connector index: [docs.x.ai/grok/connectors](https://docs.x.ai/grok/connectors)  
Entra grant-consent: [Grant tenant-wide admin consent](https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/grant-admin-consent)

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

## 2.0 Entra admin consent (do this first for OneDrive / SharePoint)

Tenant-wide admin consent lets every user in the tenant skip the “need admin approval” wall for **that app’s registered permissions**. It is **not** AINav dual-admit. Review scopes before you click Accept.

### Roles that can grant it

Any one of:

- Cloud Application Administrator
- Application Administrator
- Privileged Role Administrator
- Global Administrator

Application permissions (app roles) that are Microsoft Graph **application** permissions usually need a Global Administrator to approve. SharePoint **write** (`Files.ReadWrite.All`) and `Sites.Selected` are in that class. Delegated Mail/Calendars/Teams can often be granted by Cloud Application Administrator.

### Find the tenant ID

1. Sign in at [https://entra.microsoft.com](https://entra.microsoft.com).
2. **Entra ID** -> **Overview**.
3. Copy **Tenant ID** (GUID). The verified domain (`contoso.onmicrosoft.com` or `contoso.com`) also works in consent URLs and in the xAI console.

You will paste this into console.x.ai for OneDrive and SharePoint.

### Path A -- xAI console (OneDrive and SharePoint)

Required on Grok Business / Enterprise before members can connect those two.

1. Sign in to [https://console.x.ai](https://console.x.ai) with Team Read-Write.
2. Open **Grok Business** -> **Connectors** -> **Add Connector**.
3. Pick **OneDrive** or **SharePoint**.
4. Paste the Entra tenant ID.
5. SharePoint only: choose **Delegated** (AINav default) or **Application `Sites.Selected`**.
6. Consent options xAI shows:
   - **Approve as admin** -- Microsoft popup. Sign in as an Entra admin above. Review permissions. **Accept**.
   - **Copy link for your IT admin** -- send that URL. It is the same tenant-wide admin-consent endpoint.
   - **Skip** -- finish later. Members will keep seeing admin-approval errors until you complete it.
7. SharePoint write is a **second** app. After read consent: **Enable Write Access** -> another consent popup for `Files.ReadWrite.All`. Leave this **off** unless written.
8. Application mode only: after consent, pick allowed sites in the console picker. Unlisted sites are not indexed.

Do this once per connector (and once more for SharePoint write). Then each operator still clicks Connect with their own work account.

### Path B -- Entra admin center (any Grok / SpaceXAI / Office add-in)

Use this when a user hits **Need admin approval** on Outlook or Teams, or when the xAI popup is blocked.

1. Have one user start Connect once so the service principal appears in the tenant. If it does not appear, use Path C.
2. Sign in to [https://entra.microsoft.com](https://entra.microsoft.com) as Cloud Application Administrator or higher.
3. **Entra ID** -> **Enterprise apps** -> **All applications**.
4. Search **Grok**, **xAI**, **SpaceXAI**, or the exact name on the consent screen. SharePoint **write** may be a second enterprise app.
5. Open the app -> **Security** -> **Permissions**.
6. Review every Graph scope. Expected sets are in sections 2.1--2.5. If you see `Sites.Read.All` plus write you did not ask for, **do not** grant.
7. **Grant admin consent for <your org>** -> **Accept**.
8. Confirm the list shows **Granted by: An administrator**.

Same grant also exists under **Entra ID** -> **App registrations** -> app -> **API permissions** -> **Grant admin consent**, but only for apps **your tenant registered**. Grok apps are usually **Enterprise applications** (Path B), not your own registration.

### Path C -- admin-consent URL (when you have the client ID)

Microsoft format:

```text
https://login.microsoftonline.com/{tenant}/adminconsent?client_id={client-id}
```

`{tenant}` = tenant GUID or verified domain. `{client-id}` = the app’s Application (client) ID from the consent screen or from Enterprise apps -> app -> Overview.

Do **not** invent a Grok client ID. Prefer Path A’s **Copy link** -- that URL already has the correct ID. xAI may register **more than one** app (read vs write). Consent each ID separately.

### Path D -- user request (“Approval required”)

If the tenant disabled user consent:

1. User clicks Connect -> **Approval required** -> justification -> **Request approval**.
2. Reviewers: **Entra ID** -> **Enterprise apps** -> **Admin consent requests** (workflow must be on: Enterprise apps -> Consent and permissions -> Admin consent settings).
3. A reviewer with a grant-capable role approves. Graph **application** permissions still need a Global Administrator.

Enable the workflow only if you want users to queue requests instead of emailing IT. It can take up to an hour to turn on.

### Verify

```text
Entra -> Enterprise apps -> [Grok app] -> Permissions
  Admin consent tab lists the scopes in 2.1-2.5
  Granted by: An administrator

grok.com/connectors -> operator Connect succeeds without admin-approval error
```

Optional Graph check (admin):

```http
GET https://graph.microsoft.com/v1.0/servicePrincipals?$filter=startswith(displayName,'Grok')
```

Then inspect `oauth2PermissionGrants` / `appRoleAssignments` for that service principal.

### Revoke

- Operator: grok.com/connectors -> **Disconnect**, and [myapps.microsoft.com](https://myapps.microsoft.com).
- Tenant: Entra -> Enterprise apps -> app -> Permissions -> **Admin consent** tab -> revoke. User-consent rows cannot be revoked in the portal UI; use Graph/PowerShell.
- Removing the connector in console.x.ai deletes org-wide indexed data for OneDrive/SharePoint.

### Assignment (optional harden)

After tenant-wide consent, Enterprise apps -> app -> **Properties** -> **Assignment required = Yes**, then assign only the AINav operators (or the dedicated SharePoint reader account). Unassigned users cannot use the app even though the tenant consented.

### What consent is not

- Not a dual seat
- Not LIVE_PIN_OK
- Not permission to put BC MCP in this repo
- Not “Grok may post a payment journal”

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

If “need admin approval”: Path B or D in section 2.0.

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

Complete **section 2.0 Path A** first.

**Member:** grok.com/connectors -> OneDrive -> work account -> Accept.

**Can:** browse nested folders; upload Grok-generated files (xlsx, pdf, reports).

**Cannot:** see other users’ drives. Full-text search of OneDrive *for Business* files needs the **SharePoint** connector as well (those files live on SharePoint infrastructure).

**Scopes:** `Files.ReadWrite`, `User.Read`, `offline_access` (delegated).

Disconnect deletes indexed data for that user. Admin removal deletes org-wide index.

**AINav:** drop L1 reports and AE drafts here. Not a DecisionRecord store.

---

### 2.5 SharePoint

Docs: [SharePoint connector](https://docs.x.ai/grok/connectors/sharepoint)

**Business / Enterprise only.** Complete **section 2.0 Path A** first (delegated + site-scoped account).

**Read scopes:** `Sites.Read.All`, `Files.Read.All`, `User.Read`, `offline_access`.  
**Write (if enabled):** `Files.ReadWrite.All` on a **second** enterprise app.

Every query is access-checked as the asking user.

**Can:** search documents across allowed sites; read library files; browse folders/drives; upload artifacts if write is on.

**AINav:** keep write **off** unless you have a written reason.

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

They do not hash tickets and they are not a dual seat. First user may also hit **Need admin approval** -- Path B in section 2.0.

---

## 5. Cursor on the same tenant

Cursor has **no** first-party “Connect Microsoft 365 Business.”

Official Microsoft links:

- **Teams `@Cursor`** -- Cloud Agent on a Git repo (needs Cursor GitHub app + usage-based pricing)
- **Azure DevOps** -- repos / PRs
- **Azure MCP** -- same allowlist as Build
- **Dataverse plugin** -- Marketplace; do **not** enable write in the plane folder

Mail / OneDrive / SharePoint inside Cursor = extra Graph MCP + Entra app + admin consent (section 2.0 Path B on **that** app, not Grok’s). Prefer Grok connectors for that context. Keep Cursor MCP = GitHub + Azure only.

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
    -> Entra admin consent (2.0) then operator Connect
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
Entra (admin)
  [ ] Tenant ID copied from Entra Overview
  [ ] Cloud Application Admin (or higher) available
  [ ] Path A: console.x.ai OneDrive + SharePoint provisioned
  [ ] Path A/B: Grant admin consent; Permissions show Granted by administrator
  [ ] SharePoint write app left off
  [ ] Optional: Assignment required = Yes, operators only

Grok account
  [ ] Same login for grok.com and grok CLI
  [ ] Outlook Mail + Outlook Calendar (two grants)
  [ ] Teams (engineering only)
  [ ] OneDrive Connect succeeds (no admin-approval error)
  [ ] SharePoint Connect as site-scoped account
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
  [ ] PIM role "AINav Approver" != GitHub CODEOWNER (same human, different seat)
  [ ] Teams Premium licenses on the two controllers only
  [ ] Separate AINav card app for admit
```

---

## 8. What this file is not

- Not a substitute for the Accept click in Entra
- Not LIVE_PIN_OK
- Not U-DUAL Redis
- Not a Grok / Cursor SKU
- Not permission to put BC MCP in this repo

Cursor and Grok Build ship code. AINav admits the write.

---

## 9. Links

| What | URL |
|------|-----|
| Grant tenant-wide admin consent | https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/grant-admin-consent |
| User vs admin consent | https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/user-admin-consent-overview |
| Admin consent workflow | https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/configure-admin-consent-workflow |
| Review / revoke app permissions | https://learn.microsoft.com/en-us/entra/identity/enterprise-apps/manage-application-permissions |
| Entra admin center | https://entra.microsoft.com |
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
