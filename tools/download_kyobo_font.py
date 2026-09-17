import urllib.request
import os

url = "https://cdn.jsdelivr.net/gh/projectnoonnu/noonfonts_20-04@1.0/KyoboHand.woff"
os.makedirs("assets/fonts", exist_ok=True)
dest = "assets/fonts/KyoboHand.woff"
try:
    urllib.request.urlretrieve(url, dest)
    print("Downloaded:", os.path.exists(dest), "Size:", os.path.getsize(dest))
except Exception as e:
    print("Error:", e)
