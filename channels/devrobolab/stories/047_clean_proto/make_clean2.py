r"""Clean-style Short v2 (chapter grammar learned from the study): corner burst shapes, chapter label + chip, screen card in the middle, caption ABOVE the card, bullets BELOW one by one, counting number, Devanagari cards.
Run (ffmpeg on PATH):  python make_clean2.py [frames t1 t2 ...]"""
import sys, math
import numpy as np
from PIL import Image
import make_clean as mc
from make_clean import *

ORANGE = "#F4743B"
def burst(size, rot=0, n=7):
    c = size / 2; lines = ""
    for i in range(n):
        a = math.radians(i * 360 / n + rot); l = size * (0.34 + 0.12 * ((i * 5) % 3) / 2)
        lines += f'<line x1="{c}" y1="{c}" x2="{c + l * math.cos(a)}" y2="{c + l * math.sin(a)}" stroke="{ORANGE}" stroke-width="{size * 0.11}" stroke-linecap="round"/>'
    return sprite(f'<svg width="{size}" height="{size}" style="display:block">{lines}</svg>')

def decor(base, t, sid):
    k = 0.5 + 0.5 * ease_out((t - SC[sid]) / 0.6)
    place(base, burst(520, rot=t * 6), 40, 80, k, 1.0)
    place(base, burst(420, rot=-t * 5 + 20), 1060, 1500, k, 1.0)

def chip(name, icon):
    return sprite(f'<div style="display:flex;align-items:center;gap:14px;background:#fff;border-radius:16px;padding:6px 26px 10px 14px;font:800 46px MK;color:#222;{SH}">{ic(icon, 44)}{name}</div>')
def big_label(txt): return sprite(f'<div style="font:800 150px MK;color:#111;white-space:nowrap">{txt}</div>')
def bullet(txt, icon="star"): return sprite(f'<div style="display:flex;align-items:center;gap:22px;font:700 54px MK;color:#111;white-space:nowrap">{ic(icon, 54)}<span>{txt}</span></div>')

def chapter(base, t, sid, label, chip_name, chip_icon, card_spr, words, bullets, cap_top=1010, card_y=600, key_label=None):
    t0 = SC[sid]; intro = 0.95
    if t < t0 + intro:
        q = pop(t, t0 + 0.02); out = 1 - fade(t, t0 + intro - 0.2, 0.2)
        place(base, big_label(label), 540, 800, 0.8 + 0.2 * q, fade(t, t0, 0.15) * out)
        place(base, chip(chip_name, chip_icon), 540, 980, pop(t, t0 + 0.25), fade(t, t0 + 0.25, 0.15) * out)
    else:
        place(base, chip(chip_name, chip_icon), 540, card_y - card_spr.height * 1.15 / 2 - 70, 1.35, 1.0)
        q = pop(t, t0 + intro, 0.4); slide = (1 - ease_out((t - t0 - intro) / 0.4)) * 120
        place(base, card_spr, 540, card_y + slide, 1.15 * (0.9 + 0.1 * q), fade(t, t0 + intro, 0.2))
        caption(base, t, sid, words, label=key_label, top=cap_top)
        for i, (k, txt, icn) in enumerate(bullets):
            tb = T(sid, k) - 0.05
            if t >= tb:
                a = fade(t, tb, 0.2); place(base, bullet(txt, icn), 540, 1450 + i * 120 + (1 - a) * 30, 1.2, a)

def S_hook(base, t):
    decor(base, t, "hook"); mc.S_hook(base, t)

def S_what(base, t):
    sid = "what"; v = min(2.5, 1.0 + 1.5 * clamp((t - T(sid, 11)) / 1.0)); v = round(v, 1)
    card_ = card(760, f'<div style="text-align:center;font:800 190px MK;color:#111;line-height:1.1">{v}x</div><div style="text-align:center;font:700 44px MK;color:#666">tez jawab</div>', pad=34, r=40)
    words = [("Ye", False), ("Fast", True), ("mode", True), ("hai.", False), ("Model", False), ("wahi", True), ("Opus", True), ("rehta", False), ("hai,", False), ("quality", False), ("bhi", False), ("same,", True), ("bas", False), ("jawab", False), ("tez", True), ("aate", False), ("hain.", False)]
    chapter(base, t, sid, "Pehla", "FAST MODE", "bolt", sprite(card_), words, [(5, "Model wahi, Opus", "check"), (11, "Quality same", "check")], cap_top=1010)

def S_how(base, t):
    sid = "how"; typed = T(sid, 3); on = T(sid, 13)
    state = 2 if t >= on else (1 if t >= typed else 0)
    body = {0: '<span style="color:#7cf0a8">&gt;</span> <span style="opacity:.5">_</span>', 1: '<span style="color:#7cf0a8">&gt;</span> /fast', 2: '<span style="color:#7cf0a8">&gt;</span> /fast<br><span style="color:#FFC800">&#9889; Fast mode ON</span>'}[state]
    term = sprite(card(800, f'<div style="display:flex;gap:10px;margin-bottom:18px"><i style="width:16px;height:16px;border-radius:50%;background:#ff5f57"></i><i style="width:16px;height:16px;border-radius:50%;background:#febc2e"></i><i style="width:16px;height:16px;border-radius:50%;background:#28c840"></i></div><div style="font:700 56px MO;line-height:1.5;color:#e6edf7;min-height:170px">{body}</div>', bg="#0f172a", pad=34))
    words = [("Terminal", True), ("mein", False), ("slash", True), ("fast", True), ("likho,", False), ("Space", True), ("dabao,", False), ("phir", False), ("Enter.", True), ("screen", False), ("par", False), ("Fast", True), ("mode", True), ("ON", True), ("dikhega,", False), ("aur", False), ("prompt", False), ("ke", False), ("paas", False), ("ek", False), ("chhota", False), ("icon.", True)]
    chapter(base, t, sid, "Doosra", "TERMINAL", "term", term, words, [(5, "Space dabao", "star"), (8, "Phir Enter", "star"), (19, "Paas mein ⚡ icon", "bolt")], cap_top=1010)

def S_caution(base, t):
    sid = "caution"
    c = sprite(card(800, f'<div style="display:flex;align-items:center;gap:26px">{ic("warn", 130)}<div style="font:800 64px MK;line-height:1.15">Careful</div></div>', pad=40, r=40))
    words = [("Dhyan", True), ("rakho!", True), ("Ye", False), ("sirf", False), ("Opus", True), ("par", False), ("chalta", False), ("hai,", False), ("aur", False), ("har", False), ("token", True), ("ka", False), ("daam", True), ("zyada", True), ("hai.", False), ("Subscription", False), ("mein", False), ("Ye", False), ("usage", False), ("credits", False), ("se", False), ("kat-ta", False), ("hai.", False)]
    chapter(base, t, sid, "Teesra", "CAUTION", "warn", c, words, [(4, "Sirf Opus par", "warn"), (12, "Har token mehnga", "warn"), (20, "Usage credits se kat-ta hai", "warn")], cap_top=1010)

def S_tip(base, t):
    sid = "tip"
    c = sprite(card(800, '<div style="font:800 74px MK;text-align:center;line-height:1.2">Shuru mein <span style="background:#FFC800;padding:0 14px;border-radius:12px">/fast</span> chalu</div>', pad=44, r=40))
    words = [("Isliye", False), ("session", True), ("ki", False), ("shuruaat", True), ("mein", False), ("chalu", True), ("karo,", False), ("aur", False), ("kharcha", False), ("zyada", False), ("lage", False), ("toh", False), ("phir", False), ("slash", True), ("fast", True), ("se", False), ("band", True), ("kar", False), ("do.", False)]
    chapter(base, t, sid, "Tip", "TIP", "star", c, words, [(5, "Session ke start mein ON", "check"), (16, "Kharcha badhe toh OFF", "check")], cap_top=1010)

def S_cta(base, t):
    decor(base, t, "cta"); mc.S_cta(base, t)

mc.SCENES.update({"hook": S_hook, "what": S_what, "how": S_how, "caution": S_caution, "tip": S_tip, "cta": S_cta})

if __name__ == "__main__":
    (HERE / "review").mkdir(exist_ok=True); (HERE / "output").mkdir(exist_ok=True)
    if len(sys.argv) > 1 and sys.argv[1] == "frames":
        for tt in [float(v) for v in sys.argv[2:]]: Image.fromarray(mc.frame(tt)).save(HERE / f"review/D_{tt:05.1f}.png")
    else:
        mc.build_audio(HERE / "audio/voice.wav"); n = int(TOTAL * FPS)
        mc.encode((mc.frame(i / FPS) for i in range(n)), n, HERE / "audio/voice.wav", ROOT / "shared/music/clean/Local_Forecast_Elevator.mp3", HERE / "output/clean_v2.mp4")
