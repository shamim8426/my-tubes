import json, subprocess, time, urllib.parse
UA = "devrobolab-research/1.0 (video asset search)"
meta = json.load(open("raw/meta.json"))
Q = {"documents": ["paper documents", "folders paperwork", "files folders"], "doors": ["door", "doors hallway"], "pencils": ["colored pencils", "pencils"], "binders": ["binders shelf", "office files"]}
for key, qs in Q.items():
    got = []
    for q in qs:
        for attempt in range(3):
            time.sleep(6)
            url = "https://api.openverse.org/v1/images/?" + urllib.parse.urlencode({"q": q, "license": "cc0,pdm", "page_size": 20, "mature": "false"})
            out = subprocess.run(["curl", "-s", "--max-time", "40", "-A", UA, url], capture_output=True, text=True).stdout
            try: res = json.loads(out).get("results", []); break
            except Exception: res = None
        if res is None: print(key, q, "api fail"); continue
        got = [r for r in res if (r.get("width") or 0) >= 1200 and r.get("license") in ("cc0", "pdm")]
        print(key, q, len(res), "->", len(got), flush=True)
        if got: break
    meta[key] = []
    for i, r in enumerate(got[:3]):
        f = f"raw/{key}_{i}.jpg"
        subprocess.run(["curl", "-sL", "--max-time", "60", "--max-filesize", "12000000", "-A", UA, "-o", f, r["url"]])
        meta[key].append({"file": f, "title": r.get("title"), "creator": r.get("creator"), "license": r.get("license"), "source": r.get("source"), "landing": r.get("foreign_landing_url"), "w": r.get("width"), "h": r.get("height")})
json.dump(meta, open("raw/meta.json", "w"), indent=1, ensure_ascii=False)
print("done")
