import os
import sys
from datetime import datetime

def generate_prompt(scene_title="미스터리_씬", lens="85mm", lighting="야간_시네마틱_앰비언트"):
    output_dir = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\prompts"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_title = scene_title.replace(" ", "_")
    filename = f"{safe_title}_프롬프트.txt"
    filepath = os.path.join(output_dir, filename)
    
    prompt_text = (
        f"A cinematic vertical 9:16 photograph of Neura in {scene_title}. "
        f"Neura is an East Asian Korean woman in her early 20s with monolid eyes, fair natural skin texture with subtle visible pores (strictly NO smooth plastic AI skin), damp black hair. "
        f"Wearing an authentic matte cotton gabardine trench coat over a champagne gold slip dress. "
        f"Shot on {lens} portrait lens, f/1.8 shallow depth of field, natural candid shot. "
        f"Dramatic lighting with {lighting}, realistic cool blue screen glow reflections on her cheekbones, jawline, and lips. "
        f"Hyperrealistic 35mm film grain, 8k resolution, authentic atmosphere. --ar 9:16 --style raw --v 6.0"
    )
    
    content = f"""# 🎨 G3 실사 프롬프트: {scene_title}
- 생성 일시: {timestamp}
- 렌즈: {lens}
- 조명: {lighting}

## 📋 최종 완성 영문 프롬프트 (복사용)
{prompt_text}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ 프롬프트 파일 생성 성공: {filepath}")
    return filepath

if __name__ == "__main__":
    title = sys.argv[1] if len(sys.argv) > 1 else "심청전_인당수_불시착"
    lens = sys.argv[2] if len(sys.argv) > 2 else "85mm"
    generate_prompt(title, lens)
