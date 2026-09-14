#!/usr/bin/env python3
"""
video_assembler.py — Hookverse Studio 자동 비디오 조립 렌더러 v1.0
역할: 성우 나레이션 음성(MP3)과 4장의 컷 이미지를 결합하여
      시네마틱 줌인/줌아웃 카메라 무빙(Ken Burns)이 적용된 9:16 세로 숏폼 완성본(MP4)을 자동 렌더링합니다.
비용: 100% $0원 (로컬 imageio-ffmpeg 기반)
"""

import os
import sys
import re
import glob
import subprocess
import argparse
from datetime import datetime

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
AUDIO_DIR = os.path.join(WORKSPACE, "assets", "audio")
IMAGES_DIR = os.path.join(WORKSPACE, "assets", "images")
VIDEOS_DIR = os.path.join(WORKSPACE, "assets", "videos")

def get_ffmpeg_binary():
    try:
        import imageio_ffmpeg
        return imageio_ffmpeg.get_ffmpeg_exe()
    except Exception:
        return "ffmpeg"

def get_audio_duration(ffmpeg_exe: str, audio_path: str) -> float:
    """FFmpeg를 통해 오디오의 정확한 재생 시간(초)을 측정"""
    cmd = [ffmpeg_exe, "-i", audio_path]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    # Duration: 00:00:25.50, ...
    m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
    if m:
        hours = float(m.group(1))
        minutes = float(m.group(2))
        seconds = float(m.group(3))
        return hours * 3600 + minutes * 60 + seconds
    return 28.0  # 기본값

def assemble_shorts(
    audio_path: str,
    image_paths: list,
    output_filename: str = "IMF2화_자정의조흥은행_최종완성본.mp4",
    width: int = 1080,
    height: int = 1920,
    fps: int = 30
):
    os.makedirs(VIDEOS_DIR, exist_ok=True)
    ffmpeg_exe = get_ffmpeg_binary()
    
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"오디오 파일을 찾을 수 없습니다: {audio_path}")
        
    duration = get_audio_duration(ffmpeg_exe, audio_path)
    num_images = len(image_paths)
    if num_images == 0:
        raise ValueError("합성할 이미지가 없습니다.")
        
    per_image_duration = duration / num_images
    print(f"[*] 🎬 비디오 조립 시작:")
    print(f"    - 총 오디오 길이: {duration:.2f}초")
    print(f"    - 이미지 수: {num_images}장 (장당 약 {per_image_duration:.2f}초)")
    print(f"    - 해상도: {width}x{height} (9:16 Vertical Shorts)")
    
    output_path = os.path.join(VIDEOS_DIR, output_filename)
    
    # 각 이미지 클립을 생성하기 위한 FFmpeg 입력 구성
    # 켄 번스(Ken Burns) 줌인/줌아웃 효과 필터
    # 컷 1: 서서히 줌인 (1.0 -> 1.08)
    # 컷 2: 서서히 줌아웃 (1.08 -> 1.0)
    # 컷 3: 다급한 줌인 (1.0 -> 1.10)
    # 컷 4: 아련한 줌아웃 (1.08 -> 1.0)
    
    # 복합 필터 그래프 생성
    inputs = []
    filter_complex_parts = []
    
    for idx, img in enumerate(image_paths):
        inputs.extend(["-loop", "1", "-t", str(per_image_duration), "-i", img])
        
        # 줌 모션 설정 (zoompan 필터 사용 또는 scale+crop)
        # 1080x1920 해상도에 맞게 scale 및 패딩/크롭
        # 줌인과 줌아웃 교차 적용
        zoom_expr = "min(zoom+0.0008,1.08)" if idx % 2 == 0 else "max(1.08-0.0008*on,1.0)"
        
        filter_part = (
            f"[{idx}:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},"
            f"zoompan=z='{zoom_expr}':d={int(per_image_duration*fps)}:s={width}x{height}:fps={fps},"
            f"setsar=1[v{idx}];"
        )
        filter_complex_parts.append(filter_part)
        
    concat_inputs = "".join([f"[v{i}]" for i in range(num_images)])
    concat_part = f"{concat_inputs}concat=n={num_images}:v=1:a=0[vcat]"
    filter_complex_parts.append(concat_part)
    
    filter_complex_str = "".join(filter_complex_parts)
    
    cmd = [
        ffmpeg_exe, "-y",
        *inputs,
        "-i", audio_path,
        "-filter_complex", filter_complex_str,
        "-map", "[vcat]",
        "-map", f"{num_images}:a",
        "-c:v", "libx264",
        "-preset", "fast",
        "-pix_fmt", "yuv420p",
        "-c:a", "aac",
        "-b:a", "192k",
        "-shortest",
        output_path
    ]
    
    print(f"[*] 🚀 FFmpeg 인코딩 렌더링 중... (잠시만 기다려주세요)")
    res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    
    if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
        file_size = os.path.getsize(output_path)
        print(f"[+] 🎉 30초 세로 쇼츠 완성본(MP4) 디스크 안착 성공!")
        print(f"    - 파일 경로: {output_path}")
        print(f"    - 파일 용량: {file_size:,} bytes ({file_size/1024/1024:.2f} MB)")
        return output_path
    else:
        print("[-] 인코딩 실패 로그:")
        print(res.stderr[-800:])
        raise RuntimeError("비디오 조립 인코딩 실패")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hookverse Shorts Video Assembler")
    parser.add_argument("--audio", "-a", default=None)
    parser.add_argument("--output", "-o", default="IMF2화_자정의조흥은행_최종완성본.mp4")
    args = parser.parse_args()
    
    # 기본 오디오
    target_audio = args.audio
    if not target_audio or not os.path.exists(target_audio):
        target_audio = os.path.join(AUDIO_DIR, "IMF2화_자정의조흥은행_30초대본_성우음성.mp3")
        
    # 2화 4컷 이미지 수집
    ep02_img_dir = os.path.join(IMAGES_DIR, "IMF2화")
    img_files = sorted(glob.glob(os.path.join(ep02_img_dir, "*.jpg")))
    
    if len(img_files) < 4:
        # 혹시 4장이 안 보이면 상위 이미지 탐색
        img_files = sorted(glob.glob(os.path.join(IMAGES_DIR, "**", "*.jpg"), recursive=True))[:4]
        
    print(f"[*] 대상 오디오: {target_audio}")
    print(f"[*] 매칭된 이미지: {len(img_files)}장")
    for f in img_files:
        print(f"    - {os.path.basename(f)}")
        
    assemble_shorts(target_audio, img_files, output_filename=args.output)
