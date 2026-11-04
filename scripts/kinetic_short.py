"""Kinetic-text Short renderer v1 ("Claude explainer"): colourful gradients + HD image cards + word-by-word text. Pillow frames + ffmpeg.
Only the TTS and (fallback) image steps cost money; both log to cost_log.csv.

    .venv\\Scripts\\python -X utf8 scripts\\gen_kinetic_images.py <story_dir>      # HD images, free first
    .venv\\Scripts\\python -X utf8 scripts\\kinetic_short.py <story_dir> --tts       # one voice file per beat
    .venv\\Scripts\\python -X utf8 scripts\\kinetic_short.py <story_dir> --still 3,12  # PNG stills (layout check)
    .venv\\Scripts\\python -X utf8 scripts\\kinetic_short.py <story_dir> --render [--seconds N]

Spec <story_dir>/short.json: {"voice": {id, style}, "beats": [{layout, grad: [hex, hex], voice, lines, label, chip, badge, image, sub}]}.
"*word*" in a line = emphasis (accent colour). Layouts: HOOK_IMG (full-bleed image + title), FEATURE (image card + badge + title + chip +
lines), CTA (blurred image + question). Output: <story_dir>/short/output/short.mp4 (1080x1920, 30 fps, about -14 LUFS).
Look follows channels/devrobolab/STYLE_GUIDE.md; nothing is copied from another creator.
"""
import argparse
import json
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
FF = next((str(p) for p in (ROOT / "tools/ffmpeg/ffmpeg.exe", ROOT / "tools/ffmpeg/bin/ffmpeg.exe") if p.exists()), None) \
    or shutil.which("ffmpeg")
W, H, FPS, SR = 1080, 1920, 30, 24000
LEAD, GAP, TAIL = 0.35, 0.30, 1.2
SAFE_X = (80, 1000)
FONTS = ROOT / "shared/fonts"
F_HEAD, F_BOLD, F_MONO = FONTS / "Poppins-ExtraBold.ttf", FONTS / "Poppins-Bold.ttf", FONTS / "IBMPlexMono-Bold.ttf"
MUSIC = ROOT / "shared/music/noor/Soaring.mp3"
SWOOSH = ROOT / "shared/sfx/noor/swoosh_mikesmultimedia_349698.mp3"
WHITE, YELLOW, SOFT = (255, 255, 255), (255, 218, 74), (226, 232, 248)


# ---------------------------------------------------------------- helpers
def clamp(x, a=0.0, b=1.0):
    return max(a, min(b, x))


def ease_out(p):
    return 1 - (1 - p) ** 3


def ease_back(p):
    c1, c3 = 1.70158, 2.70158
    return 1 + c3 * (p - 1) ** 3 + c1 * (p - 1) ** 2


def hexrgb(h):
    h = h.lstrip("#")
    return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))


_fc = {}


def font(path, size):
    k = (str(path), int(size))
    if k not in _fc:
        _fc[k] = ImageFont.truetype(str(path), int(size), layout_engine=ImageFont.Layout.BASIC)
    return _fc[k]


def parse_line(line):
    out, emph = [], False
    for part in line.split("*"):
        out += [(w, emph) for w in part.split() if w]
        emph = not emph
    return out


def fit_size(text, fpath, start, max_w):
    s = start
    while s > 28 and font(fpath, s).getlength(text) > max_w:
        s -= 2
    return s


def sprite_text(text, fpath, size, rgb, pad=6, shadow=True):
    f = font(fpath, size)
    l, t, r, b = f.getbbox(text)
    img = Image.new("RGBA", (r - l + 2 * pad + 6, int(size * 1.4) + 2 * pad + 6), (0, 0, 0, 0))
    if shadow:  # soft dark drop shadow keeps white text readable on any gradient
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0))
        ImageDraw.Draw(sh).text((pad - l + 3, pad + 4), text, font=f, fill=(0, 0, 0, 120))
        img = Image.alpha_composite(img, sh.filter(ImageFilter.GaussianBlur(3)))
    ImageDraw.Draw(img).text((pad - l, pad), text, font=f, fill=(*rgb, 255))
    return img


class El:
    """Animated sprite: appears at t0 (beat-local seconds); anim 'rise' (slide up + fade) or 'pop' (scale + fade)."""

    def __init__(self, sprite, x, y, t0, anim="rise", dur=0.38):
        self.rgb, self.alpha = sprite.convert("RGB"), sprite.getchannel("A")
        self.x, self.y, self.t0, self.anim, self.dur = x, y, t0, anim, dur


def rrect(size, fill, radius, alpha=255, outline=None, width=0):
    img = Image.new("RGBA", size, (0, 0, 0, 0))
    ImageDraw.Draw(img).rounded_rectangle([0, 0, size[0] - 1, size[1] - 1], radius=radius, fill=(*fill, alpha),
                                          outline=(*outline, 255) if outline else None, width=width)
    return img


def line_els(line, size, y, t0, stagger=0.07, max_w=SAFE_X[1] - SAFE_X[0], accent=YELLOW, base=WHITE, cx=W // 2):
    words = parse_line(line)
    plain = " ".join(w for w, _ in words)
    size = fit_size(plain, F_HEAD, size, max_w)
    space = font(F_BOLD, size).getlength(" ")
    widths = [font(F_HEAD if e else F_BOLD, size).getlength(w) for w, e in words]
    x = cx - (sum(widths) + space * (len(words) - 1)) / 2
    els = []
    for i, ((w, e), wd) in enumerate(zip(words, widths)):
        els.append(El(sprite_text(w, F_HEAD if e else F_BOLD, size, accent if e else base), x - 6, y, t0 + i * stagger, "rise", 0.30))
        x += wd + space
    return els, int(size * 1.35)


def lines_block(lines, size, y, t0, gap=10, **kw):
    if not lines:
        return [], y
    mw = kw.get("max_w", SAFE_X[1] - SAFE_X[0])
    size = min(fit_size(" ".join(w for w, _ in parse_line(ln)), F_HEAD, size, mw) for ln in lines)  # one size for the block
    els, y0, t = [], y, t0
    for ln in lines:
        e, h = line_els(ln, size, y0, t, **kw)
        els += e
        y0 += h + gap
        t += 0.2 + 0.07 * len(parse_line(ln))
    return els, y0


def chip_el(text, size, y, t0, tint):
    size = fit_size(text, F_MONO, size, 880 - 70)
    f = font(F_MONO, size)
    w, h = int(f.getlength(text) + 70), int(size * 1.4 + 36)
    card = rrect((w, h), (8, 10, 24), 26, alpha=170, outline=tint, width=3)
    ImageDraw.Draw(card).text((35, 16 - f.getbbox(text)[1] // 4), text, font=f, fill=(*tint, 255))
    return El(card, (W - w) // 2, y, t0, "pop", 0.45), h


# ---------------------------------------------------------------- backgrounds and images
def gradient_bg(c1, c2):
    yy, xx = np.mgrid[0:H, 0:W].astype(np.float32)
    t = np.clip(yy / H * 0.85 + xx / W * 0.15, 0, 1)[..., None]
    img = np.array(c1, np.float32) * (1 - t) + np.array(c2, np.float32) * t
    glow = np.exp(-(((xx - W * 0.85) / 520) ** 2 + ((yy - H * 0.22) / 520) ** 2))[..., None]
    glow2 = np.exp(-(((xx - W * 0.1) / 560) ** 2 + ((yy - H * 0.85) / 560) ** 2))[..., None]
    img = img + glow * 70 + glow2 * 50
    return Image.fromarray(np.clip(img, 0, 255).astype(np.uint8))


def load_image(story, name):
    p = story / "images" / name if name else None
    if p and p.exists():
        return Image.open(p).convert("RGB")
    return None


def crop_resize(src, w, h, zoom, fx=0.5, fy=0.5):
    """Cover-fit src into (w, h), zoomed by `zoom` around (fx, fy): one high-quality resample of the visible part."""
    s0 = max(w / src.width, h / src.height)
    cw, ch = w / s0 / zoom, h / s0 / zoom
    x0 = clamp(fx * src.width - cw / 2, 0, src.width - cw)
    y0 = clamp(fy * src.height - ch / 2, 0, src.height - ch)
    return src.resize((w, h), Image.LANCZOS, box=(x0, y0, x0 + cw, y0 + ch))


class Scene:
    def __init__(self, beat, story, rng):
        g = beat.get("grad", ["#1b1b4b", "#0b7ea8"])
        self.c1, self.c2 = hexrgb(g[0]), hexrgb(g[1])
        self.tint = tuple(min(255, int(c * 0.45 + 150)) for c in self.c2)  # light tint of the second colour for chips
        self.bg = gradient_bg(self.c1, self.c2)
        lum = 0.2126 * self.c2[0] + 0.7152 * self.c2[1] + 0.0722 * self.c2[2]
        self.bright = lum > 140
        self.base, self.accent = ((22, 24, 62), (150, 20, 70)) if self.bright else (WHITE, YELLOW)
        self.kind = beat["layout"]
        self.img = load_image(story, beat.get("image"))
        self.els = []
        self.card = None
        kind = self.kind
        if kind == "HOOK_IMG":
            y, t = 1040, 0.15
            for i, ln in enumerate(beat["lines"]):
                e, h = line_els(ln, [150, 112][min(i, 1)], y, t, stagger=0.09)
                self.els += e
                y += h + 8
                t += 0.45
            ov = np.zeros((H, W), np.float32)
            yy = np.arange(H)[:, None] / H
            ov[:] = np.clip((yy - 0.45) * 2.0, 0, 1) * 215 + np.clip((0.18 - yy) * 4, 0, 1) * 120
            self.overlay_mask = Image.fromarray(ov.astype(np.uint8))
            self.overlay_rgb = Image.new("RGB", (W, H), tuple(int(c * 0.25) for c in self.c1))
        elif kind == "FEATURE":
            cx, cy, cw, ch = 70, 170, 940, 830
            self.card = dict(x=cx, y=cy, w=cw, h=ch)
            self.card["mask"] = rrect((cw, ch), WHITE, 46).getchannel("A")
            self.card["ring"] = rrect((cw, ch), (0, 0, 0), 46, alpha=0, outline=(255, 255, 255), width=4)
            sh = Image.new("RGBA", (cw + 160, ch + 160), (0, 0, 0, 0))
            ImageDraw.Draw(sh).rounded_rectangle([80, 100, 80 + cw, 100 + ch], radius=46, fill=(0, 0, 0, 150))
            self.card["shadow"] = sh.filter(ImageFilter.GaussianBlur(28))
            r = 78
            badge = Image.new("RGBA", (2 * r, 2 * r), (0, 0, 0, 0))
            bd = ImageDraw.Draw(badge)
            bd.ellipse([0, 0, 2 * r - 1, 2 * r - 1], fill=(*YELLOW, 255))
            f = font(F_HEAD, 96)
            tx = str(beat["badge"])
            bd.text((r - f.getlength(tx) / 2, r - 70 - f.getbbox(tx)[1] // 5), tx, font=f, fill=(*self.c1, 255))
            self.els.append(El(badge, cx + 26, cy + 26, 0.25, "pop", 0.5))
            y = cy + ch + 36
            e, h = line_els(beat["label"], 118, y, 0.35, base=self.base, accent=self.accent)
            self.els += e
            y += h + 8
            c, chh = chip_el(beat["chip"], 66, y, 0.8, self.tint if not self.bright else (255, 236, 170))
            self.els.append(c)
            y += chh + 18
            e, _ = lines_block(beat.get("lines", []), 62, y, 1.3, accent=self.accent, base=self.base)
            self.els += e
        elif kind == "CTA":
            e, y = lines_block(beat["lines"], 118, 760, 0.1, gap=14)
            self.els += e
            if beat.get("sub"):
                e, _ = line_els(beat["sub"], 56, y + 40, 1.2, base=SOFT)
                self.els += e
            if self.img:
                self.blur = crop_resize(self.img, 270, 480, 1.0).filter(ImageFilter.GaussianBlur(6)).resize((W, H), Image.BICUBIC)
        else:
            raise SystemExit(f"unknown layout {kind}")


def draw_scene(fr, sc, lt, out):
    """Image layers of a scene (under the text elements)."""
    if sc.kind == "HOOK_IMG" and sc.img:
        z = 1.0 + 0.12 * clamp(lt / 7.0)
        fr.paste(crop_resize(sc.img, W, H, z, 0.5, 0.5))
        fr.paste(sc.overlay_rgb, (0, 0), sc.overlay_mask)
    elif sc.kind == "FEATURE" and sc.card:
        c = sc.card
        p = clamp(lt / 0.5)
        op = ease_out(p) * out
        dy = (1 - ease_out(p)) * 90 - (1 - out) * 30
        if op > 0.01:
            sh = c["shadow"]
            fr.paste(sh.convert("RGB"), (int(c["x"] - 80), int(c["y"] - 60 + dy)), sh.getchannel("A").point([int(i * op) for i in range(256)]))
            z = 1.04 + 0.14 * clamp(lt / 7.0)
            im = crop_resize(sc.img, c["w"], c["h"], z, 0.5 + 0.03 * np.sin(lt * 0.8), 0.5) if sc.img else Image.new("RGB", (c["w"], c["h"]), sc.c2)
            m = c["mask"].point([int(i * op) for i in range(256)])
            fr.paste(im, (c["x"], int(c["y"] + dy)), m)
            ring = c["ring"]
            fr.paste(ring.convert("RGB"), (c["x"], int(c["y"] + dy)), ring.getchannel("A").point([int(i * op * 0.55) for i in range(256)]))
    elif sc.kind == "CTA" and sc.img:
        fr.paste(Image.blend(sc.blur, Image.new("RGB", (W, H), sc.c1), 0.55))


def draw_frame(sparks, t, beats_t, scenes, total):
    bi = max(i for i, (s, e) in enumerate(beats_t) if s <= t or i == 0)
    s, e = beats_t[bi]
    lt, sc = t - s, scenes[bi]
    out = clamp((e - t) / 0.22)
    fr = sc.bg.copy()
    d = ImageDraw.Draw(fr)
    draw_scene(fr, sc, lt, out)
    d = ImageDraw.Draw(fr)
    for (x, y, r, sp) in sparks:  # drifting light specks
        yy = (y - t * sp) % H
        d.ellipse([x - r, yy - r, x + r, yy + r], fill=(205, 218, 255))
    for el in sc.els:
        p = clamp((lt - el.t0) / el.dur)
        if p <= 0:
            continue
        op = clamp(p * 1.6) * out
        if op <= 0.01:
            continue
        rgb, al, x, y = el.rgb, el.alpha, el.x, el.y
        if el.anim == "rise":
            y = y + (1 - ease_out(p)) * 56 - (1 - out) * 30
        else:
            k = 0.55 + 0.45 * ease_back(p)
            w, h = max(1, int(rgb.width * k)), max(1, int(rgb.height * k))
            rgb, al = rgb.resize((w, h), Image.BILINEAR), al.resize((w, h), Image.BILINEAR)
            x, y = x + (el.rgb.width - w) / 2, y + (el.rgb.height - h) / 2 - (1 - out) * 30
        fr.paste(rgb, (int(x), int(y)), al.point([int(i * op) for i in range(256)]))
    if lt < 0.30 and bi > 0:  # colour wipe at every cut
        q = ease_out(lt / 0.30)
        ImageDraw.Draw(fr).rectangle([0, 0, W, int(H * (1 - q))], fill=tuple(min(255, int(c * 0.9 + 40)) for c in sc.c2))
    ImageDraw.Draw(fr).rectangle([0, 0, int(W * clamp(t / total)), 8], fill=YELLOW)  # progress bar
    return fr


# ---------------------------------------------------------------- audio
def wav_len(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def build_voice(files, out):
    spans, t = [], LEAD
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR)
        w.writeframes(b"\x00\x00" * int(SR * LEAD))
        for i, f in enumerate(files):
            with wave.open(str(f)) as r:
                assert r.getframerate() == SR and r.getnchannels() == 1
                w.writeframes(r.readframes(r.getnframes()))
                d = r.getnframes() / SR
            spans.append((t, t + d))
            gap = GAP if i < len(files) - 1 else TAIL
            w.writeframes(b"\x00\x00" * int(SR * gap))
            t += d + gap
    return spans, t


def mix(voice, starts, total, out):
    n = len(starts)
    sw = ";".join(f"[sw{i}]adelay={int(max(0, s - 0.12) * 1000)}|{int(max(0, s - 0.12) * 1000)},volume=0.42[x{i}]" for i, s in enumerate(starts))
    split = "[2:a]asplit=%d%s" % (n, "".join(f"[sw{i}]" for i in range(n)))
    fc = (f"[0:a]asplit=2[v][vk];[1:a]atrim=0:{total + 1:.2f},volume=0.35,afade=t=in:d=1.2,afade=t=out:st={total - 1.5:.2f}:d=1.5[m];"
          f"[m][vk]sidechaincompress=threshold=0.02:ratio=6:attack=20:release=500[md];{split};{sw};{''.join(f'[x{i}]' for i in range(n))}"
          f"amix=inputs={n}:normalize=0[sfx];[v][md][sfx]amix=inputs=3:normalize=0,atrim=0:{total:.2f}[o]")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(voice), "-ss", "20", "-i", str(MUSIC), "-i", str(SWOOSH),
                    "-filter_complex", fc, "-map", "[o]", "-ar", "48000", str(out) + ".raw.wav"], check=True)
    err = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(out) + ".raw.wav", "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    lufs = float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", err)[-1])
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(out) + ".raw.wav", "-af",
                    f"volume={-14.0 - lufs:.2f}dB,alimiter=limit=0.84:level=false", "-ar", "48000", str(out)], check=True)
    Path(str(out) + ".raw.wav").unlink()


def tts_text(b):
    return re.sub(r"\s+", " ", b["voice"]).strip()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--tts", action="store_true")
    ap.add_argument("--voice", help="override voice id (audition)")
    ap.add_argument("--still")
    ap.add_argument("--render", action="store_true")
    ap.add_argument("--seconds", type=float)
    a = ap.parse_args()
    story = Path(a.story).resolve()
    spec = json.loads((story / "short.json").read_text(encoding="utf-8-sig"))
    beats = spec["beats"]
    tts_dir = story / "audio" / "tts"
    files = [tts_dir / f"beat_{i:02d}.wav" for i in range(len(beats))]

    if a.tts:
        import gemini_tts
        tts_dir.mkdir(parents=True, exist_ok=True)
        for i, (b, f) in enumerate(zip(beats, files)):
            if f.exists():
                continue
            r = gemini_tts.speak(tts_text(b), a.voice or spec["voice"]["id"], spec["voice"]["style"], f)
            print(f"beat {i}: {r['seconds']:.1f}s  ~${r['usd']:.4f}")
        return

    import random
    rng = random.Random(spec.get("seed", 1))
    scenes = [Scene(b, story, rng) for b in beats]
    sparks = [(rng.randint(0, W), rng.randint(0, H), rng.choice([2, 2, 3]), rng.choice([10, 18, 28])) for _ in range(36)]
    durs = [wav_len(f) if f.exists() else 0.4 * len(tts_text(b).split()) for b, f in zip(beats, files)]
    t, beats_t = LEAD, []
    for i, d in enumerate(durs):
        end = t + d + (GAP if i < len(durs) - 1 else TAIL)
        beats_t.append((0.0 if i == 0 else t, end))
        t = end
    total = beats_t[-1][1]

    if a.still:
        out = story / "short" / "stills"
        out.mkdir(parents=True, exist_ok=True)
        for s in a.still.split(","):
            ts = float(s)
            draw_frame(sparks, ts, beats_t, scenes, total).save(out / f"still_{ts:05.1f}.png")
        print("stills ->", out, f"(total {total:.1f}s, beats at {[round(b[0], 1) for b in beats_t]})")
        return

    if a.render:
        missing = [f.name for f in files if not f.exists()]
        if missing:
            sys.exit(f"missing TTS: {missing} (run --tts first)")
        out_dir = story / "short" / "output"
        out_dir.mkdir(parents=True, exist_ok=True)
        voice = out_dir / "_voice.wav"
        spans, total = build_voice(files, voice)
        beats_t = [(0.0 if i == 0 else spans[i][0], spans[i + 1][0] if i + 1 < len(spans) else total) for i in range(len(spans))]
        audio = out_dir / "_mix.wav"
        mix(voice, [s for s, _ in spans], total, audio)
        n = int(round(min(total, a.seconds or total) * FPS))
        final = out_dir / ("short.mp4" if not a.seconds else f"short_check_{int(a.seconds)}s.mp4")
        enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                                "-i", str(audio), "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p",
                                "-c:a", "aac", "-b:a", "192k", "-frames:v", str(n), "-t", f"{n / FPS:.3f}", "-movflags", "+faststart",
                                str(final)], stdin=subprocess.PIPE)
        for i in range(n):
            enc.stdin.write(draw_frame(sparks, i / FPS, beats_t, scenes, total).tobytes())
            if i % 300 == 0:
                print(f"  frame {i}/{n}", flush=True)
        enc.stdin.close()
        if enc.wait():
            sys.exit("ffmpeg failed")
        print(f"OK {final}  {n / FPS:.1f}s")


if __name__ == "__main__":
    main()
