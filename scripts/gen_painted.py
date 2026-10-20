"""Kissago Painted style test (style migration, own budget "style_migration" ₹35): painted character sheets for
Dadi, Golu, Mitthu (old sheets as identity reference) and two test scenes.

    python scripts/gen_painted.py sheets [dadi golu mitthu]
    python scripts/gen_painted.py scenes [A B]
Style block: verbatim from channels/<key>/brand/STYLE_PAINTED.md (section 1). No studio/film/artist names anywhere.
Outputs: characters/<name>/sheet_painted.png (old sheets untouched), style_tests/painted/scene_A.png, scene_B.png.
"""
import re
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gemini_image import generate  # noqa: E402
from paths import ROOT, channel_dir  # noqa: E402
from story_budget import check  # noqa: E402

CHAN = channel_dir()
CHAR = CHAN / "characters"
OUT = ROOT / "style_tests" / "painted"
BUDGET = "style_migration"


def style_block() -> str:
    t = (CHAN / "brand" / "STYLE_PAINTED.md").read_text(encoding="utf-8")
    return re.search(r"## 1\..*?```\n(.*?)\n```", t, re.S).group(1).strip()


SHEET = ("Character reference sheet of ONE single character on a plain warm off-white paper background. Top row: three "
         "full-body poses. Bottom row: three head-and-shoulders expressions. The character must look identical in every "
         "pose: same face, body, outfit and colours. No other characters, no scenery, no labels or words. Keep the "
         "character's identity exactly as in the attached old reference sheet (face shape, hair, outfit, colours, "
         "props), only repainted in the new painted look.")
SHEETS = {
    "dadi": ("Dadi (Kamla Devi): kind Indian grandmother about 70, round kind face, white hair in a bun, round golden "
             "spectacles, light green saree with a yellow border, gold bangles, small red bindi, wooden walking stick. "
             "Poses: standing with her stick; sitting on a charpai; walking holding a small brass lantern. Expressions: "
             "warm smile, curious thinking, gentle laugh."),
    "golu": ("Golu: chubby Indian boy about 10, round face, messy black hair, yellow T-shirt, blue half-pants, white "
             "socks, red shoes. Poses: standing excited; pointing forward; sitting cross-legged looking up. Expressions: "
             "excited open-mouth grin, scared wide eyes, sheepish smile."),
    "mitthu": ("Mitthu: a green parrot with a red beak and ONLY a thin red ring around his neck - NO black band, no black stripe or black chin anywhere on the neck or throat (gale me sirf patli laal ring, koi kaali patti nahi); the throat is plain green. He is a bird: wings "
               "and two feet only, NO hands, never holding anything. Poses: perched on a branch; flying with wings "
               "spread; hopping on the ground. Expressions: beak open squawking, curious head tilt, proud puffed "
               "chest."),
}
SCENES = {
    "A": (["dadi", "golu", "mitthu"],
          "16:9 scene, evening (shaam) in Dadi's aangan in Gulmohar Mohalla: a small mud house with a clay-tile roof "
          "and a brown wooden door, a clean swept courtyard with a tulsi pot. Dadi sits on a charpai smiling, Golu sits "
          "close beside her listening, and Mitthu perches on a low branch of a big gulmohar tree full of flame-orange "
          "flowers above them. Low amber sun, long soft shadows, apricot and rose sky with soft clouds, green fields "
          "behind the house. Keep every character exactly as in the attached reference sheets. Mitthu is a bird with "
          "wings and feet only, no hands."),
    "B": (["dadi", "golu", "mitthu"],
          "16:9 scene, night on a flat rooftop (chhat) in Gulmohar Mohalla: Dadi and Golu sit together on a mat, "
          "both looking up and Golu pointing at the stars; Mitthu perches on the low roof wall beside them. A small "
          "brass lantern glows warm orange on the mat. Deep indigo-blue night sky full of softly painted stars, "
          "silver moonlight, neighbouring flat roofs with water tanks and clotheslines in the distance, a gulmohar "
          "tree silhouette. Faces clearly readable. Keep every character exactly as in the attached reference "
          "sheets. Mitthu is a bird with wings and feet only, no hands."),
}
EST_INR = 5.0  # pre-GST estimate per 1K image with references (actual average so far ~₹5)


def sheets(names):
    for n in names:
        out = CHAR / n / "sheet_painted.png"
        check(BUDGET, EST_INR)
        t0 = time.time()
        generate(f"{SHEET}\n\n{SHEETS[n]}", out, refs=[CHAR / f"{n}_sheet.png"], aspect_ratio="3:2", size="1K",
                 style=style_block())
        print(f"saved {out} ({time.time() - t0:.0f}s)", flush=True)


def scenes(ids):
    for i in ids:
        who, prompt = SCENES[i]
        out = OUT / f"scene_{i}.png"
        check(BUDGET, EST_INR)
        t0 = time.time()
        generate(prompt, out, refs=[CHAR / w / "sheet_painted.png" for w in who], aspect_ratio="16:9", size="1K",
                 style=style_block())
        print(f"saved {out} ({time.time() - t0:.0f}s)", flush=True)


if __name__ == "__main__":
    cmd, rest = sys.argv[1], sys.argv[2:]
    {"sheets": lambda: sheets(rest or list(SHEETS)), "scenes": lambda: scenes(rest or list(SCENES))}[cmd]()
