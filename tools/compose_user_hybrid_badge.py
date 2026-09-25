#!/usr/bin/env python3
"""
compose_user_hybrid_badge.py —
오빠의 1번 필름 배경 + 2번 3D 크롬 글자 정밀 합성 & 모션 비디오 렌더러 (v2 완벽 옥의티 박멸)
1. 1번 이미지에서 마크/이전글자 침범 0% 순수 스프로킷 레일(상/하) 및 좌우 빛바램 추출
2. 중앙 인화면을 1번 이미지의 오리지널 웜 브라운 조명과 순수 가죽 그레인으로 100% 무결점 복원
3. 2번 이미지의 초고화질 3D 크롬 "HOOKVERSE STUDIO" 글자 정밀 분리 (블랙 배경 투명화)
4. 배지 사이즈(380x136) 정중앙에 황금 비율로 안착
5. 기존 셔터 모션 효과 (35mm 수직 스크래치 + 6.5초 소프트 쉰 + 10초 카메라 플래시 버스트) 렌더링
"""

import os
import math
import random
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg
import subprocess

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
IMAGES_DIR = os.path.join(WORKSPACE, "assets", "images")

PATH_IMG1 = r"C:\Users\june2\.gemini\antigravity-ide\brain\ca192b04-baee-4d55-a3f1-37e9601b7fd9\.user_uploaded\media_1790361281032.jpg"
PATH_IMG2 = r"C:\Users\june2\.gemini\antigravity-ide\brain\ca192b04-baee-4d55-a3f1-37e9601b7fd9\.user_uploaded\media_1790361465780.jpg"

OUT_STILL = os.path.join(IMAGES_DIR, "hookverse_badge_hybrid_user_choice.png")
OUT_STILL_OFFICIAL = os.path.join(IMAGES_DIR, "hookverse_top_left_badge.png")
OUT_STILL_ART = r"C:\Users\june2\.gemini\antigravity-ide\brain\ca192b04-baee-4d55-a3f1-37e9601b7fd9\hookverse_badge_hybrid_user_choice.png"
OUT_MP4 = os.path.join(IMAGES_DIR, "hookverse_badge_hybrid_user_choice_motion.mp4")
OUT_MP4_ART = r"C:\Users\june2\.gemini\antigravity-ide\brain\ca192b04-baee-4d55-a3f1-37e9601b7fd9\hookverse_badge_hybrid_user_choice_motion.mp4"

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

TARGET_W, TARGET_H = 380, 136

def extract_clean_film_background(img1, target_w, target_h):
    """
    1번 이미지에서 이전 글자와 마크를 100% 완벽히 제거하고
    순수 스프로킷 레일, 좌우 오리지널 빛바램, 웜 브라운 조명 가죽 인화면만 복원
    """
    w1, h1 = img1.size
    
    # 1. 상단/하단 스프로킷 레일 (마크/글자 침범 0% 순수 영역 분리)
    rail_h = 24
    rail_top = img1.crop((0, 0, w1, 95)).resize((target_w, rail_h), Image.Resampling.LANCZOS)
    rail_bottom = img1.crop((0, 585, w1, h1)).resize((target_w, rail_h), Image.Resampling.LANCZOS)

    # 2. 인화면 높이 = 136 - 48 = 88px
    inner_h = target_h - (rail_h * 2)
    inner_canvas = Image.new("RGBA", (target_w, inner_h), (0, 0, 0, 255))

    # 3. 중앙 조명 앰비언트 (1번 이미지 고유의 웜 골드-브라운 스포트라이트)
    for y in range(inner_h):
        ny = (y - inner_h / 2.0) / (inner_h / 2.0)
        for x in range(target_w):
            nx = (x - target_w / 2.0) / (target_w / 2.0)
            dist = math.sqrt(nx * nx * 0.8 + ny * ny * 1.6)
            intensity = max(0.0, 1.0 - min(1.0, dist)) ** 1.3

            r = int(26 + (72 - 26) * intensity)
            g = int(18 + (50 - 18) * intensity)
            b = int(14 + (28 - 14) * intensity)
            inner_canvas.putpixel((x, y), (r, g, b, 255))

    # 4. 순수 가죽 그레인 텍스처 (1번 이미지 우측 순수 가죽 영역 x: 910~1010, y: 150~550)
    leather_src = img1.crop((910, 150, 1010, 550)).resize((target_w, inner_h), Image.Resampling.LANCZOS)
    inner_canvas = Image.blend(inner_canvas, leather_src, 0.22)

    # 5. 좌측 빛바램 (x: 0~120, y: 95~585) - 글자 침범 0%
    burn_left = img1.crop((0, 95, 120, 585)).resize((80, inner_h), Image.Resampling.LANCZOS)
    burn_mask = Image.new("L", (80, inner_h), 0)
    for x in range(80):
        alpha = int(255 * ((1.0 - (x / 80.0)) ** 1.3))
        for y in range(inner_h):
            burn_mask.putpixel((x, y), alpha)
    inner_canvas.paste(burn_left, (0, 0), burn_mask)

    # 6. 우측 비네팅 엣지 (x: 900~1024, y: 95~585) - 글자 침범 0%
    edge_right = img1.crop((900, 95, w1, 585)).resize((70, inner_h), Image.Resampling.LANCZOS)
    right_mask = Image.new("L", (70, inner_h), 0)
    for x in range(70):
        alpha = int(255 * ((x / 70.0) ** 1.3))
        for y in range(inner_h):
            right_mask.putpixel((x, y), alpha)
    inner_canvas.paste(edge_right, (target_w - 70, 0), right_mask)

    # 7. 전체 필름 베이스 조립
    clean_film = Image.new("RGBA", (target_w, target_h), (12, 10, 8, 255))
    clean_film.paste(rail_top, (0, 0))
    clean_film.paste(inner_canvas, (0, rail_h))
    clean_film.paste(rail_bottom, (0, target_h - rail_h))

    return clean_film

def extract_3d_chrome_text(img2):
    """
    2번 이미지에서 3D 크롬 "HOOKVERSE STUDIO" 글자 영역을 정밀 분리 (블랙 배경 100% 투명화)
    """
    crop_area = (20, 310, 1004, 725)
    text_crop = img2.crop(crop_area).convert("RGBA")
    tw, th = text_crop.size

    clean_text = Image.new("RGBA", (tw, th), (0, 0, 0, 0))
    for y in range(th):
        for x in range(tw):
            px = text_crop.getpixel((x, y))
            r, g, b = int(px[0]), int(px[1]), int(px[2])

            max_c = max(r, g, b)
            min_c = min(r, g, b)
            sat = max_c - min_c
            bright = max_c

            if bright < 28:
                alpha = 0
            elif bright < 55 and sat < 15:
                ratio = (bright - 28) / (55 - 28)
                alpha = int(255 * ratio)
            else:
                alpha = 255

            if alpha > 0:
                clean_text.putpixel((x, y), (r, g, b, alpha))

    return clean_text

def build_composite_badge():
    img1 = Image.open(PATH_IMG1).convert("RGBA")
    img2 = Image.open(PATH_IMG2).convert("RGBA")

    # 1. 이전 글자 잔상 0% 100% 무결점 필름 배경 생성
    base_film = extract_clean_film_background(img1, TARGET_W, TARGET_H)

    # 2. 3D 크롬 글자 추출
    clean_text = extract_3d_chrome_text(img2)

    # 3. 글자 크기 최적 조정
    target_th = 72
    aspect = clean_text.width / float(clean_text.height)
    target_tw = int(target_th * aspect)
    if target_tw > TARGET_W - 30:
        target_tw = TARGET_W - 30
        target_th = int(target_tw / aspect)

    resized_text = clean_text.resize((target_tw, target_th), Image.Resampling.LANCZOS)

    # 4. 글자 뒤 3D 드롭 섀도우 (깊이감 강화)
    shadow = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
    tx = (TARGET_W - target_tw) // 2
    ty = (TARGET_H - target_th) // 2

    text_alpha = resized_text.split()[-1]
    black_shape = Image.new("RGBA", resized_text.size, (0, 0, 0, 235))
    black_shape.putalpha(text_alpha)
    shadow.paste(black_shape, (tx + 2, ty + 3), black_shape)
    shadow = shadow.filter(ImageFilter.GaussianBlur(2.0))

    # 5. 최종 합성
    final_badge = base_film.copy()
    final_badge = Image.alpha_composite(final_badge, shadow)
    final_badge.paste(resized_text, (tx, ty), resized_text)

    # 스틸 이미지 저장 및 공식 배지 반영
    final_badge.save(OUT_STILL)
    final_badge.save(OUT_STILL_OFFICIAL)
    final_badge.save(OUT_STILL_ART)
    print(f"[+] 🎯 완벽 무결점 하이브리드 배지 스틸 렌더링 완료: {OUT_STILL}")

    return final_badge

def render_motion_video(base_badge):
    bg_path = os.path.join(WORKSPACE, "assets", "images", "IMF2화_스틸_cut01_raw.png")
    if os.path.exists(bg_path):
        bg_src = Image.open(bg_path).convert("RGBA").crop((20, 40, 20 + 420, 40 + 176)).resize((420, 176))
    else:
        bg_src = Image.new("RGBA", (420, 176), (15, 18, 28, 255))

    fps = 30
    duration = 10.0
    total_frames = int(fps * duration)

    frames_dir = os.path.join(WORKSPACE, "scratch", "frames_user_hybrid")
    os.makedirs(frames_dir, exist_ok=True)

    print(f"[*] 하이브리드 배지 10초 풀 모션 비디오 렌더링 시작 (총 {total_frames}프레임)...")
    flash_peaks = [1.5, 8.5]

    for f in range(total_frames):
        t = f / fps
        frame = base_badge.copy()

        # 1. 35mm 필름 화이트 수직 스크래치
        scratch = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
        s_draw = ImageDraw.Draw(scratch)
        random.seed(f * 883 + 19)
        if random.random() < 0.35:
            sx = random.randint(15, TARGET_W - 16)
            s_draw.line([(sx, 4), (sx + random.uniform(-1, 1), TARGET_H - 4)], fill=(255, 255, 255, random.randint(90, 160)), width=1)
        frame = Image.alpha_composite(frame, scratch)

        # 2. 6.5초 주기 소프트 실크 쉰 (3.0 ~ 5.0초 단 1회 스치고 지나감)
        if 3.0 <= t <= 5.0:
            sweep_ratio = (t - 3.0) / 2.0
            beam_pos = int(-40 + (TARGET_W + 80) * sweep_ratio)
            sheen = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
            sh_draw = ImageDraw.Draw(sheen)
            beam_w = 40
            for bx in range(beam_pos - beam_w, beam_pos + beam_w):
                dist = abs(bx - beam_pos) / float(beam_w)
                alpha = int(90 * (0.5 * (1.0 + math.cos(dist * math.pi))))
                if alpha > 0 and 5 <= bx < TARGET_W - 5:
                    sh_draw.line([(bx, 24), (bx + 20, TARGET_H - 24)], fill=(255, 255, 230, alpha), width=1)
            sheen = sheen.filter(ImageFilter.GaussianBlur(3.0))
            frame = Image.alpha_composite(frame, sheen)

        # 3. 카메라 플래시 버스트 (타원형 없는 전체 노출 플래시)
        flash_power = 0.0
        for peak in flash_peaks:
            dt = t - peak
            if 0.0 <= dt < 0.35:
                flash_power = max(flash_power, math.exp(-dt * 12.0))

        if flash_power > 0.02:
            bloom_alpha = int(220 * flash_power)
            flash_overlay = Image.new("RGBA", (TARGET_W, TARGET_H), (255, 252, 235, bloom_alpha))
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

    import shutil
    shutil.copy2(OUT_MP4, OUT_MP4_ART)
    print(f"[+] 🎯 완벽 무결점 하이브리드 배지 10초 풀 모션 MP4 완결: {OUT_MP4}")

    # 임시 프레임 폴더 정리
    try:
        shutil.rmtree(frames_dir)
        print("[+] 임시 프레임 폴더 정리 완료")
    except Exception:
        pass

if __name__ == "__main__":
    badge = build_composite_badge()
    render_motion_video(badge)
