#!/usr/bin/env python3
"""
generate_badge_options.py — 시안 B(티켓/데님 스터브) & 시안 C(루미너스 화이트 페이드) 고해상도 생성기
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
FONT_PATH = os.path.join(WORKSPACE, "assets", "fonts", "FontdinerSwanky-Regular.ttf")
OUT_B = os.path.join(WORKSPACE, "assets", "images", "badge_option_b_ticket.png")
OUT_C = os.path.join(WORKSPACE, "assets", "images", "badge_option_c_luminous.png")

def get_text_metrics():
    font = ImageFont.truetype(FONT_PATH, 44)
    dummy = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    d = ImageDraw.Draw(dummy)
    b1 = d.textbbox((0, 0), "Hookverse", font=font)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    b2 = d.textbbox((0, 0), "Studio", font=font)
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]
    return font, w1, h1, w2, h2

def make_option_b():
    # 시안 B: 1997 아날로그 티켓 스터브 & 데님 실밥 타공 엣지
    font, w1, h1, w2, h2 = get_text_metrics()
    line_spacing = 6
    pad_y = 14
    pad_x = 24
    
    max_w = max(w1, w2)
    W = int(max_w + pad_x * 2 + 25) # 우측 티켓 엣지 여유 25px
    H = int(h1 + line_spacing + h2 + pad_y * 2)

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    
    c_start = (8, 20, 38)     # 딥 네이비
    c_end = (0, 91, 234)      # 일렉트릭 블루

    # 1. 그라데이션 베이스 채우기
    base_w = W - 20
    for x in range(W):
        ratio = min(1.0, x / max(1, base_w))
        r = int(c_start[0] + (c_end[0] - c_start[0]) * ratio)
        g = int(c_start[1] + (c_end[1] - c_start[1]) * ratio)
        b = int(c_start[2] + (c_end[2] - c_start[2]) * ratio)
        for y in range(H):
            img.putpixel((x, y), (r, g, b, 255))

    # 2. 우측 티켓 톱니 타공(Ticket Perforation / Zigzag cutout) 마스크
    # 우측 15px 구간에 아날로그 티켓 반원 펀칭 및 지그재그 엣지 적용
    draw = ImageDraw.Draw(img)
    
    # 상단/하단 절취 홈 (반원 노치)
    draw.pieslice([base_w - 6, -8, base_w + 10, 8], 0, 360, fill=(0, 0, 0, 0))
    draw.pieslice([base_w - 6, H - 8, base_w + 10, H + 8], 0, 360, fill=(0, 0, 0, 0))
    
    # 우측 세로 절취선 점선 타공 효과 (Ticket Punch Holes)
    num_holes = 7
    step = H / (num_holes + 1)
    for i in range(1, num_holes + 1):
        cy = int(i * step)
        draw.ellipse([base_w - 2, cy - 3, base_w + 4, cy + 3], fill=(0, 0, 0, 0))

    # 끝단 지그재그 실밥 마감 (Frayed hem / Zigzag)
    for y in range(H):
        # 톱니 파동
        wave_offset = int(math.sin(y * 0.45) * 3) + int(math.sin(y * 0.9) * 2)
        cut_x = base_w + 8 + wave_offset
        for x in range(cut_x, W):
            img.putpixel((x, y), (0, 0, 0, 0))

    # 3. 텍스트 렌더링
    x1 = pad_x
    x2 = pad_x + (max_w - w2) // 2
    start_y = pad_y - 2

    # 드롭 섀도우
    draw.text((x1 + 1, start_y + 1), "Hookverse", fill=(0, 0, 0, 150), font=font)
    draw.text((x2 + 1, start_y + h1 + line_spacing + 1), "Studio", fill=(0, 0, 0, 150), font=font)
    # 순백색 본문
    draw.text((x1, start_y), "Hookverse", fill=(255, 255, 255, 255), font=font)
    draw.text((x2, start_y + h1 + line_spacing), "Studio", fill=(255, 255, 255, 255), font=font)

    # 테두리 라인
    draw.rectangle([0, 0, base_w, H-1], outline=(0, 160, 255, 140), width=1)

    img.save(OUT_B, "PNG")
    print(f"[+] ✅ 시안 B 생성 완료: {OUT_B} ({W}x{H})")

def make_option_c():
    # 시안 C: 루미너스 화이트-사이언 페이드 엣지
    font, w1, h1, w2, h2 = get_text_metrics()
    line_spacing = 6
    pad_y = 14
    pad_x = 24
    
    max_w = max(w1, w2)
    fade_w = 45 # 우측 빛의 페이드 구간 45px
    W = int(max_w + pad_x * 2 + fade_w)
    H = int(h1 + line_spacing + h2 + pad_y * 2)

    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    
    c_start = (8, 20, 38)     # 딥 네이비
    c_mid = (0, 91, 234)      # 일렉트릭 블루
    c_glow = (220, 245, 255)  # 눈부신 루미너스 화이트-사이언 광원

    solid_w = W - fade_w

    for x in range(W):
        if x < solid_w:
            # 좌측~중앙: 딥 네이비 -> 일렉트릭 블루
            ratio = x / max(1, solid_w)
            r = int(c_start[0] + (c_mid[0] - c_start[0]) * ratio)
            g = int(c_start[1] + (c_mid[1] - c_start[1]) * ratio)
            b = int(c_start[2] + (c_mid[2] - c_start[2]) * ratio)
            alpha = 255
        else:
            # 우측 끝 45px: 일렉트릭 블루 -> 루미너스 화이트 광원 팁 -> 알파 페이드아웃
            fade_ratio = (x - solid_w) / fade_w
            # 중간 피크에서 흰빛이 번쩍임
            if fade_ratio < 0.35:
                sub_r = fade_ratio / 0.35
                r = int(c_mid[0] + (c_glow[0] - c_mid[0]) * sub_r)
                g = int(c_mid[1] + (c_glow[1] - c_mid[1]) * sub_r)
                b = int(c_mid[2] + (c_glow[2] - c_mid[2]) * sub_r)
                alpha = 255
            else:
                sub_r = (fade_ratio - 0.35) / 0.65
                r = c_glow[0]
                g = c_glow[1]
                b = c_glow[2]
                alpha = int(255 * (1.0 - sub_r * sub_r)) # 부드러운 가우스 페이드아웃

        for y in range(H):
            img.putpixel((x, y), (r, g, b, alpha))

    draw = ImageDraw.Draw(img)

    # 텍스트 렌더링
    x1 = pad_x
    x2 = pad_x + (max_w - w2) // 2
    start_y = pad_y - 2

    # 드롭 섀도우
    draw.text((x1 + 1, start_y + 1), "Hookverse", fill=(0, 0, 0, 160), font=font)
    draw.text((x2 + 1, start_y + h1 + line_spacing + 1), "Studio", fill=(0, 0, 0, 160), font=font)
    # 순백색 본문
    draw.text((x1, start_y), "Hookverse", fill=(255, 255, 255, 255), font=font)
    draw.text((x2, start_y + h1 + line_spacing), "Studio", fill=(255, 255, 255, 255), font=font)

    # 상/하/좌 테두리 라운드 림
    draw.line([(0, 0), (solid_w, 0)], fill=(0, 180, 255, 180), width=1)
    draw.line([(0, H-1), (solid_w, H-1)], fill=(0, 180, 255, 180), width=1)
    draw.line([(0, 0), (0, H-1)], fill=(0, 180, 255, 180), width=1)

    img.save(OUT_C, "PNG")
    print(f"[+] ✅ 시안 C 생성 완료: {OUT_C} ({W}x{H})")

if __name__ == "__main__":
    make_option_b()
    make_option_c()
