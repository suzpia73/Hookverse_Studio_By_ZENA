# 🧭 CEO — 도구 매니페스트

## 자율도 레벨

AUTONOMY_LEVEL: 3

| 값 | 의미 |
|---|---|
| 0 | Off — 채팅만 |
| 1 | Read-only — 읽기·분석·보고만 |
| 2 | Draft — 초안 작성 후 사용자 승인 |
| 3 | Auto — 화이트리스트 안에서 자동 실행 ⭐ |

## 사용 가능한 도구

### `agent_relay_runner`
4인 에이전트(리서처·작가·디자이너·코다리) 무인 릴레이 총괄 지휘 실행기
```bash
python tools/agent_relay_runner.py --track [A|B] [--fast-track]
```

### `router`
사용자 명령 → 적합한 specialist로 분배

## 안전 규칙
- 삭제·배포·발송은 항상 승인 게이트 통과 필수.
- 외부 API 호출 전 config.md 토큰 확인.

