from PIL import Image
ts = ["134.9","135.2","144","145.3"]
sh = Image.new("RGB", (1280, 720))
for k, t in enumerate(ts): sh.paste(Image.open(f"review/fx_{t}.png"), ((k % 2) * 640, (k // 2) * 360))
sh.save("review/fixed_check.png")

