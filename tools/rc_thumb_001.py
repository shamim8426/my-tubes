"""Reality Check 001 thumbnail (own render, no face): glowing impact on an asteroid, big text. Output long/output/001_thumbnail.png (1280x720)."""
import sys
sys.path.insert(0, str(__import__("pathlib").Path(__file__).parent))
import cv2, numpy as np, math
from PIL import Image, ImageDraw, ImageFont
import rc_build_long as B
import rc_explain as E
from rc_explain import rock_spr, craft_spr, blit, W, H

im = np.zeros((H, W, 3), np.uint8)
B.draw_bg(im, 3.0, 1, None)
B.glow(im, 1380, 560, 900, (60, 90, 200), 0.18)
# asteroid (right ~55 %)
spr = rock_spr(2, 900, 1.0, (1.0, 0.9), 0.0)
blit(im, spr, 1520, 600, 1.0, 0.35)
# impact flash on its left limb
fx, fy = 1130, 560
B.glow(im, fx, fy, 520, (40, 120, 255), 0.95)
B.glow(im, fx, fy, 300, (120, 200, 255), 1.0)
B.glow(im, fx, fy, 150, (235, 250, 255), 1.0)
B.circ(im, fx, fy, 42, (255, 255, 255), -1)
for k in range(14):
    a = -0.9 + k * 0.14 + 0.3
    L = 240 + 140 * ((k * 37) % 5) / 4
    B.line(im, fx, fy, fx - L * math.cos(a) * 1.0, fy + L * math.sin(a) * 0.9 - 60, B.mix((120, 190, 255), 0.55), 3)
rng = np.random.default_rng(7)
for i in range(60):
    a = rng.uniform(math.pi * 0.55, math.pi * 1.45)
    d = rng.uniform(80, 420)
    B.circ(im, fx + d * math.cos(a), fy + d * math.sin(a) * 0.8, rng.uniform(2, 6), B.mix((190, 205, 225), rng.uniform(0.4, 0.9)), -1)
# small craft (scale cue) with streaks
for k in range(10):
    B.line(im, 330 - k * 26, 700 + k * 4, 520, 700 + k * 4, B.mix("white", 0.07 + 0.01 * k), 2)
blit(im, craft_spr(), 600, 705, 0.30, 0.0)
im = cv2.convertScaleAbs(im, alpha=1.08, beta=-4)
pil = Image.fromarray(cv2.cvtColor(im, cv2.COLOR_BGR2RGB)).convert("RGBA")
d = ImageDraw.Draw(pil)
f = ImageFont.truetype(str(B.ROOT / "shared/fonts/Poppins-Bold.ttf"), 215)
fs = ImageFont.truetype(str(B.ROOT / "shared/fonts/Poppins-Bold.ttf"), 120)
# line 1: yellow box "7 MIN?"
t1 = "7 MIN?"
w1 = d.textlength(t1, font=f)
d.rounded_rectangle([50, 70, 50 + w1 + 70, 70 + 290], 28, fill=(255, 214, 10, 255))
d.text((85, 60), t1, font=f, fill=(12, 14, 26, 255))
t2 = "NAHI, "
d.text((60, 400), t2, font=f, fill=(255, 255, 255, 255), stroke_width=10, stroke_fill=(5, 7, 16, 255))
w2 = d.textlength(t2, font=f)
d.text((60 + w2, 400), "33", font=f, fill=(255, 140, 40, 255), stroke_width=10, stroke_fill=(5, 7, 16, 255))
out = pil.convert("RGB").resize((1280, 720), Image.LANCZOS)
p = B.ROOT / "channels/reality-check/stories/001_asteroid-defence/long/output/001_thumbnail.png"
out.save(p)
print(p)
