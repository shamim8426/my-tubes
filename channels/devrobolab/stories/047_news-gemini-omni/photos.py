import sys
from pathlib import Path
H = Path(__file__).parent; ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from cf_image import generate
P = {
 "hook": "realistic product photo of a filmmaker's desk with a laptop showing a colourful cinematic video timeline, small clapperboard and a camera, soft studio light, shallow depth of field, no text, no people",
 "sport": "realistic photo of a football in mid-air with motion blur and splashing water droplets on a wet pitch, dynamic fast action, dramatic light, no text, no people",
 "devices": "realistic product photo of a laptop, a tablet and a smartphone on a clean white desk, screens showing abstract colourful video thumbnails, soft light, no text, no logos",
}
for k, pr in P.items():
    out = H / f"raw/photos/{k}.png"
    if out.exists(): continue
    generate(pr, out, width=1344, height=768); print(k, "ok", flush=True)
