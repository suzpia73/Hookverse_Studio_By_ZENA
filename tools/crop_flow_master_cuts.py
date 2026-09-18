import os
from PIL import Image

ARTIFACT_DIR = r"C:\Users\june2\.gemini\antigravity-ide\brain\1ad897b3-7fb9-4802-9eb1-6708fdd7e0ee"
OUTPUT_DIR = os.path.abspath("assets/images/IMF2화")
os.makedirs(OUTPUT_DIR, exist_ok=True)

CUT_SOURCES = [
    {
        "cut": 1,
        "src": os.path.join(ARTIFACT_DIR, "cut_check_4_1789737116573.png"),
        "dest": os.path.join(OUTPUT_DIR, "IMF전날밤의비밀_ep02_cut01.jpg"),
        "name": "Cut 01 : 골목 질주 및 뒤돌아보는 훅"
    },
    {
        "cut": 2,
        "src": os.path.join(ARTIFACT_DIR, "cut02_view_1789737026153.png"),
        "dest": os.path.join(OUTPUT_DIR, "IMF전날밤의비밀_ep02_cut02.jpg"),
        "name": "Cut 02 : 골목 은신 & 스마트폰 1% 배터리"
    },
    {
        "cut": 3,
        "src": os.path.join(ARTIFACT_DIR, "cut_check_7_1789737212418.png"),
        "dest": os.path.join(OUTPUT_DIR, "IMF전날밤의비밀_ep02_cut03.jpg"),
        "name": "Cut 03 : 사냥꾼 따돌리는 빗속 전력 질주"
    },
    {
        "cut": 4,
        "src": os.path.join(ARTIFACT_DIR, "google_flow_editor_view_1789736813767.png"),
        "dest": os.path.join(OUTPUT_DIR, "IMF전날밤의비밀_ep02_cut04.jpg"),
        "name": "Cut 04 : 부스 안 은색 전화기 본체+코일선+통화 충격"
    }
]

def process():
    for item in CUT_SOURCES:
        src = item["src"]
        dest = item["dest"]
        print(f"Processing {item['name']}...")
        if not os.path.exists(src):
            print(f"[-] Source not found: {src}")
            continue
            
        img = Image.open(src)
        w, h = img.size
        print(f"    Original screenshot size: {w}x{h}")
        
        # In Google Flow editor view:
        # Header bar: ~80px
        # Bottom prompt bar: ~100px
        # Center image is displayed vertically.
        # Let's inspect center bounding box of the 9:16 vertical image.
        # Flow editor typically centers the 9:16 image between x ~ 370 and x ~ 750 (approx ~380px wide)
        # or fits vertically from y ~ 85 to y ~ 830 (approx 745px high).
        # At 9:16 aspect ratio: 745 * 9 / 16 ≈ 419px wide.
        # Center X ≈ w / 2 ≈ 686 (if w=1372).
        
        # Let's find precise bounding box by scanning non-background pixels if background is dark/black (#0b0f19 or similar)
        # Or fixed vertical box:
        # Top: 80, Bottom: 835 (height = 755).
        # Width for 9:16: 755 * 9 / 16 = 424.
        # Center X: 1372 / 2 - 120? Let's check where the image sits in screenshot:
        # The main preview image sits in the center-left.
        # Let's crop dynamically by finding the image borders:
        # We can crop the inner 9:16 region.
        
        # Let's do a smart crop or exact bounding:
        # From the screenshots, the image top is around y=85, bottom is around y=835 (height ~ 750).
        # Left is around x=370, right is around x=760.
        # Let's write out the crop and resize to 1080x1920:
        
        # Let's sample pixels or use precise box:
        # Let's check image bounding box:
        box = (370, 85, 760, 835) # approx 390x750 (approx 9:17.3, close to 9:16)
        cropped = img.crop(box)
        
        # Resize to standard 1080x1920 (9:16) with high-quality Lanczos:
        resized = cropped.resize((1080, 1920), Image.Resampling.LANCZOS)
        resized.save(dest, "JPEG", quality=95)
        print(f"[+] Successfully saved {dest} (1080x1920)")

if __name__ == "__main__":
    process()
