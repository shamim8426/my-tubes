import json,subprocess,sys,wave,math
from pathlib import Path
import numpy as np, cv2
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[4]; D=HERE.parent
sys.path.insert(0,str(HERE))
import talk
FF=str(ROOT/"tools/ffmpeg/ffmpeg.exe"); W=HERE/"work"; W.mkdir(exist_ok=True)
FPS=30; OW,OH=1080,1920
lines=json.load(open(HERE/"lines_v3.json",encoding="utf-8"))
def dur(p):
    with wave.open(str(p)) as w: return w.getnframes()/w.getframerate()
PAD=0.4
tl=[];t=0.0
for i,l in enumerate(lines):
    a=D/f"audio/v3_l{l['n']:02d}.wav"; lead=0.25 if i==0 else 0.0
    if l["n"]==6: lead=1.6  # "next morning" card
    d=lead+dur(a)+PAD+(0.8 if i==len(lines)-1 else 0)
    tl.append(dict(l=l,a=a,st=t,lead=lead,d=d)); t+=d
TOTAL=t; print("total",round(TOTAL,1))
# zoom plan per shot (start,end,cx,cy offset) for variety
ZOOM={1:(1.00,1.07,0,0),2:(1.04,1.00,0,0.01),3:(1.06,1.14,0,0),4:(1.00,1.06,0,-0.01),5:(1.10,1.18,0,0),6:(1.02,1.00,0,0),7:(1.00,1.07,0,0)}
RENDER=not (W/'v3_video.mp4').exists()
enc=RENDER and subprocess.Popen([FF,"-y","-loglevel","error","-f","rawvideo","-pix_fmt","bgr24","-s",f"{OW}x{OH}","-r",str(FPS),"-i","-","-c:v","libx264","-crf","17","-preset","medium","-pix_fmt","yuv420p","-colorspace","bt709","-color_primaries","bt709","-color_trc","bt709",str(W/"v3_video.mp4")],stdin=subprocess.PIPE)
cache={}
for s in (tl if RENDER else []):
    l=s["l"]; n=int(round(s["d"]*FPS))
    if l["img"] not in cache: cache[l["img"]]=talk.Talker(talk.load_img(D/f"images/{l['img']}.png"))
    tk=cache[l["img"]]
    env=talk.envelope(s["a"],FPS)
    z0,z1,ox,oy=ZOOM[l["n"]]
    lead_f=int(round(s["lead"]*FPS))
    for f in range(n):
        k=f-lead_f
        o=float(env[k]) if 0<=k<len(env) else 0.0
        fr=tk.frame(o)
        p=f/max(n-1,1); e=0.5-0.5*math.cos(math.pi*p)
        z=z0+(z1-z0)*e
        sway=math.sin(2*math.pi*(f/FPS)/3.1)*0.0035
        breathe=1+0.004*math.sin(2*math.pi*(f/FPS)/2.4)
        z*=breathe
        cx=OW/2+ox*OW+sway*OW; cy=OH*0.5+oy*OH
        M=np.float32([[z,0,OW/2-z*cx],[0,z,OH/2-z*cy]])
        # keep the face a bit above centre: shift down so the face sits in the upper 60%
        M[1,2]+=0
        out=cv2.warpAffine(fr,M,(OW,OH),flags=cv2.INTER_CUBIC,borderMode=cv2.BORDER_REPLICATE)
        enc.stdin.write(out.tobytes())
    print("shot",l["n"],n,"frames",flush=True)
if RENDER: enc.stdin.close(); enc.wait()
# voice track
sr=24000; buf=np.zeros(int(TOTAL*sr)+sr,dtype=np.float32)
for s in tl:
    with wave.open(str(s["a"])) as w: x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    st=int((s["st"]+s["lead"])*sr); buf[st:st+len(x)]+=x
buf=buf[:int(TOTAL*sr)]; buf=buf/np.abs(buf).max()*0.85
with wave.open(str(W/"v3_voice.wav"),"wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((buf*32767).astype(np.int16).tobytes())
# subtitles
def ts(x): return f"{int(x//3600)}:{int(x%3600//60):02d}:{x%60:05.2f}"
head=("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
"[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
"Style: Sub,Mukta Bold,80,&H00FFFFFF,&H00FFFFFF,&H8C0A0C14,&H8C0A0C14,0,0,0,0,100,100,0,0,3,16,0,2,90,90,330,1\n"
"Style: Ayah,Amiri,250,&H0078C8F0,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,0,3,8,0,0,0,0\n"
"Style: Src,Mukta Bold,50,&H006EAAC8,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,3,2,8,0,0,0,1\n"
"Style: Card,Mukta Bold,92,&H00FFFFFF,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,4,3,8,0,0,0,1\n\n"
"[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
ev=[]
for s in tl:
    l=s["l"]; a=s["st"]+s["lead"]; e=s["st"]+s["d"]-0.05
    ev.append(f"Dialogue: 0,{ts(a)},{ts(e)},Sub,,0,0,0,,{l['text']}")
    if l["n"]==4:
        ev.append(r"Dialogue: 1,%s,%s,Ayah,,0,0,0,,{\pos(540,90)\fad(300,300)}إِنَّ مَعَ ٱلْعُسْرِ يُسْرًا"%(ts(a+1.6),ts(e)))
        ev.append(r"Dialogue: 1,%s,%s,Src,,0,0,0,,{\pos(540,330)\fad(300,300)}सूरह अल-इन्शिराह · आयत 94:6"%(ts(a+1.6),ts(e)))
    if l["n"]==6:
        ev.append(r"Dialogue: 1,%s,%s,Card,,0,0,0,,{\pos(540,300)\fad(400,500)}अगली सुबह…"%(ts(s["st"]),ts(s["st"]+1.5)))
open(W/"v3.ass","w",encoding="utf-8").write(head+"\n".join(ev)+"\n")
def esc(p): return Path(p).resolve().as_posix().replace(":","\:")
out=D/"short/imaan_short_03_cute.mp4"
fc=(f"[0:v]subtitles=filename='{esc(W/'v3.ass')}':fontsdir='{esc(ROOT/'shared/fonts')}'[v];"
 f"[2:a]volume=0.14,afade=t=in:d=1,afade=t=out:st={TOTAL-1.5:.2f}:d=1.5[ma];[1:a][ma]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
cmd=[FF,"-y","-i",str(W/"v3_video.mp4"),"-i",str(W/"v3_voice.wav"),"-stream_loop","-1","-i",str(ROOT/"shared/music/noor/Quietude_Sections_Merged.mp3"),"-filter_complex",fc,"-map","[v]","-map","[a]","-t",f"{TOTAL:.2f}","-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",str(out)]
r=subprocess.run(cmd,capture_output=True,text=True); print(r.returncode,r.stderr[-500:] if r.returncode else "OK",out)
