import os
import sys
from datetime import datetime

def scan_trends(keyword="IMF 1997 타임슬립", platform="YouTube Shorts"):
    output_dir = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\_company\reports"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_kw = keyword.replace(" ", "_")
    filename = f"{safe_kw}_트렌드분석.md"
    filepath = os.path.join(output_dir, filename)
    
    content = f"""# 🔍 트렌드 & 바이럴 키워드 분석 리포트: {keyword}

- **분석 대상**: {keyword}
- **플랫폼**: {platform}
- **분석 일시**: {timestamp}
- **분석 에이전트**: Researcher (트렌드 & 데이터 리서처)

---

## 📈 1. 숏폼 알고리즘 바이럴 후크 포인트
1. **역사적 IF 가설**: "만약 1997년 IMF를 미리 알고 과거로 갔다면?" ➡️ 시청 지속시간(AVD) 85% 이상 기대.
2. **시각적 대조**: 1997년 아날로그 빗속 거리 vs 2026년 최신 스마트폰의 푸른빛 대비 효과.
3. **댓글 토론 유발**: "스마트폰 기지국 없는데 왜 뜸?", "나라면 달러부터 샀다" 등 알고리즘 폭발 댓글 유도.

## 🏷️ 2. 추천 해시태그 & 검색어 팩트셋
- `#HookverseStudio`, `#타임슬립`, `#1997IMF`, `#국가부도`, `#만약에`, `#shorts`
- 검색 연관 키워드: 1997년 11월 21일, 조흥은행, 한국통신 공중전화, 환율 폭등

## 🎯 3. 다음 에이전트 연계 액션
- ✍️ **Writer**: 위 분석 키워드를 바탕으로 3화 시나리오 대본 파일 생성 투입.
- 🎨 **Designer**: 1997년 아날로그 대비 스마트폰 푸른빛 극대화 프롬프트 작성.
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ 트렌드 리포트 파일 생성 성공: {filepath}")
    return filepath

if __name__ == "__main__":
    kw = sys.argv[1] if len(sys.argv) > 1 else "IMF 1997 타임슬립"
    scan_trends(kw)
