"""Noor-e-Raah narrator audition (user 2026-10-24): FREE key only (stops on 429, never the paid key), then a Whisper
check of the nuqta words. Output: channels/noor-e-raah/characters/voices/audition_<date>/ (<voice>.wav, all_voices.m3u,
audition.md).

    .venv\\Scripts\\python -X utf8 scripts\\noor_audition.py [--whisper-only]
"""
import sys
import wave
from datetime import date
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import gemini_keys  # noqa: E402
import gemini_tts  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "channels" / "noor-e-raah" / "characters" / "voices" / f"audition_{date.today().isoformat()}"
VOICES = ["Iapetus", "Algieba", "Schedar", "Rasalgethi", "Sulafat", "Erinome"]
STYLE = ("Calm, respectful Indian Hindi-Urdu narrator explaining the Quran to families: warm, steady and clear, correct "
         "Urdu nuqta sounds (ज़, फ़, क़, ख़, ग़), unhurried medium-slow pace, gentle reverence, no drama, never singing "
         "or chanting")
PARAGRAPH = ("सूरह अल-फ़ातिहा क़ुरआन की पहली सूरह है। फ़ातिहा का मतलब है — खोलने वाली। इसमें सात आयतें हैं, "
             "और ज़्यादातर उलमा के मुताबिक़ यह मक्का में नाज़िल हुई। हर नमाज़ में पढ़ी जाने वाली यह सूरह, "
             "अल्लाह की तारीफ़ से शुरू होती है और सीधे रास्ते की दुआ पर ख़त्म होती है।")
HARD = ("शान-ए-नुज़ूल की यह बात तफ़सीर इब्न कसीर में दर्ज है: हम्द, ग़ैब पर ईमान, क़यामत का दिन, "
        "और सिरात-ए-मुस्तक़ीम की ख़्वाहिश।")
TEXT = PARAGRAPH + " ... " + HARD
NUQTA_WORDS = ["फ़ातिहा", "क़ुरआन", "ज़्यादातर", "मुताबिक़", "नाज़िल", "नमाज़", "तारीफ़", "ख़त्म",
               "नुज़ूल", "तफ़सीर", "ग़ैब", "क़यामत", "मुस्तक़ीम", "ख़्वाहिश"]
NUQTA = str.maketrans({"़": None})  # combining nuqta
PRECOMPOSED = {"ज़": "ज", "फ़": "फ", "क़": "क", "ख़": "ख", "ग़": "ग", "ड़": "ड", "ढ़": "ढ"}


SPELLING = {"ं": "न", "ँ": "न", "्": "", "ू": "ु", "ी": "ि", "ै": "े", "ौ": "ो", "ा": "", "ह": ""}  # Whisper's spelling


def plain(s: str) -> str:
    """Nuqta removed and common Whisper spelling variants folded (बंदा = बन्दा, सूरह = सुरा)."""
    for a, b in PRECOMPOSED.items():
        s = s.replace(a, b)
    s = s.translate(NUQTA)
    for a, b in SPELLING.items():
        s = s.replace(a, b)
    return s


def synth():
    OUT.mkdir(parents=True, exist_ok=True)
    for v in VOICES:
        out = OUT / f"{v}.wav"
        if out.exists():
            print(f"{v}: already there, skipped")
            continue
        try:
            res = gemini_tts.speak(TEXT, v, STYLE, out, free_only=True)
        except gemini_keys.FreeQuotaOver as e:
            print(f"STOP: {e}")
            return False
        print(f"{v}: {res['seconds']:.1f}s, cost row {res['row']['cost_inr']} (free)")
    return True


def whisper_check():
    import numpy as np
    from faster_whisper import WhisperModel

    model = WhisperModel("small", device="cpu", compute_type="int8",
                         download_root=str(ROOT / "tools" / "whisper-models"))
    rows = []
    for v in VOICES:
        f = OUT / f"{v}.wav"
        if not f.exists():
            continue
        with wave.open(str(f)) as w:
            sr = w.getframerate()
            x = np.frombuffer(w.readframes(w.getnframes()), np.int16).astype(np.float32) / 32768
        secs = len(x) / sr
        x16 = np.interp(np.arange(0, len(x), sr / 16000), np.arange(len(x)), x).astype(np.float32)  # as make_short
        segs, _ = model.transcribe(x16, language="hi", beam_size=5)
        text = " ".join(s.text.strip() for s in segs)
        heard = [clean(w) for w in plain(text).split()]
        script = [w for w in TEXT.replace("...", " ").split() if clean(w)]
        missed = [w for w in script if not found(clean(plain(w)), heard)]  # script words Whisper did not hear
        nuqta_missed = [w for w in NUQTA_WORDS if not found(clean(plain(w)), heard)]
        rows.append((v, secs, len(script) / secs, len(script) - len(missed), len(script), missed, nuqta_missed, text))
    return rows


def clean(w: str) -> str:
    return "".join(c for c in w if c.isalnum() or "ऀ" <= c <= "ॿ").strip("।")


def found(word: str, heard: list, cutoff=0.7) -> bool:
    """Whisper small writes Hindi without nuqta and joins/splits words; so: nuqta removed on both sides, then a word
    (or two heard words joined) that is >= 70 % similar counts as heard."""
    from difflib import SequenceMatcher
    cands = heard + [a + b for a, b in zip(heard, heard[1:])]
    return any(SequenceMatcher(None, word, c).ratio() >= cutoff or (len(word) >= 2 and word in c) for c in cands)


def main():
    if "--whisper-only" not in sys.argv and not synth():
        return
    rows = whisper_check()
    (OUT / "all_voices.m3u").write_text("#EXTM3U\n" + "".join(f"#EXTINF:-1,{r[0]}\n{r[0]}.wav\n" for r in rows),
                                        encoding="utf-8")
    md = [f"# Narrator audition — {date.today().isoformat()} (free key, ₹0)", "",
          f"Style: {STYLE}", "", f"Text: {TEXT}", "",
          f"Nuqta words checked ({len(NUQTA_WORDS)}): {', '.join(NUQTA_WORDS)}", "",
          "Whisper small writes Hindi without nuqta, so nuqta SOUNDS cannot be proven by it: words are matched with nuqta "
          "removed (>= 70 % similar). Listen for ज़/फ़/क़/ख़/ग़ yourself.", "",
          "| Voice | Length | Words/s | Script words heard | Not heard (possible skip / unclear) | Nuqta words not heard |",
          "|---|---|---|---|---|---|"]
    md += [f"| {v} | {s:.1f}s | {wps:.2f} | {ok}/{n} | {', '.join(m) or '-'} | {', '.join(q) or '-'} |"
           for v, s, wps, ok, n, m, q, _ in rows]
    md += ["", "## Whisper transcripts", ""] + [f"- **{r[0]}:** {r[7]}" for r in rows]
    (OUT / "audition.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n".join(md[6:6 + 2 + len(rows)]))
    print("->", (OUT / "audition.md").relative_to(ROOT).as_posix())


if __name__ == "__main__":
    main()
