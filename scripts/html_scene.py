"""Render an HTML/SVG slide scene to stills (proof of the presentation-style pipeline). Real Chrome via Playwright (no browser download).

    .venv\\Scripts\\python -X utf8 scripts\\html_scene.py <scene.html> <out_dir> <t1,t2,...>      # stills at those seconds
The HTML must expose setT(seconds). A video render is the same loop at 30 fps piped to ffmpeg (next step, not done here).
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def main():
    html, out, times = Path(sys.argv[1]).resolve(), Path(sys.argv[2]), [float(x) for x in sys.argv[3].split(",")]
    out.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="chrome")
        except Exception:  # cloud Linux has no Chrome: use the Chromium that Playwright installs
            b = p.chromium.launch()
        pg = b.new_page(viewport={"width": 1080, "height": 1920})
        pg.goto(html.as_uri())
        wh = pg.evaluate("typeof W==='number'?[W,H]:[1080,1920]")
        pg.set_viewport_size({"width": wh[0], "height": wh[1]})  # landscape decks: 1920x1080
        pg.evaluate("document.fonts.ready")
        for t in times:
            pg.evaluate(f"setT({t})")
            pg.screenshot(path=str(out / f"t_{t:05.2f}.png"))
        b.close()
    print("stills ->", out)


if __name__ == "__main__":
    main()
