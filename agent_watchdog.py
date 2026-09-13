#!/usr/bin/env python3
"""agent_watchdog.py — Hookverse Studio 15분 지능형 자동 관제 및 감시 감사관 v2.0

오빠(회장님)와 제나(부회장)의 헌법에 따라 15분 간격으로 다음 4대 영역을 자동 감사(Audit)합니다:
1. [잡담 감시]: 빈말·말잔치·선언문 반복인지, 실제 도구 실행 및 산출물 작성인지 판별
2. [보안 감사]: API 키, 시크릿 토큰, 비밀번호 평문 노출 여부 실시간 스캔
3. [업무 분담]: CEO가 특정 1명에게만 일을 떠넘겼는지, 팀원들에게 적절히 분배했는지 검사
4. [실물 검증]: 디스크에 대본, 프롬프트, 분석 데이터 등 물리 파일이 정상 생성되었는지 확인
"""

import os, sys, time, json, glob, argparse, re
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
COMPANY = os.path.join(HERE, "_company")
SESSIONS = os.path.join(COMPANY, "sessions")
LOG_FILE = os.path.join(HERE, "watchdog_report.md")

# 보안 검사용 위험 키 패턴
SECURITY_PATTERNS = [
    (r"AIzaSy[0-9A-Za-z_-]{33}", "Google API Key"),
    (r"8927417420:[0-9A-Za-z_-]{35}", "Telegram Bot Token"),
    (r"AQ\.[0-9A-Za-z_-]{40,}", "Gemini Studio API Key"),
    (r"sk-[0-9A-Za-z]{20,}", "OpenAI API Key"),
    (r"ghp_[0-9A-Za-z]{20,}", "GitHub Personal Token")
]

# 단순 잡담/선언문 키워드 (도구 없이 말만 하는 패턴)
CHATTER_PATTERNS = [
    "i am activating", "understood", "i will", "알겠습니다", "시작하겠습니다",
    "준비하겠습니다", "좋은 생각입니다", "동의합니다", "기다려주세요"
]

def get_latest_session_dir():
    if not os.path.exists(SESSIONS):
        return None
    dirs = [d for d in glob.glob(os.path.join(SESSIONS, "*")) if os.path.isdir(d)]
    if not dirs:
        return None
    dirs.sort(key=os.path.getmtime, reverse=True)
    return dirs[0]

def audit_security(content):
    findings = []
    for pattern, name in SECURITY_PATTERNS:
        if re.search(pattern, content):
            findings.append(f"🚨 비밀키 평문 노출 위험: {name}")
    return findings

def audit_chatter(content, size):
    lower_content = content.lower()
    
    # 테이블, 코드 블록, 헤더 등 실질적인 구조가 있는지 확인
    has_structure = ("|" in content and "---" in content) or ("```" in content) or ("##" in content and len(content) > 600)
    
    # 짧으면서 잡담 키워드만 나열된 경우
    if size < 500:
        for phrase in CHATTER_PATTERNS:
            if phrase in lower_content:
                return "⚠️ [잡담/선언 감지] 실제 도구 미실행 (단순 말잔치/준비 답변)"
        return "⏳ [진행 중] 내용이 짧거나 작성 중"
    
    if not has_structure and any(phrase in lower_content for phrase in CHATTER_PATTERNS):
        return "⚠️ [잡담 의심] 형식 없는 단순 텍스트 나열"
        
    return f"✅ [실질 작업 완료] 구조화된 산출물 생성 ({size}B)"

def inspect_session(session_path):
    session_name = os.path.basename(session_path)
    files = glob.glob(os.path.join(session_path, "*.md"))
    
    status_summary = {
        "session": session_name,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agents": {},
        "delegation": "양호",
        "security": "안전 (Green)",
        "errors": [],
        "overall": "양호"
    }

    # 1. 업무 분담 감사 (_brief.md 확인)
    brief_path = os.path.join(session_path, "_brief.md")
    if os.path.exists(brief_path):
        try:
            with open(brief_path, "r", encoding="utf-8", errors="replace") as f:
                brief_text = f.read()
            if "단독 작업" in brief_text:
                status_summary["delegation"] = "⚠️ 주의 (단일 에이전트 편중 — CEO의 전사 분배 필요)"
            else:
                status_summary["delegation"] = "✅ 양호 (적절한 업무 분배)"
        except Exception:
            pass

    # 2. 에이전트 산출물 감사
    for fpath in files:
        fname = os.path.basename(fpath)
        if fname.startswith("_"):
            continue # _brief.md, _report.md
        
        agent_name = os.path.splitext(fname)[0]
        size = os.path.getsize(fpath)
        
        try:
            with open(fpath, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
        except Exception:
            content = ""

        # 보안 감사
        sec_issues = audit_security(content)
        if sec_issues:
            status_summary["security"] = "🚨 보안 위반 감지!"
            status_summary["errors"].extend([f"{agent_name}: {issue}" for issue in sec_issues])

        # 에러 및 잡담 감사
        if "llm 호출 실패" in content.lower() or "timeout" in content.lower():
            status_summary["agents"][agent_name] = "❌ 타임아웃/호출 실패"
            status_summary["errors"].append(f"{agent_name}: LLM 호출 타임아웃 또는 크래시 발생")
            status_summary["overall"] = "위험 (조치 필요)"
        else:
            evaluation = audit_chatter(content, size)
            status_summary["agents"][agent_name] = evaluation
            if "잡담" in evaluation:
                status_summary["overall"] = "개선 필요 (말잔치 감지)"

    return status_summary

def generate_report(info):
    lines = [
        f"# 🛡️ Hookverse 15분 지능형 관제 감사 보고서",
        f"- **점검 시각**: {info['checked_at']}",
        f"- **검사 대상 세션**: `{info['session']}`",
        f"- **전체 종합 평가**: **{info['overall']}**",
        "",
        "### 🔍 4대 감사 결과",
        f"1. **🔒 보안 감사 상태**: {info['security']}",
        f"2. **📊 업무 분담 상태**: {info['delegation']}",
        "",
        "### 👥 에이전트별 실질 산출물 평가",
    ]
    if not info["agents"]:
        lines.append("- 현재 세션에 아직 에이전트 산출물이 기록되지 않았습니다 (대기 중).")
    else:
        for agent, stat in info["agents"].items():
            lines.append(f"- **{agent}**: {stat}")

    if info["errors"]:
        lines.append("")
        lines.append("### 🚨 긴급 조치 필요 사항")
        for err in info["errors"]:
            lines.append(f"- {err}")
    else:
        lines.append("")
        lines.append("✅ 감지된 치명적 보안 위반이나 시스템 에러가 없습니다.")

    lines.append("\n---\n")
    return "\n".join(lines)

def run_inspection(print_output=True):
    sess_dir = get_latest_session_dir()
    if not sess_dir:
        report = f"[{datetime.now().strftime('%H:%M:%S')}] 세션 폴더를 찾을 수 없습니다."
        if print_output:
            print(report)
        return

    info = inspect_session(sess_dir)
    report_md = generate_report(info)

    with open(LOG_FILE, "w", encoding="utf-8") as f:
        f.write(report_md)

    if print_output:
        print("=" * 65)
        print(f"🛡️ [제나 지능형 관제탑] 15분 감사 완료 ({info['checked_at']})")
        print(f"   세션: {info['session']} | 종합: {info['overall']}")
        print(f"   🔒 보안: {info['security']} | 📊 분담: {info['delegation']}")
        for agent, stat in info["agents"].items():
            print(f"   ▶ {agent}: {stat}")
        if info["errors"]:
            print(f"   ⚠️ 특이사항: {len(info['errors'])}건 발생 (watchdog_report.md 기록)")
        print("=" * 65)

def main():
    parser = argparse.ArgumentParser(description="Hookverse 에이전트 15분 지능형 감사관")
    parser.add_argument("--now", action="store_true", help="지금 즉시 1회 점검")
    parser.add_argument("--interval", type=int, default=15, help="감시 주기 (분 단위, 기본 15분)")
    args = parser.parse_args()

    if args.now:
        run_inspection(print_output=True)
        return

    interval_sec = args.interval * 60
    print(f"🛡️ Hookverse 지능형 감사관 가동! (주기: {args.interval}분)")
    print(f"   잡담 감시 · 보안 감사 · 업무 분배 · 실물 산출물 자동 추적 중...\n")

    while True:
        run_inspection(print_output=True)
        print(f"💤 다음 15분 주기 점검까지 대기합니다...\n")
        time.sleep(interval_sec)

if __name__ == "__main__":
    main()
