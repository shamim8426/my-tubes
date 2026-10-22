#!/usr/bin/env python3
"""READ-ONLY YouTube look-up for Khoji's saturation check (shared/RULES.md section 16). Never uploads or changes anything.

Usage:
    python tools/yt_read.py search "<keywords>" --lang hi|en [--n 10]   # 100 quota units (search.list) + 1 (videos.list)
    python tools/yt_read.py quota                                       # units used today by this tool

Prints JSON: how many results came back, YouTube's rough total, the biggest video's views, and the top views list.
Titles are printed ONLY for counting/checking relevance; never copy a title, script, angle or thumbnail (RULES 16).
Uses the existing OAuth token (secrets/youtube_token_<channel>.json) with read calls only; never prints tokens.
Quota guard: max 10 searches per day by this tool (1000 units; uploads need ~1600 of the 10,000/day).
"""
import argparse
import datetime as dt
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
QUOTA_LOG = ROOT / "channels" / "_new_realstories" / "research" / "yt_quota.log"
TOKEN_CHANNEL = "dadi-ki-kahaniyan"  # read calls only; the new channel has no token yet
MAX_SEARCHES_PER_DAY = 10


def used_today():
    if not QUOTA_LOG.exists():
        return 0, 0
    today = dt.date.today().isoformat()
    rows = [l.split(",") for l in QUOTA_LOG.read_text(encoding="utf-8").splitlines() if l.startswith(today)]
    return sum(1 for r in rows if r[1] == "search"), sum(int(r[2]) for r in rows)


def log_units(kind, units):
    QUOTA_LOG.parent.mkdir(parents=True, exist_ok=True)
    with QUOTA_LOG.open("a", encoding="utf-8") as f:
        f.write(f"{dt.date.today().isoformat()},{kind},{units}\n")


def service():
    from google.oauth2.credentials import Credentials
    from google.auth.transport.requests import Request
    from googleapiclient.discovery import build
    tok = ROOT / "secrets" / f"youtube_token_{TOKEN_CHANNEL}.json"
    if not tok.exists():
        sys.exit("no YouTube token; read look-ups need the existing OAuth token")
    creds = Credentials.from_authorized_user_file(str(tok))
    if not creds.valid and creds.refresh_token:
        creds.refresh(Request())
    return build("youtube", "v3", credentials=creds)


def search(q, lang, n):
    searches, units = used_today()
    if searches >= MAX_SEARCHES_PER_DAY:
        sys.exit(f"quota guard: {searches} searches already today (max {MAX_SEARCHES_PER_DAY}); use the WebSearch estimate")
    yt = service()
    res = yt.search().list(part="snippet", q=q, type="video", maxResults=min(n, 50), relevanceLanguage=lang,
                           order="viewCount").execute()
    log_units("search", 100)
    ids = [i["id"]["videoId"] for i in res.get("items", [])]
    vids = []
    if ids:
        v = yt.videos().list(part="statistics,snippet", id=",".join(ids)).execute()
        log_units("videos", 1)
        vids = sorted(({"views": int(x["statistics"].get("viewCount", 0)), "title": x["snippet"]["title"],
                        "lang": x["snippet"].get("defaultAudioLanguage") or x["snippet"].get("defaultLanguage") or "?",
                        "published": x["snippet"]["publishedAt"][:10]} for x in v.get("items", [])),
                      key=lambda r: -r["views"])
    print(json.dumps({"query": q, "lang": lang, "returned": len(vids),
                      "total_estimate": res.get("pageInfo", {}).get("totalResults"),
                      "max_views": vids[0]["views"] if vids else 0, "top": vids[:5],
                      "searches_today": searches + 1}, ensure_ascii=False, indent=1))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["search", "quota"])
    ap.add_argument("q", nargs="?")
    ap.add_argument("--lang", default="hi", choices=["hi", "en"])
    ap.add_argument("--n", type=int, default=10)
    a = ap.parse_args()
    if a.cmd == "quota":
        s, u = used_today()
        print(f"today: {s} searches, {u} units (max {MAX_SEARCHES_PER_DAY} searches)")
    else:
        if not a.q:
            ap.error("search needs keywords")
        search(a.q, a.lang, a.n)


if __name__ == "__main__":
    main()
