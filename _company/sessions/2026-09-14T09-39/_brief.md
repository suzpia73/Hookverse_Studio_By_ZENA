# 📋 작업 브리프

**원 명령:** CEO! 2호 쇼츠 2단계 미션을 하달한다.

[지휘 명령]:
1. 작가가 완성한 1997년 명동 대본을 바탕으로, 디자이너를 즉각 투입하여 씬 1~4 실사 영문 프롬프트(85mm 렌즈, 뉴라 매력점, 1997 조흥은행 고증) 작성을 완료하라.
2. 가짜 계획서(planning JSON)나 영어 변명 잡담(Explanation)을 절대 금지하며, 디자이너는 오직 순수 프롬프트 본문 출력과 <run_command> 도구 실행으로 assets/prompts/ 에 실제 파일을 저장해야 한다.
3. CEO는 순수한 JSON 규격으로 디자이너에게 즉각 업무를 하달하라!

## 요약


## 분배
- **✍️ Writer**: 1997년 IMF 전날 서울 명동 환전 골목: 뉴라를 중심으로 작품 작성 및 py -3 _company/_agents/writer/tools/short_script.py "IMF전날밤의비밀" "타임슬립" 물리 실행
- **🎨 Designer**: 1997년 명동 환전 골목: 뉴라를 중심으로 씬별 실사 영문 프롬프트 작성 및 py -3 _company/_agents/designer/tools/prompt_gen.py "IMF2화_자정의조흥은행" "35mm" "야간_시네마틱" 물리 실행
