import sys
from pathlib import Path
H = Path(__file__).parent; ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from cf_image import generate
P = {
 "search": "realistic photo of a glowing magnifying glass in front of a blurred bright screen, soft green and white light, shallow depth of field, no text, no logos, no people",
 "phone": "realistic photo of a modern smartphone lying on a wooden desk next to earbuds, soft daylight, shallow depth of field, blank screen, no text, no logos, no people",
 "table": "realistic top-down photo of a wooden table with a notebook, a paper map, coffee cups and sticky notes, warm light, no readable text, no logos, no people",
}
for k, pr in P.items():
    out = H / f"raw/photos/{k}.png"
    if out.exists(): continue
    generate(pr, out, width=1344, height=768); print(k, "ok", flush=True)
