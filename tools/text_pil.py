"""Hindi (Devanagari) text sprites with Pillow + libraqm (HarfBuzz).

Why: the libass inside the cloud's ffmpeg (Ubuntu 6.1.1 and the static 7.0.2 build) mis-shapes Devanagari (visible halant,
lost nuqta; Munshi final 2026-10-30). Pillow's RAQM layout shapes the same text correctly. The Windows ffmpeg on the PC is
fine, so callers use `available()` to choose the engine.

Sizes: an ASS font size is the line height (ascent+descent) of the font, so for Mukta px = ASS size / 1.662.
"""
from pathlib import Path

import numpy as np
from PIL import Image, ImageDraw, ImageFont, features

ROOT = Path(__file__).resolve().parent.parent
FONT_DIR = ROOT / "shared/fonts"
MUKTA_ASC, MUKTA_DESC = 1.130, 0.532  # per em (Mukta hhea, measured with getmetrics at 1000)
HL_DEFAULT = (255, 214, 10)


def available() -> bool:
    return bool(features.check("raqm"))


def _font(name: str, px: float):
    return ImageFont.truetype(str(FONT_DIR / f"{name}.ttf"), max(1, int(round(px))), layout_engine=ImageFont.Layout.RAQM)


def _tokens(text: str):
    """'a *b* c' -> [('a', False), ('b', True), ('c', False)] (a *...* run may hold several words)."""
    out, hl = [], False
    for part in text.split("*"):
        out += [(w, hl) for w in part.split(" ") if w]
        hl = not hl
    return out


def _wrap(tokens, font, maxw):
    lines, cur = [], []
    for tk in tokens:
        trial = " ".join(w for w, _ in cur + [tk])
        if cur and maxw and font.getlength(trial) > maxw:
            lines.append(cur)
            cur = [tk]
        else:
            cur.append(tk)
    if cur:
        lines.append(cur)
    return lines


def render(text, style, maxw=None, max_lines=None, hl=HL_DEFAULT):
    """Text -> RGBA numpy array (H, W, 4) with the text, outline/shadow or ONE box behind all lines.
    style: {size (ASS size), font, fill (r,g,b), opacity, outline (px), outline_rgba (r,g,b,a 0-1), shadow (px),
            shadow_rgba, box (rgba or None; padded by `outline`), bold_stroke}
    If max_lines is set and the text needs more, the size shrinks (down to 70 %) until it fits."""
    name = style.get("font", "Mukta-Bold")
    scale = 1.0
    while True:
        px = style["size"] / (MUKTA_ASC + MUKTA_DESC) * scale
        font = _font(name, px)
        lines = _wrap(_tokens(text), font, maxw)
        if not max_lines or len(lines) <= max_lines or scale <= 0.7:
            break
        scale -= 0.05
    asc, line_h = MUKTA_ASC * px, (MUKTA_ASC + MUKTA_DESC) * px
    widths = [font.getlength(" ".join(w for w, _ in ln)) for ln in lines]
    ol, sh = float(style.get("outline", 0)), float(style.get("shadow", 0))
    box = style.get("box")
    pad = int(round(ol + sh + 6))
    W = int(max(widths)) + 2 * pad + 2
    H = int(round(line_h * len(lines))) + 2 * pad
    fill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    stroke = Image.new("L", (W, H), 0)
    shadow = Image.new("L", (W, H), 0)
    fm = {False: Image.new("L", (W, H), 0), True: Image.new("L", (W, H), 0)}
    sw = 0 if box else int(round(ol))
    for i, (ln, w) in enumerate(zip(lines, widths)):
        x = (W - w) / 2
        y = pad + i * line_h + asc
        for j, (word, is_hl) in enumerate(ln):
            pre = " ".join(t for t, _ in ln[:j])
            xx = x + (font.getlength(pre + " ") if pre else 0)
            ImageDraw.Draw(fm[is_hl]).text((xx, y), word, font=font, fill=255, anchor="ls")
            if sw:
                ImageDraw.Draw(stroke).text((xx, y), word, font=font, fill=255, anchor="ls", stroke_width=sw)
            if sh:
                ImageDraw.Draw(shadow).text((xx + sh, y + sh), word, font=font, fill=255, anchor="ls", stroke_width=sw)
    out = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    if box:
        x0 = (W - max(widths)) / 2 - ol
        d = ImageDraw.Draw(out)
        d.rectangle([x0, pad - ol, x0 + max(widths) + 2 * ol, pad + line_h * len(lines) + ol],
                    fill=(*box[:3], int(round(255 * box[3]))))
    def layer(mask, rgb, op):
        a = mask.point(lambda v: int(v * op))
        return Image.merge("RGBA", (*[Image.new("L", (W, H), c) for c in rgb], a))
    if sh:
        out = Image.alpha_composite(out, layer(shadow, style["shadow_rgba"][:3], style["shadow_rgba"][3]))
    if sw:
        out = Image.alpha_composite(out, layer(stroke, style["outline_rgba"][:3], style["outline_rgba"][3]))
    op = style.get("opacity", 1.0)
    out = Image.alpha_composite(out, layer(fm[False], style["fill"], op))
    out = Image.alpha_composite(out, layer(fm[True], hl, op))
    return np.asarray(out)


def blend(frame_bgr: np.ndarray, sprite_rgba: np.ndarray, x: int, y: int, fade: float = 1.0):
    """Alpha-blend a sprite onto a BGR frame in place at top-left (x, y); fade 0-1 scales its alpha."""
    h, w = sprite_rgba.shape[:2]
    fh, fw = frame_bgr.shape[:2]
    x0, y0, x1, y1 = max(x, 0), max(y, 0), min(x + w, fw), min(y + h, fh)
    if x1 <= x0 or y1 <= y0 or fade <= 0:
        return
    s = sprite_rgba[y0 - y:y1 - y, x0 - x:x1 - x]
    a = (s[..., 3:4].astype(np.float32) / 255.0) * fade
    dst = frame_bgr[y0:y1, x0:x1].astype(np.float32)
    frame_bgr[y0:y1, x0:x1] = (dst * (1 - a) + s[..., 2::-1].astype(np.float32) * a).astype(np.uint8)
