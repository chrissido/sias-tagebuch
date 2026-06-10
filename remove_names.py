#!/usr/bin/env python3
"""Remove all names/roles from momente.json descriptions - replace with generic terms."""
import json
import re
import os

MOMENTE_FILE = "D:/Sias Tagebuch/momente.json"

with open(MOMENTE_FILE, "r", encoding="utf-8") as f:
    momente = json.load(f)

# Mapping: name -> replacement (context-aware)
replacements = {
    "Mama": "ein Familienmitglied",
    "Papa": "ein Familienmitglied",
    "Oma": "ein Familienmitglied",
    "Opa": "ein Familienmitglied",
    "Timo": "jemand",
    "Tante Melly": "jemand",
    "Vanessa": "jemand",
    "Johannes": "jemand",
    "Leano": "ein Kind",
    "Levi": "ein Kind",
    "Lias": "ein Kind",
    "Mark": "jemand",
}

# Sort by length descending so longer names match first
sorted_names = sorted(replacements.keys(), key=len, reverse=True)

changes = 0
for entry in momente:
    old_desc = entry.get("beschreibung", "")
    if not old_desc:
        continue
    
    new_desc = old_desc
    for name in sorted_names:
        # Replace "Name und" -> "jemand und", "Name" -> "jemand" etc.
        new_desc = re.sub(r'\b' + re.escape(name) + r'\b', replacements[name], new_desc)
    
    # Clean up grammar: "ein Familienmitglied und ein Familienmitglied" -> "zwei Familienmitglieder"
    new_desc = re.sub(r'ein Familienmitglied und ein Familienmitglied', 'zwei Familienmitglieder', new_desc)
    new_desc = re.sub(r'ein Kind und ein Kind', 'zwei Kinder', new_desc)
    new_desc = re.sub(r'ein Familienmitglied und ein Kind', 'jemand mit', new_desc)
    new_desc = re.sub(r'ein Kind und ein Familienmitglied', 'jemand mit', new_desc)
    new_desc = re.sub(r'ein Kind', 'jemand', new_desc)
    new_desc = re.sub(r'zwei Kinder', 'zwei Kinder', new_desc)  # keep
    
    # Remove "in den Armen von jemand" -> "in jemandes Armen"
    new_desc = re.sub(r'in den Armen von jemand', 'in liebevollen Armen', new_desc)
    # "von jemand" at end of sentence
    new_desc = re.sub(r'von jemand\.', '.', new_desc)
    # "jemand und Sia" -> "Sia und jemand" (prettier)
    new_desc = re.sub(r'^jemand und Sia', 'Sia und jemand', new_desc)
    
    if new_desc != old_desc:
        entry["beschreibung"] = new_desc
        changes += 1
    
    # Remove personen array
    if "personen" in entry:
        del entry["personen"]

with open(MOMENTE_FILE, "w", encoding="utf-8") as f:
    json.dump(momente, f, ensure_ascii=False, indent=2)

print(f"✅ {changes} Beschreibungen bereinigt (Namen entfernt)")
print(f"📝 Alle {len(momente)} Einträge jetzt anonymisiert")
