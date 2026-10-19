"""Generate scene images from a scene_prompts.json.

Usage:  python scripts/gen_scenes.py channels/<key>/stories/<story>/scene_prompts.json [ids...]
        (images go to the story's images/, shared by its long video and shorts)
Spec keys: looks, base, scenes[{id, refs, prompt}], optional out_dir, aspect (default 9:16), ref_files {name: path}.
Refs: "scene:N" -> an earlier image in out_dir; a name in ref_files -> that file; else channels/<key>/characters/<name>_sheet.png.
"""
import json
import sys
import time
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from gemini_image import generate  # noqa: E402
from paths import ROOT, channel_dir, channel_of  # noqa: E402
import pricing  # noqa: E402
from gemini_image import MODEL  # noqa: E402
from story_budget import check  # noqa: E402


def load(arg):
    path = ROOT / arg
    if path.is_dir():
        path = path / "scene_prompts.json"
    spec = json.loads(path.read_text(encoding="utf-8"))
    out_dir = ROOT / spec["out_dir"] if "out_dir" in spec else path.parent / "images"
    spec["_chars"] = channel_dir(channel_of(path)) / "characters"
    return spec, out_dir


def ref_path(ref: str, spec, out_dir: Path) -> Path:
    if ref.startswith("scene:"):
        return out_dir / f"scene_{int(ref[6:]):02d}.png"
    if ref in spec.get("ref_files", {}):
        return ROOT / spec["ref_files"][ref]
    return spec["_chars"] / f"{ref}_sheet.png"


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
            refs = [spec["_chars"] / "dadi_sheet.png"]
            prompt += ("\n\nThe attached image is a STYLE reference only: match its art style, outline thickness "
                       "and colour palette exactly. Do NOT draw the grandmother from it in this scene.")
        out = out_dir / f"scene_{scene['id']:02d}.png"
        # RULES 15 budget guard: story cap + ₹50 floor on actual cost (exits before spending)
        est = pricing.image_estimate_usd(MODEL, "1K", len(spec['base']) + len(prompt), len(refs)) * pricing.usd_to_inr()
        check(out_dir.parent.name, est)
        t0 = time.time()
        try:
            generate(f"{spec['base']}\n\n{prompt}", out, refs=refs, aspect_ratio=aspect, size="1K")
            print(f"saved {out}  ({time.time() - t0:.0f}s)", flush=True)
        except Exception as e:  # timeout (>90s) or API error -> skip, continue with next scene
            print(f"SKIPPED scene {scene['id']} after {time.time() - t0:.0f}s: {e}", flush=True)


if __name__ == "__main__":
    main(sys.argv[1], [int(x) for x in sys.argv[2:]])
