"""Code-extract Surah 97 bytes from Tanzil quran-uthmani v1.1 (never typed by hand). Bismillah (first 4 words) of 97:1 stripped."""
import hashlib, json
from pathlib import Path
R = Path(__file__).resolve().parent
rows = [l.split("|", 2) for l in (R / "quran-uthmani.txt").read_text(encoding="utf-8").splitlines() if l.startswith("97|")]
ay = []
for s, a, t in rows:
    if a == "1":
        t = t.split(" ", 4)[4]
    ay.append({"ayah": int(a), "ref": f"97:{a}", "text": t, "words": len(t.split()), "sha256_utf8": hashlib.sha256(t.encode()).hexdigest()})
(R / "tanzil_97.json").write_text(json.dumps({"source": "Tanzil quran-uthmani v1.1 (research/quran-uthmani.txt lines 6126-6130), bytes unchanged, Bismillah (first 4 words) of 97:1 stripped", "ayat": ay}, ensure_ascii=False, indent=1), encoding="utf-8")
for x in ay: print(x["ref"], x["words"], x["text"])
