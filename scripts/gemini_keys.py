"""Which Gemini key a call uses (keys from .env, never printed).

Free-first (user rule 2026-10-24): GEMINI_API_KEY_FREE (the Noor-e-Raah Google project, no billing) is used ONLY for
files of the channels in FREE_CHANNELS. Such a call goes to the free key first; on 429 (free quota used up) the same
request goes straight to the paid GEMINI_API_KEY. Every other channel (Jugnu Stories) only ever uses the paid key.
A free call is logged in cost_log.csv with actual ₹0 and " free" in its size column.
Only models in FREE_MODELS try the free key: test 2026-10-24 (free key, ₹0): gemini-3.8-flash-tts works;
gemini-nano-banana-2.1 gives 429 "limit: 0 ... on Free Tier", so images always use the paid key.
"""
import os
from pathlib import Path

import requests
from dotenv import load_dotenv

from paths import CHANNELS

ROOT = Path(__file__).resolve().parent.parent
load_dotenv(ROOT / ".env")

FREE_CHANNELS = {"noor-e-raah", "_new_claude_explainer", "devrobolab", "jugnu-stories"}  # 2026-11-01: jugnu-stories added per the user's free-first rule for ALL channels (2026-10-30, CLAUDE.md); 2026-10-31: user wants only free TTS for the Claude explainer videos (shares the Noor free quota)
FREE_MODELS = {"gemini-3.8-flash-tts", "gemini-3.8-flash-lite-tts"}  # lite verified on the free key 2026-11-04 (Rs0, own quota)


def channel_for(out) -> str | None:
    """Channel of the output file (channels/<key>/...), else of the running build (STORY_CHANNEL). If both are set
    and differ, None: such a call never gets the free key."""
    env = os.environ.get("STORY_CHANNEL")
    try:
        own = Path(out).resolve().relative_to(CHANNELS).parts[0]
    except (ValueError, IndexError):
        own = None
    if own and env and own != env:
        return None
    return own or env


def keys_for(out, model: str = "") -> list[tuple[str, str]]:
    """[(tier, key), ...] in the order to try: ("free", ...) first only for FREE_CHANNELS + FREE_MODELS, then ("paid", ...)."""
    keys = []
    free = os.environ.get("GEMINI_API_KEY_FREE")
    if free and model in FREE_MODELS and channel_for(out) in FREE_CHANNELS:
        keys.append(("free", free))
    paid = os.environ.get("GEMINI_API_KEY")
    if paid:
        keys.append(("paid", paid))
    if not keys:
        raise RuntimeError("GEMINI_API_KEY missing in .env")
    return keys


def _post(endpoint, body, key, timeout):
    """One request; a dropped connection or a read time-out is tried again twice (5 s, 15 s)."""
    import time
    for wait in (5, 15, None):
        try:
            return requests.post(endpoint, json=body, headers={"x-goog-api-key": key}, timeout=timeout)
        except (requests.ConnectionError, requests.Timeout):
            if wait is None:
                raise
            print(f"Gemini: network error, retry in {wait}s", flush=True)
            time.sleep(wait)


class FreeQuotaOver(RuntimeError):
    """free_only call got 429 (or has no free key): stop, never spend."""


def post(endpoint: str, body: dict, out, timeout=90, label="Gemini", free_only=False):
    """POST with free-first fallback. Returns (response, tier). free_only: never the paid key (stop instead)."""
    keys = keys_for(out, body.get("model", ""))
    if free_only:
        keys = [k for k in keys if k[0] == "free"]
        if not keys:
            raise FreeQuotaOver(f"{label}: no free key for this channel/model; paid key not allowed here")
        r = _post(endpoint, body, keys[0][1], timeout)
        if r.status_code == 429:
            raise FreeQuotaOver(f"{label}: free key quota used up (429); paid key not allowed here")
        return r, "free"
    for i, (tier, key) in enumerate(keys):
        r = _post(endpoint, body, key, timeout)
        if r.status_code == 429 and tier == "free" and i + 1 < len(keys):
            print(f"{label}: free key quota (429) -> same request on the paid key")
            continue
        return r, tier
    return r, tier
