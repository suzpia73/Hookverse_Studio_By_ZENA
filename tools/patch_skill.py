import os

skill_path = r"C:\Users\june2\.gemini\config\skills\hookverse_system\SKILL.md"
with open(skill_path, 'r', encoding='utf-8') as f:
    content = f.read()

target = "## Ⅵ. 부회장 제나의 영구 실천 맹세"
sec44 = """### [섹션 44] Vrew 4.6.0 라이브 브라우저 실전 습득 및 10대 에이전트 훈련 교본 표준화 (2026-09-17)

1. **오빠의 절대 훈시**:
   - "제나가 툴을 사용할 줄 알아야 에이전트 쟤네들을 학습시키고 완벽한 무인 자동화를 이룰 수 있다!"
2. **실전 브라우저 침투 및 검증 내역**:
   - `https://vrew.ai/ko/try/index.html` 직통 침투, 좌측 프리뷰 재생 버튼(Space)으로 실시간 프리뷰 렌더링 검증 완료.
   - [서식], [효과], [삽입], [AI 목소리], [템플릿], [도움말], [내보내기] 전 탭의 DOM/UI 인터랙션 완료.
   - 내보내기 모달에서 MP4 FHD(1080x1920), 최고화질, GPU 가속 활성화 파라미터 전수 확인.
   - 실전 비디오 기록: `vrew_tool_learning_1789631026038.webp` 보존.
3. **에이전트 훈련 교본 영구 박제**:
   - `_company/00_Raw/vrew_captures/Vrew_4.6.0_마스터운용_및_에이전트_훈련교본.md` 완비.
   - `standard_cinema_engine.py`에 교보손글씨(88~92pt), 네온퍼플(5.2px), Y=1380 파도낙하, 그네타기(2.0s 진자) 수치를 1:1 완벽 내재화하여 10대 에이전트 파이프라인과 직결.

---

"""

if target in content and "[섹션 44]" not in content:
    content = content.replace(target, sec44 + target)
    with open(skill_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("SUCCESS")
else:
    print("SKIPPED")
