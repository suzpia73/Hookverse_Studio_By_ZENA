import os
import math
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
    # =========================================================================
    inner = Image.new("RGBA", (safe_w, inner_h), (20, 14, 10, 255))
    for y in range(inner_h):
        ny = (y - inner_h / 2.0) / (inner_h / 2.0)
        for xx in range(safe_w):
            nx = (xx - safe_w / 2.0) / (safe_w / 2.0)
            dist = math.sqrt((nx * 1.35) ** 2 + ny ** 2)
            intensity = max(0.0, 1.0 - min(1.0, dist)) ** 1.3
            r = int(24 + (92 - 24) * intensity)
            g = int(15 + (62 - 15) * intensity)
            b = int(10 + (32 - 10) * intensity)
            inner.putpixel((xx, y), (r, g, b, 255))

    # 빈티지 필름 가죽 질감 블렌딩
    leather = img1.crop((910, 150, 1010, 550)).resize((safe_w, inner_h), Image.Resampling.LANCZOS)
    inner = Image.blend(inner, leather, 0.22)

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
    # 3. [★ 실물 35mm 정품 타공 규격 1:1 수학적 칼대칭 렌더러]
    #    (18x26px 직사각형 라운드, 41.0px 정밀 등간격, 따뜻한 앰버 영사기 투과광!)
    # =========================================================================
    rail_top = Image.new("RGBA", (safe_w, rail_h), (16, 12, 10, 255))
    rail_bottom = Image.new("RGBA", (safe_w, rail_h), (16, 12, 10, 255))

    d_top = ImageDraw.Draw(rail_top)
    d_bot = ImageDraw.Draw(rail_bottom)

    # A) 레일 배경: 앰버 필름 그라데이션
    for y in range(rail_h):
        r_top = int(24 - 10 * (y / rail_h))
        g_top = int(18 - 8 * (y / rail_h))
        b_top = int(14 - 6 * (y / rail_h))
        d_top.line([0, y, safe_w, y], fill=(r_top, g_top, b_top, 255))

        r_bot = int(14 + 10 * (y / rail_h))
        g_bot = int(10 + 8 * (y / rail_h))
        b_bot = int(8 + 6 * (y / rail_h))
        d_bot.line([0, y, safe_w, y], fill=(r_bot, g_bot, b_bot, 255))

    # B) 레일 경계선 골든 앰버 헤어라인
    d_top.line([0, rail_h - 1, safe_w, rail_h - 1], fill=(70, 52, 35, 255), width=1)
    d_bot.line([0, 0, safe_w, 0], fill=(70, 52, 35, 255), width=1)

    # C) 35mm 실물 측정 규격 정밀 배치
    # 폭 18px, 높이 26px, r=3px (실물 필름과 100% 동일한 직사각형 라운드 형태)
    hole_w = 18
    hole_h = 26
    corner_r = 3
    pitch = 41.0  # 실물 측정 평균 피치

    # 안전구역 좌우 칼대칭 시작 X좌표 계산
    total_holes = int(safe_w // pitch)  # 37개
    used_span = (total_holes - 1) * pitch + hole_w
    start_x = (safe_w - used_span) / 2.0  # 완벽한 좌우 대칭 오프셋

    hole_y_top = (rail_h - hole_h) // 2  # 15px ~ 41px
    hole_y_bot = (rail_h - hole_h) // 2  # 15px ~ 41px

    for i in range(total_holes):
        hx = int(round(start_x + i * pitch))

        for draw, hy in [(d_top, hole_y_top), (d_bot, hole_y_bot)]:
            # 1단계: 외곽 미세 섀도우 림 (1px)
            draw.rounded_rectangle([hx - 1, hy - 1, hx + hole_w, hy + hole_h],
                                   radius=corner_r + 1, fill=(28, 20, 14, 255))
            # 2단계: 실물 필름 웜 앰버 골드 영사기 투과광 (은은한 백라이트)
            draw.rounded_rectangle([hx, hy, hx + hole_w - 1, hy + hole_h - 1],
                                   radius=corner_r, fill=(218, 168, 88, 240))
            # 3단계: 구멍 중심 따뜻한 샴페인 빛 (아날로그 투과 효과)
            draw.rounded_rectangle([hx + 1, hy + 1, hx + hole_w - 2, hy + hole_h - 2],
                                   radius=max(1, corner_r - 1), fill=(235, 185, 105, 255))

    print(f"🎬 실물 규격 35mm 타공 렌더링 완료: 상/하 각 {total_holes}개 구멍 (등간격 {pitch}px, 이빨 빠짐/겹침 0%!)")

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

    # 글자 백그라운드 섀도우
    t_glow = Image.new("RGBA", (safe_w, safe_h), (0, 0, 0, 0))
    d_tg = ImageDraw.Draw(t_glow)
    d_tg.ellipse([tx_in_slide - 25, ty_in_slide - 15,
                  tx_in_slide + target_tw + 25, ty_in_slide + target_th + 15],
                 fill=(10, 8, 5, 150))
    t_glow = t_glow.filter(ImageFilter.GaussianBlur(20))
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
    print("🎬 실물 규격 35mm 완벽 타공 배너 완성!")
    print(f"- 텍스트: {target_tw}x{target_th}px")
    print(f"- 뉴라: {neu_vis_w}x{neu_h}px")
    print(f"- 간격: {gap}px")
    print(f"- 좌측 여백: {actual_left}px, 우측 여백: {actual_right}px (오차: {abs(actual_left - actual_right)}px)")
    print("==================================================")

if __name__ == "__main__":
    build_authentic_35mm_precision_banner()
