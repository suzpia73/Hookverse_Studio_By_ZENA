import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter

def generate_perfect_symmetric_banner():
    W, H = 2560, 1440
    
    # 📱 금색 사각 라인 = 모바일(휴대폰) 화면 전체 사이즈 (1546 x 423)
    safe_w, safe_h = 1546, 423
    safe_x1 = (W - safe_w) // 2  # 507
    safe_y1 = (H - safe_h) // 2  # 508
    safe_x2 = safe_x1 + safe_w   # 2053
    safe_y2 = safe_y1 + safe_h   # 931
    safe_cx = W // 2             # 1280

    # 1. 캔버스: 미드나이트 흑요석 (#06070c)
    canvas = Image.new("RGBA", (W, H), (6, 7, 12, 255))
    
    # 앰버 골드 & 샴페인 오라 레이어
    aura = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    d_aura = ImageDraw.Draw(aura)
    
    for r in range(1250, 60, -30):
        ratio = 1.0 - (r / 1250.0)
        al_gold = int(24 * (ratio ** 1.5))
        d_aura.ellipse([safe_cx - int(r*1.8), H//2 - int(r*0.75), safe_cx + int(r*1.8), H//2 + int(r*0.75)], fill=(225, 175, 60, al_gold))
        
    random.seed(1004)
    for _ in range(120):
        px = random.randint(safe_x1 - 200, safe_x2 + 200)
        py = random.randint(safe_y1 - 100, safe_y2 + 100)
        pr = random.randint(1, 4)
        pa = random.randint(30, 140)
        d_aura.ellipse([px - pr, py - pr, px + pr, py + pr], fill=(255, 235, 175, pa))

    aura = aura.filter(ImageFilter.GaussianBlur(8))
    canvas = Image.alpha_composite(canvas, aura)

    # 폰트 로드
    font_bold_path = r"C:\Windows\Fonts\malgunbd.ttf"
    if not os.path.exists(font_bold_path):
        font_bold_path = r"C:\Windows\Fonts\arialbd.ttf"

    font_brand = ImageFont.truetype(font_bold_path, 50)
    font_slogan_kr = ImageFont.truetype(font_bold_path, 24)
    font_sub_ip = ImageFont.truetype(font_bold_path, 16)
    font_handle = ImageFont.truetype(font_bold_path, 19)

    # [준비 1] 텍스트 폭 정밀 측정
    temp_img = Image.new("RGBA", (10, 10))
    d_temp = ImageDraw.Draw(temp_img)
    
    title_text = "HOOKVERSE STUDIO"
    slogan_text = "새로운 시선이 당신의 상상을 깨우는 곳"
    ip_text = "스토리텔링  ·  웹툰  ·  웹소설  ·  음악 & OST"
    handle_text = "@hookverse_studio"
    
    t_bbox = d_temp.textbbox((0, 0), title_text, font=font_brand)
    s_bbox = d_temp.textbbox((0, 0), slogan_text, font=font_slogan_kr)
    ip_bbox = d_temp.textbbox((0, 0), ip_text, font=font_sub_ip)
    
    title_w = t_bbox[2] - t_bbox[0]   # 약 460px
    slogan_w = s_bbox[2] - s_bbox[0]  # 약 410px
    text_w = max(title_w, slogan_w)
    
    # [준비 2] 엠블럼 규격
    logo_size = 250  # 250 x 250
    
    # [준비 3] 뉴라 캐릭터 (상반신 크롭 & 좌우 반전 & 마스크)
    neura_path = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\G3캐릭터앵커LOCK\전신_우측.jpg"
    neura_full = Image.open(neura_path).convert("RGBA")
    crop_box = (0, 0, neura_full.width, int(neura_full.height * 0.52))
    neura_crop = neura_full.crop(crop_box).transpose(Image.Transpose.FLIP_LEFT_RIGHT)
    
    neu_h = 750
    aspect = neura_crop.width / neura_crop.height
    neu_w = int(neu_h * aspect)
    neura_scaled = neura_crop.resize((neu_w, neu_h), Image.Resampling.LANCZOS)
    
    # 알파 마스크: 뉴라의 몸통을 살리고 주변 회색 스튜디오 배경은 부드럽게 감쇠
    mask = Image.new("L", (neu_w, neu_h), 0)
    m_draw = ImageDraw.Draw(mask)
    body_cx = int(neu_w * 0.52)
    body_cy = int(neu_h * 0.48)
    
    for r in range(290, 20, -10):
        al = int(255 * (1.0 - (r / 290.0) ** 2.2))
        m_draw.ellipse([body_cx - int(r*0.65), body_cy - int(r*1.15), body_cx + int(r*0.65), body_cy + int(r*1.15)], fill=al)
        
    mask = mask.filter(ImageFilter.GaussianBlur(20))
    neura_scaled.putalpha(mask)
    
    # 뉴라의 실제 시각적 가시 너비(알파 > 25인 BBox)
    bbox = neura_scaled.getbbox()
    neu_vis_w = bbox[2] - bbox[0] if bbox else neu_w
    neu_offset_left = bbox[0] if bbox else 0
    neu_offset_right = neu_w - bbox[2] if bbox else 0
    
    print(f"Text width: {text_w}, Logo width: {logo_size}, Neura visual width: {neu_vis_w}")

    # =========================================================================
    # ★ 좌우 균등 대칭 황금 공식 (오빠의 지침 100% 반영)
    #
    # 금색 사각 박스(휴대폰 사이즈: 1546px) 안에서:
    # [왼쪽 여백 Margin] == [오른쪽 여백 Margin] 완벽 일치!
    #
    # 구성 요소:
    # 1) 좌측: 엠블럼 (폭 250px)
    # 2) 간격 G1: 엠블럼과 텍스트 사이 (약 45px)
    # 3) 중앙: 텍스트 & 배지 그룹 (폭 text_w 약 460px)
    # 4) 간격 G2: 텍스트와 뉴라 사이 (약 65px - 텍스트와 절대 안 겹침!)
    # 5) 우측: 뉴라 (시각적 폭 neu_vis_w 약 380px)
    #
    # 총 콘텐츠 폭 = 250 + 45 + text_w + 65 + neu_vis_w
    # 여백 Margin = (1546 - 총 콘텐츠 폭) // 2
    # =========================================================================
    
    gap1 = 45
    gap2 = 65
    total_content_w = logo_size + gap1 + text_w + gap2 + neu_vis_w
    side_margin = (safe_w - total_content_w) // 2
    
    print(f"Total Content Width: {total_content_w}")
    print(f"Calculated Side Margin: {side_margin} px (Left == Right!)")

    # 1. 엠블럼 위치 (금색 박스 왼쪽 선 safe_x1 에서 side_margin 만큼 띄움)
    lx = safe_x1 + side_margin
    ly = safe_y1 + (safe_h - logo_size) // 2

    # 2. 텍스트 그룹 위치
    tx = lx + logo_size + gap1
    bx = tx
    by = safe_y1 + 45

    # 3. 뉴라 캐릭터 위치
    # 뉴라의 시각적 시작점 = tx + text_w + gap2
    neu_vis_start = tx + text_w + gap2
    neu_x = neu_vis_start - neu_offset_left
    
    # ★ 오빠의 혜안 100% 반영: 휴대폰(금색 사각 박스)에서 정수리/이마가 잘리지 않고
    # 매력적인 옆모습 얼굴 전체(이마~눈~코~입~턱선)가 황금비율로 온전히 드러나도록 수직 위치 조정!
    # (기존 -135px -> -30px로 약 105px 내려서 모바일 화면 안에 얼굴이 쏙 들어옴)
    neu_y = safe_y1 - 30

    # 뉴라의 시각적 끝점과 오른쪽 여백 검증
    neu_vis_end = neu_vis_start + neu_vis_w
    right_margin = safe_x2 - neu_vis_end
    print(f"Left margin: {lx - safe_x1} px, Right margin: {right_margin} px")

    # [1] 엠블럼 렌더링
    logo_path = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\hookverse_studio_logo_transparent.png"
    if os.path.exists(logo_path):
        logo_raw = Image.open(logo_path).convert("RGBA")
        logo_scaled = logo_raw.resize((logo_size, logo_size), Image.Resampling.LANCZOS)
        
        glow_box = Image.new("RGBA", (logo_size + 140, logo_size + 140), (0, 0, 0, 0))
        g_draw = ImageDraw.Draw(glow_box)
        gc = (logo_size + 140) // 2
        for r in range(130, 20, -15):
            al = int(35 * (1.0 - r / 130))
            g_draw.ellipse([gc - r, gc - r, gc + r, gc + r], fill=(220, 165, 40, al))
        glow_box = glow_box.filter(ImageFilter.GaussianBlur(18))
        
        canvas.paste(glow_box, (lx - 70, ly - 70), glow_box)
        canvas.paste(logo_scaled, (lx, ly), logo_scaled)

    # [2] 배지 렌더링
    badge_path = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\hookverse_top_left_badge.png"
    if os.path.exists(badge_path):
        badge_raw = Image.open(badge_path).convert("RGBA")
        bw, bh = int(badge_raw.width * 0.95), int(badge_raw.height * 0.95)
        badge_scaled = badge_raw.resize((bw, bh), Image.Resampling.LANCZOS)
        
        b_shadow = Image.new("RGBA", (bw + 20, bh + 20), (0, 0, 0, 0))
        bs_draw = ImageDraw.Draw(b_shadow)
        bs_draw.rectangle([10, 10, bw + 10, bh + 10], fill=(0, 0, 0, 180))
        b_shadow = b_shadow.filter(ImageFilter.GaussianBlur(8))
        canvas.paste(b_shadow, (bx - 10, by - 5), b_shadow)
        canvas.paste(badge_scaled, (bx, by), badge_scaled)

    # [3] 텍스트 레이어
    text_canvas = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    t_draw = ImageDraw.Draw(text_canvas)

    ty = safe_y1 + 186

    # 메인 타이틀: "HOOKVERSE STUDIO"
    t_draw.text((tx + 3, ty + 3), title_text, font=font_brand, fill=(0, 0, 0, 240))
    t_draw.text((tx + 1, ty + 1), title_text, font=font_brand, fill=(40, 25, 5, 200))
    for ox, oy in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
        t_draw.text((tx + ox, ty + oy), title_text, font=font_brand, fill=(190, 140, 30, 140))
    t_draw.text((tx, ty), title_text, font=font_brand, fill=(255, 238, 185, 255))

    # 한글 슬로건
    sy = ty + 74
    t_draw.text((tx + 2, sy + 2), slogan_text, font=font_slogan_kr, fill=(0, 0, 0, 220))
    t_draw.text((tx, sy), slogan_text, font=font_slogan_kr, fill=(245, 215, 145, 255))

    # 서브 IP 라벨
    iy = sy + 38
    t_draw.text((tx + 1, iy + 1), ip_text, font=font_sub_ip, fill=(0, 0, 0, 200))
    t_draw.text((tx, iy), ip_text, font=font_sub_ip, fill=(195, 180, 150, 240))

    # 채널 핸들 캡슐
    hy = iy + 32
    cap_w = 250
    cap_h = 32
    t_draw.rounded_rectangle([tx, hy, tx + cap_w, hy + cap_h], radius=8, fill=(18, 20, 26, 230), outline=(218, 165, 32, 220), width=2)
    t_draw.ellipse([tx + 12, hy + 7, tx + 25, hy + 20], fill=(255, 30, 30, 255))
    t_draw.polygon([(tx + 16, hy + 10), (tx + 16, hy + 17), (tx + 21, hy + 14)], fill=(255, 255, 255, 255))
    t_draw.text((tx + 32, hy + 3), handle_text, font=font_handle, fill=(255, 220, 80, 255))

    canvas = Image.alpha_composite(canvas, text_canvas)

    # [4] 뉴라 캐릭터 렌더링
    halo = Image.new("RGBA", (neu_w + 120, neu_h + 120), (0, 0, 0, 0))
    d_halo = ImageDraw.Draw(halo)
    hc_x, hc_y = neu_w // 2 + 30, neu_h // 2
    for r in range(260, 40, -20):
        al = int(30 * (1.0 - r / 260))
        d_halo.ellipse([hc_x - r, hc_y - r, hc_x + r, hc_y + r], fill=(235, 185, 75, al))
    halo = halo.filter(ImageFilter.GaussianBlur(28))
    
    canvas.paste(halo, (neu_x - 60, neu_y - 60), halo)
    canvas.paste(neura_scaled, (neu_x, neu_y), neura_scaled)

    # 저장
    output_dir = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images"
    banner_path = os.path.join(output_dir, "hookverse_youtube_channel_banner_2560x1440.png")
    canvas.save(banner_path, "PNG", optimize=True)
    print(f"Perfect Symmetric Banner Saved: {banner_path}")

    # 세이프존 프리뷰 저장
    preview = canvas.copy()
    p_draw = ImageDraw.Draw(preview)
    p_draw.rectangle([0, safe_y1, W, safe_y2], outline=(0, 220, 255, 200), width=3)
    p_draw.text((60, safe_y1 + 15), "💻 DESKTOP DISPLAY (2560 x 423)", font=font_slogan_kr, fill=(0, 230, 255, 240))
    p_draw.rectangle([safe_x1, safe_y1, safe_x2, safe_y2], outline=(255, 215, 0, 255), width=4)
    p_draw.text((safe_x1 + 20, safe_y2 - 38), f"📱 MOBILE SAFE ZONE (1546 x 423) - 좌우 여백 {side_margin}px 완벽 일치", font=font_slogan_kr, fill=(255, 215, 0, 255))
    p_draw.text((60, 60), "📺 TV DISPLAY AREA (2560 x 1440 FULL SCREEN)", font=font_slogan_kr, fill=(220, 220, 220, 220))
    
    # 좌우 여백 표시 가이드라인 (시각적 확인용)
    p_draw.line([(safe_x1, ly + logo_size//2), (lx, ly + logo_size//2)], fill=(255, 100, 100, 220), width=3)
    p_draw.line([(neu_vis_end, ly + logo_size//2), (safe_x2, ly + logo_size//2)], fill=(255, 100, 100, 220), width=3)
    p_draw.text((safe_x1 + 10, ly + logo_size//2 - 25), f"좌측여백: {side_margin}px", font=font_sub_ip, fill=(255, 120, 120, 255))
    p_draw.text((safe_x2 - 130, ly + logo_size//2 - 25), f"우측여백: {right_margin}px", font=font_sub_ip, fill=(255, 120, 120, 255))

    preview_path = os.path.join(output_dir, "hookverse_channel_banner_safezone_preview.png")
    preview.save(preview_path, "PNG")
    print(f"Safezone Preview Saved: {preview_path}")

if __name__ == "__main__":
    generate_perfect_symmetric_banner()
