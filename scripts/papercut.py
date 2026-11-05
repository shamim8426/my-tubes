"""Paper-cut look for real images (free, local): cut-out + white paper border with a slightly rough edge + soft drop shadow.
    from papercut import cutout_grabcut, cutout_white, sticker, paper_rect
    sticker(rgba_image, border=18, rough=2.2, shadow=True, seed=1)  -> RGBA PIL image (transparent outside the paper)
    paper_rect(rgb_image, border=22, torn=True)                      -> same look for a rectangular screenshot / photo
"""
import numpy as np
import cv2
from PIL import Image


def cutout_grabcut(img, rect=None, iters=6):
    """Background removal for a photo with a fairly plain/contrasting background (OpenCV GrabCut). rect=(x,y,w,h) around the object."""
    bgr = cv2.cvtColor(np.array(img.convert("RGB")), cv2.COLOR_RGB2BGR)
    h, w = bgr.shape[:2]
    rect = rect or (int(w * .03), int(h * .03), int(w * .94), int(h * .94))
    mask = np.zeros((h, w), np.uint8)
    bg, fg = np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64)
    cv2.grabCut(bgr, mask, rect, bg, fg, iters, cv2.GC_INIT_WITH_RECT)
    m = np.where((mask == 1) | (mask == 3), 255, 0).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((5, 5), np.uint8))
    m = cv2.morphologyEx(m, cv2.MORPH_CLOSE, np.ones((9, 9), np.uint8))
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:  # keep the biggest blob, fill holes
        k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); m = np.where(lab == k, 255, 0).astype(np.uint8)
        cnt, _ = cv2.findContours(m, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE); m[:] = 0; cv2.drawContours(m, cnt, -1, 255, -1)
    m = cv2.GaussianBlur(m, (5, 5), 0)
    out = img.convert("RGBA"); out.putalpha(Image.fromarray(m)); return out


def cutout_white(img, thr=238):
    """Background removal for a picture on (near) white: flood-fill the white from the borders."""
    rgb = np.array(img.convert("RGB")); h, w = rgb.shape[:2]
    white = (rgb.min(axis=2) >= thr).astype(np.uint8) * 255
    ff = white.copy(); mask = np.zeros((h + 2, w + 2), np.uint8)
    for p in [(0, 0), (w - 1, 0), (0, h - 1), (w - 1, h - 1)]:
        if ff[p[1], p[0]] == 255: cv2.floodFill(ff, mask, p, 128)
    m = np.where(ff == 128, 0, 255).astype(np.uint8)
    m = cv2.morphologyEx(m, cv2.MORPH_OPEN, np.ones((9, 9), np.uint8))  # drops thin grid lines
    n, lab, st, _ = cv2.connectedComponentsWithStats(m)
    if n > 1:
        k = 1 + int(np.argmax(st[1:, cv2.CC_STAT_AREA])); m = np.where(lab == k, 255, 0).astype(np.uint8)
    out = img.convert("RGBA"); out.putalpha(Image.fromarray(cv2.GaussianBlur(m, (3, 3), 0))); return out


def _rough(mask, rough, rng):
    if rough <= 0: return mask
    h, w = mask.shape
    n = rng.standard_normal((h // 8 + 2, w // 8 + 2)).astype(np.float32)
    n = cv2.resize(n, (w, h), interpolation=cv2.INTER_CUBIC) * rough * 4
    soft = cv2.GaussianBlur(mask.astype(np.float32), (0, 0), rough * 1.5)
    return np.where(soft + n * 6 > 127, 255, 0).astype(np.uint8)


def sticker(rgba, border=18, rough=2.2, shadow=True, seed=1, pad=60):
    rng = np.random.default_rng(seed)
    a = np.array(rgba.split()[3]); h, w = a.shape
    canvas = np.zeros((h + 2 * pad, w + 2 * pad), np.uint8); canvas[pad:pad + h, pad:pad + w] = a
    big = np.zeros((h + 2 * pad, w + 2 * pad, 4), np.uint8); big[pad:pad + h, pad:pad + w] = np.array(rgba)
    k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (2 * border + 1, 2 * border + 1))
    paper = _rough(cv2.dilate((canvas > 100).astype(np.uint8) * 255, k), rough, rng)
    paper = cv2.GaussianBlur(paper, (3, 3), 0)
    out = np.zeros_like(big)
    out[..., :3] = 250; out[..., 3] = paper  # white paper
    # light paper grain on the border
    grain = rng.normal(0, 3, paper.shape).astype(np.int16); out[..., :3] = np.clip(out[..., :3].astype(np.int16) + grain[..., None], 0, 255).astype(np.uint8)
    img = Image.fromarray(out)
    obj = Image.fromarray(big)
    img.alpha_composite(obj)
    # thin edge line for depth
    edge = cv2.Canny(paper, 50, 150); edge = cv2.GaussianBlur(edge, (3, 3), 0)
    res = np.array(img); res[..., :3] = np.where(edge[..., None] > 30, (res[..., :3] * .85).astype(np.uint8), res[..., :3]); img = Image.fromarray(res)
    if shadow:
        sh = Image.new("RGBA", img.size, (0, 0, 0, 0)); sa = cv2.GaussianBlur(paper, (0, 0), 14).astype(np.float32) * .30
        sh_arr = np.zeros((img.size[1], img.size[0], 4), np.uint8); sh_arr[..., 3] = np.roll(np.roll(sa, 16, 0), 8, 1).astype(np.uint8)
        sh = Image.fromarray(sh_arr); sh.alpha_composite(img); img = sh
    bbox = img.getbbox()
    return img.crop(bbox) if bbox else img


def paper_rect(img, border=22, torn=True, seed=2, pad=60, shadow=True):
    rgba = img.convert("RGBA"); w, h = rgba.size
    return sticker(rgba, border=border, rough=2.6 if torn else 0, shadow=shadow, seed=seed, pad=pad)
