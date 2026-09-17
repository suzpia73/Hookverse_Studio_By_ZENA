import urllib.request
import os

urls = [
    "https://image.kyobobook.co.kr/ink/resource/font/KyoboHandwriting2019.ttf",
    "http://image.kyobobook.co.kr/prom/2020/general/200325_handwriting/KyoboHandwriting2019.ttf",
    "https://image.kyobobook.co.kr/prom/2020/general/200325_handwriting/KyoboHandwriting2019.zip",
    "https://cdn.jsdelivr.net/gh/webfontworld/kyobo/KyoboHandwriting2019.ttf"
]

for url in urls:
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
        dest = os.path.join("assets", "fonts", os.path.basename(url))
        with urllib.request.urlopen(req) as resp, open(dest, 'wb') as out:
            out.write(resp.read())
        print(f"Success: {url} -> {dest} ({os.path.getsize(dest)} bytes)")
        break
    except Exception as e:
        print(f"Failed {url}: {e}")
