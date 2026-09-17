from PIL import Image

im = Image.open(r"C:\Users\june2\.gemini\antigravity-ide\brain\6f64338c-c4bf-4316-a1b8-3503cde43325\.user_uploaded\media_1789624267612.png")
# Subtitle is in the bottom of the video preview on left
# In this 1024x576 image, video is around x=30 to x=210, y=100 to y=420
# Let's crop around x=30..220, y=360..430
crop = im.crop((30, 360, 215, 430))
crop.save(r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\vrew_sub_crop.png")
print("Subtitle crop saved.")
