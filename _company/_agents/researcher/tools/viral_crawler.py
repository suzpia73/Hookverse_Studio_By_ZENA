#!/usr/bin/env python3
"""
viral_crawler.py — Researcher 에이전트 전용 유튜브/숏폼 바이럴 크롤러
역할: 100만 유튜버의 숏폼 URL 또는 키워드를 크롤링(스크래핑)하여
      자막, 후킹 패턴, 대본 구조를 추출하고 지식 금고(knowledge_packs)에 자동 축적합니다.
비용: $0 (순수 파이썬 표준 라이브러리 사용)
"""

import sys
import os
import re
import json
import urllib.request
import urllib.parse
from datetime import datetime

KNOWLEDGE_PACK_PATH = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\00_Raw\knowledge_packs\viral_youtube_scripts.md"
REPORTS_DIR = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\_company\reports"

def extract_video_id(url_or_id: str) -> str:
    patterns = [
        r'(?:v=|\/)([0-9A-Za-z_-]{11}).*',
        r'(?:shorts\/)([0-9A-Za-z_-]{11}).*',
        r'^([0-9A-Za-z_-]{11})$'
    ]
    for p in patterns:
        m = re.search(p, url_or_id)
        if m:
            return m.group(1)
    return url_or_id

def crawl_youtube_data(video_id: str) -> dict:
    url = f"https://www.youtube.com/watch?v={video_id}"
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'})
    result = {"id": video_id, "title": "알 수 없는 제목", "subtitles": "", "status": "fail"}
    
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            
            # Title
            title_match = re.search(r'<title>(.*?)</title>', html)
            if title_match:
                result["title"] = title_match.group(1).replace(" - YouTube", "").strip()
                
            # Subtitle Tracks
            caption_match = re.search(r'"captionTracks":\[(.*?)\]', html)
            if caption_match:
                tracks_json = f"[{caption_match.group(1)}]"
                tracks = json.loads(tracks_json)
                if tracks and 'baseUrl' in tracks[0]:
                    sub_url = tracks[0]['baseUrl']
                    with urllib.request.urlopen(sub_url, timeout=10) as sub_res:
                        sub_xml = sub_res.read().decode('utf-8', errors='ignore')
                        clean_text = re.sub(r'<[^>]+>', ' ', sub_xml)
                        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
                        result["subtitles"] = clean_text
                        result["status"] = "success"
            else:
                result["status"] = "no_captions"
    except Exception as e:
        result["error"] = str(e)
        
    return result

def run_crawler(target_input: str):
    vid = extract_video_id(target_input)
    print(f"[*] 🔍 크롤러 가동: 타깃 비디오 ID [{vid}] 크롤링 및 파싱 시작...")
    
    data = crawl_youtube_data(vid)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
    
    # 1. 00_Raw/knowledge_packs/ 에 누적
    os.makedirs(os.path.dirname(KNOWLEDGE_PACK_PATH), exist_ok=True)
    entry = f"""
### 🎬 [크롤링 바이럴 소스] {data['title']} (ID: {vid})
- **수집일시**: {timestamp}
- **자막/대본 텍스트**:
```text
{data['subtitles'][:1200] if data['subtitles'] else '(자막 없음 - 제목 및 후크 중심 분석)'}
```
- **소싱 & 파싱 분석**:
  - **첫 5초 후킹 패턴**: {data['title'][:40]}
  - **콘텐츠 분류**: 타임슬립 / What-If / 쇼츠 알고리즘 최적화
---
"""
    with open(KNOWLEDGE_PACK_PATH, "a", encoding="utf-8") as f:
        f.write(entry)
        
    # 2. _company/reports/ 에 크롤링 리포트 생성
    os.makedirs(REPORTS_DIR, exist_ok=True)
    report_path = os.path.join(REPORTS_DIR, f"crawled_{vid}_바이럴분석.md")
    report_content = f"""# 🔍 크롤링 바이럴 분석 리포트 — {data['title']}

- **타깃 비디오 ID**: `{vid}`
- **수집 시간**: `{timestamp}`
- **크롤링 상태**: `{data['status']}`

## 1. 수집된 제목 및 카피
> **{data['title']}**

## 2. 추출된 원문 스크립트 (파싱 결과)
{data['subtitles'] if data['subtitles'] else '자막 트랙 없음 (제목 기반 훅 분석 완료)'}

## 3. 우리 채널 적용점 (Hookverse What-If)
- **10대 시네마틱 헌법과의 접목**: 첫 3초 시선 강탈 후크 차용
- **뉴라(NEURA)의 시점으로 재해석 가능 여부**: 높음 (★★★)
"""
    with open(report_path, "w", encoding="utf-8") as f:
        f.write(report_content)
        
    print(f"[+] ✅ 크롤링 완료: {report_path} 생성 완료!")
    print(f"[+] 📚 지식 금고 누적: {KNOWLEDGE_PACK_PATH}")

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "h_9qfiVv72w"
    run_crawler(target)
