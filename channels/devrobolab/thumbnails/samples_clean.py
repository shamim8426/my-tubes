r"""Thumbnail SAMPLES in the 'clean editorial' look (2026-11-07, learned from a competitor's Shorts: light grey frame, one hero picture with a soft shadow, mixed light/bold words, a black label with white words,
small channel watermark; the 16:9 version = the vertical frame in the middle of a blurred bigger copy). Our own pictures only, no copied elements.
    .venv\Scripts\python -X utf8 channels\devrobolab\thumbnails\samples_clean.py"""
import base64
from pathlib import Path

from PIL import Image, ImageFilter

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
OUT = HERE / "out" / "clean"; OUT.mkdir(parents=True, exist_ok=True)
FONTS = ROOT / "shared/fonts"
MASCOT = ROOT / "channels/devrobolab/mascot/cut"


def b64(p, mime): return f"data:{mime};base64," + base64.b64encode(Path(p).read_bytes()).decode()


CSS = """<style>
@font-face{font-family:PX;src:url('@@PX@@');font-weight:800}
@font-face{font-family:PB;src:url('@@PB@@');font-weight:700}
@font-face{font-family:PM;src:url('@@PM@@');font-weight:500}
*{box-sizing:border-box;margin:0;padding:0}
body{width:1080px;height:1920px;position:relative;overflow:hidden;background:#f2f2f2;color:#1b1b1f;font-family:PM,sans-serif}
.grid{position:absolute;inset:0;background-image:linear-gradient(rgba(0,0,0,.045) 2px,transparent 2px),linear-gradient(90deg,rgba(0,0,0,.045) 2px,transparent 2px);background-size:90px 90px;mask-image:radial-gradient(900px 1100px at 50% 40%,#000 30%,transparent 80%)}
.ghost{position:absolute;opacity:.07}
.circ{position:absolute;border-radius:50%;background:#fff;box-shadow:0 18px 40px rgba(0,0,0,.18),0 4px 10px rgba(0,0,0,.08);display:flex;align-items:center;justify-content:center}
.card{position:absolute;background:#fff;border-radius:40px;box-shadow:0 30px 70px rgba(0,0,0,.22),0 6px 16px rgba(0,0,0,.08)}
.t{position:absolute;left:0;width:1080px;text-align:center}
.lt{font:500 70px PM;color:#5b5b63}.bd{font:800 96px PX;color:#111}
.lab{display:inline-block;background:#0e0e11;color:#fff;font:700 74px PB;padding:6px 34px 12px;border-radius:12px;box-shadow:0 14px 30px rgba(0,0,0,.3)}
.wm{position:absolute;left:0;width:1080px;text-align:center;bottom:70px;font:700 44px PB;color:rgba(0,0,0,.28);letter-spacing:1px}
img{position:absolute}
.line{position:absolute;background:#1b1b1f;opacity:.55}
</style>"""

ICON = {
    "bolt": '<svg width="@@S@@" height="@@S@@" viewBox="0 0 40 40"><path d="M23 2L7 23h10l-3 15 19-24H22z" fill="#FFC800" stroke="#14213d" stroke-width="2.5" stroke-linejoin="round"/></svg>',
    "term": '<svg width="@@S@@" height="@@S@@" viewBox="0 0 40 40"><rect x="3" y="6" width="34" height="28" rx="6" fill="#14213d"/><path d="M10 15l7 5-7 5M20 27h10" fill="none" stroke="#7cf0a8" stroke-width="3" stroke-linecap="round" stroke-linejoin="round"/></svg>',
    "clock": '<svg width="@@S@@" height="@@S@@" viewBox="0 0 40 40"><circle cx="20" cy="20" r="16" fill="#fff" stroke="#14213d" stroke-width="3"/><path d="M20 10v11l7 4" fill="none" stroke="#14213d" stroke-width="3" stroke-linecap="round"/></svg>',
    "photo": '<svg width="@@S@@" height="@@S@@" viewBox="0 0 40 40"><rect x="4" y="7" width="32" height="26" rx="5" fill="#bfe0ff" stroke="#14213d" stroke-width="3"/><circle cx="14" cy="16" r="4" fill="#FFC800"/><path d="M6 31l9-9 7 6 5-4 7 7" fill="#8fe3a8" stroke="#14213d" stroke-width="2.5" stroke-linejoin="round"/></svg>',
    "file": '<svg width="@@S@@" height="@@S@@" viewBox="0 0 40 40"><path d="M9 3h16l8 8v26H9z" fill="#fff" stroke="#14213d" stroke-width="3" stroke-linejoin="round"/><path d="M25 3v8h8M14 20h14M14 26h14M14 32h9" fill="none" stroke="#14213d" stroke-width="2.5" stroke-linecap="round"/></svg>',
    "star": '<svg width="@@S@@" height="@@S@@" viewBox="0 0 40 40"><path d="M20 2c2 10 8 16 18 18-10 2-16 8-18 18-2-10-8-16-18-18C12 18 18 12 20 2z" fill="#D97757" stroke="#14213d" stroke-width="2" stroke-linejoin="round"/></svg>',
    "hook": '<svg width="@@S@@" height="@@S@@" viewBox="0 0 40 40"><path d="M20 4v18a8 8 0 1 1-8-8" fill="none" stroke="#14213d" stroke-width="4" stroke-linecap="round"/><circle cx="20" cy="6" r="3.5" fill="#FFC800" stroke="#14213d" stroke-width="2"/></svg>',
    "gear": '<svg width="@@S@@" height="@@S@@" viewBox="0 0 40 40"><circle cx="20" cy="20" r="7" fill="#fff" stroke="#14213d" stroke-width="3"/><path d="M20 3v6M20 31v6M3 20h6M31 20h6M8 8l4 4M28 28l4 4M32 8l-4 4M12 28l-4 4" stroke="#14213d" stroke-width="4" stroke-linecap="round"/></svg>',
}


def ic(name, size): return ICON[name].replace("@@S@@", str(size))


def circ(x, y, d, icon, ratio=0.55):
    return f'<div class=circ style="left:{x}px;top:{y}px;width:{d}px;height:{d}px">{ic(icon, int(d * ratio))}</div>'


A = CSS + f"""<body><div class=grid></div>
<div class=ghost style="left:-120px;top:120px">{ic('bolt', 720)}</div>
{circ(390, 330, 300, 'bolt', .62)}
{circ(120, 400, 190, 'term')}{circ(780, 420, 200, 'clock')}{circ(110, 700, 160, 'star', .5)}{circ(810, 690, 160, 'gear', .5)}
<div class=card style="left:300px;top:690px;width:480px;height:170px;display:flex;align-items:center;justify-content:center;font:800 120px PX;color:#111">2.5x</div>
<div class=t style="top:1060px"><div class=lt>Claude Code</div><div class=bd>ab 2.5x tez</div><div style="margin-top:22px"><span class=lab>/fast se</span></div></div>
<div class=wm>devrobolab</div></body>"""

B = CSS + f"""<body><div class=grid></div>
<div class=ghost style="right:-140px;top:140px">{ic('file', 760)}</div>
<div class=card style="left:290px;top:230px;width:500px;height:640px;transform:rotate(-4deg);padding:56px 48px">
  <div style="width:150px;height:56px;border-radius:12px;background:#e5484d;color:#fff;font:800 38px PX;text-align:center;line-height:56px">PDF</div>
  <div style="height:22px;border-radius:12px;background:#e6e6ea;margin-top:46px"></div><div style="height:22px;border-radius:12px;background:#e6e6ea;margin-top:26px;width:85%"></div>
  <div style="height:22px;border-radius:12px;background:#e6e6ea;margin-top:26px"></div><div style="height:22px;border-radius:12px;background:#e6e6ea;margin-top:26px;width:70%"></div>
  <div style="height:22px;border-radius:12px;background:#e6e6ea;margin-top:26px;width:90%"></div></div>
{circ(110, 420, 200, 'photo', .6)}{circ(780, 640, 230, 'star', .6)}
<div class=t style="top:1060px"><div class=lt>Claude ko</div><div class=bd>PDF aur photo do</div><div style="margin-top:22px"><span class=lab>sawal poochho</span></div></div>
<div class=wm>devrobolab</div></body>"""

C = CSS + f"""<body><div class=grid></div>
<div class=ghost style="left:-100px;top:100px">{ic('hook', 760)}</div>
<div class=line style="left:536px;top:560px;width:6px;height:150px"></div>
<div class=line style="left:330px;top:560px;width:430px;height:6px"></div><div class=line style="left:330px;top:560px;width:6px;height:150px"></div><div class=line style="left:754px;top:560px;width:6px;height:150px"></div>
{circ(420, 230, 240, 'file', .55)}
{circ(205, 700, 250, 'file', .55)}{circ(415, 700, 250, 'star', .55)}{circ(625, 700, 250, 'hook', .55)}
<div style="position:absolute;left:150px;top:980px;width:780px;display:flex;justify-content:space-between;font:800 44px PX;color:#111"><span style="width:250px;text-align:center">CLAUDE.md</span><span style="width:250px;text-align:center">Skill</span><span style="width:250px;text-align:center">Hook</span></div>
<div class=t style="top:1110px"><div class=lt>Kaunsa use karein</div><div class=bd>kab, kahan?</div><div style="margin-top:22px"><span class=lab>CLAUDE.md, Skill ya Hook</span></div></div>
<img src="@@ROBOT@@" style="right:50px;bottom:105px;height:290px">
<div class=wm>devrobolab</div></body>"""


def compose169(png9, out):
    im = Image.open(png9).convert("RGB")
    bg = im.resize((1280, int(1920 * 1280 / 1080)), Image.LANCZOS)
    top = (bg.height - 720) // 2 + 120
    bg = bg.crop((0, top, 1280, top + 720)).filter(ImageFilter.GaussianBlur(14))
    front = im.resize((405, 720), Image.LANCZOS)
    sh = Image.new("RGBA", (405 + 120, 720 + 120), (0, 0, 0, 0))
    from PIL import ImageDraw
    ImageDraw.Draw(sh).rectangle([60, 70, 60 + 405, 70 + 720], fill=(0, 0, 0, 70)); sh = sh.filter(ImageFilter.GaussianBlur(22))
    c = bg.convert("RGBA"); c.alpha_composite(sh, ((1280 - 405) // 2 - 60, -30)); c.paste(front, ((1280 - 405) // 2, 0))
    c.convert("RGB").save(out)


def main():
    from playwright.sync_api import sync_playwright
    px, pb, pm = (b64(FONTS / n, "font/ttf") for n in ("Poppins-ExtraBold.ttf", "Poppins-Bold.ttf", "Poppins-Medium.ttf"))
    robot = b64(MASCOT / "think.png", "image/png")
    jobs = [("A_fast", A), ("B_pdf", B), ("C_skill_hook", C)]
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, html in jobs:
            html = html.replace("@@PX@@", px).replace("@@PB@@", pb).replace("@@PM@@", pm).replace("@@ROBOT@@", robot)
            pg = b.new_page(viewport={"width": 1080, "height": 1920}); pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
            f9 = OUT / f"{name}_9x16.png"; pg.screenshot(path=str(f9)); pg.close()
            compose169(f9, OUT / f"{name}_16x9.png"); print("wrote", name)
        b.close()


if __name__ == "__main__":
    main()
