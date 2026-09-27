import os
from PIL import Image, ImageDraw

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
src_logo = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo.png")
dst_logo1 = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo_transparent.png")
dst_logo2 = os.path.join(WORKSPACE, "assets", "HOOKVERSE_공식_3대_브랜딩_완제품", "03_공식원형앰블럼_636x636_투명HQ.png")

img = Image.open(src_logo).convert("RGBA")
W, H = img.size

# 수학적으로 100% 완벽한 정원 중심점 및 반지름 설정 (오차 0.0px)
# 실측 금색 림: X=[81, 709](너비 628), Y=[77, 703](높이 626) -> 중심: (395, 390)
cx = 395.0
cy = 390.0
radius = 314.0  # 직경 628px 1:1 완전 정원

# 1. 1차 4x 슈퍼샘플링 정원 마스크
scale = 4
mask_large = Image.new("L", (W * scale, H * scale), 0)
draw_large = ImageDraw.Draw(mask_large)
draw_large.ellipse([(cx - radius) * scale, (cy - radius) * scale, (cx + radius) * scale, (cy + radius) * scale], fill=255)
circle_mask = mask_large.resize((W, H), Image.Resampling.LANCZOS)

# 2. 픽셀 단위 정밀 분리 (안팎 100% 투명화)
result_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

for y in range(H):
    for x in range(W):
        c_val = circle_mask.getpixel((x, y))
        c_alpha = c_val[0] if isinstance(c_val, tuple) else (c_val or 0)
        if c_alpha == 0:
            continue
        
        px = img.getpixel((x, y))
        if isinstance(px, tuple) and len(px) >= 3:
            r, g, b = px[0], px[1], px[2]
        else:
            continue
        
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        saturation = max_c - min_c
        brightness = max_c
        
        # 검은 배경 판정 (어둡고 채도가 낮은 픽셀)
        if brightness < 48 and saturation < 25:
            final_alpha = 0
        elif brightness < 75 and saturation < 35:
            ratio = (brightness - 48) / (75 - 48)
            final_alpha = int(c_alpha * ratio)
        else:
            final_alpha = c_alpha
            
        if final_alpha > 0:
            result_img.putpixel((x, y), (r, g, b, int(final_alpha)))

# 1:1 완벽 정원으로 크롭
crop_box = (int(cx - radius), int(cy - radius), int(cx + radius), int(cy + radius))
final_logo = result_img.crop(crop_box)

final_logo.save(dst_logo1, "PNG")
final_logo.save(dst_logo2, "PNG")
print(f"[+] ✅ 수학적 1:1 완전 정원(628x628) 안팎 투명 앰블럼 생성 완료!")
print(f"    - 저장 위치 1: {dst_logo1}")
print(f"    - 저장 위치 2: {dst_logo2}")
print(f"    - 바운딩 박스: {final_logo.getbbox()}")
