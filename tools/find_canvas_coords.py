import os
from PIL import Image

p = r"C:\Users\june2\.gemini\antigravity-ide\brain\6f64338c-c4bf-4316-a1b8-3503cde43325\.user_uploaded\media_1789621841268.png"
im = Image.open(p).convert("RGBA")
W, H = im.size
print(f"Image size: {W}x{H}")

# Print first 35 rows average RGB
for y in range(35):
    pixels = [im.getpixel((x, y))[:3] for x in range(W)]
    r_avg = sum(p[0] for p in pixels) / W
    g_avg = sum(p[1] for p in pixels) / W
    b_avg = sum(p[2] for p in pixels) / W
    print(f"y={y:02d}: R={r_avg:.1f}, G={g_avg:.1f}, B={b_avg:.1f}")
