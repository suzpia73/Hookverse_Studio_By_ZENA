import os
from PIL import Image

cap_path = r"C:\Users\june2\.gemini\antigravity-ide\brain\6f64338c-c4bf-4316-a1b8-3503cde43325\.tempmediaStorage\media_1789621938406.jpg"

if not os.path.exists(cap_path):
    print("Not found")
    exit()

img = Image.open(cap_path)
W, H = img.size
print(f"[*] 캡처 이미지 크기: W={W}, H={H}")

# 파란색 배지 영역 탐색 (R < 50, G < 150, B > 180)
blue_pixels = []
for y in range(H):
    for x in range(W // 2): # 좌측 절반
        r, g, b = img.getpixel((x, y))[:3]
        if b > 160 and r < 60 and g < 120:
            blue_pixels.append((x, y))

if blue_pixels:
    xs = [p[0] for p in blue_pixels]
    ys = [p[1] for p in blue_pixels]
    bx1, bx2 = min(xs), max(xs)
    by1, by2 = min(ys), max(ys)
    bw = bx2 - bx1 + 1
    bh = by2 - by1 + 1
    print(f"[+] 좌측 배지 실측: X={bx1}, Y={by1}, W={bw}, H={bh} (중심점: cx={bx1+bw/2:.1f}, cy={by1+bh/2:.1f})")

# 우측 엠블럼 영역 탐색 (우측 절반에서 금색 테두리 탐색: R > 150, G > 100, B < 80)
gold_pixels = []
for y in range(H):
    for x in range(W // 2, W):
        r, g, b = img.getpixel((x, y))[:3]
        # 골드 림 색상
        if r > 140 and g > 110 and b < 90:
            gold_pixels.append((x, y))

if gold_pixels:
    xs = [p[0] for p in gold_pixels]
    ys = [p[1] for p in gold_pixels]
    gx1, gx2 = min(xs), max(xs)
    gy1, gy2 = min(ys), max(ys)
    gw = gx2 - gx1 + 1
    gh = gy2 - gy1 + 1
    print(f"[+] 우측 엠블럼 실측: X={gx1}, Y={gy1}, W={gw}, H={gh} (중심점: cx={gx1+gw/2:.1f}, cy={gy1+gh/2:.1f})")

    # 상대적 비율 계산
    print("--- [비교 분석 결과] ---")
    print(f"1. 배지 대비 엠블럼 크기 비율: W비율={gw/bw:.2f}, H비율={gh/bh:.2f}")
    print(f"2. 상단 마진 비교: 배지 Y={by1}, 엠블럼 Y={gy1} (차이: {gy1 - by1}px)")
    print(f"3. 수평 중심선 비교: 배지 cy={by1+bh/2:.1f}, 엠블럼 cy={gy1+gh/2:.1f} (차이: {(gy1+gh/2) - (by1+bh/2):.1f}px)")
    print(f"4. 좌우 마진: 좌측 배지 X={bx1}, 우측 엠블럼 우측여백={W - gx2}")
