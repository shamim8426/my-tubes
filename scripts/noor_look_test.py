"""Noor-e-Raah look test (user 2026-10-24): one scene in 3 styles, 16:9, 1K, then an Arabic + Hindi font overlay.
Paid images (budget "noor_samples", ₹45 incl. GST, checked before every call). Output: channels/noor-e-raah/samples/look_test/

    .venv\\Scripts\\python -X utf8 scripts\\noor_look_test.py
"""
import shutil
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))
import gemini_image  # noqa: E402
import pricing  # noqa: E402
import story_budget  # noqa: E402
from name_guard import find_names  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "channels" / "noor-e-raah" / "samples" / "look_test"
FF = next((str(p) for p in (ROOT / "tools/ffmpeg/bin/ffmpeg.exe", ROOT / "tools/ffmpeg/ffmpeg.exe") if p.exists()),
          None) or shutil.which("ffmpeg")  # Linux / cloud: ffmpeg on PATH
NO = "no people, no human figures, no animals, no faces, no silhouettes of people, no text, no letters, no calligraphy, no logos, no watermark"
SCENE = ("A quiet desert night among the hills of 7th-century Arabia: a narrow sandy path winding between dark rocky hills, "
         "a few small clay oil lamps placed along the path glowing warm orange, a sky full of bright stars and the faint "
         "Milky Way, a few date palms far away, tiny flat-roofed mud-brick houses in the distance. Completely empty and "
         "peaceful. Wide 16:9 landscape; keep the upper-middle sky calm and uncluttered for on-screen text.")
STYLES = {
    "a_cinematic_painted": "cinematic digital painting, rich painterly brushwork, soft volumetric light, deep indigo night "
                           "sky, warm lantern glow, wide cinematic composition, high detail, " + NO,
    "b_soft_watercolor": "soft watercolor illustration on textured paper, gentle transparent washes and soft bleeding "
                         "edges, muted indigo, sand and warm amber palette, calm and airy, " + NO,
    "c_semi_realistic_matte": "semi-realistic matte painting, natural colours, realistic night lighting with a slightly "
                              "painted finish, subtle film grain, calm atmosphere, " + NO,
}
ARABIC = "بِسْمِ ٱللَّهِ ٱلرَّحْمَٰنِ ٱلرَّحِيمِ"  # Tanzil Uthmani 1:1, unchanged
HINDI = "सरल भावार्थ — माने हुए तर्जुमों के आधार पर"


def overlay(img: Path, out: Path):
    """Arabic (Amiri) centred in the upper half + small Hindi label (Mukta), on a soft dark band."""
    ar, hi = OUT / "_arabic.txt", OUT / "_hindi.txt"
    ar.write_text(ARABIC, encoding="utf-8")
    hi.write_text(HINDI, encoding="utf-8")
    font_ar = (ROOT / "shared/fonts/Amiri-Regular.ttf").as_posix().replace(":", "\\:")
    font_hi = (ROOT / "shared/fonts/Mukta-Bold.ttf").as_posix().replace(":", "\\:")
    p = lambda f: f.as_posix().replace(":", "\\:")  # noqa: E731
    vf = ("scale=1920:1080:force_original_aspect_ratio=increase,crop=1920:1080,"
          "drawbox=x=0:y=ih*0.20:w=iw:h=ih*0.30:color=black@0.28:t=fill,"
          f"drawtext=fontfile='{font_ar}':textfile='{p(ar)}':text_shaping=1:fontsize=96:fontcolor=white:"
          "x=(w-text_w)/2:y=h*0.25:shadowcolor=black@0.6:shadowx=2:shadowy=2,"
          f"drawtext=fontfile='{font_hi}':textfile='{p(hi)}':fontsize=34:fontcolor=white@0.92:"
          "x=(w-text_w)/2:y=h*0.42:shadowcolor=black@0.6:shadowx=2:shadowy=2")
    subprocess.run([FF, "-hide_banner", "-loglevel", "error", "-y", "-i", str(img), "-vf", vf, "-q:v", "3", str(out)],
                   check=True)


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, style in STYLES.items():
        img = OUT / f"{name}.png"
        if not img.exists():
            if find_names(SCENE + " " + style):
                sys.exit(f"BLOCK (RULES 12a): name in prompt {name}")
            est = pricing.image_estimate_usd(gemini_image.MODEL, "1K", len(SCENE) + len(style), 0) * pricing.usd_to_inr()
            story_budget.check("noor_samples", est)
            gemini_image.generate(SCENE, img, aspect_ratio="16:9", size="1K", style=style)
        overlay(img, OUT / f"{name}_overlay.jpg")
        print("overlay:", (OUT / f"{name}_overlay.jpg").relative_to(ROOT).as_posix())
    print(story_budget.summary_line("noor_samples"))


if __name__ == "__main__":
    main()
