r"""PROTOTYPE of the 'clean editorial' Short look (user 2026-11-07, learned from a faceless competitor channel; principles only): light grey page + grid, a small hero picture (cards/hub with the robot) with soft shadows,
kinetic caption (words fade in grey -> dark, key words bold, one black label), small channel watermark. Every element is rendered by Chromium (correct Hindi shaping, soft shadows) and animated here with PIL.
Reuses the voice of story 043 (Claude Code /fast), so this prototype costs Rs 0.   Run:  python make_clean.py [frames t1 t2 ...]   (render = no args; ffmpeg must be on PATH)"""
import base64, hashlib, io, json, math, sys, wave
from pathlib import Path
import numpy as np
from PIL import Image, ImageDraw, ImageFilter

HERE = Path(__file__).parent; ROOT = HERE.parents[3]
SRC = ROOT / "channels/devrobolab/stories/043_cc-fast-mode"
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import ease_out, ease_back, ease_io, wav_dur
import subprocess

W, H, FPS = 1080, 1920, 30
LEAD, AFTER = 0.05, 0.05
deck = json.load(open(SRC / "deck.json", encoding="utf-8")); WT = json.load(open(SRC / "wt.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]
WAVES = [SRC / "audio/tts" / f"s_{i:02d}.wav" for i in range(len(IDS))]
D = [LEAD + wav_dur(w) + AFTER for w in WAVES]; D[-1] += 1.2; START = [sum(D[:i]) for i in range(len(D))]; TOTAL = sum(D)
SC = dict(zip(IDS, START))
def T(sid, k): toks = WT[sid]["tokens"]; return SC[sid] + LEAD + toks[min(k, len(toks) - 1)][1]
def E(sid): return SC[sid] + D[IDS.index(sid)]
def clamp(x): return max(0.0, min(1.0, x))
def pop(t, t0, dur=0.32): return ease_back((t - t0) / dur) if t >= t0 else 0.0
def fade(t, t0, dur=0.25): return clamp((t - t0) / dur)

# ---------- Chromium sprite renderer ----------
FONTS = ROOT / "shared/fonts"
def _b64(n): return "data:font/ttf;base64," + base64.b64encode((FONTS / n).read_bytes()).decode()
PAGE_CSS = ("@font-face{font-family:MK;src:url('%s');font-weight:800}@font-face{font-family:MK;src:url('%s');font-weight:700}@font-face{font-family:MO;src:url('%s');font-weight:700}"
            "*{box-sizing:border-box;margin:0;padding:0}body{background:transparent;font-family:MK,sans-serif;color:#111}#c{display:inline-block;padding:70px}") % (
    _b64("Mukta-ExtraBold.ttf"), _b64("Mukta-Bold.ttf"), _b64("IBMPlexMono-Bold.ttf"))
_pw = None; _page = None; _cache = {}
def sprite(html):
    """render html (an element with its own size/shadow) -> RGBA PIL image, cached"""
    global _pw, _page
    k = hashlib.md5(html.encode("utf-8")).hexdigest()
    if k in _cache: return _cache[k]
    f = HERE / "cache" / f"{k}.png"; f.parent.mkdir(exist_ok=True)
    if not f.exists():
        if _page is None:
            from playwright.sync_api import sync_playwright
            _pw = sync_playwright().start(); br = _pw.chromium.launch(); _page = br.new_page(viewport={"width": 1400, "height": 900}, device_scale_factor=1)
        _page.set_content(f"<style>{PAGE_CSS}</style><div id=c>{html}</div>"); _page.evaluate("document.fonts.ready"); _page.wait_for_timeout(60)
        _page.locator("#c").screenshot(path=str(f), omit_background=True)
    im = Image.open(f).convert("RGBA"); _cache[k] = im; return im

SH = "box-shadow:0 30px 60px rgba(0,0,0,.20),0 6px 14px rgba(0,0,0,.08)"
def circle(d, inner, bg="#fff"): return f'<div style="width:{d}px;height:{d}px;border-radius:50%;background:{bg};{SH};display:flex;align-items:center;justify-content:center;overflow:hidden">{inner}</div>'
def card(w, inner, h=None, bg="#fff", pad=26, r=34, extra=""): return f'<div style="width:{w}px;{"height:%dpx;" % h if h else ""}border-radius:{r}px;background:{bg};padding:{pad}px;{SH};{extra}">{inner}</div>'
def b64img(p): return "data:image/png;base64," + base64.b64encode(Path(p).read_bytes()).decode()
ROB = {n: b64img(ROOT / f"channels/devrobolab/mascot/cut/{n}.png") for n in ("wave", "stop", "thumbs", "work", "think")}
def robot_circle(d, pose, scale=1.15): return circle(d, f'<img src="{ROB[pose]}" style="height:{int(d * scale)}px;margin-top:{int(d * 0.12)}px">')
ICON = {
    "bolt": '<svg width="@@" height="@@" viewBox="0 0 40 40"><path d="M23 2L7 23h10l-3 15 19-24H22z" fill="#FFC800" stroke="#14213d" stroke-width="2.5" stroke-linejoin="round"/></svg>',
    "term": '<svg width="@@" height="@@" viewBox="0 0 40 40"><rect x="3" y="6" width="34" height="28" rx="6" fill="#14213d"/><path d="M10 15l7 5-7 5M20 27h10" fill="none" stroke="#7cf0a8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "clock": '<svg width="@@" height="@@" viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="#fff" stroke="#14213d" stroke-width="3"/><path d="M20 10v11l7 4" fill="none" stroke="#14213d" stroke-width="3" stroke-linecap="round"/></svg>',
    "star": '<svg width="@@" height="@@" viewBox="0 0 40 40"><path d="M20 2c2 10 8 16 18 18-10 2-16 8-18 18-2-10-8-16-18-18C12 18 18 12 20 2z" fill="#D97757" stroke="#14213d" stroke-width="2" stroke-linejoin="round"/></svg>',
    "warn": '<svg width="@@" height="@@" viewBox="0 0 40 40"><path d="M20 4L38 35H2z" fill="#FFC800" stroke="#14213d" stroke-width="3" stroke-linejoin="round"/><path d="M20 15v10M20 29v2" stroke="#14213d" stroke-width="3.5" stroke-linecap="round"/></svg>',
    "check": '<svg width="@@" height="@@" viewBox="0 0 40 40"><circle cx="20" cy="20" r="17" fill="#34d96b" stroke="#14213d" stroke-width="3"/><path d="M12 21l6 6 11-13" fill="none" stroke="#14213d" stroke-width="4" stroke-linecap="round" stroke-linejoin="round"/></svg>',
}
def ic(n, s): return ICON[n].replace("@@", str(s))

# ---------- placement + animation helpers ----------
def place(base, spr, cx, cy, scale=1.0, alpha=1.0, rot=0):
    if scale <= 0.02 or alpha <= 0.01: return
    if abs(scale - 1) > 1e-3: spr = spr.resize((max(1, int(spr.width * scale)), max(1, int(spr.height * scale))), Image.LANCZOS)
    if rot: spr = spr.rotate(rot, resample=Image.BICUBIC, expand=True)
    if alpha < 1: a = spr.getchannel("A").point(lambda v: int(v * alpha)); spr = spr.copy(); spr.putalpha(a)
    base.alpha_composite(spr, (int(cx - spr.width / 2), int(cy - spr.height / 2)))

def line(base, p0, p1, t, t0, color=(217, 119, 87), width=7):
    q = ease_out((t - t0) / 0.45) if t >= t0 else 0
    if q <= 0: return
    x0, y0 = p0; x1, y1 = p1; x1 = x0 + (x1 - x0) * q; y1 = y0 + (y1 - y0) * q
    pad = 20; bx0, by0 = int(min(x0, x1) - pad), int(min(y0, y1) - pad); bw, bh = int(abs(x1 - x0) + 2 * pad), int(abs(y1 - y0) + 2 * pad)
    s = 4; im = Image.new("RGBA", (bw * s, bh * s), (0, 0, 0, 0)); ImageDraw.Draw(im).line([((x0 - bx0) * s, (y0 - by0) * s), ((x1 - bx0) * s, (y1 - by0) * s)], fill=color + (255,), width=width * s)
    base.alpha_composite(im.resize((bw, bh), Image.LANCZOS), (bx0, by0))

# ---------- background / watermark ----------
def make_bg():
    im = Image.new("RGBA", (W, H), (242, 242, 242, 255)); d = ImageDraw.Draw(im)
    for x in range(0, W, 90): d.line([(x, 0), (x, H)], fill=(230, 230, 230, 255), width=2)
    for y in range(0, H, 90): d.line([(0, y), (W, y)], fill=(230, 230, 230, 255), width=2)
    return im
BG = None
def wm(): return sprite('<div style="font:700 44px MK;color:rgba(0,0,0,.28);letter-spacing:1px">devrobolab</div>')

# ---------- kinetic caption ----------
LIGHT, BOLD = "#6b6b73", "#111"
def word_sprite(w, bold, dark):
    col = BOLD if dark else "#b9b9c0"
    return sprite(f'<div style="font:{800 if bold else 700} {76 if bold else 64}px MK;color:{col};white-space:nowrap;line-height:1.25">{w}</div>' if dark or True else "")
def label_sprite(t): return sprite(f'<div style="background:#0e0e11;color:#fff;font:800 70px MK;padding:0 36px 8px;border-radius:12px;white-space:nowrap;box-shadow:0 14px 30px rgba(0,0,0,.30)">{t}</div>')

def caption(base, t, sid, words, label=None, top=1180, maxw=900):
    """words: list of (text, bold) = the voice tokens in order; label=(first_token, last_token, text) shown as a black label on its own last line"""
    toks = WT[sid]["tokens"]; lines = [[]]; widths = [0]; gap = 20
    for k, (w, bold) in enumerate(words):
        if label and label[0] <= k <= label[1]: continue
        sp = word_sprite(w, bold, True); wd = sp.width - 140
        if widths[-1] + wd > maxw and lines[-1]: lines.append([]); widths.append(0)
        lines[-1].append((k, sp, wd, bold)); widths[-1] += wd + gap
    y = top
    for ln, wd in zip(lines, widths):
        x = W / 2 - (wd - gap) / 2
        lh = max(sp.height for _, sp, _, _ in ln) - 140
        for k, sp, w_, bold in ln:
            t0 = T(sid, k)
            if t >= t0 - 0.02:
                dark = ease_out((t - t0) / 0.28)
                g = word_sprite(words[k][0], words[k][1], False)
                a_in = fade(t, t0, 0.12)
                place(base, g, x + w_ / 2, y + lh / 2 + (1 - a_in) * 10, 1.0, a_in * (1 - dark))
                place(base, sp, x + w_ / 2, y + lh / 2 + (1 - a_in) * 10, 1.0, a_in * dark)
            x += w_ + gap
        y += lh + 14
    if label and t >= T(sid, label[0]) - 0.02:
        sp = label_sprite(label[2]); q = pop(t, T(sid, label[0]))
        place(base, sp, W / 2, y + 70, 0.7 + 0.3 * q, fade(t, T(sid, label[0]), 0.15))

# ---------- scenes ----------
def S_hook(base, t):
    sid = "hook"; cx, cy = 540, 560
    place(base, sprite(robot_circle(380, "wave")), cx, cy, 0.85 + 0.15 * pop(t, SC[sid] + 0.05), fade(t, SC[sid], 0.2))
    for name, ang, k in (("bolt", -145, 3), ("term", -35, 9), ("clock", 90, 6)):
        r = 330; x = cx + r * math.cos(math.radians(ang)); y = cy + r * math.sin(math.radians(ang)) * 0.9; t0 = T(sid, k)
        line(base, (cx, cy), (x, y), t, t0 - 0.2)
        place(base, sprite(circle(190, ic(name, 110))), x, y, pop(t, t0), min(1, pop(t, t0) * 1.4))
    words = [("Claude", True), ("Code", True), ("ko", False), ("dhai", True), ("guna", True), ("tak", False), ("tez", True), ("karna", False), ("hai?", False), ("bas", False), ("ek", False), ("command,", True), ("slash", True), ("fast.", True)]
    caption(base, t, sid, words, label=(12, 13, "slash fast"))

def S_what(base, t):
    sid = "what"; t0 = SC[sid] + 0.1
    bars = ('<div style="width:620px"><div style="font:700 40px MK;color:#444">Normal</div><div style="height:46px;border-radius:46px;background:#e6e6ea;margin:8px 0 26px;overflow:hidden"><div style="width:40%;height:100%;background:#9aa3b2"></div></div>'
            '<div style="font:800 40px MK">&#9889; /fast</div><div style="height:46px;border-radius:46px;background:#e6e6ea;margin:8px 0 0;overflow:hidden"><div style="width:100%;height:100%;background:linear-gradient(90deg,#FFC800,#FF9A1F)"></div></div></div>')
    q = pop(t, t0)
    place(base, sprite(card(700, bars, pad=40)), 540, 520, 0.8 + 0.2 * q, fade(t, t0, 0.2))
    place(base, sprite('<div style="background:#0e0e11;color:#fff;font:800 46px MK;padding:2px 26px 8px;border-radius:12px;box-shadow:0 14px 30px rgba(0,0,0,.3)">same Opus model</div>'), 540, 800, pop(t, T(sid, 6)), fade(t, T(sid, 6), 0.15))
    words = [("Ye", False), ("Fast", True), ("mode", True), ("hai.", False), ("Model", False), ("wahi", True), ("Opus", True), ("rehta", False), ("hai,", False), ("quality", False), ("bhi", False), ("same,", True), ("bas", False), ("jawab", False), ("tez", True), ("aate", False), ("hain.", False)]
    caption(base, t, sid, words)

def S_how(base, t):
    sid = "how"; t0 = SC[sid] + 0.1
    typed = T(sid, 3); on = T(sid, 13)
    state = 2 if t >= on else (1 if t >= typed else 0)
    body = {0: '<span style="color:#7cf0a8">&gt;</span> <span style="opacity:.5">_</span>', 1: '<span style="color:#7cf0a8">&gt;</span> /fast', 2: '<span style="color:#7cf0a8">&gt;</span> /fast<br><span style="color:#FFC800">&#9889; Fast mode ON</span>'}[state]
    term = card(800, f'<div style="display:flex;gap:10px;margin-bottom:18px"><i style="width:16px;height:16px;border-radius:50%;background:#ff5f57"></i><i style="width:16px;height:16px;border-radius:50%;background:#febc2e"></i><i style="width:16px;height:16px;border-radius:50%;background:#28c840"></i></div><div style="font:700 56px MO;line-height:1.5;color:#e6edf7;min-height:170px">{body}</div>', bg="#0f172a", pad=34)
    q = pop(t, t0)
    place(base, sprite(term), 540, 480, 0.85 + 0.15 * q, fade(t, t0, 0.2))
    for k, label in ((5, "Space"), (8, "Enter")):
        x = 360 if label == "Space" else 720
        place(base, sprite(f'<div style="background:#fff;border-radius:18px;padding:6px 38px 12px;font:800 54px MK;{SH}">{label}</div>'), x, 800, pop(t, T(sid, k)), min(1, pop(t, T(sid, k)) * 1.4))
    if t >= T(sid, 19) - 0.02: place(base, sprite(circle(120, ic("bolt", 70))), 905, 640, pop(t, T(sid, 19)), 1.0)
    words = [("Terminal", True), ("mein", False), ("slash", True), ("fast", True), ("likho,", False), ("Space", True), ("dabao,", False), ("phir", False), ("Enter।", True), ("screen", False), ("par", False), ("Fast", True), ("mode", True), ("ON", True), ("dikhega,", False), ("aur", False), ("prompt", False), ("ke", False), ("paas", False), ("ek", False), ("chhota", False), ("icon.", True)]
    caption(base, t, sid, words)

def S_caution(base, t):
    sid = "caution"
    place(base, sprite(robot_circle(300, "stop")), 540, 330, pop(t, SC[sid] + 0.05), fade(t, SC[sid], 0.2))
    rows = [(3, "warn", "Sirf Opus par"), (9, "warn", "Har token ka daam zyada"), (15, "warn", "Subscription: usage credits se katta hai")]
    for i, (k, icn, txt) in enumerate(rows):
        t0 = T(sid, k) - 0.1
        place(base, sprite(card(900, f'<div style="display:flex;align-items:center;gap:22px">{ic(icn, 64)}<div style="font:800 46px MK;line-height:1.15">{txt}</div></div>', pad=24, r=30)), 540, 640 + i * 150, 0.85 + 0.15 * pop(t, t0), fade(t, t0, 0.2))
    words = [("Dhyan", True), ("rakho!", True), ("Ye", False), ("sirf", False), ("Opus", True), ("par", False), ("chalta", False), ("hai,", False), ("aur", False), ("har", False), ("token", True), ("ka", False), ("daam", True), ("zyada", True), ("hai.", False), ("Subscription", False), ("mein", False), ("Ye", False), ("usage", False), ("credits", False), ("se", False), ("kat-ta", False), ("hai.", False)]
    caption(base, t, sid, words, top=1230)

def S_tip(base, t):
    sid = "tip"
    steps = [(0, "1", "Session ki shuruaat me <b>/fast</b> chalu karo"), (8, "2", "Kharcha zyada lage? <b>/fast</b> se band karo")]
    for i, (k, n, txt) in enumerate(steps):
        t0 = T(sid, k) - 0.05
        place(base, sprite(card(900, f'<div style="display:flex;align-items:center;gap:24px"><div style="width:84px;height:84px;border-radius:50%;background:#FFC800;font:800 50px MK;display:flex;align-items:center;justify-content:center;flex:none">{n}</div><div style="font:700 46px MK;line-height:1.2">{txt}</div></div>', pad=30, r=30)), 540, 420 + i * 230, 0.85 + 0.15 * pop(t, t0), fade(t, t0, 0.2))
    words = [("Isliye", False), ("session", True), ("ki", False), ("shuruaat", True), ("mein", False), ("chalu", True), ("karo,", False), ("aur", False), ("kharcha", False), ("zyada", False), ("lage", False), ("toh", False), ("phir", False), ("slash", True), ("fast", True), ("se", False), ("band", True), ("kar", False), ("do.", False)]
    caption(base, t, sid, words, label=(13, 14, "slash fast"))

def S_cta(base, t):
    sid = "cta"
    place(base, sprite(robot_circle(420, "thumbs")), 540, 520, pop(t, SC[sid] + 0.05), fade(t, SC[sid], 0.2))
    t0 = T(sid, 8)
    place(base, sprite(card(620, '<div style="font:700 34px MK;color:#777">Comment</div><div style="font:800 64px MK">FAST</div>', pad=26, r=28)), 540, 880, pop(t, t0), fade(t, t0, 0.2))
    words = [("Aise", False), ("Claude", True), ("Code", True), ("tips", True), ("chahiye?", False), ("Follow", True), ("karo,", False), ("aur", False), ("comment", True), ("mein", False), ("FAST", True), ("likho.", False)]
    caption(base, t, sid, words, label=(5, 6, "Follow DevRoboLab"), top=1100)
    # the label above replaces "Follow करो," visually; the remaining words keep the voice timing

SCENES = {"hook": S_hook, "what": S_what, "how": S_how, "caution": S_caution, "tip": S_tip, "cta": S_cta}
def frame(t):
    global BG
    if BG is None: BG = make_bg()
    base = BG.copy(); sid = next((s for s in IDS if SC[s] <= t < E(s)), IDS[-1])
    SCENES[sid](base, t); place(base, wm(), W / 2, H - 90)
    return np.array(base.convert("RGB"))

SR = 24000
def build_audio(out):
    n = int(TOTAL * SR) + SR; a = np.zeros(n, dtype=np.float32)
    for i, w in enumerate(WAVES):
        with wave.open(str(w)) as f: x = np.frombuffer(f.readframes(f.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int((START[i] + LEAD) * SR); a[s:s + len(x)] += x
    with wave.open(str(out), "wb") as f: f.setnchannels(1); f.setsampwidth(2); f.setframerate(SR); f.writeframes((np.clip(a, -1, 1) * 32767).astype(np.int16).tobytes())

def encode(frames_iter, n, voice, music, out):
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(voice), "-ss", "6", "-i", str(music)]
    fc = "[2:a]volume=-26dB,aformat=sample_rates=24000:channel_layouts=mono[m];[1:a]aformat=sample_rates=24000:channel_layouts=mono[v];[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-12.8:TP=-1.5:LRA=7[a]"
    cmd += ["-filter_complex", fc, "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE)
    for i, fr in enumerate(frames_iter):
        p.stdin.write(fr.tobytes())
        if i % 150 == 0: print(f"  frame {i}/{n}", flush=True)
    p.stdin.close(); p.wait()

def main():
    print(f"total {TOTAL:.1f}s", [(s, round(SC[s], 1)) for s in IDS])
    (HERE / "review").mkdir(exist_ok=True); (HERE / "output").mkdir(exist_ok=True); (HERE / "audio").mkdir(exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(frame(tt)).save(HERE / f"review/C_{tt:05.1f}.png")
        return
    build_audio(HERE / "audio/voice.wav"); n = int(TOTAL * FPS)
    encode((frame(i / FPS) for i in range(n)), n, HERE / "audio/voice.wav", ROOT / "shared/music/presentation/Funkorama.mp3", HERE / "output/clean_proto.mp4")

if __name__ == "__main__":
    main()
