"""Find CC0 / public-domain PHOTOS via the Openverse API for each beat of a script; download originals (<=12 MB) + metadata."""
import json, subprocess, sys, time, urllib.parse, re
UA = "devrobolab-research/1.0 (video asset search)"
OUT = "raw/"
Q = {"workspace": "desk laptop notebook workspace", "typing": "typing on laptop keyboard hands", "documents": "stack of documents folders paperwork",
     "checklist": "checklist clipboard pen", "doors": "two closed doors corridor", "pencils": "five pencils", "library2": "library reading room", "filing": "filing cabinet drawers"}
meta = {}
for key, q in Q.items():
    url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "license": "cc0,pdm", "category": "photograph", "page_size": 12, "mature": "false"})
    out = subprocess.run(["curl", "-s", "--max-time", "30", "-A", UA, url], capture_output=True, text=True).stdout
    try: res = json.loads(out).get("results", [])
    except Exception: print(key, "api fail", out[:100]); continue
    c = [r for r in res if (r.get("width") or 0) >= 1200 and r.get("license") in ("cc0", "pdm")]
    print(key, len(res), "->", len(c), flush=True)
    meta[key] = []
    for i, r in enumerate(c[:3]):
        f = f"{OUT}{key}_{i}.jpg"
        subprocess.run(["curl", "-sL", "--max-time", "60", "--max-filesize", "12000000", "-A", UA, "-o", f, r["url"]])
        meta[key].append({"file": f, "title": r.get("title"), "creator": r.get("creator"), "license": r.get("license"), "source": r.get("source"), "landing": r.get("foreign_landing_url"), "w": r.get("width"), "h": r.get("height")})
    time.sleep(2)
json.dump(meta, open(OUT + "meta.json", "w"), indent=1, ensure_ascii=False)
print("done")
