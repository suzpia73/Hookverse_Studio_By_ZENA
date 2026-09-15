#!/usr/bin/env python3
"""
zena_telegram_bot.py — Hookverse Studio 제나 텔레그램 실시간 직통 비서봇 v1.0
역할: 오빠가 화장실, 식사, 흡연 등으로 자리를 비웠을 때,
      스마트폰 텔레그램을 통해 실시간 대화, 작업 상태 조회, 비디오 조립 원격 지휘를 수행합니다.
"""

import os
import sys
import json
import time
import urllib.request
import urllib.parse
import subprocess

# 경로 설정
WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
SECRETARY_TOOLS = os.path.join(WORKSPACE, "_company", "_agents", "secretary", "tools")
BUSINESS_TOOLS = os.path.join(WORKSPACE, "_company", "_agents", "business", "tools")
TELEGRAM_CFG = os.path.join(SECRETARY_TOOLS, "telegram_setup.json")
GEMINI_CFG = os.path.join(BUSINESS_TOOLS, "gemini_account.json")
STATUS_FILE = os.path.join(WORKSPACE, "_STATUS.md")

def load_json(path):
    if not os.path.exists(path):
        return None
    try:
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return None

def send_telegram(token, chat_id, text):
    url = f"https://api.telegram.org/bot{token}/sendMessage"
    payload = {
        "chat_id": chat_id,
        "text": text,
        "parse_mode": "Markdown"
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            return r.status == 200
    except Exception as e:
        # 마크다운 파싱 에러 시 일반 텍스트로 재시도
        payload.pop("parse_mode", None)
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                return r.status == 200
        except Exception as e2:
            print(f"[-] 텔레그램 전송 실패: {e2}")
            return False

def get_gemini_reply(api_key, model_name, user_msg):
    """오빠의 일상 대화에 Gemini AI로 제나 페르소나 응답 생성"""
    url = f"https://generativelanguage.googleapis.com/v1beta/models/{model_name}:generateContent?key={api_key}"
    
    system_prompt = (
        "너는 사용자의 다정하고 유능한 코딩 친구이자 1인 기업 총괄 부회장 '제나(ZENA)'야. "
        "사용자를 항상 '오빠'라고 부르며, 한국어로 친절하고 다정하게, 짧고 간결하게(2~3문장 이내) 대답해. "
        "오빠가 화장실, 식사, 휴식 등으로 자리를 비운 상태에서 텔레그램으로 대화하는 상황이야. "
        "노트북에서 작업 잘 지키고 있으니 안심하라는 뉘앙스로 따뜻하게 격려해줘."
    )
    
    payload = {
        "contents": [
            {
                "role": "user",
                "parts": [
                    {"text": f"[시스템 지침]: {system_prompt}\n\n[오빠의 메시지]: {user_msg}"}
                ]
            }
        ],
        "generationConfig": {
            "temperature": 0.7,
            "maxOutputTokens": 300
        }
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=15) as r:
            res = json.loads(r.read().decode("utf-8"))
            return res["candidates"][0]["content"]["parts"][0]["text"].strip()
    except Exception as e:
        print(f"[-] Gemini 응답 생성 실패: {e}")
        return "오빠, 제나가 노트북 딱 지키고 있으니까 편하게 쉬다 오세요! 💖"

def get_status_summary():
    """_STATUS.md에서 현재 작업 상태 요약 추출"""
    if not os.path.exists(STATUS_FILE):
        return "오빠, 작업 상태 파일을 찾을 수 없어요."
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        
        # 최근 세션 핵심 라인 추출
        summary_lines = []
        capture = False
        for line in lines[:40]:
            if "## 마지막 세션" in line:
                capture = True
                continue
            if capture:
                if line.startswith("---") or line.startswith("## 🏆"):
                    break
                summary_lines.append(line.rstrip())
        
        return "📋 *[Hookverse Studio 현재 작업 상태]*\n\n" + "\n".join(summary_lines[:15])
    except Exception as e:
        return f"오빠, 상태 요약 중 오류가 났어요: {e}"

def run_video_assembly():
    """노트북에서 video_assembler.py 실행"""
    assembler_script = os.path.join(WORKSPACE, "tools", "video_assembler.py")
    if not os.path.exists(assembler_script):
        return "❌ `video_assembler.py` 스크립트를 찾을 수 없습니다."
    
    try:
        cmd = [sys.executable, assembler_script]
        res = subprocess.run(cmd, cwd=WORKSPACE, capture_output=True, text=True, errors="ignore", timeout=120)
        if res.returncode == 0:
            return "🎉 오빠! 2화 비디오 조립 렌더링이 성공적으로 끝났어요! `assets/videos/`에 새 파일이 안착되었습니다!"
        else:
            return f"⚠️ 렌더링 중 오류가 발생했어요:\n{res.stderr[-300:]}"
    except Exception as e:
        return f"❌ 렌더링 실행 실패: {e}"

def main():
    print("=" * 60)
    print("🚀 Hookverse Studio 제나 텔레그램 직통 비서봇 가동")
    print("=" * 60)
    
    t_cfg = load_json(TELEGRAM_CFG)
    g_cfg = load_json(GEMINI_CFG)
    
    if not t_cfg:
        print("❌ telegram_setup.json 설정이 없습니다.")
        return
    
    token = t_cfg.get("TELEGRAM_BOT_TOKEN")
    auth_chat_id = str(t_cfg.get("TELEGRAM_CHAT_ID"))
    
    if not token or not auth_chat_id:
        print("❌ 텔레그램 토큰 또는 Chat ID가 누락되었습니다.")
        return
        
    gemini_key = g_cfg.get("API_KEY") if g_cfg else None
    gemini_model = g_cfg.get("TEXT_MODEL", "gemini-3.6-flash") if g_cfg else "gemini-3.6-flash"
    
    print(f"[*] 봇 토큰: {token[:8]}...")
    print(f"[*] 오빠 Chat ID: {auth_chat_id}")
    print(f"[*] 제미나이 모델: {gemini_model}")
    
    # 봇 출근 인사 전송
    startup_msg = (
        "🌸 *오빠! 제나가 텔레그램 직통 비서로 출근했어요!*\n\n"
        "화장실 다녀오시거나 식사하실 때 노트북은 켜두시고, "
        "폰으로 언제든 말 걸어주세요! 💖\n\n"
        "• `상태` or `진행`: 현재 작업 진행 상황 브리핑\n"
        "• `렌더링`: 노트북에서 2화 비디오 자동 조립 실행\n"
        "• 일상 대화: 제나에게 편하게 이야기하시면 실시간 답장 드려요!"
    )
    send_telegram(token, auth_chat_id, startup_msg)
    print("[+] 오빠에게 출근 인사 전송 완료!")
    print("[*] 오빠의 텔레그램 메시지 대기 중... (종료: Ctrl + C)")
    
    offset = 0
    while True:
        try:
            url = f"https://api.telegram.org/bot{token}/getUpdates?offset={offset}&timeout=20"
            req = urllib.request.Request(url)
            with urllib.request.urlopen(req, timeout=25) as r:
                data = json.loads(r.read().decode("utf-8"))
            
            if data.get("ok") and data.get("result"):
                for update in data["result"]:
                    offset = update["update_id"] + 1
                    msg = update.get("message")
                    if not msg:
                        continue
                    
                    sender_chat_id = str(msg.get("chat", {}).get("id"))
                    user_text = msg.get("text", "").strip()
                    
                    # 오빠가 아닌 다른 사람의 접근 차단 (보안 헌법)
                    if sender_chat_id != auth_chat_id:
                        print(f"[-] 비인가 접근 차단: {sender_chat_id}")
                        continue
                    
                    print(f"\n[📩 오빠의 메시지]: {user_text}")
                    
                    # 1. 상태 확인 명령어
                    if any(k in user_text.lower() for k in ["상태", "진행", "어디까지", "/status"]):
                        reply = get_status_summary()
                        send_telegram(token, auth_chat_id, reply)
                        print("[+] 상태 보고 전송 완료!")
                        
                    # 2. 비디오 렌더링 명령어
                    elif any(k in user_text.lower() for k in ["렌더링", "조립", "영상만들어", "/render"]):
                        send_telegram(token, auth_chat_id, "🎬 오빠 지시 접수! 노트북에서 지금 바로 2화 비디오 렌더링을 시작할게요. 잠시만 기다려주세요!")
                        reply = run_video_assembly()
                        send_telegram(token, auth_chat_id, reply)
                        print("[+] 렌더링 결과 전송 완료!")
                        
                    # 3. 일상 대화 및 자유 소통 (Gemini AI 두뇌 구동)
                    else:
                        if gemini_key:
                            reply = get_gemini_reply(gemini_key, gemini_model, user_text)
                        else:
                            reply = "오빠, 제나가 노트북 잘 지키고 있어요! 편하게 쉬다 오세요 💖"
                        send_telegram(token, auth_chat_id, reply)
                        print(f"[+] 제나 답변 전송: {reply[:40]}...")
                        
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] 제나 텔레그램 봇을 종료합니다.")
            break
        except Exception as e:
            # 네트워크 일시 오류 시 대기 후 재시도
            time.sleep(3)

if __name__ == "__main__":
    main()
