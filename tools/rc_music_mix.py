"""Documentary score for a Long: REAL music tracks follow the script's emotional arc (cue map), crossfaded, ducked under speech.
python tools/rc_music_mix.py 002 [--cues long/music_cues.json] [--samples "0-60,325-365"] [--below 21]
Writes (cache/reality-check/<story>/music/): music_stem.wav, mix_norm.wav (voice+music, loudnorm -14 two-pass), sample_<a>-<b>.mp3, report.txt; long/sound_cues.md.
Does NOT touch the video.  Music: high-pass 60 Hz, low-pass 9 kHz, calibrated to (voice LUFS - below) in speech, +3 dB in silent holds, extra dip on key numbers, fades.
Cue file: {"xf": 5, "fade_in": 4, "fade_out": 12, "cues": [{"t": 0, "track": "shared/music/doc/X.mp3", "off": 0, "name": "...", "arc": "..."}, ...], "number_lines": [22, 24, ...]}"""
import argparse
import re
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import rc_sound as RS  # noqa: E402

SR = RS.SR
FF = RS.find_ff()


def load_track(path, off, dur):
    raw = subprocess.run([FF, "-v", "error", "-ss", f"{off:.2f}", "-i", str(ROOT / path), "-t", f"{dur:.2f}", "-ac", "2", "-ar", str(SR), "-f", "f32le", "-"], capture_output=True).stdout
    return np.frombuffer(raw, np.float32).reshape(-1, 2).copy()


def full_track(path, off, need):
    """need seconds of music starting at `off`; loops (equal-power crossfade, restarting a little later in the track) when the track is too short."""
    x = load_track(path, off, need + 2)
    if len(x) >= need * SR:
        return x[: int(need * SR)]
    whole = load_track(path, 0, 3600)
    out = x
    start = min(max(off, 15.0), max(len(whole) / SR - 40, 0))
    while len(out) < need * SR:
        nxt = whole[int(start * SR):]
        xf = int(4 * SR)
        w = np.linspace(0, np.pi / 2, xf)
        out[-xf:] = out[-xf:] * np.cos(w)[:, None] + nxt[:xf] * np.sin(w)[:, None]
        out = np.concatenate([out, nxt[xf:]])
        start = (start + 25) % max(len(whole) / SR - 60, 30)
    return out[: int(need * SR)]


# ---------------------------------------------------------------- synthesised, clearly audible effects (own work, no licence issue)
def _env(n, a, d):
    t = np.arange(n) / SR
    return np.minimum(t / a, 1.0) * np.exp(-t / d)


def synth_fx(kind, seed=7):
    r = np.random.default_rng(seed)
    if kind == "impact":      # low boom: sub sweep + body thump + dark noise burst, 2.8 s tail
        n = int(2.8 * SR); t = np.arange(n) / SR
        sub = np.sin(2 * np.pi * np.cumsum(32 + 70 * np.exp(-t * 6)) / SR) * np.exp(-t / 0.9)
        thump = np.sin(2 * np.pi * np.cumsum(70 + 160 * np.exp(-t * 18)) / SR) * np.exp(-t / 0.28)
        nz = RS.fft_filter(r.standard_normal(n), lo=40, hi=220) * np.exp(-t / 0.35) * 0.5   # low only: no noise sweep
        x = sub + 0.8 * thump + nz
        x[:int(0.004 * SR)] *= np.linspace(0, 1, int(0.004 * SR))
    elif kind == "riser":     # 1.6 s tension build: rising filtered noise + rising tone, cut at the top
        n = int(1.6 * SR); t = np.arange(n) / SR; u = t / 1.6
        nz = r.standard_normal(n)
        lo, hi = 250 + 3500 * u ** 2, 700 + 6500 * u ** 2
        X = np.fft.rfft(nz); f = np.fft.rfftfreq(n, 1 / SR)
        out = np.zeros(n)
        for k in range(8):                       # time-varying band via 8 segments crossfaded
            c = (k + 0.5) / 8
            m = (f > 250 + 3500 * c ** 2) & (f < 700 + 6500 * c ** 2)
            band = np.fft.irfft(X * m, n)
            out += band * np.exp(-0.5 * ((u - c) / 0.09) ** 2)
        tone = np.sin(2 * np.pi * np.cumsum(90 + 520 * u ** 2) / SR) * 0.35
        x = (out / (np.abs(out).max() + 1e-9) * 0.9 + tone) * (u ** 1.8)
        x[-int(0.03 * SR):] *= np.linspace(1, 0, int(0.03 * SR))
    elif kind == "whoosh":    # 0.9 s band sweep, rises then falls
        n = int(0.9 * SR); t = np.arange(n) / SR; u = t / 0.9
        nz = r.standard_normal(n); X = np.fft.rfft(nz); f = np.fft.rfftfreq(n, 1 / SR)
        out = np.zeros(n)
        for k in range(8):
            c = (k + 0.5) / 8
            m = (f > 200 + 2600 * c) & (f < 500 + 4200 * c)
            out += np.fft.irfft(X * m, n) * np.exp(-0.5 * ((u - c) / 0.11) ** 2)
        x = out / (np.abs(out).max() + 1e-9) * np.sin(np.pi * u) ** 1.5
    else:                     # subhit: short low thud with air
        n = int(1.1 * SR); t = np.arange(n) / SR
        x = np.sin(2 * np.pi * np.cumsum(38 + 90 * np.exp(-t * 14)) / SR) * np.exp(-t / 0.3)
        x += 0.35 * RS.fft_filter(r.standard_normal(n), lo=300, hi=3000) * np.exp(-t / 0.08)
    return (x / (np.abs(x).max() + 1e-9)).astype(np.float32)


def write_wav(path, x):
    y = (np.clip(x, -1, 1) * 32767).astype("<i2")
    with wave.open(str(path), "wb") as w:
        w.setnchannels(2 if y.ndim == 2 else 1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(y.tobytes())


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--cues", default="")
    ap.add_argument("--samples", default="0-60,325-365")
    ap.add_argument("--below", type=float, default=21.0)
    a = ap.parse_args()
    sd = next((ROOT / "channels/reality-check/stories").glob(a.story + "_*"))
    ld = sd / "long"
    cfg = json.loads(Path(a.cues or ld / "music_cues.json").read_text(encoding="utf-8"))
    lines = json.loads((sd / "audio/voiceover_timing.json").read_text(encoding="utf-8"))
    voice = RS.load_audio(sd / "audio/voiceover_full.wav", 1)[:, 0]
    total = max(len(voice) / SR, lines[-1]["end"]) + 8.0 if False else 752.24
    N = int(total * SR)
    nc = int(total * RS.CR) + 2
    voice = np.pad(voice, (0, max(0, N - len(voice))))[:N]
    sp = np.zeros(nc)
    for l in lines:
        sp[int(l["start"] * RS.CR): int(l["end"] * RS.CR) + 1] = 1.0
    spm = RS.env_interp(sp, N)
    vl = RS.lufs(voice[spm > 0.5])
    # ---- music stem from the cue map
    cues = cfg["cues"]
    xf = cfg.get("xf", 5.0)
    music = np.zeros((N, 2), np.float32)
    for i, c in enumerate(cues):
        t0 = c["t"]
        t1 = cues[i + 1]["t"] if i + 1 < len(cues) else total
        a0, a1 = max(0.0, t0 - (xf / 2 if i else 0)), min(total, t1 + xf / 2)
        seg = full_track(c["track"], c.get("off", 0.0), a1 - a0)
        n = len(seg)
        win = np.ones(n)
        r = int(xf * SR)
        if i:
            win[:r] = np.sin(np.linspace(0, np.pi / 2, min(r, n)))[: min(r, n)]
        if i + 1 < len(cues):
            win[-r:] = np.cos(np.linspace(0, np.pi / 2, r))[:r] if n >= r else win[-r:]
        i0 = int(a0 * SR)
        music[i0:i0 + n] += (seg * win[:, None])[: N - i0]
    # filters: high-pass 60 Hz, low-pass 9 kHz (zero-phase FFT, smooth skirts)
    for ch in (0, 1):
        music[:, ch] = RS.fft_filter(music[:, ch], lo=60, hi=9000)
    # slow leveler: the tracks have loud and near-silent passages; keep the music loudness steady so it stays light but audible everywhere
    blk = SR // RS.CR
    nb = N // blk
    e = (music[: nb * blk] ** 2).mean(1).reshape(nb, blk).mean(1) + 1e-10
    edb = 10 * np.log10(e)
    k = np.ones(int(8 * RS.CR)) / int(8 * RS.CR)
    sm = np.convolve(np.pad(edb, (len(k) // 2, len(k) // 2), mode="edge"), k, mode="valid")[: nb]
    gdb = np.clip(np.median(sm) - sm, -cfg.get("lev_max_down", 12.0), cfg.get("lev_max_up", 14.0))
    k2 = np.ones(int(5 * RS.CR)) / int(5 * RS.CR)
    gdb = np.convolve(np.pad(gdb, (len(k2) // 2, len(k2) // 2), mode="edge"), k2, mode="valid")[: nb]
    music[: nb * blk] *= np.repeat(10 ** (gdb / 20), blk)[:, None]
    # per-section energy: cue "energy" 1-5 -> relative level, smoothed across the section change (real dynamics between sections)
    EN = {1: -2.0, 2: 0.0, 3: 1.5, 4: 3.0, 5: 4.5}
    step = np.zeros(nc)
    for i, c in enumerate(cues):
        a0 = int(c["t"] * RS.CR)
        a1 = int((cues[i + 1]["t"] if i + 1 < len(cues) else total) * RS.CR)
        step[a0:a1] = c["gain_db"] if "gain_db" in c else EN.get(c.get("energy", 2), 0.0)
    kk = np.ones(int(5 * RS.CR)) / int(5 * RS.CR)
    stepdb = np.convolve(np.pad(step, (len(kk) // 2, len(kk) // 2), mode="edge"), kk, mode="valid")[: nc]
    music *= RS.env_interp(10 ** (stepdb / 20), N)[:, None]
    # envelope: speech 0 dB, silent holds +3 dB, small dip on key numbers, fades
    gap = 1.0 - sp
    env_db = cfg.get('gap_boost_db', 3.0) * RS.smooth_env(gap, 0.5, 1.2)
    num = np.zeros(nc)
    byline = {l["line"]: l for l in lines}
    for n_ in cfg.get("number_lines", []):
        l = byline.get(n_)
        if l:
            num[int((l["start"] - 0.3) * RS.CR): int((l["end"] + 0.2) * RS.CR)] = 1.0
    env_db += -cfg.get('number_dip_db', 3.0) * RS.smooth_env(num, 0.5, 0.9)
    # swell at section changes, near-silence just before key numbers (the number then lands), bigger swell in silent holds
    for c in cues[1:]:
        env_db += cfg.get("section_swell_db", 4.0) * np.exp(-0.5 * ((np.arange(nc) / RS.CR - c["t"]) / 2.5) ** 2)
    pre = np.zeros(nc)
    for n_ in cfg.get("pre_dip_lines", []):
        l = byline.get(n_)
        if l:
            pre[int((l["start"] - 1.0) * RS.CR): int((l["start"] + 0.6) * RS.CR)] = 1.0
    env_db += -cfg.get("pre_dip_db", 14.0) * RS.smooth_env(pre, 0.25, 0.6)
    big = np.zeros(nc)                      # every silent hold >= big_gap_min: the music swells hard (+12..18 dB) so the contrast is audible
    huge = np.zeros(nc)
    for l0, l1 in zip(lines[:-1], lines[1:]):
        g_ = l1["start"] - l0["end"]
        if g_ >= cfg.get("big_gap_min", 0.6):
            (huge if g_ >= 1.2 else big)[int((l0["end"] + 0.05) * RS.CR): int((l1["start"] - 0.05) * RS.CR)] = 1.0
    env_db += cfg.get("mid_gap_db", 12.0) * RS.smooth_env(big, 0.12, 0.35)
    env_db += cfg.get("big_gap_db", 16.0) * RS.smooth_env(huge, 0.12, 0.4)
    off = np.zeros(nc)                      # music FULLY OFF at pivot lines (question / reversal / answer), next cue starts as the gap ends
    for a0_, a1_ in cfg.get("off_windows", []):
        off[int(a0_ * RS.CR): int(a1_ * RS.CR)] = 1.0
    env_db += -70.0 * RS.smooth_env(off, 0.15, cfg.get("off_release", 0.25))
    fi, fo = cfg.get("fade_in", 4.0), cfg.get("fade_out", 12.0)
    t = np.arange(nc) / RS.CR
    env_db += 20 * np.log10(np.clip(np.minimum(t / fi, 1.0), 1e-3, 1)) * (t < fi)
    env_db += 20 * np.log10(np.clip(np.minimum((total - t) / fo, 1.0), 1e-3, 1)) * (t > total - fo)
    music *= RS.env_interp(10 ** (env_db / 20), N)[:, None]
    ml = RS.lufs((music * (spm > 0.5)[:, None]))
    g = 10 ** ((vl - a.below - ml) / 20)
    music *= g
    print(f"voice {vl:.1f} LUFS; music in speech {ml + 20 * np.log10(g):.1f} LUFS (= voice - {a.below:g} LU)")
    for h in (cfg.get("hits", []) if not cfg.get("plan") else []):            # impact stingers aligned to reveals (placed after calibration, level relative to the voice)
        hs = load_track(h["file"], 0, h.get("len", 3.0))
        fade = np.linspace(1, 0, len(hs)) ** 1.5
        hs = hs * fade[:, None]
        hs *= 10 ** ((vl + h.get("rel", -16) - RS.lufs(hs)) / 20) if RS.lufs(hs) > -90 else 1.0
        i0 = int(h["t"] * SR)
        music[i0:i0 + len(hs)] += hs[: N - i0]
    vr = 20 * np.log10(np.sqrt((voice[spm > 0.5] ** 2).mean()) + 1e-9)
    vpk = 20 * np.log10(np.abs(voice).max() + 1e-9)          # voice peak (dBFS): effect levels below are peak-vs-voice-peak
    fxlog = []

    def put_fx(kind, t0, rel, note):
        snd = synth_fx(kind)
        RS.place(music, snd, t0, 10 ** ((vpk + rel) / 20))
        fxlog.append((t0, kind, rel, note))
    if cfg.get("plan"):                        # v5: events from the sound event plan (reference-study recipes)
        import rc_fx_v5 as FX
        evs, _ = FX.parse_plan(str(ROOT / cfg["plan"]))
        lend = {l["line"]: l["end"] for l in lines}
        booms = [e["t"] for e in evs if e["type"].startswith("BOOM")]
        cnt = {}
        for e in evs:
            end = None
            if e["type"] == "RISE":
                end = min([b_ for b_ in booms if 0.5 < b_ - e["t"] < 2.6] or [e["t"] + 1.8])
            elif e["type"] == "AMB":
                m_ = re.search(r"by (\d+(?:\.\d)?) s", e["text"])
                end = float(m_[1]) if m_ else lend.get(e["line"] + (1 if re.search(r"lines? \d+-\d+", e["text"]) else 0), e["t"] + 6)
                nb = [b_ for b_ in booms if 0 < b_ - e["t"] < 12]
                if nb:
                    end = min(end, nb[0] + 0.4)
            snd = FX.render(e, end)
            i0 = int((e["t"] - (len(snd) / SR if e["type"] == "RISE" and False else 0)) * SR)
            if e["type"] == "RISE":
                i0 = int((end - len(snd) / SR) * SR)
            g_ = 10 ** ((vpk + e["rel"] + (cfg.get("amb_boost", 0.0) if e["type"] == "AMB" else 0.0)) / 20)
            mono = snd * g_
            if i0 + len(mono) > N:
                mono = mono[: N - i0]
            music[i0:i0 + len(mono), 0] += mono
            music[i0:i0 + len(mono), 1] += mono
            cnt[e["type"]] = cnt.get(e["type"], 0) + 1
            fxlog.append((e["t"], e["type"], e["rel"], e["text"][:40]))
        print("events placed:", cnt)
        for w_ in cfg.get("off_windows", []):          # new cue starts with a soft hit at the end of each music-off window
            if not any(abs(e["t"] - w_[1]) < 1.5 and e["type"].startswith("BOOM") for e in evs):
                snd = FX.render({"type": "BOOM-soft"}) * 10 ** ((vpk - 8.0) / 20)
                i0 = int(w_[1] * SR)
                music[i0:i0 + len(snd), 0] += snd[: N - i0]
                music[i0:i0 + len(snd), 1] += snd[: N - i0]
                fxlog.append((w_[1], "BOOM-soft", -8.0, "cue-start hit after music-off"))
    else:
        for q in cfg.get("sfx", []):
            put_fx("whoosh" if "whoosh" in q["kind"] else "subhit", q["t"], cfg.get("sfx_rel", -11.0) if "whoosh" in q["kind"] else cfg.get("sub_rel", -10.0), f"graphic start line {q.get('line', '')}")
    (ROOT / "cache/reality-check" / a.story / "music").mkdir(parents=True, exist_ok=True)
    (ROOT / "cache/reality-check" / a.story / "music/fx_log.json").write_text(json.dumps(fxlog), encoding="utf-8")
    cdir = ROOT / "cache/reality-check" / a.story / "music"
    cdir.mkdir(parents=True, exist_ok=True)
    write_wav(cdir / "music_stem.wav", music)
    mix = np.stack([voice, voice], 1) + music
    raw = cdir / "mix_raw.f32"
    raw.write_bytes(mix.astype("<f4").tobytes())
    base = ["-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw)]
    p = subprocess.run([FF, "-hide_banner", *base, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S)[-1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}"
          f":offset={js['target_offset']}:linear=true,alimiter=limit=0.82:level=disabled,aresample=48000")
    subprocess.run([FF, "-y", "-loglevel", "error", *base, "-af", ln, "-t", f"{total:.3f}", str(cdir / "mix_norm.wav")], check=True)
    for s in a.samples.split(","):
        a0, a1 = [float(x) for x in s.split("-")]
        out = cdir / f"sample_{int(a0)}-{int(a1)}.mp3"
        subprocess.run([FF, "-y", "-loglevel", "error", "-ss", f"{a0}", "-t", f"{a1 - a0}", "-i", str(cdir / "mix_norm.wav"), "-af", f"afade=t=in:st=0:d=0.3,afade=t=out:st={a1 - a0 - 1.0}:d=1.0", "-c:a", "libmp3lame", "-b:a", "192k", str(out)], check=True)
        print("SAMPLE", out)
    # objective report
    rep = []
    e = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(cdir / "mix_norm.wav"), "-filter_complex", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    rep += [x.strip() for x in e.splitlines() if re.search(r"^\s+(I|LRA|Peak):", x)][-3:]
    fl = []
    n = 4096
    mono = music.mean(1)
    for i in range(0, N - n, n * 8):
        if spm[i] > 0.5:
            S = np.abs(np.fft.rfft(mono[i:i + n] * np.hanning(n)))[8:1500] + 1e-9
            fl.append(float(np.exp(np.log(S).mean()) / S.mean()))
    rep.append(f"music stem spectral flatness (median over speech frames; white noise ~0.56, tonal music < 0.2): {np.median(fl):.3f}")
    X = np.abs(np.fft.rfft(mono[: N // 8 * 8].reshape(-1)[: 2 ** 22])) ** 2
    fr = np.fft.rfftfreq(2 ** 22, 1 / SR)
    tot = X.sum()
    rep.append("music band energy: <100 Hz %.0f%%, 100-2k %.0f%%, 2k-9k %.0f%%, >9k %.2f%%" % tuple(100 * X[(fr >= lo) & (fr < hi)].sum() / tot for lo, hi in ((0, 100), (100, 2000), (2000, 9000), (9000, 1e6))))
    (cdir / "report.txt").write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
