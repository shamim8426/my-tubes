"""Add (or change) the music bed of an already rendered deck video WITHOUT re-rendering the picture (video stream is copied).

    .venv\\Scripts\\python -X utf8 scripts\\remux_music.py <story_dir> <music.mp3> [--start 6] [--rel 12] [--out short_music.mp4]

Uses <story_dir>/build/voice.wav + the swoosh cue times stored in build/deck.html, and <story_dir>/output/short.mp4 as the picture."""
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import html_video as HV  # noqa: E402


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    story, music = Path(sys.argv[1]).resolve(), str(Path(sys.argv[2]).resolve())
    start, rel, out_name = float(arg("--start", 0)), float(arg("--rel", 12)), arg("--out", "short_music.mp4")
    html = (story / "build" / "deck.html").read_text(encoding="utf-8")
    sfx = json.loads(re.search(r'"sfx":\s*(\[[^\]]*\])', html).group(1))
    voice = story / "build" / "voice.wav"
    with wave.open(str(voice)) as w:
        total = w.getnframes() / w.getframerate() + 0.3
    audio = story / "output" / "_music_mix.wav"
    HV.build_audio(str(voice), sfx, 0.0, total, audio, music=music, music_start=start, music_rel=rel)
    out = story / "output" / out_name
    subprocess.run([HV.FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(story / "output" / "short.mp4"), "-i", str(audio),
                    "-map", "0:v", "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "224k", "-shortest", "-movflags", "+faststart", str(out)], check=True)
    audio.unlink()
    print("OK", out)


if __name__ == "__main__":
    main()
