import os
import json
import urllib.request
import urllib.parse
import datetime

HERE = os.path.dirname(os.path.abspath(__file__))
CONFIG_PATH = os.path.join(HERE, "_company", "_agents", "secretary", "tools", "google_calendar_write.json")
SESSION_CONFIG_PATH = os.path.join(HERE, "_company", "sessions", "_company", "_agents", "secretary", "tools", "google_calendar_write.json")

def main():
    print("====================================================")
    print("   Google Calendar OAuth 토큰 수동 발급 도구")
    print("====================================================")
    
    if not os.path.exists(CONFIG_PATH):
        print(f"❌ 설정 파일을 찾을 수 없습니다: {CONFIG_PATH}")
        return
        
    with open(CONFIG_PATH, "r", encoding="utf-8") as f:
        cfg = json.load(f)
        
    client_id = cfg.get("CLIENT_ID")
    client_secret = cfg.get("CLIENT_SECRET")
    
    if not client_id or not client_secret:
        print("❌ Client ID 또는 Client Secret이 비어 있습니다. 먼저 설정해 주세요.")
        return

    # 캘린더 권한 + 계정 이메일 조회를 위한 scope 설정
    scopes = [
        "https://www.googleapis.com/auth/calendar.events",
        "https://www.googleapis.com/auth/userinfo.email"
    ]
    scope_str = " ".join(scopes)
    redirect_uri = "http://127.0.0.1:5814/yt-oauth-callback"
    
    auth_params = {
        "client_id": client_id,
        "redirect_uri": redirect_uri,
        "response_type": "code",
        "scope": scope_str,
        "access_type": "offline",
        "prompt": "consent"
    }
    
    auth_url = "https://accounts.google.com/o/oauth2/v2/auth?" + urllib.parse.urlencode(auth_params)
    
    print("\n1. 아래 링크를 마우스 우클릭으로 복사하여 크롬/엣지 브라우저 주소창에 넣고 접속해 주세요:")
    print("-" * 80)
    print(auth_url)
    print("-" * 80)
    
    print("\n2. 구글 로그인 및 권한 부여를 완료해 주세요.")
    print("   (로그인 중 체크박스가 나오면 반드시 모두 체크해 주셔야 합니다!)")
    print("   (완료되면 브라우저 화면에 '사이트에 연결할 수 없음'이 뜨는 것이 정상입니다.)")
    
    print("\n3. 로그인이 완료된 후, 브라우저 주소창의 전체 URL을 복사하여 아래에 입력해 주세요.")
    url_input = input("주소창 URL 입력: ").strip()
    
    # code 파싱
    code = None
    if "code=" in url_input:
        parsed_url = urllib.parse.urlparse(url_input)
        params = urllib.parse.parse_qs(parsed_url.query)
        code = params.get("code", [None])[0]
    else:
        code = url_input
        
    if not code:
        print("❌ 입력된 URL에서 인증 코드(code)를 찾을 수 없습니다. 다시 시도해 주세요.")
        return
        
    print(f"\n✓ 인증 코드 획득 성공: {code[:10]}...")
    
    # 토큰 교환 요청
    token_url = "https://oauth2.googleapis.com/token"
    token_data = {
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri
    }
    
    print("⌛ Google OAuth 서버와 통신하여 Refresh Token을 발급받는 중...")
    try:
        data = urllib.parse.urlencode(token_data).encode("utf-8")
        req = urllib.request.Request(token_url, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")
        
        with urllib.request.urlopen(req, timeout=15) as r:
            res_body = r.read().decode("utf-8")
            res_data = json.loads(res_body)
            
        refresh_token = res_data.get("refresh_token")
        access_token = res_data.get("access_token")
        
        if not refresh_token:
            print("⚠️ 경고: Refresh Token이 발급되지 않았습니다. 기존에 로그인했던 기록이 남아있을 수 있습니다.")
            print("   혹시 작동에 문제가 있다면 Google 계정 보안 페이지에서 앱 권한을 삭제하고 다시 해보세요.")
            
        # 연결된 계정 정보 조회
        connected_email = "알 수 없음"
        try:
            info_url = f"https://www.googleapis.com/oauth2/v3/userinfo?access_token={access_token}"
            with urllib.request.urlopen(info_url, timeout=10) as info_r:
                info_data = json.loads(info_r.read().decode("utf-8"))
                connected_email = info_data.get("email", "알 수 없음")
        except Exception:
            pass
            
        # 설정 파일 갱신
        cfg["REFRESH_TOKEN"] = refresh_token or cfg.get("REFRESH_TOKEN", "")
        cfg["_CONNECTED_AS"] = connected_email
        cfg["_CONNECTED_AT"] = datetime.datetime.now().isoformat()
        
        with open(CONFIG_PATH, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
            
        # 세션용 설정 파일 동기화
        if os.path.exists(SESSION_CONFIG_PATH):
            with open(SESSION_CONFIG_PATH, "r", encoding="utf-8") as sf:
                scfg = json.load(sf)
            scfg["REFRESH_TOKEN"] = refresh_token or scfg.get("REFRESH_TOKEN", "")
            scfg["_CONNECTED_AS"] = connected_email
            scfg["_CONNECTED_AT"] = cfg["_CONNECTED_AT"]
            with open(SESSION_CONFIG_PATH, "w", encoding="utf-8") as sf:
                json.dump(scfg, sf, indent=2, ensure_ascii=False)
                
        print("\n====================================================")
        print("🎉 Google Calendar OAuth 연동 완료!")
        print(f"   연결 계정: {connected_email}")
        print(f"   설정 파일에 Refresh Token이 정상 저장되었습니다.")
        print("====================================================")
        
    except Exception as e:
        print(f"❌ 토큰 발급 실패: {e}")
        if hasattr(e, 'read'):
            print(f"   상세 에러: {e.read().decode('utf-8', errors='replace')}")

if __name__ == "__main__":
    main()
