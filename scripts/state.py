"""Per-channel stage state + locks for the Kaarigar agents (user 2026-10-25, "Kadam-1 safety").

    python scripts/state.py status                       # shared/status.md: one line per channel (also printed)
    python scripts/state.py start <key> <story> <stage> [--paid]   # take the channel lock (exit 3 if busy)
    python scripts/state.py done  <key> <stage> [--cost INR] [--note TEXT]
    python scripts/state.py fail  <key> <stage> --note TEXT   # also appends shared/incidents.md
    python scripts/state.py check <key> <story> <stage>  # stage contract (shared/stage_contracts.md) - exit 1 if broken

State: shared/state/<key>.json (story, stage, status running|done|failed, started, finished, pid, paid, cost, note,
last_error). One RUNNING stage per channel at a time; a PAID stage also takes the channel's paid lock - so two channels
can run together but never two paid stages in one channel. A lock older than its stage's time limit
(shared/stage_contracts.md) counts as stale: `start` refuses until the Sanchalak checks it (no silent takeover).
"""
import datetime as dt
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
STATE = ROOT / "shared" / "state"
STATUS = ROOT / "shared" / "status.md"
INCIDENTS = ROOT / "shared" / "incidents.md"
CHANNELS = ["dadi-ki-kahaniyan", "noor-e-raah"]
PAID = {"sheets", "images", "tts", "thumbnail"}  # stages that may spend money (Gemini)
LIMIT_MIN = {"sheets": 30, "images": 60, "tts": 60, "music_sfx": 15, "shots": 15, "build_long": 60, "build_short": 30,
             "thumbnail": 15, "upload": 30, "comments": 10, "sync": 10, "status": 10}


def now():
    return dt.datetime.now().isoformat(timespec="seconds")


def path(key):
    STATE.mkdir(parents=True, exist_ok=True)
    return STATE / f"{key}.json"


def load(key):
    p = path(key)
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def save(key, d):
    tmp = path(key).with_suffix(".tmp")
    tmp.write_text(json.dumps(d, ensure_ascii=False, indent=1), encoding="utf-8")
    tmp.replace(path(key))


def age_min(ts):
    return (dt.datetime.now() - dt.datetime.fromisoformat(ts)).total_seconds() / 60 if ts else 0


def start(key, story, stage, paid=False):
    d = load(key)
    if d.get("status") == "running":
        stale = age_min(d.get("started")) > LIMIT_MIN.get(d.get("stage"), 60)
        sys.exit(f"BUSY: {key} already runs '{d.get('stage')}' for {d.get('story')} since {d.get('started')}"
                 + (" - STALE (over its time limit): Sanchalak must check it, then `done`/`fail` it" if stale else ""))
    d.update(story=story, stage=stage, status="running", started=now(), finished=None, pid=os.getpid(),
             paid=bool(paid or stage in PAID), cost=None, note=None)
    save(key, d)
    write_status()
    print(f"started {key} {story} {stage}")


def finish(key, stage, ok, cost=None, note=None):
    d = load(key)
    if d.get("stage") != stage:
        sys.exit(f"{key}: running stage is '{d.get('stage')}', not '{stage}'")
    d.update(status="done" if ok else "failed", finished=now(), cost=cost, note=note)
    if not ok:
        d["last_error"] = f"{now()} {stage}: {note}"
        with INCIDENTS.open("a", encoding="utf-8") as f:
            f.write(f"| {now()} | {key} | {d.get('story')} | {stage} | {note} | open |\n")
    save(key, d)
    write_status()


def write_status():
    rows = ["# Status (scripts/state.py; Sanchalak updates it after every stage)", "",
            "| Channel | Story | Stage | Status | Since | Cost ₹ | Last error |", "|---|---|---|---|---|---|---|"]
    for k in CHANNELS:
        d = load(k)
        rows.append(f"| {k} | {d.get('story', '-')} | {d.get('stage', '-')} | {d.get('status', 'idle')} | "
                    f"{d.get('finished') or d.get('started') or '-'} | {d.get('cost') or '-'} | {d.get('last_error') or '-'} |")
    STATUS.write_text("\n".join(rows) + "\n", encoding="utf-8")
    return "\n".join(rows)


def check(key, story, stage):
    """Stage contract: the files a finished stage must have produced (shared/stage_contracts.md, section per stage)."""
    sd = ROOT / "channels" / key / "stories" / story
    need = {
        "tts": [sd / "long/lines.json"], "images": [sd / "images"], "build_long": [sd / "long/output"],
        "thumbnail": [sd / "long/output"], "upload": [sd / "long/output/upload_result.json"],
        "status": [ROOT / "shared/status.md"],
    }.get(stage, [])
    missing = [p.relative_to(ROOT).as_posix() for p in need if not p.exists()]
    if stage == "build_long":
        if not list((sd / "long/output").glob("*_final.mp4")):
            missing.append(f"{(sd / 'long/output').relative_to(ROOT).as_posix()}/*_final.mp4")
        if list((sd / "long/output").glob("*.part.mp4")):
            missing.append("a .part.mp4 is still there (render not finished)")
    if stage == "upload" and not missing:
        r = json.loads((sd / "long/output/upload_result.json").read_text(encoding="utf-8"))
        if not r.get("video_id"):
            missing.append("upload_result.json has no video_id")
    print("CONTRACT OK" if not missing else "CONTRACT BROKEN: " + "; ".join(missing))
    return not missing


def guard():
    """Stop/SubagentStop hook: a RUNNING stage over its time limit is reported (status STALE + one incident line).
    It is never killed or marked done here - the Sanchalak checks it (Monitor / files) and decides."""
    for k in CHANNELS:
        d = load(k)
        if d.get("status") == "running" and age_min(d.get("started")) > LIMIT_MIN.get(d.get("stage"), 60):
            if not d.get("stale_reported"):
                with INCIDENTS.open("a", encoding="utf-8") as f:
                    f.write(f"| {now()} | {k} | {d.get('story')} | {d.get('stage')} | over time limit "
                            f"({LIMIT_MIN.get(d.get('stage'), 60)} min) since {d.get('started')} | open |\n")
                d["stale_reported"] = True
                d["last_error"] = f"{now()} {d.get('stage')}: STALE (over time limit)"
                save(k, d)
    write_status()


def main():
    a = sys.argv[1:]
    if not a or a[0] == "status":
        print(write_status())
    elif a[0] == "guard":
        guard()
    elif a[0] == "start":
        start(a[1], a[2], a[3], "--paid" in a)
    elif a[0] in ("done", "fail"):
        cost = a[a.index("--cost") + 1] if "--cost" in a else None
        note = a[a.index("--note") + 1] if "--note" in a else None
        finish(a[1], a[2], a[0] == "done", cost, note)
    elif a[0] == "check":
        sys.exit(0 if check(a[1], a[2], a[3]) else 1)


if __name__ == "__main__":
    main()
