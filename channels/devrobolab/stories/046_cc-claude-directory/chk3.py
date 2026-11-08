from PIL import Image
idx = [int(t*4)+1 for t in range(1, 212, 3)]
per = 24
for s in range(0, len(idx), per):
    g = idx[s:s+per]; sh = Image.new("RGB", (480*4, 270*6))
    for k, i in enumerate(g): sh.paste(Image.open(f"review/v_{i:04d}.png"), ((k % 4) * 480, (k // 4) * 270))
    sh.save(f"review/final_{s//per}.png")
print(len(idx))
