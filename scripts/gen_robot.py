"""Mascot poses for the Claude explainer decks (FREE only: Cloudflare flux; never the paid image key).

    .venv\\Scripts\\python -X utf8 scripts\\gen_robot.py <name> "<pose description>" [<name> "<pose>" ...]

Output: channels/devrobolab/mascot/<name>.png (1024x1024, pure white background so it blends with `multiply` on the white
slides). One shared character description keeps the robot recognisable across poses; flux gives no exact consistency, so check them."""
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
sys.path.insert(0, str(ROOT / "tools"))
OUT = ROOT / "channels/devrobolab/mascot"
CHARACTER = ("a cute friendly small robot mascot, round head with a dark rounded visor face and two big glowing yellow eyes, tiny antenna "
             "with a yellow ball, chubby rounded white and yellow body with black accents, flat vector sticker illustration, thick clean "
             "black outlines, simple soft shapes, full body, centered, solid pure white background, lots of empty white space around. "
             "No text, no letters, no logo, no brand, no people.")


def main():
    import cf_image
    from name_guard import find_names
    args = sys.argv[1:]
    OUT.mkdir(parents=True, exist_ok=True)
    for name, pose in zip(args[0::2], args[1::2]):
        out = OUT / f"{name}.png"
        if out.exists():
            continue
        prompt = f"{CHARACTER} Pose: {pose}."
        if find_names(prompt):
            sys.exit("BLOCK (name_guard)")
        try:
            cf_image.generate(prompt, out, width=1024, height=1024)
            print(f"{name}: free (Cloudflare), Rs0")
        except cf_image.FreeImageError as e:
            sys.exit(f"STOP (free only): {e}")


if __name__ == "__main__":
    main()
