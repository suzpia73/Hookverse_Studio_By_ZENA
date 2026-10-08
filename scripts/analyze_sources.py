import os
from PIL import Image

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"

film_path = os.path.join(WORKSPACE, "assets", "images", "raw_film_source.jpg")
text_path = os.path.join(WORKSPACE, "assets", "images", "raw_text_source.jpg")
banner_path = os.path.join(WORKSPACE, "assets", "HOOKVERSE_공식_3대_브랜딩_완제품", "01_유튜브_공식채널배너_2560x1440_QHD마스터.png")

print("Checking banner text area:")
banner = Image.open(banner_path)
print("Banner size:", banner.size)

film = Image.open(film_path)
print("Film size:", film.size)

text = Image.open(text_path)
print("Text size:", text.size)
