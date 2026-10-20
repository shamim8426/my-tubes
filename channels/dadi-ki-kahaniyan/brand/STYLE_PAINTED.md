# Kissago Painted — image style guide (from story 005)

Status: APPROVED by the user 2026-10-20 (test: `style_tests/painted/`). `channel.json` → `"image_style": "kissago_painted"`;
`scripts/gen_scenes.py` applies it from story 005. Stories up to 004 keep the old flat-cartoon style.

This style has one name only: **Kissago Painted**. No studio, film, anime or artist name is ever used anywhere —
not in prompts, file names, metadata or comments (shared/RULES.md section 12).

## 1. Style block (paste VERBATIM at the end of every image prompt)

```
soft hand-painted 2D anime illustration, watercolor and gouache textures, visible gentle brush strokes, warm golden natural light, lush detailed painted backgrounds, soft clouds, gentle expressive faces with simple features, cozy Indian neighbourhood life, calm nostalgic mood, no text, no logos, no watermark
```

Plus, for every image with a permanent character: the character's `characters/<name>/sheet_painted.png` as a
reference image ("keep this character exactly as in the reference sheet"). Only the characters in that scene.

## 2. Colour palette
| Use | Colours |
|---|---|
| Day sky | soft cerulean blue with cream-white painted clouds |
| Walls and lanes | warm ochre, terracotta, faded turquoise, pale pink, limewash white |
| Greens | sap green and olive foliage, moss on old walls |
| Accent (Gulmohar) | flame orange-red flowers, always somewhere in outdoor scenes |
| Evening | apricot and rose sky, long amber light |
| Night | deep indigo-blue sky, silver moonlight, warm lantern-orange pools of light; faces always readable |
| Shadows | cool lavender-blue, never pure black |

## 3. Light by time of day
- **Morning/day:** warm golden sun from one side, soft painted shadows, light dust in the air.
- **Evening (shaam):** low amber sun, long shadows, glowing sky, first lit windows.
- **Night (raat):** indigo palette, moonlight rim on characters, lantern/diya as the main warm light, stars painted softly.

## 4. Characters (look never changes; painted version of the bible)
- **Dadi (Kamla Devi):** ~70, round kind face, white hair in a bun, round golden spectacles, light green saree with a
  yellow border, gold bangles, small red bindi, wooden walking stick.
- **Golu:** ~10, chubby, round face, messy black hair, yellow T-shirt, blue half-pants, white socks, red shoes.
- **Mitthu:** green parrot, red beak, ONLY a thin red neck ring — throat and chin plain green, no black patch (the
  painted sheet v2 still shows a soft dark chin patch: every Mitthu prompt adds this line, gen_scenes does it
  automatically; check his throat in image review). A bird: wings and feet only, NO hands, never holds things.
- Other bible characters (Pandey ji, Sharma ji, Gupta aunty, Raju, Mishra dada, …) get a `sheet_painted.png` only
  when a story needs them (~₹6 each, from that story's budget), from their old sheet as reference.
- Clothes, faces and homes are always Indian.

## 5. Gulmohar Mohalla (recurring places)
- **Gulmohar tree:** big spreading tree with flame-orange flowers, petals on the ground.
- **Dadi's aangan:** mud house with a clay-tile roof, brown wooden door, clean swept courtyard, charpai, tulsi pot,
  green fields behind.
- **Chhat (rooftops):** flat roofs with low walls, water tanks, clotheslines, neighbouring roofs close together.
- **Gali (lanes):** narrow lanes, colourful two-storey houses, small balconies, overhead wires, Raju's chai stall.

## 6. Prompt shape
`<scene: who, where, what they do, mood, time of day>` + `Keep every character exactly as in the attached reference
sheets.` + `Mitthu is a bird with wings and feet only, no hands.` (if he is in it) + the style block (section 1).
Never add any studio/film/artist name or "in the style of …".
