# CHANNEL BIBLE — "Jugnu Stories"

> Channel ka naam: **जुगनू स्टोरीज़ | Jugnu Stories** (`channel.json` `display_name`). Folder/key `jugnu-stories` wahi hai.
> **Cast v3 (2026-11-01 se, user):** nayi har video me SIRF neeche ka naya cast. Purana cast (Dadi, Golu, Mitthu,
> Pandey, Tara, purana Tinku, Sharma ji ...) retired: `channel_bible_old_cast.md` + `characters/_old_cast/`, sirf
> stories 001-007 ke rebuild ke liye.
> Title ke ant me `| Jugnu Stories` (channel.json `title_suffix`); thumbnail ke kone me "Jugnu Stories".
> Channel art: `brand/jugnu_banner.png`, `brand/jugnu_dp.png`; description `brand/channel_description.md`.

> Har script aur har scene isi bible ko follow karega. Koi bhi nayi kahani likhne ya scene banane se pehle ise padho.

---

## 1. Channel

- **Format:** Hindi kahaniyan: Long (target 3:40–4:00) + uska Short (35–40 s) (shared/RULES.md 15).
- **Kism:** naitik kahaniyan (imaandari, dosti, himmat, rishte) aur Tinku–Jugnu ki chhoti paheliyan.
- **Maqsad:** hasi + sochne ki baat + dil me ek chhoti seekh.
- **Tone:** family-friendly. Koi khoon-kharaba ya darawni cheez nahi.

---

## 2. Permanent Cast v3 (look KABHI nahi badlega)

**Kirdaar = cut-out PNG** (user 2026-11-01): har kirdaar ki drawing `characters/<id>/<id>_<pose>.png` (1200x2000,
transparent) hu-ba-hu scene me lagti hai (`tools/compose_scene.py`). AI kirdaaron ko KABHI dobara nahi banata.
Poses: stand, walk, point, think, happy, surprised, scared, laugh. Sheet: `characters/<id>/<id>_sheet.png`;
sab ek saath: `characters/cast_lineup.png`. Naya pose/expression chahiye to drawing code `characters/_source/`
(`jugnucast.ts`) me jodo, look wahi rahe.

| id | Kirdaar | Look (exact) | Haath me (prop) |
|---|---|---|---|
| `tinku` | **टिंकू** (hero), ~10 saal | dubla, saaf side-parting wale kaale baal, gol patla chashma, gehra neela polo (jeb me 3 pen), khaki half-pant, kandhe se tirchha bhoora jhola, bhoori chappal | jhola |
| `jugnu` | **जुगनू**, Tinku ka chamakta dost | asli jugnu (firefly beetle), insaan jaisa NAHI: kaala lamba oval sharir, naarangi sir-kavach par bhoore dhabbe, do paardarshi pankh, patle antenna, peeli-hari chamakti poonchh; insaan ki awaaz me bolta hai | — |
| `bholu` | **भोलू**, ~10 saal | gol-matol, chhote bikhre kaale baal, laal T-shirt, bhoori half-pant, neele crocs | hara amrood |
| `ira` | **इरा**, ~10 saal | kaala bob, safed phool wala clip, lavender kurti (neeche safed bindiyon ki patti), safed leggings, chappal | peeli notebook |
| `titli` | **तितली** (natkhat), ~10 saal | do oonchi chotiyaan rang-birange clip ke saath, gulabi frock peeli kinari aur peeli baahon ke saath | phirki (pinwheel) |
| `daroga_singh` | **दरोगा सिंह**, ~45 saal | mote-mazedaar, khaki vardi aur topi (peetal ka billa), ghani moonchh, bhoori belt peetal ka buckle, bhoore joote | magnifying glass (+ biscuit) |
| `kesar_dadi` | **केसर दादी**, ~70 saal, kisson wali | safed-grey baalon ka joora, laal bindi, sone ke jhumke, haldi-naarangi saree safed pallu ke saath, chappal | lakdi ki chhadi |
| `tinku_mummy` | **टिंकू की मम्मी**, ~35 saal | teal saree safed bindiyon aur sunehri patti ke saath, kandhe par lambi choti, laal bindi, jhumke, haar | thaali |

### Cast ke niyam
- Sab bachche umar ke hisaab se masoom aur family-friendly; dosti me romance/crush wala angle KABHI nahi.
- Bholu ke mote hone ka mazaak ho sakta hai, par kahani use kabhi neecha nahi dikhayegi.
- Daroga Singh ka look/mazaak hamara apna; kisi TV/cartoon ke daroga jaisa nahi (name check 2026-10-30).
- Jugnu kabhi insaan jaisa (haath-pair, kapde, chehra) nahi banega; sirf kide ka roop, chamak aur awaaz.

---

## 2b. Bolne ka andaaz (swabhaav DRAFT — user ki manzoori baaki; awaazein PAKKI, user 2026-11-01)

Awaaz ka style + pitch: `scripts/voices.py` (speaker id = upar ki table ka id); samples `characters/voices/cast_v3/`.

Saral Hindi, bachche aur bade dono samjhein. Pakki line ek kahani me max 1–2 baar.

| Kirdaar | Kaise bolta/bolti hai | Awaaz (Gemini TTS) |
|---|---|---|
| **Tinku** | shaant, hoshiyar, dhyan se dekhta hai; sawaal poochh kar sach tak pahunchta hai | **Puck**, pitch +4 (bachcha) |
| **Jugnu** | chhota, chamakta, thoda shararati; Tinku ko ishaara/suraag deta hai, kabhi poora hal nahi batata | **Zephyr** |
| **Bholu** | khushmizaaj, khaane ka shauqeen, jaldbaaz; ek galat andaza aksar usi ka | **Fenrir**, pitch +3 (bachcha) |
| **Ira** | sab kuch notebook me likhti hai, tathya yaad rakhti hai, saaf aur tez | **Pulcherrima**, pitch +3 (bachchi) |
| **Titli** | natkhat, chanchal, sawaal par sawaal; uski shararat kabhi-kabhi suraag ban jaati hai | **Autonoe**, pitch +4 (chhoti bachchi) |
| **Daroga Singh** | rob jhaadne wale, zor se bolte, phir jhenp; dil ke naram, biscuit ke shauqeen | **Algenib**, pitch -1 (bhaari) |
| **Kesar Dadi** | kisson wali, meethi, muhavare; seekh kahani ke ant me pyaar se | **Vindemiatrix** (boodhi) |
| **Tinku ki mummy** | pyaar bhari par sakht, ghar ki baat | **Aoede** |
| **Narrator** | kahani sunane wala, saaf aur garam (Charon) | Charon |

---

## 3. Side characters

- Har kahani ke naye kirdaar bhi **isi drawing style** me cut-out bante hain (`characters/_source/jugnucast.ts`
  me naya Spec, ₹0) — kabhi AI-painted kirdaar nayi video me nahi.
- Naye kirdaar ka look story ke `story.md` me likho; dobara aaye to **wahi look** (aur wahi PNG).
- Purane side characters (Sharma ji, Pappu, Gupta aunty, Raju, Bunty, Mishra dada) purane style ke hain: nayi video
  me chahiye to pehle naye style me banao.

---

## 5. Setting — "Gulmohar Mohalla"

- Chhoti galiyan, gulmohar ka ped, kaccha ghar, khaprail ki chhat, chhat, chai stall, park, mandir.
- Kabhi-kabhi special: shaadi, mela, train, gaon.

---

## 7. Script Rules

- Lambai/kharcha: shared/RULES.md 15 (Long 3:40–4:00, Short 35–40 s).
- 2-sec hook; ek saaf seekh; har kahani me Tinku + Jugnu.
- Paheli wali kahani: Bholu (ya koi bachcha) ka **ek galat andaza**, Jugnu/Tinku ka **ek suraag observation**,
  end me sawaal (jaise **"बताओ, दोषी कौन?"**), **answer alag file me**.
- Script me har scene ke liye likho: kaun-kaun, kis pose me (8 poses me se), kahan khada.

---

## 8. Image Rules (cut-out, 2026-11-01 se)

- **Kirdaar:** sirf `characters/<id>/` ke PNG, `tools/compose_scene.py` se (story ka `cutout_scenes.json`).
  Scene image = background + kirdaar; output wahi `images/scene_XX.png`, builder (make_short / parallax) same.
- **Background:** BINA kirdaaron ka (koi insaan/janwar nahi), free pehle (Cloudflare `scripts/cf_image.py`), warna
  paid; style: saaf flat cartoon jo kirdaaron se mel khaye (moti outline nahi chahiye, rang garam), koi text nahi.
- Scene ki roshni: `"light": day / morning / evening / night` taaki kirdaar background me mil jaayein.
- Kirdaar frame ke kinaron (4%) aur Shorts ke YouTube buttons wale hisse se door; bolne wala saaf dikhe.
- Kisi studio/film/anime/artist ka naam KAHIN nahi (RULES 12a).
