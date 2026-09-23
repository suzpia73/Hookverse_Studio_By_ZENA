# ✂️ 편집자 전문 스킬: 모션 비디오 카메라 무빙 & 캡컷 키프레임 연출법

## 1. 개요
편집자(Editor)는 정지된 스틸컷을 살아 숨 쉬는 숏폼 완제품으로 벼려내는 시네마토그래퍼다. AI 비디오 프롬프트 파이프라인과 캡컷/Vrew 편집 레일에서 카메라 줌인, 줌아웃, 틸트, 패닝을 키프레임과 모션으로 직접 구현한다.

---

## 2. 캡컷(CapCut) 키프레임 카메라 연출 공식
정지 스틸컷이나 AI 비디오 클립을 배치할 때, 단 1초도 정지된 상태로 두지 않는다 (미스터비스트 0초 룰):

1. **임팩트 줌인 (Crash Zoom-In / Push-in)**:
   - 시작점(0.0s) Scale: 100% ➡️ 종료점(2.5s) Scale: 125% (인물 얼굴 또는 핵심 소품 중심으로 키프레임 확대).
   - 반전 순간: 0.2초 만에 Scale 100% ➡️ 135%로 급격한 크래시 줌.
2. **고립 줌아웃 (Pull-Back / Zoom-out)**:
   - 시작점 Scale: 120% ➡️ 종료점 Scale: 100% (점점 프레임이 넓어지며 빗속 골목에 포위된 사냥꾼들의 실루엣이 드러남).
3. **다이내믹 패닝 & 셰이크 (Dynamic Pan & Shake)**:
   - 도주/질주 씬(Cut 02, Cut 03)에서 X축 이동 키프레임(-50px ➡️ +50px)과 미세한 카메라 흔들림(Camera Shake 3~5%)을 주어 현장감 극대화.
4. **버티고 효과 (Dolly Zoom / Vertigo Effect)**:
   - 전경의 뉴라는 일정한 크기를 유지하면서 배경이 급격히 확장/축소되는 렌즈 왜곡 연출로 충격 극대화.

---

## 3. AI 비디오 엔진(Omni 1.1 / Veo) 연동 모션 파라미터 매핑
- `tools/veo_omni_pipeline.py` 및 `tools/motion_video_generator.py` 호출 시:
  * Cut 01: `motion_type="slow_tilt_down_and_zoom_out"`
  * Cut 02: `motion_type="fast_corner_tracking_pan"`
  * Cut 03: `motion_type="forward_rush_into_phonebooth"`
  * Cut 04: `motion_type="macro_crash_zoom_on_shocked_eyes"`
