"""Claude Feature 02 (Projects) - EDITED version (user 2026-11-06: visuals must match the words, sync to the voice, real motion, real editing style).
Every beat = one visual that depicts the phrase being spoken, cut exactly on the spoken word (Whisper word times, wt.json).
Editing: cut every 2-4 s, whip-pan / flash transitions with SFX whoosh, 2.5D parallax + punch-in + shake, kinetic word-by-word captions,
callout screenshots that slide in on the trigger word with a UI pop SFX, top progress bar, vignette + light grain.
Run: python make.py prep   (parallax clips for AI beats)   then   python make.py render"""
import json, re, subprocess, sys, wave
from pathlib import Path
import cv2, numpy as np
from PIL import Image, ImageDraw, ImageFont
HERE = Path(__file__).parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from photo_video import *
from papercut import paper_rect

LEAD, AFTER, SR, TR = 0.30, 0.28, 24000, 0.24
deck = json.load(open(HERE.parent / "034_cfe02-projects/deck.json", encoding="utf-8"))
IDS = [s["id"] for s in deck["scenes"]]; VOICE = {s["id"]: re.sub(r"\s+", " ", s["voice"]).strip() for s in deck["scenes"]}
waves = [HERE / "audio/tts" / f"s_{i:02d}.wav" for i in range(7)]
D = [LEAD + wav_dur(w) + AFTER for w in waves]; START = [sum(D[:i]) for i in range(7)]; TOTAL = sum(D)
WT = json.load(open(HERE / "wt.json", encoding="utf-8"))


def tok_time(scene, phrase):
    """absolute time (s) when the first token of `phrase` is spoken (token index found in the voice text)."""
    i = IDS.index(scene); toks = WT[scene]["tokens"]; words = VOICE[scene].split(" ")
    if phrase is None: return START[i]
    pw = phrase.split(" ")
    for k in range(len(words)):
        if words[k:k + len(pw)] == pw:
            if WT[scene]["n_whisper"] < 0.85 * WT[scene]["n_tokens"]:   # Whisper dropped words: fall back to character position in the voice duration
                ch = len(" ".join(words[:k])) / max(1, len(VOICE[scene])); return START[i] + LEAD + WT[scene]["voice_s"] * ch * 0.97 - 0.12
            return START[i] + LEAD + toks[k][1] - 0.12
    raise ValueError(f"phrase not found: {phrase!r} in {scene}")


# (scene, start phrase, kind, source, caption (*key* in yellow), motion preset, callout screenshot)
B = [("hook", None, "ai", "messy", "har baar *wahi files*?", "push_in", None),
     ("hook", "Claude में Projects", "photo", "workspace_1", "*Projects* banao", None, None),
     ("hook", "हर project एक", "ai", "rooms", "har project = *alag workspace*", "pan_right", None),
     ("create", None, "shot", "create", "Projects > *+ New Project*", None, None),
     ("create", "और नाम", "photo", "workspace_0", "*naam + description* do", None, None),
     ("create", "ध्यान रखो,", "shot", "create2", "Claude ko ye *nahi dikhta*", None, None),
     ("knowledge", None, "photo", "binders_0", "*documents* daalo", None, None),
     ("knowledge", "text या code", "ai", "tofolder", "text, *code* bhi", "push_in", None),
     ("knowledge", "जो भी", "ai", "book", "sab *chats* me kaam aayega", "pull_out", "knowledge"),
     ("instr", None, "photo", "checklist_0", "*Set project instructions*", None, "instr"),
     ("instr", "ये instructions", "ai", "rooms", "har chat par *lagu*", "pull_out", None),
     ("ctx", None, "ai", "sealed", "chats ke beech *context share nahi*", "gentle_orbit", "ctx"),
     ("ctx", "जो चाहिए,", "ai", "drop", "jo chahiye, *knowledge* me daalo", "push_in", None),
     ("free", None, "photo", "workspace_2", "*free* accounts par bhi", None, None),
     ("free", "पाँच projects", "five", "pencils_0", "free = *5 projects*", None, "free"),
     ("follow", None, "cta", "pencils_0", "", None, None)]
BS = [tok_time(s, p) for s, p, *_ in B]
BE = BS[1:] + [TOTAL]


def parallax_path(n): return HERE / "clips" / f"b{n:02d}.mp4"


def prep():
    for n, (s, p, kind, src, cap, pre, call) in enumerate(B):
        if kind != "ai": continue
        out = parallax_path(n)
        if out.exists(): continue
        secs = round(BE[n] - BS[n] + 0.7, 2)
        print("parallax", n, src, secs, flush=True)
        subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "tools/parallax.py"), "clip", str(HERE / "ai" / f"{src}.png"), str(out), "--preset", pre, "--seconds", str(secs), "--format", "short"], check=True)


class Clip:
    def __init__(self, path): self.cap = cv2.VideoCapture(str(path)); self.n = 0; self.last = None
    def get(self, lt):
        want = int(lt * FPS)
        while self.n <= want:
            ok, f = self.cap.read()
            if not ok: break
            self.last = cv2.cvtColor(f, cv2.COLOR_BGR2RGB); self.n += 1
        return self.last


PH = {k: load(HERE / "raw" / f"{k}.jpg") for k in ["workspace_0", "workspace_1", "workspace_2", "binders_0", "checklist_0", "pencils_0"]}
BL = {k: blurred_fill(v, 0.5) for k, v in PH.items()}
for n in ["intro", "create", "knowledge", "instr", "ctx", "free"]:
    f = HERE / "cut" / f"shot_{n}.png"; f.parent.mkdir(exist_ok=True)
    if not f.exists(): paper_rect(Image.open(HERE / "shots" / f"{n}.png").convert("RGB"), border=26, seed=sum(map(ord, n)) % 97).save(f)
SPR = {n: load(HERE / "cut" / f"shot_{n}.png", "RGBA") for n in ["intro", "create", "knowledge", "instr", "ctx", "free"]}
CH = sprite_w(HERE.parent / "034_cfe02-projects/cut/char_3.png", 400)
F = lambda s: ImageFont.truetype(FONT, s)
clips = {}


def kb(img, t, dur, w=1080, z0=1.0, z1=1.22, pan=(0, 0), rot=0.0, shake=0.0):
    """strong Ken-Burns + optional tilt and shake; returns w x h' frame."""
    h = round(img.shape[0] * w / img.shape[1]); base = cv2.resize(img, (w, h), interpolation=cv2.INTER_CUBIC)
    p = ease_out(t / max(dur, 0.2)); z = z0 + (z1 - z0) * p
    cx = w / 2 + pan[0] * w * 0.12 * (p - 0.5) * 2; cy = h / 2 + pan[1] * h * 0.12 * (p - 0.5) * 2
    sx = shake * np.sin(t * 38) * 6; sy = shake * np.cos(t * 31) * 5
    M = cv2.getRotationMatrix2D((cx + sx, cy + sy), rot * (p - 0.5) * 2, z); M[0, 2] += w / 2 - cx; M[1, 2] += h / 2 - cy
    return cv2.warpAffine(base, M, (w, h), flags=cv2.INTER_CUBIC, borderMode=cv2.BORDER_REPLICATE)


def beat_frame(n, t):
    s, p, kind, src, cap, pre, call = B[n]; dur = BE[n] - BS[n]
    fr = np.zeros((H, W, 3), np.uint8)
    if kind == "ai":
        if n not in clips: clips[n] = Clip(parallax_path(n))
        f = clips[n].get(t + 0.0)
        if f is not None: fr[:] = cv2.resize(f, (W, H)) if f.shape[:2] != (H, W) else f
        z = 1.0 + 0.10 * ease_out(t / max(dur, 0.2)); M = np.float32([[z, 0, W * (1 - z) / 2], [0, z, H * (1 - z) / 2]])
        fr = cv2.warpAffine(fr, M, (W, H), flags=cv2.INTER_LINEAR)
    elif kind in ("photo", "five"):
        bg = BL[src]; zb = 1.0 + 0.10 * ease_out(t / max(dur, 0.2)); M = np.float32([[zb, 0, W * (1 - zb) / 2], [0, zb, H * (1 - zb) / 2]])
        fr[:] = cv2.warpAffine(bg, M, (W, H), borderMode=cv2.BORDER_REPLICATE)
        img = kb(PH[src], t, dur, 1080, 1.0, 1.30, (0.6, -0.4), rot=1.6, shake=0.4 if kind == "photo" else 0.0)
        paste(fr, img, 0, 560)
        if kind == "five":
            a = ease_back((t - 0.25) / 0.45); s5 = text_sprite("5", 460, YEL); paste_rgba(fr, s5, (W - s5.shape[1]) // 2, 700, alpha=min(1, a), scale=max(0.01, a))
    elif kind == "shot":
        fr[:] = BL["workspace_1"]; spr = SPR["create"]; zoom = 1.0 + 0.55 * ease_out(t / max(dur, 0.2))
        base = cv2.resize(spr, (940, round(spr.shape[0] * 940 / spr.shape[1])), interpolation=cv2.INTER_AREA)
        if src == "create2": zoom = 1.25 + 0.3 * ease_out(t / max(dur, 0.2))
        s = cv2.resize(base, (int(base.shape[1] * zoom), int(base.shape[0] * zoom)), interpolation=cv2.INTER_LINEAR)
        x = (W - s.shape[1]) // 2; y = 680 - int((zoom - 1) * 120)
        paste_rgba(fr, s, x, y, alpha=min(1, t / 0.15))
    else:  # cta
        fr[:] = BL["pencils_0"]; paste(fr, kb(PH["pencils_0"], t, dur, 1080, 1.0, 1.15), 0, 900)
        words_reveal("DevRoboLab\nko follow karo", 110, t, 0.2, 1.4, 330, fr)
        a = ease_back((t - 1.3) / 0.5); btn = Image.new("RGBA", (520, 190), (0, 0, 0, 0)); d = ImageDraw.Draw(btn)
        d.rounded_rectangle((0, 0, 519, 189), 95, fill=YEL + (255,)); d.text((260 - F(100).getlength("Follow") / 2, 36), "Follow", font=F(100), fill=(20, 20, 20, 255))
        paste_rgba(fr, np.array(btn), 280, 560, alpha=min(1, a), scale=max(0.01, a)); paste_rgba(fr, CH, 330, 1480, alpha=min(1, max(0, (t - 0.6) / 0.2)), scale=0.6 + 0.4 * ease_back((t - 0.6) / 0.45))
    return fr


def caption(fr, n, t):
    cap = B[n][4]
    if not cap: return
    toks = cap.split(" "); T0, T1 = 0.08, min(1.1, (BE[n] - BS[n]) * 0.55); k = len(toks)
    shown = [j for j in range(k) if t >= T0 + (T1 - T0) * j / max(1, k)]
    if not shown: return
    hl = set(re.sub(r"[*]", "", x) for x in toks if "*" in x)
    plain_all = cap.replace("*", ""); brk = (k + 1) // 2 if len(plain_all) > 20 else k   # wrap long captions on two lines, break fixed so words do not jump
    parts = [x.replace("*", "") for x in toks[:len(shown)]]
    ln = " ".join(parts[:brk]) + (("\n" + " ".join(parts[brk:])) if len(parts) > brk else "")
    sp = text_sprite(ln, 78, hl=hl)
    if sp.shape[1] > 1000: sp = cv2.resize(sp, (1000, round(sp.shape[0] * 1000 / sp.shape[1])), interpolation=cv2.INTER_AREA)
    last_t = T0 + (T1 - T0) * (len(shown) - 1) / max(1, k); pop = 1.0 + 0.12 * max(0, 1 - (t - last_t) / 0.18)
    paste_rgba(fr, sp, (W - sp.shape[1]) // 2, 1560 - (sp.shape[0] - 120 if "\n" in ln else 0), alpha=1.0, scale=pop)


def callout(fr, n, t):
    call = B[n][6]
    if not call: return
    t0 = 0.9
    if t < t0: return
    s = SPR[call]; w = 860; s = cv2.resize(s, (w, round(s.shape[0] * w / s.shape[1])), interpolation=cv2.INTER_AREA)
    p = ease_back((t - t0) / 0.5); x = int(W + 40 - p * (W - 110)) if (t - t0) < 0.5 else 110
    paste_rgba(fr, s, x, 250, alpha=1.0)


def vignette_grain(fr, t):
    v = VIG; fr = (fr.astype(np.float32) * v[..., None]).astype(np.uint8)
    g = np.random.default_rng(int(t * 30)).normal(0, 3.0, (H // 4, W // 4)).astype(np.float32); g = cv2.resize(g, (W, H), interpolation=cv2.INTER_LINEAR)
    return np.clip(fr.astype(np.float32) + g[..., None], 0, 255).astype(np.uint8)


yy, xx = np.mgrid[0:H, 0:W]; VIG = (1 - 0.22 * (((xx - W / 2) / (W / 2)) ** 2 + ((yy - H / 2) / (H / 2)) ** 2)).astype(np.float32)


def whip(a, b, p, direction):
    """horizontal whip-pan between frames a (out) and b (in) with motion blur."""
    sh = int(W * ease_io(p)); out = np.roll(a, -sh * direction, axis=1); inc = np.roll(b, (W - sh) * direction, axis=1)
    m = np.zeros((H, W), np.float32); m[:, :max(0, W - sh)] = 1 if direction == 1 else 0
    if direction == 1:
        res = np.concatenate([a[:, sh:], b[:, :sh]], axis=1)
    else:
        res = np.concatenate([b[:, W - sh:], a[:, :W - sh]], axis=1)
    k = max(3, int(60 * np.sin(np.pi * min(1, max(0, p)))) | 1)
    return cv2.blur(res, (k, 1)) if k > 3 else res


def render_frame(k):
    t = k / FPS
    n = max(j for j in range(len(B)) if BS[j] <= t + 1e-6); lt = t - BS[n]
    fr = beat_frame(n, lt)
    caption(fr, n, lt); callout(fr, n, lt)
    if n > 0 and lt < TR:
        prev = beat_frame(n - 1, t - BS[n - 1]); caption(prev, n - 1, t - BS[n - 1])
        p = lt / TR; same_scene = B[n][0] == B[n - 1][0]
        if same_scene: fr = whip(prev, fr, p, 1 if n % 2 else -1)
        else:
            f = fr.astype(np.float32); fl = 255 * np.sin(np.pi * p) ** 2
            fr = np.clip((prev.astype(np.float32) * (1 - ease_io(p)) + f * ease_io(p)) + fl * 0.55, 0, 255).astype(np.uint8)
    fr = vignette_grain(fr, t)
    cv2.rectangle(fr, (0, 0), (int(W * t / TOTAL), 10), YEL[::-1][::-1], -1)
    return fr


def sfx_track():
    def dec(p, db):
        raw = subprocess.run(["ffmpeg", "-v", "error", "-i", str(p), "-f", "s16le", "-ac", "1", "-ar", str(SR), "-"], capture_output=True).stdout
        a = np.frombuffer(raw, np.int16).astype(np.float32) / 32768; return a * 10 ** (db / 20)
    wh = dec(ROOT / "shared/sfx/whoosh_803771.mp3", -9); pop = dec(ROOT / "shared/sfx/magic_376747.mp3", -14)
    tr = np.zeros(int(TOTAL * SR) + SR, np.float32)
    def put(a, t0):
        i = int(max(0, t0) * SR); tr[i:i + len(a)] += a[:max(0, len(tr) - i)]
    for n in range(1, len(B)):
        put(wh, BS[n] - 0.10)
    for n, b in enumerate(B):
        if b[6]: put(pop, BS[n] + 0.9)
    out = HERE / "build/sfx.wav"
    with wave.open(str(out), "wb") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR); o.writeframes((np.clip(tr, -1, 1) * 32767).astype(np.int16).tobytes())
    return out


def build_voice():
    voice = HERE / "build/voice.wav"
    with wave.open(str(voice), "wb") as o:
        o.setnchannels(1); o.setsampwidth(2); o.setframerate(SR)
        for w in waves:
            with wave.open(str(w)) as r: o.writeframes(b"\x00\x00" * int(SR * LEAD) + r.readframes(r.getnframes()) + b"\x00\x00" * int(SR * AFTER))
    return voice


def render():
    voice = build_voice(); sfx = sfx_track(); out = HERE / "output/short_edited.mp4"
    cmd = ["ffmpeg", "-y", "-v", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", str(voice), "-i", str(sfx),
           "-ss", "6", "-i", str(ROOT / "shared/music/presentation/Funkorama.mp3"),
           "-filter_complex", "[3:a]volume=-24dB,aformat=sample_rates=24000:channel_layouts=mono[m];[1:a]aformat=sample_rates=24000:channel_layouts=mono[v];[2:a]aformat=sample_rates=24000:channel_layouts=mono[s];[v][m][s]amix=inputs=3:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=7[a]",
           "-map", "0:v", "-map", "[a]", "-c:v", "libx264", "-preset", "medium", "-crf", "18", "-pix_fmt", "yuv420p", "-colorspace", "bt709", "-color_primaries", "bt709", "-color_trc", "bt709",
           "-c:a", "aac", "-b:a", "192k", "-ar", "48000", "-shortest", str(out)]
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE); N = int(TOTAL * FPS)
    for k in range(N):
        p.stdin.write(render_frame(k).tobytes())
        if k % 150 == 0: print(f"  frame {k}/{N}", flush=True)
    p.stdin.close(); p.wait(); print("done")


if __name__ == "__main__":
    print("beats", [round(x, 1) for x in BS], "total", round(TOTAL, 1), flush=True)
    if len(sys.argv) > 1 and sys.argv[1] == "prep": prep()
    elif len(sys.argv) > 1 and sys.argv[1] == "render": render()
