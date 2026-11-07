r"""DevRoboLab thumbnails v2 (2026-11-07): HTML -> PNG with real Chrome (Playwright). Faceless, big words, a visual of the video's own topic,
a different colour + background style + visual layout per video. Long = 1280x720 (16:9), Short = 1080x1920 (9:16).
    .venv\Scripts\python -X utf8 channels\devrobolab\thumbnails\make_thumbs.py [video_id ...]      (no ids = all in VIDEOS)
Rules: <= 4 big words readable at 160 px width; text only claims what the video's title says; no real person, no real logo; bottom-right free for the time stamp."""
import base64
import sys
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
FONTS = ROOT / "shared/fonts"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)

CSS = """
@font-face{font-family:PX;src:url('%(px)s');font-weight:800}
@font-face{font-family:PB;src:url('%(pb)s');font-weight:700}
@font-face{font-family:PM;src:url('%(pm)s');font-weight:500}
@font-face{font-family:MO;src:url('%(mo)s');font-weight:700}
*{box-sizing:border-box;margin:0;padding:0}
body{overflow:hidden;position:relative;font-family:PB,sans-serif;background:var(--bg);color:var(--fg)}
body.land{width:1280px;height:720px}
body.port{width:1080px;height:1920px}
.s-dark{--bg:#05070d;--fg:#fff;--card:rgba(18,23,36,.94);--cfg:#fff;--line:var(--ac);--sub:rgba(255,255,255,.7)}
.s-light{--bg:#f6f1e6;--fg:#10131c;--card:#ffffff;--cfg:#10131c;--line:#10131c;--sub:rgba(16,19,28,.65)}
.s-color{--bg:var(--ac);--fg:#0b0f19;--card:#0b0f19;--cfg:#fff;--line:#0b0f19;--sub:rgba(11,15,25,.7)}
.bg{position:absolute;inset:0}
.s-dark .bg{background:radial-gradient(900px 640px at 82%% 45%%,color-mix(in srgb,var(--ac) 36%%,transparent),transparent 62%%),linear-gradient(135deg,#070b16,#04060b)}
.s-light .bg{background:radial-gradient(700px 500px at 85%% 20%%,color-mix(in srgb,var(--ac) 40%%,transparent),transparent 65%%),repeating-linear-gradient(0deg,rgba(0,0,0,.025) 0 2px,transparent 2px 6px)}
.s-color .bg{background:radial-gradient(900px 700px at 20%% 0%%,rgba(255,255,255,.35),transparent 60%%),var(--ac)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(127,127,127,.09) 1px,transparent 1px),linear-gradient(90deg,rgba(127,127,127,.09) 1px,transparent 1px);background-size:64px 64px}
.tag{position:absolute;font:700 28px PB;letter-spacing:2px;color:#05070d;background:var(--ac);padding:10px 22px;border-radius:999px}
.s-light .tag{color:#0b0f19}.s-color .tag{background:#0b0f19;color:var(--ac)}
.words{position:absolute;font-family:PX;font-weight:800;line-height:1.0;text-transform:uppercase}
.wl{display:block;white-space:nowrap;width:max-content}
.s-dark .words{text-shadow:0 8px 0 rgba(0,0,0,.45)}
.w2{color:var(--ac)}
.s-dark .w2{text-shadow:0 0 36px color-mix(in srgb,var(--ac) 65%%,transparent),0 8px 0 rgba(0,0,0,.45)}
.s-light .w2,.s-color .w2{background:#0b0f19;color:var(--ac);padding:.02em .2em;border-radius:.16em}
.s-light .w2{background:var(--ac);color:#0b0f19}
.brand{position:absolute;font:800 28px PX;letter-spacing:1px}
.brand span{color:var(--ac)}.s-light .brand span{color:#0b0f19;background:var(--ac);padding:0 6px;border-radius:6px}.s-color .brand span{color:#fff}
.land .tag{left:56px;top:40px}.land .words{left:56px;top:112px;width:700px}.land .brand{left:58px;bottom:34px}
.land .vis{position:absolute;left:770px;top:72px;width:470px}
.port .tag{left:60px;top:70px;font-size:40px;padding:14px 30px}.port .words{left:60px;top:190px;width:960px}.port .brand{left:60px;bottom:70px;font-size:40px}
.port .vis{position:absolute;left:35px;top:520px;width:470px;zoom:2.0}
.card{background:var(--card);color:var(--cfg);border:3px solid var(--line);border-radius:30px;padding:24px;box-shadow:0 26px 54px rgba(0,0,0,.35)}
.s-dark .card{box-shadow:0 0 56px color-mix(in srgb,var(--ac) 42%%,transparent),0 26px 54px rgba(0,0,0,.6)}
.rot{transform:rotate(3deg)}.rotl{transform:rotate(-3deg)}
.bub{background:rgba(127,127,127,.18);border:2px solid rgba(127,127,127,.3);border-radius:20px;padding:14px 18px;font:500 26px PM;margin-bottom:10px}
.bub.me{background:color-mix(in srgb,var(--ac) 35%%,transparent);border-color:var(--ac)}
.chip{display:inline-block;background:rgba(127,127,127,.15);border:2px solid var(--ac);border-radius:999px;padding:7px 16px;font:700 24px PB;margin:0 8px 9px 0}
.s-light .chip,.s-color .chip{border-color:var(--cfg)}
.chip b{color:var(--ac)}.s-light .chip b{color:#0b0f19;background:var(--ac);padding:0 6px;border-radius:6px}
.hd{font:800 26px PX;letter-spacing:2px;color:var(--ac);margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}
.s-light .hd{color:#0b0f19}
.red{background:#ff4d5e;color:#fff;font:800 20px PX;padding:5px 12px;border-radius:10px;transform:rotate(-3deg)}
.sw{width:104px;height:54px;border-radius:54px;background:var(--ac);position:relative;box-shadow:0 0 24px var(--ac)}.sw i{position:absolute;right:5px;top:5px;width:44px;height:44px;border-radius:50%%;background:#fff}
.tr{display:flex;align-items:center;justify-content:space-between;margin-top:12px;font:700 24px PB}
.win .dots{display:flex;gap:8px;margin-bottom:14px}.win .dots i{width:14px;height:14px;border-radius:50%%;background:#ff5f57}.win .dots i:nth-child(2){background:#febc2e}.win .dots i:nth-child(3){background:#28c840}
.mono{font:700 26px MO;line-height:1.6;white-space:pre}.mono .p{color:var(--ac)}.s-light .mono .p,.s-color .mono .p{color:#0f8a4b}.mono .ok{color:#34d96b}.mono .dm{opacity:.6}
.row{display:flex;align-items:center;gap:14px;padding:12px 14px;border:2px solid rgba(127,127,127,.3);border-radius:16px;margin-bottom:10px;font:700 26px PB}
.row .t{width:34px;height:34px;border-radius:50%%;border:3px solid var(--line);display:flex;align-items:center;justify-content:center;font:800 22px PX;flex:none}
.row.on .t{background:var(--ac);color:#0b0f19;border-color:var(--ac)}
.s-color .row.on .t{background:#fff;color:#0b0f19;border-color:#fff}
.big{font:800 190px PX;line-height:1;text-align:center;color:var(--ac)}
.s-light .big{color:#10131c}.s-color .big{color:#fff}
.bsub{font:700 34px PB;text-align:center;margin-top:8px;opacity:.9}
.vs{display:flex;gap:14px;align-items:stretch}.vs .c{flex:1;border:3px solid var(--line);border-radius:22px;padding:16px;text-align:center}
.vs .c h5{font:800 26px PX;color:var(--ac);margin-bottom:8px}.s-light .vs .c h5{color:#0b0f19}.vs .c p{font:700 22px PB}
.bar{height:46px;border-radius:46px;background:rgba(127,127,127,.25);overflow:hidden;margin:10px 0}.bar i{display:block;height:100%%;background:var(--ac);border-radius:46px}
.ph{width:300px;margin:0 auto;border:8px solid #111;border-radius:44px;background:var(--card);padding:18px;box-shadow:0 26px 54px rgba(0,0,0,.45);color:var(--cfg)}
"""

HTML = """<style>%(css)s</style><body class="%(cls)s s-%(style)s" style="--ac:%(ac)s"><div class=bg></div><div class=grid></div>
<div class=tag>%(tag)s</div>
<div class=words>%(words)s</div>
<div class=vis>%(vis)s</div>
<div class=brand>Dev<span>Robo</span>Lab</div>
<script>
const MAXW=%(maxw)d;
function fit(){document.querySelectorAll('.wl').forEach(el=>{let fs=parseInt(el.dataset.s);el.style.fontSize=fs+'px';let g=0;while(el.getBoundingClientRect().width>MAXW&&fs>24&&g<200){fs-=2;el.style.fontSize=fs+'px';g++}})}
document.fonts.ready.then(fit);
</script></body>"""


def chat(me, bot, chips, toggle=None, red=None):
    c = "".join(f'<span class=chip><b>{a}</b> {b}</span>' for a, b in chips)
    t = f'<div class=tr><span>{toggle}</span><div class=sw><i></i></div></div>' if toggle else ""
    r = f'<span class=red>{red}</span>' if red else ""
    return (f'<div class="card rot"><div class="bub me">{me}</div><div class=bub>{bot}</div>'
            f'<div style="border:2px dashed var(--line);border-radius:20px;padding:14px;margin-top:4px"><div class=hd><span>MEMORY</span>{r}</div>{c}{t}</div></div>')


def chat2(me, bot, chips):
    c = "".join(f'<span class=chip>{x}</span>' for x in chips)
    return f'<div class="card rot"><div class="bub me">{me}</div><div class=bub>{bot}</div><div style="margin-top:8px">{c}</div></div>'


def term(title, lines):
    body = "\n".join(lines)
    return f'<div class="card win rotl"><div class=dots><i></i><i></i><i></i></div><div class=hd><span>{title}</span></div><div class=mono>{body}</div></div>'


def steps(items, done=None):
    done = done if done is not None else len(items)
    rows = "".join(f'<div class="row {"on" if i < done else ""}"><div class=t>{"&#10003;" if i < done else i + 1}</div>{x}</div>' for i, x in enumerate(items))
    return f'<div class="card rot">{rows}</div>'


def versus(cols):
    c = "".join(f'<div class=c><h5>{a}</h5><p>{b}</p></div>' for a, b in cols)
    return f'<div class="card rotl"><div class=vs>{c}</div></div>'


def bignum(big, sub, chips=(), size=190):
    c = "".join(f'<span class=chip>{x}</span>' for x in chips)
    return f'<div class="card rot" style="text-align:center"><div class=big style="font-size:{size}px">{big}</div><div class=bsub>{sub}</div><div style="margin-top:14px">{c}</div></div>'


def tree(items):
    rows = "\n".join(items)
    return f'<div class="card win rotl"><div class=dots><i></i><i></i><i></i></div><div class=mono>{rows}</div></div>'


def meter(label, pct, chips):
    c = "".join(f'<span class=chip>{x}</span>' for x in chips)
    return f'<div class="card rot"><div class=hd><span>{label}</span><span>{pct}%</span></div><div class=bar><i style="width:{pct}%"></i></div><div style="margin-top:12px">{c}</div></div>'


def phone(title, rows, chips=()):
    r = "".join(f'<div class=row>{x}</div>' for x in rows)
    c = "".join(f'<span class=chip>{x}</span>' for x in chips)
    return f'<div class="ph rot"><div class=hd><span>{title}</span></div>{r}<div>{c}</div></div>'


ACC = ["#5BC8FF", "#B8F03C", "#FF8A3D", "#FF5CAA", "#3DFFB5", "#FFD23D", "#9B7BFF", "#FF5B5B", "#3DD6FF", "#C8FF3D"]
P, L = "port", "land"
# (video id, orientation, style, accent index, tag, (w1, w2, w3), visual html). IDs are checked against the channel list before upload.
VIDEOS = [
    ("zfOBSjw3RA0", L, "dark", 0, "CLAUDE FEATURE 05", ("CLAUDE KO", "SAB YAAD", "HAI?"),
     chat("Mera naam Rahul hai", "Hi Rahul! Yaad hai", [("ROLE", "student"), ("PROJECT", "thesis"), ("STYLE", "short answers")], "Generate memory", "DELETE &#10005;")),
    ("E-yaXp_ZgMw", L, "color", 5, "CLAUDE CODE 03", ("AAPKA .CLAUDE", "FOLDER", "KYA HAI?"),
     tree(['<span class=p>.claude/</span>', '  CLAUDE.md      <span class=ok>&#10003;</span>', '  settings.json  <span class=ok>&#10003;</span>', '  skills/        <span class=ok>&#10003;</span>', '  agents/        <span class=ok>&#10003;</span>'])),
    ("nHhmmwqwMtw", L, "dark", 3, "AI NEWS", ("AAJ KI", "5 AI", "KHABREIN"),
     bignum("5", "badi khabrein", ["Gemini 4", "Mistral", "Ollama", "ElevenLabs"])),
    ("GpVCvYrwqd4", P, "dark", 4, "CLAUDE CODE HOOKS", ("FILE EDIT", "KE BAAD", "AUTO FORMAT"),
     term("hook", ['<span class=p>&gt;</span> app.py edit hui', '<span class=dm>hook chala...</span>', 'app.py <span class=ok>formatted &#10003;</span>'])),
    ("z9LEeI0YNKo", P, "color", 2, "CLAUDE CODE CHECKPOINTS", ("ESC ESC", "SE SAB", "UNDO"), bignum("Esc Esc", "ek jhatke me undo", ["Checkpoints"], 112)),
    ("jQWCNgezK38", P, "light", 6, "CLAUDE CODE MEMORY", ("~CLAUDE.md", "KO SAB", "YAAD HAI"),
     term("CLAUDE.md", ['# Project', '- tests: npm test', '- style: short answers', '<span class=ok>&#10003; har session me padha</span>'])),
    ("yl0Cjc4E_1w", P, "dark", 1, "CLAUDE CODE SKILLS", ("EK BAAR", "LIKHO", "BAAR BAAR CHALAO"), steps(["Skill likho", "/skill-name likho", "Baar baar chalao"])),
    ("XdC3f07GzXw", P, "color", 7, "CLAUDE CODE SUBAGENTS", ("BADA KAAM", "HELPER KO", "DO"),
     steps(["Main Claude", "Helper 1: files dhundo", "Helper 2: test chalao"], 3)),
    ("XjGT3YxVC3Q", P, "dark", 8, "CLAUDE CODE MCP", ("TOOLS SE", "SEEDHA", "CONNECT"),
     term("mcp", ['<span class=p>$</span> claude mcp add ...', '<span class=ok>tool connected &#10003;</span>', 'ab Claude use kar sakta hai'])),
    ("whEYixIMx0Q", P, "light", 9, "CLAUDE CODE TOOLS", ("KAUN POOCHTA", "KAUN", "NAHI?"),
     versus([("READ", "bina pooche"), ("EDIT", "pooch ke"), ("BASH", "pooch ke")])),
    ("s5jjwxwXVQg", P, "dark", 2, "PERMISSION MODES", ("SHIFT+TAB", "SE", "CONTROL"), steps(["Normal: pooche", "Auto-accept edits", "Plan mode"], 3)),
    ("Xxp98DvODfk", P, "color", 0, "CLAUDE CODE WORKTREES", ("PARALLEL", "SESSIONS", "ALAG FOLDER"),
     tree(['<span class=p>repo/</span>', '  worktree-a/  <span class=ok>session 1</span>', '  worktree-b/  <span class=ok>session 2</span>'])),
    ("MG3qhsH0guE", P, "dark", 5, "CLAUDE CODE SESSIONS", ("RESUME", "NAAM AUR", "BRANCH"),
     term("sessions", ['<span class=p>$</span> claude --resume', 'session: fix-login <span class=ok>&#10003;</span>', 'branch: fix/login'])),
    ("dwekrfHuLXI", P, "light", 3, "CLAUDE CODE STATUS LINE", ("CONTEXT AUR", "COST", "DIKHAO"), meter("CONTEXT", 62, ["model", "cost", "branch"])),
    ("ag6O1FR5Qqw", P, "dark", 6, "CLAUDE CODE", ("~claude -p", "SCRIPT ME", "CHALAO"),
     term("script", ['<span class=p>$</span> claude -p "summary"', '<span class=ok>output &#8594; file &#10003;</span>'])),
    ("uXhFF5o4Qz4", P, "color", 4, "CLAUDE CODE PLUGINS", ("EK UNIT ME", "SKILLS HOOKS", "MCP"),
     tree(['<span class=p>my-plugin/</span>', '  skills/  <span class=ok>&#10003;</span>', '  hooks/   <span class=ok>&#10003;</span>', '  .mcp.json <span class=ok>&#10003;</span>'])),
    ("vbCJlFz2TmU", P, "dark", 7, "CLAUDE CODE CONTEXT", ("COMPACT KE", "BAAD KYA", "BACHTA?"), meter("COMPACT", 28, ["summary", "CLAUDE.md", "files"])),
    ("BHwc7iL1ujk", P, "light", 8, "CLAUDE CODE", ("CLAUDE CODE", "KYA HAI?", "5 JAGAH"), bignum("5", "jagah chalta hai", ["helper"])),
    ("R5eSmgK_xrM", P, "dark", 1, "CLAUDE CODE QUICKSTART", ("4 STEPS", "ME", "SHURU"), steps(["Install", "Login", "Folder kholo", "Pehla prompt"], 4)),
    ("9fmGXDSdZus", P, "color", 9, "CLAUDE CODE", ("3 PHASES", "MAGIC", "TRICK"), bignum("3", "phases", ["magic trick"])),
    ("p2iHbx76Bzo", P, "dark", 3, "KAUNSA KAB?", ("~CLAUDE.md", "SKILL YA", "HOOK?"), versus([("CLAUDE.md", "hamesha"), ("SKILL", "jab chaho"), ("HOOK", "apne aap")])),
    ("vve7vJpP04Y", P, "light", 0, "CLAUDE CODE LOGIN", ("LOGIN KAB", "KHATAM", "HOGA?"), bignum("&#8987;", "ab pata chalega", ["login"])),
    ("DF-KEvEcHm4", P, "dark", 4, "CLAUDE CODE", ("BUG FIX", "3 SIMPLE", "STEPS"), steps(["Bug batao", "Fix karwao", "Test chalao"], 3)),
    ("tMsznaDv0dU", P, "color", 5, "AI NEWS", ("IMAGE SE", "GIF", "BAN GAYA"), phone("ChatGPT", ["Image", "&#8595;", "GIF &#10003;"], ["naya feature"])),
    ("ZLfCsEMZReI", P, "dark", 6, "CLAUDE FEATURE 01", ("CLAUDE", "PROJECTS", "STEP BY STEP"), steps(["Project banao", "Files jodo", "Instructions likho"], 3)),
    ("UVgiYp0N6g0", P, "light", 2, "CLAUDE FEATURE 02", ("CHAT SE", "ARTIFACT", "BANAO"), chat2("Ek calculator banao", "Artifact ready &#10003;", ["Artifact", "chat se"])),
    ("1t6XbC5RCMg", P, "dark", 8, "CLAUDE FEATURE 03", ("CLAUDE KHUD", "RESEARCH", "KARTA HAI"), steps(["Web search", "Sources check", "Report ready"], 3)),
    ("B9f8_sC0elI", P, "color", 3, "AI NEWS", ("PAISE KA", "HISAAB", "CLAUDE SE"), phone("Kharcha", ["Food", "Rent"], ["category"])),
    ("5eH-XqR6SQ0", P, "dark", 5, "CLAUDE CODE 02", ("/FAST", "2.5x", "TEZ"), bignum("2.5x", "/fast se tez", ["Opus"])),
    ("lXYyyQmxVfg", P, "light", 1, "CLAUDE FEATURE 04", ("PDF AUR PHOTO", "UPLOAD", "KARO"), chat2("Is PDF me kya hai?", "Ye raha summary &#10003;", ["PDF", "PHOTO"])),
]
SIZES = {L: (1280, 720, 700, [(104, 84), (166, 122), (176, 168)]), P: (1080, 1920, 960, [(112, 100), (220, 200), (190, 170)])}


def render(vid_list):
    from playwright.sync_api import sync_playwright
    def b64(n): return "data:font/ttf;base64," + base64.b64encode((FONTS / n).read_bytes()).decode()
    css = CSS % dict(px=b64("Poppins-ExtraBold.ttf"), pb=b64("Poppins-Bold.ttf"), pm=b64("Poppins-Medium.ttf"), mo=b64("IBMPlexMono-Bold.ttf"))
    outs = []
    with sync_playwright() as p:
        b = p.chromium.launch()
        for vid, ori, style, ai, tag, w, vis in VIDEOS:
            if vid_list and vid not in vid_list: continue
            W, H, maxw, fs = SIZES[ori]
            idx = 0 if ori == L else 1
            words = "".join(f'<span class="wl w{i + 1}" data-s="{fs[i][0]}" style="font-size:{fs[i][0]}px{";text-transform:none" if x.startswith("~") else ""}">{x.lstrip("~")}</span>' for i, x in enumerate(w))
            html = HTML % dict(css=css, cls="land" if ori == L else "port", style=style, ac=ACC[ai], tag=tag, words=words, vis=vis, maxw=maxw)
            pg = b.new_page(viewport={"width": W, "height": H}, device_scale_factor=1)
            pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
            out = OUT / f"{vid}_{'16x9' if ori == L else '9x16'}.png"
            pg.screenshot(path=str(out)); pg.close(); outs.append(out)
        b.close()
    return outs


if __name__ == "__main__":
    o = render(sys.argv[1:])
    print(len(o), "thumbnails ->", OUT)
