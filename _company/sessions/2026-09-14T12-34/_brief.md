# 📋 작업 브리프

**원 명령:** CEO! 2호 쇼츠 'IMF 전날 밤의 비밀' 100점 완제품 프로덕션 파이프라인 가동하라.
[작업 표준서 엄수]:
1. 모든 보고서, 총평, 연출 지문은 100% 한국어로 작성하고 영어 보고를 일체 금지한다.
2. 작가는 성우가 바로 읽을 30초 대본 4줄 본문을 완성형 구어체로 작성하고, 맨 끝에 <run_command> 태그로 short_script 도구를 반드시 물리 실행하라.
3. 디자이너는 씬 1~4 실사 영문 프롬프트 전체 블록을 완결하고, 맨 끝에 <run_command> 태그로 prompt_gen 도구를 반드시 물리 실행하라.

## 요약


## 분배
- **✍️ Writer**: 2호 쇼츠 'IMF 전날 밤의 비밀' (30초) - 한국어 대본 작성: 작가로 부르기.   py -3 _company/_agents/writer/tools/short_script.py "IMF전날밤의비밀" "타임슬립" 실행
- **🎨 Designer**: Scene 1~4 실사 영문 프롬프트 완성: 디자이너에게 부르기.   py -3 _company/_agents/designer/tools/prompt_gen.py "IMF2화_자정의중앙 금융 금고" "35mm" "야간_시네마틱" 실행
