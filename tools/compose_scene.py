"""Cut-out scenes for Jugnu Stories (cast v3, user 2026-11-01): the exact character PNGs on a background (free, local).

The characters are never redrawn by AI. Each scene = one background image + the cast PNGs
(channels/jugnu-stories/characters/<who>/<who>_<pose>.png, 1200x2000 transparent) placed on it. The output is the
normal images/scene_XX.png, so make_short.py / parallax.py build it like any other scene image.

    python tools/compose_scene.py <story folder or cutout_scenes.json> [--only 3,5] [--check] [--sheet]

cutout_scenes.json (in the story folder):
{
  "channel": "jugnu-stories",
  "out_dir": "images",                         # relative to the story folder
  "size": [1920, 1080],                        # optional; default = the background's size
  "backgrounds": {"aangan": "images/bg_aangan.png"},
  "scenes": [
    {"id": 1, "bg": "aangan",
     "cast": [
       {"who": "tinku", "pose": "point", "x": 0.35, "foot": 0.93, "h": 0.62},
       {"who": "bholu", "pose": "laugh", "x": 0.62, "foot": 0.90, "h": 0.60, "flip": true},
       {"who": "jugnu", "pose": "stand", "x": 0.80, "y": 0.30, "h": 0.12}
     ]}
  ]
}
Per character: x = centre (fraction of width); foot = where the soles touch the ground (fraction of height);
h = character height (fraction of height, from the top of the head to the soles); flip = mirror (face the other way).
Jugnu (firefly) flies: give "y" (centre) instead of "foot"; it gets no ground shadow.
Per scene: "light": day (default) / morning / evening / night or [r, g, b] factors, so the cast matches the background.
Draw order = far to near (smaller foot first), so nearer characters overlap farther ones.
Poses: stand, walk, point, think, happy, surprised, scared, laugh (new poses: characters/_source/).
--check validates paths/poses/placement only (writes nothing); --sheet also writes images/_cutout_sheet.jpg.
"""
import argparse
import json
import sys
from pathlib import Path

from PIL import Image, ImageDraw, ImageFilter

ROOT = Path(__file__).resolve().parents[1]
FLYING = {"jugnu"}
# scene "light": multiply the characters' colours so they sit in the background's light ([r, g, b] also accepted)
LIGHTS = {"day": (1.0, 1.0, 1.0), "morning": (1.0, 0.97, 0.90), "evening": (1.0, 0.86, 0.74), "night": (0.70, 0.76, 0.98)}
SAFE_X = (0.04, 0.96)  # keep characters off the very edge of the frame


def load_spec(arg: str):
    p = Path(arg)
    if p.is_dir():
        p = p / "cutout_scenes.json"
    if not p.exists():
        sys.exit(f"compose_scene: {p} not found")
    return json.loads(p.read_text(encoding="utf-8")), p.parent


def char_png(chars: Path, who: str, pose: str) -> Path:
    f = chars / who / f"{who}_{pose}.png"
    if not f.exists():
        have = sorted(x.stem.split("_")[-1] for x in (chars / who).glob(f"{who}_*.png") if not x.stem.endswith("_sheet"))
        if not have:
            sys.exit(f"compose_scene: no character '{who}' in {chars} (old cast is in characters/_old_cast/, not usable)")
        sys.exit(f"compose_scene: '{who}' has no pose '{pose}'; poses: {', '.join(have)}")
    return f


def cut(path: Path) -> Image.Image:
    """Character PNG cropped to its visible pixels (alpha bbox)."""
    im = Image.open(path).convert("RGBA")
    return im.crop(im.getchannel("A").getbbox())


def relight(im: Image.Image, light) -> Image.Image:
    k = LIGHTS[light] if isinstance(light, str) else tuple(light)
    if k == (1.0, 1.0, 1.0):
        return im
    r, g, b, a = im.split()
    r, g, b = (ch.point(lambda v, f=f: min(255, round(v * f))) for ch, f in zip((r, g, b), k))
    return Image.merge("RGBA", (r, g, b, a))


def place(bg: Image.Image, c: dict, chars: Path, warn: list, light="day") -> None:
    W, H = bg.size
    who, pose = c["who"], c.get("pose", "stand")
    im = relight(cut(char_png(chars, who, pose)), light)
    if c.get("flip"):
        im = im.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    th = max(8, round(c["h"] * H))
    tw = max(1, round(im.width * th / im.height))
    im = im.resize((tw, th), Image.Resampling.LANCZOS)
    cx = round(c["x"] * W)
    if who in FLYING or "y" in c:
        top = round(c.get("y", 0.3) * H) - th // 2
    else:
        foot = round(c["foot"] * H)
        top = foot - th
        # soft contact shadow under the feet: ellipse ~0.8 x the body width, blurred, multiplied onto the ground
        sw, sh = round(tw * 0.8), max(4, round(th * 0.045))
        sh_layer = Image.new("L", (sw + 40, sh + 40), 0)
        ImageDraw.Draw(sh_layer).ellipse((20, 20, 20 + sw, 20 + sh), fill=round(255 * c.get("shadow", 0.35)))
        sh_layer = sh_layer.filter(ImageFilter.GaussianBlur(max(2, sh // 3)))
        dark = Image.new("RGBA", sh_layer.size, (40, 25, 45, 255))
        dark.putalpha(sh_layer)
        bg.alpha_composite(dark, (cx - sw // 2 - 20, foot - sh // 2 - 20))
    left = cx - tw // 2
    if left < SAFE_X[0] * W or left + tw > SAFE_X[1] * W:
        warn.append(f"{who} touches the frame edge (x {left / W:.2f}-{(left + tw) / W:.2f})")
    if top < 0 or top + th > H:
        warn.append(f"{who} is cut off at the top/bottom (y {top / H:.2f}-{(top + th) / H:.2f})")
    bg.paste(im, (left, top), im)  # paste (not alpha_composite) also accepts negative offsets


def order_key(c: dict) -> float:
    return c.get("foot", c.get("y", 0.3) + c.get("h", 0) / 2)


def main():
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("spec")
    ap.add_argument("--only", help="comma list of scene ids")
    ap.add_argument("--check", action="store_true")
    ap.add_argument("--sheet", action="store_true")
    a = ap.parse_args()

    spec, base = load_spec(a.spec)
    chars = ROOT / "channels" / spec.get("channel", "jugnu-stories") / "characters"
    out_dir = base / spec.get("out_dir", "images")
    only = {int(x) for x in a.only.split(",")} if a.only else None
    bgs = {k: (base / v if not Path(v).is_absolute() else Path(v)) for k, v in spec["backgrounds"].items()}
    for k, v in bgs.items():
        if not v.exists():
            sys.exit(f"compose_scene: background '{k}' missing: {v}")

    made, problems = [], 0
    for sc in spec["scenes"]:
        if only and sc["id"] not in only:
            continue
        bg = Image.open(bgs[sc["bg"]]).convert("RGBA")
        if spec.get("size"):
            bg = bg.resize(tuple(spec["size"]), Image.Resampling.LANCZOS)
        warn = []
        for c in sorted(sc.get("cast", []), key=order_key):
            place(bg, c, chars, warn, sc.get("light", "day"))
        for w in warn:
            print(f"  WARN scene {sc['id']}: {w}")
        problems += len(warn)
        out = out_dir / f"scene_{sc['id']:02d}.png"
        if not a.check:
            out_dir.mkdir(parents=True, exist_ok=True)
            bg.convert("RGB").save(out)
            made.append(out)
        print(f"scene {sc['id']:02d}: {len(sc.get('cast', []))} characters -> {'(check only)' if a.check else out}")

    if a.sheet and made:
        thumbs = [Image.open(m).convert("RGB") for m in made]
        tw = 480
        thumbs = [t.resize((tw, round(t.height * tw / t.width))) for t in thumbs]
        cols = min(4, len(thumbs))
        rows = -(-len(thumbs) // cols)
        th = max(t.height for t in thumbs)
        sheet = Image.new("RGB", (cols * tw, rows * th), "white")
        for i, t in enumerate(thumbs):
            sheet.paste(t, ((i % cols) * tw, (i // cols) * th))
        sheet.save(out_dir / "_cutout_sheet.jpg", quality=88)
        print(f"sheet -> {out_dir / '_cutout_sheet.jpg'}")
    print(f"done: {len(made)} written, {problems} warning(s), cost Rs 0 (local)")


if __name__ == "__main__":
    main()
