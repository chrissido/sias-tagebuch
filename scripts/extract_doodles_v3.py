from PIL import Image, ImageEnhance
import os

img_path = r"C:\Users\csido\AppData\Local\hermes\profiles\lumi\image_cache\img_3f0a27da5160.jpg"
out_dir = r"D:\Sias Tagebuch\assets\doodles"
os.makedirs(out_dir, exist_ok=True)

img = Image.open(img_path).convert("RGBA")
w, h = img.size
print(f"Bildgröße: {w}x{h}")

cols, rows = 4, 4
cell_w, cell_h = w // cols, h // rows

# Bunte Pastellfarben - jede Farbe für einen Doodle
# (r, g, b) - schöne kräftige Pastelltöne
palette = [
    (220, 120, 140),  # Rosa
    (200, 160, 220),  # Lila
    (160, 200, 140),  # Salbeigrün
    (140, 180, 220),  # Himmelblau
    (220, 170, 120),  # Pfirsich
    (180, 140, 200),  # Lavendel
    (220, 140, 120),  # Koralle
    (160, 210, 180),  # Mint
    (200, 180, 130),  # Goldgelb
    (130, 180, 200),  # Taubenblau
    (210, 150, 170),  # Altrosa
    (170, 200, 160),  # Pistazie
    (200, 160, 130),  # Creme
    (150, 190, 200),  # Seegrün
    (220, 190, 150),  # Aprikose
    (190, 150, 180),  # Flieder
]

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
        
        # Farbe für diesen Doodle
        cr, cg, cb = palette[count % len(palette)]
        
        has_content = False
        for py in range(crop.height):
            for px in range(crop.width):
                r, g, b, a = pixels[px, py]
                brightness = (r + g + b) / 3.0
                if brightness > 225:
                    pixels[px, py] = (255, 255, 255, 0)  # transparent
                else:
                    has_content = True
                    # Original-Helligkeit beibehalten, aber Farbe ersetzen
                    intensity = 1.0 - (brightness / 255.0)
                    # Linien werden farbig: je dunkler das Original, desto mehr Farbe
                    nr = int(cr - (cr - 60) * intensity * 0.7)
                    ng = int(cg - (cg - 60) * intensity * 0.7)
                    nb = int(cb - (cb - 60) * intensity * 0.7)
                    pixels[px, py] = (max(0, min(nr, 255)), max(0, min(ng, 255)), max(0, min(nb, 255)), 255)

        if not has_content:
            continue
        
        # Automatisch zuschneiden
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
        
        pad = 10
        x1_c = max(0, min_x - pad)
        y1_c = max(0, min_y - pad)
        x2_c = min(crop.width, max_x + pad)
        y2_c = min(crop.height, max_y + pad)
        crop = crop.crop((x1_c, y1_c, x2_c, y2_c))
        
        fname = f"{names[count] if count < len(names) else f'doodle_{count}'}.png"
        crop.save(os.path.join(out_dir, fname))
        count += 1
        print(f"Doodle {count}: {fname} - Farbe rgb({cr},{cg},{cb}) ({crop.size[0]}x{crop.size[1]})")

print(f"\n✅ {count} bunte Doodles erstellt!")
