import json
from pathlib import Path
S = Path(__file__).resolve().parent
L = [
 ("1_rain_cave","तीन आदमी सफ़र में थे। अचानक तेज़ बारिश होने लगी।",["बारिश"]),
 ("1_rain_cave","वो भागकर पहाड़ की एक गुफा में छिप गए।",["गुफा"]),
 ("2_rock_blocks","तभी पहाड़ से एक बड़ी चट्टान लुढ़की, और गुफा का मुँह बंद हो गया।",["चट्टान"]),
 ("2_rock_blocks","तब एक ने कहा: अब सिर्फ़ अपने सच्चे अच्छे कामों का वास्ता देकर, अल्लाह से दुआ करो।",["अल्लाह"]),
 ("3_parents_bowl","पहले ने कहा: ऐ अल्लाह, मेरे बूढ़े माँ-बाप थे।",["माँ-बाप"]),
 ("3_parents_bowl","एक रात मैं देर से आया, और वो सो चुके थे।",[]),
 ("3_parents_bowl","मैं दूध का प्याला लिए, सुबह तक उनके सिरहाने खड़ा रहा।",["सुबह"]),
 ("3_parents_bowl","अगर ये काम तेरे लिए था, तो हमें इस मुसीबत से निकाल दे।",["तेरे"]),
 ("2_rock_blocks","चट्टान थोड़ी सी खिसकी, पर रास्ता अब भी बंद था।",["खिसकी"]),
 ("4_gold_turn_away","दूसरे ने कहा: मुझे एक बहुत बड़ी बुराई का मौक़ा मिला था।",["बुराई"]),
 ("4_gold_turn_away","पर मुझे अल्लाह का डर याद आया, और मैं पीछे हट गया।",["डर"]),
 ("5_field_herd","तीसरे ने कहा: एक मज़दूर अपनी मज़दूरी छोड़कर चला गया था।",["मज़दूर"]),
 ("5_field_herd","मैंने उसका पैसा बढ़ाया, और सालों बाद उसे सब कुछ लौटा दिया।",["सब"]),
 ("6_rock_open","और फिर चट्टान पूरी तरह हट गई। तीनों सलामत बाहर निकल आए।",["सलामत"]),
 ("6_rock_open","ये वाक़िआ सहीह बुख़ारी और सहीह मुस्लिम की हदीस में आया है।",[]),
]
P = ["push_in","pan_right","pull_out","pan_left"]
M = "shared/music/noor/River_Flute.mp3"
lines = [{"n":i+1,"text":t,"img":im,"motion":True,"preset":P[i%4],"overlay":[["dust",0.08]],"sfx":[],"amb":[],"music":M,"ayah":False,"gold":g} for i,(im,t,g) in enumerate(L)]
cfg = {"title":"Teen musafir aur gufa (sample)","voice":"Charon",
 "style":"Calm, warm, clear Hindi storyteller. Simple spoken Hindi, gentle emotion, normal conversational pace, correct Urdu sounds.",
 "tempo":1.0,"ambience":"shared/sfx/history/wind_desert_675710.mp3","music":M,"music_vol":0.5,"amp":0.08,"amb_db":-6,"sfx_db":-3,"duck":True,"lines":lines}
(S/"script.json").write_text(json.dumps(cfg,ensure_ascii=False,indent=1),encoding="utf-8")
(S/"audio").mkdir(exist_ok=True); (S/"output").mkdir(exist_ok=True)
