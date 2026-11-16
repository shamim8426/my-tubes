import sys
sys.path.insert(0,'scripts')
from pathlib import Path
import gemini_image
S=Path(sys.argv[1])/'images'
BASE=("Polished cinematic 3D-illustration film still, ultra sharp crisp focus, high contrast, deep rich saturated colors, clean clear air, absolutely no haze, no fog, no mist, no dust clouds, no washed-out whites, no bloom, deep dark shadows, 7th-century Arabia Madinah, mud-brick and palm-trunk architecture, no people, no text, no modern objects. 16:9 wide.")
J={
'12_land_plot_palms':"Wide plot of farmland with rows of young date palms and a small irrigation channel, low mud wall, rocky hills far away, bright clear late morning.",
'14_camel_kneeling':"A single camel kneeling on a dirt road beside a palm grove, saddle blanket, rope, far away, clear afternoon sun, no people.",
'17_mountain_night_route':"Rocky mountain path at night under a huge starry sky and moon, sharp black silhouettes of cliffs, deep blue night, no people.",
'18_provisions_bag':"Close-up on a wooden table: a leather water skin, a cloth food bag and a plain cloth waist-band torn in two halves, warm oil-lamp light, dark room, no people, no hands.",
'19_night_desert_road':"A lone dirt road through a desert valley at night, bright full moon, stars, sharp rocks, deep blue night, no people.",
'21_sunrise_palms':"Date palm grove at sunrise, golden sun rays through clear air, green fronds, mud wall, birds in the sky, crisp and vivid, no people.",
}
for k,v in J.items():
    f=S/(k+'.png')
    if f.exists(): continue
    try:
        gemini_image.generate(BASE+' '+v,f,aspect_ratio='16:9',size='1K',style=BASE); print(k,'ok',flush=True)
    except Exception as e:
        print(k,'ERR',str(e)[:150],flush=True)
