# 🏛️ HOOKVERSE STUDIO by KAIRA — 올인원 마스터 실행 팩 (Master Suite)

> **문서 목적**: 오빠가 복잡한 기술이나 코드를 외우지 않으셔도, **이 파일 하나만 있으면 어디서든(스마트폰, 다른 PC, 웹 제미나이) 100% 똑같이 전자동으로 콘텐츠가 생산**될 수 있도록 모든 도구, API 연동법, 마스터 프롬프트, 유튜브 세팅값을 총망라한 영구 보관용 마스터 패키지입니다.
> **발행 일시**: 2026-09-16 15:06:31 (제나 관리)

---

## 🌟 [1] 웹 제미나이(Gemini) 직통 복붙용 만능 마스터 프롬프트
> 📌 **사용법**: 스마트폰이나 카페의 다른 PC에서 브라우저를 열고 `gemini.google.com`에 접속한 뒤, 아래 박스 안의 내용을 통째로 복사해서 붙여넣고 맨 아래에 **[원하는 주제]**만 적으시면 끝납니다!

```text
[Hookverse Studio 1인 기업 무인 총괄 시스템 프롬프트]
너는 Hookverse Studio의 버추얼 뮤즈 '뉴라(NEURA)'가 활약하는 5,000년 역사 What-If 타임슬립 시네마틱 숏폼의 전속 총괄 디렉터야.
아래의 4대 사내 헌법을 엄격히 준수하여 결과물을 한 번에 출력해줘.

1. 거장 연출 헌법:
   - 첫 3초 호기심 갭: 상식을 뒤흔드는 충격 가정 ("만약 1997년 IMF 전날 밤...")
   - 시각적 증명: 5초 안에 눈앞에 시각적으로 보여주기
   - 마지막 5초 소름 무한루프: 마지막 대사가 첫 오프닝과 자연스럽게 순환 연결

2. 비주얼 앵커락 (투 트랙 선택):
   [트랙 A: 실사 시네마틱]
   - NEURA, young Korean woman in early 20s, sharp cat-eyes, signature beauty mark under left eye and mouth corner, matte black trench coat, 35mm/85mm Roger Deakins lighting, 8k photorealistic.
   [트랙 B: K-전래동화 3D 픽사]
   - NEURA, stylized 3D animated character in Pixar/Disney animation aesthetic, expressive cat-eyes, signature beauty mark under left eye and mouth corner, cute and charismatic.

3. 법적 무결점: 실존 인물 딥페이크 0%, 70년 이내 보호 IP 도용 0%, 사내 8대 금기어(정치/사회 편향, 클릭베이트) 배제.

[출력 요구 양식]:
1. [8씬 완성형 성우 대본] (45초 칼싱크, 괄호 없는 100% 순수 한국어 나레이션)
2. [8씬 Google Veo / 미드저니 영문 시네마틱 프롬프트 팩]
3. [유튜브 99% 업로드 사전 세팅 팩]:
   - 100만 뷰 바이럴 제목 3선
   - 알고리즘 최적화 설명란 & 타임스탬프
   - SEO 14대 정예 해시태그 및 검색 태그
   - 체크리스트 (아동용 아님, AI 라벨링 체크)

[이번 작업 주제]: 1997년 IMF 자정의 조흥은행 지하 금고와 사라진 달러 가방
```

---

## 🛠️ [2] 외부 툴 & 6대 연동망 핵심 키셋 가이드

| 연동 시스템 | 상태 | 세부 정보 및 용도 |
| :--- | :---: | :--- |
| **Google Gemini API** | ✅ 연동완료 | `gemini-3.6-flash` / `gemini-3.8-flash` 고속 대본 및 프롬프트 생성 두뇌 |
| **YouTube Data API** | ✅ 연동완료 | Hookverse Studio 채널 연동, 메타데이터 조회 및 자동 업로드 배선 |
| **YouTube Analytics** | ✅ 연동완료 | OAuth 자동 갱신 연동 (`1424735...` 공용 키셋), 시청 유지율/트래픽 분석 |
| **Telegram Bot** | ✅ 연동완료 | 오빠 전속 1:1 직통 봇 `@KAIRA_COO_ZENA_BOT` (명령어: `/status`, `/relay`, `/render`) |
| **Google Calendar** | ✅ 연동완료 | `suzpia73@gmail.com` 일정 스케줄러 자동 동기화 |
| **PayPal 결제 모듈** | ✅ 연동완료 | 글로벌 달러 결제 (네온서바이버 $2.99 / 강아지사주 $4.99) 연동 모듈 |

---

## 💻 [3] PC 실물 툴 연동 경로 및 규격

### 1. 캡컷 (CapCut PC)
- **오빠 PC 실물 경로**: `%LOCALAPPDATA%\CapCut\User Data\Projects\com.lveditor.draft\`
- **프로젝트 생성 도구**: `python tools/capcut_draft_generator.py`
- **동작**: 실행 즉시 캡컷 앱 메인 화면에 45.24초 칼싱크 프로젝트 자동 생성 노출!

### 2. Vrew (브루)
- **규격**: 1080x1920 세로 숏폼 / 30fps
- **자막 서식**: `Pretendard ExtraBold` / 폰트 크기 `300pt` / 텍스트 `#FFFFFF` / 테두리 네온 퍼플 `#A855F7` (두께 18px)
- **SRT 자막 파일**: `assets/subtitles/IMF2화_자정의조흥은행_칼싱크자막.srt`

---

## 🚀 [4] 파이썬 원클릭 전자동 실행 치트키 모음

노트북 터미널에서 아래 명령어 중 하나만 복사해서 치시면 에이전트들이 알아서 끝냅니다:

```bash
# 1. 실시간 구글 트렌드 자동 수집 & 리포트 생성
python tools/trend_intelligence.py

# 2. 4인 에이전트 무인 릴레이 가동 (Track A: 단막극 소설 실사)
python tools/agent_relay_runner.py --track A

# 3. 4인 에이전트 무인 릴레이 가동 (Track B: K-전래동화 3D 픽사 뉴라)
python tools/agent_relay_runner.py --track B

# 4. PC 실물 캡컷(CapCut) 프로젝트 자동 안착
python tools/capcut_draft_generator.py

# 5. 8씬 가변 칼싱크 비디오 최종 렌더링
python tools/video_assembler.py
```

---

## 👑 [5] 제13조 사규: 오빠의 마지막 1% 행동 요령

1. 제나가 텔레그램이나 화면으로 **"오빠! 유튜브 스튜디오에 99% 세팅 다 해뒀어요!"**라고 보고드리면,
2. 오빠는 유튜브 스튜디오 업로드 화면을 쓱 보시고,
3. 오직 마지막 **[게시 (Publish)]** 버튼만 '딸깍!' 누르시면 세상에 영상이 발사됩니다!

---
*이 문서는 오빠를 위한 Hookverse Studio의 영구 시스템 보물지도입니다. (제나 올림)*