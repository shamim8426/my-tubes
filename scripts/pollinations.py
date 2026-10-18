"""Pollinations.ai (free, no key) image helper."""
import time
import urllib.parse
from pathlib import Path

import requests

BASE = "https://image.pollinations.ai/prompt/"
STYLE = "flat 2D cartoon, thick bold black outlines, warm colors, clean vector look, plain white background"


def generate(prompt: str, out: Path, width=768, height=768, seed=42, retries=4) -> Path:
    url = BASE + urllib.parse.quote(f"{prompt}, {STYLE}")
    params = {"width": width, "height": height, "seed": seed, "nologo": "true"}
    for attempt in range(retries):
        try:
            r = requests.get(url, params=params, timeout=300)
        except requests.exceptions.RequestException as e:
            print(f"  {type(e).__name__} -> retry in 60s")
            time.sleep(60)
            continue
        if r.ok and r.headers.get("Content-Type", "").startswith("image"):
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(r.content)
            return out
        wait = int(r.headers.get("Retry-After", 60))
        print(f"  {r.status_code} {r.text[:120]!r} -> retry in {wait}s")
        time.sleep(wait)
    raise RuntimeError(f"Pollinations failed for {out.name}")
