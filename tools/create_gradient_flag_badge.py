#!/usr/bin/env python3
"""
create_gradient_flag_badge.py — 
오빠의 '딥 네이비 ➡️ 일렉트릭 블루 그라데이션' 및 '1:1 완벽 정원 엠블럼' 에셋 정밀 제작기
"""

import os
from PIL import Image, ImageDraw, ImageFont

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
FONT_PATH = os.path.join(WORKSPACE, "assets", "fonts", "FontdinerSwanky-Regular.ttf")
BADGE_OUT = os.path.join(WORKSPACE, "assets", "images", "hookverse_top_left_badge.png")
LOGO_OUT = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo_transparent.png")
SRC_LOGO = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo.png")

def create_gradient_badge():
    # 폰트 로드
    font_size = 44
    font = ImageFont.truetype(FONT_PATH, font_size)

    text_line1 = "Hookverse"
    text_line2 = "Studio"

    # 더미 드로우로 텍스트 크기 정밀 측정
    dummy = Image.new("RGBA", (100, 100), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dummy)
    bbox1 = d_draw.textbbox((0, 0), text_line1, font=font)
    w1, h1 = bbox1[2] - bbox1[0], bbox1[3] - bbox1[1]

    bbox2 = d_draw.textbbox((0, 0), text_line2, font=font)
    w2, h2 = bbox2[2] - bbox2[0], bbox2[3] - bbox2[1]

    line_spacing = 6
    pad_y = 14
    pad_x = 22

    max_w = max(w1, w2)
    W = int(max_w + pad_x * 2)
    H = int(h1 + line_spacing + h2 + pad_y * 2)

    # 1. 수평 그라데이션 배경 생성 (딥 네이비 #081426 -> 일렉트릭 블루 #005BEA)
    badge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    
    c_start = (8, 20, 38)     # 딥 네이비
    c_end = (0, 91, 234)      # 일렉트릭 로열 블루

    for x in range(W):
        ratio = x / max(1, W - 1)
        r = int(c_start[0] + (c_end[0] - c_start[0]) * ratio)
        g = int(c_start[1] + (c_end[1] - c_start[1]) * ratio)
        b = int(c_start[2] + (c_end[2] - c_start[2]) * ratio)
        for y in range(H):
            badge.putpixel((x, y), (r, g, b, 255))

    draw = ImageDraw.Draw(badge)

    # 미세한 1px 내부 골든/블루 림 하이라이트 (고급감 극대화)
    draw.rectangle([0, 0, W-1, H-1], outline=(0, 160, 255, 180), width=1)

    # 텍스트 중앙 정렬 렌더링
    x1 = (W - w1) // 2
    x2 = (W - w2) // 2
    start_y = pad_y - 2

    # 소프트 텍스트 그림자
    draw.text((x1 + 1, start_y + 1), text_line1, fill=(0, 0, 0, 140), font=font)
    draw.text((x2 + 1, start_y + h1 + line_spacing + 1), text_line2, fill=(0, 0, 0, 140), font=font)

    # 선명한 순백색 본문
    draw.text((x1, start_y), text_line1, fill=(255, 255, 255, 255), font=font)
    draw.text((x2, start_y + h1 + line_spacing), text_line2, fill=(255, 255, 255, 255), font=font)

    badge.save(BADGE_OUT, "PNG")
    print(f"[+] ✅ 좌측 깃발 그라데이션 배지 생성 완료: {W}x{H}px | {BADGE_OUT}")
    return W, H

def verify_perfect_circle_emblem():
    if not os.path.exists(SRC_LOGO):
        print(f"[!] 원본 로고 없음: {SRC_LOGO}")
        return

    img = Image.open(SRC_LOGO).convert("RGBA")
    W, H = img.size
    cx, cy = W // 2, H // 2

    # 정원 마스크 생성 (4x 슈퍼샘플링 안티앨리어싱)
    radius = min(cx, cy) - 10
    scale = 4
    mask_large = Image.new("L", (W * scale, H * scale), 0)
    draw_l = ImageDraw.Draw(mask_large)
    cx_l, cy_l = cx * scale, cy * scale
    r_l = radius * scale
    draw_l.ellipse([cx_l - r_l, cy_l - r_l, cx_l + r_l, cy_l + r_l], fill=255)
    mask = mask_large.resize((W, H), Image.Resampling.LANCZOS)

    # 마스크 결합
    img.putalpha(mask)

    # 정확한 1:1 정사각형 바운딩 박스로 크롭
    square_box = (cx - radius, cy - radius, cx + radius, cy + radius)
    circle_img = img.crop(square_box)
    
    # 512x512 고해상도 마스터 정원으로 리샘플링
    circle_img = circle_img.resize((512, 512), Image.Resampling.LANCZOS)
    circle_img.save(LOGO_OUT, "PNG")
    print(f"[+] ✅ 우측 원형 엠블럼 1:1 정원(Circle) 보정 완료: 512x512px | {LOGO_OUT}")

if __name__ == "__main__":
    print("[*] 3단계: 엠블럼 1:1 정원 및 깃발 웨이브 배지 에셋 제작 중...")
    bw, bh = create_gradient_badge()
    verify_perfect_circle_emblem()
    print("[*] 3단계 에셋 준비 100% 완료.")
