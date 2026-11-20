"""Scene images for 011 Al-Qadr (RULES 2h/2i/2j faceless storybook). Free Cloudflare flux first; paid Gemini
fallback only with --paid and only for the names given (max 3-4 per video, RULES 2h).
Ayah 4 (angels, ar-Ruh): NEVER an angel in any form, not even as light figures; only the calm night town / lamps (RULES 2/2a).
    .venv\\Scripts\\python -X utf8 channels/noor-e-raah/stories/011_al-qadr/gen.py [--only a,b] [--paid name1,name2]
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
    "01_qadr_night": "Scene: a deep, calm, holy-feeling night over a quiet desert valley town with low mud-brick houses and palm trees, "
        "a huge sky full of bright stars and a soft silver glow over everything, perfect stillness and peace." + NOP + " Wide shot.",
    "02_mountain_night": "Scene: tall dark rocky mountains near the town at night, a small cave opening high on a rocky slope, the starry sky "
        "above glowing softly, quiet and solemn mood." + NOP + " Wide shot.",
    "03_ramadan_lamps": "Scene: night in a narrow lane of mud-brick houses, a small warm oil lamp glowing in front of every door and window, "
        "a thin crescent moon in the sky, quiet blessed mood." + NOP + " Medium-wide shot.",
    "04_sky_light_valley": "Scene: from the starry night sky a single wide, soft column of pale golden light comes gently down onto an empty "
        "quiet desert valley, the sand glowing where it touches, calm, majestic and peaceful." + NOP + " Wide shot.",
    "05_looking_up_stars": "Scene: a small faceless man in a simple beige robe stands alone on top of a sand dune at night, seen from behind, "
        "looking up at an enormous sky full of stars and the milky way, he is tiny compared to the sky, feeling of wonder. Only this one "
        "figure. Wide shot.",
    "06_old_man_years": "Scene: late afternoon, a very old faceless man with a white beard-less round blank head, a walking stick and a simple "
        "brown robe sits on a bench outside his mud-brick house door, a long life behind him, palm tree shadow, calm reflective mood. "
        "Only this one figure. Medium shot.",
    "07_night_prayer_far": "Scene: night, seen from far outside through the open doorway of a simple lamp-lit mud-brick room, a faceless man "
        "in a simple robe stands calmly in prayer facing away from the viewer, hands folded on his chest, a woven prayer mat, a clay lamp, "
        "quiet devotion. Only this one figure, seen from behind and far. Wide shot.",
    "08_dua_hands_lamp": "Scene: night, close-up seen from just behind and above the shoulder of a faceless person sitting on a woven mat: his two dark gloved hands are held together low in front of his chest, cupped, palms open and facing UP toward the sky like holding water, elbows bent close to the body, the sleeves of a simple beige robe, a small clay oil lamp glowing warmly on the mat ahead, soft bokeh of a starry night through an open doorway. No head visible, no glowing circles, only the hands and sleeves. Close-up shot.",
    "09_town_lamps_night": "Scene: a high view over the whole sleeping mud-brick town at night, warm lamp light glowing in many small windows, "
        "the starry sky very bright and calm above, a feeling that the whole night is blessed." + NOP + " Wide shot.",
    "10_still_palms": "Scene: still night, tall palm trees by a calm small pool of water reflecting the stars, a very gentle breeze, total "
        "peace and safety, soft blue and silver colours." + NOP + " Medium-wide shot.",
    "11_fajr_breaks": "Scene: the first light of fajr breaking over dark rocky hills, the horizon turning soft gold and pink, the last stars "
        "fading above, a quiet valley town below." + NOP + " Wide shot.",
    "12_pale_sun": "Scene: early morning, a soft pale round sun just above the desert horizon, gentle and mild, with NO strong rays, no glare, "
        "a hazy calm white-gold light over the dunes and palm trees, serene." + NOP + " Wide shot.",
    "13_masjid_night_far": "Scene: night, a very simple early mosque seen from outside and far away: low mud-brick walls, a flat roof of palm "
        "trunks and palm leaves, no dome, no minaret, warm lamp light inside, a row of tiny faceless worshippers seen from behind standing "
        "in prayer, calm devotion. Wide shot.",
    "14_closed_door_calm": "Scene: the plain wooden door of a simple mud-brick prayer room at night, closed, a single lamp beside it, a quiet "
        "empty courtyard, a feeling of something precious kept hidden." + NOP + " Medium shot.",
    "15_family_night_dua": "Scene: night inside a simple mud-brick room, a faceless father, a faceless mother in a modest head scarf and a small "
        "faceless child sit on a woven mat seen from behind, all three with hands raised in dua in front of their chests, a clay oil lamp "
        "glowing, peaceful hopeful mood. Only these three figures, seen from behind. Medium shot.",
    "thumb_scene": "Scene: a vast quiet desert valley under a deep night sky full of stars, a soft golden glow rising at the horizon on the "
        "right, a low mud-brick town with tiny lamp lights. The LEFT 45 percent of the image is calm dark-blue empty night sky with very "
        "few details, kept clear for large text. Matte painted look, reverent, deep indigo and warm gold." + NOP,
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
