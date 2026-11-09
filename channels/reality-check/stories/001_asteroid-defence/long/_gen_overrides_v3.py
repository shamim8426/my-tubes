"""Merge the v3 scene plan (own animated explainer scenes) into footage_overrides.json. Real shots kept: 1,2,3,46 (+48 real replay)."""
import json, sys
from pathlib import Path
d = Path(__file__).parent
ov = json.loads((d / "footage_overrides_v2_backup.json").read_text(encoding="utf-8"))
def sc(lines, typ, sync=None, **kw):
    for n in lines:
        e = {"scene": dict(type=typ, sync=sync or lines[0], **kw)}
        ov[str(n)] = e
sc([4,5,6,7,8], "dhakka_main", 4)
sc([14], "earth_incoming"); sc([15], "airburst_years")
sc([16], "airburst_city", kt=5, label="5 kt = 5,000 t TNT", sub="1 kt = 1,000 ton TNT")
sc([17,18,19,20,21], "chely")
sc([22,23], "unseen")
sc([24], "tunguska_date"); sc([25], "airburst_side"); sc([26], "trees_top"); sc([27], "estimate_swarm")
sc([28,29,30,31,32], "size_ladder")
sc([33,34], "extinction"); sc([35,36], "rare_ladder"); sc([37,38], "known_unknown")
sc([39], "can_we_push"); sc([40], "acronym"); sc([41,42,43], "pair_scale"); sc([44,45], "safe_target")
sc([47], "journey")
ov["48"] = {"status": "REAL", "segs": [{"file": "footage/jhuapl_dart_impact_replay.mp4", "tin": 26.0, "tout": 34.4, "speed": 1.0, "z0": 1.0, "z1": 1.06,
            "crop": [0.2333, 0.0, 0.7667, 1.0], "credit": "NASA/Johns Hopkins APL"}]}
sc([49,50], "push_basic"); sc([51,52], "crit73"); sc([53,54,55,56], "result_orbit"); sc([57,58], "two_methods")
sc([59,60], "still_orbiting"); sc([61,62], "clue")
sc([63,64,65,66], "survey_sky"); sc([67,68,69,70,71], "dots_found"); sc([72,73,74,75], "goals")
sc([76,77,78,79,80], "neo_surveyor"); sc(list(range(81,88)), "yr4_chart"); sc([88], "film_vs_real")
sc(list(range(89,97)), "apophis"); sc([97,98], "recap_dials"); sc(list(range(99,111)), "push_full")
sc([111,112,113,114], "ejecta"); sc([115,116,117,118], "mass_unknown"); sc([119,120,121], "solar_orbit")
sc([122,123,124], "summary3")
sc([125], "method_demo", kind="kinetic", ttl="tareeka 1: kinetic impactor (DART wala dhakka)", need="sabse achha tab chalta hai jab pind ko hum jaante hon|aur chetavani ka samay ho")
sc([126,127], "tractor_demo"); sc([128], "laser_demo"); sc([129,130], "exercise"); sc([131,132,133], "nuclear")
sc([134,135,136,137], "nuclear_caveats"); sc([138,139,140], "film_plan"); sc(list(range(141,149)), "hera")
sc([149,150,151], "unknowns"); sc([152,153,154,155,156], "verdict"); sc([157,158,159], "final3")
# warm flash at block boundaries (chapter starts and the two reveals)
for n in (5, 14, 39, 63, 97, 104, 124, 141, 152):
    ov[str(n)]["scene"]["flash"] = True
(d / "footage_overrides.json").write_text(json.dumps(ov, ensure_ascii=False, indent=1), encoding="utf-8")
print(len(ov))
