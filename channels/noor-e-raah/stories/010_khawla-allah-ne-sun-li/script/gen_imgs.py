import sys, time
from pathlib import Path
sys.path.insert(0, "scripts")
import cf_image
S = Path(__file__).resolve().parent.parent
BASE = ("Cinematic 3D-illustration film still of 7th century Madinah, Arabia, ultra sharp crisp focus, high contrast, deep rich saturated colors, "
        "clean clear air, no haze, no fog, deep dark shadows, warm earthy palette, wide 16:9 composition. Absolutely no text, no letters, no modern objects, "
        "no visible faces, no Prophet, no angels, no domes, no minarets, no arches, no tall towers, no modern buildings, only low flat-roofed mud-brick houses and palm trees. ")
P = {
"01_night_lane": "Narrow mud-brick lane of old Madinah at night, one small house window glowing with a tiny oil lamp, dark blue night, empty street.",
"02_palm_morning": "Early morning over date palm groves and simple mud-brick houses of old Madinah, soft golden sunrise, empty.",
"03_house_hearth": "Inside a simple mud house, small hearth fire glowing, a few plain woven sleeping mats on the floor, clay pots, nobody in view, no scrolls, no books.",
"04_closed_door": "A closed old wooden door of a mud house at dusk, strong wind blowing sand across the ground, lonely mood.",
"05_stuck_rope": "A frayed rope knotted tightly between two wooden posts in a dusty empty yard at dusk, symbol of being stuck in the middle.",
"06_empty_room": "Empty mud room with one bare mat and a single oil lamp, lonely quiet mood, long shadows.",
"07_kids_clothes": "Small folded children's clothes on a mat beside a clay plate with a dry flatbread, soft sad light, nobody in view.",
"08_woman_walking": "A woman in a long dark cloak seen from far away from behind, walking on a sandy path at dawn toward the simple early mosque with palm-trunk pillars. Face not visible.",
"09_mosque_wall": "Mud-brick wall and palm-trunk roof of the early mosque of Madinah, empty courtyard, calm morning light.",
"10_hands_raised": "Back view of a person in a dark cloak kneeling on sand at dusk, both hands raised to the sky in prayer. Seen from behind, face not visible.",
"11_light_ray": "Dark clouds parting over palm trees, a bright ray of golden light shining down, hopeful.",
"12_ayah_card": "Dark deep-green background with an ornate golden Islamic geometric border frame, completely plain empty solid dark-green center, nothing inside the frame, elegant, no text, no city.",
"13_open_sky": "Wide open sky with golden light over desert and palm trees, peaceful and big.",
"14_old_custom_falls": "Old torn scroll pages blown away by wind across desert sand, bright light breaking through, symbol of an old custom ending.",
"15a_broken_chain": "A broken iron shackle chain lying on sand in warm light, symbol of freeing a slave.",
"15b_moon_nights": "Night sky with a thin crescent moon rising above a date palm grove, calm, symbol of fasting months.",
"15c_food_cloth": "A spread cloth on the ground with dates, bread and bowls of food ready to feed the poor, warm light, nobody in view.",
"16_dates_basket": "A large woven basket full of fresh dates, handed over at the doorway of a mud house, warm light, nobody in view.",
"17_door_opens": "A wooden door of a mud house standing open, warm golden light flowing out from inside, empty doorstep, absolutely no people.",
"18_night_stars": "Starry night sky over quiet Madinah mud houses and palm trees, peaceful.",
"19_morning_market": "Morning in a simple Madinah market with stalls of dates and sacks, empty stalls, absolutely no people, warm light.",
"20_palm_walk": "A tiny distant person in a dark cloak walking away from the camera through a golden date palm grove, back view only, no face.",
"21_moon_night": "Full moon over a quiet desert town and palms, calm and peaceful.",
}
only = sys.argv[1:] 
for k, v in P.items():
    out = S / "images" / f"{k}.png"
    if out.exists() or (only and k not in only): continue
    for t in range(3):
        try:
            cf_image.generate(BASE + v, out, width=1920, height=1088); print("OK", k); break
        except Exception as e:
            print("ERR", k, str(e)[:120]); time.sleep(5)
