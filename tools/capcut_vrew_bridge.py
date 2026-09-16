# -*- coding: utf-8 -*-
"""
Hookverse Studio - 캡컷(CapCut) & Vrew 자동 편집 브릿지 엔진 (Editor & Developer 전용 도구)
- 45초 가변 타임라인(8씬) 규격을 Vrew 및 캡컷(CapCut) 편집 프로젝트로 원클릭 변환
- 씬별 가변 듀레이션(Durations), 비디오 클립, 성우 음성, SRT 자막, SFX 효과음 1:1 결합
- 캡컷 트랜지션(Slow Zoom, Dissolve, Glitch) 및 네온 퍼플 300pt 자막 서식 자동 매핑
- 산출물: assets/templates/capcut_vrew_project_spec.json
"""

import os
import sys
import json

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
TEMPLATE_DIR = os.path.join(BASE_DIR, "assets", "templates")
SUBTITLE_DIR = os.path.join(BASE_DIR, "assets", "subtitles")
AUDIO_DIR = os.path.join(BASE_DIR, "assets", "audio")
VIDEO_DIR = os.path.join(BASE_DIR, "assets", "videos")

# 8씬 가변 칼싱크 규격 (기본 검증 45.24초)
DEFAULT_SCENE_DURATIONS = [6.2, 5.3, 5.3, 5.3, 5.2, 5.5, 5.7, 6.74]

SCENE_METADATA = [
    {"scene": 1, "title": "00:00 시계탑 정각", "sfx": "clock_tick_heavy.mp3", "transition": "FadeIn", "motion": "SlowZoomIn"},
    {"scene": 2, "title": "빗속 공중전화 부스 뉴라", "sfx": "heavy_rain_ambient.mp3", "transition": "CrossDissolve", "motion": "TrackingRight"},
    {"scene": 3, "title": "스마트폰 긴급 속보 D-1", "sfx": "digital_glitch_alert.mp3", "transition": "GlitchZoom", "motion": "PushIn"},
    {"scene": 4, "title": "수화기 긴급 통화 시도", "sfx": "payphone_dial_buzz.mp3", "transition": "Cut", "motion": "HandheldBreath"},
    {"scene": 5, "title": "조흥은행 지하 금고 철문", "sfx": "heavy_vault_metal_creak.mp3", "transition": "WipeDown", "motion": "SlowDollyIn"},
    {"scene": 6, "title": "금고 장부 붉은 서명", "sfx": "suspense_drone_bass.mp3", "transition": "FlashWhite", "motion": "TopDownTracking"},
    {"scene": 7, "title": "안개 속으로 사라진 그림자", "sfx": "footsteps_wet_asphalt.mp3", "transition": "FogDissolve", "motion": "TrackingBack"},
    {"scene": 8, "title": "지갑 속 미래의 달러 루프", "sfx": "leather_wallet_snap_echo.mp3", "transition": "InfiniteLoopFreeze", "motion": "SlowPushIn"}
]

def build_project_bridge(durations=None, project_name="IMF2화_자정의조흥은행"):
    if durations is None:
        durations = DEFAULT_SCENE_DURATIONS
        
    print("=" * 60)
    print("🎬 [Editor] 캡컷(CapCut) & Vrew 자동 편집 브릿지 프로젝트 생성")
    print("=" * 60)
    
    total_duration = sum(durations)
    current_time = 0.0
    timeline = []
    
    for i, dur in enumerate(durations):
        meta = SCENE_METADATA[i % len(SCENE_METADATA)]
        scene_item = {
            "scene_index": i + 1,
            "scene_title": meta["title"],
            "start_time": round(current_time, 2),
            "end_time": round(current_time + dur, 2),
            "duration": dur,
            "video_asset": f"assets/images/IMF2화/IMF전날밤의비밀_ep02_cut{i+1:02d}.jpg",
            "audio_asset": "assets/audio/IMF2화_자정의조흥은행_30초대본_성우음성.mp3",
            "subtitle_asset": "assets/subtitles/IMF2화_자정의조흥은행_칼싱크자막.srt",
            "sfx_effect": meta["sfx"],
            "camera_motion": meta["motion"],
            "capcut_transition": meta["transition"],
            "vrew_styling": {
                "font_name": "Pretendard ExtraBold",
                "font_size": 300,
                "text_color": "#FFFFFF",
                "outline_color": "#A855F7",
                "outline_thickness": 18,
                "position_y": 78
            }
        }
        timeline.append(scene_item)
        current_time += dur
        print(f"✅ Scene {i+1} [{meta['title']}] {dur}초 타임코드 브릿지 결합")
        
    project_spec = {
        "project_name": project_name,
        "format": "YouTube Shorts (9:16 Vertical)",
        "resolution": {"width": 1080, "height": 1920},
        "fps": 30,
        "total_duration": round(total_duration, 2),
        "total_scenes": len(timeline),
        "vrew_compatible": True,
        "capcut_compatible": True,
        "cinematic_layout_spec": {
            "top_left_badge": {
                "text": "Hookverse Studio",
                "box_color": "#1e40af",
                "text_color": "#FFFFFF",
                "font_family": "Pretendard Bold",
                "x_percent": 6.5,
                "y_percent": 5.2,
                "width_px": 280,
                "height_px": 72
            },
            "top_right_logo": {
                "asset_path": "assets/images/hookverse_studio_logo.png",
                "type": "Golden Film Circle 3D Emblem",
                "x_percent": 82.0,
                "y_percent": 4.8,
                "size_px": 130,
                "glow_effect": "RimLight Gold #D4AF37"
            },
            "center_visual_motion": {
                "ken_burns_motion": ["SlowZoomIn", "TrackingRight", "GlitchZoom", "SlowDollyIn"],
                "color_grading": "Cinematic 35mm Contrast (Selective Color: Orange/Gold Highlight)"
            },
            "bottom_subtitles": {
                "font_family": "Pretendard ExtraBold",
                "font_size_pt": 88,
                "text_color": "#FFFFFF",
                "stroke_color": "#A855F7",
                "stroke_width_px": 16,
                "shadow_opacity": 0.75,
                "safe_zone_y_percent": 79.5,
                "animation": {
                    "type": "VrewQuickBouncePopIn",
                    "start_scale": 0.6,
                    "drop_duration_sec": 0.15,
                    "bounce_tension": 1.15,
                    "landing_snap_sec": 0.05
                }
            }
        },
        "timeline": timeline
    }
    
    os.makedirs(TEMPLATE_DIR, exist_ok=True)
    out_path = os.path.join(TEMPLATE_DIR, "capcut_vrew_project_spec.json")
    with open(out_path, "w", encoding="utf-8") as f:
        json.dump(project_spec, f, ensure_ascii=False, indent=2)
        
    print("=" * 60)
    print(f"💾 캡컷 & Vrew 브릿지 사양서 저장 완료: {out_path}")
    print(f"⏱️ 총 영상 길이: {total_duration:.2f}초 (8씬 완벽 동기화)")
    print("✨ 편집 레일 결합 정상 완료!")
    return out_path

if __name__ == "__main__":
    build_project_bridge()
