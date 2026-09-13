# 👑 CEO 탑다운 미션 하달 & 물리 도구 실행 통제 (top_down_dispatch)

> **목표**: 제나-오빠가 협의한 미션을 15분 워치독 사이클에 맞춰 전사 에이전트에게 직통 하달하고, 실제 물리적 산출물 생성을 강제한다.

---

## 1. 탑다운 직통 하달 원칙
1. **단일 미션 주입**: `_company/_shared/goals.md`에 등록된 1순위 미션을 읽어 즉시 담당 에이전트에게 할당.
2. **도구 실행 강제 (Tool Enforcement)**:
   - 말잔치(추론 텍스트)만 늘어놓는 행위 금지.
   - Writer는 반드시 `short_script.py`, Designer는 `prompt_gen.py`, Researcher는 `trend_scanner.py` 도구를 호출하도록 명령.
3. **완료 검증**:
   - `assets/scripts/` 또는 `assets/prompts/`에 실제 파일이 생성되었는지 확인 후 상태 갱신.

---

## 2. 메모리 비만 방지 수칙
- CEO 메모리가 10KB를 초과하지 않도록 주기적으로 핵심 3줄 요약 유지.
