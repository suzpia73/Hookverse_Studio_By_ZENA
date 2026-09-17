from PIL import Image

# 1. Text color picker
im_text = Image.open(r"C:\Users\june2\.gemini\antigravity-ide\brain\6f64338c-c4bf-4316-a1b8-3503cde43325\.user_uploaded\media_1789624771679.png")
print("Text Color Picker size:", im_text.size)

# Let's find the checkmark or selected swatch
# In text picker: bottom preset has a checked box (purple)
# Also row 2 column 7 has a checkmark
# Let's inspect the checked swatch colors in text picker:
# Find purple pixels in bottom row of popup
for y in range(im_text.height - 50, im_text.height - 10):
    for x in range(10, 150):
        r, g, b = im_text.getpixel((x, y))[:3]
        if r > 100 and b > 150 and g < 60:
            print(f"Text selected purple: R={r}, G={g}, B={b} (# {r:02X}{g:02X}{b:02X})")
            break

# 2. Outline picker
im_out = Image.open(r"C:\Users\june2\.gemini\antigravity-ide\brain\6f64338c-c4bf-4316-a1b8-3503cde43325\.user_uploaded\media_1789624791180.png")
print("Outline Picker size:", im_out.size)
# In outline picker, black box is checked at bottom, and slider says 5
# Also row 3 column 10 (white swatch) has a checkmark?
# Let's find checkmark in outline picker:
for y in range(im_out.height):
    for x in range(im_out.width):
        # checkmark is white on dark, or dark on light
        pass

# Also let's inspect the actual subtitle text "1997년 11월" in media_1789624267612.png
im_sub = Image.open(r"C:\Users\june2\.gemini\antigravity-ide\brain\6f64338c-c4bf-4316-a1b8-3503cde43325\.user_uploaded\media_1789624267612.png")
print("Subtitle preview image size:", im_sub.size)
