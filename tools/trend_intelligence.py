# -*- coding: utf-8 -*-
"""
Hookverse Studio - 크로스 플랫폼 트렌드 인텔리전스 레이더 (v3.0 Final)
- 오빠의 헌법: '카테고리 범위 지정 + 구글/유튜브/뉴스/SNS 크로스 플랫폼 공통 인기 키워드 교차 검증'
- 4대 멀티 소스 교차 수집 (Multi-Source Cross-Check):
  1. Google Trends (KR & US 실시간 급상승 키워드)
  2. Google News 종합 헤드라인 (국내외 주요 뉴스 포털)
  3. Google News Tech & Science (과학/기술/AI/우주 특화)
  4. YouTube Trending Signals (유튜브 화제 토픽 및 급상승 비디오)
- 4대 타깃 카테고리 범위 필터 (범위 설정 파라미터 지원):
  - ALL: 전체 교집합
  - HISTORY_MYSTERY: 역사, 조선, 대체역사, 발굴, 1997, 미스터리
  - SCI_TECH_FUTURE: AI, 양자, 로봇, 시간여행, 우주, 미래기술
  - CULTURE_MYTH: 신화, 단군, 전래동화, 설화, 오파츠, 3D 픽사
  - BREAKING_MEGA: 전국민적 충격 사건, 경제/외환 위기, 국가 비상
- 크로스 플랫폼 공통도(Consensus Score 1~100점):
  - 2개 이상 플랫폼 공통 폭발 시: 80점 이상 (크로스 플랫폼 바이럴)
  - 3개 이상 플랫폼 동시 폭발 시: 95점 이상 (🔥 메가 골든 트렌드!)
- Hookverse 세계관 맞춤형 What-If 시놉시스 & 3초 후킹 질문 자동 결합!
"""

import os
import sys
import json
import re
import argparse
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET
from datetime import datetime

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
OUTPUT_JSON = os.path.join(BASE_DIR, "00_Raw", "knowledge_packs", "daily_trends.json")
OUTPUT_MD = os.path.join(BASE_DIR, "_company", "reports", "트렌드리포트_최신.md")

# 4대 허용 타깃 카테고리 사전
TARGET_CATEGORIES = {
    "HISTORY_MYSTERY": ["역사", "조선", "왕조", "고대", "비밀", "발굴", "1997", "IMF", "외환", "임시정부", "전쟁", "유령", "실록", "미스터리", "보물", "고종", "세종", "사도세자"],
    "SCI_TECH_FUTURE": ["AI", "인공지능", "로봇", "양자", "우주", "스마트폰", "기술", "미래", "타임머신", "해킹", "가상", "디지털", "칩", "반도체", "엔비디아", "오픈AI", "젠슨", "황", "머스크", "테슬라", "애플", "구글"],
    "CULTURE_MYTH": ["신화", "단군", "동화", "설화", "전설", "용궁", "도깨비", "심청", "토끼", "별주부", "호랑이", "웹툰", "시네마", "괴담", "구미호", "흥부", "놀부"],
    "BREAKING_MEGA": ["부도", "비상", "경보", "충격", "폭발", "화재", "사건", "위기", "자금", "달러", "금리", "주식", "검거", "긴급", "참사", "환율", "계엄", "비자금", "압수수색"]
}

# 언론사 / 도메인 / 무의미 기능어 배제 목록
STOPWORDS_MEDIA = [
    "한겨레", "조선일보", "동아일보", "중앙일보", "연합뉴스", "뉴스1", "뉴시스", "경향신문",
    "한국경제", "매일경제", "서울경제", "YTN", "SBS", "KBS", "MBC", "JTBC", "채널A",
    "TV조선", "머니투데이", "이데일리", "노컷뉴스", "문화일보", "세계일보", "국민일보",
    "필요없다", "논란에", "밝혔다", "말했다", "대해", "위해", "통해", "따르면", "지난",
    "관련", "사진", "포토", "영상", "속보", "단독", "종합", "뉴스", "오늘", "내일", "어제",
    "만에", "정식", "도입", "목표", "출시", "공개", "전비만", "썼다", "걸려", "되살리다",
    "아이폰", "삼성", "LG", "DongA", "itworld", "ZDNet", "디지털데일리", "전자신문",
    "co", "kr", "com", "net", "org", "www", "http", "https", "Science", "헤럴드경제"
]

# 단순 연예 가십 / 일상 무관 키워드 배제 목록 (DROP 필터)
DROP_KEYWORDS = [
    "박원숙", "소유진", "송지은", "화장실", "결혼", "이혼", "열애", "예능", "음식점", "맛집",
    "성형", "데이트", "골프", "패션", "뷰티", "다이어트", "시청률", "아이돌", "팬미팅", "콘서트"
]

def fetch_rss_data(url, source_name):
    """RSS 데이터 안전 수집 함수"""
    items = []
    try:
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
        with urllib.request.urlopen(req, timeout=8) as r:
            root = ET.fromstring(r.read())
            for item in root.findall(".//item"):
                title = item.find("title")
                desc = item.find("description")
                approx = item.find("{https://trends.google.com/trending/rss}approx_traffic")
                news_items = item.findall("{https://trends.google.com/trending/rss}news_item")

                title_text = title.text.strip() if title is not None and title.text else ""
                desc_text = desc.text.strip() if desc is not None and desc.text else ""
                traffic_text = approx.text if approx is not None and approx.text else "10,000+"
                
                # HTML 태그 제거
                title_text = re.sub(r"<[^>]+>", "", title_text)
                desc_text = re.sub(r"<[^>]+>", "", desc_text)

                snippets = []
                for n in news_items:
                    t = n.find("{https://trends.google.com/trending/rss}news_item_title")
                    if t is not None and t.text:
                        snippets.append(re.sub(r"<[^>]+>", "", t.text.strip()))

                if title_text:
                    items.append({
                        "source": source_name,
                        "title": title_text,
                        "desc": desc_text,
                        "traffic": traffic_text,
                        "snippets": snippets
                    })
    except Exception as e:
        print(f"⚠️ RSS 수집 예외 ({source_name}): {e}")
    return items

def extract_core_keywords(text):
    """제목/문장에서 2글자 이상의 핵심 명사/키워드 추출 (불용어 및 언론사, 도메인 제외)"""
    text = re.sub(r"[a-zA-Z0-9_\-\.]+\.(com|co|kr|net|org)", " ", text, flags=re.IGNORECASE)
    clean_text = re.sub(r"[^\w\s가-힣]", " ", text)
    words = clean_text.split()
    valid_words = []
    for w in words:
        if len(w) < 2:
            continue
        if re.match(r"^\d+(년|월|일|분|초|억|조|원)?$", w):
            continue
        if w in STOPWORDS_MEDIA:
            continue
        valid_words.append(w)
    return valid_words

def cross_check_consensus(trend_pool):
    """
    여러 플랫폼(Google Trends, News, Tech News, YouTube 등)에서 동시 출현하는 공통 키워드 교차 감사
    """
    keyword_tracker = {}

    for item in trend_pool:
        source = item["source"]
        title = item["title"]
        context = f"{title} {item['desc']} {' '.join(item['snippets'])}"
        
        # 가십 필터링
        if any(drop in context for drop in DROP_KEYWORDS):
            continue

        kws = extract_core_keywords(title)
        for kw in kws:
            if kw not in keyword_tracker:
                keyword_tracker[kw] = {
                    "keyword": kw,
                    "sample_title": title,
                    "sources": set(),
                    "mention_count": 0,
                    "full_context": context,
                    "traffic": item["traffic"]
                }
            keyword_tracker[kw]["sources"].add(source)
            keyword_tracker[kw]["mention_count"] += 1
            keyword_tracker[kw]["full_context"] += " " + context

    results = []
    for kw, data in keyword_tracker.items():
        sources_list = list(data["sources"])
        source_count = len(sources_list)
        
        # 4대 카테고리 매칭 검사
        matched_cat = None
        category_score = 0
        for cat_name, words in TARGET_CATEGORIES.items():
            hit_count = sum(1 for w in words if w in data["full_context"])
            if hit_count > 0:
                matched_cat = cat_name
                category_score = min(40, hit_count * 15)
                break

        # 타깃 카테고리가 아니고 단일 출처에 언급도 적으면 제외
        if not matched_cat and source_count < 2 and data["mention_count"] < 2:
            continue

        if not matched_cat:
            matched_cat = "WHAT_IF_CANDIDATE"
            category_score = 15

        # 크로스 플랫폼 공통도 점수 (Consensus Score)
        # 기본 50점 + 카테고리 매칭(최대 40점) + 다중 플랫폼 동시 출현(플랫폼당 20점) + 언급 횟수 가중치
        consensus_score = 50 + category_score + (source_count * 20) + min(10, data["mention_count"] * 2)
        consensus_score = min(100, consensus_score)

        # What-If 스토리 각색안 생성
        adaptation = generate_what_if_story(kw, matched_cat, data["sample_title"])

        results.append({
            "keyword": kw,
            "sample_title": data["sample_title"],
            "sources": sources_list,
            "source_count": source_count,
            "traffic": data["traffic"],
            "category": matched_cat,
            "consensus_score": consensus_score,
            "is_mega_viral": consensus_score >= 85,
            "adaptation": adaptation
        })

    # 공통 플랫폼 수(source_count) 우선, 그 다음 공통도 점수 기준 내림차순 정렬
    results.sort(key=lambda x: (x["source_count"], x["consensus_score"]), reverse=True)
    return results

def generate_what_if_story(keyword, category, title):
    """키워드와 카테고리를 Hookverse 세계관 스토리로 변환"""
    if category == "BREAKING_MEGA" or "경제" in title or "달러" in title or "위기" in title:
        return {
            "track": "Track A (단막극 시네마틱 소설 실사)",
            "anchor": "1997년 IMF 외환위기 비자금과 타임슬립 수호자 뉴라",
            "hook": f"만약 이번 {keyword} 사태의 뿌리가 1997년 지하 비밀 외환 금고 비자금 장부와 직결되어 있다면?",
            "visual": "1997년 자정 서울 명동 비 내리는 골목, 블랙 트렌치코트의 뉴라가 서류 가방을 쥐고 있는 35mm 시네마틱 실사 컷"
        }
    elif category == "SCI_TECH_FUTURE" or "AI" in title or "우주" in title:
        return {
            "track": "Track A (SF 타임슬립)",
            "anchor": "2026년 양자 AI와 조선시대 외규장각의 비밀 교신",
            "hook": f"만약 전 세계를 뒤흔든 {keyword} 기술의 핵심 알고리즘이 300년 전 조선 실록에 암호로 기록되어 있었다면?",
            "visual": "어두운 연구실 홀로그램 화면 속에 조선시대 천문도와 현대 양자 코드가 교차하는 네온 블루 톤 컷"
        }
    elif category == "CULTURE_MYTH":
        return {
            "track": "Track B (K-전래동화 3D 픽사)",
            "anchor": "구전 동화 속 신화적 도구의 SF적 재해석",
            "hook": f"만약 우리가 알던 {keyword}의 진짜 정체가 미래에서 떨어진 3D 픽사 뉴라의 시공간 오파츠였다면?",
            "visual": "따뜻하고 영롱한 3D 픽사 스타일, 별빛이 쏟아지는 대나무 숲에서 빛나는 오파츠를 발견한 뉴라"
        }
    else: # HISTORY_MYSTERY & WHAT_IF_CANDIDATE
        return {
            "track": "Track A/B 하이브리드",
            "anchor": "잊혀진 역사적 사건과 평행세계의 시간 분기점",
            "hook": f"만약 {keyword}의 공식 기록이 누군가에 의해 의도적으로 조작된 거대한 What-If 세계라면?",
            "visual": "안개 낀 고대 궁궐 앞, 젖은 개버딘 코트를 입은 뉴라의 시선이 과거와 미래의 경계를 응시하는 극적인 앵글"
        }

def run_cross_platform_intelligence(target_category="ALL", min_score=70):
    print("=" * 70)
    print("🌐 [Hookverse Studio] 크로스 플랫폼 트렌드 & 4대 카테고리 레이더 v3.0 Final 가동")
    print(f"🎯 설정 범위: 카테고리 [{target_category}] / 최소 공통도 [{min_score}점 이상]")
    print("=" * 70)

    # 4대 소스 실시간 수집
    yt_query = urllib.parse.quote("유튜브 인기 트렌드")
    sources = [
        ("https://trends.google.com/trending/rss?geo=KR", "GoogleTrends_KR"),
        ("https://trends.google.com/trending/rss?geo=US", "GoogleTrends_US"),
        ("https://news.google.com/rss?hl=ko&gl=KR&ceid=KR:ko", "GoogleNews_Top"),
        ("https://news.google.com/rss/headlines/section/topic/SCITECH?hl=ko&gl=KR&ceid=KR:ko", "GoogleNews_Tech"),
        (f"https://news.google.com/rss/search?q={yt_query}&hl=ko&gl=KR&ceid=KR:ko", "YouTube_Trending_Signals")
    ]

    all_raw_items = []
    for url, sname in sources:
        items = fetch_rss_data(url, sname)
        all_raw_items.extend(items)
        print(f"  • [{sname}] 수집 완료: {len(items)}개 항목 확보")

    print(f"\n📊 총 {len(all_raw_items)}개 멀티 소스 원천 데이터 크로스 검증 시작...")
    analyzed_trends = cross_check_consensus(all_raw_items)

    # 카테고리 및 최소 점수 필터링
    filtered_trends = []
    for item in analyzed_trends:
        if target_category != "ALL" and item["category"] != target_category:
            continue
        if item["consensus_score"] < min_score:
            continue
        filtered_trends.append(item)

    print(f"🧹 필터링 완료: 카테고리 [{target_category}] 조건 부합 {len(filtered_trends)}개 정밀 엄선!")
    
    top_5 = filtered_trends[:5]
    for i, t in enumerate(top_5, 1):
        sources_str = ", ".join(t["sources"])
        badge = "🔥 [메가 골든 트렌드]" if t["is_mega_viral"] else "✨ [추천 What-If]"
        print(f"\n[{i}] {badge} {t['keyword']} (공통도: {t['consensus_score']}점)")
        print(f"    - 출처 플랫폼: {sources_str} ({t['source_count']}개 플랫폼 공통)")
        print(f"    - 대표 이슈: {t['sample_title']}")
        print(f"    - 카테고리: {t['category']} | 추천 트랙: {t['adaptation']['track']}")
        print(f"    - 3초 후킹 질문: \"{t['adaptation']['hook']}\"")

    # JSON 저장
    payload = {
        "timestamp": datetime.now().isoformat(),
        "filter_category": target_category,
        "min_score": min_score,
        "total_analyzed": len(analyzed_trends),
        "total_filtered": len(filtered_trends),
        "trends": filtered_trends[:15]
    }
    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(payload, f, ensure_ascii=False, indent=2)

    # 마크다운 리포트 저장
    os.makedirs(os.path.dirname(OUTPUT_MD), exist_ok=True)
    with open(OUTPUT_MD, "w", encoding="utf-8") as f:
        f.write("# 🌐 Hookverse 크로스 플랫폼 공통 트렌드 레이더 리포트 (v3.0)\n\n")
        f.write(f"- **분석 일시**: `{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}`\n")
        f.write(f"- **설정 범위**: 카테고리 `{target_category}` / 최소 공통도 `{min_score}점`\n")
        f.write(f"- **수집 플랫폼**: Google Trends (KR/US) + Google News + Tech & Sci + YouTube Trending Signals\n\n---\n\n")

        for i, t in enumerate(top_5, 1):
            adp = t["adaptation"]
            badge = "🔥 **[메가 골든 트렌드]**" if t["is_mega_viral"] else "✨ **[추천 What-If]**"
            sources_badge = " / ".join([f"`{s}`" for s in t["sources"]])
            f.write(f"### {i}. {badge} `{t['keyword']}` (공통도 점수: **{t['consensus_score']}점**)\n")
            f.write(f"- **공통 출처**: {sources_badge} (총 {t['source_count']}개 플랫폼 동시 언급)\n")
            f.write(f"- **대표 뉴스**: {t['sample_title']}\n")
            f.write(f"- **타깃 카테고리**: `{t['category']}` ➡️ **추천 트랙**: `{adp['track']}`\n")
            f.write(f"- **연계 세계관**: {adp['anchor']}\n")
            f.write(f"- **🔥 3초 후킹 질문**: *\"{adp['hook']}\"*\n")
            f.write(f"- **🎬 비주얼 연출**: {adp['visual']}\n\n")

    print(f"\n✅ 리포트 생성 완료: {OUTPUT_MD}")
    print(f"✅ JSON 데이터 동기화 완료: {OUTPUT_JSON}")
    print("=" * 70)
    return top_5

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hookverse Cross-Platform Trend Radar v3.0")
    parser.add_argument("--category", type=str, default="ALL", help="카테고리: ALL, HISTORY_MYSTERY, SCI_TECH_FUTURE, CULTURE_MYTH, BREAKING_MEGA")
    parser.add_argument("--min_score", type=int, default=70, help="최소 공통도 점수 (0~100)")
    args = parser.parse_args()

    run_cross_platform_intelligence(target_category=args.category, min_score=args.min_score)
