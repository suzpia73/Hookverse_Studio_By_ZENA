import os
import sys
import argparse
import subprocess

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
PIPELINE_SCRIPT = os.path.join(WORKSPACE, "tools", "ai_production_pipeline.py")

def generate_script(title="IMF3화_유령을쫓는자들", genre="타임슬립/What If/스릴러"):
    cmd = [sys.executable, PIPELINE_SCRIPT, f"{title} ({genre})"]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    print(res.stdout)
    if res.returncode != 0:
        print("[-] 에러 발생:", res.stderr)
    return os.path.join(WORKSPACE, "assets", "scripts", f"{title}_대본.md")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hookverse AI Script Generator")
    parser.add_argument("title", nargs="?", default="IMF3화_유령을쫓는자들")
    parser.add_argument("genre", nargs="?", default="타임슬립/What If/스릴러")
    args = parser.parse_args()
    generate_script(args.title, args.genre)

---

## 📸 8단 실사 컷 연계 (G3 앵커 락 & 소품 연속성 100% 준수)
- 씬 1 (35mm Wide): 중앙 금융 금고 폴리스 라인 및 취재진 롱샷
- 씬 2 (50mm Bust): 텅 빈 금고를 바라보며 경악하는 수사관 POV
- 씬 3 (85mm Macro): 바닥에 놓인 장부 위 붉은 잉크 'NEURA' 서명 클로즈업
- 씬 4 (50mm Medium): 무전기 들고 긴급 수배령 내리는 요원 바스트
- 씬 5 (35mm Side): 안개 낀 한강 다리 난간에 선 트렌치코트 뉴라 실루엣
- 씬 6 (85mm Macro): 미래 스마트폰 액정 위 환율 폭등 경보 및 배터리 1%
- 씬 7 (50mm Cine): 2026 현대 모니터 속 1997년 비밀 외환 로그 분석
- 씬 8 (85mm POV): 현대 스마트폰 뱅킹 앱 달러 잔고 확인 클로즈업
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ [Writer] 대본 파일 생성 성공: {filepath}")
    return filepath

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hookverse 30s Viral Script Generator")
    parser.add_argument("title", nargs="?", default="IMF_전날밤의비밀")
    parser.add_argument("genre", nargs="?", default="타임슬립/What If")
    parser.add_argument("--body", "-b", help="Custom script body text", default=None)
    args = parser.parse_args()
    generate_script(args.title, args.genre, script_body=args.body)

