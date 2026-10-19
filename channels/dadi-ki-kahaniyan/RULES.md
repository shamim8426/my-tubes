# Channel RULES — किस्सागो | Kissago (key: dadi-ki-kahaniyan; formerly दादी की कहानियाँ)

Only the rules special to this channel. Read `shared/RULES.md` first; everything there applies here too.
- Channel RULES can be stricter than shared RULES, never looser. Copyright, channel ID, secrets and upload safety can never be relaxed by a channel.

## Story and characters (from `channel_bible.md`)
- Dadi (Kamla Devi) narrates the moral stories. In Gulmohar Mohalla stories where Dadi is herself a character, the narrator voice narrates. Every other character speaks their own lines in their own voice.
- Mitthu (parrot) has no hands: no hand gestures, holding things or pointing with hands.
- Dadi's home (in Gulmohar Mohalla): a kacha mud house with a tiled roof, BROWN wooden door, swept aangan, green fields behind, exactly like the channel banner (`channels/dadi-ki-kahaniyan/brand/_work/banner_art.png`). There is no green door.
- Setting: Dadi's home, the Golu–Mitthu opening/closing frame and all Dadi Jasoos cases are in Gulmohar Mohalla. The story Dadi narrates inside a moral-story video can be set in any village or town the approved script names (e.g. Rampur in LONG_01); check location consistency against that script. Village kitchens still use a mitti ka chulha, never a gas stove.

## Metadata
- Mystery (Dadi Jasoos) videos: the answer never goes in the title, description or thumbnail. It goes in the pinned comment 24 h after publishing.
- किस्सागो (Kissago) is set to made_for_kids = false (family audience, decided by the user). So title, thumbnail, description and tags must speak to the whole family, not only to children: no "for kids" / "बच्चों के लिए" / nursery-style wording. Flag any such wording as FIX.
- Titles end with the channel brand: `title_suffix` from channel.json ("| किस्सागो"). The old suffix "| दादी की कहानियाँ" is not used any more.
- Thumbnail corner label = `brand_label` from channel.json ("किस्सागो").
- Dadi, Golu and Mitthu stay the channel's hosts/characters; the mystery series keeps its name "दादी जासूस" (Dadi Jasoos).

## Short cover (poster style, from the next Short after short_01_sona-chori)
Style reference: `brand/reference/short_cover_style_ref.png` (user's choice, 2026-10-19). Made by `scripts/gen_short_cover.py <short folder>` from the `cover` block in the Short's meta.json; output `output/<short>_cover.png` (1080x1920). One Gemini image (9:16, 1K, ~₹3.24) counts as a paid step of the story in auto mode (inside the ₹130 cap).
- Look: dramatic poster, dark navy-to-warm-orange gradient background, high contrast, flat 2D cartoon with thick outlines (channel style).
- Layout (Shorts grid crops the top, the app covers the bottom; RULES 14 text inside 15%-85%):
  - 0-14% height: background only (no text, no faces).
  - 15-20%: gold label — "किस्सागो जासूस" for Dadi Jasoos mysteries, else "किस्सागो" (`brand_label`).
  - 20-33%: big yellow title, 2-3 words, Mukta ExtraBold with thick black outline, ends with "?" or "!".
  - 33-63%: ONE big hero character (strong emotion: thinking, shocked, shouting).
  - 61-82%: the key object/clue and 1-3 other characters (suspects, worried faces).
  - 82-100%: no faces, no text (bodies/ground only).
  - Mitthu may sit small in a top-right corner as a recurring mascot (below 15%).
- Hindi text is never drawn by the image model; the script draws it (libass, letter spacing 0) and Munshi zooms in to check matras.
- No spoiler (answer, twist, or a reveal like "Sona is a cat"), no misleading promise: everything shown must be in the Short. Title text must not repeat the video title word for word.
- Characters exactly as in the bible / sheets. The API cannot set Short covers: the file is for manual upload in the YouTube app/Studio (the Short's first frame stays a strong visual without a title card, RULES 13).
