import sys, json, wave, numpy as np
sys.path.insert(0, r"D:\Story-Channel\scripts")
import make_short as m
from pathlib import Path
S = Path(r"D:\Story-Channel\channels\dadi-ki-kahaniyan\stories\001_lalchi-halwai")
sh = S/"shorts/short_01_jadui-kadhai"; W = sh/"output/short_01_jadui-kadhai_work"
lines = json.load(open(sh/"lines.json", encoding="utf8"))
def rd(p):
    with wave.open(str(p)) as w:
        sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768
        if w.getnchannels()>1: x=x.reshape(-1,w.getnchannels()).mean(1)
    return x,sr
def f0(x,sr):
    # median autocorr pitch over voiced frames
    hop=int(.02*sr); n=int(.04*sr); ps=[]
    for i in range(0,len(x)-n,hop):
        f=x[i:i+n]; 
        if np.sqrt(np.mean(f**2))<0.03: continue
        f=f-f.mean(); c=np.correlate(f,f,'full')[n-1:]
        lo,hi=int(sr/400),int(sr/70); k=lo+np.argmax(c[lo:hi])
        if c[k]>0.4*c[0]: ps.append(sr/k)
    return np.median(ps) if ps else 0
for i,l in enumerate(lines):
    raw = S/"audio/tts_cache"/m.tts_key(l["text"], l["speaker"])
    out = W/f"line_{i+1:02d}_{l['speaker']}.wav"
    xr,sr=rd(raw); xo,so=rd(out)
    # trimmed versions
    tr=np.frombuffer(m.trim((np.clip(xo,-1,1)*32767).astype(np.int16).tobytes()),np.int16).astype(np.float32)/32768
    edge=lambda y,a,b: 20*np.log10(np.sqrt(np.mean(y[a:b]**2))+1e-9)
    e=int(.03*so)
    pk=20*np.log10(np.abs(xo).max()+1e-9)
    print(f"L{i+1} {l['speaker']:10s} raw {len(xr)/sr:5.2f}s out {len(xo)/so:5.2f}s ratio {len(xr)/sr/(len(xo)/so):.3f} "
          f"f0 raw {f0(xr,sr):5.0f} out {f0(xo,so):5.0f} | trimmed {len(tr)/so:5.2f}s first30ms {edge(tr,0,e):6.1f}dB last30ms {edge(tr,-e,None):6.1f}dB peak {pk:5.1f} raw_exists {raw.exists()}")
# voice.wav gaps
v,sr=rd(W/"voice.wav"); hop=int(.01*sr)
lev=20*np.log10(np.sqrt(np.mean(v[:len(v)//hop*hop].reshape(-1,hop)**2,1))+1e-9)
sil=lev<-50; runs=[]; s=None
for k,b in enumerate(sil):
    if b and s is None: s=k
    if not b and s is not None:
        if k-s>=5: runs.append((s/100,k/100))
        s=None
if s is not None: runs.append((s/100,len(sil)/100))
print("voice.wav", len(v)/sr, "silences>=50ms:", [(a,round(b-a,2)) for a,b in runs])
