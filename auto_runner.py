#!/usr/bin/env python3
"""auto_runner.py — HOOKVERSE STUDIO 자동 실행 스케줄러 v1.0

컴퓨터가 켜져 있으면 매일 정해진 시간에 에이전트 도구들을 자동으로 실행합니다.

실행 스케줄 (기본):
  - 매일 09:00 — 웹 트렌드 수집 + 텔레그램 보고
  - 매일 09:05 — my_videos_check (내 채널 분석 + 텔레그램 보고)
  - 매일 09:10 — trend_sniper (YouTube 트렌드 분석)

사용법:
  # 백그라운드 실행 (컴퓨터 켜져 있는 동안 계속)
  python auto_runner.py

  # 지금 당장 모든 도구 한 번 실행 (테스트용)
  python auto_runner.py --now

  # 특정 시간 설정
  python auto_runner.py --time 08:30

Windows 자동 시작 등록:
  schtasks /create /tn "HOOKVERSE_AutoRunner" /tr "python D:\\HOOKVERSE-SYSTEM\\HOOKVERSE_STUDIO_V2\\auto_runner.py" /sc ONLOGON /f
"""

import os, sys, time, subprocess, argparse, json
from datetime import datetime, timedelta

HERE = os.path.dirname(os.path.abspath(__file__))
AGENTS = os.path.join(HERE, "_company", "_agents")
LOG    = os.path.join(HERE, "auto_runner.log")

# 텔레그램 설정 로드 (secretary 도구에서)
def _load_telegram():
    tg_path = os.path.join(AGENTS, "secretary", "tools", "telegram_setup.json")
    try:
        with open(tg_path, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        return cfg.get("TELEGRAM_BOT_TOKEN", ""), cfg.get("TELEGRAM_CHAT_ID", "")
    except Exception:
        return "", ""

def _push_telegram(msg: str):
    token, chat = _load_telegram()
    if not token or not chat:
        return
    try:
        import requests
        requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat, "text": msg},
            timeout=10,
        )
    except Exception:
        pass

# ──────────────────────────────────────────
# 실행할 도구 목록
# ──────────────────────────────────────────
TASKS = [
    {
        "name":    "🔍 웹 트렌드 수집",
        "script":  os.path.join(AGENTS, "researcher", "tools", "web_search.py"),
        "args":    ["AI 유튜브 콘텐츠 트렌드 2026", "--mode", "news", "--save"],
        "delay":   0,
        "timeout": 60,    # 1분
    },
    {
        "name":    "📺 내 채널 분석",
        "script":  os.path.join(AGENTS, "youtube", "tools", "my_videos_check.py"),
        "args":    [],
        "delay":   300,
        "timeout": 120,   # 2분
    },
    {
        "name":    "🎯 YouTube 트렌드 스나이퍼",
        "script":  os.path.join(AGENTS, "youtube", "tools", "trend_sniper.py"),
        "args":    [],
        "delay":   600,
        "timeout": 600,   # 10분 (키워드 8개 × API 호출)
    },
]

# ──────────────────────────────────────────
# 로그
# ──────────────────────────────────────────
def log(msg: str):
    ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    line = f"[{ts}] {msg}"
    print(line)
    with open(LOG, "a", encoding="utf-8") as f:
        f.write(line + "\n")

# ──────────────────────────────────────────
# 단일 태스크 실행
# ──────────────────────────────────────────
def run_task(task: dict) -> bool:
    script = task["script"]
    if not os.path.exists(script):
        log(f"⚠️ 스크립트 없음, 건너뜀: {script}")
        return False

    timeout = task.get("timeout", 120)
    cmd = [sys.executable, script] + task["args"]
    log(f"▶ {task['name']} 시작")
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=timeout,
        )
        if result.returncode == 0:
            log(f"✅ {task['name']} 완료")
            return True
        else:
            log(f"❌ {task['name']} 실패 (exit {result.returncode})")
            if result.stderr:
                log(f"   stderr: {result.stderr[:300]}")
            return False
    except subprocess.TimeoutExpired:
        log(f"⏰ {task['name']} 타임아웃 ({timeout}초 초과)")
        return False
    except Exception as e:
        log(f"❌ {task['name']} 예외: {e}")
        return False

# ──────────────────────────────────────────
# 모든 태스크 순차 실행
# ──────────────────────────────────────────
def run_all_tasks(no_delay: bool = False):
    log("=" * 50)
    log("🚀 HOOKVERSE 자동 실행 시작" + (" (즉시 모드)" if no_delay else ""))
    log("=" * 50)

    results = []
    base_time = time.time()
    for task in TASKS:
        if not no_delay:
            elapsed = time.time() - base_time
            wait = task["delay"] - elapsed
            if wait > 0:
                log(f"⏳ {task['name']} — {int(wait)}초 후 실행")
                time.sleep(wait)
        ok = run_task(task)
        results.append((task["name"], ok))

    log("=" * 50)
    succeeded = sum(ok for _, ok in results)
    total = len(results)
    status = "✅" if succeeded == total else "⚠️"
    log(f"{status} 오늘 자동 실행 결과: {succeeded}/{total} 성공")
    log("=" * 50)

    # 텔레그램으로 완료 요약 전송
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    summary = "모든 작업 성공" if succeeded == total else f"{total - succeeded}개 작업 실패"
    lines = [f"🤖 HOOKVERSE 자동 실행 결과 ({ts}) — {summary}", ""]
    for name, ok in results:
        icon = "✅" if ok else "❌"
        lines.append(f"{icon} {name}")
    lines.append("")
    lines.append("(상세 결과는 각 도구 보고서 확인)")
    _push_telegram("\n".join(lines))

# ──────────────────────────────────────────
# 다음 실행 시각 계산
# ──────────────────────────────────────────
def next_run_time(hour: int, minute: int) -> datetime:
    now = datetime.now()
    target = now.replace(hour=hour, minute=minute, second=0, microsecond=0)
    if target <= now:
        target += timedelta(days=1)
    return target

# ──────────────────────────────────────────
# 메인 루프
# ──────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="HOOKVERSE 자동 실행 스케줄러")
    parser.add_argument("--now",  action="store_true", help="지금 당장 모든 도구 실행 (테스트)")
    parser.add_argument("--time", default="09:00",     help="실행 시각 (HH:MM, 기본 09:00)")
    args = parser.parse_args()

    if args.now:
        run_all_tasks(no_delay=True)
        return

    try:
        h, m = map(int, args.time.split(":"))
        if not (0 <= h <= 23 and 0 <= m <= 59):
            raise ValueError
    except ValueError:
        print(f"❌ 시간 형식 오류: {args.time} → HH:MM 형식으로 입력하세요.")
        sys.exit(1)

    log(f"⏰ HOOKVERSE 자동 스케줄러 시작 — 매일 {h:02d}:{m:02d} 실행")
    log(f"   종료하려면 Ctrl+C")

    while True:
        target = next_run_time(h, m)
        wait_sec = (target - datetime.now()).total_seconds()
        log(f"💤 다음 실행: {target.strftime('%Y-%m-%d %H:%M')} (약 {int(wait_sec/3600)}시간 {int((wait_sec%3600)/60)}분 후)")

        # 1분 간격으로 체크 (더 정확하게)
        while datetime.now() < target:
            time.sleep(60)

        run_all_tasks()

        # 같은 날 다시 실행되지 않도록 61초 대기
        time.sleep(61)

if __name__ == "__main__":
    main()
