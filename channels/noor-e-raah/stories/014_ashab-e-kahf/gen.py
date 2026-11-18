"""Scene images for 014 Ashab-e-Kahf (RULES 2e/2g/2j faceless storybook, 2l template). FREE Cloudflare flux only
(history videos: no paid images, RULES 2f). Order = priority; if the free quota ends, later scenes become crops.
    .venv\\Scripts\\python -X utf8 channels/noor-e-raah/stories/014_ashab-e-kahf/gen.py
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from cf_image import generate, FreeImageError  # noqa: E402

S = Path(__file__).resolve().parent
B = ("Illustrated storybook scene, hand-painted warm 2D cartoon with soft outlines, painterly background, cinematic light, "
     "crisp, high contrast, rich warm colours. ALL people are FACELESS stylized figures: smooth round blank white head with NO eyes, "
     "NO nose, NO mouth, NO face features, simple dark gloved hands, simple modest long robes and head cloths. "
     "Ancient Middle-East, rocky mountains, old stone town with flat roofs. No text, no letters, no writing, no modern objects, "
     "no domes, no minarets, no towers, no crosses, no glass lanterns. 16:9. ")
Y = "young men, each with a soft white glow around the head"
NP = " Absolutely no people, no humans, no figures anywhere in the picture."
P = {
    "06_cave_mouth": "Scene: a dark cave opening in a rocky mountainside at golden evening, a narrow stone path leading up to it, "
        "quiet and mysterious, no people. Wide shot.",
    "08_sleep_cave": f"Scene: inside a wide cave, five faceless {Y}, lying asleep on their backs side by side on the sandy cave floor, "
        "covered with simple woollen blankets up to the shoulders, every head is a smooth blank pure WHITE oval like an egg with no ears, "
        "no hair, no beard, no eyes, soft warm light from the cave opening, calm and safe mood. Medium-wide shot from a distance.",
    "10_dog_entrance": "Scene: a calm brown dog lying alone at the entrance of a dark cave with both front legs stretched forward on the ground, "
        "head up, watchful, golden light outside on rocky mountains. ONLY the dog, absolutely no people, no humans, no figures. Medium shot.",
    "02_town_idols": "Scene: an ancient stone town square in daylight, several rough block-shaped stone idols (crude pillar shapes, not realistic human statues, fully clothed) on low platforms, a small crowd "
        "of faceless townspeople in colourful robes bowing in front of the idols, offerings at their feet, heavy gloomy mood. Wide shot.",
    "03_youths_together": f"Scene: a quiet simple stone room at night, five faceless {Y}, sitting close together on a woven mat, "
        "talking softly, a small clay oil lamp glowing between them, warm golden light, hopeful mood. Medium shot.",
    "04_youths_stand": f"Scene: a stone town square, four faceless {Y}, standing upright and firm side by side in the centre, calm and brave, "
        "facing a small group of hooded townspeople seen from behind in the foreground. EVERY person without exception has a smooth blank "
        "white egg-shaped head with no face, no eyes, no mouth, no beard, no skin-coloured faces anywhere. Dramatic warm light. Wide shot.",
    "05_leave_town": f"Scene: five faceless {Y}, seen from behind, walking away from an old stone town toward rocky mountains, "
        "a brown dog walking with them, dusk sky with first stars. Wide shot.",
    "07_dua_cave": f"Scene: inside a cave, five faceless {Y}, seen from behind, sitting on the cave floor and raising their open hands "
        "in quiet prayer toward the cave opening where soft light comes in, peaceful mood. Medium shot.",
    "09_sun_cave": "Landscape painting only: a rocky mountainside with one dark cave opening in the middle, the morning sun low on the "
        "upper right, bright golden sun rays falling across the rocks to the right of the cave, the cave mouth stays in soft blue shade, "
        "empty wild nature, no town, no buildings. Wide shot."+NP,
    "11_wake_talk": f"Scene: inside a cave in morning light, five faceless {Y}, just woken up, sitting up on the cave floor, "
        "one raises a hand as if asking a question, others look at each other, surprised mood. Medium shot.",
    "12_coins": "Scene: extreme close-up of an open dark gloved palm holding a few old worn round silver coins, filling the frame, "
        "plain blurred warm cave rock background, nothing else."+NP+" Close-up.",
    "13_market": f"Scene: an old stone market street in daylight, fruit and bread stalls, a young man in an old-fashioned robe with a soft "
        "white glow around his head holds out a silver coin to a shopkeeper who leans back in surprise. EVERY person has a smooth blank white "
        "egg-shaped head with NO face: no eyes, no mouth, no nose, no beard. Medium-wide shot.",
    "14_people_cave": "Scene: a crowd of faceless townspeople in robes walking up a rocky mountain path toward a cave opening, some "
        "pointing at the cave, afternoon light. Wide shot.",
    "15_stars_cave": "Scene: a calm night over rocky mountains with a small dark cave opening in the mountainside, a sky full of bright stars "
        "and a thin crescent moon, peaceful and timeless mood. Wide shot."+NP,
    "16_dawn_cave": "Scene: a mountain cave at dawn, golden sunrise light pouring over the mountains, beautiful soft sky, peaceful "
        "and hopeful mood, no people. Wide shot.",
}


def main():
    only = sys.argv[1].split(",") if len(sys.argv) > 1 else None
    for k, v in P.items():
        if only and k not in only:
            continue
        out = S / "images" / f"{k}.png"
        if out.exists():
            continue
        try:
            generate(B + v, out, width=1920, height=1088)
            print(k, "free ok", flush=True)
        except FreeImageError as e:
            print(k, "FREE FAIL", str(e)[:160], flush=True)


if __name__ == "__main__":
    main()
