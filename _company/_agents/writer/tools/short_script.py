import os
import sys
import json
from datetime import datetime

def generate_script(title="미스터리_숏폼", genre="타임슬립/What If", characters="뉴라 (NEURA)"):
    output_dir = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\scripts"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_title = title.replace(" ", "_")
    filename = f"{safe_title}_30초대본.md"
    filepath = os.path.join(output_dir, filename)
    
    content = f"""# 🎬 30초 5-in-1 바이럴 숏폼 대본: {title}

- **장르/세계관**: {genre}
- **등장인물**: {characters}
- **생성 일시**: {timestamp}
- **권장 성우**: 손서현 (중저음 미스터리 딕션)
- **자막 스타일**: 네온 퍼플 테두리 + 화이트 폰트 (300pt)

---

## 📜 30초 나레이션 대본 (손서현 톤)

[0~5초 : 컷 1 - 오프닝 충격 후크]
세상이 기억하는 역사는 모두 거짓이었습니다.
{title}의 그날 밤, 멈춰버린 시계탑 아래 한 여자가 서 있었습니다.

[6~12초 : 컷 2 - 비밀의 발각]
그녀의 손에 들린 화면엔 미래의 기록이 선명하게 떠올랐고,
차갑게 젖은 거리의 사람들은 수군거리기 시작했습니다.

[13~18초 : 컷 3 - 카운트다운 긴장감]
통신망은 끊겼지만, 폰 안의 데이터는 똑똑히 가리키고 있었습니다.
"파멸의 순간까지 남은 시간은 단 10초."

[19~24초 : 컷 4 - 서스펜스 클리프행어 엔딩]
그 순간, 골목 어둠 너머로 검은 그림자들이 다가오기 시작했습니다.
그녀는 과연 역사의 톱니바퀴를 멈출 수 있을까요?
아니면...

---

## 📸 4단 실사 컷 기획
- 컷 1 (0~5초): 오프닝 배경 와이드 샷 + 서서히 줌인
- 컷 2 (6~12초): 뉴라 클로즈업 (G3 안면 앵커락 유지) + 심장박동 바운스
- 컷 3 (13~18초): 스마트폰 화면 디테일 (한글 속보 타임스탬프)
- 컷 4 (19~24초): 다가오는 추적자 실루엣 + 충격적인 엔딩 리액션
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ 대본 파일 생성 성공: {filepath}")
    return filepath

if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "심청전_SF각색"
    genre = sys.argv[2] if len(sys.argv) > 2 else "전래동화/신화 SF각색"
    generate_script(title, genre)
