import json
import random
import urllib.request
from datetime import datetime, timedelta, timezone

DATA_FILE = "data/content.json"

# Pre-curated bilingual batches for Day 6, Day 7, Day 8...
CURATED_BATCHES = [
    # Day 6
    {
        "vocab": [
            {"type": "OWS", "word": "Omnipotent", "meaning": "सर्वशक्तिमान (Having unlimited or universal power)", "important": True},
            {"type": "OWS", "word": "Omnipresent", "meaning": "सर्वव्यापी (Present everywhere at the same time)", "important": False},
            {"type": "OWS", "word": "Omniscient", "meaning": "सर्वज्ञ (Knowing everything)", "important": True},
            {"type": "OWS", "word": "Optimist", "meaning": "आशावादी (One who looks at the bright side of things)", "important": False},
            {"type": "OWS", "word": "Pacifist", "meaning": "शांतिवादी (A person who believes that war and violence are unjustifiable)", "important": True},
            {"type": "OWS", "word": "Panacea", "meaning": "रामबाण औषधि (A solution or remedy for all difficulties or diseases)", "important": True},
            {"type": "OWS", "word": "Pedestrian", "meaning": "पैदल यात्री (A person walking along a road or in a developed area)", "important": False},
            {"type": "OWS", "word": "Philanthropist", "meaning": "मानवप्रेमी / परोपकारी (A person who seeks to promote the welfare of others)", "important": True},
            {"type": "OWS", "word": "Plagiarism", "meaning": "साहित्यिक चोरी (Copying another person's work or ideas as one's own)", "important": True},
            {"type": "OWS", "word": "Polyglot", "meaning": "बहुभाषी (A person who knows and is able to use several languages)", "important": True},
            {"type": "Idiom", "word": "A piece of cake", "meaning": "बहुत आसान काम (Something very easy to do)", "important": False},
            {"type": "Idiom", "word": "Add insult to injury", "meaning": "जले पर नमक छिड़कना (Make a bad situation even worse)", "important": True},
            {"type": "Idiom", "word": "At a snail's pace", "meaning": "बहुत धीमी गति से (Very slowly)", "important": False},
            {"type": "Idiom", "word": "Bolt from the blue", "meaning": "अचानक आई मुसीबत (An unexpected and shocking event)", "important": True},
            {"type": "Idiom", "word": "Burn bridges", "meaning": "वापसी के सारे रास्ते बंद करना (Destroy relationships permanently)", "important": True},
            {"type": "Idiom", "word": "Every cloud has a silver lining", "meaning": "हर निराशा में आशा की किरण होती है (Every bad situation has some good aspect)", "important": True},
            {"type": "Idiom", "word": "In the nick of time", "meaning": "ठीक समय पर / अंतिम क्षण में (Just in time before it is too late)", "important": True},
            {"type": "Idiom", "word": "Let the cat out of the bag", "meaning": "राज़ उजागर कर देना (Reveal a secret carelessly)", "important": False},
            {"type": "Idiom", "word": "Sit on the fence", "meaning": "तटस्थ रहना / निर्णय न लेना (Avoid making a decision or taking sides)", "important": True},
            {"type": "Idiom", "word": "Take with a grain of salt", "meaning": "संदेह के साथ स्वीकार करना (Not take something completely literally)", "important": True},
            {"type": "Syn/Ant", "word": "Abstruse", "meaning": "गूढ़ / कठिन | Syn: Obscure, Complex | Ant: Clear, Lucid", "important": True},
            {"type": "Syn/Ant", "word": "Benevolent", "meaning": "दयालु | Syn: Kind, Charitable | Ant: Cruel, Malevolent", "important": False},
            {"type": "Syn/Ant", "word": "Cajole", "meaning": "फुसलाना / चापलूसी करना | Syn: Persuade, Coax | Ant: Bully, Force", "important": True},
            {"type": "Syn/Ant", "word": "Debilitate", "meaning": "दुर्बल बनाना | Syn: Weaken, Enfeeble | Ant: Strengthen, Fortify", "important": True},
            {"type": "Syn/Ant", "word": "Eloquent", "meaning": "वाक्पटु / प्रभावशाली | Syn: Fluent, Articulate | Ant: Inarticulate, Tongue-tied", "important": True},
            {"type": "Syn/Ant", "word": "Gregarious", "meaning": "मिलनसार | Syn: Sociable, Affable | Ant: Introverted, Aloof", "important": False},
            {"type": "Syn/Ant", "word": "Indolent", "meaning": "आलसी / सुस्त | Syn: Lazy, Slothful | Ant: Industrious, Diligent", "important": True},
            {"type": "Syn/Ant", "word": "Jubilant", "meaning": "उल्लासित / अति प्रसन्न | Syn: Exultant, Joyful | Ant: Despondent, Gloomy", "important": True},
            {"type": "Syn/Ant", "word": "Mundane", "meaning": "सांसारिक / साधारण | Syn: Ordinary, Routine | Ant: Extraordinary, Exciting", "important": True},
            {"type": "Syn/Ant", "word": "Transient", "meaning": "क्षणिक / अस्थायी | Syn: Temporary, Fleeting | Ant: Permanent, Enduring", "important": True}
        ],
        "passage": {
            "title": "Financial Literacy & Retail Investors",
            "text": "A surge in digital brokerage platforms has democratized access to capital markets, bringing millions of first-time retail investors into equities and mutual funds. While greater participation channels household savings into productive economic growth, impulsive trading driven by unverified social media tips poses substantial financial risk. Educating new investors on asset allocation, compounding, and risk diversification is vital to ensure sustainable wealth creation rather than speculative losses.",
            "questions": [
                {"q": "What has enabled millions of first-time retail investors to enter capital markets?", "opts": ["Free government bonds", "A surge in digital brokerage platforms", "Closure of savings accounts", "Higher bank locker fees"], "ans": 1},
                {"q": "What major risk for new investors is highlighted in the passage?", "opts": ["Low internet speed", "Impulsive trading driven by unverified social media tips", "Too many bank holidays", "Lack of stock exchanges"], "ans": 1},
                {"q": "Which word in the passage means 'based on guesswork rather than sound analysis'?", "opts": ["Productive", "Speculative", "Diversification", "Compounding"], "ans": 1}
            ]
        }
    }
]

EXTRA_WORDS = [
    "acrimonious", "affable", "alacrity", "ambiguous", "antipathy", "apathy", "audacity",
    "bellicose", "benign", "brevity", "camaraderie", "candor", "catharsis", "circumspect",
    "clemency", "coalesce", "complacent", "conundrum", "copious", "corroborate", "credulous",
    "deference", "demure", "deride", "despondent", "diatribe", "didactic", "disparage",
    "dogmatic", "duplicity", "eclectic", "edify", "efficacious", "elucidate", "empathy",
    "ennui", "equivocal", "erudite", "esoteric", "eulogy", "exacerbate", "exemplary",
    "exonerate", "expedite", "explicit", "fastidious", "fatuous", "felicity", "fervent",
    "flamboyant", "fortuitous", "frivolous", "garrulous", "gratuitous", "hackneyed", "harangue",
    "hedonist", "hegemony", "iconoclast", "idiosyncrasy", "ignominious", "immutable", "impartial",
    "impetuous", "implacable", "implicit", "impudent", "inadvertent", "incisive", "incorrigible",
    "indefatigable", "indigenous", "ineffable", "inexorable", "ingenuous", "innocuous", "insipid",
    "intrepid", "inveterate", "irascible", "juxtapose", "laconic", "lament", "laudable",
    "lethargy", "loquacious", "lugubrious", "magnanimity", "malevolent", "malleable", "mellifluous"
]

def fetch_word_details(word):
    try:
        url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
        with urllib.request.urlopen(req, timeout=8) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            m = data[0]["meanings"][0]
            defn = m["definitions"][0]["definition"]
            syns = m.get("synonyms", [])[:2]
            ants = m.get("antonyms", [])[:2]
            extra = ""
            if syns:
                extra += f" | Syn: {', '.join(syns)}"
            if ants:
                extra += f" | Ant: {', '.join(ants)}"
            return f"{defn}{extra}"
    except Exception:
        return "High-frequency SSC CGL/MTS vocabulary term (Revise usage and context)"

def main():
    with open(DATA_FILE, "r", encoding="utf-8") as f:
        content = json.load(f)

    next_day = content.get("day_count", 5) + 1
    day_label = f"Day {next_day}"
    batch_idx = next_day - 6
    existing = {v["word"].lower() for v in content["vocab"]}

    if 0 <= batch_idx < len(CURATED_BATCHES):
        batch = CURATED_BATCHES[batch_idx]
        for item in batch["vocab"]:
            if item["word"].lower() not in existing:
                row = dict(item)
                row["day"] = day_label
                content["vocab"].append(row)
        p = dict(batch["passage"])
        p["day"] = day_label
        content["passages"].append(p)
    else:
        pool = [w for w in EXTRA_WORDS if w.lower() not in existing]
        random.shuffle(pool)
        selected = pool[:15] if pool else random.sample(EXTRA_WORDS, 10)
        for idx, w in enumerate(selected):
            cat = "OWS" if idx < 5 else ("Syn/Ant" if idx < 10 else "Idiom")
            content["vocab"].append({
                "day": day_label,
                "type": cat,
                "word": w.capitalize(),
                "meaning": fetch_word_details(w),
                "important": (idx % 2 == 0)
            })

    ist = timezone(timedelta(hours=5, minutes=30))
    now_ist = datetime.now(ist).strftime("%Y-%m-%d %I:%M %p IST")
    content["day_count"] = next_day
    content["last_updated"] = now_ist

    with open(DATA_FILE, "w", encoding="utf-8") as f:
        json.dump(content, f, ensure_ascii=False, indent=2)

    print(f"Successfully updated to {day_label} at {now_ist}")

if __name__ == "__main__":
    main()
