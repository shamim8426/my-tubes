"""Synthesise our own light 'tiptoe mystery' music bed (no third-party audio -> no copyright risk).

Usage: python scripts/gen_music.py [seconds]   -> shared/music/mystery_bed.wav
"""
import sys
import wave
from pathlib import Path

import numpy as np

SR = 44100
ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "shared" / "music" / "mystery_bed.wav"
BPM = 104
BEAT = 60 / BPM


def midi_hz(n):
    return 440.0 * 2 ** ((n - 69) / 12)


def pluck(freq, dur, rng, bright=0.5):
    """Karplus-Strong plucked string (pizzicato feel)."""
    n = int(SR * dur)
    period = max(2, int(SR / freq))
    buf = rng.uniform(-1, 1, period)
    out = np.empty(n)
    for i in range(n):
        out[i] = buf[i % period]
        buf[i % period] = 0.996 * (bright * buf[i % period] + (1 - bright) * buf[(i + 1) % period])
    return out * np.exp(-np.linspace(0, 6, n))


def pad(freqs, dur):
    t = np.arange(int(SR * dur)) / SR
    sig = sum(np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * 2.003 * f * t) for f in freqs)
    env = np.minimum(1, t / 0.8) * np.minimum(1, (dur - t) / 0.8)
    return sig * env / len(freqs)


def tick(dur=0.05):
    t = np.arange(int(SR * dur)) / SR
    return np.sin(2 * np.pi * 1800 * t) * np.exp(-t * 90)


def render(seconds: float) -> np.ndarray:
    rng = np.random.default_rng(7)
    total = int(SR * (seconds + 2))
    mix = np.zeros(total)

    def add(sig, at):
        i = int(at * SR)
        j = min(total, i + len(sig))
        if i < total:
            mix[i:j] += sig[: j - i]

    # D minor-ish sneaky pattern: 4 bars, repeated
    chords = [(50, 53, 57), (46, 50, 53), (48, 52, 55), (45, 49, 52)]  # Dm, Bb, C, A
    melody = [62, None, 65, 64, 62, None, 60, 57,
              58, None, 62, 60, 58, None, 57, 55,
              60, None, 64, 62, 60, None, 59, 55,
              57, None, 61, 64, 62, None, None, None]
    bar = 4 * BEAT
    t = 0.0
    step = 0
    while t < seconds:
        bar_i = step // 8 % 4
        if step % 8 == 0:
            add(0.10 * pad([midi_hz(n) for n in chords[bar_i]], bar), t)
            add(0.55 * pluck(midi_hz(chords[bar_i][0] - 12), bar * 0.9, rng, 0.3), t)  # bass
        if step % 2 == 0:
            add(0.05 * tick(), t)  # clock tick
        note = melody[step % 32]
        if note is not None:
            add(0.35 * pluck(midi_hz(note), BEAT * 1.5, rng, 0.6), t)
        t += BEAT / 2
        step += 1

    mix = mix[: int(SR * seconds)]
    fade = int(SR * 1.5)
    mix[:fade] *= np.linspace(0, 1, fade)
    mix[-fade:] *= np.linspace(1, 0, fade)
    return mix / (np.abs(mix).max() + 1e-9) * 0.7


def main(seconds=70.0):
    mono = render(seconds)
    # gentle stereo: tiny delay on right channel
    d = int(SR * 0.012)
    right = np.concatenate([np.zeros(d), mono[:-d]])
    stereo = (np.stack([mono, right], axis=1) * 32767).astype(np.int16)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(OUT), "wb") as w:
        w.setnchannels(2)
        w.setsampwidth(2)
        w.setframerate(SR)
        w.writeframes(stereo.tobytes())
    print("saved", OUT)


if __name__ == "__main__":
    main(float(sys.argv[1]) if len(sys.argv) > 1 else 70.0)
