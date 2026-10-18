# Brand guide — किस्सागो | Kissago

- **Name:** किस्सागो | Kissago (channel key `dadi-ki-kahaniyan`, formerly दादी की कहानियाँ)
- **Handle:** @KissagoKahaniya — https://www.youtube.com/@Kissagokahaniya
- **Tagline:** हर शाम एक नया किस्सा
- **Hosts / characters:** Dadi, Golu, Mitthu (looks: `channel_bible.md`). Mystery series: "दादी जासूस".

## Colours
| Name | Hex | Use |
|---|---|---|
| Night indigo | `#1F1B4D` | backgrounds (DP circle, banner sky, cards) |
| Marigold | `#F4A300` | the name "किस्सागो", highlights |
| Cream | `#FFF4DC` | secondary text ("KISSAGO", tagline), light backgrounds |
| Parrot green | `#2FA84F` | accent only (Mitthu, small details) |

libass/ASS colours are BGR: marigold `&H0000A3F4&`, cream `&H00DCF4FF&`, indigo `&H004D1B1F&`, green `&H004FA82F&`.

## Fonts
- **Wordmark:** Rozha One (Indian Type Foundry, SIL OFL 1.1) — `shared/fonts/RozhaOne-Regular.ttf`. Only for the name "किस्सागो" (and big titles if wanted).
- **Everything else:** Mukta (Bold/ExtraBold) — `shared/fonts/`.
- Hindi text is always rendered by libass/HarfBuzz (letter spacing 0), never by an image model. Zoom-check matras.

## Logo
Files (in `brand/`, transparent PNG unless noted): `icon.png` (2048x2048, Mitthu on an open book, no text),
`logo_horizontal.png` (icon left + name right), `logo_stacked.png` (icon top + name below),
`kissago_dp_ki.png` (800x800, **profile picture**: monogram "कि" in Rozha One marigold on indigo with a marigold ring — chosen by the user 2026-10-18; older DP options: `kissago_dp_v3.png`, `_work/dp_concepts/`), `kissago_banner_v3.png` (2560x1440, night sky, logo without panel — live), `watermark.png` (150x150).
Known notes on banner v3 (accepted by the user): Golu looks slimmer than his sheet and the roof is thatched instead of khaprail; a regen (~₹4.86) can fix both if wanted.

When to use what:
- **Monogram "कि":** profile picture only (`kissago_dp_ki.png`).
- **Icon only (Mitthu):** video watermark, favicon-size places, anything smaller than ~200 px wide.
- **Horizontal (icon + name):** banner, thumbnail corner, end cards, wide layouts.
- **Stacked:** square / vertical layouts (Shorts covers, posters, social posts).

Rules:
- **Minimum size:** icon 48 px; horizontal lockup 240 px wide (name must stay readable); stacked 160 px wide.
- **Clear space:** keep empty space around the logo of at least the height of the "क" in "किस्सागो" (about 1/4 of the icon height) on every side.
- On busy pictures put the logo on a soft indigo or cream patch (60-80% opacity) instead of stretching or outlining it.
- Do not recolour, stretch, rotate, add effects, or redraw the name in another font. Do not put the icon inside another shape except the DP circle.

## Thumbnails
- Corner brand: small `logo_horizontal` (about 18-20% of the thumbnail width) at bottom-left — never bottom-right (video length sits there).
- Main title text: Mukta ExtraBold, max 4 words, high contrast (RULES sections 6 and 13).

## Banner
- Everything important inside the 1546x423 safe area (centre of the 2560x1440 canvas); check desktop, TV and mobile crops.
