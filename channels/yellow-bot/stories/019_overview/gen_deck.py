"""Generates deck.json for Short 019 (docs: overview). Run: .venv\\Scripts\\python -X utf8 gen_deck.py"""
import json
from pathlib import Path

CHK = '<svg width="{s}" height="{s}" viewBox="0 0 150 150" style="flex:none"><circle cx="75" cy="75" r="68" fill="#FFD60A" stroke="#111" stroke-width="8"/><path d="M42 78L65 101L110 52" fill="none" stroke="#111" stroke-width="16" stroke-linecap="round" stroke-linejoin="round"/></svg>'


def row(text, sub="", size=54):
    return (CHK.format(s=84) + f'<div><div style="font-size:{size}px;font-weight:800;line-height:1.1">{text}</div>'
            + (f'<div style="font-size:34px;font-weight:600;color:#555;margin-top:2px">{sub}</div>' if sub else "") + "</div>")


ROWCSS = "width:{w}px;height:{h}px;border:6px solid #111;border-radius:34px;background:#fff;display:flex;align-items:center;gap:28px;padding:0 30px;box-sizing:border-box"


def box(html, x, y, css, **kw):
    d = dict(kind="box", html=html, x=x, y=y, css=css)
    d.update(kw)
    return d


def win(title, body, dark=False, w=860, h=640):
    bg = "#111" if dark else "#fff"
    fg = "#fff" if dark else "#111"
    bar = "#2a2a2a" if dark else "#111"
    return (f'<div style="width:{w}px;height:{h}px;border:6px solid #111;border-radius:36px;background:{bg};color:{fg};overflow:hidden;position:relative">'
            f'<div style="height:84px;background:{bar};display:flex;align-items:center;gap:22px;padding-left:28px"><div class="dot3"><i style="background:#FFD60A"></i><i style="background:#888"></i><i style="background:#888"></i></div>'
            f'<div class="mono" style="font-size:34px;color:#FFD60A">{title}</div></div>'
            f'<div style="padding:30px 36px">{body}</div></div>')


def mono(t, col="#111", size=44, extra=""):
    return f'<div class="mono" style="font-size:{size}px;line-height:1.5;color:{col};{extra}">{t}</div>'


def chip(t):
    return f'<div class="yel" style="display:inline-block;margin-top:26px;font-size:46px;font-weight:800;padding:10px 32px;border-radius:999px;border:5px solid #111">{t}</div>'


def bars(n, yel=(1,)):
    return "".join(f'<div style="height:22px;border-radius:11px;margin:14px 0;width:{60 + (i * 37) % 35}%;background:{"#FFD60A" if i in yel else "#111"}"></div>' for i in range(n))


CARDS = [
    ("एक, Terminal", "Terminal", True, mono("$ claude", "#FFD60A", 52) + mono("● login bug theek kiya", "#fff", 44) + mono("● file badli, test pass", "#fff", 44) + mono("█", "#FFD60A", 44),
     "text wali **window**"),
    ("दो, VS Code", "VS Code", False, mono("- if (user = null)", "#111", 40, "text-decoration:line-through;opacity:.6") + mono("+ if (user == null)", "#111", 40, "background:#FFD60A;border-radius:10px;padding:0 12px") + bars(3, ()) + chip("inline diffs"),
     "code ka **editor** (IDE)"),
    ("तीन, JetBrains", "IntelliJ · PyCharm · WebStorm", False, '<div style="display:flex;gap:30px"><div style="width:34%">' + bars(6, (2,)) + '</div><div style="width:60%">' + mono("+ naya code", "#111", 40, "background:#FFD60A;border-radius:10px;padding:0 12px") + bars(4, ()) + "</div></div>" + chip("interactive diff"),
     "ye bhi code ka **editor**"),
    ("चार, Desktop", "Desktop app", False, '<div style="display:flex;gap:26px"><div style="width:50%;border:5px solid #111;border-radius:22px;padding:14px 22px;background:#fff">' + mono("session 1", "#111", 36) + bars(4, (1,)) + '</div><div style="width:50%;border:5px solid #111;border-radius:22px;padding:14px 22px;background:#FFD60A">' + mono("session 2", "#111", 36) + bars(4, (0,)) + "</div></div>" + chip("side by side"),
     "alag **app** me kai sessions saath"),
    ("पाँच, Web", "claude.ai/code", False, mono("task 1 · chal raha hai", "#111", 42, "border:5px solid #111;border-radius:20px;padding:10px 22px;margin:14px 0") + mono("task 2 · chal raha hai", "#111", 42, "border:5px solid #111;border-radius:20px;padding:10px 22px;margin:14px 0;background:#FFD60A") + chip("bina setup"),
     "**browser** me, bina install"),
]


def surfaces():
    L = []
    cues = [c[0] for c in CARDS]
    L.append(dict(kind="text", html="**5 jagah** ek ek karke", x=80, y=520, size=110, w=900, stream=True, step=0.15, sat=0.25, out=f"{cues[0]}|-0.25"))
    L.append(dict(kind="count", to=5, suf="/5", size=250, x=80, y=1320, css="width:520px", k=[[0.1, {"f": 0, "o": 0}], [0.3, {"o": 1}]] +
                  sum([[[f"{cues[i]}|-0.02", {"f": i / 5}], [f"{cues[i]}|0.3", {"f": (i + 1) / 5}]] for i in range(5)], [])))
    for i, (cue, title, dark, body, cap) in enumerate(CARDS):
        nxt = CARDS[i + 1][0] if i < 4 else None
        L.append(box(win(title, body, dark), 100, 300, "", **{"in": f"{cue}|-0.1", "ind": 0.38, "spring": True, "sh": True, "push": 4, **({"out": f"{nxt}|-0.2"} if nxt else {})}))
        L.append(dict(kind="text", html=cap, x=80, y=1000, size=92, w=900, stream=True, step=0.15, sat=f"{cue}|0.25", **({"out": f"{nxt}|-0.2"} if nxt else {})))
    return L


scenes = []
V0 = "Claude Code पाँच जगह चलता है! ये एक AI helper है, जो files पढ़ता है, code लिखता है और commands चलाता है। जैसे कोई समझदार assistant, तुम्हारे साथ बैठा हो।"
scenes.append(dict(id="hook", type="stage", wipe="right", voice=V0, layers=[
    dict(kind="count", to=5, size=440, x=60, y=240, css="width:340px;text-align:center", k=[[0.0, {"o": 1, "f": 1}]], **{"in": 0.02, "ind": 0.4, "spring": True}),
    dict(kind="text", html="**jagah** chalta hai", x=400, y=380, size=104, w=600, stream=True, step=0.2, sat=0.3),
    dict(kind="img", img="work", size=430, x=690, y=800, bob=1, k=[["AI helper|-0.2", {"x": 1200, "o": 1}], ["AI helper|0.5", {"x": 690}]]),
    box(row("Files padhta", "", 48), 70, 800, ROWCSS.format(w=640, h=130), **{"in": "files पढ़ता|-0.1", "spring": True, "sh": True}),
    box(row("Code likhta", "", 48), 70, 960, ROWCSS.format(w=640, h=130), **{"in": "code लिखता|-0.1", "spring": True, "sh": True}),
    box(row("Commands chalata", "", 48), 70, 1120, ROWCSS.format(w=640, h=130), **{"in": "commands चलाता|-0.1", "spring": True, "sh": True}),
    box('<div style="font-size:34px;font-weight:700;margin-bottom:6px">jaise ek...</div><div style="font-size:66px;font-weight:800;line-height:1.1">smart assistant</div>', 110, 1340,
        "width:700px;padding:30px 44px;box-sizing:border-box", cls="sticky", k=[[0, {"r": -3}]], **{"in": "जैसे कोई|-0.1", "spring": True}),
]))

V1 = "इसे बोलते हैं agentic, यानी जो खुद काम करे। तुम बोलो, login bug ठीक करो। ये पूरा project देखता है, कई files बदलता है, और चेक करता है कि सब चल रहा है।"
scenes.append(dict(id="agentic", type="stage", wipe="up", voice=V1, layers=[
    dict(kind="text", html="**Agentic** = khud kaam karne wala", x=80, y=250, size=92, w=920, stream=True, step=0.15, sat=0.4),
    box('<span style="color:#FFD60A;margin-right:24px">&gt;</span> login bug theek karo', 80, 700, "width:920px;height:150px;border-radius:34px;padding:0 44px;display:flex;align-items:center;font-size:56px;font-weight:700;font-family:Mono,monospace;box-sizing:border-box", cls="ink", sh=True, **{"in": "तुम बोलो|-0.1", "spring": True}),
    dict(kind="draw", x=0, y=0, w=1080, h=1920, sw=9, items=[{"t": "arrow", "from": [540, 868], "to": [540, 960], "at": "ये पूरा|-0.2", "dur": .5}]),
    box(row("Pura project dekhta hai"), 80, 990, ROWCSS.format(w=920, h=128), **{"in": "पूरा project|-0.1", "spring": True, "sh": True}),
    box(row("Kai files badalta hai"), 80, 1140, ROWCSS.format(w=920, h=128), **{"in": "कई files|-0.1", "spring": True, "sh": True}),
    box(row("Check bhi karta hai"), 80, 1290, ROWCSS.format(w=920, h=128), **{"in": "चेक करता|-0.1", "spring": True, "sh": True}),
]))

V2 = "वो पाँच जगहें: एक, Terminal, यानी text वाली window। दो, VS Code। तीन, JetBrains। ये दोनों code लिखने के editor हैं, जिन्हें IDE कहते हैं। चार, Desktop app। पाँच, Web, यानी browser में, बिना install के।"
scenes.append(dict(id="surfaces", type="stage", wipe="right", voice=V2, layers=surfaces()))

scenes.append(dict(id="usecases", type="list", wipe="fade", icons=True, head="Fayda: wo **boring** kaam", hy=230, y0=500, rh=320, ksize=84, dsize=46,
                   voice="तुम्हें फ़ायदा? वो boring काम जो तुम टालते हो: tests लिखना, bug ठीक करना, और git commit या pull request बनाना। समय बचता है।",
                   items=[{"k": "Tests likhna", "d": "jo tum taalte rehte ho"}, {"k": "Bug theek karna", "d": "error batao, fix wo kare"}, {"k": "Commit + pull request", "d": "git ka kaam bhi wahi karta hai"}],
                   foot="Tumhara **time bachta** hai", cues=["tests लिखना", "bug ठीक", "git commit", "समय बचता"]))

V4 = "और इंजन एक ही है। इसलिए CLAUDE.md, यानी project के नियमों की पर्ची, settings और MCP, यानी बाहर के tools जोड़ने का तरीका, हर जगह चलते हैं। जैसे एक दिमाग, कई दरवाज़े।"
door = ["Terminal", "IDE", "Desktop", "Web"]
items = [{"t": "box", "x": 80 + i * 230, "y": 250, "w": 210, "h": 110, "label": d, "size": 38, "at": f"इंजन|{0.1 + i * 0.15}", "dur": .5} for i, d in enumerate(door)]
items += [{"t": "arrow", "from": [185 + i * 230, 370], "to": [185 + i * 230 + (540 - (185 + i * 230)) * .35, 470], "at": f"एक ही|{0.1 + i * .12}", "dur": .45} for i in range(4)]
items += [{"t": "box", "x": 80, "y": 480, "w": 900, "h": 170, "label": "ek hi ENGINE", "size": 76, "fill": "#FFD60A", "fo": .85, "at": "एक ही|0.2", "dur": .8}]
st = lambda t, d, rot: f'<div style="font-size:30px;font-weight:700;margin-bottom:2px">{d}</div><div class="mono" style="font-size:50px;font-weight:700;line-height:1.1">{t}</div>'
scenes.append(dict(id="engine", type="stage", wipe="up", voice=V4, layers=[
    dict(kind="draw", x=0, y=0, w=1080, h=1920, sw=8, items=items),
    box(st("CLAUDE.md", "project ke rules ki parchi", 0), 400, 740, "width:600px;padding:26px 36px;box-sizing:border-box", cls="sticky", k=[[0, {"r": -2.5}]], **{"in": "CLAUDE.md|-0.1", "spring": True}),
    box(st("settings", "wahi settings sab jagah", 0), 400, 940, "width:600px;padding:26px 36px;box-sizing:border-box", cls="sticky", k=[[0, {"r": 2}]], **{"in": "settings|-0.1", "spring": True}),
    box(st("MCP", "bahar ke tools jodna", 0), 400, 1140, "width:600px;padding:26px 36px;box-sizing:border-box", cls="sticky", k=[[0, {"r": -1.5}]], **{"in": "MCP|-0.1", "spring": True}),
    dict(kind="svgbot", size=640, x=-90, y=760, talk=[[0.5, 12]],
         k=[[0, {"x": -600, "ar": 0}], [0.6, {"x": -90, "e": "b"}], ["CLAUDE.md|-0.2", {"ar": -80}], ["settings|0", {"ar": -86}], ["MCP|0", {"ar": -92}], ["जैसे एक|0", {"ar": 0}]]),
    dict(kind="text", html="Ek **dimaag** - kai darwaze", x=80, y=1400, size=88, w=920, stream=True, step=0.15, sat="जैसे एक|0"),
]))

V5 = "याद रखो: Claude Code एक helper है, खुद काम करता है, पाँच जगह चलता है। तुम कहाँ से शुरू करोगे, terminal, IDE या web? Comment में बताओ।"
scenes.append(dict(id="cta", type="stage", wipe="left", voice=V5, layers=[
    box(row("Khud kaam karta helper"), 80, 260, ROWCSS.format(w=920, h=128), **{"in": "helper है|-0.4", "spring": True, "sh": True}),
    box(row("5 jagah chalta hai"), 80, 410, ROWCSS.format(w=920, h=128), **{"in": "पाँच जगह|-0.1", "spring": True, "sh": True}),
    dict(kind="text", html="Tum kahan se **shuru** karoge?", x=80, y=640, size=100, w=920, stream=True, step=0.16, sat="तुम कहाँ|-0.1"),
    box('<div class="keycap">Terminal</div><div class="keycap">IDE</div><div class="keycap">Web</div>', 80, 1110, "display:flex;gap:22px;font-size:44px", **{"in": "terminal|-0.1", "spring": True}),
    dict(kind="img", img="thumbs", size=520, x=560, y=1250, bob=1, k=[["Comment|-0.3", {"x": 1200, "o": 1}], ["Comment|0.3", {"x": 560}]]),
]))

deck = {"_note": "Short 019 Overview. Source: https://code.claude.com/docs/en/overview.md (read 2026-11-04). New style: marker word-stream, count layer, rail, tick list, sticky notes.",
        "tag": "Claude Code · Overview", "rail": True,
        "music": {"file": "shared/music/presentation/Funkorama.mp3", "start": 6, "rel": 12},
        "voice": {"id": "Charon", "style": "Speak like a friendly Indian tech YouTuber chatting casually in Hinglish. Natural conversational pace, warm and clear, a little energetic but not theatrical. No sing-song, no exaggerated emphasis."},
        "scenes": scenes}
Path(__file__).with_name("deck.json").write_text(json.dumps(deck, ensure_ascii=False, indent=1), encoding="utf-8")
print("deck.json written,", len(scenes), "scenes")
