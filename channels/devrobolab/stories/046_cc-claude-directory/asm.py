import re
old = open("../044_cfe-memory/make_final.py", encoding="utf-8").read().split("\n")
head = "\n".join(old[:289]); tail = "\n".join(old[546:])
mid = open("mid.py", encoding="utf-8").read()
head = head.replace("SKY = (91, 200, 255)", "SKY = (80, 224, 170)").replace('FPOPB = str(ROOT / "shared/fonts/Poppins-Bold.ttf")', 'FPOPB = str(ROOT / "shared/fonts/Poppins-Bold.ttf"); FMONO = str(ROOT / "shared/fonts/IBMPlexMono-Bold.ttf")')
head = head.replace('{"m": FMUK, "p": FPOP, "b": FPOPB}[kind]', '{"m": FMUK, "p": FPOP, "b": FPOPB, "t": FMONO}[kind]')
head = head.replace('("hook", "notebook", "laptop", "folders", "trash")', '("hook", "team", "home", "shield")').replace(".k{color:#5BC8FF}", ".k{color:#50E0AA}")
head = head.replace('"""Claude Feature 05 (Memory) LONG video FINAL build', '"""Claude Code 03 (.claude directory) LONG video build (adapted from 044 make_final.py)', 1)
head = head.replace("KB = {", "KB0 = {", 1)
i = head.index("KB0 = {"); j = head.index("CX0, CY0")
head = head[:i] + head[j:]
head = head.replace("BG0 = (7, 9, 15)", "BG0 = (6, 11, 13)")
old_b = 'place(base, pill(c[1].upper(), 26, (20, 24, 34), WHITE, pad=(18, 6), outline=OUT, kind="p"), 86 + 36 + 100, 70, absolute=True)'
assert old_b in head
head = head.replace(old_b, '_pb = pill(c[1].upper(), 26, (20, 24, 34), WHITE, pad=(18, 6), outline=OUT, kind="p"); place(base, _pb, 86 + 36 + _pb.width / 2 + 2, 70, absolute=True)')
src = head + "\n" + mid + "\n" + tail
src = src.replace('"output/long_final.mp4"', '"output/long.mp4"').replace('"audio/voice_final.wav"', '"audio/voice.wav"')
open("make_final.py", "w", encoding="utf-8").write(src); print(len(src))
