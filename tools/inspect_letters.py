from PIL import Image

im = Image.open(r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\vrew_sub_crop.png").convert("RGB")
w, h = im.size

# Let's inspect the pixels of the digits '1997'
# In this crop, the digits are around y=30 to 55, x=50 to 120
print("Sample pixels across vertical slice through digit '1' around x=58:")
for y in range(25, 55):
    r, g, b = im.getpixel((58, y))
    print(f"y={y}: R={r:3d}, G={g:3d}, B={b:3d} -> ", end="")
    if r > 220 and g > 220 and b > 220:
        print("WHITE (Fill)")
    elif r > 100 and b > 140 and g < 100:
        print("PURPLE (Outline/Stroke)")
    elif r < 60 and g < 60 and b < 60:
        print("BLACK (Outer Border/Shadow)")
    else:
        print(f"Other ({r},{g},{b})")
