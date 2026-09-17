from PIL import Image

im = Image.open(r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\vrew_sub_crop.png").convert("RGB")
w, h = im.size

purple_pixels = []
for y in range(h):
    for x in range(w):
        r, g, b = im.getpixel((x, y))
        if b > 140 and r > 100 and g < 100:
            purple_pixels.append((x, y, r, g, b))

print(f"Found {len(purple_pixels)} purple pixels in subtitle crop!")
if purple_pixels:
    sample = purple_pixels[:10]
    for p in sample:
        print(f"  x={p[0]}, y={p[1]}: RGB=({p[2]},{p[3]},{p[4]}) -> #{p[2]:02X}{p[3]:02X}{p[4]:02X}")
