"""Possibilities FINAL channel art (option E: black + bright yellow). Output channels/reality-check/brand/ (logo_800.png, banner_2048x1152.png)."""
import sys
from pathlib import Path
from PIL import Image, ImageDraw

sys.path.insert(0, str(Path(__file__).parent))
from rc_brand_variants import OUT, F, grad, over, glow   # noqa: E402
from rc_brand_variants2 import D, deco, mark_ring        # noqa: E402

BRAND = OUT.parent
p = D["E_blackyellow"]

# ---- logo 800x800, circle-safe (everything within r=330 of the centre) ----
S = 800
im = deco(grad(S, S, *p["bg"]), p["deco"], p, S, S)
im = glow(im, 380, 420, 240, p["main"], .16)
im = over(im, lambda d: mark_ring(d, 372, 430, 440, p["main"], p["dim"], p["dot"]))
im.convert("RGB").save(BRAND / "logo_800.png")

# ---- banner 2048x1152: text + logo inside the 1235x338 centre safe area ----
W, H = 2048, 1152
bn = deco(grad(W, H, *p["bg"]), p["deco"], p, W, H)
mx, my = 560, H // 2 + 6
bn = glow(bn, mx, my, 210, p["main"], .16)
bn = over(bn, lambda d: mark_ring(d, mx, my, 300, p["main"], p["dim"], p["dot"]))
d = ImageDraw.Draw(bn)
y1 = H // 2 - 100
d.text((790, y1), "POSSIBILITIES", font=F(100), fill=(255, 255, 255))
d.text((794, y1 + 128), "Kya ho sakta hai?", font=F(54), fill=p["sub"])
bn.convert("RGB").save(BRAND / "banner_2048x1152.png")
pv = bn.convert("RGB").copy()
ImageDraw.Draw(pv).rectangle([(W - 1235) / 2, (H - 338) / 2, (W + 1235) / 2, (H + 338) / 2], outline=(0, 255, 0), width=3)
pv.resize((1024, 576)).save(BRAND / "banner_safe_preview.png")
# circle preview of the logo as YouTube shows it
c = Image.open(BRAND / "logo_800.png").convert("RGBA")
mask = Image.new("L", c.size, 0)
ImageDraw.Draw(mask).ellipse([0, 0, c.size[0], c.size[1]], fill=255)
bg = Image.new("RGBA", c.size, (60, 60, 60, 255))
bg.paste(c, (0, 0), mask)
bg.convert("RGB").resize((400, 400)).save(BRAND / "logo_circle_preview.png")
print(BRAND)
