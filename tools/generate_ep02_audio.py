#!/usr/bin/env python3
"""
generate_ep02_audio.py — IMF 2화 4컷 정밀 대본 전용 고음질 손서현 성우 나레이션 생성기
"""

import os
import asyncio
import edge_tts
import imageio_ffmpeg
import subprocess

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

script_text = (
    "하지만 이미 놈들이 움직였습니다. "
    "1997년 11월 21일 자정, 조흥은행 시계탑이 멈춘 순간. "
    "어둠 속에서 좁혀오는 검은 양복의 사냥꾼들. "
    "흠뻑 젖은 그녀는 빗속 골목길로 필사의 질주를 시작했습니다. "
    "골목 끝 은색 공중전화 부스. "
    "손에 쥔 스마트폰 배터리는 단 1%... "
    "남은 기회는 단 한 번뿐이었습니다. "
    "수화기 너머 조력자에게 남긴 마지막 명령. "
    "박 과장님, 놈들이 왔어요. 지금 당장 금고를 잠그세요! "
    "그리고 전화는 끊겼습니다."
)

output_audio = os.path.join(WORKSPACE, "assets", "audio", "IMF2화_추격과비밀통화_4컷_성우음성.mp3")

async def generate():
    # 28~30초 완벽 안착 딕션 (rate=+12%, pitch=-2Hz 미스터리 스릴러)
    comm = edge_tts.Communicate(script_text, "ko-KR-SunHiNeural", rate="+12%", pitch="-2Hz")
    await comm.save(output_audio)

print("[*] 1. IMF 2화 4컷 손서현 성우 나레이션 생성 중...")
asyncio.run(generate())

# 오디오 길이 측정
res = subprocess.run([ffmpeg, "-i", output_audio], capture_output=True, text=True, errors="ignore")
import re
m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
if m:
    sec = float(m.group(1))*3600 + float(m.group(2))*60 + float(m.group(3))
    print(f"[+] ✅ 오디오 생성 완료: {output_audio} (재생 시간: {sec:.2f}초)")
else:
    print(f"[+] ✅ 오디오 생성 완료: {output_audio}")
