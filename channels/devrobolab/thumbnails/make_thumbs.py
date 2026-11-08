r"""DevRoboLab thumbnails v3 (2026-11-07, user-approved look): LIGHT clean background, SMALL words (2 lines, one highlighted), the DevRoboLab robot, and a picture that shows how it works.
Long = 1280x720 (16:9), Short = 1080x1920 (9:16). One robot pose/side, background colour and picture type per video.
    .venv\Scripts\python -X utf8 channels\devrobolab\thumbnails\make_thumbs.py [video_id ...]      (no ids = all in VIDEOS)
HARD RULE (user 2026-11-07): the channel name (DevRoboLab) must NEVER overlap any other content. Every render is checked: the brand box is measured against the tag, the title, the picture and the robot,
and everything must stay inside the frame; a thumbnail that fails the check is NOT written as OK (the run prints FAIL and apply_thumbs.py refuses it)."""
import base64
import re
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
FONTS = ROOT / "shared/fonts"
MASCOT = ROOT / "channels/devrobolab/mascot/cut"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)

CSS = """
@font-face{font-family:PX;src:url('@@PX@@');font-weight:800}
@font-face{font-family:PB;src:url('@@PB@@');font-weight:700}
@font-face{font-family:PM;src:url('@@PM@@');font-weight:500}
@font-face{font-family:MO;src:url('@@MO@@');font-weight:700}
*{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#14213d;--y:#FFC800}
body{position:relative;overflow:hidden;font-family:PB,sans-serif;color:var(--ink);background:var(--bg)}
body.land{width:1280px;height:720px}body.port{width:1080px;height:1920px}
.dots{position:absolute;inset:0;background-image:radial-gradient(rgba(20,33,61,.11) 2px,transparent 2px);background-size:34px 34px}
.blob{position:absolute;border-radius:50%;background:var(--blob)}
.tag{position:absolute;font:700 26px PB;letter-spacing:2px;background:var(--ink);color:var(--y);padding:9px 22px;border-radius:999px;white-space:nowrap}
.ttl{position:absolute;font-family:PX;font-weight:800;line-height:1.1}
.ttl .l{display:block;white-space:nowrap;width:max-content}
mark{background:var(--y);color:var(--ink);padding:0 .12em;border-radius:.14em}
.brand{position:absolute;font:800 26px PX;white-space:nowrap}.brand span{background:var(--y);padding:0 6px;border-radius:6px}
img.robot{position:absolute}
.vis{position:absolute}
.card{background:#fff;border:4px solid var(--ink);border-radius:24px;box-shadow:8px 8px 0 var(--ink);padding:18px;color:var(--ink)}
.bub{font:700 28px PB;line-height:1.2}
.lab{font:700 24px PB;margin:12px 0 0 6px}
.lab b{background:var(--ink);color:var(--y);border-radius:50%;display:inline-block;width:34px;height:34px;line-height:34px;text-align:center;font-size:22px;margin-right:8px}
.arr{display:block;margin:6px auto}
.hd{background:var(--y);padding:10px 14px;font:800 22px PX;display:flex;justify-content:space-between;align-items:center;gap:8px;white-space:nowrap}
.red{background:#ff4d5e;color:#fff;font:800 16px PX;padding:4px 9px;border-radius:8px;white-space:nowrap}
.rowi{font:700 26px PB;padding:6px 0;display:flex;align-items:center;gap:10px}
.chip{display:inline-block;background:#fff;border:3px solid var(--ink);border-radius:999px;padding:5px 14px;font:700 22px PB;margin:0 6px 8px 0}
.row{display:flex;align-items:center;gap:12px;padding:10px 12px;border:3px solid var(--ink);border-radius:16px;margin-bottom:10px;font:700 26px PB;background:#fff}
.row .t{width:34px;height:34px;border-radius:50%;border:3px solid var(--ink);display:flex;align-items:center;justify-content:center;font:800 20px PX;flex:none;background:#fff}
.row.on .t{background:var(--y)}
.mono{font:700 24px MO;line-height:1.6;white-space:pre}
.win{background:#0f172a;color:#e6edf7;border-radius:24px;border:4px solid var(--ink);box-shadow:8px 8px 0 var(--ink);padding:16px 20px}
.win .dots3{display:flex;gap:8px;margin-bottom:10px}.win .dots3 i{width:14px;height:14px;border-radius:50%;background:#ff5f57}.win .dots3 i:nth-child(2){background:#febc2e}.win .dots3 i:nth-child(3){background:#28c840}
.win .mono .p,.win .mono .ok{color:#7cf0a8}.win .mono .dm{opacity:.55}
.big{font:800 150px PX;line-height:1;text-align:center}
.bsub{font:700 30px PB;text-align:center;margin-top:6px}
.bar{height:54px;border-radius:54px;background:#e5e7eb;border:4px solid var(--ink);overflow:hidden;margin:8px 0 16px}.bar i{display:flex;align-items:center;justify-content:flex-end;height:100%;padding-right:16px;font:800 28px PX}
.vs{display:flex;gap:10px}.vs .c{flex:1;border:3px solid var(--ink);border-radius:18px;padding:12px 6px;text-align:center;background:#fff}
.vs .c h5{font:800 22px PX;background:var(--y);border-radius:8px;padding:2px 6px;display:inline-block;margin-bottom:6px}.vs .c p{font:700 22px PB}
.ph{border:8px solid #111;border-radius:40px;background:#fff;padding:16px;box-shadow:8px 8px 0 var(--ink);width:320px;margin:0 auto}
.fgrid{display:grid;grid-template-columns:1fr 1fr;gap:18px}
.f{border:4px solid var(--ink);border-radius:18px;background:#fff;box-shadow:6px 6px 0 var(--ink);padding:12px}
.f b{font:800 20px PX;border-radius:8px;padding:3px 9px;display:inline-block}.f div{font:700 22px PB;margin-top:6px}
.land .tag{left:40px;top:36px}
.land .brand{right:40px;top:40px}
.port .tag{left:60px;top:70px;font-size:32px;padding:11px 26px}
.port .brand{right:60px;top:76px;font-size:40px}
.port .ttl{left:60px;top:190px}
.port .vis{left:30px;top:330px;width:470px;zoom:2.0}
"""

THEMES = {"cream": ("#FFFAEB", "#FFE680"), "sky": ("#E8F3FF", "#BFE0FF"), "mint": ("#E6FAF0", "#BFF0D6"), "pink": ("#FFEAF2", "#FFC6DD"),
          "lav": ("#F0EBFF", "#D5C8FF"), "peach": ("#FFF0E3", "#FFD3A8"), "lime": ("#F4FAD9", "#DDF08A")}


def _mk(t):
    return re.sub(r"\*(.+?)\*", r"<mark>\1</mark>", t)


def flow(items):
    out = []
    for i, (cap, html, tint) in enumerate(items):
        pad = 0 if html.startswith("<div class=hd") else 18
        out.append(f'<div class=card style="background:{tint};padding:{pad}px;overflow:hidden">{html}</div><div class=lab><b>{i + 1}</b>{cap}</div>')
        if i < len(items) - 1:
            out.append('<svg class=arr width="40" height="34" viewBox="0 0 40 34"><path d="M20 2v24M8 16l12 14 12-14" fill="none" stroke="#14213d" stroke-width="6" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    return "".join(out)


FOLDER = '<svg width="26" height="20" viewBox="0 0 26 20"><path d="M1 3h8l3 3h13v13H1z" fill="#FFC800" stroke="#14213d" stroke-width="2"/></svg>'


def row_flow(items):
    cols = []
    for i, (cap, html, tint) in enumerate(items):
        pad = 0 if html.startswith("<div class=hd") else 18
        cols.append(f'<div style="flex:{1.45 if "class=hd" in html else 1}"><div class=card style="background:{tint};padding:{pad}px;overflow:hidden">{html}</div><div class=lab><b>{i + 1}</b>{cap}</div></div>')
        if i < len(items) - 1:
            cols.append('<svg width="44" height="40" viewBox="0 0 56 40" style="flex:none;margin-top:46px"><path d="M2 20h40M30 6l14 14-14 14" fill="none" stroke="#14213d" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>')
    return '<!--w820--><div style="display:flex;align-items:flex-start;gap:8px">' + "".join(cols) + '</div>'


def memory_flow():
    return row_flow([("Aap bolte ho", '<div class=bub>Mera naam Rahul hai</div>', "#fff"),
                 ("Claude yaad rakhta hai", f'<div class=hd>MEMORY<span class=red>DELETE &#10005;</span></div><div style="padding:10px 16px"><div class=rowi>{FOLDER} Role: student</div><div class=rowi>{FOLDER} Project: thesis</div><div class=rowi>{FOLDER} Style: short</div></div>', "#fff"),
                 ("Agli chat me bhi", '<div class=bub>Hi Rahul! Yaad hai</div>', "#E8F7EC")])


def files(items):
    f = "".join(f'<div class=f><b style="background:{c}">{n}</b><div>{d}</div></div>' for n, c, d in items)
    return f'<div style="margin-bottom:10px"><svg width="130" height="88" viewBox="0 0 440 280"><path d="M10 40q0-20 20-20h110l30 34h250q20 0 20 20v176q0 20-20 20H30q-20 0-20-20z" fill="#FFC800" stroke="#14213d" stroke-width="10" stroke-linejoin="round"/></svg></div><div class=fgrid>{f}</div>'


def bars(rows):
    out = "".join(f'<div style="font:700 28px PB">{label}</div><div class=bar><i style="width:{pct}%;background:{col}">{txt}</i></div>' for label, pct, txt, col in rows)
    return f'<div class=card>{out}</div>'


def steps(items, done=None):
    done = len(items) if done is None else done
    return "".join(f'<div class="row {"on" if i < done else ""}"><div class=t>{"&#10003;" if i < done else i + 1}</div>{x}</div>' for i, x in enumerate(items))


def term(title, lines):
    return f'<div class=win><div class=dots3><i></i><i></i><i></i></div><div style="font:800 22px PX;color:#FFC800;margin-bottom:8px">{title}</div><div class=mono>{chr(10).join(lines)}</div></div>'


def big(num, sub, chips=(), size=150):
    c = "".join(f'<span class=chip>{x}</span>' for x in chips)
    return f'<div class=card style="text-align:center"><div class=big style="font-size:{size}px">{num}</div><div class=bsub>{sub}</div><div style="margin-top:12px">{c}</div></div>'


def meter(label, pct, chips):
    c = "".join(f'<span class=chip>{x}</span>' for x in chips)
    return f'<div class=card><div style="font:800 24px PX;display:flex;justify-content:space-between"><span>{label}</span><span>{pct}%</span></div><div class=bar><i style="width:{pct}%;background:#FFC800"></i></div><div>{c}</div></div>'


def phone(title, rows, chips=()):
    r = "".join(f'<div class=row style="margin-bottom:8px">{x}</div>' for x in rows)
    c = "".join(f'<span class=chip>{x}</span>' for x in chips)
    return f'<div class=ph><div style="font:800 24px PX;margin-bottom:8px">{title}</div>{r}<div>{c}</div></div>'


def versus(cols):
    c = "".join(f'<div class=c><h5>{a}</h5><p>{b}</p></div>' for a, b in cols)
    return f'<div class=card><div class=vs>{c}</div></div>'


P, L = "port", "land"
# (video id, orientation, theme, robot pose, robot side (l/r), tag, (line1, line2), picture html)
VIDEOS = [
    ("zfOBSjw3RA0", L, "cream", "think", "l", "CLAUDE FEATURE 05", ("Claude ko sab", "*yaad* hai?"), memory_flow()),
    ("E-yaXp_ZgMw", L, "sky", "work", "r", "CLAUDE CODE 03", ("Aapke *.claude*", "folder me kya hai?"),
     files([("CLAUDE.md", "#FFC800", "instructions"), ("settings.json", "#7CC6FF", "permissions"), ("skills/", "#8FE3A8", "reusable prompts"), ("agents/", "#FF9EC4", "helpers")])),
    ("nHhmmwqwMtw", L, "pink", "wave", "l", "AI NEWS", ("Aaj ki *5 AI*", "khabrein"), big("5", "badi khabrein", ["Gemini 4", "Mistral", "Ollama", "ElevenLabs"], 120)),
    ("GpVCvYrwqd4", P, "mint", "work", "r", "CLAUDE CODE HOOKS", ("File edit ke baad", "*auto format*"), term("hook", ['<span class=p>&gt;</span> app.py edit hui', '<span class=dm>hook chala...</span>', 'app.py <span class=ok>formatted &#10003;</span>'])),
    ("z9LEeI0YNKo", P, "peach", "thumbs", "r", "CLAUDE CODE CHECKPOINTS", ("*Esc Esc* se", "sab undo"), big("Esc Esc", "ek jhatke me undo", ["Checkpoints"], 100)),
    ("jQWCNgezK38", P, "lav", "think", "l", "CLAUDE CODE MEMORY", ("CLAUDE.md ko", "sab *yaad* hai"), term("CLAUDE.md", ['# Project', '- tests: npm test', '- style: short answers', '<span class=ok>&#10003; har session me padha</span>'])),
    ("yl0Cjc4E_1w", P, "lime", "wave", "r", "CLAUDE CODE SKILLS", ("Ek baar likho,", "*baar baar* chalao"), steps(["Skill likho", "/skill-name likho", "Baar baar chalao"])),
    ("XdC3f07GzXw", P, "pink", "work", "l", "CLAUDE CODE SUBAGENTS", ("Bada kaam", "*helper* ko do"), steps(["Main Claude", "Helper 1: files dhundo", "Helper 2: test chalao"])),
    ("XjGT3YxVC3Q", P, "sky", "think", "r", "CLAUDE CODE MCP", ("Tools se", "*seedha* connect"), term("mcp", ['<span class=p>$</span> claude mcp add ...', '<span class=ok>tool connected &#10003;</span>', 'ab Claude use kar sakta hai'])),
    ("whEYixIMx0Q", P, "cream", "stop", "l", "CLAUDE CODE TOOLS", ("Kaun poochta,", "*kaun nahi?*"), versus([("READ", "bina pooche"), ("EDIT", "pooch ke"), ("BASH", "pooch ke")])),
    ("s5jjwxwXVQg", P, "mint", "wave", "r", "PERMISSION MODES", ("*Shift+Tab* se", "control"), steps(["Normal: pooche", "Auto-accept edits", "Plan mode"])),
    ("Xxp98DvODfk", P, "lav", "work", "l", "CLAUDE CODE WORKTREES", ("*Parallel* sessions,", "alag folder"), term("worktrees", ['<span class=p>repo/</span>', '  worktree-a/  <span class=ok>session 1</span>', '  worktree-b/  <span class=ok>session 2</span>'])),
    ("MG3qhsH0guE", P, "peach", "thumbs", "r", "CLAUDE CODE SESSIONS", ("*Resume*, naam", "aur branch"), term("sessions", ['<span class=p>$</span> claude --resume', 'session: fix-login <span class=ok>&#10003;</span>', 'branch: fix/login'])),
    ("dwekrfHuLXI", P, "lime", "think", "l", "CLAUDE CODE STATUS LINE", ("*Context* aur cost", "hamesha dikhao"), meter("CONTEXT", 62, ["model", "cost", "branch"])),
    ("ag6O1FR5Qqw", P, "sky", "work", "r", "CLAUDE CODE", ("*claude -p*", "script me chalao"), term("script", ['<span class=p>$</span> claude -p "summary"', '<span class=ok>output &#8594; file &#10003;</span>'])),
    ("uXhFF5o4Qz4", P, "pink", "wave", "l", "CLAUDE CODE PLUGINS", ("Ek unit me", "*skills, hooks, MCP*"), term("my-plugin", ['<span class=p>my-plugin/</span>', '  skills/   <span class=ok>&#10003;</span>', '  hooks/    <span class=ok>&#10003;</span>', '  .mcp.json <span class=ok>&#10003;</span>'])),
    ("vbCJlFz2TmU", P, "cream", "stop", "r", "CLAUDE CODE CONTEXT", ("*Compact* ke baad", "kya bachta hai?"), meter("COMPACT", 28, ["summary", "CLAUDE.md", "files"])),
    ("BHwc7iL1ujk", P, "mint", "wave", "l", "CLAUDE CODE", ("Claude Code", "*kya hai?* 5 jagah"), big("5", "jagah chalta hai", ["helper"], 150)),
    ("R5eSmgK_xrM", P, "lav", "thumbs", "r", "CLAUDE CODE QUICKSTART", ("*4 steps* me", "shuru karo"), steps(["Install", "Login", "Folder kholo", "Pehla prompt"])),
    ("9fmGXDSdZus", P, "peach", "think", "l", "CLAUDE CODE", ("*3 phases*", "ka magic trick"), big("3", "phases", ["magic trick"], 170)),
    ("p2iHbx76Bzo", P, "lime", "work", "r", "KAUNSA KAB?", ("CLAUDE.md,", "*Skill ya Hook?*"), versus([("CLAUDE.md", "hamesha"), ("SKILL", "jab chaho"), ("HOOK", "apne aap")])),
    ("vve7vJpP04Y", P, "sky", "stop", "l", "CLAUDE CODE LOGIN", ("Login kab", "*khatam* hoga?"), big("&#8987;", "ab pata chalega", ["login"], 130)),
    ("DF-KEvEcHm4", P, "mint", "work", "r", "CLAUDE CODE", ("Bug fix:", "*3 simple steps*"), steps(["Bug batao", "Fix karwao", "Test chalao"])),
    ("tMsznaDv0dU", P, "pink", "wave", "l", "AI NEWS", ("Image se", "*GIF* ban gaya"), phone("ChatGPT", ["Image", "&#8595;", "GIF &#10003;"], ["naya feature"])),
    ("ZLfCsEMZReI", P, "cream", "thumbs", "r", "CLAUDE FEATURE 01", ("Claude *Projects*", "step by step"), steps(["Project banao", "Files jodo", "Instructions likho"])),
    ("UVgiYp0N6g0", P, "lav", "think", "l", "CLAUDE FEATURE 02", ("Chat se", "*Artifact* banao"), flow([("Aap bolte ho", '<div class=bub>Ek calculator banao</div>', "#fff"), ("Claude banata hai", '<div class=bub>Artifact ready &#10003;</div>', "#E8F7EC")])),
    ("1t6XbC5RCMg", P, "peach", "work", "r", "CLAUDE FEATURE 03", ("Claude khud", "*research* karta hai"), steps(["Web search", "Sources check", "Report ready"])),
    ("B9f8_sC0elI", P, "lime", "wave", "l", "AI NEWS", ("Paise ka *hisaab*", "Claude se"), phone("Kharcha", ["Food", "Rent"], ["category"])),
    ("5eH-XqR6SQ0", P, "mint", "thumbs", "r", "CLAUDE CODE 02", ("Claude Code", "ab *2.5x* tez"), bars([("Normal", 40, "1x", "#9aa3b2"), ("/fast", 100, "2.5x", "#FFC800")])),
    ("lXYyyQmxVfg", P, "sky", "think", "l", "CLAUDE FEATURE 04", ("PDF aur photo", "*upload* karo"), flow([("Aap upload karte ho", '<div class=bub>PDF + photo</div>', "#fff"), ("Claude jawab deta hai", '<div class=bub>Ye raha summary &#10003;</div>', "#E8F7EC")])),
    ("oQni7skZzgs", P, "lav", "wave", "r", "AI NEWS", ("Google AI video", "*15 second* ka"), bars([("Pehle", 66, "10 s", "#9aa3b2"), ("Ab", 100, "15 s", "#7B5CF6")])),
]

HTML = """<style>%(css)s</style><body class="%(cls)s" style="--bg:%(bg)s;--blob:%(blob)s"><div class=dots></div>
%(blob_html)s
<div class=tag>%(tag)s</div>
<div class=ttl style="%(ttl_style)s">%(ttl)s</div>
<div class=vis style="%(vis_style)s">%(vis)s</div>
<img class=robot src="%(robot)s" style="%(robot_style)s">
<div class=brand>Dev<span>Robo</span>Lab</div>
<script>
const MAXW=%(maxw)d;
function fit(){document.querySelectorAll('.ttl .l').forEach(el=>{let fs=parseInt(el.dataset.s);el.style.fontSize=fs+'px';let g=0;while(el.getBoundingClientRect().width>MAXW&&fs>24&&g<200){fs-=2;el.style.fontSize=fs+'px';g++}})}
function fitvis(){const v=document.querySelector('.vis');if(!document.body.classList.contains('port'))return;let z=2.0,g=0;
const place=()=>{v.style.zoom=z;v.style.left=(60/z)+'px';v.style.top=(555/z)+'px'};place();
while((v.getBoundingClientRect().bottom>1210||v.getBoundingClientRect().right>1030)&&z>1.1&&g<60){z-=0.05;place();g++}}
document.fonts.ready.then(()=>{fit();fitvis()});
</script></body>"""

MEASURE = """() => { const r = s => { const e = document.querySelector(s); if(!e) return null; const b = e.getBoundingClientRect(); return [b.left,b.top,b.right,b.bottom]; };
  return {brand:r('.brand'), tag:r('.tag'), ttl:r('.ttl'), vis:r('.vis'), robot:r('img.robot'), W:innerWidth, H:innerHeight}; }"""


def check(m):
    """brand must not overlap anything; tag/title/picture/brand inside the frame (the robot may bleed at the bottom/side on purpose)"""
    probs = []
    b = m["brand"]
    def hit(a, c, pad=6): return not (a[2] + pad <= c[0] or c[2] + pad <= a[0] or a[3] + pad <= c[1] or c[3] + pad <= a[1])
    for k in ("tag", "ttl", "vis", "robot"):
        if m[k] and hit(b, m[k]): probs.append(f"brand overlaps {k}")
    for k in ("tag", "ttl", "vis", "brand"):
        r = m[k]
        if r and (r[0] < 0 or r[1] < 0 or r[2] > m["W"] + 1 or r[3] > m["H"] + 1): probs.append(f"{k} cut by the frame {[round(x) for x in r]}")
    for a, c in (("tag", "ttl"), ("ttl", "vis"), ("tag", "vis")):
        if m[a] and m[c] and hit(m[a], m[c], 0): probs.append(f"{a} overlaps {c}")
    return probs


def render(vid_list):
    from playwright.sync_api import sync_playwright
    def b64(p, mime): return f"data:{mime};base64," + base64.b64encode(Path(p).read_bytes()).decode()
    css = (CSS.replace("@@PX@@", b64(FONTS / "Poppins-ExtraBold.ttf", "font/ttf")).replace("@@PB@@", b64(FONTS / "Poppins-Bold.ttf", "font/ttf"))
           .replace("@@PM@@", b64(FONTS / "Poppins-Medium.ttf", "font/ttf")).replace("@@MO@@", b64(FONTS / "IBMPlexMono-Bold.ttf", "font/ttf")))
    robots = {p: b64(MASCOT / f"{p}.png", "image/png") for p in ("think", "work", "wave", "thumbs", "stop")}
    results = {}
    with sync_playwright() as p:
        b = p.chromium.launch()
        for vid, ori, theme, pose, side, tag, lines, vis in VIDEOS:
            if vid_list and vid not in vid_list: continue
            bg, blob = THEMES[theme]
            if ori == L:
                W, H, maxw, fs = 1280, 720, 560, 62
                robot_style = ("left:14px;bottom:-14px;height:520px" if side == "l" else "right:14px;bottom:-14px;height:520px")
                ttl_style = "left:430px;top:36px;" if side == "l" else "left:40px;top:100px;"
                vw = int(re.match(r"<!--w(\d+)-->", vis).group(1)) if vis.startswith("<!--w") else 520
                vis_style = f"left:430px;top:215px;width:{min(vw, 820)}px;" if side == "l" else f"left:40px;top:260px;width:{vw}px;"
                blob_html = f'<div class=blob style="{"left:-120px" if side == "l" else "right:-120px"};top:140px;width:640px;height:640px"></div>'
            else:
                W, H, maxw, fs = 1080, 1920, 960, 104
                robot_style = ("left:20px;bottom:30px;height:650px" if side == "l" else "right:20px;bottom:30px;height:650px")
                ttl_style = ""; vis_style = ""
                blob_html = f'<div class=blob style="{"left:-120px" if side == "l" else "right:-120px"};top:1180px;width:840px;height:840px"></div>'
            ttl = "".join(f'<span class=l data-s="{fs}" style="font-size:{fs}px">{_mk(x)}</span>' for x in lines)
            html = HTML % dict(css=css, cls="land" if ori == L else "port", bg=bg, blob=blob, blob_html=blob_html, tag=tag, ttl_style=ttl_style, ttl=ttl, vis_style=vis_style, vis=vis,
                               robot=robots[pose], robot_style=robot_style, maxw=maxw)
            pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
            pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
            m = pg.evaluate(MEASURE); probs = check(m)
            out = OUT / f"{vid}_{'16x9' if ori == L else '9x16'}.png"
            failtxt = OUT / f"{vid}.FAIL.txt"
            if probs:
                failtxt.write_text("; ".join(probs), encoding="utf-8")
                if out.exists(): out.unlink()
                pg.screenshot(path=str(OUT / f"{vid}.failed.png")); print("FAIL", vid, probs)
            else:
                for f in (failtxt, OUT / f"{vid}.failed.png"):
                    if f.exists(): f.unlink()
                pg.screenshot(path=str(out)); print("ok  ", vid)
            results[vid] = probs; pg.close()
        b.close()
    return results


if __name__ == "__main__":
    r = render(sys.argv[1:])
    bad = [k for k, v in r.items() if v]
    print(len(r) - len(bad), "ok,", len(bad), "FAIL", bad)
