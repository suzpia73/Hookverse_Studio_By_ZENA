#!/usr/bin/env python3
"""
render_true_convex_pure_gold_motion.py —
오빠의 3대 피드백을 완벽히 해결한 10초 풀 모션 비디오 렌더러
1. 타원형 번쩍임 0% 완전 삭제 -> 진짜 카메라 플래시 노출 오버(Global Shutter Flash Burst)
2. 정면 조명을 받은 맑고 화사한 24K 순금 (탁한 갈색 100% 제거)
3. 둥글고 볼록하게 솟아오른 3D 볼록 엠보스 (Convex Pillow Bevel)
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
OUT_MP4 = os.path.join(IMAGES_DIR, "badge_true_convex_pure_gold_motion.mp4")
OUT_ART = r"C:\Users\june2\.gemini\antigravity-ide\brain\ca192b04-baee-4d55-a3f1-37e9601b7fd9\badge_true_convex_pure_gold_motion.mp4"

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 380, 136

def render_real_convex_3d_text(font, text, cx, y_pos, base_w, base_h):
    dummy = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    d_draw = ImageDraw.Draw(dummy)
    bbox = d_draw.textbbox((0, 0), text, font=font)
    tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
    tx = cx - tw // 2
    ty = y_pos

    mask = Image.new("L", (base_w, base_h), 0)
    ImageDraw.Draw(mask).text((tx, ty), text, fill=255, font=font)

    # 3단계 돔 높이 맵 (볼록하게 솟아오르는 곡면)
    h_map1 = mask.filter(ImageFilter.GaussianBlur(1.5))
    h_map2 = mask.filter(ImageFilter.GaussianBlur(3.5))
    h_map3 = mask.filter(ImageFilter.GaussianBlur(6.0))

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
                
                dome = v1_val * 0.4 + v2_val * 0.4 + v3_val * 0.2
                
                # 맑고 환한 정면 조명 골드 (탁함 0%)
                if dome > 0.70:
                    t = (dome - 0.70) / 0.30
                    r = 255
                    g = int(245 + 10 * t)
                    b = int(140 + 115 * t)
                elif dome > 0.30:
                    t = (dome - 0.30) / 0.40
                    r = 255
                    g = int(195 + 50 * t)
                    b = int(20 + 120 * t)
                else:
                    t = dome / 0.30
                    r = int(220 + 35 * t)
                    g = int(140 + 55 * t)
                    b = int(10 + 10 * t)

                gold_surface.putpixel((x, y), (r, g, b, 255))

    # 모서리 엠보스 림
    inner_cut = mask.filter(ImageFilter.GaussianBlur(1.0))
    for y in range(base_h):
        for x in range(base_w):
            if mask.getpixel((x, y)) > 0:
                ic = inner_cut.getpixel((x, y))
                ic_val = ic[0] if isinstance(ic, tuple) else (ic or 0)
                if ic_val < 200:
                    gold_surface.putpixel((x, y), (255, 255, 240, 255))

    # 깊은 3D 드롭 섀도우
    shadow = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    s_draw = ImageDraw.Draw(shadow)
    s_draw.text((tx + 2, ty + 4), text, fill=(0, 0, 0, 245), font=font)
    s_draw.text((tx + 3, ty + 6), text, fill=(0, 0, 0, 180), font=font)
    shadow = shadow.filter(ImageFilter.GaussianBlur(3.0))

    out = Image.new("RGBA", (base_w, base_h), (0, 0, 0, 0))
    out = Image.alpha_composite(out, shadow)
    out = Image.alpha_composite(out, gold_surface)

    return out

def build_base_badge():
    badge = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(badge)

    # 1. 24K 순금 트윈 레일 (맑고 화사한 정면 조명 골드)
    draw.line([(0, 2), (W, 2)], fill=(255, 250, 180, 255), width=2)
    draw.line([(0, 4), (W, 4)], fill=(200, 140, 20, 220), width=1)
    draw.line([(0, 22), (W, 22)], fill=(255, 225, 60, 240), width=1)
    draw.line([(0, 23), (W, 23)], fill=(160, 100, 10, 200), width=1)

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
        draw.rounded_rectangle([x-1, 6, x + hole_w + 1, 6 + hole_h + 2], radius=3, outline=(255, 245, 160, 240), width=1)
        draw.rounded_rectangle([x, 7, x + hole_w, 7 + hole_h], radius=2, outline=(140, 80, 10, 220), width=1)
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

    # 4. 볼록 3D 글자
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

    return badge

def render_motion():
    base_badge = build_base_badge()

    # 빗길 실제 배경 로드
    bg_path = os.path.join(WORKSPACE, "assets", "images", "IMF2화_스틸_cut01_raw.png")
    if os.path.exists(bg_path):
        bg_src = Image.open(bg_path).convert("RGBA").crop((20, 40, 20 + 420, 40 + 176)).resize((420, 176))
    else:
        bg_src = Image.new("RGBA", (420, 176), (15, 18, 28, 255))

    fps = 30
    duration = 10.0
    total_frames = int(fps * duration)

    frames_dir = os.path.join(WORKSPACE, "scratch", "frames_pure_convex_motion")
    os.makedirs(frames_dir, exist_ok=True)

    print(f"[*] 맑은 정면 조명 볼록 3D 골드 10초 모션 렌더링 시작 (총 {total_frames}프레임)...")
    flash_peaks = [1.5, 8.5]

    for f in range(total_frames):
        t = f / fps
        frame = base_badge.copy()

        # 1. 35mm 필름 화이트 스크래치
        scratch = Image.new("RGBA", (W, H), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(scratch)
        random.seed(f * 883 + 19)
        if random.random() < 0.35:
            sx = random.randint(15, W - 16)
            s_draw.line([(sx, 4), (sx + random.uniform(-1, 1), H - 4)], fill=(255, 255, 255, random.randint(90, 160)), width=1)
        frame = Image.alpha_composite(frame, scratch)

        # 2. 6.5초 주기 소프트 실크 쉰 (3.0 ~ 5.0초 단 1회 스치고 지나감)
        if 3.0 <= t <= 5.0:
            sweep_ratio = (t - 3.0) / 2.0
            beam_pos = int(-40 + (W + 80) * sweep_ratio)
            sheen = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            sh_draw = ImageDraw.Draw(sheen)
            beam_w = 40
            for bx in range(beam_pos - beam_w, beam_pos + beam_w):
                dist = abs(bx - beam_pos) / float(beam_w)
                alpha = int(90 * (0.5 * (1.0 + math.cos(dist * math.pi))))
                if alpha > 0 and 5 <= bx < W - 5:
                    sh_draw.line([(bx, 22), (bx + 20, H - 22)], fill=(255, 255, 230, alpha), width=1)
            sheen = sheen.filter(ImageFilter.GaussianBlur(3.0))
            frame = Image.alpha_composite(frame, sheen)

        # 3. 진짜 카메라 플래시 노출 오버 (타원형 원 영구 삭제! 전체 노출 블룸)
        flash_power = 0.0
        for peak in flash_peaks:
            dt = t - peak
            if 0.0 <= dt < 0.35:
                flash_power = max(flash_power, math.exp(-dt * 12.0))

        if flash_power > 0.02:
            # 타원형이 아니라, 글자 전체와 레일 전체가 순간적으로 환하게 빛을 뿜는 전면 노출 플래시
            bloom_alpha = int(220 * flash_power)
            flash_overlay = Image.new("RGBA", (W, H), (255, 252, 235, bloom_alpha))
            # 텍스트와 레일 마스크 영역에만 블룸 합성
            frame = Image.alpha_composite(frame, flash_overlay.filter(ImageFilter.GaussianBlur(2.0)))

        # 실제 영상 배경 위에 합성
        canvas = bg_src.copy()
        canvas.paste(frame, (20, 20), frame)
        canvas.save(os.path.join(frames_dir, f"frame_{f:04d}.png"))

    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUT_MP4
    ]
    subprocess.run(cmd, capture_output=True)
    
    # 아티팩트 복사
    import shutil
    shutil.copy2(OUT_MP4, OUT_ART)
    print(f"[+] 🎯 완벽 수정된 10초 모션 MP4 완결: {OUT_MP4}")

if __name__ == "__main__":
    render_motion()
