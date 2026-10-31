"""Presentation-style Short builder (Claude explainer): deck.json -> free TTS -> timed HTML deck -> mp4. All local and free except
nothing: the voice uses ONLY the free Gemini key (stops when its daily quota is over, never falls back to paid).

    .venv\\Scripts\\python -X utf8 scripts\\build_deck.py <story_dir> --tts
    .venv\\Scripts\\python -X utf8 scripts\\build_deck.py <story_dir> --still 3,9,15          # layout stills (no TTS needed)
    .venv\\Scripts\\python -X utf8 scripts\\build_deck.py <story_dir> --render                # voice.wav + deck.html + short.mp4

deck.json: {"tag", "voice": {id, style}, "scenes": [{id, type, voice, cues: [phrase of the voice text, ...], wipe, ...scene fields}]}
Scene types live in channels/yellow-bot/templates/deck_template.html. A cue is a phrase of the scene's voice text: the item
appears just before that phrase is spoken (position estimated from its place in the sentence).
"""
import argparse
import json
import re
import subprocess
import sys
import wave
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "scripts"))
TEMPLATE = ROOT / "channels/yellow-bot/templates/deck_template.html"
DOCS = ROOT / "channels/yellow-bot/shared_docs"
MASCOT = ROOT / "channels/yellow-bot/mascot"
LEAD, AFTER, SR = 0.30, 0.28, 24000


def vtext(sc):
    return re.sub(r"\s+", " ", sc["voice"]).strip()


def wav_len(p):
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def phrase_time(sc, dur, ph):
    if isinstance(ph, (int, float)) or ph is None:
        return ph
    text = vtext(sc)
    i = text.find(ph)
    if i < 0:
        print(f"  warn: cue {ph!r} not found in the voice text of scene {sc.get('id')}")
        return None
    return round(max(0.2, LEAD + dur * (i / max(1, len(text))) * 0.97 - 0.12), 2)


def resolve_cues(sc, dur):
    return [phrase_time(sc, dur, ph) for ph in sc.get("cues", [])]


def music_args(spec):
    m = spec.get("music")
    if not m:
        return []
    return ["--music", str(ROOT / m["file"]), "--music-start", str(m.get("start", 0)), "--music-rel", str(m.get("rel", 14))]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("story")
    ap.add_argument("--deck", default="deck.json", help="spec file name inside the story folder")
    ap.add_argument("--tts", action="store_true")
    ap.add_argument("--paid", action="store_true", help="allow the paid key when the free quota is over (user OK 2026-10-31)")
    ap.add_argument("--still")
    ap.add_argument("--render", action="store_true")
    a = ap.parse_args()
    story = Path(a.story).resolve()
    spec = json.loads((story / a.deck).read_text(encoding="utf-8-sig"))
    scenes = spec["scenes"]
    tts_dir = story / "audio" / "tts"
    files = [tts_dir / f"s_{i:02d}.wav" for i in range(len(scenes))]

    if a.tts:
        import gemini_tts
        from gemini_keys import FreeQuotaOver
        tts_dir.mkdir(parents=True, exist_ok=True)
        for i, (sc, f) in enumerate(zip(scenes, files)):
            if f.exists():
                continue
            try:
                r = gemini_tts.speak(vtext(sc), spec["voice"]["id"], spec["voice"]["style"], f, free_only=not a.paid)
            except FreeQuotaOver as e:
                left = [x.name for x in files if not x.exists()]
                sys.exit(f"STOP (free only): {e}\n  still missing: {left}\n  Free quota resets daily; nothing was spent.")
            print(f"scene {i} ({sc['id']}): {r['seconds']:.1f}s  cost ~${r['usd']:.4f}" + ("  (FREE key)" if r['usd'] == 0 else "  (paid key)"))
        return

    durs = [wav_len(f) if f.exists() else 0.082 * len(vtext(sc)) for sc, f in zip(scenes, files)]
    t, data = 0.0, []
    for sc, d in zip(scenes, durs):
        end = t + LEAD + d + AFTER
        item = dict(sc)
        item.update(start=round(t, 3), end=round(end, 3), cues=resolve_cues(sc, d))
        if sc["type"] == "docs":
            item["imgUrl"] = (DOCS / sc["img"]).as_uri()
            item["hls"] = [dict(h, at=phrase_time(sc, d, (sc.get("hlcues") or [None] * 9)[k]) or h.get("at", 1.0)) for k, h in enumerate(sc.get("hls", []))]
        robs = [dict(r) for r in (sc.get("robots") or ([sc["robot"]] if sc.get("robot") else []))]
        for r in robs:
            r["url"] = (MASCOT / (r["img"] + ".png")).as_uri()
            r["at"] = phrase_time(sc, d, r.get("cue")) or 1.0
        if robs:
            item["robots"] = robs
        if sc.get("layers"):
            item["layers"] = [dict(L, url=(MASCOT / (L["img"] + ".png")).as_uri()) if L.get("kind") == "img" else L for L in sc["layers"]]
        data.append(item)
        t = end
    total = round(t + 0.2, 3)
    build = story / "build"
    build.mkdir(exist_ok=True)
    html = TEMPLATE.read_text(encoding="utf-8")
    payload = {"tag": spec.get("tag", ""), "scenes": data, "total": total, "sfx": [s["start"] for s in data[1:]]}
    html = html.replace("/*DATA*/null", json.dumps(payload, ensure_ascii=False)).replace("{{FONTS}}", (ROOT / "shared/fonts").as_uri())
    deck = build / "deck.html"
    deck.write_text(html, encoding="utf-8")
    print(f"deck.html: {len(data)} scenes, {total:.1f}s; starts {[round(d[chr(115)+chr(116)+chr(97)+chr(114)+chr(116)],1) for d in data]}")

    if a.still:
        subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "scripts/html_scene.py"), str(deck), str(build / "stills"), a.still], check=True)
        return

    if a.render:
        missing = [f.name for f in files if not f.exists()]
        if missing:
            sys.exit(f"missing voice files {missing}: run --tts first")
        voice = build / "voice.wav"
        with wave.open(str(voice), "wb") as w:
            w.setnchannels(1), w.setsampwidth(2), w.setframerate(SR)
            for f in files:
                with wave.open(str(f)) as r:
                    assert r.getframerate() == SR and r.getnchannels() == 1
                    w.writeframes(b"\x00\x00" * int(SR * LEAD) + r.readframes(r.getnframes()) + b"\x00\x00" * int(SR * AFTER))
        out = story / "output" / "short.mp4"
        out.parent.mkdir(exist_ok=True)
        subprocess.run([sys.executable, "-X", "utf8", str(ROOT / "scripts/html_video.py"), str(deck), str(voice), str(out), "--lead", "0", "--tail", "0.3"] + music_args(spec), check=True)


if __name__ == "__main__":
    main()
