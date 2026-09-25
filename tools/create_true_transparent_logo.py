import os
from PIL import Image, ImageDraw

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
src_logo = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo.png")
dst_logo = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo_transparent.png")

img = Image.open(src_logo).convert("RGBA")
W, H = img.size
cx, cy = W // 2, H // 2

# 반지름 318px (골든 릴 외곽)
radius = 318

# 1. 1차 정원 마스크 (원 바깥 완벽 100% 차단)
scale = 4
mask_large = Image.new("L", (W * scale, H * scale), 0)
draw_large = ImageDraw.Draw(mask_large)
draw_large.ellipse([(cx - radius) * scale, (cy - radius) * scale, (cx + radius) * scale, (cy + radius) * scale], fill=255)
circle_mask = mask_large.resize((W, H), Image.Resampling.LANCZOS)

# 2. 픽셀 단위 정밀 분리:
# 금색 릴과 보라/마젠타 HV 로고는 살리고, 내부의 검은 가죽 배경은 100% 투명화!
result_img = Image.new("RGBA", (W, H), (0, 0, 0, 0))

for y in range(H):
    for x in range(W):
        c_val = circle_mask.getpixel((x, y))
        c_alpha = int(c_val[0]) if isinstance(c_val, tuple) else int(c_val or 0)
        if c_alpha == 0:
            continue
        
        px = img.getpixel((x, y))
        if isinstance(px, tuple) and len(px) >= 3:
            r, g, b = int(px[0]), int(px[1]), int(px[2])
        else:
            continue
        
        # 밝기(Luminance) 및 채도(Colorfulness) 계산
        # 금색: R, G가 높음 (r > 60 or g > 50)
        # HV 로고: 마젠타/보라색 (r > 60 or b > 60, 채도 높음)
        # 검은 배경: r < 40 and g < 40 and b < 40
        max_c = max(r, g, b)
        min_c = min(r, g, b)
        saturation = max_c - min_c
        brightness = max_c
        
        # 검은 배경 판정 (어둡고 채도가 낮은 픽셀)
        if brightness < 48 and saturation < 25:
            # 100% 투명
            final_alpha = 0
        elif brightness < 75 and saturation < 35:
            # 부드러운 경계 안티앨리어싱
            ratio = (brightness - 48) / (75 - 48)
            final_alpha = int(c_alpha * ratio)
        else:
            # 금색 릴 & HV 로고 본체는 100% 불투명
            final_alpha = c_alpha
            
        if final_alpha > 0:
            result_img.putpixel((x, y), (r, g, b, final_alpha))

# 바운딩 박스로 크롭
crop_box = (cx - radius, cy - radius, cx + radius, cy + radius)
final_logo = result_img.crop(crop_box)

final_logo.save(dst_logo, "PNG")
print(f"[+] ✅ 안팎 100% 투명화된 순수 3D 골든릴 & HV 로고 생성 완료: {dst_logo} (크기: {final_logo.size})")
