# 🔍 웹검색 도구 (web_search)

DuckDuckGo 기반 웹검색. API 키 불필요, 무료.

## ✅ 완성된 기능

| 기능 | 상태 | 설명 |
|---|---|---|
| 일반 웹검색 | ✅ 완성 | DuckDuckGo 텍스트 검색 |
| 뉴스 검색 | ✅ 완성 | 최신 뉴스 헤드라인 수집 |
| YouTube 트렌드 | ✅ 완성 | site:youtube.com 제한 검색 |
| 보고서 저장 | ✅ 완성 | web_search_report.md에 누적 |

## 사용법

```powershell
# 일반 웹검색
python web_search.py "AI 유튜브 트렌드 2026"

# 뉴스 검색
python web_search.py "유튜브 알고리즘 변화" --mode news

# YouTube 트렌드 검색
python web_search.py "쇼츠 수익화" --mode youtube

# 결과 저장
python web_search.py "AI 콘텐츠 전략" --save

# 결과 수 조정 (기본 8개)
python web_search.py "검색어" --max 15
```

## 설치 (최초 1회)

```powershell
pip install duckduckgo-search
```

## 출력

- 콘솔에 마크다운 형식 결과 출력
- `--save` 옵션 시 `web_search_report.md`에 누적 저장
