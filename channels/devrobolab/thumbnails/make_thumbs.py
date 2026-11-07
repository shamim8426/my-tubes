r"""DevRoboLab thumbnails v1 (2026-11-07): HTML -> PNG with real Chrome (Playwright), 1280x720, faceless, big words, topic visual, one accent colour per video.
    .venv\Scripts\python -X utf8 channels\devrobolab\thumbnails\make_thumbs.py <key>      (key = a name in THUMBS below, or 'all')
Design rules (see shared/STYLE_LIBRARY.md): <= 4 big words readable at 160 px width, white + ONE accent colour, strong contrast, safe margins (bottom-right stays free for the YouTube time stamp), the visual shows what the video is about (our own illustration, never a real person/logo)."""
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
*{box-sizing:border-box;margin:0;padding:0}
body{width:1280px;height:720px;overflow:hidden;background:#05070d;font-family:PB,sans-serif;position:relative;color:#fff}
.bg{position:absolute;inset:0;background:
 radial-gradient(900px 600px at 82%% 45%%, color-mix(in srgb, var(--ac) 38%%, transparent) 0%%, transparent 62%%),
 radial-gradient(700px 500px at 5%% 100%%, rgba(255,255,255,.07) 0%%, transparent 60%%),
 linear-gradient(135deg,#070b16 0%%,#04060b 100%%)}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(255,255,255,.05) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.05) 1px,transparent 1px);background-size:64px 64px;mask-image:linear-gradient(90deg,transparent 0%%,#000 40%%,#000 100%%)}
.tag{position:absolute;left:56px;top:44px;font:700 30px PB;letter-spacing:2px;color:#05070d;background:var(--ac);padding:10px 22px;border-radius:999px}
.words{position:absolute;left:56px;top:112px;width:700px;font-family:PX;font-weight:800;line-height:.98;text-transform:uppercase;text-shadow:0 8px 0 rgba(0,0,0,.45)}
.w1{font-size:84px;margin-bottom:6px}
.w2{font-size:122px;color:var(--ac);text-shadow:0 0 40px color-mix(in srgb,var(--ac) 65%%,transparent),0 8px 0 rgba(0,0,0,.45)}
.w3{font-size:168px;margin-top:4px}
.brand{position:absolute;left:58px;bottom:34px;font:800 30px PX;letter-spacing:1px}
.brand span{color:var(--ac)}
.card{position:absolute;left:760px;top:70px;width:470px;transform:rotate(3deg);background:rgba(18,23,36,.92);border:3px solid color-mix(in srgb,var(--ac) 70%%,#fff 0%%);border-radius:34px;padding:26px;box-shadow:0 0 60px color-mix(in srgb,var(--ac) 45%%,transparent),0 30px 60px rgba(0,0,0,.6)}
.bub{background:rgba(255,255,255,.1);border:2px solid rgba(255,255,255,.18);border-radius:22px;padding:16px 20px;font:500 28px PM;margin-bottom:12px}
.bub.me{background:color-mix(in srgb,var(--ac) 28%%,#0b1220);border-color:var(--ac)}
.mem{margin-top:6px;border:2px dashed var(--ac);border-radius:24px;padding:18px}
.mem h4{font:800 28px PX;color:var(--ac);letter-spacing:2px;margin-bottom:12px;display:flex;justify-content:space-between;align-items:center}
.dl{font:800 22px PX;letter-spacing:1px;background:#ff4d5e;color:#fff;padding:6px 14px;border-radius:12px;transform:rotate(-3deg);box-shadow:0 6px 16px rgba(0,0,0,.45)}
.chip{display:inline-block;background:#0e1626;border:2px solid var(--ac);border-radius:999px;padding:8px 18px;font:700 26px PB;margin:0 8px 10px 0}
.chip b{color:var(--ac)}
.tog{display:flex;align-items:center;justify-content:space-between;margin-top:14px;font:700 26px PB}
.sw{width:120px;height:62px;border-radius:62px;background:var(--ac);position:relative;box-shadow:0 0 30px var(--ac)}
.sw i{position:absolute;right:6px;top:6px;width:50px;height:50px;border-radius:50%%;background:#fff}
.del{position:absolute;left:1010px;top:560px;transform:rotate(-5deg);background:#ff4d5e;color:#fff;font:800 38px PX;padding:12px 26px;border-radius:18px;box-shadow:0 14px 30px rgba(0,0,0,.5)}
"""

HTML = """<style>%(css)s</style><body style="--ac:%(ac)s"><div class=bg></div><div class=grid></div>
<div class=tag>%(tag)s</div>
<div class=words><div class=w1>%(w1)s</div><div class=w2>%(w2)s</div><div class=w3>%(w3)s</div></div>
<div class=card>%(card)s</div>%(extra)s
<div class=brand>Dev<span>Robo</span>Lab</div></body>"""

THUMBS = {
    "044_memory": dict(ac="#5BC8FF", tag="CLAUDE FEATURE 05", w1="Claude ko", w2="Sab Yaad", w3="Hai?",
        card="""<div class=bub class=me style="background:rgba(91,200,255,.25);border-color:#5BC8FF">Mera naam Rahul hai</div>
<div class=bub>Hi Rahul! Yaad hai 👍</div>
<div class=mem><h4>MEMORY <span class=dl>DELETE &#10005;</span></h4><span class=chip><b>ROLE</b> student</span><span class=chip><b>PROJECT</b> thesis</span><span class=chip><b>STYLE</b> short answers</span>
<div class=tog><span>Generate memory</span><div class=sw><i></i></div></div></div>""",
        extra=""),
}


def render(key):
    from playwright.sync_api import sync_playwright
    t = THUMBS[key]
    import base64
    def b64(n): return "data:font/ttf;base64," + base64.b64encode((FONTS / n).read_bytes()).decode()
    css = CSS % dict(px=b64("Poppins-ExtraBold.ttf"), pb=b64("Poppins-Bold.ttf"), pm=b64("Poppins-Medium.ttf"))
    html = HTML % dict(css=css, **t)
    out = OUT / f"{key}_16x9.png"
    with sync_playwright() as p:
        b = p.chromium.launch(); pg = b.new_page(viewport={"width": 1280, "height": 720}, device_scale_factor=1)
        pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
        pg.screenshot(path=str(out)); b.close()
    print("wrote", out, out.stat().st_size // 1024, "KB")
    return out


if __name__ == "__main__":
    keys = list(THUMBS) if sys.argv[1:] == ["all"] or not sys.argv[1:] else sys.argv[1:]
    for k in keys: render(k)
