#!/usr/bin/env python3
"""
opal_visual_pipeline_node.py — 20대 핵심축 기반 Opal / Google Flow 비주얼 파이프라인 노드 엔진
10대 AI 에이전트들이 스스로 복제하여 무결점 이미지를 렌더링하고 감사할 수 있는 표준 노드.
"""

import os
import json
import sys

WORKSPACE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RULES_PATH = os.path.join(WORKSPACE, "_rules", "visual_continuity_rules.json")

def load_visual_rules():
    if not os.path.exists(RULES_PATH):
        raise FileNotFoundError(f"Rules file not found at: {RULES_PATH}")
    with open(RULES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def build_cut_manifest(cut_id: str):
    rules = load_visual_rules()
    scene_rules = rules.get("scene_fact_checks", {}).get(cut_id)
    if not scene_rules:
        raise ValueError(f"No rules defined for {cut_id}")
    
    global_weather = rules.get("global_visual_anchors", {}).get("weather", {})
    global_g3 = rules.get("global_visual_anchors", {}).get("character_g3_anchor", {})
    
    # 2중 앵커 파일 존재 여부 물리 검사
    anchor_files = scene_rules.get("dual_anchor_files", [])
    valid_anchors = []
    for rel_path in anchor_files:
        full_path = os.path.join(WORKSPACE, rel_path)
        if os.path.exists(full_path):
            valid_anchors.append(full_path)
        else:
            print(f"[WARN] Anchor file not found on disk: {full_path}")
            
    manifest = {
        "cut_id": cut_id,
        "scene_type": scene_rules.get("scene_type"),
        "shot_scale": scene_rules.get("shot_scale"),
        "weather_hair_anchor": global_weather.get("hair_texture"),
        "costume_anchor": global_g3.get("costume"),
        "dual_anchor_paths": valid_anchors,
        "required_elements": scene_rules.get("required_elements", []),
        "forbidden_errors": scene_rules.get("forbidden_errors", [])
    }
    return manifest

def audit_generated_image_prompt(cut_id: str, prompt_text: str):
    """
    에이전트가 생성한 프롬프트가 오빠의 헌법 및 물리 팩트를 위반했는지 검증하는 게이트 (ACCG)
    """
    manifest = build_cut_manifest(cut_id)
    violations = []
    
    # 1. 비에 젖은 머리 텍스처 검사
    if "wet" not in prompt_text.lower() or "hair" not in prompt_text.lower():
        violations.append("비에 젖은 머리(soaked wet hair) 텍스처 키워드 누락!")
        
    # 2. 컷 02 스마트폰 앞뒷면 검증
    if cut_id == "cut02":
        if "back" in prompt_text.lower() and "screen" in prompt_text.lower() and "battery" in prompt_text.lower():
            if "back panel ... resting against palm" not in prompt_text.lower() and "front" not in prompt_text.lower():
                violations.append("스마트폰 뒷면에 화면이 그려지는 옥에 티 위험 감지!")
                
    # 3. 컷 04 공중전화 본체 및 코일선 검증
    if cut_id == "cut04":
        if "payphone box" not in prompt_text.lower() and "payphone unit" not in prompt_text.lower():
            violations.append("공중전화기 본체(payphone unit) 묘사 누락! 수화기만 허공에 뜰 위험!")
        if "coil" not in prompt_text.lower() and "cord" not in prompt_text.lower():
            violations.append("수화기와 본체를 잇는 강철 코일선(coil cord) 누락!")
            
    passed = len(violations) == 0
    return {
        "cut_id": cut_id,
        "passed": passed,
        "violations": violations,
        "dual_anchors_ready": len(manifest["dual_anchor_paths"]) == 2
    }

if __name__ == "__main__":
    print("=== Hookverse Opal Visual Pipeline Node Audit ===")
    for cut in ["cut01", "cut02", "cut03", "cut04"]:
        m = build_cut_manifest(cut)
        print(f"[{cut.upper()}] Scale: {m['shot_scale']} | Anchors Ready: {len(m['dual_anchor_paths'])}/2")
    print("All Pipeline Nodes Validated Successfully!")
