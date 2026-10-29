"""Free AI image: Cloudflare Workers AI flux-2-klein-4b (free tier, Apache 2.0). Rs0 per image.

Keys come from the environment / .env (never printed): CLOUDFLARE_ACCOUNT_ID and CLOUDFLARE_API_TOKEN_FREE
(or CLOUDFLARE_API_TOKEN). Needs api.cloudflare.com reachable (the cloud environment's Allowed domains).
Free-first rule (user 2026-10-30): wallpapers / scene images try this first; the paid Gemini image is the fallback.
Every call is logged in cost_log.csv with Rs0 and " free" in the size column, like free TTS.

    from cf_image import generate, FreeImageError
    generate(prompt, out_path, width=1920, height=1088)   # raises FreeImageError when it cannot make the picture
"""
import base64
import os
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

import cost_log

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

MODEL = "@cf/black-forest-labs/flux-2-klein-4b"
ENDPOINT = "https://api.cloudflare.com/client/v4/accounts/{acc}/ai/run/" + MODEL


class FreeImageError(RuntimeError):
    """The free engine could not make the picture (no key, blocked network, quota, bad answer)."""


def available() -> str | None:
    """None when the free engine can be tried, else the reason it cannot."""
    if not os.environ.get("CLOUDFLARE_ACCOUNT_ID"):
        return "CLOUDFLARE_ACCOUNT_ID missing"
    if not (os.environ.get("CLOUDFLARE_API_TOKEN_FREE") or os.environ.get("CLOUDFLARE_API_TOKEN")):
        return "CLOUDFLARE_API_TOKEN_FREE missing"
    return None


def generate(prompt: str, out: Path, width: int = 1920, height: int = 1088, retries: int = 2) -> Path:
    why = available()
    if why:
        raise FreeImageError(why)
    acc = os.environ["CLOUDFLARE_ACCOUNT_ID"]
    tok = os.environ.get("CLOUDFLARE_API_TOKEN_FREE") or os.environ["CLOUDFLARE_API_TOKEN"]
    last = ""
    for attempt in range(retries + 1):
        try:
            r = requests.post(ENDPOINT.format(acc=acc), headers={"Authorization": f"Bearer {tok}"}, timeout=240,
                              files={"prompt": (None, prompt), "width": (None, str(width)), "height": (None, str(height))})
        except requests.exceptions.RequestException as e:  # blocked host, DNS, timeout
            raise FreeImageError(f"Cloudflare not reachable ({type(e).__name__}): is api.cloudflare.com allowed?") from None
        if r.ok:
            try:
                data = base64.b64decode(r.json()["result"]["image"])
            except Exception:  # noqa: BLE001
                raise FreeImageError(f"Cloudflare answered without an image: {r.text[:200]}") from None
            out.parent.mkdir(parents=True, exist_ok=True)
            out.write_bytes(data)
            cost_log.record_call(out, "cf-flux-2-klein-4b", f"{width}x{height} free",
                                 {"estimated_usd": 0.0, "actual_usd": 0.0})
            return out
        last = f"HTTP {r.status_code}: {r.text[:200]}"
        if r.status_code in (429, 500, 502, 503) and attempt < retries:
            time.sleep(int(r.headers.get("Retry-After", 20)))
            continue
        break
    raise FreeImageError(f"Cloudflare free image failed ({last}) - daily free quota used up?")
