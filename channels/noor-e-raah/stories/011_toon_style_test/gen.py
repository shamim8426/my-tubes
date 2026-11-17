import sys
from pathlib import Path
sys.path.insert(0,"scripts")
import gemini_image as g
S=Path(__file__).resolve().parent
CHAR=("Illustrated storybook scene, hand-painted warm 2D cartoon with soft outlines, painterly background, cinematic spotlight and golden light. "
"ALL people are FACELESS stylized figures: smooth round blank white head with NO eyes, NO nose, NO mouth, NO face features at all, simple gloved dark hands, simple clothes. "
"Setting: 7th-century Medina village courtyard, mud-brick walls, date palms with dates, wooden door, warm sunset. No text, no writing, no modern objects, no domes or minarets. 16:9.")
P={
"A_door":CHAR+" Scene: a woman figure (long dark green robe, white headscarf, faceless blank white head) stands at a wooden doorway looking worried, hands clasped, a soft white glow around her head. In front of her a man figure (brown robe and white turban, faceless) turns away with an angry pointing arm. Two small child figures (faceless, tiny) peek from the doorway behind her. Medium-wide shot, characters clearly readable.",
"B_dua":CHAR+" Scene: the same woman figure (long dark green robe, white headscarf, faceless blank white head with soft white glow) kneels under a date palm at dusk with both hands raised in prayer, a beam of golden light from the sky falling on her. Calm emotional mood. Medium shot.",
}
for k,v in P.items():
    out=S/"images"/f"{k}.png"
    if not out.exists():
        g.generate(v,out,aspect_ratio="16:9",size="1K"); print(k,"ok",flush=True)
