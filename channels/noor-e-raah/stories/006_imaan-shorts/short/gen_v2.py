import sys,base64,os,requests
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/"scripts"))
import cf_image
from dotenv import load_dotenv
load_dotenv(ROOT/".env")
OUT=ROOT/"channels/noor-e-raah/stories/006_imaan-shorts/images"
STYLE=("stylised 3D animated family-film render, soft sculpted face, big expressive kind eyes, smooth skin, rich warm golden lamp light, "
"shallow depth of field, head and shoulders close-up filling the frame, face perfectly front-facing and centered looking at the camera, "
"mouth closed and relaxed, plain modest village home background blurred, vertical 9:16, no text, no letters")
MAN="a 26-year-old South Asian man with short black hair and light stubble in a plain cream kurta"
MOM="a kind 50-year-old South Asian mother in a soft teal headscarf"
ENDP=cf_image.ENDPOINT.format(acc=os.environ["CLOUDFLARE_ACCOUNT_ID"])
TOK=os.environ.get("CLOUDFLARE_API_TOKEN_FREE") or os.environ["CLOUDFLARE_API_TOKEN"]
def gen(name,prompt,ref=None):
    f=OUT/f"{name}.png"
    if f.exists(): return
    files={"prompt":(None,prompt),"width":(None,"768"),"height":(None,"1344")}
    if ref: files["input_image_0"]=("ref.png",open(OUT/f"{ref}.png","rb"),"image/png")
    r=requests.post(ENDP,headers={"Authorization":f"Bearer {TOK}"},files=files,timeout=240)
    print(name,r.status_code,r.text[:120] if not r.ok else "ok")
    if r.ok: f.write_bytes(base64.b64decode(r.json()["result"]["image"]))
gen("v2_man_sad",f"close-up of {MAN}, tired, worried, sad eyes, {STYLE}")
gen("v2_mom_calm",f"close-up of {MOM}, warm gentle serious loving eyes, {STYLE}")
gen("v2_man_happy",f"the same man as in the reference image, same face, hair, stubble and clothes, now with a bright joyful wide smile and shining happy eyes, {STYLE}","v2_man_sad")
gen("v2_mom_happy",f"the same woman as in the reference image, same face and teal headscarf, now with a soft proud smile and teary shining happy eyes, {STYLE}","v2_mom_calm")
