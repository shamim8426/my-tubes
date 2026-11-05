"""Claude Feature 02 (Projects) - UI WALKTHROUGH version (user 2026-11-06: demo first, chat inside, step by step, same editing motions).
ui2.html = illustration of the app built ONLY from the official help steps (labelled on screen: not a screen recording). Playwright renders each frame,
a virtual camera zooms/pans to the active area, cursor/typing/chat are driven by spoken-word times (Whisper wt.json). Dark theme + Claude-Code orange.
Editing: kinetic captions, step banner, click punch-in, cross-dissolves, progress bar, vignette + grain, no sound effects (voice + music only).
Run: python make.py render"""
import json, re, subprocess, sys, wave
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
waves = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(7)]
D = [LEAD + wav_dur(w) + AFTER for w in waves]; START = [sum(D[:i]) for i in range(7)]; TOTAL = sum(D)
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


FILES = ["physics_ch1.pdf", "maths_formulas.txt"]
CARDS = [{"t": "Home budget", "d": "Monthly"}, {"t": "Trip plan", "d": "Goa"}]
INS = "Explain in simple Hinglish, with one example."
REPLY = "Simple Hinglish me: paudhe dhoop se apna khana banate hain. Example: jaise aap roti banate ho, paudha dhoop + paani + CO2 se glucose banata hai."

# ---- key times
hk = T("hook", "Claude में Projects"); sd = T("create", "Sidebar में"); c1 = T("create", "click करो।"); bt = T("create", "ऊपर दाईं"); c2 = T("create", "दबाओ।")
nm = T("create", "Project का नाम"); ds = T("create", "description लिखो।"); nt = T("create", "ध्यान रखो,")
kp = T("knowledge", "Project knowledge में"); kc = T("knowledge", "दबाओ,"); kf = T("knowledge", "अपनी files"); ka = T("knowledge", "ये files")
ip = T("instr", "Set project"); ic = T("instr", "दबाओ,"); iw = T("instr", "लिखो कि"); isv = T("instr", "save करो।"); ich = T("instr", "फिर chat"); ians = T("instr", "जवाब इन्हीं")
cx1 = T("ctx", "एक chat"); cx2 = T("ctx", "वो दूसरी"); cx3 = T("ctx", "जो हर"); cx4 = T("ctx", "उसे project")
fr1 = T("free", "पर free users"); fr2 = T("free", "पाँच projects")
S_create, S_know, S_instr, S_ctx, S_free = START[1], START[2], START[3], START[4], START[5]


def state(t):
    """UI state at absolute time t (dict for ui2.html) + step banner (n, label) + camera (cx, cy, zoom) + click time."""
    st = dict(page="projects", cards=CARDS, cx=None, cy=None); step = None; cam = (700, 560, 1.25); clicks = []
    if t < S_create:   # hook: Projects page idle
        st.update(page="projects", cx=900, cy=500); cam = (700, 560, 1.25)
    elif t < S_know:   # create: steps 1-3
        st.update(page="projects", cards=CARDS)
        px, py = path([(S_create, 900, 500), (sd + 0.2, 900, 500), (c1 - 0.05, 150, 273), (bt, 150, 273), (bt + 0.9, 1302, 93), (c2 + 0.1, 1302, 93)], t)
        st.update(cx=px, cy=py); step = (1, "Sidebar me *Projects* par click"); cam = (420, 330, 1.9)
        if t > c1 - 0.05: st.update(sideHl=True)
        if t >= c1 + 0.1 and t < bt: step = (1, "Sidebar me *Projects* par click"); cam = (420, 330, 1.9)
        if t >= bt - 0.3: step = (2, "Upar daayein: *+ New Project*"); cam = (1100, 190, 1.8)
        if t > c2 - 0.05 and t < nm - 0.2: st.update(btnHl=True)
        clicks = [c1, c2]
        if t >= c2 + 0.15:   # modal opens (step 3)
            n_txt = typ("Class 12 notes", t, nm + 0.1, nm + 1.2); d_txt = typ("Physics and maths chapters", t, ds - 1.0, ds + 0.7)
            fa = "d" if t > ds - 1.1 else "n"
            st.update(btnHl=False, sideHl=False, sideOn=True, modal=dict(title="Create a project", btn="Create project", fields=[dict(l="Project name", v=n_txt, act=fa == "n"), dict(l="Description", v=d_txt, act=fa == "d")]))
            px, py = path([(c2 + 0.15, 1302, 93), (nm, 990, 318), (ds - 1.1, 990, 318), (ds - 0.9, 990, 426)], t); st.update(cx=px, cy=py)
            step = (3, "*Naam + description* likho"); cam = (990, 390, 1.55)
            if t > nt: step = (3, "Claude ko ye *nahi dikhta*")
    elif t < S_instr:  # knowledge: step 4
        p = dict(files=[], plusHl=False)
        px, py = path([(S_know, 1200, 330), (kp + 0.2, 1200, 330), (kc - 0.1, 1389, 78)], t)
        if t > kc - 0.1: p["plusHl"] = True
        if t > kc + 0.6: p["files"] = FILES[:1]
        if t > kf + 0.5: p["files"] = FILES
        st.update(page="project", title="Class 12 notes", panel=p, cx=px, cy=py, inp=None); step = (4, "Knowledge me *+* se files daalo"); cam = (1150, 260, 1.7); clicks = [kc]
        if t > kc + 0.8: st.update(cx=px, cy=py + 40)
        if t > ka: step = (4, "Files *sari chats* me kaam aati hain"); cam = (1000, 380, 1.4)
    elif t < S_ctx:    # instructions + chat: step 5
        p = dict(files=FILES, plusHl=False, insHl=False, saved=None)
        px, py = path([(S_instr, 1200, 400), (ip, 1200, 400), (ic - 0.1, 1185, 318)], t)
        st.update(page="project", title="Class 12 notes", panel=p, cx=px, cy=py); step = (5, "*Set project instructions* dabao"); cam = (1150, 330, 1.7); clicks = [ic, isv]
        if t > ic - 0.1: p["insHl"] = True
        if t >= ic + 0.25 and t < isv + 0.6:
            st.update(modal=dict(title="Project instructions", btn="Save instructions", hl=t > isv - 0.1, fields=[dict(l="How should the assistant respond?", v=typ(INS, t, iw, isv - 0.3), tall=True, act=True)]))
            px, py = path([(ic + 0.25, 1185, 318), (iw, 990, 330), (isv - 0.5, 990, 330), (isv - 0.1, 1260, 560)], t); st.update(cx=px, cy=py); step = (5, "Likho aur *Save* karo"); cam = (990, 420, 1.5)
        if t >= isv + 0.6:
            p["saved"] = "Instructions: " + INS; p["insHl"] = False
            q = "Photosynthesis kya hai?"; qt = typ(q, t, ich + 0.1, ich + 1.5)
            msgs = []; inp = qt; send = False
            if t > ich + 1.6: msgs = [dict(r="u", t=q)]; inp = None
            if t > ich + 1.6 and t < ich + 1.9: send = True
            if t > ich + 2.0: msgs.append(dict(r="a", t=typ(REPLY, t, ich + 2.0, ians + 1.5)))
            st.update(msgs=msgs, inp=inp or None, inpAct=True, sendHl=send)
            px, py = path([(isv + 0.6, 1260, 560), (ich + 0.1, 560, 1005), (ich + 1.5, 560, 1005), (ich + 1.65, 1050, 1005), (ich + 2.2, 800, 700)], t); st.update(cx=px, cy=py)
            step = (5, "Chat me sawal: jawab *instructions* ke hisaab se"); cam = (740, 640, 1.35); clicks = [ich + 1.62]
    elif t < S_free:   # ctx
        files = FILES + (["exam_date.txt"] if t > cx4 + 0.8 else [])
        tab = 0 if t < cx2 + 0.4 else 1
        c1m = [dict(r="u", t="Mera exam 15 tarikh ko hai."), dict(r="a", t="Theek hai, noted.")] if t > S_ctx + 0.5 else []
        if tab == 0:
            msgs = [dict(r="u", t=typ("Mera exam 15 tarikh ko hai.", t, cx1 + 0.2, cx1 + 1.3))] if t < cx1 + 1.4 else c1m
            if t > cx1 + 1.4: msgs = [c1m[0], dict(r="a", t=typ("Theek hai, noted.", t, cx1 + 1.6, cx1 + 2.2))]
        else:
            msgs = [dict(r="u", t="Mera exam kab hai?")] if t > cx2 + 0.8 else []
            if t > cx2 + 1.6: msgs.append(dict(r="a", t=typ("Mujhe is chat me exam ki date nahi dikh rahi. Use project knowledge me daal do.", t, cx2 + 1.6, cx2 + 3.4)))
        st.update(page="project", title="Class 12 notes", panel=dict(files=files), tabs=["Chat 1", "Chat 2"], tabOn=tab, msgs=msgs, inp=None)
        px, py = path([(S_ctx, 700, 700), (cx2 - 0.3, 700, 700), (cx2 + 0.3, 520, 175), (cx2 + 1.0, 560, 1005), (cx3, 560, 1005), (cx4 + 0.3, 1389, 78)], t)
        st.update(cx=px, cy=py); step = (6, "Ek chat ka context *dusri me nahi*"); cam = (740, 620, 1.35); clicks = [cx2 + 0.3]
        if t > cx3: step = (6, "Jo har chat me chahiye: *knowledge* me daalo"); cam = (1000, 380, 1.4)
    else:              # free
        cards = [dict(t=n, d=d) for n, d in [("Class 12 notes", "Physics"), ("Home budget", "Monthly"), ("Trip plan", "Goa"), ("Resume", "Job"), ("Side project", "Ideas")]]
        n_show = 1 + int(min(4, max(0, (t - S_free - 0.2) / 0.55)))
        st.update(page="projects", cards=cards[:n_show], counter=f"{n_show} / 5 projects (free plan)", cx=None); step = (0, "Free plan: *5 projects* tak"); cam = (700, 380, 1.4)
        if t > fr2 + 0.2: st.update(counter="5 / 5 projects (free plan)")
    return st, step, cam, clicks


def cam_at(t):
    """camera keyframes: follow state()'s cam but smoothed by sampling a few frames back/forward"""
    return None


class Renderer:
    def __init__(self):
        self.pw = sync_playwright().start(); self.b = self.pw.chromium.launch(); self.pg = self.b.new_page(viewport={"width": 1500, "height": 1100}, device_scale_factor=1.5)
        self.pg.goto((HERE / "ui2.html").as_uri()); self.cam = None; self.stock = None
    def shot(self, st):
        self.pg.evaluate("(s)=>ui(s)", st)
        return cv2.cvtColor(cv2.imdecode(np.frombuffer(self.pg.screenshot(type="jpeg", quality=90), np.uint8), cv2.IMREAD_COLOR), cv2.COLOR_BGR2RGB)


def camera(img, cam, punch=0.0):
    cx, cy, z = cam; z = max(1.4, z) * (1 + punch); S = img.shape[1] / 1500
    cw = 1500 / z; ch = cw * 1100 / 1080
    cx = min(max(cx, cw / 2), 1500 - cw / 2); cy = min(max(cy, ch / 2), 1100 - ch / 2)
    x0, y0 = int((cx - cw / 2) * S), int((cy - ch / 2) * S); x1, y1 = int((cx + cw / 2) * S), int((cy + ch / 2) * S)
    return cv2.resize(img[max(0, y0):y1, max(0, x0):x1], (1080, 1100), interpolation=cv2.INTER_AREA)


def banner(fr, step, t, t_start):
    if not step: return
    n, label = step; a = ease_out((t - t_start) / 0.3)
    hl = set(re.sub(r"\*", "", w) for w in label.split(" ") if "*" in w)
    if n:
        pill = Image.new("RGBA", (260, 96), (0, 0, 0, 0)); d = ImageDraw.Draw(pill); d.rounded_rectangle((0, 0, 259, 95), 48, fill=ORG + (255,)); f = ImageFont.truetype(FONT, 52)
        txt = f"STEP {n}"; d.text((130 - f.getlength(txt) / 2, 14), txt, font=f, fill=(20, 20, 20, 255))
        paste_rgba(fr, np.array(pill), 60, 90, alpha=a)
    sp = text_sprite(label.replace("*", ""), 56, hl=hl, color=(255, 255, 255)); sp = cv2.resize(sp, (min(sp.shape[1], 960), round(sp.shape[0] * min(sp.shape[1], 960) / sp.shape[1])), interpolation=cv2.INTER_AREA) if sp.shape[1] > 960 else sp
    paste_rgba(fr, sp, 40, 205 + int((1 - a) * 20), alpha=a)


CAPS = [(T("create", "ध्यान रखो,"), "Claude ko ye *nahi dikhta*", 2.6), (ka, "files *sari chats* me kaam aati hain", 2.4), (ians, "jawab *instructions* ke hisaab se", 2.8),
        (cx2, "ek chat ka context *dusri me nahi*", 3.0), (cx4, "jo chahiye, *knowledge* me daalo", 2.6), (fr2, "free = *5 projects*", 2.2)]


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
        cap = cv2.VideoCapture(str(ROOT / "channels/devrobolab/stories/037_cfe02-video/raw/overwhelmed.mp4")); cap.set(cv2.CAP_PROP_POS_MSEC, 500); STOCK.update(cap=cap, t=0.5, last=None)
    while STOCK["t"] < 0.5 + t or STOCK["last"] is None:
        ok, f = STOCK["cap"].read()
        if not ok: break
        STOCK["last"] = f; STOCK["t"] += 1 / 30.0
    f = cv2.cvtColor(STOCK["last"], cv2.COLOR_BGR2RGB); h, w = f.shape[:2]; s = H / h * 1.05
    r = cv2.resize(f, (int(w * s), int(h * s))); x0 = (r.shape[1] - W) // 2; return r[:H, x0:x0 + W]


yy, xx = np.mgrid[0:H, 0:W]; VIG = (1 - 0.22 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)).astype(np.float32)
STEP_T = {}


def frame(R, k):
    t = k / FPS; scene = max(i for i in range(7) if START[i] <= t + 1e-6)
    if scene == 6:   # CTA
        fr = np.zeros((H, W, 3), np.uint8); fr[:] = (12, 12, 12); lt = t - START[6]
        words_reveal("DevRoboLab\nko follow karo", 110, lt, 0.2, 1.4, 520, fr, hl={"DevRoboLab"})
        a = ease_back((lt - 1.3) / 0.5); btn = Image.new("RGBA", (520, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(btn)
        d.rounded_rectangle((0, 0, 519, 189), 95, fill=ORG + (255,)); f = ImageFont.truetype(FONT, 100); d.text((260 - f.getlength("Follow") / 2, 36), "Follow", font=f, fill=(20, 20, 20, 255))
        paste_rgba(fr, np.array(btn), 280, 900, alpha=min(1, a), scale=max(0.01, a))
    else:
        st, step, cam, clicks = state(t)
        if scene == 0 and t < hk:   # hook: stock cutaway first
            fr = stock_frame(t)
            fr = (fr.astype(np.float32) * 0.8).astype(np.uint8)
            words_reveal("har chat me *wahi files*?".replace("*", ""), 78, t, 0.3, 1.2, 1560, fr, hl={"wahi", "files?"})
        else:
            if scene == 0: st.update(cx=900 - 60 * min(1, (t - hk) / 1.0), cy=500)
            img = R.shot(st)
            punch = max([0.07 * max(0, 1 - abs(t - c) / 0.25) for c in clicks] + [0.0])
            if R.cam is None: R.cam = list(cam)
            R.cam = [R.cam[i] + (cam[i] - R.cam[i]) * 0.10 for i in range(3)]; c = tuple(R.cam)
            view = camera(img, c, punch)
            fr = np.zeros((H, W, 3), np.uint8); fr[:] = (0, 0, 0); fr[330:1430] = view
            if step:
                key2 = (scene, step[0], step[1]); STEP_T.setdefault(key2, t); banner(fr, step, t, STEP_T[key2])
            caption_at(fr, t)
    if scene > 0 and t - START[scene] < TR * 0.5:   # soft dip at scene change
        a = 1 - ease_io((t - START[scene]) / (TR * 0.5)); fr = (fr.astype(np.float32) * (1 - 0.6 * a)).astype(np.uint8)
    fr = (fr.astype(np.float32) * VIG[..., None]).astype(np.uint8)
    cv2.rectangle(fr, (0, 0), (int(W * t / TOTAL), 10), ORG[::-1][::-1], -1)
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
