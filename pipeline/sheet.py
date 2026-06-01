#!/usr/bin/env python3
"""
Sheet + Drive helper for the UGC Ads bulk pipeline.

Claude (the agent) calls this via the terminal to read/write the Google Sheet
and download product images from Drive. Claude itself handles product
understanding, scriptwriting, avatar choice, and Higgsfield generation.

Auth: a Google service account (see pipeline/README.md). The service-account
email must have Editor on the Sheet and Viewer on the Drive folder.

Usage (run from the pipeline/ dir):
  python3 sheet.py test
  python3 sheet.py rows [--status Approved]
  python3 sheet.py get --row 5 --col "Status"
  python3 sheet.py set --row 5 --col "Claude Script" --value-file /tmp/script.txt
  python3 sheet.py set --row 5 --col "Status" --value "Done"
  python3 sheet.py download --row 5 --dest ../Ads/<pid>_<slug>
Row numbers are the sheet's 1-based row numbers (header is row 1; first data row is 2).
"""
import argparse, json, os, re, sys, io

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG = json.load(open(os.path.join(HERE, "config.json")))
SCOPES = [
    "https://www.googleapis.com/auth/spreadsheets",
    "https://www.googleapis.com/auth/drive.readonly",
]
IMAGE_MIMES = ("image/jpeg", "image/png", "image/webp", "image/jpg")


def _abs(p):
    return p if os.path.isabs(p) else os.path.normpath(os.path.join(HERE, p))


def auth():
    from google.oauth2.service_account import Credentials
    import gspread
    from googleapiclient.discovery import build
    key_path = _abs(CONFIG["service_account_path"])
    if not os.path.exists(key_path):
        sys.exit(f"ERROR: service account key not found at {key_path}. See pipeline/README.md.")
    creds = Credentials.from_service_account_file(key_path, scopes=SCOPES)
    gc = gspread.authorize(creds)
    drive = build("drive", "v3", credentials=creds, cache_discovery=False)
    return gc, drive


def get_ws(gc):
    sid = CONFIG["sheet_id"]
    if sid == "PASTE_SHEET_ID_HERE":
        sys.exit("ERROR: set sheet_id in pipeline/config.json first.")
    sh = gc.open_by_key(sid)
    return sh.worksheet(CONFIG["worksheet"])


def _headers(ws):
    return ws.row_values(1)


def _col_index(ws, col_name):
    headers = _headers(ws)
    if col_name not in headers:
        sys.exit(f"ERROR: column '{col_name}' not found. Headers: {headers}")
    return headers.index(col_name) + 1  # 1-based


def cmd_test(args):
    gc, drive = auth()
    ws = get_ws(gc)
    print(json.dumps({
        "ok": True,
        "sheet_title": ws.spreadsheet.title,
        "worksheet": ws.title,
        "headers": _headers(ws),
        "data_rows": ws.row_count,
    }, indent=2))


def cmd_rows(args):
    gc, _ = auth()
    ws = get_ws(gc)
    records = ws.get_all_records()  # list of dicts keyed by header
    out = []
    for i, rec in enumerate(records, start=2):  # data starts at row 2
        if args.status and str(rec.get(CONFIG["columns"]["status"], "")).strip().lower() != args.status.lower():
            continue
        rec["_row"] = i
        out.append(rec)
    print(json.dumps(out, indent=2, ensure_ascii=False))


def cmd_get(args):
    gc, _ = auth()
    ws = get_ws(gc)
    c = _col_index(ws, args.col)
    print(ws.cell(args.row, c).value or "")


def cmd_set(args):
    gc, _ = auth()
    ws = get_ws(gc)
    c = _col_index(ws, args.col)
    if args.value_file:
        value = open(args.value_file, encoding="utf-8").read()
    else:
        value = args.value if args.value is not None else ""
    ws.update_cell(args.row, c, value)
    print(json.dumps({"ok": True, "row": args.row, "col": args.col, "chars": len(value)}))


def _extract_id(url):
    for pat in (r"/folders/([a-zA-Z0-9_-]+)", r"/file/d/([a-zA-Z0-9_-]+)", r"[?&]id=([a-zA-Z0-9_-]+)"):
        m = re.search(pat, url)
        if m:
            return m.group(1)
    return None


def _is_folder(drive, fid):
    meta = drive.files().get(fileId=fid, fields="mimeType,name", supportsAllDrives=True).execute()
    return meta["mimeType"] == "application/vnd.google-apps.folder", meta


def _download_file(drive, fid, name, dest):
    from googleapiclient.http import MediaIoBaseDownload
    path = os.path.join(dest, name)
    req = drive.files().get_media(fileId=fid)
    with io.FileIO(path, "wb") as fh:
        dl = MediaIoBaseDownload(fh, req)
        done = False
        while not done:
            _, done = dl.next_chunk()
    return path


def cmd_download(args):
    gc, drive = auth()
    dest = _abs(args.dest)
    os.makedirs(dest, exist_ok=True)
    fid = _extract_id(args.url) if args.url else None
    if not fid and args.row:
        ws = get_ws(gc)
        c = _col_index(ws, CONFIG["columns"]["drive"])
        link = ws.cell(args.row, c).value or ""
        fid = _extract_id(link)
    if not fid:
        sys.exit("ERROR: could not extract a Drive file/folder id (pass --url or --row).")
    is_folder, meta = _is_folder(drive, fid)
    saved = []
    if is_folder:
        q = f"'{fid}' in parents and trashed = false"
        res = drive.files().list(q=q, fields="files(id,name,mimeType)",
                                  supportsAllDrives=True, includeItemsFromAllDrives=True).execute()
        for f in res.get("files", []):
            if f["mimeType"] in IMAGE_MIMES:
                saved.append(_download_file(drive, f["id"], f["name"], dest))
    else:
        saved.append(_download_file(drive, fid, meta["name"], dest))
    print(json.dumps({"ok": True, "dest": dest, "files": saved}, indent=2))


def main():
    ap = argparse.ArgumentParser(description="UGC bulk pipeline sheet/drive helper")
    sub = ap.add_subparsers(dest="cmd", required=True)
    sub.add_parser("test")
    p = sub.add_parser("rows"); p.add_argument("--status")
    p = sub.add_parser("get"); p.add_argument("--row", type=int, required=True); p.add_argument("--col", required=True)
    p = sub.add_parser("set"); p.add_argument("--row", type=int, required=True); p.add_argument("--col", required=True)
    p.add_argument("--value"); p.add_argument("--value-file")
    p = sub.add_parser("download"); p.add_argument("--row", type=int); p.add_argument("--url"); p.add_argument("--dest", required=True)
    args = ap.parse_args()
    {"test": cmd_test, "rows": cmd_rows, "get": cmd_get, "set": cmd_set, "download": cmd_download}[args.cmd](args)


if __name__ == "__main__":
    main()
