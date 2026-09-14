# 📋 작업 브리프

**원 명령:** CEO! 2호 쇼츠 'IMF 전날 밤의 비밀' 제작 미션을 하달한다.

[지휘 원칙]:
1. 불필요한 추론이나 기획 훈수를 절대 금지하며, 오직 순수한 JSON 1개만 출력하라.
2. 팀원들이 겹쳐서 난립하지 않도록 [1단계: 대본 작성 및 도구 실행 ➡️ 2단계: 프롬프트 작성 및 도구 실행] 순차 릴레이로 배분하라.
3. 모든 팀원은 반드시 <run_command> 태그를 실행하여 assets/scripts/ 와 assets/prompts/ 에 실제 물리 파일을 저장해야 한다.
4. 외부 툴 실행 오류나 시스템 문제가 발생하면 핑계 대지 말고 requests_to_user 필드로 즉각 지원을 요청하라.

지금 즉시 순차 파이프라인 가동 개시!

## 요약


## 분배
- **✍️ Writer**: IMF 전날 밤의 비밀 30초 대본 작성 및 py -3 _company/_agents/writer/tools/short_script.py "IMF전날밤의비밀" "타임슬립" 물리 실행
- **🎨 Designer**: 4단 실사 프롬프트 작성 및 py -3 _company/_agents/designer/tools/prompt_gen.py "IMF2화_자정의조흥은행" "35mm" "야간_시네마틱" 물리 실행
