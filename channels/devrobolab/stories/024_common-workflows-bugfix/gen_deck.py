"""Short 024 docs: Common workflows - fix bugs efficiently (3 steps). Style: Day 1 'clean product-page'.
Source: https://code.claude.com/docs/en/common-workflows.md (read 2026-11-04)."""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "templates"))
from ydeck_helpers import *

PROMPT = "background:#fff;border:2px solid #E3E7EE;border-radius:999px;padding:20px 38px;" + SHADOW


def prompt_card(text, x, y, cue, off=-0.3, w=900):
    return box(f'<div class="mono" style="font-size:36px;font-weight:700;line-height:1.35"><span style="color:#B58900">&gt;</span> {text}</div>', x, y, f"width:{w}px;box-sizing:border-box;background:#14171C;color:#fff;border-radius:30px;padding:30px 36px;{SHADOW}", **pop(cue, off))


S = []
V = "Code में error आया और समझ नहीं आ रहा? Claude Code से तीन आसान steps में उसे fix करवाओ।"
L = [tx("**Error** aaya? 3 steps", 80, 230, 112, 920, 0.1),
     ic("bug", 130, 640, 260, cue="error", off=0.0, float=8, wig="error|0.4"),
     box('<div style="font-size:60px;font-weight:800;line-height:1.15">npm test<br><span style="color:#B00020">failed</span></div>', 520, 650, f"background:#fff;border:2px solid #E3E7EE;border-radius:34px;padding:34px 44px;{SHADOW}", **pop("error", 0.2)),
     box('<div style="font-size:64px;font-weight:800">1 &nbsp;2 &nbsp;3</div>', 130, 1060, f"background:#FFD60A;border-radius:999px;padding:18px 60px;{SHADOW}", **pop("तीन आसान", -0.1)),
     tx("seedhe **fix** tak", 80, 1300, 100, 920, "fix करवाओ|-0.3"),
     dict(kind="img", img="wave", size=330, x=720, y=1500, bob=1, k=[["Claude Code|0.2", {"x": 1200, "o": 1}], ["Claude Code|1.0", {"x": 720}]])]
S.append(dict(id="hook", type="stage", wipe="fade", voice=V, layers=L))

V = "पहला: error बताओ, जैसे डॉक्टर को लक्षण बताते हो। लिखो: I'm seeing an error when I run npm test।"
L = [tx("**Step 1:** error batao", 80, 230, 104, 920, 0.1),
     box(card('<div style="font-size:30px;font-weight:700;color:#667">jaise ek... doctor ko lakshan</div><div style="font-size:60px;font-weight:800;margin-top:10px">symptoms</div>', 700, "30px 40px"), 100, 520, "", k=[[0, {"r": -2}]], **pop("डॉक्टर", -0.3)),
     ic("user", 800, 560, 150, cue="डॉक्टर", off=0.0, float=7),
     prompt_card("I'm seeing an error when I run npm test", 90, 900, "लिखो", off=0.0),
     ic("check", 800, 1230, 150, cue="npm test", off=0.3, drawon=["npm test|0.4", 0.6]),
     tx("**error** saaf batao", 80, 1230, 90, 700, "error बताओ|0.0")]
S.append(dict(id="step1", type="stage", wipe="fade", voice=V, layers=L))

V = "दूसरा: सीधे fix मत करवाओ, पहले options पूछो। जैसे: suggest a few ways to fix the at ts-ignore in user dot ts।"
L = [tx("**Step 2:** options poochho", 80, 230, 96, 920, 0.1),
     prompt_card("suggest a few ways to fix the @ts-ignore in user.ts", 90, 520, "suggest", off=-0.2),
     box(card('<div style="font-size:40px;font-weight:800">Option A</div>', 400, "22px 34px"), 90, 930, "", **pop("options", 0.4)),
     box(card('<div style="font-size:40px;font-weight:800">Option B</div>', 400, "22px 34px"), 520, 930, "", **pop("options", 0.8)),
     box(card('<div style="font-size:40px;font-weight:800">Option C</div>', 400, "22px 34px"), 305, 1090, "", **pop("options", 1.2)),
     ic("cross", 800, 1300, 130, cue="सीधे fix", off=0.0, wig="सीधे fix|0.4"),
     tx("pehle **options**", 80, 1300, 100, 700, "पहले options|0.0")]
S.append(dict(id="step2", type="stage", wipe="fade", voice=V, layers=L))

V = "तीसरा: जो तरीका पसंद आए, उसे लगवा दो। लिखो: update user dot ts to add the null check you suggested।"
L = [tx("**Step 3:** fix lagwao", 80, 230, 104, 920, 0.1),
     box(card('<div style="font-size:40px;font-weight:800">Option B <span style="background:#FFD60A;padding:0 12px;border-radius:12px">pasand</span></div>', 700, "26px 38px"), 90, 520, "", **pop("पसंद आए", -0.4)),
     prompt_card("update user.ts to add the null check you suggested", 90, 780, "लिखो", off=0.0),
     ic("file", 130, 1170, 170, cue="update", off=0.6, float=6),
     flow([[320, 1255], [560, 1255]], None, "null check|-0.2", dur=0.5, sw=8, n=2, per=1.2, r=12),
     ic("check", 600, 1170, 170, cue="null check", off=0.4, drawon=["null check|0.6", 0.6]),
     tx("fix **lag** gaya", 80, 1440, 100, 920, "suggested|0.0")]
S.append(dict(id="step3", type="stage", wipe="fade", voice=V, layers=L))

V = "ध्यान रखो: Claude को सिर्फ़ error मत दो। वो command भी बताओ जिससे error दोबारा आता है, और ये भी कि error हर बार आता है या कभी कभी।"
L = [tx("**Dhyan** rakho", 80, 230, 110, 920, 0.1),
     box('<div style="width:130px;height:130px;border-radius:65px;background:#FFD60A;display:flex;align-items:center;justify-content:center;font-size:90px;font-weight:800">!</div>', 880, 215, "", wig="सिर्फ़ error|0.6", **pop("ध्यान", 0.0)),
     box(card('<div style="font-size:30px;font-weight:700;color:#667">sirf error</div><div style="font-size:44px;font-weight:800;margin-top:8px">kaafi nahi</div>', 860, "28px 44px"), 110, 520, "", **pop("सिर्फ़ error", -0.2)),
     ic("cross", 790, 540, 120, cue="मत दो", off=-0.1, wig="मत दो|0.3"),
     box(card('<div style="font-size:34px;font-weight:700;color:#667">saath me batao</div><div class="mono" style="font-size:40px;font-weight:700;margin-top:10px">1  command jo error laata hai</div><div class="mono" style="font-size:40px;font-weight:700;margin-top:10px">2  steps to reproduce</div>', 860, "30px 44px"), 110, 800, "", **pop("command", -0.5)),
     box(card('<div style="font-size:40px;font-weight:800">3  har baar <span style="color:#667">ya</span> kabhi kabhi?</div>', 860, "28px 44px"), 110, 1180, "", **pop("हर बार", -0.4)),
     ic("check", 800, 1420, 130, cue="कभी कभी", off=0.2, drawon=["कभी कभी|0.2", 0.6])]
S.append(dict(id="caution", type="stage", wipe="fade", voice=V, layers=L))

V = "याद रखो: error बताओ, options पूछो, फिर fix लगवाओ।"
L = [tx("**Yaad** rakho", 80, 230, 110, 920, 0.1),
     box(card('<span style="font-size:48px;font-weight:800">1</span><span style="font-size:44px;font-weight:700"> error batao</span>', 800, "26px 40px"), 110, 520, "", **pop("error बताओ", -0.3)),
     box(card('<span style="font-size:48px;font-weight:800">2</span><span style="font-size:44px;font-weight:700"> options poochho</span>', 800, "26px 40px"), 110, 740, "", **pop("options पूछो", -0.3)),
     box(card('<span style="font-size:48px;font-weight:800">3</span><span style="font-size:44px;font-weight:700"> fix lagwao</span>', 800, "26px 40px"), 110, 960, "", **pop("fix लगवाओ", -0.3)),
     ic("check", 800, 1200, 120, cue="fix लगवाओ", off=0.3, drawon=["fix लगवाओ|0.3", 0.6]),
     dict(kind="img", img="thumbs", size=400, x=90, y=1250, bob=1, k=[["options पूछो|0.0", {"o": 0}], ["options पूछो|0.4", {"o": 1}]])]
S.append(dict(id="recap", type="stage", wipe="fade", voice=V, layers=L))
S.append(cta_scene())

finish(HERE, "Short 024 Common workflows: fix bugs in 3 steps. Source https://code.claude.com/docs/en/common-workflows.md (read 2026-11-04). Day 1 product-page style.", "Claude Code · Workflows", S)
