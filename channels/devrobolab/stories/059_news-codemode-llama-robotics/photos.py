import sys
from pathlib import Path
H = Path(__file__).parent; ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
from cf_image import generate
P = {
 "code": "realistic photo of a laptop on a desk showing blurry colorful code editor lines, dark room, soft blue glow, shallow depth of field, no readable text, no logos, no people",
 "chip": "realistic macro photo of a computer chip on a green circuit board, soft light, shallow depth of field, no text, no logos, no people",
 "robot": "realistic photo of an industrial robot arm in a bright clean factory, soft daylight, shallow depth of field, no text, no logos, no people",
}
for k, pr in P.items():
    out = H / f"raw/photos/{k}.png"
    if out.exists(): continue
    generate(pr, out, width=1344, height=768); print(k, "ok", flush=True)
