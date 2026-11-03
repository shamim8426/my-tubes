from PIL import Image, ImageDraw, ImageFont
ROOT = r"D:\my-tubes"
S = ROOT + r"\channels\yellow-bot\stories\020_quickstart"
FB = ROOT + r"\shared\fonts\Poppins-Bold.ttf"
FM = ROOT + r"\shared\fonts\Poppins-Medium.ttf"
try:
    fb = lambda n: ImageFont.truetype(FB, n)
    fm = lambda n: ImageFont.truetype(FM, n)
    fm(10)
except Exception:
    fm = fb
items = [
    ("t_09.00", "~9 s  HOOK", "Kinetic counter '4' + 4 step icons pop in & float, travelling dots, sparkles, robot slide-in"),
    ("t_46.00", "~46 s  ICON HUB", "Icons ORBIT the robot; connector lines follow them with travelling dots; camera slow push (not visible in a still)"),
    ("t_20.50", "~20 s  TERMINAL", "Typing terminal with blinking cursor, install -> version -> check icons (draw-on), step ring 1/4"),
    ("t_56.00", "~56 s  BEFORE / AFTER", "Split-screen before/after, speech-bubble pop, keycap 'Yes' + moving cursor click, picture-in-picture robot"),
    ("t_10.15", "~10 s  TRANSITION", "Zoom-through caught mid-way (old scene zooms past and fades, new one scales in). Also built: push/slide, iris, fade, yellow wipe"),
    ("t_31.00", "~31 s  RING + KEYCAPS", "Step progress ring 2/4 (fills 25% per step), floating keycap chips, key -> globe -> check flow"),
    ("t_70.00", "~70 s  ROBOT POINTS", "Robot points; icon trail: packets travel from robot to icons; keycap combos /help /clear Shift+Tab"),
    ("t_79.00", "~79 s  RECAP", "Icons fly in and assemble, kinetic counter 4/4, check ticks pop, PiP robot, open question"),
]
FW, FH = 405, 720
M = 24
W = 4 * FW + 5 * M
cap_h = 118
legend_h = 330
H = 2 * (FH + cap_h) + 3 * M + legend_h + 70
sh = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(sh)
d.text((M, 18), "Short 020 Quickstart - reference stills (real renders of the planned deck; timings approximate, voice not generated yet)", font=fb(26), fill="#111")
for i, (f, t, desc) in enumerate(items):
    x = M + (i % 4) * (FW + M)
    y = 70 + (i // 4) * (FH + cap_h + M)
    im = Image.open(f"{S}\\build\\stills\\{f}.png").convert("RGB").resize((FW, FH), Image.LANCZOS)
    sh.paste(im, (x, y))
    d.rectangle([x - 1, y - 1, x + FW, y + FH], outline="#111", width=2)
    d.rectangle([x, y + FH + 6, x + FW, y + FH + 38], fill="#FFD60A")
    d.text((x + 8, y + FH + 8), t, font=fb(22), fill="#111")
    # wrap description
    words, line, yy = desc.split(), "", y + FH + 46
    for w_ in words:
        if d.textlength(line + " " + w_, font=fm(17)) > FW:
            d.text((x, yy), line, font=fm(17), fill="#111"); yy += 22; line = w_
        else:
            line = (line + " " + w_).strip()
    d.text((x, yy), line, font=fm(17), fill="#111")
ly = 70 + 2 * (FH + cap_h + M) + 4
d.rectangle([M, ly, W - M, ly + legend_h], outline="#111", width=2)
leg = [
    ("ICONS (inline SVG, one stroke width, layer kind 'icon')", "terminal, code, desktop, globe, phone, file, folder, gear, bolt, lock, plug, sparkle, magnifier, check, cross, arrow, clock, branch, chat, key, bulb, box, shield, rocket, cursor, play, user, bug  (+ robot mascot, svgbot)"),
    ("MOTIONS (opt-in fields)", "float, pulse, spin, orbit, in+spring (pop-in overshoot, scale 0.6 to 1), drawon (stroke draw-on), wig (wiggle), stagger (cue offsets), flow (connector + travelling dot/packet + trail), spark (twinkling stars), typed (typing + blinking cursor), ring (progress ring), count (bouncing counter), cam (camera push/pan)"),
    ("TRANSITIONS (scene field 'wipe')", "yellow wipe (right/left/up), fade, push, iris, zoom  -  plus word-by-word marker text (stream), speech bubbles (cls bubble), key-caps (class keycap), sticky notes, soft shadow (sh), picture-in-picture robot, before/after split"),
    ("NOT visible in a single still", "blinking cursor, travelling dots, orbit, floating, twinkling, spin, camera push, counter bounce, transitions in motion, word-by-word marker sweep, draw-on strokes"),
]
yy = ly + 12
for h, b in leg:
    d.text((M + 14, yy), h, font=fb(20), fill="#111"); yy += 28
    line = ""
    for w_ in b.split():
        if d.textlength(line + " " + w_, font=fm(18)) > W - 2 * M - 40:
            d.text((M + 14, yy), line, font=fm(18), fill="#333"); yy += 24; line = w_
        else:
            line = (line + " " + w_).strip()
    d.text((M + 14, yy), line, font=fm(18), fill="#333"); yy += 36
sh.save(S + r"\output\reference_sheet.jpg", quality=90)
print(sh.size)
