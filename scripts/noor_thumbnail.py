"""Noor-e-Raah long thumbnail (₹0): one of the story's own images + Arabic surah name (Amiri) + a short Hindi line
(libass, so the nuqta stays). 1280x720 JPG <= 2 MB; bottom-right corner kept clear (YouTube time stamp).

    .venv\\Scripts\\python -X utf8 scripts\\noor_thumbnail.py <story> <image id> "<arabic>" "<hindi line>" ["<small line>"]
"""
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FF = next(str(p) for p in (ROOT / "tools/ffmpeg/bin/ffmpeg.exe", ROOT / "tools/ffmpeg/ffmpeg.exe") if p.exists())


def esc(p: Path) -> str:
    return Path(p).resolve().as_posix().replace(":", "\\:")


def main():
    story = (ROOT / sys.argv[1]).resolve()
    sys.path.insert(0, str(ROOT / "scripts"))
    from paths import learnings_brief
    print("learnings.md (Nigraan) LAGU KARO:\n  " + (learnings_brief(story.parents[1].name).replace("\n", "\n  ") or "-"))
    img = story / "images" / f"{sys.argv[2]}.png"
    arabic, hindi = sys.argv[3], sys.argv[4]
    small = sys.argv[5] if len(sys.argv) > 5 else ""
    out_dir = story / "long/output"
    ar = out_dir / "_thumb_ar.txt"
    ar.write_text(arabic, encoding="utf-8")
    ass = out_dir / "_thumb.ass"
    ass.write_text(
        "[Script Info]\nScriptType: v4.00+\nPlayResX: 1280\nPlayResY: 720\nScaledBorderAndShadow: yes\n\n[V4+ Styles]\n"
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, "
        "Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, "
        "MarginV, Encoding\n"
        "Style: Big,Mukta ExtraBold,124,&H00FFFFFF,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,0,0,1,7,4,7,0,0,0,1\n"
        "Style: Small,Mukta Bold,50,&H005AC8F5,&H00FFFFFF,&H00101010,&H90000000,0,0,0,0,100,100,0,0,1,4,2,7,0,0,0,1\n"
        # Arabic through libass (drawtext put the harakat off their letters, Munshi final R1); 4.35 = Amiri ASS scale
        "Style: Ar,Amiri,260,&H00B8E3F3,&H00FFFFFF,&H00101010,&H99000000,0,0,0,0,100,100,0,0,1,0,4,7,0,0,0,0\n\n"
        "[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n"
        f"Dialogue: 0,0:00:00.00,0:00:05.00,Ar,,0,0,0,,{{\\pos(56,-30)}}{arabic}\n"
        f"Dialogue: 0,0:00:00.00,0:00:05.00,Big,,0,0,0,,{{\\pos(56,262)}}{hindi}\n"
        + (f"Dialogue: 0,0:00:00.00,0:00:05.00,Small,,0,0,0,,{{\\pos(62,200)}}{small}\n" if small else ""),
        encoding="utf-8")
    # soft darkening top-left (not a hard box), fading out by 70 % width and towards the bottom
    import cv2
    import numpy as np
    bg = cv2.imread(str(img))
    ih, iw = bg.shape[:2]
    s = max(1280 / iw, 720 / ih)
    bg = cv2.resize(bg, (round(iw * s), round(ih * s)), interpolation=cv2.INTER_LANCZOS4)
    y0, x0 = (bg.shape[0] - 720) // 2, (bg.shape[1] - 1280) // 2
    bg = bg[y0:y0 + 720, x0:x0 + 1280].astype(np.float32)
    gx = np.clip(1 - np.arange(1280) / (1280 * 0.7), 0, 1)
    gy = np.clip(1 - (np.arange(720) - 430) / 140, 0, 1)
    bg *= (1 - 0.62 * np.outer(gy, gx))[:, :, None]
    base = out_dir / "_thumb_bg.png"
    cv2.imwrite(str(base), bg.astype(np.uint8))
    img = base
    vf = f"scale=1280:720,subtitles=filename='{esc(ass)}':fontsdir='{esc(ROOT / 'shared/fonts')}'"
    out = out_dir / f"{story.name}_thumbnail.jpg"
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(img), "-vf", vf, "-frames:v", "1",
                    "-q:v", "3", str(out)], check=True)
    print(out.relative_to(ROOT).as_posix(), f"{out.stat().st_size / 1024:.0f} KB")


if __name__ == "__main__":
    main()
