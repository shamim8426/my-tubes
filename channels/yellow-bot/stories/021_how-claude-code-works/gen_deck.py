"""Generates deck.json for Short 021 (docs: how-claude-code-works) - 'Magic trick' story.
Run: .venv\\Scripts\\python -X utf8 channels\\yellow-bot\\stories\\021_how-claude-code-works\\gen_deck.py [--ph]
--ph also writes silent placeholder wavs (length ~ voice text) into audio/tts for timing stills; real voice = build_deck.py --tts."""
import json
import re
import sys
import wave
from pathlib import Path

HERE = Path(__file__).parent

# ---- FINAL CTA (the user chooses the wording; change ONLY these 3 lines, then: move audio\tts\s_07.wav to _to_delete, run build_deck.py --tts, --render)
CTA_VOICE = "ऐसे ही मज़ेदार Claude Code tricks के लिए Yellow Bot को follow करो।"   # placeholder wording
CTA_SCREEN = "**Yellow Bot** ko follow karo"     # big on-screen line (words between ** get the yellow marker)
CTA_PILL = "Follow"                               # label on the yellow pill that gets clicked


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


def flow(a, b=None, at=0, **kw):
    d = dict(kind="flow", at=at)
    if b is None:
        d["pts"] = a
    else:
        d["from"], d["to"] = a, b
    d.update(kw)
    return d


def win(title, w, h, dark=True):
    bg, fg, bar = ("#111", "#fff", "#2a2a2a") if dark else ("#fff", "#111", "#111")
    return (f'<div style="width:{w}px;height:{h}px;border:6px solid #111;border-radius:36px;background:{bg};color:{fg};overflow:hidden;position:relative;box-sizing:border-box">'
            f'<div style="height:80px;background:{bar};display:flex;align-items:center;gap:22px;padding-left:28px"><div class="dot3"><i style="background:#FFD60A"></i><i style="background:#888"></i><i style="background:#888"></i></div>'
            f'<div class="mono" style="font-size:32px;color:#FFD60A">{title}</div></div></div>')


def ring(f0, f1, cue):
    return dict(kind="ring", size=180, x=830, y=200, sw=20, mul=3, unit="/3",
                k=[[0.0, {"f": f0}], [f"{cue}|0", {"f": f0}], [f"{cue}|0.6", {"f": f1}]], **{"in": 0.1, "spring": True})


scenes = []

# ============ S0 HOOK: 'Magic dekhna hai?' + number 3, wand underline, dust
V0 = "Magic देखना है? Claude Code का trick सिर्फ़ तीन phases का है। तुम बोलो, बाकी वो खुद सँभालता है।"
L = [tx("**Magic** dekhna hai?", 80, 230, 124, 920, 0.1),
     dict(kind="wand", shape="underline", pts=[[90, 552], [610, 552]], at=0.35, dur=0.7, sw=24, ss=18),
     dict(kind="count", to=3, size=420, x=50, y=640, css="width:340px;text-align:center", k=[[0.0, {"o": 1, "f": 1}]], **{"in": 0.2, "ind": 0.4, "spring": True}),
     tx("**phases** ka trick", 400, 760, 100, 600, 0.45),
     dict(kind="dust", from_=[220, 830], at=0.3, n=70, speed=650, life=1.1, size=18, mode="burst"),
     dict(kind="morph", icons=["magnifier", "code", "check"], size=300, x=110, y=1180, ts=["तीन phases|1.3", "तीन phases|2.6"], md=0.45, float=8, **pop("तीन phases", 0.2)),
     box('<div style="font-size:60px;font-weight:800">gather</div>', 110, 1520, "background:#FFD60A;border:6px solid #111;border-radius:999px;padding:6px 34px", **{"in": "तीन phases|0.5", "out": "तीन phases|1.4", "spring": True}),
     box('<div style="font-size:60px;font-weight:800">act</div>', 110, 1520, "background:#FFD60A;border:6px solid #111;border-radius:999px;padding:6px 34px", **{"in": "तीन phases|1.4", "out": "तीन phases|2.7", "spring": True}),
     box('<div style="font-size:60px;font-weight:800">verify</div>', 110, 1520, "background:#FFD60A;border:6px solid #111;border-radius:999px;padding:6px 34px", **{"in": "तीन phases|2.7", "spring": True}),
     dict(kind="img", img="wave", size=480, x=540, y=1380, bob=1, k=[["Magic देखना|0.2", {"x": 1200, "o": 1}], ["Magic देखना|0.9", {"x": 540}]])]
scenes.append(dict(id="hook", type="stage", wipe="right", voice=V0, layers=L))

# ============ S1 ROBOT CASTS: aura + dust + typed prompt
V1 = "तुम बस बोलो: fix the failing tests। फिर Claude, जैसे कोई जादूगर, एक के बाद एक काम करता है। तुम्हें files या commands बताने की ज़रूरत नहीं।"
L = [tx("Tum bas **bolo**", 80, 230, 110, 920, 0.1),
     box(win("terminal", 920, 240), 80, 430, "", sh=True, **pop("fix the failing tests", -0.6)),
     typed("> fix the failing tests", 112, 548, 50, "fix the failing tests|-0.2", cps=17),
     dict(kind="aura", from_=[330, 1180], at=3.0, dur=3.8, r=330),
     dict(kind="svgbot", size=760, x=-60, y=800, talk=[[0.6, 12]], k=[[0, {"x": -700, "ar": 0}], [0.8, {"x": -60, "e": "b"}], ["जादूगर|-0.4", {"ar": -150, "al": 0}], ["जादूगर|0.2", {"al": 150}]]),
     dict(kind="dust", from_=[430, 930], at=3.2, n=60, speed=600, life=1.0, size=16, mode="burst"),
     box('<div style="font-size:30px;font-weight:700;margin-bottom:4px">jaise ek...</div><div style="font-size:60px;font-weight:800;line-height:1.1">jaadugar</div>', 610, 830, "width:380px;padding:26px 34px;box-sizing:border-box",
         cls="sticky", k=[[0, {"r": 3}]], **pop("जादूगर", -0.3)),
     ic("file", 600, 1200, 150, cue="files या commands", off=-0.1, label=None, float=6),
     ic("terminal", 790, 1200, 150, cue="files या commands", off=0.3, label=None, float={"a": 6, "ph": 1}),
     ic("cross", 700, 1170, 90, cue="बताने की ज़रूरत", off=0.0, wig="बताने की ज़रूरत|0.3"),
     tx("**batana** nahi", 560, 1420, 80, 440, "बताने की ज़रूरत|0")]
scenes.append(dict(id="cast", type="stage", wipe="up", voice=V1, layers=L))

# ============ S2 TA-DA: portal + shock + glint + dust, PiP robot
V2 = "और ta-da! Claude ने tests दोबारा चलाकर चेक कर लिया कि सब ठीक है।"
L = [box("", 90, 400, "width:900px;height:360px;border-radius:50px;background:#FFD60A;border:8px solid #111;box-shadow:0 24px 50px rgba(0,0,0,.2)", **pop(0.75)),
     dict(kind="glinttext", html="TA-DA!", x=90, y=480, w=900, size=190, glint=[1.05, 0.7]),
     dict(kind="shock", from_=[540, 580], at=0.75, dur=0.9, r=900, rings=2),
     dict(kind="dust", from_=[540, 580], at=1.0, n=60, speed=640, life=1.1, size=16, mode="burst"),
     ic("check", 330, 860, 340, cue="चेक कर लिया", off=-0.6, wig="चेक कर लिया|0.3", drawon=["चेक कर लिया|-0.5", 0.6]),
     tx("Tests **verify** hue", 80, 1250, 100, 920, "tests दोबारा|0.0"),
     box('<div style="width:260px;height:260px;border-radius:130px;border:7px solid #111;background:#FFD60A;box-shadow:0 18px 40px rgba(0,0,0,.2)"></div>', 720, 1560, "", **pop("सब ठीक", -0.6)),
     dict(kind="img", img="thumbs", size=300, x=700, y=1555, k=[["सब ठीक|-0.4", {"o": 0}], ["सब ठीक|-0.1", {"o": 1}]])]
scenes.append(dict(id="tada", type="stage", wipe="portal", trd=0.7, voice=V2, layers=L))

# ============ S3 TRICK: agentic loop, morph, magnet, flow loop, ring 1/3..3/3
V3 = "अब trick क्या है? इसे कहते हैं agentic loop, यानी बार बार घूमने वाला चक्कर। पहला phase, gather context, यानी files पढ़कर समझना। दूसरा, take action, यानी code बदलना। तीसरा, verify results, यानी tests चलाकर चेक करना।"
N1, N2, N3 = (540, 830), (850, 1250), (230, 1250)
rg = dict(kind="ring", size=180, x=830, y=200, sw=20, mul=3, unit="/3", **{"in": 0.1, "spring": True},
          k=[[0.0, {"f": 0}], ["gather context|0", {"f": 0}], ["gather context|0.6", {"f": 1 / 3}], ["take action|0", {"f": 1 / 3}], ["take action|0.6", {"f": 2 / 3}], ["verify results|0", {"f": 2 / 3}], ["verify results|0.6", {"f": 1}]])
L = [tx("**Agentic** loop", 80, 230, 100, 720, 0.1), rg,
     tx("= baar baar ka chakkar", 80, 360, 54, 740, "agentic loop|0.6", color="#555"),
     ic("magnifier", N1[0] - 90, N1[1] - 90, 180, cue="gather context", off=-0.1, label="gather context", ls=36, lw=300, float=7),
     ic("code", N2[0] - 90, N2[1] - 90, 180, cue="take action", off=-0.1, label="take action", ls=36, lw=300, float={"a": 7, "ph": 1.5}),
     ic("check", N3[0] - 90, N3[1] - 90, 180, cue="verify results", off=-0.1, label="verify results", ls=36, lw=300, float={"a": 7, "ph": 3}),
     flow([[665, 880], [815, 1125]], None, "take action|-0.7", dur=0.4, sw=8, n=2, per=1.4),
     flow([[750, 1250], [330, 1250]], None, "verify results|-0.7", dur=0.4, sw=8, n=2, per=1.4),
     flow([[200, 1130], [430, 880]], None, "verify results|0.9", dur=0.4, sw=8, n=2, per=1.4),
     dict(kind="magnet", to=[N1[0], N1[1]], at=3.6, dur=0.8, stag=0.18, size=100, arc=240, items=[{"name": "file", "from": [90, 560]}, {"name": "folder", "from": [990, 640]}, {"name": "code", "from": [60, 1000]}]),
     tx("**repeat** jab tak kaam ho", 80, 1560, 84, 920, "verify results|1.4")]
scenes.append(dict(id="loop", type="stage", wipe="zoom", voice=V3, layers=L, hideN=True))

# ============ S4 TOOLS: icon hub with orbit + flows, toolbox analogy
V4 = "ये सब काम tools से होते हैं। Tools के बिना Claude सिर्फ़ text बोल सकता है। Tools के साथ वो file पढ़ता, search करता, commands चलाता, web खोलता है, और code intelligence भी, plugins से। जैसे औज़ारों का डिब्बा।"
CX, CY = 540, 1010
cats = [("file", "files"), ("magnifier", "search"), ("terminal", "run"), ("globe", "web"), ("bulb", "code intel")]
cues = ["file पढ़ता", "search करता", "commands चलाता", "web खोलता", "code intelligence"]
L = [tx("**Tools** = Claude ke haath", 80, 230, 96, 920, 0.1),
     dict(kind="img", img="think", size=480, x=CX - 240, y=CY - 260, bob=1, k=[["tools से|-0.3", {"o": 0}], ["tools से|0.2", {"o": 1}]])]
for i, ((n, lab), cue) in enumerate(zip(cats, cues)):
    orb = {"cx": CX, "cy": CY, "rx": 345, "ry": 300, "a0": 270 + i * 72, "w": 11}
    L.append(flow({"orbit": orb}, [CX, CY], f"{cue}|0.0", dur=0.4, sw=6, n=1, per=1.3, r=13, head=False))
    L.append(ic(n, 0, 0, 130, cue=cue, off=-0.2, orbit=orb, label=lab, ls=30, lw=130))
L += [box('<div style="font-size:30px;font-weight:700">jaise ek...</div><div style="font-size:62px;font-weight:800;line-height:1.1">toolbox</div>', 80, 1480, "width:520px;padding:26px 36px;box-sizing:border-box", cls="sticky", k=[[0, {"r": -2.5}]], **pop("औज़ारों का डिब्बा", -0.3)),
      ic("box", 700, 1470, 180, cue="औज़ारों का डिब्बा", off=0.0, float=7, wig="औज़ारों का डिब्बा|0.4"),
      box('<div style="font-size:46px;font-weight:800;line-height:1.15">tools ke bina:<br><span style="color:#999">sirf text</span></div>', 80, 1700, "", **pop("सिर्फ़ text", -0.2))]
scenes.append(dict(id="tools", type="stage", wipe="push", voice=V4, layers=L))

# ============ S5 YOU STEER: Esc, before/after, typed correction, Enter
V5 = "और तुम भी इस loop का हिस्सा हो। Esc दबाओ, Claude तुरंत रुक जाता है। या सुधार लिखकर Enter दबाओ, वो अपना रास्ता बदल लेता है।"


def path_card(lbl, ok):
    col = "#FFD60A" if ok else "#fff"
    return (f'<div style="width:440px;height:330px;border:6px solid #111;border-radius:30px;background:{col};overflow:hidden;box-sizing:border-box;position:relative">'
            f'<div style="height:64px;background:#111;color:#FFD60A;display:flex;align-items:center;padding-left:22px;font-size:28px" class="mono">{lbl}</div></div>')


L = [tx("**Tum** bhi loop me", 80, 230, 100, 920, 0.1),
     box('<div class="keycap" style="font-size:80px;padding:10px 60px">Esc</div>', 90, 480, "", wig="Esc दबाओ|0.5", **pop("Esc दबाओ", -0.3)),
     ic("cross", 420, 470, 150, cue="तुरंत रुक", off=-0.2, wig="तुरंत रुक|0.3"),
     tx("**turant** ruk", 620, 505, 80, 400, "तुरंत रुक|0.0"),
     box(path_card("pehle: galat raasta", False), 80, 760, "", sh=True, **pop("सुधार लिखकर", -0.6)),
     box(path_card("baad me: naya raasta", True), 560, 760, "", sh=True, **pop("रास्ता बदल", -0.4)),
     ic("cross", 190, 880, 130, cue="सुधार लिखकर", off=-0.3),
     ic("check", 670, 880, 130, cue="रास्ता बदल", off=-0.1, wig="रास्ता बदल|0.3"),
     box(win("terminal", 920, 250), 80, 1180, "", sh=True, **pop("सुधार लिखकर", 0.0)),
     typed("The issue is in the session handling", 112, 1300, 38, "सुधार लिखकर|0.3", w=860, cps=20),
     box('<div class="keycap" style="font-size:60px;padding:8px 44px">Enter</div>', 120, 1500, "", wig="Enter दबाओ|0.6", **pop("Enter दबाओ", -0.3)),
     ic("cursor", 0, 0, 110, k=[["Enter दबाओ|-0.5", {"x": 560, "y": 1700, "o": 0}], ["Enter दबाओ|-0.1", {"x": 560, "y": 1700, "o": 1}], ["Enter दबाओ|0.5", {"x": 300, "y": 1570}]], wig="Enter दबाओ|0.6"),
     tx("rasta **badal** leta hai", 80, 1680, 80, 920, "रास्ता बदल|0.3")]
scenes.append(dict(id="steer", type="stage", wipe="iris", voice=V5, layers=L))

# ============ S6 RECAP: assemble, wand underline, loop return arrow, PiP robot, question
V6 = "तो याद रखो: gather, act, verify, और दोहराओ। Delegate करो, dictate नहीं।"
L = [dict(kind="assemble", text="3 phases", cx=540, cy=380, size=200, at=0.3, dur=0.9, gap=8),
     dict(kind="wand", shape="underline", pts=[[150, 520], [930, 520]], at=1.25, dur=0.7, sw=22, ss=18),
     ic("magnifier", 140, 620, 150, cue="gather", off=-0.1, label="gather", ls=34, lw=150, float=7),
     ic("code", 465, 620, 150, cue="act", off=-0.1, label="act", ls=34, lw=150, float={"a": 7, "ph": 1.4}),
     ic("check", 790, 620, 150, cue="verify", off=-0.1, label="verify", ls=34, lw=150, float={"a": 7, "ph": 2.8}),
     flow([[300, 695], [455, 695]], None, "act|0.0", dur=0.3, sw=7, n=1, per=1.1, r=11),
     flow([[625, 695], [780, 695]], None, "verify|0.0", dur=0.3, sw=7, n=1, per=1.1, r=11),
     flow([[860, 840], [860, 930], [215, 930], [215, 840]], None, "दोहराओ|-0.2", dur=0.7, sw=8, n=2, per=1.6),
     ic("arrow", 470, 880, 90, cue="दोहराओ", off=0.4, rotation=180) if False else dict(kind="text", html="**dohrao**", x=420, y=950, size=56, w=300, stream=True, sat="दोहराओ|0.2"),
     tx("**Delegate** karo, dictate nahi", 80, 1110, 100, 920, "Delegate|-0.1"),
     box('<div style="width:310px;height:310px;border-radius:155px;border:7px solid #111;background:#FFD60A;box-shadow:0 18px 40px rgba(0,0,0,.2)"></div>', 640, 1500, "", **pop("dictate", -0.5)),
     dict(kind="img", img="thumbs", size=360, x=615, y=1505, k=[["dictate|-0.2", {"o": 0}], ["dictate|0.2", {"o": 1}]]),
     ic("sparkle", 150, 1560, 190, cue="Delegate", off=0.2, float=8, label=None)]
scenes.append(dict(id="recap", type="stage", wipe="fade", voice=V6, layers=L))

# ============ S7 FOLLOW CTA (~3-4 s): robot thumbs-up, big Follow pill + cursor click + dust, bell wiggle
L = [tx(CTA_SCREEN, 80, 260, 120, 920, 0.15),
     box(f'<div style="font-size:120px;font-weight:800;line-height:1">{CTA_PILL}</div>', 190, 800, "background:#FFD60A;border:9px solid #111;border-radius:999px;padding:30px 110px;box-shadow:0 24px 50px rgba(0,0,0,.22)", wig=1.5, **pop(0.5)),
     dict(kind="icon", name="cursor", x=0, y=0, size=140, k=[[0.9, {"x": 820, "y": 1060, "o": 0}], [1.0, {"x": 820, "y": 1060, "o": 1}], [1.5, {"x": 520, "y": 880}]], wig=1.55),
     dict(kind="dust", from_=[540, 860], at=1.5, n=50, speed=620, life=1.0, size=16, mode="burst"),
     ic("bell", 430, 1080, 200, cue=None, wig=1.9, float=6, **{"in": 1.7, "spring": True}),
     dict(kind="img", img="thumbs", size=520, x=260, y=1300, bob=1, k=[[0.2, {"x": -700, "o": 1}], [0.9, {"x": 260}]])]
scenes.append(dict(id="follow", type="stage", wipe="right", voice=CTA_VOICE, layers=L))

for sc in scenes:
    for L in sc["layers"]:
        if "from_" in L:
            L["from"] = L.pop("from_")

deck = {"_note": "Short 021 How Claude Code works - 'Magic trick' story. Source: https://code.claude.com/docs/en/how-claude-code-works.md (read 2026-11-04).",
        "tag": "Claude Code · How it works", "rail": True,
        "music": {"file": "shared/music/presentation/Funkorama.mp3", "start": 6, "rel": 12},
        "voice": {"id": "Charon", "style": "Speak like a friendly Indian tech YouTuber chatting casually in Hinglish. Natural conversational pace, warm and clear, a little energetic but not theatrical. No sing-song, no exaggerated emphasis."},
        "scenes": scenes}
(HERE / "deck.json").write_text(json.dumps(deck, ensure_ascii=False, indent=1), encoding="utf-8")
print("deck.json written,", len(scenes), "scenes, voice chars", [len(re.sub(r"\s+", " ", s["voice"])) for s in scenes])
if "--ph" in sys.argv:
    (HERE / "audio" / "tts").mkdir(parents=True, exist_ok=True)
    for i, sc in enumerate(scenes):
        d = 0.066 * len(re.sub(r"\s+", " ", sc["voice"]))
        with wave.open(str(HERE / "audio" / "tts" / f"s_{i:02d}.wav"), "wb") as w:
            w.setnchannels(1), w.setsampwidth(2), w.setframerate(24000)
            w.writeframes(b"\x00\x00" * int(24000 * d))
    print("placeholder wavs written (NOT real voice)")
