import os
import sys
import argparse
from datetime import datetime

def generate_prompt(scene_title="IMF2화_자정의조흥은행", lens="35mm", lighting="야간_시네마틱_이중색온도", custom_prompt=None):
    output_dir = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\prompts"
    os.makedirs(output_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    safe_title = scene_title.replace(" ", "_")
    filename = f"{safe_title}_프롬프트.txt"
    filepath = os.path.join(output_dir, filename)
    
    if custom_prompt:
        final_prompt = custom_prompt
    else:
        final_prompt = (
            f"A cinematic vertical 9:16 hyperrealistic photograph of Neura in 1997 vintage Seoul Myeongdong alley at midnight (00:00). "
            f"Heavy cold rain, wet reflective asphalt streets with warm vintage Korean neon signage reflections (Chohung Bank vintage logo signage in distant background). "
            f"Neura is a 24-year-old Korean woman with authentic natural skin texture, visible subtle pores, two distinct beauty marks (one below left eye, one near right collarbone). "
            f"Wearing a vintage matte cotton gabardine trench coat, completely soaked with realistic water dripping, collars flipped up, holding an umbrella slightly tilted. "
            f"Shot on {lens} cine lens, shallow depth of field. "
            f"Lighting: {lighting}, dual color temperature (warm tungsten streetlights vs cold cyan rain ambiance), rim light outlining her drenched silhouette. "
            f"Kodak Portra 400 35mm film grain, 8k resolution, authentic Korean 1997 atmosphere, highly detailed, masterwork. --ar 9:16 --style raw --v 6.0"
        )
    
    content = f"""# 🎨 G3 실사 프롬프트: {scene_title}
- 생성 일시: {timestamp}
- 렌즈 규격: {lens}
- 조명 기법: {lighting}
- 연출 헌법: 10대 시네마틱 연속성 연출헌법 준수 (G3 안면 앵커락)

## 📋 최종 완성 영문 프롬프트 (Midjourney / SD 복사용)
{final_prompt}
"""
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(content)
        
    print(f"✅ [Designer] 프롬프트 파일 생성 성공: {filepath}")
    return filepath

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hookverse G3 Cinematic Prompt Generator")
    parser.add_argument("title", nargs="?", default="IMF2화_자정의조흥은행")
    parser.add_argument("lens", nargs="?", default="35mm")
    parser.add_argument("lighting", nargs="?", default="야간_시네마틱_이중색온도")
    parser.add_argument("--prompt", "-p", help="Custom English prompt text", default=None)
    args = parser.parse_args()
    generate_prompt(args.title, args.lens, args.lighting, custom_prompt=args.prompt)
