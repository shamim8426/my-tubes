import subprocess, sys
from PIL import Image, ImageDraw, ImageFont
F=r"D:\Story-Channel\tools\ffmpeg\ffmpeg.exe"
P=r"D:\Story-Channel\channels\dadi-ki-kahaniyan\stories\001_lalchi-halwai\shorts\short_01_jadui-kadhai\output\short_01_jadui-kadhai_preview.mp4"
R=sys.argv[1]; ts=[float(t) for t in sys.argv[3].split(",")]
font=ImageFont.truetype("arial.ttf",22); tiles=[]
for t in ts:
    f=f"{R}/p_{t:04.1f}.png"
    subprocess.run([F,"-y","-v","error","-ss",str(t),"-i",P,"-frames:v","1","-vf","scale=270:-2",f],check=True)
    im=Image.open(f).convert("RGB"); d=ImageDraw.Draw(im); d.rectangle((0,0,90,28),fill=0); d.text((4,3),f"{t:.2f}s",fill=(255,230,0),font=font); tiles.append(im)
cols=6; rows=(len(tiles)+cols-1)//cols; h=tiles[0].height
s=Image.new("RGB",(cols*270,rows*h))
for i,im in enumerate(tiles): s.paste(im,((i%cols)*270,(i//cols)*h))
s.save(f"{R}/{sys.argv[2]}")
