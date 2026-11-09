import sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[5]
sys.path.insert(0,str(ROOT/"scripts"))
import cf_image
OUT=ROOT/"channels/noor-e-raah/stories/006_imaan-shorts/images"
STYLE=("stylised 3D animated family-film render, soft sculpted faces, big expressive kind eyes, smooth skin, "
"rich warm golden lamp light, cinematic shallow depth of field, detailed cloth texture, vertical 9:16 composition, "
"modest village home, no text, no letters, no logo")
MOM="a young South Asian mother in a soft teal headscarf and long plain olive dress"
GIRL="a small 6-year-old girl with two braids in a mustard kurta"
OLD="a tired elderly man with grey stubble, plain white cap and a worn brown shawl"
S={
 "s1":f"close-up of {GIRL} lying on a simple floor mat at night, big sad hungry eyes looking up, oil lamp glow, {STYLE}",
 "s2":f"{MOM} sitting on the floor in a small mud-brick room at night, tender smile, a single round flatbread roti on a plain cloth between her and {GIRL}, oil lamp, {STYLE}",
 "s3":f"open wooden doorway at night, {OLD} standing outside leaning on a stick, exhausted kind face, lamp light from inside, {STYLE}",
 "s4":f"close-up of {MOM} gently placing half a roti into the hands of {OLD}, warm caring expression, {STYLE}",
 "s5":f"{GIRL} and {MOM} asleep peacefully together on a floor mat, soft moonlight through a small window, calm, {STYLE}",
 "s6":f"morning golden sunrise at the wooden door, a smiling neighbour woman in a maroon headscarf holding a big steaming pot of food, {MOM} and {GIRL} smiling in surprise and happiness, {STYLE}",
}
for k,p in S.items():
    f=OUT/f"{k}.png"
    if f.exists(): continue
    try: cf_image.generate(p,f,width=768,height=1344); print("ok",k)
    except Exception as e: print("FAIL",k,e)
