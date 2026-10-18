import sys, json, wave, subprocess, numpy as np
sys.path.insert(0, r"D:\Story-Channel\scripts")
import make_short as m
from pathlib import Path
S = Path(r"D:\Story-Channel\channels\dadi-ki-kahaniyan\stories\001_lalchi-halwai")
sh = S/"shorts/short_01_jadui-kadhai"; W = sh/"output/short_01_jadui-kadhai_work"; R=sh/"review/r3"
lines = json.load(open(sh/"lines.json", encoding="utf8"))
def rd(p):
    with wave.open(str(p)) as w: return np.frombuffer(w.readframes(w.getnframes()),np.int16).astype(np.float32)/32768, w.getframerate()
def voicing(x,sr):
    n=int(.04*sr); hop=int(.02*sr); v=[]; jit=[]
    for i in range(0,len(x)-n,hop):
        f=x[i:i+n]-x[i:i+n].mean()
        if np.sqrt(np.mean(f**2))<0.03: continue
        c=np.correlate(f,f,'full')[n-1:]; lo,hi=int(sr/400),int(sr/70); k=lo+np.argmax(c[lo:hi]); v.append(c[k]/c[0])
    return np.mean(v)
def hf(x,sr):  # share of energy above 4 kHz (phasing/metallic artefacts push this around)
    X=np.abs(np.fft.rfft(x))**2; f=np.fft.rfftfreq(len(x),1/sr); return 10*np.log10(X[f>4000].sum()/X.sum())
for i,l in enumerate(lines):
    raw = S/"audio/tts_cache"/m.tts_key(l["text"], l["speaker"])
    ref = R/f"ref_{i+1}.wav"  # same chain at 1.0x
    chain = m.pitch_filter(m.CAST[l["speaker"]][2], m.SR) or "anull"
    subprocess.run([str(m.FFMPEG),"-y","-v","error","-i",str(raw),"-af",chain,"-ac","1","-ar","24000","-sample_fmt","s16",str(ref)],check=True)
    xr,sr=rd(ref); xo,_=rd(W/f"line_{i+1:02d}_{l['speaker']}.wav")
    tr=np.frombuffer(m.trim((xr*32767).astype(np.int16).tobytes()),np.int16).astype(np.float32)/32768
    to=np.frombuffer(m.trim((xo*32767).astype(np.int16).tobytes()),np.int16).astype(np.float32)/32768
    e=int(.03*sr); db=lambda y:20*np.log10(np.sqrt(np.mean(y**2))+1e-9)
    print(f"L{i+1} voicing 1.0x {voicing(xr,sr):.3f} 1.08x {voicing(xo,sr):.3f} | HF share {hf(xr,sr):6.1f} vs {hf(xo,sr):6.1f} dB | onset30ms {db(tr[:e]):6.1f} vs {db(to[:e]):6.1f} | tail30ms {db(tr[-e:]):6.1f} vs {db(to[-e:]):6.1f}")
