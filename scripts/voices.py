"""Voice cast (Gemini TTS) shared by voice_samples.py and make_short.py.

character: (Gemini voice, style direction, pitch shift in semitones applied with FFmpeg afterwards)
"""
CAST = {
    "narrator": ("Charon", "Indian Hindi storyteller narrating a kids' mystery: clear, engaging, slightly dramatic, "
                           "medium pace, not rushed", 0),
    "sharma": ("Sadachbia", "fussy, upset 55-year-old Indian neighbour complaining that his brand-new bicycle was "
                            "stolen, slightly whiny, fast", 0),
    "dadi": ("Gacrux", "70-year-old Indian grandmother: warm, calm, wise, a little teasing, confident, medium pace", 0),
    "golu": ("Leda", "excited 10-year-old Indian boy, fast, over-eager, high energy, sure he is right", 0),
    "mitthu": ("Laomedeia", "a squeaky, high-pitched cartoon parrot squawking and repeating the word, very short "
                            "and sharp", 5),
    "pandey": ("Algenib", "pompous, heavy, loud Indian police inspector giving a bossy command, comic", 0),
    "pappu": ("Achird", "simple, honest village milkman, a bit nervous and defensive, friendly", 0),
    "raju": ("Zubenelgenubi", "chatty street-side chai seller, casual, then indignant at the accusation", 0),
    "bunty": ("Fenrir", "17-year-old college boy, quick and slightly too eager to give an alibi, a little nervous", 0),
    # --- long videos ---
    "dadi_story": ("Gacrux", "70-year-old Indian grandmother telling a bedtime moral story to her grandson: warm, "
                             "expressive, gentle, a little dramatic at key moments, medium pace", 0),
    # --- long_01: लालची हलवाई ---
    "ghasita": ("Alnilam", "greedy, fat old Indian sweet-shop owner with a rough, raspy, rude voice, impatient and "
                           "scornful", 0),
    "chhotu": ("Iapetus", "kind, gentle young Indian helper, soft warm voice, humble and caring", 0),
    "sadhu": ("Sadaltager", "very old, wise Indian holy man, slow, calm, slightly trembling aged voice, peaceful", 0),
    "woman": ("Aoede", "ordinary village woman buying sweets, polite and casual", 0),
    "kid": ("Autonoe", "small poor 8-year-old village boy, timid, hopeful, pleading softly", 0),
    "villager": ("Umbriel", "cheerful village man enjoying a sweet, warm and hearty", 0),
    "kids": ("Zephyr", "a group of excited village children cheering together, loud and joyful", 0),
    # --- long_02 (story 003): मिट्ठू ने सब बता दिया ---
    "raghu": ("Puck", "friendly, honest young Indian milkman, polite and a little nervous when everyone stares, natural pace", 0),
    "gupta": ("Despina", "chatty, dramatic 50-year-old Indian neighbour who loves gossip, expressive and theatrical, quick", 0),
    # --- long_03 (story 004): छत पर भूत? ---
    "mishra": ("Enceladus", "gentle, soft-spoken 70-year-old Indian man, polite, a little lonely and shy, slow and warm", 0),
    # --- Golu ki toli (permanent, 2026-10-20) ---
    "tara": ("Pulcherrima", "clever, cheerful 9-year-old Indian girl: clear, quick, bright and confident, a little bossy but warm", 0),
    # --- long_06 (story 007): बच्चों की अदालत (new keys only; the old pandey/sharma styles stay for cache keys) ---
    "pandey_soft": ("Algenib", "the same pompous Indian police inspector now whispering softly, amused, trying not to "
                               "laugh", 0),
    "sharma_fond": ("Sadachbia", "forgetful, flustered 55-year-old Indian neighbour, then laughing warmly at himself, "
                                 "friendly", 0),
    # --- cast v3 (story 008+, chosen by the user 2026-11-01 from characters/voices/cast_v3/) ---
    "tinku": ("Puck", "Speak like a real 10-year-old Indian boy: a small child's light, thin, high voice, never an adult; "
                      "clever and curious, calm, thinks before speaking, wears glasses", 4),
    "jugnu": ("Zephyr", "a tiny glowing firefly who talks: small, bright, playful and a little cheeky, quick", 0),
    "bholu": ("Fenrir", "Speak like a real 10-year-old Indian boy: a small child's light, thin, high voice, never an adult; "
                        "chubby, jolly, hasty, loves food, laughs easily", 3),
    "ira": ("Pulcherrima", "Speak like a real 10-year-old Indian girl: a small child's light, thin, high voice, never an "
                           "adult; sharp, notes everything in her notebook, clear and quick", 3),
    "titli": ("Autonoe", "Speak like a real 8-year-old Indian girl: a small child's light, thin, high voice, never an adult; "
                         "naughty, bubbly, giggly, asks question after question", 4),
    "daroga_singh": ("Algenib", "heavy, deep, booming voice of a plump 45-year-old Indian police daroga: loud and bossy, "
                                "then comically embarrassed", -1),
    "kesar_dadi": ("Vindemiatrix", "a very old 75-year-old Indian grandmother: aged, slightly shaky and breathy old-lady "
                                   "voice, slow, warm, sweet and wise, telling a story", 0),
    "tinku_mummy": ("Aoede", "loving but firm 35-year-old Indian mother at home: warm, a little strict", 0),
    "lon_chacha": ("Orus", "enthusiastic, quirky 50-year-old Indian inventor uncle: cheerful, a little dramatic, proud of his "
                           "home-made rocket, quick and warm (test voice 2026-11-01, not chosen by the user yet)", 0),
}

# Stories before cast v3 (001-007) spoke with these voices under the same speaker names; make_short swaps them in
# for those stories so old TTS caches stay valid (use_old_cast).
OLD_CAST = {
    "tinku": ("Achernar", "thin, innocent 9-year-old Indian boy: slightly thin, light voice, sweet and funny, a little shaky when scared", 0),
}
CAST_V3_FROM = 8


def use_old_cast(story_num: int) -> None:
    """Old stories get their old voices back (CAST is changed in place, so every importer sees it)."""
    if story_num and story_num < CAST_V3_FROM:
        CAST.update(OLD_CAST)


def pitch_filter(semitones: float, sr: int = 24000) -> str | None:
    """FFmpeg filter that shifts pitch but keeps duration."""
    if not semitones:
        return None
    f = 2 ** (semitones / 12)
    return f"asetrate={sr * f:.0f},aresample={sr},atempo={1 / f:.5f}"
