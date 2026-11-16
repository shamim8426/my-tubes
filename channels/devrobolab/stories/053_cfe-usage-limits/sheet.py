from PIL import Image
import glob, sys
fs = sorted(glob.glob("review/d_*.png"))
for n in range(0, len(fs), 10):
    sub = fs[n:n+10]; ims = [Image.open(f).resize((270, 480)) for f in sub]
    sh = Image.new("RGB", (270*5, 480*2), "white")
    for i, im in enumerate(ims): sh.paste(im, ((i%5)*270, (i//5)*480))
    sh.save(f"review/sheet{n//10+1}.png"); print(sub)
