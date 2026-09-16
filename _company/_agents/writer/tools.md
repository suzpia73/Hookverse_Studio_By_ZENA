# ✍️ Writer — 도구 매니페스트

_Writer 에이전트가 어떤 도구를 어디까지 자율적으로 쓸 수 있는지 정의합니다._
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

### `legal_guardrail` (신규 핵심 · 초록색 불) ⭐ 법적 무결점 0% 검사기
작성된 대본의 초상권, 저작권, 사내 8대 금기어(정치/사회 편향, 클릭베이트)를 자동 감사하여 100점 만점으로 채점하고 검증합니다.
- **실행 명령**: `python tools/legal_guardrail.py`

### `short_script` (활성 · 연두색 불)
Hookverse Studio 5-in-1 바이럴 공식에 맞춘 30초 숏폼 나레이션 대본 및 4단 컷 기획서를 물리적 `.md` 파일로 즉시 생성하여 `assets/scripts/`에 저장합니다.

- **실행 스크립트**: `_agents/writer/tools/short_script.py`
- **매니페스트**: `_agents/writer/tools/short_script.json`
- **산출물 경로**: `assets/scripts/{제목}_30초대본.md`
- **사내 바이블**: `_company/_shared/거장_연출_및_후킹_바이블.md` 적용 필수!

---

## 로드맵 (예정)

### `tone_learner` _(예정)_
사용자 과거 글 학습 → 톤 복제

### `multi_platform_adapt` _(예정)_
하나의 스크립트 → YouTube/IG/블로그 자동 변환

### `hook_library` _(예정)_
후크·CTA 라이브러리 운영


---

## 안전 규칙 (모든 레벨 공통, 절대 우회 X)

- **삭제·배포·발송**(rm, deploy --prod, send, publish) 류는 자율도와 무관하게 **항상 승인 게이트**.
- 외부 API 호출 전 `config.md`의 토큰 존재 여부 확인.
- 모든 외부 행동은 `_agents/writer/activity.log`에 한 줄 기록 (감사용).
- 승인 대기 액션은 `approvals/pending/` 에 저장 → 텔레그램 `/approvals` 로 조회.

---

_레벨을 어떻게 골라야 할지 모르겠다면 `2 (Draft)`가 안전한 시작점입니다._
