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
}


def pitch_filter(semitones: float, sr: int = 24000) -> str | None:
    """FFmpeg filter that shifts pitch but keeps duration."""
    if not semitones:
        return None
    f = 2 ** (semitones / 12)
    return f"asetrate={sr * f:.0f},aresample={sr},atempo={1 / f:.5f}"
