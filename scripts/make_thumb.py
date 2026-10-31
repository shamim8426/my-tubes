r"""Thumbnails for the yellow Bot channel, made from HTML (free, real Chrome via Playwright).

    .venv\Scripts\python -X utf8 scripts\make_thumb.py <story folder> [--all]

Reads <story>/thumb.json, writes <story>/output/thumb_16x9.png (1280x720) and thumb_9x16.png (1080x1920).
thumb.json: {"tag": "CLAUDE CODE", "title": "Claude ke <mark>tools</mark>", "sub": "kaun <b>poochta</b> hai?", "chips": ["Read","Edit","Bash"],
             "robot": "work", "ts_h": 118, "ts_v": 160}
robot = one of mascot/<name>.png (wave, think, work, stop, thumbs). --all: every story under channels/yellow-bot/stories that has a thumb.json."""
import html
import sys
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFilter
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
CH = ROOT / "channels/yellow-bot"
TEMPLATE = CH / "templates/thumb_template.html"
CUT = CH / "mascot/cut"


def cutout(name):
    """Transparent robot (white background connected to the border removed); cached in mascot/cut/."""
    out = CUT / f"{name}.png"
    if out.exists():
        return out
    CUT.mkdir(exist_ok=True)
    im = Image.open(CH / f"mascot/{name}.png").convert("RGB")
    work, key = im.copy(), (255, 0, 255)
    for seed in ((0, 0), (im.width - 1, 0), (0, im.height - 1), (im.width - 1, im.height - 1)):
        if work.getpixel(seed) != key:
            ImageDraw.floodfill(work, seed, key, thresh=26)
    a = np.asarray(work)
    bg = (a[:, :, 0] == 255) & (a[:, :, 1] == 0) & (a[:, :, 2] == 255)
    mask = Image.fromarray(np.where(bg, 0, 255).astype("uint8")).filter(ImageFilter.MinFilter(3)).filter(ImageFilter.GaussianBlur(1.0))
    rgba = im.convert("RGBA")
    rgba.putalpha(mask)
    rgba.crop(rgba.getbbox()).save(out)
    return out


def page(spec, fmt):
    t = TEMPLATE.read_text(encoding="utf-8")
    chips = "".join(f'<span class="chip">{html.escape(c)}</span>' for c in spec.get("chips", []))
    ts = spec.get("ts_" + fmt)
    rep = {"{{FONTS}}": (ROOT / "shared/fonts").as_uri(), "{{FORMAT}}": fmt, "{{ROBOT}}": cutout(spec.get("robot", "wave")).as_uri(),
           "{{TAG}}": html.escape(spec.get("tag", "CLAUDE CODE")), "{{TITLE}}": spec["title"], "{{SUB}}": spec.get("sub", ""),
           "{{CHIPS}}": chips, "{{TS}}": f"--ts:{ts}px" if ts else "", "{{SY}}": f"--sy:{spec['sy_' + fmt]}px" if spec.get("sy_" + fmt) else ""}
    for k, v in rep.items():
        t = t.replace(k, v)
    return t


def render(story):
    import json
    story = Path(story).resolve()
    spec = json.loads((story / "thumb.json").read_text(encoding="utf-8-sig"))
    out = story / "output"
    out.mkdir(exist_ok=True)
    tmp = story / "build"
    tmp.mkdir(exist_ok=True)
    with sync_playwright() as p:
        try:
            b = p.chromium.launch(channel="chrome")
        except Exception:
            b = p.chromium.launch()
        for fmt, size, name in (("h", (1280, 720), "thumb_16x9.png"), ("v", (1080, 1920), "thumb_9x16.png")):
            f = tmp / f"thumb_{fmt}.html"
            f.write_text(page(spec, fmt), encoding="utf-8")
            pg = b.new_page(viewport={"width": size[0], "height": size[1]})
            pg.goto(f.as_uri())
            pg.wait_for_timeout(600)
            pg.screenshot(path=str(out / name))
            pg.close()
        b.close()
    print("thumbs ->", out)


def main():
    if "--all" in sys.argv:
        for d in sorted((CH / "stories").iterdir()):
            if (d / "thumb.json").exists():
                render(d)
    else:
        render(sys.argv[1])


if __name__ == "__main__":
    main()
