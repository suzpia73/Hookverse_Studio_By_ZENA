# -*- coding: utf-8 -*-
"""
오빠 검토용 최신 생성 이미지 3종을 assets/images/review/ 에 복사하는 스크립트
"""
import os
import shutil

BRAIN_DIR = r"C:\Users\june2\.gemini\antigravity-ide\brain\f4180318-3846-4324-a558-26b558f47513"
REVIEW_DIR = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review"

os.makedirs(REVIEW_DIR, exist_ok=True)

MAPPING = {
    "imf_ep02_cut02_perfect_neura_1789556934502.jpg": "review_cut02_neura.jpg",
    "imf_ep02_cut03_running_to_booth_1789557427251.jpg": "review_cut03_running.jpg",
    "imf_ep02_cut04_trembling_eyes_call_1789557451531.jpg": "review_cut04_call.jpg"
}

for src_name, dst_name in MAPPING.items():
    src_path = os.path.join(BRAIN_DIR, src_name)
    dst_path = os.path.join(REVIEW_DIR, dst_name)
    if os.path.exists(src_path):
        shutil.copy2(src_path, dst_path)
        print(f"✅ 복사 완료: {dst_name}")
    else:
        print(f"❌ 원본 없음: {src_name}")

print("Review images ready!")
