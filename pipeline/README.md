# Pipeline helpers

Two small helpers the agent drives from the terminal. The agent does the thinking
(product understanding, scriptwriting, generation); these handle Google I/O.

## `gauth.py` — OAuth-as-user (recommended write path)
Uploads files to Drive + writes Sheet cells, authenticated as **you** (no service
account, no external sharing — works inside locked-down Workspaces).
```
python3 gauth.py login                                   # one-time browser consent
python3 gauth.py upload --folder <DRIVE_FOLDER_ID> --files a.mp4 b.mp4
python3 gauth.py setcells --sheet <SHEET_ID> --row 2 --kv "Status=Done" --kv "Count=2"
```
Needs a **Desktop OAuth client** at `../.secrets/oauth_client.json` (see root README, Setup).

## `sheet.py` — service-account reader/writer (optional)
Only works if your org allows sharing a Sheet/Drive with a **service account**
(`../.secrets/service_account.json`). Many Workspaces block this — if so, use the
Google Drive MCP connector for reads + `gauth.py` for writes instead.
```
python3 sheet.py test
python3 sheet.py rows [--status Approved]
python3 sheet.py download --row 2 --dest ../Ads/<pid>_<slug>
```

Install deps: `pip3 install --user gspread google-auth google-auth-httplib2 google-auth-oauthlib google-api-python-client`
