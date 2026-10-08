import os
from PIL import Image, ImageEnhance, ImageFilter

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"

files = [
    os.path.join(WORKSPACE, "assets", "images", "raw_film_source.jpg"),
    os.path.join(WORKSPACE, "assets", "images", "raw_text_source.jpg"),
    os.path.join(WORKSPACE, "assets", "HOOKVERSE_공식_3대_브랜딩_완제품", "01_유튜브공식채널배너_2560x1440_QHD마스터.png"),
    os.path.join(WORKSPACE, "assets", "HOOKVERSE_공식_3대_브랜딩_완제품", "02_좌상단시네마틱배지_1024p_마스터.png")
]

for f in files:
    if os.path.exists(f):
        im = Image.open(f)
        print(os.path.basename(f), im.size, im.mode)
    else:
        print(os.path.basename(f), "NOT FOUND")
