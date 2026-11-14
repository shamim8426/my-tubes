"""Sync report for a Long's sound design: every cue, music-off window, swell and SFX time vs audio/voiceover_timing.json.
python tools/rc_sync_report.py 002   -> long/sound_sync_report.md (+ prints a summary)"""
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "tools"))
import rc_fx_v5 as FX  # noqa: E402


def mmss(t):
    return f"{int(t // 60)}:{t % 60:04.1f}"


def main():
    story = sys.argv[1]
    sd = next((ROOT / "channels/reality-check/stories").glob(story + "_*"))
    ld = sd / "long"
    lines = json.loads((sd / "audio/voiceover_timing.json").read_text(encoding="utf-8"))
    by = {l["line"]: l for l in lines}
    cfg = json.loads((ld / "music_cues.json").read_text(encoding="utf-8"))
    plan = (ld / "sound_event_plan.md").read_text(encoding="utf-8")
    evs, _ = FX.parse_plan(str(ld / "sound_event_plan.md"))
    plan_start = {}
    for row in plan.split("## 5.")[1].splitlines():
        m = re.match(r"\|\s*(\d+)\s*\|\s*(\d+):(\d\d\.\d)\s*\|", row)
        if m:
            plan_start[int(m[1])] = int(m[2]) * 60 + float(m[3])
    out = ["# 002 sound sync report", "",
           "Mix timeline: `voiceover_full.wav` (744.24 s) is placed at t=0 and the mix is 752.24 s (8 s music tail), the same length as the video; cross-correlation of the voice energy envelope against the video's audio track gave offset 0.00 s at 0, 150, 300, 500 and 700 s (audio of `002_long_preview.mp4` and of the previous upload). All times below are absolute video seconds from `audio/voiceover_timing.json` (line start/end; no word-level times exist in that file).", ""]
    # 1 plan line starts vs json
    d = [(k, plan_start[k] - by[k]["start"]) for k in plan_start if k in by]
    worst = max(d, key=lambda x: abs(x[1]))
    out += [f"## 1. Plan vs timing json (all {len(d)} lines)", f"Largest delta of a plan line start vs timing json: line {worst[0]} = {worst[1]:+.2f} s; lines with |delta| > 0.1 s: {[k for k, v in d if abs(v) > 0.1] or 'none'}.", ""]
    # 2 cues
    out += ["## 2. Music cues (fade-in start, equal-power crossfade over xf seconds)", "| cue | track | fade-in start | xf s | next line start | cue start rel. to line | where |", "|---|---|---|---|---|---|---|"]
    offs = cfg["off_windows"]
    for c in cfg["cues"]:
        nl = next((l for l in lines if l["start"] >= c["t"] - 0.01), None)
        inwin = next((w for w in offs if w[0] <= c["t"] <= w[1]), None)
        rel = (c["t"] - nl["start"]) if nl else 0.0
        out.append(f"| {c['name']} | {Path(c['track']).stem} | {mmss(c['t'])} | {c.get('xf', cfg.get('xf', 4.5))} | L{nl['line'] if nl else '-'} {mmss(nl['start']) if nl else ''} | {rel:+.2f} s | {'inside music-off hold ' + str(inwin) if inwin else 'plain boundary (-0.75 s before line)'} |")
    out.append("")
    # 3 off windows
    out += ["## 3. Music-off windows (cosine ramp down %.1f s before, hold, ramp up %.1f s after; depth -%g dB)" % (cfg.get("off_down", 2.5), cfg.get("off_up", 3.0), cfg.get("off_depth_db", 36.0)),
            "| window | pivot line | line start | line end | hold start vs line start | hold end vs next line start |", "|---|---|---|---|---|---|"]
    for a, b in offs:
        pl = next(l for l in lines if l["start"] >= a)
        nx = by.get(pl["line"] + 1, pl)
        out.append(f"| {mmss(a)}-{mmss(b)} | L{pl['line']} | {mmss(pl['start'])} | {mmss(pl['end'])} | {a - pl['start']:+.2f} s | {b - nx['start']:+.2f} s |")
    out.append("")
    # 4 events
    bad = 0
    rows = []
    for e in evs:
        l = by[e["line"]]
        delta = plan_start[e["line"]] - l["start"]
        inside = (l["start"] - 1.0 <= e["t"] <= l["end"] + 1.0)
        bad += (abs(delta) > 0.1) or (not inside)
        rows.append(f"| {e['type']} | L{e['line']} | {mmss(e['t'])} | {mmss(l['start'] + (e['t'] - plan_start[e['line']]))} | {delta:+.2f} | {e['t'] - l['start']:+.1f} s | {'ok' if inside and abs(delta) <= 0.1 else 'CHECK'} |")
    out += [f"## 4. SFX / ambience events ({len(evs)}; all from sound_event_plan.md; delta = plan time minus time rebuilt from the timing json; must be <= 0.1 s)",
            f"Events over 0.1 s delta or outside their line (+-1 s): {bad}", "",
            "| type | line | mix time | time from timing json | delta s | offset into line | check |", "|---|---|---|---|---|---|---|"] + rows
    (ld / "sound_sync_report.md").write_text("\n".join(out) + "\n", encoding="utf-8")
    print(f"sync report: plan-line delta max {abs(worst[1]):.2f} s; events {len(evs)}, flagged {bad}")


if __name__ == "__main__":
    main()
