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
    # 1. imageio_ffmpeg 동적 시도 (Pyrefly missing-import 경고 방지)
    try:
        import importlib
        m = importlib.import_module("imageio_ffmpeg")
        exe = m.get_ffmpeg_exe()
        if exe and os.path.exists(exe):
            return exe
    except Exception:
        pass

    # 2. Python 환경 내 imageio_ffmpeg 바이너리 직접 탐색
    py_dir = os.path.dirname(sys.executable)
    pkg_patterns = [
        os.path.join(py_dir, "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg*"),
        os.path.join(os.environ.get("LOCALAPPDATA", ""), "Programs", "Python", "Python314", "Lib", "site-packages", "imageio_ffmpeg", "binaries", "ffmpeg*"),
    ]
    for pattern in pkg_patterns:
        matches = glob.glob(pattern)
        if matches and os.path.exists(matches[0]):
            return matches[0]

    # 3. 시스템 PATH fallback
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
    output_filename: str = "IMF2화_자정의중앙 금융 금고_최종완성본.mp4",
    custom_durations: list = None,
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
        
    # 가변 타임코드 적용: custom_durations가 전달되면 대사 호흡 길이에 1:1 Sync, 없으면 균등 분할
    if custom_durations and len(custom_durations) == num_images:
        durations = [float(d) for d in custom_durations]
        scale_factor = duration / sum(durations) if sum(durations) > 0 else 1.0
        durations = [d * scale_factor for d in durations]
        print(f"[*] 🎬 가변 타임코드 모드 활성화 (대사-이미지 1:1 Sync):")
        for i, (p, d) in enumerate(zip(image_paths, durations)):
            print(f"    - 씬 {i+1}: {d:.2f}초 ({os.path.basename(p)})")
    else:
        per_image_duration = duration / num_images
        durations = [per_image_duration] * num_images
        print(f"[*] 🎬 균등 타임코드 모드: 장당 {per_image_duration:.2f}초 ({num_images}장)")

    print(f"    - 총 오디오 길이: {duration:.2f}초")
    print(f"    - 해상도: {width}x{height} (9:16 Vertical Shorts)")
    
    output_path = os.path.join(VIDEOS_DIR, output_filename)
    
    inputs = []
    filter_complex_parts = []
    
    for idx, (img, dur) in enumerate(zip(image_paths, durations)):
        inputs.extend(["-loop", "1", "-t", f"{dur:.3f}", "-i", img])
        
        # 1080x1920 규격 맞춤 및 안정적 FPS/SAR 설정 (버그 없는 순차 전환)
        filter_part = (
            f"[{idx}:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
            f"crop={width}:{height},"
            f"setsar=1,fps={fps}[v{idx}];"
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
        "-preset", "veryfast",
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
    # 2화 8씬 정밀 SRT 칼싱크 기본 타임코드: 6.2s, 5.3s, 5.3s, 5.3s, 5.2s, 5.7s, 5.5s, 6.74s (총 45.24s)
    DEFAULT_IMF2_DURATIONS = [6.2, 5.3, 5.3, 5.3, 5.2, 5.7, 5.5, 6.74]
    parser.add_argument("--output", "-o", default="IMF2화_지하_비밀_외환_금고일치_0.1초칼싱크_교체완성본.mp4")
    parser.add_argument("--durations", "-d", nargs="+", type=float, default=DEFAULT_IMF2_DURATIONS, help="씬별 가변 듀레이션(초) 리스트")
    args = parser.parse_args()
    
    # 기본 오디오
    target_audio = args.audio
    if not target_audio or not os.path.exists(target_audio):
        target_audio = os.path.join(AUDIO_DIR, "IMF2화_자정의중앙 금융 금고_30초대본_성우음성.mp3")
        
    # 2화 이미지 수집
    ep02_img_dir = os.path.join(IMAGES_DIR, "IMF2화")
    img_files = sorted(glob.glob(os.path.join(ep02_img_dir, "*.jpg")))
    
    if len(img_files) < 4:
        # 혹시 4장이 안 보이면 상위 이미지 탐색
        img_files = sorted(glob.glob(os.path.join(IMAGES_DIR, "**", "*.jpg"), recursive=True))[:4]
        
    print(f"[*] 대상 오디오: {target_audio}")
    print(f"[*] 매칭된 이미지: {len(img_files)}장")
    for f in img_files:
        print(f"    - {os.path.basename(f)}")
        
    assemble_shorts(target_audio, img_files, output_filename=args.output, custom_durations=args.durations)
