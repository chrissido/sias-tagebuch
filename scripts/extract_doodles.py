from PIL import Image
import os

img_path = r"C:\Users\csido\AppData\Local\hermes\profiles\lumi\image_cache\img_3f0a27da5160.jpg"
out_dir = r"D:\Sias Tagebuch\assets\doodles"
os.makedirs(out_dir, exist_ok=True)

img = Image.open(img_path).convert("RGBA")
w, h = img.size
print(f"Bildgröße: {w}x{h}")

# Das Bild hat ungefähr 4 Spalten x 4 Zeilen Doodles
cols, rows = 4, 4
cell_w, cell_h = w // cols, h // rows

# Farbpalette für die Doodles (Pastelltöne)
colors = [
    (180, 120, 140),  # Rosé
    (160, 190, 140),  # Salbei
    (190, 160, 120),  # Gold
    (130, 160, 180),  # Himmelblau
    (190, 140, 160),  # Altrosa
    (150, 170, 150),  # Minze
    (200, 170, 130),  # Creme
    (170, 150, 180),  # Lavendel
    (140, 180, 170),  # Seegrün
    (180, 150, 130),  # Pfirsich
    (160, 140, 160),  # Flieder
    (200, 190, 140),  # Zitrone
]

count = 0
cropped = []

for row in range(rows):
    for col in range(cols):
        margin = 15
        x1, y1 = col * cell_w + margin, row * cell_h + margin
        x2, y2 = (col+1) * cell_w - margin, (row+1) * cell_h - margin
        if x2 > w or y2 > h:
            continue
            
        crop = img.crop((x1, y1, x2, y2))
        pixels = crop.load()
        
        # Weißen Hintergrund transparent machen + prüfen ob Inhalt da
        has_content = False
        for py in range(crop.height):
            for px in range(crop.width):
                r, g, b, a = pixels[px, py]
                if r > 235 and g > 235 and b > 235:
                    pixels[px, py] = (255, 255, 255, 0)
                else:
                    has_content = True
        
        if not has_content:
            continue
            
        # Farbe anwenden - schwarze Linien durch Pastellfarbe ersetzen
        color = colors[count % len(colors)]
        for py in range(crop.height):
            for px in range(crop.width):
                r, g, b, a = pixels[px, py]
                if a > 255:
                    a = 255
                if a > 0:
                    gray = (r + g + b) / 3.0
                    intensity = gray / 255.0
                    # Farbig machen
                    nr = int(color[0] * (1.0 - intensity * 0.6) + r * intensity * 0.2)
                    ng = int(color[1] * (1.0 - intensity * 0.6) + g * intensity * 0.2)
                    nb = int(color[2] * (1.0 - intensity * 0.6) + b * intensity * 0.2)
                    pixels[px, py] = (max(0, min(nr, 255)), max(0, min(ng, 255)), max(0, min(nb, 255)), 255)
        
        # Besseren Namen geben
        names = [
            "herz", "stern", "hase", "brief",
            "wolke", "kamera", "sonne", "blume",
            "geschenk", "gluehbirne", "krone", "eis",
            "ballon", "ente", "croissant", "herzfluegel"
        ]
        fname = f"{names[count] if count < len(names) else f'doodle_{count}'}.png"
            
        # Automatisch zuschneiden (entferne leere Ränder)
        crop.save(os.path.join(out_dir, fname))
        cropped.append((fname, col, row, crop.size))
        count += 1
        print(f"Doodle {count}: {fname} bei ({col},{row}) - {crop.size}")

print(f"\nInsgesamt {count} Doodles erstellt in {out_dir}")
