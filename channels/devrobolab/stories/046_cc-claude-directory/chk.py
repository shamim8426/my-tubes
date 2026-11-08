import glob, numpy as np
from PIL import Image
fs = sorted(glob.glob("review/v_*.png")); bad = []; prev = None
for i, f in enumerate(fs):
    a = np.asarray(Image.open(f).convert("RGB")).astype(int)
    reg = a[34:232, :, :]   # y 120..930 of 1080 -> content area
    lum = reg.sum(axis=2); frac = (lum > 120).mean()
    if frac < 0.012: bad.append((round(i / 4, 2), round(float(frac), 4)))
print("n", len(fs), "low-content samples:", bad)
