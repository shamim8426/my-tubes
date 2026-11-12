import sys, glob
from PIL import Image, ImageDraw
fs = sorted(glob.glob("review/F_*.png"))
fs = [f for f in fs if "sheet" not in f]
per = 6
for s in range(0, len(fs), per):
    grp = fs[s:s + per]; sh = Image.new("RGB", (1920, 540 * 3), (0, 0, 0))
    for i, f in enumerate(grp):
        im = Image.open(f).resize((960, 540)); ImageDraw.Draw(im).text((10, 560 - 40), f[-10:-4], fill=(255, 255, 0)); sh.paste(im, ((i % 2) * 960, (i // 2) * 540))
    sh.save(f"review/sheet_{s // per}.png")
print(len(fs))
