import sys,base64,os,requests
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/"scripts"))
import cf_image
from dotenv import load_dotenv
load_dotenv(ROOT/".env")
OUT=Path(__file__).resolve().parents[1]/"images"
STYLE=("adorable stylised 3D animated family-film character, extremely cute, huge sparkling glossy eyes, round soft cheeks, tiny nose and small mouth, smooth skin, rich warm golden lamp light, "
"shallow depth of field, head and shoulders close-up filling the frame, face perfectly front-facing and centered looking at the camera, "
"mouth closed and relaxed, plain modest village home background blurred, vertical 9:16, no text, no letters")
BOY="a 10-year-old South Asian boy with short black hair, a small white prayer cap (topi) and a simple light-blue kurta, big dark brown eyes"
GIRL="a young South Asian schoolgirl of about 7 with two small braids and a faded yellow frock, big dark eyes"
NANI="a gentle South Asian young mother with a kind round face and a soft green headscarf (dupatta)"
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
gen("s_boy_calm",f"close-up of {BOY}, soft thoughtful slightly worried eyes, {STYLE}")
gen("s_ammi_calm",f"close-up of {NANI}, warm loving gentle eyes and a soft calm expression, {STYLE}")
gen("s_girl_sad",f"close-up of {GIRL}, big sad glistening eyes with a small gentle pout, {STYLE}")
gen("s_boy_happy",f"the same boy as in the reference image, same face, white cap and light-blue kurta, now with a big joyful smile and sparkling happy eyes, {STYLE}","s_boy_calm")
gen("s_ammi_happy",f"the same mother as in the reference image, same face and green headscarf, now with a proud tearful smile, {STYLE}","s_ammi_calm")
gen("s_girl_happy",f"the same little girl as in the reference image, same face, braids and yellow frock, now with a big joyful smile and sparkling happy eyes, {STYLE}","s_girl_sad")
