import os
from PIL import Image

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"

# 1. raw_text_source bbox of non-black pixels
text = Image.open(os.path.join(WORKSPACE, "assets", "images", "raw_text_source.jpg")).convert("RGBA")
# find bounding box where rgb is not near black (e.g. max(r,g,b) > 20)
gray = text.convert("L")
bbox = gray.point(lambda p: 255 if p > 25 else 0).getbbox()
print("raw_text_source text bbox:", bbox)

# 2. banner text area
# banner is 2560x1440, let's inspect the center area (around x: 600..1800, y: 400..1000)
banner = Image.open(os.path.join(WORKSPACE, "assets", "HOOKVERSE_공식_3대_브랜딩_완제품", "01_유튜브_공식채널배너_2560x1440_QHD마스터.png"))
# The safezone is 1546x423 in the center (x: 507..2053, y: 508..931)
print("Banner center sample ok")
