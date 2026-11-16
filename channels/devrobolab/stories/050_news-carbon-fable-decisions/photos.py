import sys
from pathlib import Path
H = Path(__file__).parent; ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from cf_image import generate
P = {
 "chip": "realistic macro photo of a glowing computer processor chip on a dark circuit board, blue and violet light, shallow depth of field, no text, no logos, no people",
 "server": "realistic photo of a modern data center aisle with server racks and soft blue lights, clean, no text, no logos, no people",
 "code": "realistic photo of a laptop on a desk showing a dark code editor, soft warm light, shallow depth of field, no readable text, no logos, no people",
}
for k, pr in P.items():
    out = H / f"raw/photos/{k}.png"
    if out.exists(): continue
    generate(pr, out, width=1344, height=768); print(k, "ok", flush=True)
