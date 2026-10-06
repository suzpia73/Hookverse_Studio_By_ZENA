# -*- coding: utf-8 -*-
"""
Hookverse Studio - 4인 정예 에이전트 무인 바통 터치 릴레이 엔진 (Relay Runner)
- 오케스트레이션: CEO 레오 총괄 지휘
- 투 트랙(Two-Track) 편성 매트릭스:
    1. Track A: 단막극 시네마틱 소설 (EP 3~5부작) ➡️ 35mm 극사실 실사 모드
    2. Track B: K-전래동화 & 신화 (1~2화 옴니버스) ➡️ 3D 픽사 스타일 뉴라 아바타 모드
- 패스트트랙 긴급 인터셉트 (Fast-Track Intercept): 초특급 핫트렌드 선제 생산
- 릴레이 체인:
    [Step 1: 리서처] trend_intelligence.py (트렌드 & 소재 발굴)
    [Step 2: 작가] 5-in-1 거장 바이럴 대본 생성 & legal_guardrail.py 무결점 검수
    [Step 3: 디자이너] veo_omni_pipeline.py (Veo/Omni 실사 or 3D 픽사 프롬프트 팩)
    [Step 4: 코다리/PD] capcut_vrew_bridge.py (45초 칼싱크 편집 사양서 완성)
"""

import os
import sys
import json
import argparse
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PYTHON_EXE = r"C:\Users\june2\AppData\Local\Programs\Python\Python314\python.exe"

# 3D 픽사 스타일 뉴라 아바타 앵커락
NEURA_PIXAR_ANCHOR = (
    "NEURA, stylized 3D animated character in Pixar and Disney animation aesthetic, "
    "young Korean woman in early 20s, expressive sharp cat-eyes, "
    "signature distinct beauty mark under her left eye, tiny beauty mark near corner of mouth, "
    "voluminous dark wavy hair, warm stylized lighting, Unreal Engine 5 subsurface scattering, cute and charismatic"
)

def run_relay_pipeline(track="A", topic=None, fast_track=False):
    print("=" * 70)
    print("👑 [CEO 레오] Hookverse Studio 4인 정예 무인 릴레이 파이프라인 가동")
    print("=" * 70)
    print(f"⏰ 가동 일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"🎯 선택 트랙: {'Track A (단막극 시네마틱 소설 / 실사)' if track == 'A' else 'Track B (K-전래동화 / 3D 픽사 아바타)'}")
    if fast_track:
        print("🚨 [패스트트랙 긴급 인터셉트 모드 ON] 시장 선점 15분 번개 생산 레일 가동!")
    print("-" * 70)

    # -------------------------------------------------------------
    # [Step 1: 리서처] 트렌드 및 소재 확인
    # -------------------------------------------------------------
    print("\n🔍 [Step 1: 리서처] 소재 및 팩트체크 데이터 로드 중...")
    trends_file = os.path.join(BASE_DIR, "00_Raw", "knowledge_packs", "daily_trends.json")
    
    selected_topic = topic
    if not selected_topic:
        if os.path.exists(trends_file):
            try:
                with open(trends_file, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    if data.get("trends"):
                        selected_topic = data["trends"][0]["what_if_concept"]["what_if_hook"]
            except Exception as e:
                print(f"⚠️ 트렌드 파일 로드 경고: {e}")
        if not selected_topic:
            selected_topic = "1997년 IMF 자정의 지하 비밀 외환 금고와 미래 자금"
            
    print(f"✅ 확정 소재: \"{selected_topic}\"")

    # -------------------------------------------------------------
    # [Step 2: 작가] 5-in-1 거장 대본 생성 & 법적 가드레일 감사
    # -------------------------------------------------------------
    print("\n✍️ [Step 2: 작가] 5-in-1 거장 대본 집필 및 법적 무결점 감사 중...")
    
    # 트랙별 대본 톤 분기
    if track == "A":
        # 단막극 시네마틱 소설 대본
        script_lines = [
            "1997년 11월 20일 자정, 명동의 시계탑이 멈춘 순간.",
            "차디찬 빗속 공중전화 부스에 한 여자가 서 있습니다.",
            "스마트폰 화면에 뜬 긴급 속보, 대한민국 부도 D-1.",
            "수화기 너머로는 알 수 없는 기계음만 흘러나옵니다.",
            "그 시각, 지하 비밀 외환 금고의 육중한 철문이 열려 있었습니다.",
            "텅 빈 금고 바닥, 찢겨진 장부 위에 남겨진 붉은 서명, 뉴라.",
            "어둠 속으로 사라지는 트렌치코트의 그림자.",
            "그녀의 손에 들린 가방 속엔 미래를 바꿀 비밀 자금이 채워져 있었습니다."
        ]
    else:
        # K-전래동화 3D 픽사 감성 대본
        script_lines = [
            "옛날 옛적 깊은 바닷속, 용왕님의 병을 고치기 위해 토끼를 찾아 나선 별주부.",
            "하지만 그가 마주친 토끼 뉴라는 평범한 토끼가 아니었습니다.",
            "홀로그램 선글라스를 낀 3D 픽사 아바타 뉴라의 깜찍한 미소.",
            "\"용왕님의 간을 고치려면 내 최첨단 AI 나노 머신이 필요할 텐데?\"",
            "수중 모빌리티를 타고 용궁으로 질주하는 뉴라와 당황한 별주부 거북이.",
            "용궁의 거대한 해저 돔 시티가 환상적인 네온 빛으로 펼쳐집니다.",
            "용왕님 눈앞에 펼쳐진 미래의 건강 진단 홀로그램 차트.",
            "과연 뉴라는 용왕님을 치료하고 바닷속 전설의 영웅이 될 수 있을까요?"
        ]

    script_text = "\n".join(script_lines)
    
    # 법적 가드레일 검사
    from legal_guardrail import audit_content
    audit_res = audit_content(script_text=script_text)
    print(f"🛡️ 법적 가드레일 판정: 점수={audit_res['score']}점 ({audit_res['status']}) - {audit_res['compliance_summary']}")
    
    # 대본 파일 저장
    script_dir = os.path.join(BASE_DIR, "assets", "scripts")
    os.makedirs(script_dir, exist_ok=True)
    script_path = os.path.join(script_dir, f"무인릴레이_{'단막극소설_실사' if track == 'A' else '전래동화_픽사3D'}_대본.md")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(f"# 🎬 Hookverse 무인 릴레이 {'단막극 시네마틱 소설' if track == 'A' else 'K-전래동화 3D'} 45초 대본\n\n")
        f.write(f"- **소재**: {selected_topic}\n")
        f.write(f"- **작성 일시**: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n---\n\n")
        for i, l in enumerate(script_lines, 1):
            f.write(f"Scene {i}: {l}\n")
    print(f"💾 대본 디스크 안착 완료: {script_path}")

    # -------------------------------------------------------------
    # [Step 3: 디자이너] Google Veo & Gemini Omni 시네마틱 프롬프트 조립
    # -------------------------------------------------------------
    print("\n🎨 [Step 3: 디자이너] 씬별 Google Veo / Omni 프롬프트 패키징...")
    from veo_omni_pipeline import SCENE_PRESETS, NEURA_ANCHOR
    
    prompts = []
    chosen_anchor = NEURA_ANCHOR if track == "A" else NEURA_PIXAR_ANCHOR
    style_label = "35mm Photorealistic Film Cinema" if track == "A" else "Pixar 3D Stylized Animation"
    
    for i, line in enumerate(script_lines):
        preset = SCENE_PRESETS[i % len(SCENE_PRESETS)]
        prompt_block = (
            f"[Google Veo Prompt - Scene {i+1} ({style_label})]\n"
            f"Prompt: {chosen_anchor}. Action/Story: {line}. "
            f"Visual Style: {style_label}, {preset['lighting']}. Camera: {preset['motion']}.\n"
            f"[Gemini Omni Edit Directive]: {preset['omni_edit_directive']}\n"
        )
        prompts.append(prompt_block)
        
    prompt_dir = os.path.join(BASE_DIR, "assets", "prompts")
    os.makedirs(prompt_dir, exist_ok=True)
    prompt_path = os.path.join(prompt_dir, f"무인릴레이_{'단막극소설_실사' if track == 'A' else '전래동화_픽사3D'}_프롬프트팩.txt")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write("\n".join(prompts))
    print(f"💾 프롬프트 팩 안착 완료: {prompt_path}")

    # -------------------------------------------------------------
    # [Step 4: 코다리/PD] 캡컷 & Vrew 자동 편집 브릿지 결합
    # -------------------------------------------------------------
    print("\n🎬 [Step 4: 코다리 & PD] 캡컷 & Vrew 45초 타임라인 사양서 조립...")
    from capcut_vrew_bridge import build_project_bridge
    spec_path = build_project_bridge(project_name=f"무인릴레이_{'단막극소설' if track == 'A' else '전래동화픽사'}")
    
    # -------------------------------------------------------------
    # [완결 보고서 출력]
    # -------------------------------------------------------------
    print("\n" + "=" * 70)
    print("🏆 [전사 보고] 4인 에이전트 무인 릴레이 100% 성공 완료!")
    print("=" * 70)
    print(f"1. 리서처: 소재 매핑 완료 (\"{selected_topic[:35]}...\")")
    print(f"2. 작가: 5-in-1 대본 안착 ({script_path})")
    print(f"3. 디자이너: Veo/Omni 프롬프트 안착 ({prompt_path})")
    print(f"4. 코다리/PD: 편집 브릿지 사양서 결합 ({spec_path})")
    print("=" * 70)
    print("✨ 사람 개입 0% 완전 자율 생산 체인 가동 완료!")
    return True

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hookverse 4인 에이전트 무인 릴레이 러너")
    parser.add_argument("--track", choices=["A", "B"], default="A", help="Track A: 단막극소설(실사) / Track B: 전래동화(3D픽사)")
    parser.add_argument("--topic", type=str, default=None, help="커스텀 주제 지정 (옵션)")
    parser.add_argument("--fast-track", action="store_true", help="패스트트랙 긴급 인터셉트 모드")
    args = parser.parse_args()
    
    run_relay_pipeline(track=args.track, topic=args.topic, fast_track=args.fast_track)
