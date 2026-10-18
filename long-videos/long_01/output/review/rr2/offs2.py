import numpy as np, subprocess
FF="D:/Story-Channel/tools/ffmpeg/ffmpeg.exe"; P="D:/Story-Channel/long-videos/long_01/output/"
def rd(f):
    r=subprocess.run([FF,"-v","error","-i",f,"-ac","1","-ar","8000","-f","f32le","-"],capture_output=True); return np.frombuffer(r.stdout,np.float32)
mus=rd(P+"long_01_work/music.wav"); tr=rd("D:/Story-Channel/assets/music/dukh/Heartbreaking.mp3")
for probe in [70.0,85.0,95.0]:
    snip=mus[int(probe*8000):int((probe+3)*8000)]
    c=[(np.dot(snip,tr[k:k+len(snip)])/(np.linalg.norm(tr[k:k+len(snip)])*np.linalg.norm(snip)+1e-9),k/8000) for k in range(0,len(tr)-len(snip),8)]
    b=max(c); print(probe,"corr %.3f track %.3f offset(seg start 67.07) %.2f"%(b[0],b[1],b[1]-(probe-67.07)))
