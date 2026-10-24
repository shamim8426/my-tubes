#!/usr/bin/env python3
"""Per-channel YouTube login: every channel has its own OAuth client and its own token.

    python tools/yt_auth.py <channel_key>            # log in if there is no token, then show the channel
    python tools/yt_auth.py <channel_key> --login    # new browser login (replaces this channel's token)
    python tools/yt_auth.py <channel_key> --check    # no browser: show which files would be used

Where the files are (channels/<key>/channel.json):
    "secrets_dir": "secrets/<key>"  ->  secrets/<key>/client_secret.json + secrets/<key>/token.json
    no secrets_dir                  ->  old layout, ONLY for LEGACY channels:
                                        secrets/client_secret.json + secrets/youtube_token_<key>.json
A secrets_dir must be exactly secrets/<channel_key>, so a channel can never point at another channel's token.
The token must also come from the same OAuth client as the channel's client_secret.json.

After a login the channel from channels.list(mine=true) must have the title in channel.json
("youtube_title", else "display_name"); then its ID is written to channel.json "channel_id" (if empty).
Never prints secrets or tokens.
"""
import argparse
import json
import sys
from pathlib import Path

try:
    sys.stdout.reconfigure(encoding="utf-8")
    sys.stderr.reconfigure(encoding="utf-8")
except Exception:
    pass

ROOT = Path(__file__).resolve().parent.parent
SECRETS = ROOT / "secrets"
LEGACY = {"dadi-ki-kahaniyan"}  # channels that keep the old shared layout (token untouched)
SCOPES = [
    "https://www.googleapis.com/auth/youtube.upload",
    "https://www.googleapis.com/auth/youtube",
    "https://www.googleapis.com/auth/youtube.force-ssl",  # captions, comments, playlists
]


def config_file(key: str) -> Path:
    if not key or not all(c.isalnum() or c in "-_" for c in key):
        sys.exit(f"invalid channel key: {key!r}")
    f = ROOT / "channels" / key / "channel.json"
    if not f.exists():
        sys.exit(f"no channel config: {f.relative_to(ROOT).as_posix()}")
    return f


def config(key: str) -> dict:
    return json.loads(config_file(key).read_text(encoding="utf-8"))


def paths(key: str):
    """(client_secret, token) of this channel. Exits if the channel has no own place for them."""
    sd = config(key).get("secrets_dir")
    if sd:
        if Path(sd).as_posix().strip("/") != f"secrets/{key}":
            sys.exit(f"channels/{key}/channel.json secrets_dir must be secrets/{key} (is {sd})")
        d = ROOT / "secrets" / key
        return d / "client_secret.json", d / "token.json"
    if key in LEGACY:
        return SECRETS / "client_secret.json", SECRETS / f"youtube_token_{key}.json"
    sys.exit(f"channels/{key}/channel.json has no secrets_dir: set \"secrets_dir\": \"secrets/{key}\" "
             "and put that channel's own client_secret.json there")


def _client_id(client_file: Path):
    d = json.loads(client_file.read_text(encoding="utf-8"))
    return next(iter(d.values()), {}).get("client_id")


def service(key: str, interactive: bool = True, force_login: bool = False, channel_name: str = ""):
    """YouTube API client for this channel only. interactive=False never opens a browser (scheduled tasks)."""
    from google.auth.transport.requests import Request
    from google.oauth2.credentials import Credentials
    from google_auth_oauthlib.flow import InstalledAppFlow
    from googleapiclient.discovery import build

    client, tok = paths(key)
    creds = None
    if tok.exists() and not force_login:
        creds = Credentials.from_authorized_user_file(str(tok))  # the token's own granted scopes
        if client.exists() and creds.client_id != _client_id(client):
            sys.exit(f"{tok.relative_to(ROOT).as_posix()} was not made with {client.relative_to(ROOT).as_posix()} "
                     "(different OAuth client). Nothing done. Log in again: python tools/yt_auth.py "
                     f"{key} --login")
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not interactive:
                sys.exit(f"no valid YouTube token for {key}; log in once: python tools/yt_auth.py {key}")
            if not client.exists():
                sys.exit(f"Missing {client.relative_to(ROOT).as_posix()}. Do the one-time setup first.")
            print(f"Browser login: pick the Google account AND the channel '{channel_name or config(key).get('display_name', key)}'.")
            flow = InstalledAppFlow.from_client_secrets_file(str(client), SCOPES)
            creds = flow.run_local_server(port=0)
        tok.parent.mkdir(parents=True, exist_ok=True)
        tok.write_text(creds.to_json(), encoding="utf-8")
    return build("youtube", "v3", credentials=creds)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("channel_key")
    ap.add_argument("--login", action="store_true", help="new browser login (replaces this channel's token)")
    ap.add_argument("--check", action="store_true", help="no network: show the files this channel would use")
    a = ap.parse_args()

    cfg_file = config_file(a.channel_key)
    cfg = config(a.channel_key)
    client, tok = paths(a.channel_key)
    if a.check:
        for label, p in (("client", client), ("token", tok)):
            print(f"{label}: {p.relative_to(ROOT).as_posix()} ({'present' if p.exists() else 'MISSING'})")
        return

    yt = service(a.channel_key, force_login=a.login)
    items = yt.channels().list(part="id,snippet", mine=True).execute().get("items", [])
    if not items:
        sys.exit("This Google account has no YouTube channel. channel.json not changed.")
    cid, title = items[0]["id"], items[0]["snippet"]["title"]
    print(f"Logged-in channel: {title} ({cid})")
    want = cfg.get("youtube_title") or cfg.get("display_name")
    if title.strip() != (want or "").strip():
        sys.exit(f"STOP: expected the channel '{want}', got '{title}'. channel.json not changed. "
                 f"Delete {tok.relative_to(ROOT).as_posix()} and log in again with the right channel.")
    if cfg.get("channel_id") and cfg["channel_id"] != cid:
        sys.exit(f"STOP: channel.json has channel_id {cfg['channel_id']}, the login is {cid}. Nothing changed.")
    if not cfg.get("channel_id"):
        cfg["channel_id"] = cid
        cfg_file.write_text(json.dumps(cfg, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(f"channel_id written to {cfg_file.relative_to(ROOT).as_posix()}")
    print("Token:", tok.relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
