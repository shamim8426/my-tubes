"""Rewrite long/images.json for RULES 2h (people image per ayah block). Intro/parichay/shan-e-nuzul stay places-only
(RULES 2: shan-e-nuzul scenes show only places). A people image that does not exist yet keeps the old places entry
(from long/images_places.json), so the video always builds.
    .venv/Scripts/python -X utf8 channels/noor-e-raah/stories/008_al-fil/script/make_images_json.py
"""
import json
from pathlib import Path

S = Path(__file__).resolve().parent.parent
old_f = S / "long/images_places.json"
if not old_f.exists():
    old_f.write_text((S / "long/images.json").read_text(encoding="utf-8"), encoding="utf-8")
old = json.loads(old_f.read_text(encoding="utf-8"))["images"]

PEOPLE = [  # (start, id, base image id, rect or None); paid Gemini x4 (Cloudflare quota empty), crops for the 2nd jumla
    ({"ayah": 1}, "p01_grandpa_story", "p01_grandpa_story", None),
    ({"ayah": 2}, "p01_grandpa_story_b", "p01_grandpa_story", {"fx": 0.66, "fy": 0.35, "zc": 1.5}),
    ({"ayah": 3}, "p01_grandpa_story_c", "p01_grandpa_story", {"fx": 0.28, "fy": 0.6, "zc": 1.5}),
    ({"ayah": 4}, "p05_fallen_stones", "p05_fallen_stones", None),
    ({"ayah": 5}, "p05_fallen_stones_b", "p05_fallen_stones", {"fx": 0.62, "fy": 0.55, "zc": 1.4}),
    ({"ayah": 6}, "p06_kids_birds", "p06_kids_birds", None),
    ({"ayah": 7}, "p06_kids_birds_b", "p06_kids_birds", {"fx": 0.45, "fy": 0.25, "zc": 1.5}),
    ({"ayah": 10}, "p11_chaff_hands_b", "p11_chaff_hands", {"fx": 0.25, "fy": 0.25, "zc": 1.7}),
    ({"ayah": 11}, "p11_chaff_hands_c", "p11_chaff_hands", {"fx": 0.15, "fy": 0.3, "zc": 1.7}),
]
by_start = {json.dumps(p[0], sort_keys=True): p for p in PEOPLE}
out, used_new = [], []
for im in old:
    key = json.dumps(im["start"], sort_keys=True)
    p = by_start.get(key)
    if p and (S / "images" / f"{p[2]}.png").exists():
        e = {"id": p[1], "start": im["start"], "new": "paid Gemini 1K (free quota empty), RULES 2h people image"}
        if p[1] != p[2]:
            e["reuse_id"] = p[2]
        if p[3]:
            e["rect"] = p[3]
        out.append(e)
        used_new.append(p[1])
    else:
        out.append(im)
# a mid-block crop inside an ayah block that now has its people image is dropped (one big image per block)
if "p01_grandpa_story" in used_new:
    out = [e for e in out if e["id"] != "11_sunrays_clouds_b"]
# a reuse_id entry whose base image entry was replaced still needs that base file: keep a copy note
ids = {e["id"] for e in out}
for e in out:
    if "reuse_id" in e and e["reuse_id"] not in ids and not (S / "images" / f"{e['reuse_id']}.png").exists():
        base = next(i for i in old if i["id"] == e["reuse_id"])
        e["reuse"] = base["reuse"]
        e["_was_crop_of"] = e.pop("reuse_id")
doc = {"_help": "008 Al-Fil images v2 (RULES 2h, 2026-11-17): people image per ayah block (4 new paid Gemini, Cloudflare free quota empty at 05:36 IST); "
                "intro/parichay/shan-e-nuzul = reused places (RULES 2). Old plan: images_places.json.",
       "images": out}
(S / "long/images.json").write_text(json.dumps(doc, ensure_ascii=False, indent=1), encoding="utf-8")
print("people images used:", len(used_new), used_new)
