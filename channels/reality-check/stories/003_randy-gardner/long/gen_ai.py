"""003 sample: free Cloudflare flux images (Rs0). No people, no faces, no text. python gen_ai.py [--workers 3]"""
import sys
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / "scripts"))
from dotenv import load_dotenv

load_dotenv("D:/my-tubes/.env")
import cf_image  # noqa: E402

STYLE = ("Cinematic still, muted mid-tone colour grade (not too dark), soft film grain, shallow depth of field, 1960s California atmosphere, "
         "photoreal, no people, no faces, no text, no letters, no watermark. ")
P = {
    "a01_bedroom_night": "A small empty teenager's bedroom at night, desk lamp glowing over a notebook, unmade bed, blue night light through the window.",
    "a02a_clock_3am": "Close-up of an old bedside alarm clock glowing in the dark, hands near three o'clock, blurred bedroom behind.",
    "a02b_notebook": "A notebook page covered with scribbled, smeared pencil lines and a pencil, shallow focus, warm desk lamp, a few crossed-out lines.",
    "a02c_hallway_shadow": "A long dim hallway in an old house at night, a strange tall shadow on the far wall, nobody visible, eerie but calm.",
    "a03_pinball": "Close-up of a vintage 1960s pinball machine playfield glowing with coloured lights, only a pair of hands on the flipper buttons, arcade atmosphere.",
    "a04a_street_night": "A quiet San Diego street at night in 1964, parked vintage cars, palm trees, street lamps, wet road reflections, no pedestrians.",
    "a04b_traffic_light": "A lone traffic signal glowing over an empty night intersection with a vintage car's blurred headlights in the distance, 1964 California.",
    "a05_moon_rooftops": "A calm night view from a window over suburban rooftops and palm trees, a pale moon, quiet and reflective mood.",
    "a06_phone_bed": "A hand holding a glowing smartphone in a dark bedroom, bluish light spilling on the sheets, only the hand visible, late night.",
    "a07_school": "A 1960s California high school building at dusk, palm trees, long shadows, empty lawn, warm sky.",
    "a08_science_fair": "A science fair table with a blank cardboard display board, glass beakers, a lamp, neat tools, a school gym background, nobody present.",
    "a09_hourglass": "An hourglass with falling sand on a wooden table, soft window light, blurred room behind, calm.",
    "a10_stopwatch": "A vintage stopwatch lying on a wooden desk next to a notebook and a pen, warm light, shallow focus.",
    "a11_bed_made": "A neatly made single bed with a white pillow in a bright morning bedroom, untouched, quiet.",
    "a12_pillow_moon": "A pillow and rumpled sheets lit by pale moonlight, close-up, nobody in the bed, soft shadows.",
    "a13_register": "Two pairs of hands writing in a large ledger register on a table under a lamp, only hands and pens visible, night, 1960s.",
}
OUT = Path(__file__).parent / "ai"
OUT.mkdir(exist_ok=True)


def one(kv):
    k, p = kv
    f = OUT / f"{k}.png"
    if f.exists() and f.stat().st_size > 50000:
        return k, "cached"
    for attempt in range(4):
        try:
            cf_image.generate(STYLE + p, f, 1920, 1088, retries=1)
            return k, "ok"
        except Exception as e:  # noqa: BLE001
            msg = str(e)[:120]
            if "429" in msg or "quota" in msg.lower():
                return k, "QUOTA " + msg
    return k, "FAIL"


if __name__ == "__main__":
    W = int(sys.argv[sys.argv.index("--workers") + 1]) if "--workers" in sys.argv else 3
    with ThreadPoolExecutor(W) as ex:
        for k, r in ex.map(one, P.items()):
            print(k, r, flush=True)
