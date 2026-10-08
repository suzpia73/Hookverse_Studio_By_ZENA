import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter, ImageEnhance

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"

film_path = os.path.join(WORKSPACE, "assets", "images", "raw_film_source.jpg")
text_path = os.path.join(WORKSPACE, "assets", "images", "raw_text_source.jpg")

film_orig = Image.open(film_path).convert("RGBA")
W, H = film_orig.size  # 1024, 683

text_orig = Image.open(text_path).convert("RGBA")

# 1. 3D Chrome HOOKVERSE STUDIO 텍스트 정밀 크롭
crop_area = (20, 310, 1010, 755)
text_crop = text_orig.crop(crop_area)
tw, th = text_crop.size

clean_text = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
for y in range(th):
    for x in range(tw):
        pixel = text_crop.getpixel((x, y))
        if isinstance(pixel, (tuple, list)) and len(pixel) >= 3:
            r, g, b = int(pixel[0]), int(pixel[1]), int(pixel[2])
        else:
            continue
        bright = max(r, g, b)
        sat = bright - min(r, g, b)
        if bright < 22:
            alpha = 0
        elif bright < 50 and sat < 15:
            alpha = int(255 * (bright - 22) / (50 - 22))
        else:
            alpha = 255
        if alpha > 0:
            clean_text.putpixel((x, y), (r, g, b, alpha))

# 2. 필름 슬라이드 베이스 생성:
# 상단 레일(y: 0..95)과 하단 레일(y: 585..683)은 raw_film_source의 실물 타공을 100% 온전히 유지!
badge_canvas = Image.new("RGBA", (W, H), (0, 0, 0, 255))

rail_top = film_orig.crop((0, 0, W, 95))
rail_bottom = film_orig.crop((0, 585, W, H))

badge_canvas.paste(rail_top, (0, 0))
badge_canvas.paste(rail_bottom, (0, 585))

# 3. 중앙 필름 내부(y: 95..585, 높이 490px)를 옛날 앰블럼/옛날 글자 0% 잔상 없는 순수 시네마틱 가죽 앰버 배경으로 생성!
inner_h = 585 - 95  # 490
inner = Image.new("RGBA", (W, inner_h), (20, 14, 10, 255))

# (1) 앰버 브라운 방사형 비네팅 그라데이션
for y in range(inner_h):
    ny = (y - inner_h / 2.0) / (inner_h / 2.0)
    for x in range(W):
        nx = (x - W / 2.0) / (W / 2.0)
        dist = math.sqrt((nx * 1.25) ** 2 + ny ** 2)
        intensity = max(0.0, 1.0 - min(1.0, dist)) ** 1.3
        r = int(25 + (96 - 25) * intensity)
        g = int(16 + (66 - 16) * intensity)
        b = int(11 + (35 - 11) * intensity)
        inner.putpixel((x, y), (r, g, b, 255))

# (2) 좌우 순수 빈티지 가죽 질감 블렌딩 (글자가 100% 전혀 없는 순수 가죽 안전 구역 x: 910..1010에서 샘플링)
clean_leather = film_orig.crop((910, 150, 1010, 550)).resize((W, inner_h), Image.Resampling.LANCZOS)
inner = Image.blend(inner, clean_leather, 0.25)

# (3) 좌우 사이드 필름 번(Burn) 앰버 빛 블렌딩
burn_left = film_orig.crop((0, 95, 120, 585)).resize((120, inner_h), Image.Resampling.LANCZOS)
b_mask = Image.new("L", (120, inner_h), 0)
for x in range(120):
    a = int(255 * ((1.0 - x / 120.0) ** 1.3))
    for y in range(inner_h):
        b_mask.putpixel((x, y), a)
inner.paste(burn_left, (0, 0), b_mask)

burn_right = film_orig.crop((W - 120, 95, W, 585)).resize((120, inner_h), Image.Resampling.LANCZOS)
r_mask = Image.new("L", (120, inner_h), 0)
for x in range(120):
    a = int(255 * ((x / 120.0) ** 1.3))
    for y in range(inner_h):
        r_mask.putpixel((x, y), a)
inner.paste(burn_right, (W - 120, 0), r_mask)

badge_canvas.paste(inner, (0, 95))

# 4. 아날로그 필름 노이즈 레이어링 (오빠 훈시 100% 반영: 스크래치, 둥근원 루프 실오라기, 먼지)
rng = random.Random(2026)
noise_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d_noise = ImageDraw.Draw(noise_layer)

inner_y1 = 95
inner_y2 = 585

# 1) 세로 실선 스크래치 (좌/우 및 중앙 전반 4줄)
scratch_xs = [rng.randint(70, 180), rng.randint(200, 360), rng.randint(660, 820), rng.randint(840, 950)]
for sx in scratch_xs:
    sy1 = rng.randint(inner_y1 + 4, inner_y1 + 35)
    sy2 = rng.randint(inner_y2 - 35, inner_y2 - 4)
    sc_col = (250, 225, 185, rng.randint(150, 220))
    d_noise.line([sx, sy1, sx + rng.randint(-3, 3), sy2], fill=sc_col, width=1)

# 2) 변형적 둥근원 모양의 루프 실오라기 (curled loop hair, 3개: 좌측 1개, 우측 2개)
loop_centers = [(rng.randint(110, 260), rng.randint(inner_y1 + 40, inner_y2 - 40)),
                (rng.randint(760, 910), rng.randint(inner_y1 + 40, inner_y2 - 40)),
                (rng.randint(820, 930), rng.randint(inner_y1 + 100, inner_y2 - 100))]
for cx, cy in loop_centers:
    rx = rng.randint(14, 24)
    ry = rng.randint(10, 18)
    rot_angle = rng.uniform(0, math.pi * 2)

    loop_pts = []
    steps = rng.randint(24, 34)
    for s in range(steps):
        theta = (s / float(steps)) * 2.8 * math.pi
        cur_r = 1.0 - 0.22 * (s / float(steps))
        lx = rx * cur_r * math.cos(theta)
        ly = ry * cur_r * math.sin(theta)
        rot_x = lx * math.cos(rot_angle) - ly * math.sin(rot_angle)
        rot_y = lx * math.sin(rot_angle) + ly * math.cos(rot_angle)
        loop_pts.append((cx + rot_x, cy + rot_y))

    l_col = rng.choice([
        (255, 240, 210, rng.randint(210, 255)),
        (245, 195, 120, rng.randint(190, 245))
    ])
    for i in range(len(loop_pts) - 1):
        d_noise.line([loop_pts[i], loop_pts[i + 1]], fill=l_col, width=1)

# 3) 꼬불꼬불한 아날로그 실오라기 (6가닥)
for _ in range(6):
    pts = []
    cx = rng.randint(80, W - 80)
    cy = rng.randint(inner_y1 + 25, inner_y2 - 25)
    pts.append((cx, cy))
    for _ in range(rng.randint(8, 14)):
        cx += rng.randint(-15, 15)
        cy += rng.randint(-15, 15)
        cx = max(60, min(W - 60, cx))
        cy = max(inner_y1 + 10, min(inner_y2 - 10, cy))
        pts.append((cx, cy))
    hair_col = rng.choice([
        (255, 245, 225, rng.randint(200, 255)),
        (245, 195, 120, rng.randint(180, 240)),
        (225, 215, 195, rng.randint(170, 225))
    ])
    w = rng.choice([1, 1, 2])
    for i in range(len(pts) - 1):
        d_noise.line([pts[i], pts[i + 1]], fill=hair_col, width=w)

# 4) 점먼지 파티클 (소형 50개, 중형 20개, 대형 필름 스팟 6개)
for _ in range(50):
    gx = rng.randint(50, W - 50)
    gy = rng.randint(inner_y1 + 8, inner_y2 - 8)
    grad = rng.uniform(0.6, 1.4)
    d_noise.ellipse([gx - grad, gy - grad, gx + grad, gy + grad],
                    fill=(255, 245, 230, rng.randint(150, 235)))

for _ in range(20):
    dx = rng.randint(70, W - 70)
    dy = rng.randint(inner_y1 + 12, inner_y2 - 12)
    rad = rng.uniform(1.4, 2.4)
    dust_col = rng.choice([
        (255, 250, 235, rng.randint(180, 245)),
        (240, 195, 125, rng.randint(170, 235)),
        (40, 28, 18, rng.randint(140, 200))
    ])
    d_noise.ellipse([dx - rad, dy - rad, dx + rad, dy + rad], fill=dust_col)

for _ in range(6):
    dx = rng.randint(80, W - 80)
    dy = rng.randint(inner_y1 + 18, inner_y2 - 18)
    rad = rng.uniform(2.5, 3.8)
    dust_col = rng.choice([
        (255, 240, 210, rng.randint(190, 250)),
        (235, 185, 115, rng.randint(180, 235))
    ])
    d_noise.ellipse([dx - rad, dy - rad, dx + rad, dy + rad], fill=dust_col)

noise_layer = noise_layer.filter(ImageFilter.GaussianBlur(0.2))
badge_canvas = Image.alpha_composite(badge_canvas, noise_layer)

# 5. 유튜브 공식 채널 배너와 100% 동일한 3D 크롬 HOOKVERSE STUDIO 텍스트 정중앙 배치
target_tw = 730
target_th = int(target_tw * (th / float(tw)))
scaled_text = clean_text.resize((target_tw, target_th), Image.Resampling.LANCZOS)

# 선명도 & 채도 & 밝기 최적화 (탁함 0%, 쨍하고 눈부신 3D 크롬 완성)
enhancer_s = ImageEnhance.Sharpness(scaled_text)
scaled_text = enhancer_s.enhance(1.45)
enhancer_b = ImageEnhance.Brightness(scaled_text)
scaled_text = enhancer_b.enhance(1.18)
enhancer_c = ImageEnhance.Contrast(scaled_text)
scaled_text = enhancer_c.enhance(1.14)

# 정확한 정중앙 (중간맞춤) 좌표 계산
text_x = (W - target_tw) // 2  # 수학적 정중앙
# 상하 레일(95, 585) 사이 중앙: 340
text_y = 340 - (target_th // 2) - 4

# 부드러운 샴페인 골드 앰비언트 글로우
glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
d_glow = ImageDraw.Draw(glow)
gx1 = text_x - 30
gy1 = text_y - 15
gx2 = text_x + target_tw + 30
gy2 = text_y + target_th + 15
for r in range(35, 0, -4):
    a = int(32 * (1.0 - r / 35.0))
    d_glow.rounded_rectangle([gx1 - r, gy1 - r, gx2 + r, gy2 + r], radius=25 + r, fill=(245, 195, 115, a))
glow = glow.filter(ImageFilter.GaussianBlur(14))
badge_canvas = Image.alpha_composite(badge_canvas, glow)

# 텍스트 최종 합성!
badge_canvas.paste(scaled_text, (text_x, text_y), scaled_text)

# 6. 저장
out_1024 = os.path.join(WORKSPACE, "assets", "HOOKVERSE_공식_3대_브랜딩_완제품", "02_공식시네마틱배지_1024p_마스터스틸.png")
badge_canvas.save(out_1024, "PNG", optimize=True)
print("Saved 1024p Master Badge:", out_1024)

# 270x136 스케일다운 (좌상단 배지 공식 스틸)
badge_270 = badge_canvas.resize((270, 136), Image.Resampling.LANCZOS)
out_270 = os.path.join(WORKSPACE, "assets", "HOOKVERSE_공식_3대_브랜딩_완제품", "02_좌상단시네마틱배지_270px_공식스틸.png")
badge_270.save(out_270, "PNG", optimize=True)
print("Saved 270px Badge:", out_270)
