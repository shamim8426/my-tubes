import numpy as np, subprocess
FF="D:/Story-Channel/tools/ffmpeg/ffmpeg.exe"; P="D:/Story-Channel/long-videos/long_01/output/"
def rd(f):
    r=subprocess.run([FF,"-v","error","-i",f,"-ac","1","-ar","8000","-f","f32le","-"],capture_output=True); return np.frombuffer(r.stdout,np.float32)
mus=rd(P+"long_01_work/music.wav")
for name,seg_start,probe in [("dukh/Heartbreaking.mp3",67.07,80.0),("seekh/Touching_Moments_Two_Higher.mp3",224.59,228.0)]:
    tr=rd("D:/Story-Channel/assets/music/"+name)
    snip=mus[int(probe*8000):int((probe+3)*8000)]
    best=max(((np.dot(snip,tr[k:k+len(snip)])/ (np.linalg.norm(tr[k:k+len(snip)])*np.linalg.norm(snip)+1e-9),k/8000) for k in range(0,int(40*8000),40)))
    print(name,"best corr %.3f at track time %.2f -> offset %.2f"%(best[0],best[1],best[1]-(probe-seg_start)))
