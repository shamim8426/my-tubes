r"""DevRoboLab thumbnail SAMPLES v3 (2026-11-07, after the user's feedback): light clean background, SMALLER words, the DevRoboLab robot, and a picture that shows how it works.
    .venv\Scripts\python -X utf8 channels\devrobolab\thumbnails\samples_v3.py"""
import base64
from pathlib import Path

HERE = Path(__file__).parent
ROOT = HERE.parents[2]
FONTS = ROOT / "shared/fonts"
MASCOT = ROOT / "channels/devrobolab/mascot/cut"
OUT = HERE / "out"; OUT.mkdir(exist_ok=True)


def b64(path, mime):
    return f"data:{mime};base64," + base64.b64encode(Path(path).read_bytes()).decode()


BASE = """<style>
@font-face{font-family:PX;src:url('@@PX@@');font-weight:800}
@font-face{font-family:PB;src:url('@@PB@@');font-weight:700}
@font-face{font-family:PM;src:url('@@PM@@');font-weight:500}
*{box-sizing:border-box;margin:0;padding:0}
:root{--ink:#14213d;--y:#FFC800}
body{position:relative;overflow:hidden;font-family:PB,sans-serif;color:var(--ink)}
.tag{position:absolute;font:700 26px PB;letter-spacing:2px;background:var(--ink);color:var(--y);padding:9px 22px;border-radius:999px}
.ttl{position:absolute;font-family:PX;font-weight:800;line-height:1.08}
mark{background:var(--y);color:var(--ink);padding:0 .12em;border-radius:.14em}
.card{background:#fff;border:4px solid var(--ink);border-radius:24px;box-shadow:8px 8px 0 var(--ink);padding:18px}
.bub{font:700 28px PB;line-height:1.2}
.lab{font:700 24px PB;text-align:center;margin-top:16px}
.lab b{background:var(--ink);color:var(--y);border-radius:50%;display:inline-block;width:34px;height:34px;line-height:34px;font-size:22px;margin-right:8px}
.brand{position:absolute;font:800 26px PX}.brand span{background:var(--y);padding:0 6px;border-radius:6px}
img{position:absolute}
.arrow{position:absolute}
</style>"""

A = BASE + """<body style="width:1280px;height:720px;background:#FFFAEB">
<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(20,33,61,.12) 2px,transparent 2px);background-size:34px 34px"></div>
<div style="position:absolute;left:-120px;top:120px;width:640px;height:640px;border-radius:50%;background:#FFE680"></div>
<div class=tag style="left:40px;top:36px">CLAUDE FEATURE 05</div>
<img src="@@THINK@@" style="left:20px;bottom:-14px;height:610px">
<div class=ttl style="left:440px;top:30px;font-size:72px">Claude ko sab<br><mark>yaad</mark> hai?</div>
<div style="position:absolute;left:400px;top:235px;width:850px;display:flex;align-items:center;gap:6px">
  <div style="width:250px"><div class=card><div class=bub style="font-size:26px">Mera naam Rahul hai</div></div><div class=lab><b>1</b>Aap bolte ho</div></div>
  <svg width="44" height="40" viewBox="0 0 56 40"><path d="M2 20h40M30 6l14 14-14 14" fill="none" stroke="#14213d" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <div style="width:285px"><div class=card style="padding:0;overflow:hidden"><div style="background:var(--y);padding:10px 16px;font:800 24px PX;display:flex;justify-content:space-between;align-items:center">MEMORY<span style="background:#ff4d5e;color:#fff;font-size:17px;padding:4px 10px;border-radius:8px">DELETE &#10005;</span></div>
    <div style="padding:12px 16px;font:700 24px PB;line-height:1.75">
    <div><svg width="26" height="20" viewBox="0 0 26 20"><path d="M1 3h8l3 3h13v13H1z" fill="#FFC800" stroke="#14213d" stroke-width="2"/></svg> Role: student</div>
    <div><svg width="26" height="20" viewBox="0 0 26 20"><path d="M1 3h8l3 3h13v13H1z" fill="#FFC800" stroke="#14213d" stroke-width="2"/></svg> Project: thesis</div>
    <div><svg width="26" height="20" viewBox="0 0 26 20"><path d="M1 3h8l3 3h13v13H1z" fill="#FFC800" stroke="#14213d" stroke-width="2"/></svg> Style: short</div></div></div><div class=lab><b>2</b>Claude yaad rakhta hai</div></div>
  <svg width="44" height="40" viewBox="0 0 56 40"><path d="M2 20h40M30 6l14 14-14 14" fill="none" stroke="#14213d" stroke-width="7" stroke-linecap="round" stroke-linejoin="round"/></svg>
  <div style="width:215px"><div class=card style="background:#E8F7EC"><div class=bub style="font-size:26px">Hi Rahul! Yaad hai</div></div><div class=lab><b>3</b>Agli chat me bhi</div></div>
</div>
<div class=brand style="right:40px;top:40px;color:var(--ink)">Dev<span>Robo</span>Lab</div>
</body>"""

B = BASE + """<body style="width:1280px;height:720px;background:#E8F3FF">
<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(20,33,61,.10) 2px,transparent 2px);background-size:34px 34px"></div>
<div style="position:absolute;right:-100px;top:140px;width:640px;height:640px;border-radius:50%;background:#BFE0FF"></div>
<div class=tag style="left:40px;top:36px">CLAUDE CODE 03</div>
<div class=ttl style="left:40px;top:96px;font-size:60px;width:720px">Aapke <mark>.claude</mark> folder<br>me kya hai?</div>
<img src="@@WORK@@" style="right:10px;bottom:-14px;height:520px">
<svg style="position:absolute;left:30px;top:330px" width="300" height="200" viewBox="0 0 440 280"><path d="M10 40q0-20 20-20h110l30 34h250q20 0 20 20v176q0 20-20 20H30q-20 0-20-20z" fill="#FFC800" stroke="#14213d" stroke-width="8" stroke-linejoin="round"/><path d="M10 90h420" stroke="#14213d" stroke-width="8"/></svg>
<div style="position:absolute;left:350px;top:260px;width:560px;height:400px">
  <div class=card style="position:absolute;left:0;top:0;width:260px;transform:rotate(-3deg)"><div style="font:800 22px PX;background:#FFC800;border-radius:10px;padding:4px 10px;display:inline-block">CLAUDE.md</div><div class=bub style="font-size:22px;margin-top:8px">instructions</div></div>
  <div class=card style="position:absolute;left:285px;top:10px;width:260px;transform:rotate(3deg)"><div style="font:800 22px PX;background:#7CC6FF;border-radius:10px;padding:4px 10px;display:inline-block">settings.json</div><div class=bub style="font-size:22px;margin-top:8px">permissions</div></div>
  <div class=card style="position:absolute;left:10px;top:190px;width:260px;transform:rotate(2deg)"><div style="font:800 22px PX;background:#8FE3A8;border-radius:10px;padding:4px 10px;display:inline-block">skills/</div><div class=bub style="font-size:22px;margin-top:8px">reusable prompts</div></div>
  <div class=card style="position:absolute;left:285px;top:200px;width:260px;transform:rotate(-3deg)"><div style="font:800 22px PX;background:#FF9EC4;border-radius:10px;padding:4px 10px;display:inline-block">agents/</div><div class=bub style="font-size:22px;margin-top:8px">helpers</div></div>
</div>
<div class=brand style="right:40px;top:40px">Dev<span>Robo</span>Lab</div>
</body>"""

C = BASE + """<body style="width:1080px;height:1920px;background:#E6FAF0">
<div style="position:absolute;inset:0;background-image:radial-gradient(rgba(20,33,61,.10) 3px,transparent 3px);background-size:44px 44px"></div>
<div style="position:absolute;left:140px;top:1000px;width:900px;height:900px;border-radius:50%;background:#BFF0D6"></div>
<div class=tag style="left:60px;top:70px;font-size:38px;padding:12px 28px">CLAUDE CODE 02</div>
<div class=ttl style="left:60px;top:180px;font-size:104px;width:960px">Claude Code<br>ab <mark>2.5x</mark> tez</div>
<div class=card style="position:absolute;left:60px;top:560px;width:960px;padding:36px">
  <div style="font:700 34px PB;margin-bottom:8px">Normal</div>
  <div style="height:70px;border-radius:70px;background:#e5e7eb;border:4px solid var(--ink);overflow:hidden"><div style="width:40%;height:100%;background:#9aa3b2;display:flex;align-items:center;justify-content:flex-end;padding-right:18px;font:800 36px PX;color:#fff">1x</div></div>
  <div style="font:700 34px PB;margin:28px 0 8px;display:flex;align-items:center;gap:12px"><svg width="34" height="44" viewBox="0 0 34 44"><path d="M20 0L2 26h13l-3 18L32 16H19z" fill="#FFC800" stroke="#14213d" stroke-width="3" stroke-linejoin="round"/></svg>/fast</div>
  <div style="height:70px;border-radius:70px;background:#e5e7eb;border:4px solid var(--ink);overflow:hidden"><div style="width:100%;height:100%;background:linear-gradient(90deg,#FFC800,#FF9A1F);display:flex;align-items:center;justify-content:flex-end;padding-right:24px;font:800 44px PX;color:#14213d">2.5x</div></div>
</div>
<img src="@@WAVE@@" style="right:30px;bottom:30px;height:820px">
<div class=brand style="left:60px;bottom:70px;font-size:40px">Dev<span>Robo</span>Lab</div>
</body>"""


def main():
    from playwright.sync_api import sync_playwright
    px, pb, pm = (b64(FONTS / n, "font/ttf") for n in ("Poppins-ExtraBold.ttf", "Poppins-Bold.ttf", "Poppins-Medium.ttf"))
    imgs = {"THINK": b64(MASCOT / "think.png", "image/png"), "WORK": b64(MASCOT / "work.png", "image/png"), "WAVE": b64(MASCOT / "wave.png", "image/png")}
    jobs = [("v3_A_memory", A, 1280, 720), ("v3_B_claude_folder", B, 1280, 720), ("v3_C_fast_short", C, 1080, 1920)]
    with sync_playwright() as p:
        b = p.chromium.launch()
        for name, html, w, h in jobs:
            html = html.replace("@@PX@@", px).replace("@@PB@@", pb).replace("@@PM@@", pm)
            for k, v in imgs.items(): html = html.replace(f"@@{k}@@", v)
            pg = b.new_page(viewport={"width": w, "height": h}); pg.set_content(html); pg.evaluate("document.fonts.ready"); pg.wait_for_timeout(500)
            pg.screenshot(path=str(OUT / f"{name}.png")); pg.close(); print("wrote", name)
        b.close()


if __name__ == "__main__":
    main()
