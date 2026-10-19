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
STORY_DIRS = {"long_01": channel_dir() / "stories" / "001_lalchi-halwai",
              "long_02": channel_dir() / "stories" / "003_mitthu-ne-sab-bata-diya"}
C01 = channel_dir() / "stories" / "002_sharma-ji-ki-cycle" / "images"  # Case 01 scenes (Sharma ji, Raju look refs)
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
    "long_02": {
        # value: (file name, prompt[, extra refs[, output dir]]) - Sharma ji is a recurring channel character
        "sharma": ("sharma_sheet.png", f"""{SHEET}
Character: Sharma ji, the Gulmohar Mohalla neighbour in his mid-50s, EXACTLY as he looks in the attached Case 01 scene
images (those images are the truth for his face, glasses, clothes and colours): bald head with grey hair on the sides,
rectangular spectacles, cream kurta-pyjama, brown sleeveless jacket, slightly round, always a little worried.
Poses: STANDING CALLING SOMEONE (one hand cupped at his mouth); WORRIED, HOLDING HIS HEAD with both hands;
HAPPY, GENTLY HUGGING a small cat-shaped empty space at his chest (do not draw a cat).
Expressions: WORRIED, CONFUSED, RELIEVED SMILE.""", [C01 / "scene_01.png", C01 / "scene_02.png"], CHAR),
        "raghu": ("raghu_sheet.png", f"""{SHEET}
Character: Raghu, a new young Indian milkman about 25. Slim, friendly honest face, short neat black hair, clean-shaven.
Blue-and-white CHECK shirt with rolled sleeves, khaki trousers, brown sandals. He has a GREEN bicycle with two shiny
steel milk cans hanging at the back (clearly different from the other milkman Pappu, who wears a white kurta with a red
gamchha and rides a black cycle).
Poses: STANDING NEXT TO HIS GREEN BICYCLE with the two milk cans (smiling, waving hello); CARRYING ONE MILK CAN in one
hand; PUZZLED, palms open ('why is everyone staring at me?').
Expressions: FRIENDLY SMILE, CONFUSED, RELIEVED LAUGH."""),
        "gupta": ("gupta_sheet.png", f"""{SHEET}
Character: Mrs. Gupta, the mohalla's chatty neighbour about 50. Plump, expressive face with big eyes, a big hair bun,
a maroon bindi, gold bangles on both wrists. PINK saree with a thin gold border, worn neatly.
Poses: GOSSIPING, leaning in with a hand beside her mouth; 'HAI RAM!' both hands on her cheeks; POINTING dramatically.
Expressions: SHOCKED, EXCITED GOSSIP, EMBARRASSED APOLOGETIC SMILE."""),
        "sona": ("sona_sheet.png", """Character reference sheet of ONE cat on a plain off-white background, flat 2D cartoon
with thick bold black outlines, warm colours, flat cel shading, small uppercase labels. Sona, a golden-orange tabby cat
with soft darker stripes, WHITE paws, big friendly green eyes, a small GREEN collar with a tiny golden bell. Always calm,
cosy and happy - never scared, never in danger.
Top row: SITTING (tail around the paws), LAPPING MILK from a small steel bowl, WALKING (side view).
Bottom row: SLEEPING CURLED UP in the sun (eyes closed, content), HAPPY FACE close-up, YAWNING.
The cat must look identical in every pose. No people, no scenery."""),
    },
}

if __name__ == "__main__":
    vid = sys.argv[1]
    names = sys.argv[2:] or list(SPECS[vid])
    out_dir = STORY_DIRS[vid] / "characters"
    for name in names:
        fname, prompt, *more = SPECS[vid][name]  # optional: extra refs, output dir (recurring channel characters)
        extra_refs = more[0] if more else []
        target = (more[1] if len(more) > 1 else out_dir) / fname
        t0 = time.time()
        out = generate(f"{prompt}\n\n{STYLE_NOTE}", target, refs=STYLE_REFS + list(extra_refs), aspect_ratio="3:2",
                       size="1K")
        print(f"saved {out}  ({time.time() - t0:.0f}s)", flush=True)
