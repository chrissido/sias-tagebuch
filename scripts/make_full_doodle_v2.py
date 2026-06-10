from PIL import Image
import os

img_path = r"C:\Users\csido\AppData\Local\hermes\profiles\lumi\image_cache\img_3f0a27da5160.jpg"
out_dir = r"D:\Sias Tagebuch\assets\doodles"
os.makedirs(out_dir, exist_ok=True)

img = Image.open(img_path).convert("RGBA")
w, h = img.size
print(f"Original: {w}x{h}")

# Ziel: Hochformat (9:16) für Handys, aber auch für Desktop geeignet
# Das Bild ist 1280x853 (3:2 Querformat). Wir machen es quadratisch
# mit transparentem Rand oben und unten
target_w = 1000
target_h = 1400  # Etwa 5:7, gut für beide Formate

# Skalieren auf Zielbreite
scale = target_w / w
new_w = target_w
new_h = int(h * scale)
img_resized = img.resize((new_w, new_h), Image.LANCZOS)

# Neues Bild mit transparentem Hintergrund
canvas = Image.new("RGBA", (target_w, target_h), (255, 255, 255, 0))
# Zentriert einfügen
y_offset = (target_h - new_h) // 2
canvas.paste(img_resized, (0, y_offset), img_resized)

pixels = canvas.load()

# Bunte Farben in 5x7 Zonen
cols, rows = 5, 7
cell_w, cell_h = target_w // cols, target_h // rows

palette = [
    (210, 140, 160), (180, 155, 200), (155, 185, 140), (155, 175, 210), (215, 165, 125),
    (170, 145, 195), (145, 190, 170), (195, 175, 135), (200, 145, 130), (130, 175, 195),
    (205, 195, 145), (195, 155, 175), (205, 155, 130), (150, 185, 200), (185, 165, 145),
    (220, 190, 150), (210, 140, 160), (180, 155, 200), (155, 185, 140), (155, 175, 210),
    (215, 165, 125), (170, 145, 195), (145, 190, 170), (195, 175, 135), (200, 145, 130),
    (130, 175, 195), (205, 195, 145), (195, 155, 175), (205, 155, 130), (150, 185, 200),
    (185, 165, 145), (220, 190, 150), (210, 140, 160), (180, 155, 200), (155, 185, 140),
]

for y in range(target_h):
    for x in range(target_w):
        r, g, b, a = pixels[x, y]
        if a == 0:
            continue  # Transparent lassen
        
        brightness = (r + g + b) / 3.0
        zone_col = min(x // cell_w, cols - 1)
        zone_row = min(y // cell_h, rows - 1)
        zone_idx = zone_row * cols + zone_col
        base_color = palette[zone_idx % len(palette)]
        
        if brightness > 225:
            pixels[x, y] = (255, 255, 255, 0)
        elif brightness > 200:
            intensity = 1.0 - (brightness / 255.0)
            factor = 0.15
            nr = int(base_color[0] * factor + r * (1 - factor))
            ng = int(base_color[1] * factor + g * (1 - factor))
            nb = int(base_color[2] * factor + b * (1 - factor))
            pixels[x, y] = (max(0, min(255, nr)), max(0, min(255, ng)), max(0, min(255, nb)), 120)
        else:
            intensity = 1.0 - (brightness / 255.0)
            nr = int(base_color[0] - (base_color[0] - 60) * min(1.0, intensity * 1.2))
            ng = int(base_color[1] - (base_color[1] - 60) * min(1.0, intensity * 1.2))
            nb = int(base_color[2] - (base_color[2] - 60) * min(1.0, intensity * 1.2))
            pixels[x, y] = (max(0, min(255, nr)), max(0, min(255, ng)), max(0, min(255, nb)), 255)

output_path = os.path.join(out_dir, "full_doodle.png")
canvas.save(output_path)
print(f"✅ Neues Doodle: {target_w}x{target_h}")
print(f"   Gespeichert: {output_path}")
