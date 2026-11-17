"""008 Al-Fil: people-driven images per ayah block (RULES 2h, user 2026-11-15). Free Cloudflare flux first, Rs0.
Ordinary fictional people only (faces allowed); never a Nabi/Sahabi/Quran-named person/angel; no army/elephant attack
acted out; generic setting; modest dress; no text.
    .venv/Scripts/python -X utf8 channels/noor-e-raah/stories/008_al-fil/script/gen_imgs.py [ids...]
"""
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
import cf_image  # noqa: E402

S = Path(__file__).resolve().parent.parent
BASE = ("Warm cinematic film still, realistic people, rich warm earthy palette, golden natural light, soft depth of field, "
        "sharp focus on the subject, wide 16:9 composition, a simple old desert village with low flat-roofed mud-brick houses "
        "and date palms. Ordinary everyday people in modest simple traditional clothes: men in plain long kurta-like robes "
        "and a simple cloth head wrap, women in long loose dresses with a headscarf covering the hair. Correct hands with "
        "five fingers. Absolutely no text, no letters, no writing, no modern objects, no domes, no minarets, no towers, "
        "no castles, no glass lanterns, no angels, no wings on people, no halos. ")
P = {
    "p01_grandpa_story": "Evening by a small fire outside a mud house, an old grandfather with a white beard telling a story "
                         "to three young children who listen with wide amazed eyes, warm firelight on their faces.",
    "p02_father_son_dawn": "A father and his young son standing on a rocky hill at sunrise, looking out over a wide golden "
                           "desert valley in awe, the father's hand on the boy's shoulder, seen from a three-quarter angle.",
    "p03_mother_dust": "A worried young mother holding her small child close at the doorway of a mud house, both looking "
                       "toward a huge dust cloud rising on the far horizon, tense evening light.",
    "p04_proud_man": "A proud rich man in fine embroidered robes standing on a flat rooftop with his arms crossed, smiling "
                     "confidently over the village at noon, a tall neat pile of stacked stones beside him.",
    "p05_fallen_stones": "A man in fine robes kneeling beside a collapsed scattered pile of stones on a dusty ground, his "
                         "hands open, shocked face, his big plan ruined, dramatic late light.",
    "p06_kids_birds": "A shepherd boy and his little sister on a sandy hill pointing up at the evening sky where a large "
                      "flock of small dark birds is flying, goats around them, wonder on their faces.",
    "p07_flocks_sky": "Flock after flock of small dark birds streaming across a glowing orange evening sky over desert "
                      "dunes, an old woman in the foreground shading her eyes with her hand and looking up.",
    "p08_pebbles_palm": "Close-up of a child's open palm holding a few small reddish-brown baked clay pebbles, the child's "
                        "curious face softly blurred behind, warm morning light.",
    "p09_potter_kiln": "An old potter sitting beside a small glowing clay kiln, his hands holding small hard baked clay "
                       "pieces still warm from the fire, focused calm face, workshop of a mud house.",
    "p10_farmer_field": "An old farmer standing alone in a flattened empty field of broken dry stalks after a storm, "
                        "thoughtful quiet face, wide sky, early morning light.",
    "p11_chaff_hands": "Close-up of a farmer's weathered hands holding a heap of dry crumbling chewed straw and chaff, "
                       "pieces falling between the fingers, threshing floor, warm light.",
    "p12_family_dua": "A small family of a father, mother and two children seen from behind sitting on a mat on a rooftop "
                      "at dawn, making dua: elbows bent close to the body, hands in front of the chest below the chin, "
                      "palms open facing up, heads slightly bowed.",
    "p13_mother_door": "A mother smiling softly and tucking a blanket around her sleeping child inside a calm mud house, "
                       "morning light from a small window, safe peaceful mood.",
    "p14_morning_walk": "Village people walking calmly to work on a sandy path between date palms in fresh golden morning "
                        "light, a father carrying a child on his shoulders, peaceful hopeful mood.",
}

if __name__ == "__main__":
    only = sys.argv[1:]
    for k, v in P.items():
        out = S / "images" / f"{k}.png"
        if out.exists() or (only and k not in only):
            continue
        for t in range(2):
            try:
                cf_image.generate(BASE + v, out, width=1920, height=1088)
                print("OK", k, flush=True)
                break
            except Exception as e:  # noqa: BLE001
                print("ERR", k, str(e)[:160], flush=True)
                if "quota" in str(e) or "429" in str(e):
                    sys.exit("QUOTA")
                time.sleep(5)
