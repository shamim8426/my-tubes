"""Reality Check - Asli: narrate a story's voiceover_clean.txt line by line with Gemini TTS (voice Kore).

    python tools/rc_tts.py <story> [--voice Kore] [--dry]    # run from the repo root of the worktree
Needs the repo .env (GEMINI keys): set RC_ENV to its path, e.g. D:\\my-tubes\\.env.

One TTS call per non-heading line (the line is one beat; gives per-line timing for the editor). Free key first, paid key
as fallback (gemini_keys). Cache: channels/reality-check/stories/<story>/audio/tts_cache/line_NNN.wav, so a re-run only
pays for missing lines. Cost guard: scripts/story_budget.check before the run (story cap in shared/pricing.json).
Output: audio/voiceover_full.wav (24 kHz mono) + audio/voiceover_timing.json (start/end per line, section starts).
Pauses: 0.45 s after a line, 0.9 s before a new section (heading line in the text file).
"""
import argparse
import json
import os
import sys
import time
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
from dotenv import load_dotenv  # noqa: E402

load_dotenv(os.environ.get("RC_ENV", str(ROOT / ".env")))
import gemini_tts  # noqa: E402
import story_budget  # noqa: E402

SR = gemini_tts.SR
STYLE = ("Calm, curious documentary narrator in Hinglish. Natural conversational pace, short pauses at full stops, "
         "slight emphasis on numbers. Warm, confident, not theatrical.")
USD_INR, GST, USD_PER_SEC = 96.5, 1.18, 25 * 9 / 1e6  # 25 audio tokens/s at $9 per 1M (shared/pricing.json)


def units(txt):
    out, new_section = [], True
    for raw in txt.splitlines():
        s = raw.strip()
        if not s:
            continue
        if s.startswith("#"):
            new_section = True
            continue
        out.append({"text": s, "section_start": new_section})
        new_section = False
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--voice", default="Kore")
    ap.add_argument("--dry", action="store_true")
    a = ap.parse_args()
    sd = ROOT / "channels/reality-check/stories" / a.story
    lines = units((sd / "script/voiceover_clean.txt").read_text(encoding="utf-8"))
    cache = sd / "audio/tts_cache"
    cache.mkdir(parents=True, exist_ok=True)
    todo = [i for i in range(len(lines)) if not (cache / f"line_{i + 1:03d}.wav").exists()]
    words = sum(len(lines[i]["text"].split()) for i in todo)
    est_secs = words / 130 * 60
    est_inr = est_secs * USD_PER_SEC * USD_INR * GST
    print(f"{len(lines)} lines, {len(todo)} to generate, ~{words} words, est ~{est_secs / 60:.1f} min audio, est cost ~Rs{est_inr:.1f} (if all paid)", flush=True)
    if a.dry or not todo:
        if a.dry:
            return
    else:
        story_budget.check(a.story, next_cost_inr=est_inr * 1.15)
    for n, i in enumerate(todo, 1):
        out = cache / f"line_{i + 1:03d}.wav"
        for attempt in (1, 2, 3):
            try:
                r = gemini_tts.speak(lines[i]["text"], a.voice, STYLE, out)
                print(f"[{n}/{len(todo)}] line {i + 1} {r['seconds']:.1f}s usd {r['usd']:.4f}", flush=True)
                break
            except Exception as e:  # noqa: BLE001
                print(f"line {i + 1} attempt {attempt} failed: {str(e)[:160]}", flush=True)
                if attempt == 3:
                    sys.exit(f"STOP at line {i + 1}; re-run to resume (cached lines are kept)")
                time.sleep(5)
        time.sleep(1.0)
    # concatenate + timing
    pcm, t, timing = bytearray(), 0.0, []
    cutf = sd / "script/cuts.json"  # {"skip_lines": [n..], "hold_after": {"2": 5.0}} (user 2026-11-08: no teasers; silent holds on footage)
    cuts = json.loads(cutf.read_text(encoding="utf-8")) if cutf.exists() else {}
    skip, hold = set(cuts.get("skip_lines", [])), {int(k): float(v) for k, v in cuts.get("hold_after", {}).items()}
    carry_section = False
    for i, ln in enumerate(lines):
        if (i + 1) in skip:
            carry_section = carry_section or ln["section_start"]
            continue
        if carry_section:
            ln = dict(ln, section_start=True)
            carry_section = False
        with wave.open(str(cache / f"line_{i + 1:03d}.wav")) as w:
            frames, dur = w.readframes(w.getnframes()), w.getnframes() / w.getframerate()
        if ln["section_start"] and i:
            gap = int(0.9 * SR) * 2
            pcm += b"\x00" * gap
            t += 0.9
        timing.append({"line": i + 1, "start": round(t, 2), "end": round(t + dur, 2), "section_start": ln["section_start"], "text": ln["text"]})
        pcm += frames
        t += dur
        pcm += b"\x00" * (int(0.45 * SR) * 2)
        t += 0.45
    with wave.open(str(sd / "audio/voiceover_full.wav"), "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR), w.writeframes(bytes(pcm))
    (sd / "audio/voiceover_timing.json").write_text(json.dumps(timing, ensure_ascii=False, indent=1), encoding="utf-8")
    nw = sum(len(x["text"].split()) for x in timing)
    print(f"DONE: {t / 60:.2f} min total, {nw} words -> {nw / (t / 60):.0f} wpm incl. pauses", flush=True)


if __name__ == "__main__":
    main()
