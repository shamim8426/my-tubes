import shutil, sys, time
from pathlib import Path
sys.path.insert(0, "scripts")
import cf_image
S = Path(__file__).resolve().parent.parent
K10 = S.parent / "010_khawla-allah-ne-sun-li" / "images"
REUSE = {"30_ayah_card": "12_ayah_card", "35_night_stars": "18_night_stars", "26_dawn": "02_palm_morning", "29_light_ray": "11_light_ray"}
for k, v in REUSE.items():
    o = S / "images" / f"{k}.png"
    if not o.exists():
        shutil.copy(K10 / f"{v}.png", o); print("REUSE", k, "<-", v)
BASE = ("Cinematic 3D-illustration film still of 7th century Madinah, Arabia, ultra sharp crisp focus, high contrast, deep rich saturated colors, "
        "clean clear air, deep dark shadows, warm earthy palette, wide 16:9 composition. Simple plain period clothing: long wool robes, head cloths, leather sandals. "
        "Every person has exactly two arms and two hands with five fingers each, no extra limbs. Absolutely no text, no letters, no modern objects, "
        "no domes, no minarets, no arches, no towers, no glass, no street lamps, only low flat-roofed mud-brick houses with palm-trunk beams and date palms. ")
NOFACE = " The people are seen only from behind, faces not visible."
NIGHT = " Night scene: deep indigo darkness, the only light is the warm golden flame of a small clay oil lamp."
P = {
"01_night_house": "Night exterior of one small mud-brick house, its doorway glowing warm gold from a tiny oil lamp inside, a lone man in a dark robe standing at the doorway, deep blue night sky with stars." + NOFACE,
"02_lamp_glow": "Close-up of a small clay oil lamp with a single flame on a woven palm mat inside a dark mud room, warm gold light on rough mud walls.",
"03_madinah_morning": "Bright morning in old Madinah: a sandy lane between low mud-brick houses, tall date palms, a few townspeople walking with baskets and a donkey, vivid blue sky, hard shadows.",
"04_travelers": "A small group of tired travellers with cloth bundles on their shoulders and two camels arriving on a desert road toward the date palms and mud houses of Madinah, afternoon sun, seen from behind." + NOFACE,
"05_welcome_house": "At the open wooden door of a mud house a local man in a plain robe welcomes a weary traveller with a bundle, his hand on the traveller's shoulder, warm afternoon light." + NOFACE,
"06_palm_share": "Close-up of hands: one pair of hands pouring fresh dates from a woven basket into another person's open hands, under date palm trees, golden light, only hands and sleeves visible.",
"07_tired_man": "A thin tired man in a worn plain robe sitting on the ground with his back against a mud-brick wall, head lowered, seen from behind and a little to the side, hot midday sun, hard shadows." + NOFACE,
"08_messenger_walk": "A man in a plain robe walking along a row of small simple mud-brick rooms with palm-leaf curtains as doors, midday light, seen from behind." + NOFACE,
"09_water_pot": "Inside a bare mud room: a single clay water jar with a wooden cup on top standing on the earth floor, an empty woven mat, a beam of daylight from a small window, nothing else.",
"10_empty_bowl": "Close-up of an empty wooden bowl and an empty clay plate on a woven mat, beside a small clay water jug, soft daylight, simple and bare.",
"11_courtyard": "A simple open courtyard enclosed by mud-brick walls with palm-trunk pillars and a palm-leaf roof at one side, a row of men in plain robes sitting on the sand, seen from behind and far away, calm afternoon light, nobody standing in the centre." + NOFACE,
"12_man_stands": "Among men sitting on the sand in a mud-walled courtyard, one man in a plain brown robe has stood up, seen from behind, the others seated, afternoon light, palm-trunk pillars." + NOFACE,
"13_two_walk": "Two men in plain robes walking side by side away from the camera down a narrow sandy lane between mud-brick houses at dusk, orange sky, long shadows." + NOFACE,
"14_door_arrive": "Two men in plain robes standing at the doorway of a small mud-brick house at nightfall, seen from behind, warm lamp light inside the room, a woman's figure far inside in shadow." + NOFACE + NIGHT,
"15_wife_hearth": "Inside a small mud house at night: a woman in a long dark robe and headscarf kneeling beside a tiny cooking fire with one small clay pot, seen from behind." + NOFACE + NIGHT,
"16_small_pot": "Close-up of one small clay cooking pot with a little porridge and two small pieces of flatbread on a woven mat, tiny amount of food, dim warm firelight.",
"17_couple_talk": "Inside a dim mud room at night, a man and a woman in long plain robes standing close and talking quietly, both seen from behind, a small oil lamp on a shelf." + NOFACE + NIGHT,
"18_lamp_light": "Close-up of a woman's hands with long sleeves lighting the wick of a small clay oil lamp, a warm flame starting, dark mud wall behind, only hands visible." + NIGHT,
"19_kids_sleep": "Three small children asleep on a woven mat under a simple wool blanket in a dark mud room, faces turned away from the camera toward the wall, a mother's hand gently on the blanket, faint lamp glow." + NIGHT,
"20_three_sit": "Three people in plain robes sitting on a woven mat around a cloth with one small bowl of food and a clay oil lamp, seen from behind in a dark mud room." + NOFACE + NIGHT,
"21_lamp_out": "Extreme close-up of a clay oil lamp whose flame has just been put out, a thin curl of smoke rising, a woman's hand with long sleeve beside it, almost dark room.",
"22_dark_room": "A dark mud-brick room at night, only faint blue moonlight through the open doorway, the outline of a woven mat and a bowl, very dark, quiet.",
"23_pretend": "In a nearly dark mud room lit only by faint blue moonlight from the doorway, three dark figures sitting on a mat around a bowl, seen from behind, silhouettes." + NOFACE,
"24_guest_eats": "Close-up of a man's hands breaking a piece of flatbread over a small bowl in faint blue moonlight, only hands and sleeves visible, dark background.",
"25_sleep_hungry": "A moonlit mud room at night: two people lying asleep on woven mats under wool blankets, far from the camera, faces turned away, an empty clay pot in the foreground." + NOFACE,
"27_walk_morning": "A man in a plain robe walking away from the camera down a sunny morning lane of mud-brick houses toward a long mud-brick wall with palm trees, fresh morning light, seen from behind." + NOFACE,
"28_light_door": "An empty open doorway in a long mud-brick wall with palm-trunk beams, filled with soft golden morning light streaming out onto the sand, nobody in view.",
"31_sharing_bread": "Close-up of two hands: one hand giving a round flatbread to another open hand, warm golden light, only hands and simple sleeves visible.",
"32_open_hand": "Close-up of an open palm offering a few fresh dates toward the camera, golden sunlight, date palms softly out of focus behind.",
"33_market_give": "A simple old Madinah market by day with stalls of dates and grain sacks, an ordinary trader handing a small bag of dates to a poor old man, other townspeople around, vivid blue sky, hard shadows.",
"34_dark_lamp": "A clay oil lamp with no flame sitting on a mud windowsill at night, a thin wisp of smoke, blue moonlight and stars outside the small window.",
"36_lamp_end": "A single small clay oil lamp glowing warm gold on the ledge of a mud-brick window at night, looking out over dark palm trees and a starry sky, peaceful.",
}
only = sys.argv[1:]
for k, v in P.items():
    out = S / "images" / f"{k}.png"
    if out.exists() or (only and k not in only):
        continue
    for t in range(3):
        try:
            cf_image.generate(BASE + v, out, width=1920, height=1088); print("OK", k, flush=True); break
        except Exception as e:
            print("ERR", k, str(e)[:160], flush=True); time.sleep(5)
