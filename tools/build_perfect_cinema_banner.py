import os
import math
from PIL import Image, ImageDraw, ImageFilter

def build_original_amber_banner():
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
    w1, h1 = img1.size

    rail_h = 56
    inner_h = safe_h - (rail_h * 2)  # 311px

    # 2. 정품 필름 상하 스프로킷 타공 레일 추출 및 타일링
    rail_top_src = img1.crop((0, 0, w1, 95))
    rail_bottom_src = img1.crop((0, 585, w1, h1))

    rail_top = Image.new("RGBA", (safe_w, rail_h))
    rail_bottom = Image.new("RGBA", (safe_w, rail_h))

    tile_w = int(rail_h * (w1 / 95.0) * 0.42)
    t_tile = rail_top_src.resize((tile_w, rail_h), Image.Resampling.LANCZOS)
    b_tile = rail_bottom_src.resize((tile_w, rail_h), Image.Resampling.LANCZOS)

    x = 0
    while x < safe_w:
        rail_top.paste(t_tile, (x, 0))
        rail_bottom.paste(b_tile, (x, 0))
        x += tile_w

    # 3. ★ 오빠가 말씀하신 원본 '따뜻한 앰버 브라운' 필름 내부 바탕색 복원!
    inner = Image.new("RGBA", (safe_w, inner_h), (20, 14, 10, 255))
    for y in range(inner_h):
        ny = (y - inner_h / 2.0) / (inner_h / 2.0)
        for xx in range(safe_w):
            nx = (xx - safe_w / 2.0) / (safe_w / 2.0)
            dist = math.sqrt((nx * 1.35) ** 2 + ny ** 2)
            intensity = max(0.0, 1.0 - min(1.0, dist)) ** 1.3
            # 따뜻한 앰버 브라운 톤 그라데이션
            r = int(24 + (92 - 24) * intensity)
            g = int(15 + (62 - 15) * intensity)
            b = int(10 + (32 - 10) * intensity)
            inner.putpixel((xx, y), (r, g, b, 255))

    # 빈티지 필름 가죽 질감 블렌딩 (오리지널 텍스처)
    leather = img1.crop((910, 150, 1010, 550)).resize((safe_w, inner_h), Image.Resampling.LANCZOS)
    inner = Image.blend(inner, leather, 0.22)

    # 좌우 사이드 필름 번(Burn) 앰버 빛 효과
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

    # 필름 슬라이드 조립
    film_slide = Image.new("RGBA", (safe_w, safe_h), (12, 8, 6, 255))
    film_slide.paste(rail_top, (0, 0))
    film_slide.paste(inner, (0, rail_h))
    film_slide.paste(rail_bottom, (0, safe_h - rail_h))

    # 4. [초고해상도] 3D Chrome HOOKVERSE STUDIO 텍스트
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

    # 글자 크기: 높이 210px로 확대하여 시원하게
    target_th = 210
    target_tw = int(target_th * (tw / float(th)))
    text_scaled = clean_text.resize((target_tw, target_th), Image.Resampling.LANCZOS)
    text_scaled = text_scaled.filter(ImageFilter.UnsharpMask(radius=1.8, percent=150, threshold=2))

    # 5. [초고해상도] 뉴라 상반신 바스트 실루엣 (허리 샷 ❌ -> 바스트 상반신 샷 ⭕)
    neura_full = Image.open(neura_path).convert("RGBA")
    # 바스트/언더바스트 라인까지 크롭 (상단 42%)
    crop_box = (0, 0, neura_full.width, int(neura_full.height * 0.42))
    neura_crop = neura_full.crop(crop_box).transpose(Image.Transpose.FLIP_LEFT_RIGHT)

    # 상반신이 크게 보이도록 높이 335px로 당당하게 확대
    neu_h = 335
    neu_w = int(neu_h * (neura_crop.width / neura_crop.height))
    neura_scaled = neura_crop.resize((neu_w, neu_h), Image.Resampling.LANCZOS)

    # 타원형 스포트라이트 조명 (흰바탕이 앰버 조명을 받아 부드럽게 빛남)
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

    # 뉴라의 시각적 가시 너비 BBox
    n_bbox = neura_scaled.split()[-1].getbbox()
    neu_vis_w = (n_bbox[2] - n_bbox[0]) if n_bbox else neu_w

    # 6. ★ 완벽한 대칭 배치 (글자와 뉴라 사이 간격 38px, 좌우 여백 100% 동일)
    gap = 38
    total_group_w = target_tw + gap + neu_vis_w
    side_margin = (safe_w - total_group_w) // 2

    # 필름 슬라이드 내부 좌표
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

    # 7. 전체 캔버스 (2560 x 1440)에 안전영역 필름 슬라이드 결합
    c = Image.new("RGBA", (W, H), (6, 7, 12, 255))
    c.paste(film_slide, (safe_x1, safe_y1))

    # 저장 경로
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
    print("🎬 오리지널 앰버 브라운 필름 배너 완성!")
    print(f"- 텍스트: {target_tw}x{target_th}px")
    print(f"- 뉴라 바스트: {neu_vis_w}x{neu_h}px")
    print(f"- 간격: {gap}px")
    print(f"- 좌측 여백: {actual_left}px, 우측 여백: {actual_right}px (오차: {abs(actual_left - actual_right)}px)")
    print("==================================================")

if __name__ == "__main__":
    build_original_amber_banner()
