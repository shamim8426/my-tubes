"""Noor unattended driver: runs every mechanical stage of one story, resumable and idempotent, up to the Munshi gates and the upload.

    .venv/bin/python -X utf8 scripts/noor_run.py channels/noor-e-raah/stories/<NNN>_<slug> [--detach] [--status] [--until STAGE]

Stages (each skipped when its output already exists, so a container restart or a re-run just continues):
    parse -> images -> tts (rate-limit retries) -> [gate: long/review/tts_review.md VERDICT PASS]
          -> render (chunked, parallel, resumable) -> thumbnail -> [gate: long/review/final_review.md VERDICT PASS]
          -> upload (youtube_upload.py, once) -> mark queue + budget line + log + sync
The two gates are Munshi's reviews (an agent): the driver stops with exit code 3 and says which review is needed; the Sanchalak runs
Munshi and starts the driver again. Exit codes: 0 done, 3 waiting for a review, 1 failed.
--detach starts the driver in its own session (survives the shell), logging to <story>/run.log."""
import json
import re
import shutil
import subprocess
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PY = sys.executable
STAGES = ["parse", "images", "tts", "gate_tts_review", "render", "thumbnail", "gate_final_review", "upload"]
RATE_WAIT, RATE_TRIES = 75, 6


def sh(args, log=None, check=False):
    r = subprocess.run([PY, "-X", "utf8", *map(str, args)], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")
    out = (r.stdout or "") + (r.stderr or "")
    if log:
        with open(log, "a", encoding="utf-8") as f:
            f.write(out)
    return r.returncode, out


def verdict(review: Path):
    """Last 'VERDICT: X' word in a review file (None if the file or verdict is missing)."""
    if not review.exists():
        return None
    m = re.findall(r"VERDICT:?\s*\**\s*(PASS|FIX|ASK)", review.read_text(encoding="utf-8"))
    return m[-1] if m else None


class Run:
    def __init__(self, story: Path):
        self.story = story
        self.key = story.parents[1].name
        self.slug = story.name
        self.out = story / "long/output"
        self.sf = story / "run_state.json"
        self.state = json.loads(self.sf.read_text()) if self.sf.exists() else {}
        self.log = story / "run.log"

    def note(self, stage, status, msg=""):
        self.state[stage] = {"status": status, "at": time.strftime("%Y-%m-%d %H:%M:%S"), "note": msg}
        self.sf.write_text(json.dumps(self.state, indent=1, ensure_ascii=False), encoding="utf-8")
        line = f"[{time.strftime('%H:%M:%S')}] {stage}: {status} {msg}"
        print(line, flush=True)
        with open(self.log, "a", encoding="utf-8") as f:
            f.write(line + "\n")

    def state_py(self, *a):  # shared/status.md bookkeeping; never fatal
        try:
            sh(["scripts/state.py", *a])
        except Exception:
            pass

    # ---- stages: each returns "done" | "skip" | "wait" | raises RuntimeError
    def parse(self):
        lines, script = self.story / "long/lines.json", self.story / "script/script.md"
        if lines.exists() and lines.stat().st_mtime >= script.stat().st_mtime:
            return "skip", "lines.json is current"
        rc, out = sh(["scripts/noor_build.py", self.story, "parse"], self.log)
        if rc:
            raise RuntimeError("parse failed: " + out[-300:])
        return "done", ""

    def images(self):
        rc, out = sh(["scripts/noor_build.py", self.story, "images"], self.log)
        if rc:
            raise RuntimeError("images failed: " + out[-300:])
        return "done", out.strip().splitlines()[-1][:160] if out.strip() else ""

    def tts(self):
        for attempt in range(1, RATE_TRIES + 1):
            rc, out = sh(["scripts/noor_build.py", self.story, "tts"], self.log)
            if rc == 0:
                return "done", [l for l in out.splitlines() if "Whisper OK" in l][-1:][0] if "Whisper OK" in out else ""
            if "429" in out or "Rate limit" in out:
                self.note("tts", "rate-limited", f"attempt {attempt}/{RATE_TRIES}, waiting {RATE_WAIT}s (finished lines stay cached)")
                time.sleep(RATE_WAIT)
                continue
            raise RuntimeError("tts failed: " + out[-300:])
        raise RuntimeError("tts: still rate-limited after retries (daily quota?) - ask the owner")

    def gate(self, review_name):
        v = verdict(self.story / "long/review" / review_name)
        if v == "PASS":
            return "skip", "Munshi PASS"
        if v in ("FIX", "ASK"):
            raise RuntimeError(f"{review_name} says {v}: fix what it lists, then re-run")
        return "wait", f"needs Munshi: write long/review/{review_name} with 'VERDICT: PASS'"

    def render(self):
        final = self.out / f"{self.slug}_final.mp4"
        if final.exists() and final.stat().st_size > 1_000_000:
            return "skip", "final.mp4 exists"
        rc, out = sh(["scripts/noor_render.py", self.story], self.log)
        if rc or not final.exists():
            raise RuntimeError("render failed (chunks stay on disk, re-run resumes): " + out[-300:])
        return "done", out.strip().splitlines()[-1][:160]

    def thumbnail(self):
        t = self.out / f"{self.slug}_thumbnail.jpg"
        if t.exists():
            return "skip", "thumbnail exists"
        rc, out = sh(["scripts/noor_thumb_v3.py", self.story, "--generate", "--engine", "auto", "--layouts", "ABC"], self.log)
        c = self.out / f"{self.slug}_thumbnail_v3C.jpg"
        if rc or not c.exists():
            raise RuntimeError("thumbnail failed: " + out[-300:])
        shutil.copy(c, t)  # default layout C (hook first); Munshi may swap it in the final review
        return "done", "layout C copied (A/B also in output/)"

    def upload(self):
        if (self.out / "upload_result.json").exists():
            return "skip", "already uploaded (upload_result.json)"
        rc, out = sh(["tools/youtube_upload.py", "--job", self.out / "upload.json"], self.log)
        if rc or not (self.out / "upload_result.json").exists():
            raise RuntimeError("upload failed (NOT retried automatically): " + out[-400:])
        res = json.loads((self.out / "upload_result.json").read_text(encoding="utf-8"))
        slug_key = re.sub(r"^\d+_", "", self.slug).replace("_", "-")
        sh(["scripts/noor_daily.py", "mark", slug_key, "uploaded", "--note", res.get("video_id", "")], self.log)
        _, b = sh(["scripts/story_budget.py", self.slug, "--log"], self.log)
        with open(ROOT / f"channels/{self.key}/log.md", "a", encoding="utf-8") as f:
            f.write(f"\n- {time.strftime('%Y-%m-%d')} {self.slug} UPLOADED private by noor_run: https://youtu.be/{res.get('video_id')} - "
                    f"{(res.get('studio_action') or '').splitlines()[0] if res.get('studio_action') else ''} | {b.strip().splitlines()[0] if b.strip() else ''}\n")
        subprocess.run(["bash", "tools/sync.sh", f"noor {self.slug[:3]}: uploaded private"], cwd=ROOT, capture_output=True)
        return "done", f"https://youtu.be/{res.get('video_id')}"


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    story = (ROOT / args[0]).resolve() if not Path(args[0]).is_absolute() else Path(args[0])
    r = Run(story)
    if "--status" in sys.argv:
        for st in STAGES:
            s = r.state.get(st, {})
            print(f"{s.get('status', '-'):14} {st:18} {s.get('note', '')}")
        return 0
    if "--detach" in sys.argv:
        cmd = [PY, "-X", "utf8", str(Path(__file__).resolve()), str(story)] + [a for a in sys.argv[2:] if a != "--detach"]
        subprocess.Popen(cmd, cwd=ROOT, stdout=open(r.log, "a"), stderr=subprocess.STDOUT, stdin=subprocess.DEVNULL, start_new_session=True)
        print(f"started detached; log: {r.log}")
        return 0
    until = sys.argv[sys.argv.index("--until") + 1] if "--until" in sys.argv else None
    for st in STAGES:
        fn = r.gate if st.startswith("gate_") else getattr(r, st)
        r.state_py("start", r.key, r.slug, st) if not st.startswith("gate_") else None
        try:
            res, msg = fn("tts_review.md" if st == "gate_tts_review" else "final_review.md") if st.startswith("gate_") else fn()
        except RuntimeError as e:
            r.note(st, "failed", str(e))
            r.state_py("fail", r.key, st, str(e)[:120])
            return 1
        r.note(st, {"done": "done", "skip": "done (skipped, already ok)", "wait": "WAITING"}[res], msg)
        if not st.startswith("gate_"):
            r.state_py("done", r.key, st)
        if res == "wait":
            return 3
        if until == st:
            return 0
    r.note("all", "done", "pipeline finished")
    return 0


if __name__ == "__main__":
    sys.exit(main())
