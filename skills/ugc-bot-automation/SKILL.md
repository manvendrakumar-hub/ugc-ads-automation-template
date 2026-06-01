---
name: ugc-bot-automation
description: Operate a Google-Sheet-driven bulk UGC ad pipeline — read product rows from a sheet, pull product images from Drive, read the product page, write scripts back, generate videos via a video model, download finals locally, upload approved finals to Drive, and update the sheet. Use whenever the user wants to run the bulk pipeline or any part of it ("run scripts", "run approved", "process the sheet", "update the sheet"). This is the OPS brain; the creative brain (scripts, voice, avatars, generation params) lives in the `ugc-ads` skill.
---

# UGC Bot Automation — Sheet-driven bulk pipeline (template)

Operations layer for producing UGC ads at scale from a Google Sheet. Pairs with the **`ugc-ads`** creative skill. This skill owns the plumbing: Sheet ↔ Drive ↔ video model ↔ local files.

> Commands + setup: `RUNBOOK.md`. Fill every `<PLACEHOLDER>` with your own IDs.

## Architecture (who does what)
- **Reads → Google Drive** (a Drive MCP connector authed as the user, or `pipeline/sheet.py` with a service account if your org allows it). Read sheet rows, list/inspect the Drive input folder, create per-PID output folders.
- **Writes → OAuth as the user** via `pipeline/gauth.py` (Drive + Sheets APIs): upload finals, write cells. This works even in locked-down Workspaces that block service accounts and automated-browser logins.
- **Generation → your video model** (e.g. Higgsfield Marketing Studio for talking-head Product-First; a reference-driven model like Seedance for "Yapping"). See the `ugc-ads` skill.
- **Glue → shell** (download, restructure).

## The sheet
Columns: `PID Name | Drive Link | Product Detail Page | Claude Script | Feedback | Status | Count | Style | Avatar | Video Output | Job ID`
- Human fills: PID Name, Drive Link (input product images), Product Detail Page, (later) Feedback, Status, Count, Style.
- Bot writes: Claude Script, Avatar, Video Output, Job ID, Status=Done.
- `Status`: blank → `Approved` / `Hold` → `Done`. `Count` blank = 1. `Style` = your ad styles.
- Sheet id, tab name → `pipeline/config.json`.

## Two-phase flow
**Phase 1 — `run scripts`** (rows with Drive Link + Product Detail Page + empty Claude Script): read row → read product page → write a script (per `ugc-ads` rules) into `Claude Script` → **stop at the approval gate.**

**Human:** review, optionally edit `Feedback`, set `Status = Approved / Hold`.

**Phase 2 — `run approved`** (Status = Approved): final script = Feedback if filled else Claude Script → pick avatar → generate `Count` video(s) in `Style` → download raw → human post-produces into `Ads/<PID>/final/` → upload to the per-PID Drive subfolder → write Video Output / Avatar / Job ID / Status=Done. **Always show a cost summary before generating.**

## Folder structure
```
Ads/<PID>_<slug>/raw_higgsfield/   (bot raw outputs)
Ads/<PID>_<slug>/final/            (human post-produced finals → uploaded)
pipeline/  gauth.py  sheet.py  config.json  README.md
.secrets/  (NEVER commit)  oauth_client.json  token.json  service_account.json
```
Drive: one output parent folder → one subfolder per PID.

See `RUNBOOK.md` for exact commands, new-machine setup, and the gotchas learned building this.
