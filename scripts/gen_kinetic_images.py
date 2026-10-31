"""HD scene images for a kinetic Short. FREE FIRST (Cloudflare flux, Rs0), paid Gemini 2K only as the fallback (RULES: free-first).

    .venv\\Scripts\\python -X utf8 scripts\\gen_kinetic_images.py <story_dir> [--paid]

Reads <story_dir>/short.json: spec["image_style"] + each beat's "image" / "image_prompt". Missing files only (cached). Output <story_dir>/images/.
"""
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "tools"))


def main():
    story = Path(sys.argv[1]).resolve()
    force_paid = "--paid" in sys.argv
    spec = json.loads((story / "short.json").read_text(encoding="utf-8"))
    out_dir = story / "images"
    out_dir.mkdir(exist_ok=True)
    import cf_image
    from name_guard import find_names
    todo = [(b["image"], b["image_prompt"] + ". " + spec["image_style"]) for b in spec["beats"] if b.get("image_prompt")]
    seen = set()
    for name, prompt in todo:
        out = out_dir / name
        if out in seen or out.exists():
            continue
        seen.add(out)
        if find_names(prompt):
            sys.exit(f"BLOCK (name_guard): a name in the prompt of {name}")
        if not force_paid:
            try:
                cf_image.generate(prompt, out, width=1024, height=1792)
                print(f"{name}: free (Cloudflare), Rs0")
                continue
            except cf_image.FreeImageError as e:
                print(f"{name}: free engine unavailable ({str(e)[:90]}) -> paid Gemini 2K")
        import gemini_image
        gemini_image.generate(prompt, out, aspect_ratio="9:16", size="2K", style=spec["image_style"])
        print(f"{name}: paid Gemini 2K")


if __name__ == "__main__":
    main()
