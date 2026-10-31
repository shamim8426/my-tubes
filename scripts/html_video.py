"""Render an HTML/SVG slide scene to a video with its voice-over (free: local Chrome via Playwright + ffmpeg).

    .venv\\Scripts\\python -X utf8 scripts\\html_video.py <scene.html> <voice.wav> <out.mp4> [--lead 0.3] [--tail 1.0]

The HTML exposes setT(seconds) and window.SFX = [seconds, ...] (soft swoosh at each). Voice starts `lead` seconds in. Audio: voice +
swoosh, normalised to -14 LUFS (measure, then gain + limiter). Frames: 1080x1920 at 30 fps, one Chrome screenshot per frame.
"""
import re
import subprocess
import sys
import wave
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe") if (ROOT / "tools/ffmpeg/ffmpeg.exe").exists() else "ffmpeg"
SWOOSH = ROOT / "shared/sfx/noor/swoosh_mikesmultimedia_349698.mp3"
FPS = 30
MUSIC_FILE, MUSIC_START, MUSIC_REL = None, 0.0, 14.0


def run(args):
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", *map(str, args)], check=True)


def lufs_of(path, ss=None, t=None):
    args = [FF, "-hide_banner", "-nostats"] + (["-ss", str(ss)] if ss else []) + (["-t", str(t)] if t else []) + \
           ["-i", str(path), "-af", "ebur128=framelog=quiet", "-f", "null", "-"]
    err = subprocess.run(args, capture_output=True, text=True).stderr
    return float(re.findall(r"I:\s+(-?[0-9.]+) LUFS", err)[-1])


def build_audio(voice, sfx, lead, total, out, music=None, music_start=0.0, music_rel=14.0):
    """voice (+ soft swoosh at each cue) (+ music bed that ducks under the voice, `music_rel` LU below it) -> -14 LUFS."""
    n = len(sfx)
    parts, mix_in = [], []
    lead_ms = int(lead * 1000)
    if music:
        parts.append(f"[0:a]adelay={lead_ms}|{lead_ms},asplit=2[v][vk]")
        g = (lufs_of(voice) - music_rel) - lufs_of(music, music_start, 40)
        parts.append(f"[2:a]volume={g:.2f}dB,afade=t=in:d=1.0,afade=t=out:st={max(0.0, total - 1.6):.2f}:d=1.6[m]")
        parts.append("[m][vk]sidechaincompress=threshold=0.02:ratio=6:attack=15:release=350[md]")
        mix_in += ["[v]", "[md]"]
    else:
        parts.append(f"[0:a]adelay={lead_ms}|{lead_ms}[v]")
        mix_in.append("[v]")
    if n:
        parts.append(f"[1:a]asplit={n}" + "".join(f"[s{i}]" for i in range(n)))
        parts += [f"[s{i}]adelay={int(max(0, t - 0.1) * 1000)}|{int(max(0, t - 0.1) * 1000)},volume=0.45[x{i}]" for i, t in enumerate(sfx)]
        parts.append("".join(f"[x{i}]" for i in range(n)) + f"amix=inputs={n}:normalize=0[sfx]")
        mix_in.append("[sfx]")
    parts.append("".join(mix_in) + f"amix=inputs={len(mix_in)}:normalize=0,apad,atrim=0:{total:.2f}[o]")
    raw = str(out) + ".raw.wav"
    inputs = ["-i", voice, "-i", SWOOSH] + (["-ss", str(music_start), "-stream_loop", "-1", "-i", music] if music else [])
    run(inputs + ["-filter_complex", ";".join(parts), "-map", "[o]", "-ar", 48000, raw])
    lufs = lufs_of(raw)
    run(["-i", raw, "-af", f"volume={-14.0 - lufs:.2f}dB,alimiter=limit=0.80:level=false", "-ar", 48000, out])
    Path(raw).unlink()


def main():
    html, voice, out = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve()
    lead = float(sys.argv[sys.argv.index("--lead") + 1]) if "--lead" in sys.argv else 0.3
    tail = float(sys.argv[sys.argv.index("--tail") + 1]) if "--tail" in sys.argv else 1.0
    global MUSIC_FILE, MUSIC_START, MUSIC_REL
    MUSIC_FILE = sys.argv[sys.argv.index("--music") + 1] if "--music" in sys.argv else None
    MUSIC_START = float(sys.argv[sys.argv.index("--music-start") + 1]) if "--music-start" in sys.argv else 0.0
    MUSIC_REL = float(sys.argv[sys.argv.index("--music-rel") + 1]) if "--music-rel" in sys.argv else 14.0
    with wave.open(str(voice)) as w:
        total = lead + w.getnframes() / w.getframerate() + tail
    out.parent.mkdir(parents=True, exist_ok=True)
    n = int(round(total * FPS))
    enc = None
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(html.as_uri())
        pg.evaluate("document.fonts.ready")
        sfx = pg.evaluate("window.SFX || []")
        audio = out.with_suffix(".audio.wav")
        build_audio(voice, sfx, lead, total, audio, music=MUSIC_FILE, music_start=MUSIC_START, music_rel=MUSIC_REL)
        enc = subprocess.Popen([FF, "-v", "error", "-y", "-f", "image2pipe", "-c:v", "mjpeg", "-r", str(FPS), "-i", "-", "-i", str(audio),
                                "-vf", "scale=in_range=full:out_range=tv,format=yuv420p", "-c:v", "libx264", "-preset", "medium", "-crf", "17", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "192k",
                                "-frames:v", str(n), "-movflags", "+faststart", str(out)], stdin=subprocess.PIPE)
        for i in range(n):
            pg.evaluate(f"setT({i / FPS})")
            enc.stdin.write(pg.screenshot(type="jpeg", quality=93))
            if i % 90 == 0:
                print(f"  frame {i}/{n}", flush=True)
        b.close()
    enc.stdin.close()
    if enc.wait():
        sys.exit("ffmpeg failed")
    audio.unlink(missing_ok=True)
    print(f"OK {out}  {total:.1f}s")


if __name__ == "__main__":
    main()
