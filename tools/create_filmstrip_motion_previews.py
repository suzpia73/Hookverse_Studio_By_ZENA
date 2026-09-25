#!/usr/bin/env python3
"""
create_filmstrip_motion_previews.py —
오빠를 위한 '영화 필름지 배지' 2대 시안 모션 영상 (MP4) 정밀 생성기
- 시안 1: 시네마틱 골든 & 네이비 필름스트립 (영사기 렌즈 빛 스윕 모션)
- 시안 2: 1997 아날로그 빈티지 35mm 필름스트립 (영사기 셔터 롤링/지터 모션)
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont
import imageio_ffmpeg
import subprocess

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
FONT_SWANKY = os.path.join(WORKSPACE, "assets", "fonts", "FontdinerSwanky-Regular.ttf")
IMAGES_DIR = os.path.join(WORKSPACE, "assets", "images")

OUT_MP4_1 = os.path.join(IMAGES_DIR, "badge_filmstrip_option1_golden.mp4")
OUT_MP4_2 = os.path.join(IMAGES_DIR, "badge_filmstrip_option2_vintage.mp4")

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

W, H = 360, 130  # 짝수 규격

def draw_sprocket_holes(draw, y_top, w, h, num_holes=7, border_color=None, fill_color=(0, 0, 0, 0)):
    # 필름지 상하 퍼포레이션 홀(사각 구멍) 그리기
    hole_w = 16
    hole_h = 10
    step = (w - 20) / num_holes
    for i in range(num_holes):
        x = int(10 + i * step + (step - hole_w) / 2)
        y = y_top
        # 모서리가 살짝 둥근 사각 구멍
        draw.rounded_rectangle([x, y, x + hole_w, y + hole_h], radius=2, fill=fill_color, outline=border_color, width=1)

def build_base_option1():
    # 시안 1 베이스: 골든 & 딥 네이비 필름스트립
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. 외곽 골든 림 테두리 & 상하 레일
    draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=8, fill=(12, 18, 30, 255), outline=(212, 175, 55, 230), width=2)

    # 2. 중앙 필름 인화면 (Deep Navy -> Electric Blue 그라데이션)
    inner_top = 22
    inner_bottom = H - 22
    inner_h = inner_bottom - inner_top
    inner_w = W - 12
    
    c_start = (6, 16, 32)
    c_end = (0, 91, 234)
    
    for x in range(6, W - 6):
        ratio = (x - 6) / max(1, inner_w - 1)
        r = int(c_start[0] + (c_end[0] - c_start[0]) * ratio)
        g = int(c_start[1] + (c_end[1] - c_start[1]) * ratio)
        b = int(c_start[2] + (c_end[2] - c_start[2]) * ratio)
        for y in range(inner_top, inner_bottom):
            img.putpixel((x, y), (r, g, b, 255))

    draw = ImageDraw.Draw(img)
    # 인화면 골든 얇은 경계선
    draw.rectangle([6, inner_top, W - 7, inner_bottom], outline=(180, 140, 40, 180), width=1)

    # 3. 상하 퍼포레이션 홀 (투명 펀칭 + 골든 아웃라인)
    draw_sprocket_holes(draw, 5, W, H, num_holes=8, border_color=(212, 175, 55, 200), fill_color=(15, 23, 42, 255))
    draw_sprocket_holes(draw, H - 15, W, H, num_holes=8, border_color=(212, 175, 55, 200), fill_color=(15, 23, 42, 255))

    # 4. 텍스트 렌더링
    font = ImageFont.truetype(FONT_SWANKY, 36)
    b1 = draw.textbbox((0, 0), "Hookverse", font=font)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    b2 = draw.textbbox((0, 0), "Studio", font=font)
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]

    cx = W // 2
    y_center = (inner_top + inner_bottom) // 2
    
    start_y = y_center - (h1 + 4 + h2) // 2
    x1 = cx - w1 // 2
    x2 = cx - w2 // 2

    # 드롭 섀도우 & 순백색 본문
    draw.text((x1 + 1, start_y + 1), "Hookverse", fill=(0, 0, 0, 160), font=font)
    draw.text((x2 + 1, start_y + h1 + 4 + 1), "Studio", fill=(0, 0, 0, 160), font=font)
    draw.text((x1, start_y), "Hookverse", fill=(255, 255, 255, 255), font=font)
    draw.text((x2, start_y + h1 + 4), "Studio", fill=(255, 255, 255, 255), font=font)

    return img

def build_base_option2():
    # 시안 2 베이스: 1997 아날로그 빈티지 35mm 필름스트립
    img = Image.new("RGBA", (W, H), (0, 0, 0, 0))
    draw = ImageDraw.Draw(img)

    # 1. 셀룰로이드 필름 베이스 (다크 앰버/차콜 블랙)
    draw.rounded_rectangle([0, 0, W - 1, H - 1], radius=4, fill=(18, 16, 14, 255), outline=(60, 50, 40, 255), width=2)

    # 2. 중앙 필름 인화면 (빈티지 시네마틱 틴트)
    inner_top = 24
    inner_bottom = H - 24
    draw.rectangle([8, inner_top, W - 9, inner_bottom], fill=(28, 22, 18, 255), outline=(70, 55, 45, 200), width=1)

    # 3. 상하 클래식 퍼포레이션 홀
    draw_sprocket_holes(draw, 6, W, H, num_holes=8, border_color=(80, 70, 60, 255), fill_color=(8, 7, 6, 255))
    draw_sprocket_holes(draw, H - 16, W, H, num_holes=8, border_color=(80, 70, 60, 255), fill_color=(8, 7, 6, 255))

    # 4. 레트로 필름 프레임 넘버링 (1997, 35mm, KODAK 감성)
    try:
        small_font = ImageFont.load_default()
    except Exception:
        small_font = None

    if small_font:
        # 상단 레일 텍스트: 오렌지 앰버 필름 코드
        draw.text((16, 6), "▶ 1997 KAIRA 500T", fill=(230, 150, 40, 220), font=small_font)
        draw.text((W - 100, 6), "SAFETY FILM", fill=(230, 150, 40, 200), font=small_font)
        # 하단 레일 텍스트: 프레임 번호
        draw.text((16, H - 15), "35mm FILM", fill=(230, 150, 40, 200), font=small_font)
        draw.text((W - 90, H - 15), "FRAME 02 ▶▶", fill=(230, 150, 40, 220), font=small_font)

    # 5. 텍스트 렌더링
    font = ImageFont.truetype(FONT_SWANKY, 36)
    b1 = draw.textbbox((0, 0), "Hookverse", font=font)
    w1, h1 = b1[2] - b1[0], b1[3] - b1[1]
    b2 = draw.textbbox((0, 0), "Studio", font=font)
    w2, h2 = b2[2] - b2[0], b2[3] - b2[1]

    cx = W // 2
    y_center = (inner_top + inner_bottom) // 2
    start_y = y_center - (h1 + 4 + h2) // 2
    x1 = cx - w1 // 2
    x2 = cx - w2 // 2

    # 따뜻한 아이보리/골든 화이트 본문
    draw.text((x1 + 1, start_y + 1), "Hookverse", fill=(0, 0, 0, 180), font=font)
    draw.text((x2 + 1, start_y + h1 + 4 + 1), "Studio", fill=(0, 0, 0, 180), font=font)
    draw.text((x1, start_y), "Hookverse", fill=(255, 245, 230, 255), font=font)
    draw.text((x2, start_y + h1 + 4), "Studio", fill=(255, 245, 230, 255), font=font)

    return img

def render_motion_option1():
    # 시안 1 모션: 영사기 렌즈 빛줄기 스윕(Light Beam Sweep) 2.5초 루프
    base = build_base_option1()
    fps = 30
    duration = 2.5
    total_frames = int(fps * duration)

    frames_dir = os.path.join(WORKSPACE, "scratch", "frames_opt1")
    os.makedirs(frames_dir, exist_ok=True)

    beam_w = 60  # 빛의 폭

    for f in range(total_frames):
        t = f / total_frames
        # 빛줄기가 좌측(-beam_w)에서 우측(W + beam_w)으로 이동
        # 0.0 ~ 0.6 구간 동안 스윕, 0.6 ~ 1.0은 잠시 고요함 유지
        if t < 0.65:
            beam_x = int(-beam_w + (W + beam_w * 2) * (t / 0.65))
        else:
            beam_x = -999  # 화면 밖

        frame = base.copy()
        
        if beam_x > -beam_w and beam_x < W + beam_w:
            # 반투명 화이트/골든 빛줄기 블렌딩
            glow_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
            g_draw = ImageDraw.Draw(glow_layer)
            
            # 대각선 빛줄기
            for bx in range(beam_x - beam_w // 2, beam_x + beam_w // 2):
                dist = abs(bx - beam_x) / (beam_w / 2)
                alpha = int(140 * (1.0 - dist * dist))
                if alpha > 0 and 6 <= bx < W - 6:
                    g_draw.line([(bx, 22), (bx + 20, H - 22)], fill=(255, 250, 220, alpha), width=1)
            
            frame = Image.alpha_composite(frame, glow_layer)

        # 숏폼 영상 배경(다크 네이비 캔버스 380x150) 위에 안착
        canvas = Image.new("RGB", (380, 150), (10, 14, 22))
        canvas.paste(frame, (10, 10), frame)
        canvas.save(os.path.join(frames_dir, f"frame_{f:04d}.png"))

    # FFmpeg으로 MP4 렌더링
    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUT_MP4_1
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"[+] 🎯 시안 1 모션 비디오 렌더링 완결: {OUT_MP4_1}")

def render_motion_option2():
    # 시안 2 모션: 1997 아날로그 영사기 셔터 지터(Jitter) & 미세 진동 루프
    base = build_base_option2()
    fps = 30
    duration = 2.5
    total_frames = int(fps * duration)

    frames_dir = os.path.join(WORKSPACE, "scratch", "frames_opt2")
    os.makedirs(frames_dir, exist_ok=True)

    for f in range(total_frames):
        t = f / total_frames
        
        # 영사기 특유의 미세한 수직 지터 (±1.5px) 및 필름 플리커(Flicker)
        jitter_y = int(math.sin(f * 1.8) * 1.5 + math.cos(f * 3.7) * 1.0)
        jitter_x = int(math.sin(f * 0.9) * 0.8)

        # 영사기 셔터 펄스 (밝기 미세 진동)
        flicker_alpha = int(15 * math.sin(f * 2.5))

        frame = base.copy()
        
        if flicker_alpha > 0:
            shutter = Image.new("RGBA", (W, H), (255, 230, 180, flicker_alpha))
            frame = Image.alpha_composite(frame, shutter)

        # 숏폼 배경(다크 앰버 캔버스 380x150) 위에 안착
        canvas = Image.new("RGB", (380, 150), (14, 12, 10))
        canvas.paste(frame, (10 + jitter_x, 10 + jitter_y), frame)
        canvas.save(os.path.join(frames_dir, f"frame_{f:04d}.png"))

    cmd = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        "-movflags", "+faststart",
        OUT_MP4_2
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"[+] 🎯 시안 2 모션 비디오 렌더링 완결: {OUT_MP4_2}")

if __name__ == "__main__":
    print("[*] 영화 필름지 배지 2대 시안 모션 렌더링 시작...")
    render_motion_option1()
    render_motion_option2()
    print("[*] 완료!")
