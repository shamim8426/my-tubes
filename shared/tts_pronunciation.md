# TTS pronunciation notes (Gemini TTS, Hindi) — all channels

Kalam writes scripts so the TTS says them right; builders check new lines with Whisper on `--final`.
Status 2026-10-21: no line was ever reported as mispronounced in a published video's review. The entries below come
from voice auditions (Whisper hearing the samples) and from spellings we standardised; add every new case here
(word · what TTS/Whisper produced · how to write it · source).

| Word / case | What happened | Write it as | Source |
|---|---|---|---|
| मिट्ठू (the parrot) | old scripts used मिठ्ठू / मिट्ठु — inconsistent sound and captions | always **मिट्ठू** | story 003 decision |
| years / numbers (e.g. 1965) | digits may be read in English or in an odd way | write the words: **उन्नीस सौ पैंसठ** (captions show the spoken words) | story 005 line 35 |
| दौड़ो, लग रहा | Whisper heard "दोरो", "लगरा" on fast child voices (ड़ / रहा swallowed) | keep the word, give the line a little air (comma before it, no tempo above 1.1 on that voice) | Tara/Tinku auditions 2026-10-20 |
| सोचो (Erinome voice) | heard as "सुचो" | prefer voices that read it clearly (Tara = Pulcherrima); keep short sentences | Tara audition |
| English words | mixed Hindi-English lines sound uneven | avoid; use plain Hindi (टॉर्च, फ़ोटो, हैंडपंप are fine as everyday Hindi) | style |
| nuqta words (ज़, फ़, ख़) | fine when written with the nuqta | keep the nuqta: ख़ज़ाना, ज़रा, फ़ोटो | stories 004–005 |
| "..." pauses | create a real pause — good for comedy timing; too many slow the line | max 1–2 per line | stories 003–005 |
| Names | पांडे जी (not पाण्डेय), कम्मो, बबलू | as written in the bible | bible |

How to add: after a final build, if Whisper or Munshi shows a word heard differently, add a row here and fix the
spelling in that story's lines.json (new TTS only for that line).
