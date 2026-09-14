import urllib.request
import re

url = "https://store.kyobobook.co.kr/handwriting/font"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"})
try:
    with urllib.request.urlopen(req, timeout=5) as resp:
        html = resp.read().decode("utf-8", errors="ignore")
        files = re.findall(r'https?://[^\s"\'\(\)]+\.(?:zip|ttf|otf)', html)
        print("Files found:", files)
        matches = re.findall(r'https?://[^\s"\'\(\)]+2019[^\s"\'\(\)]*', html)
        print("2019 matches:", matches)
except Exception as e:
    print("Error:", e)
