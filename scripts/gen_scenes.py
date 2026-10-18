"""Generate scene images from a scene_prompts.json.

Usage:  python scripts/gen_scenes.py case01_cycle_chori [ids...]              (Shorts: cases/<case>/scene_prompts.json)
        python scripts/gen_scenes.py long-videos/long_01/scene_prompts.json [ids...]
Spec keys: looks, base, scenes[{id, refs, prompt}], optional out_dir, aspect (default 9:16), ref_files {name: path}.
Refs: "scene:N" -> an earlier image in out_dir; a name in ref_files -> that file; else characters/<name>_sheet.png.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gemini_image import generate  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


def load(arg):
    if arg.endswith(".json"):
        path = ROOT / arg
        spec = json.loads(path.read_text(encoding="utf-8"))
        out_dir = ROOT / spec["out_dir"] if "out_dir" in spec else path.parent / "images"
    else:
        spec = json.loads((ROOT / "cases" / arg / "scene_prompts.json").read_text(encoding="utf-8"))
        out_dir = ROOT / "images" / arg
    return spec, out_dir


def ref_path(ref: str, spec, out_dir: Path) -> Path:
    if ref.startswith("scene:"):
        return out_dir / f"scene_{int(ref[6:]):02d}.png"
    if ref in spec.get("ref_files", {}):
        return ROOT / spec["ref_files"][ref]
    return ROOT / "characters" / f"{ref}_sheet.png"


def main(arg: str, only: list[int]):
    spec, out_dir = load(arg)
    aspect = spec.get("aspect", "9:16")
    for scene in spec["scenes"]:
        if only and scene["id"] not in only:
            continue
        refs = [ref_path(r, spec, out_dir) for r in scene["refs"]]
        missing = [r for r in refs if not r.exists()]
        if missing:
            print(f"SKIPPED scene {scene['id']}: missing refs {missing}", flush=True)
            continue
        prompt = scene["prompt"].format(**spec["looks"])
        if refs:
            prompt += ("\n\nThe attached images are approved references. Keep every character's face, body, "
                       "outfit and colours EXACTLY as in the references, keep places consistent with any location "
                       "reference, and match their art style. Draw only the characters this prompt asks for.")
        else:
            refs = [ROOT / "characters" / "dadi_sheet.png"]
            prompt += ("\n\nThe attached image is a STYLE reference only: match its art style, outline thickness "
                       "and colour palette exactly. Do NOT draw the grandmother from it in this scene.")
        out = out_dir / f"scene_{scene['id']:02d}.png"
        t0 = time.time()
        try:
            generate(f"{spec['base']}\n\n{prompt}", out, refs=refs, aspect_ratio=aspect, size="1K")
            print(f"saved {out}  ({time.time() - t0:.0f}s)", flush=True)
        except Exception as e:  # timeout (>90s) or API error -> skip, continue with next scene
            print(f"SKIPPED scene {scene['id']} after {time.time() - t0:.0f}s: {e}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], [int(x) for x in sys.argv[2:]])
