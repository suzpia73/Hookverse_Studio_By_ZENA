import os
from PIL import Image

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
film = Image.open(os.path.join(WORKSPACE, "assets", "images", "raw_film_source.jpg"))
W, H = film.size
print("raw_film_source:", W, H)

# Let's inspect vertical slices:
# Top rail: roughly y: 0 .. 95
# Bottom rail: roughly y: 585 .. 683
# Central area: y: 95 .. 585 (height 490)
# Emblem is roughly centered horizontally (x: 400..624) and in upper half of central area (y: 120..320)
# Old text is roughly in lower half (y: 320..500)
