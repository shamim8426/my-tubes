"""Noor-e-Raah "Musafir" v3 (user 2026-10-25): plain light earth-tone (beige/khaki) kurta-pajama, shoulder bag, small
plain cap or bare head - NOT a white kurta with a white head cloth. Angle ONLY from directly behind (or at most ~20
degrees off, head turned away): no part of the face ever, no "three-quarter / lost profile". Style V2 cinematic matte.
2 images: character sheet (all views from behind: standing, sitting, dua) + scene 2 (two paths). Scene 2 gets ONLY a
crop of the sheet's standing + dua views as reference (so no other angle is copied). Scene 1 of v2 passed and is kept.
Budget "noor_musafir_v3" ₹12 incl. GST.

    .venv\\Scripts\\python -X utf8 scripts\\noor_musafir_v3.py
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
OUT = ROOT / "channels/noor-e-raah/samples/musafir_v3"
BUDGET = "noor_musafir_v3"
STYLE = ("cinematic matte painting like a film still, painterly and NOT photorealistic, volumetric god rays, shallow "
         "depth of field with a sharp foreground and a softly blurred background, widescreen composition, subtle film "
         "grain, warm golden color grade")
LOOK = ("an ordinary clean-shaven slim young man of about 18-20 with short dark hair, wearing a plain light earth-tone "
        "(beige / khaki) simple kurta-pajama (knee-length plain shirt and loose trousers), a small cloth bag on one "
        "shoulder, a small plain cap or bare head, simple sandals; NOT white clothes, NOT a white head cloth, NOT a robe, "
        "NOT a turban; an everyday traveller, not resembling any specific or famous person")
NOFACE = ("He is seen ONLY from directly behind (at most about 20 degrees off his back) with his head turned away from "
          "the viewer: only the back of his head, his cap or hair and the back of one ear are visible. No part of the face "
          "at all - no nose, no eyelashes, no eyebrow, no lips and no chin extend past the outline of his head or cheek. "
          "Never a three-quarter view, never a side profile, never a profile silhouette. Hands anatomically correct with "
          "five separate fingers, or hidden. No other people. No domes, no minarets, no text, no letters, no logos, no "
          "watermark.")
DUA = ("making dua, seen from directly behind: elbows bent and close to the body, both forearms raised in front of his "
       "chest, hands a little apart at chest height below the chin, palms open and facing upward toward his face, head "
       "clearly bowed forward a little with the back of his neck visible; from behind the hands are mostly hidden by his "
       "shoulders. NOT hands beside the head, NOT above the shoulders, NOT palms facing forward")
SHEET = ("Character sheet of one character, three views side by side on a plain warm neutral background, same clothes "
         f"and proportions in every view: {LOOK}. All views from directly behind: (1) standing, seen from directly "
         f"behind; (2) sitting on a rock, seen from directly behind; (3) {DUA}. {NOFACE} Wide 16:9.")
SCENE2 = (f"The traveller ({LOOK}) stands where a desert path splits into two: one path bright and lit by warm light, the "
          "other dark and fading into shadow; he stands between the two paths, seen from directly behind, slightly off "
          f"to one side, looking toward the two paths; only the back of his head shows. {NOFACE} Keep the traveller "
          "exactly as in the reference (same beige kurta-pajama, bag, cap or hair). Wide 16:9.")


def gen(prompt, out, refs=()):
    if out.exists():
        return
    if find_names(prompt + " " + STYLE):
        sys.exit(f"BLOCK (RULES 12a): a name in the prompt of {out.name}")
    est = pricing.image_estimate_usd(gemini_image.MODEL, "1K", len(prompt) + len(STYLE), len(refs)) * pricing.usd_to_inr()
    story_budget.check(BUDGET, est)
    gemini_image.generate(prompt, out, refs=list(refs), aspect_ratio="16:9", size="1K", style=STYLE)


def label(im, text, w, h):
    im = cv2.resize(im, (w, h))
    cv2.rectangle(im, (0, 0), (w, 40), (0, 0, 0), -1)
    cv2.putText(im, text, (10, 28), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 255), 2)
    return im


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    sheet = OUT / "musafir_v3_sheet.png"
    gen(SHEET, sheet)
    # reference for the scene: only the standing (left third) and the dua (right third) views of the sheet (₹0)
    im = cv2.imread(str(sheet))
    w = im.shape[1]
    ref = OUT / "musafir_v3_ref_back_dua.png"
    cv2.imwrite(str(ref), np.hstack([im[:, : w // 3], im[:, 2 * w // 3:]]))
    gen(SCENE2, OUT / "2_two_paths__V2.png", refs=[ref])
    s1 = ROOT / "channels/noor-e-raah/samples/musafir_v2/1_dua_sunrise__V2.png"
    top = label(cv2.imread(str(sheet)), "Musafir v3 character sheet (all from behind)", 1600, 900)
    row = np.hstack([label(cv2.imread(str(s1)), "1_dua_sunrise | v2 (PASS, kept)", 800, 450),
                     label(cv2.imread(str(OUT / "2_two_paths__V2.png")), "2_two_paths | v3", 800, 450)])
    cv2.imwrite(str(OUT / "compare_musafir_v3.jpg"), np.vstack([top, row]), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print(story_budget.summary_line(BUDGET))


if __name__ == "__main__":
    main()
