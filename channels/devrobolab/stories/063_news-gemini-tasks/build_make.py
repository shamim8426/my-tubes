"""Assemble make_final.py = 061 helpers (copied from 044 look) + beats.py (this video) + 061 render tail."""
import re
src = open("../061_cfe-usage-saving/make_final.py", encoding="utf-8").read()
head, rest = src.split("# ---------- beats ----------", 1)
tail = "FN = {" + rest.split("FN = {", 1)[1]
head = head.split('"""', 2)[2]
doc = '''"""AI Khabar (news deep dive) LONG: 'Tasks in Gemini' (Google, 2026-11-17) 16:9 1920x1080.
Helpers copied from stories/061_cfe-usage-saving/make_final.py (itself a copy of stories/044_cfe-memory/make_final.py: dark neon, chapter badge,
Chromium Hindi captions, cursor demos, every action at its spoken word via T(scene, token)). New highlight colour: TURQUOISE.
Official-page crops are our own Playwright captures (raw/capture.py) with the key phrase marked yellow; note() crops around the marked rect.
Built by build_make.py (helpers + beats.py). Run: python make_final.py [frames t1 t2 ... | sheet step | range t0 t1 out.mp4]"""'''
head = head.replace("ACC = (170, 236, 90)", "ACC = (64, 224, 208)").replace("SOFT = (32, 44, 30)", "SOFT = (20, 48, 48)")
head = head.replace("(34, 52, 30, 255) if side == \"user\"", "(22, 50, 50, 255) if side == \"user\"")
head = head.replace(".k{color:#AAEC5A}", ".k{color:#40E0D0}").replace("border:3px solid #2c3a24", "border:3px solid #1f4a48")
head = re.sub(r"CHAP = \{.*?\}\n", '''CHAP = {"hook": None, "what": (1, "what is tasks"), "who": (2, "who gets it"), "start": (3, "turn it on"), "ex1": (4, "example: inbox"),
        "ex2": (5, "example: schedule"), "ex3": (6, "example: research"), "safety": (7, "safety"), "us": (8, "us-only features"), "limits": (9, "limits"),
        "off": (10, "turn it off"), "cta": (11, "recap")}
''', head, flags=re.S)
head = re.sub(r"KEYW = \{.*?\}\n", '''KEYW = {"Tasks", "Task", "free", "India", "subscription", "schedule", "Schedule", "PDF", "confirmation", "पंद्रह", "छह", "America", "inbox", "safety",
        "Hydrogen", "Spark", "control", "History", "experimental", "Submit", "pause", "Turn", "off"}
''', head, flags=re.S)
note_new = '''SRCN = {"blog": "blog.google  /  Put Gemini to work for you", "help": "support.google.com  /  Gemini Apps Help", "rel": "gemini.google  /  Release notes 2026.11.17",
        "sec": "blog.google  /  Gemini defense-in-depth"}
NSRC = {"blogfree": "blog", "vm": "blog", "inject": "blog", "usfirst": "blog", "helpfree": "help", "inbox": "help", "price": "help", "research": "help", "control": "help",
        "fifteen": "help", "exp": "help", "paused": "help", "monday": "help", "hydrogen": "rel", "english": "rel", "microvm": "sec", "confirm": "sec"}
RECTS = json.load(open(HERE / "raw/rects.json"))
_shot = {}
def note(key, w=1000, hh=440):
    """crop of raw/shot_<key>.png around the marked phrase (its text column, DPR 2) on a white card + official source tag"""
    ck = (key, w, hh)
    if ck in _shot: return _shot[ck]
    src = Image.open(HERE / f"raw/shot_{key}.png").convert("RGB"); r = RECTS[key]; S = 2
    x0 = max(0, (r[4] - 24) * S); x1 = min(src.width, (r[4] + r[5] + 24) * S); cw = x1 - x0; ch = int(cw * (hh - 60) / (w - 60))
    if ch > src.height: ch = src.height; cw2 = int(ch * (w - 60) / (hh - 60)); cx = (x0 + x1) / 2; x0, x1 = int(cx - cw2 / 2), int(cx + cw2 / 2)
    cy = (r[1] + r[3] / 2) * S; y0 = int(min(max(0, cy - ch / 2), src.height - ch))
    pg = src.crop((int(x0), y0, int(x1), y0 + ch)).resize((w - 60, hh - 60), Image.LANCZOS).convert("RGBA")
    g = np.ones(pg.height, dtype=np.float32); fl = 30; g[:fl] = np.linspace(0, 1, fl); g[-fl:] = np.minimum(g[-fl:], np.linspace(1, 0, fl))
    arr = np.array(pg).astype(np.float32); arr[:, :, :3] = 250 - (250 - arr[:, :, :3]) * g[:, None, None]; pg = Image.fromarray(arr.astype(np.uint8), "RGBA")
    sh = Image.new("RGBA", (w, hh + 56), (0, 0, 0, 0)); d = ImageDraw.Draw(sh); d.rounded_rectangle([0, 0, w - 1, hh - 1], 18, fill=(250, 249, 246, 255), outline=(200, 204, 214, 255), width=3)
    sh.alpha_composite(pg, (30, 30))
    tag = pill("Official: " + SRCN[NSRC[key]], 20, (20, 24, 34), (200, 208, 224), pad=(16, 5), kind="p", outline=OUT)
    if tag.width > w: tag = tag.resize((w, int(tag.height * w / tag.width)), Image.LANCZOS)
    sh.alpha_composite(tag, ((w - tag.width) // 2, hh - 6)); _shot[ck] = sh; return sh
'''
head = re.sub(r"SRC = \{.*?return sh\n", note_new, head, count=1, flags=re.S)
assert "RECTS" in head and "TURQ" not in head
open("make_final.py", "w", encoding="utf-8").write(doc + head + open("beats.py", encoding="utf-8").read() + "\n\n" + tail)
print("ok", len(open("make_final.py", encoding="utf-8").read().splitlines()))
