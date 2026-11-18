# Munshi script R1 — 014 Ashab-e-Kahf (Quran 18:9-26) — 2026-11-19

STEP: script R1 (HISTORY story Long)   PROJECT: noor-e-raah/014_ashab-e-kahf   VERDICT: **FIX** (sab free, Rs0)

## Kya check kiya
- RULES 2e/2f/2g/2i/2j/2k/2l/2n padhe; script.md (52 lines) + make_script.py ke [F#] comments + script.json; dossier F1-F16, W1-W10.
- Arabic: script.json "ar" vs research/quran-uthmani.txt (Tanzil 1.1) Python se byte compare:
  L7 = 18:13 word 5 se (إِنَّهُمْ), L20 = 18:10 word 6 se (رَبَّنَآ), L47 = 18:25 poori — teeno **byte-equal**, ayah ke ant tak.
  Ucharan (Devanagari) teeno sahi baithte hain.
- Images: current images/*.png se nayi contact sheet `review/sheet_munshi_r1.jpg` + zooms (02, 04, 09, 10, 13); _rej* ignore.
- Length: 686 words (661 Hindi + 25 ucharan). Measured TTS lines 1-13 = 185 words / 73.5 s = 2.52 w/s -> ~4:33 voice;
  gaps/ayah cards ke saath ~4:45-4:55. **4:00-5:00 ke andar, koi line drop nahi.** (Final 5:00 se upar jaye to L50-51 hatao.)
- Nigraan LAGU KARO: hook 1-2 + pehli ayah L7 ~35 s par = theek.

## Tathya / W# (FACT + SURAH CHECK)
- Har line apne [F#] ke andar; dossier ke saare fix (L2, L29, L39-41, L44) lag chuke. W1-W10 me se kuch nahi (naam, jagah,
  raqim, masjid/imaarat, tareekh, 309 shamsi/qamari, ginti "saat" pakki, sabab-e-nuzul — sab bahar).
- F12 (tafseer) sirf hedge ke saath (L40). F14 "ye sab andaaze the" sahi jagah (pehli do raay ke baad, Quran ke kram me).
- Shan-e-nuzul: script me koi nahi (W5 chhoda gaya) -> alag S# line ki zaroorat nahi.
- Koi sawaal viewer se nahi (L32 sirf kirdaar ka dialogue), koi lesson/teaser nahi, aakhri line L52 = sirf source line.

## Depiction
- Koi Nabi/farishta nahi. Nau-jawan har jagah faceless + glow; aam log faceless; 09 = khaali landscape (dhoop daayin, gufa chhaaon me). Koi insaani chehra nahi -> OK.
- 07 dua: peeth se, haath uthe, izzat wala posture -> OK.

## FIX list (BLOCKER: koi nahi; sab free, sirf make_script.py me badlav)
1. **L4** img `15_stars_cave` -> `16_dawn_cave` (line "कह्फ़ का मतलब है गुफा" par gufa dikhni chahiye; 15 me gufa hai hi nahi). Text same, TTS dobara nahi.
2. **L43, L44, L45** img `15_stars_cave` -> `14_people_cave` (logon ki ginti par behas = log dikhne chahiye). L46 `15_stars_cave` hi rahe. Text same.
3. **L18** img `10_dog_entrance` -> `05_leave_town` (05 me kutta nau-jawanon ke saath chal raha hai = "उनके साथ उनका एक कुत्ता भी था"). Text same.
4. **L38** img `05_leave_town` -> `04_youths_stand` (pathar maarne ka darr = shehar ke log saamne; 05 me sirf shehar chhodna). Text same.
5. **L40** (2f, bhaari shabd "मुफ़स्सिरीन") ->
   "क़ुरआन समझाने वाले पुराने आलिम लिखते हैं, कि वहाँ सब बदल चुका था, और उसके बहुत पुराने सिक्के देखकर लोग हैरान रह गए।"
6. **L49** (2f, MINOR) ->
   "और साथ ही फ़रमाया: अल्लाह ही ख़ूब जानता है, कि वो कितना रहे। आसमानों और ज़मीन की हर छिपी बात, बस वही जानता है।"
7. **L46** (MINOR, 18:22 me "क़ुल" = kaho; "मेरा रब" Quran ka bolna nahi) ->
   "क़ुरआन में आया है: कहो, मेरा रब ही उनकी गिनती सबसे अच्छी तरह जानता है। उन्हें बहुत थोड़े लोग ही जानते हैं।"
Note: text fix sirf L40, L46, L49 (TTS abhi sirf 1-13 bani) -> koi paid re-TTS nahi. Fix 1-4 sirf img field.

## MINOR (carry_over, regen nahi)
- 02_town_idols: log idol ke aage jhuke (dossier visual note "idols door dhundhle, worship close-up nahi" se zyada saaf); idol ke paas naarangi aakriti = doosri moorti (chehra pathar ka). Line 5/12/13 se match karti hai; push_in mat lagao (pan theek).
- 08_sleep_cave me 5 sone wale, baaki images me 4 nau-jawan (continuity). Script ginti tay nahi karti, isliye chalega.
- 10_dog_entrance: kutte ke agle pairon par kaale "dastaane" jaise patte (style leak). Cosmetic.
- 13_market: baayin stall ke kapde par laal nakli-likhawat (2j "no text"); motion/crop se baayin kinara kam dikhao.
- L13 "दलील" -> "सबूत" behtar hota, par TTS ban chuki; chhodo.
- Process: TTS lines 1-13 script R1 se pehle shuru hui (10 lines paid key par, 429 free). STOP condition nahi.

## STOP condition (RULES 14/15)
Koi nahi: balance floor / copyright shak / channel ID mismatch me se kuch nahi. Tanzil Arabic attribution ke saath, Hindi = apna bhaavarth.

Agla kadam: builder fix 1-7 make_script.py me lagaye (Rs0), script.json dobara banaye, phir TTS jaari; Munshi R2 me sirf L4/18/38/40/43-46/49 dekhega.
