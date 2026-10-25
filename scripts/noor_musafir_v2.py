"""Noor-e-Raah "Musafir" v2 (user 2026-10-25): young (18-20), clean-shaven, plain kurta-pajama-like clothes, shoulder
bag, simple head cloth or bare head - no big robe, no grand turban (RULES 2a). Munshi R1 fixes in the prompts: face only
as a lost profile (three-quarter from behind; never nose/lips/eyes, never a side profile) and the correct dua posture.
Style V2 cinematic matte only. 3 images: character sheet, scene 1 (dua), scene 2 (two paths); the sheet is the
reference for the scenes. Budget "noor_musafir_v2" ₹20 incl. GST.

    .venv\\Scripts\\python -X utf8 scripts\\noor_musafir_v2.py
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
OUT = ROOT / "channels/noor-e-raah/samples/musafir_v2"
BUDGET = "noor_musafir_v2"
STYLE = ("cinematic matte painting like a film still, painterly and NOT photorealistic, volumetric god rays, shallow "
         "depth of field with a sharp foreground and a softly blurred background, widescreen composition, subtle film "
         "grain, warm golden color grade")
LOOK = ("an ordinary clean-shaven young man of about 18-20 with NO beard, slim, wearing plain light-coloured simple "
        "kurta-pajama-like clothes (a knee-length plain shirt and loose trousers), a small cloth bag on one shoulder, a "
        "simple light cloth loosely on his head, simple sandals; NOT a long robe or cloak, NOT a big turban; an everyday "
        "traveller, not resembling any specific or famous person")
NOFACE = ("His face is never shown: he is seen from the back, or from behind at a three-quarter angle (lost profile) where "
          "only the back of the cheek and the ear show - nose, lips and eyes are turned away and never visible; never a "
          "side profile, never a profile silhouette outline. Hands anatomically correct with five separate fingers, or "
          "hidden. No other people. No domes, no minarets, no text, no letters, no logos, no watermark.")
DUA = ("making dua, seen from directly behind: elbows bent and close to the body, both forearms raised in front of his "
       "chest, hands a little apart at chest height below the chin, palms open and facing upward toward his face, head "
       "slightly bowed; from behind the hands are mostly hidden by his shoulders, only the fingertips may show. NOT hands "
       "beside the head, NOT above the shoulders, NOT palms facing forward, NOT waving")
SHEET = ("Character sheet of one character, four views side by side on a plain warm neutral background, same clothes and "
         f"proportions in every view: {LOOK}. Views: (1) standing, seen from the back; (2) standing, seen from behind at a "
         "three-quarter angle (lost profile, looking away); (3) sitting on a rock, seen from behind at a three-quarter "
         f"angle; (4) {DUA}. {NOFACE} Wide 16:9.")
SCENES = {
    "1_dua_sunrise": f"Wide shot: the traveller ({LOOK}) stands in a quiet morning desert, small in the frame (about one "
                     f"sixth of the image height), {DUA}, facing the rising sun on the horizon. {NOFACE} Wide 16:9.",
    "2_two_paths": f"The traveller ({LOOK}) stands where a desert path splits into two: one path bright and lit by warm "
                   "light, the other dark and fading into shadow; seen from behind at a three-quarter angle (lost "
                   f"profile), looking toward the two paths. {NOFACE} Wide 16:9.",
}
REF_NOTE = "Keep the traveller exactly as in the reference character sheet (same young beardless look, clothes, bag, head cloth)."


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
    sheet = OUT / "musafir_v2_sheet.png"
    gen(SHEET, sheet)
    for name, scene in SCENES.items():
        gen(f"{scene} {REF_NOTE}", OUT / f"{name}__V2.png", refs=[sheet])
    top = label(cv2.imread(str(sheet)), "Musafir v2 character sheet (V2 cinematic matte)", 1600, 900)
    row = np.hstack([label(cv2.imread(str(OUT / f"{n}__V2.png")), f"{n} | V2", 800, 450) for n in SCENES])
    cv2.imwrite(str(OUT / "compare_musafir_v2.jpg"), np.vstack([top, row]), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print(story_budget.summary_line(BUDGET))


if __name__ == "__main__":
    main()
