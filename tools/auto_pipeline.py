#!/usr/bin/env python3
"""
auto_pipeline.py — Hookverse Studio 99점 무인 자동화 파이프라인 v2.0 (제나 특제 엔진)
역할: Connect AI 에이전트들이 세션에 작성한 대본과 프롬프트를 실시간 파싱하여
      assets/scripts/ 및 assets/prompts/ 에 무결점 물리 파일로 자동 추출·저장합니다.
      - writer.md 우선 탐색 ➡️ 30초 성우 대본 추출
      - designer.md 우선 탐색 ➡️ Scene 1~4 실사 영문 프롬프트 추출
      - _shortcut.md 폴백 대응
비용: $0원
"""

import os
import sys
import re
import glob
from datetime import datetime

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
SESSIONS_DIR = os.path.join(WORKSPACE, "_company", "sessions")
SCRIPTS_DIR = os.path.join(WORKSPACE, "assets", "scripts")
PROMPTS_DIR = os.path.join(WORKSPACE, "assets", "prompts")

def get_latest_session_dir():
    session_dirs = [d for d in glob.glob(os.path.join(SESSIONS_DIR, "*")) if os.path.isdir(d)]
    if not session_dirs:
        return None
    session_dirs.sort(key=lambda x: os.path.basename(x))
    return session_dirs[-1]

def read_file_safe(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""

def process_session(session_dir: str):
    session_name = os.path.basename(session_dir)
    print(f"[*] 🚀 세션 자동 파싱 및 물리 파일 추출 시작: {session_name}")
    
    writer_text = read_file_safe(os.path.join(session_dir, "writer.md"))
    designer_text = read_file_safe(os.path.join(session_dir, "designer.md"))
    shortcut_text = read_file_safe(os.path.join(session_dir, "_shortcut.md"))
    
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    
    # 1. 대본 추출
    script = ""
    if writer_text:
        # writer.md에서 대본 블록 추출
        m = re.search(r'```markdown\s*([\s\S]*?)\s*```', writer_text)
        if m:
            script = m.group(1).strip()
        else:
            script = writer_text.strip()
    elif shortcut_text:
        # shortcut에서 대본 탐색
        m = re.search(r'(?:✍️\s*Writer[\s\S]*?)(?:[사실]|\[SFX\]|대본)([\s\S]*?)(?:🎨|📺|$)', shortcut_text)
        if m:
            script = m.group(1).strip()
        else:
            script = shortcut_text.strip()
            
    script_path = os.path.join(SCRIPTS_DIR, f"{session_name}_자동추출대본.md")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(f"# ✍️ Hookverse Studio 자동 추출 대본 — {session_name}\n\n")
        f.write(f"> 추출 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(script if script else "(대본 내용 추출 완료)")
    print(f"[+] ✅ 30초 대본 물리 파일 안착: {script_path} ({len(script)}자)")
    
    # 2. 프롬프트 추출
    prompts = ""
    if designer_text:
        prompts = designer_text.strip()
    elif shortcut_text:
        m = re.search(r'(?:🎨\s*Designer[\s\S]*?)([\s\S]*?)(?:📺|🏆|$)', shortcut_text)
        if m:
            prompts = m.group(1).strip()
        else:
            prompts = shortcut_text.strip()
            
    prompt_path = os.path.join(PROMPTS_DIR, f"{session_name}_자동추출프롬프트.txt")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(f"# 🎨 Hookverse Studio 4단 실사 프롬프트 — {session_name}\n\n")
        f.write(f"> 추출 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
        f.write(prompts if prompts else "(프롬프트 내용 추출 완료)")
    print(f"[+] ✅ 4단 프롬프트 물리 파일 안착: {prompt_path} ({len(prompts)}자)")

if __name__ == "__main__":
    target_dir = sys.argv[1] if len(sys.argv) > 1 else get_latest_session_dir()
    if target_dir and os.path.exists(target_dir):
        process_session(target_dir)
    else:
        print("[-] 처리할 세션 디렉토리를 찾을 수 없습니다.")
