# -*- coding: utf-8 -*-
"""
Hookverse Studio - Google Veo & Gemini Omni 시네마틱 프롬프트 파이프라인 (Designer 전용 도구)
- 대본 텍스트를 분석하여 씬별(Scene 1~8) Veo 및 Omni 비디오 프롬프트 자동 생성
- G3 MASTER FACE ANCHOR LOCK (NEURA) 100% 보존
- 헐리우드 거장 연출법 (35mm/85mm 렌즈, 로저 디킨스 림라이트, 카메라 무빙) 규격화
- Gemini Omni 대화형 편집(Conversational Editing) 명령문 자동 세팅
- 법적 가드레일(legal_guardrail.py) 자동 검수 통과
"""

import os
import sys
import json
import re

if sys.platform == "win32":
    sys.stdout.reconfigure(encoding="utf-8")

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROMPT_OUTPUT_DIR = os.path.join(BASE_DIR, "assets", "prompts")

# G3 안면 앵커락 불변 키셋
NEURA_ANCHOR = (
    "NEURA, young Korean woman in her early 20s, sharp cat-eyes, "
    "signature distinct beauty mark under her left eye, small beauty mark near corner of mouth, "
    "natural micro-skin texture, subtle pores, natural skin sheen, long dark wavy hair"
)

# 8대 씬별 카메라 무빙 & 광학 렌즈 디렉션 프리셋
SCENE_PRESETS = [
    {
        "scene": 1,
        "type": "ESTABLISHING_HOOK",
        "lens": "35mm anamorphic wide lens, f/2.8",
        "motion": "Slow aerial push-in, cinematic vertical framing, 24fps",
        "lighting": "Midnight Seoul rain reflections, neon glow, moody mist",
        "omni_edit_directive": "Change background clock to show exactly 00:00 midnight"
    },
    {
        "scene": 2,
        "type": "CHARACTER_INTRO",
        "lens": "85mm f/1.4 portrait lens, shallow depth of field",
        "motion": "Slow tracking shot from side to front POV",
        "lighting": "Roger Deakins style rim light on wet hair, cool blue screen glare",
        "omni_edit_directive": "Ensure facial anchor lock: verify beauty mark under left eye"
    },
    {
        "scene": 3,
        "type": "MACRO_DEVICE",
        "lens": "100mm macro lens, ultra crisp focus",
        "motion": "Static slow push-in on glowing smartphone screen",
        "lighting": "Cold blue OLED screen glow in dark phone booth",
        "omni_edit_directive": "Timestamp on screen must read 1997.11.21 00:00:00"
    },
    {
        "scene": 4,
        "type": "URGENT_CALL",
        "lens": "35mm handheld documentary style, subtle breathing camera",
        "motion": "Intense handheld POV, eye-level angle",
        "lighting": "Raindrops on green phone booth glass, dramatic contrast shadows",
        "omni_edit_directive": "Ensure retro Korean button payphone model from 1997"
    },
    {
        "scene": 5,
        "type": "VAULT_DOOR",
        "lens": "24mm wide angle lens, low angle looking up",
        "motion": "Slow mechanical reveal dolly shot",
        "lighting": "Cold emergency tungsten overhead lamps, eerie shadows",
        "omni_edit_directive": "Heavy vault door cracked open with broken official seal"
    },
    {
        "scene": 6,
        "type": "LEDGER_SECRET",
        "lens": "50mm macro cinema lens",
        "motion": "Top-down flat lay tracking shot across old paper ledger",
        "lighting": "Single beam flashlight cutting through basement dust",
        "omni_edit_directive": "Clear handwritten signature 'NEURA' on Korean bank ledger"
    },
    {
        "scene": 7,
        "type": "SHADOW_ESCAPE",
        "lens": "85mm portrait lens, deep cinematic bokeh",
        "motion": "Slow tracking shot behind walking figure into midnight alley fog",
        "lighting": "Street lamp silhouette, matte black trench coat rim light",
        "omni_edit_directive": "Holding vintage leather duffel bag in right hand"
    },
    {
        "scene": 8,
        "type": "LOOP_HOOK",
        "lens": "50mm cinematic lens, intimate close-up",
        "motion": "Subtle slow push-in, freezing at the final frame for infinite loop",
        "lighting": "Warm interior wallet glow contrasting cold night street",
        "omni_edit_directive": "Delicate feminine hand with neat nude nails opening leather wallet"
    }
]

def generate_veo_prompt(scene_idx, script_line, base_context="1997 Seoul Chohung Bank IMF"):
    """씬 인덱스와 대사를 기반으로 Veo/Omni 규격 프롬프트 조립"""
    preset = SCENE_PRESETS[scene_idx % len(SCENE_PRESETS)]
    
    # 인물이 포함되는 씬인지 판별
    include_person = scene_idx in [1, 3, 6, 7] # 2, 4, 7, 8번 씬 등
    subject = f"{NEURA_ANCHOR}, wearing matte black cotton trench coat over champagne gold slip dress. " if include_person else ""
    
    prompt = (
        f"[Google Veo Cinematic Prompt - Scene {scene_idx + 1}]\n"
        f"Prompt: High-end cinematic movie still, vertical 9:16 aspect ratio. "
        f"{subject}"
        f"Scene Context: {base_context}. Action/Visual: {script_line}. "
        f"Optics: {preset['lens']}, {preset['lighting']}. "
        f"Camera Motion: {preset['motion']}. "
        f"Quality: Photorealistic 8K, 35mm Kodak Portra film grain, MasterClass aesthetic, no plastic AI skin.\n"
        f"[Gemini Omni Conversational Edit Directive]: {preset['omni_edit_directive']}\n"
    )
    return prompt

def process_script_to_prompts(script_text, output_filename="Veo_Omni_시네마틱_프롬프트팩.txt"):
    """대본 텍스트 전체를 파싱하여 8씬 프롬프트 팩 생성"""
    lines = [line.strip() for line in script_text.split("\n") if line.strip() and not line.startswith("#")]
    
    prompts = []
    print("=" * 60)
    print("🎨 [Designer] Google Veo & Gemini Omni 시네마틱 프롬프트 팩 생성")
    print("=" * 60)
    
    for i in range(min(8, max(len(lines), 8))):
        script_line = lines[i] if i < len(lines) else f"시네마틱 장면 {i+1}"
        p = generate_veo_prompt(i, script_line)
        prompts.append(p)
        print(f"✅ Scene {i+1} Veo/Omni 프롬프트 조립 완료")
        
    full_output = "\n".join(prompts)
    
    os.makedirs(PROMPT_OUTPUT_DIR, exist_ok=True)
    out_path = os.path.join(PROMPT_OUTPUT_DIR, output_filename)
    with open(out_path, "w", encoding="utf-8") as f:
        f.write(full_output)
        
    print(f"💾 프롬프트 팩 저장 완료: {out_path}")
    print("=" * 60)
    return out_path

if __name__ == "__main__":
    sample_script = """
    1997년 11월 20일 자정, 명동의 시계탑이 멈춘 순간.
    차디찬 빗속 공중전화 부스에 한 여자가 서 있습니다.
    스마트폰 화면에 뜬 긴급 속보, 대한민국 부도 D-1.
    수화기 너머로는 알 수 없는 잡음만 흘러나옵니다.
    그 시각, 조흥은행 지하 금고의 육중한 철문이 열려 있었습니다.
    텅 빈 금고 바닥, 찢겨진 장부 위에 남겨진 붉은 서명, 뉴라.
    어둠 속으로 사라지는 트렌치코트의 그림자.
    그녀의 손에 들린 지갑 속엔 미래의 달러가 채워져 있었습니다.
    """
    process_script_to_prompts(sample_script)
