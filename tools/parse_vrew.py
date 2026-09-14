import urllib.request
import re

url = "https://vrew.ai/try/assets/index-DYzqoPJ3.js"
req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
try:
    with urllib.request.urlopen(req, timeout=10) as resp:
        content = resp.read().decode("utf-8", errors="ignore")
        # search for font url or s3/cloudfront
        m = re.findall(r'https?://[^\s"\'<>]+\.woff2?', content)
        print("Woff URLs in Vrew:", list(set(m))[:10])
        # search for font cdn
        cdn = re.findall(r'https?://[^\s"\'<>]*font[^\s"\'<>]*', content)
        print("Font endpoints:", list(set(cdn))[:10])
except Exception as e:
    print("Error:", e)
