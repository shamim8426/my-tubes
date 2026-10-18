"""Gemini TTS helper. Key from .env (never printed). Every call is logged to cost_log.csv."""
import base64
import os
import wave
from pathlib import Path

import requests
from dotenv import load_dotenv

import cost_log

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

ENDPOINT = "https://generativelanguage.googleapis.com/v1beta/interactions"
MODEL = "gemini-3.8-flash-tts"
# USD per 1M tokens (ai.google.dev/gemini-api/docs/pricing, checked 2026-10-17; doubles from 2027-01-01)
PRICE_IN, PRICE_OUT = 0.50, 9.00
AUDIO_TOKENS_PER_SEC = 25
SR = 24000


def _find(obj, pred):
    if isinstance(obj, dict):
        if pred(obj):
            return obj
        for v in obj.values():
            if (hit := _find(v, pred)) is not None:
                return hit
    elif isinstance(obj, list):
        for v in obj:
            if (hit := _find(v, pred)) is not None:
                return hit
    return None


def _usage_tokens(js):
    """(input_tokens, output_tokens) if the response reports usage, else (None, None)."""
    u = _find(js, lambda d: any("token" in k.lower() for k in d) and not d.get("data"))
    if not u:
        return None, None
    get = lambda *names: next((u[k] for k in u for n in names if k.lower() == n), None)
    return get("input_tokens", "total_input_tokens", "prompttokencount"), \
        get("output_tokens", "total_output_tokens", "candidatestokencount")


def speak(text: str, voice: str, style: str, out: Path) -> dict:
    key = os.environ.get("GEMINI_API_KEY")
    if not key:
        raise RuntimeError("GEMINI_API_KEY missing in .env")
    body = {
        "model": MODEL,
        "input": [{"type": "user_input", "content": [{
            "type": "text", "text": text,
            "annotations": [{"type": "speech_metadata", "style": style}]}]}],
        "response_format": {"type": "audio", "mime_type": "audio/l16", "sample_rate": SR},
        "generation_config": {"speech_config": [{"voice": voice}]},
    }
    r = requests.post(ENDPOINT, json=body, headers={"x-goog-api-key": key}, timeout=90)
    if not r.ok:
        raise RuntimeError(f"Gemini TTS {r.status_code}: {r.text[:500]}")
    js = r.json()
    blob = _find(js, lambda d: d.get("data") and "audio" in str(d.get("type", "")) + str(d.get("mime_type", "")))
    if not blob:
        raise RuntimeError(f"No audio in response: {str(js)[:500]}")
    pcm = base64.b64decode(blob["data"])
    out.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out), "wb") as w:
        w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR), w.writeframes(pcm)
    secs = len(pcm) / 2 / SR

    tin, tout = _usage_tokens(js)
    estimated = tout is None
    tout = tout if tout is not None else secs * AUDIO_TOKENS_PER_SEC
    tin = tin if tin is not None else (len(text) + len(style)) / 2
    usd = tin / 1e6 * PRICE_IN + tout / 1e6 * PRICE_OUT
    row = cost_log.record_usd(out, MODEL, f"tts {secs:.1f}s{' est' if estimated else ''}", usd)
    return {"seconds": secs, "usd": usd, "row": row, "usage_reported": not estimated}
