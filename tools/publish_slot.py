#!/usr/bin/env python3
"""Publish timing (shared/RULES.md section 8): decided right AFTER the upload finishes, from the real IST clock.

Long:
  - 19:00-23:59 IST and no other long that day  -> public now.
  - 00:00-18:59 IST and no other long that day  -> scheduled 19:00 the same day.
  - that day already has a long (public or scheduled) -> next free day 19:00.
Short of a long: long's publish time + 60 min (a long at 19:00 -> Short 20:00). If that falls after 23:59 of the
long's day, or is already (almost) past, the Short goes public now.
Stand-alone Short: same as a long's day logic but at the Short time (20:00), no one-per-day limit.

Usage (check only, no network):
    python tools/publish_slot.py <channel_key> long [--now 2026-10-21T20:10] [--earliest 2026-11-01]
"""
import argparse
import datetime as dt
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
IST = dt.timezone(dt.timedelta(hours=5, minutes=30))
MIN_LEAD = dt.timedelta(minutes=5)  # a slot closer than this is treated as "now"


def now_ist() -> dt.datetime:
    return dt.datetime.now(IST)


def _hm(s: str) -> dt.time:
    h, m = s.split(":")
    return dt.time(int(h), int(m))


def channel_times(key: str):
    cfg = json.loads((ROOT / "channels" / key / "channel.json").read_text(encoding="utf-8"))
    t = cfg.get("publish_times_ist", {})
    return _hm(t.get("long", "19:00")), int(cfg.get("short_after_long_min", 60)), cfg


def _day(iso):
    if not iso:
        return None
    try:
        t = dt.datetime.fromisoformat(str(iso).replace("Z", "+00:00"))
    except ValueError:
        return None
    return t.astimezone(IST).date() if t.tzinfo else None


def result_publish_time(result: dict):
    """The time a video (counts as) publishing: planned time from the new rule, else the old fixed publish_at."""
    for k in ("planned_publish_at", "publish_at"):
        if result.get(k):
            return result[k]
    return None


def local_long_days(key: str, exclude_video: str = None) -> set:
    """IST days that already have a long, from every upload_result.json of the channel (removed/vetoed skipped)."""
    days = set()
    for res in (ROOT / "channels" / key / "stories").glob("**/output/upload_result.json"):
        if any(p.startswith("_") for p in res.relative_to(ROOT).parts[:-1]):
            continue  # e.g. output/_v1_revealed (removed from YouTube)
        r = json.loads(res.read_text(encoding="utf-8"))
        if r.get("vetoed_at") or r.get("removed") or r.get("video_id") == exclude_video:
            continue
        job_file = res.parent / "upload.json"
        fmt = json.loads(job_file.read_text(encoding="utf-8")).get("format") if job_file.exists() else None
        if (fmt or ("long" if "/long/" in res.as_posix() else "short")) != "long":
            continue
        d = _day(result_publish_time(r))
        if d:
            days.add(d)
    return days


def _seconds(iso_dur: str) -> int:
    m = re.fullmatch(r"P(?:(\d+)D)?T?(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?", iso_dur or "")
    if not m:
        return 0
    d, h, mi, s = (int(x or 0) for x in m.groups())
    return ((d * 24 + h) * 60 + mi) * 60 + s


def api_long_days(yt, exclude_video: str = None, max_items: int = 50) -> set:
    """IST days with a long on the channel itself: scheduled (publishAt) or public (publishedAt). Long = over 75 s."""
    ch = yt.channels().list(part="contentDetails", mine=True).execute()["items"][0]
    uploads = ch["contentDetails"]["relatedPlaylists"]["uploads"]
    items = yt.playlistItems().list(part="contentDetails", playlistId=uploads, maxResults=max_items).execute()
    ids = [i["contentDetails"]["videoId"] for i in items.get("items", []) if i["contentDetails"]["videoId"] != exclude_video]
    days = set()
    if not ids:
        return days
    for v in yt.videos().list(part="status,snippet,contentDetails", id=",".join(ids)).execute().get("items", []):
        if _seconds(v["contentDetails"].get("duration")) <= 75:
            continue
        st = v["status"]
        d = _day(st.get("publishAt")) if st.get("publishAt") else (
            _day(v["snippet"].get("publishedAt")) if st.get("privacyStatus") == "public" else None)
        if d:
            days.add(d)
    return days


def plan_long(now: dt.datetime, taken: set, long_time: dt.time, earliest: dt.date = None):
    """(when, mode) for a long; mode 'now' or 'schedule'."""
    now = now.astimezone(IST)
    day = max(now.date(), earliest) if earliest else now.date()
    if day == now.date() and day not in taken and now.time() >= long_time:
        return now, "now"
    while day in taken:
        day += dt.timedelta(days=1)
    when = dt.datetime.combine(day, long_time, IST)
    if when <= now:  # today's slot passed but today taken -> loop above already moved on; safety
        day += dt.timedelta(days=1)
        while day in taken:
            day += dt.timedelta(days=1)
        when = dt.datetime.combine(day, long_time, IST)
    if when - now < MIN_LEAD:
        return now, "now"
    return when, "schedule"


def plan_short(now: dt.datetime, parent_time: dt.datetime, gap_min: int = 60):
    """(when, mode) for a Short of a long published (or scheduled) at parent_time."""
    now = now.astimezone(IST)
    parent_time = parent_time.astimezone(IST)
    when = parent_time + dt.timedelta(minutes=gap_min)
    if when.date() != parent_time.date() or when - now < MIN_LEAD:
        return now, "now"
    return when, "schedule"


def plan_standalone_short(now: dt.datetime, long_time: dt.time, gap_min: int = 60, earliest: dt.date = None):
    short_time = (dt.datetime.combine(dt.date.today(), long_time) + dt.timedelta(minutes=gap_min)).time()
    return plan_long(now, set(), short_time, earliest)


def find_result(video_id: str):
    """upload_result.json dict of any video in any channel (None if not found)."""
    for res in ROOT.glob("channels/*/stories/**/output/upload_result.json"):
        r = json.loads(res.read_text(encoding="utf-8"))
        if r.get("video_id") == video_id:
            return r
    return None


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("channel_key")
    ap.add_argument("format", choices=["long", "short"])
    ap.add_argument("--parent", help="Short: the long video's id")
    ap.add_argument("--now", help="IST time to test with, e.g. 2026-10-21T20:10")
    ap.add_argument("--earliest", help="long: not before this date (YYYY-MM-DD)")
    a = ap.parse_args()
    now = dt.datetime.fromisoformat(a.now).replace(tzinfo=IST) if a.now else now_ist()
    long_time, gap, _ = channel_times(a.channel_key)
    earliest = dt.date.fromisoformat(a.earliest) if a.earliest else None
    if a.format == "long":
        taken = local_long_days(a.channel_key)
        when, mode = plan_long(now, taken, long_time, earliest)
        print("days with a long (local):", ", ".join(sorted(map(str, taken))) or "-")
    elif a.parent:
        r = find_result(a.parent) or {}
        pt = result_publish_time(r)
        if not pt:
            raise SystemExit(f"no publish time known for parent {a.parent}")
        when, mode = plan_short(now, dt.datetime.fromisoformat(pt), gap)
    else:
        when, mode = plan_standalone_short(now, long_time, gap, earliest)
    print(f"now {now:%Y-%m-%d %H:%M} IST -> {'PUBLIC NOW' if mode == 'now' else f'SCHEDULE {when:%Y-%m-%d %H:%M} IST'}")


if __name__ == "__main__":
    main()
