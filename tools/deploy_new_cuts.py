# -*- coding: utf-8 -*-
"""
IMF 2화 3대 핵심 컷(씬 2, 씬 4, 씬 8) 정식 에셋 폴더 교체 배포 스크립트
"""
import os
import shutil

SOURCE_DIR = r"C:\Users\june2\.gemini\antigravity-ide\brain\f4180318-3846-4324-a558-26b558f47513"
TARGET_DIR = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\IMF2화"

# 매핑 정의
MAPPING = {
    "imf_ep02_cut02_neura_rain_1789553973964.jpg": "IMF전날밤의비밀_ep02_cut02.jpg",
    "imf_ep02_cut04_neura_phone_1789553990614.jpg": "IMF전날밤의비밀_ep02_cut04.jpg",
    "imf_ep02_cut08_female_hand_dollar_1789554007068.jpg": "IMF전날밤의비밀_ep02_cut08.jpg"
}

def deploy():
    print("=== [배포 시작] IMF 2화 3대 컷 정식 교체 ===")
    os.makedirs(TARGET_DIR, exist_ok=True)
    
    for src_name, tgt_name in MAPPING.items():
        src_path = os.path.join(SOURCE_DIR, src_name)
        tgt_path = os.path.join(TARGET_DIR, tgt_name)
        
        if os.path.exists(src_path):
            shutil.copy2(src_path, tgt_path)
            size_kb = os.path.getsize(tgt_path) / 1024
            print(f"✅ 교체 성공: {tgt_name} ({size_kb:.1f} KB)")
        else:
            print(f"❌ 원본 없음: {src_path}")
            
    print("=== [배포 완료] 3대 컷 안착 완료! ===")

if __name__ == "__main__":
    deploy()
