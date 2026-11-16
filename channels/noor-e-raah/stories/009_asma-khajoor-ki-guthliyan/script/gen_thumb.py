import sys
sys.path.insert(0,'scripts')
from pathlib import Path
import gemini_image
S=Path(sys.argv[1])
BASE=("Polished cinematic 3D-illustration movie poster still, ultra sharp crisp focus, high contrast, deep rich saturated colors, strong golden rim light, clean clear air, absolutely no haze, no fog, no mist, no dust clouds, no bloom, deep dark shadows, 7th-century Madinah palm grove, no text, no modern objects, wide 16:9 composition. Any person is seen strictly from BEHIND, face never visible, exactly two arms and two hands.")
J={
'A':"Left third: a woman seen from behind in a long dark robe and headscarf, carrying a large heap of date stones on her head with both hands raised steadying it, walking on a sandy path. Right two thirds: a kneeling camel and a small group of travellers on camels, tiny and far away on the path ahead, backlit by a huge glowing low sun between date palms. Dramatic golden hour, long sharp shadows.",
'B':"Extreme low-angle shot from behind a woman in a long dark robe and headscarf carrying a heavy bundle of date stones on her head, a huge dramatic sunset sky with strong orange and deep blue contrast above a long empty road lined with date palms, a single kneeling camel far ahead. Powerful movie-poster composition, subject on the left third.",
}
for k,v in J.items():
    f=S/f'thumb/{k}.png'
    try:
        gemini_image.generate(BASE+' '+v,f,aspect_ratio='16:9',size='1K',style=BASE); print(k,'ok',flush=True)
    except Exception as e: print(k,'ERR',str(e)[:150],flush=True)
