"""Claude Feature 02 (Projects) - VIDEO version (user 2026-11-06: images did not match the words, cut sounds irritating, wants MOTION VIDEOS not stills).
Every beat = a real stock VIDEO clip (Mixkit 'Free License') that shows what is being said, or the official help page scrolling (real pixels of our screenshot).
Cut exactly on the spoken word (Whisper word times, wt.json). Smooth cross-dissolves, NO sound effects at cuts (voice + low music only).
Run: python make.py render"""
import json, re, subprocess, sys, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import *

LEAD, AFTER, SR, TR = 0.30, 0.28, 24000, 0.45
deck = json.load(open(HERE.parent / "034_cfe02-projects/deck.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]; VOICE = {s["id"]: re.sub(r"\s+", " ", s["voice"]).strip() for s in deck["scenes"]}
waves = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(7)]
D = [LEAD + wav_dur(w) + AFTER for w in waves]; START = [sum(D[:i]) for i in range(7)]; TOTAL = sum(D)
WT = json.load(open(HERE / "wt.json", encoding="utf-8"))


def tok_time(scene, phrase):
    i = IDS.index(scene); toks = WT[scene]["tokens"]; words = VOICE[scene].split(" ")
    if phrase is None: return START[i]
    pw = phrase.split(" ")
    for k in range(len(words)):
        if words[k:k + len(pw)] == pw:
            if WT[scene]["n_whisper"] < 0.85 * WT[scene]["n_tokens"]:
                ch = len(" ".join(words[:k])) / max(1, len(VOICE[scene])); return START[i] + LEAD + WT[scene]["voice_s"] * ch * 0.97 - 0.12
            return START[i] + LEAD + toks[k][1] - 0.12
    raise ValueError(f"phrase not found: {phrase!r} in {scene}")


# (scene, start phrase, kind, source, start offset in clip / scroll y0, caption, callout)
B = [("hook", None, "vid", "overwhelmed", 0.5, "har baar *wahi files*?", None),
     ("hook", "Claude में Projects", "vid", "laptop_man", 4.0, "*Projects* banao", None),
     ("hook", "हर project एक", "vid", "open_office", 2.0, "har project = *alag workspace*", None),
     ("create", None, "scroll", "create", 560, "Projects > *+ New Project*", None),
     ("create", "और नाम", "vid", "typing_close", 3.0, "*naam + description* do", None),
     ("create", "ध्यान रखो,", "scroll", "create2", 600, "Claude ko ye *nahi dikhta*", None),
     ("knowledge", None, "vid", "hand_sheet", 0.5, "*documents* daalo", None),
     ("knowledge", "text या code", "vid", "code_close", 3.0, "text, *code* bhi", None),
     ("knowledge", "जो भी", "vid", "whatsapp", 2.0, "sab *chats* me kaam aayega", "knowledge"),
     ("instr", None, "vid", "todo_list", 1.0, "*Set project instructions*", "instr"),
     ("instr", "ये instructions", "vid", "phone_typing", 3.0, "har chat par *lagu*", None),
     ("ctx", None, "vid", "padlock_door", 4.0, "chats ke beech *context share nahi*", "ctx"),
     ("ctx", "जो चाहिए,", "vid", "sticky_note", 2.5, "jo chahiye, *knowledge* me daalo", None),
     ("free", None, "vid", "woman_phone", 1.0, "*free* accounts par bhi", None),
     ("free", "पाँच projects", "five", "woman_list", 3.0, "free = *5 projects*", "free"),
     ("follow", None, "cta", "macbook", 0.0, "", None)]
BS = [tok_time(s, p) for s, p, *_ in B]; BE = BS[1:] + [TOTAL]
F = lambda s: ImageFont.truetype(FONT, s)


class Clip:
    def __init__(self, name, ss):
        self.cap = cv2.VideoCapture(str(HERE / "raw" / f"{name}.mp4")); self.fps = self.cap.get(cv2.CAP_PROP_FPS) or 24
        self.cap.set(cv2.CAP_PROP_POS_MSEC, ss * 1000); self.t = ss - 1 / self.fps; self.last = None
    def get(self, lt, ss):
        want = ss + lt
        while self.t < want - 0.5 / self.fps:
            ok, f = self.cap.read()
            if not ok: break
            self.last = f; self.t += 1 / self.fps
        return cv2.cvtColor(self.last, cv2.COLOR_BGR2RGB) if self.last is not None else np.zeros((H, W, 3), np.uint8)


def fit_portrait(f, p, pan=0.0, zoom=0.10):
    h, w = f.shape[:2]; z = 1.0 + zoom * ease_out(p)
    s = (H / h) * z if w >= h else max(W / w, H / h) * z
    r = cv2.resize(f, (int(w * s) + 1, int(h * s) + 1), interpolation=cv2.INTER_CUBIC if s < 2 else cv2.INTER_LINEAR)
    x0 = int((r.shape[1] - W) / 2 + pan * (r.shape[1] - W) * 0.35 * (p - 0.5)); y0 = (r.shape[0] - H) // 2
    x0 = max(0, min(r.shape[1] - W, x0)); return r[y0:y0 + H, x0:x0 + W]


FULL = load(HERE / "shots/_full.png")          # 2x screenshot of the official 'create and manage projects' article
SPR = {n: load(HERE / "cut" / f"shot_{n}.png", "RGBA") for n in ["knowledge", "instr", "ctx", "free"]}
CH = sprite_w(HERE.parent / "034_cfe02-projects/cut/char_3.png", 400)
clips = {}


def beat_frame(n, t):
    s, p, kind, src, ss, cap, call = B[n]; dur = BE[n] - BS[n]; pr = t / max(dur, 0.2)
    if kind in ("vid", "five", "cta"):
        if n not in clips: clips[n] = Clip(src, ss)
        f = clips[n].get(t, ss); fr = fit_portrait(f, pr, pan=1.0 if n % 2 else -1.0, zoom=0.10)
        if kind == "five":
            a = ease_back((t - 0.25) / 0.45); s5 = text_sprite("5", 460, YEL); paste_rgba(fr, s5, (W - s5.shape[1]) // 2, 640, alpha=min(1, a), scale=max(0.01, a))
        if kind == "cta":
            fr = (fr.astype(np.float32) * 0.45).astype(np.uint8)
            words_reveal("DevRoboLab\nko follow karo", 110, t, 0.2, 1.4, 330, fr)
            a = ease_back((t - 1.3) / 0.5); btn = Image.new("RGBA", (520, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(btn)
            d.rounded_rectangle((0, 0, 519, 189), 95, fill=YEL + (255,)); d.text((260 - F(100).getlength("Follow") / 2, 36), "Follow", font=F(100), fill=(20, 20, 20, 255))
            paste_rgba(fr, np.array(btn), 280, 760, alpha=min(1, a), scale=max(0.01, a)); paste_rgba(fr, CH, 330, 1380, alpha=min(1, max(0, (t - 0.6) / 0.2)), scale=0.6 + 0.4 * ease_back((t - 0.6) / 0.45))
        return fr
    # scroll: the official page moving (real pixels), slight zoom
    wnd_w = 840; wnd_h = round(wnd_w * H / W); y0 = int(ss + (180 if src == "create" else 60) * ease_io(pr)); z = 1.0 + (0.10 if src == "create" else 0.35) * ease_out(pr)
    cw, ch = wnd_w / z, wnd_h / z; cy = y0 + wnd_h / 2 - (0 if src == "create" else 150 * z / 1.35)
    x0 = (FULL.shape[1] - cw) / 2; yy0 = cy - ch / 2
    M = np.float32([[W / cw, 0, -x0 * W / cw], [0, H / ch, -yy0 * H / ch]])
    return cv2.warpAffine(FULL, M, (W, H), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def caption(fr, n, t):
    cap = B[n][5]
    if not cap: return
    toks = cap.split(" "); T0, T1 = 0.15, min(1.2, (BE[n] - BS[n]) * 0.55); k = len(toks)
    shown = [j for j in range(k) if t >= T0 + (T1 - T0) * j / max(1, k)]
    if not shown: return
    hl = set(re.sub(r"[*]", "", x) for x in toks if "*" in x); brk = (k + 1) // 2 if len(cap.replace("*", "")) > 20 else k
    parts = [x.replace("*", "") for x in toks[:len(shown)]]
    ln = " ".join(parts[:brk]) + (("\n" + " ".join(parts[brk:])) if len(parts) > brk else "")
    sp = text_sprite(ln, 78, hl=hl)
    if sp.shape[1] > 1000: sp = cv2.resize(sp, (1000, round(sp.shape[0] * 1000 / sp.shape[1])), interpolation=cv2.INTER_AREA)
    last_t = T0 + (T1 - T0) * (len(shown) - 1) / max(1, k); pop = 1.0 + 0.10 * max(0, 1 - (t - last_t) / 0.2)
    paste_rgba(fr, sp, (W - sp.shape[1]) // 2, 1560 - (sp.shape[0] - 120 if "\n" in ln else 0), alpha=1.0, scale=pop)


def callout(fr, n, t):
    call = B[n][6]; t0 = 1.0
    if not call or t < t0: return
    s = SPR[call]; w = 860; s = cv2.resize(s, (w, round(s.shape[0] * w / s.shape[1])), interpolation=cv2.INTER_AREA)
    a = ease_out((t - t0) / 0.6); paste_rgba(fr, s, 110, int(190 - (1 - a) * 160), alpha=a)


yy, xx = np.mgrid[0:H, 0:W]; VIG = (1 - 0.20 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)).astype(np.float32)


def gradient_bottom(fr):
    """soft dark gradient under the caption so it is readable on any clip."""
    g = np.linspace(0, 1, 560, dtype=np.float32) ** 1.5 * 0.55
    fr[H - 560:] = (fr[H - 560:].astype(np.float32) * (1 - g)[:, None, None]).astype(np.uint8)


def render_frame(k):
    t = k / FPS; n = max(j for j in range(len(B)) if BS[j] <= t + 1e-6); lt = t - BS[n]
    fr = beat_frame(n, lt)
    if n > 0 and lt < TR:
        prev = beat_frame(n - 1, t - BS[n - 1]); a = ease_io(lt / TR)
        fr = (prev.astype(np.float32) * (1 - a) + fr.astype(np.float32) * a).astype(np.uint8)
        gradient_bottom(fr); caption(fr, n - 1, t - BS[n - 1]) if a < 0.5 else None
    else: gradient_bottom(fr)
    caption(fr, n, lt) if not (n > 0 and lt < TR * 0.5) else None
    callout(fr, n, lt)
    fr = (fr.astype(np.float32) * VIG[..., None]).astype(np.uint8)
    cv2.rectangle(fr, (0, 0), (int(W * t / TOTAL), 10), YEL, -1)
    return fr


def build_voice():
    voice = HERE / "build/voice.wav"; voice.parent.mkdir(exist_ok=True)
    with wave.open(str(voice), "wb") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
        for w in waves:
            with wave.open(str(w)) as r: o.writeframes(b"\x00\x00" * int(SR * LEAD) + r.readframes(r.getnframes()) + b"\x00\x00" * int(SR * AFTER))
    return voice


def render():
    voice = build_voice(); out = HERE / "output/short_video.mp4"; out.parent.mkdir(exist_ok=True)
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(voice), "-ss", "6", "-i", str(ROOT / "shared/music/presentation/Funkorama.mp3"),
           "-filter_complex", "[2:a]volume=-24dB,aformat=sample_rates=24000:channel_layouts=mono[m];[1:a]aformat=sample_rates=24000:channel_layouts=mono[v];[v][m]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); N = int(TOTAL * FPS)
    for k in range(N):
        p.stdin.write(render_frame(k).tobytes())
        if k % 150 == 0: print(f"  frame {k}/{N}", flush=True)
    p.stdin.close(); p.wait(); print("done")


if __name__ == "__main__":
    print("beats", [round(x, 1) for x in BS], "total", round(TOTAL, 1), flush=True)
    if len(sys.argv) > 1 and sys.argv[1] == "render": render()
