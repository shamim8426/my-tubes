"""Short 023 docs: Extend Claude Code (features-overview): CLAUDE.md vs Skill vs Hook. Style: Day 1 'clean product-page'.
Source: https://code.claude.com/docs/en/features-overview.md (read 2026-11-04)."""
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "templates"))
from ydeck_helpers import *

CHIP = f"background:#fff;border:2px solid #E3E7EE;border-radius:30px;padding:22px 38px;{SHADOW}"
S = []
V = "Claude Code को अपने हिसाब से चलाना है? तीन चीज़ें हैं, और हर एक का अपना अलग काम है।"
L = [tx("Claude Code ko **apne hisaab** se", 80, 230, 96, 920, 0.1),
     box('<div style="font-size:70px;font-weight:800">CLAUDE.md</div>', 140, 640, CHIP, **pop("तीन चीज़ें", 0.0)),
     box('<div style="font-size:70px;font-weight:800">Skill</div>', 140, 860, CHIP, **pop("तीन चीज़ें", 0.5)),
     box('<div style="font-size:70px;font-weight:800">Hook</div>', 140, 1080, CHIP, **pop("तीन चीज़ें", 1.0)),
     ic("file", 640, 650, 120, cue="तीन चीज़ें", off=0.0, float=6),
     ic("sparkle", 640, 870, 120, cue="तीन चीज़ें", off=0.5, float=6),
     ic("bolt", 640, 1090, 120, cue="तीन चीज़ें", off=1.0, float=6),
     tx("har ek ka **alag** kaam", 80, 1380, 96, 640, "अलग काम|-0.4"),
     dict(kind="img", img="wave", size=330, x=720, y=1500, bob=1, k=[["Claude Code|0.2", {"x": 1200, "o": 1}], ["Claude Code|1.0", {"x": 720}]])]
S.append(dict(id="hook", type="stage", wipe="fade", voice=V, layers=L))

V = "पहली है CLAUDE.md. ये हर session में अपने आप load होने वाले नियम हैं, जैसे फ्रिज पर चिपकी घर के नियमों की list। जैसे: use pnpm, not npm।"
L = [tx("**1.** CLAUDE.md", 80, 230, 110, 920, 0.1),
     box('<div style="font-size:30px;font-weight:700;margin-bottom:14px">jaise ek... fridge note</div><div class="mono" style="font-size:40px;font-weight:700;line-height:1.5">Use pnpm, not npm.<br>Run tests before committing.</div>', 100, 520, "width:880px;padding:40px 44px;box-sizing:border-box", cls="sticky", k=[[0, {"r": -2}]], **pop("फ्रिज", -0.4)),
     ic("file", 100, 1010, 190, cue="load होने", off=-0.2, float=7),
     tx("har session me **apne aap**", 330, 1040, 84, 700, "हर session|-0.1"),
     ic("check", 140, 1330, 130, cue="जैसे: use", off=0.0, drawon=["जैसे: use|0.2", 0.6]),
     tx("**hamesha** wale niyam", 330, 1340, 84, 700, "नियम|0.0")]
S.append(dict(id="claudemd", type="stage", wipe="fade", voice=V, layers=L))

V = "दूसरी है Skill। ये एक recipe card है, जो ज़रूरत पड़ने पर ही load होती है। जब एक ही prompt बार बार टाइप करते हो, उसे skill बना दो, जैसे slash deploy।"
L = [tx("**2.** Skill", 80, 230, 110, 920, 0.1),
     box(card('<div style="font-size:30px;font-weight:700;color:#667">jaise ek... recipe card</div><div style="font-size:60px;font-weight:800;margin-top:12px">/deploy</div><div style="font-size:38px;margin-top:6px;color:#445">deployment checklist</div>', 860, "34px 44px"), 110, 520, "", k=[[0, {"r": 2}]], **pop("recipe card", -0.3)),
     ic("sparkle", 780, 560, 130, cue="recipe card", off=0.2, float=7),
     box(window("same prompt, again and again", 860, 330, dark=True), 110, 960, "", **pop("बार बार", -0.5)),
     typed("> deploy checklist chalao...", 150, 1080, 40, "बार बार|0.0", w=800, cps=16),
     typed("> /deploy", 150, 1170, 46, "slash deploy|-0.9", w=800, cps=14, color="#FFD60A"),
     tx("**ek baar** likho, baar baar use", 80, 1390, 84, 920, "skill बना दो|0.0")]
S.append(dict(id="skill", type="stage", wipe="fade", voice=V, layers=L))

V = "तीसरा है Hook। ये हर बार अपने आप चलता है, Claude के सोचने पर निर्भर नहीं। जैसे हर file edit के बाद ESLint चलाना।"
L = [tx("**3.** Hook", 80, 230, 110, 920, 0.1),
     box(window("every file edit", 880, 560), 100, 520, "", **pop("हर बार", -0.4)),
     ic("file", 160, 690, 170, cue="file edit", off=-0.3, wig="file edit|0.3"),
     flow([[340, 775], [560, 775]], None, "ESLint|-0.8", dur=0.5, sw=8, n=2, per=1.2, r=12),
     ic("gear", 580, 680, 190, cue="ESLint", off=-0.4, spin=60, spinAt="ESLint|-0.2"),
     ic("check", 810, 690, 160, cue="ESLint", off=0.5, drawon=["ESLint|0.5", 0.6]),
     box('<div class="mono" style="font-size:38px;font-weight:700">ESLint</div>', 560, 900, "", **pop("ESLint", -0.2)),
     tx("**automatic**, har baar", 80, 1230, 80, 920, "अपने आप|-0.1"),
     tx("Claude ke **sochne** par nirbhar nahi", 80, 1480, 60, 920, "सोचने|-0.3", color="#445")]
S.append(dict(id="hook2", type="stage", wipe="fade", voice=V, layers=L))

V = "गलती मत करना: CLAUDE.md में never edit dot env लिखना सिर्फ़ एक request है, guarantee नहीं। जो नियम हर बार टिकना ज़रूरी है, उसे hook बनाओ।"
L = [tx("**Request** ya **guarantee**?", 80, 230, 96, 920, 0.1),
     box(card('<div style="font-size:30px;font-weight:700;color:#667">CLAUDE.md</div><div class="mono" style="font-size:40px;font-weight:700;margin-top:10px">never edit .env</div><div style="font-size:46px;font-weight:800;margin-top:14px">= sirf request</div>', 860, "34px 44px"), 110, 520, "", **pop("CLAUDE.md में", -0.3)),
     ic("cross", 790, 780, 120, cue="request", off=-0.2, wig="request|0.3"),
     box(card('<div style="font-size:30px;font-weight:700;color:#667">Hook (PreToolUse)</div><div class="mono" style="font-size:40px;font-weight:700;margin-top:10px">blocks the edit</div><div style="font-size:46px;font-weight:800;margin-top:14px">= <span style="background:#FFD60A;padding:0 12px;border-radius:12px">enforcement</span></div>', 860, "34px 44px"), 110, 960, "", **pop("hook बनाओ", -0.6)),
     ic("shield", 790, 1230, 130, cue="hook बनाओ", off=0.0, float=6),
     tx("har baar **tikna** ho = hook", 80, 1450, 84, 920, "हर बार टिकना|0.0")]
S.append(dict(id="caution", type="stage", wipe="fade", voice=V, layers=L))

V = "याद रखो: हमेशा का नियम CLAUDE.md में, दोहराया हुआ काम skill में, और जो हर बार अपने आप चले, वो hook में।"
L = [tx("**Yaad** rakho", 80, 230, 110, 920, 0.1),
     box(card('<span style="font-size:50px;font-weight:800">CLAUDE.md</span><span style="font-size:42px;font-weight:700;color:#445"> = hamesha ka niyam</span>', 900, "30px 40px"), 90, 520, "", **pop("CLAUDE.md में", -0.2)),
     box(card('<span style="font-size:50px;font-weight:800">Skill</span><span style="font-size:42px;font-weight:700;color:#445"> = dohraya kaam</span>', 900, "30px 40px"), 90, 760, "", **pop("skill में", -0.2)),
     box(card('<span style="font-size:50px;font-weight:800">Hook</span><span style="font-size:42px;font-weight:700;color:#445"> = har baar apne aap</span>', 900, "30px 40px"), 90, 1000, "", **pop("hook में", -0.2)),
     ic("check", 880, 1260, 120, cue="hook में", off=0.4, drawon=["hook में|0.5", 0.6]),
     dict(kind="img", img="thumbs", size=400, x=90, y=1250, bob=1, k=[["हर बार अपने|-0.3", {"o": 0}], ["हर बार अपने|0.0", {"o": 1}]])]
S.append(dict(id="recap", type="stage", wipe="fade", voice=V, layers=L))
S.append(cta_scene())

finish(HERE, "Short 023 Extend Claude Code: CLAUDE.md vs Skill vs Hook. Source https://code.claude.com/docs/en/features-overview.md (read 2026-11-04). Day 1 product-page style.", "Claude Code · Extend", S)
