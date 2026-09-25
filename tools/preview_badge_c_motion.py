#!/usr/bin/env python3
"""
preview_badge_c_motion.py — 시안 C (루미너스 화이트 페이드) 깃발 펄럭임(Flag Wave) 순수 Pillow 애니메이션 생성기
"""

import os
import math
from PIL import Image
import imageio_ffmpeg
import subprocess

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
SRC_BADGE = os.path.join(WORKSPACE, "assets", "images", "badge_option_c_luminous.png")
OUT_GIF = os.path.join(WORKSPACE, "assets", "images", "badge_c_flag_wave_preview.gif")
OUT_MP4 = os.path.join(WORKSPACE, "assets", "images", "badge_c_flag_wave_preview.mp4")

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

def generate_flag_wave_animation():
    base_img = Image.open(SRC_BADGE).convert("RGBA")
    W, H = base_img.size
    
    fps = 30
    duration_sec = 2.0  # 2초 무한 루프
    total_frames = int(fps * duration_sec)
    
    pad_top = 18
    pad_bottom = 18
    out_H = H + pad_top + pad_bottom
    out_W = W + 6

    # 1px 열(column) 슬라이스들 미리 캐싱
    columns = [base_img.crop((x, 0, x + 1, H)) for x in range(W)]
    
    frames = []

    for f in range(total_frames):
        t = f / total_frames
        phase = 2 * math.pi * t

        frame = Image.new("RGBA", (out_W, out_H), (0, 0, 0, 0))

        # 좌측은 고정(anchor), 우측으로 갈수록 부드러운 물결 파동
        for x in range(W):
            ratio = x / max(1, W - 1)
            # 2차 곡선으로 우측 팁으로 갈수록 유연하게 펄럭임
            amp = 7.5 * (ratio ** 1.3)
            wave = math.sin(phase - ratio * 2.2 * math.pi)
            y_shift = int(amp * wave)
            
            dest_y = pad_top + y_shift
            frame.paste(columns[x], (x, dest_y), columns[x])

        frames.append(frame)

    # 1. 고화질 애니메이션 GIF 저장 (loop=0 무한반복)
    frames[0].save(
        OUT_GIF,
        save_all=True,
        append_images=frames[1:],
        duration=int(1000 / fps),
        loop=0,
        disposal=2
    )
    print(f"[+] ✅ 시안 C 깃발 펄럭임 애니메이션 GIF 생성 완료: {OUT_GIF}")

    # 2. 어두운 배경(영상 시뮬레이션용) 결합 비디오 클립 생성
    # 검은 캔버스 위에 GIF 오버레이하여 MP4 출력
    cmd = [
        ffmpeg, "-y",
        "-f", "lavfi", "-i", f"color=c=0x0d1117:s={out_W}x{out_H}:d=2.0:r={fps}",
        "-i", OUT_GIF,
        "-filter_complex", "[0:v][1:v]overlay=0:0:shortest=1",
        "-c:v", "libx264", "-pix_fmt", "yuv420p",
        OUT_MP4
    ]
    subprocess.run(cmd, capture_output=True)
    print(f"[+] ✅ 시안 C 깃발 펄럭임 MP4 클립 생성 완료: {OUT_MP4}")

if __name__ == "__main__":
    generate_flag_wave_animation()
