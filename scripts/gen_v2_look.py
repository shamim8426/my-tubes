"""One-off: new cute 'Kissago Painted v2' portraits of all characters (user request 2026-10-22). Run from the repo root."""
import sys
from pathlib import Path

sys.path.insert(0, "scripts"); sys.path.insert(0, "tools")
from name_guard import find_names  # noqa: E402
from gemini_image import generate  # noqa: E402
import story_budget as SB  # noqa: E402

CH = Path("channels/dadi-ki-kahaniyan/characters")
OUT = CH / "_v2_look"
STYLE = ("clean 2D digital illustration with smooth soft cel shading and gentle gradients, thin clean linework, very cute "
         "and beautiful characters with luminous large expressive eyes and bright catchlights, soft rosy blush, glossy hair "
         "with soft highlights, healthy natural proportions, warm cinematic natural light, richly painted detailed Indian "
         "village background with soft depth of field, cozy heart-warming mood, no pencil texture, no rough brush strokes, "
         "no text, no logos, no watermark")
ENV = ("Background: a lived-in Indian village home in Gulmohar Mohalla: mud walls, clay-tile roofs, a brown wooden door, "
       "pink bougainvillea over the wall, potted plants, a swept courtyard, soft light and gentle depth of field.")
REF = ("Keep the character's identity, outfit and colours from the attached reference sheet, but render them in the new "
       "clean cute style described; do not copy the sheet's texture or layout. Only this one character in the image.")
CHARS = {
    "dadi": ("dadi/sheet_painted.png",
             "Dadi, a sweet Indian grandmother about 70: silver-white hair in a neat bun, round golden spectacles, soft "
             "gentle wrinkles, a warm cute smile with twinkling eyes, small red bindi, light green saree with a yellow "
             "border and a warm earthy printed woollen shawl over her shoulders, gold bangles, her wooden walking stick "
             "beside her. She sits on a low wooden stool in her courtyard, sorting fresh green vegetables in a brass "
             "bowl, morning sun."),
    "golu": ("golu/sheet_painted.png",
             "Golu, an Indian boy about 10, tall for his age and healthy with soft round cheeks (a little chubby, cute), "
             "messy black hair, big shining eyes, a huge joyful laugh; yellow T-shirt, blue half-pants, white socks, red "
             "shoes. He runs happily in a village lane rolling an old bicycle tyre with a stick, golden evening light. "
             "Innocent and age-appropriate."),
    "tara": ("tara/sheet_painted.png",
             "Tara, a clever cheerful Indian girl about 9, two long braids with red ribbons, bright curious big eyes, a "
             "confident warm smile; yellow cotton frock with small printed flowers, holding a small notebook and pencil. "
             "She sits on a charpai under a big tree, thinking happily about a puzzle, sunset glow. Innocent and "
             "age-appropriate; her charm comes from her clever, kind expression."),
    "tinku": ("tinku/sheet_painted.png",
              "Tinku, an Indian boy about 9, thin and a little taller than Golu, round spectacles, messy hair, big eyes, a "
              "sweet sheepish grin; loose orange-and-cream striped shirt (stripes orange and cream only), half-pants. He "
              "holds a round laddoo behind his back, caught but smiling, near a clay pot in the courtyard, late "
              "afternoon. No cap, no scarf. Innocent and age-appropriate."),
    "tinku_mummy": (None,
                    "Tinku's mother, a beautiful and very cute Indian woman about 32, clearly an adult mother: tall, slim "
                    "and healthy, soft round face, very big shining eyes, small nose, small pink lips with a sweet smile, "
                    "soft blush, small red bindi and a thin line of sindoor, small gold jhumkas, thin mangalsutra, red and "
                    "gold glass bangles, glossy black hair in a thick braid with a small white jasmine gajra, a few loose "
                    "strands framing her face. Soft peach cotton saree with small white printed flowers and a green "
                    "block-print border, draped modestly and fully covering the waist and midriff. She stands at her "
                    "doorstep at sunset holding a steel plate of round laddoos, smiling fondly. Family-friendly, dignified."),
    "mitthu": ("mitthu/sheet_painted.png",
               "Mitthu, a cute green parrot with a red beak, big shiny round eyes and ONLY a thin red ring around his "
               "neck (throat and chin plain green, no black patch); a bird with wings and feet only, no hands. He sits on "
               "a wooden perch next to a tulsi pot, head tilted cheekily, beak slightly open as if about to repeat a word, "
               "morning sun."),
    "pandey": ("pandey/sheet_painted.png",
               "Pandey ji, a plump friendly Indian police inspector about 45, thick black moustache, round cheerful face "
               "with big expressive eyes, khaki uniform and cap, a wooden lathi; he twirls his moustache with a proud but "
               "lovable smile, standing by a small village tea stall in the morning. Comic and warm, never scary."),
    "sharma": ("sharma/sheet_painted.png",
               "Sharma ji, a kind Indian neighbour about 55, bald head with grey hair on the sides, rectangular "
               "spectacles, cream kurta-pyjama, brown sleeveless jacket, a gentle sheepish smile; he waters potted plants "
               "with a small brass lota at his red iron gate, soft morning light."),
}


def main(only):
    OUT.mkdir(parents=True, exist_ok=True)
    for name, (ref, desc) in CHARS.items():
        if only and name not in only:
            continue
        out = OUT / f"{name}.png"
        if out.exists():
            print("exists, skip", out); continue
        prompt = f"Vertical 9:16 portrait illustration, waist-up or full figure.\n{desc}\n{ENV}\n" + (REF if ref else "")
        if find_names(prompt + STYLE):
            sys.exit("name guard BLOCK")
        spent, cap = SB.story_cost("character_refresh"), SB.cap("character_refresh")
        if spent + 6 > cap:
            sys.exit(f"character_refresh cap: spent {spent:.2f} of {cap}")
        if SB.remaining() < 5:
            sys.exit(f"ledger {SB.remaining():.2f} < 5: stop (recharge)")
        refs = [CH / ref] if ref else []
        generate(prompt, out, refs=refs, aspect_ratio="9:16", size="1K", style=STYLE)
        print("saved", out, flush=True)


if __name__ == "__main__":
    main(sys.argv[1:])
