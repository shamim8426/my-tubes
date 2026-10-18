import wave, numpy as np
from pathlib import Path
R=Path(r"D:\Story-Channel\channels\dadi-ki-kahaniyan\stories\001_lalchi-halwai\shorts\short_01_jadui-kadhai\review\r3"); W=R.parent.parent/"output/short_01_jadui-kadhai_work"
def rd(p):
    with wave.open(str(p)) as w: return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
def prof(x,sr=24000):
    hop=240; lev=20*np.log10(np.sqrt(np.mean(x[:len(x)//hop*hop].reshape(-1,hop)**2,1))+1e-9); return lev
for name,p,sc in [("1.0x",R/"ref_6.wav",1.0),("1.08x",W/"line_06_dadi_story.wav",1.08)]:
    lev=prof(rd(p)); thr=lev.max()-35; v=np.where(lev>thr)[0]
    print(name,"max",round(lev.max(),1),"thr",round(thr,1),"first voiced frame",v[0]*0.01,"s (src time",round(v[0]*0.01*sc,3),")")
    print("  lev 10ms frames around:", [round(a) for a in lev[max(0,v[0]-15):v[0]+8]])
