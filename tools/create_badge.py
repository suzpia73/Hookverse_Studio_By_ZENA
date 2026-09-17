import os
from PIL import Image, ImageDraw, ImageFont

W, H = 340, 110
img = Image.new('RGBA', (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 글래스모피즘 파란색 배경 (로열 블루 / 딥 네이비)
draw.rounded_rectangle([4, 4, W-4, H-4], radius=16, fill=(10, 30, 68, 235), outline=(56, 189, 248, 220), width=3)

# 은은한 하이라이트 라인
draw.line([16, 10, W-16, 10], fill=(255, 255, 255, 80), width=1)

# 폰트 로드
font_path = r'C:\Windows\Fonts\malgunbd.ttf'
if not os.path.exists(font_path):
    font_path = r'C:\Windows\Fonts\arialbd.ttf'

f_top = ImageFont.truetype(font_path, 34)
f_bot = ImageFont.truetype(font_path, 28)

# 두 줄 텍스트: HOOKVERSE / STUDIO (하얀색 굵은 글씨)
draw.text((W//2, 33), 'HOOKVERSE', fill=(255, 255, 255, 255), font=f_top, anchor='mm')
draw.text((W//2, 75), 'STUDIO', fill=(224, 242, 254, 245), font=f_bot, anchor='mm')

out_p = r'D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\hookverse_top_left_badge.png'
img.save(out_p, 'PNG')
print(f'Successfully created badge: {out_p}, size={os.path.getsize(out_p)}')
