#!/usr/bin/env python3
"""agent_watchdog.py — Hookverse Studio 에이전트 백그라운드 자동 관제관 v1.0

15분 간격으로 에이전트들의 상태(업무 분배 여부, 타임아웃, 산출물 완성도)를
자동으로 감시하고, 컴퓨터 사양(MX250)에 맞추어 지연 및 장애를 진단합니다.

사용법:
  # 백그라운드 상주 감시 (기본 15분 주기)
  python agent_watchdog.py

  # 1회 즉시 점검 및 리포트 출력
  python agent_watchdog.py --now

  # 감시 주기 변경 (예: 20분)
  python agent_watchdog.py --interval 20
"""

import os, sys, time, json, glob, argparse
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
COMPANY = os.path.join(HERE, "_company")
SESSIONS = os.path.join(COMPANY, "sessions")
LOG_FILE = os.path.join(HERE, "watchdog_report.md")

def get_latest_session_dir():
    if not os.path.exists(SESSIONS):
        return None
    dirs = [d for d in glob.glob(os.path.join(SESSIONS, "*")) if os.path.isdir(d)]
    if not dirs:
        return None
    # 최신 날짜순 정렬
    dirs.sort(key=os.path.getmtime, reverse=True)
    return dirs[0]

def inspect_session(session_path):
    session_name = os.path.basename(session_path)
    files = glob.glob(os.path.join(session_path, "*.md"))
    
    status_summary = {
        "session": session_name,
        "checked_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "agents": {},
        "errors": [],
        "overall": "양호"
    }

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

        # 상태 분석
        if "LLM 호출 실패" in content or "timeout" in content.lower():
            status_summary["agents"][agent_name] = "⚠️ 타임아웃/실패"
            status_summary["errors"].append(f"{agent_name}: 타임아웃 또는 호출 실패 감지")
            status_summary["overall"] = "주의 필요"
        elif size > 500:
            status_summary["agents"][agent_name] = f"✅ 산출물 완성 ({size}B)"
        else:
            status_summary["agents"][agent_name] = f"⏳ 진행 중/짧음 ({size}B)"

    return status_summary

def generate_report(info):
    lines = [
        f"# 🛡️ Hookverse 에이전트 관제 보고서",
        f"- **점검 시각**: {info['checked_at']}",
        f"- **최근 세션**: `{info['session']}`",
        f"- **종합 상태**: **{info['overall']}**",
        "",
        "### 👥 에이전트별 업무 수행 상태",
    ]
    if not info["agents"]:
        lines.append("- 현재 세션에 아직 에이전트 산출물이 기록되지 않았습니다 (대기 중).")
    else:
        for agent, stat in info["agents"].items():
            lines.append(f"- **{agent}**: {stat}")

    if info["errors"]:
        lines.append("")
        lines.append("### 🚨 감지된 특이사항 & 조치 필요")
        for err in info["errors"]:
            lines.append(f"- {err}")
    else:
        lines.append("")
        lines.append("✅ 감지된 치명적 에러 없음. 에이전트들이 정상 페이스로 작업 중입니다.")

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
        print("=" * 60)
        print(f"🛡️ [제나 관제탑] 에이전트 상태 점검 ({info['checked_at']})")
        print(f"   세션: {info['session']} | 종합: {info['overall']}")
        for agent, stat in info["agents"].items():
            print(f"   ▶ {agent}: {stat}")
        if info["errors"]:
            print(f"   ⚠️ 이슈: {len(info['errors'])}건 발생 (watchdog_report.md 참고)")
        print("=" * 60)

def main():
    parser = argparse.ArgumentParser(description="Hookverse 에이전트 백그라운드 자동 관제관")
    parser.add_argument("--now", action="store_true", help="지금 즉시 1회 점검")
    parser.add_argument("--interval", type=int, default=15, help="감시 주기 (분 단위, 기본 15분)")
    args = parser.parse_args()

    if args.now:
        run_inspection(print_output=True)
        return

    interval_sec = args.interval * 60
    print(f"🛡️ Hookverse 에이전트 자동 관제관 가동 시작! (주기: {args.interval}분)")
    print(f"   종료하려면 Ctrl+C를 누르세요.\n")

    while True:
        run_inspection(print_output=True)
        print(f"💤 다음 점검까지 {args.interval}분간 대기합니다...\n")
        time.sleep(interval_sec)

if __name__ == "__main__":
    main()
