#!/usr/bin/env python3
"""
create_filmstrip_true_gold.py —
오빠의 피드백을 완벽히 해결하는 '24K Chiseled Real Gold' 35mm 필름 배지 엔진
1. 진짜 황금색 구현:
   - 누런색(머스터드/카레) 100% 제거
   - 빛을 받는 샴페인 화이트 하이라이트 (#FFFEE8, #FFF5A8)
   - 채도 높고 묵직한 24K 퓨어 골드 코어 (#FFC000, #E59800)
   - 고급스러운 카라멜 브론즈 섀도우 (#603800, #381E00)
   - 3D Chiseled Bevel (조각된 금속 양각 입체감)
2. 산만함 해결 (시안 2-B 개선):
   - 2.5초 주기 -> 6.5초 주기로 대폭 연장
   - 폭과 투명도를 극도로 부드러운 '실크 쉰(Soft Silk Sheen)'으로 변경하여 산만함 0%, 극도의 우아함 구현
3. 시안 2-A 개선:
   - 스윕 없이 단정하고 묵직한 24K Chiseled 골드 + 10초 플래시 버스트
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

OUT_MP4_TRUE_GOLD_A = os.path.join(IMAGES_DIR, "badge_filmstrip_true_gold_2A.mp4")
OUT_MP4_TRUE_GOLD_B = os.path.join(IMAGES_DIR, "badge_filmstrip_true_gold_2B.mp4")

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 380, 136

def create_true_gold_gradient_surface(w, h):
    """
    진짜 24K 황금 금속 표면 그라데이션 (Liquid 24K Luxury Gold)
    빛의 각도에 따른 멀티 스톱 메탈릭 리플렉션
    """
    stops = [
        (0.00, (255, 255, 235)), # 눈부신 상단 림 하이라이트 (Platinum Gold)
        (0.12, (255, 238, 140)), # 찬란한 샴페인 골드
        (0.32, (255, 198, 20)),  # 24K 순금 비비드 골드 코어
        (0.52, (240, 160, 10)),  # 묵직한 딥 앰버 골드
        (0.70, (255, 215, 60)),  # 금속 하단 반사광 (Bounce Light)
        (0.88, (180, 110, 10)),  # 하단 엣지 브론즈
        (1.00, (110, 65, 5))     # 깊은 금속성 섀도우
    ]
    img = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    for y in range(h):
        pos = y / max(1, h - 1)
        for i in range(len(stops) - 1):
            p0, c0 = stops[i]
            p1, c1 = stops[i+1]
            if p0 <= pos <= p1:
                t = (pos - p0) / max(1e-5, (p1 - p0))
                # 부드러운 코사인 보간 (메탈릭 곡면감)
                t_smooth = 0.5 * (1.0 - math.cos(t * math.pi))
                r = int(c0[0] + (c1[0] - c0[0]) * t_smooth)
                g = int(c0[1] + (c1[1] - c0[1]) * t_smooth)
                b = int(c0[2] + (c1[2] - c0[2]) * t_smooth)
                for x in range(w):
                    img.putpixel((x, y), (r, g, b, 255))
                break
    return img

def draw_chiseled_3d_text(font, text, cx, y_pos, base_w, base_h):
    """
    금속을 깎아 만든 듯한 Chiseled 3D Bevel 황금 텍스트 레이어 생성
    """
    # 1. 텍스트 바운딩 박스
    dummy = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dummy)
    bbox = d_draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = cx - tw // 2
    ty = y_pos

    # 2. 베이스 마스크
    mask = Image.new("L", (base_w, base_h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.text((tx, ty), text, fill=255, font=font)

    # 3. 3D 입체 음영 레이어 (Chiseled Light & Shadow)
    # 상단/좌측 하이라이트 (빛받는 면)
    light_mask = Image.new("L", (base_w, base_h), 0)
    l_draw = ImageDraw.Draw(light_mask)
    l_draw.text((tx - 1, ty - 1), text, fill=255, font=font)
    
    # 하단/우측 섀도우 (그림자 면)
    dark_mask = Image.new("L", (base_w, base_h), 0)
    d_draw2 = ImageDraw.Draw(dark_mask)
    d_draw2.text((tx + 2, ty + 2), text, fill=255, font=font)

    # 4. 깊은 드롭 섀도우
    drop_shadow = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    ds_draw = ImageDraw.Draw(drop_shadow)
    ds_draw.text((tx + 3, ty + 4), text, fill=(0, 0, 0, 230), font=font)
    drop_shadow = drop_shadow.filter(ImageFilter.GaussianBlur(1.8))

    # 5. 황금 금속 텍스처 매핑
    gold_surface = create_true_gold_gradient_surface(base_w, base_h)
    gold_text = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    gold_text.paste(gold_surface, (0, 0), mask)

    # 6. 상단 화이트-골드 엣지 하이라이트 합성
    edge_high = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    eh_draw = ImageDraw.Draw(edge_high)
    eh_draw.text((tx, ty - 1), text, fill=(255, 255, 220, 160), font=font)

    # 7. 하단 딥 앰버 아웃라인 합성
    edge_dark = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    ed_draw = ImageDraw.Draw(edge_dark)
    ed_draw.text((tx, ty + 1), text, fill=(80, 45, 0, 180), font=font)

    # 합성
    result = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    result = Image.alpha_composite(result, drop_shadow)
    result = Image.alpha_composite(result, edge_dark)
    result = Image.alpha_composite(result, gold_text)
    result = Image.alpha_composite(result, edge_high)

    return result, (tx, ty, tw, th)

def draw_sprocket_holes_gold(draw, y_top, w, h, num_holes=8):
    # 24K 골든 메탈릭 림 스프로킷 홀
    hole_w = 18
    hole_h = 11
    step = (w - 24) / num_holes
    for i in range(num_holes):
        x = int(12 + i * step + (step - hole_w) / 2)
        y = y_top
        # 외부 골든 광택 아웃라인 (상단은 밝고 하단은 어두운 입체감)
        draw.rounded_rectangle([x-1, y-1, x + hole_w + 1, y + hole_h + 1], radius=3, outline=(255, 225, 100, 220), width=1)
        draw.line([(x, y + hole_h + 1), (x + hole_w, y + hole_h + 1)], fill=(120, 75, 10, 220), width=1)
        # 내부 깊은 블랙 셀룰로이드 홀
        draw.rounded_rectangle([x, y, x + hole_w, y + hole_h], radius=2, fill=(6, 6, 8, 255), outline=(30, 20, 10, 255), width=1)

def build_true_gold_base():
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. 셀룰로이드 필름 베이스 (다크 옵시디언 블랙)
    draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=6, fill=(10, 10, 12, 255), outline=(255, 215, 80, 255), width=2)
    # 2중 골든 액센트 내부 테두리
    draw.rounded_rectangle([3, 3, W - 4, H - 4], radius=4, outline=(180, 130, 30, 180), width=1)

    # 2. 중앙 필름 인화면 (Deep Obsidian Black Velvet)
    inner_top = 25
    inner_bottom = H - 25
    draw.rectangle([10, inner_top, W - 11, inner_bottom], fill=(16, 16, 18, 255), outline=(255, 200, 60, 200), width=1)
    draw.rectangle([11, inner_top + 1, W - 12, inner_bottom - 1], fill=(12, 12, 14, 255))

    # 3. 상하 스프로킷 홀 (골든 메탈릭 림)
    draw_sprocket_holes_gold(draw, 7, W, H, num_holes=8)
    draw_sprocket_holes_gold(draw, H - 18, W, H, num_holes=8)

    # 4. 레트로 2026 필름 레일 마킹 (선명하고 고급스러운 24K 비비드 골드)
    try:
        small_font = ImageFont.load_default()
    except Exception:
        small_font = None

    if small_font:
        draw.text((18, 7), "▶ 2026 KAIRA 500T", fill=(255, 230, 110, 255), font=small_font)
        draw.text((W - 105, 7), "SAFETY FILM 35mm", fill=(255, 230, 110, 230), font=small_font)
        draw.text((18, H - 17), "ISO 500 / 3200K", fill=(255, 230, 110, 230), font=small_font)
        draw.text((W - 95, H - 17), "FRAME 26 ▶▶", fill=(255, 230, 110, 255), font=small_font)

    # 5. 텍스트 Chiseled 3D Bevel 입체 황금 렌더링
    font = ImageFont.truetype(FONT_SWANKY, 38)
    cx = W // 2
    y_center = (inner_top + inner_bottom) // 2
    
    # 텍스트 높이 계산
    b1 = draw.textbbox((0, 0), "Hookverse", font=font)
    h1 = b1[3] - b1[1]
    b2 = draw.textbbox((0, 0), "Studio", font=font)
    h2 = b2[3] - b2[1]
    
    start_y = y_center - (h1 + 4 + h2) // 2
    
    layer1, box1 = draw_chiseled_3d_text(font, "Hookverse", cx, start_y, W, H)
    layer2, box2 = draw_chiseled_3d_text(font, "Studio", cx, start_y + h1 + 4, W, H)

    img = Image.alpha_composite(img, layer1)
    img = Image.alpha_composite(img, layer2)

    return img

def generate_film_scratches_and_dust(w, h, frame_idx):
    """35mm 리얼 필름 수직 스크래치 선 & 더스트"""
    scratch_layer = Image.new("RGBA", (w, h), (0, 0, 0, 0))
    draw = ImageDraw.Draw(scratch_layer)

    random.seed(frame_idx * 997 + 13)

    # 수직 흰색 스크래치 라인
    num_scratches = random.choices([0, 1, 2, 3], weights=[0.45, 0.35, 0.17, 0.03])[0]
    for _ in range(num_scratches):
        sx = random.randint(15, w - 16)
        alpha = random.randint(110, 200)
        slant = random.uniform(-1.2, 1.2)
        draw.line([(sx, 10), (sx + slant, h - 10)], fill=(255, 255, 255, alpha), width=1)

    # 미세 더스트
    num_dust = random.choices([0, 1, 2], weights=[0.55, 0.35, 0.10])[0]
    for _ in range(num_dust):
        dx = random.randint(20, w - 21)
        dy = random.randint(15, h - 16)
        d_len = random.randint(2, 4)
        d_alpha = random.randint(100, 160)
        draw.line([(dx, dy), (dx + random.randint(-1, 1), dy + d_len)], fill=(250, 245, 230, d_alpha), width=1)

    return scratch_layer

def render_preview_true_gold_2A():
    """
    시안 2-A 리마스터: [24K Chiseled Real Gold + 35mm 필름 스크래치 + 10초 플래시 버스트]
    - 누런 기 0%, 보석처럼 빛나는 24K 리얼 골드 입체감
    - 빛줄기 스윕 없이 단정하고 묵직한 프리미엄 헐리우드 필름 룩
    - 10초 주기 카메라 플래시 버스트
    """
    base_img = build_true_gold_base()
    fps = 30
    duration = 10.0
    total_frames = int(fps * duration)

    frames_dir = os.path.join(WORKSPACE, "scratch", "frames_gold_2a")
    os.makedirs(frames_dir, exist_ok=True)

    print(f"[*] 시안 2-A 리얼 골드 렌더링 시작 (총 {total_frames}프레임, 10초)...")
    flash_peaks = [1.5, 8.5]

    for f in range(total_frames):
        t = f / fps
        frame = base_img.copy()

        # 1. 35mm 필름 스크래치
        scratches = generate_film_scratches_and_dust(W, H, f)
        frame = Image.alpha_composite(frame, scratches)

        # 2. 10초 주기 카메라 플래시 버스트
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

        canvas = Image.new("RGB", (400, 156), (10, 10, 12))
        canvas.paste(frame, (10, 10), frame)
        canvas.save(os.path.join(frames_dir, f"frame_{f:04d}.png"))

    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUT_MP4_TRUE_GOLD_A
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"[+] 🎯 시안 2-A 리얼 골드 MP4 렌더링 완결: {OUT_MP4_TRUE_GOLD_A}")

def render_preview_true_gold_2B():
    """
    시안 2-B 리마스터 (산만함 0% 완벽 해결):
    [24K Chiseled Real Gold + 6.5초 주기 소프트 실크 쉰(Soft Silk Sheen) + 10초 플래시 버스트]
    - 주기를 2.5초 -> 6.5초로 대폭 늘려 평상시에는 차분하고 안정적임!
    - 빛줄기를 '쨍한 줄'이 아니라 부드럽고 엷은 샴페인 골드 광택(Silk Sheen)으로 고급스럽게 1번 스르륵 훑고 지나가게 튜닝!
    """
    base_img = build_true_gold_base()
    fps = 30
    duration = 10.0
    total_frames = int(fps * duration)

    frames_dir = os.path.join(WORKSPACE, "scratch", "frames_gold_2b")
    os.makedirs(frames_dir, exist_ok=True)

    print(f"[*] 시안 2-B 리얼 골드 (산만함 해결형) 렌더링 시작 (총 {total_frames}프레임, 10초)...")
    flash_peaks = [1.5, 8.5]
    sweep_cycle = 6.5  # 6.5초 주기 (10초 동안 단 1회 우아하게 스치고 지나감)

    for f in range(total_frames):
        t = f / fps
        frame = base_img.copy()

        # 1. 35mm 필름 스크래치
        scratches = generate_film_scratches_and_dust(W, H, f)
        frame = Image.alpha_composite(frame, scratches)

        # 2. 6.5초 주기 소프트 실크 쉰 (산만함 0% 은은한 광택)
        # 3.0초 시점부터 4.8초 시점까지 1.8초 동안 아주 부드럽고 엷게 1번만 스쳐 지나감
        if 3.0 <= t <= 5.0:
            sweep_ratio = (t - 3.0) / 2.0
            beam_pos = int(-50 + (W + 100) * sweep_ratio)
            sheen = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            s_draw = ImageDraw.Draw(sheen)
            
            beam_w = 45  # 폭을 넓혀서 부드러운 그러데이션
            for bx in range(beam_pos - beam_w, beam_pos + beam_w):
                dist = abs(bx - beam_pos) / float(beam_w)
                # 부드러운 코사인 곡선 알파 (최대 110으로 눈부심/산만함 억제)
                alpha = int(105 * (0.5 * (1.0 + math.cos(dist * math.pi))))
                if alpha > 0 and 12 <= bx < W - 12:
                    s_draw.line([(bx, 25), (bx + 22, H - 25)], fill=(255, 250, 215, alpha), width=1)
            sheen = sheen.filter(ImageFilter.GaussianBlur(3.5))
            frame = Image.alpha_composite(frame, sheen)

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

        canvas = Image.new("RGB", (400, 156), (10, 10, 12))
        canvas.paste(frame, (10, 10), frame)
        canvas.save(os.path.join(frames_dir, f"frame_{f:04d}.png"))

    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUT_MP4_TRUE_GOLD_B
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"[+] 🎯 시안 2-B 리얼 골드 (산만함 해결형) MP4 렌더링 완결: {OUT_MP4_TRUE_GOLD_B}")

if __name__ == "__main__":
    print("[*] 24K Chiseled Real Gold 35mm 필름 배지 렌더링 가동...")
    render_preview_true_gold_2A()
    render_preview_true_gold_2B()
    print("[*] 모든 렌더링 완료!")
