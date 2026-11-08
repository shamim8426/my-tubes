import re, sys
M = {"ये": "Ye", "है।": "hai.", "वही": "wahi", "रहता": "rehta", "है,": "hai,", "भी": "bhi", "बस": "bas", "जवाब": "jawab", "तेज़": "tez", "आते": "aate", "हैं।": "hain.",
     "में": "mein", "लिखो,": "likho,", "दबाओ,": "dabao,", "फिर": "phir", "स्क्रीन": "screen", "पर": "par", "दिखेगा,": "dikhega,", "और": "aur", "के": "ke", "पास": "paas", "एक": "ek", "छोटा": "chhota", "आइकन।": "icon.",
     "ध्यान": "Dhyan", "रखो!": "rakho!", "सिर्फ": "sirf", "चलता": "chalta", "हर": "har", "का": "ka", "दाम": "daam", "ज़्यादा": "zyada", "से": "se", "कटता": "kat-ta",
     "इसलिए": "Isliye", "की": "ki", "शुरुआत": "shuruaat", "चालू": "chalu", "करो,": "karo,", "खर्चा": "kharcha", "लगे": "lage", "तो": "toh", "बंद": "band", "कर": "kar", "दो।": "do.",
     "को": "ko", "ढाई": "dhai", "गुना": "guna", "तक": "tak", "करना": "karna", "है?": "hai?", "ऐसे": "Aise", "चाहिए?": "chahiye?", "लिखो।": "likho.", "fast।": "fast.", "Follow": "Follow",
     "तेज़ जवाब": "tez jawab", "पहला": "Pehla", "दूसरा": "Doosra", "तीसरा": "Teesra", "टिप": "Tip", "सावधानी": "Careful", "शुरू में": "Shuru mein", "सिर्फ़": "sirf", "महँगा": "mehnga", "कटता": "kat-ta",
     "मॉडल वही Opus": "Model wahi, Opus", "क्वालिटी एक जैसी": "Quality same", "Space दबाओ": "Space dabao", "फिर Enter": "Phir Enter", "पास में ⚡ आइकन": "Paas mein ⚡ icon", "सिर्फ़ Opus पर": "Sirf Opus par",
     "हर token महँगा": "Har token mehnga", "usage credits से कटता है": "Usage credits se kat-ta hai", "session की शुरुआत में ON": "Session ke start mein ON", "खर्चा बढ़े तो OFF": "Kharcha badhe toh OFF"}
dev = re.compile(r'[ऀ-ॿ]')
for fn in sys.argv[1:]:
    s = open(fn, encoding="utf8").read()
    for k in sorted(M, key=len, reverse=True): s = s.replace('"' + k + '"', '"' + M[k] + '"').replace('>' + k + '<', '>' + M[k] + '<')
    s = s.replace("शुरू में <span", "Shuru mein <span").replace("</span> चालू", "</span> chalu")
    open(fn, "w", encoding="utf8").write(s)
    for i, l in enumerate(s.splitlines(), 1):
        if dev.search(l): print(fn, i, l.strip()[:150])
