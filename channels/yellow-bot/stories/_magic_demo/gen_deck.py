"""Generates deck.json + silent placeholder wavs for the Yellow Bot MAGIC effects reel (no voice, Rs 0).
Run: .venv\\Scripts\\python -X utf8 channels\\yellow-bot\\stories\\_magic_demo\\gen_deck.py"""
import json
import wave
from pathlib import Path

HERE = Path(__file__).parent
BEAT = 1.1


def pop(t, **kw):
    return dict({"in": t, "spring": True}, **kw)


def ic(name, x, y, size, t=None, **kw):
    d = dict(kind="icon", name=name, x=x, y=y, size=size)
    if t is not None:
        d.update(pop(t))
    d.update(kw)
    return d


def box(html, x, y, css, **kw):
    return dict(kind="box", html=html, x=x, y=y, css=css, **kw)


def cap(txt, t0, t1, sub=""):
    h = f'<div style="display:flex;align-items:center;gap:22px"><span>{txt}</span><span style="font-size:30px;font-weight:700;color:#FFD60A">{sub}</span></div>'
    return box(h, 80, 1660, "background:#111;color:#fff;font-size:58px;font-weight:800;padding:16px 44px;border-radius:999px;white-space:nowrap;box-shadow:0 14px 30px rgba(0,0,0,.2)", **{"in": t0, "out": t1, "spring": True})


scenes = []

# ---- S1: dust, wand, assemble (3 beats)
L = [
    # beat 1 dust
    ic("sparkle", 390, 620, 300, 0.3, float=8, out=1.35),
    dict(kind="dust", from_=[540, 770], at=0.38, n=80, speed=700, life=1.1, size=18, mode="burst"),
    dict(kind="dust", from_=[540, 1080], at=0.55, dur=0.6, n=40, speed=620, life=1.0, size=14, mode="fountain", spread=1.3, grav=900),
    cap("dust", 0.2, 1.35, "burst + fountain"),
    # beat 2 wand
    dict(kind="text", html="**Magic**", x=80, y=520, size=230, w=920, in_=1.45, out=2.45),
    dict(kind="wand", shape="underline", pts=[[150, 880], [930, 880]], at=1.55, dur=0.85, sw=26, fadeAt=2.4),
    dict(kind="wand", shape="circle", cx=540, cy=700, rx=470, ry=210, at=1.9, dur=0.5, sw=12, fadeAt=2.4, ss=16),
    cap("wand", 1.3, 2.45, "comet trail draws the line"),
    # beat 3 assemble
    dict(kind="assemble", text="MAGIC", cx=540, cy=760, size=250, at=2.5, dur=0.9, gap=8),
    dict(kind="assemble", text="Yellow Bot", cx=540, cy=1030, size=120, at=2.7, dur=0.8, gap=6, dot=3),
    cap("assemble", 2.4, 3.6, "particles converge to text"),
]
scenes.append(dict(id="s1", type="stage", wipe="right", voice=".", dur=3 * BEAT - 0.3, layers=L))

# ---- S2: portal in + shock + glint, aura, poof
L = [
    box("", 90, 560, "width:900px;height:360px;border-radius:50px;background:#FFD60A;border:8px solid #111;box-shadow:0 24px 50px rgba(0,0,0,.2)", out=1.4, **pop(0.6)),
    dict(kind="glinttext", html="TA-DA!", x=90, y=640, w=900, size=190, glint=[0.95, 0.7], out=1.4),
    dict(kind="shock", from_=[540, 740], at=0.7, dur=0.9, r=900, rings=2),
    ic("check", 400, 1010, 280, 1.0, wig=1.25, drawon=[1.0, 0.5], out=1.4),
    cap("portal + shock + glint", 0.35, 1.5, "ta-da"),
    # beat 5 aura
    dict(kind="aura", from_=[540, 930], at=1.5, dur=1.2, r=330),
    dict(kind="svgbot", size=760, x=160, y=520, talk=[[1.5, 2.6]], out=2.5, k=[[0, {"x": 160, "ar": -150, "al": 0}], [1.5, {"al": 150}]], **pop(1.45)),
    cap("aura", 1.45, 2.55, "glow + light rays while casting"),
    # beat 6 poof
    dict(kind="poof", from_=[540, 900], at=2.6, dur=0.7, size=260),
    ic("rocket", 390, 740, 300, 2.8, float=6, out=3.4),
    dict(kind="poof", from_=[540, 900], at=3.4, dur=0.7, size=260),
    cap("poof", 2.55, 3.6, "smoke puff in / out"),
]
scenes.append(dict(id="s2", type="stage", wipe="portal", trd=0.7, voice=".", dur=3 * BEAT - 0.3, layers=L))

# ---- S3: morph, tilt+parallax, magnet
card_front = '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:84px;font-weight:700;color:#FFD60A" class="mono">&gt; claude</div>'
card_back = '<div style="width:100%;height:100%;display:flex;align-items:center;justify-content:center;font-size:96px;font-weight:800;color:#111">Done!</div>'
L = [
    # beat 7 morph
    dict(kind="morph", icons=["terminal", "chat", "check"], size=420, x=330, y=620, ts=[0.5, 0.9], md=0.4, out=1.3, **pop(0.25)),
    cap("morph", 0.2, 1.3, "terminal > chat > check"),
    # beat 8 tilt + parallax (depth layers z)
    dict(kind="box", html="", x=60, y=480, css="width:520px;height:520px;border-radius:260px;background:#FFD60A;opacity:.35", z=-1.2, **{"in": 1.3, "out": 2.45}),
    ic("bolt", 780, 560, 170, 1.4, z=2.2, out=2.45, float=6),
    ic("gear", 120, 1040, 150, 1.5, z=1.8, out=2.45, spin=60, spinAt=1.5),
    dict(kind="card3d", w=720, h=420, x=180, y=620, front=card_front, back=card_back,
         fcss="border-radius:44px;background:#111;border:8px solid #111;box-shadow:0 30px 60px rgba(0,0,0,.28)",
         bcss="border-radius:44px;background:#FFD60A;border:8px solid #111;box-shadow:0 30px 60px rgba(0,0,0,.28)",
         tilt=6, z=0.4, k=[[0, {"ry": 0}], [1.45, {"ry": 0}], [2.05, {"ry": 180}]], out=2.45, **pop(1.3)),
    cap("tilt + parallax", 1.3, 2.45, "3D flip, 3 depth layers"),
    # beat 9 magnet
    dict(kind="img", img="think", size=420, x=330, y=900, bob=1, k=[[2.4, {"o": 0}], [2.55, {"o": 1}]]),
    dict(kind="magnet", to=[540, 1100], at=2.5, dur=0.8, stag=0.16, size=120, arc=280,
         items=[{"name": "file", "from": [110, 380]}, {"name": "folder", "from": [980, 420]}, {"name": "code", "from": [90, 1420]}, {"name": "terminal", "from": [990, 1400]}]),
    cap("magnet", 2.4, 3.6, "items fly in arcs with trails"),
]
scenes.append(dict(id="s3", type="stage", wipe="up", voice=".", dur=3 * BEAT - 0.3, layers=L))

# normalise field names that clash with python keywords
for sc in scenes:
    for L in sc["layers"]:
        if "from_" in L:
            L["from"] = L.pop("from_")
        if "in_" in L:
            L["in"] = L.pop("in_")
            L["spring"] = True

deck = {"_note": "Yellow Bot MAGIC effects reel (no voice, Rs 0). Effects are pure functions of time (seeded PRNG).",
        "tag": "Magic · effects reel", "voice": {"id": "Charon", "style": "-"}, "scenes": []}
for i, sc in enumerate(scenes):
    d = sc.pop("dur")
    (HERE / "audio" / "tts").mkdir(parents=True, exist_ok=True)
    with wave.open(str(HERE / "audio" / "tts" / f"s_{i:02d}.wav"), "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(24000)
        w.writeframes(b"\x00\x00" * int(24000 * d))
    deck["scenes"].append(sc)
(HERE / "deck.json").write_text(json.dumps(deck, ensure_ascii=False, indent=1), encoding="utf-8")
print("deck.json written,", len(scenes), "scenes")
