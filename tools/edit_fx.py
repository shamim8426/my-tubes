"""Finishing edit (the Sampadak's edit_plan.json) on a built video: free, local, ffmpeg + OpenCV only.

Builders call it after the scene clips are joined: `finish_video` re-renders video.mp4 once with the plan's colour
grade, vignette, grain, light leak, punch-ins, shake, transitions at scene cuts and text (title card, name tags,
on-screen notes, pop numbers); `audio_extras` gives the plan's SFX accents and ambience bed for the audio mix.
No edit_plan.json = this module is never called and the build stays exactly as before.

edit_plan.json (in the video folder; "line" = the builder's 1-based line number in lines.json):
{
  "grade": "warm_story" | "soft_glow" | "none",     # colour look (GRADES)
  "vignette": 0.22, "grain": 3.0,                     # 0 = off
  "light_leak": [[from_line, to_line]],               # soft warm glow over these lines (day scenes)
  "transitions": {"default": "cut", "scenes": {"5": "whip"}},   # cut | whip | flash | dip (into that scene)
  "punch_ins": [{"line": 3, "offset": 0.0, "dur": 2.0, "zoom": 1.12, "x": 0.5, "y": 0.45}],
  "shake": [{"line": 13, "offset": 0.0, "dur": 0.55}],
  "texts": [{"line": 2, "offset": 0.1, "dur": 2.5, "style": "tag", "text": "तारा", "pos": [0.8, 0.3]}],
                                                      # style: title | tag | note | pop; pos optional (0-1 of frame)
  "sfx": [{"line": 5, "offset": -0.15, "file": "whoosh_803771.mp3", "below_db": 18}],
  "ambience": {"file": "birds_841386.mp3", "below_db": 28}
}
"""
import math
import subprocess
from pathlib import Path

import cv2
import numpy as np

GRADES = {
    # (S-curve strength, blue, green, red multipliers, saturation)
    "warm_story": (0.06, 0.97, 1.00, 1.04, 1.08),  # tools/pro_edit_demo.py look (user demo, story 005)
    "soft_glow": (0.03, 1.00, 1.00, 1.02, 1.02),   # calm channels: almost neutral, a little warmth
    "none": (0.0, 1.0, 1.0, 1.0, 1.0),
}
TRANSITION_FRAMES = 4  # each side of a cut
TEXT_STYLES = {  # name: (font, size, primary, outline, back, border style, outline px, shadow, alignment)
    "title": ("Mukta ExtraBold", 120, "&H0040D8FF", "&H00102030", "&H96000000", 1, 9, 5, 8),  # top: off the faces
    "tag": ("Mukta Bold", 46, "&H00FFFFFF", "&H00305A9A", "&H00305A9A", 3, 10, 0, 1),
    "note": ("Mukta Bold", 68, "&H00203A5A", "&H0098D8F0", "&HB0000000", 3, 18, 0, 2),
    "pop": ("Mukta ExtraBold", 200, "&H0040E0FF", "&H00000000", "&H96000000", 1, 12, 6, 5),
}


def load(path: Path):
    import json
    return json.loads(path.read_text(encoding="utf-8")) if path.exists() else None


def at(plan_item, timed):
    """Seconds on the video timeline for a {"line": n, "offset": s} anchor (n is 1-based, as the builder prints)."""
    n = int(plan_item["line"])
    if not 1 <= n <= len(timed):
        raise ValueError(f"edit_plan: line {n} not in 1..{len(timed)}")
    return timed[n - 1]["start"] + float(plan_item.get("offset", 0.0))


def resolve(plan, timed, scene_starts, total, burned_captions):
    """Turn line anchors into seconds. Punch-ins/shake are dropped when captions are burned into the frames
    (they would zoom the captions) and reported in `notes`."""
    notes = []
    tr = plan.get("transitions", {})
    cuts = []
    for sc, t in scene_starts[1:]:
        kind = tr.get("scenes", {}).get(str(sc), tr.get("default", "cut"))
        if kind != "cut":
            cuts.append((t, kind))
    punches = [(at(p, timed), float(p.get("dur", 2.0)), float(p.get("zoom", 1.12)), float(p.get("x", 0.5)),
                float(p.get("y", 0.5))) for p in plan.get("punch_ins", [])]
    shakes = [(at(s, timed), float(s.get("dur", 0.5))) for s in plan.get("shake", [])]
    if burned_captions and (punches or shakes):
        notes.append(f"punch-ins/shake skipped ({len(punches) + len(shakes)}): captions are burned into the frames")
        punches, shakes = [], []
    leaks = [(timed[a - 1]["start"], timed[b - 1]["end"]) for a, b in plan.get("light_leak", [])]
    texts = [(at(x, timed), at(x, timed) + float(x.get("dur", 2.5)), x.get("style", "tag"), x["text"], x.get("pos"))
             for x in plan.get("texts", [])]
    for t0, t1, style, *_ in texts:
        if style not in TEXT_STYLES:
            raise ValueError(f"edit_plan: text style {style!r} (allowed: {', '.join(TEXT_STYLES)})")
        if t1 > total:
            notes.append(f"text at {t0:.1f}s runs past the end")
    return {"grade": plan.get("grade", "none"), "vignette": float(plan.get("vignette", 0.0)),
            "grain": float(plan.get("grain", 0.0)), "leaks": leaks, "cuts": cuts, "punches": punches,
            "shakes": shakes, "texts": texts, "notes": notes}


def _ease(x):
    return 0.5 - 0.5 * math.cos(math.pi * min(1.0, max(0.0, x)))


def _zoom_at(t, punches):
    z, cx, cy = 1.0, 0.5, 0.5
    for s, dur, zz, x, y in punches:
        e = s + dur
        if s <= t < e:
            ramp = min(0.25, dur / 3)
            k = _ease((t - s) / ramp) if t - s < ramp else (_ease((e - t) / 0.2) if e - t < 0.2 else 1.0)
            z, cx, cy = 1 + (zz - 1) * k, x, y
    return z, cx, cy


def _grade_tables(name):
    curve, b, g, r, _ = GRADES[name]
    x = np.arange(256, dtype=np.float32) / 255
    s = x + curve * np.sin(2 * math.pi * (x - 0.25)) * (x * (1 - x)) * 4  # gentle S-curve
    return [(np.clip(np.clip(s * m + (0.01 if m < 1 else 0), 0, 1), 0, 1) * 255).astype(np.uint8) for m in (b, g, r)]


def ass_doc(texts, w, h):
    """Text events as an ASS file in the video's own pixel space (Mukta fonts from the build's fonts/ dir)."""
    scale = h / 1080 if w > h else w / 1080  # sizes are for 1080 px on the short side
    styles = "\n".join(
        f"Style: {k},{f},{round(sz * scale)},{pc},&H000000FF,{oc},{bc},-1,0,0,0,100,100,0,0,{bs},"
        f"{max(1, round(ol * scale))},{round(sh * scale)},{al},{round(70 * scale)},{round(70 * scale)},"
        f"{round((90 if k == 'note' else 70) * scale)},1"
        for k, (f, sz, pc, oc, bc, bs, ol, sh, al) in TEXT_STYLES.items())
    t = lambda s: f"{int(s // 3600)}:{int(s % 3600 // 60):02d}:{s % 60:05.2f}"
    anim = {"title": r"{\fad(250,400)\fscx70\fscy70\t(0,350,\fscx104\fscy104)\t(350,500,\fscx100\fscy100)}",
            "pop": r"{\fscx40\fscy40\t(0,140,\fscx110\fscy110)\t(140,240,\fscx100\fscy100)\fad(0,150)}",
            "tag": r"{\fad(200,250)}", "note": r"{\fad(250,250)}"}
    pos = lambda p: f"{{\\an5\\pos({round(p[0] * w)},{round(p[1] * h)})}}" if p else ""  # pos: [x, y] 0-1 of frame
    ev = "\n".join(f"Dialogue: 2,{t(a)},{t(b)},{st},,0,0,0,,{pos(p)}{anim[st]}{txt}" for a, b, st, txt, p in texts)
    return (f"[Script Info]\nScriptType: v4.00+\nPlayResX: {w}\nPlayResY: {h}\nScaledBorderAndShadow: yes\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour,"
            " Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow,"
            f" Alignment, MarginL, MarginR, MarginV, Encoding\n{styles}\n\n"
            f"[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n{ev}\n")


class Finisher:
    """The per-frame look: punch-in/shake -> transitions -> grade, vignette, light leak, grain. Used by finish_video
    (joined video) and by builders that make their own frames (Noor: apply BEFORE libass draws the Arabic, so the
    Arabic keeps its colours)."""

    def __init__(self, R, w, h, fps):
        self.R, self.w, self.h, self.fps = R, w, h, fps
        self.tabs = _grade_tables(R["grade"]) if R["grade"] != "none" else None
        self.sat = GRADES[R["grade"]][4]
        yy, xx = np.mgrid[0:h, 0:w].astype(np.float32)
        self.vig = None
        if R["vignette"]:
            d = np.sqrt(((xx - w / 2) / (w / 2)) ** 2 + ((yy - h / 2) / (h / 2)) ** 2)
            self.vig = (1 - R["vignette"] * np.clip(d - 0.55, 0, 1) ** 1.5)[..., None].astype(np.float32)
        self.glow = (np.exp(-(((xx - w * 0.85) / (w * 0.35)) ** 2 + ((yy + h * 0.1) / (h * 0.6)) ** 2))[..., None]
                     * np.float32((40, 90, 140)) * 0.35).astype(np.float32) if R["leaks"] else None
        rng = np.random.default_rng(3)
        self.grains = ([rng.normal(0, R["grain"], (h // 2, w // 2, 1)).repeat(2, 0).repeat(2, 1).astype(np.float32)
                        for _ in range(6)] if R["grain"] else None)
        self.tf = TRANSITION_FRAMES / fps

    def apply(self, f, i):
        R, w, h, fps = self.R, self.w, self.h, self.fps
        t = i / fps
        z, cx, cy = _zoom_at(t, R["punches"])
        dx = dy = 0.0
        for s, dur in R["shakes"]:
            if s <= t < s + dur:
                a = 14 * (h / 1080) * (1 - (t - s) / dur)
                dx, dy, z = a * math.sin(t * 90), a * math.cos(t * 73), max(z, 1.04)
        if z > 1.0001 or dx or dy:
            M = np.float32([[z, 0, (1 - z) * cx * w + dx], [0, z, (1 - z) * cy * h + dy]])
            f = cv2.warpAffine(f, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REFLECT)
        fade = 1.0
        for c, kind in R["cuts"]:
            d = t - c
            if -self.tf <= d < self.tf:
                k = 1 - abs(d) / self.tf
                if kind == "whip":
                    f = np.roll(cv2.blur(f, (int(9 + 70 * k * w / 1920) | 1, 1)), int(np.sign(d or 1) * -90 * k * w / 1920),
                                axis=1)
                elif kind == "flash":
                    f = cv2.addWeighted(f, 1 - 0.85 * k, np.full_like(f, 255), 0.85 * k, 0)
                elif kind == "dip":
                    fade = min(fade, 1 - 0.9 * k)
        if self.tabs:
            f = cv2.merge([cv2.LUT(ch, tb) for ch, tb in zip(cv2.split(f), self.tabs)])
        f = f.astype(np.float32)
        if self.sat != 1.0:
            gray = f.mean(axis=2, keepdims=True)
            f = gray + (f - gray) * self.sat
        if self.vig is not None:
            f *= self.vig
        if self.glow is not None and any(a <= t < b for a, b in R["leaks"]):
            f += np.roll(self.glow, int(w * 0.05 * math.sin(t * 0.3)), axis=1)
        if self.grains:
            f += self.grains[i % 6]
        if fade < 1.0:
            f *= fade
        return np.clip(f, 0, 255).astype(np.uint8)


def look_only(plan):
    """R for a builder that only wants the colour look (grade, vignette, grain, light leak) and no cuts/punch-ins/text:
    Noor-e-Raah. `light_leak` is not used there."""
    return {"grade": plan.get("grade", "none"), "vignette": float(plan.get("vignette", 0.0)),
            "grain": float(plan.get("grain", 0.0)), "leaks": [], "cuts": [], "punches": [], "shakes": [], "texts": [],
            "notes": []}


def finish_video(ffmpeg, src: Path, dst: Path, R, prof, work: Path):
    """Frame pass over the joined video (Finisher), then text burned by libass while encoding (same bt709 tags and
    encoder settings as the scene clips)."""
    w, h, fps = prof["w"], prof["h"], prof["fps"]
    cap = cv2.VideoCapture(str(src))
    n = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    vf = ""
    if R["texts"]:
        (work / "edit_texts.ass").write_text(ass_doc(R["texts"], w, h), encoding="utf-8")
        vf = "subtitles=filename=edit_texts.ass:fontsdir=fonts,"
    vf += ("scale=out_color_matrix=bt709:out_range=tv,format=yuv420p,setsar=1,"
           "setparams=range=tv:color_primaries=bt709:color_trc=bt709:colorspace=bt709")
    enc = subprocess.Popen([str(ffmpeg), "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{w}x{h}",
                            "-r", str(fps), "-i", "-", "-vf", vf, "-c:v", "libx264", *prof["enc"], "-pix_fmt", "yuv420p",
                            "-color_range", "tv", "-colorspace", "bt709", "-color_primaries", "bt709",
                            "-color_trc", "bt709", "-r", str(fps), "-video_track_timescale", str(fps * 1000), str(dst)],
                           cwd=work, stdin=subprocess.PIPE)
    fin = Finisher(R, w, h, fps)
    for i in range(n):
        ok, f = cap.read()
        if not ok:
            break
        enc.stdin.write(fin.apply(f, i).tobytes())
    enc.stdin.close()
    cap.release()
    if enc.wait():
        raise RuntimeError("edit_fx: ffmpeg failed in the finishing pass")
    return n


def audio_extras(plan, timed, sfx_dir: Path, total):
    """[(file, start s, dB below the voice, loop)] for the audio mix: SFX accents + one ambience bed."""
    out = [(sfx_dir / s["file"], max(0.0, at(s, timed)), float(s.get("below_db", 18)), False)
           for s in plan.get("sfx", [])]
    amb = plan.get("ambience")
    if amb:
        out.append((sfx_dir / amb["file"], 0.0, float(amb.get("below_db", 28)), True))
    missing = [str(f) for f, *_ in out if not f.exists()]
    if missing:
        raise FileNotFoundError(f"edit_plan sound files missing: {missing}")
    return out
