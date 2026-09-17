from PIL import Image

im = Image.open(r"C:\Users\june2\.gemini\antigravity-ide\brain\6f64338c-c4bf-4316-a1b8-3503cde43325\.user_uploaded\media_1789621841268.png")
for x in range(330, 350):
    print(f"x={x}: {im.getpixel((x, 50))}")
