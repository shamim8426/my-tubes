"""Gemini (Nano Banana) image helper. Key is read from .env and never printed."""
import base64
import mimetypes
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

import cost_log
import preview
import pricing

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL = "gemini-nano-banana-2.1"
STYLE = ("Art style: flat 2D cartoon, thick bold black outlines, warm colours, flat cel shading, "
         "no gradients, no realism, clean vector look, kid-friendly.")


def _find_image(obj):
    """Return base64 image data from anywhere in the response JSON."""
    if isinstance(obj, dict):
        if obj.get("type") == "image" and obj.get("data"):
            return obj["data"]
        if "output_image" in obj and isinstance(obj["output_image"], dict) and obj["output_image"].get("data"):
            return obj["output_image"]["data"]
        if "inlineData" in obj and obj["inlineData"].get("data"):
            return obj["inlineData"]["data"]
        for v in obj.values():
            found = _find_image(v)
            if found:
                return found
    elif isinstance(obj, list):
        for v in obj:
            found = _find_image(v)
            if found:
                return found
    return None


def generate(prompt: str, out: Path, refs: list[Path] = (), aspect_ratio="1:1", size="1K") -> Path:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing in .env")

    inputs = [{"type": "text", "text": f"{prompt}\n\n{STYLE}"}]
    for ref in refs:
        mime = mimetypes.guess_type(ref)[0] or "image/png"
        inputs.append({"type": "image", "mime_type": mime,
                       "data": base64.b64encode(Path(ref).read_bytes()).decode()})

    body = {"model": MODEL, "input": inputs,
            "response_format": {"type": "image", "aspect_ratio": aspect_ratio, "image_size": size}}
    r = requests.post(ENDPOINT, json=body, headers={"x-goog-api-key": key}, timeout=90)  # >90s -> skip
    if not r.ok:
        raise RuntimeError(f"Gemini {r.status_code}: {r.text[:500]}")

    js = r.json()
    data = _find_image(js)
    if not data:
        raise RuntimeError(f"No image in response: {r.text[:500]}")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(base64.b64decode(data))
    # actual cost from the response's usage numbers (text + every reference image in, image + thinking out)
    cost = pricing.image_cost(MODEL, size, js, prompt_chars=len(inputs[0]["text"]), n_refs=len(refs))
    print(cost_log.summary(cost_log.record_call(out, MODEL, size, cost, usage=pricing.read_usage(js))))
    preview.build()
    preview.open_in_vscode(out)
    return out
