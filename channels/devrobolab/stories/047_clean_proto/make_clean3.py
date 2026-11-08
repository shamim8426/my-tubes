r"""Clean-style Short v3 (user 2026-11-08: more VARIETY, bigger text that never overlaps, a new picture every few seconds).
Layout: picture zone on TOP (y 170-1010), caption zone at the BOTTOM (y 1090-1520), one short phrase at a time.
Each BEAT = one phrase + one picture; the picture flies in from left / right / bottom / zooms in or out, holds with a slow push, then leaves.
Run (ffmpeg on PATH):  python make_clean3.py [frames t1 t2 ...]"""
import sys, math
from PIL import Image
import make_clean as mc
from make_clean import *
from make_clean2 import ORANGE, burst, chip, big_label

PIC_Y = 600     # centre of the picture zone
CAP_TOP = 1100
FS = 92         # caption font size


# ---------- bigger phrase caption (no overlap: only the current phrase is on screen) ----------
def wspr(txt, bold, dark):
    col = "#111" if dark else "#c4c4c4"
    return sprite(f'<div style="font:{800 if bold else 600} {FS}px MK;color:{col};white-space:nowrap;padding:70px 0">{txt}</div>')

def phrase(base, t, sid, words, k0, k1, t_end, top=CAP_TOP, maxw=960):
    ts = T(sid, k0)
    if t < ts - 0.05: return
    out = 1 - fade(t, t_end - 0.18, 0.18)
    items = []; lines = [[]]; widths = [0]; gap = 22
    for k in range(k0, k1 + 1):
        w, b = words[k]; sp = wspr(w, b, True); wd = sp.width - 140
        if widths[-1] + wd > maxw and lines[-1]: lines.append([]); widths.append(0)
        lines[-1].append((k, sp, wd)); widths[-1] += wd + gap
    y = top; lh = FS + 26
    for ln, wd in zip(lines, widths):
        x = W / 2 - (wd - gap) / 2
        for k, sp, w_ in ln:
            t0 = T(sid, k)
            if t >= t0 - 0.02:
                dark = ease_out((t - t0) / 0.25); a_in = fade(t, t0, 0.12)
                g = wspr(words[k][0], words[k][1], False)
                yy = y + (1 - a_in) * 14 - (1 - out) * 20
                place(base, g, x + w_ / 2, yy, 1.0, a_in * (1 - dark) * out)
                place(base, sp, x + w_ / 2, yy, 1.0, a_in * dark * out)
            x += w_ + gap
        y += lh


# ---------- picture motion ----------
def enter_xy(style, e):
    """returns (dx, dy, scale, alpha, rot) for entry progress e in 0..1 (e may overshoot)"""
    q = 1 - e
    if style == "left":   return (-900 * q, 0, 1.0, min(1, e * 3), -6 * q)
    if style == "right":  return (900 * q, 0, 1.0, min(1, e * 3), 6 * q)
    if style == "bottom": return (0, 700 * q, 1.0, min(1, e * 3), 0)
    if style == "top":    return (0, -700 * q, 1.0, min(1, e * 3), 0)
    if style == "zoomin": return (0, 0, 0.55 + 0.45 * e, min(1, e * 2.5), 0)
    if style == "zoomout": return (0, 0, 1.5 - 0.5 * e, min(1, e * 2.5), 0)
    return (0, 0, 0.8 + 0.2 * e, min(1, e * 3), 0)

def show(base, t, spr, t0, t1, style, cy=PIC_Y, push=0.05):
    """draw one sprite for the beat window [t0, t1): fly in, slow push, leave"""
    if t < t0 or t >= t1 or spr is None: return
    e = ease_back((t - t0) / 0.5) if style in ("zoomin", "pop") else ease_out((t - t0) / 0.5)
    dx, dy, sc, al, rot = enter_xy(style, e)
    sc *= 1.0 * (1 + push * clamp((t - t0) / max(0.5, t1 - t0)))
    lv = clamp((t - (t1 - 0.22)) / 0.22)          # leave
    place(base, spr, 540 + dx, cy + dy - lv * 40, sc * (1 - 0.08 * lv), al * (1 - lv), rot)


# ---------- reusable pictures ----------
def big_card(txt, sub=None, icon=None, w=820, size=150, bg="#fff", col="#111"):
    inner = (f'<div style="display:flex;align-items:center;justify-content:center;gap:26px">{ic(icon, size * 0.9) if icon else ""}'
             f'<div style="font:800 {size}px MK;color:{col};line-height:1.05">{txt}</div></div>')
    if sub: inner += f'<div style="text-align:center;font:700 54px MK;color:#777;margin-top:12px">{sub}</div>'
    return sprite(card(w, inner, pad=44, r=44, bg=bg))

def term_card(body, w=900, size=70):
    dots = '<div style="display:flex;gap:10px;margin-bottom:20px"><i style="width:18px;height:18px;border-radius:50%;background:#ff5f57"></i><i style="width:18px;height:18px;border-radius:50%;background:#febc2e"></i><i style="width:18px;height:18px;border-radius:50%;background:#28c840"></i></div>'
    return sprite(card(w, dots + f'<div style="font:700 {size}px MO;line-height:1.5;color:#e6edf7;min-height:210px">{body}</div>', bg="#0f172a", pad=40, r=40))

PR = '<span style="color:#7cf0a8">&gt;</span> '

def keycap(txt, w=360, hl=False):
    bg = "#FFC800" if hl else "#fff"
    return sprite(f'<div style="width:{w}px;height:210px;border-radius:34px;background:{bg};{SH};border-bottom:14px solid #d0d0d6;display:flex;align-items:center;justify-content:center;font:800 70px MK;color:#111">{txt}</div>')

def small(txt, icon=None, bg="#fff", col="#111", size=64):
    return sprite(f'<div style="display:flex;align-items:center;gap:20px;background:{bg};color:{col};border-radius:28px;padding:22px 40px;font:800 {size}px MK;{SH};white-space:nowrap">{ic(icon, size) if icon else ""}{txt}</div>')

def bar_race(p1, p2):
    """two horizontal bars: normal vs fast (fast finishes first)"""
    def row(lbl, p, col):
        return (f'<div style="font:700 46px MK;color:#555;margin:6px 0 10px">{lbl}</div><div style="width:760px;height:60px;border-radius:30px;background:#e6e6ea;overflow:hidden">'
                f'<div style="width:{int(760 * p)}px;height:60px;border-radius:30px;background:{col}"></div></div>')
    return sprite(card(860, row("Normal", p1, "#9aa0ad") + '<div style="height:26px"></div>' + row("Fast mode", p2, ORANGE), pad=44, r=44))

def toggle(on):
    kn = 'right:14px' if on else 'left:14px'; bg = "#34c759" if on else "#c9c9ce"
    return sprite(card(760, f'<div style="display:flex;align-items:center;justify-content:space-between"><div style="font:800 80px MK;color:#111">/fast</div>'
                       f'<div style="position:relative;width:260px;height:130px;border-radius:65px;background:{bg}"><div style="position:absolute;top:14px;{kn};width:102px;height:102px;border-radius:50%;background:#fff;box-shadow:0 4px 10px rgba(0,0,0,.3)"></div></div></div>'
                       f'<div style="text-align:center;font:800 64px MK;margin-top:20px;color:{"#1e9e4a" if on else "#888"}">{"ON" if on else "OFF"}</div>', pad=50, r=44))

def prompt_bar(show_icon):
    icn = ic("bolt", 72) if show_icon else '<span style="width:72px"></span>'
    return sprite(card(900, f'<div style="display:flex;align-items:center;gap:22px;font:700 54px MO;color:#555">{icn}<span>Ask Claude anything...</span></div>', pad=44, r=60))

def meter(p):
    return sprite(card(860, f'<div style="font:700 50px MK;color:#555;margin-bottom:14px">Usage credits</div><div style="width:760px;height:70px;border-radius:35px;background:#e6e6ea;overflow:hidden"><div style="width:{int(760 * p)}px;height:70px;border-radius:35px;background:linear-gradient(90deg,{ORANGE},#ffb199)"></div></div>'
                      f'<div style="font:800 64px MK;color:#111;margin-top:18px">{int(p * 100)}% left</div>', pad=44, r=44))

def robot_pic(pose, d=520): return sprite(robot_circle(d, pose))


# ---------- chapter frame (persistent chip, small burst shapes behind) ----------
def decor3(base, t, sid):
    k = 0.5 + 0.5 * ease_out((t - SC[sid]) / 0.6)
    place(base, burst(250, rot=t * 6), 70, 120, k, 0.95)
    place(base, burst(190, rot=-t * 5 + 20), 1020, 250, k, 0.95)

def beats_scene(base, t, sid, label, chip_name, chip_icon, words, beats, intro=0.95):
    """beats: list of (k0, k1, picture_fn(tl)->sprite, style). Window of beat i = [start_i, start_{i+1})"""
    t0 = SC[sid]; decor3(base, t, sid)
    starts = [max(T(sid, b[0]) - 0.12, t0 + intro) if i == 0 else T(sid, b[0]) - 0.12 for i, b in enumerate(beats)]
    ends = starts[1:] + [E(sid) - 0.05]
    if label and t < t0 + intro:
        q = pop(t, t0 + 0.02); out = 1 - fade(t, t0 + intro - 0.2, 0.2)
        place(base, big_label(label), 540, 520, 0.8 + 0.2 * q, fade(t, t0, 0.15) * out)
        place(base, chip(chip_name, chip_icon), 540, 700, pop(t, t0 + 0.25), fade(t, t0 + 0.25, 0.15) * out)
    else:
        place(base, chip(chip_name, chip_icon), 540, 150, 1.25, fade(t, t0 + intro, 0.2))
    for i, (k0, k1, fn, style) in enumerate(beats):
        # a beat's own caption runs from its first word to the next beat
        cap_end = ends[i] if i < len(beats) - 1 else E(sid) - 0.05
        phrase(base, t, sid, words, k0, k1, cap_end if t < cap_end else cap_end)
        if starts[i] <= t < ends[i]: show(base, t, fn(t - starts[i]), starts[i], ends[i], style)


# ---------- scenes ----------
def W_(s): return [(w, b) for w, b in s]

def S_hook(base, t):
    sid = "hook"; t0 = SC[sid]; decor3(base, t, sid)
    words = [("Claude", True), ("Code", True), ("ko", False), ("dhai", True), ("guna", True), ("tak", False), ("tez", True), ("karna", False), ("hai?", False), ("bas", False), ("ek", False), ("command,", True), ("slash", True), ("fast.", True)]
    b = [(0, 8, lambda tl: robot_pic("wave", 560), "zoomin"),
         (9, 13, lambda tl: term_card(PR + ("/fast" if tl > 0.9 else "") + ('<span style="opacity:.6">_</span>' if int(tl * 2) % 2 == 0 else "&nbsp;")), "right")]
    beats_scene(base, t, sid, None, "DEVROBOLAB", "star", words, b)
    # robot orbit icons on the first beat
    if t < T(sid, 9) - 0.12:
        for name, ang, k in (("bolt", -145, 3), ("term", -35, 6), ("clock", 90, 9)):
            tt = T(sid, min(k, 13)); r = 400; x = 540 + r * math.cos(math.radians(ang)); y = PIC_Y + r * math.sin(math.radians(ang)) * 0.8
            place(base, sprite(circle(170, ic(name, 100))), x, y, pop(t, tt), min(1, pop(t, tt) * 1.4))

def S_what(base, t):
    sid = "what"
    words = [("Ye", False), ("Fast", True), ("mode", True), ("hai.", False), ("Model", False), ("wahi", True), ("Opus", True), ("rehta", False), ("hai,", False), ("quality", False), ("bhi", False), ("same,", True), ("bas", False), ("jawab", False), ("tez", True), ("aate", False), ("hain.", False)]
    def race(tl): return bar_race(clamp(tl / 3.2) * 0.62, clamp(tl / 1.7))
    def mult(tl): return big_card(f"{min(2.5, round(1 + 1.5 * clamp(tl / 1.3), 1))}x", "tez jawab", "bolt", w=760, size=190)
    b = [(0, 3, lambda tl: big_card("FAST MODE", None, "bolt", size=104), "left"),
         (4, 8, lambda tl: sprite(card(900, f'<div style="display:flex;align-items:center;justify-content:space-between;gap:20px"><div style="font:800 76px MK">Opus</div><div style="font:800 90px MK;color:{ORANGE}">=</div><div style="font:800 76px MK">Opus</div></div><div style="display:flex;justify-content:space-between;font:700 44px MK;color:#777;margin-top:10px"><span>normal</span><span>fast</span></div>', pad=50, r=44)), "right"),
         (9, 11, lambda tl: small("Quality same", "check", size=84), "bottom"),
         (12, 16, race, "zoomout")]
    beats_scene(base, t, sid, "Pehla", "FAST MODE", "bolt", words, b)

def S_how(base, t):
    sid = "how"
    words = [("Terminal", True), ("mein", False), ("slash", True), ("fast", True), ("likho,", False), ("Space", True), ("dabao,", False), ("phir", False), ("Enter.", True), ("screen", False), ("par", False), ("Fast", True), ("mode", True), ("ON", True), ("dikhega,", False), ("aur", False), ("prompt", False), ("ke", False), ("paas", False), ("ek", False), ("chhota", False), ("icon.", True)]
    b = [(0, 4, lambda tl: term_card(PR + ("/fast" if tl > 1.2 else "") + '<span style="opacity:.6">_</span>'), "left"),
         (5, 6, lambda tl: keycap("SPACE", 440, tl > 0.5), "bottom"),
         (7, 8, lambda tl: keycap("ENTER", 440, tl > 0.5), "right"),
         (9, 14, lambda tl: term_card(PR + "/fast<br>" + '<span style="color:#FFC800">&#9889; Fast mode ON</span>'), "zoomout"),
         (15, 21, lambda tl: prompt_bar(tl > 0.7), "bottom")]
    beats_scene(base, t, sid, "Doosra", "TERMINAL", "term", words, b)

def S_caution(base, t):
    sid = "caution"
    words = [("Dhyan", True), ("rakho!", True), ("Ye", False), ("sirf", False), ("Opus", True), ("par", False), ("chalta", False), ("hai,", False), ("aur", False), ("har", False), ("token", True), ("ka", False), ("daam", True), ("zyada", True), ("hai.", False), ("Subscription", False), ("mein", False), ("ye", False), ("usage", False), ("credits", False), ("se", False), ("kat-ta", False), ("hai.", False)]
    b = [(0, 3, lambda tl: sprite(circle(520, ic("warn", 330))), "zoomin"),
         (4, 8, lambda tl: small("Sirf Opus par", "bolt", size=84), "left"),
         (9, 14, lambda tl: big_card("Price ↑", "har token ka daam", None, size=130), "right"),
         (15, 22, lambda tl: meter(1 - 0.55 * clamp(tl / 2.5)), "bottom")]
    beats_scene(base, t, sid, "Teesra", "CAUTION", "warn", words, b)

def S_tip(base, t):
    sid = "tip"
    words = [("Isliye", False), ("session", True), ("ki", False), ("shuruaat", True), ("mein", False), ("chalu", True), ("karo,", False), ("aur", False), ("kharcha", False), ("zyada", False), ("lage", False), ("toh", False), ("phir", False), ("slash", True), ("fast", True), ("se", False), ("band", True), ("kar", False), ("do.", False)]
    b = [(0, 6, lambda tl: toggle(tl > 0.9), "left"),
         (7, 12, lambda tl: big_card("Kharcha ↑", "usage tez katta hai", None, size=120), "right"),
         (13, 18, lambda tl: toggle(not (tl > 1.0)), "zoomin")]
    beats_scene(base, t, sid, "Tip", "TIP", "star", words, b)

def S_cta(base, t):
    sid = "cta"; decor3(base, t, sid)
    place(base, sprite(robot_circle(480, "thumbs")), 540, 480, pop(t, SC[sid] + 0.05), fade(t, SC[sid], 0.2))
    t0 = T(sid, 8)
    place(base, sprite(card(700, '<div style="font:700 40px MK;color:#777">Comment</div><div style="font:800 96px MK">FAST</div>', pad=30, r=32)), 540, 880, pop(t, t0), fade(t, t0, 0.2))
    words = [("Aise", False), ("Claude", True), ("Code", True), ("tips", True), ("chahiye?", False), ("Follow", True), ("karo,", False), ("aur", False), ("comment", True), ("mein", False), ("FAST", True), ("likho.", False)]
    phrase(base, t, sid, words, 0, 4, T(sid, 5)); phrase(base, t, sid, words, 5, 11, E(sid))

mc.SCENES.update({"hook": S_hook, "what": S_what, "how": S_how, "caution": S_caution, "tip": S_tip, "cta": S_cta})

if __name__ == "__main__":
    (HERE / "review").mkdir(exist_ok=True); (HERE / "output").mkdir(exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(mc.frame(tt)).save(HERE / f"review/F_{tt:05.1f}.png")
    else:
        mc.build_audio(HERE / "audio/voice.wav"); n = int(TOTAL * FPS)
        mc.encode((mc.frame(i / FPS) for i in range(n)), n, HERE / "audio/voice.wav", ROOT / "shared/music/clean/Local_Forecast_Elevator.mp3", HERE / "output/clean_v3.mp4")
