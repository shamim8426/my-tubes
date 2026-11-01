"""TTS for the rocket test Short via make_short.build_voice (cache: audio/tts_cache, same keys as the builder)."""
import json
import sys
from pathlib import Path

D = Path(__file__).parent
ROOT = D.parents[3]
sys.path.insert(0, str(ROOT / "scripts"))
import make_short as ms  # noqa: E402

work = D / "_work"
work.mkdir(exist_ok=True)
lines = json.loads((D / "lines.json").read_text(encoding="utf-8"))
voice, total, timed, events = ms.build_voice(lines, D / "audio", work, run_whisper=True, end_hold=1.2,
                                             gap_s=0.25, gap_change=0.3)
(work / "timed.json").write_text(json.dumps({"total": total, "timed": timed}, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"total {total:.2f}s -> {voice}")
