#!/usr/bin/env python3
"""Rewrite all titles in momente.json to be beautiful and poetic."""
import json

MOMENTE_FILE = "D:/Sias Tagebuch/momente.json"

with open(MOMENTE_FILE, "r", encoding="utf-8") as f:
    momente = json.load(f)

new_titles = {
    1: "Sia ist da! 🌸",
    2: "Das erste Lächeln",
    3: "Erster Frühlingsausflug",
    4: "Endlich sitzen!",
    5: "Die ersten Zähnchen",
    6: "Erster Geburtstag! 🎂",
    7: "Die ersten Schritte",
    8: "In der Hängematte",
    9: "Auf der Schaukel",
    10: "Gemeinsam träumen",
    11: "Zwei kleine Entdecker",
    12: "Beste Freunde",
    13: "Die erste Stunde",
    14: "Erster Besuch",
    15: "Ganz verzaubert",
    16: "Tief und fest",
    17: "Erste Begegnung",
    18: "Angekommen",
    19: "Spaziergang auf dem Land",
    20: "Rundum glücklich",
    21: "Cousinen-Liebe",
    22: "Auf der Spielmatte",
    23: "Der große Knabberspaß",
    24: "Stirn an Stirn",
    25: "Erster Besuch im Krankenhaus",
    26: "Ganz nah",
    27: "Neugierig auf die Welt",
    28: "Tiefe Ruhe",
    29: "Erster Besuch – ganz nah",
    30: "Erschöpft und glücklich",
    31: "In liebevollen Armen",
    32: "Geborgen in weichen Tüchern",
    33: "Mutterglück",
    34: "Tief und fest",
    35: "Das Babyzimmer",
    36: "In der Wiege",
    37: "Ganz vorsichtig",
    38: "Erste Vertrautheit",
    39: "Zu Besuch",
    40: "Nachmittag auf dem Sofa",
    41: "Stolz wie nie",
    42: "Ganz neugierig",
    43: "Die erste Begegnung",
    44: "Völlig fasziniert",
    45: "Ein großes Grinsen",
    46: "Sias erstes Bad",
    47: "Bauchlage",
    48: "Ganz nah",
    49: "Ein besonderer Moment",
    50: "Sia zeigt Zunge",
}

for entry in momente:
    eid = entry["id"]
    if eid in new_titles:
        entry["titel"] = new_titles[eid]

with open(MOMENTE_FILE, "w", encoding="utf-8") as f:
    json.dump(momente, f, ensure_ascii=False, indent=2)

print(f"✅ Alle {len(new_titles)} Titel neu geschrieben!")
