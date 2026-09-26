#!/usr/bin/env python3
# type: ignore
"""
render_perfect_270_badge_motion.py —
[오빠의 냉철한 분석 100% 반영: 위치 완벽 일치 최종 마스터판]
1. 규격: W=270, H=136 (글자 크기 원본 그대로 보존 + 좌우 여백 안정적 38px)
2. 타공: 상하단 각 15개 구멍, 18.0px 수학적 등간격 칼대칭 & 100% 무결점 심리스 롤링 (짜집기 흔적 0%)
3. 글자 위치 100% 무결점 일치:
   - HOOKVERSE: Y: 33 ~ 76 (H=43) 아래로 +3px 정확히 내려서 하단 베벨까지 100% 일치!
   - STUDIO:    Y: 87 ~ 107 (H=20) 아래로 +7px 대폭 내려서 크롬 본체에 1:1 완벽 밀착! (이중 잔상 0% 박멸)
4. 점등: H -> O -> O -> K -> V -> E -> R -> S -> E -> S -> T -> U -> D -> I -> O
   철자 모양(Stroke Silhouette) 그대로 한 자 한 자 도미노처럼 켜지면서 누적 유지!
5. 아날로그 필름 효과: 꼬불 실오라기, 점먼지, 2~3px 펀치력 수직 스크래치, 셔터 플래시!
"""

import os
import sys
import math
import random
import subprocess
from PIL import Image, ImageDraw, ImageFilter
import imageio_ffmpeg

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
IMAGES_DIR = os.path.join(WORKSPACE, "assets", "images")
VIDEOS_DIR = os.path.join(WORKSPACE, "assets", "videos")
SCRATCH_DIR = r"C:\Users\june2\.gemini\antigravity-ide\brain\dbaf9410-e8bc-49cd-8615-a13340b70e86"
SOURCE_IMG2_MASK = os.path.join(WORKSPACE, "scratch_img2_mask.png")
BADGE_270_PATH = os.path.join(WORKSPACE, "scratch_badge_270_perfect_sprockets.png")

OUT_CLOSEUP_MP4 = os.path.join(VIDEOS_DIR, "배지모션_270px_완벽타공_글자순차점등_클로즈업.mp4")
OUT_MOBILE_MP4 = os.path.join(WORKSPACE, "📱휴대폰감상용_270px_완벽타공_글자순차점등_1080p.mp4")
OUT_MOBILE_ASSETS = os.path.join(VIDEOS_DIR, "📱휴대폰감상용_270px_완벽타공_글자순차점등_1080p.mp4")

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

TARGET_W = 270
TARGET_H = 136
RAIL_H = 24
PITCH = 18.0
HOLE_W = 9
HOLE_H = 13
CORNER_R = 2.5

# TRUE 1:1 CALIBRATED COORDINATES (NO SHADOWS, NO RESIDUAL ARTIFACTS)
LETTERS_TRUE_1TO1 = [
    # Top Row: HOOKVERSE (9 letters) — Y: 33 ~ 76
    ("H",   20, 139, 325, 585, True),
    ("O1", 139, 248, 325, 585, True),
    ("O2", 248, 355, 325, 585, True),
    ("K",  355, 488, 325, 585, True),
    ("V",  488, 602, 325, 585, True),
    ("E1", 602, 694, 325, 585, True),
    ("R",  694, 802, 325, 585, True),
    ("S1", 802, 895, 325, 585, True),
    ("E2", 895, 1012, 325, 585, True),

    # Bot Row: STUDIO (6 letters) — Y: 87 ~ 107
    ("S2", 185, 308, 598, 728, False),
    ("T",  308, 424, 598, 728, False),
    ("U",  424, 542, 598, 728, False),
    ("D",  542, 658, 598, 728, False),
    ("I",  658, 720, 598, 728, False),
    ("O3", 720, 856, 598, 728, False),
]

def build_masks():
    mask_1024 = Image.open(SOURCE_IMG2_MASK)
    letter_masks = {}
    for name, x0, x1, y0, y1, is_top in LETTERS_TRUE_1TO1:
        let_crop = mask_1024.crop((x0, y0, x1, y1))
        if is_top:
            bx0 = int(37 + (x0 - 20) * (196.0 / 992.0))
            bx1 = int(37 + (x1 - 20) * (196.0 / 992.0))
            by0 = 33
            by1 = 76
        else:
            bx0 = int(75 + (x0 - 185) * (130.0 / 671.0))
            bx1 = int(75 + (x1 - 185) * (130.0 / 671.0))
            by0 = 87
            by1 = 107

        bw = max(1, bx1 - bx0)
        bh = max(1, by1 - by0)
        resized = let_crop.resize((bw, bh), Image.Resampling.BILINEAR)

        let_canvas = Image.new("L", (TARGET_W, TARGET_H), 0)
        let_canvas.paste(resized, (bx0, by0))
        letter_masks[name] = (let_canvas, (bx0, by0, bx0 + bw, by0 + bh))
    return letter_masks

def draw_hair(draw, w, h, seed):
    rng = random.Random(seed)
    num_strands = rng.randint(1, 2)
    for _ in range(num_strands):
        pts = []
        curr_x = rng.randint(20, w - 20)
        curr_y = rng.randint(15, h - 15)
        pts.append((curr_x, curr_y))
        for _ in range(rng.randint(5, 9)):
            curr_x += rng.randint(-7, 7)
            curr_y += rng.randint(-7, 7)
            curr_x = max(5, min(w - 5, curr_x))
            curr_y = max(5, min(h - 5, curr_y))
            pts.append((curr_x, curr_y))
        hair_c = rng.choice([(255, 255, 255, rng.randint(190, 255)), (255, 240, 220, rng.randint(180, 240))])
        for i in range(len(pts) - 1):
            draw.line([pts[i], pts[i+1]], fill=hair_c, width=1)

def draw_dust(draw, w, h, seed):
    rng = random.Random(seed)
    for _ in range(rng.randint(3, 6)):
        dx = rng.randint(5, w - 5)
        dy = rng.randint(5, h - 5)
        rad = rng.uniform(0.6, 1.3)
        c = rng.choice([(255, 255, 255, rng.randint(150, 220)), (25, 20, 15, rng.randint(120, 190))])
        draw.ellipse([dx - rad, dy - rad, dx + rad, dy + rad], fill=c)

def main():
    print("=" * 65)
    print("🎬 [270px 진정한 1:1 위치 일치 최종 마스터 비디오 렌더링]")
    print("=" * 65)

    base_badge = Image.open(BADGE_270_PATH).convert("RGBA")
    letter_masks = build_masks()

    top_rail_single = base_badge.crop((0, 0, TARGET_W, RAIL_H))
    bot_rail_single = base_badge.crop((0, TARGET_H - RAIL_H, TARGET_W, TARGET_H))
    inner_art = base_badge.crop((0, RAIL_H, TARGET_W, TARGET_H - RAIL_H))

    seamless_top = Image.new("RGBA", (TARGET_W * 2, RAIL_H))
    seamless_top.paste(top_rail_single, (0, 0))
    seamless_top.paste(top_rail_single, (TARGET_W, 0))

    seamless_bot = Image.new("RGBA", (TARGET_W * 2, RAIL_H))
    seamless_bot.paste(bot_rail_single, (0, 0))
    seamless_bot.paste(bot_rail_single, (TARGET_W, 0))

    fps = 30
    duration = 8.0
    total_frames = int(fps * duration)

    frames_cu_dir = os.path.join(SCRATCH_DIR, "f_270_cu_true")
    frames_mob_dir = os.path.join(SCRATCH_DIR, "f_270_mob_true")
    os.makedirs(frames_cu_dir, exist_ok=True)
    os.makedirs(frames_mob_dir, exist_ok=True)

    bg_path = os.path.join(IMAGES_DIR, "IMF2화_스틸_cut01_raw.png")
    if os.path.exists(bg_path):
        bg_full = Image.open(bg_path).convert("RGBA").resize((1080, 1920), Image.Resampling.LANCZOS)
    else:
        bg_full = Image.new("RGBA", (1080, 1920), (15, 18, 28, 255))

    logo_path = os.path.join(IMAGES_DIR, "hookverse_studio_logo_transparent.png")
    has_logo = os.path.exists(logo_path)
    logo_raw: Image.Image | None = None
    if has_logo:
        logo_raw = Image.open(logo_path).convert("RGBA").resize((136, 136), Image.Resampling.LANCZOS)

    ignite_start_t = 1.6
    step_dt = 0.11
    letter_trigger_times = [ignite_start_t + i * step_dt for i in range(15)]

    roll_speed = 36.0 # 36px/sec = exactly 2 holes per second

    print(f"[*] 총 {total_frames}프레임 정밀 합성 중...")

    for f in range(total_frames):
        t = f / float(fps)
        rng_f = random.Random(f * 883 + 19)

        # 1. 🎞️ 100% 무결점 심리스 롤링 타공 레일
        roll_x = int((t * roll_speed) % TARGET_W)
        top_crop = seamless_top.crop((roll_x, 0, roll_x + TARGET_W, RAIL_H))
        bot_crop = seamless_bot.crop((roll_x, 0, roll_x + TARGET_W, RAIL_H))

        frame = Image.new("RGBA", (TARGET_W, TARGET_H), (10, 8, 6, 255))
        frame.paste(top_crop, (0, 0))
        frame.paste(inner_art, (0, RAIL_H))
        frame.paste(bot_crop, (0, TARGET_H - RAIL_H))

        # 2. ✨ 글자 모양 철자별 순차 누적 점등 (진정한 1:1 칼일치)
        pix = frame.load()
        for idx in range(15):
            trig_t = letter_trigger_times[idx]
            dt = t - trig_t

            if dt >= 0:
                name = LETTERS_TRUE_1TO1[idx][0]
                let_mask_img, (bx0, by0, bx1, by1) = letter_masks[name]
                l_pix = let_mask_img.load()

                if dt < 0.22:
                    # White-hot peak
                    flash_intensity = math.exp(-dt * 12.0)
                    for py in range(by0, by1):
                        for px in range(bx0, bx1):
                            m = l_pix[px, py]  # type: ignore
                            if m > 20:
                                w = m / 255.0
                                r, g, b, a = pix[px, py]  # type: ignore
                                nr = min(255, int(r + (160 + 90 * flash_intensity) * w))
                                ng = min(255, int(g + (140 + 80 * flash_intensity) * w))
                                nb = min(255, int(b + (100 + 70 * flash_intensity) * w))
                                pix[px, py] = (nr, ng, nb, a)  # type: ignore
                else:
                    # Steady warm platinum glow (누적 유지)
                    shimmer = 1.0 + 0.08 * math.sin(t * 8.0 + idx)
                    for py in range(by0, by1):
                        for px in range(bx0, bx1):
                            m = l_pix[px, py]  # type: ignore
                            if m > 20:
                                w = (m / 255.0) * shimmer
                                r, g, b, a = pix[px, py]  # type: ignore
                                nr = min(255, int(r + 140 * w))
                                ng = min(255, int(g + 120 * w))
                                nb = min(255, int(b + 80 * w))
                                pix[px, py] = (nr, ng, nb, a)  # type: ignore

        # 3. 셔터 플래시 버스트
        flash_power = 0.0
        for ft in [1.2, 7.2]:
            f_dt = abs(t - ft)
            if f_dt < 0.12:
                flash_power = max(flash_power, 1.0 - (f_dt / 0.12))

        # 4. 아날로그 필름 노이즈
        noise_layer = Image.new("RGBA", (TARGET_W, TARGET_H), (0, 0, 0, 0))
        n_draw = ImageDraw.Draw(noise_layer)
        if (25 <= f <= 35) or (110 <= f <= 122) or (180 <= f <= 195):
            draw_hair(n_draw, TARGET_W, TARGET_H, f * 991)
        draw_dust(n_draw, TARGET_W, TARGET_H, f * 337)
        if rng_f.random() < 0.40:
            sx = rng_f.randint(10, TARGET_W - 15)
            sw = rng_f.choice([1, 2, 2, 3])
            sa = rng_f.randint(120, 220)
            n_draw.line([(sx, 0), (sx, TARGET_H)], fill=(255, 255, 255, sa), width=sw)

        frame = Image.alpha_composite(frame, noise_layer)

        if flash_power > 0.05:
            white_flash = Image.new("RGBA", (TARGET_W, TARGET_H), (255, 250, 235, int(flash_power * 190)))
            frame = Image.alpha_composite(frame, white_flash)

        # Gate weave
        gw_x = rng_f.choice([-1, 0, 0, 1])
        gw_y = rng_f.choice([-1, 0, 0, 1])
        cu_frame = Image.new("RGBA", (TARGET_W, TARGET_H), (10, 8, 6, 255))
        cu_frame.paste(frame, (gw_x, gw_y))

        # 2x upscaled closeup frame (540x272)
        cu_hi = cu_frame.resize((TARGET_W * 2, TARGET_H * 2), Image.Resampling.LANCZOS)
        cu_hi.convert("RGB").save(os.path.join(frames_cu_dir, f"frame_{f:04d}.png"))

        # Mobile frame
        canvas_mob = bg_full.copy()
        dark_scrim = Image.new("RGBA", (1080, 1920), (0, 0, 0, 80))
        canvas_mob = Image.alpha_composite(canvas_mob, dark_scrim)

        # Top-left official badge
        canvas_mob.paste(frame, (70, 70), frame)
        if has_logo and logo_raw is not None:
            canvas_mob.paste(logo_raw, (874, 70), logo_raw)

        # Large center preview (810x408 - 3x scale)
        badge_large = frame.resize((810, 408), Image.Resampling.LANCZOS)
        center_y = (1920 - 408) // 2
        center_x = (1080 - 810) // 2
        canvas_mob.paste(badge_large, (center_x, center_y), badge_large)

        m_draw = ImageDraw.Draw(canvas_mob)
        m_draw.text((center_x, center_y - 40), "HOOKVERSE STUDIO [100% 진정한 1:1 위치 일치 완성판]", fill=(255, 220, 140, 240))
        m_draw.text((center_x, center_y + 420), f"Time: {t:4.2f}s | HOOKVERSE(y:33~76) STUDIO(y:87~107) Perfect 1:1", fill=(200, 200, 200, 200))

        canvas_mob.convert("RGB").save(os.path.join(frames_mob_dir, f"frame_{f:04d}.png"))

        if f % 40 == 0:
            print(f"   -> 진행률: {f}/{total_frames} ({f/total_frames*100:.1f}%)")

    print("[*] 인코딩 시작...")

    cmd_cu = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_cu_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        OUT_CLOSEUP_MP4
    ]
    subprocess.run(cmd_cu, check=True)
    print(f"[+] 클로즈업 MP4 완성: {OUT_CLOSEUP_MP4}")

    cmd_mob = [
        ffmpeg, "-y",
        "-framerate", str(fps),
        "-i", os.path.join(frames_mob_dir, "frame_%04d.png"),
        "-c:v", "libx264", "-preset", "medium", "-crf", "16", "-pix_fmt", "yuv420p",
        OUT_MOBILE_MP4
    ]
    subprocess.run(cmd_mob, check=True)
    print(f"[+] 휴대폰 감상용 MP4 완성: {OUT_MOBILE_MP4}")

    import shutil
    shutil.copy2(OUT_MOBILE_MP4, OUT_MOBILE_ASSETS)
    print("=" * 65)
    print("🎉 [완벽 완성] 1:1 위치 일치 최종 마스터 비디오 완성!")
    print("=" * 65)

if __name__ == "__main__":
    main()
