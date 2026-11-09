"""Free full-motion clips for a Noor Imaan Short: LTX-Video image-to-video on the Kaggle free T4 (user 2026-11-09, RS 0).
    python scripts/ltx_kaggle.py push   <story dir>   # reads <story>/short/motion.json, pushes the kernel
    python scripts/ltx_kaggle.py status <story dir>
    python scripts/ltx_kaggle.py fetch  <story dir>   # downloads shotN.mp4 into <story>/kaggle/clips
motion.json: [{"n":1,"img":"images/v3_girl_sad.png","motion":"A cute girl ... (name the motion)","seed":21}, ...]
Learned: 73 frames at 480x832 fits a T4 (97 and 81 ran out of memory); ~10 min per clip after a ~4 min model load;
guidance 5 and an explicit motion sentence (3.0 = almost static); the Kaggle queue can stall for hours. Needs
KAGGLE_API_TOKEN_FREE in .env (username shamimali9334).
"""
import base64, io, json, os, re, subprocess, sys
from pathlib import Path
from PIL import Image
ROOT = Path(__file__).resolve().parent.parent
USER = "shamimali9334"
def env():
    e = dict(os.environ)
    for l in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
        if l.startswith("KAGGLE_API_TOKEN_FREE="):
            e["KAGGLE_API_TOKEN"] = l.split("=", 1)[1].strip()
    return e
def kaggle(*a):
    exe = Path(sys.executable).parent / "kaggle.exe"
    exe = str(exe) if exe.exists() else "kaggle"
    return subprocess.run([exe, *a], env=env(), capture_output=True, text=True)
def slug(story): return "noor-ltx-" + re.sub(r"[^a-z0-9]+", "-", Path(story).name.lower()).strip("-")[:30]
def push(story):
    story = Path(story); shots = json.loads((story / "short" / "motion.json").read_text(encoding="utf-8"))
    imgs = {}
    for s in shots:
        if s["img"] not in imgs:
            im = Image.open(story / s["img"]).convert("RGB").resize((480, 832), Image.LANCZOS)
            b = io.BytesIO(); im.save(b, "JPEG", quality=90); imgs[s["img"]] = base64.b64encode(b.getvalue()).decode()
    S = [(s["n"], s["img"], s["motion"], s.get("seed", 7)) for s in shots]
    code = f'''
import os,base64,io,time,subprocess,sys,gc
os.environ["HF_HOME"]="/kaggle/temp/hf"
os.environ["PYTORCH_CUDA_ALLOC_CONF"]="expandable_segments:True"
subprocess.run([sys.executable,"-m","pip","install","-q","-U","diffusers","transformers","accelerate","sentencepiece","imageio","imageio-ffmpeg"],check=True)
import torch
from PIL import Image
from diffusers import LTXImageToVideoPipeline
from diffusers.utils import export_to_video
IMGS={json.dumps(imgs)}
SHOTS={json.dumps(S)}
t0=time.time()
pipe=LTXImageToVideoPipeline.from_pretrained("Lightricks/LTX-Video",torch_dtype=torch.bfloat16)
pipe.enable_model_cpu_offload(); pipe.vae.enable_tiling()
print("loaded",time.time()-t0,flush=True)
neg="worst quality, inconsistent motion, blurry, jittery, distorted, morphing face, changing identity, text, watermark, mouth wide open"
for n,name,motion,seed in SHOTS:
    try:
        img=Image.open(io.BytesIO(base64.b64decode(IMGS[name]))).convert("RGB")
        prompt=motion+" Clearly visible natural head and body movement, gentle cinematic feel, mouth closed or barely moving, 3D animated film, warm golden light"
        t1=time.time()
        out=pipe(image=img,prompt=prompt,negative_prompt=neg,width=480,height=832,num_frames=73,num_inference_steps=30,guidance_scale=5.0,generator=torch.Generator().manual_seed(seed)).frames[0]
        export_to_video(out,f"/kaggle/working/shot{{n}}.mp4",fps=24)
        print("shot",n,"done",time.time()-t1,flush=True)
    except Exception as e:
        print("shot",n,"FAILED",str(e)[:200],flush=True)
    del_ = gc.collect(); torch.cuda.empty_cache()
print("ALL DONE")
'''
    d = story / "kaggle" / "ltx"; d.mkdir(parents=True, exist_ok=True)
    (d / "script.py").write_text(code, encoding="utf-8")
    (d / "kernel-metadata.json").write_text(json.dumps({"id": f"{USER}/{slug(story)}", "title": slug(story), "code_file": "script.py", "language": "python", "kernel_type": "script", "is_private": True, "enable_gpu": True, "enable_internet": True, "dataset_sources": [], "competition_sources": [], "kernel_sources": []}, indent=1))
    r = kaggle("kernels", "push", "-p", str(d)); print(r.stdout.strip() or r.stderr.strip())
def status(story):
    r = kaggle("kernels", "status", f"{USER}/{slug(story)}"); print((r.stdout or r.stderr).strip().splitlines()[-1])
def fetch(story):
    out = Path(story) / "kaggle" / "clips"; out.mkdir(parents=True, exist_ok=True)
    r = kaggle("kernels", "output", f"{USER}/{slug(story)}", "-p", str(out), "--file-pattern", "shot.*mp4|.*log")
    print(sorted(p.name for p in out.glob("shot*.mp4")))
if __name__ == "__main__":
    cmd, story = sys.argv[1], sys.argv[2]
    {"push": push, "status": status, "fetch": fetch}[cmd](story)
