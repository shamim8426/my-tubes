"""Noor-e-Raah "Musafir" + cinematic test (user 2026-10-25): the permanent character "Musafir" (RULES 2a) - one
character sheet (no facial detail), then 3 scenes x 2 styles (V1 cinematic painted, V2 cinematic matte painting) with
the sheet as reference. Budget "noor_musafir_test" ₹40 incl. GST; name_guard on every prompt.
Output: channels/noor-e-raah/samples/musafir_test/ + compare_musafir.jpg (sheet + 2 x 3 grid with names).

    .venv\\Scripts\\python -X utf8 scripts\\noor_musafir_test.py
"""
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

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "channels/noor-e-raah/samples/musafir_test"
BUDGET = "noor_musafir_test"
LOOK = ("an ordinary young man of an old era (not resembling any specific or famous person): plain light-coloured long "
        "robe and a light outer cloth, a small cloth bag on one shoulder, a plain light head cloth wrapped as a simple "
        "turban, simple leather sandals")
NOFACE = ("His FACE is NEVER shown clearly: seen only from the back, or from the side in deep shadow / silhouette, or hidden "
          "in the shade of the head cloth - no eyes, no nose, no mouth, no facial detail at all. Hands anatomically correct "
          "with exactly five fingers. No other people. No domes, no minarets, no text, no letters, no logos, no watermark.")
SHEET = ("Character sheet of one character, four views side by side on a plain warm neutral background, same clothes and "
         f"proportions in every view: {LOOK}. Views: (1) standing, seen from the back; (2) standing, side view in deep "
         "shadow so the face is a dark silhouette; (3) sitting on a rock, seen from behind at three-quarter angle; (4) "
         f"standing with both hands raised in dua, seen from the back. {NOFACE} Wide 16:9.")
SCENES = {
    "1_dua_sunrise": f"The traveller ({LOOK}) stands in a morning desert, seen from the back, both hands raised in dua, "
                     f"facing the rising sun on the horizon, long soft shadow behind him. {NOFACE} Wide 16:9.",
    "2_two_paths": f"The traveller ({LOOK}) stands where a path splits into two: one path bright and lit by warm light, the "
                   f"other dark and fading into shadow; seen from the side with his face in deep shadow. {NOFACE} Wide 16:9.",
    "3_night_stars": f"At night the traveller ({LOOK}) sits on a rock looking up at a sky full of stars, seen three-quarters "
                     f"from behind, an old-style small clay oil lamp glowing beside him. {NOFACE} Wide 16:9.",
}
STYLES = {
    "V1_cinematic_painted": "cinematic oil and gouache painting, rich visible brushwork, deep dramatic light and shadow, "
                            "film-like lighting with a strong key light and soft fill, warm highlights and cool shadows",
    "V2_cinematic_matte": "cinematic matte painting like a film still, painterly and NOT photorealistic, volumetric god "
                          "rays, shallow depth of field with a sharp foreground and a softly blurred background, widescreen "
                          "composition, subtle film grain, warm golden color grade",
}
REF_NOTE = "Keep the traveller exactly as in the reference character sheet (same clothes, bag, head cloth, proportions)."


def gen(prompt, style, out, refs=()):
    if out.exists():
        return
    if find_names(prompt + " " + style):
        sys.exit(f"BLOCK (RULES 12a): a name in the prompt of {out.name}")
    est = pricing.image_estimate_usd(gemini_image.MODEL, "1K", len(prompt) + len(style), len(refs)) * pricing.usd_to_inr()
    story_budget.check(BUDGET, est)
    gemini_image.generate(prompt, out, refs=list(refs), aspect_ratio="16:9", size="1K", style=style)


def label(im, text, w, h):
    im = cv2.resize(im, (w, h))
    cv2.rectangle(im, (0, 0), (w, 40), (0, 0, 0), -1)
    cv2.putText(im, text, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = OUT / "musafir_sheet.png"
    gen(SHEET, STYLES["V1_cinematic_painted"], sheet)
    for sname, scene in SCENES.items():
        for vname, style in STYLES.items():
            gen(f"{scene} {REF_NOTE}", style, OUT / f"{sname}__{vname}.png", refs=[sheet])
    grid = [np.hstack([label(cv2.imread(str(OUT / f"{s}__{v}.png")), f"{s} | {v}", 800, 450) for s in SCENES])
            for v in STYLES]
    top = label(cv2.imread(str(sheet)), "Musafir character sheet (V1 cinematic painted)", 2400, 1350)
    cv2.imwrite(str(OUT / "compare_musafir.jpg"), np.vstack([top] + grid), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print(story_budget.summary_line(BUDGET))


if __name__ == "__main__":
    main()
