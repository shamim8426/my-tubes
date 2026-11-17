import json
from pathlib import Path
S = Path(__file__).resolve().parent
L = [
 ("1_rain_cave","रसूलुल्लाह ﷺ ने पिछली क़ौमों के तीन आदमियों का वाक़िआ बताया।",["तीन"]),
 ("1_rain_cave","वो सफ़र में थे। तेज़ बारिश हुई, तो वो पहाड़ की एक गुफा में चले गए।",["बारिश"]),
 ("2_rock_blocks","तभी पहाड़ से एक बड़ी चट्टान लुढ़की, और गुफा का मुँह बंद हो गया।",["चट्टान"]),
 ("2_rock_blocks","वो बोले: अब बस अपने नेक कामों के सहारे अल्लाह से दुआ करो।",["अल्लाह"]),
 ("3_parents_bowl","पहले ने कहा: ऐ अल्लाह, मेरे बूढ़े माँ-बाप थे। मैं उनसे पहले किसी को दूध नहीं पिलाता था।",["माँ-बाप"]),
 ("3_parents_bowl","एक दिन मैं चारे की तलाश में दूर निकल गया। देर से लौटा, तो वो सो चुके थे।",["देर"]),
 ("3_parents_bowl","मैं प्याला लिए सुबह तक उनके सिरहाने खड़ा रहा। मैं उन्हें जगाना नहीं चाहता था।",["सुबह"]),
 ("3_parents_bowl","ऐ अल्लाह, अगर ये मैंने तेरी ख़ुशी के लिए किया, तो हमें इस मुसीबत से निकाल।",["ख़ुशी"]),
 ("2_rock_blocks","चट्टान थोड़ी सी खिसकी, पर इतनी नहीं कि वो निकल सकें।",["खिसकी"]),
 ("4_gold_turn_away","दूसरे ने कहा: ऐ अल्लाह, मेरी एक चचेरी बहन थी, जिसे मैं बहुत चाहता था। मैं एक बड़े गुनाह के क़रीब पहुँच गया।",["गुनाह"]),
 ("4_gold_turn_away","तब उस बहन ने कहा: अल्लाह से डरो। मैं रुक गया, और जो कुछ उसे दिया था, वो भी छोड़ दिया।",["डरो"]),
 ("4_gold_turn_away","ऐ अल्लाह, अगर ये मैंने तेरे डर से किया, तो हमें निकाल दे।",["डर"]),
 ("2_rock_blocks","चट्टान और खिसकी, पर वो अब भी बाहर नहीं निकल सकते थे।",["खिसकी"]),
 ("5_field_herd","तीसरे ने कहा: मेरा एक मज़दूर अपनी मज़दूरी लिए बिना चला गया।",["मज़दूर"]),
 ("5_field_herd","मैंने उसकी मज़दूरी का अनाज बो दिया। फ़सल से गायें और एक चरवाहा हो गया।",["गायें"]),
 ("5_field_herd","वो आया तो मैंने कहा: ये सब ले जाओ। वो बोला: मुझसे मज़ाक़ मत करो। मैंने कहा: मज़ाक़ नहीं है।",["मज़ाक़"]),
 ("6_rock_open","और फिर चट्टान पूरी हट गई, और वो तीनों चलकर बाहर निकल आए।",["पूरी"]),
 ("6_rock_open","ये हदीस सहीह बुख़ारी और सहीह मुस्लिम में अब्दुल्लाह इब्ने उमर रज़ियल्लाहु अन्हु से आई है।",[]),
]
P = ["push_in","pan_right","pull_out","pan_left"]
M = "shared/music/noor/River_Flute.mp3"
lines = [{"n":i+1,"text":t,"img":im,"motion":True,"preset":P[i%4],"overlay":[["dust",0.08]],"sfx":[],"amb":[],"music":M,"ayah":False,"gold":g} for i,(im,t,g) in enumerate(L)]
cfg = {"title":"Teen musafir aur gufa (sample)","voice":"Charon",
 "style":"Calm, warm, clear Hindi storyteller. Simple spoken Hindi, gentle emotion, normal conversational pace, correct Urdu sounds.",
 "tempo":1.0,"ambience":"shared/sfx/history/wind_desert_675710.mp3","music":M,"music_vol":0.5,"amp":0.08,"amb_db":-6,"sfx_db":-3,"duck":True,"lines":lines}
(S/"script.json").write_text(json.dumps(cfg,ensure_ascii=False,indent=1),encoding="utf-8")
(S/"audio").mkdir(exist_ok=True); (S/"output").mkdir(exist_ok=True)
