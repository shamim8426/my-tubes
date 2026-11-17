import sys
from pathlib import Path
sys.path.insert(0,"scripts")
import gemini_image as g
S=Path(__file__).resolve().parent
B=("Illustrated storybook scene, hand-painted warm 2D cartoon with soft outlines, painterly background, cinematic light. "
"ALL people are FACELESS stylized figures: smooth round blank white head with NO eyes, NO nose, NO mouth, NO face features, simple dark gloved hands, simple robes. "
"Ancient Middle-East rocky hills. No text, no writing, no modern objects, no domes or minarets. 16:9. ")
P={
"1_rain_cave":B+"Scene: three faceless travelers in brown robes running through heavy rain toward the dark mouth of a mountain cave, dark stormy sky, wet rocks, lightning in the distance. Wide shot.",
"2_rock_blocks":B+"Scene: inside a dark cave, three faceless men in robes sit huddled, looking toward the cave mouth which is completely blocked by a huge round boulder, only thin light at the edges. Warm lantern-less dim light, worried mood. Medium-wide shot.",
"3_parents_bowl":B+"Scene: a dim simple room at night, two elderly faceless figures sleeping on mats, and a faceless young man standing patiently beside their heads holding a wooden milk bowl, a small oil lamp glowing, warm golden light. Medium shot.",
"4_gold_turn_away":B+"Scene: a faceless man in a robe at night turning away and walking out of a doorway, leaving a small leather pouch of gold coins on a table, moonlight at the door, calm and resolute mood. Medium shot.",
"5_field_herd":B+"Scene: a green valley at sunrise with a large herd of cattle, camels and goats grazing, a faceless old laborer in simple clothes standing in front receiving them from a faceless man who points to the herd, warm hopeful light. Wide shot.",
"6_rock_open":B+"Scene: the cave mouth at dawn with the huge boulder rolled aside, golden sunrise light pouring in, three faceless men in robes walking out safely with raised hands, beautiful sky. Wide shot.",
}
for k,v in P.items():
    out=S/"images"/f"{k}.png"
    if not out.exists():
        g.generate(v,out,aspect_ratio="16:9",size="1K"); print(k,"ok",flush=True)
