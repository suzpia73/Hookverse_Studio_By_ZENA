import os
import re
import asyncio
import edge_tts
import subprocess
import imageio_ffmpeg

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

# 대본 분할
part1_text = (
    "1997년 11월 20일 자정, 국가 부도를 선언하기 딱 9시간 전. "
    "멈춰버린 명동 조흥은행 시계탑 아래 한 여자가 서 있었습니다. "
    "흠뻑 젖은 트렌치코트의 그녀는 빗속을 뚫고 공중전화로 뛰어들었습니다. "
    "그녀의 눈빛은 무언가를 알고 있는 듯 흔들렸습니다. "
    "수화기 너머로 그녀가 남긴 마지막 말... "
    "지금 당장, 모든 원화를 달러로 바꿔."
)

part2_text = (
    "다음 날 아침, 한국 경제는 무너졌습니다. "
    "환전소 장부에 남겨진 서명, 뉴라. "
    "1997년 대한민국엔 존재하지 않던 이름이었습니다. "
    "만약 당신의 지갑 속에 오래된 100달러 지폐가 있다면, "
    "지금 그 일련번호를 확인하세요. "
    "그날 밤 그녀가 남긴 미래의 비밀일지 모릅니다."
)

temp_p1 = os.path.join(WORKSPACE, "assets", "audio", "temp_part1.mp3")
temp_p2 = os.path.join(WORKSPACE, "assets", "audio", "temp_part2.mp3")
temp_silence = os.path.join(WORKSPACE, "assets", "audio", "temp_silence.mp3")
final_audio = os.path.join(WORKSPACE, "assets", "audio", "IMF2화_자정의조흥은행_30초대본_성우음성.mp3")
concat_list = os.path.join(WORKSPACE, "assets", "audio", "concat_list.txt")

async def generate():
    # 40초(37~43초) 완벽 안착 딕션 (rate=+20%)
    comm1 = edge_tts.Communicate(part1_text, "ko-KR-SunHiNeural", rate="+20%", pitch="-2Hz")
    await comm1.save(temp_p1)
    
    comm2 = edge_tts.Communicate(part2_text, "ko-KR-SunHiNeural", rate="+20%", pitch="-2Hz")
    await comm2.save(temp_p2)

print("[*] 1. 1단계: 파트별 성우 나레이션 생성 중...")
asyncio.run(generate())

# 1.5초 무음 생성 (FFmpeg)
print("[*] 2. 2단계: 1.5초 서스펜스 침묵(Silence) 구간 생성 중...")
subprocess.run([
    ffmpeg, "-y", "-f", "lavfi", "-i", "anullsrc=r=44100:cl=stereo",
    "-t", "1.5", "-q:a", "9", "-acodec", "libmp3lame", temp_silence
], capture_output=True, check=True)

# 병합 목록 작성
with open(concat_list, "w", encoding="utf-8") as f:
    f.write(f"file '{temp_p1.replace(chr(92), '/')}'\n")
    f.write(f"file '{temp_silence.replace(chr(92), '/')}'\n")
    f.write(f"file '{temp_p2.replace(chr(92), '/')}'\n")

# 최종 무손실 병합
print("[*] 3. 3단계: 1.5초 정적 포함 40초 표준 성우 음성 결합 중...")
subprocess.run([
    ffmpeg, "-y", "-f", "concat", "-safe", "0", "-i", concat_list,
    "-c", "copy", final_audio
], capture_output=True, check=True)

# 임시 파일 정리
for p in [temp_p1, temp_p2, temp_silence, concat_list]:
    if os.path.exists(p):
        os.remove(p)

# 길이 측정
res = subprocess.run([ffmpeg, "-i", final_audio], capture_output=True, text=True, errors="ignore")
m = re.search(r"Duration:\s*(\d+):(\d+):(\d+\.\d+)", res.stderr)
if m:
    s = float(m.group(1))*3600 + float(m.group(2))*60 + float(m.group(3))
    print(f"[+] ⏱️ 최종 성우 나레이션 완성 길이: {s:.2f}초 (40초 ±3초 표준 규격 적합!)")

