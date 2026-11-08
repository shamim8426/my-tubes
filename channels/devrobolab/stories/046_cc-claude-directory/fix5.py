m = open("mid.py", encoding="utf-8").read()
a = 'kind="p", outline=RED), 960, 850, 1.0, fade(t, T("mine", 49)))'; assert a in m
m = m.replace(a, 'kind="p", outline=RED), 960, 815, 1.0, fade(t, T("mine", 49)))')
open("mid.py", "w", encoding="utf-8").write(m)
