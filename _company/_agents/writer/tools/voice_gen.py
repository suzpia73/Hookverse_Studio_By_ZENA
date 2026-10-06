#!/usr/bin/env python3
"""
voice_gen.py — J멘토식 $0원 초고품질 한국어 성우 음성 생성 엔진 v1.0
역할: 30초 대본 마크다운 파일에서 성우 나레이션 멘트만 추출하여
      Microsoft 고품질 뉴럴 엔진(edge-tts)으로 assets/audio/ 에 MP3를 자동 생성합니다.
기본 음성: ko-KR-SunHiNeural (여성 미스터리/나레이션 전문 보이스)
옵션: ko-KR-InJoonNeural (남성 보이스)
비용: 100% $0원 (무료/무제한)
"""

import os
import sys
import re
import asyncio
import argparse
from datetime import datetime

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
SCRIPTS_DIR = os.path.join(WORKSPACE, "assets", "scripts")
AUDIO_DIR = os.path.join(WORKSPACE, "assets", "audio")

DEFAULT_VOICE = "ko-KR-SunHiNeural"  # 선희 (여성 고품질 뉴럴)
MALE_VOICE = "ko-KR-InJoonNeural"    # 인준 (남성 고품질 뉴럴)

def clean_script_for_tts(raw_text: str) -> str:
    """대본에서 [SFX], [BGM], 시간 태그 (00:00~00:03) 등 특수 연출 지문을 걷어내고 순수 성우 멘트만 추출"""
    lines = raw_text.splitlines()
    clean_lines = []
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
        # 헤더, 구분선, 안내문 스킵
        if line.startswith("#") or line.startswith("---") or line.startswith(">") or line.startswith("- **") or line.startswith("* **"):
            continue
        if "🎬" in line or "📜" in line or "📸" in line or "장르" in line or "등장인물" in line or "권장 성우" in line:
            continue
        # [SFX: ...], [BGM: ...] 태그 제거
        line = re.sub(r'\[(?:SFX|BGM|연출|음악|한국어 연출 지문)[^\]]*\]', '', line)
        # 시간 구간 태그 제거: (00:00~00:03), [0~6초 : 컷 1...], **0:00 - 0:03:** 등
        line = re.sub(r'\([0-9]{2}:[0-9]{2}[^)]*\)', '', line)
        line = re.sub(r'\[[0-9]+~[0-9]+초[^\]]*\]', '', line)
        line = re.sub(r'\*\*[0-9]+:[0-9]+[^*]*\*\*', '', line)
        line = re.sub(r'\(1초 컷 1으로 무한 연결\)', '', line)
        line = re.sub(r'<run_command>[\s\S]*?<\/run_command>', '', line)
        
        line = line.strip()
        if line and len(line) > 3:
            clean_lines.append(line)
            
    return " ".join(clean_lines)

async def generate_voice_async(text: str, output_path: str, voice: str = DEFAULT_VOICE, rate: str = "+0%", pitch: str = "+0Hz"):
    import edge_tts
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_path)

def generate_voice(script_input: str, voice_name: str = DEFAULT_VOICE, output_name: str = None):
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    # 입력이 파일 경로인 경우
    if os.path.isfile(script_input):
        with open(script_input, "r", encoding="utf-8", errors="ignore") as f:
            raw_text = f.read()
        base_name = os.path.splitext(os.path.basename(script_input))[0]
    else:
        # 파일이 아니라 제목이나 텍스트 자체인 경우
        possible_file = os.path.join(SCRIPTS_DIR, f"{script_input}.md")
        if os.path.exists(possible_file):
            with open(possible_file, "r", encoding="utf-8", errors="ignore") as f:
                raw_text = f.read()
            base_name = script_input
        else:
            raw_text = script_input
            base_name = "나레이션_" + datetime.now().strftime("%Y%m%d_%H%M%S")
            
    # 나레이션 순수 텍스트 정제
    spoken_text = clean_script_for_tts(raw_text)
    if not spoken_text:
        spoken_text = "1997년 11월 20일 자정, 대한민국 경제가 무너지기 딱 24시간 전. 역사는 이미 조작되었습니다."
        
    print(f"[*] 🎙️ 정제된 성우 낭독 텍스트 ({len(spoken_text)}자):")
    print(f"    \"{spoken_text[:120]}...\"")
    
    if not output_name:
        output_name = f"{base_name}_성우음성.mp3"
    elif not output_name.endswith(".mp3"):
        output_name += ".mp3"
        
    output_path = os.path.join(AUDIO_DIR, output_name)
    print(f"[*] 🚀 Microsoft 뉴럴 성우 엔진({voice_name}) 합성 시작...")
    
    asyncio.run(generate_voice_async(spoken_text, output_path, voice=voice_name))
    
    file_size = os.path.getsize(output_path)
    print(f"[+] ✅ 고품질 성우 MP3 파일 안착 성공: {output_path} ({file_size:,} bytes)")
    return output_path

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hookverse $0 Neural Voice Generator (edge-tts)")
    parser.add_argument("script", nargs="?", default="IMF2화_자정의중앙 금융 금고_30초대본")
    parser.add_argument("--voice", "-v", choices=["sunhi", "injoon", "hyunsu"], default="sunhi")
    parser.add_argument("--output", "-o", default=None)
    args = parser.parse_args()
    
    voice_map = {
        "sunhi": DEFAULT_VOICE,
        "injoon": MALE_VOICE,
        "hyunsu": "ko-KR-HyunsuMultilingualNeural"
    }
    selected_voice = voice_map.get(args.voice, DEFAULT_VOICE)
    
    # 기본 파일 탐색
    target = args.script
    if not os.path.exists(target):
        candidate = os.path.join(SCRIPTS_DIR, f"{target}.md")
        if os.path.exists(candidate):
            target = candidate
        else:
            candidate2 = os.path.join(SCRIPTS_DIR, "IMF2화_자정의중앙 금융 금고_30초대본.md")
            if os.path.exists(candidate2):
                target = candidate2
                
    generate_voice(target, voice_name=selected_voice, output_name=args.output)
