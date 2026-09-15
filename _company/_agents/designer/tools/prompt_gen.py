import os
import sys
import argparse
import subprocess

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
PIPELINE_SCRIPT = os.path.join(WORKSPACE, "tools", "ai_production_pipeline.py")

def generate_prompt(scene_title="IMF3화_유령을쫓는자들"):
    cmd = [sys.executable, PIPELINE_SCRIPT, scene_title]
    res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")
    print(res.stdout)
    if res.returncode != 0:
        print("[-] 에러 발생:", res.stderr)
    return os.path.join(WORKSPACE, "assets", "prompts", f"{scene_title}_8씬_완성프롬프트.txt")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Hookverse AI Prompt Generator")
    parser.add_argument("title", nargs="?", default="IMF3화_유령을쫓는자들")
    args = parser.parse_args()
    generate_prompt(args.title)
