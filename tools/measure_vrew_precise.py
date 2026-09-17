from PIL import Image

im = Image.open(r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\emblem_vrew_crop.png").convert("RGBA")
W, H = im.size

# The emblem circle: find gold rim pixels
# in emblem_vrew_crop:
gold_pts = []
for y in range(H):
    for x in range(W):
        r, g, b, a = im.getpixel((x, y))
        # Golden rim hue: R > 120, G > 80, B < 65, R > B + 50
        if r > 110 and g > 70 and b < 70 and r > b + 40:
            gold_pts.append((x, y))

xs = [p[0] for p in gold_pts]
ys = [p[1] for p in gold_pts]
print(f"Emblem inside crop: X={min(xs)}..{max(xs)} (w={max(xs)-min(xs)+1}), Y={min(ys)}..{max(ys)} (h={max(ys)-min(ys)+1})")

# Since crop started at (250, 25) in media_1789621841268.png:
crop_x0, crop_y0 = 250, 25
real_ex1 = crop_x0 + min(xs)
real_ex2 = crop_x0 + max(xs)
real_ey1 = crop_y0 + min(ys)
real_ey2 = crop_y0 + max(ys)
real_ew = real_ex2 - real_ex1 + 1
real_eh = real_ey2 - real_ey1 + 1

print(f"Emblem in media_1789621841268.png: X={real_ex1}..{real_ex2} (W={real_ew}), Y={real_ey1}..{real_ey2} (H={real_eh})")

# Canvas in media_1789621841268.png is:
# Left=6, Right=332, Width=327, Top=25
canvas_x1 = 6
canvas_w = 327
canvas_y1 = 25

print(f"\n--- [캔버스 327px 기준 실측치] ---")
print(f"1. 엠블럼 직경: {max(real_ew, real_eh)}px (너비 {real_ew}px, 높이 {real_eh}px)")
print(f"2. 엠블럼 우측 마진: {canvas_x1 + canvas_w - real_ex2}px")
print(f"3. 엠블럼 상단 마진: {real_ey1 - canvas_y1}px")
print(f"4. 엠블럼 중심점(CY): {real_ey1 - canvas_y1 + real_eh/2:.1f}px")

# Also badge in media_1789621841268.png:
# Let's inspect badge:
badge_im = Image.open(r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\badge_vrew_crop.png").convert("RGBA")
b_pts = []
for y in range(badge_im.height):
    for x in range(badge_im.width):
        r, g, b, a = badge_im.getpixel((x, y))
        if b > 180 and r < 60 and g < 120:
            b_pts.append((x, y))

b_xs = [p[0] for p in b_pts]
b_ys = [p[1] for p in b_pts]
# badge crop was (6, 25)
b_real_x1 = 6 + min(b_xs)
b_real_x2 = 6 + max(b_xs)
b_real_y1 = 25 + min(b_ys)
b_real_y2 = 25 + max(b_ys)
b_real_w = b_real_x2 - b_real_x1 + 1
b_real_h = b_real_y2 - b_real_y1 + 1

print(f"\n--- [배지 실측치] ---")
print(f"1. 배지 크기: W={b_real_w}px, H={b_real_h}px (종횡비: {b_real_w/b_real_h:.2f})")
print(f"2. 배지 좌측 마진: {b_real_x1 - canvas_x1}px")
print(f"3. 배지 상단 마진: {b_real_y1 - canvas_y1}px")
print(f"4. 배지 중심점(CY): {b_real_y1 - canvas_y1 + b_real_h/2:.1f}px")

print(f"\n--- [정밀 상대 비교 비율] ---")
print(f"1. 엠블럼 직경({max(real_ew, real_eh)}px) / 배지 높이({b_real_h}px) = {max(real_ew, real_eh) / b_real_h:.2f}배")
print(f"2. 엠블럼 직경({max(real_ew, real_eh)}px) / 배지 너비({b_real_w}px) = {max(real_ew, real_eh) / b_real_w:.2f}배")
print(f"3. 상단 마진: 배지={b_real_y1 - canvas_y1}px, 엠블럼={real_ey1 - canvas_y1}px")
print(f"4. 중심선(CY): 배지 cy={b_real_y1 - canvas_y1 + b_real_h/2:.1f}px, 엠블럼 cy={real_ey1 - canvas_y1 + real_eh/2:.1f}px")

scale_factor = 1080.0 / canvas_w
print(f"\n--- [1080 x 1920 해상도 정밀 환산 (스케일 팩터 = {scale_factor:.3f})] ---")
print(f"• 배지 크기: W = {round(b_real_w * scale_factor)}px, H = {round(b_real_h * scale_factor)}px")
print(f"• 배지 좌측 마진: X = {round((b_real_x1 - canvas_x1) * scale_factor)}px")
print(f"• 배지 상단 마진: Y = {round((b_real_y1 - canvas_y1) * scale_factor)}px")
print(f"• 엠블럼 직경: D = {round(max(real_ew, real_eh) * scale_factor)}px")
print(f"• 엠블럼 우측 마진: Right_Margin = {round((canvas_x1 + canvas_w - real_ex2) * scale_factor)}px")
print(f"• 엠블럼 X 좌표: X = {1080 - round(max(real_ew, real_eh) * scale_factor) - round((canvas_x1 + canvas_w - real_ex2) * scale_factor)}px")
print(f"• 엠블럼 상단 마진: Y = {round((real_ey1 - canvas_y1) * scale_factor)}px")
