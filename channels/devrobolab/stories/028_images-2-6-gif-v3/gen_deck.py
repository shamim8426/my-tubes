"""Short 028 = Short 027 rebuilt in VISUAL STANDARD v2 (user 2026-11-05/06): BIG real official-page screenshots + free AI illustrations,
little HTML. Same voice and word times as 027 (audio/tts, wt.json copied). Source: https://openai.com/index/introducing-images-2-6"""
import json, sys
from pathlib import Path
from PIL import Image
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "templates"))
from ydeck_helpers import *

OLD = {s["id"]: s for s in json.load(open(HERE.parent / "027_images-2-6-gif-short" / "deck.json", encoding="utf-8"))["scenes"]}
IMG, PRF = HERE / "img", HERE / "proof"
CREDIT = "Source: openai.com/index/introducing-images-2-6 · 4 Nov 2026"


def big(path, crop, w, x, y, cue, off=-0.3, tag=None, credit=None, radius=26):
    """Image (or a crop of it, crop=(x0,y0,x1,y1) in source px) shown w px wide. Optional tag pill above and credit line below."""
    im = Image.open(path)
    x0, y0, x1, y1 = crop or (0, 0, im.width, im.height)
    k = w / (x1 - x0); h = round((y1 - y0) * k)
    html = (f'<div style="width:{w}px;height:{h}px;border-radius:{radius}px;overflow:hidden;border:2px solid #E3E7EE;{SHADOW};background:#000;position:relative">'
            f'<img src="{Path(path).as_uri()}" style="position:absolute;left:{-x0*k:.1f}px;top:{-y0*k:.1f}px;width:{im.width*k:.1f}px;height:{im.height*k:.1f}px"></div>')
    out = [box(html, x, y, "", push=9, **pop(cue, off))]
    if tag:
        out.append(box(f'<div style="font-size:32px;font-weight:800">{tag}</div>', x, y - 74, f"background:#FFD60A;border-radius:999px;padding:8px 30px;{SHADOW}", **pop(cue, off + 0.2)))
    if credit:
        out.append(box(f'<div style="font-size:28px;font-weight:700;color:#445">{credit}</div>', x, y + h + 16, "", **pop(cue, off + 0.4)))
    return out, h


S = []
# 0 hook: real page, tall crop (hero image + headline + the marked "50% faster" sentence)
L = [tx("**Image** ab **GIF** banegi", 60, 170, 84, 980, 0.1)]
b, h = big(PRF / "oai_speed_full.jpg", (190, 380, 590, 745), 1000, 40, 440, "पेज", -0.5, "Official website · openai.com", CREDIT)
L += b + [dict(kind="img", img="wave", size=330, x=640, y=1580, bob=1, k=[["ChatGPT|0.2", {"x": 1200, "o": 1}], ["ChatGPT|1.0", {"x": 640}]])]
S.append(dict(id="hook", type="stage", wipe="fade", voice=OLD["hook"]["voice"], layers=L))

# 1 analogy: AI illustration (flipbook), labelled
L = [tx("**GIF** = chhota loop", 60, 170, 84, 980, 0.1)]
b, h = big(IMG / "ai_flipbook.png", (60, 200, 964, 860), 1000, 40, 440, "flipbook", -0.4, "AI illustration (flipbook)")
L += b + [tx("page ke hisaab se: **loop** wali image", 80, 1250, 76, 920, "छोटा|0.0"),
          ic("play", 780, 1530, 170, cue="चलती", off=0.0, pulse=1.0)]
S.append(dict(id="analogy", type="stage", wipe="fade", voice=OLD["analogy"]["voice"], layers=L))

# 2 what: AI illustration (film strip) + two short labels
L = [tx("**Kya** chala sakte ho?", 60, 170, 84, 980, 0.1)]
b, h = big(IMG / "ai_filmstrip.png", (20, 190, 1004, 880), 1000, 40, 440, "product", -0.6, "AI illustration (film strip)")
L += b + [box('<div style="font-size:52px;font-weight:800">Mascot ya character</div>', 60, 1180, f"background:#fff;border:2px solid #E3E7EE;border-radius:999px;padding:16px 40px;{SHADOW}", **pop("mascot", -0.2)),
          box('<div style="font-size:52px;font-weight:800">Product ki photo</div>', 60, 1320, f"background:#14171C;color:#fff;border-radius:999px;padding:16px 40px;{SHADOW}", **pop("product", -0.2)),
          box('<div style="font-size:90px;font-weight:800;line-height:1">&rarr; GIF</div>', 620, 1480, f"background:#FFD60A;border-radius:34px;padding:22px 50px;{SHADOW}", wig="loop|0.0", float=6, **pop("loop", -0.3))]
S.append(dict(id="what", type="stage", wipe="fade", voice=OLD["what"]["voice"], layers=L))

# 3 example: AI sprite sheet + the prompt line
L = [tx("**6 frames**, 3 x 2", 60, 170, 84, 980, 0.1)]
b, h = big(IMG / "ai_sprites.png", None, 800, 140, 400, "sprite", -0.4, "AI illustration (sprite sheet idea)")
L += b + [box('<div class="mono" style="font-size:36px;font-weight:700;line-height:1.35;color:#fff">sprite sheet, seamless looping GIF,<br><span style="color:#FFD60A">exactly 6 frames</span>, 3 columns x 2 rows</div>', 80, 1290, "background:#14171C;border-radius:26px;padding:26px 36px;width:880px;box-sizing:border-box", **pop("छह", -0.4)),
          tx("last frame **pehle par** lautta hai", 80, 1560, 70, 920, "आख़िरी|0.0")]
S.append(dict(id="example", type="stage", wipe="fade", voice=OLD["example"]["voice"], layers=L))

# 4 caution: real "Pricing and availability" crop, key sentence marked
L = [tx("**Dhyan** rakho", 60, 170, 84, 780, 0.1),
     box('<div style="width:120px;height:120px;border-radius:60px;background:#FFD60A;display:flex;align-items:center;justify-content:center;font-size:84px;font-weight:800">!</div>', 880, 175, "", wig="दाम|0.4", **pop("ध्यान", 0.0))]
b, h = big(PRF / "oai_avail_full.jpg", (190, 385, 590, 665), 1000, 40, 440, "सभी", -0.6, "Official website · openai.com", CREDIT)
L += b + [box(card('<div style="font-size:50px;font-weight:800">API ka daam</div><div style="font-size:42px;font-weight:700;color:#444;margin-top:8px">page me nahi likha</div>', 900, "34px 44px"), 90, 1260, "", **pop("दाम", -0.3))]
S.append(dict(id="caution", type="stage", wipe="fade", voice=OLD["caution"]["voice"], layers=L))

# 5 recap: both real crops big, one line each
L = [tx("**Yaad** rakho", 60, 170, 84, 980, 0.1)]
b1, h1 = big(IMG / "oai_0.png", None, 1000, 40, 400, "GIF", -0.4, "Images 2.6: 50% faster")
b2, h2 = big(IMG / "oai_1.png", None, 1000, 40, 400 + h1 + 120, "subscription", -0.4, "Available on all tiers")
L += b1 + b2 + [box('<div style="font-size:72px;font-weight:800">Image <span style="background:#FFD60A;padding:0 12px;border-radius:12px">&rarr; GIF</span></div>', 60, 1540, "", **pop("GIF", -0.2)),
                dict(kind="img", img="thumbs", size=330, x=680, y=1540, bob=1, k=[["subscription|-0.3", {"o": 0}], ["subscription|0.0", {"o": 1}]])]
S.append(dict(id="recap", type="stage", wipe="fade", voice=OLD["recap"]["voice"], layers=L))
S.append(cta_scene())
finish(HERE, "Short 028 = 027 rebuilt in Visual Standard v2: big real official-page screenshots + free AI illustrations (labelled). Source https://openai.com/index/introducing-images-2-6", "AI News", S)
