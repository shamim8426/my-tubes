import json, wave, numpy as np, re, hashlib
P="D:/Story-Channel/long-videos/long_01/"; SR=24000
lines=json.load(open(P+"lines.json",encoding="utf-8")); t=json.load(open(P+"output/review/rr2/timed.json"))
cl=lambda s:len(re.sub(r"[^\u0900-\u097F\w]","",s))
def trim(b):
    x=np.frombuffer(b,np.int16).astype(np.float32)/32768; hop=240
    lev=20*np.log10(np.sqrt(np.mean(x[:len(x)//hop*hop].reshape(-1,hop)**2,axis=1))+1e-9)
    v=np.where(lev>lev.max()-35)[0]; s0=max(0,v[0]*hop-240); e0=min(len(x),(v[-1]+1)*hop+int(0.12*SR)); return b[s0*2:e0*2]
print("-- whisper status")
for i,l in enumerate(lines):
    if "pause" in l: continue
    w=wave.open(P+f"audio/line_{i+1:02d}_{l['speaker']}.wav"); d=trim(w.readframes(w.getnframes()))
    k=P+"audio/tts_cache/words_"+hashlib.sha1(d).hexdigest()[:16]+".json"
    try: ww=json.load(open(k,encoding="utf-8")); cov=sum(cl(x[2]) for x in ww)/max(1,sum(cl(x) for x in l["text"].split()))
    except FileNotFoundError: ww=None; cov=None
    st="NO CACHE" if ww is None else ("whisper %.0f%%"%(cov*100) if ww and 0.75<=cov<=1.35 else "PROPORTIONAL cov %s"%cov)
    if st.startswith("whisper")==False or True:
        if not st.startswith("whisper"): print(" line",i+1,l["speaker"],st)
print("-- srt")
s=open(P+"output/long_01.srt",encoding="utf-8").read().replace("\r","")
cues=[]
for blk in s.strip().split("\n\n"):
    ls=blk.split("\n"); a,b=ls[1].split(" --> ")
    f=lambda x:int(x[:2])*3600+int(x[3:5])*60+int(x[6:8])+int(x[9:])/1000
    cues.append((int(ls[0]),f(a),f(b)," ".join(ls[2:])))
print("cues",len(cues),"min dur %.3f"%min(c[2]-c[1] for c in cues))
short=[c for c in cues if c[2]-c[1]<0.45]; print("cues <0.45s:",short)
sp=[o for o in t if o["sp"]!="_pause"]
bad=[]; joined={}
for c in cues:
    own=[o for o in sp if c[1]>=o["start"]-0.3 and c[2]<=o["end"]+0.3]
    if not own: bad.append(c)
    else: joined.setdefault(own[0]["n"],[]).append(c[3])
print("cues outside any line ±0.3:",bad)
for o in sp:
    txt=" ".join(joined.get(o["n"],[])); ref=lines[o["n"]-1]["text"]
    if txt.split()!=ref.split(): print("TEXT MISMATCH line",o["n"],"|",txt,"|",ref)
ov=[(a,b) for a,b in zip(cues,cues[1:]) if b[1]<a[2]-1e-3]; print("overlaps",ov)
print("first/last", cues[0][:3], cues[-1][:3])
