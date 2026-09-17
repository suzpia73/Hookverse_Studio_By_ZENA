from PIL import Image

p = r"C:\Users\june2\.gemini\antigravity-ide\brain\6f64338c-c4bf-4316-a1b8-3503cde43325\.user_uploaded\media_1789621841268.png"
im = Image.open(p).convert("RGBA")
W, H = im.size

canvas_x1 = 6
canvas_y1 = 25
canvas_w = 327 # width in crop

print(f"Canvas Left={canvas_x1}, Top={canvas_y1}, Width={canvas_w}")

# 1. Measure blue badge
blue_pixels = []
for y in range(canvas_y1, H):
    for x in range(canvas_x1, canvas_x1 + 150): # left portion
        r, g, b, a = im.getpixel((x, y))
        # Royal blue is very blue (B > 160, R < 70, G < 130)
        if b > 180 and r < 50 and g < 120:
            blue_pixels.append((x, y))

b_xs = [pt[0] for pt in blue_pixels]
b_ys = [pt[1] for pt in blue_pixels]
bx1, bx2 = min(b_xs), max(b_xs)
by1, by2 = min(b_ys), max(b_ys)
bw = bx2 - bx1 + 1
bh = by2 - by1 + 1

# 2. Measure right emblem (golden film reel / HV)
# Look in right portion: x from canvas_x1 + 200 to canvas_x1 + canvas_w
# Find the circular emblem bounding box
# Golden color has high R, moderate G, lower B (R > 130, G > 90, B < 80)
# Or let's inspect all non-background pixels in the emblem circle
emblem_pixels = []
for y in range(canvas_y1, H):
    for x in range(canvas_x1 + 200, canvas_x1 + canvas_w):
        r, g, b, a = im.getpixel((x, y))
        # Gold reel border
        if (r > 120 and g > 80 and b < 80) or (r > 130 and b > 100): # gold or purple HV
            emblem_pixels.append((x, y))

e_xs = [pt[0] for pt in emblem_pixels]
e_ys = [pt[1] for pt in emblem_pixels]
ex1, ex2 = min(e_xs), max(e_xs)
ey1, ey2 = min(e_ys), max(e_ys)
ew = ex2 - ex1 + 1
eh = ey2 - ey1 + 1

print("\n================ [브루(Vrew) 캡처 정밀 실측 데이터] ================")
print(f"1. 좌측 파란색 배지:")
print(f"   - 위치 (Crop 절대좌표): X={bx1} ~ {bx2}, Y={by1} ~ {by2}")
print(f"   - 크기: W={bw}px, H={bh}px (종횡비 W/H = {bw/bh:.2f})")
print(f"   - 캔버스 기준 상대 오프셋: X_margin = {bx1 - canvas_x1}px, Y_margin = {by1 - canvas_y1}px")
print(f"   - 캔버스 너비 대비 비율: {bw / canvas_w * 100:.2f}%")
print(f"   - 중심점 (캔버스 기준): cx = {bx1 - canvas_x1 + bw/2:.1f}px, cy = {by1 - canvas_y1 + bh/2:.1f}px")

print(f"\n2. 우측 골든 릴 엠블럼:")
print(f"   - 위치 (Crop 절대좌표): X={ex1} ~ {ex2}, Y={ey1} ~ {ey2}")
print(f"   - 크기: W={ew}px, H={eh}px (직경 D ≈ {max(ew, eh)}px)")
print(f"   - 캔버스 기준 상대 오프셋: 우측 여백 = {canvas_x1 + canvas_w - ex2}px, Y_margin = {ey1 - canvas_y1}px")
print(f"   - 캔버스 너비 대비 비율: {max(ew, eh) / canvas_w * 100:.2f}%")
print(f"   - 중심점 (캔버스 기준): cx = {ex1 - canvas_x1 + ew/2:.1f}px, cy = {ey1 - canvas_y1 + eh/2:.1f}px")

print(f"\n3. 배지와 엠블럼 간의 상대 비율 비교:")
print(f"   - 엠블럼 크기(직경) vs 배지 높이 비율: {max(ew, eh) / bh:.2f}배")
print(f"   - 엠블럼 크기(직경) vs 배지 너비 비율: {max(ew, eh) / bw:.2f}배")
print(f"   - 상단 Y 시작점 차이: 배지 Y={by1 - canvas_y1}px vs 엠블럼 Y={ey1 - canvas_y1}px (차이: {(ey1 - canvas_y1) - (by1 - canvas_y1)}px)")
print(f"   - 수평 중심선(CY) 차이: 배지 cy={by1 - canvas_y1 + bh/2:.1f}px vs 엠블럼 cy={ey1 - canvas_y1 + eh/2:.1f}px (차이: {(ey1 - canvas_y1 + eh/2) - (by1 - canvas_y1 + bh/2):.1f}px)")

print(f"\n4. 1080 x 1920 마스터 해상도 1:1 환산 스케일 (스케일 팩터 = {1080 / canvas_w:.3f}):")
scale = 1080.0 / canvas_w
print(f"   - 배지 크기: W = {round(bw * scale)}px, H = {round(bh * scale)}px")
print(f"   - 배지 좌측/상단 여백: X = {round((bx1 - canvas_x1) * scale)}px, Y = {round((by1 - canvas_y1) * scale)}px")
print(f"   - 엠블럼 크기: D = {round(max(ew, eh) * scale)}px")
print(f"   - 엠블럼 우측/상단 여백: 우측여백 = {round((canvas_x1 + canvas_w - ex2) * scale)}px, Y = {round((ey1 - canvas_y1) * scale)}px")
print(f"   - 엠블럼 좌측 시작 X: {round(1080 - max(ew, eh) * scale - (canvas_x1 + canvas_w - ex2) * scale)}px")
