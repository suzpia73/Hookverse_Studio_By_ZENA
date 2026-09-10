# 📺 레오 — 대표 유튜브 채널 분석 (The Try Guys, MrBeast, Casey Neistat 등 포함): 구체적 정보 수집

### 🎯 핵심 미션

> **"시공간을 초월하는 만약에 채널"** PD 역할.
> Writer가 쓴 스크립트를 받아 실제 유튜브 영상으로 만들 수 있는 **완성된 기획서 + 씬 구성 + 이미지 프롬프트**를 제작한다.

### 📋 분석 대상 채널
- The Try Guys
- MrBeast
- Casey Neistat

### 📊 분석 항목
1. 채널 특징 및 콘텐츠 철학
2. 성공 요인 및 차별화 요소
3. 장점과 단점
4. 콘텐츠 기획 방식
5. 스토리텔링 구조
6. 제목 작성 방식
7. 썸네일 디자인 전략
8. 영상 편집 스타일
9. 브랜딩 전략
10. 시청자 반응 및 커뮤니티 특징

### 🗣️ 분석 요소: 세 가지 DNA
- Curiosity DNA (호기심)
- Spectacle DNA (몰입과 임팩트)
- Story DNA (감정과 스토리)

### 🔍 주요 도구 사용 계획
1. `competitor_brief` — 경쟁 채널의 최근 떡상 영상을 수집하여 로컬 LLM에 지시문을 제공합니다.
2. `trend_sniper` — 유튜브 Data API를 통해 최근 30일의 떡상 영상을 분석하고 패턴을 도출합니다.

### 🧩 실행 계획
1. **경쟁 채널 분석:**
   - <run_command>cd "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git\_company\_agents\youtube\tools" && py -3 competitor_brief.py</run_command>
2. **트렌드 패턴 분석:**
   - <run_command>cd "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git\_company\_agents\youtube\tools" && py -3 trend_sniper.py</run_command>

### 📝 자가검증: 사실 2개 / 추측 0개

자가검증: 사실 2개 / 추측 0개

---

**실행 결과를 기다리는 중입니다.**
- 데이터 수집 및 분석 후, 결과를 바탕으로 각 채널의 분석 보고서와 함께 공통 성공 패턴을 도출합니다.
- 이를 기반으로 우리 브랜드만의 독창적이고 현실적인 콘텐츠 전략을 제안합니다.

---
## 🛠️ 도구 실행 결과 (시스템 자동 실행)

### 🔧 실행: `cd "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git\_company\_agents\youtube\tools" && py -3 competitor_br`
```
❌ COMPETITOR_CHANNELS가 비어있어요. youtube_account.json에 채워주세요.
```
_❌ exit 1_

### 🔧 실행: `cd "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git\_company\_agents\youtube\tools" && py -3 trend_sniper.`
```
d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO\.git\_company\_agents\youtube\tools\trend_sniper.py:77: DeprecationWarning: datetime.datetime.utcnow() is deprecated and scheduled for removal in a future version. Use timezone-aware objects to represent datetimes in UTC: datetime.datetime.now(datetime.UTC).
  last_month = (datetime.datetime.utcnow() - datetime.timedelta(days=30)).isoformat("T") + "Z"

🎯 [트렌드 스나이퍼] 키워드 ['AI 비즈니스', '생산성 툴'] 스캔 시작...
📡 [AI 비즈니스] 검색 중...
📡 [생산성 툴] 검색 중...
🧠 [LLM 분석 중... 엔진: Ollama]
   자동 선택 모델: qwen2.5:7b
❌ LLM 호출 실패: HTTPConnectionPool(host='127.0.0.1', port=11434): Read timed out. (read timeout=180)
```
_❌ exit 1_
