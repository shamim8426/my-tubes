"""Free fallback narration with Edge TTS (Hindi male Madhur) for a history story dir (script.json -> audio/l<n>.wav, 24 kHz mono).
    .venv\\Scripts\\python -X utf8 scripts\\edge_story_tts.py <story dir>
Used only when Gemini TTS (Charon) is rate-limited; samples / tests. Rs0."""
import asyncio
import json
import subprocess
import sys
from pathlib import Path

import edge_tts

ROOT = Path(__file__).resolve().parent.parent
D = Path(sys.argv[1]).resolve()
cfg = json.loads((D / "script.json").read_text(encoding="utf-8"))
FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe")
(D / "audio").mkdir(exist_ok=True)


async def main():
    for l in cfg["lines"]:
        mp3 = D / f"audio/l{l['n']:02d}.mp3"
        wav = D / f"audio/l{l['n']:02d}.wav"
        await edge_tts.Communicate(l["text"].replace("\n", " "), "hi-IN-MadhurNeural", rate="-4%").save(str(mp3))
        subprocess.run([FF, "-y", "-loglevel", "error", "-i", str(mp3), "-ar", "24000", "-ac", "1", "-sample_fmt", "s16", str(wav)], check=True)
        print(l["n"], "ok", flush=True)


asyncio.run(main())
