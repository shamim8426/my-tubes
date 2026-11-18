"""Scene images for 009 Al-Kafirun (RULES 2h/2i/2j faceless storybook). Free Cloudflare flux first; paid Gemini
fallback only with --paid and only for the names given (max 3-4 per video, RULES 2h).
    .venv\\Scripts\\python -X utf8 channels/noor-e-raah/stories/009_al-kafirun/gen.py [--paid name1,name2]
"""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from cf_image import generate, FreeImageError  # noqa: E402

S = Path(__file__).resolve().parent
B = ("Illustrated storybook scene, hand-painted warm 2D cartoon with soft outlines, painterly background, cinematic light. "
     "ALL people are FACELESS stylized figures: smooth round blank white head with NO eyes, NO nose, NO mouth, NO face features, "
     "simple dark gloved hands, simple modest robes. 7th-century Arabia, rocky desert valley with low flat-roofed mud-brick houses "
     "and palm trees. No text, no letters, no writing, no modern objects, no domes, no minarets, no towers. 16:9. ")
P = {
    "02_chiefs_offer": "Scene: night, an open courtyard of a rich mud-brick house, five faceless elderly chiefs in fine colourful robes "
        "and head cloths sit in a half circle on woven carpets around a small oil lamp, one chief leans forward offering with both open "
        "palms as if making a deal, the others nod, warm orange lamp light, deep blue night sky. Medium-wide shot.",
    "03_idols_shrine": "Scene: a dusty open shrine yard with several rough carved stone idols of different sizes on low stone platforms, "
        "small offerings of dates and cloth at their feet, a few faceless people in robes standing in front of them, late afternoon "
        "hazy light, heavy and gloomy mood. Wide shot.",
    "04_light_valley": "Scene: wide view over a quiet rocky valley town at dawn, soft beams of golden light coming down from the clouds "
        "onto the valley, calm and powerful mood, no people. Wide shot.",
    "05_two_paths": "Scene: high view of a clear Y-shaped fork in a sandy desert track, the track splits into TWO clearly separate "
        "roads going in opposite directions: the left road goes down into dark grey shadow toward a small group of rough stone idols, "
        "the right road climbs a hill into bright golden sunrise light. Strong contrast between dark left and bright right. "
        "No people. Wide shot.",
    "06_family_dua": "Scene: inside a simple mud-brick room at night, a faceless father, a faceless mother in a modest head scarf and a "
        "small faceless child sit together on a woven mat, all three raising their open hands in front of their chests in quiet "
        "prayer, a small clay oil lamp glowing, warm golden light, peaceful mood. Medium shot from slightly behind.",
    "07_neighbors": "Scene: a narrow lane in the morning with two neighbouring mud-brick houses with different coloured doors, a faceless "
        "man at one door hands a basket of bread and dates to a faceless neighbour at the other door, both friendly and calm, "
        "warm soft light. Only these two adult men, no children, no other people. Medium shot.",
    "08_sleep_lamp": "Scene: a simple quiet mud-brick room at night, a thin sleeping mattress on the floor with a small pillow and "
        "a folded woollen blanket, ready for sleep, a small clay oil lamp glowing on the floor beside it, a small window showing "
        "stars. Nobody in the room, no people. Warm calm peaceful mood. Medium shot.",
    "09_dawn_walk": "Scene: early morning, a faceless man in a simple beige robe seen from behind walks steadily along a straight path "
        "toward a bright golden sunrise between rocky hills, palm trees, calm and confident mood. Wide shot.",
    "10_stars_valley": "Scene: peaceful night over a quiet desert valley town with low mud-brick houses, a sky full of stars and a "
        "thin crescent moon, a few small lamps glowing in windows, calm and safe mood. No people. Wide shot.",
}


def main():
    paid = set(sys.argv[sys.argv.index("--paid") + 1].split(",")) if "--paid" in sys.argv else set()
    for k, v in P.items():
        out = S / "images" / f"{k}.png"
        if out.exists():
            continue
        if k in paid:
            import gemini_image as g
            g.generate(B + v, out, aspect_ratio="16:9", size="1K")
            print(k, "PAID ok", flush=True)
            continue
        try:
            generate(B + v, out, width=1920, height=1088)
            print(k, "free ok", flush=True)
        except FreeImageError as e:
            print(k, "FREE FAIL", str(e)[:160], flush=True)


if __name__ == "__main__":
    main()
