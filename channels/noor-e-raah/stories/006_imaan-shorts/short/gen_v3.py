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
GIRL="a 12-year-old South Asian girl in a soft pink headscarf (hijab) and a light cream dress, big dark brown eyes"
NANI="a sweet elderly South Asian grandmother with a round kind face, gentle wrinkles and a white floral headscarf"
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
gen("v3_girl_sad",f"close-up of {GIRL}, sad worried teary eyes with a small trembling frown, {STYLE}")
gen("v3_nani_calm",f"close-up of {NANI}, warm loving gentle eyes and a soft calm expression, {STYLE}")
gen("v3_girl_happy",f"the same girl as in the reference image, same face, pink headscarf and dress, now with a big joyful smile and sparkling happy eyes, {STYLE}","v3_girl_sad")
gen("v3_nani_happy",f"the same grandmother as in the reference image, same face and white floral headscarf, now with a proud tearful smile, {STYLE}","v3_nani_calm")
