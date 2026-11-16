# Munshi script review, story 008 (Ghaar-e-Thawr sample), 2026-11-13
VERDICT: FIX (1 BLOCKER, rest MINOR). After the ayah fix it is PASS.

Checked: script.json (10 lines), script/dossier.md, RULES 1d/2, name_guard (OK), Tanzil uthmani 9:40 fetched live and compared codepoint by codepoint.

## BLOCKER
1. ayah_ar bytes differ from Tanzil. Tanzil has shadda BEFORE fatha (U+0651 U+064E) on the nun of "inna" and on lam/ha of "Allaha"; script.json has fatha before shadda (U+064E U+0651). Looks the same on screen but is not Tanzil bytes (RULES: Tanzil bytes only). Words/letters otherwise correct.
   Replace ayah_ar with the exact Tanzil string, built in code: take the 9:40 line from Tanzil txt-2 (https://tanzil.net/pub/download/index.php?quranType=uthmani&outType=txt-2&agree=true) and slice from "لَا تَحْزَنْ" up to (not incl.) " فَأَنزَلَ". Expected codepoints for "inna Allaha": ا-kasra ن-shadda-fatha, ٱ ل ل-shadda-fatha ه-fatha.

## Claim trace
- L1 Thawr, south of Makkah = F9 (direction seerah-reported, ok as stated), cave = F1. "two people" ok.
- L2 first Hijri / ~622 = time section; 100 camels = F8 (Bukhari 3906). OK.
- L3 three nights, honorifics = F4. OK.
- L4 = F4 exactly (Abdullah news, Amir goats' milk). OK.
- L5 searchers came = F2 context; "bilkul qareeb" is a bit stronger than the dossier (exact distance = pata nahi). MINOR: use "gufa ke paas".
- L6 Bukhari 3653 "law anna ahadahum nazara tahta qadamayhi la-absarana": script matches, no added words. OK.
- L7 "ma zannuka ya Aba Bakr bi-ithnayni Allahu thalithuhuma": script matches, no added words. OK. (I could not open sunnah.com myself, same 403 as Khoji; wording agrees with the dossier's Arabic F2.)
- L8 ayah bhaavarth = 9:40, plain, ok (RULES 1a saral).
- L9 = F5/F10, but timing slightly off, see FIX 2.
- L10 seekh: ok, generic, no invented fact.
- No spider, pigeon, tree, snake, no dialogue beyond L6/L7, no figures described. Weak W1-W5 not used.

## FIX / MINOR (exact replacements)
2. L9 (MINOR-to-FIX, accuracy): Bukhari 3905 says the guide arrived at the cave at dawn after the third night. Replace with:
   "तीसरी रात बीतने पर सुबह-सुबह गाइड दो ऊँटनियाँ लेकर गुफ़ा पर आ गया, और मदीने का सफ़र शुरू हुआ।"
3. L5 (MINOR): "फिर एक दिन तलाश करने वाले क़ुरैश गुफ़ा के पास तक आ पहुँचे।"
4. L2 (MINOR, plain Hindi): "इनको" -> "इन्हें": "क़ुरैश ने इन्हें पकड़ने पर सौ ऊँटों का इनाम रखा था।"
5. L6 (MINOR, honorific): "सही बुख़ारी में आता है कि अबू बक्र रज़ियल्लाहु अन्हु ने कहा, अगर इनमें से कोई अपने पैरों की तरफ़ नीचे देख ले, तो हमें देख लेगा।" (the second mention may stay short in L4.)
6. L8 (MINOR, flow): the ayah is Quran's own report of the cave, not necessarily the same minute as L7. Prefix the bhaavarth with "क़ुरआन में इसी गुफ़ा का ज़िक्र है:" or show ayah_src only; do not imply L7 and L8 are one sentence.
7. title (MINOR): drop "(SAMPLE 1 min)" before any upload; "तीसरा अल्लाह था" can sound odd to a new listener, suggest "ग़ार-ए-सौर: ग़म न करो, अल्लाह हमारे साथ है".

## Hindi and nuqta
Good: ग़ार, गुफ़ा, ख़बरें, ताज़ा, क़रीब, क़ुरैश, वक़्त, ग़ुलाम, वाक़िये, फ़रमाया. Plain spoken, short sentences. "गुमान" is the hadith's word, fine.

## Duration
182 words -> about 84 s at 130 wpm (before tempo). If the sample must be ~60 s, cut L4 and L10 (about 40 words) or accept ~85 s; Noor Short minimum is 60 s so 84 s is allowed.

## STOP conditions
None (no copyright doubt, no balance issue, no channel mismatch).
