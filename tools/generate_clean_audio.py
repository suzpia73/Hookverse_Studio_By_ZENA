import os
import re
import asyncio
import edge_tts
import subprocess
import imageio_ffmpeg

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
script_path = os.path.join(WORKSPACE, "assets", "scripts", "IMF2화_자정의조흥은행_30초대본.md")
out_audio = os.path.join(WORKSPACE, "assets", "audio", "IMF2화_자정의조흥은행_30초대본_성우음성.mp3")

with open(script_path, "r", encoding="utf-8") as f:
    text = f.read()

narration_part = ""
if "## 📜" in text:
    narration_part = text.split("## 📜")[1]
if "## 📸" in narration_part:
    narration_part = narration_part.split("## 📸")[0]

lines = []
for line in narration_part.splitlines():
    line = line.strip()
    if not line or line.startswith("#") or line.startswith("---"):
        continue
    if "나레이션 대본" in line or "사운드 큐" in line:
        continue
    line = re.sub(r"\[.*?\]", "", line)
    line = re.sub(r"\(.*?\)", "", line)
    line = line.strip()
    if line:
        lines.append(line)

clean_text = " ".join(lines)
print(f"[*] 추출 텍스트: {clean_text}")

async def run():
    # rate=+16%: 약 30~33초 쇼츠 딕션 최적화
    comm = edge_tts.Communicate(clean_text, "ko-KR-SunHiNeural", rate="+16%", pitch="-1Hz")
    await comm.save(out_audio)

asyncio.run(run())

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
res = subprocess.run([ffmpeg, "-i", out_audio], capture_output=True, text=True, errors="ignore")
m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
if m:
    s = float(m.group(1))*3600 + float(m.group(2))*60 + float(m.group(3))
    print(f"[+] ⏱️ 성우 나레이션 최종 길이: {s:.2f}초")
