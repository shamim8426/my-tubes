# 009 Al-Kafirun: Munshi SCRIPT review R1 (SURAH CHECK), 2026-11-18

VERDICT: **FIX** (all fixes free except re-TTS of about 12 changed lines, roughly ₹1.5, free key first). 0 copyright doubt, no STOP condition.
Checked against: noor RULES 1, 1a, 1c, 1d, 2, 2a, 2e, 2f, 2g/2h, 2i, 2j, 2k, 2l, 2m, 2n, 3; shared RULES 10, 11, 12a; learnings.md LAGU KARO.

## What I opened and measured
- make_script.py, script.json (44 lines, 509 words, voice Charon, tempo 1.0, one track River_Flute, in the register at line 147, CC BY 4.0).
- research/dossier.md, sources.json, ucharan.md. Raw Tanzil v1.1 file `.claude/worktrees/hi-30f55e/.../quran-uthmani.txt` lines 109|1-6.
- **Arabic:** script `ar` == sources.json `ayat[].text` 6/6, sha256 6/6 equal, == raw Tanzil file 6/6 (109:1 = the file line minus the 39-char Bismillah prefix). 109:3 == 109:5 bytes. 109:4 uses U+06E0 (Tanzil v1.1), not the U+06ED of the old alquran.cloud build. NFC was NOT applied (5/6 strings are non-NFC, as in the source). OK.
- **Ucharan:** spoken text of 6/6 ayah lines == the ucharan.md Devanagari column; lines 20 and 25 (ayah 3/5) are identical. OK. (Note: the ucharan.md *Arabic* column is still Khoji's NFC copy and does not byte-match sources.json. Doc-only MINOR: paste the sources.json bytes there.)
- **Length:** 32/44 lines of TTS were already made during the review: measured 359 words / 155.8 s = **2.30 w/s**. Estimate with 0.45 s padding per line = **~4:01**. That sits right on the RULES 2n floor (4:00–5:00, ~550–700 words), so any trim drops it under. The fixes below add about 45 sourced words, which brings it to **~4:20**.
- First ayah starts at ~61 s (L1–L11 measured). learnings LAGU KARO target is 30–40 s, so this is a MINOR. RULES 1 order (parichay + shan-e-nuzul first) explains it.
- 10 scene images viewed in full, with heads zoomed (review/zoom_*.jpg). Proposed people-free crops are in review/script_crops.jpg.
- I could not open sunnah.com or the tafseer pages (no web tool in this run). The hadith numbers Muslim 726 and 1218a, Abu Dawud 5055, Tirmidhi 3403 and Bukhari 2620 agree with the dossier mirror and the standard sunnah.com numbering. The PC check from the dossier is still open.

## Shan-e-nuzul / fact lines (each its own line)
| Line | Claim | Dossier | Grade | Status |
|---|---|---|---|---|
| L1–L2 | 6 ayat, name = "inkaar karne wale" | P1 (Tanzil, Qurtubi, Ibn 'Ashur, Tafheem) | maana hua | OK |
| L3 | 109th surah; "zyadatar ulama: Makka me" | P1, P2 (Qurtubi, Ibn 'Ashur, Tafheem, quran.com) | ikhtilaaf | **MAJOR: the other view (Madani: Ibn al-Zubayr, one view of Ibn 'Abbas) is missing; RULES 1 requires it** |
| L4 | al-Muqashqisha = "shirk se paak karne wali" | P4 (Qurtubi, Ibn 'Ashur) | maana hua | OK |
| L5 | main message | P5 | maana hua | OK |
| L6 | Makka me log buton ki pooja karte the | N1/U2 (Ibn Kathir: buton) | maana hua | OK |
| L7 | "kuch log buton ko chhodkar ek Allah ki taraf aane lage the" | **not in dossier** | none | **MAJOR (unsourced halaat claim)** |
| L8–L11 | Quraysh sardar wanted a "beech ka raasta", "kuch tum hamari, kuch hum tumhari", "kai baar", surah = aakhri jawab | N1 (Tabari, Ibn 'Ashur, Ma'ariful, Tafheem, Qurtubi) | maana hua | OK. N3/C1–C5 absent (no "ek saal", no names, no wealth/marriage offer) |
| L14 | "Qul" = faisla Allah ki taraf se | K1 (Tabari, Ibn 'Ashur, Tafheem) | maana hua | OK in substance; 2i word-gloss form (MINOR) |
| L15 | khitaab = us waqt ka khaas giroh | N2 (Tabari, Qurtubi/al-Mawardi) | maana hua | OK (word choice MINOR) |
| L26–L29 | dohraav: zor / aaj+aage / kiski+kaise | K2 a,b,c (Qurtubi, Tabari, Ibn Kathir, Ma'ariful) | ikhtilaaf (3 views, told as "kuch kehte hain") | OK |
| L32–L34 | ayah 6 ≠ "sab raaste ek"; alagaav in ibadat, not in bartaav | K3 + K4 | maana hua | OK (not "all religions same") |
| L35 | 60:8 | K4 (Quran 60:8, Ibn Kathir) | maana hua | **MAJOR: not faithful. The ayah says "Allah does not FORBID you" kindness and justice toward those who did not FIGHT you over DEEN and did not DRIVE YOU from your homes. The script makes it an order ("करो") and drops both conditions** |
| L36 | Bukhari 2620 | K4 | sahih | substance OK; MINOR: in the hadith she asked and he said "haan" (yes); 25 words, so split |
| L37–L39 | Fajr sunnat + tawaf 2 rak'at | Z1 Muslim 726, Z2 Muslim 1218a | sahih | MINOR: Muslim 726 says "qara'a" (he recited), not a habit "पढ़ा करते थे" (the habitual wording leans on Z4, whose grade is disputed) |
| L40–L41 | before sleep, "shirk se bari hone ka elaan" | Z3 Abu Dawud 5055, Tirmidhi 3403 | sahih/hasan | OK; MINOR: name the source |
| L42–L44 | summary | P5, K5 | maana hua | OK (3 lines, no lesson/teaser) |
Absent, as required: C6/C7 (1/4, 1/3 Quran), Z4 Maghrib, C8–C14, sardaron ke naam. Format: one narrator, 0 questions, no tilawat disclaimer, no next-video teaser, no "seekh" line. "Kafir" is only glossed as "inkaar karne wale" and tied to that giroh (N2). Bhaavarth U1–U6 match all 3 translations in meaning. U1 and U6 are near-identical to Farooq Khan / Suhel Farooq Khan, but a 4–6 word literal ayah leaves no other faithful wording, so this is a Note, not MAJOR.

## Exact script fixes (make_script.py; L = current n)
1. **L3 (MAJOR):** "ये क़ुरआन की एक सौ नौवीं सूरह है। ज़्यादातर उलमा के मुताबिक़ ये मक्का में उतरी, और कुछ उलमा से इसके मदीना में उतरने की राय भी नक़्ल है।" (P2)
2. **L7 (MAJOR):** "और क़ुरैश के सरदार अपने बुतों को छोड़ने को तैयार नहीं थे।" (N2)
3. **L35 (MAJOR), split into 2 lines:** "क़ुरआन की सूरह मुम्तहिना में है: जो लोग दीन की वजह से तुमसे नहीं लड़े," / "और जिन्होंने तुम्हें घरों से नहीं निकाला, अल्लाह तुम्हें उनके साथ भलाई और इंसाफ़ करने से नहीं रोकता।" (gold "भलाई और इंसाफ़")
4. L14 (MINOR, 2i no word-gloss): "ये जवाब अल्लाह के हुक्म से दिया गया, अपनी तरफ़ से नहीं।"
5. L15 (MINOR, tone; "गिरोह" sounds like "gang"): "और ये बात उस वक़्त के उन ख़ास लोगों से कही गई, जो अपनी ज़िद पर अड़े हुए थे।"
6. L18 (MINOR, RULES 12a/3 tone): "वो बुत, जिनके आगे तुम झुकते हो, मैं उनके आगे नहीं झुकता।" (drop "ये पत्थर")
7. L21 (MINOR, 2f): "...उसके साथ किसी को साझी नहीं बनाता।"  L33 (MINOR, 2f): "अक़ीदे" -> "यक़ीन".
8. L36 (MINOR), split: "सहीह बुख़ारी में है, कि एक सहाबिया की माँ, जो मुसलमान नहीं थीं, उनसे मिलने आईं।" / "उन्होंने नबी ﷺ से पूछा, तो आप ﷺ ने कहा: हाँ, अपनी माँ के साथ अच्छा रिश्ता रखो।"
9. L37–L38 (MINOR): "सहीह मुस्लिम में है, कि नबी ﷺ ने फ़ज्र की दो सुन्नत रकअतों में," / "ये सूरह और सूरह इख़लास पढ़ीं।"
10. L40 (MINOR): "अबू दाऊद और तिर्मिज़ी की एक हदीस में है, कि सोने से पहले ये सूरह पढ़ो,"
After the fixes: ~47 lines, ~555 words, ~4:20. Re-TTS only the changed or new lines (free key first). Cached lines stay.

## Images (faceless storybook, RULES 2/2h/2j)
All 10 images: blank white heads (01's right walker has a blank tan face with no features: Note), no text, no domes or minarets, modest dress, dua posture in 06 is hands in front of the chest (OK), no angel or Prophet drawn. The gen.py prompts carry no names. **But 3 line-image pairings make an ordinary figure act as the Prophet ﷺ / a Sahabiya (a "stand-in", RULES 2/2e/2h). These are BLOCKER-level and the fix is free:**
- **B1 L11–L14** (04_light_valley): light coming down onto a figure with open arms while the narration says "ye surah utri… kah do" = Prophet stand-in. Fix: new file `images/04b_light_sky.png` = crop [0,0,880,495] of 04, upscaled to 1920x1080 (no people; verified in review/script_crops.jpg). Use it for L11–L14. L4–L5 may keep 04.
- **B2 L37–L39** (09_dawn_walk): a lone man from behind while the narration says "Nabi ﷺ ne … padhi" = back-view stand-in. Fix: `images/09b_dawn_sky.png` = crop [520,0,1400,495] of 09 (palms and sunrise, no people).
- **B3 L36 (both new lines)** (07_neighbors): two figures while the narration names Nabi ﷺ and a Sahabiya. Dossier: "Sahabiya ka naam aaye to koi image nahi". Fix: `images/01b_rooftops.png` = crop [0,0,960,540] of 01_valley_evening (houses and palms, no people). L34 and both new L35 lines keep 07.
- MAJOR L9 (02_chiefs_offer): "कुछ तुम हमारी मानो…" over two figures gesturing at each other reads as a deal with the Prophet ﷺ. Move L9 to 03_idols_shrine. L8, L10 and L15 may stay on 02 (the council among themselves).
- MINOR (2i: 2–4 images per ayah; ayah 2/3/4 have 1 each): L16 (ayah 2 card) -> 02_chiefs_offer, L19 (ayah 3 card) -> 04b_light_sky, L22 (ayah 4 card) -> 03_idols_shrine.
- MINOR (2g anachronism, as 011 carry-over): 10_stars_valley has modern-looking glass wall lanterns. Use `images/10b_moon_sky.png` = crop [500,0,1460,540] for L30–L31 and L42–L44. 06_family_dua has a glass-chimney lamp and a wall lantern: Note only.
- Note: 03 and 05 idols have carved faces. They are medium/far shots and nothing is destroyed, so OK. Never zoom in on them (dossier section 6).

## Not a STOP
No balance, copyright or channel-ID issue. Arabic licence Tanzil CC BY 3.0 (register row 140 says "2007-2021", the v1.1 file says "2007-2026"; fix this at the metadata step, MINOR). After the fixes, R2 checks only L3, L7, L14, L15, L18, L21, L33, L35–L41 and the new line-image map.
