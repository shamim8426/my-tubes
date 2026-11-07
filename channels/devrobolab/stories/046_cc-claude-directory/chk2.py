from PIL import Image
ts = ["0170","0171","0172","0173","0174","0175","0176","0177"]
# v_ index = t*4 + 1
idx = [int(x*4)+1 for x in (42.0, 42.25, 42.5, 42.75, 43.0, 60.5, 60.75, 61.25)]
sh = Image.new("RGB", (480*4, 270*2))
for k, i in enumerate(idx): sh.paste(Image.open(f"review/v_{i:04d}.png"), ((k % 4) * 480, (k // 4) * 270))
sh.save("review/blankchk.png")
