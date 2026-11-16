"""Noor-e-Raah History video builder (per-line "sfx": [[file, offset_s, dB]] one-shots and "amb": [[file, dB]] looping beds)

Noor-e-Raah History video builder (16:9, still images + ~25% 2.5D motion shots, narration, subs, SFX, music).

    .venv\\Scripts\\python -X utf8 scripts\\history_build.py <story dir> [--tts] [--seconds N]

<story dir>/script.json:
  {"title": "...", "voice": "Charon", "style": "<TTS style>", "ayah_ar": "...", "tempo": 1.0,
   "ambience": "shared/sfx/noor/desert_wind_felixblume_156414.mp3",
   "lines": [{"n":1, "text":"Hindi narration", "img":"01_x", "motion":false, "preset":"push_in",
              "overlay":[["dust",0.25]], "sfx":[["shared/sfx/steps_682886.mp3", 0.5, -8]],
              "ayah":false, "translit_ar":null}]}
Images: <story dir>/images/<img>.png.  --tts makes missing line audio (audio/l<n>.wav, free key first).
Output: <story dir>/output/video.mp4 (+ video.srt).  Rs0 except TTS fallback.
Motion shots (motion:true) use tools/parallax.py (depth parallax + overlays); others a slow eased zoom/pan.
"""
import json
import subprocess
import sys
import wave
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "scripts"))
import parallax  # noqa: E402

parallax.MAX_SECONDS = 20
FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe")
FONTS = ROOT / "shared/fonts"
PRESETS = ["push_in", "pan_right", "pull_out", "pan_left"]
PAD = 0.45
SR = 24000


def dur(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def ts(x):
    h = int(x // 3600)
    m = int(x % 3600 // 60)
    s = x % 60
    return f"{h}:{m:02d}:{s:05.2f}"


def esc(p):
    return Path(p).resolve().as_posix().replace(":", "\\:")


def make_tts(D, cfg):
    import gemini_tts
    A = D / "audio"
    A.mkdir(exist_ok=True)
    for l in cfg["lines"]:
        out = A / f"l{l['n']:02d}.wav"
        if out.exists():
            continue
        gemini_tts.speak(l["text"], cfg.get("voice", "Charon"), cfg["style"], out, free_only=False)
        print("tts", l["n"], "ok")


def main():
    D = Path(sys.argv[1]).resolve()
    cfg = json.loads((D / "script.json").read_text(encoding="utf-8"))
    limit = float(sys.argv[sys.argv.index("--seconds") + 1]) if "--seconds" in sys.argv else 1e9
    if "--tts" in sys.argv:
        try:
            make_tts(D, cfg)
        except Exception as e:  # the Gemini wrapper writes the wav then fails on cost-log path in worktrees
            print("tts note:", str(e)[:120])
    W = D / "work"
    W.mkdir(exist_ok=True)
    (D / "output").mkdir(exist_ok=True)
    tempo = float(cfg.get("tempo", 1.0))
    tl = []
    t = 0.0
    for i, l in enumerate(cfg["lines"]):
        a = D / f"audio/l{l['n']:02d}.wav"
        d = dur(a) / tempo + PAD + (0.8 if i == len(cfg["lines"]) - 1 else 0)
        tl.append((l, a, t, d))
        t += d
        if t >= limit:
            break
    TOTAL = min(t, limit)
    print("total", round(TOTAL, 1), "s;", sum(1 for x in tl if x[0].get("motion")), "motion shots of", len(tl))
    clips = []
    for i, (l, a, st, d) in enumerate(tl):
        c = W / f"c{l['n']:02d}_{d:.1f}.mp4"
        if not c.exists():
            ov = [(k, float(o), (0.5, 0.6)) for k, o in l.get("overlay", [])]
            parallax.render_clip(D / f"images/{l['img']}.png", c, seconds=d, preset=l.get("preset", PRESETS[i % 4]),
                                 fmt="long", mode="auto" if l.get("motion") else "zoom", overlays=ov, amp=float(l.get("amp", cfg.get("amp", 0.08))))
        clips.append(c)
    (W / "list.txt").write_text("".join(f"file '{c.as_posix()}'\n" for c in clips))
    # ---- subtitles (libass; Hindi Mukta Bold, Arabic Amiri)
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
            "[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
            "Style: Sub,Mukta Bold,62,&H00FFFFFF,&H00FFFFFF,&H8C0A0C14,&H8C0A0C14,0,0,0,0,100,100,0,0,3,14,0,2,160,160,60,1\n"
            "Style: Ayah,Amiri,330,&H0078C8F0,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,0,3,8,0,0,0,0\n"
            "Style: Tr,Mukta Bold,70,&H00FFFFFF,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,3,2,8,0,0,0,1\n"
            "Style: Src,Mukta Bold,44,&H006EAAC8,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,2,1,8,0,0,0,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    ev, srt = [], []
    for k, (l, a, st, d) in enumerate(tl, 1):
        e = min(st + d - 0.05, TOTAL)
        if l.get("ayah"):
            ev.append(r"Dialogue: 0,%s,%s,Ayah,,0,0,0,,{\pos(960,330)\fad(300,200)}%s" % (ts(st), ts(e), cfg["ayah_ar"]))
            ev.append(r"Dialogue: 0,%s,%s,Tr,,0,0,0,,{\pos(960,560)\fad(300,200)}%s" % (ts(st), ts(e), l["text"].replace("\n", r"\N")))
            ev.append(r"Dialogue: 0,%s,%s,Src,,0,0,0,,{\pos(960,860)\fad(300,200)}%s" % (ts(st), ts(e), cfg.get("ayah_src", "")))
        else:
            txt = l["text"]
            for w in l.get("gold", []):  # keyword highlight (learned from reference style, 2026-11-13)
                txt = txt.replace(w, r"{\1c&H0078C8F0&}" + w + r"{\1c&HFFFFFF&}")
            ev.append(f"Dialogue: 0,{ts(st)},{ts(e)},Sub,,0,0,0,,{txt}")
            if l.get("src"):  # small source tag under the caption, e.g. hadith number
                ev.append(r"Dialogue: 0,%s,%s,Src,,0,0,0,,{\pos(960,1030)\fad(200,150)}%s" % (ts(st), ts(e), l["src"]))
        srt.append(f"{k}\n{ts(st).replace('.', ',')} --> {ts(e).replace('.', ',')}\n{l['text']}\n")
    (W / "subs.ass").write_text(head + "\n".join(ev) + "\n", encoding="utf-8")
    (D / "output/video.srt").write_text("\n".join(srt), encoding="utf-8")
    # ---- voice track
    buf = np.zeros(int(TOTAL * SR) + SR, dtype=np.float32)
    for l, a, st, d in tl:
        sp = W / f"v{l['n']:02d}.wav"
        if tempo != 1.0:
            subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(a), "-af", f"atempo={tempo}", str(sp)], check=True)
        else:
            sp = a
        with wave.open(str(sp)) as w:
            x = np.frombuffer(w.readframes(w.getnframes()), dtype=np.int16).astype(np.float32) / 32768
        s = int(st * SR) + int(0.1 * SR)
        buf[s:s + len(x)] += x[:len(buf) - s]
    buf = buf[:int(TOTAL * SR)]
    buf = buf / max(1e-6, np.abs(buf).max()) * 0.85
    with wave.open(str(W / "voice.wav"), "wb") as w:
        w.setnchannels(1)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes((buf * 32767).astype(np.int16).tobytes())
    # ---- mix (clear voice first): voice + per-scene music (crossfaded) + ambience beds (both ducked under voice) + SFX hits
    inputs = [FF, "-y", "-f", "concat", "-safe", "0", "-i", str(W / "list.txt"), "-i", str(W / "voice.wav")]
    n_in = 2
    fcs = []
    bg, hits = [], []
    default_music = cfg.get("music", "shared/music/noor/River_Flute.mp3")
    mvol = cfg.get("music_vol", 0.5)
    groups = []  # per-scene music cue: consecutive lines with the same track share one segment
    for l, a_, st, d in tl:
        m = l.get("music", default_music)
        if groups and groups[-1][0] == m:
            groups[-1][2] = st + d
        else:
            groups.append([m, st, st + d])
    for gi, (m, g0, g1) in enumerate(groups):
        seg = (g1 - g0) + (1.5 if gi < len(groups) - 1 else 0.0)
        inputs += ["-stream_loop", "-1", "-i", str(ROOT / m)]
        fo = max(0.0, seg - 1.5)
        ms = int(g0 * 1000)
        fcs.append(f"[{n_in}:a]atrim=0:{seg:.2f},asetpts=PTS-STARTPTS,volume={mvol},afade=t=in:d=1.5,"
                   f"afade=t=out:st={fo:.2f}:d=1.5,adelay={ms}|{ms}[b{n_in}]")
        bg.append(f"[b{n_in}]")
        n_in += 1
    amb_db = float(cfg.get("amb_db", -6))   # extra dB on every ambience bed (keeps speech clear)
    sfx_db = float(cfg.get("sfx_db", -3))
    for l, a_, st, d in tl:
        for f, gain in l.get("amb", []):
            pth = ROOT / f
            if not pth.exists():
                print("missing amb", f); continue
            inputs += ["-stream_loop", "-1", "-i", str(pth)]
            ms = int(max(0.0, st - 0.3) * 1000)
            fcs.append(f"[{n_in}:a]atrim=0:{d + 0.9:.2f},asetpts=PTS-STARTPTS,volume={gain + amb_db}dB,afade=t=in:d=0.6,"
                       f"afade=t=out:st={d + 0.3:.2f}:d=0.6,adelay={ms}|{ms}[b{n_in}]")
            bg.append(f"[b{n_in}]")
            n_in += 1
        for f, off, gain in l.get("sfx", []):
            pth = ROOT / f
            if not pth.exists():
                print("missing sfx", f); continue
            inputs += ["-i", str(pth)]
            ms = int((st + off) * 1000)
            fcs.append(f"[{n_in}:a]volume={gain + sfx_db}dB,adelay={ms}|{ms}[h{n_in}]")
            hits.append(f"[h{n_in}]")
            n_in += 1
    duck = cfg.get("duck", True)
    fc = f"[0:v]subtitles=filename='{esc(W / 'subs.ass')}':fontsdir='{esc(FONTS)}'[v];" + ";".join(fcs) + ";"
    fc += "[1:a]highpass=f=70,asplit=2[vo][vsc];"
    fc += "".join(bg) + f"amix=inputs={len(bg)}:duration=longest:normalize=0[bgraw];"
    if duck:
        fc += "[bgraw][vsc]sidechaincompress=threshold=0.02:ratio=10:attack=15:release=500:makeup=1[bgd];"
    else:
        fc += "[bgraw]anull[bgd];[vsc]anullsink;"
    mixin = ["[vo]", "[bgd]"] + hits
    fc += "".join(mixin) + f"amix=inputs={len(mixin)}:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]"
    full = inputs
    out = D / "output/video.mp4"
    cmd = full + ["-filter_complex", fc, "-map", "[v]", "-map", "[a]", "-t", f"{TOTAL:.2f}", "-c:v", "libx264", "-crf", "18",
                  "-preset", "medium", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k", "-movflags", "+faststart", str(out)]
    r = subprocess.run(cmd, capture_output=True, text=True)
    print("OK" if r.returncode == 0 else r.stderr[-900:], out)


if __name__ == "__main__":
    main()
