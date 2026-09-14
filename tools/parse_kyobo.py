import urllib.request
import re

js_url = "https://contents.kyobobook.co.kr/display/next/ui-store/build-1789089189/_next/static/chunks/app/handwriting/ink/font/page-a8c89106d7367ecb.js"
req = urllib.request.Request(js_url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        content = resp.read().decode("utf-8", errors="ignore")
        matches = re.findall(r'https?://[^\s"\'<>]+\.(?:zip|ttf|otf)', content)
        print("Direct font files in JS:", matches)
        matches_2019 = re.findall(r'.{0,50}2019.{0,50}', content)
        for m in matches_2019[:10]:
            print("2019 snippet:", m)
except Exception as e:
    print(e)
