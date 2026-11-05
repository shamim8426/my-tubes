"""Short 027 (from long 026): ChatGPT Images 2.6 GIFs. Style of the day 'news bulletin + proof window' (research/daily/2026-11-05.md).
Source: https://openai.com/index/introducing-images-2-6 (Nov 4, 2026; page blocks automated browsers, so the proof is a quote card). Run: .venv\\Scripts\\python -X utf8 <this file>"""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "templates"))
from ydeck_helpers import *

IMG = HERE / "img"


def proof_win(name, w, h, label, credit, cue, x=100, y=1000):
    """Rounded inset window with a real screenshot of the official OpenAI page (key sentence in yellow marker), label pill above, credit below."""
    win = (f'<div style="width:{w}px;height:{h}px;border-radius:30px;overflow:hidden;border:2px solid #E3E7EE;{SHADOW};background:#000">'
           f'<img src="{(IMG / (name + ".png")).as_uri()}" style="width:{w}px;height:{h}px;object-fit:cover;display:block"></div>')
    return [box(win, x, y, "", push=9, **pop(cue, -0.3)),
            box(f'<div style="font-size:30px;font-weight:800">{label}</div>', x, y - 72, f"background:#FFD60A;border-radius:999px;padding:8px 30px;{SHADOW}", **pop(cue, -0.1)),
            box(f'<div style="font-size:26px;font-weight:700;color:#556">{credit}</div>', x, y + h + 14, "", **pop(cue, 0.1))]


CREDIT = "Source: openai.com/index/introducing-images-2-6 · 4 Nov 2026"
MK = '<mark style="background:#FFD60A;color:#111;padding:2px 8px;border-radius:6px">'
S = []


def qcard(src, html, size, cue, y):
    return box(f'<div style="width:920px;box-sizing:border-box;padding:36px 44px;border-radius:30px;border:2px solid #E3E7EE;background:#fff;{SHADOW}">'
               f'<div style="font-size:26px;font-weight:700;color:#778;margin-bottom:20px">{src}</div><div style="font-size:{size}px;font-weight:700;line-height:1.35">{html}</div></div>', 80, y, "", **pop(cue, -0.2))


V = "ChatGPT अब आपकी image को GIF बना सकता है। OpenAI ने Images 2.6 launch किया है, और पेज के हिसाब से images पचास percent तेज़ बनती हैं।"
L = [tx("**Image** ab **GIF** banegi", 80, 230, 104, 920, 0.1),
     box('<div style="font-size:34px;font-weight:700">ChatGPT Images 2.6 · 4 Nov 2026</div>', 80, 560, f"background:#fff;border:2px solid #E3E7EE;border-radius:999px;padding:14px 32px;{SHADOW}", **pop(0.4, 0.0)),
     box('<div style="font-size:190px;font-weight:800;line-height:1">50%</div><div style="font-size:42px;font-weight:700;color:#444">tez (page ke hisaab se)</div>', 130, 700, f"background:#FFD60A;border-radius:40px;padding:30px 70px;{SHADOW}", wig="पचास|0.2", **pop("पचास", -0.3)),
     ic("sparkle", 760, 900, 190, cue="GIF", off=0.0, float=8, wig="GIF|0.3"),
     dict(kind="img", img="wave", size=330, x=640, y=1560, bob=1, k=[["ChatGPT|0.2", {"x": 1200, "o": 1}], ["ChatGPT|1.0", {"x": 640}]])]
L = L + proof_win("oai_0", 880, 338, "Official page", CREDIT, "पेज", 100, 1060)
S.append(dict(id="hook", type="stage", wipe="fade", voice=V, layers=L))

V = "GIF यानी एक छोटा loop वाला animation। जैसे flipbook, जिसके पन्ने तेज़ी से पलटो तो तस्वीर चलती दिखती है।"
L = [tx("**GIF** = chhota loop", 80, 230, 108, 920, 0.1),
     box(card('<div style="font-size:34px;font-weight:700;color:#667">ANALOGY</div><div style="font-size:64px;font-weight:800;line-height:1.15;margin-top:12px">Flipbook</div><div style="font-size:42px;font-weight:700;color:#444;margin-top:10px">pannen palto, tasveer chale</div>', 860, "36px 46px"), 110, 560, "", **pop("flipbook", -0.3)),
     ic("play", 150, 1050, 230, cue="loop", off=0.0, pulse=1.0),
     ic("arrow", 450, 1090, 150, cue="पलटो", off=-0.3, drawon=["पलटो|-0.3", 0.5]),
     box('<div style="font-size:110px;font-weight:800;line-height:1">GIF</div>', 640, 1040, f"background:#FFD60A;border-radius:34px;padding:24px 56px;{SHADOW}", wig="चलती|0.0", **pop("तस्वीर", -0.2)),
     tx("page ke hisaab se: **loop** wali image", 80, 1380, 76, 920, "छोटा|0.0")]
S.append(dict(id="analogy", type="stage", wipe="fade", voice=V, layers=L))

V = "पेज के हिसाब से आप अपने mascot या character को चला सकते हो, या product की फोटो को एक eye-catching loop में बदल सकते हो।"
L = [tx("**Kya** chala sakte ho?", 80, 230, 104, 920, 0.1),
     box(card('<div style="display:flex;align-items:center;gap:28px"><i data-ic="user" data-s="110"></i><div><div style="font-size:54px;font-weight:800">Mascot ya character</div><div style="font-size:36px;font-weight:700;color:#444">ko chalao</div></div></div>', 860, "30px 42px"), 110, 540, "", **pop("mascot", -0.2)),
     box(card('<div style="display:flex;align-items:center;gap:28px;color:#fff"><i data-ic="box" data-s="110"></i><div><div style="font-size:54px;font-weight:800">Product ki photo</div><div style="font-size:36px;font-weight:700;color:#C9CFDA">eye-catching loop</div></div></div>', 860, "30px 42px", "#14171C"), 110, 840, "", **pop("product", -0.2)),
     ic("arrow", 470, 1130, 130, cue="बदल सकते", off=-0.4, drawon=["बदल सकते|-0.4", 0.5]),
     box('<div style="font-size:90px;font-weight:800;line-height:1">GIF</div>', 330, 1300, f"background:#FFD60A;border-radius:34px;padding:22px 60px;{SHADOW}", wig="loop|0.0", float=6, **pop("loop", -0.3))]
S.append(dict(id="what", type="stage", wipe="fade", voice=V, layers=L))

V = "पेज पर एक example prompt है। उसमें छह frames वाली sprite sheet माँगी गई है, तीन columns और दो rows में, ताकि आख़िरी frame घूमकर पहले पर लौटे।"
cells = "".join(f'<div style="width:250px;height:190px;border-radius:22px;background:#fff;border:2px solid #E3E7EE;{SHADOW};display:flex;align-items:center;justify-content:center;font-size:90px;font-weight:800">{i}</div>' for i in range(1, 7))
L = [tx("**6 frames**, 3 x 2", 80, 230, 104, 920, 0.1),
     box('<div style="font-size:30px;font-weight:700;color:#556">OpenAI page ka example prompt (OpenArt ne banaya), chhota hissa:</div>', 80, 440, "", **pop(0.4, 0.0)),
     box('<div class="mono" style="font-size:36px;font-weight:700;line-height:1.35;color:#fff">sprite sheet, seamless looping GIF,<br><span style="color:#FFD60A">exactly 6 frames</span>, 3 columns x 2 rows</div>', 80, 530, "background:#14171C;border-radius:26px;padding:26px 36px;width:880px;box-sizing:border-box", **pop("छह", -0.4)),
     box(f'<div style="display:grid;grid-template-columns:repeat(3,250px);gap:20px">{cells}</div>', 100, 800, "", **pop("तीन columns", -0.3)),
     ic("check", 800, 1260, 150, cue="पहले पर", off=-0.2, drawon=["पहले पर|-0.2", 0.6]),
     tx("last frame **pehle par** lautta hai", 80, 1500, 70, 920, "आख़िरी|0.0")]
S.append(dict(id="example", type="stage", wipe="fade", voice=V, layers=L))

V = "ध्यान रखो: API का दाम इस पेज पर नहीं लिखा। पेज सिर्फ इतना कहता है कि ChatGPT और Codex में ये सभी subscription tiers पर मिल रहा है।"
L = [tx("**Dhyan** rakho", 80, 230, 110, 920, 0.1),
     box('<div style="width:130px;height:130px;border-radius:65px;background:#FFD60A;display:flex;align-items:center;justify-content:center;font-size:90px;font-weight:800">!</div>', 880, 215, "", wig="दाम|0.4", **pop("ध्यान", 0.0)),
     box(card('<div style="font-size:48px;font-weight:800">API ka daam</div><div style="font-size:40px;font-weight:700;color:#444;margin-top:8px">page me nahi likha</div>', 860, "34px 44px"), 110, 520, "", **pop("दाम", -0.3)),
     ]
L = L + proof_win("oai_1", 880, 238, "Official page", CREDIT, "सभी", 100, 800)
S.append(dict(id="caution", type="stage", wipe="fade", voice=V, layers=L))

V = "तो याद रखो: Images 2.6 में अपनी image को GIF बना सकते हो, और images पचास percent तेज़ बनती हैं। ये सब subscription tiers पर मिल रहा है।"
L = [tx("**Yaad** rakho", 80, 230, 110, 920, 0.1),
     box(card('<div style="font-size:50px;font-weight:800">Image <span style="background:#FFD60A;padding:0 12px;border-radius:12px">&rarr; GIF</span></div>', 860, "34px 44px"), 110, 540, "", **pop("GIF", -0.2)),
     box(card('<div style="font-size:50px;font-weight:800">Images <span style="background:#FFD60A;padding:0 12px;border-radius:12px">50% tez</span></div>', 860, "34px 44px"), 110, 800, "", **pop("पचास", -0.2)),
     box(card('<div style="font-size:44px;font-weight:800">Sabhi subscription tiers</div><div style="font-size:34px;font-weight:700;color:#444;margin-top:8px">ChatGPT aur Codex (page ke hisaab se)</div>', 860, "30px 44px"), 110, 1060, "", **pop("subscription", -0.2)),
     dict(kind="img", img="thumbs", size=420, x=600, y=1400, bob=1, k=[["subscription|-0.3", {"o": 0}], ["subscription|0.0", {"o": 1}]])]
S.append(dict(id="recap", type="stage", wipe="fade", voice=V, layers=L))
S.append(cta_scene())

finish(HERE, "Short 027 from long 026: ChatGPT Images 2.6 GIFs. Source https://openai.com/index/introducing-images-2-6 (read 2026-11-05). Style of the day: news bulletin + proof window.", "AI News", S)
