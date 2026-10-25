"""Noor-e-Raah 30 s SYNC SAMPLE (user 2026-10-24), style a (cinematic painted): real script lines (parichay 5-7 +
ayah 1 lines 30, 32), 3 new images + the look-test image a + 1 calligraphy title card (font), Ken Burns shots, music and
ambience cues, music fade-out 1 s before the Arabic ayah, River Flute back after it. Paid key allowed (free first);
budget "noor_samples" (₹45 incl. GST) checked before every paid call.

    .venv\\Scripts\\python -X utf8 scripts\\noor_sync_sample.py             # style a -> samples/sync_sample/
    .venv\\Scripts\\python -X utf8 scripts\\noor_sync_sample.py --style b   # style b test -> samples/sync_sample_b/
      (user 2026-10-25, budget "noor_style_b" ₹12: 2 new images; the look-test b image is reused and the door shot
       reuses the dawn image with another move; voice lines copied from the style a sample)
"""
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import numpy as np  # noqa: E402

import gemini_image  # noqa: E402
import gemini_tts  # noqa: E402
import pricing  # noqa: E402
import story_budget  # noqa: E402
from name_guard import find_names  # noqa: E402
from noor_audition import missing  # noqa: E402
from noor_look_test import SCENE as LOOK_SCENE, STYLES  # noqa: E402,F401

ROOT = Path(__file__).resolve().parent.parent
STYLE_B = "--style" in sys.argv and sys.argv[sys.argv.index("--style") + 1] == "b"
OUT = ROOT / "channels/noor-e-raah/samples" / ("sync_sample_b" if STYLE_B else "sync_sample")
LOOK_A = ROOT / "channels/noor-e-raah/samples/look_test" / ("b_soft_watercolor.png" if STYLE_B else "a_cinematic_painted.png")
BUDGET = "noor_style_b" if STYLE_B else "noor_samples"
FF = next(str(p) for p in (ROOT / "tools/ffmpeg/bin/ffmpeg.exe", ROOT / "tools/ffmpeg/ffmpeg.exe") if p.exists())
FONT_AR = ROOT / "shared/fonts/Amiri-Regular.ttf"
FONT_HI = ROOT / "shared/fonts/Mukta-Bold.ttf"
VOICES = json.loads((ROOT / "channels/noor-e-raah/channel.json").read_text(encoding="utf-8"))["voices"]
STYLE = STYLES["b_soft_watercolor" if STYLE_B else "a_cinematic_painted"]
IMAGES = {  # script SCREEN notes (parichay: valley in growing light; ayah 1: green earth after rain, morning sun)
    "dawn_valley": "A wide valley between two rocky hills of old Arabia at the very first light of dawn, the sky turning "
                   "from deep blue to soft gold, a sandy path, a few date palms, calm and hopeful. Wide 16:9; keep the "
                   "upper third calm for on-screen text.",
    "green_after_rain": "Desert ground turning green after rain: fresh small green shoots and tiny wildflowers on wet sand "
                        "between rocks, puddles reflecting the warm morning sun, soft mist, hills behind. Wide 16:9; keep "
                        "the upper-middle area calm for on-screen text.",
    "open_door_sunrise": "An old mud-brick house with a simple wooden door standing open at sunrise, warm light falling "
                         "on a small courtyard and a clay oil lamp on a ledge, a path leading out into the soft morning. "
                         "Wide 16:9.",
}
LINES = [  # (script line, speaker, text) — tags removed
    (5, "sawaal", "पहले नाम। 'फ़ातिहा' का मतलब क्या है?"),
    (6, "ustaad", "'फ़ातिहा' यानी खोलने वाली। क़ुरआन इसी सूरह से खुलता है।"),
    (7, "ustaad", "ये क़ुरआन की पहली सूरह है, और इसकी आयतें सात हैं — इस पर उलमा एक राय हैं।"),
    (30, "ustaad", "पहली आयत: अल्लाह के नाम से शुरू — वो, जो बेहद मेहरबान है, और बहुत रहम करने वाला है।"),
    (32, "ustaad", "यानी हर काम की शुरुआत अल्लाह के नाम से — उसकी मदद और बरकत के साथ।"),
]
ARABIC = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"  # Tanzil Uthmani 1:1, unchanged
TITLE_AR, TITLE_HI, SERIES = "سُورَةُ ٱلْفَاتِحَةِ", "सूरह अल-फ़ातिहा", "शुरू से क़ुरआन"
LABEL = "सरल भावार्थ — माने हुए तर्जुमों के आधार पर"
CARDS = ["मक्की (ज़्यादातर उलमा)", "आयतें: 7", "क़ुरआन में क्रम: 1"]
FPS, GAP, XF = 30, 0.6, 0.5


def run(args):
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *args], check=True)


def esc(p: Path) -> str:
    return p.resolve().as_posix().replace(":", "\\:")


def lufs(path, start=0.0, dur=None):
    args = [FF, "-hide_banner", "-nostats", "-ss", str(start)] + (["-t", str(dur)] if dur else []) + \
           ["-i", str(path), "-af", "ebur128=framelog=quiet", "-f", "null", "-"]
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", subprocess.run(args, capture_output=True, text=True).stderr)[-1])


def wav_len(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def images():
    (OUT / "images").mkdir(parents=True, exist_ok=True)
    for name, scene in IMAGES.items():
        if STYLE_B and name == "open_door_sunrise":  # ₹12 cap: 2 new images only
            continue
        img = OUT / "images" / f"{name}.png"
        if img.exists():
            continue
        if find_names(scene + " " + STYLE):
            sys.exit(f"BLOCK (RULES 12a): name in prompt {name}")
        est = pricing.image_estimate_usd(gemini_image.MODEL, "1K", len(scene) + len(STYLE), 0) * pricing.usd_to_inr()
        story_budget.check(BUDGET, est)
        gemini_image.generate(scene, img, aspect_ratio="16:9", size="1K", style=STYLE)


def voices():
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8", download_root=str(ROOT / "tools/whisper-models"))
    (OUT / "lines").mkdir(parents=True, exist_ok=True)
    if STYLE_B:  # same lines, same voices: copy the style a takes (₹0)
        import shutil
        for f in (OUT.parent / "sync_sample/lines").glob("*.*"):
            if not (OUT / "lines" / f.name).exists():
                shutil.copy(f, OUT / "lines" / f.name)
    files = []
    for n, who, text in LINES:
        f = OUT / "lines" / f"{n:03d}_{who}.wav"
        v = VOICES[who]
        ok = f.with_suffix(".ok")  # passed once = never re-checked (Whisper is not fully repeatable)
        for attempt in range(0 if (f.exists() and ok.exists()) else 3):  # first take + max 2 retries (RULES 1b)
            if not f.exists():
                story_budget.check(BUDGET, pricing.tts_estimate_usd(gemini_tts.MODEL, len(text) + len(v["style"]),
                                                                            len(text) / 8) * pricing.usd_to_inr())
                gemini_tts.speak(text, v["voice"], v["style"], f)
            with wave.open(str(f)) as w:
                sr = w.getframerate()
                x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
            x16 = np.interp(np.arange(0, len(x), sr / 16000), np.arange(len(x)), x).astype(np.float32)
            heard = " ".join(s.text.strip() for s in model.transcribe(x16, language="hi", beam_size=5)[0])
            miss = missing(text, heard)
            print(f"line {n} {who}: missing={miss} | {heard}")
            if not miss:
                ok.write_text(heard, encoding="utf-8")
                break
            if attempt == 2:
                break
            f.unlink()
        files.append(f)
    return files


def ts(t: float) -> str:
    t = max(t, 0.0)
    return f"{int(t // 3600)}:{int(t % 3600 // 60):02d}:{t % 60:05.2f}"


def hindi_ass(starts, lens, arabic_off, t_card) -> str:
    """All Hindi screen text through libass: ffmpeg drawtext drops the nuqta of क़ु (tested with Mukta and Nirmala)."""
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1920\nPlayResY: 1080\nWrapStyle: 2\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
            "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
            "MarginR, MarginV, Encoding\n"
            "Style: Sub,Mukta Bold,64,&H00FFFFFF,&H00FFFFFF,&H73000000,&H73000000,0,0,0,0,100,100,0,0,3,12,0,2,80,80,120,1\n"
            "Style: Card,Mukta Bold,58,&H00FFFFFF,&H00FFFFFF,&H64261408,&H64261408,0,0,0,0,100,100,0,0,3,14,0,7,0,0,0,1\n"
            "Style: Label,Mukta Bold,46,&H14FFFFFF,&H00FFFFFF,&H80000000,&H80000000,0,0,0,0,100,100,0,0,1,0,2,8,0,0,0,1\n"
            "Style: TitleHi,Mukta Bold,92,&H00FFFFFF,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,0,0,0,1\n"
            "Style: Series,Mukta Bold,52,&H005AA5C9,&H00FFFFFF,&H00000000,&H00000000,0,0,0,0,100,100,0,0,1,0,0,8,0,0,0,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    ev = [f"Dialogue: 0,{ts(0)},{ts(t_card)},TitleHi,,0,0,0,,{{\\pos(960,600)}}{TITLE_HI}",
          f"Dialogue: 0,{ts(0)},{ts(t_card)},Series,,0,0,0,,{{\\pos(960,722)}}{SERIES}"]
    for i, c in enumerate(CARDS):  # info cards during line 7
        ev.append(f"Dialogue: 0,{ts(starts[2] + i * 0.7)},{ts(starts[2] + lens[2])},Card,,0,0,0,,"
                  f"{{\\pos(115,{100 + i * 110})\\fad(250,200)}}{c}")
    ev.append(f"Dialogue: 0,{ts(starts[3])},{ts(arabic_off - 0.5)},Label,,0,0,0,,{{\\pos(960,452)\\fad(250,250)}}{LABEL}")
    for (_, _, text), s, ln in zip(LINES, starts, lens):
        ev.append(f"Dialogue: 0,{ts(s)},{ts(s + ln)},Sub,,0,0,0,,{text}")
    return head + "\n".join(ev) + "\n"


def title_card(path: Path):
    """Calligraphy title card made with fonts only (no AI text); its Hindi lines come from the ASS file."""
    t = OUT / "_title_ar.txt"
    t.write_text(TITLE_AR, encoding="utf-8")
    vf = ("drawbox=x=iw*0.18:y=ih*0.18:w=iw*0.64:h=ih*0.64:color=0xC9A55A@0.55:t=3,"
          "drawbox=x=iw*0.19:y=ih*0.195:w=iw*0.62:h=ih*0.61:color=0xC9A55A@0.25:t=1,"
          f"drawtext=fontfile='{esc(FONT_AR)}':textfile='{esc(t)}':text_shaping=1:fontsize=150:fontcolor=0xF3E3B8:"
          "x=(w-text_w)/2:y=h*0.30")
    run(["-f", "lavfi", "-i", "gradients=s=1920x1080:c0=0x0B1426:c1=0x1C2A44:x0=0:y0=0:x1=1920:y1=1080:d=1", "-frames:v", "1",
         "-vf", vf, str(path)])


MOVES = ["push_in", "pan_right", "pull_out", "pan_left", "gentle_orbit"]  # every shot a different move
MAX_SHOT = 8.0  # one move over 6-8 s; a longer stretch on one image is split into two moves


def shot(img: Path, dur: float, out: Path, preset: str):
    """Eased camera move (tools/parallax.py, "zoom" mode = no depth): 1.00 -> 1.07 or ~4% pan, sub-pixel cubic
    sampling - no zoompan integer-pixel shake (tools/motion_check.py)."""
    import parallax as PX
    frames = max(int(round(dur * FPS)), 1)
    enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "bgr24", "-s", "1920x1080",
                            "-r", str(FPS), "-i", "-", "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast",
                            "-crf", "16", "-pix_fmt", "yuv420p", str(out)], stdin=subprocess.PIPE)
    gen, _ = PX.shot_frames(img, 1920, 1080, frames, preset, mode="zoom")
    for f in gen:
        enc.stdin.write(f.tobytes())
    enc.stdin.close()
    if enc.wait():
        raise RuntimeError(f"encode failed: {out.name}")


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    images()
    files = voices()
    lens = [wav_len(f) for f in files]

    # ---- timeline (s)
    T_CARD = 2.2
    starts = [T_CARD + 0.3]
    for i in (1, 2):
        starts.append(starts[-1] + lens[i - 1] + GAP)
    fade_start = starts[2] + lens[2] + 0.4          # music fade-out 1 s
    A0 = fade_start + 1.0                           # Arabic only after the music is silent
    starts.append(A0 + 2.0)                         # Arabic alone ~2 s, then the bhaavarth
    arabic_off = starts[3] + lens[3] + 0.8          # Arabic fades 0.5 s, fully gone here
    music_back = arabic_off                         # River Flute starts only after the Arabic left
    starts.append(arabic_off + 0.6)
    END = starts[4] + lens[4] + 1.6
    print("timeline:", [round(s, 2) for s in starts], "fade", round(fade_start, 2), "A0", round(A0, 2),
          "arabic_off", round(arabic_off, 2), "end", round(END, 2))

    # ---- shots: card | look A (line 5) | dawn valley (6-7) | green after rain (ayah) | open door (matlab)
    card = OUT / "_card.png"
    title_card(card)
    base = [(card, 0.0), (LOOK_A, T_CARD), (OUT / "images/dawn_valley.png", starts[1] - 0.3),
            (OUT / "images/green_after_rain.png", fade_start), (OUT / ("images/dawn_valley.png" if STYLE_B else "images/open_door_sunrise.png"), arabic_off)]
    seq = []  # split stretches longer than MAX_SHOT into equal parts (same image, next move)
    for i, (img, s) in enumerate(base):
        e = base[i + 1][1] if i + 1 < len(base) else END
        parts = max(1, int(-(-(e - s) // MAX_SHOT)))
        seq += [(img, s + k * (e - s) / parts) for k in range(parts)]
    clips = []
    for i, (img, s) in enumerate(seq):
        nxt = seq[i + 1][1] if i + 1 < len(seq) else END
        dur = nxt - s + (XF if i + 1 < len(seq) else 0)
        c = OUT / f"_shot{i}.mp4"
        preset = "static_breathe" if img == card else MOVES[(i - 1) % len(MOVES)]
        shot(img, dur, c, preset)
        print(f"shot {i}: {img.name} {s:.1f}-{nxt:.1f}s {preset}")
        clips.append((c, s))
    # chain with xfade: clip i+1 content starts at its timeline start
    inputs, fc, last = [], [], "[0:v]"
    for i, (c, _) in enumerate(clips):
        inputs += ["-i", str(c)]
    for i in range(1, len(clips)):
        out_lbl = f"[x{i}]"
        fc.append(f"{last}[{i}:v]xfade=transition=fade:duration={XF}:offset={clips[i][1]:.3f}{out_lbl}")
        last = out_lbl

    # ---- text overlays (fonts only)
    ar = OUT / "_t_ar.txt"
    ar.write_text(ARABIC, encoding="utf-8")
    ass = OUT / "_hindi.ass"
    ass.write_text(hindi_ass(starts, lens, arabic_off, T_CARD), encoding="utf-8")
    ov = []
    a_alpha = (f"if(lt(t,{A0:.2f}),0,if(lt(t,{A0 + 0.5:.2f}),(t-{A0:.2f})/0.5,if(lt(t,{arabic_off - 0.5:.2f}),1,"
               f"if(lt(t,{arabic_off:.2f}),({arabic_off:.2f}-t)/0.5,0))))")
    ov.append(f"drawbox=x=0:y=ih*0.20:w=iw:h=ih*0.30:color=black@0.30:t=fill:enable='between(t,{A0:.2f},{arabic_off:.2f})'")
    ov.append(f"drawtext=fontfile='{esc(FONT_AR)}':textfile='{esc(ar)}':text_shaping=1:fontsize=96:fontcolor=white:"
              f"alpha='{a_alpha}':x=(w-text_w)/2:y=h*0.25:shadowcolor=black@0.6:shadowx=2:shadowy=2")
    ov.append(f"subtitles=filename='{esc(ass)}':fontsdir='{esc(FONT_HI.parent)}'")  # all Hindi text
    fc.append(f"{last}{','.join(ov)},format=yuv420p[vout]")

    # ---- audio
    voice = OUT / "_voice.wav"
    vin, vfc = [], []
    for i, (f, s) in enumerate(zip(files, starts)):
        vin += ["-i", str(f)]
        vfc.append(f"[{i}]aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo,adelay={int(s * 1000)}:all=1[d{i}]")
    run(vin + ["-filter_complex", ";".join(vfc) + ";" + "".join(f"[d{i}]" for i in range(len(files)))
               + f"amix=inputs={len(files)}:normalize=0,apad=whole_dur={END:.2f},atrim=0:{END:.2f}[o]", "-map", "[o]", str(voice)])
    v_gain = -16.0 - lufs(voice)
    soar, flute = ROOT / "shared/music/noor/Soaring.mp3", ROOT / "shared/music/noor/River_Flute.mp3"
    breeze = ROOT / "shared/sfx/noor/gentle_breeze_mario1298_181252.mp3"
    s_len, f_len = fade_start + 1.0, END - music_back
    s_gain = -38.0 - lufs(soar, 20, s_len)
    f_gain = -38.0 - lufs(flute, 120, max(f_len, 5))
    b_gain = -46.0 - lufs(breeze, 5, END)
    fmt = "aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo"
    nv = len(clips)  # audio inputs come after the video clips: voice, Soaring, River Flute, breeze
    afc = [f"[{nv}]{fmt},volume={v_gain:.2f}dB,aecho=0.8:0.7:40|75:0.10|0.06,asplit=2[v][vk]",
           f"[{nv + 1}]{fmt},volume={s_gain:.2f}dB,afade=t=in:d=1.5,afade=t=out:st={fade_start:.2f}:d=1,apad=whole_dur={END:.2f}[ms]",
           f"[{nv + 2}]{fmt},volume={f_gain:.2f}dB,afade=t=in:d=2.5,adelay={int(music_back * 1000)}:all=1,"
           f"afade=t=out:st={END - 1.5:.2f}:d=1.5,apad=whole_dur={END:.2f}[mf]",
           "[ms][mf]amix=inputs=2:normalize=0[m0]",
           "[m0][vk]sidechaincompress=threshold=0.03:ratio=3:attack=20:release=400[m]",
           f"[{nv + 3}]{fmt},volume={b_gain:.2f}dB,afade=t=in:d=0.8,apad=whole_dur={END:.2f}[b]",
           f"[v][m][b]amix=inputs=3:normalize=0,atrim=0:{END:.2f},afade=t=out:st={END - 1.2:.2f}:d=1.2,alimiter=limit=0.89[aout]"]
    out = OUT / "sync_sample.mp4"
    run(inputs + ["-i", str(voice), "-ss", "20", "-t", f"{s_len:.2f}", "-i", str(soar),
                  "-ss", "120", "-t", f"{f_len:.2f}", "-i", str(flute), "-ss", "5", "-t", f"{END:.2f}", "-i", str(breeze),
                  "-filter_complex", ";".join(fc + afc), "-map", "[vout]", "-map", "[aout]", "-t", f"{END:.2f}",
                  "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", str(out)])
    for p in OUT.glob("_shot*.mp4"):
        p.unlink()
    print(f"OK {out.relative_to(ROOT).as_posix()}  {END:.1f}s  total {lufs(out):.1f} LUFS")
    print(story_budget.summary_line(BUDGET))


if __name__ == "__main__":
    main()
