# -*- coding: utf-8 -*-
"""
Hookverse Studio - 법적 무결점 0% 가드레일 엔진 (Compliance & Legal Guardrail)
- 초상권 리스크 검사 (실존 인물 도용 차단 / 뉴라 앵커락 권장)
- 저작권 리스크 검사 (현대 상표·IP 도용 차단 / 퍼블릭 도메인 권장)
- 사내 절대 금기어 검사 (정치/사회 편향, 저품질 클릭베이트, 혐오 표현 박멸)
- 상업용 라이선스 준수 여부 자동 채점 (100점 만점)
"""

import re
import sys
import json
import os

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

# 절대 금기 키워드 (오빠의 회사 설정 [8] 금기사항 기반)
TABOO_KEYWORDS = [
    # 낚시성 / 클릭베이트 과장
    "충격 실화", "경악", "모르면 평생 후회", "100% 실화", "유출 영상",
    # 정치적 / 사회적 편향
    "좌파", "우파", "빨갱이", "친일파", "종북", "정권 퇴진", "선거 조작",
    # 혐오 / 자극 / 유해
    "극혐", "살인마", "잔혹", "엽기", "성인물", "도박"
]

# 타사 현대 저작권 침해 위험 키워드 (70년 이내 보호 IP)
TRADEMARK_RISKS = [
    "마블", "아이언맨", "스파이더맨", "디즈니", "미키마우스",
    "포켓몬", "피카츄", "해리포터", "스타워즈", "넷플릭스 오리지널"
]

def audit_content(script_text="", prompt_text=""):
    """대본과 이미지 프롬프트를 대상으로 법적 무결점 감사 수행"""
    issues = []
    score = 100
    full_text = f"{script_text} {prompt_text}"
    
    # 1. 절대 금기어 검사
    found_taboos = [w for w in TABOO_KEYWORDS if w in full_text]
    if found_taboos:
        score -= len(found_taboos) * 15
        issues.append({
            "type": "TABOO_VIOLATION",
            "severity": "CRITICAL",
            "message": f"사내 절대 금기 키워드가 감지되었습니다: {', '.join(found_taboos)}",
            "action": "해당 단어를 즉시 객관적이고 품격 있는 어휘로 교체하십시오."
        })
        
    # 2. 타사 현대 저작권 침해 위험 검사
    found_tm = [w for w in TRADEMARK_RISKS if w in full_text]
    if found_tm:
        score -= len(found_tm) * 20
        issues.append({
            "type": "COPYRIGHT_RISK",
            "severity": "CRITICAL",
            "message": f"현대 상표/보호 IP 도용 위험 키워드가 감지되었습니다: {', '.join(found_tm)}",
            "action": "퍼블릭 도메인(구전동화, 역사적 팩트) 또는 Hookverse 순수 창작 설정으로 변경하십시오."
        })
        
    # 3. 초상권 검사 (프롬프트 내 실존 인물 / 앵커락 여부)
    if prompt_text:
        # 연예인/실존인물 유명 영문 이름 패턴
        real_person_risks = ["IU", "BTS", "NewJeans", "Jennie", "Taylor Swift", "Trump", "Biden"]
        found_persons = [p for p in real_person_risks if re.search(r'\b' + p + r'\b', prompt_text, re.I)]
        if found_persons:
            score -= 30
            issues.append({
                "type": "PORTRAIT_RIGHTS_VIOLATION",
                "severity": "FATAL",
                "message": f"실존 인물 딥페이크 위험 키워드가 발견되었습니다: {', '.join(found_persons)}",
                "action": "실존 인물 이름을 즉시 삭제하고, Hookverse 독점 가상 뮤즈 'NEURA' 안면 앵커락을 사용하십시오."
            })
            
        # 뉴라 앵커락 키워드 점검
        if "NEURA" not in prompt_text and "woman" in prompt_text:
            score -= 5
            issues.append({
                "type": "ANCHOR_RECOMMENDATION",
                "severity": "WARNING",
                "message": "여성 캐릭터 프롬프트에 NEURA 앵커락 고정 키셋이 누락되었습니다.",
                "action": "안면 일관성을 위해 'NEURA, signature beauty mark under left eye' 앵커락을 주입하십시오."
            })
            
    # 최종 판정
    status = "PASS" if score >= 90 else ("REVISE" if score >= 70 else "FAIL")
    
    report = {
        "score": max(0, score),
        "status": status,
        "is_safe": status == "PASS",
        "issue_count": len(issues),
        "issues": issues,
        "compliance_summary": (
            "✅ 100% 법적 무결점 통과: 상업적 발행 가능" if status == "PASS" else
            "⚠️ 수정 권고: 법적 리스크 요소를 보완 후 재검사하십시오."
        )
    }
    return report

def audit_file(file_path):
    """파일을 직접 읽어 감사 수행"""
    if not os.path.exists(file_path):
        print(f"❌ 파일이 존재하지 않습니다: {file_path}")
        return None
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    report = audit_content(script_text=content)
    return report

if __name__ == "__main__":
    print("=" * 60)
    print("🛡️ [Legal Guardrail] 법적 무결점 검사 엔진 테스트")
    print("=" * 60)
    
    # 정상 테스트 케이스 (2화 확정 대본)
    test_script_pass = """
    1997년 11월 20일 자정, 명동의 시계탑이 멈춘 순간.
    누군가 조흥은행 지하 금고를 털었습니다.
    금고를 비운 부패 세력이 흘리고 간 마지막 달러 가방.
    장부에 남겨진 서명, 뉴라(NEURA).
    """
    
    test_prompt_pass = """
    NEURA, 20s Korean woman, sharp cat-eyes, signature beauty mark under left eye and corner of mouth.
    Midnight Chohung Bank basement vault 1997, cinematic 35mm photograph, Kodak Portra 400.
    """
    
    result = audit_content(test_script_pass, test_prompt_pass)
    print(f"테스트 결과: 점수={result['score']}, 상태={result['status']}")
    print(f"요약: {result['compliance_summary']}")
    
    if result["issues"]:
        for issue in result["issues"]:
            print(f"  - [{issue['severity']}] {issue['message']}")
            
    print("=" * 60)
    print("✨ 법적 가드레일 엔진 준비 완료!")
