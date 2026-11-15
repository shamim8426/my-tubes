import sys
from pathlib import Path
H = Path(__file__).parent; ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from cf_image import generate
P = {
 "hook": "realistic product photo of a small wireless speaker and a smartphone on a clean desk next to a laptop, soft studio light, shallow depth of field, no text, no logos, no people",
 "globe": "realistic photo of a desk globe, over-ear headphones and a notebook on a bright desk, soft daylight, shallow depth of field, no text, no people",
 "mic": "realistic product photo of a studio microphone with a pop filter on a boom arm, soft warm light, blurred background, no text, no logos, no people",
}
for k, pr in P.items():
    out = H / f"raw/photos/{k}.png"
    if out.exists(): continue
    generate(pr, out, width=1344, height=768); print(k, "ok", flush=True)
