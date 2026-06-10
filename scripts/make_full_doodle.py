from PIL import Image
import os

img_path = r"C:\Users\csido\AppData\Local\hermes\profiles\lumi\image_cache\img_3f0a27da5160.jpg"
out_dir = r"D:\Sias Tagebuch\assets\doodles"
os.makedirs(out_dir, exist_ok=True)

img = Image.open(img_path).convert("RGBA")
w, h = img.size
print(f"Original: {w}x{h}")

# Auf 900px Breite skalieren
target_w = 900
scale = target_w / w
new_w = target_w
new_h = int(h * scale)
img = img.resize((new_w, new_h), Image.LANCZOS)
print(f"Skaliert: {new_w}x{new_h}")

pixels = img.load()

# Farbpalette für verschiedene Zonen - warme Baby-Pastelltöne
# Aufgeteilt in 4x4 Zonen
cols, rows = 4, 4
cell_w, cell_h = new_w // cols, new_h // rows

palette = [
    (210, 140, 160),  # Altrosa
    (180, 155, 200),  # Flieder
    (155, 185, 140),  # Salbeigrün
    (155, 175, 210),  # Hellblau
    (215, 165, 125),  # Pfirsich
    (170, 145, 195),  # Lavendel
    (145, 190, 170),  # Minze
    (195, 175, 135),  # Goldgelb
    (200, 145, 130),  # Koralle
    (130, 175, 195),  # Taubenblau
    (205, 195, 145),  # Zitrone
    (195, 155, 175),  # Rosé
    (205, 155, 130),  # Aprikose
    (150, 185, 200),  # Seegrün
    (185, 165, 145),  # Creme
    (220, 190, 150),  # Vanille
]

for y in range(new_h):
    for x in range(new_w):
        r, g, b, a = pixels[x, y]
        brightness = (r + g + b) / 3.0
        
        # Bestimme welche Zone
        zone_col = x // cell_w
        zone_row = y // cell_h
        zone_idx = zone_row * cols + zone_col
        if zone_idx >= len(palette):
            zone_idx = zone_idx % len(palette)
        
        base_color = palette[zone_idx]
        
        if brightness > 225:
            # Weißer Hintergrund -> transparent
            pixels[x, y] = (255, 255, 255, 0)
        elif brightness > 200:
            # Sehr helle Bereiche leicht farbig
            intensity = 1.0 - (brightness / 255.0)
            factor = 0.15
            nr = int(base_color[0] * factor + r * (1 - factor))
            ng = int(base_color[1] * factor + g * (1 - factor))
            nb = int(base_color[2] * factor + b * (1 - factor))
            pixels[x, y] = (max(0, min(255, nr)), max(0, min(255, ng)), max(0, min(255, nb)), 120)
        else:
            # Linien mit voller Farbe
            intensity = 1.0 - (brightness / 255.0)
            nr = int(base_color[0] - (base_color[0] - 60) * min(1.0, intensity * 1.2))
            ng = int(base_color[1] - (base_color[1] - 60) * min(1.0, intensity * 1.2))
            nb = int(base_color[2] - (base_color[2] - 60) * min(1.0, intensity * 1.2))
            pixels[x, y] = (max(0, min(255, nr)), max(0, min(255, ng)), max(0, min(255, nb)), 200)

# Alte Einzel-Doodles löschen, nur full_doodle behalten
for f in os.listdir(out_dir):
    fp = os.path.join(out_dir, f)
    if os.path.isfile(fp) and f != "full_doodle.png":
        os.remove(fp)

output_path = os.path.join(out_dir, "full_doodle.png")
img.save(output_path)
print(f"✅ Buntes Gesamt-Doodle erstellt: {output_path}")
print(f"   Größe: {new_w}x{new_h}")
print(f"   Farben: Rosa, Lila, Grün, Blau, Pfirsich, Lavendel, Minze, Gold...")
