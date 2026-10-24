# Munshi — script R1 (do awaaz version USTAAD/SAWAAL) — 001 Al-Fatiha — 2026-10-24

VERDICT: FIX (0 BLOCKER, 2 MAJOR, 6 MINOR). STOP condition: koi nahi. Kharcha ₹0.

## Khud jaancha (builder summary par bharosa nahi)
- Arabic: 7/7 ARABIC lines official tanzil.net quran-uthmani (aaj dobara download) se byte-equal; pichhle R2 version se bhi identical.
- BHAAVARTH: 7/7 lines R2 PASS version se shabd-ba-shabd identical (program se).
- 5-shabd overlap (poora spoken text, 65 lines, nukta hata kar) vs al-Umari, hi.farooq, hi.hindi: 0 / 0 / 0. (4-shabd: sirf "अल्लाह के नाम से", "इबादत करते हैं और" — aam vaakyansh, theek.)
- Ginti: 65 lines; USTAAD 711 shabd / 46 lines, SAWAAL 211 / 19, speaker badle 32 -> 497.8 s = 8:18 (script ka hisaab sahi). Sirf line 79 > 25 shabd (28, BHAAVARTH, R2 wali).
- Sources khole: Ibn Kathir 1:1 muqaddama (Makki: Ibn Abbas/Qatadah/Abu al-Aliyah; "no disagreement" 7 aayat; Abu Sa'id bin al-Mu'alla "greatest Surah"), IK 1:4 (us din koi milkiyat ka daava nahi; "Lord of existence incl. this life"), IK 1:5 (Muslim 395 poora matn: hamd / praised / glorified / "between Me and My servant" / "for My servant"; "best method for seeking help: first praising"), MQ 1:4, 1:5, 1:6 (api.quran.com). sunnah.com seedha 403 (pehle jaisa) — hadith matn IK ke andar se mila.
- name_guard: OK (khud chalaya). Music tracks 3/3 licence register me (Incompetech CC BY 4.0).

## Shan-e-nuzul / parichay — har baat alag
| Line | [S#] | Baat | Source | Grade | Munshi |
|---|---|---|---|---|---|
| 4 | S17 | sabse azeem surah | Bukhari 4474; IK muqaddama (khola) | maana hua | OK |
| 6 | S1 | Fatiha = kholne wali | Qurtubi bab 1; IK muqaddama (khola) | maana hua | OK |
| 7 | S12, S10 | pehli surah, 7 aayat, ittifaq | Tanzil quran-data; IK (khola: "no disagreement") | maana hua | OK |
| 8 | S11 | is ginti me Bismillah aayat 1 | IK muqaddama (khola); Qurtubi | ikhtilaaf | OK — dossier ki ijaazat wali ek line |
| 10–12 | S2–S7 | naam | Bukhari 4704, 5007; Muslim 395; IK; Qurtubi | maana hua | OK |
| 14 | S20 | markazi paigham | Tafheem; IK 1:5; MQ 1:6 | maana hua | OK |
| 18 | S15 | khaas waqiye ki mazboot riwayat nahi | IK; Qurtubi (Bayhaqi: munqati'); Wahidi | ikhtilaaf | OK |
| 19 | S15, S9 | zyadatar: Makki, bilkul shuruaati daur | IK 1:1 (khola); Qurtubi bab 2; Wahidi | ikhtilaaf | OK ("ज़्यादातर उलमा") |
| 21 | S9 | doosri raay: Madani | IK; Qurtubi; Wahidi | ikhtilaaf | OK |
| 22 | S9 | teesri raay: do baar | Qurtubi (Tha'labi); IK | ikhtilaaf | OK |
| 23 | S9 | Ibn Kathir: pehli raay zyada munasib | IK (والأول أشبه) | ikhtilaaf | OK |
| 27–28 | S16, S4 | hadith-e-qudsi taqseem | Muslim 395 (IK 1:5 me matn khola) | maana hua | line 28 MAJOR (neeche #1) |
| 45, 51, 59, 69, 85 | S16 | har hisse ka jawab | Muslim 395 (IK 1:5) | maana hua | alfaaz sahi (hamd / thana / majd / bayni-wa-bayna / li-abdi); 45 aur 59 MINOR |
| 89 | S20 | pehle tareef phir maang = sabse behtar tareeqa | IK 1:5 ("best method for seeking help") (khola) | maana hua | OK |

C1–C10 me se kuch nahi; 1:7 me qaum ka naam nahi; maslak/firqa naam nahi; nuzool kram nahi bola.

## Findings
1. MAJOR — line 28 "यानी हर हिस्से पर जवाब आता है": R1 ke purane MAJOR ("हर आयत का जवाब") jaisa phir ho gaya. Muslim 395 me Bismillah (hamari aayat 1) par jawab nahi; "हर" zyada hai, aur "यानी" quote ka matlab nahi. Fix: line 28 = "'और मेरे बंदे को वो मिलेगा जो उसने माँगा।' फिर हदीस बताती है कि फ़ातिहा के हिस्सों पर अल्लाह की तरफ़ से जवाब आता है।"
2. MAJOR — Arabic vs music samay saaf nahi: header (line 23–24) kehta hai "fade-out cue → Arabic akeli", par SCREEN note (line 87–88) "Arabic fade-out cue se ... screen par" — yani fade ke 1 s me Arabic aa sakti hai = music under on-screen ayah (build me BLOCKER). Fix (dono jagah): "Arabic ka pehla frame tabhi, jab music ka 1 s fade poora ho kar chup ho; `[MUSIC back slowly]` tabhi shuru, jab Arabic (chhoti hone wali animation samet) poori tarah screen se hat chuki ho."
3. MINOR — line 57: tightening me M4 ka "मालिक तो वो हमेशा है" hat gaya, jabki SAWAAL (56) ka sawaal yahi hai. Fix: "मालिक तो वो हमेशा है; पर हिसाब और बदले के उस दिन कोई और, किसी चीज़ का नाम-भर का मालिक भी नहीं होगा।" (IK 1:4, MQ 1:4)
4. MINOR — line 44: R2 carry-over fix ka "ख़ूबियों" hat gaya (hamd = khoobiyon ki tareef, M2). Fix: "...इन्हें देने वाले की ख़ूबियों को सराहना... क्या यही हम्द है?"
5. MINOR — line 45 "हदीस में इस पर जवाब है" sawaal ke turant baad lagta hai ki hadith SAWAAL ki misaal ki tasdeeq karti hai. Fix: "हाँ, यही। और इस आयत पर हदीस में अल्लाह का जवाब है: 'मेरे बंदे ने मेरी हम्द की।'"
6. MINOR — line 59 "— यानी मेरी बड़ाई।": quote ke bahar Ustaad "मेरी" bolta hai — Allah ke kalaam me apni vyakhya. Fix: "— 'बुज़ुर्गी' यानी बड़ाई।"
7. MINOR — line 67–68 "तो क्या ये ग़लत है?" / "नहीं, ग़लत नहीं" hukm jaisa sawaal-jawab ban gaya (dossier ka misaal sujhaav "sirf idea, tafseer nahi"; madad wala vishay C10 ke paas). Fix: 67 = "तो इस आयत का इससे क्या रिश्ता है?"; 68 = "आयत दिल के भरोसे की बात करती है — इलाज और दोस्त की मदद अपनी जगह, पर आख़िरी भरोसा और उम्मीद सिर्फ़ अल्लाह पर।" [M5][MISAAL] (MQ 1:5: kisi aur par waisa bharosa nahi jaisa Allah par)
8. MINOR — SOURCES section me music credit nahi (3 Kevin MacLeod CC BY 4.0 tracks; description me credit zaroori, warna metadata stage BLOCKER). Credit lines `shared/assets_license.csv` 141/144/147 se jodo. Ambience SFX files bhi audio stage se pehle register me hon.

Notes (problem nahi): (a) 8:18 me intro music lead, 4 section transitions aur ant ka 3 s fade nahi gine — asli ~8:30–8:40 sambhav; ~8:00 chahiye to line 29 hatao (sabse sasta), line 12 optional. (b) Line 8 me sirf ek ginti — dossier S11 ki ijaazat. (c) Visual notes sahi: koi insaan/Nabi/Sahabi/farishta nahi, Ka'ba nahi, hadith-e-qudsi bina drishya; "roshni ki taraf" prompt me kabhi aakaar/figure na bane. (d) SAWAAL ki 19 lines khud padhi: koi hukm/fazeelat/hadith/tafseer daava nahi (line 67 upar #7).
