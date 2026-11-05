"""Claude Feature 03 (Artifacts) - UI WALKTHROUGH version (user 2026-11-06: demo first, chat inside, step by step, same editing motions).
ui3.html = illustration of the app built ONLY from the official help steps (labelled on screen: not a screen recording). Playwright renders each frame,
a virtual camera zooms/pans to the active area, cursor/typing/chat are driven by spoken-word times (Whisper wt.json). Dark theme + Claude-Code orange.
Editing: kinetic captions, step banner, click punch-in, cross-dissolves, progress bar, vignette + grain, no sound effects (voice + music only).
Run: python make.py render"""
import json, math, re, subprocess, sys, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
from playwright.sync_api import sync_playwright
HERE = Path(__file__).parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import *

ORG = (217, 119, 87)
LEAD, AFTER, SR, TR = 0.30, 0.28, 24000, 0.40
deck = json.load(open(HERE / "deck.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]; VOICE = {s["id"]: re.sub(r"\s+", " ", s["voice"]).strip() for s in deck["scenes"]}
waves = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(8)]
D = [LEAD + wav_dur(w) + AFTER for w in waves]; START = [sum(D[:i]) for i in range(8)]; TOTAL = sum(D)
WT = json.load(open(HERE / "wt.json", encoding="utf-8"))


def T(scene, phrase):
    """absolute time of the first spoken token of phrase in scene (Whisper; char-position fallback when Whisper dropped words)."""
    i = IDS.index(scene); toks = WT[scene]["tokens"]; words = VOICE[scene].split(" "); pw = phrase.split(" ")
    for k in range(len(words)):
        if words[k:k + len(pw)] == pw:
            if WT[scene]["n_whisper"] < 0.85 * WT[scene]["n_tokens"]:
                ch = len(" ".join(words[:k])) / max(1, len(VOICE[scene])); return START[i] + LEAD + WT[scene]["voice_s"] * ch * 0.97 - 0.1
            return START[i] + LEAD + toks[k][1] - 0.1
    raise ValueError(f"{phrase!r} not in {scene}")


def typ(text, t, t0, t1):
    p = min(1, max(0, (t - t0) / max(0.05, t1 - t0))); return text[:int(round(len(text) * p))]


def path(pts, t):
    """pts [(time,x,y)] eased cursor path"""
    if t <= pts[0][0]: return pts[0][1], pts[0][2]
    for a, b in zip(pts, pts[1:]):
        if t <= b[0]:
            p = ease_io((t - a[0]) / max(1e-3, b[0] - a[0])); return a[1] + (b[1] - a[1]) * p, a[2] + (b[2] - a[2]) * p
    return pts[-1][1], pts[-1][2]


def rip(t, tc): return (t - tc) / 0.5 if 0 <= t - tc <= 0.5 else None


LINES = ["Weekly study planner", "Mon: Physics ch.1", "Tue: Maths formulas", "Wed: Revision test", "Thu: Chemistry", "Fri: Mock paper"]
hk = T("hook", "इसके लिए"); s_set = T("settings", "Settings में"); s_cap = T("settings", "Capabilities"); s_tog = T("settings", "चालू"); s_need = T("settings", "Artifacts के")
c_type = T("create", "अपनी"); c_send = T("create", "बनाओ।"); c_open = T("create", "बगल")
e_sel = T("edit", "Text चुनो,"); e_btn = T("edit", "Edit with"); e_wr = T("edit", "लिखो कि"); e_done = T("edit", "वहीं")
x_click = T("export", "दबाओ।"); x_w = T("export", "Word,"); x_p = T("export", "PDF,"); x_m = T("export", "Markdown"); x_g = T("export", "Google")
f_tab = T("find", "Artifacts tab"); f_later = T("find", "बाद में"); p1 = T("plans", "free accounts"); p2 = T("plans", "Docs,")
SC = {k: START[IDS.index(k)] for k in IDS}
USER_MSG = "Ek weekly study planner banao"; BOT_MSG = "Ye lo aapka weekly study planner."


def art(lines=None, **kw): return dict(title="Study planner", lines=lines or LINES, **kw)


def state(t):
    st = dict(page="chat", cx=None, cy=None); step = None; cam = (900, 540, 1.4); clicks = []
    if t < SC["settings"]:   # hook: stock cutaway, then the cursor heads for the Artifacts tab and the chat box
        px, py = path([(0, 900, 500), (hk, 900, 500), (hk + 0.9, 180, 364), (hk + 2.2, 560, 962), (SC["settings"], 560, 962)], t)
        st.update(page="chat", cx=px, cy=py, msgs=[], inp=None, side="artifacts" if hk + 0.8 < t < hk + 1.6 else None); cam = (700, 560, 1.45) if t < hk + 0.3 else ((420, 420, 1.7) if t < hk + 1.7 else (600, 800, 1.5))
    elif t < SC["create"]:     # step 1: settings > capabilities > Create and edit files
        px, py = path([(SC["settings"], 900, 500), (s_set, 900, 500), (s_cap - 0.15, 180, 988), (s_cap + 0.5, 180, 988), (s_tog - 0.2, 1305, 331)], t)
        st.update(cx=px, cy=py, msgs=[]); step = (1, "Settings > Capabilities > *Create and edit files*"); cam = (330, 760, 1.8); clicks = [s_cap - 0.05, s_tog]
        if t > s_cap - 0.05: st.update(side="settings", modal=dict(on=t > s_tog + 0.1, hl=t > s_tog - 0.25)); cam = (900, 420, 1.5)
        if t > s_tog + 0.1 and t < s_tog + 0.6: st["modal"]["hl"] = True
    elif t < SC["edit"]:       # step 2: ask in chat, artifact opens beside it
        px, py = path([(SC["create"], 900, 500), (c_type - 0.4, 560, 962), (c_send + 0.1, 807, 962), (c_open + 0.6, 1100, 600)], t)
        txt = typ(USER_MSG, t, c_type, c_type + 1.4); msgs = []
        if t > c_send + 0.3: msgs = [dict(r="u", t=USER_MSG)]; txt = None
        if t > c_send + 0.9: msgs.append(dict(r="a", t=BOT_MSG))
        st.update(cx=px, cy=py, msgs=msgs, inp=txt or None, inpAct=t < c_send + 0.3, sendHl=c_send - 0.05 < t < c_send + 0.3)
        if t > c_open - 0.35: st.update(art=art(slide=ease_out((t - (c_open - 0.35)) / 0.4)))
        step = (2, "Chat me likho: *study planner banao*"); cam = (560, 900, 1.5); clicks = [c_send + 0.05]
        if t > c_open - 0.4: step = (2, "Artifact *bagal me* khulta hai"); cam = (1100, 480, 1.35)
    elif t < SC["export"]:     # step 3: select text > Edit with Claude
        lines = list(LINES); a = dict(); done = t > e_done
        px, py = path([(SC["edit"], 1100, 600), (e_sel - 0.1, 1000, 346), (e_sel + 0.7, 1230, 346), (e_btn - 0.3, 1230, 346), (e_btn + 0.1, 1115, 282), (e_wr - 0.1, 1115, 282), (e_wr + 0.1, 1150, 420)], t)
        sel = None
        if t > e_sel + 0.1: sel = 2
        if t > e_sel + 0.9 and not done: a["ebtn"] = True; a["ebx"] = 150; a["eby"] = 230
        if t > e_btn + 0.2 and not done: a["einp"] = typ("Isko Hinglish me likho", t, e_wr, e_wr + 1.0); a["eiy"] = 360; a["ebtn"] = False
        if done: lines[2] = "Mangal: Maths ke formulas (Hinglish)"; sel = None
        msgs = [dict(r="u", t=USER_MSG), dict(r="a", t=BOT_MSG)]
        st.update(cx=px, cy=py, msgs=msgs, art=art(lines, sel=sel, **a)); step = (3, "Text chuno > *Edit with Claude*"); cam = (1130, 380, 1.8); clicks = [e_btn + 0.1]
        if done: step = (3, "Claude *wahin* edit karta hai")
    elif t < SC["find"]:       # step 4: export
        px, py = path([(SC["export"], 1150, 420), (x_click - 0.5, 1380, 85), (x_w, 1325, 162), (x_p, 1325, 218), (x_m, 1325, 274), (x_g, 1325, 330)], t)
        lines = list(LINES); lines[2] = "Mangal: Maths ke formulas (Hinglish)"; a = dict(); idx = None
        if t > x_click: a["dd"] = True
        if t > x_w - 0.2: idx = 0
        if t > x_p - 0.2: idx = 1
        if t > x_m - 0.2: idx = 2
        if t > x_g - 0.2: idx = 3
        a["ddHl"] = idx; a["expHl"] = x_click - 0.1 < t < x_click + 0.5
        st.update(cx=px, cy=py, msgs=[dict(r="u", t=USER_MSG), dict(r="a", t=BOT_MSG)], art=art(lines, **a)); step = (4, "*Export* > Word, PDF, Markdown, Google Docs"); cam = (1280, 230, 1.8); clicks = [x_click]
    elif t < SC["plans"]:      # step 5: Artifacts tab
        px, py = path([(SC["find"], 1325, 330), (f_tab - 0.1, 1325, 330), (f_tab + 0.5, 180, 364)], t)
        st.update(cx=px, cy=py, page="chat", msgs=[dict(r="u", t=USER_MSG), dict(r="a", t=BOT_MSG)], art=art(), side=None); step = (5, "Sidebar > *Artifacts* tab"); cam = (330, 380, 1.8); clicks = [f_tab + 0.5]
        if t > f_tab + 0.5:
            cards = [dict(t="Study planner", d="Doc, just now", n=True), dict(t="Quiz game", d="Interactive tool"), dict(t="Trip itinerary", d="Doc")]
            st.update(page="artifacts", cards=cards[:1 + int(min(2, max(0, (t - f_tab - 0.9) / 0.5)))], side="artifacts", art=None, msgs=None); cam = (800, 380, 1.5)
            if t > f_later: step = (5, "Baad me *dobara* khol sakte ho")
    else:                      # plans
        items = []
        if t > p1: items.append("Free accounts: artifact chat me")
        if t > p2: items.append("Docs, Slides, Design: sab plans")
        st.update(page="plans", plans=items, side=None, cx=None); step = ("PLANS", "Kaun use kar sakta hai"); cam = (750, 440, 1.4)
    return st, step, cam, clicks


def cam_at(t):
    """camera keyframes: follow state()'s cam but smoothed by sampling a few frames back/forward"""
    return None


class Renderer:
    def __init__(self):
        self.pw = sync_playwright().start(); self.b = self.pw.chromium.launch(); self.pg = self.b.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1.5)
        self.pg.goto((HERE / "ui3.html").as_uri()); self.cam = None; self.stock = None; self.scene = -1; self.last = None; self.xf = None
    def shot(self, st):
        self.pg.evaluate("(s)=>ui(s)", st)
        return cv2.cvtColor(cv2.imdecode(np.frombuffer(self.pg.screenshot(type="jpeg", quality=90), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)


def camera(img, cam, punch=0.0):
    cx, cy, z = cam; z = max(1.4, z) * (1 + punch); S = img.shape[1] / 1500
    cw = 1500 / z; ch = cw * 1100 / 1080
    cx = min(max(cx, cw / 2), 1500 - cw / 2); cy = min(max(cy, ch / 2), 1100 - ch / 2)
    # sub-pixel centre (getRectSubPix) + a fixed-size window, so slow moves never step by whole pixels
    wp, hp = int(round(cw * S)), int(round(ch * S))
    crop = cv2.getRectSubPix(img, (wp, hp), (cx * S, cy * S))
    return cv2.resize(crop, (1080, 1100), interpolation=cv2.INTER_AREA)


def banner(fr, step, t, t_start):
    if not step: return
    n, label = step; a = ease_out((t - t_start) / 0.3)
    hl = set(re.sub(r"\*", "", w) for w in label.split(" ") if "*" in w)
    if n:
        pill = Image.new("RGBA", (260, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(pill); d.rounded_rectangle((0, 0, 259, 95), 48, fill=ORG + (255,)); f = ImageFont.truetype(FONT, 52)
        txt = f"STEP {n}" if isinstance(n, int) else str(n); d.text((130 - f.getlength(txt) / 2, 14), txt, font=f, fill=(20, 20, 20, 255))
        paste_rgba(fr, np.array(pill), 60, 90, alpha=a)
    sp = text_sprite(label.replace("*", ""), 56, hl=hl, color=(255, 255, 255)); sp = cv2.resize(sp, (min(sp.shape[1], 960), round(sp.shape[0] * min(sp.shape[1], 960) / sp.shape[1])), interpolation=cv2.INTER_AREA) if sp.shape[1] > 960 else sp
    paste_rgba(fr, sp, 40, 205 + int((1 - a) * 20), alpha=a)


CAPS = [(s_need, "Artifacts ke liye *ye zaroori*", 2.6), (c_open, "artifact *bagal me* khulta hai", 2.6), (e_done, "Claude *wahin* edit karta hai", 2.4), (x_w, "Word, PDF, Markdown, *Google Docs*", 3.0),
        (f_later, "baad me *dobara* khol sakte ho", 2.6), (p1, "free par bhi *chat me*", 2.2), (p2, "Docs, Slides, Design: *sab plans*", 2.6)]


def caption_at(fr, t):
    for t0, cap, dur in CAPS:
        if t0 <= t < t0 + dur:
            toks = cap.split(" "); k = len(toks); lt = t - t0; shown = [j for j in range(k) if lt >= 0.12 * j]
            hl = set(re.sub(r"\*", "", x) for x in toks if "*" in x); parts = [x.replace("*", "") for x in toks[:len(shown)]]
            brk = (k + 1) // 2 if len(cap.replace("*", "")) > 20 else k; ln = " ".join(parts[:brk]) + (("\n" + " ".join(parts[brk:])) if len(parts) > brk else "")
            sp = text_sprite(ln, 70, hl=hl)
            if sp.shape[1] > 1000: sp = cv2.resize(sp, (1000, round(sp.shape[0] * 1000 / sp.shape[1])), interpolation=cv2.INTER_AREA)
            a = min(1, lt / 0.15) * min(1, (dur - lt) / 0.2); paste_rgba(fr, sp, (W - sp.shape[1]) // 2, 1640 - (sp.shape[0] - 100 if "\n" in ln else 0), alpha=a)
            return


STOCK = {}


def stock_frame(t):
    if not STOCK:
        cap = cv2.VideoCapture(str(ROOT / "channels/devrobolab/stories/037_cfe02-video/raw/typing_close.mp4")); cap.set(cv2.CAP_PROP_POS_MSEC, 500); STOCK.update(cap=cap, t=0.5, last=None)
    while STOCK["t"] < 0.5 + t or STOCK["last"] is None:
        ok, f = STOCK["cap"].read()
        if not ok: break
        STOCK["last"] = f; STOCK["t"] += 1 / 30.0
    f = cv2.cvtColor(STOCK["last"], cv2.COLOR_BGR2RGB); h, w = f.shape[:2]; s = H / h * 1.05
    r = cv2.resize(f, (int(w * s), int(h * s))); x0 = (r.shape[1] - W) // 2; return r[:H, x0:x0 + W]


yy, xx = np.mgrid[0:H, 0:W]; VIG = (1 - 0.22 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)).astype(np.float32)
STEP_T = {}


def frame(R, k):
    t = k / FPS; scene = max(i for i in range(8) if START[i] <= t + 1e-6)
    if scene == 7:   # CTA
        fr = np.zeros((H, W, 3), np.uint8); fr[:] = (12, 12, 12); lt = t - START[7]
        words_reveal("DevRoboLab\nko follow karo", 110, lt, 0.2, 1.4, 520, fr, hl={"DevRoboLab"})
        a = ease_back((lt - 1.3) / 0.5); btn = Image.new("RGBA", (520, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(btn)
        d.rounded_rectangle((0, 0, 519, 189), 95, fill=ORG + (255,)); f = ImageFont.truetype(FONT, 100); d.text((260 - f.getlength("Follow") / 2, 36), "Follow", font=f, fill=(20, 20, 20, 255))
        paste_rgba(fr, np.array(btn), 280, 900, alpha=min(1, a), scale=max(0.01, a))
    else:
        st, step, cam, clicks = state(t)
        if step:
            k2 = (scene, step[0], step[1]); STEP_T.setdefault(k2, t); cam = (cam[0], cam[1], cam[2] * (1 + 0.10 * ease_out(min(1, (t - STEP_T[k2]) / 3.5))))
        elif scene == 0:
            cam = (cam[0], cam[1], cam[2] * (1 + 0.12 * ease_out(min(1, max(0, t - hk) / 3.0))))
        if st.get('cx') is not None: st['cx'] += 5 * math.sin(t * 2.7); st['cy'] += 4 * math.cos(t * 2.1)
        st['pulse'] = 0.5 + 0.5 * math.sin(t * 5.2); st['blink'] = int(t * 2.5) % 2 == 0
        if scene == 0 and t < hk:   # hook: stock cutaway first
            fr = stock_frame(t)
            fr = (fr.astype(np.float32) * 0.8).astype(np.uint8)
            words_reveal("doc, slides ya *tool* banwana hai?".replace("*", ""), 78, t, 0.3, 1.2, 1560, fr, hl={"tool"})
        else:
            img = R.shot(st)
            punch = max([0.08 * max(0, 1 - abs(t - c) / 0.18) for c in clicks] + [0.0])
            if R.cam is None: R.cam = list(cam)
            R.cam = [R.cam[i] + (cam[i] - R.cam[i]) * 0.24 for i in range(3)]; c = (R.cam[0] + 8 * math.sin(t * 1.5), R.cam[1] + 6 * math.cos(t * 1.2), R.cam[2] * (1 + 0.02 * math.sin(t * 1.05)))
            view = camera(img, c, punch)
            fr = np.zeros((H, W, 3), np.uint8); fr[:] = (0, 0, 0); fr[330:1430] = view
            if step:
                key2 = (scene, step[0], step[1]); STEP_T.setdefault(key2, t); banner(fr, step, t, STEP_T[key2])
            caption_at(fr, t)
    fr = (fr.astype(np.float32) * VIG[..., None]).astype(np.uint8)
    cv2.rectangle(fr, (0, 0), (int(W * t / TOTAL), 10), ORG[::-1][::-1], -1)
    if R.scene != scene: R.xf = R.last; R.scene = scene
    if R.xf is not None and scene > 0 and t - START[scene] < TR:
        a = ease_io((t - START[scene]) / TR); fr = (R.xf.astype(np.float32) * (1 - a) + fr.astype(np.float32) * a).astype(np.uint8)
    R.last = fr
    return fr


def build_voice():
    voice = HERE / "build/voice.wav"
    with wave.open(str(voice), "wb") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
        for w in waves:
            with wave.open(str(w)) as r: o.writeframes(b"\x00\x00" * int(SR * LEAD) + r.readframes(r.getnframes()) + b"\x00\x00" * int(SR * AFTER))
    return voice


def render(limit=None):
    voice = build_voice(); out = HERE / "output/short_demo.mp4"
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(voice), "-ss", "6", "-i", str(ROOT / "shared/music/presentation/Funkorama.mp3"),
           "-filter_complex", "[2:a]volume=-24dB,aformat=sample_rates=24000:channel_layouts=mono[m];[1:a]aformat=sample_rates=24000:channel_layouts=mono[v];[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out)]
    R = Renderer(); p = subprocess.Popen(cmd, stdin=subprocess.PIPE); N = int(TOTAL * FPS)
    for k in range(N):
        p.stdin.write(frame(R, k).tobytes())
        if k % 150 == 0: print(f"  frame {k}/{N}", flush=True)
    p.stdin.close(); p.wait(); print("done")


if __name__ == "__main__":
    print("starts", [round(x, 1) for x in START], "total", round(TOTAL, 1), flush=True)
    if len(sys.argv) > 1 and sys.argv[1] == "render": render()
