"""Noor-e-Raah 30 s SYNC SAMPLE (user 2026-10-24), style a (cinematic painted): real script lines (parichay 5-7 +
ayah 1 lines 30, 32), 3 new images + the look-test image a + 1 calligraphy title card (font), Ken Burns shots, music and
ambience cues, music fade-out 1 s before the Arabic ayah, River Flute back after it. Paid key allowed (free first);
budget "noor_samples" (₹45 incl. GST) checked before every paid call.

    .venv\\Scripts\\python -X utf8 scripts\\noor_sync_sample.py
"""
import json
import re
import unicodedata
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
OUT = ROOT / "channels/noor-e-raah/samples/sync_sample"
LOOK_A = ROOT / "channels/noor-e-raah/samples/look_test/a_cinematic_painted.png"
FF = next(str(p) for p in (ROOT / "tools/ffmpeg/bin/ffmpeg.exe", ROOT / "tools/ffmpeg/ffmpeg.exe") if p.exists())
FONT_AR = ROOT / "shared/fonts/Amiri-Regular.ttf"
FONT_HI = ROOT / "shared/fonts/Mukta-Bold.ttf"
VOICES = json.loads((ROOT / "channels/noor-e-raah/channel.json").read_text(encoding="utf-8"))["voices"]
STYLE = STYLES["a_cinematic_painted"]
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


def hindi(text: str) -> str:
    """Screen text only: precomposed nuqta letters (क़ U+0958 ...) -> letter + ़, because Mukta drops the dot on the
    precomposed form. Never applied to Arabic (Tanzil text stays byte-for-byte)."""
    return unicodedata.normalize("NFD", text)


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
        img = OUT / "images" / f"{name}.png"
        if img.exists():
            continue
        if find_names(scene + " " + STYLE):
            sys.exit(f"BLOCK (RULES 12a): name in prompt {name}")
        est = pricing.image_estimate_usd(gemini_image.MODEL, "1K", len(scene) + len(STYLE), 0) * pricing.usd_to_inr()
        story_budget.check("noor_samples", est)
        gemini_image.generate(scene, img, aspect_ratio="16:9", size="1K", style=STYLE)


def voices():
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8", download_root=str(ROOT / "tools/whisper-models"))
    (OUT / "lines").mkdir(parents=True, exist_ok=True)
    files = []
    for n, who, text in LINES:
        f = OUT / "lines" / f"{n:03d}_{who}.wav"
        v = VOICES[who]
        for attempt in range(3):  # first take + max 2 retries (RULES 1b)
            if not f.exists():
                story_budget.check("noor_samples", pricing.tts_estimate_usd(gemini_tts.MODEL, len(text) + len(v["style"]),
                                                                            len(text) / 8) * pricing.usd_to_inr())
                gemini_tts.speak(text, v["voice"], v["style"], f)
            with wave.open(str(f)) as w:
                sr = w.getframerate()
                x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
            x16 = np.interp(np.arange(0, len(x), sr / 16000), np.arange(len(x)), x).astype(np.float32)
            heard = " ".join(s.text.strip() for s in model.transcribe(x16, language="hi", beam_size=5)[0])
            miss = missing(text, heard)
            print(f"line {n} {who}: missing={miss} | {heard}")
            if not miss or attempt == 2:
                break
            f.unlink()
        files.append(f)
    return files


def title_card(path: Path):
    """Calligraphy title card made with fonts only (no AI text)."""
    t = {k: OUT / f"_{k}.txt" for k in ("ar", "hi", "se")}
    t["ar"].write_text(TITLE_AR, encoding="utf-8"); t["hi"].write_text(hindi(TITLE_HI), encoding="utf-8")  # noqa: E702
    t["se"].write_text(hindi(SERIES), encoding="utf-8")
    vf = ("drawbox=x=iw*0.18:y=ih*0.18:w=iw*0.64:h=ih*0.64:color=0xC9A55A@0.55:t=3,"
          "drawbox=x=iw*0.19:y=ih*0.195:w=iw*0.62:h=ih*0.61:color=0xC9A55A@0.25:t=1,"
          f"drawtext=fontfile='{esc(FONT_AR)}':textfile='{esc(t['ar'])}':text_shaping=1:fontsize=150:fontcolor=0xF3E3B8:"
          "x=(w-text_w)/2:y=h*0.30,"
          f"drawtext=fontfile='{esc(FONT_HI)}':textfile='{esc(t['hi'])}':fontsize=60:fontcolor=white:x=(w-text_w)/2:y=h*0.56,"
          f"drawtext=fontfile='{esc(FONT_HI)}':textfile='{esc(t['se'])}':fontsize=34:fontcolor=0xC9A55A:x=(w-text_w)/2:y=h*0.67")
    run(["-f", "lavfi", "-i", "gradients=s=1920x1080:c0=0x0B1426:c1=0x1C2A44:x0=0:y0=0:x1=1920:y1=1080:d=1", "-frames:v", "1",
         "-vf", vf, str(path)])


def shot(img: Path, dur: float, out: Path, zoom_in=True):
    frames = max(int(round(dur * FPS)), 1)
    z = f"min(1+{0.06 / frames:.6f}*on,1.06)" if zoom_in else f"max(1.06-{0.06 / frames:.6f}*on,1.0)"
    run(["-loop", "1", "-i", str(img), "-vf",
         f"scale=3840:2160:force_original_aspect_ratio=increase,crop=3840:2160,"
         f"zoompan=z='{z}':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={frames}:s=1920x1080:fps={FPS},format=yuv420p",
         "-frames:v", str(frames), "-c:v", "libx264", "-preset", "veryfast", "-crf", "18", str(out)])


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
    seq = [(card, 0.0), (LOOK_A, T_CARD), (OUT / "images/dawn_valley.png", starts[1] - 0.3),
           (OUT / "images/green_after_rain.png", fade_start), (OUT / "images/open_door_sunrise.png", arabic_off)]
    clips = []
    for i, (img, s) in enumerate(seq):
        nxt = seq[i + 1][1] if i + 1 < len(seq) else END
        dur = nxt - s + (XF if i + 1 < len(seq) else 0)
        c = OUT / f"_shot{i}.mp4"
        shot(img, dur, c, zoom_in=i % 2 == 0)
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
    tx = {}
    def tfile(key, text):  # noqa: E306
        p = OUT / f"_t_{key}.txt"; p.write_text(hindi(text) if key != "ar" else text, encoding="utf-8"); tx[key] = p  # noqa: E702
    tfile("ar", ARABIC); tfile("label", LABEL)  # noqa: E702
    for i, (n, _, text) in enumerate(LINES):
        tfile(f"l{n}", text)
    for i, c in enumerate(CARDS):
        tfile(f"c{i}", c)
    ov = []
    a_alpha = (f"if(lt(t,{A0:.2f}),0,if(lt(t,{A0 + 0.5:.2f}),(t-{A0:.2f})/0.5,if(lt(t,{arabic_off - 0.5:.2f}),1,"
               f"if(lt(t,{arabic_off:.2f}),({arabic_off:.2f}-t)/0.5,0))))")
    ov.append(f"drawbox=x=0:y=ih*0.20:w=iw:h=ih*0.30:color=black@0.30:t=fill:enable='between(t,{A0:.2f},{arabic_off:.2f})'")
    ov.append(f"drawtext=fontfile='{esc(FONT_AR)}':textfile='{esc(tx['ar'])}':text_shaping=1:fontsize=96:fontcolor=white:"
              f"alpha='{a_alpha}':x=(w-text_w)/2:y=h*0.25:shadowcolor=black@0.6:shadowx=2:shadowy=2")
    ov.append(f"drawtext=fontfile='{esc(FONT_HI)}':textfile='{esc(tx['label'])}':fontsize=32:fontcolor=white@0.92:"
              f"enable='between(t,{starts[3]:.2f},{arabic_off - 0.5:.2f})':x=(w-text_w)/2:y=h*0.42")
    for i, c in enumerate(CARDS):  # info cards during line 7
        t0 = starts[2] + i * 0.7
        ov.append(f"drawtext=fontfile='{esc(FONT_HI)}':textfile='{esc(tx[f'c{i}'])}':fontsize=40:fontcolor=white:"
                  f"box=1:boxcolor=0x0B1426@0.55:boxborderw=14:enable='between(t,{t0:.2f},{starts[2] + lens[2]:.2f})':"
                  f"x=w*0.06:y=h*(0.10+{i}*0.085)")
    for (n, _, _), s, ln in zip(LINES, starts, lens):  # subtitles
        ov.append(f"drawtext=fontfile='{esc(FONT_HI)}':textfile='{esc(tx[f'l{n}'])}':fontsize=40:fontcolor=white:"
                  f"box=1:boxcolor=black@0.45:boxborderw=12:enable='between(t,{s:.2f},{s + ln:.2f})':"
                  f"x=(w-text_w)/2:y=h*0.83")
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
    afc = [f"[5]{fmt},volume={v_gain:.2f}dB,aecho=0.8:0.7:40|75:0.10|0.06,asplit=2[v][vk]",
           f"[6]{fmt},volume={s_gain:.2f}dB,afade=t=in:d=1.5,afade=t=out:st={fade_start:.2f}:d=1,apad=whole_dur={END:.2f}[ms]",
           f"[7]{fmt},volume={f_gain:.2f}dB,afade=t=in:d=2.5,adelay={int(music_back * 1000)}:all=1,"
           f"afade=t=out:st={END - 1.5:.2f}:d=1.5,apad=whole_dur={END:.2f}[mf]",
           "[ms][mf]amix=inputs=2:normalize=0[m0]",
           "[m0][vk]sidechaincompress=threshold=0.03:ratio=3:attack=20:release=400[m]",
           f"[8]{fmt},volume={b_gain:.2f}dB,afade=t=in:d=0.8,apad=whole_dur={END:.2f}[b]",
           f"[v][m][b]amix=inputs=3:normalize=0,atrim=0:{END:.2f},afade=t=out:st={END - 1.2:.2f}:d=1.2,alimiter=limit=0.89[aout]"]
    out = OUT / "sync_sample.mp4"
    run(inputs + ["-i", str(voice), "-ss", "20", "-t", f"{s_len:.2f}", "-i", str(soar),
                  "-ss", "120", "-t", f"{f_len:.2f}", "-i", str(flute), "-ss", "5", "-t", f"{END:.2f}", "-i", str(breeze),
                  "-filter_complex", ";".join(fc + afc), "-map", "[vout]", "-map", "[aout]", "-t", f"{END:.2f}",
                  "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-r", str(FPS), "-c:a", "aac", "-b:a", "192k", str(out)])
    for p in OUT.glob("_shot*.mp4"):
        p.unlink()
    print(f"OK {out.relative_to(ROOT).as_posix()}  {END:.1f}s  total {lufs(out):.1f} LUFS")
    print(story_budget.summary_line("noor_samples"))


if __name__ == "__main__":
    main()
