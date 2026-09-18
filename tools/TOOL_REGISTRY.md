# 🛠️ Hookverse Studio 도구 레지스트리 & 전사 파이프라인 지도 (v2.0)

> **관리 주체**: KAIRA 부회장 제나 (ZENA) & CEO 레오  
> **목적**: 40여 개 스크립트의 역할 및 실행 순서를 100% 명확히 정의하여 중복·혼선 방지.

---

## 🌟 1. 실전 필수 1군 코어 엔진 (Daily Production Suite)

이 도구들은 실제 유튜브 숏폼/롱폼 제작 시 매일 가동되는 핵심 엔진입니다:

| 스크립트 명 | 역할 및 담당 에이전트 | 입력 / 의존성 | 최종 산출물 |
| :--- | :--- | :--- | :--- |
| **`run_master_production.bat`** | **[원클릭 통합 마스터 실행기]** (오빠/제나 실행용) | Python 3.14, FFmpeg | 마스터 비디오 + 4컷 검증 스냅샷 일괄 렌더링 |
| **`standard_cinema_engine.py`** | **[공식 시네마틱 렌더링 엔진]** (편집감독 빅터) | 4컷 이미지 + 성우 음성 | 30초 1080x1920 최종 완제품 비디오 (`.mp4`) |
| **`studio_orchestrator.py`** | **[10대 에이전트 자율 오케스트레이터]** (CEO 레오) | Gemini API, ACCG v2.1 헌법 | 대본 ➡️ 프롬프트 ➡️ 음성 ➡️ 비디오 풀 릴레이 |
| **`opal_visual_pipeline_node.py`**| **[비주얼 노드 & ACCG 감사 게이트]** (아트 카이) | `_rules/visual_continuity_rules.json` | G3 2중 앵커 검증 및 무결점 프롬프트 매니페스트 |
| **`generate_ep02_audio.py`** | **[손서현 성우 나레이션 전용 생성기]** (사운드 소울) | 대본 텍스트 (`assets/scripts/`) | 고음질 나레이션 (`assets/audio/*.mp3`) |
| **`trend_intelligence.py`** | **[크로스 플랫폼 트렌드 레이더 v3.0]** (리서처 레이) | Google Trends, YouTube RSS | 4대 카테고리 100만 뷰 킬러 소재 기획안 |
| **`legal_guardrail.py`** | **[법적 무결점 가드레일 엔진]** (법률자문 에이전트) | 대본 및 이미지 메타데이터 | 초상권/저작권 0% 리스크 통과 필증 |
| **`youtube_studio_uploader.py`** | **[유튜브 스튜디오 99% 사전 세팅기]** (운영팀) | 마스터 비디오 + 태그/제목 | 브라우저 자동 업로드 (오빠는 최종 [게시]만) |
| **`motion_video_generator.py`** | **[시네마틱 모션 비디오 생성기]** (비주얼 디렉터) | 정지 이미지 4컷 | 살아 숨 쉬는 모션 비디오 클립 (`.mp4`) |

---

## 📦 2. 서브 브리지 및 유틸리티 도구 (2군 지원 엔진)

| 스크립트 명 | 역할 | 상태 |
| :--- | :--- | :--- |
| `capcut_draft_generator.py` | 캡컷 PC 드래프트 프로젝트 자동 조립 | 정상 (CapCut 연동 시 사용) |
| `capcut_vrew_bridge.py` | 캡컷 ↔ Vrew XML/타임라인 연동 브리지 | 정상 |
| `viral_script_ingest.py` | 바이럴 대본 수집 및 구조화 인제스트 | 정상 |
| `create_badge.py` / `create_badge_vrew.py` | 상단 로열블루 브루 배지 생성기 | 완료 (기존 에셋 보존) |
| `create_true_transparent_logo.py` | 투명 누끼 골든 릴 엠블럼 생성기 | 완료 (기존 에셋 보존) |

---

## 🏛️ 3. 연구·검증 완료 아카이브 (Historical R&D Archive)
*아래 도구들은 개발 및 튜닝 단계에서 1:1 완벽 복제(자막 바운스, 엠블럼 스윙, 폰트 분석 등)를 위해 사용되었으며, **모든 로직이 이미 `standard_cinema_engine.py`에 완전 흡수**되었습니다:*

- **Vrew 자막/모션 정밀 분석**: `analyze_subtitle_color.py`, `analyze_vrew_capture.py`, `crop_sub.py`, `measure_exact_vrew.py`, `parse_vrew.py`, `test_sub_motion.py`, `test_purple_drop.py`
- **엠블럼 스윙 물리 각도 검증**: `extract_swing_snaps.py`, `test_swing_motion.py`
- **교보손글씨 폰트 수집 및 글리프 파싱**: `parse_kyobo.py`, `inspect_letters.py`, `convert_woff_to_ttf.py`, `woff_to_ttf.py`, `fetch_kyobo_ttf.py`
- **단발성 파이프라인 테스트**: `assemble_ep02_4cuts.py`, `deploy_new_cuts.py`, `perfect_cuts_and_render.py`, `render_cinema_ep02.py`
