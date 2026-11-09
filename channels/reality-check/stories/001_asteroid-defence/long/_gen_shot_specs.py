"""Generates long/shot_specs.json for tools/rc_build_long.py from the 160 CUT cues in script/script.md (shot_plan.md).
Run:  python _gen_shot_specs.py      (hand-translated: every Devanagari on-screen cue is written here in Roman / Hinglish, plain digits.)
Coordinates are absolute px on the 1920x1080 frame. Text items 'K:text|colour|at=..|xy=x,y|px=..|r=L|out=..':
 B big number, M medium, s small dim, C chip, K card, R red tag, D date chip (top-right), H title label (top-left), S source label (bottom-left), X credit.
"""
import json
from pathlib import Path

SPECS = []


def E(k, x=0, y=0, s=0, **o):
    return [k, x, y, s, o]


def S(n, lay="c", T=None, g=None, **kw):
    SPECS.append(dict(n=n, lay=lay, T=T or [], g=g or [], **kw))


NASA_C = "NASA / JHUAPL"
HUB_C = "NASA, ESA, STScI, J.-Y. Li (PSI)"
AMB = {"c": "amber", "a": 0.07}
RED = {"c": "red", "a": 0.10}
TEAL = {"c": "teal", "a": 0.10}
STATUS = "K:Koi jaana-pehchana bada khatra\\nabhi nahi hai|teal"


def ladder(k, hi=None, extra=None):
    rad = [18, 30, 48, 84, 150]
    xs = [260, 590, 920, 1250, 1640]
    lab = ["20 m", "50-60 m", "140 m+", "1 km+", "~10 km"]
    g = []
    for i in range(k):
        cur = i == k - 1
        g.append(E("rock", xs[i], 520, rad[i], at=0.2 if cur else -5, c=(110, 116, 130), glow=(255, 176, 32) if (cur or i == hi) else None,
                   labs=[(lab[i], 0, rad[i] + 60, "amber" if (cur or i == hi) else "dim", 46, 0.4 if cur else -5)]))
    return g


def panels4(active, filled, only_active=False):
    g = []
    names = ["Kinetic push", "Gravity tractor", "Laser (idea only)", "Nuclear standoff"]
    for i in range(4):
        px, py = 315 + i * 430, 400
        act = i == active
        g.append(E("panel", px, py, 380, h=400, lc="amber" if act else "dim", at=0.2 if (act or active < 0) else -5,
                   labs=[(names[i], 0, 255, "amber" if act else "dim", 36, 0.2 if act or active < 0 else -5)] if (i in filled or act) else []))
        if i in filled:
            at = 0.5 if act else -5
            if i == 0:
                g += [E("rock", px + 60, py + 20, 52, at=at), E("craft", px - 100, py + 20, 22, at=at), E("path", pts=[(px - 70, py + 20), (px - 10, py + 20)], at=at, len=1.0, arrow=True, c="amber", th=3)]
            if i == 1:
                g += [E("rock", px + 40, py + 70, 52, at=at), E("craft", px - 60, py - 70, 22, at=at), E("path", pts=[(px - 45, py - 40), (px - 20, py + 10)], at=at, len=1.0, arrow=True, c="amber", th=2)]
            if i == 2:
                g += [E("rock", px + 60, py + 70, 46, at=at), E("laser", px, py + 10, 80, at=at)]
            if i == 3:
                g += [E("rock", px + 60, py + 40, 52, at=at), E("flash", px - 60, py - 30, 70, at=at, every=2.4)]
    return g


def verdict(k, texts, cols):
    g, T = [], []
    claims = ["Chaal badalna", "Har asteroid rokna", "Aaj bada khatra", "Filmi last-minute hal"]
    for i in range(4):
        px = 285 + i * 450
        g.append(E("panel", px, 540, 400, h=520, lc=cols[i], at=0.2 if i == k - 1 or k == 0 else -5))
        if i < k:
            now = i == k - 1
            T.append("s:%s|xy=%d,330|px=34|at=%s" % (claims[i], px, "0.4" if now else "-5"))
            T.append("K:%s|%s|xy=%d,560|px=54|at=%s" % (texts[i], cols[i], px, "0.8" if now else "-5"))
    return g, T


# ---------------------------------------------------------------- 1-14 hook, roadmap
S(1, "c", ["B:7 -> 33|amber|at=0.05|out=1.4", "D:26 Sep 2022 (UTC)"], [], media=dict(cue="DART final-approach still", credit="NASA/JHUAPL", file="svs_dart_impact_replay_still.png"), tint=AMB)
S(2, "c", ["S:[5] NASA / JHUAPL: DART impact replay"], [], media=dict(cue="DART impact replay", credit="NASA/JHUAPL", file="svs_dart_impact_replay_1080p.mp4"))
S(3, "c", ["B:22,000 km/h|amber", "C:impact speed (approx.)"], [E("streaks")], tint=AMB)
S(4, "r", ["M:Dimorphos ka ek chakkar|ink", "B:11 h 55 min|amber", "C:before the hit"],
  [E("orbit", 540, 540, 300, P=4.0), E("bar", 1400, 880, 640, v=0.21, c="amber", at=3.0, lab="Predicted change: ~7 min", h=36)])
S(5, "r", ["s:the real result|dim", "B:33 MIN|amber"],
  [E("orbit", 540, 540, 300, P=4.0, P2=3.55, hit=0.45),
   E("bar", 1400, 790, 640, v=0.21, c="amber", at=0.2, lab="7 min (predicted)", h=34),
   E("bar", 1400, 900, 640, v=1.0, c="orange", at=1.6, len=0.5, lab="33 min (measured)", h=34)], tint=AMB)
S(6, "r", ["B:26 MIN ?|orange", "s:7 + ? = 33", "R:Baaki 26 min kahan se aaye?|at=1.8"],
  [E("orbit", 540, 540, 300, P=4.0, P2=3.55, hit=0.4, q=True)], tint=RED)
S(7, "b", ["B:73 s|amber", "s:NASA ka minimum target|dim"],
  [E("bar", 960, 250, 1400, v=1.0, c="orange", at=0.3, lab="33 min", h=48), E("bar", 960, 380, 1400, v=0.037, c="amber", at=1.4, len=0.8, lab="73 s", h=48)])
S(8, "c", ["B:73 s|amber|xy=430,480|px=118|at=0.4", "s:minimum target|xy=430,590|px=36|at=0.9",
           "B:7 min|amber|xy=960,480|px=118|at=1.8", "s:predicted|xy=960,590|px=36|at=2.3",
           "B:33 min|orange|xy=1490,480|px=118|at=3.2", "s:measured|xy=1490,590|px=36|at=3.7"], [E("streaks")])
S(9, "c", ["B:7|dim|xy=600,470|px=190|at=-5", "B:33|dim|xy=1320,470|px=190|at=-5", "B:?|red|xy=960,470|px=220|at=0.5", "s:Beech mein kya hai?|xy=960,700|px=48|at=1.4"],
  [E("ring", 960, 470, 150, c="red", dash=True, at=0.5)], tint=RED)
S(10, "c", ["M:Pehle apna andaza likhiye|ink", "s:Comment mein likh dijiye|dim"], [E("bubble", 960, 270, 110, c="amber")])
S(11, "c", ["K:1  KHATRA|amber|xy=620,500|at=0.4", "K:2  DHUNDHNA|teal|xy=1300,500|at=1.6"],
  [E("path", pts=[(870, 500), (1010, 500)], at=1.2, len=0.6, arrow=True, c="dim", th=3)])
S(12, "c", ["K:3  RAAZ|orange|xy=960,520|at=0.5"], [E("clock", 960, 290, 80, at=0.4)])
S(13, "c", ["R:ANJAAN|red|px=150|at=0.5", "s:= unknown|dim|at=1.5"], [], tint=RED)
S(14, "c", ["H:CH1  KHATRA", "M:Chapter 1|dim"], [E("dot", 300, 300, 5, c="dim"), E("rock", 1500, 300, 14, c=(110, 116, 130)), E("rock", 700, 800, 10, c=(110, 116, 130)), E("rock", 1300, 760, 18, c=(110, 116, 130)), E("streaks")])

# ---------------------------------------------------------------- 15-38 chapter 1
S(15, "l", ["M:Har saal ek chhota dhamaka|ink", "C:airburst, roughly yearly|dim", "S:[1] Brown et al., Nature 2002"], [E("globe", 1360, 540, 280, every=1.3)])
S(16, "c", ["B:5 kt = 5,000 t TNT|amber", "C:kt = kilotonne of TNT"], [E("flash", 960, 330, 160, every=2.5)], tint=AMB)
S(17, "b", ["D:15 Feb 2013", "M:Sardi ki subah|ink"], [E("city", 960, 470, 1500)])
S(18, "l", ["B:~20 m|amber", "C:size of the rock"],
  [E("fire", 1000, 180, 40, dx=500, dy=260, at=0.3, len=2.5), E("bar", 1360, 700, 420, v=1.0, c="amber", at=0.5, lab="rock ~20 m", h=30), E("bar", 1360, 800, 250, v=1.0, c="dim", at=1.4, lab="bus ~12 m", h=30)])
S(19, "b", ["B:~500 kt|amber", "C:energy released in the air"], [E("fire", 400, 130, 36, dx=900, dy=300, at=0.2, len=2.6, flash=True)])
S(20, "c", ["B:~1,600|amber", "C:people injured", "s:no deaths|dim", "S:[2] Popova et al., Science 2013"], [], tint=AMB)
S(21, "b", ["M:Roshni pehle, shock wave baad mein|ink"],
  [E("crack", 640, 330, 190), E("tl", 1360, 330, 700, marks=[0.1, 0.55, 0.9], labs=[("flash", -280, 56, "amber", 34, 0.9), ("minutes", 35, 56, "ink", 34, 1.5), ("shock wave", 280, 56, "red", 34, 2.1)])])
S(22, "b", ["R:ANDEKHA|red|at=1.4", "s:telescope ne kuch nahi dekha|dim|at=1.9"],
  [E("sun", 220, 360, 34, labs=[("Sun", 0, 70, "dim", 32, 1.2)], at=1.0), E("earth", 1560, 360, 62, at=1.0, labs=[("Earth", 0, 90, "dim", 32, 1.2)]),
   E("path", pts=[(280, 360), (1480, 360)], at=1.2, len=2.5, dot=True, c="ink", th=2)], black=1.0, tint=RED)
S(23, "b", ["M:Suraj ki taraf se aaya|ink"],
  [E("sun", 220, 360, 60, g=1.8), E("earth", 1560, 360, 62, labs=[("Earth", 0, 90, "dim", 32, 0.5)]), E("path", pts=[(300, 360), (1480, 360)], at=0.4, len=2.0, dot=True, c="ink", th=2),
   E("txt", 0, 0, 0, labs=[("Suraj ki taraf se", 480, 240, "amber", 38, 0.8)])])
S(24, "b", ["D:30 Jun 1908", "M:Taiga, upar se dekha|dim", "S:[3] Chyba et al., Nature 1993"], [E("field", 960, 400, 1500, c="forest")])
S(25, "l", ["B:~50-60 m|amber", "C:rock size"],
  [E("path", pts=[(1300, 240), (1300, 800)], at=0.3, len=1.0, c="dim", th=2), E("path", pts=[(1080, 800), (1520, 800)], at=0.3, len=0.8, c="dim", th=3),
   E("path", pts=[(1300, 240), (1300, 520)], at=1.0, len=1.6, dot=True, c="amber", dc="white"), E("flash", 1300, 520, 120, at=2.4, every=2.2),
   E("txt", 0, 0, 0, labs=[("5-10 km", 1440, 660, "amber", 40, 2.0), ("ground", 1300, 850, "dim", 30, 0.6)])])
S(26, "l", ["B:~80 million|amber", "s:trees flattened", "B:~2,000 km2|orange|at=2.6"], [E("trees", 1360, 540, 330)])
S(27, "b", ["R:ANJAAN|red|at=1.2", "s:Energy ka range kaafi chauda hai|dim"], [E("bar", 960, 330, 1400, v=0.0, band=(0.06, 0.9), bc="red", at=0.3, lab="Energy: 3-50 Mt (wide range)", h=52)], tint=RED)
S(28, "c", [], ladder(1))
S(29, "c", [], ladder(2))
S(30, "c", [], ladder(3, hi=2))
S(31, "c", [], ladder(4))
S(32, "c", ["D:~66 million years ago", "S:[4] Schulte et al., Science 2010"], ladder(5))
S(33, "b", ["K:Zyaadatar vaigyanik|teal"], [E("bar", 960, 330, 1400, v=0.85, c="teal", at=0.4, lab="Most scientists: asteroid impact", h=52)], tint=TEAL)
S(34, "b", ["K:Kuch shodhkarta: volcano bhi|grey"], [E("bar", 960, 280, 1400, v=0.85, c="teal", at=-5, lab="Most scientists: asteroid impact", h=40), E("bar", 960, 410, 1400, v=0.15, c="grey", at=0.4, lab="Some researchers: volcanoes", h=40)])
S(35, "b", ["M:Bada rock, kam baar|ink"], [E("chart", 960, 340, 1000, h=360, pts=[(0, .92), (.3, .6), (.6, .25), (1, .05)], c="amber", at=0.2, len=2.2,
                                          labs=[("Size ->", 440, 205, "dim", 32), ("How often", -560, -190, "dim", 32)])])
S(36, "b", ["R:ANJAAN|red|at=1.2", "s:Chauda band = kam bharosa|dim"], [E("chart", 960, 340, 1000, h=360, pts=[(0, .92), (.3, .6), (.6, .25), (1, .05)], c="amber", at=-5, len=0.1,
                                                                               band=[(0, .8, 1.0), (.3, .42, .8), (.6, .1, .45), (1, 0, .22)], bc="red")], tint=RED)
S(37, "c", [STATUS + "|at=0.4", "s:aaj ki sthiti|dim"], [], tint=TEAL)
S(38, "c", [STATUS + "|at=-5", "R:Andekha hissa: ANJAAN|at=0.8"], [], tint=RED)

# ---------------------------------------------------------------- 39-62 chapter 2 DART
S(39, "c", ["H:CH2  DART", "M:Ek chhota experiment|ink"], [E("craft", 960, 700, 80, fly=2.5, kind="dart")])
S(40, "l", ["B:DART|amber", "s:Double Asteroid Redirection Test", "S:[5] NASA DART mission page"], [E("craft", 1360, 540, 90, kind="dart")])
S(41, "l", ["B:~780 m|amber", "C:Didymos", "C:not to scale|dim"], [E("rock", 1360, 520, 200, shape="top", labs=[("Didymos", 0, 250, "ink", 40)])])
S(42, "l", ["B:~150-160 m|amber", "C:Dimorphos (the moon)"], [E("orbit", 1360, 540, 270, P=6.0)])
S(43, "r", ["M:Dimorphos ka ek chakkar|ink", "B:11 h 55 min|amber"], [E("orbit", 540, 540, 300, P=4.0)])
S(44, "b", ["K:Koi khatra nahi|green"],
  [E("earth", 260, 360, 60, labs=[("Earth", 0, 90, "dim", 32)]), E("orbit", 1560, 360, 100, P=3.0), E("path", pts=[(340, 360), (1420, 360)], at=0.5, len=1.5, dash=True, c="dim"),
   E("txt", 0, 0, 0, labs=[("bahut door", 880, 320, "dim", 34, 1.2)])], tint=TEAL)
S(45, "c", ["K:Myth: dharti se door bheja gaya|red|at=0.4", "K:Sach: ek test, be-khatar nishane par|green|at=1.8"],
  [E("cross", 360, 480, 34, at=1.0, c="red"), E("tick", 360, 603, 34, at=2.3)])
S(46, "c", ["D:23 Nov 2021", "M:Launch|ink", "C:countdown shuru|amber"], [E("clock", 420, 540, 100), E("path", pts=[(1500, 900), (1500, 220)], at=0.5, len=3.0, arrow=True, c="ink", dot=True, th=3)])
S(47, "b", ["B:10 months|amber", "s:DRACO camera ke aakhri frames|dim"], [], media=dict(cue="DRACO camera final frames, zoom-in", credit=NASA_C))
S(48, "c", ["B:22,000 km/h|amber|at=0.6"], [E("flash", 960, 540, 420, at=2.2, every=4.0, c=(255, 240, 210)), E("streaks")], tint=AMB)
S(49, "l", ["M:Akela dhakka|ink", "C:BEFORE: ball sticks"], [E("collide", 1340, 540, 320, hit=0.4)])
S(50, "r", ["B:~7 min|amber", "C:predicted change"], [E("orbit", 540, 540, 300, P=4.0), E("ring", 540, 540, 330, c="amber", at=0.8, th=3)])
S(51, "b", ["B:73 s|amber", "S:[5] NASA release, 11 Oct 2022"], [E("bar", 960, 330, 1300, v=0.037, c="amber", at=0.4, len=0.8, lab="73 s (NASA minimum target)", h=44)])
S(52, "c", [], [E("bar", 960, 540, 1300, v=0.037, c="amber", at=0.2, len=0.6, lab="73 s", h=48)])
S(53, "r", ["D:11 Oct 2022", "B:11 h 55 -> 11 h 23|amber|px=84", "C:bar grows: 32 min"],
  [E("orbit", 540, 540, 300, P=4.0, P2=3.55, hit=0.4), E("bar", 1400, 900, 640, v=0.97, c="orange", at=1.2, len=1.6, lab="Change: 32 min", h=34)])
S(54, "c", [], [E("orbit", 520, 540, 250, P=4.0, labs=[("BEFORE  11 h 55", 0, 310, "ink", 46)]), E("orbit", 1400, 540, 210, P=3.55, labs=[("AFTER  11 h 23", 0, 270, "amber", 46, 0.9)], at=0.6)])
S(55, "b", ["B:x25+|amber", "C:goal se kai guna zyada"], [E("bar", 960, 250, 1400, v=0.037, c="amber", at=0.3, lab="73 s (goal)", h=44), E("bar", 960, 380, 1400, v=1.0, c="orange", at=1.2, lab="32 min (result)", h=44)])
S(56, "c", ["B:33 +/- 1 MIN|amber", "S:[6] Thomas et al., Nature 2023"], [E("ring", 960, 540, 480, c="dim", dash=True), E("streaks")], tint=AMB)
S(57, "c", ["s:LIGHTCURVE|xy=500,330|px=40|at=0.3", "B:-33.0 min|amber|xy=500,540|px=88|at=0.9", "s:RADAR|xy=1420,330|px=40|at=1.8", "B:-33.0 min|amber|xy=1420,540|px=88|at=2.4"],
  [E("panel", 500, 540, 780, h=420, at=0.2), E("panel", 1420, 540, 780, h=420, at=1.6)])
S(58, "c", ["K:2 tareeke, 1 jawab|green|at=0.4"], [E("tick", 520, 540, 40, at=0.9)], tint=TEAL)
S(59, "r", ["M:Dimorphos ab bhi chakkar laga raha|ink", "B:Toota nahi|green"], [E("orbit", 540, 540, 300, P=3.55, hit=None)])
S(60, "c", ["B:PEHLI BAAR|amber|px=170"], [E("flash", 960, 540, 380, every=3.0), E("streaks")], tint=AMB)
S(61, "c", ["B:?|red|xy=1500,300|px=240|at=0.8", "s:Hubble: malbe ka cone|xy=960,960|px=34|at=0.5"], [], media=dict(cue="Hubble: debris cone still", credit=HUB_C))
S(62, "b", ["M:Agla: dhundhna|ink"],
  [E("blinkframe", 600, 330, 560, h=340, seed=3, dot=(-0.08, 0.05)), E("blinkframe", 1320, 330, 560, h=340, seed=3, dot=(0.02, 0.0), circle=True, at=0.8)])

# ---------------------------------------------------------------- 63-96 chapter 3
S(63, "b", ["H:CH3  DHUNDHNA", "M:Raat ka aasman|dim"], [E("dome", 960, 450, 260)])
S(64, "c", ["D:2016", "B:PDCO|amber", "s:Planetary Defense Coordination Office|dim", "S:[7] NASA Planetary Defense"], [], tint=AMB)
S(65, "b", ["M:Survey telescope aasman chhante hain|ink"],
  [E("scope", 480, 340, 110, at=0.4, labs=[("Catalina", 0, 190, "amber", 40, 0.6)]), E("scope", 960, 340, 110, at=1.8, labs=[("Pan-STARRS", 0, 190, "amber", 40, 2.0)]),
   E("scope", 1440, 340, 110, at=3.2, labs=[("ATLAS", 0, 190, "amber", 40, 3.4)]), E("dots", 960, 600, 1300, cols=44, rows=4, all=True, c="dark", at=0)])
S(66, "b", ["M:Do tasveeren, ek bindu chalta hua|ink"],
  [E("blinkframe", 600, 330, 560, h=340, seed=7, dot=(-0.1, 0.06), circle=True), E("blinkframe", 1320, 330, 560, h=340, seed=7, dot=(0.0, 0.0), circle=True, at=0.5)])
S(67, "b", ["B:~95%|amber", "C:1 km+ asteroids: dhundhe ja chuke", "S:[8] NASA Planetary Defense Strategy 2023"], [E("bar", 960, 330, 1300, v=0.95, c="amber", at=0.3, len=2.0, lab="1 km+ asteroids", h=50)])
S(68, "b", ["D:2010", "M:90% ka lakshya poora|ink"], [E("bar", 960, 330, 1300, v=0.95, c="amber", at=-5, lab="1 km+ asteroids", h=50, mark=0.9), E("tick", 1720, 330, 34, at=0.8)])
S(69, "b", ["B:~25,000|amber", "C:140 m+ asteroids (estimate)"], [E("dots", 960, 330, 1300, cols=50, rows=8, lit=0.0, at=0.3)])
S(70, "b", ["D:2022-23 sources", "B:~40-44%|amber", "C:ab tak dhundhe gaye"], [E("dots", 960, 330, 1300, cols=50, rows=8, lit=0.42, at=0.4, len=2.5)])
S(71, "b", ["R:ANJAAN|red|at=0.8", "s:Taaza sankhya: description mein dekhiye|dim"], [E("dots", 960, 330, 1300, cols=50, rows=8, lit=0.42, at=-5, pulse=True)], tint=RED)
S(72, "c", ["D:2005", "K:Goal: 140 m+ ka 90%|amber"], [], tint=AMB)
S(73, "b", ["M:Goal poora nahi hua|ink"], [E("bar", 960, 280, 1300, v=0.9, c="amber", at=0.3, lab="Goal: 90% by 2020", h=44), E("bar", 960, 410, 1300, v=0.43, c="orange", at=1.3, lab="Actual: ~43%", h=44), E("cross", 1730, 280, 28, at=2.2)])
S(74, "b", ["B:~59%|amber", "C:by 2040, existing surveys", "S:[8] NASA Planetary Defense Strategy 2023"], [E("bar", 960, 330, 1300, v=0.59, c="orange", at=0.3, len=2.0, lab="Projection: ~59% by 2040", h=50)])
S(75, "c", ["K:Koi jaana-pehchana bada khatra\\nabhi nahi hai|teal|at=0.3", "s:Sawaal anadekhe hisse ka hai|dim|at=1.2"], [], tint=TEAL)
S(76, "l", ["M:Kaale pind dikhte nahi|ink", "S:[9] NASA NEO Surveyor"], [E("rock", 540, 540, 170, fade=(1.0, 4.0)), E("craft", 1360, 540, 100, kind="surveyor", fly=2.0)])
S(77, "l", ["M:Garmi (infrared) se dikhte hain|orange"], [E("rock", 540, 540, 170, c=(230, 120, 40), glow=(255, 130, 40)), E("craft", 1360, 540, 100, kind="surveyor"),
                                                      E("txt", 0, 0, 0, labs=[("garmi se", 540, 780, "orange", 40, 0.8)])], tint={"c": "orange", "a": 0.10})
S(78, "c", ["D:NET Sep 2027", "B:Sep 2027|amber", "C:NET = no earlier than", "S:NASA page, 3 Nov 2026"], [], tint=AMB)
S(79, "c", ["B:2026 -> 2027|amber", "R:Taareekh: ANJAAN|at=1.4"], [E("streaks")], tint=RED)
S(80, "c", ["B:90% in ~10 years|amber", "C:140 m+ ka goal"], [E("ring", 960, 540, 470, c="dim", dash=True)], tint=AMB)
S(81, "c", ["H:2024 YR4", "M:Ek naya asteroid|ink", "S:[10] NASA Science blog"], [E("rock", 1500, 400, 40), E("streaks")])
S(82, "b", ["B:~3%|orange", "C:impact chance"], [E("chart", 960, 340, 900, h=340, pts=[(0, .08), (.5, .45), (1, .9)], c="orange", at=0.3, len=2.5, labs=[("time ->", 380, 200, "dim", 30), ("chance", -520, -180, "dim", 30)])], tint=AMB)
S(83, "c", ["C:Ab tak ki sabse oonchi|amber|px=56", "C:30 m+ asteroid ke liye|dim|px=44"], [], tint=AMB)
S(84, "b", ["D:24 Feb 2025", "B:0.004%|green"], [E("chart", 960, 340, 900, h=340, pts=[(0, .9), (.35, .85), (.7, .25), (1, .02)], c="green", at=0.3, len=2.5, labs=[("time ->", 380, 200, "dim", 30), ("chance", -520, -180, "dim", 30)])], tint=TEAL)
S(85, "b", ["M:Chaand par impact chance|ink", "B:1.7 -> 3.8 -> 4.3 (%)|amber|px=96"], [E("chart", 960, 340, 900, h=300, pts=[(0, .4), (.5, .8), (1, .95)], c="orange", at=0.3, len=2.5, labs=[("1.7%", -450, 130, "ink", 30, 0.8), ("3.8%", 0, -190, "ink", 30, 1.6), ("4.3%", 450, -190, "ink", 30, 2.4)])])
S(86, "b", ["D:5 Mar 2026", "K:KHARIJ  (ruled out)|green"], [E("chart", 960, 340, 900, h=300, pts=[(0, .9), (.5, .55), (1, 0.0)], c="green", at=0.3, len=2.5)], tint=TEAL)
S(87, "c", ["M:Data aaya|ink|xy=620,540|px=76|at=0.4", "M:Sambhavna badli|amber|xy=1310,540|px=76|at=1.6"], [E("path", pts=[(870, 540), (1000, 540)], at=1.0, len=0.6, arrow=True, c="amber", th=4)])
S(88, "c", ["s:FILMI|xy=480,330|px=40|at=0.3", "M:Ek din pakka ailaan|ink|xy=480,540|px=52|at=0.5", "s:ASLI|xy=1440,330|px=40|at=1.6", "M:Badalti sankhya|amber|xy=1440,540|px=60|at=1.8"],
  [E("panel", 480, 540, 800, h=440, at=0.2), E("panel", 1440, 540, 800, h=440, at=1.5, lc="amber")])
S(89, "b", ["H:APOPHIS", "M:Ek aur naam|dim"], [E("rock", 960, 380, 150, shape="top")])
S(90, "b", ["B:~340-375 m|amber"], [E("bar", 960, 250, 1300, v=0.85, c="amber", at=0.3, lab="~340 m (NASA)", h=44), E("bar", 960, 380, 1300, v=0.94, c="blue", at=1.0, lab="~375 m (ESA)", h=44)])
S(91, "r", ["D:13 Apr 2029", "B:~32,000 km|amber", "C:Earth se closest approach"],
  [E("earth", 540, 540, 85), E("ring", 540, 540, 250, c="dim", dash=True, at=0.5, labs=[("high-orbit ring", 0, 285, "dim", 30, 0.8)]),
   E("path", pts=[(1000, 180), (820, 380), (700, 470), (690, 580), (760, 760)], at=0.6, len=3.0, dot=True, c="amber", th=3)])
S(92, "c", ["K:NASA: kam se kam 100 saal\\nkoi jokhim nahi|teal", "S:[11] NASA / ESA Apophis pages"], [], tint=TEAL)
S(93, "b", ["D:2004", "B:2.7% -> 0|amber"], [E("chart", 960, 340, 900, h=320, pts=[(0, .85), (.4, .8), (.75, .5), (1, 0.0)], c="amber", at=0.3, len=2.5)])
S(94, "l", ["M:Poorvi hemisphere se dikhega|ink"], [E("globe", 1360, 580, 250, hemi=True, at=0.2), E("eye", 1360, 250, 70, at=0.8)])
S(95, "b", ["M:Do yaan, Apophis ke paas|ink"], [E("craft", 560, 340, 60, kind="hera", labs=[("Ramses (saath mein)", 0, 120, "ink", 38, 0.6)]), E("craft", 1360, 340, 60, kind="dart", at=1.4, labs=[("OSIRIS-APEX (baad mein)", 0, 120, "ink", 38, 1.6)])])
S(96, "c", ["K:SACH NAHI|red|at=0.3", "K:Status: Apophis se jokhim nahi (NASA)|teal|at=1.6"], [E("cross", 340, 470, 30, at=0.8)])

# ---------------------------------------------------------------- 97-123 chapter 4 (the secret)
S(97, "r", ["M:Wapas pehle sawaal par|dim"], [E("orbit", 540, 540, 300, P=4.0, P2=3.55, hit=0.5)])
S(98, "c", ["H:CH4  RAAZ", "B:7 / 33|amber"], [E("ring", 960, 540, 450, c="dim", dash=True)], tint=AMB)
S(99, "l", ["B:beta = 1|amber", "C:ball chipak jaati hai"], [E("collide", 1340, 540, 320, hit=0.4)])
S(100, "l", ["M:Yaan Dimorphos se takraya|ink", "C:chipak gaya"], [E("collide", 1340, 540, 340, hit=0.4, kind="craft")])
S(101, "l", ["M:Dimorphos: pattharon ka dher|ink", "C:rubble pile"], [E("rubble", 1360, 540, 280)])
S(102, "b", ["M:Takkar se patthar aur dhool upar|ink"], [E("fountain", 960, 360, 70)])
S(103, "l", ["M:Malba upar, Dimorphos neeche|ink", "C:action = reaction"],
  [E("rock", 1360, 560, 120), E("path", pts=[(1360, 430), (1360, 170)], at=0.4, len=1.5, arrow=True, c="amber", th=6), E("path", pts=[(1360, 700), (1360, 960)], at=1.4, len=1.5, arrow=True, c="orange", th=6),
   E("txt", 0, 0, 0, labs=[("malba", 1560, 300, "amber", 40, 0.9), ("Dimorphos ka dhakka", 1560, 860, "orange", 38, 1.9)])])
S(104, "b", ["K:Yaan ka dhakka + malbe ka dhakka|orange"],
  [E("path", pts=[(400, 330), (900, 330)], at=0.3, len=1.2, arrow=True, c="amber", th=8), E("path", pts=[(900, 330), (1520, 330)], at=1.6, len=1.4, arrow=True, c="orange", th=8),
   E("txt", 0, 0, 0, labs=[("yaan", 650, 280, "amber", 38, 0.6), ("malba", 1210, 280, "orange", 38, 1.9)])])
S(105, "b", ["B:beta = 1|amber", "S:[12] Cheng et al., Nature 2023"], [E("bar", 960, 330, 1300, v=0.2, c="amber", at=0.3, len=1.2, lab="beta = 1: sirf yaan", h=50)])
S(106, "b", ["B:3.6|orange", "C:agar density barabar ho"], [E("bar", 960, 330, 1300, v=0.72, c="orange", at=0.3, len=1.8, lab="beta = 3.6", h=50, mark=0.2)])
S(107, "b", ["B:2.2 - 4.9|amber", "C:beta ka range"], [E("bar", 960, 330, 1300, v=0.0, band=(0.44, 0.98), bc="amber", at=0.3, lab="beta: 2.2 to 4.9", h=50, mark=0.2)])
S(108, "c", ["s:SIRF YAAN|xy=480,300|px=36", "s:MALBA BHI|xy=1440,300|px=36|at=1.2", "C:x2.2 - x4.9|xy=1440,800|at=2.4"],
  [E("panel", 480, 540, 800, h=520, at=0.2), E("panel", 1440, 540, 800, h=520, at=1.0, lc="amber"),
   E("path", pts=[(280, 540), (700, 540)], at=0.4, len=1.2, arrow=True, c="amber", th=8),
   E("path", pts=[(1160, 450), (1700, 450)], at=1.3, len=1.0, arrow=True, c="orange", th=8), E("path", pts=[(1160, 540), (1740, 540)], at=1.6, len=1.0, arrow=True, c="orange", th=8),
   E("path", pts=[(1160, 630), (1660, 630)], at=1.9, len=1.0, arrow=True, c="orange", th=8)])
S(109, "b", ["B:2.7 mm/s|amber", "C:speed ka badlav"], [E("bar", 960, 250, 1400, v=1.0, c="dim", at=0.3, lab="22,000 km/h", h=44), E("bar", 960, 380, 1400, v=0.004, c="amber", at=1.4, len=0.5, lab="2.7 mm/s", h=44)])
S(110, "r", ["B:-33 min|amber", "s:period chhota hua|dim"], [E("orbit", 540, 540, 300, P=1.6, P2=1.3, hit=0.5)])
S(111, "c", ["D:+2 h", "s:Hubble: malbe ka cone|dim"], [], media=dict(cue="Hubble: debris cone, +2 h", credit=HUB_C))
S(112, "c", ["B:+17 h|amber", "s:phir weeks tak lambi poonchh|dim"], [], media=dict(cue="Hubble: pinwheel +17 h, tail over weeks", credit=HUB_C))
S(113, "c", ["B:>1,000 t|amber", "C:malba (tons)"], [E("fountain", 960, 760, 40, at=0.2)], tint=AMB)
S(114, "b", ["R:ANJAAN: malba kitna?|red|at=1.0", "M:>6,000 t se 11,000-55,000 t tak|ink", "S:[17] Moreno 2023   [18] Ferrari 2025"],
  [E("bar", 960, 300, 1400, v=0.0, band=(0.1, 0.95), bc="red", at=0.3, lab="Ejecta: wide range (tons)", h=50)], tint=RED)
S(115, "b", ["B:?|red", "C:beta ka range chauda"], [E("bar", 960, 330, 1300, v=0.0, band=(0.3, 0.98), bc="red", at=0.3, lab="beta: wide band", h=50, mark=0.2)], tint=RED)
S(116, "l", ["R:Dravyaman (mass): ANJAAN"], [E("rock", 1360, 540, 170, labs=[("?", 0, 0, "red", 130, 0.6)])], tint=RED)
S(117, "l", ["M:Andar kya hai? Pata nahi|ink"], [E("rubble", 1360, 540, 280, labs=[("?", -90, -60, "red", 90, 0.6), ("?", 80, 40, "red", 90, 1.2), ("?", -30, 110, "red", 90, 1.8), ("?", 100, -110, "red", 80, 2.4)])], tint=RED)
S(118, "c", ["K:Naapa hua: 33 min|green|xy=500,540|at=0.4", "K:Hisaab: khula (open)|red|xy=1420,540|at=1.6"], [])
S(119, "c", ["D:Mar 2026", "M:Ek naya adhyayan|ink", "S:[13] Makadia, Eggl et al., Science Advances 2026"], [E("streaks")])
S(120, "b", ["M:Dono Suraj ke chakkar lagate hain|ink"], [E("sun", 960, 380, 26), E("orbit", 960, 380, 250, P=10.0, rock=False)])
S(121, "c", ["B:~0.15 s|amber", "C:Sun-orbit ka badlav", "s:Koi asar nahi|dim"], [E("ring", 960, 540, 440, c="dim", dash=True)], tint=AMB)
S(122, "c", ["H:RECAP", "M:1   7 min ki jagah 33 min|ink", "s:malbe ne bhi dhakka diya|dim"], [E("ring", 960, 560, 380, c="dim", dash=True)])
S(123, "c", ["H:RECAP", "M:2   Dimorphos ka dravyaman|ink", "R:ANJAAN|at=1.0", "M:3   Dhundhna baaki, rokne ke tareeke bhi|ink|at=3.0"], [])

# ---------------------------------------------------------------- 124-140 chapter 5
S(124, "b", ["H:CH5  TAREEKE", "M:Chaar tareeke|dim"], panels4(-1, []))
S(125, "b", ["S:[14] The Planetary Society"], panels4(0, [0]))
S(126, "b", [], panels4(1, [0, 1]))
S(127, "b", ["C:Dashakon pehle chetavni chahiye|amber"], panels4(1, [0, 1]) + [E("tl", 960, 700, 1300, marks=[0.04, 0.96], at=0.6, labs=[("aaj", -620, 50, "ink", 32, 0.9), ("dashak baad", 620, 50, "ink", 32, 1.8)])])
S(128, "b", ["C:Sirf vichaar (idea only)|dim"], panels4(2, [0, 1, 2]))
S(129, "c", ["M:Abhyaas-adhyayan, 2023|ink", "s:kai tareeke alag-alag kaam karte dikhe|dim", "S:[19] Politecnico di Milano / SMPAG 2023"], [E("ring", 960, 540, 450, c="dim", dash=True)])
S(130, "b", ["M:Chaaron ek hi raasta mod dete hain|ink"], panels4(-1, [0, 1, 2, 3]))
S(131, "b", [], panels4(3, [0, 1, 2, 3]))
S(132, "l", ["C:100 m (standoff)", "C:1 Mt (yield)", "C:~2 months pehle", "S:[15] LLNL / Acta Astronautica 2021"],
  [E("rock", 1380, 440, 110), E("flash", 1080, 400, 130, every=2.5), E("path", pts=[(1170, 410), (1260, 430)], at=0.6, len=0.8, dash=True, c="amber", th=3)])
S(133, "b", ["B:99.9%|amber", "C:tukde Dharti se door (simulation)"],
  [E("earth", 1560, 380, 80, labs=[("Earth", 0, 110, "dim", 30)]), E("rock", 260, 380, 60, at=0.2),
   E("path", pts=[(320, 380), (1250, 210), (1750, 100)], at=0.8, len=2.5, c="ink", dot=True, th=2), E("path", pts=[(320, 380), (1250, 280), (1800, 200)], at=0.9, len=2.5, c="ink", th=2),
   E("path", pts=[(320, 380), (1250, 520), (1750, 640)], at=1.0, len=2.5, c="ink", dot=True, th=2)])
S(134, "c", ["B:Sirf computer simulation|ink|px=104", "R:ANJAAN|red|at=1.6"], [E("streaks")], tint=RED)
S(135, "c", ["M:Dhamaka pind ko tukdon mein tod sakta hai|ink|xy=960,860|px=54"], [E("split", 960, 420, 150, at=1.2)])
S(136, "c", ["B:Vigyan + Qanoon|amber"], [E("scale", 960, 290, 90)], tint=AMB)
S(137, "c", ["C:'Ye pakka chalega'|grey|xy=960,430|px=52|at=0.3", "C:'Ye pakka nahi chalega'|grey|xy=960,620|px=52|at=1.5"], [E("cross", 540, 430, 28, at=1.0, c="grey"), E("cross", 480, 620, 28, at=2.2, c="grey")])
S(138, "c", ["s:FILMI|xy=480,300|px=40|at=0.3", "M:Aakhri minute: drill karo, udaa do|dim|xy=480,540|px=44|at=0.5", "s:ASLI|xy=1440,300|px=40|at=1.6", "M:Dashakon pehle ki yojana|amber|xy=1440,540|px=54|at=1.8"],
  [E("panel", 480, 540, 800, h=440, at=0.2), E("panel", 1440, 540, 800, h=440, at=1.5, lc="amber"), E("cross", 480, 440, 36, at=1.0)])
S(139, "b", ["M:Chhota dhakka, bada fark|ink"],
  [E("path", pts=[(300, 360), (1600, 360)], at=0.3, len=3.0, c="dim", th=3), E("path", pts=[(300, 360), (1600, 440)], at=0.5, len=3.0, c="amber", th=3, dot=True),
   E("txt", 0, 0, 0, labs=[("decades ->", 1000, 280, "dim", 34, 1.0)])])
S(140, "c", ["K:Jaane-pehchane bade khatre\\naaj koi nahi|teal|at=0.3"], [], tint=TEAL)

# ---------------------------------------------------------------- 141-160 chapter 6, verdict, end
S(141, "b", ["H:CH6  HERA", "M:ESA ka yaan|ink"], [E("craft", 960, 420, 90, kind="hera", fly=2.5)])
S(142, "c", ["D:7 Oct 2024", "C:Mar 2025: Mars ke paas se|xy=960,160|at=1.2"],
  [E("earth", 300, 560, 46, labs=[("Earth", 0, 70, "dim", 30)]), E("rock", 900, 330, 34, c=(220, 110, 70), labs=[("Mars", 0, 60, "dim", 30)], at=1.0),
   E("rock", 1600, 520, 30, labs=[("Didymos", 0, 60, "dim", 30)], at=2.0),
   E("path", pts=[(340, 540), (620, 400), (870, 330), (1250, 380), (1560, 500)], at=0.4, len=4.0, dot=True, c="amber", th=3, dash=True)])
S(143, "l", ["M:Hera: dravyaman aur banaawat naapega|ink", "C:aur takkar ka gaddha dekhega"],
  [E("rock", 1360, 560, 130, labs=[("?", 0, 0, "red", 110, 0.4)]), E("scale", 1360, 250, 50, at=2.0), E("ring", 1420, 600, 26, c="amber", at=1.0, th=3)])
S(144, "c", ["s:SIMULATION|xy=480,300|px=36", "s:ASAL|xy=1440,300|px=36|at=1.2"],
  [E("panel", 480, 540, 800, h=480, at=0.2), E("panel", 1440, 540, 800, h=480, at=1.0, lc="amber"),
   E("bar", 480, 560, 620, v=0.25, c="dim", at=0.5, lab="chhota badlav", h=44), E("bar", 1440, 560, 620, v=0.75, c="orange", at=1.5, lab="bada badlav", h=44)])
S(145, "b", ["M:Do chhote CubeSat|ink"], [E("shoebox", 620, 340, 80, labs=[("Milani", 0, 100, "ink", 40, 0.6)]), E("shoebox", 1300, 340, 80, at=1.2, labs=[("Juventas", 0, 100, "ink", 40, 1.4)])])
S(146, "b", ["D:27 Oct 2026", "M:Dono pind alag dikhte hain|ink", "S:[16] ESA Hera page"], [E("rock", 820, 380, 56), E("rock", 1110, 380, 30, at=0.8)])
S(147, "b", ["C:Yojana: Nov 2026|amber|px=56", "s:Hera ke pahunchne ki yojana|dim"], [E("clock", 960, 330, 90)])
S(148, "c", ["R:Pahuncha ya nahi: jaanchein|red|at=0.4", "s:ESA Hera page par taaza haal dekhein|dim|at=1.4"], [], tint=RED)
S(149, "c", ["H:ABHI KYA NAHI PATA", "R:1   Dimorphos ka dravyaman\\naur andar ki banaawat|red|at=0.4"], [], tint=RED)
S(150, "b", ["R:2   Kya har asteroid par chalega?|red|at=0.3", "s:Pattharon ka dher vs thos pind|dim"],
  [E("rubble", 700, 360, 130, labs=[("ptthar ka dher", 0, 175, "ink", 34, 0.8)]), E("rock", 1220, 360, 130, labs=[("thos pind", 0, 175, "ink", 34, 1.2)], at=0.8)], tint=RED)
S(151, "b", ["R:3   Jo pind dhunde nahi gaye|red|at=0.3", "s:Unka pata kaise ho|dim"], [E("dots", 960, 330, 1300, cols=50, rows=8, lit=0.4, at=-5, pulse=True)], tint=RED)
S(152, "c", ["H:FAISLA", "S:NASA, ESA, Nature 2023"], verdict(0, [], ["green", "red", "grey", "amber"])[0])
_g, _t = verdict(1, ["SACH", "", "", ""], ["green", "red", "grey", "amber"])
S(153, "c", _t, _g)
_g, _t = verdict(2, ["SACH", "ABHI\\nANJAAN", "", ""], ["green", "red", "grey", "amber"])
S(154, "c", _t, _g)
_g, _t = verdict(3, ["SACH", "ABHI\\nANJAAN", "NAHI\\n(anjaan bhi)", ""], ["green", "red", "grey", "amber"])
S(155, "c", _t, _g)
_g, _t = verdict(4, ["SACH", "ABHI\\nANJAAN", "NAHI\\n(anjaan bhi)", "AADHA\\nSACH"], ["green", "red", "grey", "amber"])
S(156, "c", _t, _g)
S(157, "c", ["H:RECAP", "M:7 -> 33: malbe ka dhakka|ink|px=80"], [E("ring", 960, 560, 420, c="dim", dash=True)])
S(158, "l", ["H:RECAP", "M:2  Dhundhna sabse bada kaam|ink|px=52", "M:3  Har tareeke ki seema|ink|px=52|at=2.5"], [], tint={"c": "blue", "a": 0.06})
S(159, "l", ["M:Sawaal: seemit paise hon,\\nto pehle kis par?|ink|px=54"], [], tint={"c": "blue", "a": 0.05})
S(160, "l", ["C:DHUNDHNA  (telescope)|amber|px=44", "C:ROKNA  (yaan)|teal|px=44|at=1.2"], [], tint={"c": "blue", "a": 0.05})


# ---------------------------------------------------------------- real NASA footage backing (LICENSE_LOG.md credits), own graphics stay on top
def real(n, media, drop=(), **kw):
    sp = next(s for s in SPECS if s["n"] == n)
    sp["media"] = media
    sp["g"] = [e for e in sp["g"] if e[0] not in drop]
    sp.update(kw)


real(40, dict(file="pia25329_dart_at_didymos_illustration.jpg", credit="NASA/JHUAPL/S. Gribben (illustration)", dim=0.5, zoom=0.08), drop=("craft",))
real(41, dict(file="nasa_didymos_ridge_formation.mp4", credit="NASA (Didymos ridge simulation)", mode="contain", h=780, cx=1360, cy=500, rate=1.0, zoom=0.0), drop=("rock",))
real(47, dict(files=["draco_last_image_both_asteroids.png", "draco_penultimate_image.png", "draco_last_image_all_dimorphos.png", "draco_final_image.png"],
              credit="NASA/JHUAPL (DRACO)", mode="contain", h=620, cx=960, cy=350, dim=0.95))
real(64, dict(file="pia24565_didymos_orbit.jpg", credit="NASA/JPL-Caltech (known asteroid orbits)", dim=0.45))
real(67, dict(file="nasa_planetary_defense_infographic_2023.jpg", credit="NASA (July 2023 infographic)", mode="contain", h=980, cx=1600, cy=540, zoom=0.0), lay="l",
     g=[E("bar", 520, 880, 760, v=0.95, c="amber", at=0.3, len=2.0, lab="1 km+ asteroids", h=44)])
real(76, dict(file="pia26388_neo_surveyor_concept.jpg", credit="NASA/JPL-Caltech (artist concept)", dim=0.5), drop=("craft", "rock"))
real(77, dict(file="pia26388_neo_surveyor_concept.jpg", credit="NASA/JPL-Caltech (artist concept)", dim=0.5, zoom=0.1), drop=("craft",))
real(89, dict(file="svs_apophis_beauty_1080p.mp4", credit="NASA/Goddard SVS", dim=0.6, rate=0.5), drop=("rock",))
real(92, dict(file="svs_apophis_beauty_1080p.mp4", credit="NASA/Goddard SVS", dim=0.4, rate=0.5, start=4.0))
real(100, dict(file="jhuapl_dart_collision_still.jpg", credit="NASA/JHUAPL (illustration)", dim=0.55, zoom=0.1), drop=("collide",))

SPECS.sort(key=lambda s: s["n"])
assert [s["n"] for s in SPECS] == list(range(1, 161)), [s["n"] for s in SPECS][:5]
out = Path(__file__).with_name("shot_specs.json")
out.write_text(json.dumps(SPECS, ensure_ascii=True, indent=0), encoding="utf-8")
print("wrote", out, len(SPECS), "shots")
