#!/usr/bin/env python3
"""Nigraan's data tool (READ-ONLY): YouTube Analytics + Reporting data per channel. ₹0, never uploads or changes anything.

    python tools/yt_analytics.py <key> login            # one-time browser login (analytics token, separate file)
    python tools/yt_analytics.py <key> fetch            # all public/private videos: stats, analytics, traffic, retention
    python tools/yt_analytics.py <key> video <id>       # one video (post-mortem data)
    python tools/yt_analytics.py <key> reach-setup      # create Reporting API jobs (impressions + CTR); data starts later
    python tools/yt_analytics.py <key> reach-fetch      # download the Reach reports that exist so far

The upload token is never touched: this uses its own token secrets/<key>/analytics_token.json with the scopes
yt-analytics.readonly + youtube.readonly, made with the channel's own OAuth client (tools/yt_auth.py paths). After a
login, channels.list(mine) must return channel.json "channel_id", else the token is deleted. Never prints tokens.
Output: channels/<key>/analytics/ (videos.csv, video_<id>.json, reach/*.csv, fetch_log.jsonl).
API metrics: views, estimatedMinutesWatched, averageViewDuration, averageViewPercentage, subscribersGained, likes,
engagedViews, insightTrafficSourceType, audienceWatchRatio / relativeRetentionPerformance (retention curve).
Not in the Analytics API: thumbnail impressions + CTR (Reporting API "channel_reach_basic_a1", once the job runs) and
Shorts "viewed vs swiped away" (Studio only - see the nigraan agent for CSV export steps).
"""
import csv
import datetime as dt
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

sys.path.insert(0, str(Path(__file__).resolve().parent))
import yt_auth  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
SCOPES = ["https://www.googleapis.com/auth/yt-analytics.readonly",
          "https://www.googleapis.com/auth/youtube.readonly"]
REACH = ["channel_reach_basic_a1", "channel_reach_combined_a1"]


def token_file(key: str) -> Path:
    return ROOT / "secrets" / key / "analytics_token.json"


def creds(key: str, interactive=False):
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    tok = token_file(key)
    c = Credentials.from_authorized_user_file(str(tok)) if tok.exists() else None
    if c and c.expired and c.refresh_token:
        c.refresh(Request())
        tok.write_text(c.to_json(), encoding="utf-8")
    if not c or not c.valid:
        if not interactive:
            sys.exit(f"no analytics token for {key}: run  python tools/yt_analytics.py {key} login")
        client, _ = yt_auth.paths(key)
        print(f"Browser login (analytics, read-only): pick the Google account AND the channel "
              f"'{yt_auth.config(key).get('youtube_title') or yt_auth.config(key).get('display_name')}'.")
        c = InstalledAppFlow.from_client_secrets_file(str(client), SCOPES).run_local_server(port=0)
        tok.parent.mkdir(parents=True, exist_ok=True)
        tok.write_text(c.to_json(), encoding="utf-8")
    return c


def services(key, interactive=False):
    from googleapiclient.discovery import build
    c = creds(key, interactive)
    return (build("youtube", "v3", credentials=c), build("youtubeAnalytics", "v2", credentials=c),
            build("youtubereporting", "v1", credentials=c))


def check_channel(key, yt):
    want = yt_auth.config(key)["channel_id"]
    items = yt.channels().list(part="id,snippet,statistics,contentDetails", mine=True).execute().get("items", [])
    got = items[0]["id"] if items else None
    if got != want:
        token_file(key).unlink(missing_ok=True)
        sys.exit(f"WRONG CHANNEL: login is {got}, channel.json has {want}. Analytics token deleted; log in again.")
    return items[0]


def out_dir(key) -> Path:
    d = ROOT / "channels" / key / "analytics"
    d.mkdir(parents=True, exist_ok=True)
    return d


def iso_secs(d: str) -> int:
    import re
    m = re.match(r"PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", d or "")
    return int(m.group(1) or 0) * 3600 + int(m.group(2) or 0) * 60 + int(m.group(3) or 0) if m else 0


def all_videos(yt, ch):
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    ids, page = [], None
    while True:
        r = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=50, pageToken=page).execute()
        ids += [i["contentDetails"]["videoId"] for i in r.get("items", [])]
        page = r.get("nextPageToken")
        if not page:
            break
    vids = []
    for i in range(0, len(ids), 50):
        r = yt.videos().list(part="snippet,contentDetails,statistics,status", id=",".join(ids[i:i + 50])).execute()
        vids += r.get("items", [])
    return vids


def report(ya, cid, start, end, metrics, dims=None, filters=None, sort=None, maxr=None):
    q = dict(ids=f"channel=={cid}", startDate=start, endDate=end, metrics=metrics)
    if dims:
        q["dimensions"] = dims
    if filters:
        q["filters"] = filters
    if sort:
        q["sort"] = sort
    if maxr:
        q["maxResults"] = maxr
    r = ya.reports().query(**q).execute()
    cols = [h["name"] for h in r.get("columnHeaders", [])]
    return [dict(zip(cols, row)) for row in r.get("rows", [])]


def video_data(ya, cid, v):
    vid = v["id"]
    start = v["snippet"]["publishedAt"][:10]
    end = dt.date.today().isoformat()
    f = f"video=={vid}"
    d = {"id": vid, "title": v["snippet"]["title"], "published": v["snippet"]["publishedAt"],
         "privacy": v["status"]["privacyStatus"], "seconds": iso_secs(v["contentDetails"]["duration"]),
         "statistics": v.get("statistics", {})}
    d["is_short"] = d["seconds"] <= 180 and ("#shorts" in (v["snippet"].get("description", "") + d["title"]).lower()
                                            or d["seconds"] <= 60)
    try:
        d["totals"] = (report(ya, cid, start, end, "views,engagedViews,estimatedMinutesWatched,averageViewDuration,"
                              "averageViewPercentage,subscribersGained,likes,comments,shares", filters=f) or [{}])[0]
    except Exception as e:  # engagedViews may not be available for every channel/date
        d["totals"] = (report(ya, cid, start, end, "views,estimatedMinutesWatched,averageViewDuration,"
                              "averageViewPercentage,subscribersGained,likes", filters=f) or [{}])[0]
        d["totals_note"] = str(e)[:200]
    d["traffic"] = report(ya, cid, start, end, "views,estimatedMinutesWatched", dims="insightTrafficSourceType",
                          filters=f, sort="-views")
    try:
        d["retention"] = report(ya, cid, start, end, "audienceWatchRatio,relativeRetentionPerformance",
                                dims="elapsedVideoTimeRatio", filters=f + ";audienceType==ORGANIC")
    except Exception as e:
        d["retention"], d["retention_note"] = [], str(e)[:200]
    d["daily"] = report(ya, cid, start, end, "views,estimatedMinutesWatched", dims="day", filters=f, sort="day")
    d["fetched"] = dt.datetime.now().isoformat(timespec="seconds")
    return d


def save_video(key, d):
    (out_dir(key) / f"video_{d['id']}.json").write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")


def write_csv(key, rows):
    cols = ["id", "title", "published", "privacy", "is_short", "seconds", "views", "engagedViews", "averageViewDuration",
            "averageViewPercentage", "estimatedMinutesWatched", "subscribersGained", "likes", "comments", "top_traffic",
            "retention_30s"]
    with (out_dir(key) / "videos.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=cols)
        w.writeheader()
        for d in rows:
            t = d.get("totals", {})
            ret30 = ""
            if d.get("retention") and d["seconds"]:
                target = min(1.0, 30 / d["seconds"])
                ret30 = min(d["retention"], key=lambda r: abs(r["elapsedVideoTimeRatio"] - target))["audienceWatchRatio"]
            w.writerow({"id": d["id"], "title": d["title"], "published": d["published"][:16], "privacy": d["privacy"],
                        "is_short": d["is_short"], "seconds": d["seconds"],
                        **{k: t.get(k, "") for k in cols[6:14]},
                        "top_traffic": (d["traffic"][0]["insightTrafficSourceType"] if d.get("traffic") else ""),
                        "retention_30s": ret30})


def log(key, what):
    with (out_dir(key) / "fetch_log.jsonl").open("a", encoding="utf-8") as f:
        f.write(json.dumps({"at": dt.datetime.now().isoformat(timespec="seconds"), **what}, ensure_ascii=False) + "\n")


def main():
    key, cmd = sys.argv[1], sys.argv[2]
    yt, ya, yr = services(key, interactive=(cmd == "login"))
    ch = check_channel(key, yt)
    cid = ch["id"]
    if cmd == "login":
        print(f"Analytics login OK: {ch['snippet']['title']} ({cid}); token {token_file(key).relative_to(ROOT).as_posix()}")
        return
    if cmd in ("fetch", "video"):
        vids = all_videos(yt, ch)
        if cmd == "video":
            vids = [v for v in vids if v["id"] == sys.argv[3]]
        rows = []
        for v in vids:
            d = video_data(ya, cid, v)
            save_video(key, d)
            rows.append(d)
            print(f"{d['id']} {'SHORT' if d['is_short'] else 'LONG '} views={d.get('totals', {}).get('views', 0)} "
                  f"avd%={d.get('totals', {}).get('averageViewPercentage', '-')} {d['title'][:50]}")
        if cmd == "fetch":
            write_csv(key, rows)
        chan = report(ya, cid, ch["snippet"]["publishedAt"][:10], dt.date.today().isoformat(),
                      "views,estimatedMinutesWatched,subscribersGained,subscribersLost")
        (out_dir(key) / "channel_totals.json").write_text(json.dumps({"channel": ch["snippet"]["title"],
                                                                       "statistics": ch["statistics"], "totals": chan},
                                                                      ensure_ascii=False, indent=1), encoding="utf-8")
        log(key, {"cmd": cmd, "videos": len(rows)})
    elif cmd == "reach-setup":
        have = {j["reportTypeId"] for j in yr.jobs().list().execute().get("jobs", [])}
        for rt in REACH:
            if rt not in have:
                j = yr.jobs().create(body={"reportTypeId": rt, "name": f"nigraan {rt}"}).execute()
                print("created job", rt, j["id"])
            else:
                print("job exists", rt)
        log(key, {"cmd": cmd})
    elif cmd == "reach-fetch":
        from googleapiclient.http import MediaIoBaseDownload
        import io
        d = out_dir(key) / "reach"
        d.mkdir(exist_ok=True)
        for j in yr.jobs().list().execute().get("jobs", []):
            if j["reportTypeId"] not in REACH:
                continue
            for rep in yr.jobs().reports().list(jobId=j["id"]).execute().get("reports", []):
                f = d / f"{j['reportTypeId']}_{rep['startTime'][:10]}.csv"
                if f.exists():
                    continue
                buf = io.BytesIO()
                req = yr.media().download_media(resourceName="")
                req.uri = rep["downloadUrl"]
                dl = MediaIoBaseDownload(buf, req)
                done = False
                while not done:
                    _, done = dl.next_chunk()
                f.write_bytes(buf.getvalue())
                print("saved", f.name)
        log(key, {"cmd": cmd})


if __name__ == "__main__":
    main()
