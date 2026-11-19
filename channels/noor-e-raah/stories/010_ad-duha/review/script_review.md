# 010 Ad-Duha: Munshi SCRIPT review R1 (SURAH CHECK), 2026-11-19

VERDICT: **FIX**. All fixes are free: TTS has not been made yet (audio/ has only _test), and the image fix uses an existing crop from 009. No copyright doubt, no STOP condition.
Checked against: noor RULES 1, 1a, 1c, 1d, 2, 2a, 2e, 2f, 2h, 2i, 2j, 2k, 2l, 2m, 2n and 3; shared RULES 11 and 12a; learnings.md LAGU KARO. I used the same checklist as 009.

## What I opened and measured
- make_script.py (source of truth) and script.json: 56 lines, 587 words, voice Charon, tempo 1.0. One track (Soaring), which is in the licence register at row 141 (CC BY 4.0) and in the 2j set.
- research/dossier.md (P1-P5, N1-N7, U1-U11, K1-K13, Z1-Z2, C1-C18), sources.json, tanzil_93.json, ucharan.md, and the raw Tanzil v1.1 file research/quran-uthmani.txt (lines 6080-6090).
- **Arabic:** for 11/11 ayah lines, the script `ar` is identical to tanzil_93.json, to sources.json `ayat[].text` and to the raw file. For 93:1 that means the file line minus its 39-character Bismillah prefix. sha256 matches sources.json for 11/11. The strings are NOT NFC (they keep the source bytes), which is OK.
- **Ucharan:** for 11/11, the spoken text (ignoring the trailing "।") is identical to the Devanagari column of ucharan.md. 93:7 and 93:8 both start with "व वजदका". Doc-only Note: the Arabic column of ucharan.md does not byte-match the Tanzil bytes (Khoji's copy; same as 009). Paste in the tanzil_93.json bytes.
- **Format:** one narrator. 0 "?" in the script. No disclaimer, no tilawat/qari line, no next-video teaser, no "seekh" line. The summary is 3 lines (L54-L56). "गुमराह"/"भटक" never appears.
- **Length:** 009 had 535 words and came to 4:29. 014 had 692 words at tempo 1.02 and came to 4:57. At those rates, 587 words over 56 lines with 11 ayah cards comes to about **4:20-4:55**, which is inside 4:00-5:00. Measure after TTS. If it goes over 5:00, drop L16 first, then L21.
- **First ayah:** L12, which comes at about 55-60 s. The LAGU KARO target is 30-40 s, so this is a MINOR. The RULES 1 order (parichay + halaat first) explains it, same as in 009.
- **Images:** I looked at all 15 images (review/script_sheet1-4.jpg) and zoomed in on every head (review/script_zoom_heads.jpg). Every head is blank with no features, the dress is modest, there is no text, no dome or minaret, and no angel or Nabi figure. 009's people-free crop is shown in review/script_alt_04b.jpg.
- I could not open sunnah.com or the tafseer pages (no web tool in this run). These hadith numbers agree with the dossier and with standard sunnah.com numbering: Bukhari 4950/4951/4983/1125/5304/6446, Muslim 1797/202, Abu Dawud 4811. The PC check from the dossier is still open.

## Shan-e-nuzul / fact lines (one line per claim)
| Line | Claim | Dossier | Source(s) | Grade | Status |
|---|---|---|---|---|---|
| L1 | "कुछ रातें ... कोई पैग़ाम नहीं आया" | N1, N5 | Bukhari 4950, 4983; Muslim 1797b | sahih ("कुछ रातें", no day count) | OK |
| L2 | revealed as consolation | P5 | quran.com 93; Tafheem intro; Ibn 'Ashur | maana hua | OK |
| L3 | 93rd surah, 11 ayat | P1 | Tanzil metadata; Qurtubi; Ibn 'Ashur; quran.com | maana hua | OK |
| L4 | Makki, early nubuwwat | P2 | Qurtubi (ijma'); Ibn 'Ashur; quran.com; Tafheem | maana hua (no ikhtilaaf, so no second view is needed) | OK |
| L5 | duha = light of the risen day | P1, K1 | Ibn Kathir; Qurtubi; Ibn 'Ashur; Tafheem | maana hua | OK |
| L6-L7 | Bukhari + Muslim: he ﷺ was ill and did not get up for night prayer for 2-3 nights | N1 | Bukhari 4950, 4983; Muslim 1797b | sahih | OK. "दो-तीन रात" is the wording of the sahih matn itself, not a C7 count of how long the pause lasted |
| L8 | in those days no wahy for some nights | N2, N5 | Muslim 1797a; Bukhari 1125 | sahih | OK. Not called fatrat al-wahy (N6) |
| L9 | "एक औरत" taunted "छोड़ दिया गया" | N1, N4 | Bukhari 4950/1125 | sahih; the name is ikhtilaaf | OK: no name (C5/C6 absent) |
| L10 | the mushriks of Makka said the same | N2 | Muslim 1797a | sahih | OK (word: MINOR 2f) |
| L11 | the surah came in reply | N1 | Bukhari 4950 | sahih | OK |
| L17-L18 | day->night is not displeasure, nor is the pause | K3 | Tafheem; Ibn 'Ashur | maana hua (2 tafseer) | OK (word "मुफ़स्सिरीन": MINOR) |
| L21 | "जब से तुमसे मुहब्बत की ... नाराज़ नहीं" | K4 | Qurtubi 93:3 | maana hua, labelled "एक तफ़्सीर" | OK |
| L24 | aakhirat is better + every coming phase is better | K5 a+b | Ibn Kathir; Ma'ariful; Qurtubi; Tafheem | ikhtilaaf (2 views, both given) | OK |
| L27 | success of deen; shafa'at; Hauz-e-Kausar | K6 | Ibn Kathir; Qurtubi; Tafheem | maana hua | OK (C12 "lakh mahal" absent) |
| L28-L29 | "मेरी उम्मत" ... "राज़ी करेंगे, रंजीदा नहीं" | K6 | Sahih Muslim 202 | sahih | OK, faithful (word "रंजीदा": MINOR) |
| L32-L33 | father before birth, mother at 6, grandfather at 8, Abu Talib | K7 | Ibn Kathir; Tafheem; Ma'ariful | maana hua | OK |
| L35-L37 | ayah 7 = unaware of the details of the path; wahy showed the way (42:52) | U7, K8 | Ibn Kathir; Ma'ariful; Qurtubi; Tafheem; Tabari | maana hua | OK: never "gumraah" (C10/C18 absent) |
| L40 | barakah through trade with Khadija RA (voice only) | K9 | Ma'ariful; Tafheem; Ibn Kathir | maana hua | OK (no image of her) |
| L41 | real wealth is wealth of the heart | K9 | Bukhari 6446 | sahih | OK (word: MINOR) |
| L44 | "मेहरबान बाप जैसे बनो" | K10 | Qatada via Ibn Kathir + Qurtubi | maana hua | OK |
| L45 | the orphan's carer in Jannat, like two fingers | K10 | Bukhari 5304 | sahih | **MAJOR: the quote has no speaker** (see fix 2) |
| L48-L49 | give, or refuse gently; answer questioners gently | K11 a+b | Qurtubi; Ibn Kathir; Ma'ariful; Tafheem | maana hua | OK |
| L52-L53 | speaking of blessings = shukr; "जो लोगों का शुक्रिया ..." | K12 | Abu Dawud 4811; Tirmidhi 1954 | sahih | OK (no book named: MINOR) |
| L55-L56 | summary | P5, K3, K13 | as above | maana hua | OK |

These are absent, as required: C1 (the puppy story), C2-C4, C5/C6 (names), C7 (12/15/25/40 days), C8, C9, C10 ("gumraah"), C11 (takbir), C12-C18, and any fazilat claim.

Bhaavarth U1-U11 match all 3 translations (Suhel Farooq Khan, Muhammad Farooq Khan, Mahmud al-Hasan) in meaning. Ayah 7 follows Suhel + Farooq ("अनजान"), as K8 requires. Two lines are near-copies: U6 (Farooq) and U8 "ग़नी कर दिया" (Suhel). U6 is a Note, because a 4-word ayah leaves no other faithful wording. U8 is a MINOR (fix 7).

## Exact fixes (make_script.py; L = current n)
1. **BLOCKER-level, free (ayat 3-8 must show NO person; same stand-in as 009 B1):** L19 and L20 use `r_04_light_valley`, which shows light falling on a figure with open arms plus 3 more figures, while the narration says "तुम्हारे रब ने न तुम्हें छोड़ा". Fix: copy `stories/009_al-kafirun/images/04b_light_sky.png` to `images/r_04b_light_sky.png` (no people; checked) and set L19 and L20 img = `r_04b_light_sky`. After that, no line uses `r_04_light_valley`.
2. **MAJOR (L45, speaker missing; a narrator "मैं" over a man figure):** replace with
   "सहीह बुख़ारी में है, नबी ﷺ ने बताया: यतीम की परवरिश करने वाला, जन्नत में उनके इतना क़रीब होगा, जैसे हाथ की दो मिली हुई उंगलियाँ।" gold ["दो मिली हुई उंगलियाँ"]. The image stays 11_orphan_care (the man is now clearly the carer).
3. MINOR (2f, as 014 L40), L17: "क़ुरआन समझाने वाले आलिम लिखते हैं: जैसे दिन के बाद रात का आना नाराज़गी नहीं,"
4. MINOR (2f), L29: "तो अल्लाह ने पैग़ाम भेजा: हम तुम्हें तुम्हारी उम्मत के बारे में राज़ी करेंगे, और दुखी नहीं करेंगे।"
5. MINOR (2f), L41: "और सहीह हदीस में है: असली अमीरी माल की ज़्यादती नहीं, दिल की अमीरी है।" gold ["दिल की अमीरी"]
6. MINOR (2f), L10: "और मक्का के बुत पूजने वाले भी यही बात कहने लगे।" gold ["बुत पूजने वाले"]
7. MINOR (1a near-copy + 2f), L39: "और तुम्हें तंगी में पाया, तो ख़ुशहाल कर दिया।" gold ["ख़ुशहाल"]
8. MINOR (name the source, as 009), L53: "अबू दाऊद की हदीस में है: जो लोगों का शुक्रिया अदा नहीं करता, वो अल्लाह का शुक्र भी अदा नहीं करता।"
9. MINOR (2i: 2-4 images per ayah). Ayat 1, 4, 6, 7, 9, 10 and 11 have 1 image each. Give each one a second free crop/rect on its 2nd-3rd line: 08 (lamp in the doorway), 09 (moon + stream), 11 (hands + bread), 12 (bowl of dates), 13 (dastarkhwan). No people may enter the crops for ayat 6-7. 05_dawn_breaks is already used 6 times, so do not add it to more lines.
10. MINOR (taste/ghaib), L27 says "हौज़े कौसर" over 07_blooming_oasis (a pond), which can read as a picture of the Kausar. Move L27 to `r_10b_stars_sky`.
Notes only (2g anachronism, same as 009): glass lanterns in 08_shelter_lamp and 02_still_night, a mango-like tree in 10_full_well, a tiled roof at the right of 13_family_meal. The child's head in 11 is skin-coloured, not white (still featureless). 12's beggar head is tan and blank.

After the fixes: 56 lines, about 590 words, about 4:20-4:55. TTS is not made yet, so all text fixes cost Rs0. R2 checks only L10, L17, L19-L20 img, L27 img, L29, L39, L41, L45, L53 and the added crops.

## Not a STOP
No balance, copyright or channel-ID issue. Arabic is under the Tanzil CC BY 3.0 licence: the register row says "2007-2021" but the v1.1 file says "2007-2026" (fix this at the metadata step, MINOR, carried over from 009).

## R2, 2026-11-19: VERDICT **PASS** (0 BLOCKER, 0 MAJOR)
- I re-read script.json: 56 lines, 602 words. The 11 Arabic ayah lines are still byte-identical to tanzil_93.json. There is no "?" anywhere, and no line uses `r_04_light_valley` any more.
- Fix 1: L19 and L20 use `r_04b_light_sky`, which is byte-identical (cmp) to 009's 04b_light_sky.png. It has no people. OK.
- Fix 2: L45 is exactly the R1 text ("नबी ﷺ ने बताया ... दो मिली हुई उंगलियाँ"), with the image kept as 11_orphan_care. OK.
- Fixes 3-8: L17, L29, L41, L10, L39 and L53 are exactly the R1 texts, and the gold keywords were updated. OK.
- Fix 10: L27 now uses r_10b_stars_sky (no pond under "हौज़े कौसर"). OK.
- Fix 9: the 7 crops are at L13, L24 (not L23, which is fine because it is still ayah 4's 2nd/3rd line), L31, L36, L44, L48 and L52. I opened the actual files: all are 1920x1080 (review/r2_ayat3-7_crops.jpg plus review/crops_sheet.jpg). The crops for ayat 4/6/7 (06_c, 08_c, 09_c) and r_04b have NO person. The figures in 01_c (ayah 1), 11_c, 12_c and 13_c (ayat 9-11) are allowed and their heads are blank. Now every ayah has 2+ views. OK.
- Length: at 602 words my estimate is about 4:25-5:00 (from 009/014 rates). Measure after TTS. If it is over 5:00, drop L16 first, then L21 (no re-TTS needed).
- Carry over (MINOR/notes): first ayah at about 55-60 s; the anachronism notes (glass lanterns, mango-like tree, tiled roof); the ucharan.md Arabic column is not Tanzil bytes (doc only); the register row says "2007-2021" for Tanzil.
- TTS: the 7 changed lines (L10, L17, L29, L39, L41, L45, L53) must be re-made (Charon, free key first). Every other line's audio stays.
