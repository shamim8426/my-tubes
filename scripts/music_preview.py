"""Make short listening previews: the video's own voice-over with each candidate music bed under it (same mixer as the render).

    .venv\\Scripts\\python -X utf8 scripts\\music_preview.py <story_dir> <music.mp3> [<music.mp3> ...] [--start 8] [--secs 32] [--rel 14]

Needs <story_dir>/build/voice.wav (made by build_deck.py --render). Output: <story_dir>/music_previews/<track>.mp3."""
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import html_video as HV  # noqa: E402


def arg(name, default):
    return float(sys.argv[sys.argv.index(name) + 1]) if name in sys.argv else default


def main():
    story = Path(sys.argv[1]).resolve()
    tracks = [a for a in sys.argv[2:] if a.lower().endswith(".mp3")]
    start, secs, rel = arg("--start", 0.0), arg("--secs", 32.0), arg("--rel", 14.0)
    out_dir = story / "music_previews"
    out_dir.mkdir(exist_ok=True)
    voice = story / "build" / "voice.wav"
    for tr in tracks:
        wav = out_dir / (Path(tr).stem + ".wav")
        HV.build_audio(str(voice), [], 0.0, secs, wav, music=str(Path(tr).resolve()), music_start=start, music_rel=rel)
        mp3 = wav.with_suffix(".mp3")
        subprocess.run([HV.FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(wav), "-b:a", "192k", str(mp3)], check=True)
        wav.unlink()
        print("preview ->", mp3)


if __name__ == "__main__":
    main()
