import json, re, wave, sys
from pathlib import Path
ROOT = Path(r"D:\my-tubes\channels\yellow-bot\stories")
LEAD = 0.30


def dur(story, i, voice):
    p = ROOT / story / "audio" / "tts" / f"s_{i:02d}.wav"
    if p.exists():
        with wave.open(str(p)) as w:
            return w.getnframes() / w.getframerate()
    return 0.082 * len(re.sub(r"\s+", " ", voice).strip())


def T(story, i, voice, ph):
    v = re.sub(r"\s+", " ", voice).strip()
    k = v.find(ph)
    assert k >= 0, (ph, voice)
    return round(max(0.2, LEAD + dur(story, i, voice) * (k / len(v)) * 0.97 - 0.12), 2)


PILL = "font-size:{fs}px;font-weight:800;padding:10px 30px;border:5px solid #111;border-radius:999px;white-space:nowrap;background:{bg}"


def head(text, hl=0.9):
    return {"kind": "text", "html": text, "x": 80, "y": 300, "size": 88, "hlAt": hl, "w": 920,
            "k": [[0.2, {"o": 0, "y": 340}], [0.7, {"o": 1, "y": 300}]]}


def appear(t, x, y, dx=0, dy=0):
    return [[t, {"x": x + dx, "y": y + dy, "o": 0}], [t + 0.45, {"x": x, "y": y, "o": 1, "e": "b"}]]


def recap(story, i, voice, title, cards, cues):
    d = dur(story, i, voice)
    ts = [T(story, i, voice, c) for c in cues]
    layers = [head(title), {
        "kind": "svgbot", "size": 800, "x": -70, "y": 560, "talk": [[0.5, round(LEAD + d - 0.2, 2)]],
        "nod": [[ts[2], round(ts[2] + 1.4, 2)]],
        "k": [[0.0, {"x": -600, "ar": 0}], [0.7, {"x": -70, "e": "b"}], [0.76, {"ar": 0}], [ts[0], {"ar": -86}],
              [ts[1], {"ar": -80}], [ts[2], {"ar": -92}], [round(LEAD + d, 2), {"ar": 0}]]}]
    for n, ((a, b), t) in enumerate(zip(cards, ts)):
        y = 560 + n * 290
        html = (f'<div style="width:78px;height:78px;border-radius:50%;background:#FFD60A;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:44px;flex:none">{n+1}</div>'
                f'<div><div style="font-size:46px;font-weight:800;line-height:1.1">{a}</div><div style="font-size:32px;color:#6b6b66;font-weight:500;margin-top:4px">{b}</div></div>')
        layers.append({"kind": "box", "html": html, "x": 440, "y": y, "css": "width:600px;display:flex;gap:24px;align-items:center",
                       "k": [[t, {"x": 520, "o": 0}], [round(t + 0.45, 2), {"x": 440, "o": 1, "e": "b"}]]})
    return {"id": "recap", "type": "stage", "wipe": "up", "voice": voice, "layers": layers}


def base(tag):
    return {"tag": tag, "music": {"file": "shared/music/presentation/Funkorama.mp3", "start": 6, "rel": 12},
            "voice": {"id": "Charon", "style": "Speak like a friendly Indian tech YouTuber chatting casually in Hinglish. Natural conversational pace, warm and clear, a little energetic but not theatrical. No sing-song, no exaggerated emphasis."}}


def write(story, spec):
    p = ROOT / story
    p.mkdir(parents=True, exist_ok=True)
    (p / "deck.json").write_text(json.dumps(spec, ensure_ascii=False, indent=1), encoding="utf-8")


def worktrees():
    s = "015_worktrees"
    V = {}
    V[0] = "सोचो दो sessions एक ही folder में काम करें, तो files टकराती हैं। Worktree हर session को अपना अलग folder और branch देता है।"
    t = lambda ph: T(s, 0, V[0], ph)
    tc, tw, ta = t("टकराती"), t("Worktree"), t("अपना अलग")
    hook = {"id": "hook", "type": "stage", "wipe": "right", "voice": V[0], "layers": [
        head("Parallel **sessions**"),
        {"kind": "doc", "w": 560, "h": 380, "file": "app.js", "lines": 7, "x": 260, "y": 520,
         "k": [[0.2, {"o": 0, "y": 560, "mess": 0}], [0.8, {"o": 1, "y": 520, "mess": 0}], [tc - 0.5, {"o": 1, "mess": 0}], [tc + 0.3, {"o": 1, "mess": 1}],
               [tw - 0.2, {"o": 1, "mess": 1}], [tw + 0.3, {"o": 0, "mess": 1}]]},
        {"kind": "box", "html": "Session A", "x": 60, "y": 1000, "css": PILL.format(fs=44, bg="#fff"), "k": appear(0.9, 60, 1000, dx=-300)},
        {"kind": "box", "html": "Session B", "x": 700, "y": 1000, "css": PILL.format(fs=44, bg="#FFD60A"), "k": appear(1.5, 700, 1000, dx=300)},
        {"kind": "box", "html": "collision!", "x": 340, "y": 940, "css": PILL.format(fs=48, bg="#FFD60A"),
         "k": [[tc, {"o": 0, "s": 0.6}], [tc + 0.4, {"o": 1, "s": 1, "e": "b"}], [tw - 0.2, {"o": 1}], [tw + 0.3, {"o": 0}]]},
        {"kind": "draw", "x": 0, "y": 560, "w": 1080, "h": 420, "sw": 7, "items": [
            {"t": "arrow", "from": [540, 10], "to": [300, 90], "at": round(tw + 0.2, 2), "dur": 0.5},
            {"t": "arrow", "from": [540, 10], "to": [780, 90], "at": round(tw + 0.2, 2), "dur": 0.5},
            {"t": "box", "x": 60, "y": 110, "w": 460, "h": 170, "label": "worktree A", "size": 48, "fill": "#FFD60A", "fo": 0.55, "at": round(tw + 0.7, 2), "dur": 0.8},
            {"t": "box", "x": 560, "y": 110, "w": 460, "h": 170, "label": "worktree B", "size": 48, "fill": "#FFD60A", "fo": 0.55, "at": round(tw + 1.2, 2), "dur": 0.8},
            {"t": "text", "x": 290, "y": 350, "text": "alag branch", "size": 42, "anchor": "middle", "at": round(ta, 2), "dur": 0.4},
            {"t": "text", "x": 790, "y": 350, "text": "alag branch", "size": 42, "anchor": "middle", "at": round(ta + 0.3, 2), "dur": 0.4}]},
        {"kind": "text", "html": "Har session ka **apna folder**", "x": 80, "y": 1240, "size": 62, "w": 560, "hlAt": round(ta + 0.3, 2),
         "k": [[ta, {"o": 0, "y": 1280}], [ta + 0.5, {"o": 1, "y": 1240}]]},
        {"kind": "img", "img": "work", "size": 380, "x": 650, "y": 1300, "bob": 1, "k": [[0.1, {"x": 1200, "o": 1}], [0.9, {"x": 650}]]}]}
    V[1] = "Docs में देखो: --worktree flag के साथ नाम दो, तो .claude/worktrees/ में नया worktree बनता है, और नई branch भी।"
    docs = {"id": "docs", "type": "docs", "wipe": "up", "img": "worktrees.png", "url": "code.claude.com/docs/en/worktrees", "voice": V[1],
            "scroll": [950, 1050], "ch": 1180, "callout": "**--worktree** = alag folder + **nayi branch**", "cosize": 62,
            "cues": ["--worktree flag"],
            "hls": [{"x": 30, "y": 1342, "w": 1440, "h": 82}, {"x": 30, "y": 1236, "w": 1440, "h": 86}],
            "hlcues": ["--worktree flag", ".claude/worktrees/"]}
    V[2] = "दो terminal खोलो। पहले में claude --worktree feature-auth चलाओ, दूसरे में claude --worktree bugfix। अब दोनों sessions अलग-अलग worktree में हैं।"
    code = {"id": "example", "type": "code", "wipe": "left", "file": "terminal · EXAMPLE", "size": 38, "y0": 330, "voice": V[2],
            "lines": ["# terminal 1", "claude --worktree feature-auth", "# terminal 2", "claude --worktree bugfix"],
            "caption": "**2 terminals** = 2 worktrees", "cosize": 66,
            "cues": ["दो terminal", "पहले में", "दूसरे में", "claude --worktree bugfix", "अलग-अलग worktree"]}
    V[3] = "Session से exit करो, तो Claude worktree check करता है। Clean और unnamed हो, तो वो अपने-आप हट जाता है। काम बचा हो, तो Claude पूछता है, keep या remove। Remove किया तो folder और branch दोनों जाते हैं।"
    flow = {"id": "cleanup", "type": "flow", "wipe": "right", "tsize": 50, "nh": 200, "gap": 90, "voice": V[3],
            "nodes": [{"t": "Exit karte ho", "s": "Claude worktree check karta hai"},
                      {"t": "Clean + unnamed", "s": "apne-aap remove"},
                      {"t": "Kaam bacha hai", "s": "keep ya remove poochta hai"}],
            "foot": "Remove = folder **aur branch** dono delete",
            "cues": ["exit करो", "Clean और unnamed", "काम बचा", "Remove किया"]}
    V[4] = "एक बारीकी: worktree fresh checkout होता है, इसलिए .env जैसी gitignored files साथ नहीं आतीं। .worktreeinclude में पैटर्न लिखो, और जो files gitignored भी हैं और match भी करती हैं, वो copy हो जाती हैं।"
    cmp_ = {"id": "nuance", "type": "compare", "wipe": "up", "voice": V[4], "footcue": 6,
            "left": {"title": "Default", "rows": [".env nahi aati", "fresh checkout hai"]},
            "right": {"title": "Include file", "rows": [".worktreeinclude me likho", "gitignored + match = copy"]},
            "foot": "Sirf **gitignored** files copy hoti hain",
            "cues": ["एक बारीकी", ".worktreeinclude में", "fresh checkout", "साथ नहीं आतीं", "पैटर्न लिखो", "match भी करती", "copy हो जाती"]}
    V[5] = "तो याद रखो: --worktree से हर session को अलग folder और branch मिलता है। Exit पर clean worktree अपने-आप हटता है। और .env जैसी files के लिए .worktreeinclude लिखो।"
    rec = recap(s, 5, V[5], "Yaad **rakho**", [("--worktree", "har session ka alag folder"), ("Clean exit", "worktree apne-aap hat jaata"), (".worktreeinclude", "gitignored files copy")],
                ["--worktree से", "Exit पर", ".worktreeinclude लिखो"])
    V[6] = "आप worktree में सबसे पहले कौन सा काम चलाओगे? Comment में बताओ।"
    cta = {"id": "cta", "type": "cta", "wipe": "left", "size": 92, "voice": V[6], "lines": ["Pehle kaunsa kaam", "**worktree** me?"], "sub": "Comment me batao",
           "cues": ["आप worktree", "कौन सा काम", "Comment में"],
           "robot": {"img": "thumbs", "x": 570, "y": 1250, "size": 460, "cue": "Comment में"}}
    spec = base("Claude Code · Worktrees")
    spec["_note"] = "Short 015: worktrees. Source: https://code.claude.com/docs/en/worktrees (read 2026-11-03). Format v3."
    spec["scenes"] = [hook, docs, code, flow, cmp_, rec, cta]
    write(s, spec)


def plugins():
    s = "016_plugins-overview"
    V = {}
    V[0] = "Skills, agents, hooks और MCP servers, सब अलग-अलग फैले हैं? Plugin इन सबको एक unit में pack कर देता है।"
    tpk = T(s, 0, V[0], "Plugin इन")
    chips = [("Skill", -330, 640, 230, 900), ("Agent", 1120, 600, 560, 900), ("Hooks", -330, 1380, 230, 1070), ("MCP", 1120, 1350, 560, 1070)]
    layers = [head("Plugin = **ek unit**")]
    layers.append({"kind": "box", "html": '<div class="mono" style="font-size:40px;font-weight:700;margin:24px 0 0 36px">my-plugin/</div>', "x": 190, "y": 800,
                   "css": "width:700px;height:520px;border:6px solid #111;border-radius:36px;background:#fff;box-shadow:0 14px 34px rgba(0,0,0,.14)",
                   "k": [[0.3, {"o": 0, "y": 840, "s": 1}], [0.9, {"o": 1, "y": 800, "s": 1}], [tpk + 1.6, {"o": 1, "s": 1}], [tpk + 1.9, {"o": 1, "s": 1.05}], [tpk + 2.3, {"o": 1, "s": 1}]]})
    for i, (nm, sx, sy, ex, ey) in enumerate(chips):
        a = 0.9 + i * 0.5
        px = min(max(sx, 40), 700)
        layers.append({"kind": "box", "html": nm, "x": sx, "y": sy, "css": PILL.format(fs=46, bg="#FFD60A" if i % 2 == 0 else "#fff"),
                       "k": [[a, {"x": sx, "y": sy, "o": 0}], [a + 0.4, {"x": px, "y": sy, "o": 1, "e": "b"}],
                             [tpk + i * 0.25, {"x": px, "y": sy, "o": 1}], [tpk + i * 0.25 + 0.6, {"x": ex, "y": ey, "o": 1, "e": "b"}]]})
    layers.append({"kind": "box", "html": "ek install, ek unit", "x": 300, "y": 1230, "css": PILL.format(fs=40, bg="#FFD60A"),
                   "k": [[tpk + 1.9, {"o": 0, "s": 0.6}], [tpk + 2.4, {"o": 1, "s": 1, "e": "b"}]]})
    layers.append({"kind": "img", "img": "thumbs", "size": 330, "x": 650, "y": 1400, "bob": 1, "k": [[0.1, {"x": 1200, "o": 1}], [tpk + 1.0, {"x": 1200}], [tpk + 1.8, {"x": 700}]]})
    hook = {"id": "hook", "type": "stage", "wipe": "right", "voice": V[0], "layers": layers}
    V[1] = "Plugin के अंदर skills होते हैं, agents होते हैं, hooks होते हैं, और MCP servers भी। इन सबको Claude Code एक साथ load करता है।"
    hub = {"id": "parts", "type": "hub", "wipe": "up", "voice": V[1], "center": "Plugin", "nodes": ["Skills", "Agents", "Hooks", "MCP servers"],
           
           "cues": ["Plugin के अंदर", "skills होते", "agents होते", "hooks होते", "MCP servers भी", "load करता", "load करता", "load करता"]}
    V[2] = "Docs में देखो: plugin एक directory है। Manifest उसका नाम देती है, और components में skills, agents, hooks और MCP servers आते हैं।"
    docs = {"id": "docs", "type": "docs", "wipe": "left", "img": "plugins-overview.png", "url": "code.claude.com/docs/en/plugins/overview", "voice": V[2],
            "scroll": [1200, 1300], "ch": 1180, "callout": "**Plugin** = directory of **components**", "cosize": 62, "cues": ["Docs में देखो"],
            "hls": [{"x": 30, "y": 1322, "w": 1440, "h": 126}, {"x": 30, "y": 1466, "w": 1440, "h": 312}],
            "hlcues": ["plugin एक directory", "skills, agents, hooks"]}
    V[3] = "Try करने के लिए terminal में /plugin चलाओ। Discover tab में marketplaces के plugins दिखते हैं। Marketplaces tab में official plugins का Context cost दिखता है। और Installed tab में Not used recently वाले plugins मिल जाते हैं।"
    code = {"id": "example", "type": "code", "wipe": "right", "file": "terminal · /plugin", "size": 36, "y0": 330, "voice": V[3],
            "lines": ["> /plugin", "Discover       -> plugins list", "Marketplaces   -> Context cost", "Installed      -> Not used recently"],
            "caption": "**/plugin** = browse + check", "cosize": 66,
            "cues": ["/plugin चलाओ", "Discover tab", "Marketplaces tab", "Installed tab", "Not used recently"]}
    V[4] = "एक बात ध्यान रखो: enabled plugin हर session का हिस्सा है। जो skills और agents Claude खुद invoke कर सकता है, उनके name और description हर turn context में रहते हैं। MCP servers और hooks भी चलते हैं। और plugin जो चलाता है, वो आपकी तरह चलता है।"
    chp = {"id": "nuance", "type": "chips", "wipe": "up", "y0": 330, "parent": "Dhyan rakho", "title": "Har session me", "voice": V[4],
           "chips": ["Naam+detail context me", "MCP + hooks chalte hain", "Jo chale, tum jaise"],
           "cues": ["एक बात", "हर session का हिस्सा", "name और description", "MCP servers और hooks", "वो आपकी तरह"]}
    V[5] = "तो याद रखो: plugin कई components को एक unit में pack करता है। /plugin से Discover tab में install करो। और enabled plugin का context cost देखना मत भूलना।"
    rec = recap(s, 5, V[5], "Yaad **rakho**", [("Plugin = ek unit", "skills, agents, hooks, MCP"), ("/plugin", "Discover se install karo"), ("Context cost", "install se pehle dekho")],
                ["plugin कई", "/plugin से", "context cost देखना"])
    V[6] = "आप कौन सा plugin सबसे पहले try करोगे? Comment में बताओ।"
    cta = {"id": "cta", "type": "cta", "wipe": "left", "size": 92, "voice": V[6], "lines": ["Pehle kaunsa", "**plugin** try karoge?"], "sub": "Comment me batao",
           "cues": ["आप कौन सा", "plugin सबसे", "Comment में"],
           "robot": {"img": "thumbs", "x": 570, "y": 1250, "size": 460, "cue": "Comment में"}}
    spec = base("Claude Code · Plugins")
    spec["_note"] = "Short 016: plugins overview. Source: https://code.claude.com/docs/en/plugins/overview (read 2026-11-03). Format v3."
    spec["scenes"] = [hook, hub, docs, code, chp, rec, cta]
    write(s, spec)


if __name__ == "__main__":
    which = sys.argv[1:] or ["15", "16"]
    if "15" in which:
        worktrees()
    if "16" in which:
        plugins()
    print("ok")
