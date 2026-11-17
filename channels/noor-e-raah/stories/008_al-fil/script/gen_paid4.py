"""008 Al-Fil: Cloudflare free quota still empty at 05:36 IST (429), so RULES 2h fallback: paid Gemini, max 4 people
images, 1K 16:9, story budget check before each call. Prompts = gen_imgs.py P (same BASE).
    .venv/Scripts/python -X utf8 channels/noor-e-raah/stories/008_al-fil/script/gen_paid4.py
"""
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(HERE))
import gemini_image  # noqa: E402
import pricing  # noqa: E402
import story_budget  # noqa: E402
from gen_imgs import BASE, P  # noqa: E402

PICK = ["p01_grandpa_story", "p05_fallen_stones", "p06_kids_birds", "p11_chaff_hands"]
S = HERE.parent
for k in PICK:
    out = S / "images" / f"{k}.png"
    if out.exists():
        continue
    est = pricing.image_estimate_usd(gemini_image.MODEL, "1K", len(P[k]) + len(BASE), 0) * pricing.usd_to_inr()
    story_budget.check(S.name, est)
    gemini_image.generate(P[k], out, aspect_ratio="16:9", size="1K", style=BASE)
    print("OK", k, flush=True)
print(story_budget.summary_line(S.name))
