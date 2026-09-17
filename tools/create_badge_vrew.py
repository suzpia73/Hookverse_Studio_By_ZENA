import os
from PIL import Image, ImageDraw, ImageFont

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
font_path = os.path.join(WORKSPACE, "assets", "fonts", "FontdinerSwanky-Regular.ttf")

# 브루 캡처 비율과 동일하게: 가로 340, 세로 125
W, H = 340, 125
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 브루의 쨍한 로열블루 직사각형 배경 (#005BEA / rgb(0, 91, 234))
blue_color = (0, 91, 234, 255)
draw.rectangle([0, 0, W, H], fill=blue_color)

# 폰트 로드 (Fontdiner Swanky Regular)
font_size = 44
font = ImageFont.truetype(font_path, font_size)

text_line1 = "Hookverse"
text_line2 = "Studio"

# 텍스트 바운딩 박스 측정
bbox1 = draw.textbbox((0, 0), text_line1, font=font)
w1 = bbox1[2] - bbox1[0]
h1 = bbox1[3] - bbox1[1]

bbox2 = draw.textbbox((0, 0), text_line2, font=font)
w2 = bbox2[2] - bbox2[0]
h2 = bbox2[3] - bbox2[1]

line_spacing = 6
total_text_height = h1 + line_spacing + h2

# 오빠의 지침: 좌우 여백을 상하 여백(약 14px)처럼 타이트하게 줄여서 컴팩트하게!
pad_y = 14
pad_x = 18  # 상하 여백과 균형을 맞춘 타이트한 좌우 여백

max_w = max(w1, w2)
W = int(max_w + pad_x * 2)
H = int(total_text_height + pad_y * 2)

# 새 이미지 생성
img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
draw = ImageDraw.Draw(img)

# 브루의 쨍한 로열블루 직사각형 (#005BEA)
blue_color = (0, 91, 234, 255)
draw.rectangle([0, 0, W, H], fill=blue_color)

# 가운데 정렬 (Center aligned)
x1 = (W - w1) // 2
x2 = (W - w2) // 2
start_y = pad_y - 2

draw.text((x1, start_y), text_line1, fill=(255, 255, 255, 255), font=font)
draw.text((x2, start_y + h1 + line_spacing), text_line2, fill=(255, 255, 255, 255), font=font)

out_p = os.path.join(WORKSPACE, "assets", "images", "hookverse_top_left_badge.png")
img.save(out_p, "PNG")
print(f"[+] ✅ Vrew 컴팩트 배지 생성 완료: W={W}, H={H}, 저장위치: {out_p}")
