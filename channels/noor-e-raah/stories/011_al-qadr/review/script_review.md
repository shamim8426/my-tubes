# 011 Al-Qadr: Munshi SCRIPT review R1 (SURAH CHECK), 2026-11-20

VERDICT: **FIX**. All fixes are free: TTS has not been made yet (audio/ has only _test), and both image fixes use existing people-free images from this story. No copyright doubt, no STOP condition.
Checked against: noor RULES 1, 1a, 1c, 1d, 2, 2a, 2e, 2f, 2h, 2i, 2j, 2k, 2m, 2n and 3; shared RULES 11 and 12a; learnings.md LAGU KARO. I used the same checklist as 010.

## What I opened and measured
- make_script.py (source of truth) and script.json: 49 lines, 606 words, voice Charon, tempo 1.1. One track (Quietude_Sections_Merged), which is in the licence register at row 144 (CC BY 4.0) and in the 2j set (night/sukoon).
- research/dossier.md (T1-T3, P1-P5, N1-N12, U1-U5, K1-K11, C1-C21, W1-W15), sources.json, tanzil_97.json, ucharan.md, and the raw Tanzil v1.1 file research/quran-uthmani.txt (lines 6126-6130).
- **Arabic:** for 5/5 ayah lines (L7, L14, L17, L22, L28), the script `ar` is identical to tanzil_97.json and to the raw file. For 97:1 that means the file line minus its 4-word Bismillah. sha256 matches tanzil_97.json and sources.json for 5/5. The strings are not NFC (they keep the source bytes), which is OK. sources.json has no ayah text, only the sha256, so there is no second copy that could drift.
- **Ucharan:** for 5/5, the spoken text (ignoring the trailing "।") is identical to the Devanagari column of ucharan.md, and the case endings are kept apart: लैलतिल / लैलतुल / लैलतुल क़द्रि.
- **Hadith check.** sunnah.com would not open here either (schannel SEC_E_UNTRUSTED_ROOT). I used the fawazahmed0 hadith-api mirror (jsdelivr) instead:
  - Bukhari 1901, 2014, 2017, 2023 and 2024 match the script's wording.
  - Muslim 760: the mirror has it as book 6 #209/210, Abu Huraira, with "previous sins forgiven". This confirms "बुख़ारी और मुस्लिम" in L31.
  - Muslim 762 has two versions. In book 6 #213, Ubayy says "its indication is that the sun rises bright on that day without rays". In book 13 #283 it reads "by the sign which the Messenger of Allah ﷺ gave us ... the sun would rise without having any ray in it". So the sign is in Sahih Muslim and comes from the Prophet ﷺ. The mirror numbers hadith within each book, so I could not confirm sunnah.com's 762 sub-letter. The script names no sub-number, so this does not matter.
  - Ibn Majah 3850 is graded sahih by Albani and Fouad, hasan sahih by Arna'ut, and da'if by Zubair Ali Zai.
  - Tirmidhi 3513 is graded sahih by Shakir and Albani, hasan sahih by Bashar, and da'if by Zubair. The "[Karim]" in it is an English bracket only, and the script's dua has no karim (C20 respected).
- **Format:** one narrator. 0 "?" in the script. No disclaimer, no tilawat/qari line, no next-video teaser, no lesson line. The summary is 4 lines (L46-L49).
  - L15 "और तुम क्या जानो, क़द्र की रात कितनी बड़ी है!" is the bhaavarth of 97:2, written as an exclamation. It is the ayah's own rhetorical form (K4), not a question to the viewer. **OK**.
- **Length:** 010 had 602 words over 56 lines with 11 ayah cards, and came to 4:54 at tempo 1.1. 011 has 606 words over 49 lines with 5 ayah cards, so there are fewer pauses. My estimate is about **4:35-4:58**. Measure after TTS. If it goes over 5:00, drop L16 first, then L20.
- **First ayah:** L7 comes after 80 words, at about 37-40 s. That is inside the LAGU KARO 30-40 s target, and there is no background or name line right after the hook.
- **Images:** I looked at the contact sheet review/img_sheet.jpg, all 13 crops (review/script_crops_sheet.jpg) and the full 04, 07 and 15, and zoomed in on every head (review/script_zoom_heads.jpg).
  - Every head is blank with no features. 06 has a white beard shape, but no eyes, nose or mouth.
  - The dress is modest. There is no text, and no dome or minaret: 13 is a flat mud building with a palm-frond shade.
  - There is no angel, Jibreel or Nabi figure.
  - 07 shows standing qiyam from behind, with the hands at the chest and the figure on a mat facing the wall. That is correct.
  - 15 shows the family from behind, sitting, palms up in front of the chest. That is correct.
  - 13 shows the worshippers inside as tiny figures standing in a row with their backs to the viewer. That is correct.
  - **04_sky_light_valley**, the soft light column, has no shape, wings or human outline. It is used on L3, L7-L8 and L47 as a symbol of the Quran coming down. **Acceptable.** It is NOT used on any ayah 4 / Jibreel / angel line: L22-L27 and L48 use 09, 01, 10 and 14, which have no figure and no light-being. Keep it that way.
  - 02_mountain_night has an empty cave in the hill, which reads as Hira from far away (dossier section 6 allows this). It is on L10 ("नबी ﷺ पर उतरता रहा") with no person in it. OK.

## Fact lines (one line per claim)
| Line | Claim | Dossier | Source(s) | Grade | Status |
|---|---|---|---|---|---|
| L1-L2, L19-L20 | 1000 months = 83 years 4 months, more than a whole life | U3, K5 | Qurtubi 97:3; Ma'ariful 97 | maana hua | OK |
| L3, L47 | Allah sent this surah about that night | P5 | Ibn 'Ashur 97:1-2; Ibn Kathir; Ma'ariful | maana hua | OK |
| L4 | 97th surah, 5 short ayat | P1 | Tanzil file; Qurtubi intro; 3 translations | maana hua | OK (P3/P4 not used, correct) |
| L5 | mostly Makki, some say Madani | P2 | Mawardi; Ibn al-Jawzi; Ibn Kathir AR; Qurtubi | ikhtilaaf | Both views given. "ज़्यादातर" is itself disputed: Mawardi says most say Makki, Tha'labi says most say Madani. MINOR, fix 6 |
| L6 | Quran came down in Ramadan, on a blessed night | N2 | Quran 2:185, 44:3; Ibn Kathir; Ma'ariful | maana hua | OK (C10 Sha'ban not used) |
| L8 | "हमने इसे, यानी क़ुरआन को" | U1, K1 | 3 translations; Qurtubi; Ibn 'Ashur | maana hua | OK |
| L9-L10 | Ibn Abbas: whole Quran to the first heaven, then little by little over "कई सालों" | K2a | Ibn Kathir; Tabari; Qurtubi; Mawardi; Ma'ariful | ikhtilaaf, framed "क़ुरआन समझाने वाले आलिम लिखते हैं" | OK (W8: no 20/23) |
| L11 | the descent began on this night | K2b | Sha'bi (Tabari, Qurtubi); Ibn 'Ashur; Ma'ariful | ikhtilaaf (no conflict) | OK, wording as the dossier says |
| L12-L13 | Qadr = honour and decree; both apply | K3 | Qurtubi; Mawardi; Ibn al-Jawzi; Ma'ariful | ikhtilaaf, both given | OK (C16 not used) |
| L15-L16 | 97:2 + this style shows greatness | U2, K4 | translations; Ibn 'Ashur; Qurtubi | maana hua | OK |
| L21 | the worship of this one night beats 1000 months without it | K5 | Tabari; Ibn Kathir; Qurtubi | maana hua, "आलिम लिखते हैं" | OK (W9: no fiqh sum) |
| L23 | 97:4 bhaavarth | U4 | translations | maana hua | OK |
| L24 | Rooh = Jibreel AS, named apart for his honour | K7 | Ibn al-Jawzi; Tabari; Ibn Kathir; Qurtubi; Suhel | maana hua (most) | OK (C14/W11 not used) |
| L25 | angels come down in great numbers, with mercy and barakah | K6 | Ibn Kathir EN; Qurtubi | maana hua | OK, no count (C7/W4 not used) |
| L26-L27 | they bring every matter Allah decided; "साल भर के फ़ैसले, रोज़ी और उम्र" handed to the angels | K8 | Qatada via Tabari; Ibn Abbas via Qurtubi; Ibn Kathir; Ma'ariful | maana hua, framed "आलिम लिखते हैं" | **OK**: 4 tafseer, no named angels (C9), no Sha'ban (C10) |
| L29-L30 | 97:5; all good, no evil, until fajr | U5, K9, K10 | Tabari; Ibn Kathir; Qurtubi | maana hua | OK |
| L31-L32 | standing in this night with faith and hope of reward = past sins forgiven | N6 | Bukhari 1901/2014; Muslim 760 (checked in the mirror) | sahih | OK |
| L33-L34 | last ten; "seek it in the odd nights of the last ten" | N7 | Bukhari 2017 (checked) | sahih | OK |
| L35 | "यानी 21, 23, 25, 27, 29" | N7, N12 | Bukhari 2017; dossier N7 allows these as examples | sahih (arithmetic of "odd nights of the last ten") | **OK**: all five are named, none is called the night (C6/W2/W14 not used) |
| L36-L38 | came out to tell, two men quarrelling, knowledge taken away, "maybe better for you" | N8 | Bukhari 2023 (checked) | sahih | OK, no names (W13). Wording: MINOR, fix 3 |
| L39 | hidden so people try every odd night | K11, N12 | Bukhari 2023; Qurtubi; Ma'ariful | maana hua | OK |
| L40 | last ten: worked hard, stayed up all night, woke the family | N9 | Bukhari 2024 (checked) | sahih | OK. No source named: MINOR, fix 5 |
| L41-L42 | sign: the sun rises without rays | N10 | Muslim 762 (both versions checked in the mirror) | sahih | OK. "हल्का" vs "bright/white": MINOR, fix 4 |
| L43-L45 | dua taught to Aisha RA, Ibn Majah wording | N11 | Ibn Majah 3850; Tirmidhi 3513 (checked, grades as in the dossier) | maana hua (one muhaqqiq da'if) | OK, no "karim" (C20) |
| L46-L49 | summary | P5, K5, K6, K9 | as above | maana hua | OK |

These are absent, as required: C1-C21 and W1-W15. There is no Bani Israel warrior, no Muwatta balagh, no Umayya, no fixed night, no angel count or named angels, no "drunkard not greeted", no Sha'ban, no extra signs, no dates for the scriptures or the first wahy, no fiqh, no maslak remark. No sahih shan-e-nuzul exists (N1), and the script claims none: the circumstances come from Quran 2:185/44:3 only.

Bhaavarth U1-U5 match all 3 translations (Suhel Farooq Khan, Muhammad Farooq Khan, Mahmud al-Hasan) in meaning. None of them is a near-copy: L15 "कितनी बड़ी है" and L29 "पूरी की पूरी सलामती ... फ़ज्र की रौशनी निकलने तक" are our own wording.

## Exact fixes (make_script.py; L = current n)
1. **BLOCKER-risk, free (a line about the Prophet ﷺ over people; stand-in reading):** L34 "नबी ﷺ ने फ़रमाया: इसे आख़िरी दस की ताक़ रातों में तलाश करो।" is on `13_masjid_night_far_c`, where two large men walk to the masjid just as "नबी ﷺ ने फ़रमाया" is heard. Set L34 img = `01_qadr_night_c` (starry sky with roofs, no person; checked). L33 and L35 keep 13 (generic worshippers, no Prophet in the line).
2. **BLOCKER-risk, free (stand-in for the Prophet ﷺ and Aisha RA):** L43 says "हज़रत आइशा को नबी ﷺ ने ... ये दुआ सिखाई:", and the very next line, L44 (the dua), is on `15_family_night_dua`, a husband and wife at home at night. Fix: L44 img = `09_town_lamps_night_c` (lit homes, no person; checked), and L45 img = `15_family_night_dua` (the full frame, where the child is clearly visible, so it reads as an ordinary family saying the dua one line later).
3. MINOR (2f + closer to Bukhari 2023 "the news about it had been taken away"), L37: "दो आदमी आपस में झगड़ रहे थे, और उस रात की पक्की ख़बर उठा ली गई।" gold ["पक्की ख़बर उठा ली गई"]
4. MINOR (closer to Muslim 762 "bright/white, without rays"), L42: "उसकी सुबह सूरज सफ़ेद-सा निकलता है, बिना तेज़ किरणों के।" gold ["बिना तेज़ किरणों"]
5. MINOR (name the source, as 010 fix 8), L40: "सहीह बुख़ारी में है, आख़िरी दस रातें आतीं, तो नबी ﷺ पूरी मेहनत से इबादत में लग जाते, रात भर जागते, और घर वालों को भी जगाते।" The image stays 03_ramadan_lamps_c (no person; correct).
6. MINOR (P2: who the "majority" is, is itself disputed), L5: "मशहूर राय ये है कि ये मक्का में उतरी, और कुछ उलमा इसे मदीना की सूरह मानते हैं।" gold ["मक्का"]

Notes only (2g anachronism and taste, no regeneration):
- Glass wall lanterns in 03, 09 and 14.
- A coat with lapels in 07.
- Palm trees growing inside the room, and a tiled roof outside the window, in 15.
- 06 is a daylight scene inside a night story (fine for "a whole life").
- 32 "जो इस रात ... खड़ा रहे" on 07 (a lone man praying) is fine: the line is about "whoever", not the Prophet ﷺ (same as 010 L45).

After the fixes: 49 lines, about 610 words, about 4:35-5:00. TTS is not made yet, so all fixes cost Rs0. R2 checks only L5, L34 img, L37, L40, L42, L44 img and L45 img.

## Final-stage notes (carry to the final check)
- Music: 014 used Quietude and its bed was only 3.7 dB under the voice. At final, check that the bed is at least 18 dB under speech, as for 010's music_vol 0.12.
- Tanzil register row 140 says "2007-2021" but the v1.1 file says "2007-2026". Fix this at the metadata step (MINOR, carried over from 009/010).

## Not a STOP
No balance, copyright or channel-ID issue. Arabic = Tanzil CC BY 3.0, unchanged bytes. Bhaavarth = our own wording.

## R2 (fix-verify only), 2026-11-20: VERDICT **PASS**
Opened script.json (48 lines, 594 words) and diffed it against review/script_v1.json (the R1 version, 49 lines), field by field.
- All R1 fixes are in. Because old L16 was dropped, every line after it moved up by one, so the new line numbers are used below.
  - L5 has the "मशहूर राय" wording, gold मक्का.
  - L33 img is 01_qadr_night_c.
  - L36 reads "पक्की ख़बर उठा ली गई", and the gold matches.
  - L39 starts with "सहीह बुख़ारी में है".
  - L41 reads "सफ़ेद-सा ... बिना तेज़ किरणों के".
  - L43 img is 09_town_lamps_night_c.
  - L44 img is 15_family_night_dua (full frame).
- Old L16 ("ये बात इस अंदाज़ में...") is dropped. Its K4 explanation was optional, and L15 still carries 97:2. Nothing else changed: the only other differences are the rotating motion presets.
- **Arabic:** the ayah lines are now L7, L14, L16, L21 and L27. For 5/5, `ar` is byte-identical to tanzil_97.json and to v1, and the sha256 values are unchanged. The spoken text is identical to v1 and is found in ucharan.md (5/5).
- **Prophet ﷺ / family lines vs people:** I made a new sheet, review/r2_prophet_lines.jpg, showing 01_c, 09_c, 15, 03_c, 14_c and 02_c.
  - These lines have no person on screen: L10 (02_c), L30 (03), L33 (01_c), L35 (14), L36 (14_c), L37 (01), L39 (03_c), L42 (03) and L43 (09_c).
  - The family image 15 comes 2 lines after "हज़रत आइशा", on the translation of the dua. The child is clearly visible, so it reads as an ordinary family. OK.
  - L31 on 07 is a "whoever" line, as in R1. L34 on 13 is the narrator's list of the odd nights. Both are OK.
- **Audio:** 48 wavs, which sum to 301.8 s (measured). That gives an estimated length of about 4:57, under 5:00.
- Note for the final check (not a fix now): in tts_check.md, Whisper misheard "अल्लाह" in L25 ("रहाने") and L44 ("आईला"), and L41 "सफ़ेद-सा निकलता" ("सवेज साने कलता"). These were accepted by hand. At the final check, spot-listen to L25, L41 and L44. If a word is really dropped, that is a free re-take on the free key.
No STOP condition.
