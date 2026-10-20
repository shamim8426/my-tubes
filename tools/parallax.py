"""2.5D parallax shots from one still image (free, local, CPU).

Depth: ONLY Depth Anything V2 Small (depth-anything/Depth-Anything-V2-Small-hf, Apache-2.0) from models/.
Base/Large/Giant are CC BY-NC (non-commercial) and must never be used.

    python tools/parallax.py clip <image> <out.mp4> [--preset push_in] [--seconds 6] [--format long|short]
                                  [--cx 0.5] [--amp 0.035] [--overlay fireflies:0.25] [--overlay diya:0.25@0.3,0.6]
    python tools/parallax.py depth <image>          # build/cache the depth map only

How a shot is made (layered depth):
  1. depth map (cached in <image folder>/_depth/<name>_<hash>.png, 16-bit, near = bright)
  2. foreground = near part of the depth map (Otsu split, cleaned, small bits removed), edges feathered; the
     foreground moves per pixel with its own depth, extended past its outline so the outline moves rigidly
  3. background plate = the image with the foreground filled by OpenCV inpaint, moving with the depth of what is
     behind; floors/walls have the same depth in both layers, so they never tear - the inpainted plate is only
     seen in the thin sliver a real depth jump reveals
  4. depth d moves (0.5 + 0.5 d) of the preset's move: foreground max ~3.5% of the width, far background half;
     eased in and out (cosine)
  5. quality guard: thin foreground parts (feathers, hair, sticks) at a big depth jump -> motion halved, and if
     still risky -> Ken Burns zoom fallback (same move as make_short "in"); every decision goes to
     shared/parallax_log.jsonl
Output: Long 1920x1080 / Short 1080x1920, 30 fps, H.264, yuv420p, bt709 (same tags as make_short).
"""
import argparse
import hashlib
import json
import math
import subprocess
import sys
import time
from pathlib import Path

import cv2
import numpy as np

ROOT = Path(__file__).resolve().parent.parent
MODEL_DIR = ROOT / "models" / "depth-anything-v2-small"
FFMPEG = ROOT / "tools" / "ffmpeg" / "ffmpeg.exe"
if not FFMPEG.exists():
    import shutil
    FFMPEG = Path(shutil.which("ffmpeg") or "ffmpeg")
LOG = ROOT / "shared" / "parallax_log.jsonl"

FORMATS = {"long": (1920, 1080), "short": (1080, 1920)}
FPS = 30
MAX_SECONDS = 8.0          # one parallax shot never runs longer than this
AMP = 0.035                # foreground max movement, fraction of the frame width (3-4%)
OVERSCAN = 1 + AMP         # just the room the sideways moves need (fg max amp/2 per side); zoom only enlarges
PRESETS = ["push_in", "pull_out", "pan_left", "pan_right", "gentle_orbit", "static_breathe"]
MOOD_PRESETS = {           # first choice per music mood; never the same preset twice in a row
    "tension": ["push_in", "static_breathe", "pan_right"],
    "comedy": ["pan_left", "pan_right", "push_in"],
    "seekh": ["pull_out", "gentle_orbit", "static_breathe"],
    "khushi": ["gentle_orbit", "pan_right", "pull_out"],
    "dukh": ["static_breathe", "pull_out"],
    "jaadu": ["gentle_orbit", "push_in"],
}
# quality guard: risk = share of thin foreground parts x depth jump at the foreground edge
RISK_HALF, RISK_FALLBACK = 0.05, 0.10
JUMP_HALF, JUMP_FALLBACK = 0.10, 0.20  # depth jump at the fg edge: busy day scenes smear in the revealed sliver
FG_MIN, FG_MAX = 0.03, 0.85  # foreground share of the frame; outside -> the split is not meaningful


# ---------- depth ----------
_model = None


def _load():
    global _model
    if _model is None:
        import torch
        from transformers import AutoImageProcessor, AutoModelForDepthEstimation
        if not (MODEL_DIR / "model.safetensors").exists():
            sys.exit(f"depth model missing: {MODEL_DIR} (run deploy.ps1 step 6)")
        cfg = json.loads((MODEL_DIR / "config.json").read_text(encoding="utf-8"))
        assert "small" in str(MODEL_DIR).lower() and cfg.get("backbone_config", {}).get("hidden_size", 384) == 384, \
            "only Depth Anything V2 SMALL is allowed (Apache-2.0)"
        torch.set_num_threads(max(1, (__import__("os").cpu_count() or 4) - 2))
        _model = (AutoImageProcessor.from_pretrained(MODEL_DIR),
                  AutoModelForDepthEstimation.from_pretrained(MODEL_DIR).eval())
    return _model


def depth_map(img_path: Path) -> np.ndarray:
    """Relative depth, float32 0..1 (1 = nearest), same size as the image. Cached as a 16-bit PNG."""
    img_path = Path(img_path)
    h = hashlib.sha256(img_path.read_bytes()).hexdigest()[:10]
    cache = img_path.parent / "_depth" / f"{img_path.stem}_{h}.png"
    if cache.exists():
        return cv2.imread(str(cache), cv2.IMREAD_UNCHANGED).astype(np.float32) / 65535
    import torch
    from PIL import Image
    proc, model = _load()
    im = Image.open(img_path).convert("RGB")
    with torch.no_grad():
        out = model(**proc(images=im, return_tensors="pt"))
    d = proc.post_process_depth_estimation(out, target_sizes=[(im.height, im.width)])[0]["predicted_depth"].numpy()
    lo, hi = np.percentile(d, 1), np.percentile(d, 99)
    d = np.clip((d - lo) / max(hi - lo, 1e-6), 0, 1).astype(np.float32)
    cache.parent.mkdir(exist_ok=True)
    cv2.imwrite(str(cache), (d * 65535).astype(np.uint16))
    return d


# ---------- layers ----------
def layers(img: np.ndarray, depth: np.ndarray):
    """(background plate, plate depth, foreground alpha 0..1, foreground depth, stats).
    Layered depth: the foreground (near part, Otsu split of the depth map) moves per pixel with its own depth; the
    plate behind it (foreground filled by OpenCV inpaint, depth filled from the far side) moves with that depth.
    Where both layers have the same depth (floors, walls) they move together, so no seam; the inpainted plate only
    shows in a thin sliver at real depth jumps (a character in front of far houses)."""
    H, W = depth.shape
    d8 = (depth * 255).astype(np.uint8)
    _, mask = cv2.threshold(cv2.GaussianBlur(d8, (0, 0), 3), 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    k = max(3, W // 300) | 1
    mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k, k)))
    mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (k * 3, k * 3)))
    n, lab, st, _ = cv2.connectedComponentsWithStats(mask)
    keep = np.zeros_like(mask)
    for i in range(1, n):
        if st[i, cv2.CC_STAT_AREA] >= 0.004 * W * H:
            keep[lab == i] = 255
    mask = keep
    area = float((mask > 0).sum())
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    perim = sum(cv2.arcLength(c, True) for c in contours)
    ragged = perim / (2 * math.sqrt(math.pi * area)) if area else 0.0
    # thin parts (feathers, hair, sticks, wires): share of the mask that a 2%-wide opening removes
    kt = int(W * 0.02) | 1
    thick = cv2.morphologyEx(mask, cv2.MORPH_OPEN, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (kt, kt)))
    thin = 1 - float((thick > 0).sum()) / area if area else 0.0
    # size of the depth jump at the foreground edge (big jump = more revealed plate)
    edge = cv2.morphologyEx(mask, cv2.MORPH_GRADIENT, np.ones((9, 9), np.uint8)) > 0
    near_v = depth[edge & (mask > 0)]
    far_v = depth[edge & (mask == 0)]
    jump = float(np.median(near_v) - np.median(far_v)) if near_v.size and far_v.size else 0.0
    # foreground depth: inside the mask its own depth; just outside, the nearest inside value (grey dilation), so
    # the outline and the feathered edge move rigidly with the character instead of stretching
    dm = np.where(mask > 0, depth, 0).astype(np.float32)
    dil = cv2.dilate(dm, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(W * 0.03) | 1,) * 2))
    fg_depth = cv2.GaussianBlur(np.where(mask > 0, depth, dil), (0, 0), max(2.0, W * 0.002))
    # plate: foreground (grown a little) filled by inpaint at 1/4 size; depth filled the same way, then smoothed
    grow = cv2.dilate(mask, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(W * 0.016) | 1,) * 2))
    # the foreground alpha covers the grown band too (feathered inside it), so the inpainted plate is never seen
    # where nothing moved - only in the thin sliver the camera actually reveals
    inner = cv2.erode(grow, cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (int(W * 0.004) | 1,) * 2))
    alpha = cv2.GaussianBlur(inner.astype(np.float32) / 255, (0, 0), max(2.0, W * 0.0025))
    s = 4
    sz = (W // s, H // s)
    msmall = cv2.dilate(cv2.resize(grow, sz, interpolation=cv2.INTER_NEAREST), np.ones((5, 5), np.uint8))  # past the outline
    filled = cv2.inpaint(cv2.resize(img, sz, interpolation=cv2.INTER_AREA), msmall, 7, cv2.INPAINT_TELEA)
    filled = cv2.GaussianBlur(cv2.resize(filled, (W, H), interpolation=cv2.INTER_CUBIC), (0, 0), 2)
    g = cv2.GaussianBlur(grow.astype(np.float32) / 255, (0, 0), W * 0.003)[..., None]
    plate = (img * (1 - g) + filled * g).astype(np.uint8)
    dfill = cv2.inpaint(cv2.resize(d8, sz, interpolation=cv2.INTER_AREA), msmall, 7, cv2.INPAINT_TELEA)
    pd = cv2.resize(dfill.astype(np.float32) / 255, (W, H), interpolation=cv2.INTER_LINEAR)
    gm = g[..., 0]
    plate_depth = cv2.GaussianBlur(fg_depth * (1 - gm) + pd * gm, (0, 0), max(2.0, W * 0.01))
    stats = {"fg_share": round(area / (W * H), 3), "ragged": round(ragged, 2), "thin": round(thin, 3),
             "jump": round(jump, 2), "fg_parts": len(contours)}
    return plate, plate_depth, alpha, fg_depth, stats


def guard(stats, amp):
    """Quality decision: (mode, amp, reason). mode = parallax | zoom. Thin parts (feathers, hair, the walking
    stick) at a big depth jump are where 2.5D shows artifacts, so motion is cut there first."""
    if not (FG_MIN <= stats["fg_share"] <= FG_MAX):
        return "zoom", 0.0, f"foreground share {stats['fg_share']} outside {FG_MIN}-{FG_MAX}"
    risk = stats["thin"] * max(stats["jump"], 0.0)
    if risk >= RISK_FALLBACK:
        return "zoom", 0.0, f"thin parts {stats['thin']} at depth jump {stats['jump']} (risk {risk:.3f})"
    if stats["jump"] >= JUMP_FALLBACK:
        return "zoom", 0.0, f"depth jump {stats['jump']} at the foreground edge (smear risk)"
    if stats["jump"] >= JUMP_HALF:
        return "parallax", amp / 2, f"depth jump {stats['jump']}: motion halved"
    if risk >= RISK_HALF:
        return "parallax", amp / 2, f"thin parts {stats['thin']} at depth jump {stats['jump']}: motion halved"
    return "parallax", amp, "ok"


# ---------- motion ----------
def ease(p):
    return 0.5 - 0.5 * math.cos(math.pi * min(1.0, max(0.0, p)))


def motion(preset, p, amp):
    """(zoom, dx, dy) for the NEAREST depth (d = 1); depth d moves (0.5 + 0.5 d) of it, so the far background
    moves half as much as the foreground. zoom = extra scale, dx/dy = fraction of the frame width/height."""
    e, a = ease(p), amp
    if preset == "push_in":
        return 2 * a * e, 0, 0
    if preset == "pull_out":
        return 2 * a * (1 - e), 0, 0
    if preset == "pan_right":    # camera moves right -> the scene slides left
        return 0, a * (0.5 - e), 0
    if preset == "pan_left":
        return 0, a * (e - 0.5), 0
    if preset == "gentle_orbit":
        th = math.pi * (e - 0.5)
        return a * 0.4 * math.cos(th), a * 0.5 * math.sin(th), 0
    if preset == "static_breathe":
        s = 0.5 - 0.5 * math.cos(2 * math.pi * p)
        return a * 0.5 * s, 0, -a * 0.15 * s
    raise ValueError(preset)


def kenburns(p):  # the old make_short "in" move: 1 -> 1.08 centred, linear
    return 1 + 0.08 * p


def choose_preset(mood, previous=None):
    for pr in MOOD_PRESETS.get(mood or "", PRESETS):
        if pr != previous:
            return pr
    return next(pr for pr in PRESETS if pr != previous)


def _warp(src, scale, dx, dy, W, H):
    """Rigid move of an overscanned layer: scale about its centre, shift, crop the centre W x H."""
    sh, sw = src.shape[:2]
    s = scale
    M = np.float32([[s, 0, (1 - s) * sw / 2 + dx * W - (sw - W) / 2],
                    [0, s, (1 - s) * sh / 2 + dy * H - (sh - H) / 2]])
    return cv2.warpAffine(src, M, (W, H), flags=cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)


class DepthWarp:
    """Per-pixel move: depth d gets zoom*(0.5+0.5d) and shift*(0.5+0.5d) (inverse map). The map is computed on a
    grid R times coarser and resized up (the move is smooth, so this is exact enough and ~10x faster)."""
    R = 4

    def __init__(self, depth, W, H):
        sh, sw = depth.shape
        self.W, self.H = W, H
        self.cx, self.cy = sw / 2, sh / 2
        oy, ox = (sh - H) // 2, (sw - W) // 2
        k = 0.5 + 0.5 * depth[oy:oy + H, ox:ox + W]
        self.k_full = k.astype(np.float32)
        w, h = W // self.R, H // self.R
        self.k = cv2.resize(self.k_full, (w, h), interpolation=cv2.INTER_AREA)
        u, v = np.meshgrid(np.linspace(0, W - 1, w, dtype=np.float32), np.linspace(0, H - 1, h, dtype=np.float32))
        self.u = u + (sw - W) / 2 - self.cx  # output pixel in source coords, relative to the centre
        self.v = v + (sh - H) / 2 - self.cy

    def maps(self, z, dx, dy):
        s = 1 + z * self.k
        mx = (self.u - dx * self.W * self.k) / s + self.cx
        my = (self.v - dy * self.H * self.k) / s + self.cy
        up = lambda m: cv2.resize(m, (self.W, self.H), interpolation=cv2.INTER_LINEAR)
        return up(mx), up(my)


# ---------- ambient overlays (generated, never downloaded) ----------
class Overlay:
    """kind: fireflies | dust | rain | diya; opacity 0.15-0.35. Particles stay in 5-75% height (captions below)."""

    def __init__(self, kind, opacity, W, H, frames, at=(0.5, 0.6), seed=7):
        self.kind, self.op, self.W, self.H, self.n = kind, min(0.35, max(0.15, opacity)), W, H, frames
        self.at = at
        r = np.random.default_rng(seed)
        cnt = {"fireflies": 28, "dust": 70, "rain": 160, "diya": 0}[kind]
        self.p = r.random((cnt, 2)) * [W, H * 0.70] + [0, H * 0.05]
        self.ph = r.random(cnt) * 2 * math.pi
        self.sp = 0.5 + r.random(cnt)
        self.sprite = {}
        for rad in (3, 5, 9):
            g = cv2.getGaussianKernel(rad * 6 + 1, rad)
            self.sprite[rad] = (g @ g.T) / (g @ g.T).max()

    def _blob(self, layer, x, y, rad, color, a):
        s = self.sprite[rad]
        k = s.shape[0] // 2
        x, y = int(x), int(y)
        y0, y1, x0, x1 = max(0, y - k), min(self.H, y + k + 1), max(0, x - k), min(self.W, x + k + 1)
        if y0 >= y1 or x0 >= x1:
            return
        sub = s[y0 - (y - k):y1 - (y - k), x0 - (x - k):x1 - (x - k)][..., None] * a
        layer[y0:y1, x0:x1] += sub * np.float32(color)

    def apply(self, frame, i):
        t = i / FPS
        W, H = self.W, self.H
        add = np.zeros((H, W, 3), np.float32)
        if self.kind == "fireflies":
            for (x, y), ph, sp in zip(self.p, self.ph, self.sp):
                xx = x + 30 * math.sin(t * 0.6 * sp + ph) * W / 1920
                yy = y + 18 * math.sin(t * 0.9 * sp + ph * 1.7) * H / 1080
                fl = 0.55 + 0.45 * math.sin(t * 3.1 * sp + ph)
                self._blob(add, xx, yy, 9, (120, 255, 230), 0.6 * fl)   # BGR warm yellow-green glow
                self._blob(add, xx, yy, 3, (200, 255, 255), fl)
        elif self.kind == "dust":
            for (x, y), ph, sp in zip(self.p, self.ph, self.sp):
                xx = (x + 12 * t * sp) % W
                yy = H * 0.05 + ((y - H * 0.05 - 8 * t * sp) % (H * 0.70))
                self._blob(add, xx, yy, 3, (230, 240, 255), 0.5 + 0.3 * math.sin(t * sp + ph))
        elif self.kind == "rain":
            ln = np.zeros((H, W), np.uint8)
            for (x, y), sp in zip(self.p, self.sp):
                yy = (y + 900 * t * sp) % H
                xx = (x - 120 * t * sp) % W
                cv2.line(ln, (int(xx), int(yy)), (int(xx - 6), int(yy + 28 * sp)), 255, 1, cv2.LINE_AA)
            add += (ln.astype(np.float32)[..., None] / 255) * np.float32((235, 225, 215))
        elif self.kind == "diya":
            cx, cy = self.at[0] * W, self.at[1] * H
            fl = 0.8 + 0.12 * math.sin(t * 7.3) + 0.08 * math.sin(t * 13.1 + 1.3)
            yy, xx = np.ogrid[:H, :W]
            r2 = ((xx - cx) ** 2 + (yy - cy) ** 2) / (0.22 * W) ** 2
            glow = np.exp(-r2).astype(np.float32) * fl
            add += glow[..., None] * np.float32((80, 170, 255))  # warm orange
        out = frame.astype(np.float32) + add * self.op
        return np.clip(out, 0, 255).astype(np.uint8)


# ---------- render ----------
_IMG = {}


def _image(path):
    path = str(path)
    if path not in _IMG:
        _IMG[path] = cv2.imread(path, cv2.IMREAD_COLOR)
    return _IMG[path]


def shot_rect(iw, ih, aspect, cx=0.5, cy=0.5, fx=0.5, fy=0.5, zc=1.0):
    """Source rectangle (x0, y0, w, h) of one shot, exactly like make_short's zoom: a frame-shaped window on the
    image centred on (cx, cy), then a 1/zc part of it centred on (fx, fy) inside that window."""
    cw, ch = min(iw, ih * aspect), min(ih, iw / aspect)
    wx0 = max(0.0, min(iw - cw, cx * iw - cw / 2))
    wy0 = max(0.0, min(ih - ch, cy * ih - ch / 2))
    rw, rh = cw / zc, ch / zc
    return (wx0 + max(0.0, min(cw - rw, fx * cw - rw / 2)), wy0 + max(0.0, min(ch - rh, fy * ch - rh / 2)), rw, rh)


def _source(img_path, W, H, cx=0.5, cy=0.5, rect=None):
    """Image (BGR) and its depth for one shot rectangle, resized to the overscanned frame size."""
    img = _image(img_path)
    dep = depth_map(img_path)
    ih, iw = img.shape[:2]
    x0, y0, w, h = rect or shot_rect(iw, ih, W / H, cx, cy)
    x0, y0, x1, y1 = int(round(x0)), int(round(y0)), int(round(x0 + w)), int(round(y0 + h))
    sw, sh = int(round(W * OVERSCAN)), int(round(H * OVERSCAN))
    return (cv2.resize(img[y0:y1, x0:x1], (sw, sh), interpolation=cv2.INTER_LANCZOS4),
            cv2.resize(dep[y0:y1, x0:x1], (sw, sh), interpolation=cv2.INTER_LINEAR))


def shot_frames(img_path, W, H, n, preset="push_in", rect=None, amp=AMP, mode="auto", overlays=(), cx=0.5, cy=0.5):
    """(frame generator, info). mode: auto (quality guard) | parallax | zoom. Motion longer than MAX_SECONDS
    becomes a slow static_breathe (one shot never runs a big move for more than 8 s)."""
    img, dep = _source(Path(img_path), W, H, cx, cy, rect)
    if n > MAX_SECONDS * FPS:
        preset = "static_breathe"
    plate = pdepth = alpha = fgd = None
    if mode == "zoom":
        decision, use_amp, reason, stats = "zoom", 0.0, "zoom mode", {}
    else:
        plate, pdepth, alpha, fgd, stats = layers(img, dep)
        decision, use_amp, reason = guard(stats, amp) if mode == "auto" else (mode, amp, "forced")
    ovs = [Overlay(k, o, W, H, n, at) for k, o, at in overlays]

    def gen():
        if decision != "zoom":
            bw, fw = DepthWarp(pdepth, W, H), DepthWarp(fgd, W, H)
        for i in range(n):
            p = i / max(1, n - 1)
            if decision == "zoom":
                frame = _warp(img, kenburns(p), 0, 0, W, H)
            else:
                z, dx, dy = motion(preset, p, use_amp)
                mx, my = bw.maps(z, dx, dy)
                bg = cv2.remap(plate, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
                mx, my = fw.maps(z, dx, dy)
                fg = cv2.remap(img, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
                al = cv2.remap(alpha, mx, my, cv2.INTER_LINEAR, borderMode=cv2.BORDER_REFLECT)
                frame = cv2.blendLinear(fg, bg, al, 1 - al)
            for ov in ovs:
                frame = ov.apply(frame, i)
            yield frame

    return gen(), {"preset": preset, "mode": decision, "amp": round(use_amp, 4), "reason": reason, **stats}


def log(entry):
    with LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps({**entry, "time": time.strftime("%Y-%m-%d %H:%M:%S")}, ensure_ascii=False) + "\n")


# ---------- crop safety (Shorts) ----------
def safe_rect(iw, ih, aspect, cx, cy, fx, fy, zc, box, keep=(0.03, 0.85)):
    """Crop safety: box = the subject (face, hands, a pointing arm) as [x0, y0, x1, y1], fractions of the image,
    from shots.json "subjects". Its part inside the shot's rows must sit in keep[0]-keep[1] of the crop width
    (Shorts: the right 15% has the YouTube buttons). Otherwise the crop centre moves; if it still does not fit,
    the shot zooms out (smaller zc, down to 1). Returns (cx, fx, zc, note)."""
    x0, y0, w, h = shot_rect(iw, ih, aspect, cx, cy, fx, fy, zc)
    sx0, sx1 = box[0] * iw, box[2] * iw

    def fits(rx0, rw):
        return sx0 >= rx0 + keep[0] * rw - 1 and sx1 <= rx0 + keep[1] * rw + 1

    if fits(x0, w):
        return cx, fx, zc, "ok"
    steps = [zc] + [z for z in (zc * 0.85, zc * 0.7, zc * 0.55) if z > 1.0] + ([1.0] if zc > 1.0 else [])
    for z in steps:
        rw = w * zc / z
        want = (sx0 + sx1) / 2 - (keep[0] + keep[1]) / 2 * rw  # subject centre in the middle of the keep range
        rx0 = max(0.0, min(iw - rw, want))
        if fits(rx0, rw) or z == steps[-1]:
            ncx = (rx0 + rw / 2) / iw
            # the window at zc=1 is centred on ncx; fx 0.5 keeps the zoomed part centred in it
            return ncx, 0.5, z, (f"centre {cx:.2f}->{ncx:.2f}" + (f", zoom {zc:.2f}->{z:.2f}" if z != zc else "")
                                 + ("" if fits(rx0, rw) else " (subject wider than the safe area: best fit)"))
    return cx, fx, zc, "unchanged"


def render_clip(img_path, out, seconds=6.0, preset="push_in", fmt="long", cx=0.5, cy=0.5, amp=AMP,
                overlays=(), mode="auto", crf=18, enc_preset="slow"):
    """Stand-alone test clip. mode: auto (parallax with the quality guard) | parallax (no guard) | zoom."""
    t_start = time.process_time()
    w0 = time.time()
    W, H = FORMATS[fmt]
    n = max(1, round(min(float(seconds), MAX_SECONDS) * FPS))
    frames, info = shot_frames(img_path, W, H, n, preset, None, amp, mode, overlays, cx, cy)
    enc = _encoder(out, W, H, crf, enc_preset)
    for f in frames:
        enc.stdin.write(f.tobytes())
    enc.stdin.close()
    enc.wait()
    res = {"image": str(img_path), "out": str(out), "format": fmt, "seconds": round(n / FPS, 2), **info,
           "overlays": [k for k, _, _ in overlays], "cpu_s": round(time.process_time() - t_start, 1),
           "wall_s": round(time.time() - w0, 1)}
    log(res)
    return res


def _overlay_arg(s):
    kind, rest = s.split(":", 1)
    op, _, at = rest.partition("@")
    xy = tuple(float(v) for v in at.split(",")) if at else (0.5, 0.6)
    return kind, float(op), xy


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("cmd", choices=["clip", "depth"])
    ap.add_argument("image")
    ap.add_argument("out", nargs="?")
    ap.add_argument("--preset", default="push_in", choices=PRESETS)
    ap.add_argument("--seconds", type=float, default=6.0)
    ap.add_argument("--format", default="long", choices=list(FORMATS))
    ap.add_argument("--cx", type=float, default=0.5)
    ap.add_argument("--cy", type=float, default=0.5)
    ap.add_argument("--amp", type=float, default=AMP)
    ap.add_argument("--mode", default="auto", choices=["auto", "parallax", "zoom"])
    ap.add_argument("--overlay", action="append", default=[], type=_overlay_arg)
    a = ap.parse_args()
    if a.cmd == "depth":
        t = time.time()
        d = depth_map(Path(a.image))
        print(f"depth {d.shape} in {time.time() - t:.1f}s")
        return
    print(json.dumps(render_clip(a.image, a.out, a.seconds, a.preset, a.format, a.cx, a.cy, a.amp, a.overlay, a.mode),
                     ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
