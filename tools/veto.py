#!/usr/bin/env python3
""""rok do" — stop a scheduled video before its slot (shared/RULES.md section 14, veto window).

Usage:
    python tools/veto.py <video_id>            # dry run (default): no network, shows what would change
    python tools/veto.py <video_id> --apply    # really do it

--apply: checks the logged-in channel, sets the video private and removes publishAt (other status fields are
kept), disables the Short's first-comment task (StoryChannel-Comment-<id>), writes vetoed_at to the video's
upload_result.json, logs a line in channels/<key>/log.md and marks the story "vetoed" in pipeline_queue.json
(the pipeline for that story pauses). A video that is already public is refused unless --force.
Never prints tokens.
"""
import argparse
import datetime as dt
import json
import re
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(Path(__file__).resolve().parent))
STATUS_KEEP = ("license", "embeddable", "publicStatsViewable", "selfDeclaredMadeForKids", "containsSyntheticMedia")


def find_upload(video_id: str):
    """(upload_result.json path, result, upload.json job) for this video id, searched in every channel."""
    for res in ROOT.glob("channels/*/stories/**/output/upload_result.json"):
        result = json.loads(res.read_text(encoding="utf-8"))
        if result.get("video_id") == video_id:
            job_file = res.parent / "upload.json"
            job = json.loads(job_file.read_text(encoding="utf-8")) if job_file.exists() else {}
            return res, result, job
    return None, None, None


def vetoed_status(current: dict) -> dict:
    """Status body for videos.update: private, no publishAt, writable fields kept (part=status replaces all)."""
    body = {k: current[k] for k in STATUS_KEEP if k in current}
    body["privacyStatus"] = "private"
    return body


def story_of(res: Path):
    """(channel key, story folder name) from .../channels/<key>/stories/<story>/.../output/upload_result.json."""
    parts = res.relative_to(ROOT).parts
    return parts[1], parts[3]


def mark_paused(key: str, story: str, video_id: str, when: str):
    q = ROOT / "channels" / key / "pipeline_queue.json"
    data = json.loads(q.read_text(encoding="utf-8")) if q.exists() else {"stories": {}}
    entry = data.setdefault("stories", {}).setdefault(story, {})
    entry.update({"stage": "vetoed", "updated": when[:10],
                  "stopped": f"rok do: {video_id} set private, publishAt removed ({when}). Pipeline paused; ASK the user."})
    q.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("video_id")
    ap.add_argument("--apply", action="store_true", help="really change the video (default is a dry run)")
    ap.add_argument("--force", action="store_true", help="also make an already public video private")
    args = ap.parse_args()
    vid = args.video_id.strip()
    if not re.fullmatch(r"[A-Za-z0-9_-]{11}", vid):
        sys.exit(f"Not a YouTube video id: {vid!r} (11 characters)")

    res, result, job = find_upload(vid)
    if not res:
        sys.exit(f"No upload_result.json with video_id {vid} in channels/*/stories. Nothing done.")
    key, story = story_of(res)
    if not job.get("channel_id"):
        sys.exit(f"{res.parent / 'upload.json'} missing or has no channel_id. Nothing done.")
    task = f"StoryChannel-Comment-{vid}"
    print("Video:      ", f"https://youtu.be/{vid}", f"({job.get('format', '?')})")
    print("Title:      ", job.get("title", "-"))
    print("Channel:    ", key, job["channel_id"])
    print("Story:      ", story)
    print("Slot now:   ", result.get("publish_at") or job.get("publish_at") or "-")
    print("Will do:     privacyStatus=private, remove publishAt, disable task", task,
          f"| log.md + pipeline_queue.json: {story} -> vetoed")

    if not args.apply:
        print("\nDry run OK. Nothing changed (add --apply to really stop this video).")
        return

    from youtube_upload import check_channel, get_service, with_retry
    yt = get_service(job)
    check_channel(yt, job)  # exits on a channel ID mismatch
    items = yt.videos().list(part="status", id=vid).execute().get("items", [])
    if not items:
        sys.exit(f"Video {vid} not found on the channel. Nothing done.")
    cur = items[0]["status"]
    if cur.get("privacyStatus") == "public" and not args.force:
        sys.exit(f"{vid} is already PUBLIC (slot passed). Not changed; run with --force to make it private anyway.")
    body = {"id": vid, "status": vetoed_status(cur)}
    with_retry(lambda: yt.videos().update(part="status", body=body).execute(), "veto")
    after = yt.videos().list(part="status", id=vid).execute()["items"][0]["status"]
    if after.get("privacyStatus") != "private" or after.get("publishAt"):
        sys.exit(f"Veto did not stick: privacy={after.get('privacyStatus')} publishAt={after.get('publishAt')}. Check Studio.")

    from post_comment import _ps, task_exists
    task_note = "no comment task"
    if task_exists(task):
        _ps(f"Disable-ScheduledTask -TaskName '{task}' | Out-Null")
        task_note = f"task {task} disabled"

    now = dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds")
    result.update({"vetoed_at": now, "publish_at_before_veto": cur.get("publishAt") or result.get("publish_at"),
                   "publish_at": None})
    res.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
    with (ROOT / "channels" / key / "log.md").open("a", encoding="utf-8") as f:
        f.write(f"{now[:10]} | {story} | VETO (rok do) | {vid} private, publishAt removed "
                f"(was {cur.get('publishAt') or '-'}); {task_note}; pipeline paused\n")
    mark_paused(key, story, vid, now)
    print(f"\nStopped: https://youtu.be/{vid} is private, no schedule. {task_note}. Pipeline for {story} paused.")


if __name__ == "__main__":
    main()
