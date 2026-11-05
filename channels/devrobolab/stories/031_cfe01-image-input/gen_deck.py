"""Claude Feature 01 (series Claude for Everyone, index 01): uploading photos/files to Claude. REAL-IMAGE paper-cut style.
Source (official): https://support.claude.com/en/articles/8241126-upload-files-to-claude (article dated July 23, 2026; read 2026-11-06).
Real assets: own screenshots of that article (shoot.py), public-domain manuscript photo (Wikimedia Commons, Book of Hours Metz), AI-drawn character stickers (labelled)."""
import sys
from pathlib import Path
from PIL import Image, ImageFilter
HERE = Path(__file__).parent
ROOT = HERE.parents[3]
sys.path.insert(0, str(HERE.parents[1] / "templates")); sys.path.insert(0, str(ROOT / "scripts"))
from ydeck_helpers import *
from papercut import cutout_grabcut, sticker, paper_rect

CUT, SH, RAW = HERE / "cut", HERE / "shots", HERE / "assets_raw"


def make_assets():
    if not (CUT / "photo.png").exists():
        im = Image.open(RAW / "photo_manuscript.jpg").convert("RGB").crop((0, 250, 1920, 1565)).resize((960, 658))  # Commons, public domain (Book of Hours, Metz)
        paper_rect(im, border=22, seed=3).save(CUT / "photo.png")
        small = im.resize((48, 33), Image.BILINEAR).resize(im.size, Image.NEAREST)  # low-resolution version of the same photo
        paper_rect(small, border=22, seed=4).save(CUT / "photo_lowres.png")
    for n in ["intro", "how", "formats", "limits", "tips", "project"]:
        if not (CUT / f"shot_{n}.png").exists():
            paper_rect(Image.open(SH / f"{n}.png").convert("RGB"), border=26, seed=sum(map(ord, n)) % 97).save(CUT / f"shot_{n}.png")


def pic(name, w, x, y, cue, off=-0.3, **kw):
    im = Image.open(CUT / f"{name}.png"); h = round(im.height * w / im.width)
    return box(f'<img src="{(CUT / (name + ".png")).as_uri()}" style="width:{w}px;height:{h}px;display:block">', x, y, "", **pop(cue, off, **kw)), h


def pill(text, x, y, cue, off=-0.2, dark=False, size=40):
    css = "background:#14171C;color:#fff;" if dark else "background:#FFD60A;color:#111;"
    return box(f'<div style="font-size:{size}px;font-weight:800;white-space:nowrap">{text}</div>', x, y, css + f"border-radius:999px;padding:12px 34px;{SHADOW}", **pop(cue, off))


def bg():
    return box(f'<img src="{(CUT / "paper_bg.jpg").as_uri()}" style="width:1080px;height:1920px;display:block">', 0, 0, "")


make_assets()
V = ["फोटो खींची और Claude को दिखानी है? Claude documents और images, दोनों upload करके आपके साथ काम कर सकता है। चलो देखते हैं कैसे।",
     "Chat box के बाएँ नीचे plus button दबाओ, Add files or photos चुनो, और फोटो चुनो। या फोटो को सीधे chat में drag and drop करो, या clipboard से paste करो।",
     "Images में JPEG, PNG, GIF और WebP चलते हैं।",
     "एक chat में बीस files तक, और image आठ हज़ार गुणा आठ हज़ार pixels तक।",
     "बेहतर नतीजे के लिए हज़ार गुणा हज़ार pixels या उससे बड़ी image लो। छोटी और low-resolution image से बचो।",
     "फ़ाइल को Project के Files section में भी रख सकते हो, ताकि हर बातचीत में उसका reference रहे।"]
T = lambda t: tx(t, 60, 170, 84, 980, 0.1)
S = []
a, h = pic("shot_intro", 960, 60, 420, "upload", -0.7)
s, sh = pic("photo", 880, 100, 420 + h + 70, "फोटो", -0.4)
S.append(dict(id="hook", type="stage", wipe="fade", voice=V[0], layers=[bg(), T("**Photo** dikhao, Claude ko"), a, s,
          pill("Real photo: old manuscript page (public domain)", 60, 420 + h + 70 + sh + 40, "फोटो", 0.3, True, 30)]))
a, h = pic("shot_how", 960, 60, 420, "plus", -0.6)
y = 420 + h + 50
S.append(dict(id="how", type="stage", wipe="fade", voice=V[1], layers=[bg(), T("Photo kaise **daalo**"), a,
          pill("+ button", 60, y, "plus", -0.2), pill("Drag & drop", 380, y, "drag", -0.2, True), pill("Clipboard se paste", 60, y + 110, "clipboard", -0.2)]))
a, h = pic("shot_formats", 960, 60, 420, "JPEG", -0.7)
s, sh = pic("char_0", 520, 280, 420 + h + 50, "WebP", 0.0)
S.append(dict(id="formats", type="stage", wipe="fade", voice=V[2], layers=[bg(), T("Kaunse **formats** chalte hain"), a, s]))
a, h = pic("shot_limits", 960, 60, 420, "बीस", -0.6)
y = 420 + h + 70
S.append(dict(id="limits", type="stage", wipe="fade", voice=V[3], layers=[bg(), T("**Limits** yaad rakho"), a,
          pill("20 files / chat", 60, y, "बीस", -0.2, False, 66), pill("8000 x 8000 px", 60, y + 150, "हज़ार", -0.2, True, 66)]))
a, h = pic("shot_tips", 960, 60, 420, "बेहतर", -0.6)
y = 420 + h + 60
s1, h1 = pic("photo", 470, 40, y, "हज़ार", -0.3); s2, h2 = pic("photo_lowres", 470, 560, y, "low", -0.3)
S.append(dict(id="tips", type="stage", wipe="fade", voice=V[4], layers=[bg(), T("Behtar **nateeja** kaise"), a, s1, s2,
          pill("1000 x 1000+", 70, y + h1 + 40, "हज़ार", -0.1), pill("Chhoti, blurry", 590, y + h2 + 40, "low", -0.1, True)]))
a, h = pic("shot_project", 960, 60, 420, "Project", -0.6)
s, sh = pic("char_3", 520, 280, 420 + h + 60, "reference", -0.3)
S.append(dict(id="project", type="stage", wipe="fade", voice=V[5], layers=[bg(), T("**Project** me bhi rakho"), a, s,
          pill("Project > Files section", 60, 420 + h + 60 + sh + 40, "reference", -0.2)]))
S.append(cta_scene())
finish(HERE, "Claude Feature 01 (Claude for Everyone): upload photos and files. Source https://support.claude.com/en/articles/8241126-upload-files-to-claude (read 2026-11-06).", "Claude Feature 01 · Photo upload", S)
