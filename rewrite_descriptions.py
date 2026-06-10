#!/usr/bin/env python3
"""Rewrite all momente.json descriptions with personalized, warm texts."""
import json
import os
import sys

BASE_DIR = "D:/Sias Tagebuch"
MOMENTE_FILE = os.path.join(BASE_DIR, "momente.json")
RESULTS_FILE = os.path.join(BASE_DIR, "face_scan_results.json")

def load_json(path):
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)

def get_person_names(faces, entry, context_clues):
    """Extract meaningful person names from face recognition results with context clues."""
    names = set()
    for f in faces:
        p = f.get("person", "")
        conf = f.get("confidence", 0)
        # Only trust good confidence matches
        if conf >= 50:
            names.add(p)
    
    # Context clues from titel, ort, autor
    titel = entry.get("titel", "").lower()
    ort = entry.get("ort", "").lower()
    autor = entry.get("autor", "").lower()
    desc = entry.get("beschreibung", "").lower()
    
    # Context-based fallbacks for photos where face rec didn't identify adults
    if "geburt" in titel or "erste stunde" in titel or "erstes mal" in titel:
        if "krankenhaus" in ort:
            if len(names) <= 1:  # Only Sia detected
                names.add("Mama")
                if "papa" in titel or "christian" in autor:
                    names.add("Papa")
    
    if "mutter" in desc or "erschöpft" in desc:
        names.add("Mama")
    
    if "opa" in titel or "opa" in desc:
        names.add("Opa")
    if "oma" in titel or "oma" in desc or "enkelin" in desc:
        names.add("Oma")
    
    if "papa" in titel or "vater" in desc or "papa" in autor.lower():
        names.add("Papa")
    
    if "timo" in titel.lower() or "timo" in autor.lower():
        names.add("Timo")
    
    if "rote" in desc and "schal" in desc:
        names.add("Oma")  # Context: likely Oma besucht
    
    if "mel" in desc or "tante" in desc:
        names.add("Tante Melly")
    
    # Ensure Sia is always included
    names.add("Sia")
    
    # Clean up - remove if confidence was too low for some
    return sorted(names, key=lambda x: (x != "Sia", x))  # Put non-Sia first

def write_warm_description(entry, person_names):
    """Write a warm, personal description based on entry context and detected people."""
    titel = entry.get("titel", "")
    ort = entry.get("ort", "")
    datum = entry.get("datum", "")
    typ = entry.get("typ", "")
    bild = entry.get("bild")
    # Remove emoji-heavy stuff from titel for analysis
    clean_titel = titel.replace("🎂", "").replace("🌸", "").replace("🎉", "").strip()
    
    # Get adults (non-Sia)
    adults = [p for p in person_names if p not in ("Sia", "Lias", "Leano", "Levi")]
    kids = [p for p in person_names if p in ("Lias", "Leano", "Levi")]
    
    # For entries without images
    if not bild or bild == "null":
        if typ == "baby":
            return {
                "beschreibung": "Sia ist da! Ein kleiner Mensch erobert die Herzen im Sturm.",
                "personen": ["Sia"]
            }
    
    if typ == "meilenstein":
        milestones = {
            "Das erste Lächeln": "Verschlafen, aber eindeutig – Sias erstes Lächeln. Ein kleines Zucken der Mundwinkel, das die ganze Welt heller macht.",
            "6 Monate": "Sia kann sitzen! Stolz und wackelig thront sie aufrecht und entdeckt die Welt aus einer neuen Perspektive.",
            "Die ersten Zähne": "Zwei kleine, spitze Zähnchen schieben sich durch das Zahnfleisch. Sia erkundet die Welt jetzt auch mit dem Mund.",
            "Erster Geburtstag": "Ein Jahr ist vergangen. Sia pustet zum ersten Mal eine Kerze aus – mit Hilfe von Mama und Papa.",
            "Erster Frühlingsausflug": "Die Sonne scheint, die Vögel zwitschern. Sia erlebt ihren ersten Frühling im Park.",
            "Die ersten Schritte": "Unsicher, aber mutig – Sia löst sich von der Couch und macht ihre ersten eigenen Schritte. Ein großer Moment.",
        }
        for key, text in milestones.items():
            if key.lower() in clean_titel.lower():
                return {"beschreibung": text, "personen": person_names}
    
    # For entries with images
    bild = entry.get("bild")
    if not bild or bild == "null":
        # No image - use titel context
        if "geburtstag" in typ:
            return {
                "beschreibung": "Ein Jahr voller erster Male – Sia feiert ihren Geburtstag umgeben von ihrer Familie.",
                "personen": person_names
            }
        return {"beschreibung": "", "personen": person_names}
    
    # Build description from context
    desc_parts = []
    
    # Who's in the photo
    if adults:
        adult_names = " und ".join(adults)
        if kids:
            kid_names = " und ".join(kids)
            if len(person_names) == 2:
                desc_parts.append(f"{adult_names} mit Sia")
            else:
                desc_parts.append(f"{adult_names} mit {kid_names} und Sia")
        else:
            if len(person_names) == 1:
                desc_parts.append("Sia")
            elif len(person_names) <= 3:
                desc_parts.append(f"{adult_names} mit Sia")
            else:
                desc_parts.append(f"{adult_names} umgeben von Sia")
    elif kids:
        if len(kids) == 1:
            desc_parts.append(f"{kids[0]} und Sia")
        else:
            desc_parts.append(f"{', '.join(kids[:-1])} und {kids[-1]} mit Sia")
    else:
        desc_parts.append("Sia")
    
    # When / where
    time_context = ""
    if "frühling" in clean_titel.lower() or "april" in datum:
        time_context = "einem warmen Frühlingstag"
    elif "sommer" in clean_titel.lower() or datum.endswith(("06", "07", "08")):
        time_context = "einem sonnigen Sommertag"
    elif "dezember" in datum or "winter" in clean_titel.lower():
        time_context = "einem ruhigen Wintertag"
    elif "mai" in datum:
        time_context = "einem lauen Maitag"
    else:
        time_context = "einem friedlichen Nachmittag"
    
    # Specific beautiful descriptions per ID
    special_descs = {
        8: f"Sia kuschelt mit {adults[0] if adults else 'jemand'} in der Hängematte – die Welt schaukelt sanft, der Himmel ist blau. Ein lauter Nachmittag voller Vertrauen.",
        9: f"Sia auf der Schaukel – den Schnuller im Mund, die Locken im Wind. Sie lacht, während {adults[0] if adults else 'jemand'} sie vorsichtig anschubst.",
        10: f"Sia und {adults[0] if adults else 'ein Familienmitglied'} beim Mittagsschlaf – erschöpft, glücklich, geborgen. Zwei Menschen, ein Rhythmus.",
        11: f"{kids[0] if kids else 'Leano'} und Sia auf dem grünen Sofa – zwei kleine Freunde, die die Welt noch ganz langsam erkunden.",
        12: f"{kids[0] if kids else 'Lias'} und Sia kuscheln auf dem Sofa. Mehr Nähe geht nicht.",
        13: f"{adults[0] if adults else 'Mama'} hält Sia zum ersten Mal im Arm – die Nabelschnur durchtrennt, die Verbindung für immer. Ein neues Leben, ganz nah am Herzen.",
        14: f"Ein erster Besuch im Krankenhaus: {kids[0] if kids else 'jemand'} trifft Sia zum ersten Mal und hält sie ganz vorsichtig im Arm.",
        15: f"{kids[0] if kids else 'jemand'} und Sia – ganz verzaubert von der Kleinen.",
        16: "Sia schläft friedlich in ihrem Bettchen – ein zufriedenes Neugeborenes, geborgen in weiße Tücher gewickelt.",
        17: f"{adults[0] if adults else 'Vanessa'} besucht Sia im Krankenhaus – hält die Neugeborene vorsichtig im Arm, eine erste Begegnung voller Zärtlichkeit.",
        18: f"{adults[0] if adults else 'Oma'} hält Sia auf dem Arm, eingekuschelt in die flauschige Regenbogendecke. Sias erster Nachmittag zu Hause.",
        19: "Sia wird auf einem Spaziergang auf dem Rücken getragen – weite Felder, blauer Himmel, ein friedlicher Ausflug.",
        20: f"Sia zwischen {adults[0] if len(adults) > 0 else 'Mama'} und {adults[1] if len(adults) > 1 else 'Papa'} auf dem Bett, die rosa Trinklernflasche in der Hand – alle drei lachen um die Wette.",
        21: f"Sia auf dem hellen Cord-Sofa, umgeben von ihren Cousins {kids[0] if kids else 'Leano'} und {kids[1] if len(kids) > 1 else 'Levi'}. Ein gemütlicher Nachmittag voller Geschwisterliebe.",
        22: "Sia auf der beigen Spielmatte – bunte Tiere und Zahlen umgeben sie. Stolz hält sie ein Holzspielzeug in den Händen.",
        23: "Mit beiden Händen umklammert Sia einen großen Knochen und knabbert voller Hingabe daran – eine echte Gourmet-Momentchen.",
        24: f"Stirn an Stirn – {adults[0] if adults else 'Timo'} hält Sia ganz nah bei sich. Beide in weißen Shirts, Sias Blick neugierig.",
        25: f"{adults[0] if adults else 'Papa'} hält Sia zum ersten Mal im Arm – neugeboren und winzig, in hellblaues Tuch gewickelt. Der erste Besuch im Krankenhaus.",
        26: f"{adults[0] if adults else 'Papa'} hält Sia im Arm, ihr kleines Gesicht ganz nah an seiner Brust. Geborgenheit von der ersten Stunde an.",
        27: "Sia, noch ganz frisch auf der Welt, liegt wach im Arm – die Äuglein offen, neugierig. Ein ruhiger Moment am ersten Tag.",
        28: "Sia schläft tief, eingekuschelt in eine weiche Decke. Ein friedlicher Moment – die Welt da draußen zählt nicht.",
        29: f"{adults[0] if adults else 'Oma'} und {adults[1] if len(adults) > 1 else 'Opa'} schauen voller Zärtlichkeit auf das Neugeborene. Die erste Begegnung mit Sia – stilles Glück.",
        30: f"{adults[0] if adults else 'Mama'} schläft tief, das Neugeborene an ihre Brust gekuschelt. Haut an Haut, ganz nah – die Strapazen der Geburt weichen stiller Verbundenheit.",
        31: f"Neugeboren und friedlich – Sia schlummert in den Armen von {adults[0] if adults else 'Mama'}. Ein stiller Moment voller Vertrauen.",
        32: "Winzig und zufrieden liegt Sia da, die Äuglein fest geschlossen. Die Welt ist noch so neu und geborgen.",
        33: f"{adults[0] if adults else 'Mama'} lächelt müde und glücklich, die kleine Sia an ihre Schulter geschmiegt. Mutter und Kind, ganz bei sich.",
        34: "Sia schlummert friedlich im weißen Strampler, die Händchen an die Brust gelegt. Sanftes Licht, weiche Decken – die Welt ist noch ganz klein.",
        35: "Ein heller Raum mit Regenbogenvorhang und weißer Wiege. Alles bereit für Sia, die hier groß werden darf.",
        36: "Eingekuschelt in die flauschige weiße Wiege – Sia schläft den tiefsten Schlaf unter der Regenbogen-Decke.",
        37: f"{adults[0] if adults else 'Oma'} sitzt am Holztisch und hält das Neugeborene ganz vorsichtig. Die erste Begegnung mit ihrer Enkelin.",
        38: f"{adults[0] if adults else 'Papa'} hält Sia nah bei sich, eingewickelt in die kuschelige Decke. Familie von der ersten Stunde an.",
        39: f"{adults[0] if adults else 'Oma'} mit rotem Schal besucht Sia zu Hause – die Kleine schläft zufrieden auf dem hellen Cord-Sofa.",
        40: f"{adults[0] if adults else 'Oma'} im roten Schal, Sia schlafend in ihren Armen. Ein stiller, glücklicher Nachmittag von oben betrachtet.",
        41: f"{adults[0] if adults else 'Papa'} strahlt über das ganze Gesicht, die kleine Sia im Arm. Ein glücklicher Vatermoment auf dem Sofa.",
        42: f"Leano beugt sich neugierig vor und schaut sich das Neugeborene an. Sia liegt sicher im Arm von {adults[0] if adults else 'Mama'}.",
        43: "Leano betrachtet Sia mit großen Augen, ganz fasziniert von der Winzigen.",
        44: "Leano schaut Sia an, als wäre sie das spannendste Wesen der Welt.",
        45: f"Levi lacht über das ganze Gesicht, als er Sia zum ersten Mal sieht – ein strahlender Cousin.",
        46: f"In der blauen Babywanne, vorsichtig gewaschen von {adults[0] if adults else 'Mama'} – Sia genießt das warme Wasser.",
        47: "Das erste Bauchlage-Training – in weiß-blau gepunktetem Strampler liegt Sia auf der kuscheligen Decke.",
        48: f"{adults[0] if adults else 'Tante Melly'} hält Sia liebevoll im Arm, goldener Schmuck funkelt. Ein friedlicher Moment.",
        49: f"Sia liegt bei {adults[0] if adults else 'Mama'}, beide ganz ruhig. Der Blick voller Liebe und Staunen.",
        50: "Mit herausgestreckter Zunge schaut Sia zufrieden – frech und glücklich zugleich. Ein erster kleiner Charaktermoment.",
    }
    
    if entry["id"] in special_descs:
        return {"beschreibung": special_descs[entry["id"]], "personen": person_names}
    
    # Generic warm description
    scene = f"Ein {time_context}."
    if ort:
        scene += f" {ort.capitalize()}."
    
    return {
        "beschreibung": f"{', '.join(person_names)}. {scene}",
        "personen": person_names
    }

def main():
    momente = load_json(MOMENTE_FILE)
    face_results = load_json(RESULTS_FILE)
    
    changes = 0
    for entry in momente:
        eid = entry["id"]
        sid = str(eid)
        result = face_results.get(sid, {})
        
        faces = result.get("faces", [])
        context_clues = {"titel": entry.get("titel", ""), "ort": entry.get("ort", "")}
        person_names = get_person_names(faces, entry, context_clues)
        
        new_data = write_warm_description(entry, person_names)
        
        old_desc = entry.get("beschreibung", "")
        new_desc = new_data["beschreibung"]
        new_personen = new_data["personen"]
        
        if new_desc and new_desc != old_desc:
            entry["beschreibung"] = new_desc
            changes += 1
        
        # Update personen array
        entry["personen"] = new_personen
    
    with open(MOMENTE_FILE, "w", encoding="utf-8") as f:
        json.dump(momente, f, ensure_ascii=False, indent=2)
    
    print(f"\n✅ {changes} Beschreibungen aktualisiert!")
    print(f"📝 Alle 50 Einträge personalisiert.")

if __name__ == "__main__":
    main()
