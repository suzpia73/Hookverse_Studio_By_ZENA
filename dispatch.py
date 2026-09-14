import os
import sys
import re
import subprocess
from datetime import datetime

PYTHON_EXE = r"C:\Users\june2\AppData\Local\Programs\Python\Python314\python.exe"
BASE_DIR = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"

def dispatch(command: str):
    print(f"\n=======================================================")
    print(f"👑 KAIRA 에이전트 지휘 사령관 (Direct Dispatcher)")
    print(f"명령어: '{command}'")
    print(f"일시: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print(f"=======================================================\n")
    
    cmd_lower = command.lower()
    
    # 0. 사내 표준 제작 파이프라인 (SOP: Writer ➡️ Designer 순차 가동)
    if any(k in cmd_lower for k in ["파이프라인", "제작", "표준", "풀세트"]):
        print("👑 [CEO 레오 지휘] ➡️ 사내 표준 절차서(SOP)에 따라 2단계 제작 파이프라인을 가동합니다!")
        title = "IMF2화_자정의조흥은행"
        if "별주부" in command:
            title = "별주부전_SF_자라의음모"
        elif "심청" in command:
            title = "심청전_인당수의비밀"
        elif "imf" in cmd_lower or "조흥" in command:
            title = "IMF2화_자정의조흥은행"
            
        print(f"\n[1단계: Writer] 30초 대본 생성 도구 가동...")
        script_tool = os.path.join(BASE_DIR, "_company", "_agents", "writer", "tools", "short_script.py")
        res1 = subprocess.run([PYTHON_EXE, script_tool, title], capture_output=True, text=True)
        print(res1.stdout.strip())
        
        print(f"\n[2단계: Designer] 씬 1~4 시네마틱 범용 프롬프트 도구 가동...")
        prompt_tool = os.path.join(BASE_DIR, "_company", "_agents", "designer", "tools", "prompt_gen.py")
        res2 = subprocess.run([PYTHON_EXE, prompt_tool, title, "35mm", "야간_시네마틱"], capture_output=True, text=True)
        print(res2.stdout.strip())
        
        print(f"\n🎉 [CEO 레오] 사내 표준 제작 파이프라인 완료! (대본 ➡️ 프롬프트 물리 파일 안착 완결)\n")
        return

    # 1. 작가 (Writer) 단독 라우팅
    if any(k in cmd_lower for k in ["작가", "대본", "스크립트", "writer", "글써", "시나리오"]):
        print("🤖 [Writer 에이전트 호출] ➡️ 30초 숏폼 대본 생성 도구 가동 중...")
        match = re.search(r"['\"](.*?)['\"]", command)
        title = match.group(1) if match else "IMF_2화_IMF전날밤의비밀"
        
        script_tool = os.path.join(BASE_DIR, "_company", "_agents", "writer", "tools", "short_script.py")
        res = subprocess.run([PYTHON_EXE, script_tool, title], capture_output=True, text=True)
        print(res.stdout)
        if res.returncode == 0:
            print(f"🎉 Writer 업무 완료! 산출물이 assets/scripts/ 에 준비되었습니다.\n")
        return

    # 2. 디자이너 (Designer) 단독 라우팅
    elif any(k in cmd_lower for k in ["디자이너", "프롬프트", "그림", "이미지", "designer", "컷", "실사"]):
        print("🤖 [Designer 에이전트 호출] ➡️ G3 실사 프롬프트 생성 도구 가동 중...")
        match = re.search(r"['\"](.*?)['\"]", command)
        title = match.group(1) if match else "IMF2화_자정의조흥은행"
        
        prompt_tool = os.path.join(BASE_DIR, "_company", "_agents", "designer", "tools", "prompt_gen.py")
        res = subprocess.run([PYTHON_EXE, prompt_tool, title], capture_output=True, text=True)
        print(res.stdout)
        if res.returncode == 0:
            print(f"🎉 Designer 업무 완료! 산출물이 assets/prompts/ 에 준비되었습니다.\n")
        return

    # 3. 리서처 (Researcher) 라우팅
    elif any(k in cmd_lower for k in ["리서처", "조사", "트렌드", "키워드", "분석", "researcher"]):
        print("🤖 [Researcher 에이전트 호출] ➡️ 트렌드 & 키워드 분석 도구 가동 중...")
        match = re.search(r"['\"](.*?)['\"]", command)
        kw = match.group(1) if match else "숏폼 트렌드"
        
        trend_tool = os.path.join(BASE_DIR, "_company", "_agents", "researcher", "tools", "trend_scanner.py")
        res = subprocess.run([PYTHON_EXE, trend_tool, kw], capture_output=True, text=True)
        print(res.stdout)
        if res.returncode == 0:
            print(f"🎉 Researcher 업무 완료! 리포트가 _company/reports/ 에 준비되었습니다.\n")
        return

    # 4. 개발자 코다리 (Developer) 라우팅
    elif any(k in cmd_lower for k in ["개발", "코다리", "린트", "빌드", "developer"]):
        print("🤖 [코다리 에이전트 호출] ➡️ 린트 검사 도구 가동 중...")
        lint_tool = os.path.join(BASE_DIR, "_company", "_agents", "developer", "tools", "lint_test.py")
        res = subprocess.run([PYTHON_EXE, lint_tool], capture_output=True, text=True)
        print(res.stdout)
        return

    # 5. 기본: CEO 업무 지시
    else:
        print("🤖 [CEO 레오 호출] ➡️ 지시사항을 goals.md에 기록하고 전사 에이전트에게 하달합니다...")
        goals_file = os.path.join(BASE_DIR, "_company", "_shared", "goals.md")
        with open(goals_file, "a", encoding="utf-8") as f:
            f.write(f"\n\n### 📢 긴급 지시사항 ({datetime.now().strftime('%Y-%m-%d %H:%M')})\n- {command}\n")
        print(f"✅ goals.md에 긴급 미션으로 등록 완료! 전사 에이전트가 다음 사이클에서 실행합니다.\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        cmd = " ".join(sys.argv[1:])
        dispatch(cmd)
    else:
        print("사용법: python dispatch.py \"작가야, '별주부전 SF' 30초 대본 써와\"")
