import json, re, wave, sys
from pathlib import Path
S = Path(r"D:\my-tubes\channels\devrobolab\stories")
MUSIC = {"file": "shared/music/presentation/Funkorama.mp3", "start": 6, "rel": 12}
VOICE = {"id": "Charon", "style": "Speak like a friendly Indian tech YouTuber chatting casually in Hinglish. Natural conversational pace, warm and clear, a little energetic but not theatrical. No sing-song, no exaggerated emphasis."}
CARD = "border:6px solid #111;border-radius:32px;background:#fff;box-sizing:border-box;box-shadow:0 14px 34px rgba(0,0,0,.14)"


def dur(story, i, voice):
    f = S / story / "audio" / "tts" / f"s_{i:02d}.wav"
    if f.exists():
        with wave.open(str(f)) as w:
            return w.getnframes() / w.getframerate()
    return 0.082 * len(re.sub(r"\s+", " ", voice).strip())


def mkT(story, i, voice):
    text = re.sub(r"\s+", " ", voice).strip()
    d = dur(story, i, voice)

    def T(ph):
        j = text.find(ph)
        if j < 0:
            raise SystemExit(f"cue not found {story}/{i}: {ph!r}")
        return round(max(0.2, 0.30 + d * (j / len(text)) * 0.97 - 0.12), 2)
    return T


def title(html, size=88):
    return {"kind": "text", "html": html, "x": 80, "y": 300, "size": size, "hlAt": 0.9, "w": 920,
            "k": [[0.2, {"o": 0, "y": 340}], [0.7, {"o": 1, "y": 300}]]}


def pop(html, x, y, css, t):
    st = {"o": 0, "s": 0.6}
    return {"kind": "box", "html": html, "x": x, "y": y, "css": css,
            "k": [[t, st], [round(t + 0.4, 2), {"o": 1, "s": 1, "e": "b"}]]}


def slide(html, x, y, css, t):
    return {"kind": "box", "html": html, "x": x, "y": y, "css": css,
            "k": [[t, {"x": x - 400, "o": 0}], [round(t + 0.45, 2), {"x": x, "o": 1, "e": "b"}]]}


PILL = "font-size:36px;font-weight:800;padding:8px 26px;border:5px solid #111;border-radius:999px;white-space:nowrap;background:{bg}"


def numrow(n, big, small, x, y, t):
    return {"kind": "box", "x": x, "y": y, "css": "width:600px;display:flex;gap:24px;align-items:center",
            "html": f'<div style="width:78px;height:78px;border-radius:50%;background:#FFD60A;display:flex;align-items:center;justify-content:center;font-weight:800;font-size:44px;flex:none">{n}</div><div><div style="font-size:42px;font-weight:800;line-height:1.1">{big}</div><div style="font-size:30px;color:#6b6b66;font-weight:500;margin-top:4px">{small}</div></div>',
            "k": [[t, {"x": x + 80, "o": 0}], [round(t + 0.45, 2), {"x": x, "o": 1, "e": "b"}]]}


def recap(T, head, items, cues, endph):
    t0, t1, t2 = [T(c) for c in cues]
    tend = T(endph)
    ks = [[0.0, {"x": -600, "ar": 0}], [0.7, {"x": -70, "e": "b"}], [0.76, {"ar": 0}], [t0, {"ar": -86}],
          [t1, {"ar": -80}], [t2, {"ar": -92}], [round(tend + 1.5, 2), {"ar": 0}]]
    L = [title(head), {"kind": "svgbot", "size": 800, "x": -70, "y": 560, "talk": [[0.5, round(tend + 1.2, 2)]],
                       "nod": [[t2, round(t2 + 1.4, 2)]], "k": ks}]
    for n, ((b, s), t, y) in enumerate(zip(items, (t0, t1, t2), (560, 850, 1140)), 1):
        L.append(numrow(n, b, s, 440, y, t))
    return L


def build_013():
    st = "013_context-window"
    sc = []
    v = "देखो, Claude Code की context window में सब कुछ आता है: तुम्हारी instructions, वो files जो वो पढ़ता है, और उसके अपने जवाब। Session चलता है तो ये भरती जाती है।"
    T = mkT(st, 0, v)
    a, b, c, d = T("instructions"), T("files"), T("जवाब"), T("भरती")
    L = [title("Claude ki **memory**"),
         {"kind": "meter", "x": 90, "y": 520, "w": 900, "h": 70, "f": 0,
          "k": [[0.0, {"o": 0, "f": 0}], [0.4, {"o": 1, "f": 0.02}], [a, {"f": 0.05}], [round(a + 0.8, 2), {"f": 0.3}], [b, {"f": 0.3}],
                [round(b + 0.8, 2), {"f": 0.6}], [c, {"f": 0.6}], [round(c + 0.8, 2), {"f": 0.85}], [d, {"f": 0.85}], [round(d + 1.2, 2), {"f": 0.97}]]},
         {"kind": "text", "html": "context **window**", "x": 90, "y": 620, "size": 54, "w": 900, "hlAt": 0.9, "k": [[0.4, {"o": 0, "y": 650}], [0.9, {"o": 1, "y": 620}]]},
         pop("instructions", 90, 790, PILL.format(bg="#FFD60A"), a),
         pop("files jo wo padhta hai", 90, 900, PILL.format(bg="#FFD60A"), b),
         pop("uske apne jawab", 90, 1010, PILL.format(bg="#FFD60A"), c),
         {"kind": "text", "html": "Session ke saath **bharti** jaati hai", "x": 80, "y": 1190, "size": 64, "w": 560, "hlAt": round(d + 0.2, 2),
          "k": [[d, {"o": 0, "y": 1230}], [round(d + 0.5, 2), {"o": 1, "y": 1190}]]},
         {"kind": "img", "img": "work", "size": 380, "x": 650, "y": 1250, "bob": 1, "k": [[0.1, {"x": 1200, "o": 1}], [0.9, {"x": 650}]]}]
    sc.append({"id": "hook", "type": "stage", "wipe": "right", "voice": v, "layers": L})

    v = "अब docs की table देखो: compaction के बाद project-root CLAUDE.md और auto memory, दोनों disk से दोबारा inject होती हैं।"
    sc.append({"id": "docs", "type": "docs", "wipe": "up", "img": "../stories/013_context-window/docs.png", "url": "code.claude.com/docs/en/context-window",
               "voice": v, "scroll": [0, 60], "ch": 1180, "callout": "**CLAUDE.md** + **Auto memory**: disk se wapas", "cosize": 62,
               "cues": ["compaction के बाद"],
               "hls": [{"x": 30, "y": 545, "w": 1440, "h": 52}, {"x": 30, "y": 600, "w": 1440, "h": 52}],
               "hlcues": ["project-root", "auto memory"]})

    v = "/compact एक structured summary बनाता है। System prompt और output style still apply रहते हैं, और CLAUDE.md व auto memory disk से आती हैं।"
    T = mkT(st, 2, v)
    r1, r2, sm = T("System prompt"), T("CLAUDE.md व auto"), T("structured summary")
    rowcss = "width:920px;height:190px;display:flex;align-items:center;gap:36px;padding:0 40px;" + CARD

    def row(big, small, y, t):
        return slide(f'<div style="width:100px;height:100px;border-radius:50%;background:#FFD60A;border:5px solid #111;flex:none"></div><div><div style="font-size:46px;font-weight:800;line-height:1.1">{big}</div><div style="font-size:32px;color:#6b6b66;font-weight:500;margin-top:6px">{small}</div></div>', 80, y, rowcss, t)
    ys = (460, 690, 920)
    items = []
    for (tt, y) in zip((r1, r2), ys):
        cy = y + 95
        items += [{"t": "line", "from": [150, cy + 4], "to": [172, cy + 28], "at": round(tt + 0.5, 2), "dur": 0.2},
                  {"t": "line", "from": [172, cy + 28], "to": [214, cy - 26], "at": round(tt + 0.7, 2), "dur": 0.25}]
    L = [title("Compact ke **baad**"),
         row("System prompt + output style", "dono still apply", ys[0], r1),
         row("CLAUDE.md + auto memory", "disk se wapas", ys[1], r2),
         {"kind": "draw", "x": 0, "y": 0, "w": 1080, "h": 1100, "sw": 12, "items": items},
         {"kind": "meter", "x": 90, "y": 1000, "w": 900, "h": 70, "f": 0.95,
          "k": [[0.0, {"o": 0, "f": 0.95}], [0.4, {"o": 1}], [sm, {"f": 0.95}], [round(sm + 1.0, 2), {"f": 0.25}]]},
         {"kind": "text", "html": "/compact = **summary**", "x": 90, "y": 1100, "size": 60, "w": 900, "hlAt": round(sm + 0.4, 2), "k": [[sm, {"o": 0, "y": 1130}], [round(sm + 0.5, 2), {"o": 1, "y": 1100}]]}]
    sc.append({"id": "survives", "type": "stage", "wipe": "left", "voice": v, "layers": L})

    v = "देखो, /compact के साथ focus लिखो, जैसे auth bug fix, तो summary में वही रहता है जो तुम चुनो। /context से live breakdown दिखता है।"
    sc.append({"id": "example", "type": "code", "wipe": "right", "file": "terminal \u00b7 DOCS EXAMPLES", "size": 38, "y0": 330, "voice": v,
               "lines": ["> /compact focus on the auth bug fix", "# summary me wahi, jo tum chuno", "> /context", "# live breakdown by category"],
               "caption": "Summary me wahi, jo **tum** chuno", "cosize": 62,
               "cues": ["/compact के साथ", "तो summary में", "/context से", "live breakdown", "दिखता है"]})

    v = "लेकिन एक बारीकी: path-scoped rules compaction में summarize हो जाते हैं। अगर rule हमेशा चाहिए, तो paths: frontmatter हटाओ, या उसे project-root CLAUDE.md में रखो।"
    sc.append({"id": "nuance", "type": "compare", "wipe": "up", "voice": v,
               "left": {"title": "Summarize", "rows": ["paths: wala rule"]}, "right": {"title": "Disk se wapas", "rows": ["project-root CLAUDE.md"]},
               "foot": "Rule **zaroori** hai? Root me rakho", "footcue": 4,
               "cues": ["बारीकी", "अगर rule", "path-scoped", "project-root", "में रखो"]})

    v = "तो याद रखो: /context से देखो क्या भरा है, /compact में focus लिखो, और जो rule ज़रूरी हो उसे project-root CLAUDE.md में रखो।"
    T = mkT(st, 5, v)
    sc.append({"id": "recap", "type": "stage", "wipe": "right", "voice": v,
               "layers": recap(T, "Yaad **rakho**", [("/context", "dekho kya bhara hai"), ("/compact focus", "summary me tumhara focus"), ("Zaroori rule", "project-root CLAUDE.md me")],
                               ["/context से", "/compact में", "जो rule"], "में रखो")})

    v = "आप अपने session में /compact कब चलाते हो? Comment में बताओ।"
    sc.append({"id": "cta", "type": "cta", "wipe": "left", "size": 92, "voice": v, "lines": ["Aap **/compact**", "kab chalate ho?"], "sub": "Comment me batao",
               "cues": ["आप अपने", "/compact कब", "Comment में"], "robot": {"img": "thumbs", "x": 570, "y": 1250, "size": 460, "cue": "Comment में"}})
    return {"_note": "Short 013: Context window. Source: https://code.claude.com/docs/en/context-window (read 2026-11-03). Format v3.",
            "tag": "Claude Code \u00b7 Context window", "music": MUSIC, "voice": VOICE, "scenes": sc}


def build_014():
    st = "014_sessions"
    sc = []
    v = "Claude Code की हर conversation एक session होती है, जो local save होती है। Exit करो या /clear चलाओ, फिर भी वापस आ सकते हो।"
    T = mkT(st, 0, v)
    a, b, c, d = T("session होती"), T("local save"), T("Exit करो"), T("वापस")
    L = [title("Claude ke **sessions**"),
         pop('<span class="mono">session: auth-refactor</span>', 90, 520, "font-size:46px;font-weight:700;padding:30px 40px;" + CARD, a),
         pop("local file me save", 90, 690, PILL.format(bg="#FFD60A"), b),
         pop("exit", 90, 840, PILL.format(bg="#fff"), c),
         pop('<span class="mono">/clear</span>', 330, 840, PILL.format(bg="#fff"), round(c + 0.5, 2)),
         pop('<span class="mono">claude --resume auth-refactor</span>', 90, 1000, "font-size:36px;font-weight:700;padding:22px 34px;background:#FFD60A;border:5px solid #111;border-radius:30px;white-space:nowrap", d),
         {"kind": "text", "html": "Wahin se **shuru**", "x": 80, "y": 1190, "size": 70, "w": 560, "hlAt": round(d + 0.5, 2), "k": [[round(d + 0.4, 2), {"o": 0, "y": 1230}], [round(d + 0.9, 2), {"o": 1, "y": 1190}]]},
         {"kind": "img", "img": "wave", "size": 380, "x": 650, "y": 1250, "bob": 1, "k": [[0.1, {"x": 1200, "o": 1}], [0.9, {"x": 650}]]}]
    sc.append({"id": "hook", "type": "stage", "wipe": "right", "voice": v, "layers": L})

    v = "Docs की table में entry points हैं: claude --continue सबसे recent session खोलता है, claude --resume picker खोलता है, और /resume अंदर से दूसरे session पर ले जाता है।"
    sc.append({"id": "docs", "type": "docs", "wipe": "up", "img": "../stories/014_sessions/docs.png", "url": "code.claude.com/docs/en/sessions", "voice": v,
               "scroll": [0, 40], "ch": 1180, "callout": "**--continue**, **--resume**, **/resume**", "cosize": 62, "cues": ["Docs की table"],
               "hls": [{"x": 30, "y": 365, "w": 1440, "h": 52}, {"x": 30, "y": 420, "w": 1440, "h": 52}, {"x": 30, "y": 640, "w": 1440, "h": 52}],
               "hlcues": ["claude --continue", "claude --resume picker", "/resume अंदर"]})

    v = "Session को नाम दो: claude -n auth-refactor से, या अंदर /rename से। फिर picker में arrow keys से चुनो, Enter से resume करो, और Space से preview देखो।"
    T = mkT(st, 2, v)
    n1, n2, pk, ar, en, spc = T("claude -n"), T("/rename"), T("picker में"), T("arrow keys"), T("Enter से"), T("Space से")
    rows = ["auth-refactor", "fix-login", "try-streaming"]
    L = [title("Session ka **naam**"),
         pop('<span class="mono">claude -n auth-refactor</span>', 90, 470, "font-size:40px;font-weight:700;padding:22px 34px;background:#FFD60A;border:5px solid #111;border-radius:30px;white-space:nowrap", n1),
         pop('<span class="mono">/rename auth-refactor</span>', 90, 600, "font-size:40px;font-weight:700;padding:22px 34px;background:#fff;border:5px solid #111;border-radius:30px;white-space:nowrap", n2),
         pop('<div class="mono" style="font-size:30px;color:#FFD60A;background:#111;padding:14px 28px;border-radius:26px 26px 0 0">/resume  (picker \u00b7 example)</div>', 90, 760, "width:900px;overflow:hidden;border:6px solid #111;border-radius:32px;background:#fff;height:430px", pk),
         {"kind": "box", "html": "", "x": 100, "y": 860, "css": "width:880px;height:90px;background:#FFD60A;border-radius:20px;border:4px solid #111",
          "k": [[pk, {"o": 0, "y": 860}], [round(pk + 0.3, 2), {"o": 1, "y": 860}], [ar, {"y": 860}], [round(ar + 0.5, 2), {"y": 970}], [round(ar + 1.2, 2), {"y": 1070}], [en, {"y": 1070}], [round(en + 0.5, 2), {"y": 970}]]}]
    for i, r in enumerate(rows):
        L.append({"kind": "box", "html": f'<span class="mono">{r}</span>', "x": 130, "y": 872 + i * 105 + 14, "css": "font-size:40px;font-weight:700",
                  "k": [[pk, {"o": 0}], [round(pk + 0.3, 2), {"o": 1}]]})
    cap = "font-size:38px;font-weight:800;padding:12px 28px;background:#111;color:#FFD60A;border-radius:16px;white-space:nowrap;box-shadow:0 8px 0 #555"
    L += [pop("\u2191 \u2193", 90, 1250, cap, ar), pop("Enter = resume", 290, 1250, cap, en), pop("Space = preview", 90, 1380, cap, spc)]
    sc.append({"id": "picker", "type": "stage", "wipe": "left", "voice": v, "layers": L})

    v = "दूसरा approach try करना है? /branch चलाओ, नाम भी दे सकते हो। Conversation की copy बन जाती है, और original session वैसा ही रहता है।"
    sc.append({"id": "example", "type": "code", "wipe": "right", "file": "terminal \u00b7 DOCS EXAMPLE", "size": 38, "y0": 330, "voice": v,
               "lines": ["> /branch try-streaming-approach", "# conversation ki copy", "$ claude --continue --fork-session", "# command line se bhi"],
               "caption": "Original **waisa ka waisa**", "cosize": 66,
               "cues": ["/branch चलाओ", "Conversation की copy", "original session", "वैसा ही", "रहता है"]})

    v = "एक बारीकी: बिना नाम वाले session का default name, जैसे my-app-3f, resume के लिए काम नहीं करता। Generated title या तुम्हारा दिया नाम काम करता है।"
    sc.append({"id": "nuance", "type": "compare", "wipe": "up", "voice": v,
               "left": {"title": "Nahi chalta", "rows": ["default name my-app-3f"]}, "right": {"title": "Chalta hai", "rows": ["tumhara naam ya generated title"]},
               "foot": "Default name **handle nahi** hai", "footcue": 4,
               "cues": ["बारीकी", "Generated title", "my-app-3f", "या तुम्हारा", "काम करता है"]})

    v = "तो याद रखो: --continue या --resume से वापस आओ, नाम दो ताकि ढूँढना आसान हो, और /branch से नया रास्ता try करो।"
    T = mkT(st, 5, v)
    sc.append({"id": "recap", "type": "stage", "wipe": "right", "voice": v,
               "layers": recap(T, "Yaad **rakho**", [("Wapas aao", "--continue ya --resume"), ("Naam do", "-n ya /rename"), ("Naya raasta", "/branch")],
                               ["--continue या", "नाम दो", "/branch से"], "नया रास्ता")})

    v = "आप कितने sessions एक साथ चलाते हो? Comment में बताओ।"
    sc.append({"id": "cta", "type": "cta", "wipe": "left", "size": 92, "voice": v, "lines": ["Aap kitne **sessions**", "ek saath?"], "sub": "Comment me batao",
               "cues": ["आप कितने", "एक साथ", "Comment में"], "robot": {"img": "thumbs", "x": 570, "y": 1250, "size": 460, "cue": "Comment में"}})
    return {"_note": "Short 014: Sessions. Source: https://code.claude.com/docs/en/sessions (read 2026-11-03). Format v3.",
            "tag": "Claude Code \u00b7 Sessions", "music": MUSIC, "voice": VOICE, "scenes": sc}


for st, fn in (("013_context-window", build_013), ("014_sessions", build_014)):
    (S / st / "deck.json").write_text(json.dumps(fn(), ensure_ascii=False, indent=1), encoding="utf-8")
    print("ok", st)




