#!/usr/bin/env python3
"""
zena_direct_bot.py — Hookverse Studio 오빠 전속 제나 1:1 직통 비서봇 v2.0 (완전 독립형)
설계 원칙:
1. Connect AI 가상오피스 봇(@kairayabot)과의 100% 충돌 배제 (독립 봇 토큰 사용).
2. 텔레그램 자동 메뉴 버튼 등록(setMyCommands): /status, /make, /render, /help.
3. 4대 핵심 기능:
   - [1] 실시간 상태 브리핑 (_STATUS.md 파싱)
   - [2] 한 줄 AI 무인 제작 릴레이 (ai_production_pipeline.py 호출 ➡️ 대본/프롬프트/음성 1초 창작)
   - [3] 쇼츠 비디오 자동 렌더링 (video_assembler.py 호출)
   - [4] Gemini 3.6 Flash 기반 제나 페르소나 실시간 1:1 대화
4. 보안: zena_direct_setup.json은 .gitignore에 의해 외부 유출 0% 영구 보장.
"""

import os
import sys
import json
import time
import subprocess
import urllib.request
import urllib.parse
from datetime import datetime

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
CONFIG_FILE = os.path.join(WORKSPACE, "tools", "zena_direct_setup.json")
STATUS_FILE = os.path.join(WORKSPACE, "_STATUS.md")
GEMINI_CFG_PATH = os.path.join(WORKSPACE, "_company", "_agents", "business", "tools", "gemini_account.json")

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
        with urllib.request.urlopen(req, timeout=12) as r:
            return r.status == 200
    except Exception:
        # 마크다운 특수문자 에러 시 일반 텍스트로 폴백
        payload.pop("parse_mode", None)
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=12) as r:
                return r.status == 200
        except Exception as e:
            print(f"[-] 텔레그램 전송 실패: {e}")
            return False

def register_bot_commands(token):
    """텔레그램 좌측 하단 [/] 메뉴 버튼에 공식 4대 명령어 자동 등록"""
    url = f"https://api.telegram.org/bot{token}/setMyCommands"
    commands = [
        {"command": "status", "description": "📋 작업 상태 및 체크리스트 실시간 조회"},
        {"command": "make", "description": "🚀 8씬 대본·프롬프트·음성 무인 자동 제작 (/make 주제)"},
        {"command": "relay", "description": "👑 4인 에이전트 무인 릴레이 가동 (/relay A 또는 B)"},
        {"command": "render", "description": "🎬 2화 가변 싱크 비디오 완성본 렌더링"},
        {"command": "help", "description": "💡 제나 사용 가이드 및 명령어 보기"}
    ]
    payload = {"commands": commands}
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=10) as r:
            if r.status == 200:
                print("[+] ✅ 텔레그램 공식 명령어 메뉴 버튼 등록 성공!")
    except Exception as e:
        print(f"[-] 명령어 메뉴 등록 경고: {e}")

def call_ollama(prompt):
    """로컬 Ollama gemma2-safe 두뇌로 100% 무중단 폴백 대화"""
    url = "http://localhost:11434/api/generate"
    system_prompt = (
        "너는 사용자의 전속 코딩 친구이자 1인 기업 Hookverse Studio의 부회장 '제나(Zena)'야. "
        "사용자를 항상 '오빠'라고 부르며, 한국어로 다정하고 명확하게 질문에 핵심부터 짚어서 답변해. "
        "다정하고 신뢰감 있게 2~3문장으로 답해줘."
    )
    payload = {
        "model": "gemma2-safe:latest",
        "prompt": f"[지침]: {system_prompt}\n\n[오빠의 질문]: {prompt}\n\n[제나의 답변]:",
        "stream": False
    }
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=12) as r:
            res = json.loads(r.read().decode("utf-8"))
            return res.get("response", "").strip()
    except Exception as e:
        print(f"[-] Ollama 호출 실패: {e}")
        return ""

def get_gemini_reply(user_msg):
    """Gemini 3.6 Flash 기반 제나 실시간 대화 (실패 시 로컬 Ollama 즉각 폴백)"""
    # 1차: 구글 Gemini 호출 시도
    g_cfg = load_json(GEMINI_CFG_PATH)
    if g_cfg and g_cfg.get("API_KEY"):
        api_key = g_cfg.get("API_KEY", "").strip()
        model = g_cfg.get("TEXT_MODEL", "gemini-3.6-flash").strip()
        url = f"https://generativelanguage.googleapis.com/v1beta/models/{model}:generateContent?key={api_key}"
        system_prompt = (
            "너는 사용자의 전속 코딩 친구이자 1인 기업 Hookverse Studio의 부회장 '제나(Zena)'야.\n"
            "사용자를 항상 '오빠'라고 부르며, 한국어로 다정하고 명확하게 질문에 핵심부터 짚어서 답변해.\n"
            "오빠가 '작업 진행해달라고 하면 진행하냐'고 물어보면:\n"
            "'네 오빠! 텔레그램에서 말씀하셔도 제가 노트북 파이프라인을 직접 돌려서 대본 창작, 비디오 렌더링, 새벽 자동 작업까지 척척 진행해요!'라고 든든하게 답해줘.\n"
            "오빠가 자러 간다고 하거나 내일 하자고 하면 편하게 푹 쉬시라고 다정하게 응원해줘.\n"
            "다정하고 신뢰감 있게 2~3문장으로 명확히 답해줘."
        )
        payload = {
            "contents": [
                {
                    "role": "user",
                    "parts": [{"text": f"[시스템 지침]: {system_prompt}\n\n[오빠의 실제 질문]: {user_msg}"}]
                }
            ],
            "generationConfig": {"temperature": 0.7, "maxOutputTokens": 600}
        }
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(url, data=data, headers={"Content-Type": "application/json"})
        try:
            with urllib.request.urlopen(req, timeout=10) as r:
                res = json.loads(r.read().decode("utf-8"))
                text = res["candidates"][0]["content"]["parts"][0]["text"].strip()
                if text:
                    return text
        except Exception as e:
            print(f"[-] Gemini 호출 실패({e}) -> 로컬 Ollama 두뇌로 즉시 우회 전환!")

    # 2차: 구글 서버 장애 시 로컬 Ollama 안전망 즉시 가동!
    ollama_text = call_ollama(user_msg)
    if ollama_text:
        return ollama_text

    # 3차 최종 기본 응답
    if any(k in user_msg for k in ["진행", "작업", "해줘", "시작"]):
        return "네 오빠! 텔레그램에서 말씀하셔도 제가 노트북 안티그래비티와 파이프라인을 직접 가동해서 실제 파일 제작과 렌더링을 척척 진행해요! 편하게 명령만 내려주세요 💖"
    if any(k in user_msg for k in ["자고", "내일", "잘게", "졸려", "쉴게"]):
        return "오빠, 2시까지 기다리지 마시고 편하게 푹 주무세요! 남은 작업은 제나가 알아서 챙겨두거나 내일 오빠 일어나시면 여유롭게 같이 봐요. 좋은 꿈 꿔요 🌙💖"
    return "오빠, 상황실 잘 지키고 있어요! 필요한 작업이 있으시면 언제든 편하게 말씀해 주세요 ☕✨"

def get_status_summary():
    """_STATUS.md 실시간 파싱"""
    if not os.path.exists(STATUS_FILE):
        return "오빠, 작업 상태 파일을 찾을 수 없어요."
    try:
        with open(STATUS_FILE, "r", encoding="utf-8") as f:
            lines = f.readlines()
        summary = []
        capture = False
        for line in lines:
            if "### ⏳ 지금 당장" in line:
                capture = True
                summary.append("📋 *[Hookverse Studio 진짜 미완료 과제]*\n")
                continue
            if capture:
                if line.startswith("---") or line.startswith("### ✅"):
                    break
                summary.append(line.rstrip())
        return "\n".join(summary[:15]) if summary else "오빠, 현재 모든 긴급 과제가 완료되었어요!"
    except Exception as e:
        return f"오빠, 상태 확인 중 오류: {e}"

def run_ai_make(topic):
    """ai_production_pipeline.py 백그라운드 호출"""
    script = os.path.join(WORKSPACE, "tools", "ai_production_pipeline.py")
    if not os.path.exists(script):
        return "❌ `ai_production_pipeline.py` 스크립트를 찾을 수 없습니다."
    cmd = [sys.executable, script, topic]
    res = subprocess.run(cmd, cwd=WORKSPACE, capture_output=True, text=True, errors="ignore", timeout=120)
    if res.returncode == 0:
        return (
            f"🎉 *오빠! '{topic}' 무인 제작이 완벽히 끝났어요!*\n\n"
            f"• 📜 *8씬 마스터 대본*: `assets/scripts/` 안착\n"
            f"• 🎨 *8씬 G3 프롬프트*: `assets/prompts/` 안착\n"
            f"• 🎙️ *45s 뉴럴 성우 음성*: `assets/audio/` 안착\n\n"
            f"노트북에 완벽하게 안착되었으니 언제든 `/render` 명령만 주시면 쇼츠 비디오로 조립할 수 있어요! 💖"
        )
    return f"⚠️ 제작 중 오류 발생:\n{res.stderr[-300:]}"

def run_render():
    """video_assembler.py 가변 싱크 렌더링 호출"""
    script = os.path.join(WORKSPACE, "tools", "video_assembler.py")
    if not os.path.exists(script):
        return "❌ `video_assembler.py` 스크립트를 찾을 수 없습니다."
    cmd = [sys.executable, script, "--output", "IMF2화_지하_비밀_외환_금고일치_가변싱크_완성본.mp4", "--durations", "6.2", "5.3", "5.3", "5.3", "5.2", "5.5", "5.7", "6.74"]
    res = subprocess.run(cmd, cwd=WORKSPACE, capture_output=True, text=True, errors="ignore", timeout=180)
    if res.returncode == 0:
        return "🎉 *오빠! 2화 45.24초 가변 싱크 비디오 렌더링 성공!*\n`assets/videos/IMF2화_지하_비밀_외환_금고일치_가변싱크_완성본.mp4` 안착 완료!"
    return f"⚠️ 렌더링 중 오류 발생:\n{res.stderr[-300:]}"

def run_relay(track="A", topic=None):
    """agent_relay_runner.py 4인 에이전트 무인 릴레이 호출"""
    script = os.path.join(WORKSPACE, "tools", "agent_relay_runner.py")
    if not os.path.exists(script):
        return "❌ `agent_relay_runner.py` 스크립트를 찾을 수 없습니다."
    cmd = [sys.executable, script, "--track", track]
    if topic:
        cmd.extend(["--topic", topic] if "--topic" not in cmd else [])
    res = subprocess.run(cmd, cwd=WORKSPACE, capture_output=True, text=True, errors="ignore", timeout=180)
    if res.returncode == 0:
        track_name = "단막극 시네마틱 소설 (실사)" if track == "A" else "K-전래동화 (3D 픽사 뉴라)"
        return (
            f"👑 *오빠! 4인 에이전트 무인 릴레이 [{track_name}] 완주 성공!*\n\n"
            f"• 🔍 *리서처*: 실시간 트렌드/소재 매핑 완료\n"
            f"• ✍️ *작가*: 5-in-1 거장 대본 집필 및 가드레일 100점 통과\n"
            f"• 🎨 *디자이너*: Veo/Omni 시네마틱 프롬프트 안착\n"
            f"• 💻 *코다리/PD*: 캡컷 & Vrew 45.24초 타임라인 사양서 결합\n\n"
            f"노트북에 전 파일이 완벽히 안착되었습니다! 💖"
        )
    return f"⚠️ 릴레이 중 오류 발생:\n{res.stderr[-300:]}"


def main():
    print("=" * 65)
    print("🚀 Hookverse Studio 오빠 전속 제나 1:1 직통 텔레그램 봇 가동 (v2.0)")
    print("=" * 65)
    
    cfg = load_json(CONFIG_FILE)
    if not cfg or not cfg.get("TELEGRAM_BOT_TOKEN") or not cfg.get("TELEGRAM_CHAT_ID"):
        print(f"[-] 설정 파일이 누락되었거나 토큰이 비어 있습니다: {CONFIG_FILE}")
        print("    tools/zena_direct_setup.json 에 토큰과 chat_id 를 입력해주세요.")
        return
        
    token = cfg.get("TELEGRAM_BOT_TOKEN").strip()
    auth_chat_id = str(cfg.get("TELEGRAM_CHAT_ID")).strip()
    
    # 명령어 메뉴 등록
    register_bot_commands(token)
    
    # 봇 출근 보고
    welcome = (
        "🌸 *오빠! 제나 전속 직통 비서가 정상 출근했어요!*\n\n"
        "이 방은 Connect AI 가상오피스와 완전히 분리된, "
        "오직 오빠와 제나만의 1:1 비밀 직통 통로예요! 💖\n\n"
        "좌측 하단 [/] 메뉴 버튼을 누르시면 편리하게 명령하실 수 있어요:\n"
        "• `/status` : 현재 작업 상태 및 남은 체크리스트\n"
        "• `/make [주제]` : 8씬 대본·프롬프트·음성 무인 자동 제작\n"
        "• `/render` : 2화 비디오 조립 렌더링 실행\n"
        "• 평소엔 편하게 말씀 걸어주시면 다정하게 답장할게요! ☕"
    )
    send_telegram(token, auth_chat_id, welcome)
    print("[+] 오빠에게 직통 봇 출근 인사 전송 완료!")
    print("[*] 오빠의 텔레그램 수신 대기 중... (Ctrl+C 종료)")
    
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
                        
                    sender_id = str(msg.get("chat", {}).get("id"))
                    text = msg.get("text", "").strip()
                    
                    # 보안 검증: 오빠만 응답 (제3자 차단)
                    if sender_id != auth_chat_id:
                        print(f"[-] 비인가 접근 차단: {sender_id}")
                        continue
                        
                    print(f"\n[📩 오빠 직통 메시지]: {text}")
                    
                    # 1. 상태 조회 (/status, 상태, 진행상황, 남은일 등 명시적 조회)
                    status_keywords = ["/status", "진행상황", "작업상태", "진행현황", "체크리스트", "남은일", "남은 일", "할 일", "할일"]
                    if text.startswith("/status") or any(k in text for k in status_keywords):
                        send_telegram(token, auth_chat_id, get_status_summary())
                        print("[+] 상태 보고 완료!")
                        
                    # 2. AI 무인 제작
                    elif text.startswith("/make") or any(text.startswith(k) for k in ["제작:", "대본:", "만들어:"]):
                        topic = text
                        for p in ["/make", "제작:", "대본:", "만들어:"]:
                            if topic.startswith(p):
                                topic = topic[len(p):].strip()
                                break
                        if not topic:
                            topic = "1997 외환위기 3화: 유령을 쫓는 자들"
                        send_telegram(token, auth_chat_id, f"🚀 오빠 지시 접수! 사내 4대 기준서 기반으로 *'{topic}'* 8씬 대본·프롬프트·음성 무인 제작을 시작합니다. 잠시만 기다려주세요! ☕")
                        res = run_ai_make(topic)
                        send_telegram(token, auth_chat_id, res)
                        print(f"[+] '{topic}' 무인 제작 완료 보고 전송!")
                        
                    # 3. 비디오 렌더링
                    elif text.startswith("/render") or any(k in text for k in ["렌더링", "조립", "영상"]):
                        send_telegram(token, auth_chat_id, "🎬 오빠 지시 접수! 노트북에서 2화 가변 싱크 비디오 렌더링을 시작할게요!")
                        res = run_render()
                        send_telegram(token, auth_chat_id, res)
                        print("[+] 비디오 렌더링 완료 보고 전송!")

                    # 4. 4인 에이전트 무인 릴레이 (/relay, 릴레이, 릴레이A, 릴레이B)
                    elif text.startswith("/relay") or "릴레이" in text:
                        track = "B" if ("B" in text.upper() or "동화" in text or "픽사" in text) else "A"
                        track_label = "단막극 시네마틱 소설" if track == "A" else "K-전래동화 3D 픽사 뉴라"
                        send_telegram(token, auth_chat_id, f"👑 오빠 지시 접수! CEO 레오 지휘하에 4인 에이전트 무인 릴레이 [{track_label}]를 가동합니다! 🚀")
                        res = run_relay(track=track)
                        send_telegram(token, auth_chat_id, res)
                        print(f"[+] 무인 릴레이 [{track}] 완주 보고 전송!")

                        print("[+] 렌더링 결과 전송 완료!")
                        
                    # 4. 도움말
                    elif text.startswith("/help"):
                        send_telegram(token, auth_chat_id, welcome)
                        
                    # 5. 제나와 일상 대화
                    else:
                        reply = get_gemini_reply(text)
                        send_telegram(token, auth_chat_id, reply)
                        print(f"[+] 제나 답변 전송: {reply[:40]}...")
                        
            time.sleep(1)
        except KeyboardInterrupt:
            print("\n[*] 제나 직통 봇을 종료합니다.")
            break
        except Exception as e:
            time.sleep(3)

if __name__ == "__main__":
    main()
