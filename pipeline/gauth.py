#!/usr/bin/env python3
"""
OAuth (as the user) helper for Drive upload + Sheet cell writes.
Uses a Desktop OAuth client (.secrets/oauth_client.json), caches token in
.secrets/token.json. This is the compliant write path (acts as the user; no
external sharing, no service account).

Commands:
  login                         one-time browser consent; caches token
  upload --folder <id> --files a.mp4 b.mp4    upload local files into a Drive folder
  setcells --sheet <id> --row N --kv "Col Name=Value" --kv "Col2=Val2"
"""
import argparse, json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
SEC = os.path.normpath(os.path.join(HERE, "..", ".secrets"))
CLIENT = os.path.join(SEC, "oauth_client.json")
TOKEN = os.path.join(SEC, "token.json")
SCOPES = [
    "https://www.googleapis.com/auth/drive",
    "https://www.googleapis.com/auth/spreadsheets",
]


def get_creds(interactive=False):
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    creds = None
    if os.path.exists(TOKEN):
        creds = Credentials.from_authorized_user_file(TOKEN, SCOPES)
    if creds and creds.valid:
        return creds
    if creds and creds.expired and creds.refresh_token:
        creds.refresh(Request())
        open(TOKEN, "w").write(creds.to_json())
        return creds
    if not interactive:
        sys.exit("NO_TOKEN: run `python3 gauth.py login` first.")
    from google_auth_oauthlib.flow import InstalledAppFlow
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT, SCOPES)
    creds = flow.run_local_server(
        port=0,
        open_browser=False,
        authorization_prompt_message="AUTHURL>>> {url}",
        success_message="Auth complete. You can close this tab and return to Claude.",
    )
    open(TOKEN, "w").write(creds.to_json())
    print("LOGIN_OK")
    return creds


def cmd_login(args):
    get_creds(interactive=True)


def cmd_upload(args):
    from googleapiclient.discovery import build
    from googleapiclient.http import MediaFileUpload
    drive = build("drive", "v3", credentials=get_creds(), cache_discovery=False)
    out = []
    for path in args.files:
        name = os.path.basename(path)
        media = MediaFileUpload(path, resumable=True)
        meta = {"name": name, "parents": [args.folder]}
        f = drive.files().create(body=meta, media_body=media,
                                 fields="id,name,webViewLink").execute()
        out.append({"name": f["name"], "id": f["id"], "link": f["webViewLink"]})
    print(json.dumps({"ok": True, "uploaded": out}, indent=2))


def _col_letter(idx0):
    s = ""
    n = idx0 + 1
    while n:
        n, r = divmod(n - 1, 26)
        s = chr(65 + r) + s
    return s


def cmd_setcells(args):
    from googleapiclient.discovery import build
    svc = build("sheets", "v4", credentials=get_creds(), cache_discovery=False).spreadsheets()
    headers = svc.values().get(spreadsheetId=args.sheet, range="1:1").execute().get("values", [[]])[0]
    data = []
    for kv in args.kv:
        col, val = kv.split("=", 1)
        if col not in headers:
            sys.exit(f"Column '{col}' not in headers {headers}")
        a1 = f"{_col_letter(headers.index(col))}{args.row}"
        data.append({"range": a1, "values": [[val]]})
    svc.values().batchUpdate(spreadsheetId=args.sheet,
                             body={"valueInputOption": "RAW", "data": data}).execute()
    print(json.dumps({"ok": True, "row": args.row, "wrote": [d["range"] for d in data]}))


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("login")
    p = sub.add_parser("upload"); p.add_argument("--folder", required=True); p.add_argument("--files", nargs="+", required=True)
    p = sub.add_parser("setcells"); p.add_argument("--sheet", required=True); p.add_argument("--row", type=int, required=True); p.add_argument("--kv", action="append", required=True)
    args = ap.parse_args()
    {"login": cmd_login, "upload": cmd_upload, "setcells": cmd_setcells}[args.cmd](args)


if __name__ == "__main__":
    main()
