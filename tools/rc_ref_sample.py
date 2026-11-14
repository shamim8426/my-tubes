"""Reference-style sample mix for the first minute of 002: ONE beatless dark ambient bed + sub booms/thuds only, smooth music-off at the pivot line.
python tools/rc_ref_sample.py 002 [--track shared/music/doc2/Ancient_Rite.mp3] [--end 60]
Writes cache/reality-check/002/ref_sample/{mix_norm.wav, report.txt} and prints the measured music envelope, level under voice and event-vs-timing deltas. No video, no upload."""
import argparse
import json
import re
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import rc_fx_v5 as FX  # noqa: E402
import rc_music_mix as MM  # noqa: E402
import rc_sound as RS  # noqa: E402

SR, CR = RS.SR, RS.CR


def cos_ramp(t, a, b, up):
    """0 before a, 1 after b, cosine in between (up=True) ; mirrored when up=False."""
    x = np.clip((t - a) / (b - a), 0, 1)
    y = 0.5 - 0.5 * np.cos(np.pi * x)
    return y if up else 1 - y


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--track", default="shared/music/doc2/Ancient_Rite.mp3")
    ap.add_argument("--end", type=float, default=60.0)
    a = ap.parse_args()
    sd = next((ROOT / "channels/reality-check/stories").glob(a.story + "_*"))
    ld = sd / "long"
    lines = json.loads((sd / "audio/voiceover_timing.json").read_text(encoding="utf-8"))
    by = {l["line"]: l for l in lines}
    total = a.end
    N = int(total * SR)
    nc = int(total * CR) + 2
    voice = RS.load_audio(sd / "audio/voiceover_full.wav", 1)[:, 0][:N]
    sp = np.zeros(nc)
    for l in lines:
        sp[int(l["start"] * CR): min(nc, int(l["end"] * CR) + 1)] = 1.0
    spm = RS.env_interp(sp, N)
    vl = RS.lufs(voice[spm > 0.5])
    # ---- one bed, looped only if shorter than the sample
    bed = MM.full_track(a.track, 0.0, total)
    for ch in (0, 1):
        bed[:, ch] = RS.fft_filter(bed[:, ch], lo=45, hi=9000)
    t = np.arange(nc) / CR
    # pivot: L5 "ye hua kaise?" -> music off while the narrator continues (hold 27.4-32.9), 2 s down, 2.5 s up
    off0, off1 = by[5]["start"] - 0.2, by[6]["start"] - 2.9            # 27.4 .. 32.9
    d = np.zeros(nc)
    d += cos_ramp(t, off0 - 2.0, off0, True) * cos_ramp(t, off1, off1 + 2.5, False)
    d = np.where((t >= off0) & (t <= off1), 1.0, d)
    d = np.where(t > off1 + 2.5, 0.0, d)
    depth = 30.0
    env_db = -depth * d
    # open section a little louder (about 12 LU under the voice), body 15.5; changes over 3 s (brightness/density change = level only, same bed)
    open_db = 3.5 * cos_ramp(t, off0 - 2.0 - 3.0, off0 - 2.0, False)
    env_db += open_db
    env_db += -24.0 * np.clip(1 - t / 6.0, 0, 1)                         # fade in over 6 s
    env_db += -45.0 * np.clip(1 - (total - t) / 1.5, 0, 1) if False else 0
    bed *= RS.env_interp(10 ** (env_db / 20), N)[:, None]
    # calibrate so the BODY (after the pivot, 36-60 s speech) sits 15.5 LU under the voice
    body = (spm > 0.5) & (np.arange(N) / SR > by[6]["start"])
    ml = RS.lufs(bed[body])
    g = 10 ** ((vl - 15.5 - ml) / 20)
    bed *= g
    # ---- sub events only: opening soft boom, thud on the caption landing, title-card boom, section boom after the pivot (+ the plan's tick on the timeline pin at -24 dB)
    vpk = 20 * np.log10(np.abs(voice).max() + 1e-9)
    evs, _ = FX.parse_plan(str(ld / "sound_event_plan.md"))
    plan = {}
    txt = (ld / "sound_event_plan.md").read_text(encoding="utf-8")
    for row in txt.split("## 5.")[1].splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*(\d+):(\d\d\.\d)\s*\|", row)
        if m:
            plan[int(m[1])] = int(m[2]) * 60 + float(m[3])
    keep = []
    for e in evs:
        if e["t"] >= total - 1.0 or e["type"] not in ("BOOM", "BOOM-soft", "THUD", "TICK"):
            continue
        if e["type"] == "TICK" and e["rel"] < -23:                      # graphic ticks at about -24 dB
            keep.append(dict(e, rel=-24.0))
        elif e["type"] != "TICK":
            keep.append(e)
    # the section start after the pivot gets a full sub boom (2.2 s tail) instead of the soft one
    for e in keep:
        if e["line"] == 6 and e["type"] == "BOOM-soft":
            e["type"], e["rel"] = "BOOM", -6.0
    out = np.zeros(N, np.float32)
    rows = []
    for e in keep:
        snd = FX.render(e)
        i0 = int(e["t"] * SR)
        sg = snd[: N - i0] * 10 ** ((vpk + e["rel"]) / 20)
        out[i0:i0 + len(sg)] += sg
        l = by[e["line"]]
        rows.append((e["type"], e["line"], e["t"], l["start"] + (e["t"] - plan[e["line"]]), e["rel"]))
    music_only = bed.copy()
    bed[:, 0] += out
    bed[:, 1] += out
    mix = np.stack([voice, voice], 1) + bed
    cdir = ROOT / "cache/reality-check" / a.story / "ref_sample"
    cdir.mkdir(parents=True, exist_ok=True)
    raw = cdir / "mix_raw.f32"
    raw.write_bytes(mix.astype("<f4").tobytes())
    base = ["-f", "f32le", "-ar", str(SR), "-ac", "2", "-i", str(raw)]
    p = subprocess.run([MM.FF, "-hide_banner", *base, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11:print_format=json", "-f", "null", "-"], capture_output=True, text=True)
    js = json.loads(re.findall(r"\{[^{}]*\"input_i\"[^{}]*\}", p.stderr, re.S)[-1])
    ln = (f"loudnorm=I=-14:TP=-1.5:LRA=11:measured_I={js['input_i']}:measured_TP={js['input_tp']}:measured_LRA={js['input_lra']}:measured_thresh={js['input_thresh']}"
          f":offset={js['target_offset']}:linear=true,alimiter=limit=0.82:level=disabled,aresample=48000")
    subprocess.run([MM.FF, "-y", "-loglevel", "error", *base, "-af", ln, "-t", f"{total:.3f}", str(cdir / "mix_norm.wav")], check=True)
    # ---- measurements
    rep = [f"bed track: {a.track}", f"voice {vl:.1f} LUFS; body music = voice - 15.5 LU by construction"]
    mono = music_only.mean(1)
    fr = int(0.5 * SR)
    n = len(mono) // fr
    r = 20 * np.log10(np.sqrt((mono[: n * fr].reshape(n, fr) ** 2).mean(1)) + 1e-9)
    # envelope slope on the applied gain (not the music's own dynamics): env_db + open step, 1 s windows
    G = env_db[:nc]
    slope = np.abs(G[CR:] - G[:-CR])
    rep.append("music-only 0.5 s RMS (dBFS) every 2.5 s: " + " ".join(f"{i * 0.5:.0f}s:{r[i]:.0f}" for i in range(0, n, 5)))
    rep.append(f"applied music gain: max {slope.max():.1f} dB/s (off ramps designed: 2 s down / 2.5 s up, depth {depth:.0f} dB); fade-in 6 s from -24 dB")
    for s0 in range(0, int(total), 10):
        a_, b_ = s0 * SR, min((s0 + 10) * SR, N)
        mk = (spm[a_:b_] > 0.5)
        if mk.sum() > SR // 2:
            rep.append(f"  {s0:2d}-{s0 + 10:2d} s: music {RS.lufs(music_only[a_:b_][mk]) - RS.lufs(voice[a_:b_][mk]):6.1f} LU vs voice (speech frames)")
    rep.append("events (type, line, mix time, time from timing json, delta s, level vs voice peak):")
    for ty, ln_, tm, tj, rel in rows:
        rep.append(f"  {ty:9s} L{ln_:<3d} {tm:6.2f}  {tj:6.2f}  {tm - tj:+.2f}  {rel:+.0f} dB   (line {by[ln_]['start']:.2f}-{by[ln_]['end']:.2f})")
    rep.append(f"music-off hold {off0:.1f}-{off1:.1f} s (L5 'ye hua kaise?' line {by[5]['start']:.2f}-{by[5]['end']:.2f}); section boom at L6 start {by[6]['start']:.2f}")
    e = subprocess.run([MM.FF, "-hide_banner", "-nostats", "-i", str(cdir / "mix_norm.wav"), "-filter_complex", "ebur128=peak=true", "-f", "null", "-"], capture_output=True, text=True).stderr
    rep += [x.strip() for x in e.splitlines() if re.search(r"^\s+(I|Peak):", x)][-2:]
    (cdir / "report.txt").write_text("\n".join(rep), encoding="utf-8")
    print("\n".join(rep))


if __name__ == "__main__":
    main()
