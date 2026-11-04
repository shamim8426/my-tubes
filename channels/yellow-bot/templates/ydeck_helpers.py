"""Shared helpers for Yellow Bot gen_deck.py files (Day 1 'clean product-page' style, 2026-11-04). Import:
    sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "templates")); from ydeck_helpers import *"""
import json
import re
from pathlib import Path

BG = "#F3F5F9"   # calm light background (deck field "bg"), faint dot grid (deck field "bgGrid")
CTA_VOICE = "AI के ऐसे काम के features चाहिए? Yellow Bot को follow करो।"   # line A (STYLE_GUIDE ending rule)
CTA_SCREEN = "**Yellow Bot** ko follow karo"
CTA_PILL = "Follow"
SHIFT = 120
SHADOW = "box-shadow:0 26px 60px rgba(25,35,60,.13),0 3px 8px rgba(25,35,60,.08)"


def pop(cue, off=-0.1, **kw):
    return dict({"in": f"{cue}|{off}", "spring": True}, **kw)


def ic(name, x, y, size=130, cue=None, off=-0.1, **kw):
    d = dict(kind="icon", name=name, x=x, y=y, size=size)
    if cue is not None:
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


def window(title, w, h, dark=False):
    """App/terminal window mock-up with a soft shadow (use as box html; css = '')."""
    bg, fg, bar, bd = ("#14171C", "#fff", "#262B33", "#14171C") if dark else ("#fff", "#111", "#EDF0F5", "#E3E7EE")
    dots = '<i style="background:#FFD60A"></i><i style="background:#9AA3B2"></i><i style="background:#9AA3B2"></i>'
    return (f'<div style="width:{w}px;height:{h}px;border:2px solid {bd};border-radius:34px;background:{bg};color:{fg};overflow:hidden;position:relative;{SHADOW}">'
            f'<div style="height:78px;background:{bar};display:flex;align-items:center;gap:22px;padding-left:28px"><div class="dot3">{dots}</div>'
            f'<div class="mono" style="font-size:30px;color:{"#FFD60A" if dark else "#566"}">{title}</div></div></div>')


def card(inner, w, pad="34px 40px", bg="#fff"):
    return f'<div style="width:{w}px;padding:{pad};background:{bg};border:2px solid #E3E7EE;border-radius:34px;{SHADOW};box-sizing:border-box">{inner}</div>'


def line(code, size=40, color="#fff"):
    return f'<div class="mono" style="font-size:{size}px;color:{color};white-space:nowrap">{code}</div>'


def cta_scene(wipe="fade"):
    L = [tx(CTA_SCREEN, 80, 260, 120, 920, 0.15),
         box(f'<div style="font-size:120px;font-weight:800;line-height:1">{CTA_PILL}</div>', 190, 800, f"background:#FFD60A;border:0;border-radius:999px;padding:30px 110px;{SHADOW}", wig=4.35, float=5, **pop(0.5)),
         dict(kind="icon", name="cursor", x=0, y=0, size=140, k=[[3.4, {"x": 820, "y": 1060, "o": 0}], [3.5, {"x": 820, "y": 1060, "o": 1}], [4.2, {"x": 520, "y": 880}]], wig=4.3),
         ic("bell", 430, 1080, 200, cue=None, wig=4.7, float=6, **{"in": 4.5, "spring": True}),
         dict(kind="img", img="thumbs", size=520, x=260, y=1300, bob=1, k=[[0.2, {"x": -700, "o": 1}], [0.9, {"x": 260}]])]
    return dict(id="follow", type="stage", wipe=wipe, voice=CTA_VOICE, layers=L)


def finish(here, note, tag, scenes, music_start=6):
    """Attach measured word times (wt.json from scripts/yb_wordtimes.py) and write deck.json."""
    wtp = here / "wt.json"
    wt = json.loads(wtp.read_text(encoding="utf-8")) if wtp.exists() else {}
    for sc in scenes:
        if sc["id"] in wt:
            sc["wt"] = wt[sc["id"]]
        if sc["id"] != "follow":  # push content down a little so the lower half is not empty (Day 1 layout, 2026-11-04)
            for L in sc["layers"]:
                if L.get("kind") == "img" or not isinstance(L.get("y", L.get("from_", 0)), (int, float)) and "pts" not in L and "from_" not in L:
                    continue
                if L.get("kind") == "flow":
                    for key in ("pts",):
                        if key in L:
                            L[key] = [[p[0], p[1] + SHIFT] for p in L[key]]
                    for key in ("from_", "from", "to"):
                        if key in L and isinstance(L[key], list):
                            L[key] = [L[key][0], L[key][1] + SHIFT]
                elif isinstance(L.get("y"), (int, float)) and L["y"] >= 420:
                    L["y"] += SHIFT
        for L in sc["layers"]:
            if "from_" in L:
                L["from"] = L.pop("from_")
    deck = {"_note": note, "tag": tag, "bg": BG, "bgGrid": True,
            "music": {"file": "shared/music/presentation/Funkorama.mp3", "start": music_start, "rel": 12},
            "voice": {"id": "Charon", "style": "Speak like a friendly Indian tech YouTuber chatting casually in Hinglish. Natural conversational pace, warm and clear, a little energetic but not theatrical. No sing-song, no exaggerated emphasis."},
            "scenes": scenes}
    (here / "deck.json").write_text(json.dumps(deck, ensure_ascii=False, indent=1), encoding="utf-8")
    print("deck.json written,", len(scenes), "scenes, voice chars", [len(re.sub(r"\s+", " ", s["voice"])) for s in scenes], "wt" if wt else "(no wt.json yet)")
