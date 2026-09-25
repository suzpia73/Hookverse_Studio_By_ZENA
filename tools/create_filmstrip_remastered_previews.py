#!/usr/bin/env python3
"""
create_filmstrip_remastered_previews.py —
오빠의 피드백을 100% 반영한 '시안 2 빈티지 35mm 필름스트립' 최고급 리마스터 모션 생성기
1. 연도: 1997 -> 2026 (유튜브 시작 시점)
2. 흔들림(지진) 제거: 프레임 완전 고정
3. 필름 흰줄 노이즈(Vertical Scratches) 및 더스트/그레인 리얼 구현
4. 색감: 탁한 색 완전히 제거 -> 영롱한 24K 리얼 샴페인 골드 (광택 & 입체 베벨)
5. 글자 모션 & 10초 간격 카메라 플래시 버스트 (Flash Burst)
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import imageio_ffmpeg
import subprocess

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
FONT_SWANKY = os.path.join(WORKSPACE, "assets", "fonts", "FontdinerSwanky-Regular.ttf")
IMAGES_DIR = os.path.join(WORKSPACE, "assets", "images")

OUT_MP4_2A = os.path.join(IMAGES_DIR, "badge_filmstrip_v2_flash_burst.mp4")
OUT_MP4_2B = os.path.join(IMAGES_DIR, "badge_filmstrip_v2_shimmer_and_flash.mp4")

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 380, 136  # 가로 380, 세로 136

def create_metallic_gold_gradient(height):
    # 영롱하고 반짝이는 24K 리얼 샴페인 골드 그라데이션 컬러맵
    # 상단 하이라이트(#FFF8D6) -> 눈부신 골드(#FFD700) -> 앰버 골드(#DDA020) -> 딥 골드(#A07010)
    stops = [
        (0.00, (255, 252, 230)), # 최상단 눈부신 샴페인 화이트골드
        (0.25, (255, 230, 120)), # 밝은 리치 골드
        (0.55, (235, 185, 45)),  # 24K 순금 베이스
        (0.80, (200, 140, 20)),  # 깊은 앰버 골드
        (1.00, (160, 105, 10))   # 묵직한 하단 그림자 골드
    ]
    colormap = []
    for y in range(height):
        pos = y / max(1, height - 1)
        # 보간
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i+1]
            if p0 <= pos <= p1:
                t = (pos - p0) / max(1e-5, (p1 - p0))
                r = int(c0[0] + (c1[0] - c0[0]) * t)
                g = int(c0[1] + (c1[1] - c0[1]) * t)
                b = int(c0[2] + (c1[2] - c0[2]) * t)
                colormap.append((r, g, b))
                break
        else:
            colormap.append(stops[-1][1])
    return colormap

def draw_sprocket_holes(draw, y_top, w, h, num_holes=8):
    # 정교한 35mm 필름 퍼포레이션 홀 (골든 메탈릭 림 + 깊은 흑연 구멍)
    hole_w = 18
    hole_h = 11
    step = (w - 24) / num_holes
    for i in range(num_holes):
        x = int(12 + i * step + (step - hole_w) / 2)
        y = y_top
        # 외부 골든 음영 아웃라인
        draw.rounded_rectangle([x-1, y-1, x + hole_w + 1, y + hole_h + 1], radius=3, outline=(240, 200, 80, 180), width=1)
        # 내부 깊은 블랙 홀
        draw.rounded_rectangle([x, y, x + hole_w, y + hole_h], radius=2, fill=(8, 8, 10, 255), outline=(40, 30, 15, 255), width=1)

def build_remastered_base():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. 셀룰로이드 필름 베이스 (다크 흑연 블랙 + 미세 앰버 틴트)
    draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=6, fill=(14, 14, 16, 255), outline=(218, 175, 55, 230), width=2)
    # 2중 골든 액센트 내부 테두리
    draw.rounded_rectangle([3, 3, W - 4, H - 4], radius=4, outline=(140, 105, 25, 140), width=1)

    # 2. 중앙 필름 인화면 (Deep Cinematic Charcoal Velvet)
    inner_top = 25
    inner_bottom = H - 25
    draw.rectangle([10, inner_top, W - 11, inner_bottom], fill=(20, 20, 24, 255), outline=(200, 160, 50, 160), width=1)
    draw.rectangle([11, inner_top + 1, W - 12, inner_bottom - 1], fill=(16, 16, 20, 255))

    # 3. 상하 스프로킷 홀 (골든 메탈릭 림)
    draw_sprocket_holes(draw, 7, W, H, num_holes=8)
    draw_sprocket_holes(draw, H - 18, W, H, num_holes=8)

    # 4. 레트로 2026 필름 레일 마킹 (선명하고 고급스러운 골드 앰버)
    try:
        small_font = ImageFont.load_default()
    except Exception:
        small_font = None

    if small_font:
        # 상단 레일: 올해 2026 KAIRA 마킹!
        draw.text((18, 7), "▶ 2026 KAIRA 500T", fill=(255, 215, 80, 240), font=small_font)
        draw.text((W - 105, 7), "SAFETY FILM 35mm", fill=(255, 215, 80, 220), font=small_font)
        # 하단 레일: 시네마 프레임 마킹
        draw.text((18, H - 17), "ISO 500 / 3200K", fill=(255, 215, 80, 220), font=small_font)
        draw.text((W - 95, H - 17), "FRAME 26 ▶▶", fill=(255, 215, 80, 240), font=small_font)

    # 5. 텍스트 레이어 생성 (24K 리얼 골드 그라데이션 렌더링)
    font = ImageFont.truetype(FONT_SWANKY, 38)
    b1 = draw.textbbox((0, 0), "Hookverse", font=font)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    b2 = draw.textbbox((0, 0), "Studio", font=font)
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]

    cx = W // 2
    y_center = (inner_top + inner_bottom) // 2
    start_y = y_center - (h1 + 4 + h2) // 2
    x1 = cx - w1 // 2
    x2 = cx - w2 // 2

    # 텍스트 전용 마스크 레이어
    text_mask = Image.new("L", (W, H), 0)
    mask_draw = ImageDraw.Draw(text_mask)
    mask_draw.text((x1, start_y), "Hookverse", fill=255, font=font)
    mask_draw.text((x2, start_y + h1 + 4), "Studio", fill=255, font=font)

    # 텍스트 깊은 드롭 섀도우 (글자가 필름에서 튀어나오는 듯한 입체감)
    shadow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow_layer)
    s_draw.text((x1 + 2, start_y + 2), "Hookverse", fill=(0, 0, 0, 220), font=font)
    s_draw.text((x2 + 2, start_y + h1 + 4 + 2), "Studio", fill=(0, 0, 0, 220), font=font)
    shadow_layer = shadow_layer.filter(ImageFilter.GaussianBlur(1.0))
    img = Image.alpha_composite(img, shadow_layer)

    # 텍스트 베벨 아웃라인 (상단 하이라이트 골드, 하단 딥 브론즈)
    outline_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    o_draw = ImageDraw.Draw(outline_layer)
    for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (1, 1)]:
        o_draw.text((x1 + dx, start_y + dy), "Hookverse", fill=(160, 110, 20, 200), font=font)
        o_draw.text((x2 + dx, start_y + h1 + 4 + dy), "Studio", fill=(160, 110, 20, 200), font=font)
    img = Image.alpha_composite(img, outline_layer)

    # 영롱한 24K 골드 그라데이션을 텍스트 마스크에 채우기
    gold_colormap = create_metallic_gold_gradient(H)
    gold_fill = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    for y in range(H):
        r, g, b = gold_colormap[y]
        for x in range(W):
            gold_fill.putpixel((x, y), (r, g, b, 255))

    # 마스크 합성
    gold_text = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    gold_text.paste(gold_fill, (0, 0), text_mask)

    # 골드 텍스트를 베이스 위에 합성
    img = Image.alpha_composite(img, gold_text)

    return img, (x1, start_y, w1, h1, x2, h1 + 4, w2, h2)

def generate_film_scratches_and_dust(w, h, frame_idx):
    """
    옛날 35mm 필름의 리얼 화이트 세로 스크래치 선 & 먼지 파티클 생성
    흔들림(지진)은 0%이며, 필름 표면에 얇은 흰 줄들이 불규칙하게 깜빡이고 스쳐 지나감
    """
    scratch_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scratch_layer)

    # 시드 고정 및 프레임 변화
    random.seed(frame_idx * 997 + 13)

    # 1. 수직 흰색 스크래치 라인 (간헐적으로 1~3개 발생)
    num_scratches = random.choices([0, 1, 2, 3], weights=[0.4, 0.35, 0.2, 0.05])[0]
    for _ in range(num_scratches):
        sx = random.randint(15, w - 16)
        alpha = random.randint(110, 210)
        # 살짝 기울어진 수직선
        slant = random.uniform(-1.5, 1.5)
        # 점선이거나 약간 끊어진 얇은 선
        draw.line([(sx, 10), (sx + slant, h - 10)], fill=(255, 255, 255, alpha), width=1)

    # 2. 미세한 필름 더스트/헤어(Dust & Hair) 입자
    num_dust = random.choices([0, 1, 2], weights=[0.5, 0.35, 0.15])[0]
    for _ in range(num_dust):
        dx = random.randint(20, w - 21)
        dy = random.randint(15, h - 16)
        d_len = random.randint(2, 5)
        d_alpha = random.randint(100, 180)
        draw.line([(dx, dy), (dx + random.randint(-2, 2), dy + d_len)], fill=(250, 245, 230, d_alpha), width=1)

    return scratch_layer

def render_preview_option_2A():
    """
    시안 2-A: [24K 리얼 골드 + 35mm 필름 스크래치 + 10초 주기 카메라 플래시 버스트]
    - 프레임 고정 (지진 0%)
    - 흰색 수직 스크래치 & 필름 더스트
    - 10초 주기 카메라 플래시 번쩍임 (0~10초 동안, 2초 시점과 8초 시점에 플래시 버스트 폭발)
    """
    base_img, text_box = build_remastered_base()
    fps = 30
    duration = 10.0  # 10초 풀 모션
    total_frames = int(fps * duration)

    frames_dir = os.path.join(WORKSPACE, "scratch", "frames_opt2a")
    os.makedirs(frames_dir, exist_ok=True)

    print(f"[*] 시안 2-A 렌더링 시작 (총 {total_frames}프레임, 10초)...")

    # 플래시 폭발 시점 (초 단위): 1.5초 시점, 8.5초 시점
    flash_peaks = [1.5, 8.5]

    for f in range(total_frames):
        t = f / fps
        frame = base_img.copy()

        # 1. 35mm 필름 화이트 스크래치 & 더스트 오버레이
        scratches = generate_film_scratches_and_dust(W, H, f)
        frame = Image.alpha_composite(frame, scratches)

        # 2. 10초 주기 카메라 플래시 버스트 (Flash Burst)
        # 플래시가 터질 때: 0.05초 만에 최대 광량 도달 후 0.4초 동안 감쇄
        flash_power = 0.0
        for peak in flash_peaks:
            dt = t - peak
            if 0.0 <= dt < 0.45:
                # 급격한 폭발 후 지수 감쇄
                flash_power = max(flash_power, math.exp(-dt * 9.0))

        if flash_power > 0.01:
            # 플래시 레이어: 중앙에서 터지는 눈부신 렌즈 플레어 & 전체 글자 블룸
            flash_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            f_draw = ImageDraw.Draw(flash_layer)
            
            alpha_burst = int(245 * flash_power)
            # 글자 전체를 감싸는 눈부신 샴페인 화이트 플래시
            f_draw.rectangle([8, 25, W - 9, H - 25], fill=(255, 252, 235, int(alpha_burst * 0.65)))
            
            # 중앙 플래시 코어 (Lens Flare Glow)
            cx, cy = W // 2, H // 2
            max_r = int(140 * flash_power)
            if max_r > 5:
                flare = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                flare_draw = ImageDraw.Draw(flare)
                flare_draw.ellipse([cx - max_r, cy - max_r // 2, cx + max_r, cy + max_r // 2], fill=(255, 255, 250, alpha_burst))
                flare = flare.filter(ImageFilter.GaussianBlur(12.0))
                frame = Image.alpha_composite(frame, flare)

            flash_layer = flash_layer.filter(ImageFilter.GaussianBlur(4.0))
            frame = Image.alpha_composite(frame, flash_layer)

        # 숏폼 캔버스 (400x156) 위에 안착 (완전 고정)
        canvas = Image.new("RGB", (400, 156), (12, 12, 14))
        canvas.paste(frame, (10, 10), frame)
        canvas.save(os.path.join(frames_dir, f"frame_{f:04d}.png"))

    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUT_MP4_2A
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"[+] 🎯 시안 2-A MP4 렌더링 완결: {OUT_MP4_2A}")

def render_preview_option_2B():
    """
    시안 2-B: [리얼 골드 35mm 필름 + 빛줄기 앰비언트 스윕(Shimmer Sweep) + 플래시 버스트]
    - 시안 2-A의 모든 요소(골드, 스크래치, 플래시)에 더해,
    - 플래시 사이의 평상시에도 글자 위를 2.5초마다 샤라락 지나가는 영롱한 빛줄기(Shimmer Sweep) 결합!
    """
    base_img, text_box = build_remastered_base()
    x1, start_y, w1, h1, x2, h2_offset, w2, h2 = text_box
    fps = 30
    duration = 10.0
    total_frames = int(fps * duration)

    frames_dir = os.path.join(WORKSPACE, "scratch", "frames_opt2b")
    os.makedirs(frames_dir, exist_ok=True)

    print(f"[*] 시안 2-B 렌더링 시작 (총 {total_frames}프레임, 10초)...")

    flash_peaks = [1.5, 8.5]
    sweep_cycle = 2.5  # 2.5초마다 빛줄기 스윕

    for f in range(total_frames):
        t = f / fps
        frame = base_img.copy()

        # 1. 35mm 필름 화이트 스크래치 & 더스트
        scratches = generate_film_scratches_and_dust(W, H, f)
        frame = Image.alpha_composite(frame, scratches)

        # 2. 글자 표면을 타고 흐르는 앰비언트 골든 빔 스윕 (Shimmer Sweep)
        sweep_t = (t % sweep_cycle) / sweep_cycle
        if sweep_t < 0.6:  # 0~60% 동안 스윕 지나감
            beam_pos = int(-40 + (W + 80) * (sweep_t / 0.6))
            shimmer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(shimmer)
            for bx in range(beam_pos - 25, beam_pos + 25):
                dist = abs(bx - beam_pos) / 25.0
                alpha = int(160 * (1.0 - dist * dist))
                if alpha > 0 and 12 <= bx < W - 12:
                    s_draw.line([(bx, 25), (bx + 18, H - 25)], fill=(255, 255, 230, alpha), width=1)
            shimmer = shimmer.filter(ImageFilter.GaussianBlur(2.0))
            frame = Image.alpha_composite(frame, shimmer)

        # 3. 10초 주기 카메라 플래시 버스트
        flash_power = 0.0
        for peak in flash_peaks:
            dt = t - peak
            if 0.0 <= dt < 0.45:
                flash_power = max(flash_power, math.exp(-dt * 9.0))

        if flash_power > 0.01:
            flash_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            f_draw = ImageDraw.Draw(flash_layer)
            alpha_burst = int(245 * flash_power)
            f_draw.rectangle([8, 25, W - 9, H - 25], fill=(255, 252, 235, int(alpha_burst * 0.65)))
            
            cx, cy = W // 2, H // 2
            max_r = int(140 * flash_power)
            if max_r > 5:
                flare = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                flare_draw = ImageDraw.Draw(flare)
                flare_draw.ellipse([cx - max_r, cy - max_r // 2, cx + max_r, cy + max_r // 2], fill=(255, 255, 250, alpha_burst))
                flare = flare.filter(ImageFilter.GaussianBlur(12.0))
                frame = Image.alpha_composite(frame, flare)

            flash_layer = flash_layer.filter(ImageFilter.GaussianBlur(4.0))
            frame = Image.alpha_composite(frame, flash_layer)

        # 숏폼 캔버스에 안착
        canvas = Image.new("RGB", (400, 156), (12, 12, 14))
        canvas.paste(frame, (10, 10), frame)
        canvas.save(os.path.join(frames_dir, f"frame_{f:04d}.png"))

    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUT_MP4_2B
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"[+] 🎯 시안 2-B MP4 렌더링 완결: {OUT_MP4_2B}")

if __name__ == "__main__":
    print("[*] 오빠의 피드백 반영 35mm 필름 배지 10초 리마스터 프리뷰 렌더링 시작...")
    render_preview_option_2A()
    render_preview_option_2B()
    print("[*] 모든 렌더링 완료!")
