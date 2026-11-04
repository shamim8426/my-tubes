import sys,glob
from PIL import Image
d=sys.argv[1]; fs=sorted(glob.glob(d+"/t_*.png")); ims=[Image.open(f).convert("RGB").resize((360,640)) for f in fs]
cols=5; rows=(len(ims)+cols-1)//cols
S=Image.new("RGB",(cols*360,rows*640),"white")
for i,im in enumerate(ims): S.paste(im,((i%cols)*360,(i//cols)*640))
S.save(sys.argv[2]); print(len(ims))
