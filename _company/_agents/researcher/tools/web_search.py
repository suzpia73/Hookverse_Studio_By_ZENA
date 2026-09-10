#!/usr/bin/env python3
"""web_search.py — Researcher 에이전트 웹검색 도구 v3.0

duckduckgo-search 라이브러리 기반. 재시도 + 타임아웃 + 폴백 강화.
없으면 자동 pip install 시도.

사용법:
  python web_search.py "검색어"
  python web_search.py "AI 유튜브 트렌드 2026" --max 10
  python web_search.py "유튜브 알고리즘" --save
  python web_search.py "유튜브 쇼츠" --mode news
  python web_search.py "유튜브 조회수" --mode youtube
"""

import sys, os, json, time, argparse, re, subprocess, threading
from datetime import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
REPORT = os.path.join(HERE, "web_search_report.md")

# ──────────────────────────────────────────
# duckduckgo-search 자동 설치
# ──────────────────────────────────────────
def ensure_ddgs():
    try:
        from duckduckgo_search import DDGS
        return DDGS
    except ImportError:
        print("📦 duckduckgo-search 설치 중...", file=sys.stderr)
        subprocess.check_call(
            [sys.executable, "-m", "pip", "install", "duckduckgo-search", "-q"],
            stdout=subprocess.DEVNULL,
        )
        from duckduckgo_search import DDGS
        print("✅ 설치 완료!", file=sys.stderr)
        return DDGS

# ──────────────────────────────────────────
# 타임아웃 래퍼
# ──────────────────────────────────────────
def _run_with_timeout(func, timeout=15):
    """func을 timeout초 안에 실행. 초과하면 [] 반환."""
    result = []
    error  = []

    def _target():
        try:
            result.extend(func())
        except Exception as e:
            error.append(e)

    t = threading.Thread(target=_target, daemon=True)
    t.start()
    t.join(timeout)
    if t.is_alive():
        print(f"⏰ 검색 타임아웃 ({timeout}초) — 빈 결과 반환", file=sys.stderr)
        return []
    if error:
        raise error[0]
    return result

# ──────────────────────────────────────────
# 웹 검색 (재시도 포함)
# ──────────────────────────────────────────
def search_web(query: str, max_results: int = 8, retries: int = 2) -> list[dict]:
    """일반 웹 검색. 실패 시 최대 retries번 재시도."""
    DDGS = ensure_ddgs()
    last_err = None
    for attempt in range(1, retries + 2):
        try:
            print(f"🌐 웹 검색 시도 {attempt}/{retries+1}...", file=sys.stderr)
            def _do():
                with DDGS() as ddgs:
                    return [
                        {
                            "title": r.get("title", ""),
                            "url":   r.get("href", ""),
                            "body":  r.get("body", "")[:300],
                        }
                        for r in ddgs.text(query, max_results=max_results, region="kr-kr")
                    ]
            results = _run_with_timeout(_do, timeout=15)
            if results:
                print(f"✅ {len(results)}건 수집됨", file=sys.stderr)
                return results
            print("⚠️ 결과 0건 — 잠시 후 재시도...", file=sys.stderr)
        except Exception as e:
            last_err = e
            print(f"⚠️ 웹검색 오류 (시도 {attempt}): {e}", file=sys.stderr)
        if attempt <= retries:
            time.sleep(3 * attempt)   # 3초, 6초 대기 후 재시도
    if last_err:
        print(f"❌ 최종 실패: {last_err}", file=sys.stderr)
    return []

# ──────────────────────────────────────────
# 뉴스 검색 (재시도 포함)
# ──────────────────────────────────────────
def search_news(query: str, max_results: int = 8, retries: int = 2) -> list[dict]:
    """최신 뉴스 검색. 실패 시 일반 검색으로 폴백."""
    DDGS = ensure_ddgs()
    last_err = None
    for attempt in range(1, retries + 2):
        try:
            print(f"📰 뉴스 검색 시도 {attempt}/{retries+1}...", file=sys.stderr)
            def _do():
                with DDGS() as ddgs:
                    return [
                        {
                            "title":  r.get("title", ""),
                            "url":    r.get("url", ""),
                            "body":   r.get("body", r.get("excerpt", ""))[:300],
                            "date":   r.get("date", ""),
                            "source": r.get("source", ""),
                        }
                        for r in ddgs.news(query, max_results=max_results, region="kr-kr")
                    ]
            results = _run_with_timeout(_do, timeout=15)
            if results:
                print(f"✅ {len(results)}건 수집됨", file=sys.stderr)
                return results
            print("⚠️ 뉴스 결과 0건...", file=sys.stderr)
        except Exception as e:
            last_err = e
            print(f"⚠️ 뉴스검색 오류 (시도 {attempt}): {e}", file=sys.stderr)
        if attempt <= retries:
            time.sleep(3 * attempt)
    # 뉴스 완전 실패 → 일반 웹 검색으로 폴백
    print("   → 일반 웹 검색으로 폴백...", file=sys.stderr)
    return search_web(f"{query} 최신 뉴스", max_results)

# ──────────────────────────────────────────
# YouTube 트렌드 검색
# ──────────────────────────────────────────
def search_youtube(query: str, max_results: int = 8) -> list[dict]:
    """YouTube 관련 검색."""
    return search_web(f"site:youtube.com {query}", max_results)

# ──────────────────────────────────────────
# 결과 포맷
# ──────────────────────────────────────────
def format_results(query: str, results: list[dict], mode: str = "web") -> str:
    ts = datetime.now().strftime("%Y-%m-%d %H:%M")
    mode_label = {"web": "🌐 웹", "news": "📰 뉴스", "youtube": "📺 YouTube"}.get(mode, "🌐 웹")

    lines = [
        f"# 🔍 웹검색 결과 [{mode_label}]",
        f"_검색어: `{query}` · {ts} · {len(results)}건_",
        "",
    ]

    if not results:
        lines.append("_검색 결과를 가져오지 못했습니다._")
        lines.append("")
        lines.append("> **해결 방법:**")
        lines.append("> 1. 인터넷 연결을 확인하세요")
        lines.append("> 2. VPN 또는 프록시를 비활성화하세요")
        lines.append("> 3. 잠시 후 다시 시도하세요 (DuckDuckGo rate limit)")
        return "\n".join(lines)

    for i, r in enumerate(results, 1):
        title  = r.get("title", "(제목 없음)")
        url    = r.get("url", "")
        body   = r.get("body", "")
        date   = r.get("date", "")
        source = r.get("source", "")

        lines.append(f"## {i}. {title}")
        meta_parts = []
        if source:
            meta_parts.append(f"📰 {source}")
        if date:
            meta_parts.append(f"🗓 {date[:10] if len(date) > 10 else date}")
        if meta_parts:
            lines.append(" | ".join(meta_parts))
        if url:
            lines.append(f"🔗 {url}")
        if body:
            lines.append(f"> {body}...")
        lines.append("")

    return "\n".join(lines)

# ──────────────────────────────────────────
# 저장 (upsert — 동일 검색어 최신 1개만 유지)
# ──────────────────────────────────────────
def save_report(content: str):
    """보고서 파일에 새 검색 결과 추가 (append 방식)."""
    with open(REPORT, "a", encoding="utf-8") as f:
        f.write("\n\n" + content + "\n\n---\n")
    print(f"\n✅ 보고서 저장: {REPORT}", file=sys.stderr)

# ──────────────────────────────────────────
# 메인
# ──────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(description="DuckDuckGo 웹검색 도구 v3.0")
    parser.add_argument("query", nargs="?", default="", help="검색어")
    parser.add_argument("--max",  type=int, default=8,
                        help="최대 결과 수 (기본 8)")
    parser.add_argument("--save", action="store_true",
                        help="결과를 web_search_report.md에 저장")
    parser.add_argument("--mode", choices=["web", "news", "youtube"], default="web",
                        help="검색 모드: web(기본) / news / youtube")
    parser.add_argument("--retries", type=int, default=2,
                        help="실패 시 재시도 횟수 (기본 2)")
    args = parser.parse_args()

    if not args.query:
        print('사용법: python web_search.py "검색어" [--max 10] [--save] [--mode web|news|youtube]')
        sys.exit(1)

    print(f"🔍 검색 중: {args.query} (mode={args.mode})", file=sys.stderr)

    if args.mode == "news":
        results = search_news(args.query, args.max, args.retries)
    elif args.mode == "youtube":
        results = search_youtube(args.query, args.max)
    else:
        results = search_web(args.query, args.max, args.retries)

    report = format_results(args.query, results, args.mode)
    print(report)

    if args.save:
        save_report(report)

if __name__ == "__main__":
    main()
