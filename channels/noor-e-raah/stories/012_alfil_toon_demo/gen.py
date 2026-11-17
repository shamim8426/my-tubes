import sys
from pathlib import Path
sys.path.insert(0,"scripts")
import gemini_image as g
S=Path(__file__).resolve().parent
B=("Illustrated storybook scene, hand-painted warm 2D cartoon with soft outlines, painterly background, cinematic light. "
"ALL people are FACELESS stylized figures: smooth round blank white head with NO eyes, NO nose, NO mouth, NO face features, simple dark gloved hands, simple clothes. "
"7th-century Arabia, desert valley setting. No text, no writing, no modern objects, no domes or minarets. 16:9. ")
P={
"1_army":B+"Scene: a large ancient army marching across a sandy desert at golden hour, a huge war elephant with a decorated saddle in front, rows of faceless soldiers with spears and round shields behind, dust in the air, distant rocky mountains. Wide shot.",
"2_kaaba":B+"Scene: view from a hillside down into a quiet rocky valley where a small cube-shaped stone house covered with a plain black cloth stands in the middle of a wide open courtyard, a few tiny faceless people in simple robes standing and watching from far away, calm warm evening light. No dome, no minaret.",
"3_elephant_sits":B+"Scene: the huge war elephant sitting down on the sand and refusing to move, faceless soldiers pulling on ropes and pushing with sticks, confused and tired, dust, desert hills behind. Medium-wide shot.",
"4_birds":B+"Scene: a huge flock of small birds filling the evening sky, flying down in waves over the army below (tiny faceless soldiers, an elephant, spears), each bird carrying a tiny pebble, dramatic orange and purple sky with rays of light. Wide shot.",
"5_night_valley":B+"Scene: peaceful night over the same quiet valley with the small cube-shaped house covered in black cloth in the middle, a sky full of stars and a soft crescent moon, a few tiny faceless people sitting quietly in the distance, calm and safe mood. Wide shot.",
}
for k,v in P.items():
    out=S/"images"/f"{k}.png"
    if not out.exists():
        g.generate(v,out,aspect_ratio="16:9",size="1K"); print(k,"ok",flush=True)
