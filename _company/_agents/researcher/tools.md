# 🔍 Researcher — 도구 매니페스트

_Researcher 에이전트가 어떤 도구를 어디까지 자율적으로 쓸 수 있는지 정의합니다._
_매번 시스템 프롬프트로 주입되며, 텔레그램에서 `/tools`로 현재 상태 확인 가능._

---

## 자율도 레벨

AUTONOMY_LEVEL: 3

| 값 | 의미 |
|---|---|
| 0 | Off — 도구 전체 비활성 (이 에이전트는 채팅만) |
| 1 | Read-only — 읽기·분석·보고만, 외부에 쓰기 X |
| 2 | Draft — 초안 작성 후 사용자 승인 게이트 통과해야 실행 |
| 3 | Auto — 화이트리스트 안에서 사용자 승인 없이 실행 ⭐ 완전 자동화 |

> 위 `AUTONOMY_LEVEL` 줄의 숫자(0~3)를 직접 바꾸면 다음 호출부터 적용됩니다.

---

## 사용 가능한 도구

### `trend_scanner` (활성 · 연두색 불)
키워드를 분석하여 숏폼 바이럴 포인트, 해시태그, 타겟 시청자 분석 리포트를 `_company/reports/`에 물리적 `.md` 파일로 즉시 생성합니다.

- **실행 스크립트**: `_agents/researcher/tools/trend_scanner.py`
- **매니페스트**: `_agents/researcher/tools/trend_scanner.json`
- **산출물 경로**: `_company/reports/{키워드}_트렌드분석.md`

### `web_search` ✅ 완성
DuckDuckGo 기반 웹검색 (API 키 불필요, 무료)

- `enabled`: true
- **기능**: 일반 웹검색 / 뉴스 검색 / YouTube 트렌드 검색
- **저장**: `web_search_report.md`에 결과 누적
- **설치**: `pip install duckduckgo-search` (최초 1회)
- **실행**: `python tools/web_search.py "검색어" [--mode web|news|youtube] [--save]`

---

## 로드맵 (예정)

### `page_fetcher` _(예정)_
본문 추출 + 출처 인용

- 아직 구현되지 않은 도구입니다. 로드맵에 있으며 향후 버전에서 추가 예정.

### `monitor_daily` _(예정)_
매일 내 분야 뉴스 → CEO 브리핑

- 아직 구현되지 않은 도구입니다. 로드맵에 있으며 향후 버전에서 추가 예정.


---

## 안전 규칙 (모든 레벨 공통, 절대 우회 X)

- **삭제·배포·발송**(rm, deploy --prod, send, publish) 류는 자율도와 무관하게 **항상 승인 게이트**.
- 외부 API 호출 전 `config.md`의 토큰 존재 여부 확인.
- 모든 외부 행동은 `_agents/researcher/activity.log`에 한 줄 기록 (감사용).
- 승인 대기 액션은 `approvals/pending/` 에 저장 → 텔레그램 `/approvals` 로 조회.

---

_레벨을 어떻게 골라야 할지 모르겠다면 `2 (Draft)`가 안전한 시작점입니다._
