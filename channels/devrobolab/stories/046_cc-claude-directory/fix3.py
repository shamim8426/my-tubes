m = open("mid.py", encoding="utf-8").read()
def rep(a, b):
    global m
    assert a in m, a
    m = m.replace(a, b)
# hook_a larger
rep('enter(base, photo("hook", 700, 480, lt, b["t1"] - o + 4), 470, 520, t, o + 0.02, side=-1)\n    enter(base, _hook_term(t, o), 1400, 520, t, o + 0.2, side=1)', 'enter(base, photo("hook", 780, 600, lt, b["t1"] - o + 4), 450, 560, t, o + 0.02, side=-1)\n    enter(base, _hook_term(t, o), 1410, 560, t, o + 0.2, side=1)')
rep('im, d, ox, oy = termwin(860, 480, "Claude Code")\n    tl(d, ox + 30, oy + 100, "> ", GREEN); t_b = T("hook", 11)', 'im, d, ox, oy = termwin(880, 600, "Claude Code")\n    tl(d, ox + 30, oy + 110, "> ", GREEN); t_b = T("hook", 11)')
rep('tl(d, ox + 66, oy + 100, typed("Always run tests first", t, o + 0.5, t_b), WHITE, 28)\n    if t >= T("hook", 12): tl(d, ox + 30, oy + 160, "Got it.", SKY, 28)\n    if t >= T("hook", 13): d.line([(ox + 30, oy + 235), (ox + 830, oy + 235)], fill=OUT + (255,), width=2); tl(d, ox + 30, oy + 255, "-- next session --", DIM, 24)\n    if t >= T("hook", 16): tl(d, ox + 30, oy + 320, "How do I run the tests?", AMB, 28)\n    return im',
    'tl(d, ox + 70, oy + 110, typed("Always run tests first", t, o + 0.5, t_b), WHITE, 32)\n    if t >= T("hook", 12): tl(d, ox + 30, oy + 190, "Got it.", SKY, 32)\n    if t >= T("hook", 13): d.line([(ox + 30, oy + 290), (ox + 850, oy + 290)], fill=OUT + (255,), width=2); tl(d, ox + 30, oy + 320, "-- next session --", DIM, 26)\n    if t >= T("hook", 16): tl(d, ox + 30, oy + 410, "How do I run the tests?", AMB, 32)\n    return im')
rep('"hook_a": 1.0,', '"hook_a": 1.0,')
# what_a / what_b
rep('place(base, pill("1   THIS PROJECT", 38, SKY, INK, pad=(32, 10), kind="b"), 500, 235,', 'place(base, pill("1   THIS PROJECT", 38, SKY, INK, pad=(32, 10), kind="b"), 500, 205,')
rep('place(base, pill("2   YOUR HOME FOLDER", 38, AMB, INK, pad=(32, 10), kind="b"), 500, 235,', 'place(base, pill("2   YOUR HOME FOLDER", 38, AMB, INK, pad=(32, 10), kind="b"), 500, 205,')
rep('enter(base, photo("team", 700, 380, lt, b["t1"] - o + 4), 500, 450,', 'enter(base, photo("team", 700, 460, lt, b["t1"] - o + 4), 500, 490,')
rep('enter(base, photo("home", 700, 380, lt, b["t1"] - o + 4), 500, 450,', 'enter(base, photo("home", 700, 460, lt, b["t1"] - o + 4), 500, 490,')
rep('tree_card(640, 500, TREE_P, t, o, tt, SKY), 1400, 520,', 'tree_card(640, 560, TREE_P, t, o, tt, SKY), 1400, 530,')
rep('tree_card(640, 450, TREE_H, t, o, tt, AMB), 1400, 500,', 'tree_card(640, 560, TREE_H, t, o, tt, AMB), 1400, 530,')
rep('"git commit  >  whole team gets it", 32, (30, 44, 62), WHITE, pad=(28, 10), kind="b", outline=SKY, hl=("team",)), 560, 760,', '"git commit  >  whole team gets it", 32, (30, 44, 62), WHITE, pad=(28, 10), kind="b", outline=SKY, hl=("team",)), 560, 790,')
rep('kind="p", outline=OUT), 560, 760, 1.0, fade(t, T("what", 14) - 0.2))', 'kind="p", outline=OUT), 560, 790, 1.0, fade(t, T("what", 14) - 0.2))')
rep('"personal  -  all your projects", 32, (30, 44, 62), WHITE, pad=(28, 10), kind="b", outline=AMB), 560, 760,', '"personal  -  all your projects", 32, (30, 44, 62), WHITE, pad=(28, 10), kind="b", outline=AMB), 560, 790,')
rep('1400, 790, 0.7 + 0.3 * pp, min(1, pp * 1.4))\n\n\n# ---------- two key files', '1400, 850, 0.7 + 0.3 * pp, min(1, pp * 1.4))\n\n\n# ---------- two key files')
# cta_b
rep('960, 480, 0.8 + 0.2 * pop(t, t2)', '960, 510, 0.8 + 0.2 * pop(t, t2)')
rep('960, 655, 0.8 + 0.2 * pop(t, t3)', '960, 690, 0.8 + 0.2 * pop(t, t3)')
rep('560 + 800 * i, 830, t, tt + 0.3 * i, side=0)', '560 + 800 * i, 860, t, tt + 0.3 * i, side=0)'); rep('enter(base, spr, 560 + 800 * i, 830, t, tt + 0.3 * i)', 'enter(base, spr, 560 + 800 * i, 860, t, tt + 0.3 * i)')
open("mid.py", "w", encoding="utf-8").write(m)
