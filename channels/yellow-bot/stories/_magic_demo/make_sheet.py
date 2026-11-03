import subprocess
from PIL import Image, ImageDraw, ImageFont
R = r"D:\my-tubes"
S = R + r"\channels\yellow-bot\stories\_magic_demo"
PY = R + r"\.venv\Scripts\python.exe"
# extra stills (portal+glint, morph)
subprocess.run([PY, "-X", "utf8", R + r"\scripts\build_deck.py", S, "--still", "0.9,2.1,3.2,4.6,5.8,8.2,8.75,10.3,6.6"], check=True, capture_output=True)
fb = lambda n: ImageFont.truetype(R + r"\shared\fonts\Poppins-Bold.ttf", n)
fm = lambda n: ImageFont.truetype(R + r"\shared\fonts\Poppins-Medium.ttf", n)
items = [
    ("t_00.90", "dust", "Stardust burst + fountain from a point; seeded particles"),
    ("t_02.10", "wand", "Glowing comet draws the circle/underline, sparkle trail"),
    ("t_03.20", "assemble", "Text materialises from converging particles (reverse = dissolve)"),
    ("t_04.60", "portal + shock + glint", "Ring portal reveals the scene, shockwave, light sweep on the text"),
    ("t_05.80", "aura", "Pulsing glow + rotating light rays behind the robot casting"),
    ("t_08.20", "morph", "Liquid (goo) morph terminal > chat > check"),
    ("t_08.75", "tilt + parallax", "3D card flip with perspective; depth layers drift"),
    ("t_10.30", "magnet", "Icons fly in curved arcs with trails into the target"),
]
FW, FH, M = 405, 720, 24
W = 4 * FW + 5 * M
cap_h = 92
leg_h = 520
H = 70 + 2 * (FH + cap_h + M) + leg_h + 30
sh = Image.new("RGB", (W, H), "white")
d = ImageDraw.Draw(sh)
d.text((M, 18), "Yellow Bot MAGIC effects - stills from effects_reel.mp4 (real renders; motion is in the video)", font=fb(26), fill="#111")
for i, (f, t, desc) in enumerate(items):
    x = M + (i % 4) * (FW + M)
    y = 70 + (i // 4) * (FH + cap_h + M)
    sh.paste(Image.open(f"{S}\\build\\stills\\{f}.png").convert("RGB").resize((FW, FH), Image.LANCZOS), (x, y))
    d.rectangle([x - 1, y - 1, x + FW, y + FH], outline="#111", width=2)
    d.rectangle([x, y + FH + 6, x + FW, y + FH + 40], fill="#FFD60A")
    d.text((x + 8, y + FH + 8), t, font=fb(22), fill="#111")
    line, yy = "", y + FH + 48
    for w_ in desc.split():
        if d.textlength(line + " " + w_, font=fm(17)) > FW:
            d.text((x, yy), line, font=fm(17), fill="#111"); yy += 22; line = w_
        else:
            line = (line + " " + w_).strip()
    d.text((x, yy), line, font=fm(17), fill="#111")
ly = 70 + 2 * (FH + cap_h + M)
d.rectangle([M, ly, W - M, ly + leg_h], outline="#111", width=2)
leg = [
    ("dust", '{"kind":"dust","from":[x,y],"at","dur","n","speed","life","size","mode":"burst|fountain","spread","grav"}'),
    ("wand", '{"kind":"wand","shape":"underline|circle|line|poly","pts" or "cx,cy,rx,ry","at","dur","sw","fadeAt","ss"}'),
    ("assemble", '{"kind":"assemble","text","cx","cy","size","at","dur","reverse":true (= dissolve),"gap","dot","color"}'),
    ("portal / shock", 'scene {"wipe":"portal","trd":0.7}   layer {"kind":"shock","from","at","dur","r","rings"}'),
    ("glint", '{"kind":"glinttext","html","x","y","w","size","glint":[t0,dur]}  (yellow/white sweep through the letters)'),
    ("aura", '{"kind":"aura","from","at","dur","r","rays","rayLen"}   (place BEFORE the robot layer so it glows behind)'),
    ("poof", '{"kind":"poof","from","at","dur","size"}   (cartoon smoke; not in the 8 stills, see reel 6.4 s)'),
    ("morph", '{"kind":"morph","icons":["terminal","chat","check"],"size","ts":[t1,t2],"md":0.4}'),
    ("tilt / parallax", '{"kind":"card3d","w","h","front","back","fcss","bcss","tilt","k":[[t,{"ry":deg}]]}   any layer: "z": depth (parallax drift)'),
    ("magnet", '{"kind":"magnet","items":[{"name","from":[x,y]}],"to":[x,y],"at","dur","stag","arc","size"}'),
]
yy = ly + 14
d.text((M + 14, yy), "EFFECTS and their deck fields (times in seconds from scene start; all are pure functions of time, seeded PRNG)", font=fb(20), fill="#111"); yy += 34
for n, s in leg:
    d.text((M + 14, yy), n, font=fb(18), fill="#111")
    d.text((M + 230, yy), s, font=fm(17), fill="#333"); yy += 29
yy += 8
d.text((M + 14, yy), "Not visible in a still: particle motion, comet travel, converging dots, ring expansion, light-ray rotation, goo morph, 3D flip, arc trails.", font=fm(17), fill="#333")
sh.save(S + r"\output\reel_sheet.jpg", quality=88)
print(sh.size)
