"""Noor-e-Raah long video render (channel RULES 1, 1b, 1c, 2): timeline from long/lines.json (script cues), images
from long/images.json, smooth eased camera moves (tools/parallax.py, cubic sub-pixel, no shake), Arabic ayat in Amiri
(drawtext, Tanzil text byte-for-byte), all Hindi screen text through libass (speaker-coloured subtitles, cards),
music continuous through the video with a soft swoosh as each ayah comes in (user 2026-10-25), ambience by mood. Free (no paid calls).

    .venv\\Scripts\\python -X utf8 scripts\\noor_render.py <story> [--seconds N] [--plan]

Output: <story>/long/output/<story>_final.mp4 (+ .srt, timeline.json). --seconds N = first N s only (check).
"""
import json
import math
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402

import parallax as PX  # noqa: E402
import edit_fx as FX  # noqa: E402  (Sampadak look: long/edit_plan.json, optional)
import text_pil as TP  # noqa: E402  (Hindi text through Pillow+raqm when libass cannot shape Devanagari)

ROOT = Path(__file__).resolve().parent.parent
FF = next((str(p) for p in (ROOT / "tools/ffmpeg/bin/ffmpeg.exe", ROOT / "tools/ffmpeg/ffmpeg.exe") if p.exists()),
          None) or shutil.which("ffmpeg")  # Linux / cloud: ffmpeg on PATH
W, H, FPS, SR = 1920, 1080, 30, 48000
FONT_AR = ROOT / "shared/fonts/Amiri-Regular.ttf"
FONT_DIR = ROOT / "shared/fonts"
LEAD, SECTION_GAP, GAP_CHANGE, GAP_SAME = 0.8, 0.8, 0.6, 0.35  # first word <= 1.0 s (Munshi final R1)
AMIRI_ASS_K = 4.35  # ASS size / pixel size for Amiri in libass (see arabic_fs)
ARABIC_ALONE, ARABIC_HOLD, ARABIC_FADE = 2.0, 0.3, 0.5
XF, MAX_SHOT = 0.5, 8.0
MOVES = ["push_in", "pan_right", "pull_out", "pan_left", "gentle_orbit", "push_in", "pan_left", "pull_out", "pan_right"]
RECTS = [(0.5, 0.5, 1.0), (0.38, 0.5, 1.15), (0.62, 0.5, 1.15), (0.5, 0.45, 1.25)]  # (fx, fy, zc) per shot on one image
MUSIC = {"Soaring": "shared/music/noor/Soaring.mp3", "Quietude": "shared/music/noor/Quietude_Sections_Merged.mp3",
         "River Flute": "shared/music/noor/River_Flute.mp3"}
SWOOSH = ("shared/sfx/noor/swoosh_mikesmultimedia_349698.mp3", -35.0)  # ~14 LU under the voice as heard in the mix
AYAH_LEAD = 0.6  # from the ayah cue to the Arabic (swoosh starts 0.5 s before it)
AMB = {"breeze": ("shared/sfx/noor/gentle_breeze_mario1298_181252.mp3", -46.0),
       "desert": ("shared/sfx/noor/desert_wind_felixblume_156414.mp3", -46.0),
       "night": ("shared/sfx/noor/night_wind_crickets_felixblume_165526.mp3", -48.0),
       "birds": ("shared/sfx/noor/wind_birds_petebuchwald_288899.mp3", -52.0)}
VOICE_LUFS, MUSIC_BELOW, TARGET_LUFS = -16.0, 20.2, -14.0  # 20.2 here = 19 LU under the voice as heard in the mix
#   (user 2026-10-25 "a bit louder" = 19 LU; the voice chain - stereo + aecho - lands ~1.2 LU lower, Munshi final R1)
TEMPO = 1.08  # voices 8 % faster, same pitch (user 2026-10-25); from the same TTS files, no new TTS
SUB_COLOUR = {"ustaad": "&H00FFFFFF", "sawaal": "&H0080D8F5"}  # white / soft gold (ASS is BGR)
LABEL = "सरल भावार्थ — माने हुए तर्जुमों के आधार पर"
SERIES_DEFAULT, TAGLINE_DEFAULT = "नूर-ए-राह", "क़ुरआन, आसान ज़बान में।"
# Hindi text drawn by Pillow (same look as the libass styles in ass_doc); ASS size / colours converted: ASS alpha 0 = opaque
PIL_STYLES = {
    "Sub_ustaad": dict(size=62, fill=(255, 255, 255), box=(0, 0, 0, 0.55), outline=12),
    "Sub_sawaal": dict(size=62, fill=(245, 216, 128), box=(0, 0, 0, 0.55), outline=12),
    "Card": dict(size=56, fill=(255, 255, 255), box=(8, 20, 38, 0.61), outline=14),
    "Translit": dict(size=52, fill=(240, 225, 170), outline=3, outline_rgba=(0, 0, 0, 0.5), shadow=2, shadow_rgba=(0, 0, 0, 0.7)),
    "Label": dict(size=44, fill=(255, 255, 255), opacity=0.92, shadow=2, shadow_rgba=(0, 0, 0, 0.5)),
    "Big": dict(size=92, fill=(255, 255, 255), outline=3, outline_rgba=(0, 0, 0, 0.44), shadow=2, shadow_rgba=(0, 0, 0, 0.7)),
    "Gold": dict(size=54, fill=(201, 165, 90), outline=2, outline_rgba=(0, 0, 0, 0.44), shadow=1, shadow_rgba=(0, 0, 0, 0.7)),
    "Small": dict(size=34, fill=(255, 255, 255), opacity=0.88, outline=2, outline_rgba=(0, 0, 0, 0.44), shadow=1,
                  shadow_rgba=(0, 0, 0, 0.7)),
}
TRANSLIT_Y, LABEL_Y_TR, TRANSLIT_BAND_BOTTOM = 480, 640, 700  # layout when a story has "ucharan" lines
CFG = {}  # per-story screen config, set by load_cfg(story) (long/render.json); see render_cfg_help below


def load_cfg(story: Path) -> dict:
    """long/render.json: {"title_ar", "title_hi", "series", "tagline", "end_from": <line n where the end card starts>,
    "cards": [{"line": n, "until": m, "y": 120, "stack": false, "items": ["..."]}]}.  Missing keys fall back to
    thumbnail.json (arabic/hindi), SERIES_DEFAULT/TAGLINE_DEFAULT, no cards, end card on the last two lines.
    Story 001 keeps its own render.json (its old hard-coded values)."""
    f = story / "long/render.json"
    cfg = json.loads(f.read_text(encoding="utf-8")) if f.exists() else {}
    th = story / "thumbnail.json"
    if th.exists():
        t = json.loads(th.read_text(encoding="utf-8"))
        cfg.setdefault("title_ar", t.get("arabic", ""))
        cfg.setdefault("title_hi", t.get("hindi", ""))
    cfg.setdefault("series", SERIES_DEFAULT)
    cfg.setdefault("tagline", TAGLINE_DEFAULT)
    cfg.setdefault("cards", [])
    return cfg


def run(args, **kw):
    return subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *args], check=True, **kw)


def esc(p: Path) -> str:
    return Path(p).resolve().as_posix().replace(":", "\\:")


def lufs_file(path) -> float:
    err = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=framelog=quiet", "-f", "null",
                          "-"], capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", err)[-1])


def decode(path, start=0.0, dur=None, ch=2, af=None) -> np.ndarray:
    """Audio as float32 (n, ch) at 48 kHz (af: optional ffmpeg audio filter, e.g. atempo)."""
    args = [FF, "-v", "error", "-ss", f"{start:.3f}", "-i", str(path)] + (["-t", f"{dur:.3f}"] if dur else []) + \
           (["-af", af] if af else []) + ["-f", "f32le", "-ac", str(ch), "-ar", str(SR), "-"]
    raw = subprocess.run(args, capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, ch).copy()


def write_wav(path, x: np.ndarray):
    x = np.clip(x, -1, 1)
    with wave.open(str(path), "wb") as w:
        w.setnchannels(x.shape[1]), w.setsampwidth(2), w.setframerate(SR)
        w.writeframes((x * 32767).astype(np.int16).tobytes())


# ---------------------------------------------------------------- timeline
def track_of(value):
    return next((k for k in MUSIC if k.lower() in value.lower()), None)


def timeline(items):
    t, prev, first_section = LEAD, None, True
    lines, ayat, music, amb = [], [], [], []
    cur_music, cur_amb, arabic = None, None, None
    fade_at = {}

    def music_to(track, at, fin):
        nonlocal cur_music
        if cur_music and cur_music["track"] == track and cur_music["end"] is None:
            return  # the same track is already playing: it just goes on (Munshi carry-over, lines 23/88)
        if cur_music and cur_music["end"] is None:
            cur_music["end"], cur_music["fout"] = at + 1.5, 1.5
        cur_music = {"track": track, "start": at, "fin": fin, "end": None, "fout": 0.0}
        music.append(cur_music)

    def music_off(at, fade):
        nonlocal cur_music
        if cur_music and cur_music["end"] is None:
            cur_music["end"], cur_music["fout"] = at + fade, fade
        cur_music = None

    def amb_to(names, at):
        nonlocal cur_amb
        if cur_amb and cur_amb["names"] == names:
            return
        if cur_amb:
            cur_amb["end"] = at + 1.0
        cur_amb = {"names": names, "start": at, "end": None}
        amb.append(cur_amb)

    amb_to(["breeze"], 0.0)
    for it in items:
        k = it["kind"]
        if k == "section":
            if it["name"].upper().startswith("HEADER"):
                continue
            if not first_section:
                t += SECTION_GAP
            first_section = False
        elif k == "cue" and it["type"] == "music":
            v = it["value"]
            if ("fade-out" in v or v.lower().startswith("swoosh")) and "ARABIC" in v:  # swoosh = the new cue name
                # user 2026-10-25: the music no longer stops for an ayah - it plays on; a soft swoosh brings the Arabic in
                arabic = {"ayah": it["ayah"], "fade": t, "a0": t + AYAH_LEAD, "swoosh": t + AYAH_LEAD - 0.5}
                fade_at[it["ayah"]] = t
                t = arabic["a0"] + ARABIC_ALONE
            elif v.lower().startswith(("back slowly", "continue")):  # "continue: <track>" = the music plays on
                if arabic:
                    arabic["off"] = t + ARABIC_HOLD + ARABIC_FADE
                    ayat.append(arabic)
                    t = arabic["off"]
                    arabic = None
                music_to(track_of(v), t, 2.5)
            elif "fade-out" in v:  # the end: music out, ~3 s breeze only
                music_off(t, 3.0)
                t += 3.5
            elif track_of(v):
                music_to(track_of(v), t, 1.5)
        elif k == "cue" and it["type"] == "ambience":
            v = it["value"].lower()
            names = (["desert", "night"] if "desert" in v else ["birds", "breeze"] if "birds" in v else ["breeze"])
            amb_to(names, t)
        elif k == "arabic":
            arabic["text"] = it["text"]
        elif k == "line":
            if prev:
                t += GAP_CHANGE if it["speaker"] != prev else GAP_SAME
            sec = it["seconds"] / TEMPO
            lines.append({**it, "start": round(t, 3), "end": round(t + sec, 3)})
            t += sec
            prev = it["speaker"]
    end = t + 0.5
    music_off(end, 0.5)
    if cur_amb:
        cur_amb["end"] = end
    return {"lines": lines, "ayat": ayat, "music": music, "amb": amb, "end": round(end, 3), "fade_at": fade_at}


def shots_for(story, tl):
    plan = json.loads((story / "long/images.json").read_text(encoding="utf-8"))["images"]
    starts = {l["n"]: l["start"] for l in tl["lines"]}
    anchors = []
    for i, im in enumerate(plan):
        st = im["start"]
        t0 = 0.0 if i == 0 else (tl["fade_at"][st["ayah"]] if "ayah" in st else starts[st["line"]] - 0.3)
        f = story / "images" / f"{im.get('reuse_id', im['id'])}.png"
        anchors.append((t0, f, im["id"], im.get("rect")))
    anchors.sort()
    shots, k = [], 0
    for i, (t0, f, iid, rect) in enumerate(anchors):
        t1 = anchors[i + 1][0] if i + 1 < len(anchors) else tl["end"]
        parts = max(1, math.ceil((t1 - t0) / MAX_SHOT))
        for j in range(parts):
            a, b = t0 + j * (t1 - t0) / parts, t0 + (j + 1) * (t1 - t0) / parts
            # a fixed window (images.json "rect", e.g. to keep a flaw out) holds for every shot of that image
            fx, fy, zc = (rect["fx"], rect["fy"], rect["zc"]) if rect else RECTS[j % len(RECTS)]
            shots.append({"img": f, "id": iid, "start": round(a, 3), "end": round(b, 3), "move": MOVES[k % len(MOVES)],
                          "fx": fx, "fy": fy, "zc": zc})
            k += 1
    return shots


# ---------------------------------------------------------------- audio
def build_audio(story, tl, out_dir, seconds):
    total = int(round(min(tl["end"], seconds) * SR))
    voice = np.zeros((total, 1), np.float32)
    for l in tl["lines"]:
        a = int(l["start"] * SR)
        if a >= total:
            break
        x = decode(story / l["audio"], ch=1, af=f"atempo={TEMPO}")
        voice[a:a + len(x)] += x[: max(0, total - a)]
    vfile = out_dir / "_voice.wav"
    write_wav(vfile, voice)

    music = np.zeros((total, 2), np.float32)
    cursor = {}
    for seg in tl["music"]:
        a, b = int(seg["start"] * SR), int(min(seg["end"], tl["end"]) * SR)
        if a >= total:
            continue
        n = b - a
        off = cursor.get(seg["track"], 20.0 if seg["track"] == "Soaring" else 30.0)
        x = decode(ROOT / MUSIC[seg["track"]], off, n / SR + 0.1)[:n]
        cursor[seg["track"]] = off + n / SR
        gain = 10 ** ((VOICE_LUFS - MUSIC_BELOW - lufs_of(x)) / 20)
        env = np.ones(len(x), np.float32)
        fi, fo = int(seg["fin"] * SR), int(seg["fout"] * SR)
        if fi:
            env[:fi] = 0.5 - 0.5 * np.cos(np.pi * np.arange(min(fi, len(env))) / fi)
        if fo:
            env[-fo:] *= 0.5 + 0.5 * np.cos(np.pi * np.arange(fo) / fo)
        m = x * env[:, None] * gain
        e = min(total, a + len(m))
        music[a:e] += m[: e - a]
    mfile = out_dir / "_music.wav"
    write_wav(mfile, music)

    amb = np.zeros((total, 2), np.float32)
    for seg in tl["amb"]:
        a, b = int(seg["start"] * SR), int(min(seg["end"], tl["end"]) * SR)
        if a >= total:
            continue
        n = min(b, total) - a
        for name in seg["names"]:
            path, target = AMB[name]
            src = decode(ROOT / path, 3.0)
            reps = int(np.ceil(n / len(src))) + 1
            x = np.concatenate([src] * reps)[:n]
            g = 10 ** ((target - lufs_of(src)) / 20)
            env = np.ones(n, np.float32)
            r = min(int(1.0 * SR), n // 2)
            env[:r] = np.linspace(0, 1, r)
            env[-r:] *= np.linspace(1, 0, r)
            amb[a:a + n] += x * env[:, None] * g
    sw = decode(ROOT / SWOOSH[0])
    sw_gain = 10 ** ((SWOOSH[1] - lufs_of(sw)) / 20)
    for ay in tl["ayat"]:  # soft swoosh as each ayah comes in (not ducked: there is no voice at that moment)
        a = int(ay["swoosh"] * SR)
        if a < total:
            e = min(total, a + len(sw))
            amb[a:e] += sw[: e - a] * sw_gain
    afile = out_dir / "_amb.wav"
    write_wav(afile, amb)

    v_gain = VOICE_LUFS - lufs_file(vfile)
    mix = out_dir / "_mix.wav"
    fc = (f"[0]aformat=channel_layouts=stereo,volume={v_gain:.2f}dB,aecho=0.8:0.7:40|75:0.10|0.06,asplit=2[v][vk];"
          "[1][vk]sidechaincompress=threshold=0.03:ratio=3:attack=20:release=400[m];"
          "[v][m][2]amix=inputs=3:normalize=0[o]")
    run(["-i", str(vfile), "-i", str(mfile), "-i", str(afile), "-filter_complex", fc, "-map", "[o]", "-ar", str(SR), str(mix)])
    final = out_dir / "_audio_final.wav"  # limit 0.77 (-2.3 dB): true peak after AAC stayed -0.7 dBFS with 0.84 on story 002
    g = TARGET_LUFS - lufs_file(mix)
    run(["-i", str(mix), "-af", f"volume={g:.2f}dB,alimiter=limit=0.77:level=false", "-ar", str(SR), str(final)])
    return final


def lufs_of(x: np.ndarray) -> float:
    tmp = ROOT / "cache" / "_lufs_tmp.wav"
    tmp.parent.mkdir(exist_ok=True)
    write_wav(tmp, x if x.ndim == 2 else x[:, None])
    return lufs_file(tmp)


# ---------------------------------------------------------------- text
def ts(t):
    t = max(t, 0.0)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def use_pillow() -> bool:
    """Hindi engine: render.json "hindi_engine" = pillow | libass; auto = Pillow where libraqm exists (the cloud), libass on the PC."""
    e = CFG.get("hindi_engine", "auto")
    return e == "pillow" or (e == "auto" and TP.available())


def ass_doc(tl, pil=False):
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, "
            "Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, "
            "MarginL, MarginR, MarginV, Encoding\n")
    styles = [f"Style: Sub_{who},Mukta Bold,62,{col},&H00FFFFFF,&H73000000,&H73000000,0,0,0,0,100,100,0,0,3,12,0,2,160,160,70,1"
              for who, col in SUB_COLOUR.items()]
    styles += ["Style: Card,Mukta Bold,56,&H00FFFFFF,&H00FFFFFF,&H64261408,&H64261408,0,0,0,0,100,100,0,0,3,14,0,7,0,0,0,1",
               "Style: Label,Mukta Bold,44,&H14FFFFFF,&H00FFFFFF,&H80000000,&H80000000,0,0,0,0,100,100,0,0,1,0,2,8,0,0,0,1",
               "Style: Big,Mukta Bold,92,&H00FFFFFF,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,3,2,8,0,0,0,1",
               "Style: Gold,Mukta Bold,54,&H005AA5C9,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,2,1,8,0,0,0,1",
               "Style: Small,Mukta Bold,34,&H20FFFFFF,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,2,1,8,0,0,0,1",
               # Arabic through libass too: ffmpeg drawtext put the harakat off their letters (Munshi final R1 BLOCKER)
               "Style: Ayah,Amiri,140,&H00FFFFFF,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,0,3,8,0,0,0,0",
               "Style: ArTitle,Amiri,400,&H00B8E3F3,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,0,4,8,0,0,0,0"]
    if any(l["role"] == "ucharan" for l in tl["lines"]):  # only stories with ucharan lines (001 keeps its exact ASS)
        styles.append("Style: Translit,Mukta Bold,52,&H00AAE1F0,&H00FFFFFF,&H80000000,&H80000000,0,0,0,0,100,100,0,0,1,3,2,8,0,0,0,1")
    ev = []
    tl["hindi"] = []

    def H(layer, a, b, style, text, prefix="", pos=None, an=None, fad=None):
        """One Hindi event: an ASS line (libass mode) or an entry of tl["hindi"] (Pillow mode)."""
        if pil:
            tl["hindi"].append({"start": a, "end": b, "style": style, "text": text, "pos": pos, "an": an, "fad": fad})
        else:
            ev.append(f"Dialogue: {layer},{ts(a)},{ts(b)},{style},,0,0,0,,{prefix}{text}")

    lines = tl["lines"]
    first_end = lines[1]["end"] if len(lines) > 1 else lines[0]["end"]
    end_from = CFG.get("end_from") or (lines[-2]["n"] if len(lines) > 1 else lines[0]["n"])
    ar_fs = title_fs(CFG["title_ar"])
    ev.append(f"Dialogue: 2,{ts(0.2)},{ts(first_end)},ArTitle,,0,0,0,,{{\\pos(960,110)\\fs{ar_fs}\\fad(400,400)}}{CFG['title_ar']}")
    for ay in tl["ayat"]:  # Tanzil text bytes unchanged (a long ayah is only split at spaces, never edited)
        # the "सरल भावार्थ" label sits at y 470 while a bhaavarth line is spoken: the ayah ink must stay above it then
        with_label = any(l["role"] == "bhaavarth" and l["start"] < ay["off"] and l["end"] + ARABIC_HOLD > ay["a0"] for l in lines)
        # "ucharan" lines (user 2026-10-30): the Arabic words in Devanagari, read plainly by the Ustaad (not tilawat), written
        # under the Arabic while it is on screen; the bhaavarth label then moves lower (LABEL_Y_TR)
        ay["translit"] = [l for l in lines if l["role"] == "ucharan" and ay["a0"] <= l["start"] < ay["off"]]
        parts, band = ayah_lines(ay["text"], 450 if (with_label or ay["translit"]) else 760)
        if ay["translit"]:
            band = (band[0] if band else 194, max(band[1] if band else 0, TRANSLIT_BAND_BOTTOM))
        ay["band"] = band
        for ln, fs, y in parts:
            ev.append(f"Dialogue: 2,{ts(ay['a0'])},{ts(ay['off'])},Ayah,,0,0,0,,"
                      f"{{\\pos(960,{y})\\fs{fs}\\fad(500,{int(ARABIC_FADE * 1000)})}}{ln}")
    H(1, 0.2, first_end, "Big", CFG["title_hi"], "{\\pos(960,560)\\fad(400,400)}", (960, 560), 8, (400, 400))
    H(1, 0.2, first_end, "Gold", CFG["series"], "{\\pos(960,690)\\fad(400,400)}", (960, 690), 8, (400, 400))
    tr_mode = any(l["role"] == "ucharan" for l in lines)
    for ay in tl["ayat"]:
        for l in ay["translit"]:
            H(1, l["start"], ay["off"], "Translit", l["text"], f"{{\\pos(960,{TRANSLIT_Y})\\fad(250,300)}}",
              (960, TRANSLIT_Y), 8, (250, 300))
    for l in lines:
        top = "{\\an8\\pos(960,150)}" if l["n"] >= end_from else ""  # last lines above the end-screen area
        if l["role"] == "ucharan":
            continue  # shown under the Arabic (Translit), not as a bottom subtitle
        H(0, l["start"], l["end"], f"Sub_{l['speaker']}", l["text"], top,
          (960, 150) if l["n"] >= end_from else (960, 1010), 8 if l["n"] >= end_from else 2, None)
        if l["role"] == "bhaavarth":
            ly = LABEL_Y_TR if tr_mode else 470
            H(1, l["start"], l["end"] + ARABIC_HOLD, "Label", LABEL, f"{{\\pos(960,{ly})\\fad(250,250)}}", (960, ly), 8, (250, 250))
    by_n = {l["n"]: l for l in lines}
    for card in CFG["cards"]:
        n = card["line"]
        if n not in by_n:
            continue
        l = by_n[n]
        end = by_n[card["until"]]["end"] if card.get("until") in by_n else l["end"]
        for i, c in enumerate(card["items"]):
            y = card.get("y", 120) + (i * 110 if card.get("stack") else 0)
            H(1, l["start"] + i * 0.7, end, "Card", c, f"{{\\pos(110,{y})\\fad(250,200)}}", (110, y), 7, (250, 200))
    # end card (the last lines + tail)
    if end_from in by_n:
        a = by_n[end_from]["start"]
        H(1, a, tl["end"], "Big", CFG["tagline"], "{\\pos(960,330)\\fad(500,600)}", (960, 330), 8, (500, 600))
        H(1, a, tl["end"], "Gold", CFG["series"], "{\\pos(960,460)\\fad(500,600)}", (960, 460), 8, (500, 600))
        H(1, a, tl["end"], "Small", f"Arabic text: Tanzil Project, tanzil.net  ·  {LABEL}",
          "{\\pos(960,560)\\fad(500,600)}", (960, 560), 8, (500, 600))
    return head + "\n".join(styles) + "\n\n[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, " \
                                      "Effect, Text\n" + "\n".join(ev) + "\n"


def title_fs(text: str) -> int:
    """ASS size of the big Arabic title: the old Al-Fatiha size (400), smaller when the name is wider than ~1300 px."""
    w = amiri_px(92).getlength(text)
    return int(400 * min(1.0, 1300 / w)) if w else 400


def amiri_px(size: int):
    """Amiri for measuring text width: the BASIC layout engine on purpose. Every constant here (AMIRI_ASS_K, the 1700 px
    limit) was calibrated on the PC, whose Pillow has no libraqm; the cloud's Pillow (RAQM) would measure ~1.5x too narrow."""
    from PIL import ImageFont
    return ImageFont.truetype(str(FONT_AR), size, layout_engine=ImageFont.Layout.BASIC)


LIBASS_WIDER = 1.11  # libass draws Amiri ~11 % wider than the BASIC measure (measured 2026-10-30, em 40-52)


def ayah_lines(text: str, end_y: int):
    """Layout of an ayah block. Returns [(line text, ASS size, \\pos y)] and the dark band (top, bottom) in px.
    A short ayah stays ONE line exactly as before (arabic_fs, pos y 165). A long one (the 50-word Ayatul Kursi) is wrapped by
    us, line by line, in a smaller size: libass's own wrapping/line spacing for Amiri is far too loose (4 lines at the old
    size ran into the subtitles, Sampadak 2026-10-30). Measured in libass: a line's ink starts 1.0 em below its \\pos y and is
    ~2.7 em high, so lines are 2.6 em apart; the whole block's ink must end above end_y."""
    for size in (78, 72, 64, 58):
        if amiri_px(size).getlength(text) <= 1700:
            return [(text, int(size * AMIRI_ASS_K), 165)], None
    words = text.split(" ")
    limit = 1700 / LIBASS_WIDER
    for em in (60, 56, 52, 48, 44, 40, 36):
        f = amiri_px(em)
        lines, cur = [], ""
        for w in words:
            t = (cur + " " + w).strip()
            if cur and f.getlength(t) > limit:
                lines.append(cur)
                cur = w
            else:
                cur = t
        lines.append(cur)
        pitch = 2.6 * em
        ink0 = 235  # top of the first line's ink (inside the dark band that starts at 194)
        bottom = ink0 + (len(lines) - 1) * pitch + 2.7 * em
        if bottom <= end_y or em == 36:
            fs = int(em * AMIRI_ASS_K)
            return [(ln, fs, int(ink0 + i * pitch - 1.0 * em)) for i, ln in enumerate(lines)], (194, int(bottom + 30))
    raise AssertionError("unreachable")


def arabic_fs(text: str) -> int:
    """ASS font size for an ayah so it fits ~1700 px: libass draws Amiri AMIRI_ASS_K times smaller than its pixel size
    (measured: same text 1183 px wide at 100 px vs 272 px at ASS size 100 - Amiri's very tall line metrics)."""
    for size in (78, 72, 64, 58):  # capped: a short ayah at 96 reached the label line
        if amiri_px(size).getlength(text) <= 1700:
            return int(size * AMIRI_ASS_K)
    return int(52 * AMIRI_ASS_K)


def video_filter(tl, out_dir, ass: Path, pil=False):
    f = []
    for ay in ([] if pil else tl["ayat"]):  # dark band behind the Arabic (the Arabic itself is drawn by libass from the ASS file)
        y0, y1 = ay.get("band") or (None, None)  # a multi-line ayah (ayah_lines) needs a taller dark band
        box = f"y={y0}:h={y1 - y0}" if y0 is not None else "y=ih*0.18:h=ih*0.33"
        f.append(f"drawbox=x=0:{box}:w=iw:color=black@0.30:t=fill:"
                 f"enable='between(t,{ay['a0']:.2f},{ay['off']:.2f})'")
    f.append(f"subtitles=filename='{esc(ass)}':fontsdir='{esc(FONT_DIR)}'")
    f.append("scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setsar=1,"
             "setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709")
    return ",".join(f)


# ---------------------------------------------------------------- frames
_SRC = {}


def source(img: Path, fx, fy, zc):
    key = (str(img), fx, fy, zc)
    if key not in _SRC:
        im = cv2.imread(str(img))
        ih, iw = im.shape[:2]
        x0, y0, w, h = PX.shot_rect(iw, ih, W / H, 0.5, 0.5, fx, fy, zc)
        crop = im[int(round(y0)):int(round(y0 + h)), int(round(x0)):int(round(x0 + w))]
        _SRC.clear() if len(_SRC) > 12 else None
        _SRC[key] = cv2.resize(crop, (int(round(W * PX.OVERSCAN)), int(round(H * PX.OVERSCAN))),
                               interpolation=cv2.INTER_LANCZOS4)
    return _SRC[key]


def shot_frame(s, t):
    a, b = s["start"] - XF / 2, s["end"] + XF / 2
    p = min(1.0, max(0.0, (t - a) / (b - a)))
    z, dx, dy = PX.motion(s["move"], p, PX.AMP)
    return PX._warp(source(s["img"], s["fx"], s["fy"], s["zc"]), 1 + z, dx, dy, W, H)


def frames(shots, n_frames):
    k = 0
    for i in range(n_frames):
        t = i / FPS
        while k + 1 < len(shots) and t >= shots[k]["end"] + XF / 2:
            k += 1
        s = shots[k]
        fr = shot_frame(s, t)
        if k + 1 < len(shots) and t >= s["end"] - XF / 2:  # crossfade into the next shot
            w = (t - (s["end"] - XF / 2)) / XF
            fr = cv2.addWeighted(fr, 1 - w, shot_frame(shots[k + 1], t), w, 0)
        yield fr


class HindiOverlay:
    """Pillow mode: dark band behind a multi-line ayah (was ffmpeg drawbox) + Hindi sprites with fades, drawn on the frame
    before ffmpeg lets libass draw the Arabic on top. Sprites are rendered once per event and dropped after it ends."""

    def __init__(self, tl):
        self.ev = sorted(tl["hindi"], key=lambda e: (e["start"], e["end"]))
        self.bands = [(ay["a0"], ay["off"], *(ay.get("band") or (int(H * 0.18), int(H * 0.18) + int(H * 0.33)))) for ay in tl["ayat"]]
        self.cache = {}

    def sprite(self, k, e):
        if k not in self.cache:
            st = PIL_STYLES[e["style"]]
            sub = e["style"].startswith("Sub_")
            spr = TP.render(e["text"], st, maxw=1600 if sub else 1700, max_lines=2 if sub else None)
            h, w = spr.shape[:2]
            x, y = e["pos"]
            x = x - w // 2 if e["an"] in (8, 2) else x  # an 8 / 2 = centred on x, an 7 = left edge at x
            y = y - h if e["an"] == 2 else y  # an 2 = bottom edge at y
            self.cache[k] = (spr, int(x), int(y))
        return self.cache[k]

    def apply(self, fr, t):
        for a, b, y0, y1 in self.bands:
            if a <= t < b:
                fr[y0:y1] = (fr[y0:y1] * 0.70).astype(np.uint8)  # black @ 0.30
        for k, e in enumerate(self.ev):
            if e["start"] <= t < e["end"]:
                f = 1.0
                if e["fad"]:
                    f = min(1.0, (t - e["start"]) / (e["fad"][0] / 1000) if e["fad"][0] else 1.0,
                            (e["end"] - t) / (e["fad"][1] / 1000) if e["fad"][1] else 1.0)
                spr, x, y = self.sprite(k, e)
                TP.blend(fr, spr, x, y, f)
            elif t >= e["end"]:
                self.cache.pop(k, None)
        return fr


# ---------------------------------------------------------------- main
def srt(tl, path):
    def st(t):
        return f"{int(t // 3600):02d}:{int(t % 3600 // 60):02d}:{int(t % 60):02d},{int(t * 1000 % 1000):03d}"
    rows = [f"{i}\n{st(l['start'])} --> {st(l['end'])}\n{l['text']}\n" for i, l in enumerate(tl["lines"], 1)]
    path.write_text("\n".join(rows), encoding="utf-8")


def main():
    story = Path(sys.argv[1]) if Path(sys.argv[1]).is_absolute() else (ROOT / sys.argv[1]).resolve()
    seconds = float(sys.argv[sys.argv.index("--seconds") + 1]) if "--seconds" in sys.argv else 1e9
    from paths import learnings_brief
    print("learnings.md (Nigraan) LAGU KARO:\n  " + (learnings_brief(story.parents[1].name).replace("\n", "\n  ") or "-"))
    items = json.loads((story / "long/lines.json").read_text(encoding="utf-8"))
    CFG.update(load_cfg(story))
    tl = timeline(items)
    shots = shots_for(story, tl)
    out_dir = story / "long/output"
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "timeline.json").write_text(json.dumps({**tl, "shots": [{**s, "img": s["img"].name} for s in shots]},
                                                      ensure_ascii=False, indent=1), encoding="utf-8")
    lens = [s["end"] - s["start"] for s in shots]
    print(f"length {tl['end']:.1f}s ({int(tl['end'] // 60)}:{tl['end'] % 60:04.1f}), lines {len(tl['lines'])}, ayat {len(tl['ayat'])}, "
          f"shots {len(shots)} ({min(lens):.1f}-{max(lens):.1f}s), music segments {len(tl['music'])}, ambience {len(tl['amb'])}")
    missing = sorted({s["img"].name for s in shots if not s["img"].exists() and s["start"] < seconds})
    if missing:
        sys.exit(f"missing images: {missing}")
    if "--plan" in sys.argv:
        return
    dur = min(tl["end"], seconds)
    audio = build_audio(story, tl, out_dir, dur)
    ass = out_dir / "_text.ass"
    pil = use_pillow()
    ass.write_text(ass_doc(tl, pil), encoding="utf-8")
    overlay = HindiOverlay(tl) if pil else None
    print(f"Hindi text engine: {'Pillow+raqm' if pil else 'libass'}")
    srt(tl, out_dir / f"{story.name}.srt")
    out = out_dir / (f"{story.name}_final.mp4" if dur == tl["end"] else f"{story.name}_check_{int(dur)}s.mp4")
    part = out.with_suffix(".part.mp4")
    n = int(round(dur * FPS))
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS),
                            "-i", "-", "-i", str(audio), "-vf", video_filter(tl, out_dir, ass, pil), "-frames:v", str(n),
                            "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                            "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
                            "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}", "-movflags", "+faststart", str(part)],
                           stdin=subprocess.PIPE)
    plan = None if "--no-edit" in sys.argv else FX.load(story / "long/edit_plan.json")
    fin = FX.Finisher(FX.look_only(plan), W, H, FPS) if plan else None  # colour look only; before libass draws the text
    if plan:
        print(f"edit_plan: look {plan.get('grade', 'none')}, vignette {plan.get('vignette', 0)}, grain {plan.get('grain', 0)}")
    for i, fr in enumerate(frames(shots, n)):
        fr = fin.apply(fr, i) if fin else fr
        if overlay:
            fr = overlay.apply(np.ascontiguousarray(fr).copy() if not fr.flags.writeable else fr, i / FPS)
        enc.stdin.write(fr.tobytes())
        if i % 900 == 0:
            print(f"  frame {i}/{n}", flush=True)
    enc.stdin.close()
    if enc.wait():
        sys.exit("ffmpeg failed")
    part.replace(out)  # the final name appears only when the file is complete and playable
    print(f"OK {out.relative_to(ROOT).as_posix()}  {dur:.1f}s  {lufs_file(out):.1f} LUFS")


if __name__ == "__main__":
    main()
