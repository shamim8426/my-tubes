"""Generates deck.json for Short 020 (docs: quickstart). Run: .venv\\Scripts\\python -X utf8 channels\\devrobolab\\stories\\020_quickstart\\gen_deck.py
Planned video, NOT rendered / NOT voiced yet (waiting for user approval)."""
import json
from pathlib import Path


def pop(cue, off=-0.1, **kw):
    return dict({"in": f"{cue}|{off}", "spring": True}, **kw)


def ic(name, x, y, size=130, cue=None, off=-0.1, **kw):
    d = dict(kind="icon", name=name, x=x, y=y, size=size)
    if cue:
        d.update(pop(cue, off))
    d.update(kw)
    return d


def tx(html, x, y, size, w, sat, **kw):
    return dict(kind="text", html=html, x=x, y=y, size=size, w=w, stream=True, step=0.14, sat=sat, **kw)


def box(html, x, y, css, **kw):
    return dict(kind="box", html=html, x=x, y=y, css=css, **kw)


def typed(text, x, y, size, sat, w=880, color="#fff", cps=16, **kw):
    return dict(kind="typed", text=text, x=x, y=y, size=size, w=w, sat=sat, color=color, cps=cps, mono=True, **kw)


def flow(a, b, at, **kw):
    return dict(kind="flow", **{"from": a, "to": b}, at=at, **kw)


def ring(step, cue):
    """recurring step ring (signature): step 1..4 -> 25..100 %"""
    return dict(kind="ring", size=180, x=830, y=200, sw=20, mul=4, unit="/4",
                k=[[0.0, {"f": (step - 1) / 4}], [f"{cue}|0", {"f": (step - 1) / 4}], [f"{cue}|0.6", {"f": step / 4}]], **{"in": 0.1, "spring": True})


def win(title, w, h, dark=True):
    bg, fg, bar = ("#111", "#fff", "#2a2a2a") if dark else ("#fff", "#111", "#111")
    return (f'<div style="width:{w}px;height:{h}px;border:6px solid #111;border-radius:36px;background:{bg};color:{fg};overflow:hidden;position:relative;box-sizing:border-box">'
            f'<div style="height:80px;background:{bar};display:flex;align-items:center;gap:22px;padding-left:28px"><div class="dot3"><i style="background:#FFD60A"></i><i style="background:#888"></i><i style="background:#888"></i></div>'
            f'<div class="mono" style="font-size:32px;color:#FFD60A">{title}</div></div></div>')


scenes = []

# ---------- S0 hook: kinetic counter + 4 step icons
V0 = "Claude Code चार steps में शुरू होता है: install, login, पहला सवाल, और पहला code change। चलो, एक एक करके देखते हैं।"
step_icons = [("terminal", "Install", "install,"), ("key", "Login", "login,"), ("chat", "Sawal", "पहला सवाल"), ("code", "Code change", "पहला code change")]
L = [dict(kind="count", to=4, size=440, x=60, y=230, css="width:340px;text-align:center", k=[[0.0, {"o": 1, "f": 1}]], **{"in": 0.02, "ind": 0.4, "spring": True}),
     tx("**steps** mein shuru", 400, 360, 100, 600, 0.3),
     dict(kind="spark", pts=[[360, 250, 26, 0], [90, 640, 22, 2], [400, 650, 20, 4]], sp=4)]
for i, (n, lab, cue) in enumerate(step_icons):
    cx = 175 + i * 230
    L.append(ic(n, cx - 85, 830, 170, cue=cue, label=lab, ls=32, lw=170, float={"a": 8, "f": 1.8, "ph": i * 1.3}))
    if i < 3:
        L.append(flow([cx + 95, 915], [cx + 135, 915], f"{step_icons[i + 1][2]}|-0.3", dur=0.35, sw=7, n=1, per=1.2, r=11))
hk = [[0.0, {"f": 0}]]
for i, (_, _, cue) in enumerate(step_icons):
    hk += [[f"{cue}|-0.1", {"f": i / 4}], [f"{cue}|0.4", {"f": (i + 1) / 4}]]
L += [dict(kind="ring", size=330, x=80, y=1130, sw=28, mul=4, unit="/4", k=hk, **{"in": 0.3, "spring": True}),
      tx("Chalo, **ek ek** karke", 450, 1190, 92, 560, "चलो|0"),
      dict(kind="img", img="wave", size=420, x=600, y=1500, bob=1, k=[["चलो|-0.2", {"x": 1200, "o": 1}], ["चलो|0.5", {"x": 600}]])]
scenes.append(dict(id="hook", type="stage", wipe="right", voice=V0, layers=L))

# ---------- S1 install: terminal typing + zoom-through transition
V1 = "Step एक, install। Terminal खोलो, यानी text वाली window, और install command चलाओ। फिर claude --version लिखो। Version number आए, तो install सही है।"
L = [tx("**Step 1** Install", 80, 230, 96, 720, 0.12), ring(1, "Step एक"),
     box(win("terminal", 920, 400), 80, 400, "", sh=True, **pop("Terminal खोलो", -0.2)),
     typed("$ curl -fsSL https://claude.ai/install.sh | bash", 112, 510, 29, "install command|-0.1", w=860, cps=24),
     typed("$ claude --version", 112, 585, 44, "claude --version|-0.2", cps=14),
     typed("<version number> (Claude Code)", 112, 665, 36, "Version number आए|0", color="#FFD60A", cps=24, cursor=False),
     ic("box", 100, 940, 180, cue="install command|0.3", label="install", ls=36, lw=180, float=8),
     flow([300, 1030], [390, 1030], "claude --version|-0.5", dur=0.4, sw=8, n=2, per=1.3),
     ic("terminal", 410, 940, 180, cue="claude --version|-0.2", label="--version", ls=36, lw=180, float={"a": 8, "ph": 1}),
     flow([610, 1030], [700, 1030], "Version number आए|-0.3", dur=0.4, sw=8, n=2, per=1.3),
     ic("check", 720, 940, 180, cue="Version number आए|0.2", label="sahi!", ls=36, lw=180, wig="Version number आए|0.5", drawon=["Version number आए|0.1", .6]),
     tx("Version **aaya** = install **sahi**", 80, 1330, 100, 920, "install सही|-0.8"),
     dict(kind="spark", pts=[[930, 940, 28, 0], [960, 1040, 20, 2.4]], sp=4)]
scenes.append(dict(hideN=True, id="install", type="stage", wipe="zoom", voice=V1, layers=L))

# ---------- S2 login: push transition, account chips, key/lock icons
V2 = "Step दो, अपने project folder में claude लिखो। पहली बार login माँगेगा: Claude account या Console account से, browser में prompts follow करो। एक बार login, फिर दोबारा नहीं।"
chips = ["Pro", "Max", "Ultra", "Team", "Enterprise", "Console"]
CPOS = [(80, 1040), (240, 1040), (410, 1040), (610, 1040), (80, 1160), (380, 1160)]
L = [tx("**Step 2** Login", 80, 230, 96, 720, 0.12), ring(2, "Step दो"),
     box(win("terminal", 920, 300), 80, 400, "", sh=True, **pop("project folder", -0.3)),
     typed("$ cd /path/to/your/project", 112, 505, 36, "project folder|0", cps=20),
     typed("$ claude", 112, 580, 52, "claude लिखो|-0.2", color="#FFD60A", cps=12),
     ic("key", 90, 780, 170, cue="login माँगेगा|-0.2", label="login", ls=34, lw=170, float=9, wig="login माँगेगा|0.3"),
     flow([280, 860], [400, 860], "browser में|-0.9", dur=0.4, sw=8, n=2, per=1.2),
     ic("globe", 420, 780, 170, cue="browser में|-0.5", label="browser", ls=34, lw=170, float={"a": 8, "ph": 2}, spin=0),
     flow([610, 860], [730, 860], "browser में|0.2", dur=0.4, sw=8, n=2, per=1.2),
     ic("check", 750, 780, 170, cue="prompts follow|0", label="ho gaya", ls=34, lw=170, drawon=["prompts follow|0", .6])]
for i, c in enumerate(chips):
    L.append(box(f'<div class="keycap" style="font-size:40px">{c}</div>', CPOS[i][0], CPOS[i][1], "", float={"a": 6, "ph": i * 1.1}, **pop("Claude account" if i < 5 else "Console account", -0.1 + 0.16 * (i % 5))))
L += [box(win("browser", 920, 250, dark=False), 80, 1310, "", sh=True, **pop("browser में", 0.5)),
      ic("user", 130, 1420, 110, cue="browser में", off=0.8, float=5),
      flow([260, 1475], [400, 1475], "prompts follow|-0.6", dur=0.4, sw=7, n=2, per=1.1),
      ic("lock", 420, 1415, 120, cue="prompts follow", off=-0.3, wig="prompts follow|0.4"),
      ic("check", 600, 1415, 120, cue="prompts follow", off=0.5, drawon=["prompts follow|0.5", .5]),
      ic("lock", 80, 1640, 130, cue="एक बार login", label=None, wig="एक बार login|0.4", float=6),
      tx("**Ek baar** login, dobara nahi", 250, 1650, 76, 760, "एक बार login|0")]
scenes.append(dict(hideN=True, id="login", type="stage", wipe="push", voice=V2, layers=L))

# ---------- S3 first question: iris reveal, speech bubble, icon hub with orbit + connectors with travelling dots, camera push
V3 = "Step तीन, पहला सवाल: what does this project do? Claude तुम्हारी files खुद पढ़ लेता है, तुम्हें context जोड़ना नहीं पड़ता।"
CX, CY = 540, 1140
L = [tx("**Step 3** Pehla sawal", 80, 230, 96, 720, 0.12), ring(3, "Step तीन"),
     box('<div style="padding:34px 44px;font-size:54px;font-weight:800;line-height:1.15">what does this project do?</div>', 80, 520, "width:920px;box-sizing:border-box", cls="bubble", **pop("what does this project", -0.4)),
     dict(kind="img", img="think", size=500, x=CX - 250, y=CY - 290, bob=1, k=[["files खुद|-0.6", {"o": 0}], ["files खुद|-0.1", {"o": 1}]])]
for i, (n, lab) in enumerate([("folder", "folder"), ("file", "file"), ("code", "code"), ("file", "file")]):
    orb = {"cx": CX, "cy": CY, "rx": 340, "ry": 290, "a0": 270 + i * 90, "w": 14}
    L.append(flow({"orbit": orb}, [CX, CY], f"files खुद|{0.2 + i * .35}", dur=0.4, sw=6, n=1, per=1.3, r=13, head=False))
    L.append(ic(n, 0, 0, 140, cue="files खुद", off=0.0 + i * .3, orbit=orb, label=None))
for i, n in enumerate(["file", "code"]):
    orb = {"cx": CX, "cy": CY, "rx": 190, "ry": 150, "a0": 90 + i * 180, "w": -20}
    L.append(flow({"orbit": orb}, [CX, CY], f"files खुद|{1.2 + i * .35}", dur=0.4, sw=6, n=1, per=1.1, r=12, head=False))
    L.append(ic(n, 0, 0, 100, cue="files खुद", off=1.0 + i * .3, orbit=orb, label=None))
L += [tx("**Context** khud, jodna nahi", 80, 1530, 80, 900, "context|-0.3"),
      dict(kind="spark", pts=[[170, 760, 24, 0], [900, 780, 24, 2], [860, 1360, 22, 4]], sp=4)]
scenes.append(dict(hideN=True, id="question", type="stage", wipe="iris", voice=V3, layers=L, cam=[[0, {"s": 1.0}], [9, {"s": 1.06}]]))

# ---------- S4 first code change: before / after split, keycap + cursor click, PiP robot
V4 = "Step चार, पहला code change। बोलो, add a hello world function to the main file। Claude सही file ढूँढकर बदलाव दिखाता है, और पूछे तो Yes चुनो।"


def code_card(lbl, after):
    rows = "".join(f'<div style="height:20px;border-radius:10px;margin:14px 0;width:{w}%;background:#111"></div>' for w in (80, 55, 70))
    new = ('<div class="mono" style="margin:14px 0;font-size:34px;font-weight:700;background:#FFD60A;border-radius:10px;padding:2px 10px">+ function hello()</div>' if after
           else '<div style="height:20px;border-radius:10px;margin:14px 0;width:40%;background:#ddd"></div>')
    return (f'<div style="width:440px;height:360px;border:6px solid #111;border-radius:30px;background:#fff;overflow:hidden;box-sizing:border-box">'
            f'<div style="height:70px;background:#111;color:#FFD60A;display:flex;align-items:center;padding-left:24px;font-size:30px" class="mono">{lbl}</div><div style="padding:14px 28px">{rows}{new}</div></div>')


L = [tx("**Step 4** Pehla code change", 80, 230, 88, 740, 0.12), ring(4, "Step चार"),
     box('<div style="padding:26px 40px;font-size:46px;font-weight:800;line-height:1.2">add a hello world function to the main file</div>', 80, 560, "width:920px;box-sizing:border-box", cls="bubble y", **pop("add a hello world", -0.3)),
     box(code_card("main.js · BEFORE", False), 80, 820, "", sh=True, **pop("add a hello world", 0.4)),
     box(code_card("main.js · AFTER", True), 560, 820, "", sh=True, **pop("बदलाव दिखाता", -0.2)),
     box('<div style="font-size:30px;font-weight:800">pehle</div>', 80, 1200, "", **pop("add a hello world", 0.6)),
     box('<div style="font-size:30px;font-weight:800">baad me</div>', 560, 1200, "", **pop("बदलाव दिखाता", 0.0)),
     ic("arrow", 478, 960, 84, cue="बदलाव दिखाता", off=-0.3, float={"a": 5, "f": 3}),
     box('<div class="keycap" style="font-size:56px;padding:8px 44px">Yes</div>', 120, 1330, "", wig="Yes चुनो|0.5", **pop("Yes चुनो", -0.3)),
     ic("cursor", 0, 0, 100, k=[["Yes चुनो|-0.4", {"x": 520, "y": 1500, "o": 0}], ["Yes चुनो|0.0", {"x": 520, "y": 1500, "o": 1}], ["Yes चुनो|0.5", {"x": 300, "y": 1390}]], wig="Yes चुनो|0.5"),
     ic("check", 420, 1330, 110, cue="Yes चुनो", off=0.6, drawon=["Yes चुनो|0.6", .5]),
     box('<div style="width:250px;height:250px;border-radius:125px;border:7px solid #111;background:#FFD60A;box-shadow:0 18px 40px rgba(0,0,0,.2)"></div>', 730, 1290, "", **pop("Claude सही file", 0.0)),
     dict(kind="img", img="thumbs", size=290, x=710, y=1290, crop=[0.0, 1.0], k=[["Claude सही file|0.2", {"o": 0}], ["Claude सही file|0.5", {"o": 1}]]),
     ic("magnifier", 90, 1640, 150, cue="Claude सही file", off=-0.2, label="sahi file", ls=32, lw=150, float=7),
     flow([260, 1715], [380, 1715], "Claude सही file|0.3", dur=0.4, sw=8, n=2, per=1.1),
     ic("file", 400, 1640, 150, cue="Claude सही file", off=0.5, label="main file", ls=32, lw=150, float={"a": 7, "ph": 1}),
     flow([570, 1715], [690, 1715], "बदलाव दिखाता|0.3", dur=0.4, sw=8, n=2, per=1.1),
     ic("code", 710, 1640, 150, cue="बदलाव दिखाता", off=0.4, label="badlav", ls=32, lw=150, wig="बदलाव दिखाता|0.9")]
scenes.append(dict(hideN=True, id="change", type="stage", wipe="up", voice=V4, layers=L))

# ---------- S5 git + shortcuts: fade, svgbot pointing, icon trail
V5 = "Git भी बातों से: बोलो, commit my changes with a descriptive message। Shortcuts: slash help, slash clear, और Shift Tab से permission mode बदलता है।"
rows = [("/help", "bulb", "commands dikhata", "slash help"), ("/clear", "cross", "history saaf", "slash clear"), ("Shift+Tab", "shield", "permission mode", "Shift Tab")]
L = [box('<div style="padding:28px 40px;font-size:46px;font-weight:800;line-height:1.2">commit my changes with a descriptive message</div>', 80, 240, "width:920px;box-sizing:border-box", cls="bubble", **pop("commit my changes", -0.4)),
     ic("branch", 100, 540, 150, cue="Git भी", off=0.2, label="git", ls=34, lw=150, float=7),
     flow([270, 615], [420, 615], "commit my changes|0.5", dur=0.4, sw=8, n=2, per=1.2),
     ic("check", 440, 540, 150, cue="commit my changes", off=0.9, label="commit", ls=34, lw=150, drawon=["commit my changes|1.0", .6]),
     dict(kind="svgbot", size=640, x=-130, y=980, talk=[[0.5, 9]], k=[[0, {"x": -600, "ar": 0}], [0.8, {"x": -110, "e": "b"}], ["slash help|-0.3", {"ar": -80}], ["slash clear|0", {"ar": -88}], ["Shift Tab|0", {"ar": -96}]])]
for i, (key, n, lab, cue) in enumerate(rows):
    y = 940 + i * 220
    L.append(flow([330, 1250], [450, y + 55], f"{cue}|-0.5", dur=0.4, sw=6, n=2, per=1.1, r=13, head=False))
    L.append(ic(n, 460, y, 110, cue=cue, off=-0.2, float={"a": 5, "ph": i * 1.5}))
    L.append(box(f'<div class="keycap" style="font-size:44px">{key}</div><div style="font-size:34px;font-weight:700;margin-top:6px">{lab}</div>', 600, y - 6, "width:400px", **pop(cue, 0.0)))
L.append(tx("Git bhi **baaton** se", 80, 1650, 92, 920, "Git भी|0.1"))
scenes.append(dict(id="git", type="stage", wipe="fade", voice=V5, layers=L))

# ---------- S6 recap + CTA: icons assemble, kinetic counter 4/4, PiP robot
V6 = "तो याद रखो: install, login, सवाल, और code change। तुम पहले कौन सा सवाल पूछोगे? Comment में बताओ।"
recap = [("terminal", "Install", "install,"), ("key", "Login", "login,"), ("chat", "Sawal", "सवाल,"), ("code", "Code", "code change")]
L = [dict(kind="count", to=4, suf="/4", size=170, x=80, y=560, css="width:360px", k=[[0.0, {"f": 0, "o": 1}]] + sum([[[f"{c}|-0.05", {"f": i / 4}], [f"{c}|0.3", {"f": (i + 1) / 4}]] for i, (_, _, c) in enumerate(recap)], []))]
starts = [(-300, 100), (1300, 80), (-300, 900), (1300, 900)]
for i, (n, lab, cue) in enumerate(recap):
    cx = 175 + i * 230
    L.append(ic(n, 0, 0, 150, label=lab, ls=32, lw=150, k=[[0.0, {"x": starts[i][0], "y": starts[i][1], "o": 0}], [f"{cue}|-0.5", {"x": starts[i][0], "y": starts[i][1], "o": 1}], [f"{cue}|0.2", {"x": cx - 75, "y": 280, "e": "b"}]], float={"a": 6, "ph": i * 1.4}))
    L.append(ic("check", cx + 20, 215, 70, cue=cue, off=0.35))
L += [tx("Tum pehle **kaunsa sawal** puchoge?", 80, 740, 96, 920, "कौन सा सवाल|-0.3"),
      box('<div style="width:300px;height:300px;border-radius:150px;border:7px solid #111;background:#FFD60A;box-shadow:0 18px 40px rgba(0,0,0,.2)"></div>', 640, 1230, "", **pop("Comment में", -0.4)),
      dict(kind="img", img="thumbs", size=350, x=615, y=1235, k=[["Comment में|-0.1", {"o": 0}], ["Comment में|0.3", {"o": 1}]]),
      ic("chat", 150, 1250, 190, cue="Comment में", off=-0.2, float=8, wig="Comment में|0.6", label="comment!", ls=36, lw=190)]
scenes.append(dict(id="cta", type="stage", wipe="right", voice=V6, layers=L))

deck = {"_note": "Short 020 Quickstart (PLANNED, not voiced/rendered). Source: https://code.claude.com/docs/en/quickstart.md (read 2026-11-04).",
        "tag": "Claude Code · Quickstart", "rail": True,
        "music": {"file": "shared/music/presentation/Funkorama.mp3", "start": 6, "rel": 12},
        "voice": {"id": "Charon", "style": "Speak like a friendly Indian tech YouTuber chatting casually in Hinglish. Natural conversational pace, warm and clear, a little energetic but not theatrical. No sing-song, no exaggerated emphasis."},
        "scenes": scenes}
Path(__file__).with_name("deck.json").write_text(json.dumps(deck, ensure_ascii=False, indent=1), encoding="utf-8")
print("deck.json written,", len(scenes), "scenes")
