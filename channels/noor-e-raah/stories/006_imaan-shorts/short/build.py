import json,subprocess,sys,wave
from pathlib import Path
import numpy as np
from PIL import Image,ImageDraw,ImageFilter,ImageFont
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/"tools")); sys.path.insert(0,str(ROOT/"scripts"))
import parallax, text_pil
parallax.MAX_SECONDS=20
FF=str(ROOT/"tools/ffmpeg/ffmpeg.exe")
D=ROOT/"channels/noor-e-raah/stories/006_imaan-shorts"; W=D/"short"/"work"; W.mkdir(exist_ok=True)
lines=json.load(open(D/"short/lines.json",encoding="utf-8"))
PRESETS=["push_in","pan_right","push_in","pull_out","push_in","pan_left","push_in","push_in"]
def dur(p):
    with wave.open(str(p)) as w: return w.getnframes()/w.getframerate()
# ayah card
def ayah_card():
    out=D/"images/ayah.png"
    bg=Image.open(D/"images/s6.png").convert("RGB").resize((1080,1920)).filter(ImageFilter.GaussianBlur(28))
    dark=Image.new("RGB",bg.size,(18,12,6)); bg=Image.blend(bg,dark,0.72)
    bg.save(out)
ayah_card()
PAD=0.35; t=0.0; tl=[]
for i,l in enumerate(lines):
    a=D/f"audio/l{l['n']:02d}.wav"; d=dur(a)+PAD+(0.5 if i==len(lines)-1 else 0)
    tl.append((l,a,t,d)); t+=d
TOTAL=t; print("total",round(TOTAL,1))
clips=[]
for i,(l,a,st,d) in enumerate(tl):
    c=W/f"c{l['n']:02d}.mp4"
    if not c.exists():
        parallax.render_clip(D/f"images/{l['img']}.png",c,seconds=d,preset=PRESETS[i],fmt="short",mode="zoom" if l["img"]=="ayah" else "auto")
    clips.append(c)
(W/"list.txt").write_text("".join(f"file '{c.as_posix()}'\n" for c in clips))
# subtitles + ayah via libass (Raqm is not available in PIL on Windows)
def ts(x):
    h=int(x//3600);m=int(x%3600//60);sec=x%60
    return f"{h}:{m:02d}:{sec:05.2f}"
head=("[Script Info]\nScriptType: v4.00+\nPlayResX: 1080\nPlayResY: 1920\nWrapStyle: 0\nScaledBorderAndShadow: yes\n\n"
"[V4+ Styles]\nFormat: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding\n"
"Style: Sub,Mukta Bold,80,&H00FFFFFF,&H00FFFFFF,&H8C0A0C14,&H8C0A0C14,0,0,0,0,100,100,0,0,3,16,0,2,90,90,430,1\n"
"Style: Ayah,Amiri,470,&H0078C8F0,&H00FFFFFF,&H00000000,&H99000000,0,0,0,0,100,100,0,0,1,0,3,8,0,0,0,0\n"
"Style: Tr,Mukta Bold,86,&H00FFFFFF,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,3,2,8,0,0,0,1\n"
"Style: Src,Mukta Bold,52,&H006EAAC8,&H00FFFFFF,&H90000000,&H00000000,0,0,0,0,100,100,0,0,1,2,1,8,0,0,0,1\n\n"
"[Events]\nFormat: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text\n")
ev=[]
for i,(l,a_,st,d) in enumerate(tl):
    e=st+d-0.05
    if l["n"]==7:
        ev.append(r"Dialogue: 0,%s,%s,Ayah,,0,0,0,,{\pos(540,520)\fad(300,200)}إِنَّ مَعَ ٱلْعُسْرِ يُسْرًا"%(ts(st),ts(e)))
        ev.append(r"Dialogue: 0,%s,%s,Tr,,0,0,0,,{\pos(540,980)\fad(300,200)}बेशक, हर मुश्किल के साथ\Nआसानी है।"%(ts(st),ts(e)))
        ev.append(r"Dialogue: 0,%s,%s,Src,,0,0,0,,{\pos(540,1260)\fad(300,200)}सूरह अल-इन्शिराह · आयत 94:6"%(ts(st),ts(e)))
    else:
        ev.append(f"Dialogue: 0,{ts(st)},{ts(e)},Sub,,0,0,0,,{l['text']}")
open(W/"subs.ass","w",encoding="utf-8").write(head+"\n".join(ev)+"\n")
# voice
sr=24000; buf=np.zeros(int(TOTAL*sr)+sr,dtype=np.float32)
for l,a,st,d in tl:
    with wave.open(str(a)) as w: x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    s=int(st*sr)+int(0.12*sr); buf[s:s+len(x)]+=x
buf=buf[:int(TOTAL*sr)]
pk=np.abs(buf).max(); buf=buf/pk*0.85
with wave.open(str(W/"voice.wav"),"wb") as w:
    w.setnchannels(1);w.setsampwidth(2);w.setframerate(sr);w.writeframes((buf*32767).astype(np.int16).tobytes())
def esc(p): return Path(p).resolve().as_posix().replace(":","\\:")
cmd=[FF,"-y","-f","concat","-safe","0","-i",str(W/"list.txt"),"-i",str(W/"voice.wav"),"-stream_loop","-1","-i",str(ROOT/"shared/music/noor/River_Flute.mp3")]
fc=(f"[0:v]subtitles=filename='{esc(W/'subs.ass')}':fontsdir='{esc(ROOT/'shared/fonts')}'[v];"
 f"[2:a]volume=0.16,afade=t=in:d=1,afade=t=out:st={TOTAL-1.2:.2f}:d=1.2[ma];[1:a][ma]amix=inputs=2:duration=first:normalize=0,loudnorm=I=-14:TP=-1.5:LRA=9[a]")
cmd+=["-filter_complex",fc,"-map","[v]","-map","[a]","-t",f"{TOTAL:.2f}","-c:v","libx264","-crf","18","-preset","medium","-pix_fmt","yuv420p","-c:a","aac","-b:a","192k","-movflags","+faststart",str(D/"short/imaan_short_01.mp4")]
r=subprocess.run(cmd,capture_output=True,text=True); print(r.returncode,r.stderr[-600:] if r.returncode else "OK")
