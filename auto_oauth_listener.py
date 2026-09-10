import http.server
import socketserver
import urllib.parse
import urllib.request
import json
import os
import sys

PORT = 5814
HERE = os.path.dirname(os.path.abspath(__file__))
CALENDAR_CFG = os.path.join(HERE, "_company", "_agents", "secretary", "tools", "google_calendar_write.json")
YOUTUBE_OAUTH = os.path.join(HERE, "_company", "_agents", "youtube", "oauth.local.json")

class OAuthCallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path == "/yt-oauth-callback":
            params = urllib.parse.parse_qs(parsed.query)
            code = params.get("code", [None])[0]
            if code:
                # Exchange token
                success = exchange_and_save(code)
                self.send_response(200)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.end_headers()
                if success:
                    html = """<html><body style="font-family:sans-serif; text-align:center; padding:50px; background:#f0fdf4;">
                    <h1 style="color:#16a34a;">🎉 Google OAuth 연동 성공!</h1>
                    <p style="font-size:18px;">새 토큰이 성공적으로 발급되어 자동 저장되었습니다.<br>이 브라우저 탭을 닫으셔도 됩니다!</p>
                    </body></html>"""
                else:
                    html = """<html><body style="font-family:sans-serif; text-align:center; padding:50px; background:#fef2f2;">
                    <h1 style="color:#dc2626;">❌ 토큰 발급 실패</h1>
                    <p style="font-size:18px;">토큰 교환 중 오류가 발생했습니다. 터미널 로그를 확인해 주세요.</p>
                    </body></html>"""
                self.wfile.write(html.encode("utf-8"))
                
                # Exit server after response
                def kill():
                    import time
                    time.sleep(1)
                    os._exit(0)
                import threading
                threading.Thread(target=kill).start()
            else:
                self.send_response(400)
                self.end_headers()
                self.wfile.write(b"No code parameter found.")
        else:
            self.send_response(404)
            self.end_headers()

    def log_message(self, format, *args):
        pass

def exchange_and_save(code):
    try:
        with open(CALENDAR_CFG, "r", encoding="utf-8") as f:
            cfg = json.load(f)
        client_id = cfg["CLIENT_ID"]
        client_secret = cfg["CLIENT_SECRET"]
        redirect_uri = f"http://127.0.0.1:{PORT}/yt-oauth-callback"

        token_url = "https://oauth2.googleapis.com/token"
        token_data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "code": code,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri
        }
        data = urllib.parse.urlencode(token_data).encode("utf-8")
        req = urllib.request.Request(token_url, data=data, method="POST")
        req.add_header("Content-Type", "application/x-www-form-urlencoded")

        with urllib.request.urlopen(req, timeout=15) as r:
            res = json.loads(r.read().decode("utf-8"))

        refresh_token = res.get("refresh_token")
        if not refresh_token:
            print("❌ No refresh_token returned")
            return False

        # Save to calendar
        cfg["REFRESH_TOKEN"] = refresh_token
        cfg["_CONNECTED_AS"] = "suzpia73@gmail.com"
        with open(CALENDAR_CFG, "w", encoding="utf-8") as f:
            json.dump(cfg, f, indent=2, ensure_ascii=False)
        print("✅ Saved to google_calendar_write.json")

        # Save to youtube oauth.local.json
        if os.path.exists(YOUTUBE_OAUTH):
            with open(YOUTUBE_OAUTH, "r", encoding="utf-8") as f:
                yt = json.load(f)
            yt["refresh_token"] = refresh_token
            yt["client_id"] = client_id
            yt["client_secret"] = client_secret
            with open(YOUTUBE_OAUTH, "w", encoding="utf-8") as f:
                json.dump(yt, f, indent=2, ensure_ascii=False)
            print("✅ Saved to youtube oauth.local.json")

        print("🎉 Google OAuth Auto-Exchange 100% COMPLETE!")
        return True
    except Exception as e:
        print(f"❌ exchange_and_save error: {e}")
        return False

if __name__ == "__main__":
    server = socketserver.TCPServer(("127.0.0.1", PORT), OAuthCallbackHandler)
    server.allow_reuse_address = True
    print(f"🚀 Waiting for OAuth callback on http://127.0.0.1:{PORT}/yt-oauth-callback ...")
    server.handle_request()
