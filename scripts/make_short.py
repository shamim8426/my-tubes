"""One command -> full Short (voice, captions, Ken Burns, music, -14 LUFS, metadata).

Usage:  python scripts/make_short.py <case> [--preview | --final] [--spend]
          --preview (default)  540x960, 24 fps, ultrafast: only for checking -> output/<case>_preview.mp4
          --final              1080x1920, 30 fps, good quality + Whisper/frame/loudness checks -> output/<case>.mp4
          --spend              allow paid TTS for lines not in the cache (otherwise the build stops and shows the cost)
Needs:  a video folder with project.json (channels/<key>/stories/<story>/long or .../shorts/short_XX_<slug>)
        + lines.json, meta.json, shots.json; story-level images/scene_XX.png, audio/, scene_prompts.json

Caching: every TTS line (audio/<case>/tts_cache) and every scene clip (cache/<case>/scene_XX_<hash>.mp4, captions
burned in) is reused while its inputs are unchanged. The final step only concatenates clips (no re-encode),
mixes the audio and muxes.
"""
import argparse
import csv
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import time
import wave
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, str(Path(__file__).parent))
import cost_log  # noqa: E402
import gemini_tts  # noqa: E402
from voices import CAST, pitch_filter  # noqa: E402
from paths import FONTS_DIR, MUSIC_DIR, REGISTER, ROOT, SFX_DIR, channel_of, story_of  # noqa: E402

FFMPEG = ROOT / "tools" / "ffmpeg" / "ffmpeg.exe"
if not FFMPEG.exists():  # new system: ffmpeg from winget on PATH (tools/ffmpeg is not in git)
    FFMPEG = Path(shutil.which("ffmpeg") or FFMPEG)
FONT = FONTS_DIR / "Mukta-ExtraBold.ttf"

PROFILES = {
    ("short", "preview"): {"w": 540, "h": 960, "fps": 24, "enc": ["-preset", "ultrafast", "-crf", "30"]},
    ("short", "final"): {"w": 1080, "h": 1920, "fps": 30, "enc": ["-preset", "slow", "-crf", "18"]},
    ("long", "preview"): {"w": 960, "h": 540, "fps": 24, "enc": ["-preset", "ultrafast", "-crf", "30"]},
    ("long", "final"): {"w": 1920, "h": 1080, "fps": 30, "enc": ["-preset", "slow", "-crf", "18"]},
}
MUSIC_XFADE = 1.5  # seconds of crossfade when the mood (music track) changes
RENDER_VERSION = 3  # bump when scene rendering code changes, to invalidate the clip cache (3: full bt709 tags)
PLAY_W, PLAY_H = 1080, 1920  # caption coordinate space (libass scales it to the output size)
SR = 24000  # Gemini TTS output rate
GAP, END_HOLD = 0.30, 1.5  # silence between lines; hold on the final question
TAIL = 0.12  # kept after the last voiced frame of each line
SHOT_LEN = 2.6  # target seconds per shot -> visual changes every 2-3s
MIN_SHOT = 1.2  # never cut faster than this
CUT_LEAD = 0.1  # a speaker's shot starts this long before their voice, never earlier
TARGET_LUFS = -14
# Music gain: voice LUFS minus this, per video kind. Checked in loudness_report the RULES way: integrated LUFS
# of the voice stem vs the music stem over the speech sections (long: 13 = old 9 lowered by 4 dB).
MUSIC_BELOW_VOICE_DB = {"short": 12.5, "long": 13}  # short: 9 -> 12.5 (3.5 dB quieter, target 12-14 LU)
SFX_BELOW_VOICE_DB = 5
MIN_CAPTION = 0.45  # a caption shorter than this only flashes; it is merged into its neighbour in the same line
PAUSE_LEAD = 2.0  # music must be audible in a music-only pause and this long before it

# Ken Burns moves for wide shots (cycled): zoom-in, pan, zoom-out, zoom-to-top
MOVES = {
    "in": ("1+0.08*on/{n}", "iw/2-iw/zoom/2", "ih/2-ih/zoom/2"),
    "out": ("1.08-0.08*on/{n}", "iw/2-iw/zoom/2", "ih/2-ih/zoom/2"),
    "pan": ("1.08", "(iw-iw/zoom)*on/{n}", "ih/2-ih/zoom/2"),
    "top": ("1+0.08*on/{n}", "iw/2-iw/zoom/2", "(ih-ih/zoom)*0.3"),
}
MOVE_CYCLE = ["in", "pan", "out", "top"]


def run(args, cwd=None):
    r = subprocess.run([str(a) for a in args], cwd=cwd, capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode:
        sys.exit(f"FAILED: {' '.join(map(str, args))[:300]}\n{r.stderr[-2000:]}")
    return r


def sha(*parts) -> str:
    h = hashlib.sha1()
    for p in parts:
        h.update(p if isinstance(p, bytes) else str(p).encode("utf-8"))
    return h.hexdigest()[:16]


# ---------- 1. voice ----------
def tts_key(text, speaker):
    voice, style, _ = CAST[speaker]
    return f"{speaker}_{sha(gemini_tts.MODEL, '|', voice, '|', style, '|', text)}.wav"


def check_tts_spend(lines, cache: Path, allow: bool):
    """Paid TTS only on cache miss, and only with --spend. Otherwise stop and show the estimate."""
    misses = [l for l in lines if "text" in l and not (cache / tts_key(l["text"], l["speaker"])).exists()]
    if not misses:
        return
    secs = sum(len(l["text"].split()) / 2.4 for l in misses)  # ~2.4 words/s
    usd = secs * gemini_tts.AUDIO_TOKENS_PER_SEC * gemini_tts.PRICE_OUT / 1e6
    print(f"  {len(misses)} TTS line(s) not cached: " + ", ".join(l["speaker"] for l in misses)
          + f"  -> ~₹{usd * cost_log.USD_TO_INR:.2f}")
    if not allow:
        sys.exit("  Paid TTS needed. Re-run with --spend to allow it.")


def tts_line(text, speaker, cache: Path, out: Path, extra_af=None, chorus=False) -> bytes:
    """Cached Gemini TTS + optional pitch shift / extra filter (e.g. echo) / chorus (3 detuned, offset copies
    so one voice sounds like a group). Returns PCM s16 mono."""
    raw = cache / tts_key(text, speaker)
    if not raw.exists():
        voice, style, _ = CAST[speaker]
        res = gemini_tts.speak(text, voice, style, raw)
        print(f"    new TTS {speaker}: ₹{res['row']['cost_inr']} (aaj ₹{res['row']['today_total_inr']}, "
              f"bacha ₹{res['row']['remaining_inr']})")
    chain = ",".join(f for f in (pitch_filter(CAST[speaker][2], SR), extra_af) if f) or "anull"
    if chorus:
        fc = (f"[0:a]{chain},asplit=3[a][b][c];[b]{pitch_filter(2, SR)},adelay=45[b2];"
              f"[c]{pitch_filter(-2, SR)},adelay=90[c2];[a][b2][c2]amix=inputs=3:normalize=0,volume=0.6[o]")
        args = ["-filter_complex", fc, "-map", "[o]"]
    else:
        args = ["-af", chain]
    run([FFMPEG, "-y", "-i", raw, *args, "-ac", "1", "-ar", SR, "-sample_fmt", "s16", out])
    with wave.open(str(out)) as w:
        return w.readframes(w.getnframes())


def trim(data: bytes) -> bytes:
    """Trim lead/tail silence by energy so the line's voice starts at its first sample."""
    x = np.frombuffer(data, np.int16).astype(np.float32) / 32768
    hop = int(0.01 * SR)
    lev = 20 * np.log10(np.sqrt(np.mean(x[: len(x) // hop * hop].reshape(-1, hop) ** 2, axis=1)) + 1e-9)
    voiced = np.where(lev > lev.max() - 35)[0]
    s0 = max(0, voiced[0] * hop - int(0.01 * SR))
    e0 = min(len(x), (voiced[-1] + 1) * hop + int(TAIL * SR))
    return data[s0 * 2:e0 * 2]


_whisper = None


def _clean_len(s):
    return len(re.sub(r"[^\u0900-\u097F\w]", "", s))


def word_times(data: bytes, text: str, cache: Path, run_whisper: bool):
    """Script tokens timed by Whisper word timestamps (cached per audio). Whisper's spelling may differ from the
    script, so timings are mapped through character position. Without a cached result, Whisper only runs when
    run_whisper (final); otherwise timings are proportional to word length."""
    global _whisper
    tokens = text.split()
    dur = len(data) / 2 / SR
    key = cache / f"words_{sha(data)}.json"
    ww, note = [], None
    if key.exists():
        ww = json.loads(key.read_text(encoding="utf-8"))
    elif run_whisper:
        if _whisper is None:
            from faster_whisper import WhisperModel
            _whisper = WhisperModel("small", device="cpu", compute_type="int8",
                                    download_root=str(ROOT / "tools" / "whisper-models"))
        x = np.frombuffer(data, np.int16).astype(np.float32) / 32768
        x16 = np.interp(np.arange(0, len(x), SR / 16000), np.arange(len(x)), x).astype(np.float32)
        # no initial_prompt: with the script as prompt Whisper sometimes skips words it thinks were already said
        segs, _ = _whisper.transcribe(x16, language="hi", word_timestamps=True, beam_size=5)
        ww = [(w.start, w.end, w.word.strip()) for s in segs for w in (s.words or []) if _clean_len(w.word)]
        key.write_text(json.dumps(ww, ensure_ascii=False), encoding="utf-8")
    else:
        note = "proportional (Whisper runs on --final)"
    # only trust Whisper if it heard roughly the whole line (it can drop words)
    coverage = sum(_clean_len(w) for _, _, w in ww) / max(1, sum(_clean_len(t) for t in tokens))
    if ww and not 0.75 <= coverage <= 1.35:
        ww, note = [], f"PROPORTIONAL (whisper coverage {coverage:.0%})"
    if ww:
        lens = [_clean_len(w) for _, _, w in ww]
        tot, acc, xs, ts = sum(lens), 0, [], []
        for (a, b, _), n in zip(ww, lens):
            xs += [acc / tot, (acc + n) / tot]
            ts += [a, b]
            acc += n
        xs[0], xs[-1] = 0.0, 1.0
        note = f"whisper {coverage:.0%}"
    else:
        xs, ts = [0.0, 1.0], [0.0, dur]
    lens = [_clean_len(t) + 1 for t in tokens]
    tot, acc, words = sum(lens), 0, []
    for tok, n in zip(tokens, lens):
        words.append((float(np.interp(acc / tot, xs, ts)), float(np.interp((acc + n) / tot, xs, ts)), tok))
        acc += n
    return words, note


def build_voice(lines, audio_dir: Path, work: Path, run_whisper: bool, end_hold: float = END_HOLD,
                gap_s: float = GAP, speed: float = 1.0):
    """speed: tempo factor for every spoken line (atempo keeps the pitch; cached TTS reused, no new cost).
    gap_s: silence between lines (meta.json "gap" / "speed" let a Short run tighter than the long video)."""
    pcm, t = bytearray(), 0.0
    GAP = gap_s  # noqa: N806 - local override of the module default
    silence = lambda sec: b"\x00\x00" * int(round(sec * SR))
    timed, events = [], {"sfx": [], "music_silent": [], "moods": []}
    cache = audio_dir / "tts_cache"
    for i, line in enumerate(lines):
        if "pause" in line:  # music-only beat with its own picture
            gap = GAP if i else 0.0
            pcm += silence(gap + line["pause"])
            start, t = t + gap, t + gap + line["pause"]
            if line.get("mood"):
                events["moods"].append((start, line["mood"]))
            if line.get("sfx"):
                events["sfx"].append((start + 0.05, line["sfx"]))
            timed.append({**line, "speaker": "_pause", "text": "", "start": start, "end": t,
                          "audio_hash": f"pause{line['pause']}", "words": []})
            events.setdefault("pauses", []).append((start - PAUSE_LEAD, t))
            print(f"  line {i + 1:2d} [{'pause':8s}] {start:6.2f}-{t:6.2f}s  music only")
            continue
        tempo = f"atempo={speed}" if speed != 1.0 else None
        data = trim(tts_line(line["text"], line["speaker"], cache,
                             work / f"line_{i + 1:02d}_{line['speaker']}.wav",  # per video, not the shared story audio/
                             extra_af=",".join(f for f in (line.get("af"), tempo) if f) or None,
                             chorus=line.get("chorus", False)))
        words, note = word_times(data, line["text"], cache, run_whisper)
        if i:
            gap = GAP + line.get("pause_before", 0)
            if line.get("music_silent_before"):
                events["music_silent"].append((t + GAP / 2, t + gap))
            pcm += silence(gap)
            t += gap
        start = t
        if line.get("mood"):
            events["moods"].append((start - (line.get("pause_before", 0) + GAP if i else 0), line["mood"]))
        pcm += data
        t += len(data) / 2 / SR
        timed.append({**line, "start": start, "end": t, "audio_hash": sha(data),
                      "words": [(start + a, start + b, w) for a, b, w in words]})
        if line.get("sfx_after"):
            events["sfx"].append((t + 0.05, line["sfx_after"]))
        print(f"  line {i + 1:2d} [{line['speaker']:8s}] {start:6.2f}-{t:6.2f}s  {note}")
    pcm += silence(end_hold)
    total = len(pcm) / 2 / SR
    voice = work / "voice.wav"
    with wave.open(str(voice), "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR), w.writeframes(bytes(pcm))
    return voice, total, timed, events


# ---------- 2. captions ----------
def ass_time(s):
    cs = max(0, int(round(s * 100)))
    return f"{cs // 360000}:{cs // 6000 % 60:02d}:{cs // 100 % 60:02d}.{cs % 100:02d}"


def caption_chunks(line):
    """[(start, end, text)] in global seconds, 2-3 words each, never past the line's audio.
    An optional "caption" in lines.json changes only the on-screen text (no new TTS); its words are timed
    through character position on the spoken words' timeline."""
    words = line["words"]
    tokens = line.get("caption", line["text"]).split()
    if "caption" in line and len(tokens) != len(words):
        lens = [_clean_len(w) + 1 for _, _, w in words]
        xs = np.concatenate([[0], np.cumsum(lens)]) / sum(lens)
        ts = [words[0][0]] + [e for _, e, _ in words]
        clens = [_clean_len(t) + 1 for t in tokens]
        cx = np.concatenate([[0], np.cumsum(clens)]) / sum(clens)
        words = [(float(np.interp(cx[k], xs, ts)), float(np.interp(cx[k + 1], xs, ts)), tok)
                 for k, tok in enumerate(tokens)]
    chunks, cur, punct = [], [], r"[।!?,.…]$"
    for j, (tok, (s, e, _)) in enumerate(zip(tokens, words)):
        cur.append((tok, s, e))
        nxt = tokens[j + 1] if j + 1 < len(tokens) else None
        lone_next = nxt is not None and re.search(punct, nxt) and len(cur) < 4  # don't orphan "है!"
        if (len(cur) >= 3 and not lone_next) or re.search(punct, tok):
            chunks.append(cur)
            cur = []
    if cur:
        chunks.append(cur)
    dur = lambda k: (chunks[k + 1][0][1] if k + 1 < len(chunks) else line["end"]) - chunks[k][0][1]
    k = 0
    while len(chunks) > 1 and k < len(chunks):
        if dur(k) < MIN_CAPTION:  # merge into the previous chunk (or the next one, for the first)
            j = k - 1 if k else 0
            chunks[j:j + 2] = [chunks[j] + chunks[j + 1]]
            k = 0
        else:
            k += 1
    out = []
    for k, ch in enumerate(chunks):
        end = chunks[k + 1][0][1] if k + 1 < len(chunks) else line["end"]
        out.append((ch[0][1], end, " ".join(tok for tok, _, _ in ch)))
    return out


def ass_doc(font_family, events):
    return f"""[Script Info]
ScriptType: v4.00+
PlayResX: {PLAY_W}
PlayResY: {PLAY_H}
WrapStyle: 0
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: Cap,{font_family},116,&H00FFFFFF,&H000000FF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,9,4,2,60,60,480,1
Style: Title,{font_family},128,&H0000E5FF,&H000000FF,&H00000000,&H78000000,0,0,0,0,100,100,0,0,1,9,4,8,60,60,170,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
""" + "\n".join(events) + "\n"


# ---------- 3. video: one cached clip per scene ----------
def shot_times(timed, total):
    """Per scene: cut points (seconds). A scene starts CUT_LEAD before its first line's voice; inside a scene
    every new speaker's line also starts a shot CUT_LEAD early; long stretches are split every ~SHOT_LEN.
    A line with "shot" in lines.json ("wide" or [x, y, zoom(, crop_x, crop_y)]) gets that one shot for its whole
    stretch; "shots": [[spec, seconds], ..., [spec, null]] splits the stretch (last one takes the rest).
    Returns (scene, cut points, per-shot override or None)."""
    scenes = []
    for i, line in enumerate(timed):
        t = 0.0 if i == 0 else line["start"] - CUT_LEAD
        if not scenes or scenes[-1][0] != line["scene"]:
            scenes.append([line["scene"], [t], [i]])
        elif line["speaker"] != timed[i - 1]["speaker"]:
            scenes[-1][1].append(t)
            scenes[-1][2].append(i)
    out = []
    for k, (sc, cuts, owners) in enumerate(scenes):
        end = scenes[k + 1][1][0] if k + 1 < len(scenes) else total
        pts = cuts + [end]
        fine, tags = [pts[0]], []
        for a, b, own in zip(pts, pts[1:], owners):
            if timed[own].get("shots"):
                t = a
                for spec, secs in timed[own]["shots"]:
                    end = b if secs is None else min(b, t + secs)
                    if end > t:
                        fine.append(end)
                        tags.append(spec)
                        t = end
                fine[-1] = b
                continue
            if timed[own].get("shot"):
                fine.append(b)
                tags.append(timed[own]["shot"])
                continue
            n = max(1, min(round((b - a) / SHOT_LEN), int((b - a) / MIN_SHOT)))
            fine += [a + (b - a) * j / n for j in range(1, n + 1)]
            tags += [None] * n
        if len(fine) == 2 and tags[0] is None and fine[1] - fine[0] >= 2 * MIN_SHOT:  # at least wide + close
            fine.insert(1, (fine[0] + fine[1]) / 2)
            tags.append(None)
        out.append((sc, fine, tags))
    return out


def plan_scenes(P, timed, total, prof, font_family, final_title, title_secs=None):
    """Everything needed to render each scene clip, plus its cache hash."""
    focus = P["focus"]
    fps, plans = prof["fps"], []
    shots_all = shot_times(timed, total)
    for idx, (sc, cuts, tags) in enumerate(shots_all):
        fcuts = [round(c * fps) for c in cuts]  # one global frame grid -> no drift between clips
        t0 = fcuts[0] / fps
        spec = focus.get(str(sc), [])
        closes, wide = (spec["closes"], spec.get("wide", True)) if isinstance(spec, dict) else (spec, True)
        # 1 shot: close-up matters more; "wide": false (scene sharing an image with another) -> close-ups only
        cycle = closes if (closes and (len(cuts) == 2 or not wide)) else ["wide"] + closes
        shots, desc = [], []
        for k in range(len(cuts) - 1):
            n = fcuts[k + 1] - fcuts[k]
            shot = tags[k] or cycle[k % len(cycle)]
            if shot == "wide":
                move = MOVE_CYCLE[(idx + k) % len(MOVE_CYCLE)]
                z, x, y = (e.format(n=n) for e in MOVES[move])
                desc.append(move)
            else:
                # x, y: inside the frame-shaped window; optional crop_x/crop_y: where that window sits on a wider or
                # taller image (subject centre, 0-1; default centre) - e.g. a 9:16 Short from 16:9 story images
                fx, fy, zc, *crop = shot
                z = f"{zc}+{zc * 0.06:.3f}*on/{n}"  # slow push-in on the close-up
                x = f"max(0,min(iw-iw/zoom,{fx}*iw-iw/zoom/2))"
                y = f"max(0,min(ih-ih/zoom,{fy}*ih-ih/zoom/2))"
                desc.append(f"close{zc}" + (f"@x{crop[0]}" if crop else ""))
            shots.append((n, z, x, y) + (tuple(crop) if shot != "wide" and crop else ()))
        lines = [l for l in timed if l["scene"] == sc]
        ass = None
        if P["burn"]:
            ev = [f"Dialogue: 0,{ass_time(s - t0)},{ass_time(e - t0)},Cap,,0,0,0,,{txt}"
                  for l in lines if l["words"] for s, e, txt in caption_chunks(l)]
            if idx == len(shots_all) - 1 and final_title:
                t_end = fcuts[-1] / fps - t0
                t_beg = max(0.0, t_end - title_secs) if title_secs else 0.0  # e.g. a 2 s end card only
                ev.append(f"Dialogue: 1,{ass_time(t_beg)},{ass_time(t_end)},Title,,0,0,0,,"
                          f"{{\\fad(300,0)}}{final_title}")
            ass = ass_doc(font_family, ev)
        img = P["image_for"](sc)
        key = sha(RENDER_VERSION, json.dumps(prof, sort_keys=True), sha(img.read_bytes()),
                  [l["audio_hash"] for l in lines], json.dumps(shots), ass)
        plans.append({"scene": sc, "t0": t0, "t1": fcuts[-1] / fps, "frames": fcuts[-1] - fcuts[0],
                      "shots": shots, "ass": ass, "img": img, "key": key, "desc": desc})
    return plans


def render_scene(p, prof, clip: Path, work: Path):
    w, h, fps = prof["w"], prof["h"], prof["fps"]
    ass_name = f"scene_{p['scene']:02d}_{p['key']}.ass"
    if p["ass"]:
        (work / ass_name).write_text(p["ass"], encoding="utf-8")
    subs = f",subtitles=filename={ass_name}:fontsdir=fonts" if p["ass"] else ""
    n = len(p["shots"])
    pre = f"[0:v]scale={w * 2}:{h * 2}:force_original_aspect_ratio=increase"
    fc = [pre + (f",split={n}" + "".join(f"[i{k}]" for k in range(n)) if n > 1 else "[i0]")]
    for k, (d, z, x, y, *crop) in enumerate(p["shots"]):
        cx, cy = (list(crop) + [0.5, 0.5])[:2]  # frame-shaped window on the image, centred on (cx, cy)
        win = (f"crop={w * 2}:{h * 2}:x='max(0,min(iw-ow,{cx}*iw-ow/2))':y='max(0,min(ih-oh,{cy}*ih-oh/2))'")
        fc.append(f"[i{k}]{win},zoompan=z='{z}':x='{x}':y='{y}':d={d}:s={w}x{h}:fps={fps}[z{k}]")
    fc.append("".join(f"[z{k}]" for k in range(n)) + (f"concat=n={n}:v=1:a=0" if n > 1 else "null")
              + f"{subs},scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setsar=1,"
                f"setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709[out]")
    tmp = clip.with_suffix(".part.mp4")
    run([FFMPEG, "-y", "-i", p["img"], "-filter_complex", ";".join(fc), "-map", "[out]", "-frames:v", p["frames"],
         "-c:v", "libx264", *prof["enc"], "-pix_fmt", "yuv420p", "-color_range", "tv", "-colorspace", "bt709",
         "-color_primaries", "bt709", "-color_trc", "bt709", "-r", fps,
         "-video_track_timescale", fps * 1000, tmp], cwd=work)
    tmp.replace(clip)


def build_video(plans, prof, cache_dir: Path, work: Path):
    todo = [p for p in plans if not (cache_dir / f"scene_{p['scene']:02d}_{p['key']}.mp4").exists()]
    for p in plans:
        state = "NEW" if p in todo else "cache"
        print(f"  scene {p['scene']:2d}: {p['t0']:6.2f}-{p['t1']:6.2f}s  {state:5s}  {' | '.join(p['desc'])}")
    with ThreadPoolExecutor(max_workers=max(2, (os.cpu_count() or 4) // 2)) as pool:
        list(pool.map(lambda p: render_scene(p, prof, cache_dir / f"scene_{p['scene']:02d}_{p['key']}.mp4", work),
                      todo))
    listing = [f"file '{(cache_dir / f'scene_{p['scene']:02d}_{p['key']}.mp4').as_posix()}'" for p in plans]
    (work / "scenes.txt").write_text("\n".join(listing), encoding="utf-8")
    run([FFMPEG, "-y", "-f", "concat", "-safe", "0", "-i", "scenes.txt", "-c", "copy", "video.mp4"], cwd=work)
    return len(plans) - len(todo), len(todo)


# ---------- 4. audio mix + loudness ----------
def pick_music(meta):
    if meta.get("music"):
        return MUSIC_DIR / meta["music"]
    bed = MUSIC_DIR / "mystery_bed.wav"
    if not bed.exists():
        run([sys.executable, ROOT / "scripts" / "gen_music.py"])
    return bed


def integrated_lufs(path, seconds=None):
    r = run([FFMPEG, "-hide_banner", "-i", path, *(["-t", seconds] if seconds else []),
             "-af", "loudnorm=print_format=json", "-f", "null", "-"])
    return float(json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])["input_i"])


def music_segments(events, meta, total):
    """[(start, end, file)]: one segment per mood run (lines.json 'mood'), or the single track for the whole video."""
    moods = meta.get("music_moods")
    if not (moods and events["moods"]):
        return [(0.0, total, pick_music(meta))]
    runs = []
    for t, mood in sorted(events["moods"]):
        if not runs or runs[-1][1] != mood:
            runs.append((max(0.0, t), mood))
    runs[0] = (0.0, runs[0][1])
    return [(t, runs[k + 1][0] if k + 1 < len(runs) else total, MUSIC_DIR / moods[mood])
            for k, (t, mood) in enumerate(runs)]


_levels = {}


def track_levels(f: Path):
    """Music track loudness every 0.1 s (dB, 0.5 s RMS window), for picking where to start a track."""
    if f not in _levels:
        r = subprocess.run([str(FFMPEG), "-v", "error", "-i", str(f), "-ac", "1", "-ar", "8000", "-f", "s16le", "-"],
                           capture_output=True)
        x = np.frombuffer(r.stdout, np.int16).astype(np.float32) / 32768
        e = np.convolve(x ** 2, np.ones(4000) / 4000, mode="same")[::800]
        _levels[f] = 10 * np.log10(e + 1e-12)
    return _levels[f]


def music_offset(f: Path, a, b, windows):
    """Seconds into the track to start a segment [a, b] so no music-only pause (plus PAUSE_LEAD before it) lands
    in a near-silent gap of the track (e.g. between piano phrases). 0 when the segment has no pause."""
    wins = [(max(s, a), min(e, b)) for s, e in windows if e > a and s < b]
    if not wins:
        return 0.0
    lev = track_levels(f)
    n = len(lev)
    idx = [i for s, e in wins if len(i := np.arange(int((s - a) * 10), int((e - a) * 10)))]
    if not idx:
        return 0.0
    score = lambda off: min(lev[(i + int(off * 10)) % n].min() for i in idx)
    ok = np.median(lev) - 10  # within 10 dB of the track's usual level counts as audible
    if score(0) >= ok:
        return 0.0
    return float(max(np.arange(0, 20.01, 0.25), key=lambda off: (min(score(off), ok), -off)))


def build_audio(voice, total, events, meta, work: Path, two_pass: bool, below_db: float):
    """Voice + music (one track, or a track per mood with crossfades) at a fixed level under the voice + stings;
    music muted in any music_silent window. Also writes music.wav (music stem) for the level check."""
    v_lufs = integrated_lufs(voice)
    segs = music_segments(events, meta, total)
    lufs_of = {}
    inputs = ["-i", voice]
    fc = [f"[0:a]aresample=48000,aformat=channel_layouts=stereo[v]"]
    for k, (a, b, f) in enumerate(segs):
        if f not in lufs_of:
            lufs_of[f] = integrated_lufs(f, 60)
        gain = v_lufs - below_db - lufs_of[f]
        last = k == len(segs) - 1
        length = (b - a) + (0 if last else MUSIC_XFADE)  # overlap into the next mood = crossfade
        fade_out = f"afade=t=out:st={length - (1.5 if last else MUSIC_XFADE):.2f}:d={1.5 if last else MUSIC_XFADE}"
        fade_in = f"afade=t=in:d={MUSIC_XFADE}," if k else ""
        ms = int(a * 1000)
        off = music_offset(f, a, b, events.get("pauses", []))
        if off:
            print(f"  music: {Path(f).stem} starts {off:.2f}s in (pause falls on an audible part)")
        inputs += ["-stream_loop", "-1", *(["-ss", f"{off:.2f}"] if off else []), "-i", f]
        fc.append(f"[{k + 1}:a]aresample=48000,aformat=channel_layouts=stereo,atrim=0:{length:.3f},"
                  f"volume={gain:.2f}dB,{fade_in}{fade_out},adelay={ms}|{ms}[mu{k}]")
    mute = "+".join(f"between(t,{a:.2f},{b:.2f})" for a, b in events["music_silent"]) or "0"
    fc.append("".join(f"[mu{k}]" for k in range(len(segs)))
              + f"amix=inputs={len(segs)}:duration=longest:normalize=0,volume='if({mute},0,1)':eval=frame,"
                f"asplit=2[m][mstem]")
    if len(segs) > 1:
        print("  music: " + " -> ".join(f"{Path(f).stem}@{a:.0f}s" for a, _, f in segs))
    mix_in, n_in = "[v][m]", len(segs) + 1
    for k, (at, kind) in enumerate(events["sfx"]):
        f = SFX_DIR / meta["sfx"][kind]
        gain = v_lufs - SFX_BELOW_VOICE_DB - integrated_lufs(f)
        inputs += ["-i", f]
        ms = int(at * 1000)
        fc.append(f"[{n_in + k}:a]aresample=48000,aformat=channel_layouts=stereo,volume={gain:.2f}dB,"
                  f"adelay={ms}|{ms}[s{k}]")
        mix_in += f"[s{k}]"
    fc.append(f"{mix_in}amix=inputs={2 + len(events['sfx'])}:duration=first:normalize=0[out]")
    mix = work / "mix.wav"
    run([FFMPEG, "-y", *inputs, "-filter_complex", ";".join(fc), "-map", "[out]", "-t", f"{total:.3f}", mix,
         "-map", "[mstem]", "-t", f"{total:.3f}", work / "music.wav"])
    ln = f"loudnorm=I={TARGET_LUFS}:TP=-1.5:LRA=11"
    if two_pass:
        r = run([FFMPEG, "-hide_banner", "-i", mix, "-af", ln + ":print_format=json", "-f", "null", "-"])
        m = json.loads(r.stderr[r.stderr.rindex("{"):r.stderr.rindex("}") + 1])
        ln += (f":measured_I={m['input_i']}:measured_TP={m['input_tp']}:measured_LRA={m['input_lra']}"
               f":measured_thresh={m['input_thresh']}:offset={m['target_offset']}:linear=true")
    norm = work / "mix_norm.wav"
    run([FFMPEG, "-y", "-i", mix, "-af", ln + ",aresample=48000", "-ar", 48000, norm])
    return norm


# ---------- 5. final-only checks ----------
def loudness_report(out: Path, work: Path, timed):
    """Final loudness + true peak, and music level the RULES way: integrated LUFS of the voice stem vs the music
    stem, both cut to the same speech sections (both stems are pre-loudnorm; loudnorm gain hits both equally)."""
    r = run([FFMPEG, "-hide_banner", "-i", out, "-af", "ebur128=peak=true", "-f", "null", "-"])
    lufs = float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])
    tp = float(re.findall(r"Peak:\s+(-?[\d.]+) dBFS", r.stderr)[-1])
    sel = "+".join(f"between(t,{l['start']:.2f},{l['end']:.2f})" for l in timed if l["speaker"] != "_pause")

    def speech_lufs(f):
        r = run([FFMPEG, "-hide_banner", "-i", f, "-af", f"aresample=48000,aformat=channel_layouts=stereo,"
                 f"aselect='{sel}',asetpts=N/SR/TB,ebur128", "-f", "null", "-"])
        return float(re.findall(r"I:\s+(-?[\d.]+) LUFS", r.stderr)[-1])

    below = speech_lufs(work / "voice.wav") - speech_lufs(work / "music.wav")
    return lufs, tp, below


def frame_check(out: Path, timed, path: Path, work: Path):
    """One frame from the middle of every line, labelled with time + speaker, tiled into one image."""
    tiles = []
    font = ImageFont.truetype("arial.ttf", 22) if Path("C:/Windows/Fonts/arial.ttf").exists() else ImageFont.load_default()
    for i, l in enumerate(timed):
        t = (l["start"] + l["end"]) / 2
        f = work / f"check_{i:02d}.png"
        run([FFMPEG, "-y", "-ss", f"{t:.2f}", "-i", out, "-frames:v", 1, "-vf", "scale=270:-2", f])
        im = Image.open(f).convert("RGB")
        ImageDraw.Draw(im).rectangle((0, 0, 270, 30), fill=(0, 0, 0))
        ImageDraw.Draw(im).text((6, 4), f"{t:5.1f}s {l['speaker']}", fill=(255, 230, 0), font=font)
        tiles.append(im)
    cols = 6
    rows = (len(tiles) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * 270, rows * tiles[0].height))
    for i, im in enumerate(tiles):
        sheet.paste(im, ((i % cols) * 270, (i // cols) * im.height))
    sheet.save(path)


def srt_time(s):
    ms = max(0, int(round(s * 1000)))
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d},{ms % 1000:03d}"


def write_srt(timed, path: Path):
    """Captions file for upload (long videos don't burn captions into the picture)."""
    cues = [c for l in timed if l["words"] for c in caption_chunks(l)]
    path.write_text("\n".join(f"{i}\n{srt_time(a)} --> {srt_time(b)}\n{txt}\n" for i, (a, b, txt) in
                              enumerate(cues, 1)), encoding="utf-8")


def register_row(f: Path):
    """The asset's row in shared/assets_license.csv (RULES section 10). No row -> stop the build."""
    rows = {r["path"]: r for r in csv.DictReader(REGISTER.open(encoding="utf-8", newline=""))}
    rel = Path(f).resolve().relative_to(ROOT).as_posix()
    if rel not in rows:
        sys.exit(f"STOP: {rel} is not in {REGISTER.name} (RULES section 10). Verify its licence and add a row first.")
    return rows[rel]


def check_register(meta):
    """Every music/SFX file this project can use must be registered before anything is built."""
    files = [MUSIC_DIR / f for f in meta.get("music_moods", {}).values()]
    files.append(MUSIC_DIR / meta["music"] if meta.get("music") else MUSIC_DIR / "mystery_bed.wav")
    files += [SFX_DIR / f for f in meta.get("sfx", {}).values()]
    for f in files:
        register_row(f)


def music_credits(meta, events, total):
    """Description credits, taken word for word from the register's attribution_text."""
    used = []
    for _, _, f in music_segments(events, meta, total):
        if f not in used:
            used.append(f)
    credits = []
    for f in used:
        row = register_row(f)
        text = row["attribution_text"].strip()
        if not text and row["license"].upper().startswith("CC BY"):
            sys.exit(f"STOP: {f.name} is {row['license']} but has no attribution_text in {REGISTER.name}.")
        if text:
            credits.append(f"Music: {text}")
    if not credits:
        return meta.get("credits", "")
    return "\n\n".join(credits) + ("\n\nSound effects: freesound.org (CC0)" if meta.get("sfx") else "")


def load_project(name):
    """A video folder with project.json: channels/<key>/stories/<story>/long or .../shorts/short_<NN>_<slug>.
    lines.json, meta.json, shots.json and output/ are in that folder; images/, audio/ and scene_prompts.json are
    at the story level (shared by the long video and its shorts)."""
    pdir = (ROOT / name).resolve()
    if not (pdir / "project.json").exists():
        sys.exit(f"{pdir} has no project.json (expected .../stories/<story>/long or .../shorts/short_XX_<slug>)")
    proj = json.loads((pdir / "project.json").read_text(encoding="utf-8"))
    kind = proj["kind"]
    story = story_of(pdir)
    channel = channel_of(pdir)
    covers = {c: s["id"] for s in json.loads((story / "scene_prompts.json").read_text(encoding="utf-8"))["scenes"]
              for c in s.get("covers", [s["id"]])}
    img_dir = story / "images"
    return {"kind": kind, "name": proj.get("name", pdir.name), "dir": pdir, "story": story, "channel": channel,
            "burn": proj.get("burn_captions", kind == "short"),
            "image_for": lambda sc: img_dir / f"scene_{covers[sc]:02d}.png",
            "audio_dir": story / "audio", "cache_dir": ROOT / "cache" / channel / story.name / pdir.name,
            "out_dir": pdir / "output"}


def plan_report(P, lines, meta):
    """--plan: show where every input comes from and that it exists. Nothing is rendered or paid for."""
    rel = lambda p: Path(p).resolve().relative_to(ROOT).as_posix()
    print(f"[PLAN] {P['kind']} '{P['name']}'  channel={P['channel']}  story={P['story'].name}")
    print(f"  project:  {rel(P['dir'])}\n  output:   {rel(P['out_dir'])}\n  cache:    {rel(P['cache_dir'])}")
    scenes = sorted({l["scene"] for l in lines})
    imgs = sorted({P["image_for"](s) for s in scenes})
    print(f"  images:   {len(imgs)} for {len(scenes)} scenes, all present: {all(p.exists() for p in imgs)}  "
          f"({rel(imgs[0].parent)})")
    cache = P["audio_dir"] / "tts_cache"
    spoken = [l for l in lines if "text" in l]
    miss = [l["speaker"] for l in spoken if not (cache / tts_key(l["text"], l["speaker"])).exists()]
    print(f"  TTS:      {len(spoken) - len(miss)}/{len(spoken)} lines cached in {rel(cache)}"
          + (f"  MISSING (paid): {miss}" if miss else ""))
    music = [MUSIC_DIR / f for f in meta.get("music_moods", {}).values()] or \
            [MUSIC_DIR / meta["music"] if meta.get("music") else MUSIC_DIR / "mystery_bed.wav"]
    sfx = [SFX_DIR / f for f in meta.get("sfx", {}).values()]
    for label, files in (("music", music), ("sfx", sfx)):
        print(f"  {label + ':':9s} {len(files)} files, all present: {all(f.exists() for f in files)}  "
              + ", ".join(rel(f) for f in files))
    print(f"  font:     {rel(FONT)} present: {FONT.exists()}")
    print(f"  register: {rel(REGISTER)} has a row for every music/SFX file (checked)")


# ---------- main ----------
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("case_pos", nargs="?", metavar="case")
    ap.add_argument("--case", dest="case_opt", help="same as the positional case name")
    g = ap.add_mutually_exclusive_group()
    g.add_argument("--preview", action="store_true", help="fast 540x960 check build (default)")
    g.add_argument("--final", action="store_true", help="1080x1920 upload build + checks")
    ap.add_argument("--spend", action="store_true", help="allow paid TTS for uncached lines")
    ap.add_argument("--plan", action="store_true", help="validate only: resolve and check every input path, no render")
    ap.add_argument("--seconds", type=float, help="preview only the first N seconds (quick test render)")
    a = ap.parse_args()
    mode = "final" if a.final else "preview"
    if a.seconds and mode == "final":
        ap.error("--seconds is only for preview test renders")
    t_start = time.perf_counter()

    name = a.case_opt or a.case_pos
    if not name:
        ap.error("project folder required, e.g. channels/dadi-ki-kahaniyan/stories/001_lalchi-halwai/long")
    P = load_project(name)
    os.environ["STORY_CHANNEL"] = P["channel"]  # cost_log rows get this channel
    prof = PROFILES[(P["kind"], mode)]
    case = P["name"]
    lines = json.loads((P["dir"] / "lines.json").read_text(encoding="utf-8"))
    meta = json.loads((P["dir"] / "meta.json").read_text(encoding="utf-8"))
    focus_file = P["dir"] / "shots.json"
    P["focus"] = json.loads(focus_file.read_text(encoding="utf-8")) if focus_file.exists() else {}
    try:
        missing = [s for s in sorted({l["scene"] for l in lines}) if not P["image_for"](s).exists()]
    except KeyError as e:
        sys.exit(f"Scene {e} has no image in scene_prompts.json 'covers'")
    if missing:
        sys.exit(f"Missing scene images: {missing}")
    check_register(meta)
    if a.plan:
        plan_report(P, lines, meta)
        return

    out_dir = P["out_dir"]
    work = out_dir / f"{case}_work"
    audio_dir = P["audio_dir"]
    cache_dir = P["cache_dir"]
    for d in (work, audio_dir / "tts_cache", cache_dir, work / "fonts"):
        d.mkdir(parents=True, exist_ok=True)
    shutil.copy(FONT, work / "fonts" / FONT.name)
    font_family = ImageFont.truetype(str(FONT)).getname()[0]
    spend_before = sum(float(r["cost_inr"]) for r in cost_log._rows())

    print(f"[{P['kind'].upper()} {mode.upper()}] {prof['w']}x{prof['h']} @ {prof['fps']} fps")
    print("1/4 voice")
    check_tts_spend(lines, audio_dir / "tts_cache", a.spend)
    voice, total, timed, events = build_voice(lines, audio_dir, work, run_whisper=(mode == "final"),
                                              end_hold=meta.get("end_hold", END_HOLD), gap_s=meta.get("gap", GAP),
                                              speed=meta.get("speed", 1.0))
    if a.seconds:  # test render: keep the lines that start inside the first N seconds
        total = min(total, a.seconds)
        timed = [l for l in timed if l["start"] < total]
        events = {k: [e for e in v if e[0] < total] for k, v in events.items()}  # music/sfx cues after the cut go too
        case = f"{case}_test{a.seconds:g}s"
    warn = P["kind"] == "short" and not a.seconds and not 45 <= total <= 60
    print(f"  total {total:.1f}s" + ("  WARNING: outside 45-60s" if warn else ""))

    print("2/4 scenes")
    plans = plan_scenes(P, timed, total, prof, font_family, meta.get("final_title", "बताओ, दोषी कौन?"),
                        meta.get("final_title_secs"))
    cached, new = build_video(plans, prof, cache_dir, work)

    print("3/4 audio")
    norm = build_audio(voice, total, events, meta, work, two_pass=(mode == "final"),
                       below_db=MUSIC_BELOW_VOICE_DB[P["kind"]])

    print("4/4 mux (video stream copied, no re-encode)")
    out = out_dir / (f"{case}.mp4" if mode == "final" else f"{case}_preview.mp4")
    run([FFMPEG, "-y", "-i", "video.mp4", "-i", norm, "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-ar", 48000,
         "-shortest", "-movflags", "+faststart", out], cwd=work)
    report = ""
    if not P["burn"] and not a.seconds:
        srt = out.with_suffix(".srt")
        write_srt(timed, srt)
        report += f"\n  captions:    {srt}"

    if mode == "final":
        lufs, tp, below = loudness_report(out, work, timed)
        check = out_dir / f"{case}_framecheck.png"
        frame_check(out, timed, check, work)
        txt = out_dir / f"{case}.txt"
        tags = f"TAGS:\n{', '.join(meta['tags'])}\n\n" if meta.get("tags") else ""
        txt.write_text(
            f"TITLE:\n{meta['title']}\n\nDESCRIPTION:\n{meta['description']}\n\n"
            f"{music_credits(meta, events, total)}\n\n{' '.join(meta['hashtags'])}\n\n{tags}"
            f"PINNED COMMENT (post later):\n{meta['pinned_comment']}\n", encoding="utf-8")
        report += (f"\n  loudness {lufs:.1f} LUFS, true peak {tp:.1f} dBFS, music {below:.1f} LU under voice "
                   f"(stem LUFS over speech)"
                   f"\n  frame check: {check}\n  metadata:    {txt}")

    spent = sum(float(r["cost_inr"]) for r in cost_log._rows()) - spend_before
    print(f"\nDONE [{mode}] {out}  ({total:.1f}s video)"
          f"\n  scenes: {cached} cache se, {new} naye   |   build time {time.perf_counter() - t_start:.0f}s"
          f"   |   is build ka kharcha ₹{spent:.2f}{report}")


if __name__ == "__main__":
    main()
