m = open("mid.py", encoding="utf-8").read()
def rep(a, b, n=1):
    global m
    assert m.count(a) >= 1, a
    m = m.replace(a, b)
rep('T(sid, 9), "$")', 'T(sid, 9), "~")')
rep('"cta_a": 1.3, "cta_b": 1.3}', '"cta_a": 1.3, "cta_b": 1.0}')
rep('"data_a": 1.05, "data_b": 1.2,', '"data_a": 1.05, "data_b": 1.1,')
rep('960, 340, 0.8 + 0.2 * pop(t, t1 - 0.2)', '960, 320, 0.8 + 0.2 * pop(t, t1 - 0.2)')
rep('960, 490, 0.8 + 0.2 * pop(t, t2)', '960, 480, 0.8 + 0.2 * pop(t, t2)')
rep('960, 790, 0.8 + 0.2 * pop(t, t3)', '960, 790, 0.8 + 0.2 * pop(t, t3)') if False else None
rep('enter(base, card(640, 150, 28, glow=True), 560 + 800 * i, 790, t, tt + 0.3 * i, side=0)\n            spr = NI(640, 150); SD(spr).text((320, 75), s, font=F(40, "b"), fill=WHITE + (255,), anchor="mm"); enter(base, spr, 560 + 800 * i, 790, t, tt + 0.3 * i)',
    'enter(base, card(640, 150, 28, glow=True), 560 + 800 * i, 830, t, tt + 0.3 * i, side=0)\n            spr = NI(640, 150); SD(spr).text((320, 75), s, font=F(40, "b"), fill=WHITE + (255,), anchor="mm"); enter(base, spr, 560 + 800 * i, 830, t, tt + 0.3 * i)')
rep('960, 650, 0.8 + 0.2 * pop(t, t3), min(1, fade(t, t3, 0.2)))', '960, 655, 0.8 + 0.2 * pop(t, t3), min(1, fade(t, t3, 0.2)))')
# extras
rep('x = 560 + 800 * (i % 2); y = 380 + 330 * (i // 2)', 'x = 560 + 800 * (i % 2); y = 440 + 330 * (i // 2)')
rep('d.text((40, 36 + size + 26), sub, font=F(30, "p")', 'd.text((40, 36 + size + 26), sub, font=F(34, "p")')
# hook_b chips
rep('x = 460 + 500 * i if i < 2 else 1480', 'x = (420, 960, 1500)[i]')
# mine_b pair lower
rep('fcard("AGENTS.md", "already in your repo?", SKY, 560, 190, 40), 560, 330,', 'fcard("AGENTS.md", "already in your repo?", SKY, 560, 190, 40), 560, 400,')
rep('960, 330, 1.0, min(1, pp * 1.4)); place(base, fcard("CLAUDE.md", "can be read instead", SKY, 560, 190, 40), 1360, 330,', '960, 400, 1.0, min(1, pp * 1.4)); place(base, fcard("CLAUDE.md", "can be read instead", SKY, 560, 190, 40), 1360, 400,')
rep('kind="b", outline=SKY), 960, 330, 1.0, fade(t, o))', 'kind="b", outline=SKY), 960, 400, 1.0, fade(t, o))')
rep('"ORGANIZATION  managed settings", 36, RED, INK, pad=(32, 10), kind="b"), 960, 560,', '"ORGANIZATION  managed settings", 36, RED, INK, pad=(32, 10), kind="b"), 960, 620,')
rep('kind=MONO, outline=OUT), 960, 680, 1.0, fade(t, tt + 0.7))', 'kind=MONO, outline=OUT), 960, 740, 1.0, fade(t, tt + 0.7))')
rep('[(930, 610), (990, 610), (960, 640)]', '[(930, 670), (990, 670), (960, 700)]')
rep('(70, 28, 36), RED, pad=(28, 9), kind="p", outline=RED), 960, 800, 1.0, fade(t, T("mine", 49)))', '(70, 28, 36), RED, pad=(28, 9), kind="p", outline=RED), 960, 850, 1.0, fade(t, T("mine", 49)))')
# data_b
rep('W / 2, 200, 1.0, fade(t, o, 0.3))\n    ta = T("data", 34) - 0.3', 'W / 2, 190, 1.0, fade(t, o, 0.3))\n    ta = T("data", 34) - 0.3')
rep('fcard(".env", "API_KEY=sk-demo-1234", AMB, 560, 190, 44), 520, 450,', 'fcard(".env", "API_KEY=sk-demo-1234", AMB, 560, 190, 44), 520, 420,')
rep('[(820, 450), (820 + 240 * a, 450)]', '[(820, 420), (820 + 240 * a, 420)]'); rep('[(1060, 450), (1030, 432), (1030, 468)]', '[(1060, 420), (1030, 402), (1030, 438)]')
rep('fcard("transcript", "API_KEY=sk-demo-1234", RED, 560, 190, 44), 1400, 450,', 'fcard("transcript", "API_KEY=sk-demo-1234", RED, 560, 190, 44), 1400, 420,')
rep('RED, pad=(28, 10), kind="p", outline=RED), 960, 640, 0.8', 'RED, pad=(28, 10), kind="p", outline=RED), 960, 590, 0.8')
rep('enter(base, card(560, 220, 28, glow=True), 520, 840, t, tt - 0.3, side=0)', 'enter(base, card(560, 220, 28, glow=True), 520, 790, t, tt - 0.3, side=0)')
rep('enter(base, spr, 520, 840, t, tt - 0.3)', 'enter(base, spr, 520, 790, t, tt - 0.3)')
rep('kind=MONO, outline=SKY), 1360, 840, 0.7', 'kind=MONO, outline=SKY), 1360, 790, 0.7')
open("mid.py", "w", encoding="utf-8").write(m)
