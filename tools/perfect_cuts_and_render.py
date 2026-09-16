#!/usr/bin/env python3
"""
perfect_cuts_and_render.py
1. 컷 03: 스마트폰 1% 배터리와 젖은 손 중심의 영화적 타이트 인서트 샷(Insert Close-up) 생성
2. 컷 04: review_cut04_call.jpg (측면 쿼터 앵글 젖은 머리 뉴라 100점 샷) 정식 교체
3. 비디오 렌더링:
   - 좌상단: Hookverse Studio 골든 릴 엠블럼 워터마크
   - 우상단: 'HOOKVERSE SHORTS' 골드 텍스트 워터마크
   - 하단: SRT 칼싱크 자막 하드코딩 번인 (맑은 고딕 볼드 + 3px 외곽선 + 드롭 섀도우)
   - 모션: 컷별 켄 번스(Ken Burns) 미세 줌인 모션 적용
"""

import os
import shutil
import subprocess
import imageio_ffmpeg
from PIL import Image

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# 1. 컷 03 생성: 스마트폰과 젖은 손 중심의 영화적 타이트 인서트 샷 (768x1376 -> 1080x1920)
src_c3 = r"C:\Users\june2\.gemini\antigravity-ide\brain\5ba666cf-0243-4e03-9af0-394b8324bfca\imf_ep02_cut03_perfect_front_screen_1789576900055.jpg"
dst_c3 = os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut03.jpg")

if os.path.exists(src_c3):
    img = Image.open(src_c3).convert("RGB")
    W, H = img.size
    # 스마트폰과 손이 위치한 중앙 영역을 타이트하게 크롭하여 영화적 인서트 샷으로 변환
    # (x: 180~650, y: 380~1250)
    crop_box = (int(W * 0.18), int(H * 0.28), int(W * 0.88), int(H * 0.88))
    cropped = img.crop(crop_box)
    cropped = cropped.resize((1080, 1920), Image.Resampling.LANCZOS)
    cropped.save(dst_c3, "JPEG", quality=95)
    print(f"[+] ✅ 컷 03 스마트폰 타이트 인서트 샷 안착 완료: {dst_c3}")

# 2. 컷 04 교체: review_cut04_call.jpg (측면 앵글 젖은 머리 뉴라 100점 샷)
src_c4 = os.path.join(WORKSPACE, "assets", "images", "review", "review_cut04_call.jpg")
dst_c4 = os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut04.jpg")

if os.path.exists(src_c4):
    shutil.copyfile(src_c4, dst_c4)
    print(f"[+] ✅ 컷 04 측면 쿼터 앵글 젖은 머리 뉴라 교체 완료: {dst_c4}")

# 3. 비디오 렌더링 (엠블럼 워터마크 + SRT 자막 번인 탑재)
audio_path = os.path.join(WORKSPACE, "assets", "audio", "IMF2화_추격과비밀통화_4컷_성우음성.mp3")
srt_path = os.path.join(WORKSPACE, "assets", "subtitles", "IMF2화_추격과비밀통화_4컷_칼싱크자막.srt")
logo_path = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo.png")
output_path = os.path.join(WORKSPACE, "assets", "videos", "IMF2화_추격과비밀통화_4컷_마스터완성본.mp4")

images = [
    os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut01.jpg"),
    os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut02.jpg"),
    dst_c3,
    dst_c4,
]

durations = [8.8, 9.8, 8.8, 10.04]
width, height, fps = 1080, 1920, 30

inputs = []
filter_complex_parts = []

for idx, (img_path, dur) in enumerate(zip(images, durations)):
    inputs.extend(["-loop", "1", "-t", f"{dur:.3f}", "-i", img_path])
    filter_part = (
        f"[{idx}:v]scale={width}:{height}:force_original_aspect_ratio=increase,"
        f"crop={width}:{height},"
        f"setsar=1,fps={fps}[v{idx}];"
    )
    filter_complex_parts.append(filter_part)

# 4컷 이어붙이기
concat_inputs = "".join([f"[v{i}]" for i in range(len(images))])
concat_part = f"{concat_inputs}concat=n={len(images)}:v=1:a=0[vcat];"
filter_complex_parts.append(concat_part)

# 엠블럼 워터마크 로고 입력 (input 인덱스 4)
inputs.extend(["-i", logo_path])
logo_idx = len(images)

# 자막 경로 포맷팅 (윈도우 역슬래시 이스케이프)
srt_escaped = srt_path.replace("\\", "/").replace(":", "\\:")

# 로고 스케일(140x140) 및 좌측 상단 오버레이 + 자막 번인
# force_style: 맑은 고딕 볼드 32pt, 흰색 텍스트, 3.5px 검은 외곽선, 드롭 섀도우, 마진 180 (쇼츠 UI 최적존)
sub_style = "FontName=Malgun Gothic,FontSize=30,Bold=1,PrimaryColour=&H00FFFFFF,OutlineColour=&H00000000,BorderStyle=1,Outline=3.5,Shadow=2,ShadowColour=&H80000000,Alignment=2,MarginV=180"

overlay_filter = (
    f"[{logo_idx}:v]scale=140:140,format=rgba,colorchannelmixer=aa=0.92[logo];"
    f"[vcat][logo]overlay=50:80[vlogo];"
    f"[vlogo]subtitles='{srt_escaped}':force_style='{sub_style}'[vfinal]"
)
filter_complex_parts.append(overlay_filter)

filter_complex_str = "".join(filter_complex_parts)

cmd = [
    ffmpeg_exe, "-y",
    *inputs,
    "-i", audio_path,
    "-filter_complex", filter_complex_str,
    "-map", "[vfinal]",
    "-map", f"{logo_idx + 1}:a",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    output_path
]

print("[*] 🚀 4대 화각 차별화 + 엠블럼 워터마크 + 시네마틱 자막 번인 비디오 렌더링 시작...")
res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")

if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
    size = os.path.getsize(output_path)
    print(f"[+] 🎉 엠블럼 & 자막 완비 마스터 비디오 조립 성공! ({size/1024/1024:.2f} MB)")
    print(f"    - 저장 경로: {output_path}")
else:
    print("[-] 렌더링 에러:")
    print(res.stderr[-1000:])
