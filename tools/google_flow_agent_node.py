#!/usr/bin/env python3
"""
google_flow_agent_node.py — Hookverse Studio 구글 Flow 비주얼 에이전트 자동화 노드 (v2.0)

[헌법 제10조 및 제16조 준수]:
- 디자이너 카이 & 아트디렉터 에이전트가 구글 Flow / Opal 환경에서
  G3 캐릭터 앵커LOCK을 부착하고 무결점 4컷을 생성·검증·배치하는 공식 노드.
"""

import os
import sys
import json

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
RULES_PATH = os.path.join(WORKSPACE, "_rules", "visual_continuity_rules.json")
FLOW_PROJECT_URL = "https://flow.google.com/project/3e5be258-bed9-4217-9b65-4ca7eeddd464"

class GoogleFlowAgentNode:
    def __init__(self):
        self.project_url = FLOW_PROJECT_URL
        self.rules = self.load_rules()
        
    def load_rules(self):
        if os.path.exists(RULES_PATH):
            with open(RULES_PATH, "r", encoding="utf-8") as f:
                return json.load(f)
        return {}

    def get_cut_spec(self, cut_id: str):
        """컷별 앵커 및 프롬프트 생성 규격 반환"""
        cut_rules = self.rules.get("scene_fact_checks", {}).get(cut_id, {})
        weather = self.rules.get("global_visual_anchors", {}).get("weather", {})
        
        spec = {
            "cut_id": cut_id,
            "project_url": self.project_url,
            "model": "Nano Banana 2",
            "aspect_ratio": "9:16",
            "anchors": [
                os.path.join(WORKSPACE, "assets", "G3캐릭터앵커LOCK", "크롭샷.jpg"),
                os.path.join(WORKSPACE, "assets", "G3캐릭터앵커LOCK", "상반신.jpg" if cut_id in ["cut01", "cut04"] else ("반신.jpg" if cut_id == "cut02" else "전신_앞.jpg"))
            ],
            "required_elements": cut_rules.get("required_elements", []),
            "forbidden_errors": cut_rules.get("forbidden_errors", [])
        }
        return spec

    def export_generation_manifest(self, output_dir: str):
        """전체 4컷 매니페스트 디스크 발행"""
        manifest = {
            "pipeline": "Google Flow Production Node",
            "version": "2.0.0",
            "timestamp": "2026-09-18T21:18:00",
            "cuts": {
                f"cut0{i}": self.get_cut_spec(f"cut0{i}") for i in range(1, 5)
            }
        }
        path = os.path.join(output_dir, "google_flow_manifest.json")
        with open(path, "w", encoding="utf-8") as f:
            json.dump(manifest, f, ensure_ascii=False, indent=2)
        print(f"[+] ✅ 구글 Flow 매니페스트 발행 완료: {path}")
        return manifest

if __name__ == "__main__":
    node = GoogleFlowAgentNode()
    out = os.path.join(WORKSPACE, "assets", "production_packages")
    os.makedirs(out, exist_ok=True)
    node.export_generation_manifest(out)
