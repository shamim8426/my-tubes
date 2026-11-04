import sys
from PIL import Image
from pathlib import Path
d=Path(sys.argv[1]); fs=sorted(d.glob("t_*.png"))
for n in range(0,len(fs),6):
    ims=[Image.open(f).convert("RGB").resize((360,640)) for f in fs[n:n+6]]
    s=Image.new("RGB",(360*len(ims),640),"white")
    for i,im in enumerate(ims): s.paste(im,(i*360,0))
    s.save(d/f"sheet{n//6}.png")
