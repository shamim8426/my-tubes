"""v4: v3 own-animation scenes + real NASA footage mixed back in (sub-cuts 'real' and 'under' layers via scene['mix'], see tools/rc_explain._prep_mix).
Source: footage_overrides_v3_backup.json. Output: footage_overrides.json. Real cuts only where the footage shows what the line says."""
import json
from pathlib import Path
d = Path(__file__).parent
ov = json.loads((d / "footage_overrides_v3_backup.json").read_text(encoding="utf-8"))
tim = json.loads((d.parent / "audio/voiceover_timing.json").read_text(encoding="utf-8"))
DUR = {l["line"]: l["end"] - l["start"] for l in tim}
CE = [0.2333, 0.0, 0.7667, 1.0]
HAPL, GSFC, JPL = "NASA/Johns Hopkins APL", "NASA Goddard (Suomi NPP)", "NASA/JPL-Caltech (What's Up)"
DRP = "footage/jhuapl_dart_impact_replay.mp4"
CH = "footage2/history_impacts/chelyabinsk_bolide_plume.mp4"
PER21 = "footage2/meteors/whatsup_perseids_2021.mp4"
PER22 = "footage2/meteors/whatsup_perseids_2022.mp4"
NEO = "footage2/asteroids/neowise_legacy.mp4"
RECAP = "footage/nasa_dart_recap_large.mp4"
APH = "footage/svs_apophis_beauty_1080p.mp4"
SUN = "footage2/sun/gradient_sun.mp4"
SOHO = "footage2/comets/sungrazers_sdo.mp4"
NC = [0, .1, 1, 1]


def D_(n):
    return "footage/" + n


def R(a, b, f, tin=None, tout=None, credit="", mode="real", cap=None, crop=None, dim=None, **kw):
    m = dict(a=a, b=b, mode=mode, file=f, credit=credit)
    if tin is not None:
        m["tin"], m["tout"] = tin, (tout if tout is not None else tin + ((b or 8) - a))
    if cap:
        m["cap"] = cap
    if crop:
        m["crop"] = crop
    if dim:
        m["dim"] = dim
    m.update(kw)
    return m


def U(f, credit, dim=0.5, a=0, b=None, **kw):   # real layer behind the scene (still with slow move, or video)
    return R(a, b, f, credit=credit, mode="under", dim=dim, **kw)


MIX = {
    4: [R(0, 2.8, DRP, 22, 24.8, HAPL, cap="Real DART footage: final approach", crop=CE)],
    6: [U(D_("draco_dimorphos_mosaic.png"), HAPL)],
    14: [R(0, 2.0, "footage2/earth/iss_earth_views_hq.mp4", 57, 59, "NASA (ISS)")],
    15: [R(0, 3.4, "footage2/earth/airglow_iss.mp4", 0.5, 4.0, "NASA/GOLD, ISS", cap="Atmosphere seen from the ISS")],
    17: [R(0, 3.0, CH, 19, 22.2, GSFC, crop=[0, .14, 1, 1], cap="Real: Chelyabinsk trail from orbit")],
    18: [R(0, 3.2, PER21, 28, 31.4, JPL, crop=[0, 0, 1, .9], cap="Real meteors")],
    19: [R(2.2, 5.5, CH, 118, 121.4, GSFC, crop=[0, .14, 1, 1])],
    22: [R(0, 2.5, SOHO, 86, 88.6, "NASA/ESA SOHO", cap="Real: the sky next to the Sun (SOHO)")],
    28: [R(0, 3.0, CH, 100, 103.2, GSFC, crop=[0, .14, 1, 1])],
    32: [R(3.6, None, "footage2/craters/chicxulub_yucatan_relief.jpg", credit="NASA/JPL", cap="Real: Chicxulub, Mexico (radar relief)")],
    33: [U("footage2/craters/chicxulub_yucatan_relief.jpg", "NASA/JPL", k=1)],
    39: [R(0, 3.6, RECAP, 37.5, 41.2, "NASA (DART launch)", cap="Real: DART launch")],
    44: [U(D_("draco_system_northup.png"), HAPL)],
    45: [U(D_("draco_didymos_northup.png"), HAPL, k=1)],
    47: [R(0, 2.8, RECAP, 42.0, 44.9, "NASA (DART launch)")],
    50: [R(0, 2.8, DRP, 31.4, 34.2, HAPL, crop=CE, cap="Real: DART's last seconds")],
    57: [R(0, 3.4, D_("jhuapl_observing_campaign_telescopes.png"), credit="NASA/JHUAPL", cap="Real: telescopes that watched Dimorphos")],
    58: [R(0, 3.2, D_("jhuapl_orbit_period_lightcurve.jpg"), credit="NASA/JHUAPL/Czech Acad. Sci.", cap="Real light curve data")],
    59: [R(0, 3.4, D_("draco_dimorphos_mosaic.png"), credit=HAPL, k=2)],
    63: [R(0, 2.6, PER22, 34.0, 36.8, JPL, cap="Telescope")],
    65: [R(0, 3.2, "footage2/surveys/catalina_small_asteroid.jpg", credit="NASA/JPL-Caltech/CSS-Univ. of Arizona", cap="Real: Catalina survey image")],
    66: [R(0, 3.6, "footage2/surveys/catalina_2018la.jpg", credit="NASA/JPL-Caltech/CSS-Univ. of Arizona", k=1)],
    67: [R(0, 3.0, NEO, 98, 101.2, JPL, crop=NC)],
    70: [R(0, 3.0, NEO, 50.5, 53.7, JPL, crop=NC)],
    72: [R(0, 3.0, NEO, 160.5, 163.7, JPL, crop=NC)],
    76: [R(0, 4.2, NEO, 122, 126.4, JPL, crop=NC, cap="Real: NEOWISE infrared telescope")],
    78: [R(0, 3.4, D_("pia26388_neo_surveyor_concept.jpg"), credit="NASA/JPL-Caltech (concept)")],
    79: [R(0, 3.0, NEO, 126.4, 129.6, JPL, crop=NC)],
    81: [R(0, 3.6, NEO, 73.5, 77.3, JPL, crop=NC)],
    85: [R(0, 3.6, NEO, 154, 157.8, JPL, crop=NC)],
    89: [R(0, 4.2, APH, 0.2, 4.6, "NASA/Goddard SVS (animation)", cap="Apophis (NASA animation)")],
    90: [U(D_("pia24168_apophis_radar.jpg"), "NASA/JPL-Caltech, NSF/AUI/GBO", dim=0.55)],
    91: [R(0, 3.6, APH, 4.6, 8.4, "NASA/Goddard SVS (animation)")],
    93: [R(0, 4.2, D_("pia23195_apophis.jpg"), credit="NASA/JPL-Caltech (illustration)")],
    95: [U(D_("pia24168_apophis_radar.jpg"), "NASA/JPL-Caltech, NSF/AUI/GBO", dim=0.55, k=1)],
    97: [U(D_("draco_didymos_northup.png"), HAPL)],
    99: [R(0, 3.0, DRP, 31.2, 34.4, HAPL, crop=CE, cap="Real: DART's last images")],
    101: [U(D_("draco_dimorphos_northup.png"), HAPL)],
    103: [R(0, 3.2, D_("draco_final_image.png"), credit=HAPL, cap="Real: Dimorphos boulders, DRACO camera")],
    105: [U(D_("jhuapl_llnl_impact_simulation.png"), "NASA/JHUAPL/LLNL (simulation)")],
    107: [R(0, 3.2, D_("draco_last_image_all_dimorphos.png"), credit=HAPL, k=1)],
    109: [U(D_("draco_dimorphos_mosaic.png"), HAPL, k=1)],
    111: [R(0, 2.6, DRP, 33.0, 34.4, HAPL, crop=CE, speed=0.55, cap="Real: impact flash")],
    116: [U(D_("draco_system_northup.png"), HAPL, k=2)],
    118: [R(0, 3.4, D_("draco_last_image_both_asteroids.png"), credit=HAPL)],
    120: [U(SUN, "NASA/SDO", dim=0.5, tin=43, tout=55)],
    125: [R(0, 4.0, DRP, 22.0, 26.0, HAPL, crop=CE, cap="Real: DART (kinetic impactor)")],
    143: [U(D_("draco_dimorphos_northup.png"), HAPL, k=1)],
    146: [U(D_("draco_last_image_both_asteroids.png"), HAPL, k=2)],
    157: [R(0, 3.6, "footage2/earth/orion_earth_timelapse.mp4", 60, 63.6, "NASA/Orion")],
    158: [R(0, 4.0, "footage2/earth/iss_aurora_kopra.jpg", credit="NASA/ISS")],
    159: [U("footage2/earth/orion_earth_2026.jpg", "NASA/Orion", dim=0.6)],
}
for n, mix in MIX.items():
    ov[str(n)]["scene"]["mix"] = mix

# ---- auto-fill: real layer behind every drawn shot whose subject is a real object (topic pools); explicit cuts above stay
HP = [(D_(x), HAPL) for x in ("draco_dimorphos_mosaic.png", "draco_dimorphos_northup.png", "draco_system_northup.png", "draco_didymos_northup.png",
      "draco_final_image.png", "draco_last_image_all_dimorphos.png", "draco_last_image_both_asteroids.png", "jhuapl_dart_before_impact_closeup.png")]
NEOP = [(NEO, JPL, dict(tin=73.5, crop=NC)), (D_("pia25253_neo_surveyor_starfield.jpg"), "NASA/JPL-Caltech"), (NEO, JPL, dict(tin=154, crop=NC)),
        ("footage2/surveys/neowise_new_find.jpg", "NASA/JPL-Caltech"), (NEO, JPL, dict(tin=98, crop=NC)), ("footage2/surveys/neowise_opens_eyes.jpg", "NASA/JPL-Caltech")]
APP = [(APH, "NASA/Goddard SVS (animation)", dict(tin=0.2)), ("footage2/radar/goldstone_2017ye5.jpg", "NASA/JPL-Caltech"),
       (D_("pia24168_apophis_radar.jpg"), "NASA/JPL-Caltech, NSF/AUI/GBO"), ("footage2/radar/goldstone_peanut_asteroid.jpg", "NASA/JPL-Caltech")]
EARTH = [("footage2/earth/iss_earth_views_hq.mp4", "NASA (ISS)", dict(tin=29)), ("footage2/earth/black_marble_night.mp4", "NASA Earth Observatory", dict(tin=24)),
         ("footage2/earth/orion_earth_timelapse.mp4", "NASA/Orion", dict(tin=40)), ("footage2/earth/iss_earth_views_hq.mp4", "NASA (ISS)", dict(tin=86))]
NUKE = [("footage2/scale_analogies/castle_bravo_blast.jpg", "US DOE (public domain)"), ("footage2/scale_analogies/castle_romeo.jpg", "US DOE (public domain)")]
SKY = [("footage2/space/milky_way_glimpse.jpg", "NASA"), ("footage2/space/milky_way_center_dust.jpg", "NASA")]
POOLS = [(range(5, 9), HP), (range(49, 63), HP), (range(97, 125), HP), (range(141, 152), HP), (range(115, 119), HP),
         (range(67, 76), NEOP), (range(77, 89), NEOP), (range(89, 97), APP), ([14, 15, 16, 33, 34, 37, 38], EARTH), ([131, 132, 133], NUKE),
         ([149, 150, 151], SKY), (range(152, 160), EARTH), (range(122, 125), HP)]
used = {}
for rng, pool in POOLS:
    for n in rng:
        v = ov.get(str(n))
        if not v or "scene" not in v or n not in DUR:
            continue
        i = used.get(id(pool), 0)
        used[id(pool)] = i + 1
        f, cr, *kw = pool[i % len(pool)]
        kw = kw[0] if kw else {}
        cuts = v["scene"].setdefault("mix", [])
        du = DUR[n]
        if not cuts:
            v["scene"]["mix"] = [U(f, cr, k=i, **({"tin": kw["tin"], "tout": kw["tin"] + du} if "tin" in kw else {}), **({"crop": kw["crop"]} if "crop" in kw else {}))]
        else:
            first, last = min(c["a"] for c in cuts), max(min(c["b"] or du, du) for c in cuts)
            if first >= 2.2:
                cuts.insert(0, U(f, cr, k=i, b=first - 0.0))
            elif du - last >= 2.2:
                cuts.append(U(f, cr, k=i, a=last, **({"tin": kw["tin"], "tout": kw["tin"] + du - last} if "tin" in kw else {})))
# slow camera push on long drawn-only shots
for k, v in ov.items():
    if k.isdigit() and "scene" in v and "mix" not in v["scene"] and DUR.get(int(k), 0) >= 8.0:
        v["scene"]["punch"] = 0.05
(d / "footage_overrides.json").write_text(json.dumps(ov, ensure_ascii=False, indent=1), encoding="utf-8")
# real/mix/anim split by screen time
real = mixs = anim = 0.0
for k, v in ov.items():
    if not k.isdigit():
        continue
    n, du = int(k), DUR.get(int(k), 0)
    if "scene" not in v:
        real += du
        continue
    cuts = v["scene"].get("mix", [])
    r = sum(min(c["b"] or du, du) - c["a"] for c in cuts if c["mode"] == "real")
    u = sum(min(c["b"] or du, du) - c["a"] for c in cuts if c["mode"] == "under")
    real += r
    mixs += u
    anim += du - r - u
tot = real + mixs + anim
print(f"real {real:.0f}s {100*real/tot:.0f}%  under-mix {mixs:.0f}s {100*mixs/tot:.0f}%  anim {anim:.0f}s {100*anim/tot:.0f}%  total {tot:.0f}s")
