m = open("mid.py", encoding="utf-8").read()
a = 'kind="b", outline=SKY), 960, 215, 1.0, fade(t, b["t0"], 0.3))\n    if t >= t1 - 0.2'
assert a in m; m = m.replace(a, 'kind="b", outline=SKY), 960, 195, 1.0, fade(t, b["t0"], 0.3))\n    if t >= t1 - 0.2')
a = '960, 320, 0.8 + 0.2 * pop(t, t1 - 0.2)'; assert a in m; m = m.replace(a, '960, 335, 0.8 + 0.2 * pop(t, t1 - 0.2)')
open("mid.py", "w", encoding="utf-8").write(m)
