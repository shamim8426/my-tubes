# ---------- Claude Code 04 (prompt caching): theme VIOLET on dark neon; scenes ----------
KB = {"hook_a": 1.05, "hook_b": 1.15, "what_a": 1.1, "what_b": 1.1, "prefix_a": 1.1, "prefix_b": 1.1, "breaks": 1.1, "demo": 1.08, "keep_a": 1.1, "keep_b": 1.15,
      "compact_a": 1.1, "compact_b": 1.1, "ttl": 1.1, "check_a": 1.1, "check_b": 1.1, "cta_a": 1.25, "cta_b": 1.0}
CHAP = {"hook": None, "what": (1, "what is caching"), "prefix": (2, "prefix rule"), "breaks": (3, "what breaks it"), "demo": (4, "terminal demo"), "keep": (5, "safe actions"),
        "compact": (6, "compact"), "ttl": (7, "cache lifetime"), "check": (8, "check it"), "cta": (9, "recap")}
KEYW = {w.strip(",.?!:।") for w in ["Claude", "Code", "cache", "Cache", "caching", "prompt", "prefix", "model", "compact", "usage", "TTL", "CLAUDE.md", "tokens", "read", "creation", "uncached",
                                    "exact", "fast", "mode", "promptCacheTtl", "hit", "rate", "ratio", "सस्ते", "महँगा", "धीमा", "नहीं", "सिर्फ", "CACHE", "एक", "घंटे", "पाँच", "मिनट"]}
MONO = "t"
GREEN = (110, 230, 150)


def termwin(w, h, title="Terminal"):
    im = card(w, h, 26, fill=(9, 12, 18), outline=OUT, ow=3); d = SD(im); ox, oy = 20, 20
    d.rounded_rectangle([ox, oy, ox + w - 1, oy + 64], 26, fill=(20, 25, 36, 255)); d.rectangle([ox, oy + 40, ox + w - 1, oy + 64], fill=(20, 25, 36, 255))
    for i, c in enumerate((RED, AMB, (120, 220, 140))): d.ellipse([ox + 28 + 34 * i, oy + 22, ox + 46 + 34 * i, oy + 40], fill=c + (255,))
    d.text((ox + w / 2, oy + 32), title, font=F(26, "p"), fill=DIM + (255,), anchor="mm")
    return im, d, ox, oy


def tl(d, x, y, s, fill=(214, 222, 238), size=30): d.text((x, y), s, font=F(size, MONO), fill=fill + (255,))


def prompt_line(d, x, y, cmd, t, a0, a1, path=">"):
    tl(d, x, y, path + " ", GREEN); w0 = len(path + " ") * 18.0
    s = typed(cmd, t, a0, a1)
    if t >= a0: tl(d, x + w0, y, s, WHITE)
    elif int(t * 3) % 2 == 0: tl(d, x + w0, y, "|", WHITE)


def key_flash(base, t, t0, x, y, s="Enter"):
    if 0 <= t - t0 <= 0.7: place(base, pill(s, 26, (36, 44, 62), SKY, pad=(18, 5), kind="b", outline=SKY), x, y, 1.0, min(1, (0.7 - (t - t0)) * 4))


def fcard(name, sub, col=SKY, w=520, h=190, size=40):
    spr = card(w, h, 26, outline=col); d = SD(spr); d.text((40, 36), name, font=F(size, MONO), fill=col + (255,)); d.text((40, 36 + size + 26), sub, font=F(34, "p"), fill=(214, 222, 238, 255))
    return spr


def lbl(w, h, text, col, size=34, fill=CARD, tc=WHITE, kind="b", glow=False):
    spr = card(w, h, 22, fill=fill, outline=col, glow=glow); d = SD(spr); d.text((w / 2 + 20, h / 2 + 20), text, font=F(size, kind), fill=tc + (255,), anchor="mm"); return spr


def P(base, text, x, y, t, t0, size=36, fill=(30, 44, 62), color=WHITE, outline=OUT, kind="b", pad=(30, 10), hl=(), hlc=SKY, glow=False):
    if t >= t0: pp = pop(t, t0); place(base, pill(text, size, fill, color, pad=pad, kind=kind, outline=outline, hl=hl, hlc=hlc, glow=glow), x, y, 0.75 + 0.25 * pp, min(1, pp * 1.4))


def C(base, spr, x, y, t, t0, side=0): enter(base, spr, x, y, t, t0, side=side)


# ---------- hook ----------
def _hook_term(t, o):
    im, d, ox, oy = termwin(840, 600, "Claude Code")
    tl(d, ox + 30, oy + 110, "> ", GREEN); tl(d, ox + 70, oy + 110, typed("/model", t, T("hook", 6) - 0.3, T("hook", 7)), WHITE, 32)
    if t >= T("hook", 8): tl(d, ox + 30, oy + 190, "Model switched.", SKY, 30)
    if t >= T("hook", 11): tl(d, ox + 30, oy + 290, "... slow turn (cache rebuilt)", AMB, 30)
    if t >= T("hook", 17): tl(d, ox + 30, oy + 380, "usage went up a lot", RED, 30)
    return im


def b_hook_a(base, t, b):
    o = b["t0"]; lt = t - o
    enter(base, photo("hook", 740, 600, lt, b["t1"] - o + 4), 490, 560, t, o + 0.02, side=-1)
    enter(base, _hook_term(t, o), 1400, 560, t, o + 0.2, side=1)
    place(base, pill("Suddenly slow after a model switch?", 38, (30, 44, 62), WHITE, pad=(30, 10), kind="b", outline=SKY, hl=("slow",)), 960, 190, 1.0, fade(t, o + 0.1, 0.3))


def b_hook_b(base, t, b):
    o = b["t0"]
    place(base, pill("prompt caching", 110, (20, 24, 34), SKY, pad=(70, 24), outline=SKY, kind="b", glow=True), W / 2, 400, 0.85 + 0.15 * pop(t, o), min(1, fade(t, o, 0.2)))
    for i, (s, tt) in enumerate([("what is the cache", T("hook", 32)), ("what breaks it", T("hook", 39)), ("check your hit rate", T("hook", 44))]):
        x = (420, 960, 1500)[i]
        if t >= tt: pp = pop(t, tt); place(base, pill(s, 36, (20, 24, 34), WHITE, pad=(30, 10), outline=OUT, kind="b"), x, 640, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t < T("hook", 32): place(base, pill("why Claude Code feels faster (and cheaper)", 34, (30, 44, 62), WHITE, pad=(30, 10), kind="p", outline=OUT), 960, 640, 1.0, fade(t, o + 0.3))


# ---------- what ----------
def b_what_a(base, t, b):
    o = b["t0"]; lt = t - o
    P(base, "every message re-sends the whole context", 960, 200, t, o + 0.1, 40, hl=("re-sends",))
    enter(base, photo("what", 640, 470, lt, b["t1"] - o + 4), 480, 540, t, o + 0.05, side=-1)
    for i, (s, col, tk) in enumerate([("System prompt", SKY, 10), ("CLAUDE.md", AMB, 13), ("Old messages + results", GREEN, 15)]):
        C(base, lbl(760, 110, s, col, 38), 1330, 400 + 135 * i, t, T("what", tk) - 0.2, side=1)
    P(base, "mostly the SAME as last time", 1330, 830, t, T("what", 19) - 0.2, 36, SKY, INK, SKY, hl=())


def b_what_b(base, t, b):
    o = b["t0"]
    P(base, "with caching", 960, 200, t, o + 0.1, 46, SKY, INK, SKY)
    t_c = T("what", 39) - 0.2; cached = t >= t_c
    C(base, lbl(1400, 130, "old part:  cached rate (cheap)" if cached else "old part:  processed again = full price", GREEN if cached else RED, 40, glow=cached), 960, 430, t, o + 0.2)
    tn = T("what", 47) - 0.2
    if t >= tn: C(base, lbl(700, 120, "new part only: processed", AMB, 38), 1310, 640, t, tn)
    P(base, "automatic", 560, 830, t, T("what", 53) - 0.1, 40, (20, 24, 34), SKY, SKY)


# ---------- prefix ----------
def seg_row(items, w=1500, h=96):
    spr = NI(w, h); d = SD(spr); x = 0
    for (s, wi, col, ok) in items:
        d.rounded_rectangle([x, 0, x + wi - 8, h - 1], 18, fill=(26, 32, 46, 255) if ok else (70, 28, 36, 255), outline=col + (255,), width=3)
        d.text((x + (wi - 8) / 2, h / 2), s, font=F(30, "b"), fill=WHITE + (255,), anchor="mm"); x += wi
    return spr


def b_prefix_a(base, t, b):
    o = b["t0"]
    P(base, "match the START of the request, exactly", 960, 200, t, o + 0.1, 40, hl=("exact", "START"), hlc=SKY)
    if t >= T("prefix", 5) - 0.2:
        C(base, lbl(260, 70, "request 1", DIM, 30, kind="p"), 330, 400, t, T("prefix", 7) - 0.2)
        C(base, seg_row([("system", 260, SKY, True), ("CLAUDE.md", 300, AMB, True), ("chat", 480, GREEN, True)], 1040, 96), 970, 400, t, T("prefix", 7) - 0.2)
    if t >= T("prefix", 11):
        C(base, lbl(260, 70, "request 2", DIM, 30, kind="p"), 330, 560, t, T("prefix", 11) - 0.2)
        C(base, seg_row([("system", 260, SKY, True), ("CLAUDE.md", 300, AMB, True), ("chat", 480, GREEN, True), ("new", 200, AMB, True)], 1240, 96), 1070, 560, t, T("prefix", 11) - 0.2)
    P(base, "same start = read from cache", 960, 740, t, T("prefix", 16), 36, SKY, INK, SKY)
    if t >= T("prefix", 18): P(base, "exact match", 960, 840, t, T("prefix", 18), 34, (20, 24, 34), WHITE, OUT, hl=("exact",))


def b_prefix_b(base, t, b):
    o = b["t0"]
    t_c = T("prefix", 25)
    place(base, pill("change at the start  =  everything after is rebuilt", 38, (70, 28, 36), RED, pad=(30, 10), kind="b", outline=RED), 960, 200, 1.0, fade(t, o + 0.1, 0.3))
    C(base, seg_row([("system", 300, RED, t < t_c), ("CLAUDE.md", 330, AMB, t < t_c), ("chat", 560, GREEN, t < t_c)], 1190, 96), 960, 330, t, o + 0.2)
    for i, (s, sub, col, tk) in enumerate([("1  System prompt", "rarely changes", SKY, 38), ("2  Project context", "CLAUDE.md, memory: set at session start", AMB, 44), ("3  Conversation", "changes every turn", GREEN, 51)]):
        spr = card(1500, 130, 22, outline=col); d = SD(spr); d.text((50, 85), s, font=F(38, "b"), fill=WHITE + (255,), anchor="lm"); d.text((1470, 85), sub, font=F(28, "p"), fill=col + (255,), anchor="rm")
        C(base, spr, 960, 500 + 150 * i, t, T("prefix", tk) - 0.3)


# ---------- breaks ----------
BR = [("/model switch", "each model has its own cache", SKY, 7), ("fast mode on / off", "separate cache per speed", AMB, 19), ("tool definitions", "MCP add / remove (no tool search)", GREEN, 31), ("many images", "oldest dropped in batches", (255, 130, 200), 44)]


def b_breaks(base, t, b):
    o = b["t0"]
    P(base, "what BREAKS the cache", 960, 190, t, o + 0.1, 44, (70, 28, 36), RED, RED, hl=("BREAKS",), hlc=RED)
    for i, (name, sub, col, tk) in enumerate(BR):
        x = 540 + 840 * (i % 2); y = 400 + 230 * (i // 2)
        C(base, fcard(name, sub, col, 740, 190, 40), x, y, t, T("breaks", tk) - 0.3)
    P(base, "next turn: slower + costlier, ONCE", 960, 800, t, T("breaks", 52) - 0.2, 38, AMB, INK, AMB)


# ---------- terminal demo ----------
def b_demo(base, t, b):
    o = b["t0"]; sid = "demo"
    t_p2 = T(sid, 17); t_p3 = T(sid, 41)
    page = 3 if t >= t_p3 else (2 if t >= t_p2 else 1)
    im, d, ox, oy = termwin(1560, 700, "Claude Code"); x0, y0 = ox + 50, oy + 110; lh = 52
    if page == 1:
        prompt_line(d, x0, y0, "/model", t, T(sid, 12) - 0.3, T(sid, 13) + 0.2)
        for i, (s, tt) in enumerate([("1. Default (recommended)", T(sid, 14)), ("2. Sonnet", T(sid, 14) + 0.2), ("3. Opus", T(sid, 14) + 0.4)]):
            if t >= tt:
                sel = (i == 1 and t >= T(sid, 16)); tl(d, x0 + 30, y0 + lh * 1.6 + i * lh, ("> " if sel else "  ") + s, SKY if sel else (214, 222, 238), 34)
        st = "STEP 1   pick the model FIRST, at session start"
        if t >= T(sid, 16): tl(d, x0, y0 + lh * 5.2, "Model set. Cache starts clean, nothing to lose.", GREEN, 30)
    elif page == 2:
        prompt_line(d, x0, y0, "/model", t, T(sid, 22) - 0.3, T(sid, 24))
        if t >= T(sid, 26):
            a = fade(t, T(sid, 26), 0.25); d.rounded_rectangle([x0, y0 + lh * 1.5, x0 + 1380, y0 + lh * 1.5 + 270], 20, fill=(50, 38, 20, int(255 * a)), outline=AMB + (int(255 * a),), width=3)
            tl(d, x0 + 30, y0 + lh * 1.5 + 30, "Cache is still warm.", tuple(int(c * a) for c in AMB), 34)
            if t >= T(sid, 31): tl(d, x0 + 30, y0 + lh * 1.5 + 90, "Switching model reads the whole chat uncached.", WHITE, 32)
            if t >= T(sid, 36): tl(d, x0 + 30, y0 + lh * 1.5 + 190, "Switch anyway?   [ Yes ]   [ No ]", SKY, 34)
        st = "STEP 2   switch later = Claude Code asks first"
    else:
        prompt_line(d, x0, y0, "/usage", t, T(sid, 42), T(sid, 44) + 0.3)
        if t >= T(sid, 46): tl(d, x0, y0 + lh * 1.6, "Session", WHITE, 36)
        if t >= T(sid, 48): tl(d, x0 + 30, y0 + lh * 2.6, "Prompt cache (main):  94% hit ratio  -  2 misses  -  warm", SKY, 30)
        if t >= T(sid, 55): d.line([(x0 + 30, y0 + lh * 3.4), (x0 + 1100, y0 + lh * 3.4)], fill=SKY + (255,), width=4)
        st = "STEP 3   /usage  >  Prompt cache line"
    enter(base, im, 960, 565, t, o, dur=0.3)
    step(base, t, T(sid, 5) - 0.3 if page == 1 else (t_p2 if page == 2 else t_p3) - 0.1, st)
    if page == 1: key_flash(base, t, T(sid, 13) + 0.5, 1560, 880)
    if page == 2: key_flash(base, t, T(sid, 24) + 0.3, 1560, 880)
    if page == 3: key_flash(base, t, T(sid, 44) + 0.5, 1560, 880)
    if page == 3 and t >= T(sid, 48): place(base, pill("example numbers", 24, (20, 24, 34), AMB, pad=(16, 4), kind="p", outline=AMB), 1500, 300)
    illu(base)


# ---------- keep ----------
KP = [("edit repo files", 10), ("permission mode", 13), ("output style", 16), ("skills + commands", 19), ("/recap", 22), ("/rewind", 25)]


def b_keep_a(base, t, b):
    o = b["t0"]
    P(base, "these KEEP the cache", 960, 200, t, o + 0.1, 46, GREEN, INK, GREEN)
    for i, (s, tk) in enumerate(KP):
        x = 480 + 480 * (i % 3); y = 440 + 210 * (i // 3)
        C(base, lbl(440, 150, "+ " + s, GREEN, 34, kind="b"), x, y, t, T("keep", tk) - 0.25)
    P(base, "cache safe", 960, 820, t, T("keep", 29) - 0.1, 36, (20, 24, 34), GREEN, GREEN)


def b_keep_b(base, t, b):
    o = b["t0"]
    P(base, "edit CLAUDE.md in the middle of a session", 960, 200, t, o + 0.1, 40, hl=("CLAUDE.md",))
    C(base, fcard("CLAUDE.md", "edited mid-session", AMB, 600, 200, 44), 520, 450, t, T("keep", 32) - 0.3, side=-1)
    P(base, "cache: kept", 1360, 380, t, T("keep", 41) - 0.1, 38, GREEN, INK, GREEN)
    P(base, "new text: NOT read yet", 1360, 520, t, T("keep", 47) - 0.1, 38, AMB, INK, AMB)
    if t >= T("keep", 55) - 0.2:
        P(base, "loads after", 480, 690, t, T("keep", 53) - 0.2, 34, (20, 24, 34), WHITE, OUT)
        for i, (s, tk) in enumerate([("/clear", 55), ("/compact", 56), ("restart", 58)]):
            P(base, s, 800 + 300 * i, 690, t, T("keep", tk) - 0.1, 40, (20, 24, 34), SKY, SKY, kind=MONO)


# ---------- compact ----------
def b_compact_a(base, t, b):
    o = b["t0"]
    P(base, "/compact  =  summary replaces history", 960, 200, t, o + 0.1, 40, hl=("summary",))
    spr = card(560, 460, 26, outline=OUT); d = SD(spr)
    for i in range(5): d.rounded_rectangle([40, 50 + 76 * i, 540, 50 + 76 * i + 56], 12, fill=(26, 32, 46, 255), outline=OUT + (255,), width=2)
    d.text((290, 20 + 2), "", font=F(10, "p"), fill=WHITE + (255,))
    C(base, spr, 520, 520, t, o + 0.2, side=-1)
    P(base, "old history", 520, 800, t, T("compact", 5) - 0.2, 32, (20, 24, 34), DIM, OUT, kind="p")
    if t >= T("compact", 9) - 0.2:
        SD(base).polygon([(800, 500), (900, 500), (900, 460), (990, 530), (900, 600), (900, 560), (800, 560)], fill=SKY + (255,))
        C(base, lbl(500, 150, "summary", SKY, 44, glow=True), 1380, 520, t, T("compact", 10) - 0.2, side=1)
    P(base, "cache warm  =  cheap", 960, 830, t, T("compact", 23) - 0.1, 40, GREEN, INK, GREEN)


def b_compact_b(base, t, b):
    o = b["t0"]; lt = t - o
    P(base, "long break  >  cache expired", 960, 200, t, o + 0.1, 40, hl=("expired",), hlc=AMB)
    enter(base, photo("clock", 600, 440, lt, b["t1"] - o + 4), 460, 520, t, o + 0.05, side=-1)
    P(base, "resume old session + /compact", 1330, 380, t, T("compact", 36) - 0.2, 34, (20, 24, 34), WHITE, OUT, kind="b")
    if t >= T("compact", 43) - 0.2: C(base, lbl(760, 130, "whole history read UNCACHED", RED, 36, fill=(70, 28, 36), tc=RED), 1330, 540, t, T("compact", 43) - 0.2)
    P(base, "most expensive case", 1330, 680, t, T("compact", 51) - 0.1, 36, RED, INK, RED)
    P(base, "better: /compact when a task is DONE", 960, 860, t, T("compact", 55) - 0.2, 38, GREEN, INK, GREEN)


# ---------- ttl ----------
def b_ttl(base, t, b):
    o = b["t0"]; lt = t - o
    P(base, "idle too long  >  cache expires", 960, 200, t, o + 0.1, 42, hl=("expires",), hlc=AMB)
    enter(base, photo("clock", 600, 520, lt, b["t1"] - o + 4), 460, 520, t, o + 0.05, side=-1)
    C(base, lbl(850, 130, "Claude subscription (in plan)", SKY, 36), 1330, 340, t, T("ttl", 15) - 0.2, side=1)
    if t >= T("ttl", 26) - 0.1: P(base, "1 hour", 1330, 470, t, T("ttl", 26) - 0.1, 70, SKY, INK, SKY)
    C(base, lbl(850, 130, "API key / credits", AMB, 36), 1330, 630, t, T("ttl", 32) - 0.2, side=1)
    if t >= T("ttl", 36) - 0.1: P(base, "5 minutes", 1330, 760, t, T("ttl", 36) - 0.1, 56, AMB, INK, AMB)
    P(base, "promptCacheTtl:  5m  or  1h", 960, 880, t, T("ttl", 42) - 0.1, 36, (20, 24, 34), SKY, SKY, kind=MONO)


# ---------- check ----------
def meter(label, col, frac, t, t0):
    spr = card(1300, 130, 26, outline=col); d = SD(spr); q = ease_out(min(1, max(0, (t - t0) / 0.9)))
    d.text((40, 40), label, font=F(30, MONO), fill=col + (255,)); d.rounded_rectangle([40, 90, 40 + 1200 * frac * q, 112], 8, fill=col + (255,)); return spr


def b_check_a(base, t, b):
    o = b["t0"]
    P(base, "2 numbers tell you", 960, 200, t, o + 0.1, 44)
    t1, t2 = T("check", 12), T("check", 21)
    C(base, meter("cache_read_input_tokens   (cheap)", GREEN, 0.85, t, t1), 960, 440, t, t1 - 0.3)
    C(base, meter("cache_creation_input_tokens   (new)", AMB, 0.25, t, t2), 960, 640, t, t2 - 0.3)
    P(base, "read HIGH + creation LOW  =  good", 960, 840, t, T("check", 28) - 0.2, 38, GREEN, INK, GREEN)


def b_check_b(base, t, b):
    o = b["t0"]
    C(base, lbl(1300, 140, "creation high every turn", RED, 42, fill=(70, 28, 36), tc=RED), 960, 340, t, T("check", 37) - 0.3)
    P(base, "something in the prefix keeps changing", 960, 500, t, T("check", 44) - 0.2, 38, (30, 44, 62), WHITE, RED, hl=("prefix",), hlc=SKY)
    P(base, "/usage  >  Prompt cache (main)", 960, 640, t, T("check", 8) + 0.0, 34, (20, 24, 34), SKY, SKY, kind=MONO) if False else None
    if t >= T("check", 51): P(base, "DISABLE_PROMPT_CACHING=1", 960, 700, t, T("check", 51) - 0.1, 44, (20, 24, 34), AMB, AMB, kind=MONO)
    if t >= T("check", 55): P(base, "only for debugging", 960, 810, t, T("check", 55) - 0.1, 36, AMB, INK, AMB)


# ---------- recap + CTA ----------
def b_cta_a(base, t, b):
    sid = "cta"
    place(base, pill("3 THINGS TO REMEMBER", 52, (20, 24, 34), WHITE, pad=(50, 14), kind="b", outline=SKY, glow=True), W / 2, 230, 1.0, fade(t, b["t0"], 0.25))
    for i, (n, s, tt) in enumerate([("1", "pick model + effort at the START", T(sid, 6)), ("2", "/compact after a task, not in the middle", T(sid, 15)), ("3", "/usage: watch your cache hit rate", T(sid, 27))]):
        y = 430 + 150 * i; enter(base, card(1300, 110, 26), 960, y, t, tt - 0.2, side=0)
        spr = NI(1300, 110); d = SD(spr); d.rounded_rectangle([24, 22, 90, 88], 14, fill=SKY + (255,)); d.text((57, 55), n, font=F(40, "b"), fill=INK + (255,), anchor="mm"); d.text((130, 55), s, font=F(36, "p"), fill=WHITE + (255,), anchor="lm"); enter(base, spr, 960, y, t, tt - 0.2)


def b_cta_b(base, t, b):
    sid = "cta"; t1, t2, t3 = T(sid, 41), T(sid, 43), T(sid, 45)
    place(base, pill("Was it useful?  Save it", 44, (30, 44, 62), WHITE, pad=(34, 12), kind="b", outline=SKY), 960, 195, 1.0, fade(t, b["t0"], 0.3))
    if t >= t1 - 0.2: place(base, pill("Comment", 60, (20, 24, 34), WHITE, pad=(40, 12), kind="b", outline=OUT), 960, 335, 0.8 + 0.2 * pop(t, t1 - 0.2), min(1, fade(t, t1 - 0.2, 0.2)))
    if t >= t2: place(base, pill("CACHE", 120, SKY, INK, pad=(60, 14), kind="b", glow=True), 960, 510, 0.8 + 0.2 * pop(t, t2), min(1, fade(t, t2, 0.2)))
    if t >= t3: place(base, pill("Follow DevRoboLab", 54, (20, 24, 34), SKY, pad=(40, 12), kind="b", outline=OUT), 960, 690, 0.8 + 0.2 * pop(t, t3), min(1, fade(t, t3, 0.2)))
    tt = t3 + 0.9
    if t >= tt:
        for i, s in enumerate(["Watch next", "Subscribe"]):
            enter(base, card(640, 150, 28, glow=True), 560 + 800 * i, 860, t, tt + 0.3 * i, side=0)
            spr = NI(640, 150); SD(spr).text((320, 75), s, font=F(40, "b"), fill=WHITE + (255,), anchor="mm"); enter(base, spr, 560 + 800 * i, 860, t, tt + 0.3 * i)


def _mk():
    B = []
    def add(i, sid, a, b): B.append(dict(id=i, sid=sid, t0=a, t1=b))
    add("hook_a", "hook", 0.0, T("hook", 23) - 0.2); add("hook_b", "hook", T("hook", 23) - 0.2, E("hook"))
    add("what_a", "what", S("what", 0), T("what", 27) - 0.2); add("what_b", "what", T("what", 27) - 0.2, E("what"))
    add("prefix_a", "prefix", S("prefix", 0), T("prefix", 21) - 0.2); add("prefix_b", "prefix", T("prefix", 21) - 0.2, E("prefix"))
    add("breaks", "breaks", S("breaks", 0), E("breaks")); add("demo", "demo", S("demo", 0), E("demo"))
    add("keep_a", "keep", S("keep", 0), T("keep", 32) - 0.2); add("keep_b", "keep", T("keep", 32) - 0.2, E("keep"))
    add("compact_a", "compact", S("compact", 0), T("compact", 31) - 0.2); add("compact_b", "compact", T("compact", 31) - 0.2, E("compact"))
    add("ttl", "ttl", S("ttl", 0), E("ttl"))
    add("check_a", "check", S("check", 0), T("check", 37) - 0.2); add("check_b", "check", T("check", 37) - 0.2, E("check"))
    add("cta_a", "cta", S("cta", 0), T("cta", 34) - 0.2); add("cta_b", "cta", T("cta", 34) - 0.2, TOTAL + 1)
    return B
B = _mk()

