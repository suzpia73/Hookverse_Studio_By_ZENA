import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter

def build_authentic_35mm_precision_banner():
    W, H = 2560, 1440
    # 📱 유튜브 모바일 안전영역 (금색 사각 박스 공식 규격: 1546 x 423)
    safe_w, safe_h = 1546, 423
    safe_x1 = (W - safe_w) // 2  # 507
    safe_y1 = (H - safe_h) // 2  # 508
    safe_x2 = safe_x1 + safe_w   # 2053
    safe_y2 = safe_y1 + safe_h   # 931

    # 1. 원본 에셋 경로
    PATH_IMG1 = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\raw_film_source.jpg"
    PATH_IMG2 = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\raw_text_source.jpg"
    neura_path = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\G3캐릭터앵커LOCK\전신_우측.jpg"

    img1 = Image.open(PATH_IMG1).convert("RGBA")
    img2 = Image.open(PATH_IMG2).convert("RGBA")

    rail_h = 56
    inner_h = safe_h - (rail_h * 2)  # 311px

    # =========================================================================
    # 2. [오리지널 앰버 브라운 & 가죽 질감] 중앙 내부 필름 레이어
    #    (좌우 명암 밸런스 자연스럽게 보정: 좌측에도 은은한 웜 앰버 깊이감 부여)
    # =========================================================================
    inner = Image.new("RGBA", (safe_w, inner_h), (20, 14, 10, 255))
    for y in range(inner_h):
        ny = (y - inner_h / 2.0) / (inner_h / 2.0)
        for xx in range(safe_w):
            nx = (xx - safe_w / 2.0) / (safe_w / 2.0)
            dist = math.sqrt((nx * 1.35) ** 2 + ny ** 2)
            intensity = max(0.0, 1.0 - min(1.0, dist)) ** 1.3
            r = int(26 + (94 - 26) * intensity)
            g = int(17 + (64 - 17) * intensity)
            b = int(12 + (34 - 12) * intensity)
            inner.putpixel((xx, y), (r, g, b, 255))

    # 빈티지 필름 가죽 질감 블렌딩
    leather = img1.crop((910, 150, 1010, 550)).resize((safe_w, inner_h), Image.Resampling.LANCZOS)
    inner = Image.blend(inner, leather, 0.22)

    # ★ [오빠 피드백 2] 변형적 원형/타원형 꼬불 실오라기 & 점먼지 & 스크래치 탑재
    rng = random.Random(1997)  # IMF 1997 시네마 시드
    noise_layer = Image.new("RGBA", (safe_w, inner_h), (0, 0, 0, 0))
    d_noise = ImageDraw.Draw(noise_layer)

    # A) 꼬불꼬불한 아날로그 직선/곡선 실오라기 (4가닥)
    for _ in range(4):
        pts = []
        cx = rng.randint(40, safe_w - 40)
        cy = rng.randint(25, inner_h - 25)
        pts.append((cx, cy))
        for _ in range(rng.randint(6, 12)):
            cx += rng.randint(-12, 12)
            cy += rng.randint(-12, 12)
            cx = max(10, min(safe_w - 10, cx))
            cy = max(5, min(inner_h - 5, cy))
            pts.append((cx, cy))
        hair_col = rng.choice([
            (255, 245, 230, rng.randint(180, 240)),
            (225, 185, 125, rng.randint(160, 220))
        ])
        for i in range(len(pts) - 1):
            d_noise.line([pts[i], pts[i + 1]], fill=hair_col, width=rng.choice([1, 2]))

    # B) ★ [오빠 요청 반영] 원형/타원형으로 둥글게 말려들어간 고리형 실오라기 (Curled Loop Fibers 3개)
    for _ in range(3):
        center_x = rng.randint(80, safe_w - 80)
        center_y = rng.randint(30, inner_h - 30)
        rx = rng.randint(8, 18)
        ry = rng.randint(6, 14)
        rot_angle = rng.uniform(0, math.pi)

        loop_pts = []
        steps = rng.randint(18, 28)
        spiral_decay = rng.uniform(0.7, 0.95)
        for s in range(steps):
            theta = (s / float(steps)) * 2.5 * math.pi  # 한 바퀴 반 회전
            cur_r = 1.0 - (1.0 - spiral_decay) * (s / float(steps))
            lx = rx * cur_r * math.cos(theta)
            ly = ry * cur_r * math.sin(theta)
            # 회전 변환
            rot_x = lx * math.cos(rot_angle) - ly * math.sin(rot_angle)
            rot_y = lx * math.sin(rot_angle) + ly * math.cos(rot_angle)
            loop_pts.append((center_x + rot_x, center_y + rot_y))

        loop_col = rng.choice([
            (255, 240, 220, rng.randint(190, 245)),
            (230, 190, 130, rng.randint(170, 225))
        ])
        for i in range(len(loop_pts) - 1):
            d_noise.line([loop_pts[i], loop_pts[i + 1]], fill=loop_col, width=1)

    # C) 아날로그 점먼지 스팟 (30개)
    for _ in range(30):
        dx = rng.randint(15, safe_w - 15)
        dy = rng.randint(8, inner_h - 8)
        rad = rng.uniform(0.8, 2.0)
        dust_col = rng.choice([
            (255, 250, 240, rng.randint(160, 230)),
            (235, 195, 130, rng.randint(150, 210)),
            (35, 25, 18, rng.randint(120, 180))
        ])
        d_noise.ellipse([dx - rad, dy - rad, dx + rad, dy + rad], fill=dust_col)

    # D) 빈티지 영사기 수직 스크래치 (3줄)
    for _ in range(3):
        sx = rng.randint(50, safe_w - 50)
        sy1 = rng.randint(0, 40)
        sy2 = rng.randint(inner_h - 40, inner_h)
        s_col = rng.choice([
            (255, 240, 210, rng.randint(70, 130)),
            (45, 30, 20, rng.randint(80, 140))
        ])
        d_noise.line([sx, sy1, sx + rng.randint(-3, 3), sy2], fill=s_col, width=1)

    noise_layer = noise_layer.filter(ImageFilter.GaussianBlur(0.3))
    inner = Image.alpha_composite(inner, noise_layer)

    # 좌우 사이드 필름 번(Burn) 앰버 빛 효과
    w1 = img1.width
    burn_left = img1.crop((0, 95, 120, 585)).resize((120, inner_h), Image.Resampling.LANCZOS)
    b_mask = Image.new("L", (120, inner_h), 0)
    for xx in range(120):
        a = int(255 * ((1.0 - xx / 120.0) ** 1.4))
        for yy in range(inner_h):
            b_mask.putpixel((xx, yy), a)
    inner.paste(burn_left, (0, 0), b_mask)

    edge_right = img1.crop((900, 95, w1, 585)).resize((120, inner_h), Image.Resampling.LANCZOS)
    r_mask = Image.new("L", (120, inner_h), 0)
    for xx in range(120):
        a = int(255 * ((xx / 120.0) ** 1.4))
        for yy in range(inner_h):
            r_mask.putpixel((xx, yy), a)
    inner.paste(edge_right, (safe_w - 120, 0), r_mask)

    # =========================================================================
    # 3. [★ 오빠 피드백 1: 양끝단 반쪽 타공(Half-Hole) 정밀 렌더러]
    #    (좌우 양끝단에 정확히 50% 잘린 반쪽 타공 배치 ➡️ 필름이 길어보이는 현상 100% 종결!)
    # =========================================================================
    rail_top = Image.new("RGBA", (safe_w, rail_h), (16, 12, 10, 255))
    rail_bottom = Image.new("RGBA", (safe_w, rail_h), (16, 12, 10, 255))

    d_top = ImageDraw.Draw(rail_top)
    d_bot = ImageDraw.Draw(rail_bottom)

    # 레일 배경 앰버 그라데이션
    for y in range(rail_h):
        r_top = int(24 - 10 * (y / rail_h))
        g_top = int(18 - 8 * (y / rail_h))
        b_top = int(14 - 6 * (y / rail_h))
        d_top.line([0, y, safe_w, y], fill=(r_top, g_top, b_top, 255))

        r_bot = int(14 + 10 * (y / rail_h))
        g_bot = int(10 + 8 * (y / rail_h))
        b_bot = int(8 + 6 * (y / rail_h))
        d_bot.line([0, y, safe_w, y], fill=(r_bot, g_bot, b_bot, 255))

    # 레일 경계선 골든 앰버 헤어라인
    d_top.line([0, rail_h - 1, safe_w, rail_h - 1], fill=(70, 52, 35, 255), width=1)
    d_bot.line([0, 0, safe_w, 0], fill=(70, 52, 35, 255), width=1)

    # ★ 반쪽 타공(Half-hole) 공식:
    # 좌측 끝단 중심: x = 0 (정확히 절반만 노출: -9px ~ +9px)
    # 우측 끝단 중심: x = safe_w (정확히 절반만 노출: safe_w - 9px ~ safe_w + 9px)
    # 총 간격 수: 38칸 ➡️ 등간격 pitch = safe_w / 38.0 = 40.684px
    hole_w = 18
    hole_h = 26
    corner_r = 3
    num_intervals = 38
    pitch = safe_w / float(num_intervals)  # 약 40.68px

    hole_y_top = (rail_h - hole_h) // 2  # 15px ~ 41px
    hole_y_bot = (rail_h - hole_h) // 2  # 15px ~ 41px

    # 총 39개 타공 구멍 (i=0은 좌측 반쪽, i=38은 우측 반쪽, i=1~37은 온전한 구멍)
    for i in range(num_intervals + 1):
        center_x = i * pitch
        hx = int(round(center_x - hole_w / 2.0))

        for draw, hy in [(d_top, hole_y_top), (d_bot, hole_y_bot)]:
            # 1단계: 외곽 미세 섀도우 림
            draw.rounded_rectangle([hx - 1, hy - 1, hx + hole_w, hy + hole_h],
                                   radius=corner_r + 1, fill=(28, 20, 14, 255))
            # 2단계: 실물 필름 웜 앰버 골드 영사기 투과광
            draw.rounded_rectangle([hx, hy, hx + hole_w - 1, hy + hole_h - 1],
                                   radius=corner_r, fill=(218, 168, 88, 240))
            # 3단계: 구멍 중심 따뜻한 샴페인 빛
            draw.rounded_rectangle([hx + 1, hy + 1, hx + hole_w - 2, hy + hole_h - 2],
                                   radius=max(1, corner_r - 1), fill=(235, 185, 105, 255))

    print(f"🎬 양끝단 반쪽 타공(Half-Hole) 렌더링 완료: 총 {num_intervals + 1}개 구멍 (등간격 {pitch:.2f}px, 완벽 대칭!)")

    # =========================================================================
    # 4. 필름 슬라이드 조립
    # =========================================================================
    film_slide = Image.new("RGBA", (safe_w, safe_h), (12, 8, 6, 255))
    film_slide.paste(rail_top, (0, 0))
    film_slide.paste(inner, (0, rail_h))
    film_slide.paste(rail_bottom, (0, safe_h - rail_h))

    # =========================================================================
    # 5. [초고해상도] 3D Chrome HOOKVERSE STUDIO 텍스트
    # =========================================================================
    crop_area = (20, 310, 1004, 725)
    text_crop = img2.crop(crop_area).convert("RGBA")
    tw, th = text_crop.size

    clean_text = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    for y in range(th):
        for xx in range(tw):
            pixel = text_crop.getpixel((xx, y))
            if isinstance(pixel, (tuple, list)) and len(pixel) >= 3:
                r, g, b = pixel[0], pixel[1], pixel[2]
            else:
                continue
            bright = max(r, g, b)
            sat = bright - min(r, g, b)
            if bright < 26:
                alpha = 0
            elif bright < 55 and sat < 15:
                alpha = int(255 * (bright - 26) / (55 - 26))
            else:
                alpha = 255
            if alpha > 0:
                clean_text.putpixel((xx, y), (r, g, b, alpha))

    target_th = 210
    target_tw = int(target_th * (tw / float(th)))
    text_scaled = clean_text.resize((target_tw, target_th), Image.Resampling.LANCZOS)
    text_scaled = text_scaled.filter(ImageFilter.UnsharpMask(radius=1.8, percent=150, threshold=2))

    # =========================================================================
    # 6. [초고해상도 무손실] 뉴라 상반신 바스트 실루엣 + 타원 조명
    # =========================================================================
    neura_full = Image.open(neura_path).convert("RGBA")
    crop_box = (0, 0, neura_full.width, int(neura_full.height * 0.42))
    neura_crop = neura_full.crop(crop_box).transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    neu_h = 335
    neu_w = int(neu_h * (neura_crop.width / neura_crop.height))
    neura_scaled = neura_crop.resize((neu_w, neu_h), Image.Resampling.LANCZOS)

    mask = Image.new("L", (neu_w, neu_h), 0)
    m_draw = ImageDraw.Draw(mask)
    body_cx = int(neu_w * 0.52)
    body_cy = int(neu_h * 0.48)
    for r in range(180, 20, -8):
        al = int(255 * (1.0 - (r / 180.0) ** 2.0))
        m_draw.ellipse([body_cx - int(r * 0.72), body_cy - int(r * 1.15),
                        body_cx + int(r * 0.72), body_cy + int(r * 1.15)], fill=al)
    mask = mask.filter(ImageFilter.GaussianBlur(16))
    neura_scaled.putalpha(mask)
    neura_scaled = neura_scaled.filter(ImageFilter.UnsharpMask(radius=1.2, percent=120, threshold=1))

    n_bbox = neura_scaled.split()[-1].getbbox()
    neu_vis_w = (n_bbox[2] - n_bbox[0]) if n_bbox else neu_w

    # =========================================================================
    # 7. 완벽한 칼대칭 배치 (간격 38px, 좌우 여백 100% 동일)
    # =========================================================================
    gap = 38
    total_group_w = target_tw + gap + neu_vis_w
    side_margin = (safe_w - total_group_w) // 2

    tx_in_slide = side_margin
    ty_in_slide = (safe_h - target_th) // 2

    neu_x_in_slide = tx_in_slide + target_tw + gap - (n_bbox[0] if n_bbox else 0)
    neu_y_in_slide = (safe_h - neu_h) // 2

    # ★ [오빠 피드백 3: 좌측 글자 뒤 웜 앰버 앰비언트 글로우 보강]
    # (왼쪽이 너무 어둡지 않게, 글자 주변에 은은한 웜 앰버 백라이트를 감싸 좌우 조화 완벽 달성)
    t_glow = Image.new("RGBA", (safe_w, safe_h), (0, 0, 0, 0))
    d_tg = ImageDraw.Draw(t_glow)
    # 깊은 섀도우 림
    d_tg.ellipse([tx_in_slide - 25, ty_in_slide - 15,
                  tx_in_slide + target_tw + 25, ty_in_slide + target_th + 15],
                 fill=(12, 9, 6, 140))
    # 따뜻한 앰버 앰비언트 (우측 뉴라 조명과 부드럽게 균형)
    d_tg.ellipse([tx_in_slide - 45, ty_in_slide - 25,
                  tx_in_slide + target_tw + 45, ty_in_slide + target_th + 25],
                 fill=(80, 50, 20, 45))
    t_glow = t_glow.filter(ImageFilter.GaussianBlur(22))
    film_slide = Image.alpha_composite(film_slide, t_glow)

    # 슬라이드에 글자와 뉴라 합성
    film_slide.paste(text_scaled, (tx_in_slide, ty_in_slide), text_scaled)
    film_slide.paste(neura_scaled, (neu_x_in_slide, neu_y_in_slide), neura_scaled)

    # =========================================================================
    # 8. 전체 캔버스 (2560 x 1440)에 결합 및 저장
    # =========================================================================
    c = Image.new("RGBA", (W, H), (6, 7, 12, 255))
    c.paste(film_slide, (safe_x1, safe_y1))

    base_dir = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images"
    out_master = os.path.join(base_dir, "hookverse_youtube_channel_banner_2560x1440.png")
    out_mobile = os.path.join(base_dir, "preview_mobile_view_1546x423.png")
    out_preview = os.path.join(base_dir, "preview_bust_film_safezone.png")

    c.save(out_master, "PNG")

    mobile_crop = c.crop((safe_x1, safe_y1, safe_x2, safe_y2))
    mobile_crop.save(out_mobile, "PNG")

    prev = c.copy()
    d_prev = ImageDraw.Draw(prev)
    d_prev.rectangle([safe_x1, safe_y1, safe_x2, safe_y2], outline=(255, 215, 0, 255), width=4)
    d_prev.line([safe_x1, safe_y1 + safe_h // 2, safe_x1 + side_margin, safe_y1 + safe_h // 2], fill=(0, 255, 255, 255), width=3)
    right_edge_x = safe_x1 + neu_x_in_slide + (n_bbox[2] if n_bbox else neu_w)
    d_prev.line([right_edge_x, safe_y1 + safe_h // 2, safe_x2, safe_y1 + safe_h // 2], fill=(0, 255, 255, 255), width=3)
    prev.save(out_preview, "PNG")

    actual_left = side_margin
    actual_right = safe_w - (neu_x_in_slide + (n_bbox[2] if n_bbox else neu_w))
    print("==================================================")
    print("🎬 양끝단 반쪽 타공 & 고리형 실오라기 완성!")
    print(f"- 텍스트: {target_tw}x{target_th}px")
    print(f"- 뉴라: {neu_vis_w}x{neu_h}px")
    print(f"- 간격: {gap}px")
    print(f"- 좌측 여백: {actual_left}px, 우측 여백: {actual_right}px (오차: {abs(actual_left - actual_right)}px)")
    print("==================================================")

if __name__ == "__main__":
    build_authentic_35mm_precision_banner()
