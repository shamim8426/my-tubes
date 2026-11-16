import sys
from pathlib import Path
sys.path.insert(0, "scripts")
import gemini_image
S = Path(__file__).resolve().parent.parent
BASE = ("Cinematic 3D-illustration film still, 7th century Madinah, Arabia, ultra sharp crisp focus, high contrast, deep rich saturated colors, warm earthy palette, "
        "clean air, no haze. Simple plain period clothing in earthy colors. Every person is seen ONLY from behind or from far away or as a dark shadow, absolutely no visible faces, "
        "no Prophet, no angels, no text, no domes, no minarets, no modern objects, only flat-roofed mud-brick houses and palm trees. ")
P = {
"03_family_hearth": "Inside a simple mud house at evening: a mother seen from behind sitting on a woven mat with three small children close around her, a small fire glowing, warm light, tender mood.",
"04_angry_husband": "At the doorway of a mud house at dusk: a man seen from behind, standing stiffly with clenched fists and tense shoulders, a woman far inside the room by the lamp, small and frightened, seen from behind, tense mood.",
"09_telling_story": "Outside the early mosque of Madinah, mud-brick wall with palm-trunk roof and an open doorway full of soft golden light, nobody visible inside; a woman seen from behind sitting on the ground at a respectful distance, hands moving as she speaks, sad hopeful mood.",
}
for k, v in P.items():
    out = S/"images_v2"/f"{k}.png"
    if out.exists(): continue
    try:
        gemini_image.generate(BASE+v, out, aspect_ratio="16:9", size="1K", style=BASE); print("OK", k, flush=True)
    except Exception as e:
        print("ERR", k, str(e)[:150], flush=True)

P2 = {"17_family_door": "At dusk, a mother, a father and three small children seen from behind standing together at the glowing open doorway of their mud house, warm golden light spilling out onto them, happy relieved mood. No faces visible."}
for k, v in P2.items():
    out = S/"images_v2"/f"{k}.png"
    if out.exists(): continue
    gemini_image.generate(BASE+v, out, aspect_ratio="16:9", size="1K", style=BASE); print("OK", k, flush=True)
