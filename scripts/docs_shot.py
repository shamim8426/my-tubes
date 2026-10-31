"""Screenshot a region of a public docs page (real Chrome via Playwright, free) for the scrolling "docs card" scene.

    .venv\\Scripts\\python -X utf8 scripts\\docs_shot.py <url> <out.png> --find "text on the page" [--before 380] [--height 1900] [--width 1000]

The region starts `before` px above the first element containing --find (falls back to the top of the page). The shot is a tall
PNG at 1.5x; the video scene scrolls it inside a browser-window card. Only used for pages the channel credits as its source."""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright


def arg(name, default):
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv else default


def main():
    url, out = sys.argv[1], Path(sys.argv[2])
    find, before, height, width = arg("--find", ""), int(arg("--before", 380)), int(arg("--height", 1900)), int(arg("--width", 1000))
    out.parent.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as p:
        b = p.chromium.launch(channel="chrome")
        pg = b.new_page(viewport={"width": width, "height": 1200}, device_scale_factor=1.5, color_scheme="light")
        pg.goto(url, wait_until="domcontentloaded", timeout=60000)
        pg.wait_for_timeout(2500)
        # remove cookie banner, chat bar and any other fixed overlay so the shot shows only the page
        pg.evaluate("document.querySelectorAll('*').forEach(e => { const p = getComputedStyle(e).position; if (p === 'fixed' || p === 'sticky') e.style.display = 'none'; })")
        pg.wait_for_timeout(300)
        top = 0
        if find:
            loc = pg.get_by_text(find, exact=False).first
            try:
                top = int(loc.evaluate("e => e.getBoundingClientRect().top + window.scrollY", timeout=8000))
            except Exception:
                print(f"text not found: {find!r}, using the top of the page")
        y0 = max(0, top - before)
        pg.screenshot(path=str(out), full_page=True, clip={"x": 0, "y": y0, "width": width, "height": height})
        b.close()
    print(f"OK {out} (from y={y0})")


if __name__ == "__main__":
    main()
