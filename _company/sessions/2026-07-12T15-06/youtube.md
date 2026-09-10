# 📺 레오 — 구체적이고 실행 가능한 한국어 지시

### [2026-06-01] 핵심 미션 및 작업 분배 보고 (핵심 콘텐츠 패턴 및 수익화 모델 정량적 분석과 5부작 시리즈 구조 설계)

**레오 PD에게 주어진 핵심 미션:**
- **"시공간을 초월하는 만약에 채널"** PD 역할.
- 완성된 기획서 + 씬 구성 + 이미지 프롬프트를 제작.

**작업 분배 보고:**

1. **기존 데이터 검토:**
   - `_company/_agents/researcher/tools/web_search_report.md` 파일을 먼저 검토하여 트렌드 데이터가 있는지 확인합니다.
   - 이 파일이 없거나 24시간 초과일 경우, "트렌드 데이터 없음, Researcher에게 요청 필요"를 보고합니다.

2. **채널 비주얼 아이덴티티 적용:**
   - 색감: 다크 + 네온 (우주·미래 느낌)
   - 폰트 스타일: 굵고 강렬 (Pretendard ExtraBold 계열)
   - 썸네일 공식: 충격적 이미지 + 큰 숫자 or 의문문
   - BGM 무드: 웅장한 오케스트라 / 신비로운 ambient / 긴장감 있는 전자음악

3. **기획서 작성 형식 준수:**
   - **영상 기획서 — [제목]**
     - 날짜: YYYY-MM-DD
     - 트렌드 기반: ✅ `web_search_report.md` 참조
     - 기본 정보:
       - 제목 (A안): 
       - 제목 (B안): 
       - 형식: 쇼츠(60초) / 롱폼(10분)
       - 타깃: 
     - 후크 (첫 5초):
       - 화면: [어떤 이미지/영상]
       - 나레이션: "... "
       - 효과: [BGM / 사운드이펙트]
     - 씬 구성:
       | 씬 | 시간 | 나레이션 | 이미지 프롬프트(AI생성용) | BGM분위기 |
       |---|---|---|---|---|
     - 썸네일 브리프:
       - 배경: 
       - 메인 이미지: 
       - 텍스트: 
       - 색감: 
     - 쇼츠 버전 (롱폼이면 별도 작성):
       - 후크: 
       - 핵심 장면 3개:
       - CTA:
     - 업로드 메타데이터:
       - 제목:
       - 설명 (첫 3줄):
       - 태그 15개:
       - 예약 시간:

4. **실시간 데이터 확인 및 수집:**
   - `trend_sniper` 도구를 실행하여 최근 떡상 영상을 분석하고, 다음 기획안을 도출합니다.
   - `<run_command>cd "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git_company_agents\youtube\tools" && py -3 trend_sniper.py</run_command>`

5. **예산 및 수익화 모델 분석:**
   - `YouTube 채널 성장 전략`을 검토하여 현재의 트렌드와 매출 비율, 시청자 데이터를 분석합니다.
   - `my_videos_check` 도구를 실행하여 최근 영상의 성과를 평가하고, 다음 기획안을 수립합니다.
   - `<run_command>cd "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git_company_agents\youtube\tools" && py -3 my_videos_check.py</run_command>`

6. **5부작 시리즈 구조 설계:**
   - `trend_sniper` 도구를 통해 얻은 데이터와 `web_search_report.md` 기반 트렌드 정보를 활용하여 5부작 시리즈의 구조를 설계합니다.

### 자가검증

- **사실 N개 / 추측 M개**: 

정보 부족 — 두뇌 폴더에 X 자료 필요

---

이러한 작업을 통해 `시공간을 초월하는 만약에 채널`의 향후 성장을 위한 구체적인 기획서와 시리즈 구조를 설계하게 됩니다. 이 과정에서 실시간 데이터 및 트렌드 분석을 통해 최적의 콘텐츠 전략을 수립할 예정입니다.

---

### 다음 단계: 

- `trend_sniper` 도구 실행 후 결과 확인
- `my_videos_check` 도구 실행 후 결과 확인
- 5부작 시리즈 구조 설계 시작

다음 단계는 `trend_sniper` 및 `my_videos_check` 도구를 통해 얻은 데이터를 바탕으로 5부작 시리즈의 구조를 설계합니다.

---

**마지막으로, CEO에게 보고:**
- 트렌드 분석 결과
- 예상 매출과 시청자 증대 계획
- 5부작 시리즈 제안

---
## 🛠️ 도구 실행 결과 (시스템 자동 실행)

### 🔧 실행: `cd "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git_company_agents\youtube\tools" && py -3 trend_sniper.py`
```
The system cannot find the path specified.
```
_❌ exit 1_

### 🔧 실행: `cd "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git_company_agents\youtube\tools" && py -3 my_videos_check`
```
The system cannot find the path specified.
```
_❌ exit 1_
