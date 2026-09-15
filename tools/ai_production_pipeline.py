#!/usr/bin/env python3
"""
ai_production_pipeline.py — Hookverse Studio AI 메타프롬프트 무인 제작 파이프라인 v1.0
철학: 벤치마킹 생활화 & 기준서·표준서·매뉴얼 기반 1인 기업 한 줄 업무 지시 시스템

역할:
1. 로컬에 축적된 4대 핵심 기준서(10대 시네마틱 연출헌법, 5-in-1 바이럴 헌법, 미스터비스트 후킹, 뉴라 세계관)를
   Gemini API의 시스템 메타프롬프트로 실시간 주입합니다.
2. 사용자가 어떤 키워드(주제)를 던지든:
   - [1단계: Writer AI] 8씬 가변 싱크(45초) 방송국급 숏폼 대본을 실시간 창작하여 assets/scripts/ 에 저장.
   - [2단계: Designer AI] 대본에 완벽 매칭되는 8씬 시네마틱 프롬프트 팩(35/50/85mm, G3 앵커락)을 창작하여 assets/prompts/ 에 저장.
   - [3단계: Voice AI] 대본의 순수 나레이션을 추출하여 edge-tts 고품질 뉴럴 음성(45초 MP3)으로 자동 합성하여 assets/audio/ 에 저장.
비용: 100% $0원 (Gemini 무료/저비용 티어 + edge-tts)
"""

import os
import sys
import re
import json
import asyncio
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
KP_DIR = os.path.join(WORKSPACE, "00_Raw", "knowledge_packs")
GEMINI_CFG_PATH = os.path.join(WORKSPACE, "_company", "_agents", "business", "tools", "gemini_account.json")
SCRIPTS_DIR = os.path.join(WORKSPACE, "assets", "scripts")
PROMPTS_DIR = os.path.join(WORKSPACE, "assets", "prompts")
AUDIO_DIR = os.path.join(WORKSPACE, "assets", "audio")

def read_file_safe(path):
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            return f.read()
    return ""

def load_gemini_config():
    if not os.path.exists(GEMINI_CFG_PATH):
        raise FileNotFoundError(f"Gemini 설정 파일을 찾을 수 없습니다: {GEMINI_CFG_PATH}")
    with open(GEMINI_CFG_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def call_gemini_generate(system_prompt: str, user_prompt: str) -> str:
    """Gemini API에 시스템 메타프롬프트와 유저 요청을 주입하여 실시간 텍스트 창작 호출"""
    cfg = load_gemini_config()
    api_key = cfg.get("API_KEY", "").strip()
    model = cfg.get("TEXT_MODEL", "gemini-3.6-flash").strip()
    
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
    
    payload = {
        "systemInstruction": {
            "parts": [{"text": system_prompt}]
        },
        "contents": [
            {
                "role": "user",
                "parts": [{"text": user_prompt}]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 4096
        }
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url, data=data,
        headers={"Content-Type": "application/json", "User-Agent": "HookverseAI/2.0"},
        method="POST"
    )
    
    with urllib.request.urlopen(req, timeout=30) as response:
        res_body = response.read().decode("utf-8")
        res_json = json.loads(res_body)
        candidates = res_json.get("candidates", [])
        if candidates:
            parts = candidates[0].get("content", {}).get("parts", [])
            if parts:
                return parts[0].get("text", "").strip()
    raise RuntimeError("Gemini API로부터 유효한 응답을 받지 못했습니다.")

def build_system_metaprompt() -> str:
    """로컬 4대 핵심 기준서를 읽어 최강의 메타프롬프트로 조립"""
    cinematic_rules = read_file_safe(os.path.join(KP_DIR, "시네마틱_10대_연속성_연출헌법.md"))
    viral_rules = read_file_safe(os.path.join(KP_DIR, "쇼츠_5in1_바이럴_스토리텔링_헌법.md"))
    mrbeast_rules = read_file_safe(os.path.join(KP_DIR, "MrBeast_후킹_로직.md"))
    neura_rules = read_file_safe(os.path.join(KP_DIR, "뉴라_NEURA_버추얼뮤즈_아이덴티티_팩.md"))
    
    metaprompt = f"""당신은 대한민국 1등 바이럴 영상 스튜디오 'Hookverse Studio'의 AI 총괄 크리에이티브 디렉터입니다.
당신은 아래의 4대 사내 공식 기준서·표준서·매뉴얼을 100% 체화하여 작업해야 합니다.

[기준서 1: 10대 시네마틱 연속성 연출헌법]
{cinematic_rules[:1500]}

[기준서 2: 5-in-1 바이럴 스토리텔링 헌법]
{viral_rules[:1500]}

[기준서 3: 미스터비스트 0.001% 후킹 바이블]
{mrbeast_rules[:1200]}

[기준서 4: 버추얼 뮤즈 뉴라(NEURA) 아이덴티티]
{neura_rules[:1200]}

[절대 작업 규칙]:
1. 영상 규격: 8씬 가변 타임코드 (총 44~46초 표준 규격).
2. 구조:
   - 파트 1 (00:00 ~ 22:10, 씬 1~4): 첫 3초 시각적 충격 후킹(VVSA) ➡️ 미스터리 발각 ➡️ 극한의 위기
   - 서스펜스 침묵 (22:10 ~ 23:60, 1.5초): 나레이션 음소거, 효과음만 흐르는 1.5초 서스펜스 정적
   - 파트 2 (23:60 ~ 45:20, 씬 5~8): 충격 반전 ➡️ 단서 공개 ➡️ 현실 일상 참여형 질문 후킹 (APVD 140% 무한루프)
3. 톤앤매너: 중저음 미스터리 다큐 스릴러 톤. 어설픈 설명조 배제, 현장감 넘치는 짧고 단호한 호흡.
"""
    return metaprompt

def run_pipeline(topic: str):
    print(f"\n==================================================================")
    print(f"🚀 [Hookverse Studio] AI 무인 파이프라인 가동: '{topic}'")
    print(f"==================================================================")
    
    os.makedirs(SCRIPTS_DIR, exist_ok=True)
    os.makedirs(PROMPTS_DIR, exist_ok=True)
    os.makedirs(AUDIO_DIR, exist_ok=True)
    
    safe_title = re.sub(r'[\\/*?:"<>| ]', '_', topic)
    metaprompt = build_system_metaprompt()
    
    # -------------------------------------------------------------
    # 1단계: Writer AI — 8씬 가변 싱크 방송국급 대본 창작
    # -------------------------------------------------------------
    print(f"[*] 1단계: Writer AI가 사내 4대 기준서를 기반으로 8씬 대본을 창작 중입니다...")
    writer_user_prompt = f"""다음 주제로 Hookverse Studio 공식 8씬 시네마틱 숏폼 대본을 작성해 주세요.
주제: "{topic}"

반드시 아래 포맷의 마크다운 형식으로만 작성하세요:
# 🎬 8씬 시네마틱 바이럴 숏폼 대본: {topic}

- **장르/세계관**: 타임슬립 / What If / 스릴러
- **등장인물**: 뉴라 (NEURA)
- **런타임**: 45.2초 (가변 싱크 8씬 규격)
- **권장 성우**: 손서현 (ko-KR-SunHiNeural, +20%, -2Hz 중저음 미스터리 딕션)

---

## 📜 8씬 나레이션 대본 & 사운드 큐

### [파트 1 : 카운트다운과 미스터리 (00:00 ~ 22:10)]
- 씬 1 (00:00 ~ 06:20 | 6.2s) : [비주얼 묘사]
  🗣️ "[성우가 읽을 실제 나레이션 대사]"
- 씬 2 (06:20 ~ 11:50 | 5.3s) : [비주얼 묘사]
  🗣️ "[성우가 읽을 실제 나레이션 대사]"
- 씬 3 (11:50 ~ 16:80 | 5.3s) : [비주얼 묘사]
  🗣️ "[성우가 읽을 실제 나레이션 대사]"
- 씬 4 (16:80 ~ 22:10 | 5.3s) : [비주얼 묘사]
  🗣️ "[성우가 읽을 실제 나레이션 대사]"

### [서스펜스 침묵 구간 (22:10 ~ 23:60 | 1.5초)]
- 🤫 (1.5초 서스펜스 정적 & 극적 효과음)

### [파트 2 : 충격적 반전 & 현실 후킹 (23:60 ~ 45:20)]
- 씬 5 (23:60 ~ 28:80 | 5.2s) : [비주얼 묘사]
  🗣️ "[성우가 읽을 실제 나레이션 대사]"
- 씬 6 (28:80 ~ 34:30 | 5.5s) : [비주얼 묘사]
  🗣️ "[성우가 읽을 실제 나레이션 대사]"
- 씬 7 (34:30 ~ 40:00 | 5.7s) : [비주얼 묘사]
  🗣️ "[성우가 읽을 실제 나레이션 대사]"
- 씬 8 (40:00 ~ 45:20 | 5.2s) : [비주얼 묘사]
  🗣️ "[성우가 읽을 실제 나레이션 대사 - 현실 참여형 질문]"
"""
    script_content = call_gemini_generate(metaprompt, writer_user_prompt)
    script_path = os.path.join(SCRIPTS_DIR, f"{safe_title}_대본.md")
    with open(script_path, "w", encoding="utf-8") as f:
        f.write(script_content)
    print(f"[+] ✅ 1단계 완료: 8씬 마스터 대본 안착 성공 ➡️ {script_path}")

    # -------------------------------------------------------------
    # 2단계: Designer AI — 8씬 시네마틱 프롬프트 팩 창작
    # -------------------------------------------------------------
    print(f"[*] 2단계: Designer AI가 대본과 G3 안면 앵커락을 결합해 8씬 프롬프트 팩을 설계 중입니다...")
    designer_user_prompt = f"""다음 대본을 정밀 분석하여, 각 씬별로 실제 AI 이미지 생성에 사용할 완벽한 영문 프롬프트 팩을 작성해 주세요.
대본 내용:
\"\"\"
{script_content}
\"\"\"

반드시 아래 규칙을 엄수하세요:
1. 뉴라 묘사 시 'G3 Master Face Anchor Lock' 필수 적용:
   - 24-year-old Korean woman, natural skin texture, two distinct beauty marks (one below left eye, one near right collarbone), wet wavy black hair.
2. 씬별 카메라 화각 배분:
   - 씬 1: 35mm Wide Cine Lens (공간감, 시대 배경)
   - 씬 2: 50mm Bust / Medium Shot
   - 씬 3: 85mm Macro Extreme Close-up (핵심 소품 접사)
   - 씬 4: 50mm Medium Close-up
   - 씬 5: 35mm Low-Angle / Wide Shot
   - 씬 6: 85mm Top-Down Close-up
   - 씬 7: 50mm Back-View / Silhouette Long Shot
   - 씬 8: 85mm First-Person POV Macro Shot
3. 형식:
   # 🎨 Hookverse Studio {topic} 8씬 시네마틱 프롬프트 팩
   - 씬 1 (타임코드) | [한국어 제목]
     [영문 실사 프롬프트]
   ... 씬 8까지 반복
"""
    prompt_content = call_gemini_generate(metaprompt, designer_user_prompt)
    prompt_path = os.path.join(PROMPTS_DIR, f"{safe_title}_8씬_완성프롬프트.txt")
    with open(prompt_path, "w", encoding="utf-8") as f:
        f.write(prompt_content)
    print(f"[+] ✅ 2단계 완료: 8씬 시네마틱 프롬프트 팩 안착 성공 ➡️ {prompt_path}")

    # -------------------------------------------------------------
    # 3단계: Voice AI — 대사 추출 및 edge-tts 성우 음성(MP3) 자동 합성
    # -------------------------------------------------------------
    print(f"[*] 3단계: Voice AI가 순수 나레이션을 추출하여 고품질 성우 음성(MP3)을 합성 중입니다...")
    dialogues = re.findall(r'🗣️\s*["\']?([^"\']+)["\']?', script_content)
    if not dialogues:
        dialogues = re.findall(r'"([^"]{5,})"', script_content)
    
    full_speech = " ".join([d.strip() for d in dialogues])
    if full_speech:
        audio_path = os.path.join(AUDIO_DIR, f"{safe_title}_성우음성.mp3")
        
        async def make_tts():
            import edge_tts
            comm = edge_tts.Communicate(full_speech, "ko-KR-SunHiNeural", rate="+20%", pitch="-2Hz")
            await comm.save(audio_path)
            
        asyncio.run(make_tts())
        print(f"[+] ✅ 3단계 완료: 성우 음성 MP3 안착 성공 ➡️ {audio_path}")
    else:
        print(f"[-] 대사 추출 실패로 오디오 합성을 건너뜁니다.")

    print(f"\n==================================================================")
    print(f"🎉 [성공] '{topic}' 한 줄 지시로 8씬 대본 ➡️ 프롬프트 ➡️ 오디오 완성!")
    print(f"==================================================================")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        user_topic = " ".join(sys.argv[1:])
    else:
        user_topic = "IMF 3화: 유령을 쫓는 자들"
    run_pipeline(user_topic)
