#!/usr/bin/env python3
"""
stock_video_fetcher.py — Hookverse Studio 무료 스톡 영상 자동 다운로드 모듈 v1.0
영감: GPT PARK 채널 'ShortsSmith' 파이프라인 (2026-09-21 내재화)

[기능]
- Pexels API (무료) / Pixabay API (무료) 에서 씬 키워드에 맞는 HD 스톡 영상 자동 검색 & 다운로드
- 배경 영상이 없을 때 assets/bgvideos/ 에 자동으로 채워주는 역할
- AI 이미지 생성(Flow)과 병행하여 배경 B롤 소재로 사용 가능

[API 키 발급 방법]
- Pexels: https://www.pexels.com/api/ → 무료 가입 후 즉시 발급
- Pixabay: https://pixabay.com/api/docs/ → 무료 가입 후 즉시 발급

[사용 방법]
  python tools/stock_video_fetcher.py "1997 Seoul rain night street"
  또는 파이프라인에서 import 하여 호출:
  from tools.stock_video_fetcher import fetch_stock_videos_for_scene
"""

import os
import sys
import json
import urllib.request
import urllib.parse
import urllib.error
import shutil
from datetime import datetime

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
GEMINI_CFG_PATH = os.path.join(WORKSPACE, "_company", "_agents", "business", "tools", "gemini_account.json")
BGVIDEO_DIR = os.path.join(WORKSPACE, "assets", "bgvideos")


# ──────────────────────────────────────────────
# 🔑 설정 로더
# ──────────────────────────────────────────────

def load_config() -> dict:
    if os.path.exists(GEMINI_CFG_PATH):
        with open(GEMINI_CFG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    return {}


# ──────────────────────────────────────────────
# 🎥 엔진 1: Pexels (무료 HD 스톡 영상)
# ──────────────────────────────────────────────

def fetch_from_pexels(keyword: str, save_path: str, per_page: int = 3) -> list:
    """
    Pexels 무료 API로 키워드 검색 후 최상위 영상 다운로드.

    API 키 발급:
      1. https://www.pexels.com/api/ 접속
      2. 무료 가입 후 API 키 즉시 발급
      3. gemini_account.json 에 "PEXELS_API_KEY": "YOUR_KEY" 추가
    """
    cfg = load_config()
    api_key = cfg.get("PEXELS_API_KEY", "").strip()

    if not api_key:
        print("  ⚠️  [Pexels] API 키 없음 → Pixabay로 전환")
        return []

    encoded = urllib.parse.quote(keyword)
    url = f"https://api.pexels.com/videos/search?query={encoded}&per_page={per_page}&size=medium"

    req = urllib.request.Request(
        url,
        headers={"Authorization": api_key, "User-Agent": "HookverseAI/2.0"}
    )

    downloaded = []
    try:
        with urllib.request.urlopen(req, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            videos = data.get("videos", [])

            for i, video in enumerate(videos):
                # 가장 해상도 높은 파일 선택 (HD 우선)
                files = sorted(
                    video.get("video_files", []),
                    key=lambda x: x.get("width", 0),
                    reverse=True
                )
                if not files:
                    continue

                video_url = files[0].get("link", "")
                if not video_url:
                    continue

                safe_kw = keyword.replace(" ", "_")[:30]
                filename = f"pexels_{safe_kw}_{i+1}.mp4"
                filepath = os.path.join(save_path, filename)

                print(f"  📥 [Pexels] 다운로드 중: {filename}")
                with urllib.request.urlopen(video_url, timeout=60) as vresp:
                    with open(filepath, "wb") as f:
                        shutil.copyfileobj(vresp, f)
                downloaded.append(filepath)
                print(f"  ✅ [Pexels] 완료: {filepath}")

    except urllib.error.HTTPError as e:
        print(f"  ❌ [Pexels] HTTP {e.code}: {e.reason}")
    except Exception as e:
        print(f"  ❌ [Pexels] 오류: {e}")

    return downloaded


# ──────────────────────────────────────────────
# 🎥 엔진 2: Pixabay (무료 스톡 영상 — 백업)
# ──────────────────────────────────────────────

def fetch_from_pixabay(keyword: str, save_path: str, per_page: int = 3) -> list:
    """
    Pixabay 무료 API로 키워드 검색 후 영상 다운로드.

    API 키 발급:
      1. https://pixabay.com/api/docs/ 접속
      2. 무료 가입 후 API 키 즉시 발급
      3. gemini_account.json 에 "PIXABAY_API_KEY": "YOUR_KEY" 추가
    """
    cfg = load_config()
    api_key = cfg.get("PIXABAY_API_KEY", "").strip()

    if not api_key:
        print("  ⚠️  [Pixabay] API 키 없음")
        return []

    encoded = urllib.parse.quote(keyword)
    url = (
        f"https://pixabay.com/api/videos/"
        f"?key={api_key}&q={encoded}&per_page={per_page}&video_type=film&safesearch=true"
    )

    downloaded = []
    try:
        with urllib.request.urlopen(url, timeout=15) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            hits = data.get("hits", [])

            for i, hit in enumerate(hits):
                videos = hit.get("videos", {})
                # 화질 우선순위: large → medium → small
                video_info = (
                    videos.get("large") or
                    videos.get("medium") or
                    videos.get("small") or
                    {}
                )
                video_url = video_info.get("url", "")
                if not video_url:
                    continue

                safe_kw = keyword.replace(" ", "_")[:30]
                filename = f"pixabay_{safe_kw}_{i+1}.mp4"
                filepath = os.path.join(save_path, filename)

                print(f"  📥 [Pixabay] 다운로드 중: {filename}")
                with urllib.request.urlopen(video_url, timeout=60) as vresp:
                    with open(filepath, "wb") as f:
                        shutil.copyfileobj(vresp, f)
                downloaded.append(filepath)
                print(f"  ✅ [Pixabay] 완료: {filepath}")

    except urllib.error.HTTPError as e:
        print(f"  ❌ [Pixabay] HTTP {e.code}: {e.reason}")
    except Exception as e:
        print(f"  ❌ [Pixabay] 오류: {e}")

    return downloaded


# ──────────────────────────────────────────────
# 🔄 자동 폴백 메인 함수
# ──────────────────────────────────────────────

def fetch_stock_videos_for_scene(
    keyword: str,
    scene_name: str = "",
    count: int = 2,
    output_dir: str = None
) -> list:
    """
    씬 키워드로 Pexels → Pixabay 순서로 자동 폴백하며 스톡 영상 다운로드.

    Args:
        keyword   : 검색 키워드 (영문 권장, 예: "1997 Seoul rain street night")
        scene_name: 저장 폴더명 (예: "씬1_조흥은행")
        count     : 다운로드할 영상 수 (기본 2개)
        output_dir: 저장 경로 (None이면 assets/bgvideos/씬이름/)

    Returns:
        다운로드된 파일 경로 리스트
    """
    if output_dir is None:
        safe_scene = scene_name.replace(" ", "_").replace("/", "_")[:20] or "misc"
        output_dir = os.path.join(BGVIDEO_DIR, safe_scene)

    os.makedirs(output_dir, exist_ok=True)

    print(f"\n🎥 스톡 영상 자동 검색: '{keyword}' → {output_dir}")

    # 1차: Pexels
    results = fetch_from_pexels(keyword, output_dir, per_page=count)

    # 부족하면 Pixabay로 보완
    if len(results) < count:
        needed = count - len(results)
        print(f"  🔄 Pexels 부족 ({len(results)}/{count}) → Pixabay 보완")
        results += fetch_from_pixabay(keyword, output_dir, per_page=needed)

    if results:
        print(f"\n✅ 총 {len(results)}개 스톡 영상 다운로드 완료!")
    else:
        print(f"\n⚠️  스톡 영상 다운로드 실패 (API 키를 확인하세요)")

    return results


# ──────────────────────────────────────────────
# 🏭 8씬 전체 자동 다운로드 (배치 모드)
# ──────────────────────────────────────────────

# Hookverse IMF 2화 8씬 배경 영상 키워드 사전 (씬 → 영문 검색어)
SCENE_KEYWORD_MAP = {
    "씬1_조흥은행거리": "1997 Seoul Korea night street rain neon",
    "씬2_뉴라질주": "woman running night rain city 1990s",
    "씬3_스마트폰화면": "smartphone screen glowing dark close up",
    "씬4_공중전화부스": "phone booth night rain Korea retro",
    "씬5_사냥꾼추격": "men running chasing dark alley night",
    "씬6_지갑동전": "hand coin wallet close up",
    "씬7_뒷모습안개": "woman silhouette fog night back view",
    "씬8_POV수화기": "telephone receiver close up vintage retro",
}

def fetch_all_scene_bgvideos(count_per_scene: int = 2) -> dict:
    """8씬 전체 배경 B롤 영상 자동 다운로드 (배치 모드)"""
    print(f"\n{'='*60}")
    print(f"🎬 [Hookverse] 8씬 배경 영상 전체 자동 다운로드 시작!")
    print(f"{'='*60}")

    results = {}
    for scene_name, keyword in SCENE_KEYWORD_MAP.items():
        files = fetch_stock_videos_for_scene(
            keyword=keyword,
            scene_name=scene_name,
            count=count_per_scene
        )
        results[scene_name] = files

    total = sum(len(v) for v in results.values())
    print(f"\n{'='*60}")
    print(f"🎉 완료! 총 {total}개 배경 영상 다운로드 → assets/bgvideos/")
    print(f"{'='*60}")
    return results


# ──────────────────────────────────────────────
# CLI 실행
# ──────────────────────────────────────────────

if __name__ == "__main__":
    if len(sys.argv) > 1:
        # 단일 키워드 모드: python stock_video_fetcher.py "Seoul rain 1997"
        kw = " ".join(sys.argv[1:])
        fetch_stock_videos_for_scene(kw, scene_name="custom_search", count=3)
    else:
        # 배치 모드: 8씬 전체 자동 다운로드
        fetch_all_scene_bgvideos(count_per_scene=2)
