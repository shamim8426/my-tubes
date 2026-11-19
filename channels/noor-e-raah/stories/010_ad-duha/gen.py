"""Scene images for 010 Ad-Duha (RULES 2h/2i/2j faceless storybook). Free Cloudflare flux first; paid Gemini
fallback only with --paid and only for the names given (max 3-4 per video, RULES 2h).
Ayat 3-8 speak to the Prophet (pbuh): those scenes are PLACES / symbols only, no person at all (RULES 2/2a/2e).
    .venv\\Scripts\\python -X utf8 channels/noor-e-raah/stories/010_ad-duha/gen.py [--only a,b] [--paid name1,name2]
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
BN = ("Illustrated storybook landscape, hand-painted warm 2D cartoon with soft outlines, painterly background, cinematic light. "
      "7th-century Arabia, rocky desert valley with low flat-roofed mud-brick houses with small dark window openings and palm trees. "
      "Completely empty scene: no people, no person, no figure, no human, no silhouette, no animals. "
      "No text, no letters, no writing, no modern objects, no glass windows, no domes, no minarets, no towers. 16:9. ")
NOP = " No people, no figures, no animals."
P = {
    "01_morning_sun": "Scene: bright late-morning sunshine pouring over a quiet desert valley town with low mud-brick houses and "
        "green palm trees, warm golden light, long soft shadows, fresh hopeful mood." + NOP + " Wide shot.",
    "02_still_night": "Scene: a very still, quiet night over the same valley town, dark blue sky full of stars, palm trees not moving, "
        "a few small lamps glowing in windows, deep calm and peace." + NOP + " Wide shot.",
    "03_empty_roof_dusk": "Scene: an empty flat mud-brick rooftop at dusk, a woven mat and a small unlit clay lamp on it, the sky "
        "fading from orange to deep blue, rocky hills around, a quiet waiting, slightly lonely mood." + NOP + " Medium-wide shot.",
    "04_dark_clouds_town": "Scene: heavy grey clouds over a quiet mud-brick town in the late afternoon, narrow empty lanes, a heavy "
        "and sad mood, muted colours." + NOP + " Wide shot.",
    "05_dawn_breaks": "Scene: the first light of dawn breaking over dark rocky mountains, the night sky turning gold at the horizon, "
        "a single bright ray of sunlight reaching down into the valley, strong feeling of hope." + NOP + " Wide shot.",
    "06_path_to_light": "Scene: a long sandy path climbing gently up a hill toward a huge soft golden light on the horizon, the path "
        "behind is in shadow, the path ahead is bright and beautiful." + NOP + " Wide shot.",
    "07_blooming_oasis": "Scene: a lush green oasis blooming in the desert, a clear spring of water, palm trees heavy with golden "
        "dates, flowers, soft golden light, abundance and contentment." + NOP + " Wide shot.",
    "08_shelter_lamp": "Scene: night in the desert, a single small mud-brick house with its wooden door open and a warm oil lamp "
        "glowing inside, a safe shelter in the dark, stars above." + NOP + " Medium-wide shot.",
    "09_star_path": "Scene: night desert, a winding path between dunes clearly lit by one very bright star and the moon, the way "
        "ahead is clear and shining." + NOP + " Wide shot.",
    "10_full_well": "Scene: an old stone well full of clear water beside palm trees heavy with dates, baskets of dates and a filled "
        "water skin on the ground, warm afternoon light, feeling of enough and plenty." + NOP + " Medium shot.",
    "11_orphan_care": "Scene: a narrow lane of mud-brick houses in warm afternoon light, a kind faceless man in a simple beige robe "
        "kneels down and gently gives a round loaf of bread to a small faceless boy in a plain worn tunic, his other gloved hand "
        "softly on the boy's shoulder, caring and gentle mood. Only these two figures. Medium shot.",
    "12_door_giving": "Scene: the wooden doorway of a mud-brick house, a faceless woman in a modest dark head scarf and long robe "
        "kindly puts dates into the wooden bowl of a faceless poor old traveller with a walking stick and a patched cloak, "
        "warm soft light, respectful and kind mood. Only these two figures. Medium shot.",
    "13_family_meal": "Scene: evening inside a simple mud-brick room, a faceless father, a faceless mother in a modest head scarf and "
        "two small faceless children sit together on a woven mat around a simple meal of bread, dates and milk, a clay oil lamp "
        "glowing, the father gestures warmly while talking, grateful happy mood. Medium shot.",
    "thumb_scene": "Scene: a vast quiet desert valley at the moment the morning sun rises, soft golden god rays spreading over the "
        "valley, deep blue night still at the top of the sky. The LEFT 45 percent of the image is calm dark-blue empty sky with "
        "very few details, kept clear for large text. Matte painted look, reverent, deep indigo and warm gold." + NOP,
}


def main():
    paid = set(sys.argv[sys.argv.index("--paid") + 1].split(",")) if "--paid" in sys.argv else set()
    only = set(sys.argv[sys.argv.index("--only") + 1].split(",")) if "--only" in sys.argv else None
    (S / "images").mkdir(exist_ok=True)
    for k, v in P.items():
        if only and k not in only:
            continue
        out = S / "images" / f"{k}.png"
        if out.exists():
            continue
        base = BN if NOP in v else B
        if k in paid:
            import gemini_image as g
            g.generate(base + v, out, aspect_ratio="16:9", size="1K")
            print(k, "PAID ok", flush=True)
            continue
        try:
            generate(base + v, out, width=1920, height=1088)
            print(k, "free ok", flush=True)
        except FreeImageError as e:
            print(k, "FREE FAIL", str(e)[:160], flush=True)


if __name__ == "__main__":
    main()
