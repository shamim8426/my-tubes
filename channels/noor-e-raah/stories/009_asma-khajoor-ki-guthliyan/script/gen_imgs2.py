import sys
sys.path.insert(0,'scripts')
from pathlib import Path
import gemini_image
S=Path(sys.argv[1])/'images'
BASE=("Polished cinematic 3D-illustration film still, ultra sharp crisp focus, high contrast, deep rich saturated colors, clean clear air, absolutely no haze, no fog, no mist, no dust clouds, no washed-out whites, no bloom, deep dark shadows, 7th-century Arabia Madinah, mud-brick and palm-trunk architecture, no people, no text, no modern objects. 16:9 wide.")
J={
'13_long_road_far':"A very long straight sandy road stretching far to distant rocky hills, a tiny small town of mud-brick houses and a palm grove far behind at one end, hard noon sun, deep blue sky, crisp shadows.",
'15_road_tracks':"A sandy road beside a palm grove at noon with fresh camel footprints in the sand and long sharp shadows of palm trees, empty, deep blue sky, crisp.",
'18_footprints_leaving':"Golden-hour sandy road with a line of camel footprints leading away toward distant hills, palm trees on one side, clear warm sky, empty, crisp.",
'16_doorway_lamp':"Wooden doorway of a mud-brick house at dusk, a warm oil lamp glowing inside, clay pots outside, deep blue evening sky, rich contrast.",
'22_stable_morning':"Open palm-leaf stable at clear morning with a well-groomed horse standing calmly, fresh hay and a water trough, mud-brick wall, sunlight rays, no people.",
'20_makkah_hills_dawn':"Barren rocky hills and a small stone-and-mud town below at dawn, clear orange sunrise sky, crisp, empty streets.",
}
for k,v in J.items():
    f=S/(k+'.png')
    if f.exists(): continue
    try:
        gemini_image.generate(BASE+' '+v,f,aspect_ratio='16:9',size='1K',style=BASE); print(k,'ok',flush=True)
    except Exception as e:
        print(k,'ERR',str(e)[:150],flush=True)
print('DONE',flush=True)
