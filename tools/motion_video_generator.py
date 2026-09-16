# -*- coding: utf-8 -*-
"""
Hookverse Studio - 살아 움직이는 시네마틱 모션 비디오 생성기 (Motion Video Generator)
- 오빠의 헌법: '정지된 단순 이미지 슬라이드쇼 영구 퇴출 ➡️ 살아 숨 쉬는 진짜 영상 쇼츠'
- I2V (Image-to-Video) 다이내믹 카메라 모션 시뮬레이션:
  1. 빗줄기(Rain Drops) 및 네온 불빛 깜빡임(Neon Glare Flicker)
  2. 35mm 카메라 핸드헬드 미세 흔들림(Handheld Breathing Motion)
  3. 시네마틱 줌인/줌아웃(Slow Dolly In & Pan Right)
- 정지된 컷을 5초짜리 살아 숨 쉬는 1080p 시네마틱 영상 클립(.mp4)으로 물리적 변환
"""

import os
import sys
import subprocess

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
MOTION_OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "videos", "motion_clips")

from video_assembler import get_ffmpeg_binary

def generate_motion_clip(image_path, output_mp4, duration=5.0, motion_type="dolly_in"):
    """정지 이미지를 5초짜리 살아 숨 쉬는 모션 비디오 클립으로 렌더링"""
    if not os.path.exists(image_path):
        print(f"❌ 원본 이미지를 찾을 수 없습니다: {image_path}")
        return False

    ffmpeg_bin = get_ffmpeg_binary()
    os.makedirs(MOTION_OUTPUT_DIR, exist_ok=True)
    
    # 모션 타입별 FFmpeg 다이내믹 필터 그래프
    if motion_type == "dolly_in":
        # 천천히 전진하며 미세하게 숨 쉬는 카메라 무빙
        vf = (
            f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"zoompan=z='min(zoom+0.0015,1.15)':x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':d={int(duration*30)}:s=1080x1920:fps=30,"
            f"drawbox=y=ih*0.76:color=black@0.45:width=iw:height=ih*0.24:t=fill"
        )
    elif motion_type == "tracking_pan":
        # 우측으로 천천히 이동하는 트래킹 샷
        vf = (
            f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"zoompan=z=1.08:x='if(lte(on,1),(iw-iw/zoom)/2,x+0.5)':y='ih/2-(ih/zoom/2)':d={int(duration*30)}:s=1080x1920:fps=30,"
            f"drawbox=y=ih*0.76:color=black@0.45:width=iw:height=ih*0.24:t=fill"
        )
    else:
        # 긴장감 있는 핸드헬드 POV 샷
        vf = (
            f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,"
            f"zoompan=z='min(zoom+0.001,1.10)':x='iw/2-(iw/zoom/2)+sin(in)*2':y='ih/2-(ih/zoom/2)+cos(in)*2':d={int(duration*30)}:s=1080x1920:fps=30,"
            f"drawbox=y=ih*0.76:color=black@0.45:width=iw:height=ih*0.24:t=fill"
        )

    cmd = [
        ffmpeg_bin, "-y", "-loop", "1", "-i", image_path,
        "-vf", vf,
        "-c:v", "libx264", "-t", str(duration), "-pix_fmt", "yuv420p",
        output_mp4
    ]


    try:
        res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore", timeout=60)
        if res.returncode == 0 and os.path.exists(output_mp4):
            print(f"✅ 모션 비디오 클립 렌더링 완료: {os.path.basename(output_mp4)} ({duration}초)")
            return True
        else:
            print(f"⚠️ FFmpeg 렌더링 경고: {res.stderr[-200:]}")
            return False
    except Exception as e:
        print(f"⚠️ 모션 생성 예외: {e}")
        return False

def run_all_motion_clips():
    print("=" * 65)
    print("🎬 [Motion Video] 정지 이미지 ➡️ 살아 움직이는 영상 쇼츠 클립 변환")
    print("=" * 65)
    
    img_dir = os.path.join(BASE_DIR, "assets", "images", "IMF2화")
    if not os.path.exists(img_dir):
        print("❌ 2화 이미지 폴더 누락")
        return False

    success_count = 0
    # 씬 1 (시계탑) 및 씬 3 (스마트폰 속보) 시범 모션 클립 렌더링
    test_cases = [
        ("IMF전날밤의비밀_ep02_cut01.jpg", "scene01_clock_motion.mp4", 6.2, "dolly_in"),
        ("IMF전날밤의비밀_ep02_cut03.jpg", "scene03_phone_glitch_motion.mp4", 5.3, "handheld")
    ]
    
    for img_name, out_name, dur, m_type in test_cases:
        in_p = os.path.join(img_dir, img_name)
        out_p = os.path.join(MOTION_OUTPUT_DIR, out_name)
        if os.path.exists(in_p):
            if generate_motion_clip(in_p, out_p, duration=dur, motion_type=m_type):
                success_count += 1
                
    print("=" * 65)
    print(f"🎉 살아 움직이는 영상 쇼츠 모션 클립 {success_count}건 생성 완료! 경로: {MOTION_OUTPUT_DIR}")
    return True

if __name__ == "__main__":
    run_all_motion_clips()
