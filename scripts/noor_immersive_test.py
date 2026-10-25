"""Noor-e-Raah "immersive" test (user 2026-10-25): style "cinematic watercolor" (style a light/depth + style b
watercolor texture), 4 scenes with the RULES 2a people rules (POV, back/far/silhouette, no facial detail).
Budget "noor_immersive_test" ₹25 incl. GST. Output: channels/noor-e-raah/samples/immersive_test/ + compare sheet.

    .venv\\Scripts\\python -X utf8 scripts\\noor_immersive_test.py
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
OUT = ROOT / "channels/noor-e-raah/samples/immersive_test"
STYLE = ("cinematic watercolor painting: rich transparent watercolor and gouache textures on paper with soft bleeding "
         "edges, combined with cinematic depth, dramatic warm natural light, deep soft shadows and atmospheric "
         "perspective, high detail, calm and reverent mood, no text, no letters, no calligraphy, no logos, no watermark")
FACE = "No visible faces anywhere: no facial features, no eyes, no profile faces."
SCENES = {
    "1_pov_dua_hands": "First-person point of view: the viewer's own two hands raised together in dua, palms open and "
                       "facing up, seen from the viewer's eyes in the lower part of the frame, simple sleeves, in front a "
                       "wide soft sunrise sky over quiet desert hills. " + FACE + " Wide 16:9.",
    "2_pov_lantern_path": "First-person point of view at night: the viewer holds a small old lantern low in front, its "
                          "warm light falling on a rocky stony path just ahead of the viewer's own feet in simple sandals, "
                          "dark hills and stars beyond. " + FACE + " Wide 16:9.",
    "3_traveller_back": "A lone traveller of an old era in simple long clothes and a head cloth, seen only from behind and "
                        "small in the frame, walking across a vast desert toward a soft light on the far horizon, long "
                        "evening shadows. " + FACE + " Wide 16:9.",
    "4_mother_child_far": "An old village of mud-brick houses at golden evening light; far away and small in the frame, a "
                          "mother in modest long clothes and head covering walks hand in hand with a small child, both seen "
                          "from behind, simple shapes. " + FACE + " Wide 16:9.",
}


def main():
    OUT.mkdir(parents=True, exist_ok=True)
    for name, scene in SCENES.items():
        f = OUT / f"{name}.png"
        if f.exists():
            continue
        if find_names(scene + " " + STYLE):
            sys.exit(f"BLOCK (RULES 12a): name in prompt {name}")
        est = pricing.image_estimate_usd(gemini_image.MODEL, "1K", len(scene) + len(STYLE), 0) * pricing.usd_to_inr()
        story_budget.check("noor_immersive_test", est)
        gemini_image.generate(scene, f, aspect_ratio="16:9", size="1K", style=STYLE)
    # compare sheet: row 1 = the 4 new images; row 2 = look test a / b / c (same night-path scene)
    lt = ROOT / "channels/noor-e-raah/samples/look_test"
    rows = [[OUT / f"{n}.png" for n in SCENES],
            [lt / "a_cinematic_painted.png", lt / "b_soft_watercolor.png", lt / "c_semi_realistic_matte.png", None]]
    labels = [list(SCENES), ["a cinematic painted", "b soft watercolor", "c semi-realistic matte", ""]]
    tiles = []
    for row, lab in zip(rows, labels):
        r = []
        for p, t in zip(row, lab):
            im = cv2.resize(cv2.imread(str(p)), (640, 360)) if p else np.zeros((360, 640, 3), np.uint8)
            cv2.putText(im, t, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 255), 2)
            r.append(im)
        tiles.append(np.hstack(r))
    cv2.imwrite(str(OUT / "compare_sheet.jpg"), np.vstack(tiles), [cv2.IMWRITE_JPEG_QUALITY, 88])
    print(story_budget.summary_line("noor_immersive_test"))


if __name__ == "__main__":
    main()
