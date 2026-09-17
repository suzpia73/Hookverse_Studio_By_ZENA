import os
from PIL import Image, ImageDraw

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
src_logo = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo.png")
dst_logo = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo_transparent.png")

img = Image.open(src_logo).convert("RGBA")
W, H = img.size
cx, cy = W // 2, H // 2

# 원형 엠블럼의 외곽 테두리 반지름 측정
img_rgb = Image.open(src_logo).convert("RGB")

r_candidates = []
# 상방향에서 금색 림 탐색
for y in range(50, cy):
    r, g, b = img_rgb.getpixel((cx, y))
    if r > 50 and g > 40:
        r_candidates.append(cy - y)
        break

# 하방향에서 금색 림 탐색
for y in range(H - 50, cy, -1):
    r, g, b = img_rgb.getpixel((cx, y))
    if r > 50 and g > 40:
        r_candidates.append(y - cy)
        break

# 좌방향에서 금색 림 탐색
for x in range(50, cx):
    r, g, b = img_rgb.getpixel((x, cy))
    if r > 50 and g > 40:
        r_candidates.append(cx - x)
        break

# 우방향에서 금색 림 탐색
for x in range(W - 50, cx, -1):
    r, g, b = img_rgb.getpixel((x, cy))
    if r > 50 and g > 40:
        r_candidates.append(x - cx)
        break

radius = sum(r_candidates) // len(r_candidates) + 3
print(f"[*] 원형 엠블럼 감지 반지름: {radius}px (지름: {radius*2}px)")

# 완벽한 4x 슈퍼샘플링 안티앨리어싱 정원 마스크 생성
scale = 4
mask_large = Image.new("L", (W * scale, H * scale), 0)
draw_large = ImageDraw.Draw(mask_large)

# 정원 그리기
cx_l, cy_l = cx * scale, cy * scale
r_l = radius * scale
draw_large.ellipse([cx_l - r_l, cy_l - r_l, cx_l + r_l, cy_l + r_l], fill=255)

# 리샘플링으로 초고품질 부드러운 안티앨리어싱 경계 생성
mask = mask_large.resize((W, H), Image.Resampling.LANCZOS)

# 원본 이미지에 마스크 결합 (내부는 100% 원본 보존, 외부는 100% 투명)
clean_img = img.copy()
clean_img.putalpha(mask)

# 원형 영역으로 바짝 크롭 (정사각형 원형 뱃지)
crop_box = (cx - radius, cy - radius, cx + radius, cy + radius)
cropped_logo = clean_img.crop(crop_box)

# 저장
cropped_logo.save(dst_logo, "PNG")
print(f"[+] ✅ 완벽한 정원 누끼 엠블럼 생성 완료: {dst_logo} (크기: {cropped_logo.size})")
