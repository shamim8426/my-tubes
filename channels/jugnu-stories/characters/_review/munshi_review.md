# Munshi review — Golu ki toli: Tara + Tinku (R1, 2026-10-20)

STEP: new permanent characters (sheets + voices)   VERDICT: FIX (MINOR only, sab free; sheets PASS, koi regen nahi)
STOP condition: nahi (balance ₹285.52 > ₹50, copyright doubt nahi, channel ID ka sawaal nahi). Kharcha: new_characters ₹11.83 of ₹20 (9 paid calls).

## Kya check kiya
- Padha: channel_bible.md 2a (DRAFT), shared/RULES.md 11/12a/15, channels/jugnu-stories/RULES.md, brand/STYLE_PAINTED.md, scripts/gen_painted.py (TOLI prompts), scripts/voices.py, channel.json (git diff).
- Dekha: tara/sheet_painted.png, tinku/sheet_painted.png, golu/sheet_painted.png (sab 1264x848), _review/toli_group.png (1884x615).
- name_guard: gen_painted.py, channel_bible.md, voices.py, channel.json -> sab "OK".
- Audio (tools/ffmpeg): duration, EBU R128, astats (flat factor/clipping), Whisper small (hi), autocorrelation F0.

## 1. Sheets vs bible
- Tara: do lambi chotiyan + laal ribbon, khuli muskaan, peeli frock, chappal, notebook + pencil — sab hai. Front, side, 3/4 (notebook pose) + 4 expressions (happy, surprised, scared, thinking). Aankhein badi/bright theek. Note: "thinking" face thoda worried lagta hai.
- Tinku: bade gol chashme, bikhre baal, dheeli dhaaridaar (orange-cream) shirt, blue half-pant, sandal; front, side, hungry/sheepish pose + 4 expressions. Golu ke saath world/proportion/paper/line style same.
- MINOR m3: Tinku "bahut dubla-patla" kam dikhta hai (slim normal bachcha), aur "Golu se thoda lamba" sheet me tay nahi (alag sheets, group collage me dono lagbhag barabar). Fix (free): scene prompts me har baar "very thin, skinny arms and legs, a little taller than Golu" likho.
- Cosmetic: Tinku side view me chashme ka lens chehre se aage nikla hua; scenes me ref se theek ho jaayega, ignore.

## 2. Children rule (12a)
- Dono masoom, umar ke hisaab se, family-friendly poses aur kapde. Tara ka varnan bible me swabhaav par (roop par zor nahi), sheet me koi glamour/pose emphasis nahi. Koi romance angle nahi. Tinku ka "bhookha" pose mazaakiya, neecha dikhane wala nahi. PASS.

## 3. Lookalike — "Kya ye kisi jaane-maane kirdaar ki nakal lagti hai?"
- Tinku: Nahi (low risk). Boy-wizard ki pehchaan (maathe ka nishaan, school robe/cloak, scarf, chhadi/wand, gol chashma + bikhre baal ek saath) me se sirf chashma + baal hain; Indian bachcha, half-pant, sandal, orange dhaariyan — copy nahi lagta. Doosre do jaane-pehchaane kirdaaron se bhi doori rakhni hai: dhaaridaar shirt + gol chashma (laal-safed dhaariyan + bobble hat wala famous kirdaar) aur gol chashma + peeli shirt + blue shorts wala famous anime bachcha. MINOR m4 (free prompt guard): Tinku ke scenes me dhaariyan hamesha orange-cream (kabhi laal-safed nahi), kabhi topi/beanie, scarf, robe/cloak, maathe par nishaan, chhadi nahi; shirt kabhi peeli/plain nahi. (Ye naam sirf yahan review me nahi likhe, prompts me bhi kabhi nahi.)
- Tara: Nahi. Do chotiyan + ribbon wali Indian bachchi ek aam look hai; peeli frock + notebook/pencil + painted style ke saath kisi ek famous kirdaar ki taraf nahi jaata.
- Koi regen ki zaroorat nahi.

## 4. Names
name_guard OK on all 4 files. Koi studio/film/artist naam nahi.

## 5. Voices
| file | dur | LUFS | true peak | sample peak | Whisper |
|---|---|---|---|---|---|
| voices/tara_Kore.wav | 3.24 s | -14.4 | -1.2 dBTP | -1.3 dB | "रूको! तहली सोचो फिर दोरो" (line: रुको! पहले सोचो, फिर दौड़ो) |
| voices/tinku_Achernar.wav | 4.24 s | -13.6 | +1.0 dBTP | -0.6 dB | "मुझे कुई दर नहीं लगरा, बस भूख लगरे है" |
| voices/golu_Leda.wav | 4.52 s | -13.1 | +1.5 dBTP | -1.3 dB | poori line |
- Clipping nahi (astats flat factor 0, peak count 2). Sample = _review copy (byte-same). Whisper small Hindi me sab shabd aaye (gadbad sirf Whisper ki matra), logprob -0.32/-0.36.
- Uniqueness: Kore aur Achernar CAST me kisi aur ke paas nahi (Charon, Puck, Despina, Enceladus, Leda alag). PASS.
- Pitch (meri autocorrelation F0 median): Tara/Kore 312 Hz, Tinku/Achernar 316 Hz, Golu/Leda 387 Hz. Builder: 261 / 289 / 338 Hz. Dono tareeke: Golu dono se ~3-4 semitone upar = alag pehchaan. Tara vs Tinku: sirf 0.2-1.8 semitone ka fark = pitch se pakka alag NAHI (alag sirf andaaz/speed se).
- MINOR m1 (free): Tinku ko Tara se alag karo — option A: Tinku = Callirrhoe (sample already bana, F0 ~264 Hz, Whisper sabse saaf "मुझे कोई"; Tara 312 / Tinku 264 / Golu 387 ~ har jodi 3 st), option B: Achernar + pitch -2 st (voices.py teesra field). User ek baar sun kar chune (taste); bina sune default = option A.
- Vindemiatrix sample -20.5 LUFS (sabse dheema) — reject theek.
- MINOR m2: channel.json "voices" speed (tara 1.0, tinku 0.95, golu 0.95) koi script nahi padhta; make_short sirf meta.json "speed" leta hai. Fix: make_short me channel.json voices speed default ke roop me jodo, ya har story ke meta.json me {"golu":0.95,"tinku":0.95} likho.
- Note m5: Tinku/Golu samples ka true peak > -1 dBTP, par build me mix normalise/limit hota hai — final me check hoga.
- Cosmetic m6: voices.py me toli ki lines "# --- long_03 (story 004)" comment aur mishra ke beech aa gayi; toli block mishra ke baad rakho.
- Note: register (assets_license.csv) me sheets/voices ki rows nahi — purani painted sheets ki bhi nahi, consistent; zaroori nahi (apna AI asset).

## Agla kadam
m1 (Tinku voice), m2 (speed wiring), m3/m4 (prompt lines in gen_scenes/bible), m6 free fixes; phir R2 sirf in par. Sheets final ke liye user ki bible approval baaki (DRAFT).

---

# R2 (2026-10-20) — sirf badle hue points   VERDICT: PASS (notes carry_over me)
STOP condition: nahi. Kharcha R2: ₹0 (new_characters ₹11.83 of ₹20).

- m1 Tinku voice -> Callirrhoe: voices.py CAST "tinku" = Callirrhoe, channel.json voices.tinku.voice = Callirrhoe; characters/voices/tinku_Callirrhoe.wav byte-same as _review copy; tinku_Achernar.wav ab _to_delete/voices/ me. Callirrhoe CAST me kisi aur ke paas nahi. Sample: 4.40 s, -16.2 LUFS, peak -1.5 dBFS, clipping nahi, Whisper "मुझे कोई दर नहीं लगरा, बस भूख लगरे है" (poori line).
  Pitch (F0 median, same method as R1): Tara/Kore 312 Hz, Tinku/Callirrhoe 264 Hz, Golu/Leda 387 Hz -> Tara-Tinku 2.9 st, Tara-Golu 3.7 st, Tinku-Golu 6.6 st. Teeno ab pitch se alag. FIXED.
- m2 speed wiring: make_short main me story >= 005 aur meta "speed" dict ho to channel.json voices speeds bache speakers bharti hain (meta jeetta hai; test merge {'tara':1.1} -> golu 0.95, tara 1.1, tinku 0.95). Stories <= 004 aur scalar speed untouched. py_compile OK. FIXED. Note -> carry_over: meta me speed na ho / number ho to channel speeds nahi lagti; story 005 meta me "speed": {} rakhna.
- m3/m4 prompt guard: bible 2a "Toli ke niyam" me Tinku (very thin, skinny arms/legs, thoda lamba, orange-cream dhaariyan, kabhi laal-safed/peeli/plain nahi, cap/scarf/robe/maathe ka nishaan/wand nahi) aur Tara (focused thinking face) ki line hai; gen_scenes CHAR_NOTES painted prompts me ref "tinku"/"tara" hone par khud jodta hai (ref_path -> characters/<name>/sheet_painted.png). FIXED. Story 005 image review me check -> carry_over.
- m6 voices.py: toli block ab mishra ke baad. FIXED.
- name_guard: gen_scenes.py, make_short.py, voices.py, channel_bible.md, channel.json -> sab OK.
