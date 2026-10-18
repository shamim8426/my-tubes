"""Reference sheets for long-video characters/props (style matched to the approved channel sheets).

Usage: python scripts/gen_long_characters.py long_01 [name ...]
Output: the story's characters/ folder (STORY_DIRS below)
"""
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gemini_image import generate  # noqa: E402

from paths import ROOT, channel_dir  # noqa: E402

CHAR = channel_dir() / "characters"
STYLE_REFS = [CHAR / "dadi_sheet.png", CHAR / "golu_sheet.png"]
STORY_DIRS = {"long_01": channel_dir() / "stories" / "001_lalchi-halwai"}
STYLE_NOTE = ("The attached images are STYLE references only (the channel's approved sheets): match their flat 2D "
              "cartoon style, thick bold black outlines, warm colours, flat cel shading, clean off-white background and "
              "sheet layout with small uppercase labels. Do NOT draw the grandmother or the boy from them.")

SHEET = ("Character reference sheet of ONE single character on a plain off-white background. Top row: three full-body "
         "poses (labelled). Bottom row: three head-and-shoulders expressions (labelled). The character must look "
         "identical in every pose: same face, body, outfit and colours. No other characters, no scenery.")

SPECS = {
    "long_01": {
        "ghasita": ("ghasita_sheet.png", f"""{SHEET}
Character: Ghasita, a greedy Indian sweet-shop owner (halwai) in his 50s. Very fat with a big round belly showing
through a loose cream kurta, white dhoti, a cloth money pouch tied at his waist. SHINY BALD head with curly black-grey
hair only on the sides, a thick HANDLEBAR moustache curled upwards at the ends in salt-and-pepper grey (must look very
different from a police inspector's straight black moustache), half-closed greedy eyes, small sly mouth.
Poses: LEANING ON SHOP COUNTER (greedy, holding a small brass weighing scale); SITTING COUNTING COINS (laughing);
DISMISSIVE HAND WAVE (sneering, shooing someone away).
Expressions: GREEDY GRIN, SNEERING, SHOCKED (eyes wide, mouth open)."""),
        "chhotu": ("chhotu_sheet.png", f"""{SHEET}
Character: Chhotu, a kind young Indian helper in his early 20s. Thin, honest open face, gentle big eyes, short neat
black hair, clean-shaven. Simple, clean but worn light-blue kurta with a small patch on the sleeve, off-white dhoti,
barefoot. No accessories.
Poses: STIRRING JALEBI in a big pan with a ladle; GIVING A ROTI with both hands (compassionate, slightly bending down);
HOLDING A SMALL GLOWING BRASS CAULDRON in both hands (wonder).
Expressions: KIND SMILE, CARING, AMAZED."""),
        "sadhu": ("sadhu_sheet.png", f"""{SHEET}
Character: Sadhu Baba, a very old, thin Indian holy man in his 70s. Long flowing white beard and white hair tied in a
small top knot, deep wrinkles, peaceful kind eyes, chandan tilak on forehead, rudraksha bead mala. Simple saffron
(kesari) dhoti and a saffron cloth over one shoulder, a wooden walking stick (lathi) and a cloth jholi bag on his shoulder.
Poses: SITTING UNDER A TREE (tired, hungry, cross-legged, only the tree trunk suggested); EATING A ROTI (grateful);
BLESSING (one palm raised, handing over a small brass cauldron with the other hand).
Expressions: TIRED, GRATEFUL, WISE SMILE."""),
        "kadhai": ("cadhai_prop.png", """Prop reference sheet on a plain off-white background, flat 2D cartoon with thick
bold outlines. Object: a small magical Indian brass kadhai (wok-shaped cauldron) that fits in two hands, golden-bronze
colour, two simple round handles, a band of traditional desi motifs (paisley and dots) engraved around the rim.
Show it labelled from: SIDE VIEW, TOP VIEW (looking inside, empty), THREE-QUARTER VIEW, and MAGIC GLOW (same kadhai
with a soft warm golden glow and a few sparkles). Same object identical in every view. No people, no other objects."""),
    },
}

if __name__ == "__main__":
    vid = sys.argv[1]
    names = sys.argv[2:] or list(SPECS[vid])
    out_dir = STORY_DIRS[vid] / "characters"
    for name in names:
        fname, prompt = SPECS[vid][name]
        t0 = time.time()
        out = generate(f"{prompt}\n\n{STYLE_NOTE}", out_dir / fname, refs=STYLE_REFS, aspect_ratio="3:2", size="1K")
        print(f"saved {out}  ({time.time() - t0:.0f}s)", flush=True)
