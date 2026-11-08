# ---------- Claude Code 03 (.claude directory): theme MINT on dark neon; scenes ----------
KB = {"hook_a": 1.0, "hook_b": 1.2, "what_a": 1.12, "what_b": 1.12, "two_a": 1.2, "demo": 1.08, "choose": 1.2, "extras": 1.12, "mine_a": 1.1, "mine_b": 1.25,
      "data_a": 1.05, "data_b": 1.1, "purge_a": 1.15, "purge_b": 1.25, "cta_a": 1.3, "cta_b": 1.0}
CHAP = {"hook": None, "what": (1, "two places"), "two": (2, "two key files"), "demo": (3, "terminal demo"), "choose": (4, "which file"), "extras": (5, "optional extras"),
        "mine": (6, "private + org"), "data": (7, "app data"), "purge": (8, "clean up"), "cta": (9, "recap")}
KEYW = {w.strip(",.?!:।") for w in ["Claude", "Code", ".claude", "CLAUDE.md", "settings.json", "settings.local.json", ".mcp.json", "CLAUDE.local.md", "AGENTS.md", "tests", "transcripts",
                                    "plain", "text", "encrypted", "purge", "dry-run", "delete", "folder", "files", "skills", "agents", "rules", "output-styles", "team", "home", "सिर्फ", "कभी", "मत",
                                    "तीस", "cleanupPeriodDays", "hooks", "permissions", "DIRECTORY", "secrets", "managed"]}
MONO = "t"
GREEN = (110, 230, 150)


def bubble(w, h, text, side="user", size=34):
    im = NI(w + 8, h + 8); d = SD(im)
    d.rounded_rectangle([4, 4, w + 3, h + 3], 26, fill=((30, 60, 56, 255) if side == "user" else (26, 31, 45, 255)), outline=(SKY if side == "user" else OUT) + (255,), width=2)
    d.text((34, h // 2 + 4), text, font=F(size, "p"), fill=WHITE + (255,), anchor="lm"); return im


def termwin(w, h, title="Terminal"):
    im = card(w, h, 26, fill=(9, 12, 18), outline=OUT, ow=3); d = SD(im); ox, oy = 20, 20
    d.rounded_rectangle([ox, oy, ox + w - 1, oy + 64], 26, fill=(20, 25, 36, 255)); d.rectangle([ox, oy + 40, ox + w - 1, oy + 64], fill=(20, 25, 36, 255))
    for i, c in enumerate((RED, AMB, (120, 220, 140))): d.ellipse([ox + 28 + 34 * i, oy + 22, ox + 46 + 34 * i, oy + 40], fill=c + (255,))
    d.text((ox + w / 2, oy + 32), title, font=F(26, "p"), fill=DIM + (255,), anchor="mm")
    return im, d, ox, oy


def tl(d, x, y, s, fill=(214, 222, 238), size=30): d.text((x, y), s, font=F(size, MONO), fill=fill + (255,))


def prompt_line(d, x, y, cmd, t, a0, a1, path="my-project"):
    tl(d, x, y, path + " $ ", GREEN); w0 = len(path + " $ ") * 18.0
    s = typed(cmd, t, a0, a1)
    if t >= a0: tl(d, x + w0, y, s, WHITE)
    elif int(t * 3) % 2 == 0: tl(d, x + w0, y, "|", WHITE)


def key_flash(base, t, t0, x, y, s="Enter"):
    if 0 <= t - t0 <= 0.7: place(base, pill(s, 26, (36, 44, 62), SKY, pad=(18, 5), kind="b", outline=SKY), x, y, 1.0, min(1, (0.7 - (t - t0)) * 4))


def fcard(name, sub, col=SKY, w=520, h=190, size=40):
    spr = card(w, h, 26, outline=col); d = SD(spr); d.text((40, 36), name, font=F(size, MONO), fill=col + (255,)); d.text((40, 36 + size + 26), sub, font=F(34, "p"), fill=(214, 222, 238, 255))
    return spr


# ---------- hook ----------
def b_hook_a(base, t, b):
    o = b["t0"]; lt = t - o
    enter(base, photo("hook", 700, 480, lt, b["t1"] - o + 4), 470, 520, t, o + 0.02, side=-1)
    im, d, ox, oy = termwin(860, 480, "Claude Code"); enter(base, im, 1400, 520, t, o + 0.2, side=1)
    tl(d, ox + 30, oy + 100, "> ", GREEN); t_a = T("hook", 3); t_b = T("hook", 11)
    tl(d, ox + 66, oy + 100, typed("Always run tests first", t, o + 0.5, t_b), WHITE, 28)
    if t >= T("hook", 12): tl(d, ox + 30, oy + 160, "Got it.", SKY, 28)
    if t >= T("hook", 12) + 0.3: pass
    t_n = T("hook", 13)
    if t >= t_n:
        d.line([(ox + 30, oy + 235), (ox + 830, oy + 235)], fill=OUT + (255,), width=2); tl(d, ox + 30, oy + 255, "-- next session --", DIM, 24)
    if t >= T("hook", 16): tl(d, ox + 30, oy + 320, "How do I run the tests?", AMB, 28)
    # redraw sprite content: window was already placed, so re-place with content when it changes
    base2 = None


def _hook_term(t, o):
    im, d, ox, oy = termwin(880, 600, "Claude Code")
    tl(d, ox + 30, oy + 110, "> ", GREEN); t_b = T("hook", 11)
    tl(d, ox + 70, oy + 110, typed("Always run tests first", t, o + 0.5, t_b), WHITE, 32)
    if t >= T("hook", 12): tl(d, ox + 30, oy + 190, "Got it.", SKY, 32)
    if t >= T("hook", 13): d.line([(ox + 30, oy + 290), (ox + 850, oy + 290)], fill=OUT + (255,), width=2); tl(d, ox + 30, oy + 320, "-- next session --", DIM, 26)
    if t >= T("hook", 16): tl(d, ox + 30, oy + 410, "How do I run the tests?", AMB, 32)
    return im


def b_hook_a(base, t, b):  # noqa: F811
    o = b["t0"]; lt = t - o
    enter(base, photo("hook", 780, 600, lt, b["t1"] - o + 4), 450, 560, t, o + 0.02, side=-1)
    enter(base, _hook_term(t, o), 1410, 560, t, o + 0.2, side=1)
    place(base, pill("Claude Code forgets?", 36, (30, 44, 62), WHITE, pad=(30, 10), kind="b", outline=SKY, hl=("forgets?",)), 960, 190, 1.0, fade(t, o + 0.1, 0.3))


def b_hook_b(base, t, b):
    o = b["t0"]
    place(base, pill(".claude", 120, (20, 24, 34), SKY, pad=(70, 24), outline=SKY, kind=MONO if False else "b", glow=True), W / 2, 400, 0.85 + 0.15 * pop(t, o), min(1, fade(t, o, 0.2)))
    for i, (s, tt) in enumerate([("which files", T("hook", 39)), ("what to change", T("hook", 44)), ("what to watch out for", T("hook", 51))]):
        x = (420, 960, 1500)[i]
        if t >= tt: pp = pop(t, tt); place(base, pill(s, 36, (20, 24, 34), WHITE, pad=(30, 10), outline=OUT, kind="b"), x, 640, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t < T("hook", 39): place(base, pill("the folder where Claude Code keeps its rules", 34, (30, 44, 62), WHITE, pad=(30, 10), kind="p", outline=OUT), 960, 640, 1.0, fade(t, o + 0.3))


# ---------- what: two places ----------
TREE_P = [("my-project/", 0, WHITE), ("CLAUDE.md", 1, SKY), (".claude/", 1, WHITE), ("settings.json", 2, SKY), ("skills/", 2, (200, 208, 224)), ("agents/", 2, (200, 208, 224)), ("rules/", 2, (200, 208, 224))]
TREE_H = [("home folder/", 0, WHITE), (".claude/", 1, WHITE), ("settings.json", 2, SKY), ("skills/", 2, (200, 208, 224)), ("agents/", 2, (200, 208, 224)), ("projects/", 2, (200, 208, 224))]


def tree_card(w, h, tree, t, t0, times, col):
    im, d, ox, oy = termwin(w, h, "files")
    for i, ((s, lv, c), tt) in enumerate(zip(tree, times)):
        if t >= tt:
            a = fade(t, tt, 0.2); y = oy + 100 + i * 56; x = ox + 40 + lv * 46
            tl(d, x, y, ("+- " if lv else "") + s, tuple(int(v * a) for v in c), 32)
    return im


def b_what_a(base, t, b):
    o = b["t0"]; lt = t - o
    place(base, pill("1   THIS PROJECT", 38, SKY, INK, pad=(32, 10), kind="b"), 500, 205, 1.0, fade(t, o, 0.25))
    enter(base, photo("team", 700, 460, lt, b["t1"] - o + 4), 500, 490, t, o + 0.05, side=-1)
    tt = [T("what", 17), T("what", 19), T("what", 19) + 0.3, T("what", 19) + 0.6, T("what", 19) + 0.9, T("what", 19) + 1.2, T("what", 19) + 1.5]
    enter(base, tree_card(640, 560, TREE_P, t, o, tt, SKY), 1400, 530, t, o + 0.15, side=1)
    if t >= T("what", 23): pp = pop(t, T("what", 23)); place(base, pill("git commit  >  whole team gets it", 32, (30, 44, 62), WHITE, pad=(28, 10), kind="b", outline=SKY, hl=("team",)), 560, 790, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t >= T("what", 14) - 0.2 and t < T("what", 23): place(base, pill("pehli jagah: project ka .claude", 30, (20, 24, 34), DIM, pad=(24, 8), kind="p", outline=OUT), 560, 790, 1.0, fade(t, T("what", 14) - 0.2))


def b_what_b(base, t, b):
    o = b["t0"]; lt = t - o
    place(base, pill("2   YOUR HOME FOLDER", 38, AMB, INK, pad=(32, 10), kind="b"), 500, 205, 1.0, fade(t, o, 0.25))
    enter(base, photo("home", 700, 460, lt, b["t1"] - o + 4), 500, 490, t, o + 0.05, side=-1)
    tt = [T("what", 38), T("what", 41), T("what", 41) + 0.3, T("what", 41) + 0.6, T("what", 41) + 0.9, T("what", 41) + 1.2]
    enter(base, tree_card(640, 560, TREE_H, t, o, tt, AMB), 1400, 530, t, o + 0.15, side=1)
    if t >= T("what", 43): pp = pop(t, T("what", 43)); place(base, pill("personal  -  all your projects", 32, (30, 44, 62), WHITE, pad=(28, 10), kind="b", outline=AMB), 560, 790, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t >= T("what", 55): pp = pop(t, T("what", 55)); place(base, pill("Windows:  %USERPROFILE%\\.claude", 30, (20, 24, 34), WHITE, pad=(26, 9), kind="p", outline=SKY), 1400, 850, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# ---------- two key files ----------
def b_two_a(base, t, b):
    o = b["t0"]
    place(base, pill("Most people edit only 2 files", 44, (30, 44, 62), WHITE, pad=(36, 12), kind="b", outline=SKY, hl=("2",)), W / 2, 200, 1.0, fade(t, o, 0.3))
    for (name, lines, ta, x, col, tl_) in [("CLAUDE.md", ["instructions for Claude", "loaded every session"], 0.6, 520, SKY, T("two", 17)),
                                           ("settings.json", ["permissions  -  hooks", "env variables  -  model"], 0.9, 1400, AMB, T("two", 31))]:
        enter(base, fcard(name, "", col, 600, 360, 50), x, 520, t, o + ta - 0.3, side=0)
        spr = NI(600, 360); d = SD(spr)
        for j, s in enumerate(lines):
            if t >= tl_ + 0.5 * j: a = fade(t, tl_ + 0.5 * j); d.rounded_rectangle([40, 130 + 90 * j, 560, 130 + 90 * j + 70], 16, fill=(26, 32, 46, int(255 * a)), outline=col + (int(255 * a),), width=2); d.text((300, 165 + 90 * j), s, font=F(30, "p"), fill=WHITE + (int(255 * a),), anchor="mm")
        enter(base, spr, x, 520, t, o + ta - 0.3)
    if False: place(base, pill("1   CLAUDE.md      2   settings.json", 40, (20, 24, 34), DIM, pad=(34, 12), kind="p", outline=OUT), W / 2, 520, 1.0, fade(t, o + 0.2))
    if t >= T("two", 41): pp = pop(t, T("two", 41)); place(base, pill("the rest is optional", 40, SKY, INK, pad=(34, 10), kind="b"), W / 2, 820, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# ---------- terminal demo ----------
def b_demo(base, t, b):
    o = b["t0"]; sid = "demo"
    t_p1 = T(sid, 5); t_p2 = T(sid, 20); t_p3 = T(sid, 35)
    page = 3 if t >= t_p3 else (2 if t >= t_p2 else 1)
    title = "CLAUDE.md" if page == 3 else "Terminal"
    im, d, ox, oy = termwin(1560, 700, title); x0, y0 = ox + 50, oy + 110; lh = 52
    if page == 1:
        a0, a1 = T(sid, 8), T(sid, 10) + 0.4
        prompt_line(d, x0, y0, "ls .claude", t, a0, a1)
        names = [("settings.json", T(sid, 12)), ("settings.local.json", T(sid, 12) + 0.25), ("rules/", T(sid, 13)), ("skills/", T(sid, 14)), ("agents/", T(sid, 16)), ("CLAUDE.md", T(sid, 16) + 0.3)]
        for i, (s, tt) in enumerate(names):
            if t >= tt:
                a = fade(t, tt, 0.2); col = SKY if s in ("settings.json", "CLAUDE.md") else (214, 222, 238); tl(d, x0 + (i % 2) * 520, y0 + lh * 1.6 + (i // 2) * lh, s, tuple(int(c * a) for c in col), 34)
        st = "STEP 1   list the folder:  ls .claude"
    elif page == 2:
        a0, a1 = T(sid, 21), T(sid, 22) + 0.5
        prompt_line(d, x0, y0, "cat .claude/settings.json", t, a0, a1)
        js = [(T(sid, 24), '{', WHITE), (T(sid, 25), '  "permissions": {', WHITE), (T(sid, 28), '    "allow": [', WHITE), (T(sid, 30), '      "Bash(npm test)"', SKY), (T(sid, 33), '    ]', WHITE), (T(sid, 33) + 0.2, '  }', WHITE), (T(sid, 33) + 0.4, '}', WHITE)]
        for i, (tt, s, c) in enumerate(js):
            if t >= tt: tl(d, x0, y0 + lh * 1.5 + i * 46, s, c, 32)
        st = "STEP 2   open settings.json  >  permissions"
    else:
        tl(d, x0, y0 - 6, "CLAUDE.md", SKY, 30); d.line([(x0, y0 + 40), (x0 + 1000, y0 + 40)], fill=OUT + (255,), width=2)
        if t >= T(sid, 36): tl(d, x0, y0 + 70, "# My project", (214, 222, 238), 34)
        a0, a1 = T(sid, 40), T(sid, 48)
        if t >= a0: tl(d, x0, y0 + 70 + lh * 1.3, typed("Run tests with:  npm test", t, a0, a1), WHITE, 34)
        st = "STEP 3   write it in plain words in CLAUDE.md"
    enter(base, im, 960, 565, t, o, dur=0.3)
    step(base, t, t_p1 - 0.3, st)
    if page == 1: key_flash(base, t, T(sid, 10) + 0.5, 1560, 880)
    if page == 2: key_flash(base, t, T(sid, 22) + 0.6, 1560, 880)
    if t >= T(sid, 51): pp = pop(t, T(sid, 51)); place(base, pill("next session: Claude reads it", 34, SKY, INK, pad=(30, 10), kind="b"), 960, 800, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if page == 2 and t >= T(sid, 30): place(base, pill("example", 24, (20, 24, 34), AMB, pad=(16, 4), kind="p", outline=AMB), 1590, 300)
    illu(base)


# ---------- choose the file ----------
ROWS = [("Project context + rules", "CLAUDE.md", SKY, 9, 19), ("Allow / block tools, hooks, env", "settings.json", AMB, 20, 36), ("Share MCP servers with the team", ".mcp.json", GREEN, 37, 46), ("Personal overrides, out of git", "settings.local.json", (255, 130, 200), 47, 57)]


def b_choose(base, t, b):
    o = b["t0"]; sid = "choose"
    place(base, pill("What do you want to do?   >   which file?", 40, (30, 44, 62), WHITE, pad=(36, 12), kind="b", outline=OUT), W / 2, 210, 1.0, fade(t, o, 0.3))
    for i, (s, fn, col, ta, tb) in enumerate(ROWS):
        y = 340 + 150 * i; tt = T(sid, ta); act = (t >= tt and (i == 3 or t < T(sid, ROWS[i + 1][3])))
        enter(base, card(1500, 110, 26, outline=col if t >= tt else OUT, glow=act), 960, y, t, o + 0.1 + 0.12 * i, side=0)
        spr = NI(1500, 110); d = SD(spr); d.text((50, 55), s, font=F(38, "p"), fill=(WHITE if t >= tt - 0.2 else DIM) + (255,), anchor="lm")
        enter(base, spr, 960, y, t, o + 0.1 + 0.12 * i)
        tf = T(sid, tb)
        if t >= tf - 0.1: pp = pop(t, tf - 0.1); place(base, pill(fn, 38, col, INK, pad=(28, 8), kind=MONO), 1330, y, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# ---------- extras ----------
EX = [("skills/", "SKILL.md  >  run with /name", 6, SKY), ("agents/", "subagent: own prompt + tools", 24, AMB), ("rules/", "topic rules, can be path-gated", 39, GREEN), ("output-styles/", "changes how Claude answers", 60, (255, 130, 200))]


def b_extras(base, t, b):
    o = b["t0"]
    place(base, pill("optional extras", 44, (30, 44, 62), WHITE, pad=(36, 12), kind="b", outline=OUT), W / 2, 200, 1.0, fade(t, o, 0.3))
    for i, (name, sub, tk, col) in enumerate(EX):
        x = 560 + 800 * (i % 2); y = 440 + 330 * (i // 2); tt = T("extras", tk) - 0.3
        enter(base, fcard(name, sub, col, 640, 270, 46), x, y, t, tt, side=0)


# ---------- mine ----------
def b_mine_a(base, t, b):
    o = b["t0"]; lt = t - o
    enter(base, photo("home", 700, 470, lt, b["t1"] - o + 4), 470, 520, t, o + 0.02, side=-1)
    place(base, fcard("CLAUDE.local.md", "your private notes", AMB, 700, 190, 40), 1400, 360, 1.0, fade(t, T("mine", 5) - 0.3))
    for i, (s, tt) in enumerate([("you create it yourself", T("mine", 9)), ("add it to .gitignore", T("mine", 15))]):
        if t >= tt: pp = pop(t, tt); place(base, pill(s, 34, (30, 44, 62), WHITE, pad=(28, 10), kind="b", outline=AMB), 1400, 540 + 100 * i, 0.7 + 0.3 * pp, min(1, pp * 1.4))
    if t < T("mine", 5) - 0.3: place(base, pill("your own preferences", 40, (30, 44, 62), WHITE, pad=(32, 10), kind="b", outline=AMB), 1400, 360, 1.0, fade(t, o + 0.1))


def b_mine_b(base, t, b):
    o = b["t0"]
    place(base, fcard("AGENTS.md", "already in your repo?", SKY, 560, 190, 40), 560, 400, 1.0, fade(t, T("mine", 27) - 0.3))
    if t >= T("mine", 33) - 0.2: pp = pop(t, T("mine", 33) - 0.2); place(base, pill("=", 70, (20, 24, 34), WHITE, pad=(30, 4), kind="b"), 960, 400, 1.0, min(1, pp * 1.4)); place(base, fcard("CLAUDE.md", "can be read instead", SKY, 560, 190, 40), 1360, 400, 0.8 + 0.2 * pp, min(1, pp * 1.4))
    if t < T("mine", 27) - 0.3: place(base, pill("already have AGENTS.md?", 40, (30, 44, 62), WHITE, pad=(34, 12), kind="b", outline=SKY), 960, 400, 1.0, fade(t, o))
    tt = T("mine", 42)
    if t >= tt:
        pp = pop(t, tt); place(base, pill("ORGANIZATION  managed settings", 36, RED, INK, pad=(32, 10), kind="b"), 960, 620, 0.8 + 0.2 * pp, min(1, pp * 1.4))
        if t >= tt + 0.7: place(base, pill("your settings.json", 34, (30, 44, 62), WHITE, pad=(30, 10), kind=MONO, outline=OUT), 960, 740, 1.0, fade(t, tt + 0.7))
        if t >= tt + 0.7: SD(base).polygon([(930, 670), (990, 670), (960, 700)], fill=RED + (255,))
        if t >= T("mine", 49): place(base, pill("managed settings win", 34, (70, 28, 36), RED, pad=(28, 9), kind="p", outline=RED), 960, 815, 1.0, fade(t, T("mine", 49)))


# ---------- app data ----------
def b_data_a(base, t, b):
    o = b["t0"]; lt = t - o
    enter(base, photo("shield", 700, 440, lt, b["t1"] - o + 4), 470, 500, t, o + 0.02, side=-1)
    im, d, ox, oy = termwin(760, 440, "inside .claude")
    tl(d, ox + 40, oy + 100, "projects/", WHITE, 30)
    for i, (s, tt) in enumerate([("session.jsonl   transcript", T("data", 17)), ("history.jsonl   prompts", T("data", 19))]):
        if t >= tt: a = fade(t, tt, 0.2); tl(d, ox + 80, oy + 160 + 60 * i, s, tuple(int(c * a) for c in SKY), 28)
    enter(base, im, 1400, 500, t, o + 0.2, side=1)
    place(base, pill("Claude Code also WRITES data here", 36, (30, 44, 62), WHITE, pad=(30, 10), kind="b", outline=AMB, hl=("WRITES",), hlc=AMB), 960, 190, 1.0, fade(t, o, 0.3))
    if t >= T("data", 23): pp = pop(t, T("data", 23)); place(base, pill("PLAIN TEXT  -  not encrypted", 40, RED, INK, pad=(34, 10), kind="b"), 960, 790, 0.75 + 0.25 * pp, min(1, pp * 1.4))


def b_data_b(base, t, b):
    o = b["t0"]
    place(base, pill("a tool reads your .env file...", 38, (30, 44, 62), WHITE, pad=(32, 10), kind="b", outline=OUT), W / 2, 190, 1.0, fade(t, o, 0.3))
    ta = T("data", 34) - 0.3
    enter(base, fcard(".env", "API_KEY=sk-demo-1234", AMB, 560, 190, 44), 520, 420, t, o + 0.1, side=-1)
    if t >= T("data", 36): a = ease_out((t - T("data", 36)) / 0.5); SD(base).line([(820, 420), (820 + 240 * a, 420)], fill=RED + (255,), width=6); SD(base).polygon([(1060, 420), (1030, 402), (1030, 438)], fill=RED + (int(255 * a),))
    if t >= T("data", 38) - 0.2: enter(base, fcard("transcript", "API_KEY=sk-demo-1234", RED, 560, 190, 44), 1400, 420, t, T("data", 38) - 0.2, side=1)
    if t >= T("data", 41): pp = pop(t, T("data", 41)); place(base, pill("the value is saved in the transcript", 34, (70, 28, 36), RED, pad=(28, 10), kind="p", outline=RED), 960, 590, 0.8 + 0.2 * pp, min(1, pp * 1.4))
    tt = T("data", 50)
    if t >= tt - 0.3:
        enter(base, card(560, 220, 28, glow=True), 520, 790, t, tt - 0.3, side=0)
        spr = NI(560, 220); d = SD(spr); d.text((280, 85), "30", font=F(110, "b"), fill=SKY + (255,), anchor="mm"); d.text((280, 175), "days  -  auto delete (default)", font=F(28, "p"), fill=WHITE + (255,), anchor="mm"); enter(base, spr, 520, 790, t, tt - 0.3)
    if t >= T("data", 59): pp = pop(t, T("data", 59)); place(base, pill("change it:  cleanupPeriodDays", 34, (20, 24, 34), SKY, pad=(28, 10), kind=MONO, outline=SKY), 1360, 790, 0.7 + 0.3 * pp, min(1, pp * 1.4))


# ---------- purge ----------
def b_purge_a(base, t, b):
    o = b["t0"]; sid = "purge"
    im, d, ox, oy = termwin(1560, 640, "Terminal"); x0, y0 = ox + 40, oy + 100; lh = 44
    prompt_line(d, x0, y0, "claude purge ~/work/my-repo --dry-run", t, T(sid, 4), T(sid, 9), "~")
    L = [(T(sid, 13), "Purge plan for /home/user/work/my-repo:", WHITE), (T(sid, 19), "  dir:    projects/...  transcripts and memory/", SKY),
         (T(sid, 22), "  config: project entry in ~/.claude.json", SKY), (T(sid, 25), "  filter: history.jsonl  12 prompt(s)", SKY), (T(sid, 26) + 0.6, "Dry run: 3 item(s) would be deleted.", AMB)]
    for i, (tt, s, c) in enumerate(L):
        if t >= tt: tl(d, x0, y0 + 80 + i * lh * 1.25, s, c, 28)
    enter(base, im, 960, 560, t, o, dur=0.3)
    step(base, t, T(sid, 3), "STEP   claude purge <project> --dry-run  =  only a preview")
    key_flash(base, t, T(sid, 9) + 0.6, 1560, 880)
    if t >= T(sid, 27): pass
    illu(base)


def b_purge_b(base, t, b):
    o = b["t0"]; sid = "purge"
    place(base, pill("NEVER DELETE", 64, RED, INK, pad=(50, 14), kind="b", glow=False), W / 2, 230, 0.85 + 0.15 * pop(t, o), fade(t, o, 0.2))
    for i, (s, why, tt) in enumerate([("~/.claude.json", "account", T(sid, 29)), ("~/.claude/settings.json", "preferences", T(sid, 30)), ("~/.claude/plugins/", "plugins", T(sid, 32))]):
        y = 420 + 140 * i; enter(base, card(1300, 110, 26, outline=RED), 960, y, t, tt - 0.3, side=0)
        spr = NI(1300, 110); d = SD(spr); d.text((50, 55), s, font=F(42, MONO), fill=WHITE + (255,), anchor="lm")
        if t >= T(sid, 40 + i): d.text((1250, 55), "= " + why, font=F(36, "b"), fill=AMB + (255,), anchor="rm")
        enter(base, spr, 960, y, t, tt - 0.3)
    if t < T(sid, 29) - 0.3: place(base, pill("careful with these three", 40, (30, 44, 62), WHITE, pad=(34, 12), kind="p", outline=RED), 960, 520, 1.0, fade(t, o))


# ---------- recap + CTA ----------
def b_cta_a(base, t, b):
    sid = "cta"
    place(base, pill("3 THINGS TO REMEMBER", 52, (20, 24, 34), WHITE, pad=(50, 14), kind="b", outline=SKY, glow=True), W / 2, 230, 1.0, fade(t, b["t0"], 0.25))
    for i, (n, s, tt) in enumerate([("1", "project .claude = team  |  home .claude = you", T(sid, 5)), ("2", "most work: CLAUDE.md + settings.json", T(sid, 19)), ("3", "transcripts are plain text: guard secrets", T(sid, 29))]):
        y = 430 + 150 * i; enter(base, card(1300, 110, 26), 960, y, t, tt - 0.2, side=0)
        spr = NI(1300, 110); d = SD(spr); d.rounded_rectangle([24, 22, 90, 88], 14, fill=SKY + (255,)); d.text((57, 55), n, font=F(40, "b"), fill=INK + (255,), anchor="mm"); d.text((130, 55), s, font=F(36, "p"), fill=WHITE + (255,), anchor="lm"); enter(base, spr, 960, y, t, tt - 0.2)


def b_cta_b(base, t, b):
    sid = "cta"; t1, t2, t3 = T(sid, 45), T(sid, 47), T(sid, 49)
    place(base, pill("Was it useful?  Send it to a friend", 44, (30, 44, 62), WHITE, pad=(34, 12), kind="b", outline=SKY), 960, 195, 1.0, fade(t, b["t0"], 0.3))
    if t >= t1 - 0.2: place(base, pill("Comment", 60, (20, 24, 34), WHITE, pad=(40, 12), kind="b", outline=OUT), 960, 335, 0.8 + 0.2 * pop(t, t1 - 0.2), min(1, fade(t, t1 - 0.2, 0.2)))
    if t >= t2: place(base, pill("DIRECTORY", 120, SKY, INK, pad=(60, 14), kind="b", glow=True), 960, 510, 0.8 + 0.2 * pop(t, t2), min(1, fade(t, t2, 0.2)))
    if t >= t3: place(base, pill("Follow DevRoboLab", 54, (20, 24, 34), SKY, pad=(40, 12), kind="b", outline=OUT), 960, 690, 0.8 + 0.2 * pop(t, t3), min(1, fade(t, t3, 0.2)))
    tt = t3 + 0.9
    if t >= tt:
        for i, s in enumerate(["Watch next", "Subscribe"]):
            enter(base, card(640, 150, 28, glow=True), 560 + 800 * i, 860, t, tt + 0.3 * i, side=0)
            spr = NI(640, 150); SD(spr).text((320, 75), s, font=F(40, "b"), fill=WHITE + (255,), anchor="mm"); enter(base, spr, 560 + 800 * i, 860, t, tt + 0.3 * i)


def _mk():
    B = []
    def add(i, sid, a, b): B.append(dict(id=i, sid=sid, t0=a, t1=b))
    add("hook_a", "hook", 0.0, T("hook", 26) - 0.2); add("hook_b", "hook", T("hook", 26) - 0.2, E("hook"))
    add("what_a", "what", S("what", 0), T("what", 35) - 0.2); add("what_b", "what", T("what", 35) - 0.2, E("what"))
    add("two_a", "two", S("two", 0), E("two")); add("demo", "demo", S("demo", 0), E("demo")); add("choose", "choose", S("choose", 0), E("choose")); add("extras", "extras", S("extras", 0), E("extras"))
    add("mine_a", "mine", S("mine", 0), T("mine", 21) - 0.2); add("mine_b", "mine", T("mine", 21) - 0.2, E("mine"))
    add("data_a", "data", S("data", 0), T("data", 30) - 0.2); add("data_b", "data", T("data", 30) - 0.2, E("data"))
    add("purge_a", "purge", S("purge", 0), T("purge", 28) - 0.2); add("purge_b", "purge", T("purge", 28) - 0.2, E("purge"))
    add("cta_a", "cta", S("cta", 0), T("cta", 38) - 0.2); add("cta_b", "cta", T("cta", 38) - 0.2, TOTAL + 1)
    return B
B = _mk()
