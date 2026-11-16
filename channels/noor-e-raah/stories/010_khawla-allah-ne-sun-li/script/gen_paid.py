import sys, importlib.util
from pathlib import Path
sys.path.insert(0, "scripts")
import gemini_image
S = Path(__file__).resolve().parent.parent
src = (S/"script/gen_imgs.py").read_text(encoding="utf-8")
ns = {}
exec(src.split("only = sys.argv")[0].replace("import cf_image",""), {"__file__": str(S/"script/gen_imgs.py"), **ns}, ns)
BASE, P = ns["BASE"], ns["P"]
for k in ["03_house_hearth","05_stuck_rope","12_ayah_card","13_open_sky","14_old_custom_falls","17_door_opens","19_morning_market"]:
    out = S/"images"/f"{k}.png"
    if out.exists(): continue
    try:
        gemini_image.generate(BASE+P[k], out, aspect_ratio="16:9", size="1K", style=BASE); print("OK", k, flush=True)
    except Exception as e:
        print("ERR", k, str(e)[:150], flush=True)
