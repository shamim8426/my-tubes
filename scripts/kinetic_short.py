"""Kinetic-text Short renderer (v0, "Claude explainer" channel). Free: Pillow frames + ffmpeg; only the TTS step costs money.

    .venv\\Scripts\\python -X utf8 scripts\\kinetic_short.py <story_dir> --tts          # voice per beat (free key first, paid fallback)
    .venv\\Scripts\\python -X utf8 scripts\\kinetic_short.py <story_dir> --still 3,12    # PNG stills at those seconds (layout check, no TTS)
    .venv\\Scripts\\python -X utf8 scripts\\kinetic_short.py <story_dir> --render [--seconds N]

Spec: <story_dir>/short.json = {"palette", "seed", "voice": {"id", "style"}, "beats": [{"layout", "voice", "lines", "label", "chip",
"chip2", "sub", "badge"}]}.  "*word*" in a line = emphasis (accent colour, heavier weight).  Layouts: HOOK_BIG, CODE_CHIP, STEP, NOTE, CTA.
Output: <story_dir>/short/output/short.mp4 (1080x1920, 30 fps, -14 LUFS).  Nothing here is copied from another creator: the look
(palettes, layouts, motion) follows channels/_new_claude_explainer/STYLE_GUIDE.md.
"""
import argparse
import json
import math
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
FF = next((str(p) for p in (ROOT / "tools/ffmpeg/ffmpeg.exe", ROOT / "tools/ffmpeg/bin/ffmpeg.exe") if p.exists()), None) \
    or shutil.which("ffmpeg")
W, H, FPS, SR = 1080, 1920, 30, 24000
LEAD, GAP, TAIL = 0.35, 0.30, 1.2
SAFE_X = (70, 1010)
FONTS = ROOT / "shared/fonts"
F_HEAD, F_BOLD, F_MONO = FONTS / "Mukta-ExtraBold.ttf", FONTS / "Mukta-Bold.ttf", FONTS / "IBMPlexMono-Bold.ttf"
MUSIC = ROOT / "shared/music/noor/Soaring.mp3"
SWOOSH = ROOT / "shared/sfx/noor/swoosh_mikesmultimedia_349698.mp3"

PALETTES = {
    "dark_terminal": dict(bg1=(11, 16, 27), bg2=(24, 33, 54), text=(240, 244, 250), dim=(150, 163, 184), accent=(255, 183, 3),
                          accent2=(46, 196, 182), card=(30, 41, 64), dot=(58, 72, 104)),
    "warm_cream": dict(bg1=(251, 244, 231), bg2=(240, 227, 204), text=(38, 33, 28), dim=(125, 112, 95), accent=(212, 84, 38),
                       accent2=(30, 118, 108), card=(255, 253, 247), dot=(214, 198, 170)),
    "ink_blue": dict(bg1=(20, 30, 90), bg2=(34, 52, 150), text=(246, 248, 255), dim=(182, 196, 240), accent=(255, 214, 64),
                     accent2=(120, 230, 200), card=(40, 58, 160), dot=(90, 112, 210)),
}


# ---------------------------------------------------------------- helpers
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(p):
    return 1 - (1 - p) ** 3


def ease_back(p):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


_font_cache = {}


def font(path, size):
    k = (str(path), int(size))
    if k not in _font_cache:
        _font_cache[k] = ImageFont.truetype(str(path), int(size), layout_engine=ImageFont.Layout.BASIC)
    return _font_cache[k]


def parse_line(line):
    """'a *b* c' -> [('a', False), ('b', True), ('c', False)]  (words, emphasis flag)."""
    out, emph = [], False
    for part in line.split("*"):
        out += [(w, emph) for w in part.split() if w]
        emph = not emph
    return out


def sprite_text(text, fpath, size, rgb, pad=4):
    f = font(fpath, size)
    l, t, r, b = f.getbbox(text)
    img = Image.new("RGBA", (r - l + 2 * pad, int(size * 1.35) + 2 * pad), (0, 0, 0, 0))
    ImageDraw.Draw(img).text((pad - l, pad), text, font=f, fill=(*rgb, 255))
    return img


class El:
    """One animated element: pre-rendered RGBA sprite placed at (x, y) (top-left), appears at t0 (beat-local seconds)."""

    def __init__(self, sprite, x, y, t0, anim="rise", dur=0.38):
        self.rgb, self.alpha = sprite.convert("RGB"), sprite.getchannel("A")
        self.x, self.y, self.t0, self.anim, self.dur = x, y, t0, anim, dur


def rounded(size, fill, radius, outline=None, width=0):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=(*fill, 255),
                                          outline=(*outline, 255) if outline else None, width=width)
    return img


def fit_size(text, fpath, start, max_w):
    s = start
    while s > 28 and font(fpath, s).getlength(text) > max_w:
        s -= 4
    return s


def text_line_els(line, pal, size, y, t0, stagger=0.07, centre_x=W // 2, max_w=SAFE_X[1] - SAFE_X[0], wfont=F_BOLD, efont=F_HEAD):
    """Words of one line, centred, revealed word by word. Returns (elements, line height)."""
    words = parse_line(line)
    plain = " ".join(w for w, _ in words)
    size = fit_size(plain, efont, size, max_w)
    space = font(wfont, size).getlength(" ")
    widths = [font(efont if e else wfont, size).getlength(w) for w, e in words]
    total = sum(widths) + space * (len(words) - 1)
    x = centre_x - total / 2
    els = []
    for i, ((w, e), wd) in enumerate(zip(words, widths)):
        sp = sprite_text(w, efont if e else wfont, size, pal["accent"] if e else pal["text"])
        els.append(El(sp, x - 4, y, t0 + i * stagger, "rise", 0.30))
        x += wd + space
    return els, int(size * 1.3)


def lines_block(lines, pal, size, y, t0, gap=18, **kw):
    # one common size for the whole block (the longest line decides), so lines never differ in size
    max_w = kw.get("max_w", SAFE_X[1] - SAFE_X[0])
    size = min(fit_size(" ".join(w for w, _ in parse_line(ln)), kw.get("efont", F_HEAD), size, max_w) for ln in lines) if lines else size
    els, y0, t = [], y, t0
    for ln in lines:
        e, h = text_line_els(ln, pal, size, y0, t, **kw)
        els += e
        y0 += h + gap
        t += 0.22 + 0.07 * len(parse_line(ln))
    return els, y0


def chip_el(text, pal, size, y, t0, colour="accent2", max_w=900):
    size = fit_size(text, F_MONO, size, max_w - 80)
    f = font(F_MONO, size)
    tw = f.getlength(text)
    w, h = int(tw + 80), int(size * 1.35 + 44)
    card = rounded((w, h), pal["card"], 26, outline=pal[colour], width=3)
    ImageDraw.Draw(card).text((40, 22 - f.getbbox(text)[1] // 3), text, font=f, fill=(*pal[colour], 255))
    return El(card, (W - w) // 2, y, t0, "pop", 0.45), h


# ---------------------------------------------------------------- layouts: each returns elements for one beat
def layout(beat, pal, rng):
    kind = beat["layout"]
    els = []
    if kind == "HOOK_BIG":
        sizes = [156, 108, 140]
        y = 560
        t = 0.05
        for i, ln in enumerate(beat["lines"]):
            e, h = text_line_els(ln, pal, sizes[min(i, 2)], y, t, stagger=0.09)
            els += e
            y += h + 26
            t += 0.5
    elif kind == "CODE_CHIP":
        if beat.get("label"):
            e, h = text_line_els(beat["label"], dict(pal, text=pal["dim"]), 56, 470, 0.0, wfont=F_BOLD)
            els += e
        c, h = chip_el(beat["chip"], pal, 160, 600, 0.25, "accent2")
        els.append(c)
        e, _ = lines_block(beat.get("lines", []), pal, 88, 600 + h + 80, 1.0)
        els += e
    elif kind == "STEP":
        r = 96
        badge = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
        ImageDraw.Draw(badge).ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=(*pal["accent"], 255))
        f = font(F_HEAD, 120)
        tx = str(beat["badge"])
        ImageDraw.Draw(badge).text((r - f.getlength(tx) / 2, r - 86 - f.getbbox(tx)[1] // 4), tx, font=f, fill=(*pal["bg1"], 255))
        els.append(El(badge, W // 2 - r, 330, 0.0, "pop", 0.5))
        e, h = text_line_els(beat["label"], pal, 112, 570, 0.3, efont=F_HEAD, wfont=F_HEAD)
        els += e
        y = 570 + h + 60
        c, ch = chip_el(beat["chip"], pal, 72, y, 0.9, "accent2")
        els.append(c)
        y += ch + 28
        if beat.get("chip2"):
            c2, ch2 = chip_el(beat["chip2"], pal, 72, y, 1.2, "accent2")
            els.append(c2)
            y += ch2 + 28
        e, _ = lines_block(beat.get("lines", []), pal, 84, y + 50, 1.6)
        els += e
    elif kind == "NOTE":
        lines = beat["lines"]
        cw, ch = 940, 200 + 135 * len(lines)
        card = rounded((cw, ch), pal["card"], 34)
        d = ImageDraw.Draw(card)
        d.rounded_rectangle([0, 0, 18, ch - 1], radius=9, fill=(*pal["accent"], 255))
        els.append(El(card, (W - cw) // 2, 520, 0.0, "rise", 0.5))
        head = sprite_text(beat["label"], F_HEAD, 100, pal["accent"])
        els.append(El(head, (W - cw) // 2 + 60, 560, 0.35, "rise"))
        y, t = 700, 0.8
        for ln in lines:
            ws = parse_line(ln)
            size = fit_size(" ".join(w for w, _ in ws), F_BOLD, 76, cw - 120)
            x = (W - cw) // 2 + 60
            for w, e in ws:
                sp = sprite_text(w, F_HEAD if e else F_BOLD, size, pal["accent2"] if e else pal["text"])
                els.append(El(sp, x - 4, y, t, "rise", 0.3))
                x += font(F_HEAD if e else F_BOLD, size).getlength(w + " ")
                t += 0.07
            y += 118
            t += 0.25
    elif kind == "CTA":
        e, y = lines_block(beat["lines"], pal, 124, 600, 0.05)
        els += e
        if beat.get("sub"):
            e, _ = text_line_els(beat["sub"], dict(pal, text=pal["dim"]), 66, y + 60, 1.4, wfont=F_BOLD)
            els += e
    else:
        raise SystemExit(f"unknown layout {kind}")
    # centre the block vertically in the safe area (above the Shorts UI at the bottom)
    top = min(e.y for e in els)
    bottom = max(e.y + e.rgb.height for e in els)
    shift = 860 - (top + bottom) / 2
    for e in els:
        e.y += shift
    return els


# ---------------------------------------------------------------- frames
def background(pal):
    a = np.linspace(0, 1, H)[:, None, None]
    c1, c2 = np.array(pal["bg1"], np.float32), np.array(pal["bg2"], np.float32)
    img = (c1 * (1 - a) + c2 * a) * np.ones((H, W, 3), np.float32)
    return Image.fromarray(img.astype(np.uint8))


def draw_frame(base, bg_dots, t, beats_t, els_by_beat, pal, total):
    fr = base.copy()
    d = ImageDraw.Draw(fr)
    for (x, y, r, sp) in bg_dots:  # slow drifting dots (depth)
        yy = (y - t * sp) % H
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=pal["dot"])
    d.rectangle([0, 0, int(W * clamp(t / total)), 10], fill=pal["accent2"])  # progress bar
    bi = max(i for i, (s, e) in enumerate(beats_t) if s <= t or i == 0)
    s, e = beats_t[bi]
    lt = t - s
    out = clamp((e - t) / 0.22)  # exit fade/slide in the last 0.22 s of the beat
    for el in els_by_beat[bi]:
        p = clamp((lt - el.t0) / el.dur)
        if p <= 0:
            continue
        op = clamp(p * 1.6) * out
        if op <= 0.01:
            continue
        rgb, al = el.rgb, el.alpha
        x, y = el.x, el.y
        if el.anim == "rise":
            y = y + (1 - ease_out(p)) * 56 - (1 - out) * 30
        else:  # pop
            k = 0.55 + 0.45 * ease_back(p)
            w, h = max(1, int(rgb.width * k)), max(1, int(rgb.height * k))
            rgb, al = rgb.resize((w, h), Image.BILINEAR), al.resize((w, h), Image.BILINEAR)
            x, y = x + (el.rgb.width - w) / 2, y + (el.rgb.height - h) / 2 - (1 - out) * 30
        mask = al.point([int(i * op) for i in range(256)])
        fr.paste(rgb, (int(x), int(y)), mask)
    return fr


# ---------------------------------------------------------------- audio
def wav_len(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def build_voice(beat_files, out):
    """Concatenate beat wavs with silence; return [(start, end)] of each beat's spoken part (video beat = start..next start)."""
    spans, t = [], LEAD
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR)
        w.writeframes(b"\x00\x00" * int(SR * LEAD))
        for i, f in enumerate(beat_files):
            with wave.open(str(f)) as r:
                assert r.getframerate() == SR and r.getnchannels() == 1
                w.writeframes(r.readframes(r.getnframes()))
                d = r.getnframes() / SR
            spans.append((t, t + d))
            t += d
            w.writeframes(b"\x00\x00" * int(SR * (GAP if i < len(beat_files) - 1 else TAIL)))
            t += GAP if i < len(beat_files) - 1 else TAIL
    return spans, t


def mix(voice, starts, total, out):
    """voice + ducked music bed + soft whoosh at each beat start -> one loudness-normalised wav (-14 LUFS)."""
    n = len(starts)
    sw = ";".join(f"[sw{i}]adelay={int(max(0, s - 0.12) * 1000)}|{int(max(0, s - 0.12) * 1000)},volume=0.42[x{i}]" for i, s in enumerate(starts))
    split = "[2:a]asplit=%d%s" % (n, "".join(f"[sw{i}]" for i in range(n)))
    mixin = "".join(f"[x{i}]" for i in range(n))
    fc = (f"[0:a]asplit=2[v][vk];[1:a]atrim=0:{total + 1:.2f},volume=0.35,afade=t=in:d=1.2,afade=t=out:st={total - 1.5:.2f}:d=1.5[m];"
          f"[m][vk]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=500[md];{split};{sw};{mixin}amix=inputs={n}:normalize=0[sfx];"
          f"[v][md][sfx]amix=inputs=3:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9,atrim=0:{total:.2f}[o]")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(voice), "-ss", "20", "-i", str(MUSIC), "-i", str(SWOOSH),
                    "-filter_complex", fc, "-map", "[o]", "-ar", "48000", str(out)], check=True)


# ---------------------------------------------------------------- main
def beat_text_for_tts(b):
    return re.sub(r"\s+", " ", b["voice"]).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--tts", action="store_true")
    ap.add_argument("--still", help="comma separated seconds -> PNG stills in <story>/short/stills/")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--seconds", type=float)
    a = ap.parse_args()
    story = Path(a.story).resolve()
    spec = json.loads((story / "short.json").read_text(encoding="utf-8"))
    pal = PALETTES[spec["palette"]]
    beats = spec["beats"]
    tts_dir = story / "audio" / "tts"
    files = [tts_dir / f"beat_{i:02d}.wav" for i in range(len(beats))]

    if a.tts:
        import gemini_tts
        tts_dir.mkdir(parents=True, exist_ok=True)
        for i, (b, f) in enumerate(zip(beats, files)):
            if f.exists():
                continue
            r = gemini_tts.speak(beat_text_for_tts(b), spec["voice"]["id"], spec["voice"]["style"], f)
            print(f"beat {i}: {r['seconds']:.1f}s  ~${r['usd']:.4f}")
        return

    # timing: real TTS durations when present, else a word-count estimate (for stills)
    durs = [wav_len(f) if f.exists() else 0.36 * len(beat_text_for_tts(b).split()) for b, f in zip(beats, files)]
    t, beats_t = LEAD, []
    for i, d in enumerate(durs):
        end = t + d + (GAP if i < len(durs) - 1 else TAIL)
        beats_t.append((t if i else 0.0, end))
        t = end
    total = beats_t[-1][1]
    import random
    rng = random.Random(spec.get("seed", 1))
    els_by_beat = [layout(b, pal, rng) for b in beats]
    base = background(pal)
    dots = [(rng.randint(0, W), rng.randint(0, H), rng.choice([2, 3, 4, 5]), rng.choice([8, 14, 22])) for _ in range(34)]

    if a.still:
        out = story / "short" / "stills"
        out.mkdir(parents=True, exist_ok=True)
        for s in a.still.split(","):
            ts = float(s)
            draw_frame(base, dots, ts, beats_t, els_by_beat, pal, total).save(out / f"still_{ts:05.1f}.png")
        print("stills ->", out, f"(total {total:.1f}s, beats at {[round(b[0], 1) for b in beats_t]})")
        return

    if a.render:
        missing = [f.name for f in files if not f.exists()]
        if missing:
            sys.exit(f"missing TTS: {missing} (run --tts first)")
        out_dir = story / "short" / "output"
        out_dir.mkdir(parents=True, exist_ok=True)
        voice = out_dir / "_voice.wav"
        spans, total_v = build_voice(files, voice)
        starts = [s for s, _ in spans]
        beats_t = [(0.0 if i == 0 else spans[i][0] - 0.0, (spans[i + 1][0] if i + 1 < len(spans) else total_v)) for i in range(len(spans))]
        beats_t[0] = (0.0, beats_t[0][1])
        total = total_v
        audio = out_dir / "_mix.wav"
        mix(voice, starts, total, audio)
        n = int(round(min(total, a.seconds or total) * FPS))
        final = out_dir / ("short.mp4" if not a.seconds else f"short_check_{int(a.seconds)}s.mp4")
        enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                "-i", str(audio), "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p",
                                "-c:a", "aac", "-b:a", "192k", "-frames:v", str(n), "-t", f"{n / FPS:.3f}", "-movflags", "+faststart",
                                str(final)], stdin=subprocess.PIPE)
        for i in range(n):
            enc.stdin.write(draw_frame(base, dots, i / FPS, beats_t, els_by_beat, pal, total).tobytes())
            if i % 300 == 0:
                print(f"  frame {i}/{n}", flush=True)
        enc.stdin.close()
        if enc.wait():
            sys.exit("ffmpeg failed")
        print(f"OK {final}  {n / FPS:.1f}s")


if __name__ == "__main__":
    main()


