from PIL import Image

p = r"C:\Users\june2\.gemini\antigravity-ide\brain\6f64338c-c4bf-4316-a1b8-3503cde43325\.user_uploaded\media_1789621841268.png"
im = Image.open(p).convert("RGBA")
W, H = im.size

# Video top is at y=25
video_top = 25

# Let's inspect columns at y=50 across X from 0 to W
print("Inspecting columns across X at y=50:")
for x in range(W):
    pix = im.getpixel((x, 50))
    # print first 20 and last 20 columns
    if x < 15 or x > W - 15:
        print(f"x={x:03d}: {pix}")
