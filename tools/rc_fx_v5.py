"""Sound events v5 for Reality Check Long (own synthesis; recipes from study_ref_QsHQxRlBy6Y_sound.md section 3.3; technique only).
BOOM/BOOM-soft/THUD (sub sines), RISE (sub-only, <350 Hz), AIR (fixed band noise burst, no sweep), TICK, CLOCK, AMB (scene ambience, fixed filters).
parse_plan(path) -> (events [{t,type,rel,text,line}], off windows).  render(ev, end) -> mono float array peak-normalised to 1.0."""
import re
import zlib

import numpy as np

import rc_sound as RS

SR = RS.SR
EV = re.compile(r"(\d+):(\d\d\.\d)\s+\*\*(BOOM-soft|BOOM|THUD|RISE|AIR|TICK|CLOCK|AMB)\*\*\s+(-?\d+)\s*dB:?\s*(.*)")


def parse_plan(path):
    txt = open(path, encoding="utf-8").read()
    events, offs = [], []
    sec2 = txt.split("## 2.")[1].split("## 3.")[0]
    for m in re.finditer(r"(\d+):(\d\d\.\d)-(\d+):(\d\d\.\d)", sec2.split("Total OFF")[0]):
        offs.append([int(m[1]) * 60 + float(m[2]), int(m[3]) * 60 + float(m[4])])
    for row in txt.split("## 5.")[1].splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*[\d:.]+\s*\|", row)
        if not m:
            continue
        line = int(m[1])
        for piece in row.split("<br>"):
            e = EV.search(piece)
            if e:
                events.append(dict(t=int(e[1]) * 60 + float(e[2]), type=e[3], rel=float(e[4]), text=e[5], line=line))
    events.sort(key=lambda x: x["t"])
    return events, offs


def _lp(x, hi):
    return RS.fft_filter(x, hi=hi, order=4)


def _norm(x):
    return (x / (np.abs(x).max() + 1e-9)).astype(np.float32)


def boom(f_end=38, f_start=62, tau=0.45, dur=2.2):
    n = int(dur * SR)
    t = np.arange(n) / SR
    f = f_end + (f_start - f_end) * np.exp(-t / 0.08)
    ph = 2 * np.pi * np.cumsum(f) / SR
    env = np.minimum(t / 0.008, 1) * np.exp(-t / tau)
    x = (np.sin(ph) + 0.125 * np.sin(2 * ph)) * env
    return _norm(_lp(x, 400))


def thud():
    n = int(0.4 * SR)
    t = np.arange(n) / SR
    x = np.sin(2 * np.pi * 68 * t) * np.minimum(t / 0.01, 1) * np.exp(-t / 0.12)
    return _norm(x)


def rise(dur=1.8):
    n = int(dur * SR)
    t = np.arange(n) / SR
    u = t / dur
    r = np.random.default_rng(3)
    ramp = 10 ** ((u - 1.0))
    nz = _lp(r.standard_normal(n), 350) * ramp
    tone = np.sin(2 * np.pi * np.cumsum(30 + 28 * u) / SR) * ramp
    x = nz / (np.abs(nz).max() + 1e-9) * 0.7 + tone
    x[-int(0.02 * SR):] *= np.linspace(1, 0, int(0.02 * SR))
    return _norm(x)


def air():
    n = int(0.25 * SR)
    t = np.arange(n) / SR
    r = np.random.default_rng(5)
    x = RS.fft_filter(r.standard_normal(n), lo=1500, hi=6000, order=3)
    x = _lp(x, 8000) * np.minimum(t / 0.005, 1) * np.exp(-t / 0.08)
    ir = np.zeros(int(0.12 * SR))
    idx = (np.array([0.0, 0.004, 0.009, 0.017, 0.03, 0.05, 0.08]) * SR).astype(int)
    ir[idx] = [1, .5, .35, .25, .15, .08, .04]
    return _norm(np.convolve(x, ir)[: int(0.37 * SR)])


def tick(f=1600.0):
    n = int(0.12 * SR)
    t = np.arange(n) / SR
    r = np.random.default_rng(int(f))
    x = np.sin(2 * np.pi * f * t) * np.minimum(t / 0.008, 1) * np.exp(-t / 0.025) + 0.05 * r.standard_normal(n) * np.exp(-t / 0.02)
    return _norm(x)


def clock():
    n = int(0.05 * SR)
    t = np.arange(n) / SR
    r = np.random.default_rng(9)
    click = RS.fft_filter(r.standard_normal(n), lo=1500, hi=2600) * np.exp(-t / 0.008)
    body = np.sin(2 * np.pi * 400 * t) * np.exp(-t / 0.012)
    return _norm(click / (np.abs(click).max() + 1e-9) + 0.6 * body)


def bubbles(dur, rate, seed, f0=300):
    n = int(dur * SR)
    out = np.zeros(n)
    r = np.random.default_rng(seed)
    for t0 in np.sort(r.uniform(0, dur, int(dur * rate))):
        m = int(0.04 * SR)
        tt = np.arange(m) / SR
        f = (f0 + r.uniform(0, 500)) * (1 + 6 * tt)
        b = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt / 0.012) * r.uniform(0.3, 1)
        i = int(t0 * SR)
        seg = b[: max(0, min(m, n - i))]
        out[i:i + len(seg)] += seg
    return out


def crackle(dur, rate, seed, hi=3500):
    n = int(dur * SR)
    out = np.zeros(n)
    r = np.random.default_rng(seed)
    for t0 in r.uniform(0, dur - 0.05, int(dur * rate)):
        m = int(0.012 * SR)
        tt = np.arange(m) / SR
        c = r.standard_normal(m) * np.exp(-tt / 0.003) * r.uniform(0.2, 1) ** 2
        i = int(t0 * SR)
        out[i:i + m] += c
    return _lp(out, hi)


def slow_mod(n, seed, per=8.0, depth=0.5):
    r = np.random.default_rng(seed)
    k = np.cumsum(r.standard_normal(n))
    k = RS.fft_filter(k, hi=1.5 / per, order=2)
    k = k / (np.abs(k).max() + 1e-9)
    return 1 - depth + depth * (0.5 + 0.5 * k)


def amb(text, dur):
    n = int(dur * SR)
    r = np.random.default_rng(zlib.crc32(text.encode()) % 1000 + 1)
    tl = text.lower()
    nz = r.standard_normal(n)
    if "surf" in tl or "sea" in tl:
        x = _lp(nz, 900) * slow_mod(n, 1, 7.0, 0.7)
    elif "underwater" in tl:
        x = _lp(nz, 350) * 0.6 + 0.3 * bubbles(dur, 1.2, 2)
    elif "eruption" in tl:
        x = _lp(nz, 90) * slow_mod(n, 3, 5.0, 0.8) * 1.5 + 0.5 * crackle(dur, 14, 4, 1200)
    elif "lava" in tl:
        x = _lp(nz, 140) * slow_mod(n, 5, 5.0, 0.6) * 1.3 + 0.7 * crackle(dur, 22, 6, 1500) + 0.25 * bubbles(dur, 2, 7, 200)
    elif "fire" in tl:
        x = _lp(nz, 450) * 0.4 + 1.0 * crackle(dur, 45, 8, 4000)
    elif "soda" in tl or "fizz" in tl:
        grain = (r.random(n // 200 + 1).repeat(200)[:n] > 0.4) * 0.6 + 0.4
        x = RS.fft_filter(nz, lo=3000, hi=8000, order=3) * grain * slow_mod(n, 9, 4.0, 0.3)
    elif "gas" in tl or "hiss" in tl:
        x = RS.fft_filter(nz, lo=2500, hi=7000, order=3) * 0.35 + 0.8 * bubbles(dur, 3, 10, 250)
    elif "bubble" in tl:
        x = bubbles(dur, 4, 11, 280) + 0.1 * _lp(nz, 300)
    elif "sub swell" in tl or "warm sub" in tl:
        x = np.sin(2 * np.pi * np.cumsum(40 + 15 * np.sin(np.arange(n) / SR * 0.5)) / SR) * slow_mod(n, 12, 6.0, 0.6)
    elif "forest" in tl or "leaves" in tl:
        x = RS.fft_filter(nz, lo=900, hi=3000, order=2) * slow_mod(n, 13, 5.0, 0.6)
    else:
        x = RS.fft_filter(nz, lo=250, hi=1300, order=2) * slow_mod(n, 14, 6.0, 0.75)
    fade = min(int(1.0 * SR), n // 2)
    env = np.ones(n)
    env[:fade] = np.linspace(0, 1, fade)
    env[-fade:] = np.linspace(1, 0, fade)
    return _norm(x * env)


def render(ev, end=None):
    t = ev["type"]
    if t == "BOOM":
        return boom()
    if t == "BOOM-soft":
        return boom(f_end=45, f_start=55, tau=0.25, dur=1.2)
    if t == "THUD":
        return thud()
    if t == "RISE":
        return rise(min(1.8, max(1.0, end - ev["t"])) if end else 1.8)
    if t == "AIR":
        return air()
    if t == "TICK":
        m = re.search(r"square (\d)", ev["text"])
        return tick(1400 + 150 * (int(m[1]) - 1) if m else 1600.0)
    if t == "CLOCK":
        return clock()
    if t == "AMB":
        return amb(ev["text"], min(max(end - ev["t"], 3.0), 12.0) if end else 6.0)
