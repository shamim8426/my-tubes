"""Build the reusable MOOD MUSIC LIBRARY (all channels): shared/music/mood_library.json + shared/music/MOOD_LIBRARY.md.
python tools/rc_mood_library.py [--pieces /path/to/incompetech_pieces.json]
Per track: path, licence + credit line, length, usable start / loop end, measured features (beat strength, onset density, brightness,
sub share <150 Hz, mid share 150 Hz-2 kHz = audible on phones, steadiness, repetitiveness), source tags (incompetech feel/genre/instruments
when known) and a one-line description. Excluded: mostly sub-bass (mid share < 25 %), vocals, or strong drums."""
import argparse
import csv
import json
import subprocess
import sys
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import rc_music_pick as MP  # noqa: E402

FF = str(ROOT / "tools/ffmpeg/ffmpeg.exe")
M = "shared/music/"
DEFAULT_BED = M + "doc2/Ossuary_6_Air.mp3"
# mood -> [(path, one-line description)]  (descriptions = our listening notes + the measured features)
MOODS = {
    "curious_mystery": [(M + "tension/Investigations.mp3", "light detective pizzicato/keys, curious, not scary"),
                        (M + "tension/Hidden_Agenda.mp3", "quiet suspicious synth + bass line, 'something is off'"),
                        (M + "neutral/Dreamy_Flashback.mp3", "soft dreamy electronic texture, gentle movement, curious")],
    "calm_wonder": [(M + "neutral/Ethereal_Relaxation.mp3", "slow airy synth pad, 28 min, thoughtful wonder"),
                    (M + "neutral/Fresh_Air.mp3", "calm open pad with soft piano colour, morning feel"),
                    (M + "noor/Quietude_Sections_Merged.mp3", "ambient synth soundscape, evolving, neutral and calm")],
    "rising_tension": [(M + "doc2/Disquiet.mp3", "uneasy low strings and pads, slowly building, no drums"),
                       (M + "doc2/Gathering_Darkness.mp3", "pulsing dark synth build, ominous, cinematic"),
                       (M + "doc2/Epic_Unease.mp3", "tense sustained strings, short (needs looping)"),
                       (M + "doc2/Unseen_Horrors.mp3", "thin suspense texture, high tension, use low")],
    "danger_dark": [(M + "doc2/Giant_Wyrm.mp3", "heavy low strings and drones, menacing, slow"),
                    (M + "clean/Lightless_Dawn.mp3", "dark slow pad, bleak, serious"),
                    (M + "doc2/Dark_Fog.mp3", "dark pulsing atmosphere, foreboding")],
    "loss_somber": [(M + "dukh/Sad_Trio.mp3", "sad slow string trio, grief"),
                    (M + "seekh/Peaceful_Desolation.mp3", "lonely sparse pad and piano, empty world"),
                    (M + "doc/Meditation_Impromptu_02.mp3", "slow sad piano with pad, quiet loss"),
                    (M + "dukh/Heartbreaking.mp3", "emotional strings, heavy sadness (use rarely)")],
    "hope_recovery": [(M + "doc2/Inspired.mp3", "warm steady strings/pad, gentle optimism"),
                      (M + "neutral/Healing.mp3", "soft healing pads, recovery, warm"),
                      (M + "neutral/Lasting_Hope.mp3", "slow hopeful piano and strings"),
                      (M + "neutral/Airship_Serenity.mp3", "floating calm synths, quietly uplifting"),
                      (M + "neutral/Reawakening.mp3", "piano and cello, gentle recovery"),
                      (M + "neutral/Wish_Background.mp3", "soft piano/strings/celesta bed, 19 min, hopeful")],
    "time_night": [(M + "neutral/Mesmerize.mp3", "slow evolving electronic texture, hypnotic, night"),
                   (M + "doc2/Rising_Tide.mp3", "steady soft pulse, clock-like motion, no drums"),
                   (M + "neutral/Clean_Soul.mp3", "warm slow electronic ambience, late-night calm")],
    "reflective_serious": [(M + "doc/Meditation_Impromptu_01.mp3", "slow solo piano, thoughtful, serious"),
                           (M + "doc/Meditation_Impromptu_03.mp3", "slow piano, reflective, a little warmer"),
                           (M + "doc/Gymnopedie_No_1.mp3", "classic slow piano, calm reflection")],
    "discovery_awe": [(M + "neutral/Bathed_in_the_Light.mp3", "bright swelling pads, sense of awe"),
                      (M + "neutral/Ascending_the_Vale.mp3", "rising cinematic pads/strings, discovery"),
                      (M + "doc2/Ossuary_1_A_Beginning.mp3", "spacious ambient opening, wonder"),
                      (M + "noor/Soaring.mp3", "uplifting strings, big open feel (use low)")],
    "ending_resolution": [(M + "doc2/Ossuary_5_Rest.mp3", "calm resolving ambient, closure"),
                          (M + "jaadu/Dreams_Become_Real.mp3", "gentle warm pad/piano, soft resolution"),
                          (M + "jaadu/Enchanted_Valley.mp3", "soft airy textures, peaceful ending")],
}
CREDIT = '"{t}" Kevin MacLeod (incompetech.com) Licensed under Creative Commons: By Attribution 4.0 License http://creativecommons.org/licenses/by/4.0/'


def bands_and_points(p):
    raw = subprocess.run([FF, "-v", "error", "-i", str(ROOT / p), "-ac", "1", "-ar", "16000", "-f", "f32le", "-"], capture_output=True).stdout
    x = np.frombuffer(raw, np.float32)
    sr = 16000
    dur = len(x) / sr
    seg = x[: min(len(x), 240 * sr)]
    X = np.abs(np.fft.rfft(seg)) ** 2
    f = np.fft.rfftfreq(len(seg), 1 / sr)
    tot = X.sum() + 1e-12
    sub, mid = X[f < 150].sum() / tot, X[(f >= 150) & (f < 2000)].sum() / tot
    r = np.array([np.sqrt((x[i:i + sr] ** 2).mean()) + 1e-9 for i in range(0, len(x) - sr, sr)])
    rdb = 20 * np.log10(r)
    med = np.median(rdb)
    start = float(np.argmax(rdb > med - 20))
    above = np.where(rdb > med - 15)[0]
    loop_end = float(max(start + 10, above[-1] - 2)) if len(above) else dur
    return dur, float(sub), float(mid), start, loop_end


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--pieces", default="")
    a = ap.parse_args()
    pieces = {}
    if a.pieces and Path(a.pieces).exists():
        for q in json.loads(Path(a.pieces).read_text(encoding="utf-8")):
            pieces[q["title"].lower().replace("-", " ").replace("  ", " ")] = q
    lic = {r[0].replace("\\", "/"): r for r in csv.reader(open(ROOT / "shared/assets_license.csv", encoding="utf-8", newline=""))}
    rows_new = []
    lib = {"default_bed": DEFAULT_BED, "_note": "Channel default/permanent bed (user pick 2026-11-15). Scenes use mood tracks per script via tools/rc_music_select.py.", "moods": {}, "excluded": []}
    for mood, items in MOODS.items():
        lib["moods"][mood] = []
        for path, desc in items + ([(DEFAULT_BED, "default channel bed: airy dark-neutral ambient (needs mid EQ on phones)")] if mood == "calm_wonder" else []):
            if not (ROOT / path).exists():
                print("missing", path)
                continue
            title = Path(path).stem.replace("_", " ")
            key = title.lower().replace("-", " ").replace("  ", " ")
            pc = pieces.get(key) or next((v for k, v in pieces.items() if k.replace(" ", "") == key.replace(" ", "")), None)
            f = MP.feats(ROOT / path) or {}
            dur, sub, mid, start, loop_end = bands_and_points(path)
            if "Quietude" in path:
                author, licence, credit = "The Imperfectionist (freemusicarchive.org)", "CC BY 4.0", '"Quietude - Ambient Synth Soundscape" by The Imperfectionist, CC BY 4.0 http://creativecommons.org/licenses/by/4.0/'
            else:
                author, licence, credit = "Kevin MacLeod", "CC BY 4.0", CREDIT.format(t=pc["title"] if pc else title)
            if path not in lic:
                rows_new.append([path, "https://incompetech.com/music/royalty-free/mp3-royaltyfree/" + (pc["filename"] if pc else title + ".mp3").replace(" ", "%20"), author, licence, credit, "2026-11-15"])
            inst = (pc or {}).get("instruments", "") or ""
            why = []
            if mid < 0.25:
                why.append(f"mostly sub-bass (mid share {mid:.0%})")
            if any(w in inst.lower() for w in ("vocal", "voice", "choir")):
                why.append("vocals")
            if "drum" in inst.lower() and f.get("tconf", 0) > 0.6:
                why.append("strong drums")
            rec = dict(path=path, title=pc["title"] if pc else title, mood=mood, licence=licence, author=author, credit=credit,
                       length_s=round(dur, 1), usable_start_s=start, loop_end_s=loop_end,
                       beat_strength=round(f.get("tconf", 0), 2), onsets_per_s=round(f.get("dens", 0), 2), brightness_hz=round(f.get("cen", 0)),
                       dynamics_db=round(f.get("dyn", 0), 1), repetitiveness=round(f.get("sim", 0), 2),
                       sub_share=round(sub, 2), mid_share_150_2k=round(mid, 2),
                       source_tags={k: (pc or {}).get(k) for k in ("feel", "instruments", "bpm", "description")} if pc else {"feel": "n/a (non-incompetech)"},
                       description=desc, default_bed=(path == DEFAULT_BED))
            if why and path != DEFAULT_BED:
                rec["excluded_because"] = ", ".join(why)
                lib["excluded"].append(rec)
            else:
                lib["moods"][mood].append(rec)
            print(f"{mood:18s} {rec['title'][:26]:26s} mid {mid:.0%} sub {sub:.0%} beat {rec['beat_strength']} {'EXCL ' + ', '.join(why) if why and path != DEFAULT_BED else ''}", flush=True)
    if rows_new:
        with open(ROOT / "shared/assets_license.csv", "a", encoding="utf-8", newline="") as fh:
            csv.writer(fh).writerows(rows_new)
    (ROOT / "shared/music/mood_library.json").write_text(json.dumps(lib, ensure_ascii=False, indent=1), encoding="utf-8")
    md = ["# Mood music library (all channels)", "",
          f"Default / permanent channel bed: `{DEFAULT_BED}` (Kevin MacLeod \"Ossuary 6 - Air\", CC BY 4.0; user pick 2026-11-15). Scenes switch to mood tracks per the script's cue sheet via `tools/rc_music_select.py`, which feeds `tools/rc_music_mix.py` (speaker-band calibration: music 10-13 LU under the voice in 150 Hz-8 kHz, 4-6 s equal-power crossfades at section boundaries, smooth music-off ramps at pivots, sub booms only at section starts, no whooshes/sweeps).",
          "Rules: no track twice in a row; mid share (150 Hz-2 kHz) >= 25 % so it is audible on phones; no vocals, no strong drums. Data per track in `mood_library.json` (length, usable start / loop end, beat strength, onsets/s, brightness, sub/mid share, repetitiveness, incompetech feel/instruments tags). Rebuild: `python tools/rc_mood_library.py --pieces <incompetech pieces.json>`.", ""]
    for mood, recs in lib["moods"].items():
        md.append(f"## {mood}")
        for r in recs:
            md.append(f"- **{r['title']}** ({r['length_s'] / 60:.1f} min, {r['licence']}): {r['description']}. Beat {r['beat_strength']}, onsets {r['onsets_per_s']}/s, brightness {r['brightness_hz']} Hz, mid {r['mid_share_150_2k']:.0%}, sub {r['sub_share']:.0%}. `{r['path']}`")
        md.append("")
    md.append("## Excluded (kept for reference)")
    for r in lib["excluded"]:
        md.append(f"- {r['title']} ({r['mood']}): {r['excluded_because']}")
    md += ["", "Credit lines: every track's `credit` field in mood_library.json goes in the description when used (CC BY 4.0)."]
    (ROOT / "shared/music/MOOD_LIBRARY.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("moods:", {k: len(v) for k, v in lib["moods"].items()}, "excluded:", len(lib["excluded"]), "new licence rows:", len(rows_new))


if __name__ == "__main__":
    main()
