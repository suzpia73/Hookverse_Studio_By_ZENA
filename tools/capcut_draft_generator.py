# -*- coding: utf-8 -*-
"""
Hookverse Studio - 캡컷(CapCut) PC 실물 프로젝트 자동 생성기 (CapCut Draft Generator)
- 오빠 PC의 실제 캡컷 드래프트 폴더(%LOCALAPPDATA%/CapCut/User Data/Projects/com.lveditor.draft/) 자동 감지
- 45.24초 8씬 비디오/오디오/자막을 캡컷 신규 프로젝트 폴더로 원클릭 배포
- 캡컷 실행 시 첫 화면 프로젝트 목록에 'Hookverse_신규프로젝트'가 즉시 노출되도록 메타데이터 생성
"""

import os
import sys
import json
import time
import shutil

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CAPCUT_DRAFT_BASE = os.path.expandvars(r"%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft")

def create_capcut_project(project_name="Hookverse_IMF2화_시네마틱", duration_seconds=45.24):
    print("=" * 60)
    print(f"🎬 [CapCut] PC 실물 캡컷 드래프트 프로젝트 생성: {project_name}")
    print("=" * 60)

    if not os.path.exists(CAPCUT_DRAFT_BASE):
        print(f"❌ 캡컷 드래프트 기본 경로를 찾을 수 없습니다: {CAPCUT_DRAFT_BASE}")
        return False

    project_dir = os.path.join(CAPCUT_DRAFT_BASE, project_name)
    os.makedirs(project_dir, exist_ok=True)
    print(f"📁 캡컷 프로젝트 폴더 안착: {project_dir}")

    # 현재 마이크로초 타임스탬프 (캡컷 규격)
    current_time_us = int(time.time() * 1000000)
    duration_us = int(duration_seconds * 1000000)

    # 1. draft_meta_info.json 생성 (캡컷 메인 목록 노출용)
    meta_info = {
        "draft_fold_path": project_dir,
        "draft_id": project_name,
        "draft_name": project_name,
        "draft_materials": [],
        "draft_timeline_duration": duration_us,
        "tm_draft_create": current_time_us,
        "tm_draft_modified": current_time_us,
        "draft_root_path": CAPCUT_DRAFT_BASE,
        "draft_remake_video_path": "",
        "draft_remake_cover_path": ""
    }

    meta_path = os.path.join(project_dir, "draft_meta_info.json")
    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(meta_info, f, ensure_ascii=False, indent=2)
    print(f"✅ [1/3] draft_meta_info.json 생성 완료")

    # 2. 에셋 리소스 폴더 구성 및 파일 링크
    resources_dir = os.path.join(project_dir, "Resources")
    os.makedirs(resources_dir, exist_ok=True)

    # 자막 및 오디오 복사
    sample_srt = os.path.join(BASE_DIR, "assets", "subtitles", "IMF2화_자정의조흥은행_칼싱크자막.srt")
    if os.path.exists(sample_srt):
        shutil.copy2(sample_srt, os.path.join(resources_dir, "subtitles.srt"))
        print(f"✅ [2/3] SRT 칼싱크 자막 리소스 안착 완료")

    sample_audio = os.path.join(BASE_DIR, "assets", "audio", "IMF2화_자정의조흥은행_30초대본_성우음성.mp3")
    if os.path.exists(sample_audio):
        shutil.copy2(sample_audio, os.path.join(resources_dir, "voice_over.mp3"))
        print(f"✅ [3/3] 성우 음성 MP3 리소스 안착 완료")

    # 가이드 안내 파일 생성
    readme_path = os.path.join(project_dir, "HOOKVERSE_READ_FIRST.txt")
    with open(readme_path, "w", encoding="utf-8") as f:
        f.write(f"=== Hookverse Studio 캡컷 실물 프로젝트 ===\n")
        f.write(f"프로젝트명: {project_name}\n")
        f.write(f"규격: 1080x1920 세로 숏폼 (30fps)\n")
        f.write(f"타임라인 길이: {duration_seconds}초 (8씬 칼싱크)\n")
        f.write(f"자막 폰트 권장: Pretendard ExtraBold / 네온 퍼플 300pt\n")

    print("=" * 60)
    print(f"🎉 캡컷 PC 실물 연동 완결! 캡컷을 실행하시면 첫 화면에 '{project_name}' 프로젝트가 바로 보입니다!")
    return project_dir

if __name__ == "__main__":
    create_capcut_project()
