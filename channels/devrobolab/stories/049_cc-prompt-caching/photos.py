import sys
from pathlib import Path
H = Path(__file__).parent; ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import cf_image
(H / "raw/photos").mkdir(parents=True, exist_ok=True)
P = {
 "hook": "cinematic photo, a developer laptop on a dark desk at night, a stopwatch beside it, warm lamp, shallow depth of field, no text, no logos, no people faces",
 "what": "photo, a library shelf of neatly stacked folders and file boxes, warm light, shallow depth of field, no text, no logos, no people",
 "clock": "photo, a vintage hourglass on a desk next to a laptop, soft light, close-up, shallow depth of field, no text, no logos, no faces",
}
for k, p in P.items():
    out = H / f"raw/photos/{k}.png"
    if out.exists(): continue
    try: cf_image.generate(p, out, width=1344, height=768); print(k, "ok", flush=True)
    except Exception as e: print(k, "FAIL", e, flush=True)


