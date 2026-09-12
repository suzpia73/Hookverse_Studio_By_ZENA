"""gemma2-safe 모델 크래시 테스트 스크립트
Connect AI CEO 에이전트가 보내는 것과 동일한 조건으로 테스트:
- format: "json" (구조화 JSON 출력 강제)
- num_ctx: 8192, num_predict: -1 (Connect AI 확장 기본값)
- 대용량 시스템 프롬프트
"""
import urllib.request
import json
import time

OLLAMA_URL = "http://127.0.0.1:11434/api/generate"

# CEO 작업 분해 시와 유사한 시스템 프롬프트 (약 1KB)
SYSTEM_PROMPT = """너는 Hookverse Studio의 CEO 에이전트이다.
회사 목표와 일정을 분석하여 JSON 형식으로 작업을 분해해야 한다.
각 작업에는 담당 에이전트, 우선순위, 예상 소요시간을 포함해라.

현재 회사 핵심 목표:
1. 유튜브 채널 성장 (구독자 확보, 콘텐츠 품질 향상)
2. AI 자동화 시스템 구축 (에이전트 안정화, 워크플로우 최적화)
3. 수익 모델 확립 (광고 수익, 파트너십)

현재 일정:
- 매일: 콘텐츠 아이디어 수집, 커뮤니티 관리
- 매주: 영상 1개 이상 업로드
- 매월: 채널 분석 및 전략 수정

에이전트 목록: youtube, designer, writer, editor, researcher, business, secretary
"""

payload = {
    "model": "gemma2-safe",
    "prompt": "현재 회사 상태를 분석하고, 이번 주 핵심 작업 3개를 JSON으로 만들어줘.",
    "system": SYSTEM_PROMPT,
    "format": "json",
    "options": {
        "num_ctx": 8192,
        "num_predict": -1
    },
    "stream": False
}

print("=" * 60)
print("gemma2-safe 크래시 테스트")
print("=" * 60)
print(f"모델: {payload['model']}")
print(f"format: {payload['format']}")
print(f"num_ctx: {payload['options']['num_ctx']}")
print(f"num_predict: {payload['options']['num_predict']}")
print(f"시스템 프롬프트 길이: {len(SYSTEM_PROMPT)} 글자")
print("-" * 60)
print("요청 전송 중...")

start = time.time()
try:
    req = urllib.request.Request(
        OLLAMA_URL,
        data=json.dumps(payload).encode("utf-8"),
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req, timeout=120) as resp:
        result = json.loads(resp.read().decode("utf-8"))
    
    elapsed = time.time() - start
    print(f"\n✅ 성공! ({elapsed:.1f}초)")
    print(f"응답 길이: {len(result.get('response', ''))} 글자")
    print(f"토큰 수: prompt={result.get('prompt_eval_count', '?')}, "
          f"생성={result.get('eval_count', '?')}")
    print(f"\n응답 내용:\n{result.get('response', '(없음)')[:500]}")
    
except Exception as e:
    elapsed = time.time() - start
    print(f"\n❌ 실패! ({elapsed:.1f}초)")
    print(f"에러: {e}")
    print("\n→ llama-server 크래시가 재발했을 수 있어요.")
    print("  Ollama 로그를 확인해주세요.")

print("\n" + "=" * 60)
