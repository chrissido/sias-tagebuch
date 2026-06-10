from PIL import Image
import os

img_path = r"C:\Users\csido\AppData\Local\hermes\profiles\lumi\image_cache\img_3f0a27da5160.jpg"
out_dir = r"D:\Sias Tagebuch\assets\doodles"
os.makedirs(out_dir, exist_ok=True)

img = Image.open(img_path).convert("RGBA")
w, h = img.size
print(f"Bildgröße: {w}x{h}")

# Das Bild hat 4 Spalten x 4 Zeilen Doodles
cols, rows = 4, 4
cell_w, cell_h = w // cols, h // rows

# Namen für die Doodles
names = [
    "herz", "stern", "hase", "brief",
    "wolke", "kamera", "papierflieger", "kaffee",
    "geschenk", "gluehbirne", "krone", "blume-zweig",
    "ballon", "ente", "croissant", "herzfluegel"
]

count = 0

for row in range(rows):
    for col in range(cols):
        margin = 12
        x1, y1 = col * cell_w + margin, row * cell_h + margin
        x2, y2 = (col+1) * cell_w - margin, (row+1) * cell_h - margin
        if x2 > w or y2 > h:
            continue
        
        crop = img.crop((x1, y1, x2, y2))
        pixels = crop.load()
        
        # Prüfen ob Inhalt da + weißen Hintergrund transparent machen
        has_content = False
        for py in range(crop.height):
            for px in range(crop.width):
                r, g, b, a = pixels[px, py]
                # Alles was sehr hell ist -> transparent
                brightness = (r + g + b) / 3.0
                if brightness > 220:
                    pixels[px, py] = (255, 255, 255, 0)
                else:
                    has_content = True
                    # Original schwarze Linien leicht abdunkeln/farbstich geben
                    # Leichten Farbton hinzufügen (sehr subtil)
                    tint = 5
                    pixels[px, py] = (
                        max(0, r - tint),
                        max(0, g - tint),
                        max(0, b - tint),
                        255
                    )
        
        if not has_content:
            continue
        
        # Automatisch zuschneiden: leere Ränder entfernen
        # finde bounding box
        min_x, min_y = crop.width, crop.height
        max_x, max_y = 0, 0
        for py in range(crop.height):
            for px in range(crop.width):
                r, g, b, a = pixels[px, py]
                if a > 0:
                    min_x = min(min_x, px)
                    min_y = min(min_y, py)
                    max_x = max(max_x, px)
                    max_y = max(max_y, py)
        
        if max_x <= min_x:
            continue
            
        # Mit etwas Padding zuschneiden
        pad = 8
        x1_c = max(0, min_x - pad)
        y1_c = max(0, min_y - pad)
        x2_c = min(crop.width, max_x + pad)
        y2_c = min(crop.height, max_y + pad)
        crop = crop.crop((x1_c, y1_c, x2_c, y2_c))
        
        fname = f"{names[count] if count < len(names) else f'doodle_{count}'}.png"
        crop.save(os.path.join(out_dir, fname))
        count += 1
        print(f"Doodle {count}: {fname} ({crop.size[0]}x{crop.size[1]})")

print(f"\n✅ {count} Doodles erstellt mit transparentem Hintergrund")
print(f"   Ordner: {out_dir}")
