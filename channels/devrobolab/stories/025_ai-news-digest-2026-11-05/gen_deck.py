"""025 LONG (16:9) AI News Digest 2026-11-05. Style: 'news bulletin' (calm light page, ticker top, dark lower-third with item title + source tag).
Sources (all read 2026-11-05, see research/news/2026-11-05_digest.md). Run: .venv\\Scripts\\python -X utf8 <this file>"""
import json
import re
import sys
from pathlib import Path
HERE = Path(__file__).parent
sys.path.insert(0, str(HERE.parents[1] / "templates"))
from ydeck_helpers import tx, box, ic, card, pop, flow, typed, line, window, SHADOW, CTA_VOICE, CTA_SCREEN, CTA_PILL

PILL = "background:#fff;border:2px solid #E3E7EE;border-radius:999px;padding:14px 34px;font-size:34px;font-weight:800;white-space:nowrap;" + SHADOW
YPILL = "background:#FFD60A;border-radius:999px;padding:14px 40px;" + SHADOW
TICK = '<span>AI NEWS DIGEST</span><span style="color:#778"> &nbsp;·&nbsp; 5 Nov 2026</span>'
S = []
IMG = (HERE / "img")


def pic(name, x, y, w, h, at=0.5):
    """Abstract AI illustration (free Cloudflare flux, no text/people/logos) as a rounded side picture."""
    return box(f'<img src="{(IMG / (name + ".png")).as_uri()}" style="width:{w}px;height:{h}px;object-fit:cover;border-radius:34px;display:block">', x, y, f"border:2px solid #E3E7EE;border-radius:34px;{SHADOW}", **pop(at, 0.0))




def frame(n, title, org, first):
    lt = (f'<div style="width:1720px;height:150px;background:#14171C;border-radius:28px;display:flex;align-items:center;overflow:hidden;color:#fff;{SHADOW}">'
          f'<div style="width:18px;height:100%;background:#FFD60A;flex:none"></div><div style="font-size:66px;font-weight:800;margin-left:34px;flex:1;white-space:nowrap">{title}</div>'
          f'<div style="background:#FFD60A;color:#111;border-radius:999px;padding:12px 32px;font-size:38px;font-weight:800;margin-right:44px;white-space:nowrap">Source: {org}</div></div>')
    return [box(TICK, 100, 44, PILL),
            box(f'{n} / 5', 1640, 44, f"background:#FFD60A;border-radius:999px;padding:14px 38px;font-size:34px;font-weight:800;{SHADOW}"),
            box(lt, 100, 880, "", **(pop(0.15, 0.0) if first else {}))]


def pcard(icon, big, small, x, y, w, cue, off=-0.1, bg="#fff", fg="#111", bsize=54, ssize=36, ish=96, k=1.25):
    bsize, ssize, ish = round(bsize * k), round(ssize * k), round(ish * k)
    y = y + 60 if 380 <= y <= 430 else y
    sub = f'<div style="font-size:{ssize}px;font-weight:700;color:{"#C9CFDA" if bg == "#14171C" else "#444"};margin-top:6px;line-height:1.2">{small}</div>' if small else ""
    h = (f'<div style="display:flex;align-items:center;gap:28px"><i data-ic="{icon}" data-s="{ish}"></i>'
         f'<div><div style="font-size:{bsize}px;font-weight:800;line-height:1.1;color:{fg}">{big}</div>{sub}</div></div>')
    return box(card(h, w, "26px 38px", bg), x, y, "", **pop(cue, off))


def dark(inner, x, y, w, cue, off=-0.2):
    y = y + 50 if 380 <= y <= 430 else y
    return box(inner, x, y, f"background:#14171C;border-radius:34px;padding:30px 44px;width:{w}px;{SHADOW}", **pop(cue, off))


def scene(sid, voice, layers):
    S.append(dict(id=sid, type="stage", wipe="fade", voice=voice, layers=layers))


def item(n, org, title, scs):
    for k, (sid, v, layers) in enumerate(scs):
        scene(sid, v, frame(n, title, org, k == 0) + layers)


def price(head, a, b):
    return (f'<div style="font-size:34px;font-weight:700;color:#C9CFDA">{head}</div>'
            f'<div style="font-size:84px;font-weight:800;color:#FFD60A;margin-top:12px;line-height:1.1">{a} <span style="font-size:40px;color:#fff">input</span></div>'
            f'<div style="font-size:84px;font-weight:800;color:#FFD60A;line-height:1.1">{b} <span style="font-size:40px;color:#fff">output</span></div>')


# ---------- HOOK ----------
V = "आज की पाँच AI खबरें, सीधी भाषा में: Google का नया model, Mistral का open model, Mac पर text to speech, ElevenLabs का v4, और Claude Code की एक काम की update।"
names = [("sparkle", "Gemini 4 Carbon", "Google"), ("box", "Mistral Large 4", "Mistral"), ("terminal", "Ollama + Mac", "Mac"), ("bolt", "ElevenLabs v4", "ElevenLabs"), ("code", "Claude Code", "Claude Code")]
L = [tx("**5 AI khabrein**", 100, 150, 150, 1000, 0.1), tx("aaj ki, seedhi bhasha me", 100, 560, 70, 1000, "सीधी भाषा|-0.2"),
     box(TICK, 100, 670, PILL, **pop(0.6)),
     dict(kind="img", img="wave", size=300, x=130, y=730, bob=1, k=[[0.3, {"x": -500, "o": 1}], [1.0, {"x": 130}]])]
for i, (icn, t, cue) in enumerate(names):
    L.append(pcard(icn, t, "", 1120, 170 + i * 142, 700, cue, -0.1, bsize=50, ish=84, k=1.0))
L.insert(0, pic("hook", 560, 640, 500, 300, 0.4))
scene("hook", V, L)

# ---------- 1 GEMINI 4 CARBON ----------
item(1, "Google DeepMind", "Gemini 4 Carbon", [
    ("g1", "पहली खबर: Google DeepMind ने Gemini 4 Carbon announce किया है। Google इसे अपना अब तक का सबसे strong model बताता है।",
     [tx("**Gemini 4 Carbon**", 100, 170, 112, 1300, 0.1), tx("Google ka naya **sabse strong** model", 100, 330, 74, 1150, "सबसे strong|-0.4"),
      pcard("globe", "Google DeepMind ne bataya", "28 Oct 2026", 100, 540, 840, "announce", -0.2),
      ic("sparkle", 1380, 230, 340, cue="Gemini 4", off=0.0, float=9, wig="सबसे strong|0.3"),
      box('<div style="font-size:44px;font-weight:800">NEW</div>', 1450, 640, YPILL, wig="सबसे strong|0.6", **pop("सबसे strong", 0.2))]),
    ("g2", "आम लोगों के लिए अभी नहीं। पेज के हिसाब से अभी सिर्फ कुछ cyber defenders को मिल रहा है, फिर trusted partners को। आम users की तारीख पेज में नहीं लिखी।",
     [tx("**Abhi sabke liye nahi**", 100, 170, 100, 1500, 0.1),
      pcard("shield", "Cyber defenders", "abhi, kuch logon ko", 100, 400, 540, "cyber defenders", -0.1, bsize=44, ssize=32, k=1.0),
      pcard("user", "Trusted partners", "dheere dheere", 690, 400, 540, "trusted partners", -0.1, bsize=44, ssize=32, k=1.0),
      pcard("phone", "Aam users", "tarikh: page me nahi likha", 1280, 400, 540, "आम users", -0.1, bsize=44, ssize=32, k=1.0),
      flow([[650, 560], [680, 560]], None, "trusted partners|-0.3", dur=0.4, sw=8, n=1, per=1.0, r=11),
      flow([[1240, 560], [1270, 560]], None, "आम users|-0.3", dur=0.4, sw=8, n=1, per=1.0, r=11),
      ic("cross", 1560, 650, 110, cue="नहीं लिखी", off=-0.6, wig="नहीं लिखी|0.0")]),
    ("g3", "ये बड़े codebase में bug ढूँढने और patch करने जैसे लंबे काम के लिए बना है। शुरुआती दाम: दो डॉलर input, दस डॉलर output, हर दस लाख tokens पर।",
     [tx("**Lambe kaam** ke liye", 100, 170, 100, 1500, 0.1),
      pcard("bug", "Bade codebase me bug", "dhoondo aur patch karo", 100, 400, 820, "bug ढूँढने", -0.2, bsize=52),
      dark(price("shuruaati daam, har 10 lakh tokens par", "$2", "$10"), 1020, 390, 800, "शुरुआती दाम"),
      box('<div style="font-size:40px;font-weight:800">token = text ka chhota tukda</div>', 100, 750, YPILL, **pop("tokens", -0.1))]),
])

# ---------- 2 MISTRAL LARGE 4 ----------
item(2, "Mistral AI", "Mistral Large 4 (open weights)", [
    ("m1", "दूसरी खबर: Mistral AI ने Mistral Large 4 के open weights जारी किए हैं। Open weights यानी model की file download करके खुद चला सकते हो।",
     [tx("**Open weights** jaari", 100, 170, 112, 1500, 0.1), pic("open", 1230, 120, 590, 300, 0.6),
      pcard("box", "Open weights", "= model ki file, download karo", 100, 400, 900, "Open weights यानी", -0.1, bsize=56),
      ic("arrow", 1060, 470, 120, cue="download", off=-0.5, drawon=["download|-0.5", 0.5]),
      pcard("desktop", "Khud ke computer par", "page: vLLM ya SGLang se self-host", 1230, 400, 590, "खुद चला", -0.1, bsize=44, ssize=32, ish=80),
      box('<div style="font-size:46px;font-weight:800">Hugging Face par</div>', 100, 750, YPILL, **pop("download", 0.2))]),
    ("m2", "License modified MIT है: use, बदलाव और commercial इस्तेमाल की इजाज़त है। पर अगर आप दूसरों को model service बेचते हो, तो Mistral से अलग commercial license चाहिए।",
     [tx("**License** kya kehta hai?", 100, 170, 100, 1500, 0.1),
      pcard("check", "Use, badlav, commercial", "modified MIT license", 100, 400, 820, "इजाज़त", -0.5, bsize=48),
      pcard("lock", "Model service bechni hai?", "Mistral se alag commercial license", 1000, 400, 820, "service बेचते", -0.2, bg="#14171C", fg="#fff", bsize=48, ssize=34),
      tx("Apne kaam ke liye **theek**, service bechne ke liye **alag license**", 100, 750, 52, 1700, "पर अगर|0.0")]),
    ("m3", "Weights Hugging Face पर हैं। API का दाम भी लिखा है: सत्तर cent input, दो डॉलर दस cent output, हर दस लाख tokens पर। इसे चलाने के लिए कितना बड़ा computer चाहिए, पेज में नहीं लिखा।",
     [tx("**API** ka daam", 100, 170, 100, 1500, 0.1),
      dark(price("har 10 lakh tokens par", "$0.70", "$2.10"), 100, 390, 800, "API", 0.3),
      pcard("desktop", "Kitna bada computer chahiye?", "page me nahi likha", 1000, 420, 820, "कितना बड़ा", -0.2, bsize=44, ssize=38),
      ic("magnifier", 1480, 640, 130, cue="नहीं लिखा", off=-0.5, float=6, wig="नहीं लिखा|0.0")]),
])

# ---------- 3 OLLAMA SPEECH ----------
item(3, "Ollama", "Ollama: text se awaaz", [
    ("o1", "तीसरी खबर: Ollama अब text को आवाज़ में बदल सकता है। पहला speech model है Phonon, जो Gradium का बनाया छोटा text to speech model है।",
     [tx("**Text** se **awaaz**", 100, 170, 112, 1500, 0.1), pic("wave", 1230, 120, 590, 300, 0.6),
      pcard("file", "\"Hello from Ollama.\"", "likha hua text", 100, 400, 780, "text को", -0.2, bsize=46),
      flow([[890, 500], [1020, 500]], None, "आवाज़ में|-0.3", dur=0.5, sw=9, n=2, per=1.0, r=12),
      pcard("play", "Phonon", "Gradium ka chhota model", 1040, 400, 780, "Phonon", -0.1, bg="#14171C", fg="#FFD60A", bsize=60, ssize=34),
      box('<div style="font-size:42px;font-weight:800">Ollama ka pehla speech model</div>', 100, 750, YPILL, **pop("पहला speech", 0.0))]),
    ("o2", "अभी ये सिर्फ Apple Silicon वाले Mac पर चलता है। Windows और Linux के लिए पेज में लिखा है, जल्द आ रहा है, तारीख नहीं।",
     [tx("**Abhi sirf Mac**", 100, 170, 112, 1500, 0.1),
      pcard("check", "Apple Silicon Mac", "Ollama 0.40.11 ya naya", 100, 400, 780, "Apple Silicon", -0.1, bsize=50),
      pcard("clock", "Windows aur Linux", "jald aa raha hai, tarikh nahi", 1000, 400, 820, "Windows और Linux", -0.1, bsize=50, ssize=34),
      ic("cross", 1640, 640, 100, cue="तारीख नहीं", off=-0.6, wig="तारीख नहीं|0.0")]),
    ("o3", "Terminal में लिखो: ollama run phonon, फिर quotes में अपना text। भाषाएँ: English, French, German, Spanish और Portuguese। Hindi का ज़िक्र पेज में नहीं है।",
     [tx("**Ek command** me", 100, 170, 100, 1500, 0.1),
      box(window("terminal", 1000, 330, dark=True), 100, 330, "", **pop(0.4)),
      typed('$ ollama run phonon "Hello"', 140, 440, 46, "ollama run|-0.4", w=940, cps=18),
      box(line('<span style="color:#FFD60A">EN FR DE ES PT</span>', 50), 140, 570, "background:#2B3038;border-radius:18px;padding:18px 28px", **pop("भाषाएँ", -0.1)),
      pcard("cross", "Hindi", "page me nahi likha", 1180, 400, 640, "Hindi", -0.2, bsize=56, ssize=34)]),
])

# ---------- 4 ELEVENLABS V4 ----------
item(4, "ElevenLabs", "ElevenLabs Eleven v4", [
    ("e1", "चौथी खबर: ElevenLabs का Eleven v4, एक text to speech model, जिसे वो अपना सबसे emotive model बताते हैं। साथ में एक तेज़ version, Eleven v4 Turbo भी है।",
     [tx("**Emotion** wali awaaz", 100, 170, 112, 1500, 0.1),
      pcard("play", "Eleven v4", "text to speech, sabse emotive", 100, 400, 850, "Eleven v4", -0.1, bg="#14171C", fg="#FFD60A", bsize=62),
      pcard("bolt", "Eleven v4 Turbo", "tez wala version", 1030, 400, 790, "Turbo", -0.2, bsize=56),
      box('<div style="font-size:42px;font-weight:800">text likho, awaaz suno</div>', 100, 750, YPILL, **pop("text to speech", 0.0))]),
    ("e2", "ये नब्बे से ज़्यादा भाषाओं में बोलता है, और आप लिखकर बता सकते हो कि लाइन किस emotion में बोलनी है। Hindi अलग से पेज में नहीं लिखा। Free account बनाकर try कर सकते हो।",
     [tx("**90+** bhashayein", 100, 170, 112, 1500, 0.1),
      pcard("globe", "90 se zyada bhashayein", "page me Hindi alag se nahi likha", 100, 400, 850, "नब्बे", -0.2, bsize=50, ssize=34),
      pcard("chat", "Likh kar batao", "line kis emotion me boli jaye", 1030, 400, 790, "लिखकर बता", -0.2, bsize=48, ssize=34),
      pcard("user", "Free account", "bana kar try kar sakte ho", 100, 690, 850, "Free account", -0.1, bg="#FFD60A", bsize=48, ssize=34)]),
    ("e3", "Voice clone के लिए दस second की audio चाहिए, ये पेज में लिखा है। दाम पेज में नहीं लिखा। और किसी की आवाज़ बिना इजाज़त clone मत करना।",
     [tx("**Voice clone**", 100, 170, 112, 1500, 0.1),
      box('<div style="font-size:150px;font-weight:800;line-height:1">10 <span style="font-size:60px">sec</span></div><div style="font-size:38px;font-weight:700;color:#444">audio chahiye (page ke hisaab se)</div>', 100, 380, f"background:#fff;border:2px solid #E3E7EE;border-radius:34px;padding:34px 50px;{SHADOW}", **pop("दस second", -0.3)),
      pcard("magnifier", "Daam?", "page me nahi likha", 900, 400, 560, "दाम", -0.1, bsize=56),
      pcard("shield", "Sirf apni awaaz", "bina ijazat kisi aur ki nahi", 900, 620, 920, "इजाज़त", -0.5, bg="#14171C", fg="#FFD60A", bsize=46, ssize=34)]),
])

# ---------- 5 CLAUDE CODE LOGIN DATE ----------
item(5, "Claude Docs", "Claude Code: login ki tarikh", [
    ("c1", "पाँचवीं खबर Claude Code से। नए version में अब पता चलता है कि आपका claude.ai sign-in कब खत्म होगा।",
     [tx("**Login** kab khatam?", 100, 170, 112, 1500, 0.1),
      pcard("lock", "claude.ai sign-in", "ab uski aakhri tarikh dikhti hai", 100, 400, 900, "sign-in", -0.2, bsize=54),
      ic("clock", 1240, 340, 300, cue="कब खत्म", off=-0.2, float=8, wig="कब खत्म|0.2"),
      box('<div style="font-size:34px;font-weight:700">Claude Code 2.1.318 · 4 Nov 2026</div>', 100, 750, PILL, **pop("नए version", 0.0))]),
    ("c2", "Terminal में claude auth status चलाओ। उसमें loginExpiresAt नाम से वो तारीख दिखती है।",
     [tx("**Step 1:** auth status", 100, 170, 100, 1500, 0.1),
      box(window("terminal", 1100, 400, dark=True), 100, 330, "", **pop(0.4)),
      typed("$ claude auth status", 140, 450, 48, "claude auth status|-0.5", w=1000, cps=20),
      box(line('<span style="color:#FFD60A">loginExpiresAt</span>: &lt;date&gt;', 48), 140, 580, "background:#2B3038;border-radius:18px;padding:22px 28px;border:3px solid #FFD60A", **pop("loginExpiresAt", -0.9)),
      ic("check", 1400, 480, 170, cue="तारीख दिखती", off=-0.3, drawon=["तारीख दिखती|-0.3", 0.6])]),
    ("c3", "claude -p चलाने वालों को JSON result में credential_expires_at मिलता है, और sign-in खत्म होने से दस दिन पहले एक लाइन की warning भी।",
     [tx("**claude -p** me bhi", 100, 170, 100, 1500, 0.1),
      pcard("code", "JSON result me", "credential_expires_at", 100, 400, 850, "JSON result", -0.2, bsize=48, ssize=40),
      pcard("bell", "10 din pehle warning", "text output me, ek line", 1030, 400, 790, "दस दिन", -0.2, bg="#FFD60A", bsize=48, ssize=34),
      box('<div style="font-size:42px;font-weight:800">scripts me bhi tarikh padh sakte ho</div>', 100, 750, PILL, **pop("warning", 0.3))]),
])

# ---------- RECAP ----------
V = "तो आज की पाँच खबरें: Gemini 4 Carbon अभी सिर्फ चुने हुए लोगों के लिए है। Mistral Large 4 के weights download हो सकते हैं। Ollama पर Mac में text to speech आ गया। ElevenLabs का v4 ज़्यादा emotion के साथ बोलता है। और Claude Code में login की तारीख दिखती है।"
rows = [("sparkle", "Gemini 4 Carbon", "abhi chune hue logon ke liye", "Gemini 4 Carbon"), ("box", "Mistral Large 4", "weights download ho sakte hain", "Mistral Large 4"),
        ("terminal", "Ollama on Mac", "text to speech aa gaya", "Ollama पर"), ("bolt", "ElevenLabs v4", "zyada emotion ke saath", "ElevenLabs का"), ("code", "Claude Code", "login ki tarikh dikhti hai", "Claude Code में")]
L = [box(TICK, 100, 44, PILL), tx("**Aaj ka recap**", 100, 130, 96, 1200, 0.1)]
for i, (icn, a, b, cue) in enumerate(rows):
    L.append(pcard(icn, a, b, 100 if i < 3 else 1000, 300 + (i if i < 3 else i - 3) * 190, 880, cue, -0.2, bsize=46, ssize=34, ish=80, k=1.0))
L.append(dict(kind="img", img="think", size=330, x=1480, y=640, bob=1, k=[["Gemini 4 Carbon|0.0", {"o": 0}], ["Gemini 4 Carbon|0.5", {"o": 1}]]))
scene("recap", V, L)

# ---------- CTA ----------
L = [tx(CTA_SCREEN, 100, 120, 130, 1200, 0.15),
     box(f'<div style="font-size:130px;font-weight:800;line-height:1">{CTA_PILL}</div>', 160, 640, f"background:#FFD60A;border:0;border-radius:999px;padding:30px 120px;{SHADOW}", wig=4.35, float=5, **pop(0.5)),
     dict(kind="icon", name="cursor", x=0, y=0, size=140, k=[[3.4, {"x": 900, "y": 880, "o": 0}], [3.5, {"x": 900, "y": 880, "o": 1}], [4.2, {"x": 520, "y": 780}]], wig=4.3),
     ic("bell", 930, 640, 200, wig=4.7, float=6, **{"in": 4.5, "spring": True}),
     dict(kind="img", img="thumbs", size=560, x=1180, y=330, bob=1, k=[[0.2, {"x": 2200, "o": 1}], [0.9, {"x": 1180}]])]
S.append(dict(id="follow", type="stage", wipe="fade", voice=CTA_VOICE, layers=L))

wtp = HERE / "wt.json"
wt = json.loads(wtp.read_text(encoding="utf-8")) if wtp.exists() else {}
for sc in S:
    if sc["id"] in wt:
        sc["wt"] = wt[sc["id"]]
# first card of every item scene shows at 0.9 s (nothing is empty for more than ~1 s), later cards follow the voice cues
for sc in S:
    if sc["id"] in ("hook", "recap", "follow"):
        continue
    for L in sc["layers"]:
        if L.get("kind") == "box" and isinstance(L.get("in"), str):
            L["in"] = 0.9
            break

deck = {"_note": "025 long AI news digest 2026-11-05 (landscape 16:9, news-bulletin style)", "format": "landscape", "tag": "AI News", "bg": "#F3F5F9", "bgGrid": False,
        "music": {"file": "shared/music/presentation/Funkorama.mp3", "start": 6, "rel": 13},
        "voice": {"id": "Charon", "style": "Speak like a friendly Indian tech YouTuber chatting casually in Hinglish. Natural conversational pace, warm and clear, a little energetic but not theatrical. No sing-song, no exaggerated emphasis."},
        "scenes": S}
(HERE / "deck.json").write_text(json.dumps(deck, ensure_ascii=False, indent=1), encoding="utf-8")
print("deck.json:", len(S), "scenes; voice chars", sum(len(re.sub(r"\s+", " ", s["voice"])) for s in S), "wt" if wt else "(no wt yet)")
