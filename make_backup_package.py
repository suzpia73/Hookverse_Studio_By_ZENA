import os
import shutil
import datetime

# 백업 소스 및 대상 설정
WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO"
BACKUP_ROOT = r"D:\HOOKVERSE-BACKUP"
TIMESTAMP = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
TARGET_DIR = os.path.join(BACKUP_ROOT, f"HOOKVERSE_BACKUP_{TIMESTAMP}")
LATEST_LINK_DIR = os.path.join(BACKUP_ROOT, "LATEST")

print(f"=== Hookverse Studio 백업 시작 ===")
print(f"대상 디렉토리: {TARGET_DIR}")

os.makedirs(TARGET_DIR, exist_ok=True)

# 1. 01_API_KEYS_AND_AUTH
dir_auth = os.path.join(TARGET_DIR, "01_API_KEYS_AND_AUTH")
os.makedirs(dir_auth, exist_ok=True)

files_to_auth = [
    (os.path.join(WORKSPACE, "test_all_keys.py"), "test_all_keys.py"),
    (os.path.join(WORKSPACE, "exchange_token.py"), "exchange_token.py"),
    (os.path.join(WORKSPACE, "_company", "_agents", "youtube", "oauth.local.json"), "youtube_oauth.local.json"),
]

for src, name in files_to_auth:
    if os.path.exists(src):
        dst = os.path.join(dir_auth, name)
        shutil.copy2(src, dst)
        print(f"[AUTH] 복사 완료: {name}")
    else:
        print(f"[AUTH] 파일 없음 (건너뜀): {src}")

# 2. 02_COMPANY_AGENTS (_company)
dir_company = os.path.join(TARGET_DIR, "02_COMPANY_AGENTS")
src_company = os.path.join(WORKSPACE, "_company")
if os.path.exists(src_company):
    def ignore_patterns(d, files):
        ignored = []
        for f in files:
            if f in [".git", "__pycache__", ".connect-ai-dev.log"]:
                ignored.append(f)
        return ignored
    shutil.copytree(src_company, os.path.join(dir_company, "_company"), ignore=ignore_patterns, dirs_exist_ok=True)
    print(f"[COMPANY] _company 폴더 백업 완료")

# 3. 03_MODELS_AND_CONFIGS
dir_configs = os.path.join(TARGET_DIR, "03_MODELS_AND_CONFIGS")
os.makedirs(dir_configs, exist_ok=True)

files_to_config = [
    (os.path.join(WORKSPACE, "Modelfile"), "Modelfile"),
    (os.path.join(WORKSPACE, "Modelfile.hookverse"), "Modelfile.hookverse"),
    (os.path.join(WORKSPACE, ".vscode", "settings.json"), "vscode_settings.json"),
    (os.path.join(WORKSPACE, "apply_safe_model.py"), "apply_safe_model.py"),
    (os.path.join(WORKSPACE, "test_gemma2_safe.py"), "test_gemma2_safe.py"),
    (os.path.join(WORKSPACE, "clear_ceo_memory.py"), "clear_ceo_memory.py"),
    (os.path.join(WORKSPACE, "auto_runner.py"), "auto_runner.py"),
    (os.path.join(WORKSPACE, "HOOKVERSE_AutoStart.bat"), "HOOKVERSE_AutoStart.bat"),
    (os.path.join(WORKSPACE, "company_state.json"), "company_state.json"),
    (os.path.join(WORKSPACE, "rag_mode.txt"), "rag_mode.txt"),
]

for src, name in files_to_config:
    if os.path.exists(src):
        dst = os.path.join(dir_configs, name)
        shutil.copy2(src, dst)
        print(f"[CONFIG] 복사 완료: {name}")
    else:
        print(f"[CONFIG] 파일 없음 (건너뜀): {src}")

# 4. 04_WEBAPP_SOURCE (my-youtube, node_modules 및 .next 제외)
dir_webapp = os.path.join(TARGET_DIR, "04_WEBAPP_SOURCE")
src_webapp = os.path.join(WORKSPACE, "my-youtube")
if os.path.exists(src_webapp):
    def ignore_webapp(d, files):
        ignored = []
        for f in files:
            if f in ["node_modules", ".next", ".git", "build", "dist"]:
                ignored.append(f)
        return ignored
    shutil.copytree(src_webapp, os.path.join(dir_webapp, "my-youtube"), ignore=ignore_webapp, dirs_exist_ok=True)
    print(f"[WEBAPP] my-youtube 소스 백업 완료 (node_modules 제외)")

# 5. 05_JENA_BRAIN (제나 규칙, 상태, 기억)
dir_brain = os.path.join(TARGET_DIR, "05_JENA_BRAIN")
os.makedirs(dir_brain, exist_ok=True)

skill_path = r"C:\Users\june2\.gemini\config\skills\hookverse_system\SKILL.md"
files_to_brain = [
    (os.path.join(WORKSPACE, "_STATUS.md"), "_STATUS.md"),
    (os.path.join(WORKSPACE, "AGENTS.md"), "AGENTS.md"),
    (os.path.join(WORKSPACE, "CODEX_NOTES.md"), "CODEX_NOTES.md"),
    (os.path.join(WORKSPACE, "[제나 전용 기억 금고 바로가기].md"), "[제나 전용 기억 금고 바로가기].md"),
    (skill_path, "SKILL.md"),
]

for src, name in files_to_brain:
    if os.path.exists(src):
        dst = os.path.join(dir_brain, name)
        shutil.copy2(src, dst)
        print(f"[JENA] 복사 완료: {name}")
    else:
        print(f"[JENA] 파일 없음 (건너뜀): {src}")

src_agents_dir = os.path.join(WORKSPACE, ".agents")
if os.path.exists(src_agents_dir):
    shutil.copytree(src_agents_dir, os.path.join(dir_brain, ".agents"), dirs_exist_ok=True)
    print(f"[JENA] .agents 폴더 백업 완료")

# 6. BACKUP_MANIFEST.md 작성
manifest_content = f"""# Hookverse Studio 백업 매니페스트 (제나 생성)

- **백업 일시**: {datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")}
- **백업 폴더**: `{TARGET_DIR}`
- **목적**: 클린 재시작(HOOKVERSE_STUDIO_V2 구축)을 위한 핵심 자산 안전 보관

## 백업 패키지 구성 내용

### 1. `01_API_KEYS_AND_AUTH/`
- `test_all_keys.py`: 6대 외부 API(Gemini, Telegram, Google Calendar, YouTube Data, YouTube Analytics, PayPal) 통합 진단기 및 키셋
- `youtube_oauth.local.json`: 정상 인증된 유튜브 OAuth Refresh Token
- `exchange_token.py`: 토큰 갱신 유틸리티

### 2. `02_COMPANY_AGENTS/`
- Connect AI 1인 기업 에이전트 프롬프트 및 도구 전체 (`_company/`)
- CEO, Secretary, Developer, Editor, Designer, Researcher, YouTube, Instagram 등

### 3. `03_MODELS_AND_CONFIGS/`
- `Modelfile`: MX250 2GB VRAM 안정 구동을 위한 gemma2-safe 정의 (num_ctx 2048)
- `vscode_settings.json`: Connect AI ollamaModel=gemma2:2b 설정
- `auto_runner.py`, `HOOKVERSE_AutoStart.bat`: 자동화 스케줄러

### 4. `04_WEBAPP_SOURCE/`
- `my-youtube/`: 대용량 `node_modules`와 `.next` 빌드 찌꺼기를 제외한 순수 소스 코드

### 5. `05_JENA_BRAIN/`
- `SKILL.md`: 6대 API 연동 역사 및 디버깅 노하우 (제나 전용 기억)
- `_STATUS.md`: 진행 상태 로그
- `AGENTS.md`, `.agents/`: 제나 행동 지침 및 워크스페이스 규칙

---

## 새 프로젝트 복원 가이드 (다음 단계)
1. 4개 프로그램 재설치 완료 후 `d:\\HOOKVERSE-SYSTEM\\HOOKVERSE_STUDIO_V2` 폴더 생성
2. 위 백업 패키지에서 필요한 설정 및 코드를 새 폴더로 이관
3. 새 GitHub 저장소 연결
4. `python test_all_keys.py` 로 6대 API 즉시 정상 검증!
"""

with open(os.path.join(TARGET_DIR, "BACKUP_MANIFEST.md"), "w", encoding="utf-8") as f:
    f.write(manifest_content)

print(f"[MANIFEST] 매니페스트 작성 완료: BACKUP_MANIFEST.md")
print(f"=== 백업 패키지 생성 완료! ===")
