# UGC Bot Automation — Runbook (template)

Fill every `<PLACEHOLDER>`. Commands run from the project; use your system `python3`.

## Daily ops
### Phase 1 — write scripts (`run scripts`)
1. Read the sheet (Drive MCP connector `read_file_content` on `<SHEET_ID>`, or `sheet.py rows`). Find rows with Drive Link + Product Detail Page and empty Claude Script.
2. For each: read the product page; write a script per the `ugc-ads` creative rules; then:
```
cd pipeline
python3 gauth.py setcells --sheet <SHEET_ID> --row <N> --kv 'Claude Script=<script>'
```
3. Stop. Wait for the human to set `Status = Approved` (approval gate).

### Phase 2 — generate + publish (`run approved`)
1. Read Approved rows. Final script = Feedback if non-empty else Claude Script.
2. Show a cost summary; get a go-ahead.
3. Generate with your video model; download raw → `Ads/<PID>_<slug>/raw_higgsfield/`.
4. Create a per-PID Drive subfolder under `<DRIVE_OUTPUT_PARENT_ID>`.
5. (Human post-produces into `Ads/<PID>_<slug>/final/`.)
6. Upload + write the sheet:
```
cd pipeline
python3 gauth.py upload --folder <SUBFOLDER_ID> --files ../Ads/<PID>_<slug>/final/*.mp4
python3 gauth.py setcells --sheet <SHEET_ID> --row <N> \
  --kv 'Video Output=<link>' --kv 'Avatar=<names>' --kv 'Job ID=<ids>' \
  --kv 'Status=Done' --kv 'Count=<n>' --kv 'Style=<style>'
```

## Setup (new machine)
1. Install **Python deps**: `pip3 install --user gspread google-auth google-auth-httplib2 google-auth-oauthlib google-api-python-client`
2. **GCP project** → enable **Google Drive API** + **Google Sheets API** (each; allow a couple minutes to propagate).
3. **OAuth Desktop client**: APIs & Services → Credentials → OAuth client ID → **Desktop** → download → save as `.secrets/oauth_client.json`. Then `python3 -u pipeline/gauth.py login` (run in background to capture the `AUTHURL>>>` it prints; open it in your browser, approve; token caches to `.secrets/token.json`).
4. **Reads**: connect a Drive MCP connector (sign in as yourself) **or** create a service account + share the sheet/folder with it (only if your org allows external sharing) and use `sheet.py`.
5. **Video model**: connect your generation tool (MCP or API).

## Gotchas (learned building this)
- **Service-account sharing is often blocked** by enterprise Workspace policy → prefer OAuth-as-user (`gauth.py`).
- **MCP file connectors can't upload large videos** (the bytes route through the model's context) and usually **can't edit Sheet cells** → use `gauth.py` for writes.
- **Browser-automation tools (e.g. Playwright) can't reliably log into Google** (Google blocks automated-browser sign-in) → not a Drive/Sheets write path.
- **Enable BOTH Drive + Sheets APIs**; wait for propagation after enabling.
- Some product pages **403 server-side fetchers** → download images with a browser User-Agent + Referer, or use the Drive input folder.
- `gauth.py login` stdout is block-buffered → run with `python3 -u` to see the auth URL.
- Editor MCP commands like `code --add-mcp` register with the **editor's** MCP host (e.g. Copilot), not necessarily with your agent — add agent MCP servers in the agent's own config (e.g. a project `.mcp.json`).
- **Never commit `.secrets/`.**
