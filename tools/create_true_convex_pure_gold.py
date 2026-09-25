#!/usr/bin/env python3
"""
create_true_convex_pure_gold.py —
오빠의 날카로운 3대 지적 100% 완전 수정:
1. 타원형 플래시 영구 박멸 (타원형 원 0%, 진짜 카메라 플래시 전체 노출 광택)
2. 정면 조명(Frontal Key Light) 투발로 맑고 눈부신 24K 순금 (탁한 갈색 0%, 맑은 샴페인 골드)
3. 2D 평면이 아닌 진짜 둥글게 볼록 솟아오른 3D 볼록 엠보스 (Convex Pillow Bevel)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
FONT_SWANKY = os.path.join(WORKSPACE, "assets", "fonts", "FontdinerSwanky-Regular.ttf")
IMAGES_DIR = os.path.join(WORKSPACE, "assets", "images")
OUT_IMG = os.path.join(IMAGES_DIR, "hookverse_badge_true_convex_pure_gold.png")
OUT_ART = r"C:\Users\june2\.gemini\antigravity-ide\brain\ca192b04-baee-4d55-a3f1-37e9601b7fd9\hookverse_badge_true_convex_pure_gold.png"

W, H = 380, 136

def render_real_convex_3d_text(font, text, cx, y_pos, base_w, base_h):
    """
    진짜 둥글게 솟아오른 볼록 3D 양각(True Convex Pillow Emboss)
    정면 스튜디오 조명(Frontal Studio Lighting)을 받아 글자 중심부가 가장 환하고 맑게 타오름
    """
    dummy = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dummy)
    bbox = d_draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = cx - tw // 2
    ty = y_pos

    # 1. 텍스트 마스크
    mask = Image.new("L", (base_w, base_h), 0)
    ImageDraw.Draw(mask).text((tx, ty), text, fill=255, font=font)

    # 2. 진짜 둥근 돔(Dome) 높이 맵 (Height Map) 생성
    # 다중 가우시안 블러로 안쪽이 볼록하게 솟아오르는 곡면 높이 계산
    h_map1 = mask.filter(ImageFilter.GaussianBlur(1.5))
    h_map2 = mask.filter(ImageFilter.GaussianBlur(3.5))
    h_map3 = mask.filter(ImageFilter.GaussianBlur(6.0))

    # 3. 정면 조명(Frontal Key Light) 음영 렌더링
    # 중심부는 정면 빛을 받아 가장 밝고 눈부신 24K 순금, 외곽은 부드럽게 둥글어지며 입체감 형성
    gold_surface = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    
    for y in range(base_h):
        for x in range(base_w):
            m = mask.getpixel((x, y))
            m_int = m[0] if isinstance(m, tuple) else (m or 0)
            if m_int > 0:
                v1 = h_map1.getpixel((x, y))
                v1_val = (v1[0] if isinstance(v1, tuple) else (v1 or 0)) / 255.0
                v2 = h_map2.getpixel((x, y))
                v2_val = (v2[0] if isinstance(v2, tuple) else (v2 or 0)) / 255.0
                v3 = h_map3.getpixel((x, y))
                v3_val = (v3[0] if isinstance(v3, tuple) else (v3 or 0)) / 255.0
                
                # 둥근 돔 높이 (중심부 1.0, 외곽 0.0)
                dome_height = v1_val * 0.4 + v2_val * 0.4 + v3_val * 0.2
                
                # 정면 조명에 의한 볼록 반사광 (구면 코사인)
                # 중심 능선이 가장 눈부신 샴페인 화이트골드
                if dome_height > 0.70:
                    # 최상단 눈부신 정면 하이라이트 (맑고 환한 순금빛)
                    t = (dome_height - 0.70) / 0.30
                    r = 255
                    g = int(245 + 10 * t)
                    b = int(140 + 115 * t)
                elif dome_height > 0.30:
                    # 24K 비비드 순금 코어 (탁함 0%, 맑고 화사한 황금)
                    t = (dome_height - 0.30) / 0.40
                    r = 255
                    g = int(195 + 50 * t)
                    b = int(20 + 120 * t)
                else:
                    # 둥근 모서리 음영 (맑은 따뜻한 앰버, 탁한 갈색 배제)
                    t = dome_height / 0.30
                    r = int(220 + 35 * t)
                    g = int(140 + 55 * t)
                    b = int(10 + 10 * t)

                gold_surface.putpixel((x, y), (r, g, b, 255))

    # 4. 정면 조명 림 하이라이트 (글자 테두리를 감싸는 얇은 순금 광택 림)
    rim_light = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rim_light)
    r_draw.text((tx, ty), text, fill=(255, 255, 230, 240), font=font)
    
    # 텍스트 외곽선을 깎아내는 정교한 엠보스 엣지
    inner_cut = mask.filter(ImageFilter.GaussianBlur(1.0))
    for y in range(base_h):
        for x in range(base_w):
            if mask.getpixel((x, y)) > 0:
                ic = inner_cut.getpixel((x, y))
                ic_val = ic[0] if isinstance(ic, tuple) else (ic or 0)
                # 모서리 경계선 추출
                if ic_val < 200:
                    gold_surface.putpixel((x, y), (255, 255, 240, 255))

    # 5. 글자 뒤 묵직한 3D 드롭 섀도우 (글자가 화면 밖으로 붕 떠오르는 입체감)
    shadow = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.text((tx + 2, ty + 4), text, fill=(0, 0, 0, 245), font=font)
    s_draw.text((tx + 3, ty + 6), text, fill=(0, 0, 0, 180), font=font)
    shadow = shadow.filter(ImageFilter.GaussianBlur(3.0))

    out = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    out = Image.alpha_composite(out, shadow)
    out = Image.alpha_composite(out, gold_surface)

    return out

def build_pure_convex_gold_badge():
    # 실제 숏폼 빗길 배경 로드
    bg_path = os.path.join(WORKSPACE, "assets", "images", "IMF2화_스틸_cut01_raw.png")
    if os.path.exists(bg_path):
        bg = Image.open(bg_path).convert("RGBA").crop((20, 40, 20 + 420, 40 + 176)).resize((420, 176))
    else:
        bg = Image.new("RGBA", (420, 176), (15, 18, 28, 255))

    badge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)

    # 1. 24K 순금 트윈 레일 (맑고 화사한 정면 조명 골드)
    # 상단 레일 2줄
    draw.line([(0, 2), (W, 2)], fill=(255, 250, 180, 255), width=2)
    draw.line([(0, 4), (W, 4)], fill=(200, 140, 20, 220), width=1)
    draw.line([(0, 22), (W, 22)], fill=(255, 225, 60, 240), width=1)
    draw.line([(0, 23), (W, 23)], fill=(160, 100, 10, 200), width=1)

    # 하단 레일 2줄
    draw.line([(0, H - 23), (W, H - 23)], fill=(255, 225, 60, 240), width=1)
    draw.line([(0, H - 22), (W, H - 22)], fill=(160, 100, 10, 200), width=1)
    draw.line([(0, H - 4), (W, H - 4)], fill=(255, 250, 180, 255), width=2)
    draw.line([(0, H - 2), (W, H - 2)], fill=(200, 140, 20, 220), width=1)

    # 2. 투명 스프로킷 홀
    num_holes = 8
    hole_w, hole_h = 18, 11
    step = W / float(num_holes)
    for i in range(num_holes):
        x = int(i * step + (step - hole_w) / 2)
        # 상단 홀
        draw.rounded_rectangle([x-1, 6, x + hole_w + 1, 6 + hole_h + 2], radius=3, outline=(255, 245, 160, 240), width=1)
        draw.rounded_rectangle([x, 7, x + hole_w, 7 + hole_h], radius=2, outline=(140, 80, 10, 220), width=1)
        # 하단 홀
        draw.rounded_rectangle([x-1, H - 19, x + hole_w + 1, H - 19 + hole_h + 2], radius=3, outline=(255, 245, 160, 240), width=1)
        draw.rounded_rectangle([x, H - 18, x + hole_w, H - 18 + hole_h], radius=2, outline=(140, 80, 10, 220), width=1)

    # 3. 2026 레트로 마킹
    try:
        small_font = ImageFont.load_default()
    except Exception:
        small_font = None

    if small_font:
        draw.text((15, 6), "▶ 2026 KAIRA 500T", fill=(255, 245, 170, 255), font=small_font)
        draw.text((W - 105, 6), "SAFETY FILM 35mm", fill=(255, 245, 170, 230), font=small_font)
        draw.text((15, H - 17), "ISO 500 / 3200K", fill=(255, 245, 170, 230), font=small_font)
        draw.text((W - 95, H - 17), "FRAME 26 ▶▶", fill=(255, 245, 170, 255), font=small_font)

    # 4. 정면 조명 3D 볼록 텍스트 합성
    font = ImageFont.truetype(FONT_SWANKY, 38)
    cx = W // 2
    y_center = H // 2
    b1 = draw.textbbox((0, 0), "Hookverse", font=font)
    h1 = b1[3] - b1[1]
    b2 = draw.textbbox((0, 0), "Studio", font=font)
    h2 = b2[3] - b2[1]
    start_y = y_center - (h1 + 4 + h2) // 2

    layer1 = render_real_convex_3d_text(font, "Hookverse", cx, start_y, W, H)
    layer2 = render_real_convex_3d_text(font, "Studio", cx, start_y + h1 + 4, W, H)

    badge = Image.alpha_composite(badge, layer1)
    badge = Image.alpha_composite(badge, layer2)

    # 빗길 배경 위에 합성
    bg.paste(badge, (20, 20), badge)
    bg.save(OUT_IMG)
    bg.save(OUT_ART)
    print(f"[+] 맑고 화사한 정면 조명 볼록 3D 골드 스틸 렌더링 완료: {OUT_IMG}")

if __name__ == "__main__":
    build_pure_convex_gold_badge()
