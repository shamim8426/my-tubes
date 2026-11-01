"""Backgrounds for the cast v3 rocket test Short (free Cloudflare flux, Rs0). Background-only: no people/animals."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
from cf_image import generate  # noqa: E402

OUT = Path(__file__).parent / "images"
STYLE = ("Flat 2D cartoon background for a children's animated story, clean simple shapes, smooth soft gradients, "
         "warm friendly colours, crisp edges, storybook look, vertical 9:16 composition. Background only: NO people, "
         "NO children, NO animals, NO insects, NO characters anywhere. No text, letters, numbers or logos.")
BGS = {
    "bg_aangan": "An Indian village courtyard (aangan) at dusk: a small mud house with a red clay-tile roof on the left "
                 "edge, a big gulmohar tree with red-orange flowers on the right edge, a low mud boundary wall, a clean "
                 "swept flat earthen ground filling the lower 40 percent, wide open empty space in the middle for a tall "
                 "object, warm orange and violet evening sky with the first stars.",
    "bg_cabin": "Inside the round cabin of a friendly cartoon rocket ship: a huge curved clear glass dome fills the "
                "upper two thirds showing deep blue starry outer space and a big pale moon in the upper right; the "
                "lower part has a simple curved cream-coloured floor and a low control panel with a few round coloured "
                "buttons along the bottom edge; the centre is open and empty.",
    "bg_earth": "View from outer space looking down at planet Earth at night: the curved Earth fills the lower half, "
                "the night side in deep blue darkness with soft wispy clouds, NO recognisable continent or country outlines, no map; "
                "only many scattered clusters of tiny warm golden city lights glowing like fireflies, a thin glowing blue "
                "atmosphere line, black-blue space with many stars in the upper half.",
}

for name, desc in BGS.items():
    out = OUT / f"{name}.png"
    if out.exists() and "--force" not in sys.argv:
        print("cached", out.name)
        continue
    generate(f"{desc}\n\n{STYLE}", out, width=1088, height=1920)
    print("made", out.name, flush=True)
