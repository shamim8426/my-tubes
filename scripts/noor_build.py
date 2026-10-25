"""Noor-e-Raah long-video builder (surah explainer, channel RULES 1, 1a-1c). Stages, each re-runnable (cache):

    .venv\\Scripts\\python -X utf8 scripts\\noor_build.py <story> parse   # script.md -> long/lines.json
    .venv\\Scripts\\python -X utf8 scripts\\noor_build.py <story> tts     # every spoken line: TTS + Whisper check

<story> = channels/noor-e-raah/stories/<NNN>_<slug>. TTS: free key first, on 429 the paid key (RULES 5); budget
check before every paid call (shared/pricing.json story cap). A line that still misses a word after 2 retries is
listed in long/review/tts_report.md for a simpler wording (never sent to production silently).
"""
import json
import re
import sys
import wave
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import numpy as np  # noqa: E402

import gemini_tts  # noqa: E402
import pricing  # noqa: E402
import story_budget  # noqa: E402
from noor_audition import missing  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
TAG = re.compile(r"\s*\[(?:S\d+|M\d+|MISAAL|NEXT)\]")
LINE = re.compile(r"^(\d+)\.\s+(USTAAD|SAWAAL)(?:\s+—\s+([A-Z]+))?:\s*\"(.*)\"\s*((?:\[[^\]]+\]\s*)*)$")
CUE = re.compile(r"^(\d+)\.\s+\[(MUSIC|AMBIENCE)([^\]]*)\]\s*$")


def parse(story: Path) -> list:
    """Script lines in order: spoken lines, numbered cues, ARABIC ayat, SCREEN notes, section/ayah headings."""
    items, section, ayah = [], None, None
    for raw in (story / "script/script.md").read_text(encoding="utf-8").splitlines():
        s = raw.strip()
        if s.startswith("## SOURCES"):
            break
        if s.startswith("## "):
            section, ayah = s[3:].strip(), None
            items.append({"kind": "section", "name": section})
            continue
        if m := re.match(r"^### \[AYAH (\d+)\]", s):
            ayah = int(m.group(1))
            items.append({"kind": "ayah", "ayah": ayah})
            continue
        if s.startswith("ARABIC:"):
            items.append({"kind": "arabic", "ayah": ayah, "text": s[len("ARABIC:"):].strip()})  # bytes unchanged
            continue
        if s.startswith("[SCREEN"):
            items.append({"kind": "screen", "section": section, "ayah": ayah, "note": s.strip("[]")})
            continue
        if m := LINE.match(s):
            n, who, role, text, tags = m.groups()
            items.append({"kind": "line", "n": int(n), "speaker": who.lower(), "role": (role or "").lower(),
                          "section": section, "ayah": ayah, "text": TAG.sub("", text).strip(),
                          "tags": re.findall(r"\[([^\]]+)\]", tags)})
            continue
        if m := CUE.match(s):
            items.append({"kind": "cue", "n": int(m.group(1)), "type": m.group(2).lower(),
                          "value": m.group(3).strip(" :—"), "section": section, "ayah": ayah})
    return items


def wav_len(p: Path) -> float:
    with wave.open(str(p)) as w:
        return w.getnframes() / w.getframerate()


def tts(story: Path):
    items = json.loads((story / "long/lines.json").read_text(encoding="utf-8"))
    voices = json.loads((story.parents[1] / "channel.json").read_text(encoding="utf-8"))["voices"]
    out_dir = story / "audio/tts"
    out_dir.mkdir(parents=True, exist_ok=True)
    from faster_whisper import WhisperModel
    model = WhisperModel("small", device="cpu", compute_type="int8", download_root=str(ROOT / "tools/whisper-models"))
    report = []
    for it in (i for i in items if i["kind"] == "line"):
        f = out_dir / f"{it['n']:03d}_{it['speaker']}.wav"
        ok = f.with_suffix(".ok")  # passed once = never re-checked
        v = voices["ustaad" if it["speaker"] == "ustaad" else "sawaal"]
        miss, heard, tries = [], "", 0
        if not (f.exists() and ok.exists()):
            for attempt in range(3):  # first take + max 2 retries (RULES 1b)
                if not f.exists():
                    est = pricing.tts_estimate_usd(gemini_tts.MODEL, len(it["text"]) + len(v["style"]),
                                                   len(it["text"]) / 8) * pricing.usd_to_inr()
                    story_budget.check(story.name, est)
                    gemini_tts.speak(it["text"], v["voice"], v["style"], f)
                    tries += 1
                with wave.open(str(f)) as w:
                    sr = w.getframerate()
                    x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
                x16 = np.interp(np.arange(0, len(x), sr / 16000), np.arange(len(x)), x).astype(np.float32)
                heard = " ".join(s.text.strip() for s in model.transcribe(x16, language="hi", beam_size=5)[0])
                miss = missing(it["text"], heard)
                if not miss:
                    ok.write_text(heard, encoding="utf-8")
                    break
                if attempt < 2:
                    f.unlink()
        it["audio"] = f.relative_to(story).as_posix()
        it["seconds"] = round(wav_len(f), 2)
        it["tts_ok"] = ok.exists()
        print(f"{it['n']:3d} {it['speaker']:6s} {it['seconds']:5.1f}s takes={tries} "
              f"{'OK' if it['tts_ok'] else 'MISSING ' + str(miss)}", flush=True)
        if not it["tts_ok"]:
            report.append(f"| {it['n']} | {it['speaker']} | {it['text']} | {', '.join(miss)} | {heard} |")
    (story / "long/lines.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
    spoken = [i for i in items if i["kind"] == "line"]
    md = [f"# TTS report — {story.name}", "", f"Lines: {len(spoken)}; total voice {sum(i['seconds'] for i in spoken):.1f}s;"
          f" Whisper OK {sum(i['tts_ok'] for i in spoken)}/{len(spoken)}", "", story_budget.summary_line(story.name), ""]
    if report:
        md += ["## Lines still missing a word after 2 retries (simplify the wording, same meaning)", "",
               "| Line | Speaker | Text | Not heard | Whisper |", "|---|---|---|---|---|", *report]
    (story / "long/review").mkdir(parents=True, exist_ok=True)
    (story / "long/review/tts_report.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[:5]))


def images(story: Path):
    """long/images.json: new images (style block + no people/text, 16:9, 1K) or reused paid sample images."""
    import shutil
    sys.path.insert(0, str(ROOT / "tools"))
    import gemini_image
    from name_guard import find_names
    from noor_look_test import STYLES
    style = STYLES["a_cinematic_painted"]
    plan = json.loads((story / "long/images.json").read_text(encoding="utf-8"))["images"]
    out = story / "images"
    out.mkdir(exist_ok=True)
    for im in plan:
        f = out / f"{im['id']}.png"
        if f.exists() or "reuse_id" in im:
            continue
        if "reuse" in im:
            shutil.copy(ROOT / im["reuse"], f)
            print(f"{im['id']}: reused (₹0)")
            continue
        if find_names(im["prompt"] + " " + style):
            sys.exit(f"BLOCK (RULES 12a): a name in the prompt of {im['id']}")
        est = pricing.image_estimate_usd(gemini_image.MODEL, "1K", len(im["prompt"]) + len(style), 0) * pricing.usd_to_inr()
        story_budget.check(story.name, est)
        gemini_image.generate(im["prompt"], f, aspect_ratio="16:9", size="1K", style=style)
    print(story_budget.summary_line(story.name))


def main():
    story = (ROOT / sys.argv[1]).resolve() if not Path(sys.argv[1]).is_absolute() else Path(sys.argv[1])
    stage = sys.argv[2]
    if stage == "parse":
        items = parse(story)
        (story / "long/lines.json").write_text(json.dumps(items, ensure_ascii=False, indent=1), encoding="utf-8")
        kinds = {k: sum(1 for i in items if i["kind"] == k) for k in ("line", "cue", "arabic", "screen", "ayah", "section")}
        print(kinds, "| ustaad", sum(1 for i in items if i.get("speaker") == "ustaad"),
              "sawaal", sum(1 for i in items if i.get("speaker") == "sawaal"))
    elif stage == "tts":
        tts(story)
    elif stage == "images":
        images(story)


if __name__ == "__main__":
    main()
