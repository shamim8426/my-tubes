import numpy as np, subprocess
FF="D:/Story-Channel/tools/ffmpeg/ffmpeg.exe"; P="D:/Story-Channel/long-videos/long_01/output/"
for f in ["long_01_work/music.wav","long_01.mp4"]:
    r=subprocess.run([FF,"-v","error","-i",P+f,"-vn","-ac","1","-ar","48000","-f","f32le","-"],capture_output=True)
    x=np.frombuffer(r.stdout,np.float32)
    db=lambda s:10*np.log10(np.mean(s**2)+1e-15)
    for a0,b0 in [(97.0,104.0),(222.0,226.5),(232.0,237.5)]:
        print(f, a0,b0, " ".join("%.0f"%db(x[int(t*48000):int((t+0.25)*48000)]) for t in np.arange(a0,b0,0.25)))
