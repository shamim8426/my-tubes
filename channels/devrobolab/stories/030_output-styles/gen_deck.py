"""Short 030: Claude Code output styles. REAL-IMAGE paper-cut style (user 2026-11-06): real docs screenshots (shoot.py), real CC0 photos
(Wikimedia Commons: Adidas SL 72 OG.jpg CC0, Magnifying-glass diamonds.jpg CC0), AI character stickers (labelled), craft-paper background.
Source: https://code.claude.com/docs/en/output-styles (read 2026-11-06). Learnings applied: brand/LONG_FORM_LEARNINGS.md + STYLE_LEARNINGS.md."""
import sys
from pathlib import Path
from PIL import Image
HERE = Path(__file__).parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parents[1] / "templates")); sys.path.insert(0, str(ROOT / "scripts"))
from ydeck_helpers import *
from papercut import cutout_grabcut, sticker, paper_rect

CUT, SH, RAW = HERE / "cut", HERE / "shots", HERE / "assets_raw"


def make_assets():
    if not (CUT / "shoe.png").exists():
        im = Image.open(RAW / "shoe_0.jpg").convert("RGB")
        rect = (int(im.width * .03), int(im.height * .12), int(im.width * .94), int(im.height * .78))
        sticker(cutout_grabcut(im, rect), border=22, seed=3).save(CUT / "shoe.png")
    for n in ["cmd", "concise", "explain", "intro", "learn"]:
        if not (CUT / f"shot_{n}.png").exists():
            paper_rect(Image.open(SH / f"{n}.png").convert("RGB"), border=26, seed=hash(n) % 97).save(CUT / f"shot_{n}.png")


def pic(name, w, x, y, cue, off=-0.3, **kw):
    im = Image.open(CUT / f"{name}.png"); h = round(im.height * w / im.width)
    return box(f'<img src="{(CUT / (name + ".png")).as_uri()}" style="width:{w}px;height:{h}px;display:block">', x, y, "", **pop(cue, off, **kw)), h


def pill(text, x, y, cue, off=-0.2, dark=False, size=40):
    css = "background:#14171C;color:#fff;" if dark else "background:#FFD60A;color:#111;"
    return box(f'<div style="font-size:{size}px;font-weight:800;white-space:nowrap">{text}</div>', x, y, css + f"border-radius:999px;padding:12px 34px;{SHADOW}", **pop(cue, off))


def bg():
    return box(f'<img src="{(CUT / "paper_bg.jpg").as_uri()}" style="width:1080px;height:1920px;display:block">', 0, 0, "")


make_assets()
V = ["Claude का जवाब बहुत लंबा लगता है? Output style से उसका अंदाज़ बदलो। Default के अलावा चार styles हैं: Proactive, Concise, Explanatory और Learning।",
     "Concise में जवाब का पहला वाक्य ही नतीजा बताता है। Lead-in और recap नहीं होते।",
     "Explanatory में Claude Insight blocks जोड़ता है, जो बताते हैं कि उसने code में ये choices क्यों कीं।",
     "Learning में Claude कुछ code आपके लिए छोड़ देता है, TODO human लिखकर, ताकि आप खुद लिखकर सीखो।",
     "Proactive में Claude तुरंत काम शुरू कर देता है, और छोटे फ़ैसलों पर पूछता नहीं।",
     "Style बदलने के लिए slash output-style लिखो, जैसे slash output-style concise। ध्यान रखो, ये सिर्फ़ instructions हैं, गारंटी नहीं। जो हर बार होना चाहिए, उसके लिए hook।"]
S = []
# 0 hook: real intro page crop + four real/stickers with their style names
a, h = pic("shot_intro", 960, 60, 400, "Output", -0.6)
L = [bg(), tx("**Claude** ka andaaz badlo", 60, 170, 84, 980, 0.1), a]
s, _ = pic("shoe", 420, 40, 800, "Proactive", -0.3); L += [s, pill("Proactive", 80, 1160, "Proactive", -0.1)]
s, _ = pic("char_1", 300, 520, 790, "Concise", -0.3); L += [s, pill("Concise", 540, 1160, "Concise", -0.1, True)]
s, _ = pic("char_2", 300, 80, 1290, "Explanatory", -0.3); L += [s, pill("Explanatory", 80, 1620, "Explanatory", -0.1)]
s, _ = pic("char_4", 300, 560, 1290, "Learning", -0.3); L += [s, pill("Learning", 560, 1620, "Learning", -0.1, True)]
L.append(pill("Real: docs page + sneaker photo (CC0) · characters AI-drawn", 60, 1760, "Output", 0.2, True, 26))
S.append(dict(id="hook", type="stage", wipe="fade", voice=V[0], layers=L))
# 1 concise
a, h = pic("shot_concise", 960, 60, 420, "पहला", -0.5)
s, _ = pic("char_1", 560, 480, 420 + h + 40, "नतीजा", -0.3)
S.append(dict(id="concise", type="stage", wipe="fade", voice=V[1], layers=[bg(), tx("**Concise**: seedha result", 60, 170, 84, 980, 0.1), a, s,
          pill("Pehla vakya = jawab", 60, 420 + h + 160, "नतीजा", -0.2), pill("Lead-in, recap nahi", 60, 420 + h + 300, "Lead-in", -0.2, True)]))
# 2 explanatory
a, h = pic("shot_explain", 960, 60, 420, "Insight", -0.5)
s, _ = pic("char_2", 640, 220, 420 + h + 60, "choices", -0.4)
S.append(dict(id="explain", type="stage", wipe="fade", voice=V[2], layers=[bg(), tx("**Explanatory**: Insight block", 60, 170, 84, 980, 0.1), a, s,
          pill("Conversation me dikhta hai, file me nahi", 60, 420 + h + 60 + 640, "choices", 0.2, True, 34)]))
# 3 learning
a, h = pic("shot_learn", 960, 60, 420, "Learning", -0.5)
s, _ = pic("char_4", 560, 480, 420 + h + 40, "TODO", -0.3)
S.append(dict(id="learn", type="stage", wipe="fade", voice=V[3], layers=[bg(), tx("**Learning**: aap bhi likho", 60, 170, 84, 980, 0.1), a, s,
          pill("TODO(human)", 60, 420 + h + 160, "TODO", -0.2), pill("Khud likho, seekho", 60, 420 + h + 300, "सीखो", -0.2, True)]))
# 4 proactive: running shoe = starts right away
s, h = pic("shoe", 960, 60, 480, "तुरंत", -0.5)
S.append(dict(id="proactive", type="stage", wipe="fade", voice=V[4], layers=[bg(), tx("**Proactive**: seedha kaam shuru", 60, 170, 84, 980, 0.1), s,
          pill("Routine decisions par sawaal nahi", 60, 480 + h + 80, "छोटे", -0.2, False, 38), pill("Real photo: sneaker (CC0)", 60, 480 + h + 200, "तुरंत", 0.3, True, 30)]))
# 5 switch + caution
a, h = pic("shot_cmd", 960, 60, 420, "slash", -0.5)
S.append(dict(id="switch", type="stage", wipe="fade", voice=V[5], layers=[bg(), tx("**/output-style** concise", 60, 170, 84, 980, 0.1), a,
          pill("Sirf instructions, guarantee nahi", 60, 420 + h + 100, "गारंटी", -0.3, False, 38), pill("Har baar chahiye? Hook", 60, 420 + h + 240, "hook", -0.3, True, 38)]))
S.append(cta_scene())
finish(HERE, "Short 030 Output styles, real-image paper-cut style. Source https://code.claude.com/docs/en/output-styles (read 2026-11-06).", "Claude Code · Output styles", S)
