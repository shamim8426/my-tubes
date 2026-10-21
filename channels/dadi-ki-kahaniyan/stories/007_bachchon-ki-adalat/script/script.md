# Story 007 — "बच्चों की अदालत" (Long 06) — script v2 APPROVED by the user 2026-10-21 (checkpoint 1)

Status: APPROVED 2026-10-21 with the user's decisions: title 1, thumbnail text "फ़ैसला क्या होगा?", no cozy pal, line 37
removed (36 -> 38 directly), publish by the RULES 8 clock (23 Oct first free day). RULES 15 auto pipeline runs from here.
Chosen from idea_bank ("बच्चों की अदालत v2", offered 2026-10-21) with the user's final note: set on a chhutti ka din /
Ravivaar in Dadi's aangan, NO Bal Diwas mention anywhere; Tara = jaj, Golu = vakil, Tinku = peshkar; the elders'
sazaayein are loving and funny, never humiliating; children respect the elders throughout; the last case is Mitthu's;
Golu sentences himself. Moral: "जो नियम सबके लिए, वही अपने लिए". Publish 23–24 Oct 2026 by the RULES 8 clock.

## HEADER

**Production profile:** shared/RULES.md section 15 (only checkpoint = script approval; no preview; Munshi stage
R1+R2 -> FINAL; final R1 only; upload with publish timing by the RULES 8 clock). Long max 4:00 (target 3:40–4:00),
Short max 40 s (target 35–40 s). Budget ≤ ₹110 actual incl. GST (estimate below). Max 16 new images: this plan uses
**14** (13 scene images + 1 new painted sheet for Sharma ji).

**STYLE:** Kissago Painted (`brand/STYLE_PAINTED.md` section 1 verbatim in every prompt; painted sheet refs only for
the characters in that scene). Painted sheets that exist: Dadi, Golu, Mitthu, Tara, Tinku, Pandey ji
(`characters/pandey/sheet_painted.png`, story 005). **New: Sharma ji painted sheet** (`characters/sharma/sheet_painted.png`,
~₹6, made from `characters/sharma_sheet.png` + bible look; counted in the 14).
- **Light:** one late-October Sunday **morning**, warm golden sun from one side, soft lavender shadows, light dust in
  the air; the whole story runs from early morning (setup) to late morning (last case). No night, no rain.
- **Season:** the gulmohar by the aangan is green, NOT in bloom (it flowers in summer) — no flame-orange flowers.
  Orange accent = a pot of marigold (genda) next to the tulsi and Tara's red ribbons.
- **Cozy pal: NO** (dialogue-heavy comedy; the length budget goes to the four cases; user can ask for one).

**NIYAM (this story):**
- Dadi is in the story -> narration by **NARRATOR (Charon)**. Voices: Golu = Leda (0.95), Tara = Pulcherrima (1.0),
  Tinku = Achernar (1.0), Dadi = Gacrux (0.9), Mitthu = Laomedeia, Pandey ji = Algenib (0.95), Sharma ji = Sadachbia
  (0.95) (scripts/voices.py, channel.json). meta.json `"speed"` always a dict (carry_over 2026-10-20).
- **Pandey ji soft lines 20, 22:** the voices.py Pandey style is "loud, bossy command", which would spoil the whisper joke. At
  production add a NEW style key `pandey_soft` (same voice Algenib, style: "the same pompous Indian police inspector now
  whispering softly, amused, trying not to laugh") and use it only for lines 20 and 22. Do NOT change the existing
  `pandey` / `sharma` style texts (003–005 cache keys). Optional new key `sharma_fond` (Sadachbia, "forgetful, flustered,
  then laughing at himself") for lines 12, 26, 29 — new key only, never edit the old one. meta.json "speed" must list
  "pandey", "pandey_soft", "sharma" (and "sharma_fond" if used) = 0.95 (channel.json has no speed for them).
- **No Bal Diwas / Children's Day** anywhere (script, titles, thumbnail, Short, description, tags). It is just a
  chhutti ka din, a Ravivaar (lines 2, 3, 34, 51). No date is named.
- **Play court, kids' props only:** charpai = jaj ki kursi, a wooden **belan** = hathauda (Tara taps it only on a
  wooden **patla**, never on anyone), the **कटघरा** = one low wooden mudha (stool) inside a small square of bamboo
  sticks tied with string; Tinku's thin notebook = peshkar ka register (no writing visible); a steel plate of
  laddoo. No costumes: every character wears exactly the bible/sheet clothes.
- **Respect (user rule):** the elders come by invitation and join happily, by choice (line 10); the children speak to
  them politely (जी, कृपया, जज साहिबा); no rude line. Every saza is loving and funny: Pandey ji = speak softly till
  evening, Sharma ji = a colourful spectacles cord (a gift), Dadi = two bedtime stories tonight. The elders tease back
  kindly (lines 22, 29, 35, 50). Pandey ji = bible 2b (rob, then softens), laughs at himself, never belittled.
  Sharma ji = forgetful/ghabraaye; the joke is only "the spectacles are on his forehead" — never his head, age or looks
  (image prompts: no focus on his bald head; spectacles pushed up on the forehead only).
- **Mitthu** has no hands: never holds or points; he sits on the charpai rail during the cases and on his own wooden
  perch stand (with a small steel water bowl) near the tulsi; every word twice (4 lines). His perch + bowl are visible
  ONLY in images 1, 10, 11, 12, 13 (images 2–9 show Mitthu on the charpai rail, no bowl) — the Short uses none of 1/10–13.
- **Fair clue (viewer honesty):** line 5–6 plants it: Mitthu calls "पानी! पानी!" and Golu, busy, says "बाद में";
  image 1 shows the dry bowl. Line 27 plants the rule Golu later applies to himself ("भूलना भी एक ग़लती है").
- **Children:** Golu–Tara only friends. Tinku's hunger joke stays light; he stands by his friend (line 46) and ends
  happy with his laddoo fee (line 53) — never put down. Tara = brains and fairness (court rule line 8, the clue line
  39–41, the fair verdicts), not looks. Water: Golu fills the bowl from a brass lota; nothing unsafe to copy.
- **Moral:** "जो नियम सबके लिए, वही अपने लिए" — Golu reaches it himself (lines 45–47), Dadi says it once (line 52).
- **Images text-free:** no writing on the notebook, the patla, any sign or wall.
- **Short = no reveal:** stops at "फ़ैसला सुनाया जाता है..." in the FIRST case (line 18); never shows Mitthu's case, the
  bowl, Golu's self-sentence or the moral.

---

## INTRO (part: intro, ≤ 10 s) — img 6 crop (Tara on the charpai, belan raised) -> img 4 wide (the elders at the court)

1. TARA (belan ko patle par thapak kar, rob se): "ख़ामोश! बच्चों की अदालत शुरू होती है!"
2. NARRATOR: "रविवार की सुबह, दादी का आँगन... और कटघरे में मोहल्ले के बड़े!"

## SHURUAAT — ADALAT SAJTI HAI

3. NARRATOR: "छुट्टी का दिन था। टोली अदालत सजा रही थी।"
4. GOLU (charpai kheenchte hue, josh me): "ये चारपाई, जज की कुर्सी! और ये बेलन... हथौड़ा!"
5. MITTHU (apne adde par, khaali katore ke paas): "पानी! पानी!"
6. GOLU (bina mude, jaldi me): "बाद में, मिट्ठू! अभी अदालत ज़रूरी है!"
7. NARRATOR: "जज तारा, वकील गोलू, पेशकार टिंकू।"
8. TARA (charpai par baith kar, saaf awaaz me): "इस अदालत का पहला नियम... नियम सबके लिए एक। छोटा हो या बड़ा!"
9. TINKU (patli copy pakde, garv se): "और पेशकार की फ़ीस... हर मुक़दमे पर एक लड्डू!"
10. NARRATOR: "न्योते पर बड़े भी हँसते-हँसते आ गए।"
11. PANDEY (moonchh par taav dekar, rob se): "बच्चों की अदालत? क़ानून तो मैं जानता हूँ! मैं ख़ुद देखूँगा!"
12. SHARMA (idhar-udhar dhoondhte hue, chashma maathe par): "मैं भी आ गया, बेटा... पर हाय, मेरा चश्मा! किसी ने देखा?"

## MUQADMA NUMBER EK — PANDEY JI

13. TINKU (khade hokar, zor se): "मुक़दमा नंबर एक! पांडे जी, कृपया कटघरे में आइए!"
14. GOLU (vakil ki tarah tehalte hue): "जज साहिबा, पांडे जी के एक 'ख़बरदार!' से कल छत के सारे कबूतर उड़ गए!"
15. TINKU (toota laddoo upar uthakar): "और मेरा लड्डू भी गिर गया! सबूत नंबर एक... ये टूटा लड्डू!"
16. MITTHU (charpai ki patti par, pankh phadphada kar): "ख़बरदार! ख़बरदार!"
17. PANDEY (pehle rob se, phir jhenp kar): "डरपोक हो सब! ...अच्छा-अच्छा, आवाज़ ज़रा ऊँची है। पर डाँटता दिल से नहीं हूँ।"
18. TARA (belan uthakar, gambhir): "फ़ैसला सुनाया जाता है..."
19. TARA (belan thapak kar): "आज शाम तक पांडे जी हर बात... धीरे बोलेंगे!"
20. PANDEY [voice style pandey_soft] (phusphusa kar, ungli honthon par): "ख़बरदार... जो कोई हँसा!"
21. [SFX ~1.5 s: comedy sting (comedy_sting_731262.mp3, CC0, already in the register) — sab hans padte hain]
22. PANDEY [voice style pandey_soft] (dheere, muskura kar chhedte hue): "वैसे जज साहिबा, आपकी आवाज़ भी कम नहीं!"

## MUQADMA NUMBER DO — SHARMA JI

23. TINKU: "मुक़दमा नंबर दो! शर्मा जी!"
24. GOLU: "जज साहिबा, शर्मा जी रोज़ चश्मा खोते हैं... जबकि चश्मा..."
25. TINKU (apne maathe ki taraf ishara karke, hanste hue): "...उनके माथे पर होता है! आज भी!"
26. SHARMA (maathe ko chhu kar, jhenp kar hanste hue): "अरे! यहीं था? हाय राम... ये तो रोज़ का है!"
27. GOLU (zor dekar): "भूलना भी एक ग़लती है, जज साहिबा! सज़ा मिलनी चाहिए!"
28. TARA (muskura kar): "फ़ैसला! शर्मा जी को टोली की तरफ़ से... चश्मे की एक रंग-बिरंगी डोरी!"
29. SHARMA (dori pehan kar, khush): "ये सज़ा है या इनाम? मंज़ूर!"

## MUQADMA NUMBER TEEN — DADI

30. TINKU: "मुक़दमा नंबर तीन... दादी!"
31. DADI (hairaani ka natak karke, hanste hue): "अरे! मुझ पर भी मुक़दमा?"
32. GOLU: "जज साहिबा, दादी रोज़ कहती हैं, 'बस एक कहानी!' पर हमें तो दस चाहिए!"
33. DADI (muskura kar, haath jod kar): "जुर्म क़बूल है, जज साहिबा।"
34. TARA: "फ़ैसला! आज रविवार है... इसलिए आज रात, दो कहानियाँ!"
35. DADI (chhedte hue): "मंज़ूर! पर दूसरी कहानी तक जज साहिबा जगी रहें... तब ना!"

## AAKHRI MUQADMA

36. MITTHU (apne adde par, zor se, pankh phadphada kar): "पानी! पानी!"
37. *(removed by the user 2026-10-21 — line 36 goes straight to line 38)*
38. GOLU (haath hila kar, bina dekhe): "मिट्ठू, तुम्हारी बारी बाद में!"
39. TARA (uth kar): "रुको! पहले सोचो, फिर दौड़ो। देखो... मिट्ठू का कटोरा।"
40. NARRATOR: "कटोरा सूखा था। सुबह से एक बूँद नहीं।"
41. TARA (dheere): "रोज़ सुबह ये कटोरा कौन भरता है?"
42. NARRATOR: "सबकी नज़र... गोलू पर।"
43. GOLU (dheere, sharminda): "मैं... अदालत सजाने में भूल गया। मिट्ठू ने तो सुबह बोला भी था।"
44. NARRATOR: "गोलू ने तुरंत कटोरा भरा।"
45. GOLU (seedha khade hokar, Tara ke saamne): "जज साहिबा, मुक़दमा नंबर चार... मेरे ख़िलाफ़।"
46. TINKU (dost ke liye): "पर गोलू ने ख़ुद मान लिया... तो सज़ा थोड़ी कम?"
47. GOLU: "नहीं, टिंकू। भूलना भी एक ग़लती है... ये मैंने ही कहा था।"
48. TARA (narm muskaan, belan thapak kar): "फ़ैसला! वकील गोलू, एक हफ़्ता मिट्ठू की पूरी सेवा करेंगे। पानी, दाना, सब!"
49. MITTHU: "सेवा! सेवा!"
50. PANDEY (zor se, phir khud ko rok kar, hanste hue): "शाबाश, वकील साहब! ...अरे, धीरे बोलना था!"

## ANT

51. NARRATOR: "उस रविवार सबको सज़ा मिली... और सबको मुस्कान।"
52. DADI: "याद रखना, जो नियम सबके लिए... वही अपने लिए।"
53. TINKU (laddoo ki thaali ki taraf dekhte hue): "जज साहिबा, अब पेशकार की फ़ीस? चार लड्डू!"
54. DADI: "कमेंट में बताइए — आपके घर में बच्चों की अदालत लगे, तो पहला मुक़दमा किस पर होगा?"

---

## IMAGES PLAN — 13 new scene images + 1 new sheet = 14 of max 16 (+ thumbnail + Short cover = 16 paid images)

Refs = painted sheets of only the characters in that image. All images: late-October Sunday morning, Dadi's aangan
(mud house, clay-tile roof, BROWN wooden door, swept courtyard, tulsi pot + marigold pot, green gulmohar without
flowers, green fields behind). Court layout fixed in every court image: charpai (jaj ki kursi) at the back centre,
the bamboo-stick कटघरा with one low mudha on the RIGHT, a low wooden bench for the waiting elders on the LEFT, a
small wooden patla next to the charpai, a steel plate of laddoo near Tinku. Mitthu's wooden perch stand with a small
steel bowl stands near the tulsi (only in images 1, 10–13).

| Img | What it shows | Refs | Lines |
|---|---|---|---|
| S | **Sharma ji painted sheet** (front, side, 3 expressions: worried, sheepish laugh, happy; prompt says "no text, no labels" — the old sheet carries English labels that must NOT be copied), from the old sheet: ~55, bald head with grey side hair, rectangular spectacles, cream kurta-pyjama, brown sleeveless jacket | old sharma_sheet.png | — |
| 1 | Early morning setup: Golu dragging the charpai across the aangan, Tinku carrying the laddoo plate, Tara placing the belan on the patla; Mitthu on his perch stand, beak open calling, next to his **empty dry steel bowl** (clearly visible); Golu has his back to Mitthu. | golu, tara, tinku, mitthu | 3 (wide), 4 (zoom Golu), 5 (zoom Mitthu + bowl), 6 (zoom Golu) |
| 2 | The court is ready: Tara sitting cross-legged on the charpai with the belan, calm confident face, one finger raised (stating the rule); Golu standing proudly in front; Tinku with a thin notebook (no writing) beside the laddoo plate; Mitthu on the charpai rail. | golu, tara, tinku, mitthu | 7 (wide), 8 (zoom Tara), 9 (zoom Tinku + plate) |
| 3 | Arrival at the brown door: Pandey ji (khaki uniform, thick moustache, lathi) striding in, twirling his moustache, smiling bossily; Sharma ji behind him looking around worried, **spectacles pushed up on his forehead**; the kids greeting them politely, hands joined (Dadi not in this image: 5 refs). | golu, tara, tinku, pandey, sharma | 10 (wide), 11 (zoom Pandey), 12 (zoom Sharma) |
| 4 | Case 1, wide: Pandey ji sitting on the mudha inside the bamboo कटघरा (right), amused; Sharma ji (spectacles on forehead) and Dadi waiting on the bench (left), smiling; Tara on the charpai (centre back); Tinku standing announcing with his notebook; Golu walking like a lawyer, one hand raised; Mitthu on the charpai rail. | dadi, golu, tara, tinku, mitthu, pandey, sharma | 2 (intro shot 2, wide), 13 (zoom Tinku), 14 (2 shots: zoom Golu, then pan to Pandey) |
| 5 | Evidence: Tinku holding up a broken laddoo with a sad comic face; Mitthu flapping his wings on the charpai rail, beak open; Pandey ji in the कटघरा, chest puffed, then (same frame) a sheepish half-smile; Golu pointing at the laddoo. | golu, tinku, mitthu, pandey | 15 (zoom Tinku + laddoo), 16 (zoom Mitthu), 17 (2 shots: zoom Pandey, wider) |
| 6 | Verdict 1: Tara on the charpai, belan raised high over the patla, serious-but-kind judge face (on the LEFT third, clear crop); Pandey ji in the कटघरा whispering with a finger on his lips, eyes twinkling; Golu and Tinku laughing behind their hands. | golu, tara, tinku, pandey | 1 (intro shot 1: crop Tara + belan only), 18 (crop Tara only), 19 (wider), 20 (zoom Pandey), 21 (wide), 22 (zoom Pandey) |
| 7 | Case 2: Sharma ji in the कटघरा looking around anxiously, **spectacles pushed up on his forehead**; Tinku laughing and tapping his OWN forehead to show where; Golu presenting with an open palm; Tara on the charpai smiling; Mitthu on the rail. | golu, tara, tinku, mitthu, sharma | 23 (wide), 24 (zoom Golu), 25 (zoom Tinku), 26 (zoom Sharma), 27 (zoom Golu) |
| 8 | Verdict 2: Sharma ji wearing his spectacles on his eyes now, with a colourful braided cord tied to them, laughing happily; Tara (standing by the charpai) has just given it; Golu and Tinku clapping. | golu, tara, tinku, sharma | 28 (zoom Tara only — the cord is not on yet while she speaks), 29 (2 shots: wide, then zoom Sharma) |
| 9 | Case 3: Dadi sitting on the mudha in the कटघरा with her stick, hand on her cheek in mock surprise, eyes laughing; Golu presenting with both hands spread ("dus kahaniyan"); Tara on the charpai smiling; Tinku with the notebook; Mitthu on the rail. | dadi, golu, tara, tinku, mitthu | 30 (wide), 31 (zoom Dadi), 32 (zoom Golu), 33 (zoom Dadi), 34 (zoom Tara), 35 (zoom Dadi) |
| 10 | Mitthu's call: Mitthu on his perch stand, wings flapping, beak wide open; Tinku looking up from his notebook; Golu waving it off without looking; Tara standing up, looking at Mitthu's dry empty steel bowl (clearly visible on the perch), calm thinking face. No adults in this image (no refs for them). | golu, tara, tinku, mitthu | 36 (zoom Mitthu), 38 (zoom Golu), 39 (2 shots: zoom Tara, then push to the bowl), 41 (zoom Tara) |
| 11 | Close-up: the dry empty steel bowl on Mitthu's perch, Mitthu looking down at it; in the soft background Tara, Tinku and Dadi turning to look at Golu (Pandey ji and Sharma ji NOT in this image); Golu with a sorry, guilty face. | golu, tara, tinku, mitthu, dadi | 40 (close on bowl), 42 (pull out to Golu), 43 (zoom Golu, 2 shots) |
| 12 | Golu kneeling, pouring water from a brass lota into the bowl; Mitthu happily drinking; Tara and Tinku smiling beside. | golu, tara, tinku, mitthu | 44 (2 shots), 49 (zoom Mitthu) |
| 13 | Finale wide: Golu standing straight in front of Tara's charpai, hand on his heart; Tara with the belan, kind smile; Tinku with the laddoo plate; Pandey ji (laughing, hand over his mouth), Sharma ji (cord on spectacles) and Dadi smiling on the bench; Mitthu on his perch, bowl full. Whole group in the LEFT ~55%; right side calm (door, tulsi, fields) for the end screen. | dadi, golu, tara, tinku, mitthu, pandey, sharma | 45 (zoom Golu), 46 (zoom Tinku), 47 (zoom Golu), 48 (2 shots: zoom Tara, wide), 50 (zoom Pandey), 51–54 + end hold (wide/left-group crops only; line 54 ~8.8 s = 2 shots) |

Crops/zooms: every line above uses its image as listed; images 4, 6, 9, 10, 13 carry several lines each. Every shot
≤ 8 s (RULES 13): lines 14, 17, 29, 39, 43, 44, 48, 54 get two shots; after TTS the shot plan re-checks every line > 7 s.
Last 20 s (from ~line 52): only wide/left-group crops of img 13. Seven-character images (4, 13) carry 7 refs (image 3 now 5) —
inside the ~₹6/image average (005 had 5-ref images at that rate); if one comes out with a wrong face, the 1 regen
(BLOCKER only) applies.

---

## SHORT (max 40 s, target 35–40 s) — NO REVEAL (RULES 13)

- Lines: **1, 11, 13, 14, 15, 16, 17, 18** (images 6-crop, 3, 4, 5, 6-crop only; Mitthu appears only on the charpai rail,
  no perch, no bowl). Speed: narrator 1.0, kids 1.05, elders 1.0, gaps 0.15/0.30 (as Short 005/006).
  Est. **~36 s + 2 s end card ≈ 38 s** (long rates 36.1 s raw for these lines; kids 1.05 and elders 1.0 save ~1.5 s; gaps ~1.4 s).
- Story in the Short: Tara opens the court ("ख़ामोश!") -> Pandey ji arrives bossy ("मैं ख़ुद देखूँगा!") -> case number
  one: his "ख़बरदार!" scared the pigeons, Tinku's laddoo evidence, Mitthu repeats it -> Pandey ji: "डरपोक हो सब!...
  पर डाँटता दिल से नहीं हूँ" -> Tara raises the belan: "फ़ैसला सुनाया जाता है..." (cliffhanger, cut before the verdict).
- Never shown or named in the Short, its title, description, tags, first comment or cover: Mitthu's "पानी" case, the
  bowl, Golu's self-sentence, the moral, any verdict (also Pandey ji's whisper), Sharma ji's or Dadi's case.
- First frame: img 6 crop — Tara with the belan raised (strong pose), voice from 0.0 s, no caption in the first 1 s.
- End card (text y ≥ 15%, carry_over): "पांडे जी को क्या सज़ा मिली? पूरी कहानी नीचे दिए लिंक पर".
- Short title idea: "पांडे जी कटघरे में! बच्चों ने लगाई अदालत | किस्सागो" (not the long thumbnail text). Cover text: "ख़ामोश! अदालत!" (cover: Tara with the belan
  raised as hero, Pandey ji in the कटघरा + Golu and Tinku in the lower group at 61–80%, Mitthu small top-right
  below 15%; only characters who appear in the Short).

## 3 TITLE OPTIONS (suffix "| किस्सागो")

1. "बच्चों की अदालत! कटघरे में पांडे जी, शर्मा जी और दादी | किस्सागो"
2. "जब बच्चे बने जज! आख़िरी मुक़दमा किसका निकला? | किस्सागो"
3. "रविवार की अदालत: जज तारा, वकील गोलू और बड़ों पर मुक़दमे | किस्सागो"

**Recommendation: 1** — the hook ("बच्चों की अदालत!") and the funny promise (three elders in the dock) sit in the
first 40 characters; all three are on screen in the court by ~40 s (promise kept in the first 60 s); no keyword block
shared with titles 001–006; no twist named. "बच्चों की अदालत" is the story's name (a court run BY the children), not
"for kids" wording (channel RULES Metadata) — if Munshi or the user reads it as audience wording, option 2 has no such
phrase. Option 2 teases the last case without naming it (no reveal).

## THUMBNAIL (no spoiler: no Mitthu bowl, no Golu in the dock)

Sunday morning, warm light, Dadi's aangan. Focal: Tara on the charpai with the belan raised, confident judge face
(left-centre); Pandey ji in the bamboo कटघरा (right) with big surprised eyes and his moustache, hand on his chest
("मैं?"); Golu beside him pointing like a lawyer; Tinku with the laddoo plate; Mitthu above, wings spread.
Text (yellow, Mukta ExtraBold, black outline, ≥ 12% height): **"फ़ैसला क्या होगा?"** (no title word repeated; not the
"किसका/कौन ...?" shape of 005/006). Corner label "किस्सागो"; bottom-right 15% x 12% empty. Refs: tara, pandey, golu,
tinku, mitthu.

---

## LENGTH ESTIMATE — after the user's cut of line 37 (Tinku, 8 words): **~3:48 (~227.7 s)**, still inside 3:40–4:00; re-measured after TTS.

### Original estimate (measured TTS rates, story 005 cache calibrated to its real 237.4 s build — same base as 006)

Rates (s/word after tempo and trim): narrator 0.424 · Golu 0.385 · Tara 0.412 · Tinku 0.543 · Dadi 0.543 ·
Mitthu ~2.15 s per line. New for 007 (raw cache s/word: Pandey 0.49–0.56 in stories 003–005, Sharma 0.38–0.44 in
003–004; same tempo/trim factor as the narrator/Dadi calibration): **Pandey ~0.47 · Sharma ~0.42**. Gap 0.35 s,
end_hold 7 s (005/006 settings). SFX line 21 ~1.5 s.

| Speaker | Words | Est. s |
|---|---|---|
| Narrator | 60 | ~25.4 |
| Golu | 102 | ~39.3 |
| Tara | 85 | ~35.0 |
| Tinku | 72 | ~39.1 |
| Dadi | 46 | ~25.0 |
| Pandey ji | 45 | ~21.1 |
| Sharma ji | 28 | ~11.8 |
| Mitthu (4 lines) | 8 | ~8.6 |
| SFX line 21 | — | ~1.5 |
| Gaps (53 x 0.35) | — | ~18.6 |
| End hold | — | 7 |
| **Total** | **446** | **~3:52 (232.4 s; Munshi model ~3:48; range ~3:44–3:58)** |

- Intro (lines 1–2) ends ~8.8 s (≤ 10 s); first word ~0.5 s; the hook ("बच्चों की अदालत") is line 1 and the elders in
  the dock (title promise) are on screen from line 2 (img 4).
- The story's question/conflict in the first 30 s: the court and its rule "नियम सबके लिए एक" (line 8, ~25 s), with
  Mitthu's unanswered "पानी! पानी!" planted at ~15 s.
- (R1: Tinku line 37 is a new joke, +5 words.) To reach ~3:50, narrator lines 3, 7, 10, 40, 42, 44 were shortened and Golu's line 24 lost a side clause (no joke cut).
- After TTS: > 3:58 -> end_hold 7 -> 6, then gap 0.33; < 3:40 -> gap 0.45. Never cut dialogue or jokes; narrator first.
- Last 20 s window starts ~212.4 s (line 52 ends ~212.1 s): lines 51–54 + end hold use only wide/left-group crops of
  img 13; line 50 (Pandey zoom) ends ~203 s.
- Short: ~36 s + 2 s end card ≈ 38 s (see SHORT).

## CONTINUITY TABLE

| Check | Value in script | Bible / registry | OK |
|---|---|---|---|
| Dadi (Kamla Devi) age | ~70, no years named | bible ~70 | yes |
| Golu age / relation | ~10, Dadi's pota; Mitthu's water bowl is his daily morning job (line 41–43) | bible ~10, pota | yes |
| Tara age / role | ~9, friend; jaj = brains and fairness | bible 2a ~9 | yes |
| Tinku age / look | ~9, very thin, a little taller than Golu, round glasses, orange-cream stripes | bible 2a | yes |
| Mitthu | Dadi's parrot, no hands, every word twice (4 lines: पानी x2, ख़बरदार, सेवा) | bible | yes |
| Pandey ji | ~45, khaki uniform, thick moustache, lathi; rob then softens, laughs at himself; voice Algenib 0.95 | bible 2/2b, painted sheet 005 | yes |
| Sharma ji | ~55, bald with grey side hair, rectangular spectacles, cream kurta-pyjama, brown jacket; forgetful; voice Sadachbia 0.95 | bible 3, old sheet; painted sheet new | yes |
| Day / time | one Ravivaar morning (chhutti); Dadi's saza "आज रात" = Sunday night | — | yes |
| "X saal pehle" sums | none in this story | — | n/a |
| Names | no new names; no real person/place | bible / registry | yes |
| Places | Dadi's aangan (brown door, mud house, charpai, tulsi); the pigeons were on "छत" (any rooftop, no place named) | bible 5, channel RULES | yes |
| Gulmohar | green, not in bloom in late October | STYLE_PAINTED (accent = marigold pot) | yes |
| Spectacles | on Sharma ji's forehead in images 3, 4, 7 -> on his eyes with the cord in 8 and 13 | — | yes |
| Laddoo | fee "एक लड्डू" per case (9) -> broken laddoo evidence (15) -> four cases = "चार लड्डू" (53) | — | yes |
| Mitthu's bowl | empty from morning (1, 5) -> noticed (39–41) -> filled (44) -> full (13) | — | yes |
| Pakki lines (≤ 2 each) | Pandey "मैं ख़ुद देखूँगा!" 1, "डरपोक हो सब!" 1; Sharma "हाय, मेरा ...!" 1 (+ "हाय राम" 1); Tara "रुको! पहले सोचो, फिर दौड़ो।" 1; Dadi "याद रखना" 1; Tinku/Golu catchphrases 0 | bible 2b | yes |

## NAYAPAN (RULES 12b) — 8/10

- **Not a folk tale.** The known "child judge / child king" tales (a shepherd boy who judges wisely from a mound or a
  throne; clever-courtier and kazi tales; the two-mothers judgment) all turn on a REAL dispute solved by one clever
  trick of the judge. Here there is no dispute and no trick: a pretend play-court in a home courtyard with four comic,
  loving "cases", and the turn is that the prosecutor (vakil Golu) is the one who broke the court's own rule and
  brings the case against himself. The judge only asks one question; the order of events (setup -> 3 comic cases ->
  a clue planted at the start pays off -> self-sentence) is ours.
- **Trope check:** "the accuser is guilty himself" — the new part: nobody exposes him; the clue was planted in the
  first minute (line 5–6), the rule he used on Sharma ji (line 27) is the rule he applies to himself (line 47), and he
  refuses the softer sentence his friend asks for (line 46–47). No magic, no reveal-by-adult.
- **Not the banned shape** (shaq -> pehra/khoj -> chor nikla bechaara/achha): no suspicion, no watch, no search, no thief.
- Trends lists (2026-10-21 and 21b): no court/judge story; nostalgia/journey/station/marbles beats not used. Topic only
  (a children-led mohalla moment).
- Would a child say "I have heard this before"? The kids-court game is familiar from real life (that is the fun); the
  story inside it is new.

## ORIGINALITY vs REGISTRY (RULES 12)

- **Closest: 006 "रंगोली पर नन्हे पंजे"** (toli + Golu owns a mistake). Different in: moral (rules apply to yourself
  vs festival joy includes small creatures), plot shape (episodic play-court with a planted clue vs dawn watch and
  reveal), genre/tone (courtroom comedy vs festival mystery), ending type (self-sentence + elders' loving sazas vs
  rice rangoli for squirrels), lead group (toli + three elders as players vs toli only) = 5 of 6 differ. 006's
  apology is to Tinku for a wrong suspicion; here Golu is not suspecting anyone.
- 003 (rumour comedy with Pandey/Sharma): moral, plot, ending, leads differ. 004, 005: different genre, moral, plot.
- Publish order: 005 (22 Oct, treasure adventure) -> 007 (23–24 Oct, comedy) -> 006 (29–31 Oct, Diwali): no same
  genre or moral twice in a row.

## COST ESTIMATE (actual incl. GST; 005 actual ₹6.07 per 1K image with refs)

| Item | Count | Est. |
|---|---|---|
| Sharma ji painted sheet | 1 | ~₹6.1 |
| Scene images (1K, refs only for the characters in each) | 13 | ~₹78.9 |
| Long thumbnail (painted) | 1 | ~₹6.1 |
| Short cover (painted) | 1 | ~₹6.1 |
| TTS (~54 long lines; Short reuses the cache) | — | ~₹7 |
| **Total** | | **~₹104** (cap ₹110, margin ~₹6) |

Fallback if a BLOCKER regeneration pushes it over ₹110 (RULES 15, no asking): image 12 becomes a crop of image 13
(Mitthu drinking at the full bowl), then image 8 becomes a crop of image 13 (Sharma ji with the cord).

## PUBLISH TIMING (RULES 8, no earliest_date)

Decided right after the upload from the IST clock (`"publish_at": "auto"`): upload finished 19:00–23:59 -> Long
public now, Short +60 min (after 23:59 -> Short public now too); upload finished 00:00–18:59 -> Long 19:00 the same
day, Short 20:00. One long per day: 21 Oct (Long 03) and 22 Oct (Long 04) are taken, so 23 Oct is the first free day.
Upload finished on 23 Oct before 19:00 -> 23 Oct 19:00; on 23 Oct 19:00–23:59 -> public right away on 23 Oct (23 is
free); on 24 Oct -> the same clock on 24 Oct. No `earliest_date`. Metadata: a Sunday play-court comedy; never Bal
Diwas / Children's Day; description and tags never use "बच्चों की कहानी" / "kids story" style wording (channel
RULES Metadata).

## OPEN FOR THE USER (only the user decides)

1. Title: option 1 (recommended) or 2 (if "बच्चों की अदालत" in the title feels like audience wording).
2. Thumbnail text "फ़ैसला क्या होगा?" (alternative: "ख़ामोश! अदालत चालू").
3. Cozy pal: none planned (could be ~10 s after line 44: Mitthu drinking in the morning sun — then narrator lines get
   shorter).
