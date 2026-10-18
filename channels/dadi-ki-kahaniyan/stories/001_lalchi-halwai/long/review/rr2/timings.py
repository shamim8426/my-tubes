import json, wave, numpy as np, sys
P="D:/Story-Channel/long-videos/long_01/"
SR=24000; GAP=0.30; END_HOLD=1.5; TAIL=0.12
lines=json.load(open(P+"lines.json",encoding="utf-8"))
def trim(x):
    hop=int(0.01*SR)
    lev=20*np.log10(np.sqrt(np.mean(x[:len(x)//hop*hop].reshape(-1,hop)**2,axis=1))+1e-9)
    v=np.where(lev>lev.max()-35)[0]
    s0=max(0,v[0]*hop-int(0.01*SR)); e0=min(len(x),(v[-1]+1)*hop+int(TAIL*SR))
    return x[s0:e0]
t=0.0; out=[]; pcm=[]
for i,l in enumerate(lines):
    if "pause" in l:
        gap=GAP if i else 0
        s=t+gap; t=s+l["pause"]; pcm.append(np.zeros(int(round((gap+l["pause"])*SR))))
        out.append(dict(n=i+1,sp="_pause",scene=l["scene"],start=s,end=t)); continue
    w=wave.open(P+f"audio/line_{i+1:02d}_{l['speaker']}.wav"); x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
    d=trim(x)
    if i:
        gap=GAP+l.get("pause_before",0); pcm.append(np.zeros(int(round(gap*SR)))); t+=gap
    s=t; pcm.append(d); t+=len(d)/SR
    out.append(dict(n=i+1,sp=l["speaker"],scene=l["scene"],start=s,end=t))
tot=t+END_HOLD
pcm.append(np.zeros(int(round(END_HOLD*SR))))
rec=np.concatenate(pcm)
w=wave.open(P+"output/long_01_work/voice.wav"); vw=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
print("total",tot,"rec samples",len(rec),"voice.wav samples",len(vw), "sr",w.getframerate())
m=min(len(rec),len(vw)); print("max abs diff", np.abs(rec[:m]-vw[:m]).max())
json.dump(out,open(P+"output/review/rr2/timed.json","w"),indent=0)
for o in out: print(f"{o['n']:2d} sc{o['scene']:2d} {o['sp']:10s} {o['start']:7.2f}-{o['end']:7.2f}")
