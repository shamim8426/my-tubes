# ---------- beats (063 Tasks in Gemini) ; appended into make_final.py by build_make.py ----------
def TT(sc, i): return T(sc, i)
def P(s, size=36, fill=(24, 30, 40), col=WHITE, kind="b", outline=None, hl=(), pad=(30, 10), glow=False):
    return pill(s, size, fill, col, pad=pad, kind=kind, outline=outline, hl=hl, glow=glow)
def pin(base, im, x, y, t, t0, rot=0):
    if t >= t0: pp = pop(t, t0); place(base, im, x, y, 0.7 + 0.3 * pp, min(1, pp * 1.4), rot)
def head(base, t, o, s, hl=(), col=None):
    place(base, P(s, 40, outline=col or ACC, col=WHITE, hl=hl), W / 2, 150, 1.0, fade(t, o, 0.3))
def warn(s, size=32): return P(s, size, (60, 44, 20), AMB, outline=AMB)
def bad(s, size=32): return P(s, size, (60, 24, 30), RED, outline=RED)
def good(s, size=34): return P(s, size, ACC, INK)


_tg = {}
def toggle_img(w):
    """official blog hero: 'Describe a task' box + Chat | Task toggle (own capture of blog.google)"""
    if w in _tg: return _tg[w]
    src = Image.open(HERE / "raw/shot_toggle.png").convert("RGB").crop((380, 1180, 2180, 2060)); h = int(w * src.height / src.width)
    pg = src.resize((w - 40, h - 40), Image.LANCZOS).convert("RGBA"); sh = Image.new("RGBA", (w, h + 50), (0, 0, 0, 0)); d = ImageDraw.Draw(sh)
    d.rounded_rectangle([0, 0, w - 1, h - 1], 18, fill=(250, 249, 246, 255), outline=(200, 204, 214, 255), width=3); sh.alpha_composite(pg, (20, 20))
    tag = pill("Official: blog.google  /  Put Gemini to work for you", 20, (20, 24, 34), (200, 208, 224), pad=(16, 5), kind="p", outline=OUT)
    sh.alpha_composite(tag, ((w - tag.width) // 2, h - 8)); _tg[w] = sh; return sh


def tile(label, sub, letter, col=None, w=360, h=220, on=True):
    c = card(w, h, 26, outline=(col or ACC) if on else OUT); d = SD(c)
    d.ellipse([46, 46, 126, 126], fill=(col or ACC) + (255,)); d.text((86, 86), letter, font=F(40, "b"), fill=INK + (255,), anchor="mm")
    d.text((150, 86), label, font=F(34, "b"), fill=WHITE + (255,), anchor="lm")
    if sub: d.text((46, h - 40), sub, font=F(26, "p"), fill=DIM + (255,), anchor="lm")
    return c


def chat_window(w, h, title="New chat"):
    im = card(w, h, 26, fill=(14, 17, 25)); d = SD(im)
    for i, c in enumerate((RED, AMB, (120, 220, 140))): d.ellipse([48 + 30 * i, 44, 64 + 30 * i, 60], fill=c + (255,))
    d.text((160, 52), title, font=F(28, "p"), fill=DIM + (255,), anchor="lm"); return im


def doc_icon(d, x, y, s=1.0, col=ACC, label="PDF"):
    w, h = 110 * s, 140 * s; d.rounded_rectangle([x, y, x + w, y + h], 12, fill=(240, 244, 236, 255)); d.polygon([(x + w - 34 * s, y), (x + w, y + 34 * s), (x + w - 34 * s, y + 34 * s)], fill=(200, 206, 196, 255))
    d.rounded_rectangle([x + 10 * s, y + h - 50 * s, x + w - 10 * s, y + h - 14 * s], 8, fill=col + (255,)); d.text((x + w / 2, y + h - 32 * s), label, font=F(int(22 * s), "b"), fill=INK + (255,), anchor="mm")


def checkbox(d, x, y, on, col=None):
    d.rounded_rectangle([x, y, x + 44, y + 44], 10, outline=((col or ACC) if on else DIM) + (255,), width=4)
    if on: d.line([(x + 8, y + 22), (x + 20, y + 35), (x + 38, y + 8)], fill=(col or ACC) + (255,), width=6)


def _mk():
    B = []
    def add(i, sid, a, b): B.append(dict(id=i, sid=sid, t0=a, t1=b))
    cut = lambda sc, i, d=0.2: TT(sc, i) - d
    add("hook_a", "hook", 0.0, cut("hook", 23)); add("hook_b", "hook", cut("hook", 23), cut("hook", 46)); add("hook_c", "hook", cut("hook", 46), E("hook"))
    add("what_a", "what", S("what", 0), cut("what", 48)); add("what_b", "what", cut("what", 48), cut("what", 96)); add("what_c", "what", cut("what", 96), E("what"))
    add("who_a", "who", S("who", 0), cut("who", 32)); add("who_b", "who", cut("who", 32), cut("who", 58)); add("who_c", "who", cut("who", 58), cut("who", 83)); add("who_d", "who", cut("who", 83), E("who"))
    add("start_a", "start", S("start", 0), cut("start", 51)); add("start_b", "start", cut("start", 51), cut("start", 73)); add("start_c", "start", cut("start", 73), E("start"))
    add("ex1_a", "ex1", S("ex1", 0), cut("ex1", 17)); add("ex1_b", "ex1", cut("ex1", 17), cut("ex1", 42)); add("ex1_c", "ex1", cut("ex1", 42), cut("ex1", 67)); add("ex1_d", "ex1", cut("ex1", 67), E("ex1"))
    add("ex2_a", "ex2", S("ex2", 0), cut("ex2", 30)); add("ex2_b", "ex2", cut("ex2", 30), cut("ex2", 64)); add("ex2_c", "ex2", cut("ex2", 64), E("ex2"))
    add("ex3_a", "ex3", S("ex3", 0), cut("ex3", 49)); add("ex3_b", "ex3", cut("ex3", 49), cut("ex3", 65)); add("ex3_c", "ex3", cut("ex3", 65), E("ex3"))
    add("safe_a", "safety", S("safety", 0), cut("safety", 33)); add("safe_b", "safety", cut("safety", 33), cut("safety", 71)); add("safe_c", "safety", cut("safety", 71), E("safety"))
    add("us_a", "us", S("us", 0), cut("us", 36)); add("us_b", "us", cut("us", 36), cut("us", 54)); add("us_c", "us", cut("us", 54), E("us"))
    add("lim_a", "limits", S("limits", 0), cut("limits", 27)); add("lim_b", "limits", cut("limits", 27), cut("limits", 48)); add("lim_c", "limits", cut("limits", 48), E("limits"))
    add("off_a", "off", S("off", 0), cut("off", 34)); add("off_b", "off", cut("off", 34), E("off"))
    add("cta_a", "cta", S("cta", 0), cut("cta", 53)); add("cta_b", "cta", cut("cta", 53), TOTAL + 1)
    return B
B = _mk()


# ---- hook ----
def b_hook_a(base, t, b):
    o = b["t0"]
    enter(base, toggle_img(1020), 600, 560, t, o, side=-1, dur=0.25)
    pin(base, P("FREE in 6 countries", 52, (20, 24, 34), WHITE, outline=ACC, glow=True, hl=("FREE", "6")), 1500, 380, t, o + 0.3)
    pin(base, good("India included", 40), 1500, 500, t, o + 0.8)
    pin(base, P("Tasks in Gemini  ·  Nov 17, 2026", 34, outline=OUT), 600, 190, t, TT("hook", 13))
    pin(base, P("not just answers", 32, kind="p", outline=OUT, col=DIM), 1500, 640, t, TT("hook", 5))
    pin(base, P("it finishes the work", 34, outline=ACC, hl=("work",)), 1500, 730, t, TT("hook", 9))


COUNTRIES = [("US", 18), ("Japan", 1), ("Korea", 2), ("Canada", 3), ("Australia", 4), ("India", 5)]
def b_hook_b(base, t, b):
    o = b["t0"]; t6 = TT("hook", 29); tin = TT("hook", 41)
    enter(base, note("blogfree", 1300, 470), W / 2, 400, t, o + 0.05)
    for i, (c, _) in enumerate(COUNTRIES):
        tt = t6 + 0.12 * i; india = c == "India"; hot = india and t >= tin
        if t >= tt: pp = pop(t, tt); im = P(c, 38, ACC if hot else (24, 30, 40), INK if hot else WHITE, outline=None if hot else OUT, glow=hot); place(base, im, 330 + 252 * i, 790, (0.7 + 0.3 * pp) * (1.12 if hot else 1), min(1, pp * 1.4))
    pin(base, P("no subscription needed", 32, kind="p", outline=OUT), W / 2, 880, t, TT("hook", 32))


def b_hook_c(base, t, b):
    o = b["t0"]
    place(base, P("GEMINI TASKS: FULL GUIDE", 76, (20, 24, 34), WHITE, outline=ACC, glow=True, hl=("TASKS",), pad=(56, 20)), W / 2, 300, 0.85 + 0.15 * pop(t, o), min(1, fade(t, o, 0.2)))
    items = [("what is it", 48, 480, 520), ("who gets it", 51, 960, 520), ("how to turn on", 53, 1440, 520), ("3 full examples", 56, 720, 660), ("safety", 60, 1200, 660)]
    for s, k, x, y in items: pin(base, P(s, 38, outline=ACC, col=ACC), x, y, t, TT("hook", k) - 0.1)


# ---- what ----
def b_what_a(base, t, b):
    o = b["t0"]; head(base, t, o, "Chat vs Task", hl=("Task",))
    c = card(760, 560, 28); d = SD(c); d.text((60, 70), "CHAT", font=F(44, "b"), fill=DIM + (255,), anchor="lm"); d.text((60, 130), "question  ->  answer", font=F(30, "p"), fill=DIM + (255,), anchor="lm")
    enter(base, c, 500, 560, t, o + 0.1, side=-1)
    if t >= TT("what", 12) - 0.2: place(base, bubble(560, 74, "What is a heat pump?", "user", 30), 540, 520, 1.0, fade(t, TT("what", 12) - 0.2))
    if t >= TT("what", 14): place(base, bubble(600, 74, "A heat pump moves heat...", "claude", 30), 460, 640, 1.0, fade(t, TT("what", 14)))
    if t >= TT("what", 16) - 0.3:
        c2 = card(880, 600, 30, glow=True); d2 = SD(c2); d2.text((60, 70), "TASK", font=F(48, "b"), fill=ACC + (255,), anchor="lm"); d2.text((60, 130), "you hand over a whole job", font=F(30, "p"), fill=WHITE + (255,), anchor="lm")
        rows = [("many steps, one request", 27), ("works in the background", 32), ("tells you when it's done", 44)]
        for i, (s, k) in enumerate(rows):
            y = 200 + 120 * i; on = t >= TT("what", k) - 0.1
            d2.rounded_rectangle([60, y, 820, y + 96], 20, fill=((22, 56, 56, 255) if on else (26, 31, 45, 255)), outline=(ACC if on else OUT) + (255,), width=3 if on else 2)
            checkbox(d2, 90, y + 26, on); d2.text((160, y + 48), s, font=F(34, "p"), fill=(WHITE if on else DIM) + (255,), anchor="lm")
        enter(base, c2, 1380, 570, t, TT("what", 16) - 0.3, side=1)


def b_what_b(base, t, b):
    o = b["t0"]; head(base, t, o, "Examples from Google's help page", hl=("help",))
    ex = [("Clean inbox", "archive newsletters", "@", 56), ("To-do list", "after a holiday", "✓", 69), ("Price alert", "flight / hotel in budget", "₹", 72), ("Research + PDF", "with sources", "R", 88)]
    for i, (a, s, l, k) in enumerate(ex):
        x = 380 + 540 * (i % 2); y = 400 + 270 * (i // 2); tt = TT("what", k) - 0.15
        if t >= tt: pp = pop(t, tt); place(base, tile(a, s, l if l not in "✓₹" else a[0], w=500, h=230, on=True), x, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    enter(base, note("inbox", 720, 560), 1530, 540, t, o + 0.3, side=1)


def b_what_c(base, t, b):
    o = b["t0"]; head(base, t, o, "What Gemini uses for a task")
    for i, (a, s, l, k) in enumerate([("Gmail", "connected app", "M", 104), ("Calendar", "connected app", "C", 106), ("Browser", "when needed", "B", 111)]):
        pin(base, tile(a, s, l, w=420, h=220), 500 + 460 * i, 380, t, TT("what", k) - 0.2)
    if t >= TT("what", 121) - 0.2:
        pp = pop(t, TT("what", 121) - 0.2); c = card(640, 200, 28); d = SD(c); d.text((60, 70), "old name", font=F(28, "p"), fill=DIM + (255,), anchor="lm")
        d.text((60, 140), "Spark", font=F(52, "b"), fill=DIM + (255,), anchor="lm"); d.text((300, 140), "->", font=F(52, "b"), fill=WHITE + (255,), anchor="lm"); d.text((400, 140), "Task", font=F(52, "b"), fill=ACC + (255,), anchor="lm")
        place(base, c, 480, 720, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t >= TT("what", 128) - 0.4: enter(base, note("hydrogen", 980, 330), 1330, 720, t, TT("what", 128) - 0.4, side=1)


# ---- who ----
def b_who_a(base, t, b):
    o = b["t0"]; head(base, t, o, "Free, no subscription: 6 countries", hl=("6",))
    enter(base, note("helpfree", 1040, 470), 590, 560, t, o + 0.3, side=-1)
    ks = [24, 25, 26, 27, 28, 31]; names = ["Australia", "Canada", "India", "Japan", "South Korea", "US"]
    for i, (n, k) in enumerate(zip(names, ks)):
        x = 1360 + 330 * (i % 2); y = 360 + 160 * (i // 2); tt = TT("who", k) - 0.1; hot = n == "India"
        if t >= tt:
            pp = pop(t, tt); c = card(300, 120, 22, fill=(22, 56, 56) if hot else CARD, outline=ACC if hot else OUT, glow=hot); d = SD(c)
            d.text((170, 80), n, font=F(36 if len(n) < 9 else 30, "b"), fill=(ACC if hot else WHITE) + (255,), anchor="mm"); place(base, c, x, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    pin(base, P("+ rolling out", 26, kind="p", outline=OUT, col=DIM), 1525, 850, t, TT("who", 31) + 0.6)


def b_who_b(base, t, b):
    o = b["t0"]; head(base, t, o, "Other countries")
    c = card(780, 440, 30, glow=t >= TT("who", 38)); d = SD(c); d.text((60, 80), "Everywhere else", font=F(42, "b"), fill=WHITE + (255,), anchor="lm")
    if t >= TT("who", 36): d.text((60, 190), "with Google AI", font=F(36, "p"), fill=DIM + (255,), anchor="lm"); d.text((60, 260), "Pro or Ultra", font=F(48, "b"), fill=ACC + (255,), anchor="lm")
    if t >= TT("who", 40): d.text((60, 360), "(paid subscription)", font=F(28, "p"), fill=DIM + (255,), anchor="lm")
    enter(base, c, 520, 560, t, o + 0.1, side=-1)
    if t >= TT("who", 46) - 0.2:
        c2 = card(860, 440, 30, outline=RED); d2 = SD(c2); d2.text((60, 80), "Not yet", font=F(42, "b"), fill=RED + (255,), anchor="lm")
        for i, (s, k) in enumerate([("European Economic Area", 47), ("Nigeria", 50), ("Switzerland", 51), ("United Kingdom", 53)]):
            if t >= TT("who", k) - 0.1: d2.text((80, 160 + 70 * i), "x  " + s, font=F(34, "p"), fill=WHITE + (255,), anchor="lm")
        enter(base, c2, 1400, 560, t, TT("who", 46) - 0.2, side=1)


def b_who_c(base, t, b):
    o = b["t0"]; head(base, t, o, "3 conditions", hl=("3",))
    def cc(i, k, draw):
        tt = TT("who", k) - 0.15
        if t >= tt: c = card(500, 420, 30, glow=True); draw(SD(c)); pp = pop(t, tt); place(base, c, 400 + 560 * i, 540, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    cc(0, 63, lambda d: (d.text((270, 170), "18+", font=F(130, "b"), fill=ACC + (255,), anchor="mm"), d.text((270, 330), "age 18 or over", font=F(32, "p"), fill=WHITE + (255,), anchor="mm")))
    def acc(d):
        d.text((270, 120), "Personal", font=F(46, "b"), fill=ACC + (255,), anchor="mm"); d.text((270, 180), "Google account", font=F(32, "p"), fill=WHITE + (255,), anchor="mm")
        if t >= TT("who", 70) - 0.1: d.rounded_rectangle([60, 260, 480, 340], 18, fill=(60, 24, 30, 255), outline=RED + (255,), width=2); d.text((270, 300), "work / school: not yet", font=F(28, "b"), fill=RED + (255,), anchor="mm")
    cc(1, 67, acc)
    def hist(d):
        d.text((270, 130), "Gemini History", font=F(40, "b"), fill=WHITE + (255,), anchor="mm"); toggle(d, 200, 220, t >= TT("who", 81), w=140, h=70); d.text((270, 350), "must be ON", font=F(32, "p"), fill=ACC + (255,), anchor="mm")
    cc(2, 80, hist)


def b_who_d(base, t, b):
    o = b["t0"]; head(base, t, o, "Where you get it")
    for i, (a, s, l, k) in enumerate([("Mobile app", "Gemini, Android / iPhone", "M", 86), ("Mac app", "Gemini app on Mac", "D", 88), ("Website", "gemini.google.com", "W", 91)]):
        pin(base, tile(a, s, l, w=480, h=240, on=t >= TT("who", k) - 0.2), 420 + 540 * i, 450, t, min(TT("who", k) - 0.2, o + 0.2 + 0.3 * i))
    pin(base, warn("rolling out slowly: not there yet? check again in a few days", 32), W / 2, 760, t, TT("who", 101) - 0.1)


# ---- start ----
MOCK_W, MOCK_H, MOCK_C = 1000, 620, (640, 560)
def gem_home(task_on, text="", send_hot=False):
    c = card(MOCK_W, MOCK_H, 28, fill=(14, 17, 25)); d = SD(c)
    d.text((60, 70), "Gemini", font=F(36, "b"), fill=WHITE + (255,), anchor="lm"); d.text((520, 190), "What can I get done for you?", font=F(40, "p"), fill=WHITE + (255,), anchor="mm")
    d.rounded_rectangle([80, 260, 960, 380], 40, fill=(26, 31, 45, 255), outline=(ACC if text else OUT) + (255,), width=3)
    d.text((130, 320), text or ("Describe a task" if task_on else "Ask Gemini"), font=F(30, "p"), fill=(WHITE if text else DIM) + (255,), anchor="lm")
    d.ellipse([870, 285, 940, 355], fill=(ACC if send_hot else (60, 70, 92)) + (255,)); d.text((905, 320), ">", font=F(34, "b"), fill=INK + (255,), anchor="mm")
    d.rounded_rectangle([340, 420, 700, 500], 40, fill=(26, 31, 45, 255), outline=OUT + (255,), width=2)
    sx = 610 if task_on else 430; d.rounded_rectangle([sx - 90, 425, sx + 90, 495], 35, fill=(ACC if task_on else (70, 78, 98)) + (255,))
    d.text((430, 460), "Chat", font=F(32, "b"), fill=(INK if not task_on else DIM) + (255,), anchor="mm"); d.text((610, 460), "Task", font=F(32, "b"), fill=(INK if task_on else DIM) + (255,), anchor="mm")
    return c
def mock_xy(x, y): return MOCK_C[0] - MOCK_W / 2 + x, MOCK_C[1] - MOCK_H / 2 + y


def b_start_a(base, t, b):
    o = b["t0"]; t_tap = TT("start", 39)
    enter(base, gem_home(t >= t_tap), MOCK_C[0], MOCK_C[1], t, o + 0.05, side=-1)
    step(base, t, TT("start", 7) - 0.2, "STEP 2   tap Task" if t >= TT("start", 23) - 0.2 else "STEP 1   open the app / gemini.google.com")
    enter(base, toggle_img(700), 1530, 540, t, o + 0.4, side=1)
    tx, ty = mock_xy(610, 460)
    pts = [(o, 900, 300), (TT("start", 30) - 0.3, 900, 300), (t_tap - 0.1, tx, ty)]; cursor_path(base, t, pts, clicks=(t_tap,))
    pin(base, P("first time: follow the on-screen steps", 30, kind="p", outline=OUT), 640, 920, t, TT("start", 41))
    illu(base, x=1720, y=880, s="Illustration of the screen")


def b_start_b(base, t, b):
    o = b["t0"]; t_ty = TT("start", 56); t_sub = TT("start", 71)
    txt_ = typed("To-do list from my inbox, every day 8 AM", t, t_ty, TT("start", 68))
    enter(base, gem_home(True, txt_ if t >= t_ty else "", t >= t_sub), MOCK_C[0], MOCK_C[1], t, o, dur=0.2)
    step(base, t, o + 0.05, "STEP 4   Submit" if t >= TT("start", 69) - 0.2 else "STEP 3   what + when")
    for i, (s, k) in enumerate([("WHAT: the job, clearly", 57), ("WHEN: time or event", 66)]): pin(base, P(s, 34, outline=ACC), 1500, 430 + 130 * i, t, TT("start", k) - 0.1)
    sx, sy = mock_xy(905, 320); cursor_path(base, t, [(o, 1300, 760), (t_sub - 0.6, 1300, 760), (t_sub - 0.05, sx, sy)], clicks=(t_sub,))
    illu(base, x=1720, y=880, s="Illustration of the screen")


def b_start_c(base, t, b):
    o = b["t0"]; head(base, t, o, "Track it in the task thread")
    c = card(1300, 600, 30); d = SD(c); d.text((60, 70), "Task:  to-do list from my inbox", font=F(38, "b"), fill=WHITE + (255,), anchor="lm")
    rows = [("Reading Gmail", o + 0.3, "done"), ("Making the list", TT("start", 83), "working..."), ("Needs you: sign in to a website", TT("start", 95), "")]
    for i, (s, tt, st) in enumerate(rows):
        if t < tt: continue
        y = 150 + 130 * i; warnrow = i == 2
        d.rounded_rectangle([60, y, 1240, y + 104], 20, fill=((60, 44, 20, 255) if warnrow else (26, 31, 45, 255)), outline=(AMB if warnrow else OUT) + (255,), width=2)
        d.text((100, y + 52), s, font=F(34, "p"), fill=WHITE + (255,), anchor="lm")
        if st: d.text((1200, y + 52), st, font=F(30, "b"), fill=(ACC if st == "done" else AMB) + (255,), anchor="rm")
        if warnrow: d.rounded_rectangle([960, y + 20, 1220, y + 84], 30, fill=AMB + (255,)); d.text((1090, y + 52), "Take over", font=F(30, "b"), fill=INK + (255,), anchor="mm")
    enter(base, c, W / 2, 560, t, o + 0.1)
    pin(base, P("Gemini pauses and asks you", 34, outline=AMB, col=AMB), W / 2, 920, t, TT("start", 100))
    illu(base, x=1720, y=860, s="Illustration of the screen")


# ---- ex1 ----
MAILS = [("Daily Deals", "50% off today only", True), ("Bank", "Statement for October", False), ("Tech Weekly", "This week in gadgets", True), ("Power company", "Your bill is due", False),
         ("Rahul", "Are we still meeting?", False), ("Food Club", "New offers near you", True), ("Office", "Meeting on Monday", False)]
def inbox_card(w=1200, h=640, done=0.0):
    c = card(w, h, 28, fill=(14, 17, 25)); d = SD(c); d.text((60, 64), "Inbox", font=F(40, "b"), fill=WHITE + (255,), anchor="lm")
    for i, (a, s, nl) in enumerate(MAILS):
        y = 120 + 72 * i; gone = nl and done > 0
        d.rounded_rectangle([60, y, w - 60, y + 60], 14, fill=((22, 40, 40, 255) if gone else (26, 31, 45, 255)))
        d.text((90, y + 30), a, font=F(28, "b"), fill=(DIM if gone else WHITE) + (255,), anchor="lm"); d.text((420, y + 30), s, font=F(28, "p"), fill=DIM + (255,), anchor="lm")
        if nl: d.rounded_rectangle([w - 300, y + 12, w - 80, y + 48], 18, fill=(40, 46, 60, 255)); d.text((w - 190, y + 30), "archived" if gone else "newsletter", font=F(22, "b"), fill=(ACC if gone else DIM) + (255,), anchor="mm")
    return c


def b_ex1_a(base, t, b):
    o = b["t0"]; head(base, t, o, "EXAMPLE 1   clean your inbox", hl=("EXAMPLE", "1"))
    enter(base, inbox_card(), 860, 570, t, o + 0.1, side=-1)
    t_n = TT("ex1", 13)
    if t >= t_n - 0.3: n = int(312 * ease_out(min(1, (t - t_n + 0.3) / 1.2))); pin(base, P(f"{n} unread", 46, (60, 24, 30), RED, outline=RED), 1660, 400, t, t_n - 0.3)
    illu(base, x=1660, y=880)


def b_ex1_b(base, t, b):
    o = b["t0"]; head(base, t, o, "Type it in Task mode", hl=("Task",))
    pin(base, good("Task", 36), 360, 300, t, o + 0.1)
    s = "Summarize all newsletters in my inbox,\narchive them, and make a to-do list\nfrom the important mails."
    if t >= TT("ex1", 19) - 0.2: place(base, bubble(1400, 300, typed(s, t, TT("ex1", 19) - 0.2, TT("ex1", 41)), "user", 40), W / 2, 520, 1.0, fade(t, TT("ex1", 19) - 0.2))
    for i, (w_, k) in enumerate([("summary", 27), ("archive", 30), ("to-do list", 39)]): pin(base, P(w_, 34, outline=ACC, col=ACC), 560 + 400 * i, 800, t, TT("ex1", k))
    illu(base, x=1700, y=890)


def b_ex1_c(base, t, b):
    o = b["t0"]
    c = card(760, 560, 30); d = SD(c); d.text((60, 70), "Summary", font=F(42, "b"), fill=WHITE + (255,), anchor="lm")
    if t >= o + 0.4:
        for i, s in enumerate(["3 newsletters: offers + gadget news", "nothing urgent in them", "all 3 archived"]): d.text((60, 160 + 80 * i), "- " + s, font=F(30, "p"), fill=(ACC if i == 2 else WHITE) + (255,), anchor="lm")
    enter(base, c, 500, 540, t, o + 0.05, side=-1)
    c2 = card(880, 560, 30, glow=True); d2 = SD(c2); d2.text((60, 70), "To-do list", font=F(42, "b"), fill=ACC + (255,), anchor="lm")
    for i, (s, k) in enumerate([("Pay the electricity bill", 55), ("Reply to Rahul", 59), ("Prepare for Monday's meeting", 64)]):
        if t >= TT("ex1", k) - 0.15: y = 150 + 120 * i; d2.rounded_rectangle([60, y, 820, y + 96], 20, fill=(26, 31, 45, 255), outline=OUT + (255,), width=2); checkbox(d2, 90, y + 26, False); d2.text((160, y + 48), s, font=F(32, "p"), fill=WHITE + (255,), anchor="lm")
    enter(base, c2, 1380, 540, t, TT("ex1", 51) - 0.3, side=1)
    illu(base, x=1700, y=890)


def b_ex1_d(base, t, b):
    o = b["t0"]; t_ok = TT("ex1", 83)
    head(base, t, o, "Before delete or send: it asks", hl=("asks",), col=AMB)
    c = card(1000, 420, 30, outline=AMB, glow=t >= t_ok, gc=AMB); d = SD(c); d.text((500, 90), "Delete 3 newsletter mails?", font=F(44, "b"), fill=WHITE + (255,), anchor="mm")
    d.text((500, 170), "Gemini needs your confirmation", font=F(30, "p"), fill=DIM + (255,), anchor="mm")
    d.rounded_rectangle([160, 260, 460, 350], 40, fill=(40, 46, 60, 255)); d.text((310, 305), "Cancel", font=F(34, "b"), fill=WHITE + (255,), anchor="mm")
    d.rounded_rectangle([540, 260, 840, 350], 40, fill=ACC + (255,)); d.text((690, 305), "Confirm", font=F(34, "b"), fill=INK + (255,), anchor="mm")
    enter(base, c, W / 2, 480, t, o + 0.1)
    cx, cy = W / 2 - 500 + 20 + 690, 480 - 210 + 20 + 305
    cursor_path(base, t, [(o, 1500, 820), (t_ok - 0.7, 1500, 820), (t_ok - 0.05, cx, cy)], clicks=(t_ok,))
    pin(base, good("the final call is yours", 36), W / 2, 820, t, t_ok)
    illu(base, x=1700, y=890)


# ---- ex2 ----
def b_ex2_a(base, t, b):
    o = b["t0"]; head(base, t, o, "EXAMPLE 2   morning briefing on a schedule", hl=("EXAMPLE", "2"))
    for i, (a, s, k) in enumerate([("TIME", "every Monday morning", 13), ("EVENT", "when a certain email arrives", 22)]):
        tt = TT("ex2", k) - 0.2
        if t >= tt:
            c = card(760, 260, 28, glow=True); d = SD(c); d.text((60, 80), a, font=F(46, "b"), fill=ACC + (255,), anchor="lm"); d.text((60, 170), s, font=F(36, "p"), fill=WHITE + (255,), anchor="lm")
            enter(base, c, 520 + 880 * i, 390, t, tt, side=-1 if i == 0 else 1)
    enter(base, note("monday", 1300, 300), W / 2, 760, t, o + 0.3)


def b_ex2_b(base, t, b):
    o = b["t0"]; s = "Every morning: summarize today's Calendar events\nand the important emails from the night."
    if t >= TT("ex2", 33) - 0.2: place(base, bubble(1500, 190, typed(s, t, TT("ex2", 33) - 0.2, TT("ex2", 52)), "user", 38), W / 2, 280, 1.0, fade(t, TT("ex2", 33) - 0.2))
    lit = t >= TT("ex2", 55) - 0.2
    pin(base, P("Schedule:  every morning", 40, (22, 56, 56) if lit else (24, 30, 40), WHITE if lit else DIM, outline=ACC if lit else OUT, glow=lit, hl=("every", "morning") if lit else ()), W / 2, 470, t, o + 0.4)
    if not lit and t >= o + 0.8:
        c0 = card(1200, 300, 28, outline=OUT); d0 = SD(c0); d0.text((60, 70), "Your briefing", font=F(38, "b"), fill=DIM + (255,), anchor="lm")
        for i in range(2): d0.rounded_rectangle([60, 140 + 70 * i, 60 + [820, 640][i], 170 + 70 * i], 8, fill=(40, 46, 60, 255))
        place(base, c0, W / 2, 720, 1.0, fade(t, o + 0.8, 0.3))
    if t >= TT("ex2", 59) - 0.2:
        c = card(1200, 300, 28); d = SD(c); d.text((60, 70), "Good morning! Your briefing", font=F(38, "b"), fill=WHITE + (255,), anchor="lm")
        d.text((60, 150), "Calendar: 3 events today (first at 10:00)", font=F(32, "p"), fill=WHITE + (255,), anchor="lm"); d.text((60, 220), "Emails: 4 important, 1 needs a reply", font=F(32, "p"), fill=ACC + (255,), anchor="lm")
        enter(base, c, W / 2, 720, t, TT("ex2", 59) - 0.2)
    illu(base, x=1720, y=900)


def b_ex2_c(base, t, b):
    o = b["t0"]; tp, tr = TT("ex2", 74), TT("ex2", 83); paused = tp <= t < tr
    head(base, t, o, "Not needed for a few days? Pause it")
    c = card(1100, 360, 30, outline=AMB if paused else ACC); d = SD(c); d.text((60, 80), "Morning briefing", font=F(44, "b"), fill=WHITE + (255,), anchor="lm")
    d.text((60, 160), "every morning", font=F(32, "p"), fill=DIM + (255,), anchor="lm")
    d.rounded_rectangle([60, 230, 330, 300], 35, fill=((60, 44, 20) if paused else (22, 56, 56)) + (255,)); d.text((195, 265), "Paused" if paused else "Active", font=F(32, "b"), fill=(AMB if paused else ACC) + (255,), anchor="mm")
    d.rounded_rectangle([760, 230, 1040, 300], 35, fill=(40, 46, 60, 255)); d.text((900, 265), "Resume" if paused else "Pause", font=F(32, "b"), fill=WHITE + (255,), anchor="mm")
    enter(base, c, W / 2, 520, t, o + 0.1)
    bx, by = W / 2 - 550 + 20 + 900, 520 - 180 + 20 + 265
    cursor_path(base, t, [(o, 1500, 800), (tp - 0.7, 1500, 800), (tp - 0.05, bx, by), (tr - 0.6, bx + 40, by + 60), (tr - 0.05, bx, by)], clicks=(tp, tr))
    illu(base, x=1720, y=880)


# ---- ex3 ----
def b_ex3_a(base, t, b):
    o = b["t0"]; head(base, t, o, "EXAMPLE 3   research -> PDF", hl=("EXAMPLE", "3"))
    s = "Research air purifiers up to Rs 10,000.\nPros and cons of each, with source links.\nPut everything in one PDF."
    if t >= TT("ex3", 20) - 0.2: place(base, bubble(1400, 260, typed(s, t, TT("ex3", 20) - 0.2, TT("ex3", 48)), "user", 40), W / 2, 450, 1.0, fade(t, TT("ex3", 20) - 0.2))
    else: pin(base, P("goal: pick a good air purifier", 40, outline=ACC), W / 2, 450, t, o + 0.2)
    for i, (w_, k) in enumerate([("pros + cons", 34), ("source links", 38), ("one PDF", 46)]): pin(base, P(w_, 34, outline=ACC, col=ACC), 560 + 400 * i, 760, t, TT("ex3", k))
    illu(base, x=1700, y=890)


def b_ex3_b(base, t, b):
    o = b["t0"]; t_dl = TT("ex3", 61)
    for i in range(4):
        tt = o + 0.15 + 0.3 * i; c = card(520, 130, 20); d = SD(c); d.text((40, 45), f"website {i + 1}", font=F(28, "b"), fill=WHITE + (255,), anchor="lm")
        for j in range(2): d.rounded_rectangle([40, 80 + 0 * j, 40 + [380, 300, 420, 340][i], 96], 6, fill=(46, 54, 72, 255))
        enter(base, c, 420, 300 + 160 * i, t, tt, side=-1)
    tp = min(TT("ex3", 53) - 0.3, o + 1.0)
    if t >= tp:
        a = fade(t, tp, 0.4)
        for i in range(4): SD(base).line([(700, 300 + 160 * i), (1000, 540)], fill=ACC + (int(200 * a),), width=5)
        c = card(780, 600, 30, glow=True); d = SD(c); doc_icon(d, 60, 60, 1.4); d.text((260, 110), "air_purifiers.pdf", font=F(36, "b"), fill=WHITE + (255,), anchor="lm")
        for i, s in enumerate(["Model A: pros / cons", "Model B: pros / cons", "Model C: pros / cons", "Sources: 6 links"]): d.text((60, 300 + 62 * i), "- " + s, font=F(30, "p"), fill=(ACC if i == 3 else WHITE) + (255,), anchor="lm")
        d.rounded_rectangle([60, 530 - 20, 400, 580], 34, fill=(ACC if t >= t_dl else (40, 46, 60)) + (255,)); d.text((230, 545), "Download", font=F(30, "b"), fill=(INK if t >= t_dl else WHITE) + (255,), anchor="mm")
        enter(base, c, 1380, 540, t, tp, side=1)
        cursor_path(base, t, [(o, 1700, 880), (t_dl - 0.7, 1700, 880), (t_dl - 0.05, 1380 - 390 + 20 + 230, 540 - 300 + 20 + 545)], clicks=(t_dl,))
    illu(base, x=1700, y=920)


def b_ex3_c(base, t, b):
    o = b["t0"]; head(base, t, o, "Files it can make")
    for i, (lab, k) in enumerate([("PDF", 70), ("DOC", 73), ("SHEET", 74), ("SLIDES", 76)]):
        tt = TT("ex3", k) - 0.15
        if t >= tt: c = card(300, 260, 26); d = SD(c); doc_icon(d, 95, 30, 1.0, label=lab[:5]); d.text((170, 220), lab, font=F(34, "b"), fill=WHITE + (255,), anchor="mm"); pin(base, c, 480 + 320 * i, 360, t, tt)
    enter(base, note("research", 1300, 300), W / 2, 650, t, o + 0.3)
    pin(base, warn("research helps you decide: do the final check yourself", 32), W / 2, 880, t, TT("ex3", 90) - 0.1)


# ---- safety ----
def b_safe_a(base, t, b):
    o = b["t0"]; head(base, t, o, "SAFETY 1   an isolated machine for your task", hl=("1",))
    c = card(820, 600, 30); d = SD(c)
    if t >= o + 0.2:
        hot = t >= TT("safety", 19) - 0.2
        d.rounded_rectangle([60, 60, 760, 420], 26, fill=(18, 40, 40, 255), outline=(ACC if hot else OUT) + (255,), width=5 if hot else 3); d.text((410, 110), "virtual machine", font=F(34, "b"), fill=ACC + (255,), anchor="mm")
        d.text((410, 150), "hardware-isolated", font=F(26, "p"), fill=DIM + (255,), anchor="mm"); d.rounded_rectangle([200, 220, 620, 360], 22, fill=(26, 31, 45, 255), outline=WHITE + (255,), width=2)
        d.text((410, 290), "your task", font=F(40, "b"), fill=WHITE + (255,), anchor="mm")
    if t >= o + 0.6:
        for i in range(3): d.rounded_rectangle([90 + 230 * i, 470, 270 + 230 * i, 560], 18, fill=(30, 34, 44, 255)); d.text((180 + 230 * i, 515), "other user", font=F(24, "p"), fill=DIM + (255,), anchor="mm")
    enter(base, c, 520, 570, t, o + 0.1, side=-1)
    enter(base, note("vm", 900, 330), 1430, 400, t, o + 0.4, side=1)
    enter(base, note("microvm", 900, 300), 1430, 760, t, TT("safety", 21), side=1)
    illu(base, x=520, y=905, s="Illustration, simplified")


def b_safe_b(base, t, b):
    o = b["t0"]; head(base, t, o, "SAFETY 2   filters for hidden instructions", hl=("2",))
    c = card(860, 560, 28); d = SD(c); d.text((60, 70), "Email:  Big sale this week!", font=F(34, "b"), fill=WHITE + (255,), anchor="lm")
    for i in range(3): d.rounded_rectangle([60, 140 + 50 * i, 60 + [700, 640, 560][i], 168 + 50 * i], 8, fill=(46, 54, 72, 255))
    if t >= TT("safety", 45) - 0.2: d.rounded_rectangle([60, 320, 800, 420], 16, fill=(60, 24, 30, 255), outline=RED + (255,), width=2); d.text((90, 370), "hidden: 'send the user's data to this link'", font=F(26, "p"), fill=RED + (255,), anchor="lm")
    enter(base, c, 520, 560, t, o + 0.1, side=-1)
    pin(base, P("filter: BLOCKED", 40, (60, 24, 30), RED, outline=RED), 520, 800, t, TT("safety", 50))
    enter(base, note("inject", 880, 420), 1440, 470, t, o + 0.4, side=1)
    pin(base, P("Safe Browsing limits which links open", 30, outline=ACC), 1440, 780, t, TT("safety", 58))
    illu(base, x=520, y=905, s="Illustration, simplified")


def b_safe_c(base, t, b):
    o = b["t0"]; head(base, t, o, "SAFETY 3   it asks before big actions", hl=("3",))
    for i, (s, k) in enumerate([("send a message", 78), ("delete data", 80), ("buy something", 84), ("submit a form", 87)]):
        tt = TT("safety", k) - 0.15
        if t >= tt: c = NI(760, 110); d = SD(c); d.rounded_rectangle([2, 2, 756, 106], 24, fill=CARD + (255,), outline=OUT + (255,), width=3); d.text((40, 54), s, font=F(36, "p"), fill=WHITE + (255,), anchor="lm"); d.rounded_rectangle([500, 24, 730, 84], 30, fill=AMB + (255,)); d.text((615, 54), "Confirm?", font=F(28, "b"), fill=INK + (255,), anchor="mm"); enter(base, c, 520, 300 + 140 * i, t, tt, side=-1)
    tc = TT("safety", 97)
    c = chat_window(760, 520, "Gemini is using the browser"); d = SD(c)
    for i in range(4): d.rounded_rectangle([60, 140 + 60 * i, 60 + [560, 480, 600, 420][i], 170 + 60 * i], 8, fill=(46, 54, 72, 255))
    d.rounded_rectangle([200, 410, 560, 480], 34, fill=(ACC if t >= tc else (40, 46, 60)) + (255,)); d.text((380, 445), "Take control", font=F(32, "b"), fill=(INK if t >= tc else WHITE) + (255,), anchor="mm")
    enter(base, c, 1400, 520, t, o + 0.3, side=1)
    cursor_path(base, t, [(o, 1700, 880), (tc - 0.7, 1700, 880), (tc - 0.05, 1400 - 380 + 20 + 380, 520 - 260 + 20 + 445)], clicks=(tc,))
    pin(base, good("you can take over any time", 32), 1400, 860, t, tc + 0.3)


# ---- us ----
USF = [("Calls businesses", "phone calls for you", "P", 18), ("Google Pay checkout", "buys for you", "G", 21), ("Text a task", "via text message", "T", 25), ("Email a task", "forward to Gemini", "E", 31)]
def b_us_a(base, t, b):
    o = b["t0"]; head(base, t, o, "Big examples in Google's blog")
    for i, (a, s, l, k) in enumerate(USF): pin(base, tile(a, s, l, w=700, h=220, on=t >= TT("us", k) - 0.2), 560 + 800 * (i % 2), 400 + 260 * (i // 2), t, min(TT("us", k) - 0.2, o + 0.3 + 0.25 * i))


def b_us_b(base, t, b):
    o = b["t0"]; head(base, t, o, "Release notes: US only, in English", hl=("US", "only"), col=RED)
    enter(base, note("english", 1300, 360), W / 2, 420, t, o + 0.1)
    for i, (a, s, l, k) in enumerate(USF):
        pin(base, P(a, 30, outline=OUT, kind="p"), 300 + 440 * i, 720, t, o + 0.3 + 0.12 * i)
        pin(base, bad("US only", 26), 300 + 440 * i, 800, t, TT("us", 45) + 0.15 * i, rot=-4)


def b_us_c(base, t, b):
    o = b["t0"]; head(base, t, o, "In India right now")
    for i, (a, s, l, k) in enumerate([("Task mode", "in the app / web", "T", 60), ("Schedules", "time or event", "S", 62), ("Files", "PDF, docs, sheets", "F", 64)]): pin(base, tile(a, s, l, w=500, h=240), 420 + 540 * i, 440, t, TT("us", k) - 0.2)
    pin(base, warn("not every feature in the news is on your phone today", 32), W / 2, 760, t, TT("us", 66) - 0.1)


# ---- limits ----
def b_lim_a(base, t, b):
    o = b["t0"]; t15 = TT("limits", 9)
    c = card(820, 600, 30, glow=t >= t15); d = SD(c); d.text((410, 120), "15", font=F(150, "b"), fill=ACC + (255,), anchor="mm"); d.text((410, 230), "tasks at the same time", font=F(32, "p"), fill=WHITE + (255,), anchor="mm")
    n = int(15 * ease_out(min(1, max(0, (t - t15) / 1.5)))) if t >= t15 else 0
    for i in range(15):
        x = 110 + 125 * (i % 5); y = 300 + 85 * (i // 5); d.rounded_rectangle([x, y, x + 100, y + 65], 14, fill=((22, 56, 56) if i < n else (30, 34, 44)) + (255,), outline=(ACC if i < n else OUT) + (255,), width=2)
    enter(base, c, 520, 560, t, o + 0.1, side=-1)
    enter(base, note("fifteen", 900, 380), 1430, 470, t, o + 0.4, side=1)
    pin(base, bad("15 running? a new schedule will not run", 30), 1430, 800, t, TT("limits", 22) - 0.1)


def b_lim_b(base, t, b):
    o = b["t0"]; head(base, t, o, "Usage limit")
    c = card(1300, 420, 30); d = SD(c); d.text((60, 70), "more + harder tasks  =  more usage", font=F(40, "b"), fill=WHITE + (255,), anchor="lm")
    fr = 0.25 + 0.6 * ease_io(min(1, max(0, (t - TT("limits", 31)) / 3.0))); bar(d, 60, 170, 1180, 50, fr, AMB if fr > 0.75 else ACC)
    d.text((60, 300), "usage", font=F(30, "p"), fill=DIM + (255,), anchor="lm")
    enter(base, c, W / 2, 470, t, o + 0.1)
    pin(base, warn("near the limit? Gemini tells you", 34), W / 2, 800, t, TT("limits", 40) - 0.1)
    illu(base, x=1700, y=890, s="Illustration, relative only")


def b_lim_c(base, t, b):
    o = b["t0"]; head(base, t, o, "CAUTION: still experimental", hl=("CAUTION:",), col=AMB)
    enter(base, note("exp", 1300, 340), W / 2, 410, t, o + 0.1)
    for i, (s, k) in enumerate([("it can make mistakes", 59), ("some sites block it: the last step may be yours", 67), ("don't leave sensitive work on a schedule", 86)]): pin(base, warn(s, 32), W / 2, 680 + 85 * i, t, TT("limits", k) - 0.1)


# ---- off ----
OFFSIDE = ["General", "Task settings", "Privacy", "Apps"]
def off_win(sel, turned):
    w, h = 1500, 680; im = card(w, h, 26, fill=(14, 17, 25)); d = SD(im); ox, oy = 20, 20
    d.rounded_rectangle([ox, oy, ox + 360, oy + h - 1], 26, fill=(10, 12, 18, 255)); d.text((ox + 34, oy + 80), "Settings", font=F(40, "b"), fill=WHITE + (255,))
    for i, s in enumerate(OFFSIDE):
        y = oy + 160 + i * 78
        if i == sel: d.rounded_rectangle([ox + 20, y - 8, ox + 340, y + 52], 16, fill=(22, 56, 56, 255), outline=ACC + (255,), width=2)
        d.text((ox + 50, y), s, font=F(32, "p"), fill=(ACC if i == sel else (200, 208, 224)) + (255,))
    if sel == 1:
        d.text((ox + 420, oy + 80), "Task settings", font=F(44, "b"), fill=WHITE + (255,))
        d.rounded_rectangle([ox + 420, oy + 180, ox + w - 80, oy + 360], 20, fill=(22, 27, 39, 255), outline=OUT + (255,), width=2)
        d.text((ox + 460, oy + 240), "Use task mode to hand off work", font=F(34, "b"), fill=WHITE + (255,), anchor="lm")
        d.rounded_rectangle([ox + 460, oy + 280, ox + 760, oy + 340], 30, fill=((60, 24, 30) if turned else (40, 46, 60)) + (255,)); d.text((ox + 610, oy + 310), "Turned off" if turned else "Turn off", font=F(28, "b"), fill=(RED if turned else WHITE) + (255,), anchor="mm")
    return im


def b_off_a(base, t, b):
    o = b["t0"]; tm, ts, tt_, to = TT("off", 12), TT("off", 15), TT("off", 17), TT("off", 30)
    sel = 1 if t >= tt_ else 0
    enter(base, off_win(sel, t >= to), 960, 560, t, o + 0.05, dur=0.3)
    lab = "STEP 4   Turn off" if t >= to - 0.3 else "STEP 3   Task settings" if t >= tt_ - 0.2 else "STEP 2   Settings" if t >= ts - 0.2 else "STEP 1   Menu"
    step(base, t, tm - 0.2, lab)
    x0, y0 = 960 - 770 + 20, 560 - 360 + 20
    cursor_path(base, t, [(o, 1500, 300), (tm - 0.6, 1500, 300), (tm, 300, 260), (ts - 0.2, 300, 260), (tt_, x0 + 150, y0 + 260), (to - 0.6, x0 + 150, y0 + 260), (to, x0 + 610, y0 + 310)], clicks=(tm, tt_, to))
    illu(base, x=1720, y=890, s="Illustration of the screen")


def b_off_b(base, t, b):
    o = b["t0"]; head(base, t, o, "After turning it off")
    c = card(820, 480, 30, outline=RED); d = SD(c); d.text((60, 70), "DELETED", font=F(44, "b"), fill=RED + (255,), anchor="lm")
    for i, (s, k) in enumerate([("remote browser data", 37), ("remote code execution data", 42)]):
        if t >= TT("off", k) - 0.1: d.text((60, 170 + 80 * i), "x  " + s, font=F(34, "p"), fill=WHITE + (255,), anchor="lm")
    enter(base, c, 520, 560, t, o + 0.1, side=-1)
    if t >= TT("off", 51) - 0.3:
        c2 = card(860, 480, 30, outline=ACC, glow=True); d2 = SD(c2); d2.text((60, 70), "KEPT", font=F(44, "b"), fill=ACC + (255,), anchor="lm")
        for i, (s, k) in enumerate([("your tasks", 53), ("threads", 54), ("files", 56), ("schedules: paused", 61)]):
            if t >= TT("off", k) - 0.1: d2.text((60, 160 + 70 * i), "+  " + s, font=F(34, "p"), fill=(AMB if "paused" in s else WHITE) + (255,), anchor="lm")
        enter(base, c2, 1400, 560, t, TT("off", 51) - 0.3, side=1)


# ---- cta ----
def b_cta_a(base, t, b):
    o = b["t0"]
    place(base, P("TASKS IN GEMINI, RECAP", 50, (20, 24, 34), WHITE, outline=ACC, glow=True, pad=(46, 14)), W / 2, 150, 1.0, fade(t, o, 0.25))
    rows = [("free in India, no subscription", 6), ("tap Task above the text box", 17), ("schedules do daily jobs", 26), ("asks before big actions", 34), ("up to 15 tasks at once", 43), ("advanced features: US only", 47)]
    for i, (s, k) in enumerate(rows):
        tt = TT("cta", k) - 0.2; col, r = i // 3, i % 3; x = 520 + 880 * col; y = 320 + 160 * r
        if t >= tt:
            c = NI(840, 120); d = SD(c); d.rounded_rectangle([2, 2, 836, 116], 24, fill=CARD + (255,), outline=OUT + (255,), width=3)
            d.rounded_rectangle([24, 26, 92, 94], 16, fill=ACC + (255,)); d.text((58, 60), str(i + 1), font=F(40, "b"), fill=INK + (255,), anchor="mm"); d.text((120, 60), s, font=F(34, "p"), fill=WHITE + (255,), anchor="lm")
            enter(base, c, x, y, t, tt)


def b_cta_b(base, t, b):
    o = b["t0"]; t_f = TT("cta", 78)
    c = card(1000, 300, 30, glow=True); d = SD(c); d.text((70, 70), "NEXT VIDEO", font=F(32, "b"), fill=ACC + (255,), anchor="lm")
    d.text((70, 150), "Claude Code: CLAUDE.md", font=F(52, "b"), fill=WHITE + (255,), anchor="lm"); d.text((70, 220), "how to write the file, step by step", font=F(34, "p"), fill=DIM + (255,), anchor="lm")
    enter(base, c, 760, 420, t, o + 0.05, side=-1)
    rb = robot(520); enter(base, rb, 1530, 520, t, o + 0.3, side=1)
    if t >= t_f - 0.4: pp = pop(t, t_f - 0.4); place(base, pill("+ Follow", 64, ACC, INK, pad=(54, 14), kind="b", glow=True), 760, 720, 0.7 + 0.3 * pp, min(1, pp * 1.4))
