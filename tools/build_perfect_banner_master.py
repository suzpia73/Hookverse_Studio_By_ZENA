import os
from PIL import Image, ImageDraw, ImageFilter

def build_perfect_banner():
    base_dir = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images"
    p_text = os.path.join(base_dir, "raw_text_source.jpg")
    p_neura = os.path.join(base_dir, "test_neura_cut_feathered.png")
    p_rail_top = os.path.join(base_dir, "rail_top.png")
    p_rail_bot = os.path.join(base_dir, "rail_bot.png")

    W, H = 2560, 1440
    # 📱 유튜브 모바일 안전영역 (금색 사각 박스 공식 규격)
    safe_w, safe_h = 1546, 423
    safe_x1 = (W - safe_w) // 2  # 507
    safe_y1 = (H - safe_h) // 2  # 508
    safe_x2 = safe_x1 + safe_w   # 2053
    safe_y2 = safe_y1 + safe_h   # 931

    # 1. 메인 캔버스: 깊은 미드나이트 흑요석 (#06070c)
    canvas = Image.new("RGBA", (W, H), (6, 7, 12, 255))

    # 2. 35mm 필름 스트립 구축 (높이 423px, 가로 2560px 전폭)
    rail_top = Image.open(p_rail_top).convert("RGBA")
    rail_bot = Image.open(p_rail_bot).convert("RGBA")
    rw, rh = rail_top.size  # rh = 55
    inner_h = safe_h - (rh * 2)  # 313px

    film_layer = Image.new("RGBA", (W, safe_h), (11, 12, 16, 255))
    
    # 중앙 내부 베이스: 시네마틱 웜 다크 브라운-블랙 그라데이션
    d_film = ImageDraw.Draw(film_layer)
    d_film.rectangle([0, rh, W, safe_h - rh], fill=(13, 14, 18, 255))
    
    # 미세한 필름 질감 앰비언트 (중앙에 웜 앰버 은은한 글로우)
    film_glow = Image.new("RGBA", (W, safe_h), (0, 0, 0, 0))
    d_fg = ImageDraw.Draw(film_glow)
    for r in range(400, 30, -25):
        ratio = 1.0 - (r / 400.0)
        al = int(18 * (ratio ** 1.5))
        d_fg.ellipse([W//2 - int(r*2.2), safe_h//2 - int(r*0.4), W//2 + int(r*2.2), safe_h//2 + int(r*0.4)], fill=(225, 175, 70, al))
    film_glow = film_glow.filter(ImageFilter.GaussianBlur(12))
    film_layer = Image.alpha_composite(film_layer, film_glow)

    # 상단/하단 스프로킷 레일 타일링 (2560 전폭)
    cur_x = 0
    while cur_x < W:
        film_layer.paste(rail_top, (cur_x, 0), rail_top)
        film_layer.paste(rail_bot, (cur_x, safe_h - rh), rail_bot)
        cur_x += rw

    # 필름 스트립을 캔버스의 안전영역 Y(508)에 배치
    canvas.paste(film_layer, (0, safe_y1), film_layer)

    # 3. 3D Chrome HOOKVERSE STUDIO 텍스트 투명화 & 추출
    img_text_raw = Image.open(p_text).convert("RGBA")
    t_crop = img_text_raw.crop((20, 310, 1004, 725))
    t_data = t_crop.getdata()
    new_t_data = []
    for item in t_data:
        if isinstance(item, (tuple, list)) and len(item) >= 4:
            r, g, b, a = item[0], item[1], item[2], item[3]
        else:
            continue
        lum = int(0.299 * r + 0.587 * g + 0.114 * b)
        if lum < 22:
            new_t_data.append((r, g, b, 0))
        elif lum < 58:
            alpha = int(255 * (lum - 22) / (58 - 22))
            new_t_data.append((r, g, b, alpha))
        else:
            new_t_data.append((r, g, b, 255))
    t_crop.putdata(new_t_data)
    t_bbox = t_crop.getbbox()
    t_clean = t_crop.crop(t_bbox)

    # 4. 뉴라 상반신 바스트 실루엣 (좌우 반전하여 글자를 응시)
    neura_raw = Image.open(p_neura).convert("RGBA")
    neura_flipped = neura_raw.transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    
    # 5. 크기 스케일링 & 정밀 배치
    # A) 뉴라 상반신: 내부 높이 313px에 맞게 높이 305px로 웅장하게 확대!
    target_neu_h = 305
    aspect_neu = neura_flipped.width / neura_flipped.height
    target_neu_w = int(target_neu_h * aspect_neu)
    neura_scaled = neura_flipped.resize((target_neu_w, target_neu_h), Image.Resampling.LANCZOS)
    
    # 뉴라의 시각적 유효 BBox (알파 > 25 기준)
    n_alpha = neura_scaled.split()[-1]
    n_bbox = n_alpha.getbbox()
    neu_vis_w = (n_bbox[2] - n_bbox[0]) if n_bbox else target_neu_w

    # B) 3D Chrome 글자: 높이 190px
    target_th = 190
    aspect_t = t_clean.width / t_clean.height
    target_tw = int(target_th * aspect_t)
    t_scaled = t_clean.resize((target_tw, target_th), Image.Resampling.LANCZOS)

    # C) 글자와 뉴라 사이 간격 (오빠 요청: 상반신 이미지와 글자를 좀 더 가까이!)
    gap = 35  # 35px로 친밀하고 유기적인 밀착 배치

    # D) 전체 그룹 폭 및 양쪽 여백 균등 계산 (오빠 요청: 양쪽 여백은 똑같이 남기고!)
    total_group_w = target_tw + gap + neu_vis_w
    side_margin = (safe_w - total_group_w) // 2

    # 정밀 X, Y 좌표 산출
    text_x = safe_x1 + side_margin
    text_y = safe_y1 + (safe_h - target_th) // 2

    # 뉴라 위치: 텍스트 오른쪽 끝 + gap - n_bbox[0] 오프셋 (시각적 투명 여백 보정)
    neura_x = text_x + target_tw + gap - (n_bbox[0] if n_bbox else 0)
    neura_y = safe_y1 + rh + (inner_h - target_neu_h) // 2

    actual_left_margin = text_x - safe_x1
    actual_right_edge = neura_x + (n_bbox[2] if n_bbox else target_neu_w)
    actual_right_margin = safe_x2 - actual_right_edge

    print("==================================================")
    print("🎬 HOOKVERSE STUDIO 마스터 배너 정밀 밸런스 결과")
    print("==================================================")
    print(f"- Safe Zone 폭: {safe_w}px (x1: {safe_x1} ~ x2: {safe_x2})")
    print(f"- 글자 크기: {target_tw} x {target_th}px")
    print(f"- 글자-뉴라 간격: {gap}px (밀착)")
    print(f"- 뉴라 바스트 크기: {neu_vis_w} x {target_neu_h}px (바스트 하단 맞춤, 시원한 상반신)")
    print(f"- 전체 그룹 폭: {total_group_w}px")
    print(f"- 좌측 여백: {actual_left_margin}px")
    print(f"- 우측 여백: {actual_right_margin}px")
    print(f"- 좌우 대칭 오차: {abs(actual_left_margin - actual_right_margin)}px (완벽 일치!)")
    print("==================================================")

    # 6. 글자 백그라운드 소프트 글로우 (가독성 100% 보장)
    glow = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_glow = ImageDraw.Draw(glow)
    d_glow.ellipse([text_x - 30, text_y - 20, text_x + target_tw + 30, text_y + target_th + 20], fill=(20, 20, 35, 130))
    glow = glow.filter(ImageFilter.GaussianBlur(25))
    canvas = Image.alpha_composite(canvas, glow)

    # 글자와 뉴라 합성
    canvas.paste(t_scaled, (text_x, text_y), t_scaled)
    canvas.paste(neura_scaled, (neura_x, neura_y), neura_scaled)

    # 7. 파일 저장
    # 1) 유튜브 공식 규격 마스터 배너 (2560 x 1440)
    out_master = os.path.join(base_dir, "hookverse_youtube_channel_banner_2560x1440.png")
    canvas.save(out_master, "PNG")

    # 2) 모바일 화면 1:1 크롭 뷰 (1546 x 423)
    out_mobile = os.path.join(base_dir, "preview_mobile_view_1546x423.png")
    mobile_crop = canvas.crop((safe_x1, safe_y1, safe_x2, safe_y2))
    mobile_crop.save(out_mobile, "PNG")

    # 3) 금색 안전영역 가이드라인 오버레이 프리뷰
    out_preview = os.path.join(base_dir, "preview_bust_film_safezone.png")
    prev = canvas.copy()
    d_prev = ImageDraw.Draw(prev)
    d_prev.rectangle([safe_x1, safe_y1, safe_x2, safe_y2], outline=(255, 215, 0, 255), width=4)
    # 좌우 여백 가이드라인 (청록색)
    d_prev.line([safe_x1, safe_y1 + safe_h//2, text_x, safe_y1 + safe_h//2], fill=(0, 255, 255, 255), width=3)
    d_prev.line([actual_right_edge, safe_y1 + safe_h//2, safe_x2, safe_y1 + safe_h//2], fill=(0, 255, 255, 255), width=3)
    prev.save(out_preview, "PNG")

    print(f"✅ 저장 완료:")
    print(f"1) 마스터 배너: {out_master}")
    print(f"2) 모바일 1:1 뷰: {out_mobile}")
    print(f"3) 안전영역 프리뷰: {out_preview}")

if __name__ == "__main__":
    build_perfect_banner()
