"""Animated cut-out Shorts (cast v3, free, local): background + the exact character PNGs, moved per frame.

    python tools/cutout_anim.py <video folder> [--seconds N] [--frames 2.0,13.5]

The video folder has lines.json (speaker/text), anim.json (scene plan, below) and _work/timed.json (line timings
from make_short.build_voice; made by the folder's voice step). Output: output/<name>.mp4 (1080x1920, 30 fps,
burned Hindi captions, voice + music + SFX mixed by make_short.build_audio). --frames only writes stills to _work/.

Motion (all procedural, Rs0): camera eases to the speaker's face (zoom), idle breathing, the speaker bobs while
talking, floating sets drift and turn slowly, Jugnu flaps (pose flip) and glows, props drift, rockets shake / launch /
land with flame + smoke, characters pop in, Earth city lights twinkle, crossfade between sets.

anim.json:
{"name": "...", "fps": 30, "world": [1620, 2880], "music": "jaadu/X.mp3", "sfx": {"kind": "file in shared/sfx"},
 "sfx_at": [["L3.start+0.3", "kind"]], "rumble": ["0.3", 3.5],
 "segments": [{"start": "0", "bg": "images/bg.png", "light": "evening", "mode": "ground|float",
   "cast": {"tinku": {"x": .5, "foot": .8, "h": .2, "pose": "happy", "appear": "L11.start"}},   # float: "y" = centre
   "props": {"rocket": {"img": "characters/_props/rocket.png", "flame": "...rocket_flame.png", "x": .5, "foot": .8, "h": .5,
             "launch": {"shake": "0.3", "flame": "0.8", "rise": "L1.end-1.2"}, "land": {"t": "L10.end", "dur": 1.4}}},
   "camera": [{"t": "0", "x": .5, "y": .5, "zoom": 1}, {"t": "L3.start", "focus": "bholu", "zoom": 1.6}],
   "pose_changes": [{"who": "bholu", "t": "L3.end", "pose": "laugh"}], "flip": [{"who": "daroga_singh", "t": "L5.start", "dur": 1.5}],
   "drift": [{"prop": "guava", "t0": "L3.start", "t1": "L3.end", "from": [x, y], "to": [x, y], "spin": 360}],
   "glow": [{"who": "jugnu", "t0": "L9.start", "t1": "L9.end", "gain": 2.5}], "twinkle": true}],
 "speak": {"L3": "point"}}                                                   # speaker pose per line
Times are seconds or "L<n>.start/end±s" (line n of lines.json, 1-based).
"""
import argparse
import json
import math
import random
import re
import subprocess
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))
import make_short as ms  # noqa: E402
from compose_scene import relight  # noqa: E402

OUT_W, OUT_H = 1080, 1920
FADE = 0.3
CHARS = ROOT / "channels" / "jugnu-stories" / "characters"


def ease(x):
    x = min(1.0, max(0.0, x))
    return x * x * (3 - 2 * x)


def ease_out_back(x):
    x = min(1.0, max(0.0, x))
    c = 1.70158
    return 1 + (c + 1) * (x - 1) ** 3 + c * (x - 1) ** 2


class Timeline:
    def __init__(self, timed):
        self.timed = timed

    def t(self, expr):
        if isinstance(expr, (int, float)):
            return float(expr)
        m = re.fullmatch(r"\s*L(\d+)\.(start|end)\s*([+-]\s*[\d.]+)?\s*", str(expr))
        if not m:
            return float(expr)
        base = self.timed[int(m.group(1)) - 1][m.group(2)]
        return base + (float(m.group(3).replace(" ", "")) if m.group(3) else 0.0)

    def line_at(self, t):
        for i, l in enumerate(self.timed):
            if l["start"] - 0.1 <= t <= l["end"] + 0.25:
                return i, l
        return None, None


class Sprites:
    """Cropped, pre-scaled PNGs (character poses, props) with the scene light applied."""

    def __init__(self):
        self.c = {}

    def get(self, path: Path, light="day", max_h=1100):
        key = (str(path), str(light))
        if key not in self.c:
            im = Image.open(path).convert("RGBA")
            im = im.crop(im.getchannel("A").getbbox())
            if im.height > max_h:
                im = im.resize((round(im.width * max_h / im.height), max_h), Image.Resampling.LANCZOS)
            self.c[key] = relight(im, light)
        return self.c[key]

    def pose(self, who, pose, light):
        return self.get(CHARS / who / f"{who}_{pose}.png", light)


def glow_sprite(size=256):
    y, x = np.mgrid[-1:1:complex(size), -1:1:complex(size)]
    a = np.clip(1 - np.sqrt(x * x + y * y), 0, 1) ** 2
    rgba = np.zeros((size, size, 4), np.uint8)
    rgba[..., 0], rgba[..., 1], rgba[..., 2] = 225, 250, 110
    rgba[..., 3] = (a * 255).astype(np.uint8)
    return Image.fromarray(rgba, "RGBA")


class Segment:
    def __init__(self, spec, tl: Timeline, base: Path, world, sprites: Sprites):
        self.s, self.tl, self.base, self.sp = spec, tl, base, sprites
        self.start = tl.t(spec.get("start", 0))
        self.light = spec.get("light", "day")
        self.float = spec.get("mode") == "float"
        self.W, self.H = world
        bg = Image.open(base / spec["bg"]).convert("RGB")
        self.bg = bg.resize((self.W, self.H), Image.Resampling.LANCZOS)
        self.cast = spec.get("cast", {})
        self.props = spec.get("props", {})
        rnd = random.Random(7)
        self.phase = {k: [rnd.uniform(0, 6.28) for _ in range(4)] for k in list(self.cast) + list(self.props)}
        self.twinkle = None
        if spec.get("twinkle"):  # warm bright dots (city lights) get a per-pixel twinkle phase
            a = np.asarray(self.bg).astype(np.float32)
            mask = ((a[..., 0] > 170) & (a[..., 1] > 130) & (a[..., 2] < 150)).astype(np.float32)
            self.twinkle = (mask, np.random.default_rng(3).uniform(0, 6.28, mask.shape).astype(np.float32))
        self.cams = [dict(k, t=tl.t(k["t"])) for k in spec.get("camera", [{"t": 0, "x": .5, "y": .5, "zoom": 1}])]

    # ----- positions -----
    def base_pos(self, who):
        c = self.cast[who]
        if "foot" in c:
            return c["x"], c["foot"] - 0.75 * c["h"]  # face height of a standing character
        return c["x"], c["y"] - 0.28 * c["h"]

    def camera(self, t):
        def target(k):
            if "focus" in k:
                x, y = self.base_pos(k["focus"])
                return x, y + k.get("dy", 0.08), k.get("zoom", 1.6)
            return k.get("x", .5), k.get("y", .5), k.get("zoom", 1.0)
        cur = target(self.cams[0])
        for k in self.cams[1:]:
            if t < k["t"]:
                break
            tgt, u = target(k), ease((t - k["t"]) / k.get("dur", 0.7))
            cur = tuple(a + (b - a) * u for a, b in zip(cur, tgt))
        x, y, z = cur
        z *= 1 + 0.012 * math.sin(t * 0.35)  # a slow breathing push so no shot is ever frozen
        vw, vh = self.W / z, self.H / z
        cx = min(max(x * self.W, vw / 2), self.W - vw / 2)
        cy = min(max(y * self.H, vh / 2), self.H - vh / 2)
        return cx - vw / 2, cy - vh / 2, vw, vh

    def pose_of(self, who, t, speak):
        c = self.cast[who]
        pose = c.get("pose", "stand")
        for ch in self.s.get("pose_changes", []):
            if ch["who"] == who and t >= self.tl.t(ch["t"]):
                pose = ch["pose"]
        i, line = self.tl.line_at(t)
        speaking = line is not None and line["speaker"] == who
        if speaking and f"L{i + 1}" in speak:
            pose = speak[f"L{i + 1}"]
        if who == "jugnu":  # wing flap: alternate with the flying pose every 4 frames
            flap = int(t * 30 / 4) % 2
            pose = (("laugh" if pose == "happy" else "walk") if flap else pose) if speaking else ("walk" if flap else pose)
        return pose, speaking, line

    # ----- drawing -----
    def render(self, t, speak):
        left, top, vw, vh = self.camera(t)
        k = OUT_W / vw
        frame = self.bg.crop((round(left), round(top), round(left + vw), round(top + vh))).resize(
            (OUT_W, OUT_H), Image.Resampling.BILINEAR).convert("RGBA")
        if self.twinkle is not None:
            mask, ph = self.twinkle
            tw = mask * (0.5 + 0.5 * np.sin(ph + t * 5.0)) * 90
            img = np.asarray(self.bg).astype(np.float32) + tw[..., None]
            frame = Image.fromarray(np.clip(img, 0, 255).astype(np.uint8)).crop(
                (round(left), round(top), round(left + vw), round(top + vh))).resize((OUT_W, OUT_H), Image.Resampling.BILINEAR).convert("RGBA")
        to = lambda wx, wy: ((wx * self.W - left) * k, (wy * self.H - top) * k)
        items = []
        for who, c in self.cast.items():
            items.append((c.get("foot", c.get("y", .5) + c["h"] / 2), "char", who))
        for name, p in self.props.items():
            items.append((p.get("foot", p.get("y", .5) + p["h"] / 2) - p.get("z", 0), "prop", name))
        for _, kind, name in sorted(items):
            if kind == "char":
                self.draw_char(frame, name, t, to, k, speak)
            else:  # smoke right behind/around its prop, under the characters in front of it
                smoke = Image.new("RGBA", (OUT_W, OUT_H), (0, 0, 0, 0))
                self.draw_prop(frame, smoke, name, t, to, k)
                frame.alpha_composite(smoke)
        return frame

    def paste(self, frame, im, cx, cy, h_px, rot=0.0, sx=1.0, sy=1.0, alpha=1.0, anchor="center"):
        if h_px < 4:
            return
        w = max(1, round(im.width * h_px / im.height * sx))
        h = max(1, round(h_px * sy))
        im = im.resize((w, h), Image.Resampling.BILINEAR)
        if rot:
            im = im.rotate(rot, resample=Image.Resampling.BILINEAR, expand=True)
        if alpha < 1:
            a = im.getchannel("A").point(lambda v: round(v * alpha))
            im.putalpha(a)
        if anchor == "foot":
            x0, y0 = cx - im.width / 2, cy - im.height
        else:
            x0, y0 = cx - im.width / 2, cy - im.height / 2
        frame.alpha_composite(im, (round(x0), round(y0))) if x0 >= 0 and y0 >= 0 else frame.paste(im, (round(x0), round(y0)), im)

    def draw_char(self, frame, who, t, to, k, speak):
        c, ph = self.cast[who], self.phase[who]
        scale = 1.0
        if "appear" in c:
            u = (t - self.tl.t(c["appear"])) / 0.35
            if u <= 0:
                return
            scale = ease_out_back(u)
        pose, speaking, line = self.pose_of(who, t, speak)
        im = self.sp.pose(who, pose, self.light)
        h = c["h"] * self.H * k * scale
        x, rot, sx, sy = c["x"], c.get("rot", 0.0), 1.0, 1.0
        if c.get("flip_x"):
            im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
        bob = 0.0
        if speaking:
            bob = abs(math.sin(2 * math.pi * 2.6 * (t - line["start"]))) * 0.012 * h
            sy = 1.02
        if who == "jugnu":
            x += 0.05 * math.sin(t * 0.9 + ph[0])
        for f in self.s.get("flip", []):
            if f["who"] == who:
                rot += 180 * ease((t - self.tl.t(f["t"])) / f.get("dur", 1.5))
        if self.float or who == "jugnu":
            y = c.get("y", c.get("foot", .5) - c["h"] / 2) + 0.012 * math.sin(2 * math.pi * t / 3.2 + ph[1])
            x += 0.008 * math.sin(2 * math.pi * t / 4.1 + ph[2])
            if self.float and who != "jugnu":
                rot += 7 * math.sin(2 * math.pi * t / 5.3 + ph[3])
            cx, cy = to(x, y)
            g = self.glow_gain(who, t)
            if g:
                gs = glow_sprite()
                pulse = 0.55 + 0.45 * math.sin(t * 6.0)
                self.paste(frame, gs, cx + 0.12 * h, cy + 0.15 * h, h * (1.6 + 0.6 * g), alpha=min(1, 0.35 * g * pulse + 0.15))
            self.paste(frame, im, cx, cy - bob, h, rot=rot, sx=sx, sy=sy)
        else:
            sy *= 1 + 0.01 * math.sin(2 * math.pi * t / 2.4 + ph[1])  # breathing
            cx, cy = to(x, c["foot"])
            self.paste(frame, im, cx, cy - bob, h, rot=rot, sx=sx, sy=sy, anchor="foot")

    def glow_gain(self, who, t):
        if who != "jugnu":
            return 0
        g = 1.0
        for e in self.s.get("glow", []):
            if e["who"] == who and self.tl.t(e["t0"]) <= t <= self.tl.t(e["t1"]) + 0.6:
                g = e.get("gain", 2.0)
        return g

    def draw_prop(self, frame, smoke, name, t, to, k):
        p = self.props[name]
        img = self.base_or_root(p["img"])
        x, y_off, rot, flame, alpha = p["x"], 0.0, 0.0, False, 1.0
        dx = 0.0
        if "launch" in p:
            L = p["launch"]
            ts, tf, tr = self.tl.t(L["shake"]), self.tl.t(L["flame"]), self.tl.t(L["rise"])
            if ts <= t < tr + 0.4:
                dx = 0.004 * math.sin(t * 71) * min(1, (t - ts) * 2)
                y_off += 0.002 * math.sin(t * 53)
            flame = t >= tf
            if t >= tr:
                y_off -= 1.6 * ((t - tr) / 1.1) ** 2
            if t >= tf:
                self.puffs(smoke, to, k, p, tf, t, until=tr + 0.8)
        if "land" in p:
            t0, dur = self.tl.t(p["land"]["t"]), p["land"].get("dur", 1.4)
            u = (t - t0) / dur
            y_off -= 1.3 * (1 - ease(u)) if u < 1 else 0
            if u < 0:
                return
            flame = u < 1.08
            if u > 0.6:
                self.puffs(smoke, to, k, p, t0 + 0.6 * dur, t, until=t0 + dur + 0.5)
        for d in self.s.get("drift", []):
            if d["prop"] == name:
                t0, t1 = self.tl.t(d["t0"]), self.tl.t(d["t1"])
                if t < t0:
                    return
                u = (t - t0) / (t1 - t0)
                (x0, y0), (x1, y1) = d["from"], d["to"]
                x = x0 + (x1 - x0) * min(u, 1) + 0.02 * max(0, u - 1)
                p = dict(p, y=y0 + (y1 - y0) * min(u, 1) - 0.01 * max(0, u - 1))
                rot = d.get("spin", 0) * u
        im = self.sp.get(self.base_or_root(p["flame"]) if flame and p.get("flame") else img, self.light, max_h=1600)
        h = p["h"] * self.H * k
        if "foot" in p:
            cx, cy = to(x + dx, p["foot"] + y_off)
            if flame and p.get("flame"):  # the flame image is taller below the nozzle: keep the body in place
                fh = h * im.height / self.sp.get(img, self.light, max_h=1600).height
                self.paste(frame, im, cx, cy - h + fh, fh, anchor="foot")
            else:
                self.paste(frame, im, cx, cy, h, anchor="foot")
        else:
            cx, cy = to(x, p["y"] + y_off)
            self.paste(frame, im, cx, cy, h, rot=rot, alpha=alpha)

    def puffs(self, smoke, to, k, p, t_from, t, until):
        """Soft smoke puffs from the rocket base: spawned every 0.07 s, grow, drift sideways, fade."""
        d = ImageDraw.Draw(smoke)
        n = int((min(t, until) - t_from) / 0.07)
        for i in range(max(0, n - 30), n + 1):
            born = t_from + i * 0.07
            age = t - born
            if age < 0 or age > 1.6:
                continue
            r = random.Random(i * 13 + 5)
            side = r.choice([-1, 1])
            wx = p["x"] + side * (0.03 + 0.22 * age * r.uniform(0.5, 1.0))
            wy = p["foot"] - 0.01 - 0.04 * age * r.uniform(0.2, 1.0)
            cx, cy = to(wx, wy)
            rad = (0.03 + 0.07 * age) * self.W * k
            a = int(150 * (1 - age / 1.6))
            g = r.randint(200, 235)
            d.ellipse((cx - rad, cy - rad * 0.8, cx + rad, cy + rad * 0.8), fill=(g, g, g, a))

    def base_or_root(self, rel):
        for root in (self.base, CHARS.parent, ROOT):  # video folder, then channel folder, then repo
            if (root / rel).exists():
                return root / rel
        sys.exit(f"cutout_anim: file not found: {rel}")


def ass_events(timed):
    ev = []
    for line in timed:
        for s, e, txt in ms.caption_chunks(line):
            ev.append(f"Dialogue: 0,{ms.ass_time(s)},{ms.ass_time(e)},Cap,,0,0,0,,{txt}")
    return ev


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("folder")
    ap.add_argument("--seconds", type=float)
    ap.add_argument("--frames", help="comma list of seconds: write stills only")
    a = ap.parse_args()
    D = Path(a.folder).resolve()
    spec = json.loads((D / "anim.json").read_text(encoding="utf-8"))
    tm = json.loads((D / "_work" / "timed.json").read_text(encoding="utf-8"))
    timed, total = tm["timed"], tm["total"]
    tl, sprites = Timeline(timed), Sprites()
    world = tuple(spec.get("world", [1620, 2880]))
    segs = [Segment(s, tl, D, world, sprites) for s in spec["segments"]]
    speak = spec.get("speak", {})
    fps = spec.get("fps", 30)
    work = D / "_work"

    def frame_at(t):
        idx = max(i for i, s in enumerate(segs) if s.start <= t)
        f = segs[idx].render(t, speak)
        if idx + 1 < len(segs) and t > segs[idx + 1].start - FADE:
            f2 = segs[idx + 1].render(t, speak)
            f = Image.blend(f, f2, (t - (segs[idx + 1].start - FADE)) / FADE)
        return f.convert("RGB")

    if a.frames:
        for s in a.frames.split(","):
            out = work / f"still_{float(s):05.2f}.jpg"
            frame_at(float(s)).save(out, quality=88)
            print(out)
        return

    # audio: voice + music + SFX (+ a synthetic launch rumble) at the builder's levels
    voice = work / "voice.wav"
    events = {"sfx": [(tl.t(t), kind) for t, kind in spec.get("sfx_at", [])], "music_silent": [], "moods": []}
    extras = []
    if spec.get("rumble"):
        rumble = work / "rumble.wav"
        t0, dur = tl.t(spec["rumble"][0]), spec["rumble"][1]
        ms.run([ms.FFMPEG, "-y", "-f", "lavfi", "-i", f"anoisesrc=color=brown:amplitude=0.9:d={dur}", "-af",
                f"lowpass=f=180,afade=t=in:d=0.4,afade=t=out:st={dur - 1.2}:d=1.2", "-ar", "48000", rumble])
        extras.append((rumble, t0, 4, False))
    meta = {"music": spec["music"], "sfx": spec.get("sfx", {})}
    audio = ms.build_audio(voice, total, events, meta, work, True, ms.MUSIC_BELOW_VOICE_DB["short"], extras)

    (work / "fonts").mkdir(exist_ok=True)
    (work / "fonts" / ms.FONT.name).write_bytes(ms.FONT.read_bytes())
    family = ImageFont.truetype(str(ms.FONT)).getname()[0]
    (work / "caps.ass").write_text(ms.ass_doc(family, ass_events(timed)), encoding="utf-8")

    dur = a.seconds or total
    n = int(math.ceil(dur * fps))
    out_dir = D / "output"
    out_dir.mkdir(exist_ok=True)
    out = out_dir / f"{spec.get('name', D.name)}{'_test' if a.seconds else ''}.mp4"
    cmd = [str(ms.FFMPEG), "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{OUT_W}x{OUT_H}",
           "-r", str(fps), "-i", "-", "-i", str(audio), "-vf", "subtitles=caps.ass:fontsdir=fonts",
           "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709",
           "-color_primaries", "bt709", "-color_trc", "bt709", "-c:a", "aac", "-b:a", "192k", "-t", f"{dur:.3f}", str(out)]
    proc = subprocess.Popen(cmd, stdin=subprocess.PIPE, cwd=work)
    for i in range(n):
        proc.stdin.write(frame_at(i / fps).tobytes())
        if i % 150 == 0:
            print(f"  frame {i}/{n}", flush=True)
    proc.stdin.close()
    if proc.wait():
        sys.exit("ffmpeg failed")
    print(f"done: {out} ({dur:.1f}s, {n} frames), cost Rs0 (local render)")


if __name__ == "__main__":
    main()
