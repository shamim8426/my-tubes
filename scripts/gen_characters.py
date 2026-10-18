"""Reference sheets for the 4 permanent characters (channel_bible.md section 2).

Usage:  python scripts/gen_characters.py dadi
        python scripts/gen_characters.py golu mitthu pandey   (uses approved dadi sheet as style ref)
"""
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gemini_image import generate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "characters"
DADI_REF = OUT / "dadi_sheet.png"

SHEET = ("Character reference sheet of ONE single character on a plain off-white background. "
         "Top row: full-body FRONT view and full-body SIDE view (profile), same outfit and proportions. "
         "Bottom row: three head-and-shoulders close-ups with expressions labelled in small text: "
         "SMILING, THINKING, SURPRISED. The character must look identical in every pose. "
         "No other characters, no scenery.")

CHARACTERS = {
    "dadi": "Dadi (Kamla Devi), an Indian grandmother about 70 years old: round face, white hair tied in a neat bun, "
            "round golden-rimmed spectacles, light green saree with a yellow border, wooden walking stick, "
            "small red bindi on forehead. Calm, sharp-eyed, gently witty expression.",
    "golu": "Golu, a chubby Indian boy about 10 years old: round face, messy black hair, yellow T-shirt, "
            "blue half-pants, red shoes. Energetic, over-eager.",
    "mitthu": "Mitthu, a green parrot with a red beak, cute and expressive.",
    "pandey": "Inspector Pandey, an Indian police inspector about 45 years old: fat, khaki police uniform with belt and cap, "
              "thick bushy black moustache. Self-important but good-natured.",
}

if __name__ == "__main__":
    for name in sys.argv[1:] or ["dadi"]:
        refs = []
        prompt = f"{SHEET}\n\nCharacter: {CHARACTERS[name]}"
        if name != "dadi":
            refs = [DADI_REF]
            prompt += ("\n\nThe attached image is the APPROVED style reference (Dadi). Match its art style, "
                       "outline thickness, colour palette and sheet layout exactly, but draw the new character, not Dadi.")
        out = generate(prompt, OUT / f"{name}_sheet.png", refs=refs, aspect_ratio="3:2", size="1K")
        print("saved", out)
