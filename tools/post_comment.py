#!/usr/bin/env python3
"""Post a video's first comment once it is public: a Short's Short -> Long link (RULES section 8), or a long's
"first_comment" from its upload.json.

Usage:
    python tools/post_comment.py --job <short video folder>/output/upload.json --dry-run
    python tools/post_comment.py --job <short video folder>/output/upload.json      (run by the scheduled task)

Runs from the Windows scheduled task StoryChannel-Comment-<video_id> that youtube_upload.py creates for
the real publish time + 5 min. Checks the logged-in channel, waits while the video is not public yet (15 min, max 12
tries = 3 h, for the manual Studio step while the API is unaudited), posts "पूरी कहानी यहाँ देखें 👉 <long URL>" (or the job's first_comment), writes comment_id to upload_result.json, logs to shared/sync.log and
removes its own scheduled task. Never prints tokens.
"""
import argparse
import datetime as dt
import json
import subprocess
import sys
import time
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
SYNC_LOG = ROOT / "shared" / "sync.log"
CTA = "पूरी कहानी यहाँ देखें 👉 https://youtu.be/{id}"
TASK_PREFIX = "StoryChannel-Comment-"


def comment_text(parent_id: str) -> str:
    return CTA.format(id=parent_id)


def log(msg: str):
    line = f"{dt.datetime.now():%Y-%m-%d %H:%M:%S}  {msg}"
    SYNC_LOG.parent.mkdir(parents=True, exist_ok=True)
    with SYNC_LOG.open("a", encoding="utf-8") as f:
        f.write(line + "\n")
    print(line)


def task_name(video_id: str) -> str:
    return TASK_PREFIX + video_id


def _ps(cmd: str) -> subprocess.CompletedProcess:
    return subprocess.run(["powershell", "-NoProfile", "-NonInteractive", "-Command", cmd],
                          capture_output=True, text=True)


def schedule_task(job_path: Path, video_id: str, when: dt.datetime) -> str:
    """Windows scheduled task that runs this script once at `when` (timezone-aware)."""
    name = task_name(video_id)
    at = when.astimezone().replace(tzinfo=None)  # local wall-clock time for the task scheduler
    args = f'-X utf8 "{Path(__file__).resolve()}" --job "{Path(job_path).resolve()}"'
    cmd = (f"$a = New-ScheduledTaskAction -Execute '{sys.executable}' -Argument '{args}' -WorkingDirectory '{ROOT}'; "
           f"$t = New-ScheduledTaskTrigger -Once -At ([datetime]'{at:%Y-%m-%dT%H:%M:%S}'); "
           f"$s = New-ScheduledTaskSettingsSet -StartWhenAvailable; "
           f"Register-ScheduledTask -TaskName '{name}' -Action $a -Trigger $t -Settings $s -Force | Out-Null")
    r = _ps(cmd)
    if r.returncode:
        raise RuntimeError(f"could not create task {name}: {r.stderr.strip()[:300]}")
    return name


def task_exists(name: str) -> bool:
    return _ps(f"if (Get-ScheduledTask -TaskName '{name}' -ErrorAction SilentlyContinue) {{ exit 0 }} else {{ exit 1 }}"
               ).returncode == 0


def remove_task(name: str):
    _ps(f"Unregister-ScheduledTask -TaskName '{name}' -Confirm:$false -ErrorAction SilentlyContinue")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--job", required=True, help="the video's upload.json")
    ap.add_argument("--dry-run", action="store_true", help="show what would happen; no network, no comment")
    ap.add_argument("--attempts", type=int, default=12)
    ap.add_argument("--wait-min", type=float, default=15)
    a = ap.parse_args()

    job_path = Path(a.job).resolve()
    job = json.loads(job_path.read_text(encoding="utf-8"))
    result_path = job_path.parent / "upload_result.json"
    result = json.loads(result_path.read_text(encoding="utf-8")) if result_path.exists() else {}
    vid, parent = result.get("video_id"), job.get("parent_video_id")
    sys.path.insert(0, str(ROOT / "tools"))
    import youtube_upload as yu  # noqa: E402

    if not parent and not job.get("first_comment"):
        sys.exit("job has no parent_video_id or first_comment: nothing to post")
    text = comment_text(parent) if parent else job["first_comment"]
    if a.dry_run:
        print("DRY RUN (no network, no comment)")
        print("Channel:   ", job.get("channel_name"), job.get("channel_id"))
        print("Short id:  ", vid or "<not uploaded yet>")
        print("Comment:   ", text)
        print("Token file:", yu.token_path(job).name, "present" if yu.token_path(job).exists() else "MISSING")
        print("Task name: ", task_name(vid or "<video_id>"))
        print(f"Plan: check channel; if video not public, retry every {a.wait_min:g} min up to {a.attempts} times; "
              "post; save comment_id; remove the task; log to shared/sync.log")
        return

    if not vid:
        sys.exit("no video_id in upload_result.json")
    if result.get("comment_id"):
        log(f"comment: already posted on {vid} ({result['comment_id']}), nothing to do")
        remove_task(task_name(vid))
        return
    if not yu.token_path(job).exists():  # never open a browser from a scheduled task
        log(f"ERROR: comment for {vid}: no YouTube token ({yu.token_path(job).name}); log in once, then run again")
        sys.exit(1)

    yt = yu.get_service(job, interactive=False)
    yu.check_channel(yt, job)
    for attempt in range(1, a.attempts + 1):
        items = yt.videos().list(part="status", id=vid).execute().get("items", [])
        status = items[0]["status"]["privacyStatus"] if items else "missing"
        if status == "public":
            resp = yt.commentThreads().insert(part="snippet", body={"snippet": {
                "videoId": vid, "topLevelComment": {"snippet": {"textOriginal": text}}}}).execute()
            result["comment_id"] = resp["id"]
            result["comment_posted_at"] = dt.datetime.now(dt.timezone.utc).isoformat()
            result_path.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding="utf-8")
            log(f"comment: posted on {vid} (comment {resp['id']}) -> pin it in Studio")
            remove_task(task_name(vid))
            return
        if attempt < a.attempts:
            log(f"comment: {vid} is {status}, retry in {a.wait_min:g} min ({attempt}/{a.attempts})")
            time.sleep(a.wait_min * 60)
    log(f"ERROR: comment for {vid} not posted: video still {status} after {a.attempts} tries "
        f"(set it Public/Scheduled in Studio, then run tools/post_comment.py --job {job_path.relative_to(ROOT)})")
    sys.exit(1)


if __name__ == "__main__":
    main()
