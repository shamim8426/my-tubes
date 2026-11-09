"""Reality Check - Asli: REAL-FOOTAGE look for the Long (called by rc_build_long.py --look real, the default).

Per shot (from long/footage_map.md): REAL = full-bleed real clip/photo; REAL-BG = real clip darkened + softly blurred with a SMALL lower-third
card / chart on top; gap shots (21, 61, 111, 112, 141) = free AI still (Cloudflare flux, Rs0, long/ai_stills/) with parallax and an
'AI illustration' label. Stills never stand still: tools/parallax.py clip (REAL stills) or an eased push + drift, plus drifting dust.
Shots > 7 s are cut into 2-3 sub-cuts (different time windows / crops, opposite push direction), 6-frame crossfades inside, 8-frame crossfade
between shots (hard cut for shots < 3.5 s). Finishing in ffmpeg per shot: curves (teal shadows / warm highlights), contrast 1.1, soft vignette,
film grain, then the ASS text (not graded). Credit chip bottom-left, 70 percent opacity, first 4 s of every real shot. On-screen text: Roman only.
Cuts (script/cuts.json): skipped lines are absent from the timing, holds extend the previous shot (footage plays with its own sound).
"""
import json
import math
import re
import subprocess
import sys
import time
import wave
from multiprocessing import Pool
from pathlib import Path

import cv2
import numpy as np

import rc_build_long as B

W, H, FPS = B.W, B.H, B.FPS
VER = "r4"
AI_SHOTS = (21, 24, 26, 61, 111, 112, 141)
PLX_SEC = 8.0
KEEP_REAL = {"orbit", "bar", "path", "flash", "tl", "chart", "txt"}
BAD_CREDIT = ("NEEDS USER OK", "CO-CREDIT")


# ---------------------------------------------------------------- map / licence
def parse_map(ld):
    rows = {}
    for line in (ld / "footage_map.md").read_text(encoding="utf-8").splitlines():
        if not line.startswith("| "):
            continue
        c = [x.strip() for x in line.strip().strip("|").split("|")]
        if not c[0].isdigit() or len(c) < 7:
            continue
        rows[int(c[0])] = dict(status=c[1], file=c[2], tin=c[3], tout=c[4], treat=c[5], credit=c[6], note=c[7] if len(c) > 7 else "")
    return rows


def review_set(ld):
    bad = set()
    for lf, base in ((ld / "footage2/LICENSE_LOG.md", "footage2"), (ld / "footage/LICENSE_LOG.md", "footage")):
        if lf.exists():
            for line in lf.read_text(encoding="utf-8").splitlines():
                if line.startswith("|") and ("REVIEW" in line or "co-credit" in line or "USER-OK" in line):
                    first = line.strip("|").split("|")[0].strip()
                    bad.add(f"{base}/{first}")
    return bad


# ---------------------------------------------------------------- cuts -> proof timing + voice
def apply_cuts(sd, cdir, span):
    """Draft timing + cuts.json -> proof timing/voice (first `span` s). Gap between present lines = original gap (0.45 if the next line was skipped)."""
    cuts = json.loads((sd / "script/cuts.json").read_text(encoding="utf-8"))
    skip = set(cuts.get("skip_lines", []))
    hold = {int(k): float(v) for k, v in cuts.get("hold_after", {}).items()}
    lines = json.loads((sd / "audio/voiceover_draft_timing.json").read_text(encoding="utf-8"))
    wf = wave.open(str(sd / "audio/voiceover_draft_mixed.wav"), "rb")
    sr, ch, sw = wf.getframerate(), wf.getnchannels(), wf.getsampwidth()
    raw = np.frombuffer(wf.readframes(wf.getnframes()), np.int16).reshape(-1, ch)
    out_t, chunks, t = [], [], 0.0
    pres = [l for l in lines if l["line"] not in skip]
    for i, l in enumerate(pres):
        a, b = int(l["start"] * sr), int(l["end"] * sr)
        seg = raw[a:b]
        d = (b - a) / sr
        out_t.append(dict(l, start=round(t, 3), end=round(t + d, 3), orig_start=l["start"]))
        chunks.append((t, seg))
        nxt = pres[i + 1] if i + 1 < len(pres) else None
        gap = (nxt["start"] - l["end"]) if nxt and nxt["line"] == l["line"] + 1 else 0.45
        t = t + d + max(gap, 0.3) + hold.get(l["line"], 0.0)
        if t > span + 6:
            break
    total = out_t[-1]["end"] + 0.4
    buf = np.zeros((int(total * sr) + sr, ch), np.int16)
    for st, seg in chunks:
        a = int(st * sr)
        buf[a:a + len(seg)] = seg[: len(buf) - a]
    cdir.mkdir(parents=True, exist_ok=True)
    vp = cdir / "proof_voice.wav"
    w = wave.open(str(vp), "wb")
    w.setnchannels(ch)
    w.setsampwidth(sw)
    w.setframerate(sr)
    w.writeframes(buf[: int(total * sr)].tobytes())
    w.close()
    tp = cdir / "proof_timing.json"
    tp.write_text(json.dumps(out_t, ensure_ascii=False, indent=1), encoding="utf-8")
    return tp, vp


# ---------------------------------------------------------------- sources
def soft(img):
    sm = cv2.resize(img, (800, 450), interpolation=cv2.INTER_AREA)
    sm = cv2.GaussianBlur(sm, (0, 0), 1.6)
    return cv2.convertScaleAbs(cv2.resize(sm, (W, H), interpolation=cv2.INTER_LINEAR), alpha=0.66)


class VidSrc:
    def __init__(self, path, tin, tout, speed, z0, z1, off, dur, crop=None, exact=False):
        self.f = B.Footage(path)
        cd = self.f.nfr / self.f.fps if self.f.fps else 10.0
        self.tin = tin if tin < cd - 1 else 0.0
        if exact:
            self.span = max(1.0, min(cd - self.tin, tout - self.tin))
        else:
            self.span = max(1.0, min(cd - self.tin, max(tout - self.tin, 10.0)))
        self.speed, self.z0, self.z1, self.off, self.dur = speed, z0, z1, off, max(dur, 0.1)
        self.crop = crop

    def get(self, t):
        tt = self.tin + ((t * self.speed + self.off) % self.span)
        z = self.z0 + (self.z1 - self.z0) * B.clamp(t / self.dur)
        fr = self.f.raw(tt)
        if self.crop:
            h, w = fr.shape[:2]
            x0, y0, x1, y1 = self.crop
            fr = fr[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)]
        return B.place_footage(fr, "cover", z, 800, 960, 540)


class StillSrc:
    def __init__(self, path, k, dur):
        img = cv2.imread(str(path))
        if img.shape[1] > 2600:
            sc = 2600 / img.shape[1]
            img = cv2.resize(img, None, fx=sc, fy=sc, interpolation=cv2.INTER_AREA)
        self.img = img
        self.dur = max(dur, 0.1)
        self.k = k
        self.fx, self.fy = [(0.5, 0.5), (0.36, 0.42), (0.64, 0.58)][k % 3]
        self.dir = 1 if k % 2 == 0 else -1

    def get(self, t):
        h, w = self.img.shape[:2]
        p = B.ease(t / self.dur)
        z = 1.10 + 0.08 * (p if self.dir > 0 else 1 - p)
        sc = max(W / w, H / h) * z
        iw, ih = w * sc, h * sc
        drift = (p - 0.5) * 0.04 * self.dir
        tx = B.clamp(W / 2 - (self.fx + drift) * iw, W - iw, 0)
        ty = B.clamp(H / 2 - (self.fy - drift * 0.5) * ih, H - ih, 0)
        M = np.float32([[sc, 0, tx], [0, sc, ty]])
        return cv2.warpAffine(self.img, M, (W, H), flags=cv2.INTER_LINEAR)


def dust(im, t):
    for x, y, r, ph, sp in B.bg_layers()["motes"]:
        px = (x + t * sp * 0.9) % W
        py = (y - t * sp * 0.5 + 12 * math.sin(t * 0.8 + ph)) % H
        B.circ(im, px, py, r * 0.9, B.mix((255, 240, 220), 0.12 + 0.08 * math.sin(t + ph) + 0.1), -1) if False else B.glow(im, px, py, int(r * 4), (255, 240, 220), 0.10)


# ---------------------------------------------------------------- shot context
def load_overrides(ld):
    f = ld / "footage_overrides.json"
    if not f.exists():
        return {}
    return {int(k): v for k, v in json.loads(f.read_text(encoding="utf-8")).items() if k.isdigit()}


def cdir_of(ld):
    return B.ROOT / "cache/reality-check" / Path(ld).parent.name[:3]


def cropped_still(path, crop, ld):
    """Still with a content crop (fractions x0,y0,x1,y1) saved as a file so parallax/StillSrc can use it."""
    if not crop:
        return shrunk_still(path, ld)
    tag = B.hashlib.sha1((str(path) + json.dumps(crop)).encode()).hexdigest()[:8]
    out = cdir_of(ld) / "crops" / f"{path.stem}_{tag}.jpg"
    if not out.exists():
        out.parent.mkdir(parents=True, exist_ok=True)
        img = cv2.imread(str(path))
        h, w = img.shape[:2]
        x0, y0, x1, y1 = crop
        cv2.imwrite(str(out), img[int(y0 * h):int(y1 * h), int(x0 * w):int(x1 * w)], [cv2.IMWRITE_JPEG_QUALITY, 95])
    return out


def shrunk_still(path, ld, maxdim=6000):
    """Huge scans (up to 27000 px) are shrunk once into the cache (PIL decompression-bomb limit, memory)."""
    if path.suffix.lower() not in (".jpg", ".jpeg", ".png"):
        return path
    from PIL import Image
    Image.MAX_IMAGE_PIXELS = None
    with Image.open(path) as im0:
        w, h = im0.size
        if max(w, h) <= maxdim:
            return path
        out = cdir_of(ld) / "crops" / f"{path.stem}_s{maxdim}.jpg"
        if not out.exists():
            out.parent.mkdir(parents=True, exist_ok=True)
            sc = maxdim / max(w, h)
            im = im0.convert("RGB").resize((max(1, int(w * sc)), max(1, int(h * sc))), Image.LANCZOS)
            im.save(out, quality=95)
    return out


def plx_path(img, preset, ld):
    return cdir_of(ld) / "parallax" / f"{img.stem}_{preset}_{PLX_SEC:.1f}.mp4"


def resolve_segs(n, mrow, ov, ld, bad, dur):
    """-> (status, [seg dict: path, isvid, tin, tout, speed, z0, z1, crop, credit, ai, exact, still_img, preset, off])."""
    status = (ov.get("status") if ov else None) or (mrow["status"] if mrow else "NONE")
    video_ext = (".mp4", ".mov", ".webm")
    out = []
    if ov and ov.get("segs"):
        for k, sg in enumerate(ov["segs"]):
            path = ld / sg["file"]
            isvid = path.suffix.lower() in video_ext
            crop = sg.get("crop")
            d = dict(path=path, isvid=isvid, tin=float(sg.get("tin", 0)), tout=float(sg.get("tout", sg.get("tin", 0) + 8)), speed=float(sg.get("speed", 1.0)),
                     z0=float(sg.get("z0", 1.0)), z1=float(sg.get("z1", 1.06)), crop=crop if isvid else None, credit=sg.get("credit", ""), ai=bool(sg.get("ai")),
                     exact=True, off=0.0, still_img=None, preset=sg.get("preset", "push_in" if k % 2 == 0 else "pull_out"))
            if not isvid:
                d["still_img"] = cropped_still(path, crop, ld)
            if d["z1"] < d["z0"] and isvid:
                pass
            out.append(d)
        return status, out
    ai = None
    if n in AI_SHOTS and (ld / f"ai_stills/shot_{n:03d}.png").exists():
        ai = ld / f"ai_stills/shot_{n:03d}.png"
    path, credit = None, ""
    if ai:
        path, credit, status = ai, "", "REAL"
    elif mrow and mrow["file"] not in ("-", ""):
        cand = ld / mrow["file"]
        if cand.exists() and mrow["file"] not in bad and not any(b in mrow["credit"] for b in BAD_CREDIT):
            path, credit = cand, mrow["credit"]
    nseg = max(1, math.ceil(dur / 5.5))
    isvid = bool(path) and path.suffix.lower() in video_ext
    m = re.search(r"slow-mo (\d+)%", mrow["treat"]) if mrow else None
    speed = int(m.group(1)) / 100.0 if m else 1.0
    m = re.search(r"(\d\.\d\d)->(\d\.\d\d)", mrow["treat"]) if mrow else None
    z0, z1 = (float(m.group(1)), float(m.group(2))) if m else (1.0, 1.05)
    tin = float(mrow["tin"]) if mrow and re.match(r"^[\d.]+$", mrow["tin"]) else 0.0
    tout = float(mrow["tout"]) if mrow and re.match(r"^[\d.]+$", mrow["tout"]) else tin + 7.5
    for k in range(nseg):
        a, b2 = (z0, z1) if k % 2 == 0 else (z1 + 0.03, z0)
        out.append(dict(path=path, isvid=isvid, tin=tin, tout=tout, speed=speed, z0=a, z1=b2, crop=None, credit=credit if k == 0 else "", ai=bool(ai), exact=False,
                        off=0.0, still_img=(shrunk_still(path, ld) if (path and not isvid) else None), preset="push_in", k=k))
    return status, out


def build_ctx(n, spec, mrow, nfr, ld, plx, ai_ok, bad, ov=None):
    dur = nfr / FPS
    status, descs = resolve_segs(n, mrow, ov, ld, bad, dur)
    nseg = len(descs)
    segs, credits = [], []
    for k, d in enumerate(descs):
        t0, t1 = dur * k / nseg, dur * (k + 1) / nseg
        sd = t1 - t0
        if d["path"] is None:
            src = None
        elif d["isvid"]:
            off = 0.0 if d["exact"] else (t0 * d["speed"] + k * 0.37 * 8.0)
            src = VidSrc(d["path"], d["tin"], d["tout"], d["speed"], d["z0"], d["z1"], off, sd, d["crop"], d["exact"])
        else:
            pc = plx.get((n, k))
            if pc and Path(pc).exists():
                src = VidSrc(Path(pc), 0.0, PLX_SEC, 1.0, 1.0, 1.0, 0.0, sd)
            else:
                src = StillSrc(d["still_img"], k, sd)
        segs.append((t0, t1, src, d["path"] is not None and not d["isvid"]))
        if d["credit"] and d["path"] is not None:
            credits.append((t0, d["credit"]))
    ai = any(d["ai"] for d in descs)
    bgmode = status == "REAL-BG"
    return dict(segs=segs, bg=bgmode, credits=credits, ai=ai, real=any(d["path"] is not None for d in descs), dur=dur, status=status)


def seg_frame(ctx, t, upto=None):
    segs = ctx["segs"]
    k = len(segs) - 1
    for i, (t0, t1, src, still) in enumerate(segs):
        if t < t1:
            k = i
            break
    t0, t1, src, still = segs[k]
    if src is None:
        return None, False
    fr = src.get(t - t0)
    if ctx["bg"]:
        fr = soft(fr)
    xf = 0.2
    if k > 0 and t - t0 < xf and segs[k - 1][2] is not None:
        t0p, t1p, sp, st2 = segs[k - 1]
        pf = sp.get(t - t0p)
        if ctx["bg"]:
            pf = soft(pf)
        a = (t - t0) / xf
        fr = cv2.addWeighted(pf, 1 - a, fr, a, 0)
    return fr, still


VF_GRADE = ("curves=r='0/0 0.3/0.275 0.7/0.735 1/1':g='0/0.012 0.3/0.305 0.7/0.70 1/0.99':b='0/0.045 0.3/0.335 0.7/0.665 1/0.95',"
            "eq=contrast=1.1:saturation=1.06,vignette=PI/6:eval=init,noise=alls=7:allf=t")


def render_real(args):
    (n, spec, mrow, nfr, out, prev, ld_s, plx, bad, ov) = args
    out = Path(out)
    if out.exists():
        return n, 0.0, "cached"
    t_start = time.time()
    ld = Path(ld_s)
    dur = nfr / FPS
    if ov and ov.get("scene"):   # own animated explainer scene (tools/rc_explain.py), no real-footage pipeline
        import rc_explain as E
        return E.render(n, nfr, out, ov["scene"], ld_s, VF_GRADE)
    ctx = build_ctx(n, spec, mrow, nfr, ld, plx, True, bad, ov)
    pctx = None
    if prev and not (prev[4] and prev[4].get("scene")):
        pn, pspec, pmrow, pnfr, pov = prev
        pctx = build_ctx(pn, pspec, pmrow, pnfr, ld, plx, True, bad, pov)
    xf_fr = 0 if dur < 3.5 else 8
    spec = dict(spec)
    status = ctx["status"]
    if ctx["real"]:
        spec["lay"] = "ll" if spec.get("lay", "c") == "c" else spec.get("lay")
        spec["pscale"] = 0.62 if spec["lay"] == "ll" else 0.78
        if status == "REAL":
            spec["g"] = [e for e in spec.get("g", []) if e[0] in KEEP_REAL]
        else:
            spec["g"] = [e for e in spec.get("g", []) if e[0] not in ("city", "field", "crack", "streaks")]
    T = list(spec.get("T", []))
    spec["T"] = T
    placed = B.layout(spec, dur)
    # panels behind stacked text
    panels = {}
    for d in placed:
        if d.get("fixed") or "xy" in d:
            continue
        x0, x1 = d["x"] - d["w"] / 2 - d["pad"], d["x"] + d["w"] / 2 + d["pad"]
        y0, y1 = d["y"] - d["h"] / 2, d["y"] + d["h"] / 2
        pn_ = panels.setdefault(d["reg"], [x0, y0, x1, y1, d["at"], d["out"]])
        pn_[0], pn_[1], pn_[2], pn_[3] = min(pn_[0], x0), min(pn_[1], y0), max(pn_[2], x1), max(pn_[3], y1)
        pn_[4] = min(pn_[4], d["at"])
        pn_[5] = max(pn_[5], d["out"])
    labs, elist = [], []
    for e in spec.get("g", []):
        kind, ex, ey, es, o = e
        ax, ay = ex, ey
        if kind == "bar":
            if o.get("lab"):
                labs.append(dict(text=o["lab"], x=ax - es / 2, y=ay - o.get("h", 44) / 2 - 30, px=o.get("lpx", 38) * 0.85, font="M", c=o.get("lc", "ink"), an=4, at=o.get("at", .3), out=dur))
        for lb in o.get("labs", []):
            txt, dx, dy = lb[0], lb[1], lb[2]
            px = (lb[4] if len(lb) > 4 else 38) * 0.85
            labs.append(dict(text=txt, x=ax + dx, y=ay + dy, px=px, font="M", c=lb[3] if len(lb) > 3 else "ink", an=lb[6] if len(lb) > 6 else 5,
                             at=max(lb[5] if len(lb) > 5 else o.get("at", 0.3) + 0.4, 0), out=dur))
        if kind != "txt":
            elist.append((kind, ax, ay, es, o))
    lab_chips = []   # dark rounded panels behind the loose labels (bar / chart numbers)
    for lb in labs:
        if lb.get("fixed") or not lb.get("text"):
            continue
        w_ = B.tw(lb["text"], lb["font"], lb["px"])
        hh = lb["px"] * 1.3
        an = lb.get("an", 5)
        x0_ = lb["x"] - w_ / 2 if an == 5 else (lb["x"] if an == 4 else lb["x"] - w_)
        lab_chips.append((x0_ - 14, lb["y"] - hh / 2 - 4, x0_ + w_ + 14, lb["y"] + hh / 2 + 4, max(lb["at"], 0.0)))
    chips = []   # small credit chips: (text, x0, y_center, at, out)
    nxt_starts = [c[0] for c in ctx["credits"]] + [dur]
    for i, (ct0, ctext) in enumerate(ctx["credits"]):
        at, out_ = ct0 + 0.2, min(ct0 + 4.2, nxt_starts[i + 1] - 0.05)
        labs.append(dict(text=ctext, x=84, y=1048, px=24, font="M", c=(235, 235, 235), an=4, at=at, out=out_, fixed="credit", alpha="00"))
        chips.append((70, 1048, B.tw(ctext, "M", 24) + 28, at, out_))
    if ctx["ai"]:
        labs.append(dict(text="AI illustration", x=1850, y=1048, px=26, font="M", c=(235, 235, 235), an=6, at=0.0, out=dur, fixed="credit", alpha="00"))
        chips.append((1850 - B.tw("AI illustration", "M", 26) - 14, 1048, B.tw("AI illustration", "M", 26) + 28, 0.0, dur))
    for lb in labs:
        lb.setdefault("fixed", None)
        lb.setdefault("kind", "L")
        lb.setdefault("alpha", None)
    assf = out.with_suffix(".ass")
    assf.write_text(B.ass_file(B.ass_events(placed, labs, dur)), encoding="utf-8")
    ff = B.find_ff()
    fonts = (B.ROOT / "shared/fonts").as_posix().replace(":", "\\:")
    tmp = out.with_name(out.stem + ".part.mp4")
    p = subprocess.Popen([ff, "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-",
                          "-vf", f"{VF_GRADE},subtitles=filename={assf.name}:fontsdir='{fonts}'", "-c:v", "libx264", "-preset", "veryfast", "-crf", "18",
                          "-pix_fmt", "yuv420p", "-g", "30", "-r", str(FPS), "-an", tmp.name], stdin=subprocess.PIPE, cwd=str(out.parent))
    im = np.empty((H, W, 3), np.uint8)
    tint = spec.get("tint")
    if tint:
        tint = dict(tint, c=B.C(tint["c"]))
    for f in range(nfr):
        t = f / FPS
        fr, still = seg_frame(ctx, t)
        if fr is None:
            B.draw_bg(im, t, n, tint)
        else:
            im[:] = fr
        if pctx and f < xf_fr:
            pf, _ = seg_frame(pctx, pctx["dur"] + t)
            if pf is not None:
                a = (f + 1) / (xf_fr + 1)
                im[:] = cv2.addWeighted(pf, 1 - a, im, a, 0)
        if still or ctx["ai"]:
            dust(im, t)
        for reg, (x0, y0, x1, y1, at, pout) in panels.items():
            a = B.ease((t - at) / 0.35) * (B.clamp((pout - t) / 0.3) if pout < dur else 1.0)
            B.rrect(im, x0 - 26, y0 - 18, x1 + 26, y1 + 18, 26, (8, 8, 14), 0.60 * a)
        for (cx0, cy0, cx1, cy1, cat) in lab_chips:
            a = B.ease((t - cat) / 0.35)
            if a > 0:
                B.rrect(im, cx0, cy0, cx1, cy1, 12, (8, 8, 14), 0.58 * a)
        for (cx, cy, cw, cat, cout) in chips:
            if cat <= t < cout:
                a = B.ease((t - cat) / 0.3) * B.clamp((cout - t) / 0.3)
                B.rrect(im, cx, cy - 22, cx + cw, cy + 22, 12, (8, 8, 14), 0.58 * a)
        for kind, ax, ay, es, o in elist:
            B.EL[kind](im, t, dur, ax, ay, es, o)
        B.draw_boxes(im, placed, t)
        p.stdin.write(im.tobytes())
    p.stdin.close()
    if p.wait():
        return n, 0.0, "ffmpeg failed"
    tmp.replace(out)
    assf.unlink(missing_ok=True)
    return n, time.time() - t_start, "ok"


def make_parallax(path, out, preset="push_in"):
    if Path(out).exists():
        return 0.0
    import os
    env = dict(os.environ, OMP_NUM_THREADS="2", MKL_NUM_THREADS="2", OPENBLAS_NUM_THREADS="2")
    tmp = Path(out).with_name(Path(out).stem + ".part.mp4")
    t = time.time()
    subprocess.run([sys.executable, "-X", "utf8", str(B.ROOT / "tools/parallax.py"), "clip", str(path), str(tmp), "--preset", preset, "--seconds", f"{PLX_SEC:.1f}"],
                   check=True, cwd=str(B.ROOT), env=env, stdout=subprocess.DEVNULL)
    tmp.replace(out)
    return time.time() - t


def parse_shots_arg(txt):
    keep = set()
    for part in str(txt).split(","):
        part = part.strip()
        if not part:
            continue
        if "-" in part:
            x, y = part.split("-")
            keep.update(range(int(x), int(y) + 1))
        else:
            keep.add(int(part))
    return keep


def still_jobs(n, mr, ov, ld, bad, dur):
    """-> {(n, k): (img, out_path, preset)} for the stills of this shot that get a depth-parallax clip."""
    res = {}
    if ov and ov.get("scene"):
        return res
    status, descs = resolve_segs(n, mr, ov, ld, bad, dur)
    for k, d in enumerate(descs):
        if d["still_img"] is None or d["path"] is None:
            continue
        if not (ov and ov.get("segs")) and k > 0:
            continue
        preset = d["preset"] if (ov and ov.get("segs")) else "push_in"
        res[(n, k)] = (d["still_img"], plx_path(d["still_img"], preset, ld), preset)
    return res


def prefetch_parallax(pend, workers):
    """pend: {out_path: (img, preset)}; run `workers` processes in parallel, cached."""
    from concurrent.futures import ThreadPoolExecutor
    todo = [(o, v) for o, v in pend.items() if not Path(o).exists()]
    print(f"parallax: {len(pend)} stills, {len(todo)} to make, {workers} parallel", flush=True)
    done = 0
    t0 = time.time()
    def one(item):
        o, (img, preset) = item
        try:
            return o, make_parallax(img, o, preset)
        except Exception as e:
            print(f"  parallax FAILED {Path(img).name}: {type(e).__name__}", flush=True)
            return o, -1
    with ThreadPoolExecutor(workers) as ex:
        for o, dt in ex.map(one, todo):
            done += 1
            print(f"  parallax {done}/{len(todo)} {Path(o).name}: {dt:.0f}s (elapsed {time.time() - t0:.0f}s)", flush=True)


def main_real(a, sd, ld):
    specs = {s["n"]: s for s in json.loads((ld / "shot_specs.json").read_text(encoding="utf-8"))}
    mp = parse_map(ld)
    bad = review_set(ld)
    ovs = load_overrides(ld)
    cdir = B.ROOT / "cache/reality-check" / a.story
    cdir.mkdir(parents=True, exist_ok=True)
    plxdir = cdir / "parallax"
    plxdir.mkdir(parents=True, exist_ok=True)
    if getattr(a, "plx_all", False):
        pend = {}
        for n in sorted(set(mp) | set(ovs) | set(AI_SHOTS)):
            for key, (img, out, preset) in still_jobs(n, mp.get(n), ovs.get(n), ld, bad, 6.0).items():
                pend[str(out)] = (img, preset)
        prefetch_parallax(pend, getattr(a, "plx_workers", 5))
        return
    span = a.seconds or 0
    if a.seconds:
        tfile, vfile = apply_cuts(sd, cdir, a.seconds)
    else:
        tfile = sd / "audio/voiceover_timing.json"
        if not tfile.exists():
            tfile = sd / "audio/voiceover_draft_timing.json"
        vfile = sd / "audio/voiceover_full.wav"
        if not vfile.exists():
            vfile = sd / "audio/voiceover_draft_mixed.wav"
    lines = json.loads(tfile.read_text(encoding="utf-8"))
    probe = subprocess.run([B.find_ff("ffprobe"), "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(vfile)], capture_output=True, text=True)
    adur = float(probe.stdout.strip())
    ends_voice = max(adur, lines[-1]["end"])
    starts = [0.0] + [l["start"] for l in lines[1:]]
    fb = [int(round(x * FPS)) for x in starts] + [int(round(ends_voice * FPS))]
    shots = [dict(n=l["line"], f0=fb[i], f1=fb[i + 1]) for i, l in enumerate(lines)]
    if not a.seconds:
        specs.setdefault(999, dict(n=999, lay="l", T=[], g=[]))
        shots.append(dict(n=999, f0=fb[-1], f1=fb[-1] + int(round(a.tail * FPS))))
    limit = int(a.seconds * FPS) if a.seconds else None
    cache = cdir / "real"
    cache.mkdir(parents=True, exist_ok=True)
    only = parse_shots_arg(a.shots) if a.shots else None
    jobs, order, plx, pend = [], [], {}, {}
    prev = None
    for s in shots:
        if limit is not None and s["f0"] >= limit:
            break
        f1 = s["f1"] if limit is None else min(s["f1"], limit)
        nfr = f1 - s["f0"]
        if nfr <= 0:
            continue
        n = s["n"]
        sp, mr, ov = specs[n], mp.get(n), ovs.get(n)
        for key, (img, out, preset) in still_jobs(n, mr, ov, ld, bad, nfr / FPS).items():
            plx[key] = str(out)
            pend[str(out)] = (img, preset)
        extra = ""
        for fp in ([ld / mr["file"]] if mr else []) + [ld / sg["file"] for sg in (ov or {}).get("segs", [])]:
            if fp.exists():
                extra += fp.name + str(fp.stat().st_mtime_ns)
        key = B.hashlib.sha1((VER + json.dumps(sp, sort_keys=True) + json.dumps(mr, sort_keys=True) + json.dumps(ov, sort_keys=True) + str(nfr) + extra
                              + (str(prev[3]) + json.dumps(prev[4], sort_keys=True) if prev else "")
                              + (__import__("rc_explain").scene_sig(ov["scene"]) if ov and ov.get("scene") else "")).encode()).hexdigest()[:10]
        out = cache / f"shot_{n:03d}_{key}.mp4"
        order.append(out)
        if only is None or n in only:
            jobs.append((n, sp, mr, nfr, str(out), prev, str(ld), plx, bad, ov))
        prev = (n, sp, mr, nfr, ov)
    keep = {p.name for p in order}
    if only is None:
        for p in cache.glob("shot_*.mp4"):
            if p.name not in keep and not p.name.endswith(".part.mp4") and a.seconds == 0:
                p.unlink()
    t0 = time.time()
    need = {}
    for j in jobs:
        if Path(j[4]).exists():
            continue
        for (n_, k_), pth in plx.items():
            if n_ == j[0]:
                need[pth] = pend[pth]
    prefetch_parallax(need, 5)
    todo = [j for j in jobs if not Path(j[4]).exists()]
    print(f"{len(jobs)} shots, {len(todo)} to render", flush=True)
    res = []
    with Pool(a.workers) as pool:
        for r in pool.imap_unordered(render_real, sorted(todo, key=lambda j: -j[3])):
            res.append(r)
            if r[2] != "ok":
                print("shot", r, flush=True)
    bad_r = [r for r in res if r[2] != "ok"]
    if bad_r:
        print("FAILED", bad_r)
        sys.exit(1)
    rt = time.time() - t0
    vid_s = float(a.seconds) if limit else fb[-1] / FPS + a.tail
    print(f"render {rt:.0f}s for {len(todo)} shots; video {vid_s:.0f}s")
    if only is not None:
        return
    lst = cdir / ("list_real_proof.txt" if limit else "list_real.txt")
    lst.write_text("".join(f"file 'real/{p.name}'\n" for p in order), encoding="utf-8")
    out_dir = ld / "output"
    out_dir.mkdir(parents=True, exist_ok=True)
    if limit:
        name = a.name or f"{a.story}_proof_real_0-{int(a.seconds)}.mp4"
    else:
        name = a.name or f"{a.story}_long_preview.mp4"
    outp = out_dir / name
    T = vid_s
    if limit:
        # sound for the proof: rc_sound on the proof timing + proof voice, first T seconds
        import rc_sound
        rc_sound.build(a.story, 0.0, None, False, timing=tfile, voice=vfile, cname="sound_proof")
        raw = cdir / "sound_proof/mix_raw.f32"
        cmd = [B.find_ff(), "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", str(lst), "-f", "f32le", "-ar", str(rc_sound.SR), "-ac", "2", "-i", str(raw),
               "-map", "0:v", "-map", "1:a", "-c:v", "libx264", "-preset", "medium", "-crf", "22", "-maxrate", "9M", "-bufsize", "18M", "-pix_fmt", "yuv420p", "-af", f"loudnorm=I=-14:TP=-1.5:LRA=11,alimiter=limit=0.82:level=disabled,aresample=48000,afade=t=out:st={T - 1:.2f}:d=1",
               "-c:a", "aac", "-b:a", "192k", "-t", f"{T:.3f}", "-movflags", "+faststart", str(outp)]
        subprocess.run(cmd, check=True, cwd=str(cdir))
        chat = out_dir / (outp.stem + "_chat.mp4")
        subprocess.run([B.find_ff(), "-y", "-loglevel", "error", "-i", str(outp), "-vf", "scale=640:360", "-c:v", "libx264", "-preset", "veryfast", "-b:v", "130k", "-ac", "1",
                        "-c:a", "aac", "-b:a", "56k", "-movflags", "+faststart", str(chat)], check=True)
        print("OUT", outp, chat)
    else:
        print("full-look mux: run rc_sound.py after concat (not done in proof mode)")
