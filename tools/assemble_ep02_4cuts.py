#!/usr/bin/env python3
"""
assemble_ep02_4cuts.py — IMF 2화 4컷 정밀 마스터 비디오 조립 렌더러
"""

import os
import subprocess
import imageio_ffmpeg

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

audio_path = os.path.join(WORKSPACE, "assets", "audio", "IMF2화_추격과비밀통화_4컷_성우음성.mp3")
output_path = os.path.join(WORKSPACE, "assets", "videos", "IMF2화_추격과비밀통화_4컷_마스터완성본.mp4")

images = [
    os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut01.jpg"),
    os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut02.jpg"),
    os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut03.jpg"),
    os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut04.jpg"),
]

# 4컷 대사 호흡 1:1 칼싱크 (총 37.44초)
durations = [8.8, 9.8, 8.8, 10.04]

width, height, fps = 1080, 1920, 30

inputs = []
filter_complex_parts = []

for idx, (img, dur) in enumerate(zip(images, durations)):
    inputs.extend(["-loop", "1", "-t", f"{dur:.3f}", "-i", img])
    filter_part = (
        f"[{idx}:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},"
        f"setsar=1,fps={fps}[v{idx}];"
    )
    filter_complex_parts.append(filter_part)

concat_inputs = "".join([f"[v{i}]" for i in range(len(images))])
concat_part = f"{concat_inputs}concat=n={len(images)}:v=1:a=0[vcat]"
filter_complex_parts.append(concat_part)

filter_complex_str = "".join(filter_complex_parts)

cmd = [
    ffmpeg_exe, "-y",
    *inputs,
    "-i", audio_path,
    "-filter_complex", filter_complex_str,
    "-map", "[vcat]",
    "-map", f"{len(images)}:a",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    output_path
]

print("[*] 🚀 IMF 2화 4컷 마스터 비디오 렌더링 시작...")
res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")

if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
    size = os.path.getsize(output_path)
    print(f"[+] 🎉 2화 마스터 비디오 렌더링 성공! ({size/1024/1024:.2f} MB)")
    print(f"    - 저장 경로: {output_path}")
else:
    print("[-] 렌더링 실패:")
    print(res.stderr[-800:])
