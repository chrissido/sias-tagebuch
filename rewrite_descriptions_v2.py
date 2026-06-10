#!/usr/bin/env python3
"""Rewrite all momente.json descriptions with warm, poetic texts - no names, no 'jemand', no 'Familienmitglied'."""
import json
import os

MOMENTE_FILE = "D:/Sias Tagebuch/momente.json"

with open(MOMENTE_FILE, "r", encoding="utf-8") as f:
    momente = json.load(f)

# Hand-crafted beautiful descriptions per entry ID
new_descs = {
    # No image milestones
    1: "Sia ist da! Ein kleiner Mensch erobert die Herzen im Sturm.",
    2: "Verschlafen, aber eindeutig – Sias erstes Lächeln. Ein kleines Zucken der Mundwinkel, das die ganze Welt heller macht.",
    3: "Die Sonne scheint, die Vögel zwitschern – Sia erlebt ihren ersten Frühling. Ein Ausflug in den Park, die Welt ist voller Farben.",
    4: "Sia kann sitzen! Stolz und wackelig thront sie aufrecht und entdeckt die Welt aus einer neuen Perspektive.",
    5: "Zwei kleine, spitze Zähnchen schieben sich durch das Zahnfleisch. Sia erkundet die Welt jetzt auch mit dem Mund.",
    6: "Ein Jahr ist vergangen – Sia pustet ihre erste Kerze aus. Ein Kreis von Menschen, die sie lieben, singt ihr ein Lied.",
    7: "Unsicher, aber mutig – Sia löst sich von der Couch und macht ihre ersten eigenen Schritte. Ein großer Moment.",
    
    # Images - atmospheric, no names
    8: "Sia liegt in der Hängematte und schaukelt sanft – über ihr der blaue Himmel, um sie herum das leise Rascheln der Blätter. Ein friedlicher Nachmittag im Garten.",
    9: "Sia auf der Schaukel – den Schnuller im Mund, die Locken im Wind. Sie lacht und schwingt sich leicht durch die Luft.",
    10: "Mittagsschlaf auf dem Sofa. Zwei Menschen, ein Rhythmus – Sias Atem wird ruhig, die Welt um sie herum verstummt.",
    11: "Zwei kleine Entdecker auf dem grünen Sofa – sie teilen sich die Welt, die noch so groß und neu ist.",
    12: "Ganz dicht beieinander auf dem Sofa – Sia und ein kleiner Freund, mehr Nähe geht nicht.",
    13: "Ein neues Leben liegt in sanften Händen – winzig, warm, frisch auf der Welt. Die erste Umarmung: vorsichtig, ehrfürchtig, für immer.",
    14: "Erster Besuch im Krankenhaus – zwei Hände, die ganz vorsichtig das Neugeborene halten, als wäre es das Kostbarste der Welt. Ist es auch.",
    15: "Die erste Begegnung – Sia wird angeschaut, als wäre sie das Wunderbarste, was es je gab.",
    16: "Sia schläft friedlich in ihrem Bettchen – rundum zufrieden, in weiße Tücher gewickelt. Ein Neugeborenes in seiner ganzen Ruhe.",
    17: "Besuch im Krankenhaus – ein Gesicht voller Zärtlichkeit beugt sich über das Neugeborene. Sia schläft, die Welt ist gut.",
    18: "Sias erster Nachmittag zu Hause – eingekuschelt in die flauschige Regenbogendecke, sicher und geborgen.",
    19: "Weite Felder, blauer Himmel – Sia wird auf einem Spaziergang durch die Landschaft getragen. Ein friedlicher Sommertag.",
    20: "Alle drei auf dem Bett – Sia in der Mitte, die rosa Trinklernflasche in der Hand. Drei Menschen, ein Moment, ganz viel Lachen.",
    21: "Sia auf dem hellen Cord-Sofa, umgeben von ihren Cousins. Drei kleine Köpfe, die zusammen die Welt entdecken.",
    22: "Sia auf der Spielmatte – bunte Tiere und Zahlen umgeben sie. Stolz hält sie ein Holzspielzeug in den Händen und schaut zufrieden in die Kamera.",
    23: "Mit beiden Händen umklammert Sia einen großen Knochen und knabbert voller Hingabe daran – ein Gourmet-Momentchen erster Klasse.",
    24: "Stirn an Stirn, ganz nah – Sia in starken Armen, die sie festhalten, als wollten sie diesen Moment für immer bewahren.",
    25: "Neugeboren und winzig, in hellblaues Tuch gewickelt – Sia wird zum ersten Mal im Arm gehalten. Der erste Besuch im Krankenhaus.",
    26: "Ganz nah an der Brust, das kleine Gesicht an warme Haut geschmiegt. Geborgenheit von der ersten Stunde an.",
    27: "Sia, noch ganz frisch auf der Welt, liegt wach und neugierig. Die Äuglein offen, bereit, alles zu entdecken.",
    28: "Tief und fest – Sia schläft, eingekuschelt in eine weiche Decke. Die Welt da draußen zählt nicht. Nur dieser eine Moment.",
    29: "Zwei Menschen beugen sich voller Zärtlichkeit über das Neugeborene. Die erste Begegnung – stilles Glück, das den Raum erfüllt.",
    30: "Haut an Haut, ganz nah – zwei Körper, die die Erschöpfung der Geburt und die Wärme des Anfangs teilen. Stille Verbundenheit.",
    31: "Neugeboren und friedlich – Sia schlummert in liebevollen Armen. Ein stiller Moment voller Vertrauen und Wärme.",
    32: "Winzig und zufrieden liegt Sia da – die Äuglein fest geschlossen. Die Welt ist noch so neu und voller Geborgenheit.",
    33: "Ein müdes, glückliches Lächeln – die kleine Sia an die Schulter geschmiegt. Zwei Menschen, ganz bei sich. So beginnt Liebe.",
    34: "Sia schlummert friedlich im weißen Strampler, die Händchen an die Brust gelegt. Sanftes Licht, weiche Decken – die Welt ist noch ganz klein.",
    35: "Ein heller Raum mit Regenbogenvorhang und weißer Wiege. Alles bereit für das neue Leben, das hier groß werden darf.",
    36: "Eingekuschelt in die flauschige Wiege – Sia schläft den tiefsten Schlaf unter der Regenbogen-Decke.",
    37: "Vorsichtig wird das Neugeborene am Holztisch gehalten – eine erste Begegnung, die von Staunen und Zärtlichkeit erzählt.",
    38: "Eingewickelt in die kuschelige Decke – Sia liegt nah bei einem Menschen, der sie von der ersten Stunde an liebt.",
    39: "Zu Besuch auf dem hellen Cord-Sofa – Sia schläft zufrieden, während eine warme Hand sie hält.",
    40: "Ein stiller Nachmittag von oben betrachtet – Sia schlafend in liebevollen Armen, ein roter Schal leuchtet im Licht.",
    41: "Stolz und Freude – ein glücklicher Moment auf dem Sofa. Sia im Arm, das Herz voll.",
    42: "Ein neugieriges Gesicht beugt sich vor, ganz fasziniert von dem Winzling. Sia liegt sicher in der Mitte der Aufmerksamkeit.",
    43: "Zwei kleine Augen schauen Sia an – eine erste Begegnung, die den Anfang einer besonderen Freundschaft markiert.",
    44: "Völlig fasziniert – Sia ist das spannendste Wesen auf der ganzen Welt. Und das ist sie ja auch.",
    45: "Ein breites Grinsen, als Sia zum ersten Mal gesehen wird – Freude pur. So schön, wenn das Herz vor Glück überläuft.",
    46: "In der blauen Babywanne – Sia genießt ihr erstes Bad. Warmes Wasser, sanfte Hände, ein wohliger Seufzer.",
    47: "Das erste Bauchlage-Training – im weiß-blau gepunkteten Strampler liegt Sia auf der kuscheligen Decke und schaut neugierig in die Welt.",
    48: "Goldener Schmuck funkelt im Licht, während Sia liebevoll im Arm gehalten wird. Ein friedlicher Moment der Nähe.",
    49: "Sia liegt ruhig da – der Blick, der auf ihr ruht, ist voller Liebe und Staunen. Mehr braucht es nicht.",
    50: "Mit herausgestreckter Zunge schaut Sia zufrieden – frech und glücklich zugleich. Ein erster kleiner Charaktermoment.",
}

for entry in momente:
    eid = entry["id"]
    if eid in new_descs:
        entry["beschreibung"] = new_descs[eid]

with open(MOMENTE_FILE, "w", encoding="utf-8") as f:
    json.dump(momente, f, ensure_ascii=False, indent=2)

print(f"✅ Alle {len(new_descs)} Beschreibungen neu geschrieben")
print("📝 Keine Namen, kein 'jemand', kein 'Familienmitglied'")
