"""Noor-e-Raah dialogue sample. Free key first; without --paid-ok it stops on 429 (₹0), with --paid-ok the paid key
takes over (budget "noor_samples" checked before each call). Each line: TTS (cached), Whisper completeness check,
max 2 retries. Then mix: lines with 0.6 s gaps, voice -16 LUFS + light warm reverb, River Flute 22 LU below with light
ducking, gentle breeze -46 LUFS. Output: channels/noor-e-raah/music_samples/dialogue_sample.wav

    .venv\\Scripts\\python -X utf8 scripts\\noor_dialogue_sample.py D:/Story-Channel
"""
import json
import re
import shutil
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(sys.argv[1])
sys.path.insert(0, str(ROOT / "scripts"))
import numpy as np  # noqa: E402

import gemini_keys  # noqa: E402
import gemini_tts  # noqa: E402
import pricing  # noqa: E402
import story_budget  # noqa: E402
from noor_audition import missing  # noqa: E402

FF = next((str(p) for p in (ROOT / "tools/ffmpeg/bin/ffmpeg.exe", ROOT / "tools/ffmpeg/ffmpeg.exe") if p.exists()),
          None) or shutil.which("ffmpeg")  # Linux / cloud: ffmpeg on PATH
OUT = ROOT / "channels/noor-e-raah/music_samples"
WORK = OUT / "dialogue_lines"
VOICES = json.loads((ROOT / "channels/noor-e-raah/channel.json").read_text(encoding="utf-8"))["voices"]
LINES = [
    ("sawaal", "उस्ताद जी, हम हर नमाज़ में अल-फ़ातिहा पढ़ते हैं... पर इसका मतलब असल ज़िंदगी में क्या है?"),
    ("ustaad", "बहुत अच्छा सवाल। इसमें बंदा सबसे पहले अपने रब का शुक्र अदा करता है, फिर उससे सीधा रास्ता माँगता है।"),
    ("sawaal", "यानी पहले शुक्रिया, फिर दुआ?"),
    ("ustaad", "बिल्कुल। जैसे हम किसी से कुछ माँगने से पहले उसका एहसान मानते हैं।"),
]
MUSIC = ROOT / "shared/music/noor/River_Flute.mp3"
AMB = ROOT / "shared/sfx/noor/gentle_breeze_mario1298_181252.mp3"
GAP, LEAD, TAIL = 0.6, 1.5, 2.0
PAID_OK = "--paid-ok" in sys.argv

_model = None


def heard_missing(path, text):
    global _model
    if _model is None:
        from faster_whisper import WhisperModel
        _model = WhisperModel("small", device="cpu", compute_type="int8", download_root=str(ROOT / "tools/whisper-models"))
    with wave.open(str(path)) as w:
        sr = w.getframerate()
        x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
    x16 = np.interp(np.arange(0, len(x), sr / 16000), np.arange(len(x)), x).astype(np.float32)
    t = " ".join(s.text.strip() for s in _model.transcribe(x16, language="hi", beam_size=5)[0])
    return t, missing(text, t)


WORK.mkdir(parents=True, exist_ok=True)
files = []
for i, (who, text) in enumerate(LINES, 1):
    f = WORK / f"{i:02d}_{who}.wav"
    v = VOICES[who]
    tries = 0
    while True:
        if not f.exists():
            if PAID_OK:  # worst case the paid key: ~1.2 s per 10 chars
                est = pricing.tts_estimate_usd(gemini_tts.MODEL, len(text) + len(v["style"]), len(text) / 8)                     if hasattr(pricing, "tts_estimate_usd") else 0.002
                story_budget.check("noor_samples", est * pricing.usd_to_inr())
            try:
                gemini_tts.speak(text, v["voice"], v["style"], f, free_only=not PAID_OK)
            except gemini_keys.FreeQuotaOver as e:
                sys.exit(f"STOP at line {i}: {e}")
            tries += 1
        t, miss = heard_missing(f, text)
        print(f"line {i} {who} ({v['voice']}) try {tries}: missing={miss} | {t}")
        if not miss or tries >= 3:  # first take + max 2 retries
            break
        f.unlink()
    files.append(f)


def lufs(path):
    err = subprocess.run([FF, "-hide_banner", "-nostats", "-i", str(path), "-af", "ebur128=framelog=quiet", "-f", "null", "-"],
                         capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", err)[-1])


# voice track: lead silence, lines with gaps, tail
fmt = "aformat=sample_fmts=fltp:sample_rates=48000:channel_layouts=stereo"
parts, inputs = [], []
for k, f in enumerate(files):
    inputs += ["-i", str(f)]
    parts.append(f"[{k}]{fmt},apad=pad_dur={GAP}[p{k}]")
concat = "".join(f"[p{k}]" for k in range(len(files))) + f"concat=n={len(files)}:v=0:a=1[cat]"
voice = WORK / "voice_track.wav"
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *inputs, "-filter_complex",
                ";".join(parts + [concat, f"[cat]adelay={int(LEAD * 1000)}:all=1,apad=pad_dur={TAIL}[o]"]),
                "-map", "[o]", str(voice)], check=True)
with wave.open(str(voice)) as w:
    total = w.getnframes() / w.getframerate()
v_gain = -16.0 - lufs(voice)
m_cut = WORK / "music_cut.wav"
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", "120", "-t", f"{total:.2f}", "-i", str(MUSIC), str(m_cut)], check=True)
a_cut = WORK / "amb_cut.wav"
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-ss", "5", "-t", f"{total:.2f}", "-i", str(AMB), str(a_cut)], check=True)
m_gain, a_gain = -38.0 - lufs(m_cut), -46.0 - lufs(a_cut)
out = OUT / "dialogue_sample.wav"
fc = [f"[0]{fmt},volume={v_gain:.2f}dB,aecho=0.8:0.7:40|75:0.10|0.06,asplit=2[v][vk]",
      f"[1]{fmt},volume={m_gain:.2f}dB,afade=t=in:d=1.5[m0]",
      "[m0][vk]sidechaincompress=threshold=0.03:ratio=3:attack=20:release=400[m]",
      f"[2]{fmt},volume={a_gain:.2f}dB,afade=t=in:d=0.8[a]",
      f"[v][m][a]amix=inputs=3:normalize=0,afade=t=out:st={total - 1.5:.2f}:d=1.5,alimiter=limit=0.89[o]"]
subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(voice), "-i", str(m_cut), "-i", str(a_cut),
                "-filter_complex", ";".join(fc), "-map", "[o]", "-ar", "48000", str(out)], check=True)
print(f"OK {out.relative_to(ROOT).as_posix()}  {total:.1f}s  total {lufs(out):.1f} LUFS")
