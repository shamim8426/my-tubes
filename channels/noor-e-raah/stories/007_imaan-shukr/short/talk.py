"""Talking close-up from ONE still: mouth opens/closes with the audio envelope (MediaPipe face mesh), free, local."""
import wave,math
from pathlib import Path
import numpy as np, cv2
import mediapipe as mp
from mediapipe.tasks import python as mpt
from mediapipe.tasks.python import vision
HERE=Path(__file__).resolve().parent
MODEL=str(HERE.parent/"anim/face_landmarker.task")
UP=[78,191,80,81,82,13,312,311,310,415,308]
LO=[78,95,88,178,87,14,317,402,318,324,308]
_lm=None
def landmarker():
    global _lm
    if _lm is None:
        import os,urllib.request
        if not os.path.exists(MODEL):
            os.makedirs(os.path.dirname(MODEL),exist_ok=True)
            urllib.request.urlretrieve("https://storage.googleapis.com/mediapipe-models/face_landmarker/face_landmarker/float16/1/face_landmarker.task",MODEL)
        o=vision.FaceLandmarkerOptions(base_options=mpt.BaseOptions(model_asset_path=MODEL),num_faces=1,min_face_detection_confidence=0.2,min_face_presence_confidence=0.2)
        _lm=vision.FaceLandmarker.create_from_options(o)
    return _lm
def load_img(path,W=1080,H=1920):
    im=cv2.imread(str(path)); im=cv2.resize(im,(W,H),interpolation=cv2.INTER_LANCZOS4); return im
def face_pts(img):
    rgb=cv2.cvtColor(img,cv2.COLOR_BGR2RGB)
    r=landmarker().detect(mp.Image(image_format=mp.ImageFormat.SRGB,data=rgb))
    if not r.face_landmarks: raise RuntimeError("no face")
    h,w=img.shape[:2]
    return np.array([[p.x*w,p.y*h] for p in r.face_landmarks[0]],dtype=np.float32)
def envelope(wav,fps=30,total=None):
    with wave.open(str(wav)) as w:
        sr=w.getframerate(); x=np.frombuffer(w.readframes(w.getnframes()),dtype=np.int16).astype(np.float32)/32768
    n=int(len(x)/sr*fps)+1
    hop=sr/fps; rms=np.array([np.sqrt(np.mean(x[int(i*hop):int((i+1)*hop)+int(hop*0.5)]**2)+1e-9) for i in range(n)])
    ref=np.percentile(rms,92)+1e-6
    o=np.clip((rms/ref),0,1.2)**0.85
    o[rms<ref*0.12]=0
    s=np.zeros_like(o); v=0
    for i,t in enumerate(o):  # fast attack, slower release
        v=v+(t-v)*(0.7 if t>v else 0.4); s[i]=v
    return np.clip(s,0,1)
class Talker:
    def __init__(self,img,pts=None):
        self.setup(img,pts)
    def setup(self,img,pts=None):
        self.img=img; self.p=face_pts(img) if pts is None else pts; p=self.p
        self.w=float(np.linalg.norm(p[61]-p[291])); self.cx=float((p[61][0]+p[291][0])/2)
        self.up=p[UP]; self.lo=p[LO]
        self.y13=float(p[13][1]); self.y14=float(p[14][1]); self.chin=float(p[152][1])
        w=self.w; self.x0=int(self.cx-1.3*w); self.x1=int(self.cx+1.3*w)
        self.y0=int(self.y13-0.9*w); self.y1=int(self.chin+0.6*w)
        self.y0=max(self.y0,0); self.y1=min(self.y1,img.shape[0]); self.x0=max(self.x0,0); self.x1=min(self.x1,img.shape[1])
        ys,xs=np.mgrid[self.y0:self.y1,self.x0:self.x1].astype(np.float32); self.xs,self.ys=xs,ys
        dx=(xs-self.cx)/(0.58*w); self.wx=np.exp(-dx*dx)
        t=np.clip((ys-(self.y13-0.01*w))/max(self.y14-self.y13+0.12*w,2.0),0,1); a=t*t*(3-2*t)  # 0 at upper lip, 1 at lower lip
        below=np.clip((ys-self.chin)/(0.45*w),0,1); b=1-below*below*(3-2*below)
        self.wy=a*b
        self.cont=0
    def frame(self,o):
        img=self.img; g=o*0.28*self.w
        out=img.copy()
        if g<0.8: return out
        dy=g*self.wx*self.wy
        roi=img[self.y0:self.y1,self.x0:self.x1]
        mapx=self.xs; mapy=self.ys-dy
        warped=cv2.remap(img,mapx,mapy,cv2.INTER_CUBIC,borderMode=cv2.BORDER_REFLECT)
        out[self.y0:self.y1,self.x0:self.x1]=warped
        w=self.w; cx=self.cx
        shift=np.array([0.85*g*max(0.0,1-((x-cx)/(0.5*w))**2)**0.7 for x in self.lo[:,0]],dtype=np.float32)
        lo=self.lo.copy(); lo[:,1]+=shift
        poly=np.concatenate([self.up,lo[::-1]]).astype(np.int32)
        H,W=out.shape[:2]
        mask=np.zeros((H,W),np.uint8); cv2.fillPoly(mask,[poly],255)
        inner=np.zeros((H,W,3),np.float32); inner[:]=(28,14,40)  # BGR dark mouth
        # teeth band under the upper lip
        th=min(g*0.30,0.055*w); teeth=np.zeros((H,W),np.uint8)
        tp=np.concatenate([self.up,(self.up+np.array([0,th],np.float32))[::-1]]).astype(np.int32); cv2.fillPoly(teeth,[tp],255)
        # tongue: lower part of the opening
        tong=np.zeros((H,W),np.uint8)
        tl=np.concatenate([(lo-np.array([0,g*0.45],np.float32)),lo[::-1]]).astype(np.int32); cv2.fillPoly(tong,[tl],255)
        m=cv2.GaussianBlur(mask,(0,0),1.8).astype(np.float32)/255
        layer=inner.copy()
        tm=(cv2.GaussianBlur(tong,(0,0),2).astype(np.float32)/255)[...,None]; layer=layer*(1-tm)+np.array((90,70,170),np.float32)*tm
        te=(cv2.GaussianBlur(teeth,(0,0),1.6).astype(np.float32)/255)[...,None]; layer=layer*(1-te)+np.array((196,206,214),np.float32)*te
        out=(out.astype(np.float32)*(1-m[...,None])+layer*m[...,None]).astype(np.uint8)
        return out
