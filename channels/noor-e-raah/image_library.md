# Noor image library (reuse first)

User 2026-10-31: new videos must REUSE images of earlier Noor videos wherever one fits (free, `"reuse": "<path>"` in long/images.json, or
`reuse_id` + a different crop `rect` for a second look). Generate a NEW image only when no library image can serve the scene (log why).
Images are no-people landscapes/objects, so most can serve different videos with a different crop. Paths are relative to the repo root.
Images are git-ignored: if the file is missing (fresh machine), the library entry is only a description - then generate once and keep.

| id | path | what it shows |
|---|---|---|
| 002/01_night_stars_dunes | `channels/noor-e-raah/stories/002_ayatul-kursi/images/01_night_stars_dunes.png` | A wide night sky full of bright stars and a faint Milky Way over smooth empty sand dunes, deep blue and indigo colours, soft starlight on th |
| 002/02_lamp_on_stone | `channels/noor-e-raah/stories/002_ayatul-kursi/images/02_lamp_on_stone.png` | A single small clay oil lamp with one calm warm flame on a rough stone ledge in a dark room, soft golden glow on the stone, everything else  |
| 002/03_madina_dawn_houses | `channels/noor-e-raah/stories/002_ayatul-kursi/images/03_madina_dawn_houses.png` | Old flat-roofed mud-brick and stone houses among tall date palms in a dry Arabian valley at sunrise, warm light on the walls, an empty sandy |
| 002/04_date_palm_path | `channels/noor-e-raah/stories/002_ayatul-kursi/images/04_date_palm_path.png` | A sandy footpath between date palms in soft morning light leading away into the distance, long gentle shadows, a few low mud-brick walls, pe |
| 002/05_dawn_horizon | `channels/noor-e-raah/stories/002_ayatul-kursi/images/05_dawn_horizon.png` | The first light of dawn over a vast, calm, empty desert, a thin line of gold on the horizon, the sky turning from deep blue to pale gold, st |
| 002/06_oasis_spring | `channels/noor-e-raah/stories/002_ayatul-kursi/images/06_oasis_spring.png` | A small green oasis in the desert: clear spring water, tall date palms and green plants around it, warm afternoon light, sand dunes behind,  |
| 002/07_moonlit_rooftops_lamp | `channels/noor-e-raah/stories/002_ayatul-kursi/images/07_moonlit_rooftops_lamp.png` | Flat-roofed mud-brick houses of an old Arabian town asleep under a bright moon and a starry sky, everything silent and dark except one singl |
| 002/08_vast_panorama | `channels/noor-e-raah/stories/002_ayatul-kursi/images/08_vast_panorama.png` | A huge panorama in one view: a calm sea, tall mountains, green valleys, and above them a sky full of stars with a bright Milky Way, majestic |
| 002/09_lit_door | `channels/noor-e-raah/stories/002_ayatul-kursi/images/09_lit_door.png` | A closed old plain wooden door with simple geometric panels in a thick stone wall, bright warm golden light shining through the gaps around  |
| 002/10_ring_in_desert | `channels/noor-e-raah/stories/002_ayatul-kursi/images/10_ring_in_desert.png` | An enormous empty flat desert plain under a huge sky at dusk, and far away in the lower middle of the picture one tiny plain metal ring lyin |
| 002/11_sunrays_clouds | `channels/noor-e-raah/stories/002_ayatul-kursi/images/11_sunrays_clouds.png` | Golden sun rays breaking through huge towering clouds over distant mountains, a vast glowing sky, majestic, calm and awe-inspiring |
| 002/12_bedtime_room_lamp | `channels/noor-e-raah/stories/002_ayatul-kursi/images/12_bedtime_room_lamp.png` | A simple empty bed with a pillow and a folded blanket on a mud floor next to a small window showing a starry night, a small oil lamp glowing |
| 003/01_one_star_night | `channels/noor-e-raah/stories/003_al-ikhlas/images/01_one_star_night.png` | A calm night sky over smooth empty sand dunes, deep indigo and blue, one single very bright star high above the horizon and only a few faint |
| 003/02_lamp_single_flame | `channels/noor-e-raah/stories/003_al-ikhlas/images/02_lamp_single_flame.png` | One small old clay oil lamp with a spout and one calm warm flame, standing alone on a flat dark stone in a dark room, a soft golden circle o |
| 003/04_dawn_sand_ridge | `channels/noor-e-raah/stories/003_al-ikhlas/images/04_dawn_sand_ridge.png` | First light of dawn over a smooth sand ridge in a vast empty desert, a thin line of gold on the horizon, the sky turning from deep blue to p |
| 003/06_milkyway_desert | `channels/noor-e-raah/stories/003_al-ikhlas/images/06_milkyway_desert.png` | A very wide dark sky full of stars with a bright Milky Way arching over a flat empty desert plain, deep blue and indigo, soft starlight, vas |
| 003/03_makka_valley_night | `channels/noor-e-raah/stories/003_al-ikhlas/images/03_makka_valley_night.png` | A dry rocky valley at night between black-brown granite hills, a few low flat-roofed stone houses far away, an empty sandy lane in soft moon |
| 003/05_paths_to_oasis | `channels/noor-e-raah/stories/003_al-ikhlas/images/05_paths_to_oasis.png` | Looking down from above on a wide desert of soft sand, several faint footpaths in the sand coming from different directions and all leading  |
| 003/07_sea_horizon_dusk | `channels/noor-e-raah/stories/003_al-ikhlas/images/07_sea_horizon_dusk.png` | A completely empty calm sea at twilight meeting a pale glowing sky in one clean straight horizon line, soft gold and blue colours, nothing o |
| 003/08_empty_room_morning | `channels/noor-e-raah/stories/003_al-ikhlas/images/08_empty_room_morning.png` | A simple empty room of mud brick with a straw mat on the floor and a folded plain blanket in the corner, soft morning light coming in throug |
| 003/09_morning_palm_path | `channels/noor-e-raah/stories/003_al-ikhlas/images/09_morning_palm_path.png` | A sandy footpath between date palms in soft early morning light leading away into the distance, long gentle shadows, a few low mud-brick wal |

Story 001 (Al-Fatiha) images: `channels/noor-e-raah/stories/001_al-fatiha/images/` (24 files, see that folder's long/images.json).
