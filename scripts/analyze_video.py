"""Analyse a video's pacing/audio for learning (no content reuse).

Usage: python scripts/analyze_video.py <video> <out_dir> [cuts.txt]
Writes <out_dir>/transcript.txt and prints a JSON summary.
Music-vs-voice and pitch numbers are estimates (no source separation).
"""
import json
import shutil
import subprocess
import sys
from pathlib import Path

import numpy as np
from faster_whisper import WhisperModel

ROOT = Path(__file__).resolve().parent.parent
FFMPEG = ROOT / "tools" / "ffmpeg" / "ffmpeg.exe"
if not FFMPEG.exists():  # new system: ffmpeg from winget on PATH (tools/ffmpeg is not in git)
    FFMPEG = Path(shutil.which("ffmpeg") or FFMPEG)
MODELS = ROOT / "tools" / "whisper-models"
SR = 16000


def load_audio(path):
    raw = subprocess.run([str(FFMPEG), "-v", "error", "-i", str(path), "-ac", "1", "-ar", str(SR), "-f", "s16le", "-"],
                         capture_output=True, check=True).stdout
    return np.frombuffer(raw, np.int16).astype(np.float32) / 32768


def db(x):
    return 20 * np.log10(np.sqrt(np.mean(x ** 2)) + 1e-9)


def f0(seg):
    """Median pitch (Hz) of a speech chunk via autocorrelation, None if unvoiced."""
    win, hop, vals = int(0.04 * SR), int(0.02 * SR), []
    lo, hi = SR // 400, SR // 70
    for i in range(0, len(seg) - win, hop):
        fr = seg[i:i + win] - seg[i:i + win].mean()
        if np.sqrt(np.mean(fr ** 2)) < 0.01:
            continue
        ac = np.correlate(fr, fr, "full")[win - 1:]
        if ac[0] <= 0:
            continue
        lag = lo + int(np.argmax(ac[lo:hi]))
        if ac[lag] / ac[0] > 0.5:
            vals.append(SR / lag)
    return float(np.median(vals)) if len(vals) > 5 else None


def main(video, out_dir, cuts_file=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    audio = load_audio(video)
    dur = len(audio) / SR

    model = WhisperModel("small", device="cpu", compute_type="int8", download_root=str(MODELS))
    # pass the array: faster-whisper's own PyAV decode is broken with the installed av version
    segs, _ = model.transcribe(audio, language="hi", word_timestamps=True, vad_filter=False, beam_size=1)
    segs = [s for s in segs if s.text.strip()]
    words = [w for s in segs for w in (s.words or [])]
    (out_dir / "transcript.txt").write_text(
        "\n".join(f"[{s.start:7.2f}-{s.end:7.2f}] {s.text.strip()}" for s in segs), encoding="utf-8")

    # pacing
    speech_time = sum(w.end - w.start for w in words)
    gaps = [b.start - a.end for a, b in zip(segs, segs[1:]) if 0 <= b.start - a.end < 5]
    hook = " ".join(w.word.strip() for w in words if w.start < 10)

    # voice vs music level: frames inside words vs frames >=0.3s away from any word
    frame = int(0.05 * SR)
    n = len(audio) // frame
    mask_speech = np.zeros(n, bool)
    mask_near = np.zeros(n, bool)
    for w in words:
        a, b = int(w.start * SR) // frame, int(w.end * SR) // frame + 1
        mask_speech[a:b] = True
        mask_near[max(0, a - 6):b + 6] = True
    frames = audio[: n * frame].reshape(n, frame)
    lev = 20 * np.log10(np.sqrt((frames ** 2).mean(1)) + 1e-9)
    speech_db = float(np.median(lev[mask_speech])) if mask_speech.any() else None
    gap_frames = lev[~mask_near]
    music_frames = gap_frames[gap_frames > -55]  # ignore true silence
    music_db = float(np.median(music_frames)) if len(music_frames) else None
    music_presence = float(len(music_frames) / max(1, len(gap_frames)))

    # music level over time (10s windows of non-speech frames) -> big shifts
    shifts, prev = [], None
    for t0 in range(0, int(dur), 10):
        sel = (~mask_near[t0 * 20:(t0 + 10) * 20])
        chunk = lev[t0 * 20:(t0 + 10) * 20][sel]
        chunk = chunk[chunk > -55]
        cur = float(np.median(chunk)) if len(chunk) > 10 else None
        if prev is not None and cur is not None and abs(cur - prev) > 6:
            shifts.append((t0, round(prev, 1), round(cur, 1)))
        prev = cur if cur is not None else prev

    # pitch per segment
    pitches = [p for s in segs if (p := f0(audio[int(s.start * SR):int(s.end * SR)]))]
    bands = {"<140Hz (deep male)": 0, "140-200 (male)": 0, "200-260 (female/high male)": 0, ">260 (child/high)": 0}
    for p in pitches:
        k = list(bands)[0 if p < 140 else 1 if p < 200 else 2 if p < 260 else 3]
        bands[k] += 1

    cuts = []
    if cuts_file and Path(cuts_file).exists():
        cuts = [float(x) for x in Path(cuts_file).read_text(encoding="utf-8-sig").split()]
    edges = [0.0] + cuts + [dur]
    shots = np.diff(edges)

    summary = {
        "duration_s": round(dur, 1),
        "cuts": len(cuts),
        "avg_shot_s": round(float(shots.mean()), 2),
        "median_shot_s": round(float(np.median(shots)), 2),
        "avg_shot_first60s": round(float(np.diff([0.0] + [c for c in cuts if c < 60] + [min(60, dur)]).mean()), 2),
        "words": len(words),
        "wpm_overall": round(len(words) / (dur / 60), 1),
        "wpm_while_speaking": round(len(words) / (speech_time / 60), 1) if speech_time else None,
        "hook_first_10s": hook,
        "line_gap_avg_s": round(float(np.mean(gaps)), 2) if gaps else None,
        "line_gap_median_s": round(float(np.median(gaps)), 2) if gaps else None,
        "speech_level_db": round(speech_db, 1) if speech_db is not None else None,
        "music_only_level_db": round(music_db, 1) if music_db is not None else None,
        "music_below_voice_db": round(speech_db - music_db, 1) if speech_db is not None and music_db is not None else None,
        "music_present_in_gaps": round(music_presence, 2),
        "music_level_shifts": shifts[:30],
        "segment_pitch_bands": bands,
        "segment_pitch_median_hz": round(float(np.median(pitches)), 1) if pitches else None,
    }
    (out_dir / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main(*sys.argv[1:])
