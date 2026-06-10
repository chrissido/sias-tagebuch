import json

with open("D:\\Sias Tagebuch\\momente.json", "r", encoding="utf-8") as f:
    data = json.load(f)

# All corrections based on actually seeing the images
corrections = {
    51: "Nach dem Planschen auf der Terrasse - Sia im flauschigen Stitch-Bademantel, die Locken noch feucht. Sommer, Sonne, beste Laune.",
    52: "Sia als Einhorn - der Sperrbildschirm von Papas Handy. Ein Laecheln fuer jeden Blick aufs Telefon, Feierabend um 19:55.",
    53: "Gemeinsam auf dem Balkon - ein Spielzeug-Laubblaeser wird zum Familienprojekt. Sia hilft kräftig mit, den Griff fest in der Hand.",
    54: "Mitten im Spielzeugparadies - Baukloetze und Stifte ueberall. Sia thront neugierig im Zentrum und schaut, was die Welt zu bieten hat.",
    55: "Sia auf dem Holzpferd mit echtem Ledersattel - im Stall, zwischen Eimern und Pferdedecken. Ein erster Ausflug in die Reiterwelt.",
    56: "Noch einmal auf dem Holzpferd - sicher gehalten, den Schnuller im Mund. Stallluft und Abenteuer fuer eine kleine Reiterin.",
    57: "Sia im Puppenwagen - lila und silbern, fast wie eine kleine Prinzessin auf dem Weg zur naechsten Entdeckung.",
    58: "Captain Fun ruft! Im Kinder-Auto durch die Mall - Leopardenjacke, Lenkrad und ein Laecheln, das keine Muenze braucht.",
    59: "Sia auf dem Sofa im Blümchenkleid - den Schnuller im Mund, die Locken frisch gekämmt. Ein ruhiger Moment daheim.",
    60: "Den Puppenwagen selbst schieben - stolz und konzentriert marschiert Sia den Gehweg entlang. Ganz die Grosse.",
    61: "Neugeboren und friedlich - Sia schlaeft tief und fest, eingekuschelt in weiche Tücher. Die Welt kann warten.",
    62: "Mama haelt Sia im Arm - beide lächeln, die ersten Wochen voller Naehe und Vertrauen.",
    63: "Papa mit Sia auf dem Arm - ein ruhiger Blick zwischen zwei Menschen, die sich gerade erst kennenlernen.",
    64: "Papa in der Küche, Sia im Arm - der Kaffee dampft, das Baby schaut. Alltag mit Neugeborenen.",
    65: "Sia ueber der Schulter - ein neugieriger Blick in die Kamera, die Welt von oben entdecken.",
    66: "Drei Wochen alt - der erste Meilenstein. Sia liegt auf dem Schoss und zeigt stolz die runde Holztafel.",
    67: "Sia in der Babywanne - warmes Wasser, sanfte Haende. Ein erstes Bad voller Vertrauen.",
    68: "Baden mit beiden Haenden - Sia wird liebevoll gewaschen, das Wasser spiegelt die Ruhe des Moments.",
    69: "Sia in der Babywippe - angeschnallt und zufrieden, die grossen Augen neugierig auf die Welt gerichtet.",
    70: "Cousin und Neugeborene - ein stolzes Laecheln neben der schlafenden Sia. Die erste Begegnung ist voller Zärtlichkeit.",
    71: "Papa haelt Sia am Fenster - das Tageslicht umarmt die beiden. Ein stiller Moment im Krankenhaus.",
    72: "Mama lächelt, Sia schaut - ein Porträt voller Liebe und neuer Vertrautheit.",
    73: "Neugeboren und wach - Sia liegt auf dem Ruecken und mustert die Welt mit grossen, dunklen Augen.",
    74: "Drei Kinder auf dem Sofa - die Cousins und Sia. Ein Vorgeschmack auf viele gemeinsame Abenteuer.",
    75: "Mama haelt Sia auf dem Sofa - schlafend und geborgen, die Decke kuschelig warm.",
    76: "Papa im Ellesse-Pullover mit Sia im Arm - ein zufriedener Blick, der alles sagt.",
    77: "Sia auf der rosa Strickdecke - der kleine Körper ruht, die Äuglein sind bereit fuer die naechste Entdeckung.",
    78: "Oma haelt Sia im gruenen Strickpullover - eine Hand voller Zärtlichkeit, ein Blick voller Stolz.",
    79: "Mama mit Einhorn-Fingerpuppe - Sia schlaeft friedlich im Arm, waehrend die kleine Fantasie tanzt.",
    80: "Sia auf dem Wickeltisch - frisch eingecremt, die Haut glaenzt. Ein Moment der Pflege und Ruhe.",
    81: "Mama und Sia im Garten - die Sonne scheint, Planschbecken und Sandmuschel warten. Sommer daheim.",
    82: "Mama lächelt mit Sia auf dem Schoss - vor der Tür der Garten, im Herzen die Sonne.",
    83: "Mama haelt Sia, beide lachen - in der Hand das Handy, im Blick das Glück.",
    84: "Sia in der Bauchlage - die Ärmchen gestützt, der Blick neugierig. Das Training fuer die grosse Freiheit.",
    85: "Opa haelt Sia auf der Terrasse - warm eingepackt, den Schnuller im Mund. Ein ruhiger Nachmittag zu zweit.",
    86: "Papa mit Sia - beide lächeln in die Kamera. Ein Porträt voller Wärme und Vertrauen.",
    87: "Sia auf der Spielmatte mit Beissring - zufrieden und entspannt, die Welt erkunden im Liegen.",
    88: "Vier Monate alt - der runde Meilenstein auf der Brust. Sia liegt stolz auf der Spielmatte.",
    89: "Vier Monate - noch einmal festgehalten. Ein kleiner Mensch waechst und wird von sanften Haenden begleitet.",
    90: "Zusammen auf der Decke im Garten - Sia und ihr Cousin geniessen die frische Luft und das weiche Gras.",
    91: "Papa mit Tattoo und Sia im Blümchenkleid - der Alltag ist bunt, wenn man ein Baby im Arm hat.",
    92: "Mama haelt Sia vor dem Fernseher - ein ruhiger Moment zu Hause, einfach beieinander sein.",
    93: "Wange an Wange - Mama und Sia teilen einen stillen Augenblick voller Zuneigung und Vertrautheit.",
    94: "Sia in der Babywippe am Hochstuhl - neugierig und wach, die Welt aus einer neuen Perspektive.",
    95: "Mama mit Sia in der Küche - helles Licht, gruene Blaetter vor dem Fenster. Ein warmer Vormittag.",
    96: "Auf der Terrasse - Mama haelt Sia, das Gruen leuchtet im Hintergrund. Sommerluft und Zufriedenheit.",
    97: "Sia mit gelbem Schnuller auf dem Bett - ein buntes Stofftier in der Hand, die Welt erkunden im Liegen.",
    98: "Sia mit der Duschgel-Flasche - ein Badartikel wird zum Spielzeug. Alltagskreativitaet im Kinderzimmer.",
    99: "Sia im Kinderwagen - angeschnallt und zufrieden, bereit fuer den naechsten Spaziergang.",
    100: "Sia auf dem Ruecken - die grossen Augen schauen direkt in die Kamera. Friedlich und unschuldig.",
    101: "Sia mit Gänseblümchen im Haar - ein Spaziergang im Gruenen, der Schnuller im Mund, die Welt ist schön.",
    102: "Videoanruf mit Papa - Sia zeigt stolz die Zunge, waehrend Papa im kleinen Fenster lächelt.",
    103: "Sia im Kinderwagen mit buntem Beissring - warm eingepackt fuer die frische Luft. Unterwegs mit Stil.",
    104: "Sia haelt ihre Fuesse - ein klassischer Babymoment, voller Flexibilitaet und Entdeckerfreude.",
    105: "Sia auf dem Wickeltisch - der Mund leicht geoeffnet, die Augen voller Neugier. Ein stiller Morgengruss.",
    106: "Sia im rosa Kleid vor dem Kinderwagen - draussen sitzen und die Welt beobachten.",
    107: "Mama haelt Sia im Arm - ein leises Lachen, ein warmes Zuhause.",
    108: "Sia vor dem Gitterbett - die kleinen Haende bereit, die naechste Etappe zu erklimmen.",
    109: "Oma spielt mit Sia - bunte Spielsachen auf dem Boden, eine Handvoll Zuneigung.",
    110: "Sia auf der Spielmatte - grosse Augen, neugieriger Blick. Die Welt ist voller Farben und Formen.",
    111: "Ein Erwachsener beugt sich ueber Sia - im hellen Zimmer teilen zwei Menschen einen innigen Augenblick.",
    112: "Sia auf der Spielmatte - greift nach der Kamera, will die Welt anfassen und begreifen.",
    113: "Zwei Haende voller Liebe - Sia wird gehalten, waehrend ein Familienmitglied Guck-guck spielt.",
    114: "Sias Mund im Nahaufnahme - die ersten Zähnchen oder ein kleiner Schnupfen. Ein Dokument der Babyzeit.",
    115: "Mama mit Sia und einem Cousin auf dem Teppich - zwei Schnuller, eine Menge Naehe.",
    116: "Sia vor dem Gitterbett - die Locken fliegen, die Augen leuchten. Ein Vormittag voller Energie.",
    117: "Sia im lila Trainingsanzug - konzentriert auf der Spielmatte, die Haare zu einem kleinen Knoten gebunden.",
    118: "Sia auf allen Vieren - umgeben von Spielzeug, die Welt wird jeden Tag ein Stück groesser.",
    119: "Oma haelt Sia auf dem Schoss - Sia greift nach einer Hand, die immer fuer sie da ist.",
    120: "Opa im Krankenhausbett reicht Sia die Hand - ein Moment, der zaehlt. Drei Generationen, eine Geste.",
    121: "Oma und Mama mit Sia - im gemütlichen Zimmer, umgeben von Liebe und Geborgenheit.",
    122: "Opa im Bett haelt Sias Hand - Mama steht daneben. Ein Bild voller Sanftmut und Zusammenhalt.",
    123: "Sia auf dem Teppich mit Papas Handy - Latzhose, Strickjacke und ein neugieriger Blick zur Seite.",
    124: "Sia krabbelt auf dem Teppich - die kleine Strickjacke, die konzentrierte Miene. Unterwegs im Wohnzimmer.",
    125: "Oma und Mama mit Sia auf dem Bett - Snacks aus der Dose, drei Generationen, ein gluecklicher Moment.",
    126: "Papa haelt Sia vor dem Fenster - Weihnachtsdeko funkelt im Hintergrund. Vorfreude auf das Fest.",
    127: "Oma und Sia, Stirn an Stirn - ein stiller Augenblick voller Zuneigung und Vertrauen.",
    128: "Sia im Tiger-Schlafanzug - die grossen Augen schauen wach in die Kamera. Zwei Zähnchen blitzen hervor.",
}

# Apply corrections
count = 0
for e in data:
    if e["id"] in corrections and e.get("bild"):
        old = e["beschreibung"]
        e["beschreibung"] = corrections[e["id"]]
        count += 1
        print(f'#{e["id"]}: ✅ Korrigiert')
        print(f'   ALT: {old[:60]}...')
        print(f'   NEU: {e["beschreibung"][:60]}...')
        print()

print(f"\n=== {count} Beschreibungen aktualisiert ===")

with open("D:\\Sias Tagebuch\\momente.json", "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)

print("✅ momente.json gespeichert")
