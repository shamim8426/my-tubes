"""Noor-e-Raah thumbnail v2 (user 2026-10-25): one new style-a image that shows the whole surah in one scene (dark
night turning to a golden dawn = praise and mercy; rising sun on the horizon = the Day; seven lamps = seven ayat / "only
You"; one bright straight path with fading side tracks = the straight path), no people, no text. Then the surah name in
Arabic calligraphy (Amiri via libass, gold with a soft glow) + Hindi (Mukta), and a small gold line. Two layouts.
Paid: 1 image (~₹5), story budget 001_al-fatiha.

    .venv\\Scripts\\python -X utf8 scripts\\noor_thumb_v2.py channels/noor-e-raah/stories/001_al-fatiha
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import cv2  # noqa: E402
import numpy as np  # noqa: E402

import gemini_image  # noqa: E402
import pricing  # noqa: E402
import story_budget  # noqa: E402
from name_guard import find_names  # noqa: E402
from noor_look_test import STYLES  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
FF = next((str(p) for p in (ROOT / "tools/ffmpeg/bin/ffmpeg.exe", ROOT / "tools/ffmpeg/ffmpeg.exe") if p.exists()),
          None) or shutil.which("ffmpeg")  # Linux / cloud: ffmpeg on PATH
SCENE = ("One powerful symbolic landscape: a vast quiet desert where a deep indigo starry night on the left gives way to a "
         "radiant golden dawn on the right; the sun is just rising on the far right horizon, with soft golden god rays "
         "spreading across the sky like mercy; one single bright, perfectly straight path of warm light runs from the "
         "lower right foreground to the rising sun, while a few thin side tracks branch off it and fade away into the "
         "dark sand; seven small old clay oil lamps glow in a row along the bright path. The LEFT 45 percent of the image "
         "is calm dark night sky and soft dunes with no objects, kept empty for large text. Dramatic, reverent, cinematic, "
         "high contrast. Wide 16:9.")
AR, HI, SMALL = "سُورَةُ ٱلْفَاتِحَةِ", "सूरह अल-फ़ातिहा", "7 आयतें • आसान मतलब"


def esc(p: Path) -> str:
    return Path(p).resolve().as_posix().replace(":", "\\:")


def ass(layout: str) -> str:
    head = ("[Script Info]\nScriptType: v4.00+\nPlayResX: 1280\nPlayResY: 720\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n"
            "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
            "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, "
            "MarginR, MarginV, Encoding\n"
            # gold Arabic + a blurred glow copy under it (Amiri: libass draws it ~4.35x smaller than the size number)
            "Style: ArGlow,Amiri,330,&H0032B4F0,&H00FFFFFF,&H0032B4F0,&H00000000,0,0,0,0,100,100,0,0,1,6,0,5,0,0,0,0\n"
            "Style: Ar,Amiri,330,&H0068D8FF,&H00FFFFFF,&H00163A5C,&H99000000,0,0,0,0,100,100,0,0,1,2,5,5,0,0,0,0\n"
            "Style: Hi,Mukta ExtraBold,118,&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,0,0,1,7,5,5,0,0,0,1\n"
            "Style: Sm,Mukta Bold,50,&H0068D8FF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,0,0,1,4,3,5,0,0,0,1\n\n"
            "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
    x = 330 if layout == "A" else 640
    ev = [f"Dialogue: 0,0:00:00.00,0:00:05.00,ArGlow,,0,0,0,,{{\\pos({x},175)\\blur14\\alpha&H70&}}{AR}",
          f"Dialogue: 1,0:00:00.00,0:00:05.00,Ar,,0,0,0,,{{\\pos({x},175)}}{AR}",
          f"Dialogue: 1,0:00:00.00,0:00:05.00,Hi,,0,0,0,,{{\\pos({x},{385 if layout == 'A' else 560})}}{HI}",
          f"Dialogue: 1,0:00:00.00,0:00:05.00,Sm,,0,0,0,,{{\\pos({x},{480 if layout == 'A' else 650})}}{SMALL}"]
    return head + "\n".join(ev) + "\n"


def main():
    story = (ROOT / sys.argv[1]).resolve()
    img = story / "images" / "thumb_v2_surah_scene.png"
    style = STYLES["a_cinematic_painted"]
    if not img.exists():
        if find_names(SCENE + " " + style):
            sys.exit("BLOCK (RULES 12a): a name in the prompt")
        est = pricing.image_estimate_usd(gemini_image.MODEL, "1K", len(SCENE) + len(style), 0) * pricing.usd_to_inr()
        story_budget.check(story.name, est)
        gemini_image.generate(SCENE, img, aspect_ratio="16:9", size="1K", style=style)
    out_dir = story / "long/output"
    bg = cv2.imread(str(img))
    bg = cv2.resize(bg, (1280, 720), interpolation=cv2.INTER_LANCZOS4).astype(np.float32)
    for layout in ("A", "B"):
        b = bg.copy()
        if layout == "A":  # darken the left text area softly
            gx = np.clip(1 - np.arange(1280) / (1280 * 0.62), 0, 1)
            b *= (1 - 0.55 * gx)[None, :, None]
        else:  # darken top and bottom bands for centred text
            gy = np.clip(1 - np.abs(np.arange(720) - 360) / 360, 0, 1)
            b *= (0.55 + 0.45 * gy)[:, None, None]
        base = out_dir / f"_thumbv2_bg_{layout}.png"
        cv2.imwrite(str(base), b.astype(np.uint8))
        a = out_dir / f"_thumbv2_{layout}.ass"
        a.write_text(ass(layout), encoding="utf-8")
        out = out_dir / f"{story.name}_thumbnail_v2{layout}.jpg"
        subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(base), "-vf",
                        f"subtitles=filename='{esc(a)}':fontsdir='{esc(ROOT / 'shared/fonts')}'", "-frames:v", "1",
                        "-q:v", "2", str(out)], check=True)
        print(out.relative_to(ROOT).as_posix(), f"{out.stat().st_size // 1024} KB")
    print(story_budget.summary_line(story.name))


if __name__ == "__main__":
    main()
