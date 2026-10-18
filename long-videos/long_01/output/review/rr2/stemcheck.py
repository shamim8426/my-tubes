import json, wave, numpy as np, subprocess
P="D:/Story-Channel/long-videos/long_01/output/"; FF="D:/Story-Channel/tools/ffmpeg/ffmpeg.exe"
def rd(f, extra=[]):
    r=subprocess.run([FF,"-v","error","-i",f,*extra,"-ac","2","-ar","48000","-f","f32le","-"],capture_output=True)
    return np.frombuffer(r.stdout,np.float32).reshape(-1,2)
mix=rd(P+"long_01_work/mix.wav"); mus=rd(P+"long_01_work/music.wav"); voi=rd(P+"long_01_work/voice.wav")
n=min(len(mix),len(mus),len(voi)); mix,mus,voi=mix[:n],mus[:n],voi[:n]
res=mix-mus-voi
t=json.load(open(P+"review/rr2/timed.json"))
db=lambda x:10*np.log10(np.mean(x**2)+1e-15)
print("whole: mix %.1f  music %.1f  voice %.1f  residual(mix-music-voice) %.1f dB"%(db(mix),db(mus),db(voi),db(res)))
# residual excluding sfx: check residual vs music in pause sections
for o in t:
    if o['sp']=='_pause':
        a,b=int(o['start']*48000),int(o['end']*48000)
        print("pause %.2f-%.2f: music rms %.1f dB, mix %.1f dB, min 0.5s-window music %.1f dB"%(o['start'],o['end'],db(mus[a:b]),db(mix[a:b]),
              min(db(mus[k:k+24000]) for k in range(a,b-24000,4800))))
# per-scene-ish: voice rms vs music rms per line
out=[]
for o in t:
    if o['sp']=='_pause': continue
    a,b=int(o['start']*48000),int(o['end']*48000)
    out.append((o['n'],o['sp'],o['start'],db(voi[a:b])-db(mus[a:b])))
d=[x[3] for x in out]
print("per-line voice-minus-music RMS dB: min %.1f max %.1f median %.1f"%(min(d),max(d),np.median(d)))
for x in sorted(out,key=lambda x:x[3])[:6]: print("  closest line",x)
# music near pauses with lead 2s
for a0,b0 in [(98.1,103.1),(222.6,225.6),(232.8,236.8)]:
    a,b=int(a0*48000),int(b0*48000)
    w=[db(mus[k:k+12000]) for k in range(a,b-12000,2400)]
    print("window %.1f-%.1f music 0.25s rms min %.1f max %.1f"%(a0,b0,min(w),max(w)))
