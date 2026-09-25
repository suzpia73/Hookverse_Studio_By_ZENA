#!/usr/bin/env python3
"""
create_filmstrip_transparent_convex_gold.py —
오빠의 4대 핵심 요구사항 100% 반영:
1. 글자의 볼록한 양각 입체감 (Pillow Bevel Convex 3D Emboss)
2. 진짜 24K 명품 황금색 (노란색/탁함 0%, 샴페인 백금 하이라이트 + 딥 웜 골드 + 리치 앰버)
3. 좌우 세로선 4개 완전 제거 -> 상하 트윈 레일(상단 2줄, 하단 2줄)만 남김 (무한 필름 릴 구조)
4. 검은 배경 100% 완전 투명화 (알파 채널 투명, 글자 뒤에 소프트 앰비언트 섀도우로 가독성 완벽 사수)
   + 비교를 위한 2가지 버전 (완전 투명 100% vs 20% 글래스모피즘 반투명)
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops
import imageio_ffmpeg
import subprocess

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
FONT_SWANKY = os.path.join(WORKSPACE, "assets", "fonts", "FontdinerSwanky-Regular.ttf")
IMAGES_DIR = os.path.join(WORKSPACE, "assets", "images")

OUT_MP4_TRANSPARENT = os.path.join(IMAGES_DIR, "badge_filmstrip_convex_transparent.mp4")
OUT_MP4_GLASSTINT = os.path.join(IMAGES_DIR, "badge_filmstrip_convex_glasstint.mp4")

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 380, 136

def create_true_gold_palette():
    # 24K 명품 순금 팔레트 (따뜻하고 묵직한 리치 골드)
    # Highlight: (255, 255, 240)
    # Pure Gold: (255, 204, 0)
    # Deep Amber: (200, 130, 10)
    # Shadow Bronze: (90, 50, 5)
    return {
        "hi": (255, 255, 240),
        "mid_hi": (255, 228, 120),
        "gold": (255, 195, 20),
        "deep_gold": (220, 150, 15),
        "shadow": (140, 85, 10),
        "dark_shadow": (70, 40, 5)
    }

def draw_convex_3d_text(font, text, cx, y_pos, base_w, base_h):
    """
    글자가 둥글고 볼록하게 튀어나온 리얼 3D 양각(Convex Pillow Emboss) 황금 텍스트 생성
    """
    dummy = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dummy)
    bbox = d_draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = cx - tw // 2
    ty = y_pos

    # 1. 텍스트 마스크
    mask = Image.new("L", (base_w, base_h), 0)
    m_draw = ImageDraw.Draw(mask)
    m_draw.text((tx, ty), text, fill=255, font=font)

    # 2. 볼록한 양각(Convex Emboss) 맵 생성
    # 거리를 안쪽으로 주어 중심부가 솟아오른 돔(Dome) 형태의 높이 맵 모사
    # 블러와 대비를 조합하여 매끄러운 볼록 곡면 생성
    blur_inner = mask.filter(ImageFilter.GaussianBlur(3.5))
    
    # 3. 45도 좌상단 광원에 의한 3D 양각 음영 (Emboss)
    # 밝은 면 (좌상단으로 2px 이동)
    light_map = Image.new("L", (base_w, base_h), 0)
    ImageDraw.Draw(light_map).text((tx - 2, ty - 2), text, fill=255, font=font)
    light_map = ImageChops.subtract(light_map, mask) # 외곽 밝은 림
    
    # 내부 볼록 하이라이트 (중심부 상단)
    inner_light = Image.new("L", (base_w, base_h), 0)
    ImageDraw.Draw(inner_light).text((tx - 1, ty - 1), text, fill=255, font=font)
    inner_light = ImageChops.multiply(inner_light, blur_inner)

    # 어두운 면 (우하단으로 2px 이동)
    dark_map = Image.new("L", (base_w, base_h), 0)
    ImageDraw.Draw(dark_map).text((tx + 2, ty + 2), text, fill=255, font=font)
    dark_map = ImageChops.subtract(dark_map, mask)

    # 4. 볼록한 24K 황금 베이스 레이어 (중심부가 밝고 가장자리가 둥글게 감싸는 곡면)
    gold_layer = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    g_draw = ImageDraw.Draw(gold_layer)
    
    # 텍스트 내부에 부드러운 볼록 그라데이션 채우기
    for y in range(ty, ty + th + 10):
        if y >= base_h: break
        ratio = (y - ty) / float(max(1, th))
        # 볼록한 원통형 굴곡: 상단 25% 지점이 가장 볼록하고 빛남
        curve = math.sin(max(0, min(1, ratio)) * math.pi)
        r = int(255 * (0.85 + 0.15 * curve))
        g = int(185 + 45 * curve - 40 * ratio)
        b = int(15 + 20 * curve)
        for x in range(base_w):
            if mask.getpixel((x, y)) > 0:
                gold_layer.putpixel((x, y), (r, g, b, 255))

    # 5. 양각 볼록 하이라이트 합성 (글자 윗면을 따라 백금처럼 번쩍이는 3D 빛)
    high_layer = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    for y in range(base_h):
        for x in range(base_w):
            val = inner_light.getpixel((x, y))
            if val > 30 and mask.getpixel((x, y)) > 0:
                alpha = min(255, int(val * 1.8))
                high_layer.putpixel((x, y), (255, 255, 235, alpha))
    high_layer = high_layer.filter(ImageFilter.GaussianBlur(1.0))

    # 6. 볼록한 가장자리 날카로운 골드 림 (좌상단 백금림, 우하단 딥브론즈림)
    rim_layer = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    r_draw = ImageDraw.Draw(rim_layer)
    # 좌상단 밝은 림
    r_draw.text((tx - 1, ty - 1), text, fill=(255, 255, 220, 200), font=font)
    # 우하단 어두운 림
    r_draw.text((tx + 1, ty + 1), text, fill=(80, 40, 5, 220), font=font)
    # 텍스트 마스크로 클리핑
    rim_layer.putalpha(mask)

    # 7. 묵직한 앰비언트 드롭 섀도우 (투명 배경에서도 100% 가독성을 보장하는 다크 글로우)
    shadow = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    # 다층 그림자로 글자가 배경 위로 3~4mm 붕 떠오른 입체감
    s_draw.text((tx + 2, ty + 3), text, fill=(0, 0, 0, 240), font=font)
    s_draw.text((tx + 3, ty + 5), text, fill=(0, 0, 0, 180), font=font)
    shadow = shadow.filter(ImageFilter.GaussianBlur(2.5))

    # 최종 글자 합성
    out = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    out = Image.alpha_composite(out, shadow)
    out = Image.alpha_composite(out, gold_layer)
    out = Image.alpha_composite(out, rim_layer)
    out = Image.alpha_composite(out, high_layer)

    return out

def draw_sprocket_holes_rails(draw, w, h, transparent=True):
    """
    오빠의 요청 100% 반영:
    - 세로선 4개 완전 제거!
    - 가로줄만 상단 2줄, 하단 2줄 (총 4개 수평 트윈 레일)
    - 24K 리얼 골드 메탈 라인
    """
    # 1. 상단 트윈 레일 (y=2, y=22)
    # 레일 1: 최상단 골든 림 (상단은 밝고 하단은 앰버)
    draw.line([(0, 2), (w, 2)], fill=(255, 235, 120, 255), width=2)
    draw.line([(0, 4), (w, 4)], fill=(140, 85, 10, 200), width=1)
    
    # 레일 2: 스프로킷 홀 하단 경계선
    draw.line([(0, 22), (w, 22)], fill=(255, 215, 60, 230), width=1)
    draw.line([(0, 23), (w, 23)], fill=(80, 45, 5, 200), width=1)

    # 2. 하단 트윈 레일 (y=H-23, y=H-3)
    # 레일 3: 스프로킷 홀 상단 경계선
    draw.line([(0, H - 23), (w, H - 23)], fill=(255, 215, 60, 230), width=1)
    draw.line([(0, H - 22), (w, H - 22)], fill=(80, 45, 5, 200), width=1)

    # 레일 4: 최하단 골든 림
    draw.line([(0, H - 4), (w, H - 4)], fill=(255, 235, 120, 255), width=2)
    draw.line([(0, H - 2), (w, H - 2)], fill=(140, 85, 10, 200), width=1)

    # 3. 스프로킷 퍼포레이션 홀 (퍼포레이션 사각 구멍)
    # 세로선이 없으므로 필름 구멍들이 상하 레일 사이에 자유롭게 펀칭된 형태
    num_holes = 8
    hole_w = 18
    hole_h = 11
    step = w / float(num_holes)
    
    for i in range(num_holes):
        x = int(i * step + (step - hole_w) / 2)
        # 상단 구멍 (y=7)
        y1 = 7
        draw.rounded_rectangle([x-1, y1-1, x + hole_w + 1, y1 + hole_h + 1], radius=3, outline=(255, 235, 120, 240), width=1)
        # 투명 배경일 때는 구멍 내부를 완전 투명하게 유지하거나 펀칭 음영만 줌
        if not transparent:
            draw.rounded_rectangle([x, y1, x + hole_w, y1 + hole_h], radius=2, fill=(6, 6, 8, 255))
        else:
            # 투명 홀 안쪽 미세한 림 섀도우
            draw.rounded_rectangle([x, y1, x + hole_w, y1 + hole_h], radius=2, outline=(60, 35, 5, 220), width=1)

        # 하단 구멍 (y=H-18)
        y2 = H - 18
        draw.rounded_rectangle([x-1, y2-1, x + hole_w + 1, y2 + hole_h + 1], radius=3, outline=(255, 235, 120, 240), width=1)
        if not transparent:
            draw.rounded_rectangle([x, y2, x + hole_w, y2 + hole_h], radius=2, fill=(6, 6, 8, 255))
        else:
            draw.rounded_rectangle([x, y2, x + hole_w, y2 + hole_h], radius=2, outline=(60, 35, 5, 220), width=1)

def build_base_badge(transparent_mode=True):
    """
    배이스 배지 렌더링
    - transparent_mode=True : 100% 완전 투명 배경 (영상 배경이 그대로 투과)
    - transparent_mode=False : 20% 반투명 글래스모피즘 틴트
    """
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    if not transparent_mode:
        # 은은한 20% 글래스모피즘 반투명 다크 틴트
        glass = Image.new("RGBA", (W, H), (12, 10, 8, 60))
        img = Image.alpha_composite(img, glass)
        draw = ImageDraw.Draw(img)

    # 1. 상하 트윈 레일 & 스프로킷 홀 (세로선 0%)
    draw_sprocket_holes_rails(draw, W, H, transparent=transparent_mode)

    # 2. 2026 레트로 필름 마킹 (24K 리얼 골드)
    try:
        small_font = ImageFont.load_default()
    except Exception:
        small_font = None

    if small_font:
        # 상단 레일 텍스트
        draw.text((15, 6), "▶ 2026 KAIRA 500T", fill=(255, 235, 120, 255), font=small_font)
        draw.text((W - 105, 6), "SAFETY FILM 35mm", fill=(255, 235, 120, 230), font=small_font)
        # 하단 레일 텍스트
        draw.text((15, H - 17), "ISO 500 / 3200K", fill=(255, 235, 120, 230), font=small_font)
        draw.text((W - 95, H - 17), "FRAME 26 ▶▶", fill=(255, 235, 120, 255), font=small_font)

    # 3. 글자 Convex 3D 양각 렌더링
    font = ImageFont.truetype(FONT_SWANKY, 38)
    cx = W // 2
    y_center = H // 2
    
    b1 = draw.textbbox((0, 0), "Hookverse", font=font)
    h1 = b1[3] - b1[1]
    b2 = draw.textbbox((0, 0), "Studio", font=font)
    h2 = b2[3] - b2[1]
    
    start_y = y_center - (h1 + 4 + h2) // 2

    layer1 = draw_convex_3d_text(font, "Hookverse", cx, start_y, W, H)
    layer2 = draw_convex_3d_text(font, "Studio", cx, start_y + h1 + 4, W, H)

    img = Image.alpha_composite(img, layer1)
    img = Image.alpha_composite(img, layer2)

    return img

def render_motion_preview(transparent_mode, out_mp4, desc):
    """
    실제 숏폼 영상 배경(IMF 2화 비오는 거리 씬) 위에 배지를 합성하여
    오빠가 "배경이 비칠 때 얼마나 리얼하고 예쁜지" 눈으로 직접 확인하실 수 있게 렌더링!
    """
    base_badge = build_base_badge(transparent_mode=transparent_mode)
    
    # 숏폼 실제 배경 로드 (Cut 01 또는 비오는 씬)
    # 만약 배경 이미지가 있으면 쓰고, 없으면 시네마틱 레인 배경을 생성하여 합성
    bg_path = os.path.join(WORKSPACE, "assets", "images", "IMF2화_스틸_cut01_raw.png")
    if not os.path.exists(bg_path):
        bg_path = os.path.join(WORKSPACE, "assets", "images", "IMF2화_cut01_마스터스틸.png")

    if os.path.exists(bg_path):
        bg_src = Image.open(bg_path).convert("RGBA")
        # 배지 영역(좌상단 20, 40) 크기 크롭 (440 x 180)
        bg_crop = bg_src.crop((20, 40, 20 + 420, 40 + 176)).resize((420, 176))
    else:
        # 다크 네이비 시네마틱 빗길 배경 생성
        bg_crop = Image.new("RGBA", (420, 176), (15, 18, 28, 255))

    fps = 30
    duration = 10.0
    total_frames = int(fps * duration)

    frames_dir = os.path.join(WORKSPACE, "scratch", f"frames_convex_{'trans' if transparent_mode else 'glass'}")
    os.makedirs(frames_dir, exist_ok=True)

    print(f"[*] {desc} 렌더링 시작 (총 {total_frames}프레임)...")
    flash_peaks = [1.5, 8.5]

    for f in range(total_frames):
        t = f / fps
        frame = base_badge.copy()

        # 1. 35mm 필름 화이트 스크래치 (필름 레일 영역에만 은은하게)
        scratch = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(scratch)
        random.seed(f * 883 + 19)
        if random.random() < 0.4:
            sx = random.randint(15, W - 16)
            s_draw.line([(sx, 4), (sx + random.uniform(-1, 1), H - 4)], fill=(255, 255, 255, random.randint(90, 170)), width=1)
        frame = Image.alpha_composite(frame, scratch)

        # 2. 6.5초 주기 소프트 실크 쉰 (3.0 ~ 5.0초 구간 1회만 부드럽게 스침)
        if 3.0 <= t <= 5.0:
            sweep_ratio = (t - 3.0) / 2.0
            beam_pos = int(-40 + (W + 80) * sweep_ratio)
            sheen = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            sh_draw = ImageDraw.Draw(sheen)
            
            beam_w = 40
            for bx in range(beam_pos - beam_w, beam_pos + beam_w):
                dist = abs(bx - beam_pos) / float(beam_w)
                alpha = int(95 * (0.5 * (1.0 + math.cos(dist * math.pi))))
                if alpha > 0 and 5 <= bx < W - 5:
                    sh_draw.line([(bx, 22), (bx + 20, H - 22)], fill=(255, 255, 230, alpha), width=1)
            sheen = sheen.filter(ImageFilter.GaussianBlur(3.0))
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
            alpha_burst = int(240 * flash_power)
            
            cx, cy = W // 2, H // 2
            max_r = int(130 * flash_power)
            if max_r > 5:
                flare = Image.new("RGBA", (W, H), (0, 0, 0, 0))
                flare_draw = ImageDraw.Draw(flare)
                flare_draw.ellipse([cx - max_r, cy - max_r // 2, cx + max_r, cy + max_r // 2], fill=(255, 255, 245, alpha_burst))
                flare = flare.filter(ImageFilter.GaussianBlur(10.0))
                frame = Image.alpha_composite(frame, flare)

        # 4. 실제 영상 배경 위에 합성 (20, 20 위치)
        canvas = bg_crop.copy()
        canvas.paste(frame, (20, 20), frame)
        canvas.save(os.path.join(frames_dir, f"frame_{f:04d}.png"))

    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        out_mp4
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"[+] 🎯 {desc} 렌더링 완결: {out_mp4}")

if __name__ == "__main__":
    print("[*] 볼록 양각 24K 황금 + 세로선 제거 + 투명 배경 렌더링 가동...")
    # 1. 완전 투명 100% 버전 (실제 영상 배경 투과)
    render_motion_preview(True, OUT_MP4_TRANSPARENT, "시안 2-B [100% 완전 투명 배경 + 볼록 양각 24K 골드]")
    # 2. 20% 반투명 글래스 틴트 버전 (비교용)
    render_motion_preview(False, OUT_MP4_GLASSTINT, "시안 2-B [20% 글래스모피즘 반투명 + 볼록 양각 24K 골드]")
    
    # 대표 투명 PNG 저장
    base = build_base_badge(transparent_mode=True)
    out_png = os.path.join(IMAGES_DIR, "hookverse_top_left_badge_transparent_convex.png")
    base.save(out_png)
    print(f"[+] 대표 투명 PNG 저장 완료: {out_png}")
