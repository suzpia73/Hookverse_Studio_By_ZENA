from PIL import Image

p = r"C:\Users\june2\.gemini\antigravity-ide\brain\6f64338c-c4bf-4316-a1b8-3503cde43325\.user_uploaded\media_1789621841268.png"
im = Image.open(p).convert("RGBA")

# Let's save a crop of x=250 to 332, y=25 to 110 to see the emblem
crop = im.crop((250, 25, 332, 110))
crop.save(r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\emblem_vrew_crop.png")
print("Emblem crop saved. Size:", crop.size)

# Also crop badge
badge_crop = im.crop((6, 25, 100, 100))
badge_crop.save(r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\badge_vrew_crop.png")
print("Badge crop saved. Size:", badge_crop.size)
