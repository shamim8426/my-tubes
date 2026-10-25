"""Shabd-sync demo (user 2026-10-26): ~36 s of Al-Fatiha (lines 38-43, ayah 2 matlab + misaal) in the new style -
the picture changes on the spoken word, Allah and His names as Arabic cards (libass + Amiri, Tanzil bytes), free
sources only (Cloudflare Workers AI images, Pixabay video clips), camera motion + moving clips. ₹0: cached TTS.

    .venv\\Scripts\\python -X utf8 scripts\\noor_shabd_demo.py fetch     # candidate clips (3 per beat) + AI images
    .venv\\Scripts\\python -X utf8 scripts\\noor_shabd_demo.py words     # Whisper word times of the demo lines
    .venv\\Scripts\\python -X utf8 scripts\\noor_shabd_demo.py render    # samples/shabd_sync_demo/shabd_sync_demo.mp4

Keys from .env (never printed): CLOUDFLARE_ACCOUNT_ID, CLOUDFLARE_API_TOKEN(_FREE), PIXABAY_API_KEY(_FREE).
"""
import base64
import json
import math
import subprocess
import sys
from difflib import SequenceMatcher
from pathlib import Path

import cv2
import numpy as np
import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import noor_render as R  # noqa: E402
import parallax as PX  # noqa: E402
from noor_audition import clean, plain  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
STORY = ROOT / "channels/noor-e-raah/stories/001_al-fatiha"
OUT = ROOT / "channels/noor-e-raah/samples/shabd_sync_demo"
ASSETS = OUT / "assets"
FIRST, LAST = 38, 43  # spoken line numbers of the demo
CARD_DIM = 0.45  # background brightness under an Arabic card
MIN_SHOT, LEAD_IN, XF = 1.1, 0.15, 0.3  # 2.4 s made a quick list ("बारिश, साँस, सूरज") lag up to 2 s behind

# Tanzil words, bytes cut from the ayah text in lines.json (never retyped)
AYAH1, AYAH2 = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ", "ٱلْحَمْدُ لِلَّهِ رَبِّ ٱلْعَٰلَمِينَ"

# Pixabay video queries (free stock, real motion) and Cloudflare prompts (free AI, camera motion)
CLIPS = {"birds": "bird feeding chicks nest", "galaxy": "milky way galaxy timelapse", "animals": "wildlife animals herd",
         "ocean": "ocean waves aerial", "rain": "rain drops leaves", "mist": "morning fog forest sunlight",
         "sunrise": "sunrise timelapse mountains", "thanks": "helping hand kindness",
         # 22-26 s: HARD RULE 2a - the misaal only through hands (no full figures / faces acting it)
         "pickup": "hand picking up from floor", "pickup2": "picking up dropped", "pickup3": "hand giving object"}
STYLE = ("cinematic painted illustration, soft painterly brush texture, warm natural light, rich colour, 16:9 "
         "composition, no text, no writing, no logo, no watermark, no domes, no minarets")
AI = {"valley": "A breathtaking green valley at sunrise between snow-capped mountains, a clear river winding through "
                "wildflower meadows, small stone houses on the hillside, golden mist, sense of wonder and gratitude",
      "helper": "A narrow old Indian street in soft morning light; a young man in a simple kurta bends to pick up books "
                "an elderly man has dropped and hands them back; warm kind expressions, modest clothes, natural faces"}

# beats: (line, word in the script text, kind, source, Arabic card or None, Hindi card line)
BEATS = [(38, "हम्द", "clip", "thanks", AYAH2.split()[0], "हम्द"),
         (39, "ख़ूबियों", "img", "valley", None, None),
         (40, "रब", "clip", "valley_mist", AYAH2.split()[2], "रब — पालने वाला"),
         (40, "पालता", "clip", "birds", None, None),
         (40, "आलमीन", "clip", "galaxy", AYAH2.split()[3], "आलमीन — सारे जहान"),
         (40, "अल्लाह", "same", None, AYAH1.split()[1], "अल्लाह"),
         (40, "मख़लूक़", "clip", "animals", None, None),
         (40, "जहान", "clip", "earth", None, None),
         # HARD RULE 2a: the misaal through hands only (was "helper": two men with faces); changes at the line start
         (42, "कोई", "img", "hands_pickup_b", None, None),
         (43, "बारिश", "clip", "rain", None, None),
         (43, "साँस", "clip", "mist", None, None),
         (43, "सूरज", "clip", "sunrise", None, None),
         (43, "ख़ूबियों", "img", "valley", None, None),
         (43, "हम्द", "same", None, AYAH2.split()[0], "हम्द")]


def env():
    e = dict(l.split("=", 1) for l in (ROOT / ".env").read_text(encoding="utf-8").splitlines() if "=" in l)
    e = {k.strip(): v.strip().strip('"') for k, v in e.items()}
    return (e.get("CLOUDFLARE_ACCOUNT_ID"), e.get("CLOUDFLARE_API_TOKEN") or e.get("CLOUDFLARE_API_TOKEN_FREE"),
            e.get("PIXABAY_API_KEY") or e.get("PIXABAY_API_KEY_FREE"))


def frame_of(video: Path, at: float, out: Path, width=480):
    R.run(["-ss", f"{at:.2f}", "-i", str(video), "-frames:v", "1", "-vf", f"scale={width}:-2", str(out)])


def fetch():
    acc, tok, pix = env()
    ASSETS.mkdir(parents=True, exist_ok=True)
    cands = {}
    for name, q in CLIPS.items():
        r = requests.get("https://pixabay.com/api/videos/", params={"key": pix, "q": q, "safesearch": "true",
                                                                    "per_page": 10}, timeout=30)
        r.raise_for_status()
        hits = [h for h in r.json()["hits"] if h["duration"] >= 5 and
                max(v.get("width", 0) for v in h["videos"].values()) >= 1920][:3]
        cands[name] = []
        for i, h in enumerate(hits):
            tiny = ASSETS / f"_cand_{name}_{i}.mp4"
            if not tiny.exists():
                tiny.write_bytes(requests.get(h["videos"]["tiny"]["url"], timeout=60).content)
            frame_of(tiny, min(2.0, h["duration"] / 2), ASSETS / f"_cand_{name}_{i}.jpg")
            cands[name].append({"id": h["id"], "page": h["pageURL"], "user": h["user"], "seconds": h["duration"],
                                "tags": h["tags"], "videos": {k: [v["url"], v["width"], v["height"]]
                                                              for k, v in h["videos"].items()}})
        print(f"{name}: {[(c['id'], c['seconds'], c['tags'][:40]) for c in cands[name]]}")
    (ASSETS / "_candidates.json").write_text(json.dumps(cands, ensure_ascii=False, indent=1), encoding="utf-8")
    H = {"Authorization": f"Bearer {tok}"}
    for name, prompt in AI.items():
        f = ASSETS / f"ai_{name}.jpg"
        if f.exists():
            continue
        r = requests.post(f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/@cf/black-forest-labs/"
                          "flux-2-klein-4b", headers=H, timeout=240,
                          files={"prompt": (None, f"{prompt}. {STYLE}"), "width": (None, "1920"), "height": (None, "1088")})
        r.raise_for_status()
        f.write_bytes(base64.b64decode(r.json()["result"]["image"]))
        print(f"ai {name}: Cloudflare flux-2-klein-4b (free) -> {f.name}")


STYLE_REAL = ("photorealistic cinematic film still, shot on 35mm film, natural light, real textures, gentle depth "
              "of field, 16:9, no text, no writing, no letters, no logo, no watermark, no domes, no minarets")
AI_REAL = {"valley": AI["valley"],
           "helper": "A narrow old lane in a North Indian town in soft morning light: plastered walls, wooden doors, "
                     "potted plants, hanging wires; a young man in a plain cream kurta bends to pick up books an "
                     "elderly man has dropped and hands them back; warm kind faces, modest clothes; the books are "
                     "plain cloth-bound with blank covers"}


def real_images():
    """Look 'real': the same two AI pictures as photographs (Cloudflare flux-2-klein-4b, free) to match stock."""
    acc, tok, _ = env()
    for name, prompt in AI_REAL.items():
        f = ASSETS / f"ai_{name}_real.jpg"
        if f.exists():
            continue
        r = requests.post(f"https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/@cf/black-forest-labs/"
                          "flux-2-klein-4b", headers={"Authorization": f"Bearer {tok}"}, timeout=240,
                          files={"prompt": (None, f"{prompt}. {STYLE_REAL}"), "width": (None, "1920"),
                                 "height": (None, "1088")})
        r.raise_for_status()
        f.write_bytes(base64.b64decode(r.json()["result"]["image"]))
        print(f"ai {name} (real): Cloudflare flux-2-klein-4b (free) -> {f.name}")


def pick(choice: dict):
    """choice = {clip name: [candidate list, index]} (picked by eye from the contact sheets; quality gate by hand in
    this demo); downloads the smallest rendition that is at least 1920 wide."""
    cands = json.loads((ASSETS / "_candidates.json").read_text(encoding="utf-8"))
    rows = []
    for name, (cand, i) in choice.items():
        c = cands[cand][i]
        url, w, h = min((v for v in c["videos"].values() if v[1] >= 1920), key=lambda v: v[1])
        f = ASSETS / f"clip_{name}.mp4"
        if not f.exists():
            f.write_bytes(requests.get(url, timeout=180).content)
        rows.append({"file": f.name, "source": "Pixabay (Content License, free)", "id": c["id"], "page": c["page"],
                     "author": c["user"], "size": f"{w}x{h}"})
        print(f"{name}: {c['page']} {w}x{h}")
    rows += [{"file": f"ai_{n}.jpg", "source": "Cloudflare Workers AI flux-2-klein-4b (Apache 2.0, free tier)"}
             for n in AI]
    (ASSETS / "sources.json").write_text(json.dumps(rows, ensure_ascii=False, indent=1), encoding="utf-8")


def words():
    """Whisper word times inside each demo line (seconds of the TTS file, before TEMPO)."""
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8", download_root=str(ROOT / "tools/whisper-models"))
    items = json.loads((STORY / "long/lines.json").read_text(encoding="utf-8"))
    by_n = {i["n"]: i for i in items if i["kind"] == "line"}
    out = {}
    for n in sorted({b[0] for b in BEATS}):
        x = R.decode(STORY / by_n[n]["audio"], ch=1)[:, 0]  # as noor_build: array in, not a file path (PyAV)
        x16 = np.interp(np.arange(0, len(x), R.SR / 16000), np.arange(len(x)), x).astype(np.float32)
        segs, _ = model.transcribe(x16, language="hi", word_timestamps=True, beam_size=5)
        heard = [(w.word.strip(), w.start, w.end) for s in segs for w in s.words]
        out[n] = heard
        print(n, " ".join(f"{w}@{a:.2f}" for w, a, _ in heard))
    (OUT / "_words.json").write_text(json.dumps(out, ensure_ascii=False, indent=1), encoding="utf-8")


def word_time(heard, word, after=0.0):
    """Start (s) of the heard word most like `word` (nuqta/spelling folded), at or after `after`; None if < 0.6."""
    target = clean(plain(word))
    best, at = 0.0, None
    for i, (w, a, _) in enumerate(heard):
        if a < after:
            continue
        for cand in (clean(plain(w)), clean(plain(w + (heard[i + 1][0] if i + 1 < len(heard) else "")))):
            r = SequenceMatcher(None, target, cand).ratio()
            if r > best:
                best, at = r, a
    return at if best >= 0.6 else None


def plan_shots(tl):
    heard = json.loads((OUT / "_words.json").read_text(encoding="utf-8"))
    starts = {l["n"]: l["start"] for l in tl["lines"]}
    shots, cards, report, last_in_line = [], [], [], {}
    for line, word, kind, src, ar, hi in BEATS:
        w = word_time(heard[str(line)], word, last_in_line.get(line, 0.0))
        t = starts[line] + (w if w is not None else 0.0) / R.TEMPO - LEAD_IN
        if w is not None:
            last_in_line[line] = w + 0.05
        if kind != "same":
            if shots and t - shots[-1]["start"] < MIN_SHOT:
                t = shots[-1]["start"] + MIN_SHOT  # too close to the last change: comes a little later
            shots.append({"kind": kind, "src": src, "start": round(max(0.0, t), 3)})
        if ar:
            cards.append({"start": round(max(0.0, t), 3), "ar": ar, "hi": hi})
        report.append(f"| {line} | {word} | {'-' if w is None else f'{w / R.TEMPO:.2f}'} | "
                      f"{starts[line] + (w or 0) / R.TEMPO:.2f} | {max(0.0, t) + LEAD_IN:.2f} | {kind}:{src or ''} |")
    shots[0]["start"] = 0.0
    for a, b in zip(shots, shots[1:]):
        a["end"] = b["start"]
    shots[-1]["end"] = tl["end"]
    for i, c in enumerate(cards):
        nxt = cards[i + 1]["start"] if i + 1 < len(cards) else c["start"] + 3.0
        own = next(s for s in shots if s["start"] <= c["start"] + 0.01 < s["end"] + 0.01)
        # a card never runs onto the next picture (ٱللَّهِ had run 0.75 s onto the elephants)
        c["end"] = round(min(c["start"] + 2.6, nxt - 0.1, own["end"] - XF / 2), 3)
    for k, s in enumerate(shots):
        s["move"] = R.MOVES[k % len(R.MOVES)]
    return shots, cards, report


def dim_at(cards, t):
    """Picture brightness under the cards: dark only while a card is on, with 0.3 s ramps (not the whole shot)."""
    d = 0.0
    for c in cards:
        if c["start"] - 0.3 <= t <= c["end"] + 0.3:
            d = max(d, min(1.0, (t - c["start"] + 0.3) / 0.3, (c["end"] + 0.3 - t) / 0.3))
    return 1 - (1 - CARD_DIM) * d


_CAP = {}


def clip_frame(name, t):
    """Frame of a stock clip at t s (looped), cover-cropped to 1920x1080 with overscan for the camera move."""
    if name not in _CAP:
        cap = cv2.VideoCapture(str(ASSETS / f"clip_{name}.mp4"))
        _CAP[name] = (cap, cap.get(cv2.CAP_PROP_FPS) or 25, int(cap.get(cv2.CAP_PROP_FRAME_COUNT)), [-1, None])
    cap, fps, n, last = _CAP[name]
    i = int(t * fps) % max(1, n - 2)
    if i != last[0]:
        if i != last[0] + 1:
            cap.set(cv2.CAP_PROP_POS_FRAMES, i)
        ok, fr = cap.read()
        if ok:
            ih, iw = fr.shape[:2]
            sc = max(W_OS / iw, H_OS / ih)
            fr = cv2.resize(fr, (math.ceil(iw * sc), math.ceil(ih * sc)), interpolation=cv2.INTER_AREA)
            y0, x0 = (fr.shape[0] - H_OS) // 2, (fr.shape[1] - W_OS) // 2
            last[1] = fr[y0:y0 + H_OS, x0:x0 + W_OS]
        last[0] = i
    return last[1]


W_OS, H_OS = int(round(R.W * PX.OVERSCAN)), int(round(R.H * PX.OVERSCAN))


_PAINT = {}


def painterly(fr, key):
    """Stock frame -> painted look (look 'paint'): edge-preserving smoothing at half size, soft colour steps."""
    if key not in _PAINT:
        h, w = fr.shape[:2]
        small = cv2.resize(fr, (w // 2, h // 2), interpolation=cv2.INTER_AREA)
        ep = cv2.edgePreservingFilter(small, flags=1, sigma_s=45, sigma_r=0.35)
        steps = (ep // 14) * 14 + 7
        ep = cv2.addWeighted(ep, 0.7, steps.astype(np.uint8), 0.3, 0)
        _PAINT.clear() if len(_PAINT) > 6 else None
        _PAINT[key] = cv2.resize(ep, (w, h), interpolation=cv2.INTER_CUBIC)
    return _PAINT[key]


def _grade_tools(look):
    """One colour grade for every picture (AI and stock alike) so they sit together: soft S-curve, slightly
    muted saturation, warm tint, vignette; 'real' adds film grain, 'paint' a canvas texture."""
    x = np.arange(256) / 255.0
    curve = np.clip(255 * (x + 0.10 * np.sin(2 * np.pi * (x - 0.5)) * (-1) * 0.5 + 0.02 * (1 - x)), 0, 255)
    lut = np.dstack([np.clip(curve * 0.96, 0, 255), curve, np.clip(curve * 1.03 + 2, 0, 255)]).astype(np.uint8)
    yy, xx = np.mgrid[0:R.H, 0:R.W]
    r = np.sqrt(((xx - R.W / 2) / (R.W / 2)) ** 2 + ((yy - R.H / 2) / (R.H / 2)) ** 2)
    vig = (1 - 0.22 * np.clip(r - 0.55, 0, 1) ** 1.5)[..., None].astype(np.float32)
    rng = np.random.default_rng(7)
    if look == "real":
        tex = [rng.normal(0, 4.0, (R.H, R.W, 1)).astype(np.float32) for _ in range(4)]
    else:
        n = cv2.GaussianBlur(rng.normal(0, 1, (R.H, R.W)).astype(np.float32), (0, 0), 1.2)
        tex = [(n * 5.0)[..., None]]
    return lut, vig, tex


def graded(fr, i, tools, sat):
    lut, vig, tex = tools
    fr = cv2.LUT(fr, lut)
    hsv = cv2.cvtColor(fr, cv2.COLOR_BGR2HSV).astype(np.float32)
    hsv[..., 1] *= sat
    fr = cv2.cvtColor(np.clip(hsv, 0, 255).astype(np.uint8), cv2.COLOR_HSV2BGR).astype(np.float32)
    return np.clip(fr * vig + tex[i % len(tex)], 0, 255).astype(np.uint8)


def shot_frame(s, t, look):
    a, b = s["start"] - XF / 2, s["end"] + XF / 2
    p = min(1.0, max(0.0, (t - a) / (b - a)))
    z, dx, dy = PX.motion(s["move"], p, PX.AMP * 0.6)
    if s["kind"] == "clip":
        src = clip_frame(s["src"], t - s["start"] + 0.5)
        if look == "paint":
            src = painterly(src, (s["src"], _CAP[s["src"]][3][0]))
    else:
        src = R.source(ASSETS / f"ai_{s['src']}{'_real' if look == 'real' else ''}.jpg", 0.5, 0.5, 1.0)
    return PX._warp(src, 1 + z, dx, dy, R.W, R.H)


def frames(shots, cards, n, look):
    tools = _grade_tools(look)
    k = 0
    for i in range(n):
        t = i / R.FPS
        while k + 1 < len(shots) and t >= shots[k]["end"] + XF / 2:
            k += 1
        fr = shot_frame(shots[k], t, look)
        if k + 1 < len(shots) and t >= shots[k]["end"] - XF / 2:
            w = (t - (shots[k]["end"] - XF / 2)) / XF
            fr = cv2.addWeighted(fr, 1 - w, shot_frame(shots[k + 1], t, look), w, 0)
        fr = graded(fr, i, tools, 0.88 if look == "real" else 0.95)
        d = dim_at(cards, t)
        yield fr if d >= 0.999 else (fr * d).astype(np.uint8)


def render(look="real"):
    items = json.loads((STORY / "long/lines.json").read_text(encoding="utf-8"))
    i0 = next(i for i, x in enumerate(items) if x.get("n") == FIRST)
    i1 = next(i for i, x in enumerate(items) if x.get("n") == LAST)
    sub = [{"kind": "cue", "type": "music", "value": "back slowly: River Flute", "ayah": 2}] + items[i0:i1 + 1]
    tl = R.timeline(sub)
    shots, cards, report = plan_shots(tl)
    OUT.mkdir(parents=True, exist_ok=True)
    (OUT / "_plan.json").write_text(json.dumps({"shots": shots, "cards": cards}, ensure_ascii=False, indent=1),
                                    encoding="utf-8")
    (OUT / "sync_report.md").write_text(
        "# Shabd-sync demo - word vs picture\n\n| Line | Word | Word at (s, in line) | Word at (video s) | "
        "Picture at (video s) | Picture |\n|---|---|---|---|---|---|\n" + "\n".join(report) + "\n", encoding="utf-8")
    print(f"length {tl['end']:.1f}s, shots {len(shots)}, cards {len(cards)}")
    audio = R.build_audio(STORY, tl, OUT, tl["end"])
    doc = R.ass_doc(tl)
    doc = "\n".join(l for l in doc.splitlines() if not any(x in l for x in (R.TITLE_AR, R.TITLE_HI, R.SERIES)))
    ev = []
    for c in cards:  # Arabic word big and gold (Amiri via libass, bytes as in Tanzil), Hindi line under it
        ev.append(f"Dialogue: 3,{R.ts(c['start'])},{R.ts(c['end'])},ArTitle,,0,0,0,,"
                  f"{{\\an5\\pos(960,430)\\fs{int(150 * R.AMIRI_ASS_K)}\\fad(250,300)}}{c['ar']}")
        ev.append(f"Dialogue: 3,{R.ts(c['start'] + 0.15)},{R.ts(c['end'])},Gold,,0,0,0,,"
                  f"{{\\an5\\pos(960,740)\\fs72\\fad(250,300)}}{c['hi']}")
    ass = OUT / "_text.ass"
    ass.write_text(doc + "\n" + "\n".join(ev) + "\n", encoding="utf-8")
    out = OUT / f"shabd_sync_demo_{look}.mp4"
    part = out.with_suffix(".part.mp4")
    n = int(round(tl["end"] * R.FPS))
    enc = subprocess.Popen([R.FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", f"{R.W}x{R.H}",
                            "-r", str(R.FPS), "-i", "-", "-i", str(audio), "-vf", R.video_filter(tl, OUT, ass),
                            "-frames:v", str(n), "-c:v", "libx264", "-preset", "medium", "-crf", "18",
                            "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-t", f"{tl['end']:.3f}",
                            "-movflags", "+faststart", str(part)], stdin=subprocess.PIPE)
    for fr in frames(shots, cards, n, look):
        enc.stdin.write(fr.tobytes())
    enc.stdin.close()
    if enc.wait():
        sys.exit("ffmpeg failed")
    part.replace(out)
    mp3 = out.with_name(out.stem + "_vscode.mp4")  # VS Code plays MP3 audio, not AAC
    R.run(["-i", str(out), "-c:v", "copy", "-c:a", "libmp3lame", "-b:a", "192k", str(mp3)])
    print(f"OK {out.relative_to(ROOT).as_posix()} {tl['end']:.1f}s {R.lufs_file(out):.1f} LUFS")


if __name__ == "__main__":
    cmd = sys.argv[1]
    if cmd == "fetch":
        fetch()
    elif cmd == "pick":
        pick(json.loads(sys.argv[2]))
    elif cmd == "words":
        words()
    elif cmd == "real-images":
        real_images()
    elif cmd == "render":
        render(sys.argv[2] if len(sys.argv) > 2 else "real")
