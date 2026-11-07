import sys
from pathlib import Path
H = Path(__file__).parent; ROOT = H.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import cf_image
(H / "raw/photos").mkdir(parents=True, exist_ok=True)
P = {
 "hook": "cinematic photo, a developer's desk at night, laptop with dark code editor glowing, warm lamp, shallow depth of field, no text, no logos, no people faces",
 "team": "photo, three colleagues' hands around a shared laptop in a bright modern office, team collaboration, shallow depth of field, no text, no logos, no faces",
 "home": "photo, a personal wooden desk drawer with a small brass lock and a notebook, warm light, close-up, shallow depth of field, no text, no logos",
 "shield": "photo, a laptop keyboard with a small padlock resting on it, cool blue light, shallow depth of field, no text, no logos, no faces",
}
for k, p in P.items():
    out = H / f"raw/photos/{k}.png"
    if out.exists(): continue
    try: cf_image.generate(p, out, width=1344, height=768); print(k, "ok", flush=True)
    except Exception as e: print(k, "FAIL", e, flush=True)

