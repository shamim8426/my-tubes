"""Reality Check - Asli: sound design for the Long (own synthesised assets, numpy only, no licence issue).

    python tools/rc_sound.py 001 [--assets-only] [--no-mux] [--tail 20] [--video PATH]

1. Assets  : shared/sfx/rc/*.wav (SFX + ambience) and shared/music/rc/*.wav (5 mood beds) are synthesised once
             (deterministic seeds) and registered in shared/assets_license.csv (licence: own).
2. Cues    : planned from long/shot_specs.json + audio/voiceover_timing.json (else voiceover_draft_timing.json),
             never from fixed seconds -> re-run after a TTS redo and the cues follow the new timing.
3. Stems   : cache/reality-check/<NNN>/sound/music.wav, sfx.wav, mix_nonvoice.wav (+ cues.json); long/sound_cues.md.
4. Mux     : voice + stems -> loudnorm two-pass (-14 LUFS, TP -1.5) -> remux into the existing preview with -c:v copy
             (no video re-render). Called by rc_build_long.py after the concat (it replaces the single mystery_bed).
Levels    : music ~13 LU under the voice (speech sections), SFX peaks 18-26 dB under voice RMS (impacts louder, always in gaps),
            ambience ~30 dB under. Max one SFX per beat (min spacing), none planned inside the first 0.2 s of a spoken number line.
"""
import argparse
import csv
import json
import re
import subprocess
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
SR = 32000
CR = 100  # control rate (Hz) for envelopes
FPS = 30


def find_ff(name="ffmpeg"):
    for c in (ROOT / f"tools/ffmpeg/{name}.exe", Path(f"D:/my-tubes/tools/ffmpeg/{name}.exe")):
        if c.exists():
            return str(c)
    return name


def shared(rel):
    p = ROOT / rel
    return p if p.parent.exists() or True else p


# ---------------------------------------------------------------- synthesis helpers
def rng(seed):
    return np.random.default_rng(seed)


def t_(dur):
    return np.arange(int(dur * SR)) / SR


def fft_filter(x, lo=None, hi=None, order=2):
    """zero-phase brickwall-ish band filter with smooth skirts (FFT)."""
    n = len(x)
    X = np.fft.rfft(x)
    f = np.fft.rfftfreq(n, 1 / SR)
    g = np.ones_like(f)
    if hi:
        g *= 1 / (1 + (f / hi) ** (2 * order))
    if lo:
        g *= 1 / (1 + (lo / np.maximum(f, 1e-3)) ** (2 * order))
    return np.fft.irfft(X * g, n)


def norm(x, peak=0.9):
    m = np.max(np.abs(x)) + 1e-9
    return x / m * peak


def fade(x, a=0.005, b=0.02):
    x = x.copy()
    na, nb = int(a * SR), int(b * SR)
    if na:
        x[:na] *= np.linspace(0, 1, na)
    if nb:
        x[-nb:] *= np.linspace(1, 0, nb)
    return x


def synth_whoosh(dur=0.9, seed=1, lo=300, hi=5000, up=True):
    r = rng(seed)
    n = int(dur * SR)
    nz = r.standard_normal(n)
    out = np.zeros(n)
    centers = np.geomspace(lo, hi, 14)
    if not up:
        centers = centers[::-1]
    tt = np.linspace(0, 1, n)
    for i, c in enumerate(centers):
        pos = (i + 0.5) / len(centers)
        env = np.exp(-((tt - pos * 0.8 - 0.1) ** 2) / (2 * 0.11 ** 2))
        out += fft_filter(nz, c * 0.7, c * 1.4) * env
    out *= np.sin(np.pi * np.clip(tt, 0, 1)) ** 1.2
    return fade(norm(out, 0.85), 0.01, 0.05)


def synth_blip(f=1500, dur=0.07, soft=True):
    t = t_(dur)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 55) + 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 90)
    return fade(norm(x, 0.8), 0.002, 0.01)


def synth_subhit(dur=1.0, f0=62, f1=34):
    t = t_(dur)
    ph = 2 * np.pi * np.cumsum(f1 + (f0 - f1) * np.exp(-t * 7)) / SR
    x = np.sin(ph) * np.exp(-t * 3.6)
    return fade(norm(x, 0.9), 0.004, 0.05)


def synth_impact(dur=3.6, seed=3):
    r = rng(seed)
    t = t_(dur)
    sub = np.sin(2 * np.pi * np.cumsum(28 + 40 * np.exp(-t * 6)) / SR) * np.exp(-t * 1.5)
    n1 = fft_filter(r.standard_normal(len(t)), None, 700) * np.exp(-t * 14)  # short noise burst (crack)
    n2 = fft_filter(r.standard_normal(len(t)), 25, 150) * np.exp(-t * 1.1) * (0.6 + 0.4 * np.sin(2 * np.pi * 5 * t))  # rumble tail
    x = 1.0 * sub + 0.7 * norm(n1, 1) * 0.8 + 0.8 * norm(n2, 1) * np.minimum(t / 0.05, 1)
    return fade(norm(x, 0.95), 0.002, 0.3)


def synth_riser(dur=3.2, seed=4):
    r = rng(seed)
    n = int(dur * SR)
    tt = np.linspace(0, 1, n)
    nz = r.standard_normal(n)
    out = np.zeros(n)
    for i, c in enumerate(np.geomspace(250, 4200, 16)):
        pos = (i + 0.5) / 16
        env = np.exp(-((tt - pos) ** 2) / (2 * 0.16 ** 2))
        out += fft_filter(nz, c * 0.75, c * 1.3) * env
    t = tt * dur
    tone = np.sin(2 * np.pi * np.cumsum(110 * 2 ** (tt * 2.2)) / SR) * 0.35
    x = (norm(out, 1) * 0.8 + tone) * (tt ** 2.2)
    return fade(norm(x, 0.85), 0.01, 0.12)


def synth_chime(f=1568, dur=1.4):
    t = t_(dur)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 4.0) + 0.35 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 7) + 0.2 * np.sin(2 * np.pi * f * 0.5 * t) * np.exp(-t * 3)
    return fade(norm(x, 0.8), 0.003, 0.2)


def synth_ping(f=740, dur=1.6):
    """'anjaan' tag: slightly detuned two-note ping with a reversed-noise breath in front (the hush)."""
    t = t_(dur)
    x = np.sin(2 * np.pi * f * t) * np.exp(-t * 3.2) + 0.5 * np.sin(2 * np.pi * f * 1.5 * t) * np.exp(-t * 4.5) + 0.25 * np.sin(2 * np.pi * f * 2.01 * t) * np.exp(-t * 6)
    return fade(norm(x, 0.8), 0.003, 0.25)


def synth_radar(dur=2.4):
    t = t_(dur)
    x = np.zeros_like(t)
    for k, g in enumerate((1.0, 0.45, 0.2)):
        tt = np.clip(t - k * 0.55, 0, None)
        x += g * np.sin(2 * np.pi * 1180 * tt) * np.exp(-tt * 9) * (t >= k * 0.55) * np.minimum(tt / 0.004, 1)
        x += g * 0.3 * np.sin(2 * np.pi * 590 * tt) * np.exp(-tt * 6) * (t >= k * 0.55)
    return fade(norm(x, 0.8), 0.002, 0.2)


def synth_whirr(dur=1.1, seed=5):
    t = t_(dur)
    f = 260 + 340 * (t / dur) ** 1.5
    saw = 2 * ((np.cumsum(f) / SR) % 1) - 1
    am = 0.6 + 0.4 * np.sin(2 * np.pi * (14 + 10 * t / dur) * t)
    x = fft_filter(saw, 150, 2200) * am * np.sin(np.pi * t / dur) ** 0.8
    beep = np.zeros_like(t)
    for st in (dur - 0.32, dur - 0.14):
        m = (t >= st) & (t < st + 0.07)
        beep[m] = np.sin(2 * np.pi * 1900 * t[m]) * np.hanning(m.sum())
    return fade(norm(x, 0.7) + 0.3 * beep, 0.01, 0.05)


def synth_ticks(n=4, gap=1.0, seed=6):
    r = rng(seed)
    dur = gap * (n - 1) + 0.2
    x = np.zeros(int(dur * SR))
    for k in range(n):
        i = int(k * gap * SR)
        tt = t_(0.06)
        c = fft_filter(r.standard_normal(len(tt)), 1500, 5000) * np.exp(-tt * 140) + 0.5 * np.sin(2 * np.pi * 880 * tt) * np.exp(-tt * 120)
        x[i:i + len(tt)] += c * (1.0 if k < n - 1 else 1.3)
    return norm(x, 0.7)


def synth_flip(seed=7):
    r = rng(seed)
    out = np.zeros(int(0.22 * SR))
    for off, g in ((0.0, 1.0), (0.075, 0.55)):
        tt = t_(0.07)
        c = fft_filter(r.standard_normal(len(tt)), 1800, 7000) * np.exp(-tt * 60) * np.minimum(tt / 0.003, 1)
        i = int(off * SR)
        out[i:i + len(tt)] += c * g
    return norm(out, 0.75)


def synth_thud(dur=0.7, seed=8):
    r = rng(seed)
    t = t_(dur)
    x = np.sin(2 * np.pi * np.cumsum(46 + 50 * np.exp(-t * 25)) / SR) * np.exp(-t * 6.5)
    x += 0.5 * fft_filter(r.standard_normal(len(t)), 60, 600) * np.exp(-t * 30)
    return fade(norm(x, 0.9), 0.002, 0.05)


def synth_debris(dur=1.6, seed=9):
    r = rng(seed)
    n = int(dur * SR)
    x = np.zeros(n)
    for _ in range(40):
        i = int(r.uniform(0, 0.8) ** 1.6 * n * 0.95)
        tt = t_(0.03)
        x[i:i + len(tt)] += fft_filter(r.standard_normal(len(tt)), 300, 3500) * np.exp(-tt * 140) * r.uniform(0.2, 1)
    x += 0.4 * fft_filter(r.standard_normal(n), 40, 180) * np.exp(-t_(dur) * 2)
    return fade(norm(x, 0.8), 0.003, 0.2)


def synth_resolve(dur=11.0):
    """warm major pad swell for the ending (C - G - D - E), no melody."""
    return pad([130.8, 196.0, 293.7, 329.6, 523.3], dur, seed=21, lp=2600, swell=True, vol=1.0)


def pad(freqs, dur, seed, lp=1800, swell=False, pulse=0.0, shimmer=0.0, vol=1.0, dark=1.0):
    """additive pad: each note = few harmonics, slow random detune + slow amplitude LFOs, stereo; own, no melody."""
    r = rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    L = np.zeros(n)
    R = np.zeros(n)
    for f in freqs:
        for ch, arr in ((0, L), (1, R)):
            for v in range(3):
                det = 1 + r.uniform(-0.0035, 0.0035)
                drift = np.cumsum(r.standard_normal(n // 400 + 2))
                drift = np.interp(np.arange(n) / 400, np.arange(len(drift)), drift)
                drift = drift / (np.abs(drift).max() + 1e-9) * 0.0025
                ph = 2 * np.pi * np.cumsum(f * det * (1 + drift)) / SR
                lfo = 0.65 + 0.35 * np.sin(2 * np.pi * r.uniform(0.04, 0.12) * t + r.uniform(0, 6.28))
                for h, a in ((1, 1.0), (2, 0.35 * dark), (3, 0.15 * dark), (4, 0.06 * dark)):
                    arr += a * np.sin(h * ph + r.uniform(0, 6.28)) * lfo / 3
    if shimmer:
        for k in range(4):
            f = freqs[-1] * 2 ** (1 + k * 0.5)
            m = 0.5 + 0.5 * np.sin(2 * np.pi * r.uniform(0.03, 0.07) * t + r.uniform(0, 6))
            L += shimmer * np.sin(2 * np.pi * f * t + r.uniform(0, 6)) * m ** 3 * 0.1
            R += shimmer * np.sin(2 * np.pi * f * 1.002 * t + r.uniform(0, 6)) * m ** 3 * 0.1
    if pulse:
        # very soft heartbeat-ish sub pulse (60 bpm), low and unobtrusive
        ph = (t % 1.0)
        env = np.exp(-ph * 9) + 0.6 * np.exp(-np.clip(ph - 0.28, 0, None) * 11) * (ph > 0.28)
        sub = np.sin(2 * np.pi * 42 * t) * env * pulse
        L += sub
        R += sub
    out = np.stack([fft_filter(L, 25, lp), fft_filter(R, 25, lp)], 1)
    if swell:
        out *= (np.sin(np.pi * np.clip(t / dur, 0, 1)) ** 0.7)[:, None]
    return out * vol / (np.sqrt((out ** 2).mean()) + 1e-9) * 0.1


def synth_drone(dur=40.0, seed=31):
    """space drone ambience: brown noise < 120 Hz + 2 slow beating sub tones; loops (made periodic by cross-fade)."""
    r = rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    b = fft_filter(r.standard_normal(n), 20, 140)
    s = np.sin(2 * np.pi * 55 * t) * 0.5 + np.sin(2 * np.pi * 55.35 * t) * 0.5 + 0.2 * np.sin(2 * np.pi * 82.4 * t)
    x = b / b.std() * 0.5 + s * 0.5 * (0.7 + 0.3 * np.sin(2 * np.pi * t / 13))
    h = fft_filter(r.standard_normal(n), 2500, 6000) * 0.03 / (b.std() + 1e-9) * (0.5 + 0.5 * np.sin(2 * np.pi * t / 9)) ** 2  # faint air
    x = x + h
    return np.stack([x, np.roll(x, 900)], 1)


def synth_room(dur=40.0, seed=32):
    """earth / city room tone: pink-ish noise < 700 Hz, slow swell, no wind gusts, no crowd."""
    r = rng(seed)
    n = int(dur * SR)
    t = np.arange(n) / SR
    x = fft_filter(r.standard_normal(n), 60, 700) + 0.4 * fft_filter(r.standard_normal(n), 150, 1800)
    x *= 0.75 + 0.25 * np.sin(2 * np.pi * t / 17)
    return np.stack([x, np.roll(x, 500)], 1)


BEDS = {  # name: (freqs, kwargs)  -> quiet ambient pads that differ by mood
    "curious": ([73.4, 110.0, 164.8, 220.0, 329.6], dict(lp=2200, shimmer=1.0, dark=0.9)),         # D sus2 / open fifths, airy
    "tense": ([65.4, 69.3, 98.0, 138.6, 196.0], dict(lp=1000, pulse=0.9, dark=0.7)),              # C + Db + Gb: dissonant low drone, soft pulse
    "calm": ([87.3, 130.8, 220.0, 329.6], dict(lp=2400, shimmer=0.5)),                            # F maj7, slow
    "mystery": ([55.0, 82.4, 98.0, 123.5, 185.0], dict(lp=1500, shimmer=1.4, dark=0.8)),           # A m(sus)/b2 colour, glassy top
    "hopeful": ([130.8, 196.0, 261.6, 329.6, 392.0, 587.3], dict(lp=3200, shimmer=0.6, dark=1.2)), # C add9, warmer + brighter
}
SFX_FILES = {
    "whoosh": lambda: synth_whoosh(0.95, 1),
    "whoosh_soft": lambda: synth_whoosh(0.6, 2, 500, 3500),
    "blip": lambda: synth_blip(1500, 0.07),
    "subhit": lambda: synth_subhit(),
    "impact": lambda: synth_impact(),
    "riser": lambda: synth_riser(),
    "chime": lambda: synth_chime(),
    "ping": lambda: synth_ping(),
    "radar": lambda: synth_radar(),
    "whirr": lambda: synth_whirr(),
    "ticks": lambda: synth_ticks(4, 1.0),
    "flip": lambda: synth_flip(),
    "thud": lambda: synth_thud(),
    "debris": lambda: synth_debris(),
    "resolve": lambda: synth_resolve(),
}
AMB_FILES = {"space_drone": synth_drone, "room_tone": synth_room}


def write_wav(path, x, sr=SR):
    x = np.asarray(x)
    if x.ndim == 1:
        x = x[:, None]
    pcm = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(x.shape[1])
        w.setsampwidth(2)
        w.setframerate(sr)
        w.writeframes(pcm.tobytes())


def read_wav(path):
    with wave.open(str(path), "rb") as w:
        n, ch = w.getnframes(), w.getnchannels()
        d = np.frombuffer(w.readframes(n), "<i2").astype(np.float32) / 32767
    return d.reshape(-1, ch)


def make_assets(force=False):
    sd = ROOT / "shared/sfx/rc"
    md = ROOT / "shared/music/rc"
    sd.mkdir(parents=True, exist_ok=True)
    md.mkdir(parents=True, exist_ok=True)
    rows = []
    for name, fn in SFX_FILES.items():
        p = sd / f"rc_{name}.wav"
        if force or not p.exists():
            write_wav(p, fn())
        rows.append((p, f"own: synthesised by tools/rc_sound.py (numpy) - {name}"))
    for name, fn in AMB_FILES.items():
        p = sd / f"rc_{name}.wav"
        if force or not p.exists():
            write_wav(p, fn())
        rows.append((p, f"own: synthesised by tools/rc_sound.py (numpy) - ambience {name}"))
    for i, (name, (freqs, kw)) in enumerate(BEDS.items()):
        p = md / f"rc_bed_{name}.wav"
        if force or not p.exists():
            write_wav(p, pad(freqs, 96.0, seed=100 + i, **kw))
        rows.append((p, f"own: synthesised by tools/rc_sound.py (numpy) - ambient pad bed '{name}', no melody"))
    lic = ROOT / "shared/assets_license.csv"
    have = set()
    with open(lic, encoding="utf-8", newline="") as f:
        for r in csv.reader(f):
            if r:
                have.add(r[0])
    with open(lic, "a", encoding="utf-8", newline="") as f:
        w = csv.writer(f, lineterminator="\n")
        for p, src in rows:
            rel = p.relative_to(ROOT).as_posix()
            if rel not in have:
                w.writerow([rel, src, "Reality Check - Asli", "own", "", "2026-11-08"])
    return rows


def load_sfx(name):
    p = ROOT / "shared/sfx/rc" / f"rc_{name}.wav"
    return read_wav(p)[:, 0]


# ---------------------------------------------------------------- audio utils (ffmpeg)
def load_audio(path, ch=1, sr=SR):
    p = subprocess.run([find_ff(), "-v", "error", "-i", str(path), "-f", "f32le", "-ar", str(sr), "-ac", str(ch), "-"], capture_output=True, check=True)
    return np.frombuffer(p.stdout, "<f4").reshape(-1, ch)


def lufs(x, sr=SR):
    x = np.asarray(x, "<f4")
    if x.ndim == 1:
        x = x[:, None]
    p = subprocess.run([find_ff(), "-v", "info", "-f", "f32le", "-ar", str(sr), "-ac", str(x.shape[1]), "-i", "-", "-af", "ebur128=peak=true", "-f", "null", "-"],
                       input=x.tobytes(), capture_output=True, text=False)
    s = p.stderr.decode("utf-8", "ignore")
    m = re.findall(r"I:\s+(-?[\d.]+) LUFS", s)
    return float(m[-1]) if m else -70.0


def env_interp(env, n):
    return np.interp(np.arange(n) / SR, np.arange(len(env)) / CR, env)


def smooth_env(x, att, rel):
    """one-pole follower on a control-rate array: fast down-going toward larger values handled by caller; here
    value rises with time-constant att and falls with rel."""
    y = np.zeros_like(x)
    a_a, a_r = np.exp(-1 / (att * CR)), np.exp(-1 / (rel * CR))
    c = 0.0
    for i, v in enumerate(x):
        c = a_a * c + (1 - a_a) * v if v > c else a_r * c + (1 - a_r) * v
        y[i] = c
    return y


def lowpass_stereo(x, hi):
    return np.stack([fft_filter(x[:, 0], None, hi), fft_filter(x[:, 1], None, hi)], 1)


# ---------------------------------------------------------------- cue planning
BIG_NUM = ["33 MIN", "~500 kt", "~80 million", ">1,000 t", "-33 min", "99.9%"]
MOOD_BY_HEAD = {"KHATRA": "tense", "DART": "calm", "DHUNDHNA": "curious", "RAAZ": "mystery", "TAREEKE": "calm", "HERA": "curious",
                "FAISLA": "mystery", "RECAP": None}
EARTH_G = {"earth", "city", "trees", "field", "dome"}
ANJ = re.compile(r"ANJAAN|ANDEKHA", re.I)
REVEAL_SILENCE = ["33 MIN", "7 / 33", "SACH|green"]  # music drops out just before these lines


def tparts(sp):
    out = []
    for s in sp.get("T", []):
        k, rest = s[0], s[2:]
        out.append((k, rest.split("|")[0], rest))
    return out


def attr(rest, key, default=None):
    m = re.search(r"\b" + key + r"=([\d.\-]+)", rest)
    return float(m.group(1)) if m else default


def plan(specs, lines, ends_voice, tail):
    """returns shots, cues(list), chapters, reveal windows, hush windows, dip windows (all times in seconds)."""
    starts = [0.0] + [l["start"] for l in lines[1:]]
    ends = starts[1:] + [ends_voice]
    shots = []
    for i, l in enumerate(lines):
        sp = specs.get(l["line"], {})
        shots.append(dict(n=l["line"], t0=starts[i], t1=ends[i], v0=l["start"], v1=l["end"], sp=sp, sec=l.get("section_start", False)))
    total = ends_voice + tail
    cand = []  # (prio, t, kind, rel_db, why, shot)

    def add(prio, t, kind, rel, why, n):
        cand.append(dict(prio=prio, t=max(0.0, t), kind=kind, rel=rel, why=why, n=n))

    ch_names = []
    for s in shots:
        sp, n = s["sp"], s["n"]
        tp = tparts(sp)
        gtypes = [g[0] for g in sp.get("g", [])]
        media = sp.get("media") or {}
        texts = " ".join(r for _, _, r in tp)
        head = next((b for k, b, r in tp if k == "H"), "")
        if s["sec"] and head:
            add(1, s["t0"] - 0.35, "whoosh", -20, f"chapter change: {head.strip()}", n)
        # impacts (exempt from spacing)
        if "DART impact" in (media.get("cue") or "") and "mp4" in (media.get("file") or ""):
            add(0, s["v1"] + 0.05, "impact", -9, "DART hits Dimorphos (impact boom + rumble tail, music low-pass dip)", n)
        for g in sp.get("g", []):
            if g[0] == "collide":
                hit = g[4].get("hit", 0.4) * min(s["t1"] - s["t0"], 8)
                add(0, s["t0"] + hit, "impact", -13, "collision graphic contact (smaller hit)", n)
        # reveal: riser + sub hit
        for pat in BIG_NUM:
            if any(b.startswith(pat) or pat in b for k, b, r in tp if k == "B"):
                add(1, s["t0"] - 0.22, "subhit", -14, f"big number card '{pat}' (sub-hit in the gap before the voice)", n)
                if pat in ("33 MIN", "~500 kt", "~80 million", ">1,000 t"):
                    add(2, s["t0"] - 3.2, "riser", -25, f"rising tension into '{pat}'", n)
                break
        # anjaan tag
        for k, b, r in tp:
            if k == "R" and ANJ.search(b):
                at = attr(r, "at", 0.6)
                add(2, s["t0"] + at, "ping", -21, "ANJAAN (unknown) tag: ping + short hush", n)
                break
        # verdict cards
        if any(k == "K" and re.match(r"(SACH|ABHI|NAHI|AADHA)", b) for k, b, r in tp):
            add(2, s["t0"] + 0.1, "flip", -20, "verdict card flips in", n)
        if any(k == "K" and re.match(r"(SACH)", b) and "green" in b for k, b, r in tp) and s["sp"].get("n") == s["n"]:
            pass
        for g in gtypes:
            if g == "scope":
                add(3, s["t0"] + 0.5, "radar", -23, "telescope graphic: radar ping", n)
            elif g == "dots":
                add(4, s["t0"] + 0.5, "radar", -26, "search field of dots: sonar pulse", n)
            elif g == "laser":
                add(3, s["t0"] + 0.3, "whirr", -23, "craft laser: whirr + beep", n)
            elif g == "clock":
                add(3, s["t0"] + 0.3, "ticks", -26, "clock graphic: countdown ticks", n)
            elif g in ("fire", "flash") and not any(c["n"] == n and c["kind"] == "impact" for c in cand):
                add(3, s["t0"] + 0.25, "thud", -20, "flash/fire graphic: low thud", n)
            elif g in ("fountain", "rubble"):
                add(3, s["t0"] + 0.4, "debris", -24, "debris graphic: rock-bits patter", n)
            elif g == "streaks":
                add(4, s["t0"] + 0.1, "whoosh_soft", -25, "speed streaks: soft whoosh", n)
        if any(k == "S" for k, b, r in tp):
            add(4, s["t0"] + 0.45, "chime", -26, "source label: tiny chime", n)
        nb = [b for k, b, r in tp if k == "B"]
        if nb:
            at = next((attr(r, "at") for k, b, r in tp if k == "B" and attr(r, "at") is not None), 0.12)
            add(5, s["t0"] + max(at, 0.12) + 0.05, "blip", -26, "number card appears: soft blip", n)
    # final resolve
    last = shots[-1]
    rec = [s for s in shots if any(k == "H" and "RECAP" in b for k, b, r in tparts(s["sp"]))]
    t_res = (rec[-1]["t0"] if rec else last["t0"]) + 0.2
    # greedy thinning: keep impacts, then priority order with min spacing
    cand.sort(key=lambda c: (c["prio"], c["t"]))
    kept = []
    for c in cand:
        if c["kind"] == "impact" or c["prio"] == 0:
            kept.append(c)
            continue
        gap = 2.4 if c["prio"] <= 2 else 3.6
        if all(abs(c["t"] - k["t"]) >= (gap if k["kind"] != "impact" else 2.0) for k in kept):
            kept.append(c)
    kept.sort(key=lambda c: c["t"])
    kept.append(dict(prio=0, t=t_res, kind="resolve", rel=-24, why="ending: warm resolve pad", n=rec[-1]["n"] if rec else last["n"]))
    # chapters -> moods
    chap = []
    cur = dict(t0=0.0, mood="curious", name="intro")
    for s in shots:
        tp = tparts(s["sp"])
        head = next((b for k, b, r in tp if k == "H"), "")
        if s["sec"] and head:
            key = next((k for k in MOOD_BY_HEAD if k in head.upper()), None)
            if key == "RECAP" or key is None:
                continue
            chap.append(cur)
            cur = dict(t0=s["t0"], mood=MOOD_BY_HEAD[key], name=head.strip())
        elif head and "RECAP" in head.upper():
            pass
    chap.append(cur)
    # verdict (FAISLA) already mystery; last recap -> hopeful
    chap.append(dict(t0=t_res - 1.0, mood="hopeful", name="ending"))
    for i, c in enumerate(chap):
        c["t1"] = chap[i + 1]["t0"] if i + 1 < len(chap) else total
    # reveal-silence windows (music + ambience dropped just before these lines)
    quiet = []
    for s in shots:
        tp = tparts(s["sp"])
        txt = " ".join(r for _, _, r in tp)
        if any(k == "B" and b.startswith("33 MIN") for k, b, r in tp) or any(k == "H" and "RAAZ" in b.upper() for k, b, r in tp) or (
                any(k == "K" and b.startswith("SACH") and "green" in r for k, b, r in tp) and not any(k == "K" and b.startswith("ABHI") for k, b, r in tp)):
            quiet.append(dict(t=s["t0"], n=s["n"]))
    return shots, kept, chap, quiet, total


# ---------------------------------------------------------------- mixing
def place(buf, snd, t, gain):
    i = int(t * SR)
    if i >= len(buf):
        return
    j = min(len(buf), i + len(snd))
    if snd.ndim == 1 and buf.ndim == 2:
        buf[i:j, 0] += snd[: j - i] * gain
        buf[i:j, 1] += snd[: j - i] * gain
    elif snd.ndim == 2 and buf.ndim == 2:
        buf[i:j] += snd[: j - i] * gain
    else:
        buf[i:j] += snd[: j - i] * gain


def loop_to(x, n, xf=int(3 * SR)):
    """loop a stereo array to length n with equal-power crossfade at the joins."""
    if n <= len(x):
        return x[:n].copy()
    out = np.zeros((n, x.shape[1]), np.float32)
    pos = 0
    first = True
    w = np.linspace(0, np.pi / 2, xf)
    fi, fo = np.sin(w)[:, None], np.cos(w)[:, None]
    while pos < n:
        seg = x.copy()
        if not first:
            seg[:xf] *= fi
        seg[-xf:] *= fo
        e = min(n, pos + len(seg))
        out[pos:e] += seg[: e - pos]
        pos += len(seg) - xf
        first = False
    return out


def build(story, tail=20.0, video=None, mux=True, timing=None, voice=None, cname="sound"):
    sd = next((ROOT / "channels/reality-check/stories").glob(story + "_*"))
    ld = sd / "long"
    specs = {s["n"]: s for s in json.loads((ld / "shot_specs.json").read_text(encoding="utf-8"))}
    tfile = Path(timing) if timing else sd / "audio/voiceover_timing.json"
    if not tfile.exists():
        tfile = sd / "audio/voiceover_draft_timing.json"
    lines = json.loads(tfile.read_text(encoding="utf-8"))
    vfile = Path(voice) if voice else sd / "audio/voiceover_full.wav"
    if not vfile.exists():
        vfile = sd / "audio/voiceover_draft_mixed.wav"
    voice = load_audio(vfile, 1)[:, 0]
    ends_voice = max(len(voice) / SR, lines[-1]["end"])
    make_assets()
    shots, cues, chap, quiet, total = plan(specs, lines, ends_voice, tail)
    N = int(total * SR)
    nc = int(total * CR) + 2
    voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
    # speech mask at control rate
    sp = np.zeros(nc)
    for l in lines:
        sp[int(l["start"] * CR): int(l["end"] * CR) + 1] = 1.0
    spm = env_interp(sp, N)
    vl = lufs(voice[spm > 0.5])
    vrms = 20 * np.log10(np.sqrt((voice[spm > 0.5] ** 2).mean()) + 1e-9)
    print(f"voice: {vl:.1f} LUFS (speech), rms {vrms:.1f} dBFS, {len(lines)} lines, total {total:.1f}s")
    # ---- music
    music = np.zeros((N, 2), np.float32)
    beds = {}
    for k in BEDS:
        b = read_wav(ROOT / f"shared/music/rc/rc_bed_{k}.wav")
        beds[k] = (b, lowpass_stereo(b, 380))
    # low-pass dip windows around impacts (control rate weight 0..1)
    lpw = np.zeros(nc)
    hush = np.zeros(nc)
    for c in cues:
        if c["kind"] == "impact":
            i0, i1 = int(c["t"] * CR), int((c["t"] + 2.6) * CR)
            lpw[i0:i1] = np.maximum(lpw[i0:i1], 1.0)
        if c["kind"] == "ping":
            i0, i1 = int(c["t"] * CR), int((c["t"] + 1.8) * CR)
            hush[i0:i1] = 1.0
    lpw = smooth_env(lpw, 0.08, 0.9)
    hush = smooth_env(hush, 0.2, 0.7)
    for i, ch in enumerate(chap):
        a, b = max(0.0, ch["t0"] - 1.0), min(total, ch["t1"] + 1.0)  # 2 s overlap = 1-2 s crossfade
        n = int((b - a) * SR)
        full, lp = beds[ch["mood"]]
        seg = loop_to(full, n)
        segl = loop_to(lp, n)
        i0 = int(a * SR)
        w = env_interp(lpw, N)[i0:i0 + n, None]
        seg = seg * (1 - w) + segl * w * 1.4
        win = np.ones(n)
        xf = int(2.0 * SR)
        ramp = np.sin(np.linspace(0, np.pi / 2, min(xf, n)))
        if i > 0:
            win[:len(ramp)] = ramp
        else:
            win[:int(2.5 * SR)] = np.sin(np.linspace(0, np.pi / 2, int(2.5 * SR)))
        if i + 1 < len(chap):
            win[-len(ramp):] = np.cos(np.linspace(0, np.pi / 2, len(ramp)))
        music[i0:i0 + n] += seg * win[:, None]
    # envelope: duck under speech (gaps come up ~5 dB), pre-reveal dropouts, hush after ANJAAN, end fade
    duck_db = -5.0 * smooth_env(sp, 0.12, 0.7)
    env_db = duck_db.copy()
    env_db += -3.0 * hush
    for q in quiet:
        i0, i1, i2 = int((q["t"] - 1.1) * CR), int((q["t"] + 0.7) * CR), int((q["t"] + 2.6) * CR)
        dip = np.zeros(nc)
        dip[i0:i1] = -40
        dip[i1:i2] = np.linspace(-40, 0, max(i2 - i1, 1))[: len(dip[i1:i2])]
        dip = -smooth_env(-dip, 0.25, 0.25)
        env_db += dip
    tail_i = int((total - 8.0) * CR)
    env_db[tail_i:] += -np.linspace(0, 40, nc - tail_i)
    music *= env_interp(10 ** (env_db / 20), N)[:, None]
    # calibrate: music over speech sections = voice LUFS - 13
    mm = music * (spm > 0.5)[:, None]
    ml = lufs(mm)
    g_music = 10 ** ((vl - 13.0 - ml) / 20)
    music *= g_music
    print(f"music: speech-section {ml:.1f} -> {ml + 20 * np.log10(g_music):.1f} LUFS (voice {vl:.1f}, target -13 LU)")
    # ---- sfx + ambience
    sfx = np.zeros((N, 2), np.float32)
    amb_db = np.zeros(nc) - 31.0
    drone = loop_to(read_wav(ROOT / "shared/sfx/rc/rc_space_drone.wav"), N)
    room = loop_to(read_wav(ROOT / "shared/sfx/rc/rc_room_tone.wav"), N)
    earth = np.zeros(nc)
    for s in shots:
        if any(g[0] in EARTH_G for g in s["sp"].get("g", [])):
            earth[int(s["t0"] * CR): int(s["t1"] * CR)] = 1.0
    earth = smooth_env(earth, 0.8, 1.0)
    amb_env = np.ones(nc)
    for q in quiet:
        i0, i1, i2 = int((q["t"] - 1.1) * CR), int((q["t"] + 0.7) * CR), int((q["t"] + 2.6) * CR)
        amb_env[i0:i1] = 0.0
        amb_env[i1:i2] = np.linspace(0, 1, max(i2 - i1, 1))[: len(amb_env[i1:i2])]
    amb_env = smooth_env(amb_env, 1.0, 0.2)
    fin = np.ones(nc)
    fin[tail_i:] = np.linspace(1, 0, nc - tail_i)
    ae = env_interp(amb_env * fin, N)[:, None]
    ev = env_interp(earth, N)[:, None]
    # ambience level: stem RMS ~ voice RMS - 31 dB (space) ; room tone -29
    def rms(x):
        return float(np.sqrt((x ** 2).mean()) + 1e-9)
    sfx += drone * (10 ** ((vrms - 31) / 20) / rms(drone)) * ae * (1 - 0.5 * ev)
    sfx += room * (10 ** ((vrms - 30) / 20) / rms(room)) * ae * ev
    for c in cues:
        snd = load_sfx(c["kind"]) if c["kind"] != "resolve" else read_wav(ROOT / "shared/sfx/rc/rc_resolve.wav")
        pk = np.abs(snd).max() + 1e-9
        # peak of the sfx = voice rms + rel dB  (rel is negative = below the voice)
        gain = 10 ** ((vrms + (c["rel"] if c["kind"] != "resolve" else -17)) / 20) / pk
        if c["kind"] == "resolve":
            place(sfx, snd.astype(np.float32), c["t"], gain)
        else:
            place(sfx, snd, c["t"], gain)
    nonvoice = music + sfx
    cdir = ROOT / "cache/reality-check" / story / cname
    cdir.mkdir(parents=True, exist_ok=True)
    write_wav(cdir / "music.wav", music)
    write_wav(cdir / "sfx.wav", sfx)
    write_wav(cdir / "mix_nonvoice.wav", nonvoice)
    (cdir / "cues.json").write_text(json.dumps(dict(cues=cues, chapters=chap, quiet=quiet, voice_lufs=vl, timing=tfile.name), indent=1), encoding="utf-8")
    if cname == "sound":
        write_cue_md(ld / "sound_cues.md", cues, chap, quiet, shots, tfile.name)
    mix = np.stack([voice, voice], 1) + nonvoice
    raw = cdir / "mix_raw.f32"
    raw.write_bytes(mix.astype("<f4").tobytes())
    print(f"cues: {len(cues)}; stems in {cdir}")
    if mux:
        mux_final(story, ld, raw, total, video)


def write_cue_md(path, cues, chap, quiet, shots, tname):
    by = {s["n"]: s for s in shots}
    L = ["# Sound cues (auto, tools/rc_sound.py)", "", f"Timing source: {tname}. Cues follow shot specs + timing, re-run after TTS redo.", "",
         "Music beds (1-2 s crossfades): " + "; ".join(f"{c['t0']:.0f}s {c['mood']} ({c['name']})" for c in chap), "",
         "Pre-reveal music/ambience dropouts (voice-only moment): " + ", ".join(f"shot {q['n']} @ {q['t']:.1f}s" for q in quiet), "",
         "Always on: space drone (-31 dB under voice RMS), earth room tone on earth/city shots, music ~13 LU under voice (+5 dB in gaps).", "",
         "| time | shot | sound | level (peak vs voice RMS) | why |", "|---|---|---|---|---|"]
    for c in cues:
        m, s = divmod(c["t"], 60)
        L.append(f"| {int(m)}:{s:05.2f} | {c['n']} | {c['kind']} | {c['rel']} dB | {c['why']} |")
    L += ["", f"Total cues: {len(cues)}"]
    path.write_text("\n".join(L), encoding="utf-8")


def mux_final(story, ld, raw, total, video):
    ff = find_ff()
    out_dir = ld / "output"
    prev = Path(video) if video else out_dir / f"{story}_long_preview.mp4"
    old = out_dir / f"{story}_long_preview_oldsound.mp4"
    if prev.exists() and not old.exists():
        old.write_bytes(prev.read_bytes())
    src = old if old.exists() else prev
    base = ["-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw)]
    p = subprocess.run([ff, "-hide_banner", *base, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S)[-1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}"
          f":measured_thresh={js['input_thresh']}:offset={js['target_offset']}:linear=true,alimiter=limit=0.82:level=disabled,aresample=48000")
    tmp = out_dir / f"{story}_long_preview_newsound.tmp.mp4"
    subprocess.run([ff, "-y", "-loglevel", "error", "-i", str(src), *base, "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-af", ln, "-c:a", "aac", "-b:a", "192k",
                    "-t", f"{total:.3f}", "-movflags", "+faststart", str(tmp)], check=True)
    tmp.replace(out_dir / f"{story}_long_preview.mp4")
    print("REMUX", out_dir / f"{story}_long_preview.mp4", "(video stream copied)")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--assets-only", action="store_true")
    ap.add_argument("--force-assets", action="store_true")
    ap.add_argument("--no-mux", action="store_true")
    ap.add_argument("--tail", type=float, default=20.0)
    ap.add_argument("--video", default="")
    a = ap.parse_args()
    if a.force_assets or a.assets_only:
        make_assets(force=a.force_assets)
        print("assets ready")
        if a.assets_only:
            return
    build(a.story, a.tail, a.video or None, not a.no_mux)


if __name__ == "__main__":
    main()
