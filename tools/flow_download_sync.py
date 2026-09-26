r"""
Google Flow 2K 원본 이미지 자동 감지 및 프로젝트 폴더 핫싱크 도구
(c) 2026 Hookverse Studio by ZENA

Flow에서 2K 업스케일링 다운로드 시 D:\Downlods 또는 C:\Users\june2\Downloads에
생성되는 최신 원본 이미지를 감지하여 assets/images/ 및 production_packages/ 로 자동 이동/복사합니다.
"""

import os
import shutil
import time
import glob
from pathlib import Path

# 모니터링 대상 다운로드 디렉토리 목록
DOWNLOAD_DIRS = [
    r"D:\Downlods",
    os.path.expanduser(r"~\Downloads"),
]

# 타겟 목적지 폴더
PROJECT_ROOT = Path(r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2")
TARGET_IMAGE_DIR = PROJECT_ROOT / "assets" / "images" / "IMF2화"
TARGET_PKG_DIR = PROJECT_ROOT / "assets" / "production_packages" / "IMF_2화__IMF_전날_밤의_비밀"

def find_latest_flow_download(max_age_seconds=600):
    """최근 max_age_seconds(기본 10분) 내에 생성된 Flow 다운로드 이미지 탐색"""
    candidates = []
    now = time.time()
    
    for d in DOWNLOAD_DIRS:
        if not os.path.exists(d):
            continue
        # 이미지 확장자 탐색
        for ext in ("*.png", "*.jpg", "*.jpeg", "*.webp"):
            for f in glob.glob(os.path.join(d, ext)):
                try:
                    mtime = os.path.getmtime(f)
                    if now - mtime <= max_age_seconds:
                        candidates.append((f, mtime, os.path.getsize(f)))
                except OSError:
                    continue
                    
    if not candidates:
        return None
        
    # 가장 최신 파일 반환
    candidates.sort(key=lambda x: x[1], reverse=True)
    return candidates[0]

def sync_flow_2k_image(cut_number=2, custom_name=None):
    """최신 Flow 다운로드 이미지를 우리 프로젝트 폴더로 핫싱크"""
    latest = find_latest_flow_download()
    if not latest:
        print(r"[!] 최근 다운로드된 이미지를 찾을 수 없습니다. (D:\Downlods 및 Downloads 확인)")
        return False
        
    src_file, mtime, size = latest
    print(f"[*] 감지된 최신 원본 파일: {src_file} ({size} bytes, {time.ctime(mtime)})")
    
    # 목적지 파일명 결정
    if custom_name:
        filename = custom_name
    else:
        filename = f"IMF2화_Cut0{cut_number}_2K원본_업스케일.png"
        
    TARGET_IMAGE_DIR.mkdir(parents=True, exist_ok=True)
    TARGET_PKG_DIR.mkdir(parents=True, exist_ok=True)
    
    dest1 = TARGET_IMAGE_DIR / filename
    dest2 = TARGET_PKG_DIR / f"0{cut_number}_Cut0{cut_number}_2K원본_업스케일.png"
    
    # 복사 진행
    shutil.copy2(src_file, dest1)
    shutil.copy2(src_file, dest2)
    
    print(f"[+] 성공적으로 핫싱크 완료!")
    print(f"    1) {dest1}")
    print(f"    2) {dest2}")
    return True

if __name__ == "__main__":
    import sys
    cut_num = int(sys.argv[1]) if len(sys.argv) > 1 else 2
    sync_flow_2k_image(cut_number=cut_num)
