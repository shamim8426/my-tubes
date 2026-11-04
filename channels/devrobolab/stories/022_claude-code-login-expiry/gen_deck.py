"""Short 022 NEWS: Claude Code 2.1.318 shows when the claude.ai sign-in ends. Style: Day 1 'clean product-page'.
Source: https://code.claude.com/docs/en/changelog.md (2.1.318, 2026-11-04). Run: .venv\\Scripts\\python -X utf8 <this file>"""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "templates"))
from ydeck_helpers import *

S = []
V = "Claude Code का login कब खत्म होगा, अब पहले से पता चलेगा। ये आज की update है।"
L = [tx("**Login** kab khatam hoga?", 80, 230, 108, 920, 0.1),
     box(card('<div style="font-size:40px;font-weight:700;color:#667">claude.ai sign-in</div><div style="font-size:110px;font-weight:800;margin-top:26px;line-height:1.1">ends: ?</div>', 800, "44px 50px"), 140, 650, "", **pop(0.5)),
     ic("clock", 640, 900, 240, cue="कब खत्म", off=0.0, float=7, wig="कब खत्म|0.4"),
     ic("lock", 170, 910, 170, cue="login", off=0.1, float={"a": 6, "ph": 1}),
     tx("**pehle se** pata chalega", 80, 1280, 96, 920, "पहले से|-0.2"),
     box('<div class="mono" style="font-size:34px;font-weight:700">Claude Code 2.1.318 · 4 Nov 2026</div>', 80, 470, f"background:#fff;border:2px solid #E3E7EE;border-radius:999px;padding:14px 32px;{SHADOW}", **pop("update", -0.4)),
     dict(kind="img", img="wave", size=330, x=640, y=1560, bob=1, k=[["Claude Code|0.2", {"x": 1200, "o": 1}], ["Claude Code|1.0", {"x": 640}]])]
S.append(dict(id="hook", type="stage", wipe="fade", voice=V, layers=L))

V = "ये वही claude.ai sign-in है जो आपके computer पर save रहता है। जैसे metro card पर लिखी expiry date, अब Claude Code भी अपनी date खुद दिखाता है।"
L = [tx("Login = **sign-in** jo save rehta hai", 80, 230, 90, 920, 0.1),
     box(window("your computer", 440, 400), 80, 620, "", **pop("computer", -0.4)),
     ic("desktop", 170, 740, 250, cue="computer", off=0.0, float=6),
     ic("key", 300, 960, 110, cue="save रहता", off=-0.2, wig="save रहता|0.3"),
     box(card('<div style="font-size:34px;font-weight:700;color:#667">METRO CARD</div><div style="font-size:60px;font-weight:800;line-height:1.1;margin-top:20px">valid till</div><div style="font-size:60px;font-weight:800;margin-top:6px;background:#FFD60A;display:inline-block;padding:0 16px;border-radius:14px">expiry date</div>', 440, "34px 38px"), 560, 650, "", k=[[0, {"r": 3}]], **pop("metro card", -0.2)),
     tx("Claude Code ab **date** dikhata hai", 80, 1180, 92, 920, "Claude Code भी|-0.1"),
     ic("sparkle", 800, 1500, 150, cue="खुद दिखाता", off=0.0, float=7)]
S.append(dict(id="analogy", type="stage", wipe="fade", voice=V, layers=L))

V = "पहला काम: terminal में claude auth status चलाओ। इसमें अब वो date दिखती है, जब तक आपका claude.ai sign-in चलेगा। नाम है loginExpiresAt।"
L = [tx("**Step 1:** auth status", 80, 230, 104, 920, 0.1),
     box(window("terminal", 920, 640, dark=True), 80, 520, "", **pop(0.5)),
     typed("$ claude auth status", 120, 650, 44, "claude auth status|-0.5", w=840, cps=20),
     box(line('<span style="color:#FFD60A">loginExpiresAt</span>: &lt;date&gt;', 44), 120, 800, "background:#2B3038;border-radius:18px;padding:22px 28px;border:3px solid #FFD60A", **pop("loginExpiresAt", -0.9)),
     box(line('# claude.ai sign-in ends on this date', 32, "#9AA3B2"), 120, 960, "", **pop("वो date", -0.3)),
     ic("clock", 120, 1250, 190, cue="वो date", off=0.0, float=7),
     tx("Yahan **date** dikhegi", 350, 1290, 90, 650, "वो date|0.0"),
     ic("check", 780, 1500, 160, cue="loginExpiresAt", off=0.2, drawon=["loginExpiresAt|0.2", 0.6])]
S.append(dict(id="status", type="stage", wipe="fade", voice=V, layers=L))

V = "दूसरा: claude -p की JSON report में credential_expires_at आता है। और तीसरा: text output में, खत्म होने से दस दिन पहले, एक line की warning मिलती है।"
L = [tx("**Step 2 + 3:** claude -p", 80, 230, 78, 920, 0.1),
     box(window("claude -p  (JSON result)", 920, 330, dark=True), 80, 450, "", **pop(0.5)),
     box(line('{ ..., <span style="color:#FFD60A">"credential_expires_at"</span>: "&lt;date&gt;" }', 33), 110, 560, "", **pop("credential_expires_at", -0.8)),
     box(window("claude -p  (text output)", 920, 330, dark=True), 80, 930, "", **pop("तीसरा", -0.3)),
     box(line('<span style="color:#FFD60A">warning:</span> 1 line on stderr', 40), 110, 1040, "", **pop("एक line", -0.5)),
     dict(kind="count", to=10, size=200, x=80, y=1330, css="width:260px;text-align:center", k=[["दस दिन|-0.2", {"o": 1, "f": 0}], ["दस दिन|0.5", {"f": 1}]], **{"in": "दस दिन|-0.3", "ind": 0.3, "spring": True}),
     tx("**din pehle** se warning", 350, 1400, 84, 650, "दस दिन|0.4"),
     ic("bulb", 880, 1220, 120, cue="warning", off=0.0, float=7)]
S.append(dict(id="claudep", type="stage", wipe="fade", voice=V, layers=L))

V = "ध्यान रखो: date निकलने के बाद sign-in fail होता है। तब error साफ़ बताता है, और claude -p में claude auth login और claude setup-token का नाम भी बताता है।"
L = [tx("**Dhyan** rakho", 80, 230, 110, 920, 0.1),
     box('<div style="width:130px;height:130px;border-radius:65px;background:#FFD60A;display:flex;align-items:center;justify-content:center;font-size:90px;font-weight:800">!</div>', 880, 215, "", wig="date निकलने|0.6", **pop("ध्यान", 0.0)),
     box(card('<div style="font-size:50px;font-weight:800">date nikli</div><div style="font-size:44px;margin-top:10px;color:#667">sign-in fail</div>', 860, "34px 44px"), 110, 520, "", **pop("date निकलने", -0.2)),
     ic("cross", 760, 560, 130, cue="fail होता", off=-0.2, wig="fail होता|0.3"),
     box(card('<div style="font-size:34px;font-weight:700;color:#667">error ab saaf batata hai</div>', 860, "26px 44px"), 110, 780, "", **pop("error साफ़", -0.3)),
     box(window("terminal", 860, 250, dark=True), 110, 1000, "", **pop("claude -p में", -0.3)),
     typed("$ claude auth login", 150, 1110, 42, "claude auth login|-0.6", w=800, cps=20),
     typed("$ claude setup-token", 150, 1190, 42, "setup-token|-0.8", w=800, cps=20),
     tx("**error** rasta bhi dikhata hai", 80, 1370, 84, 920, "का नाम भी|-0.2")]
S.append(dict(id="caution", type="stage", wipe="fade", voice=V, layers=L))

V = "तो याद रखो: auth status में date देखो, और claude -p में दस दिन पहले warning मिलेगी।"
L = [tx("**Yaad** rakho", 80, 230, 110, 920, 0.1),
     box(card('<div class="mono" style="font-size:44px;font-weight:700">claude auth status</div><div style="font-size:46px;font-weight:800;margin-top:12px">= <span style="background:#FFD60A;padding:0 12px;border-radius:12px">date</span> dekho</div>', 860, "34px 44px"), 110, 520, "", **pop("auth status", -0.2)),
     box(card('<div class="mono" style="font-size:44px;font-weight:700">claude -p</div><div style="font-size:46px;font-weight:800;margin-top:12px">= <span style="background:#FFD60A;padding:0 12px;border-radius:12px">10 din</span> pehle warning</div>', 860, "34px 44px"), 110, 830, "", **pop("claude -p", -0.2)),
     ic("check", 120, 1180, 150, cue="date देखो", off=0.1, drawon=["date देखो|0.2", 0.6]),
     ic("check", 330, 1180, 150, cue="दस दिन", off=0.1, drawon=["दस दिन|0.2", 0.6]),
     dict(kind="img", img="thumbs", size=420, x=600, y=1230, bob=1, k=[["warning|-0.3", {"o": 0}], ["warning|0.0", {"o": 1}]])]
S.append(dict(id="recap", type="stage", wipe="fade", voice=V, layers=L))
S.append(cta_scene())

finish(HERE, "Short 022 NEWS Claude Code 2.1.318 login expiry. Source https://code.claude.com/docs/en/changelog.md (read 2026-11-04). Day 1 product-page style.", "Claude Code · News", S)
