"""026 LONG (16:9) AI News Digest, second of 2026-11-05. STYLE OF THE DAY 'news bulletin + proof window' (see research/daily/2026-11-05.md):
025's bulletin look (calm light page, ticker, dark lower-third) + real official-page screenshot window with the key sentence in yellow marker on every item,
first card on screen by 0.5 s, recap rows from 0.3 s. Sources read 2026-11-05 (research/news/2026-11-05_digest2.md).
Run: .venv\\Scripts\\python -X utf8 <this file>"""
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
N_ITEMS = 4
IMG = HERE / "img"
S = []


def frame(n, title, org, first):
    lt = (f'<div style="width:1720px;height:150px;background:#14171C;border-radius:28px;display:flex;align-items:center;overflow:hidden;color:#fff;{SHADOW}">'
          f'<div style="width:18px;height:100%;background:#FFD60A;flex:none"></div><div style="font-size:66px;font-weight:800;margin-left:34px;flex:1;white-space:nowrap">{title}</div>'
          f'<div style="background:#FFD60A;color:#111;border-radius:999px;padding:12px 32px;font-size:38px;font-weight:800;margin-right:44px;white-space:nowrap">Source: {org}</div></div>')
    return [box(TICK, 100, 44, PILL),
            box(f'{n} / {N_ITEMS}', 1640, 44, f"background:#FFD60A;border-radius:999px;padding:14px 38px;font-size:34px;font-weight:800;{SHADOW}"),
            box(lt, 100, 880, "", **(pop(0.15, 0.0) if first else {}))]


def pcard(icon, big, small, x, y, w, cue, off=-0.1, bg="#fff", fg="#111", bsize=54, ssize=36, ish=96, k=1.0):
    bsize, ssize, ish = round(bsize * k), round(ssize * k), round(ish * k)
    sub = f'<div style="font-size:{ssize}px;font-weight:700;color:{"#C9CFDA" if bg == "#14171C" else "#444"};margin-top:6px;line-height:1.2">{small}</div>' if small else ""
    h = (f'<div style="display:flex;align-items:center;gap:28px"><i data-ic="{icon}" data-s="{ish}"></i>'
         f'<div><div style="font-size:{bsize}px;font-weight:800;line-height:1.1;color:{fg}">{big}</div>{sub}</div></div>')
    return box(card(h, w, "26px 38px", bg), x, y, "", **pop(cue, off))


def dark(inner, x, y, w, cue, off=-0.2):
    return box(inner, x, y, f"background:#14171C;border-radius:34px;padding:30px 44px;width:{w}px;{SHADOW}", **pop(cue, off))


def proof(name, label, credit, cue, x=900, y=235, w=920):
    """Rounded inset window with a real official-page screenshot (key sentence in yellow marker), label pill above, credit line below."""
    h = round(w * 9 / 16)
    win = (f'<div style="width:{w}px;height:{h}px;border-radius:30px;overflow:hidden;border:2px solid #E3E7EE;{SHADOW};background:#fff">'
           f'<img src="{(IMG / (name + ".png")).as_uri()}" style="width:{w}px;height:{h}px;object-fit:cover;display:block"></div>')
    return [box(win, x, y, "", push=9, **pop(cue, -0.3)),
            box(f'<div style="font-size:30px;font-weight:800">{label}</div>', x, y - 72, f"background:#FFD60A;border-radius:999px;padding:8px 30px;{SHADOW}", **pop(cue, -0.1)),
            box(f'<div style="font-size:26px;font-weight:700;color:#556">{credit}</div>', x, y + h + 14, "", **pop(cue, 0.1))]


def quote(src, text_html, label, credit, cue, x=900, y=235, w=920):
    """OpenAI blocks automated browsers (bot check), so no screenshot is taken: our own quote card of the page sentence, source named."""
    h = round(w * 9 / 16)
    card_html = (f'<div style="width:{w}px;height:{h}px;border-radius:30px;border:2px solid #E3E7EE;background:#fff;{SHADOW};box-sizing:border-box;padding:44px 52px">'
                 f'<div style="font-size:28px;font-weight:700;color:#778;margin-bottom:26px">{src}</div>'
                 f'<div style="font-size:50px;font-weight:700;line-height:1.35;color:#111">{text_html}</div></div>')
    return [box(card_html, x, y, "", **pop(cue, -0.3)),
            box(f'<div style="font-size:30px;font-weight:800">{label}</div>', x, y - 72, f"background:#FFD60A;border-radius:999px;padding:8px 30px;{SHADOW}", **pop(cue, -0.1)),
            box(f'<div style="font-size:26px;font-weight:700;color:#556">{credit}</div>', x, y + h + 14, "", **pop(cue, 0.1))]


MK = '<mark style="background:#FFD60A;color:#111;padding:2px 8px;border-radius:6px">'


def scene(sid, voice, layers):
    S.append(dict(id=sid, type="stage", wipe="fade", voice=voice, layers=layers))


def item(n, org, title, scs):
    for k, (sid, v, layers) in enumerate(scs):
        scene(sid, v, frame(n, title, org, k == 0) + layers)


# ---------- HOOK ----------
V = "सोचो, आपकी बनाई image अब ChatGPT में चलने लगे, यानी GIF बन जाए। आज की चार AI खबरें सीधी भाषा में: ChatGPT का Images 2.6, Mistral का Voxtral 3 voice model, Xcode में GitHub Copilot, और documents से data निकालने वाला एक छोटा model।"
rows = [("sparkle", "Images 2.6", "ChatGPT me GIF", "Images"), ("play", "Voxtral 3", "Mistral ki awaaz", "Voxtral"), ("code", "Copilot in Xcode", "Mac par coding", "Xcode"), ("file", "Field Extractor", "document se data", "documents")]
L = [tx("**4 AI khabrein**", 100, 150, 150, 1000, 0.1), tx("aaj ki, seedhi bhasha me", 100, 330, 70, 1000, "सीधी भाषा|-0.2"),
     box(TICK, 100, 450, PILL, **pop(0.5)),
     box('<div style="font-size:150px;font-weight:800;line-height:1;letter-spacing:2px">GIF</div><div style="font-size:40px;font-weight:700;color:#444;margin-top:8px">image jo chalne lage</div>', 100, 580,
         f"background:#fff;border:2px solid #E3E7EE;border-radius:34px;padding:30px 60px;{SHADOW}", wig="GIF|0.1", **pop(0.4, 0.0)),
     dict(kind="img", img="wave", size=300, x=660, y=640, bob=1, k=[[0.3, {"x": -500, "o": 1}], [1.0, {"x": 660}]])]
for i, (icn, t, sub, cue) in enumerate(rows):
    L.append(pcard(icn, t, sub, 1060, 170 + i * 175, 760, cue, -0.1, bsize=52, ssize=34, ish=84))
scene("hook", V, L)

# ---------- 1 OPENAI IMAGES 2.6 ----------
item(1, "OpenAI", "ChatGPT Images 2.6", [
    ("a1", "पहली खबर: OpenAI ने Images 2.6 launch किया है, ChatGPT, Codex और API में। पेज के हिसाब से images अब पहले से पचास percent तेज़ बनती हैं।",
     [tx("**Images** pehle se **tez**", 100, 170, 96, 780, 0.1),
      pcard("sparkle", "Images 2.6", "ChatGPT, Codex aur API me", 100, 480, 720, "Images 2.6", -0.2, bsize=52),
      box('<div style="font-size:120px;font-weight:800;line-height:1">50%</div><div style="font-size:36px;font-weight:700;color:#444">tez (page ke hisaab se)</div>', 100, 680,
          f"background:#FFD60A;border-radius:34px;padding:20px 50px;{SHADOW}", **pop("पचास", -0.2))]
     + quote("openai.com · Introducing Images 2.6 · Nov 4, 2026", f'{MK}Images 2.6 generates images 50% faster than before.</mark>', "Official page text", "Source: openai.com/index/introducing-images-2-6 (sentence quoted from the page)", 0.4)),
    ("a2", "सबसे मज़ेदार चीज़: GIFs। पेज के हिसाब से आप अपने mascot, character या product की फोटो को एक छोटे loop वाले animation में बदल सकते हो।",
     [tx("**GIF** banao", 100, 170, 112, 1500, 0.1),
      pcard("user", "Mascot ya character", "ko chalao", 100, 420, 560, "mascot", -0.1, bsize=48, ssize=34),
      pcard("box", "Product ki photo", "ko loop me badlo", 100, 640, 560, "product", -0.1, bsize=48, ssize=34),
      ic("arrow", 720, 520, 150, cue="बदल सकते", off=-0.6, drawon=["बदल सकते|-0.6", 0.5]),
      box('<div style="font-size:130px;font-weight:800;line-height:1">GIF</div><div style="font-size:38px;font-weight:700;color:#444">chhota animated loop</div>', 940, 430,
          f"background:#fff;border:2px solid #E3E7EE;border-radius:34px;padding:34px 70px;{SHADOW}", wig="loop|0.0", float=6, **pop("GIFs", 0.0)),
      ic("play", 1560, 470, 180, cue="loop", off=-0.2, pulse=1.0)]),
    ("a3", "ये आज से ChatGPT और Codex में सभी subscription tiers पर मिल रहा है, desktop, mobile और web तीनों पर। Developers के लिए API में दो model हैं, Flare और Sunburst। API का दाम इस पेज पर नहीं, एक अलग link पर है।",
     [tx("**Kahan** milega?", 100, 170, 100, 780, 0.1),
      pcard("check", "Sab subscription tiers", "ChatGPT aur Codex me", 100, 450, 720, "subscription", -0.2, bsize=46, ssize=34),
      pcard("code", "API me do model", "Flare aur Sunburst", 100, 650, 720, "Flare", -0.2, bg="#14171C", fg="#FFD60A", bsize=48, ssize=34)]
     + quote("openai.com · Introducing Images 2.6 · Pricing and availability", f'{MK}available globally today in ChatGPT and Codex across all subscription tiers</mark> on desktop, mobile, and web.', "Official page text", "Source: openai.com/index/introducing-images-2-6 (sentence quoted from the page)", "subscription", ) +
     [box('<div style="font-size:36px;font-weight:800">API daam: page me nahi, alag link par</div>', 900, 830 - 80, PILL, **pop("दाम", -0.2))]),
])

# ---------- 2 MISTRAL VOXTRAL 3 ----------
item(2, "Mistral AI", "Mistral Voxtral 3", [
    ("b1", "दूसरी खबर: Mistral का Voxtral 3, बोलने और सुनने वाले models का नया family। इसमें speech to text, text to speech, और voice agent बनाने का SDK है।",
     [tx("**Voxtral 3**", 100, 170, 120, 780, 0.1), tx("sunna aur bolna", 100, 310, 64, 780, "बोलने और|-0.2"),
      pcard("play", "Speech to text", "bolna sunkar text", 100, 440, 720, "speech to text", -0.1, bsize=48, ssize=34),
      pcard("chat", "Text to speech", "text ko awaaz", 100, 620, 720, "text to speech", -0.1, bsize=48, ssize=34),
      pcard("plug", "Voice agent SDK", "baat karne wala agent", 100, 790 - 0, 720, "SDK", -0.1, bg="#14171C", fg="#FFD60A", bsize=44, ssize=30, ish=72)]
     + proof("voxtral_0", "Official page", "Source: mistral.ai/news/voxtral-3 · 22 Oct 2026", 0.5)),
    ("b2", "बोली को text में बदलने वाला model पचास से ज़्यादा भाषाएँ समझता है, और पेज की language list में Hindi भी है। Mini version का दाम पेज के हिसाब से ज़ीरो पॉइंट ज़ीरो ज़ीरो तीन पाँच dollar प्रति minute है।",
     [tx("**50+** bhashayein", 100, 170, 112, 1500, 0.1),
      pcard("globe", "50 se zyada bhashayein", "list me Hindi bhi hai", 100, 420, 850, "पचास", -0.2, bsize=50, ssize=34),
      box('<div style="font-size:34px;font-weight:700;color:#444">Mini version, page ke hisaab se</div><div style="font-size:120px;font-weight:800;line-height:1.05">$0.0035</div><div style="font-size:40px;font-weight:700;color:#444">per minute</div>', 1030, 400,
          f"background:#fff;border:2px solid #E3E7EE;border-radius:34px;padding:30px 50px;{SHADOW}", **pop("ज़ीरो पॉइंट", -0.2)),
      pcard("user", "Kaun kya bola", "model alag-alag speaker pehchanta hai", 100, 660, 850, "Mini", 0.0, bsize=44, ssize=34)]),
    ("b3", "Text to speech वाला model, Voxtral Mini TTS 3, पैंतीस से ज़्यादा भाषाओं में emotion के साथ बोलता है। आप Mistral के EU-hosted API से चला सकते हो, या अपने infrastructure पर। Whisper से बेहतर होने की बात Mistral का अपना दावा है।",
     [tx("**Emotion** wali awaaz", 100, 170, 100, 780, 0.1),
      pcard("play", "Voxtral Mini TTS 3", "35+ bhashayein", 100, 450, 720, "पैंतीस", -0.2, bsize=48, ssize=34),
      pcard("lock", "EU API ya apna server", "audio kahan jaye, aap tay karo", 100, 650, 720, "infrastructure", -0.6, bg="#14171C", fg="#FFD60A", bsize=42, ssize=32, ish=80)]
     + proof("voxtral_1", "Official page", "Source: mistral.ai/news/voxtral-3 · 22 Oct 2026", 0.5)
     + [box('<div style="font-size:34px;font-weight:800">Whisper se behtar = Mistral ka dava</div>', 900, 830 - 80, PILL, **pop("दावा", -0.5))]),
])

# ---------- 3 GITHUB COPILOT IN XCODE ----------
item(3, "GitHub", "GitHub Copilot in Xcode", [
    ("x1", "तीसरी खबर: GitHub Copilot अब Xcode के अपने built-in coding assistant में चलता है। ये अभी public preview में है, और Xcode 27.3 beta से शुरू होता है।",
     [tx("**Copilot** ab Xcode me", 100, 170, 96, 780, 0.1),
      pcard("code", "Xcode ka coding assistant", "ke andar Copilot", 100, 440, 720, "built-in", -0.4, bsize=44, ssize=34),
      pcard("clock", "Public preview", "Xcode 27.3 beta se", 100, 650, 720, "public preview", -0.1, bg="#FFD60A", bsize=48, ssize=34)]
     + proof("xcode_0", "Official page", "Source: github.blog changelog · 4 Nov 2026", 0.5)),
    ("x2", "इस्तेमाल के लिए Mac पर macOS Tahoe छब्बीस पॉइंट छह या नया चाहिए। Xcode में Settings खोलो, फिर Intelligence, और वहाँ Copilot set up करो।",
     [tx("**3 steps** me set up", 100, 170, 100, 1500, 0.1),
      pcard("desktop", "macOS Tahoe 26.6 ya naya", "Mac chahiye", 100, 420, 800, "macOS", -0.1, bsize=46, ssize=34),
      box(window("terminal", 820, 330, dark=True), 1000, 400, "", **pop("Settings", -0.6)),
      typed("Xcode > Settings > Intelligence", 1040, 520, 38, "Settings|-0.4", w=760, cps=18),
      pcard("check", "Phir Copilot set up", "assistant me", 100, 640, 800, "set up", -0.1, bg="#14171C", fg="#FFD60A", bsize=46, ssize=34)]),
    ("x3", "पेज के हिसाब से सभी Copilot plans supported हैं। पुराना GitHub Copilot for Xcode extension भी अलग option बना रहता है। दाम की बात इस पेज में नहीं लिखी।",
     [tx("**Kaun** use kar sakta?", 100, 170, 100, 780, 0.1),
      pcard("check", "Sab Copilot plans", "page ke hisaab se", 100, 450, 720, "सभी", -0.2, bsize=48, ssize=34),
      pcard("box", "Purana extension bhi", "alag option, chalta rahega", 100, 650, 720, "extension", -0.2, bsize=46, ssize=34)]
     + proof("xcode_1", "Official page", "Source: github.blog changelog · 4 Nov 2026", 0.5)
     + [box('<div style="font-size:34px;font-weight:800">Daam: page me nahi likha</div>', 900, 830 - 80, PILL, **pop("दाम", -0.3))]),
])

# ---------- 4 DHARMA FIELD EXTRACTOR ----------
item(4, "Dharma AI", "Dharma Field Extractor", [
    ("d1", "चौथी खबर: Dharma AI ने Field Extractor बनाया है। सिर्फ दो billion parameters का model, जो document की image से वही fields निकालता है जो आप माँगो।",
     [tx("**Document** se **data**", 100, 170, 100, 780, 0.1),
      pcard("file", "Document ki image", "invoice, ID, form", 100, 450, 720, "document", -0.1, bsize=48, ssize=34),
      pcard("box", "2 billion parameters", "chhota model", 100, 650, 720, "दो billion", -0.2, bg="#FFD60A", bsize=46, ssize=34)]
     + proof("dharma_0", "Official page", "Source: huggingface.co/blog/Dharma-AI · 4 Nov 2026", 0.5)),
    ("d2", "जैसे invoice से supplier, invoice number, due date और total। Output JSON में आता है, field by field। आप schema दे सकते हो, या model खुद ढूँढ ले कि कौन से fields हैं।",
     [tx("**Invoice** se **4 cheezein**", 100, 170, 100, 1500, 0.1),
      box(card('<div style="font-size:40px;font-weight:700;line-height:1.7">supplier<br>invoice number<br>due date<br>total</div>', 520, "26px 40px"), 100, 400, "", **pop("supplier", -0.1)),
      flow([[660, 560], [800, 560]], None, "JSON|-0.6", dur=0.5, sw=9, n=2, per=1.0, r=12),
      box(window("terminal", 900, 400, dark=True), 860, 380, "", **pop("JSON", -0.4)),
      typed('{ "supplier": "...",\n  "total": "..." }', 900, 480, 40, "field by field|-0.2", w=800, cps=18),
      pcard("check", "Schema do ya model khud dhoondhe", "do tareeke", 100, 760 - 40, 800, "schema", -0.1, bg="#14171C", fg="#FFD60A", bsize=40, ssize=30, ish=72)]),
    ("d3", "Dharma का कहना है कि ये उनके test किए frontier models से बेहतर है और सस्ता भी। ये उनका अपना दावा है। इस model का license और download link इस पेज में साफ नहीं लिखा।",
     [tx("**Dava** ya **saboot**?", 100, 170, 100, 780, 0.1),
      pcard("bulb", "Dharma ka dava", "frontier models se behtar, sasta", 100, 450, 720, "कहना", -0.1, bsize=46, ssize=34),
      pcard("magnifier", "License, download link", "page me saaf nahi likha", 100, 650, 720, "license", -0.1, bg="#14171C", fg="#FFD60A", bsize=44, ssize=34)]
     + proof("dharma_1", "Official page", "Source: huggingface.co/blog/Dharma-AI · 4 Nov 2026", 0.5)),
])

# ---------- RECAP ----------
V = "तो आज की चार खबरें: ChatGPT के Images 2.6 में GIFs और तेज़ images। Mistral के Voxtral 3 में सुनने और बोलने वाले models। Xcode में GitHub Copilot, public preview में। और Dharma का Field Extractor, documents से data निकालने के लिए। आज क्या करें: पेज खोलकर तारीख और plan खुद check करो। आपको कौन सी खबर सबसे काम की लगी? Comment में बताओ।"
rows = [("sparkle", "Images 2.6", "GIFs aur tez images", "Images"), ("play", "Voxtral 3", "sunna aur bolna", "Voxtral"),
        ("code", "Copilot in Xcode", "public preview", "Xcode"), ("file", "Field Extractor", "document se data", "Dharma")]
L = [box(TICK, 100, 44, PILL, **pop(0.2, 0.0)), tx("**Aaj ka recap**", 100, 130, 96, 1200, 0.1)]
for i, (icn, a, b, cue) in enumerate(rows):
    L.append(pcard(icn, a, b, 100 if i < 2 else 1000, 300 + (i % 2) * 190, 880, cue, -0.2, bsize=46, ssize=34, ish=80))
L += [box('<div style="font-size:44px;font-weight:800">Aaj karo: page khol kar tarikh aur plan khud check karo</div>', 100, 720, YPILL, **pop("आज क्या", -0.1)),
      box('<div style="font-size:44px;font-weight:800">Kaun si khabar sabse kaam ki? Comment karo</div>', 100, 820 - 0, PILL, **pop("आपको कौन", -0.1)),
      dict(kind="img", img="think", size=330, x=1480, y=640, bob=1, k=[[0.2, {"o": 0}], [0.5, {"o": 1}]])]
scene("recap", V, L)

# ---------- SOURCES AND LICENCES ----------
V = "सारे sources और licence की जानकारी description में दी है।"
src = ["OpenAI: openai.com/index/introducing-images-2-6", "Mistral: mistral.ai/news/voxtral-3", "GitHub: github.blog/changelog (Copilot in Xcode)", "Hugging Face: Dharma Field Extractor blog"]
sl = "".join(f'<div style="font-size:38px;font-weight:700;margin:12px 0">{s}</div>' for s in src)
L = [tx("**SOURCES & LICENCES**", 100, 130, 96, 1700, 0.1),
     box(card(sl + '<div style="font-size:32px;font-weight:700;color:#556;margin-top:22px">Screenshots: short crops of each company\'s own page, key line marked, source named.<br>OpenAI: sentence quoted as text (page blocks automated screenshots).<br>Music: Funkorama, Kevin MacLeod (incompetech.com), CC BY 4.0.</div>', 1500, "34px 48px"), 100, 300, "", **pop(0.3, 0.0)),
     box('<div style="font-size:34px;font-weight:800">Unofficial channel, not affiliated with these companies.</div>', 100, 770, YPILL, **pop(1.0, 0.0))]
scene("src", V, L)

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
# first card of every item scene shows by 0.5 s (nothing empty for more than ~0.5 s); later cards follow the voice cues
for sc in S:
    if sc["id"] in ("hook", "recap", "follow", "src"):
        continue
    for L in sc["layers"]:
        if L.get("kind") == "box" and isinstance(L.get("in"), str) and "pcard" not in L:
            L["in"] = 0.5
            break

deck = {"_note": "026 long AI news digest 2026-11-05 (landscape 16:9, news bulletin + proof window)", "format": "landscape", "tag": "AI News", "bg": "#F3F5F9", "bgGrid": False,
        "music": {"file": "shared/music/presentation/Funkorama.mp3", "start": 6, "rel": 13},
        "voice": {"id": "Charon", "style": "Speak like a friendly Indian tech YouTuber chatting casually in Hinglish. Natural conversational pace, warm and clear, a little energetic but not theatrical. No sing-song, no exaggerated emphasis."},
        "scenes": S}
(HERE / "deck.json").write_text(json.dumps(deck, ensure_ascii=False, indent=1), encoding="utf-8")
print("deck.json:", len(S), "scenes; voice chars", sum(len(re.sub(r"\s+", " ", s["voice"])) for s in S), "wt" if wt else "(no wt yet)")
