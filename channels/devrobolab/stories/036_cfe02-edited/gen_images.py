"""Free Cloudflare FLUX images (9:16) that depict what the voice says. No people/faces, no text. Run: python gen_images.py"""
import sys
from pathlib import Path
H = Path(__file__).parent
sys.path.insert(0, str(H.parents[3] / "scripts"))
from cf_image import generate
S = "photorealistic photograph, natural light, shallow depth of field, high detail, no people, no text, no logos"
P = {"messy": f"top-down photo of a cluttered desk covered with scattered papers, sticky notes, pens and an open laptop, chaotic, {S}",
     "rooms": f"wide photo of three separate tidy workstations side by side, each with its own laptop and a small stack of books, clean office, {S}",
     "tofolder": f"close-up photo of loose papers and a USB drive being slid into an open manila folder on a wooden desk, {S}",
     "book": f"photo of a large open old book glowing with warm golden light rising from its pages, dark background, {S}",
     "sealed": f"studio photo of two separate glass boxes side by side with closed doors and brass padlocks, one holds a notebook and the other a laptop, {S}",
     "drop": f"close-up photo of a hand placing a sheet of paper into a manila folder on a desk, only the hand visible, {S}"}
for k, p in P.items():
    f = H / "ai" / f"{k}.png"
    if f.exists(): continue
    try: generate(p, f, width=896, height=1536); print("ok", k, flush=True)
    except Exception as e: print("fail", k, e, flush=True)
print("done")
