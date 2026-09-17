import os
from PIL import Image

upload_dir = r"C:\Users\june2\.gemini\antigravity-ide\brain\6f64338c-c4bf-4316-a1b8-3503cde43325\.user_uploaded"
files = os.listdir(upload_dir)

for f in sorted(files):
    p = os.path.join(upload_dir, f)
    try:
        im = Image.open(p)
        print(f"File: {f} | Size: {im.size} | Mode: {im.mode}")
    except Exception as e:
        print(f"File: {f} | Error: {e}")
