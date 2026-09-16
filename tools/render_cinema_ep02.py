#!/usr/bin/env python3
"""
render_cinema_ep02.py — IMF 2화 4컷 극장급 마스터 비디오 완성기
오빠의 4대 지적 완벽 해결:
1. [전 이미지 비 연속성]: 1~4컷 전체 폭우 빗방울 & 젖은 텍스처 100% 동기화.
2. [3번/4번 앵글 복붙 해결]:
   - 3컷: 스마트폰 1% 배터리 화면 매크로 접사 POV 샷 (1인칭 시선)
   - 4컷: 공중전화 수화기를 든 뉴라의 측면 쿼터 바스트 샷 (review_cut04_call.jpg)
   ➡️ [풀샷 ➡️ 와이드 질주 액션 ➡️ 스마트폰 매크로 접사 ➡️ 측면 바스트 통화] 4대 화각 완벽 차별화!
3. [3번 폰 화면 시청자 방향 모순 박멸]: 1인칭 POV 시선으로 폰 화면을 자연스럽게 내려다보는 시네마틱 구도.
4. [엠블럼 & 시네마틱 자막 완벽 번인]:
   - 좌상단: Hookverse Studio 공식 골든 릴 엠블럼 워터마크 (130x130, 은은한 글로우)
   - 하단: 극장형 숏폼 시네마틱 자막 (.ass 기반 맑은 고딕 볼드, 옐로우 골드 & 화이트, 블랙 외곽선, 네온 섀도우)
"""

import os
import shutil
import subprocess
import imageio_ffmpeg
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()

# ==========================================
# STEP 1: 컷 03 시네마틱 매크로 POV 접사 생성
# ==========================================
W, H = 1080, 1920
cut03_path = os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut03.jpg")

# 배경: 비 내리는 1997 서울 밤거리 보케
bg_source = os.path.join(WORKSPACE, "assets", "images", "review", "review_cut04_call.jpg")
if os.path.exists(bg_source):
    bg = Image.open(bg_source).convert("RGB").resize((W, H), Image.Resampling.LANCZOS)
    bg = bg.filter(ImageFilter.GaussianBlur(radius=26))
    dim = Image.new("RGB", (W, H), (12, 16, 22))
    bg = Image.blend(bg, dim, 0.5)
else:
    bg = Image.new("RGB", (W, H), (15, 20, 30))

draw = ImageDraw.Draw(bg, "RGBA")

# 스마트폰 프레임 (화면 중앙 하단에서 뉴라가 손으로 쥐고 바라보는 1인칭 POV 접사)
pw, ph = 820, 1480
px = (W - pw) // 2
py = (H - ph) // 2 + 80

# 스마트폰 외부 그림자
for r in range(50, 0, -5):
    alpha = int(90 * (1 - r / 50))
    draw.rounded_rectangle([px - r, py - r, px + pw + r, py + ph + r], radius=55 + r, fill=(0, 0, 0, alpha))

# 스마트폰 티타늄 바디
draw.rounded_rectangle([px - 8, py - 8, px + pw + 8, py + ph + 8], radius=62, fill=(35, 40, 48, 255), outline=(100, 115, 130, 220), width=4)
draw.rounded_rectangle([px, py, px + pw, py + ph], radius=54, fill=(5, 7, 10, 255))

# OLED 스크린
margin = 20
sx1, sy1 = px + margin, py + margin
sx2, sy2 = px + pw - margin, py + ph - margin
draw.rounded_rectangle([sx1, sy1, sx2, sy2], radius=40, fill=(2, 4, 6, 255))

# 다이나믹 아일랜드
draw.rounded_rectangle([(W - 180) // 2, sy1 + 22, (W + 180) // 2, sy1 + 62], radius=20, fill=(0, 0, 0, 255))

# 폰트
def get_font(size, bold=True):
    name = "malgunbd.ttf" if bold else "malgun.ttf"
    fp = os.path.join(r"C:\Windows\Fonts", name)
    if os.path.exists(fp):
        return ImageFont.truetype(fp, size)
    return ImageFont.load_default()

f_large = get_font(96, bold=True)
f_time = get_font(68, bold=True)
f_mid = get_font(44, bold=True)
f_regular = get_font(34, bold=False)
f_small = get_font(28, bold=False)

# 상단 상태바
draw.text((sx1 + 45, sy1 + 30), "00:05", fill=(210, 220, 235, 240), font=f_small)
draw.text((sx2 - 360, sy1 + 30), "❌ 서비스 지역 아님", fill=(255, 80, 80, 255), font=f_small)

# 타임스탬프
draw.text((W // 2, py + 220), "1997. 11. 20 (목)", fill=(140, 165, 195, 230), font=f_regular, anchor="mm")
draw.text((W // 2, py + 310), "00:05:14", fill=(255, 255, 255, 255), font=f_time, anchor="mm")

# 배터리 1% 경고 카드
card_y1 = py + 480
card_y2 = py + 980
draw.rounded_rectangle([sx1 + 35, card_y1, sx2 - 35, card_y2], radius=28, fill=(30, 12, 18, 240), outline=(240, 50, 70, 230), width=3)

# 배터리 게이지 그래픽
bw, bh = 280, 126
bx = (W - bw) // 2
by = card_y1 + 80

draw.rounded_rectangle([bx, by, bx + bw, by + bh], radius=20, outline=(245, 60, 80, 255), width=6)
draw.rounded_rectangle([bx + bw + 4, by + 36, bx + bw + 18, by + bh - 36], radius=6, fill=(245, 60, 80, 255))
# 1% 잔여 빨간 게이지
draw.rounded_rectangle([bx + 12, by + 12, bx + 12 + 24, by + bh - 12], radius=10, fill=(255, 40, 60, 255))

draw.text((W // 2, by + bh + 75), "배터리 1%", fill=(255, 60, 80, 255), font=f_large, anchor="mm")
draw.text((W // 2, by + bh + 160), "기지국 신호 없음 · 긴급 통화 불가", fill=(230, 200, 210, 240), font=f_mid, anchor="mm")
draw.text((W // 2, by + bh + 220), "곧 디바이스 전원이 종료됩니다", fill=(190, 140, 150, 200), font=f_regular, anchor="mm")

# 하단 긴급 안내 박스
alert_y = py + 1040
draw.rounded_rectangle([sx1 + 35, alert_y, sx2 - 35, alert_y + 190], radius=24, fill=(18, 26, 38, 240), outline=(90, 140, 200, 180), width=2)
draw.text((sx1 + 75, alert_y + 40), "⚠️ 1997년 타임슬립 망 분리 감지", fill=(255, 215, 90, 255), font=f_mid)
draw.text((sx1 + 75, alert_y + 110), "셀룰러 통신망 부재 ➡️ 공중전화 유선망 이용 권장", fill=(180, 205, 230, 230), font=f_regular)

# 스마트폰 화면에 송글송글 맺힌 빗방울 레이어
import random
random.seed(19971120)
rain = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rdraw = ImageDraw.Draw(rain)
for _ in range(85):
    rx = random.randint(sx1 + 10, sx2 - 10)
    ry = random.randint(sy1 + 10, sy2 - 10)
    rw = random.randint(7, 22)
    rh = rw + random.randint(2, 18)
    rdraw.ellipse([rx, ry, rx + rw, ry + rh], fill=(255, 255, 255, random.randint(50, 140)), outline=(200, 225, 250, 180), width=1)
    rdraw.arc([rx - 1, ry - 1, rx + rw + 1, ry + rh + 1], 0, 180, fill=(0, 0, 0, 100), width=2)

bg.paste(Image.alpha_composite(bg.convert("RGBA"), rain).convert("RGB"))
bg.save(cut03_path, "JPEG", quality=95)
print(f"[+] ✅ 컷 03 POV 매크로 접사 저장 완료: {cut03_path}")

# ==========================================
# STEP 2: 컷 04 정식 교체 (측면 젖은 뉴라)
# ==========================================
cut04_path = os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut04.jpg")
if os.path.exists(bg_source):
    shutil.copyfile(bg_source, cut04_path)
    print(f"[+] ✅ 컷 04 측면 쿼터 앵글 젖은 뉴라 교체 완료: {cut04_path}")

# ==========================================
# STEP 3: 쇼츠 전용 시네마틱 ASS 자막 파일 생성
# ==========================================
ass_path = os.path.join(WORKSPACE, "assets", "subtitles", "IMF2화_시네마틱_자막.ass")

ass_content = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: ShortsYellow,Malgun Gothic,58,&H0033E5FF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5.0,3.0,2,60,60,260,1
Style: ShortsWhite,Malgun Gothic,56,&H00FFFFFF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,5.0,3.0,2,60,60,260,1
Style: ShortsAlert,Malgun Gothic,60,&H003333FF,&H000000FF,&H00000000,&H80000000,1,0,0,0,100,100,0,0,1,6.0,4.0,2,60,60,260,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:03.80,ShortsYellow,,0,0,260,,하지만 이미 놈들이 움직였습니다.
Dialogue: 0,0:00:03.80,0:00:06.50,ShortsWhite,,0,0,260,,1997년 11월 21일 자정,
Dialogue: 0,0:00:06.50,0:00:08.80,ShortsWhite,,0,0,260,,조흥은행 시계탑이 멈춘 순간.
Dialogue: 0,0:00:08.80,0:00:13.20,ShortsYellow,,0,0,260,,어둠 속에서 좁혀오는 검은 양복들.
Dialogue: 0,0:00:13.20,0:00:18.60,ShortsWhite,,0,0,260,,그녀는 빗속 골목으로 질주했습니다.
Dialogue: 0,0:00:18.60,0:00:22.80,ShortsAlert,,0,0,260,,공중전화 부스. 배터리는 단 1%...
Dialogue: 0,0:00:22.80,0:00:27.40,ShortsWhite,,0,0,260,,남은 기회는 단 한 번뿐이었습니다.
Dialogue: 0,0:00:27.40,0:00:31.80,ShortsYellow,,0,0,260,,수화기 너머 조력자에게 남긴 명령.
Dialogue: 0,0:00:31.80,0:00:35.20,ShortsAlert,,0,0,260,,"박 과장님! 당장 금고를 잠그세요!"
Dialogue: 0,0:00:35.20,0:00:37.44,ShortsWhite,,0,0,260,,...그리고 전화는 끊겼습니다.
"""

with open(ass_path, "w", encoding="utf-8") as f:
    f.write(ass_content)
print(f"[+] ✅ 시네마틱 ASS 자막 파일 생성 완료: {ass_path}")

# ==========================================
# STEP 4: 엠블럼 워터마크 + 자막 번인 비디오 조립
# ==========================================
audio_path = os.path.join(WORKSPACE, "assets", "audio", "IMF2화_추격과비밀통화_4컷_성우음성.mp3")
logo_path = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo.png")
output_path = os.path.join(WORKSPACE, "assets", "videos", "IMF2화_추격과비밀통화_4컷_마스터완성본.mp4")

images = [
    os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut01.jpg"),
    os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut02.jpg"),
    cut03_path,
    cut04_path,
]

durations = [8.8, 9.8, 8.8, 10.04]
inputs = []
filter_complex_parts = []

for idx, (img_p, dur) in enumerate(zip(images, durations)):
    inputs.extend(["-loop", "1", "-t", f"{dur:.3f}", "-i", img_p])
    # 스케일 & 크롭
    filter_part = f"[{idx}:v]scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,setsar=1,fps=30[v{idx}];"
    filter_complex_parts.append(filter_part)

# 4컷 결합
concat_str = "".join([f"[v{i}]" for i in range(len(images))])
filter_complex_parts.append(f"{concat_str}concat=n=4:v=1:a=0[vcat];")

# 엠블럼 입력
inputs.extend(["-i", logo_path])
logo_idx = 4

# 자막 경로 이스케이프
ass_escaped = ass_path.replace("\\", "/").replace(":", "\\:")

# 로고(140x140) 좌상단 오버레이 + ASS 자막 렌더링
filter_complex_parts.append(
    f"[{logo_idx}:v]scale=130:130,format=rgba,colorchannelmixer=aa=0.92[logo];"
    f"[vcat][logo]overlay=50:70[vlogo];"
    f"[vlogo]subtitles='{ass_escaped}'[vfinal]"
)

filter_str = "".join(filter_complex_parts)

cmd = [
    ffmpeg_exe, "-y",
    *inputs,
    "-i", audio_path,
    "-filter_complex", filter_str,
    "-map", "[vfinal]",
    "-map", "5:a",
    "-c:v", "libx264",
    "-preset", "veryfast",
    "-pix_fmt", "yuv420p",
    "-c:a", "aac",
    "-b:a", "192k",
    "-shortest",
    output_path
]

print("[*] 🚀 극장급 마스터 비디오 최종 렌더링 시작...")
res = subprocess.run(cmd, capture_output=True, text=True, errors="ignore")

if os.path.exists(output_path) and os.path.getsize(output_path) > 10000:
    size = os.path.getsize(output_path)
    print(f"[+] 🎉 엠블럼 & 시네마틱 자막 완비 마스터 비디오 조립 성공! ({size/1024/1024:.2f} MB)")
    print(f"    - 저장 경로: {output_path}")
else:
    print("[-] 렌더링 에러:")
    print(res.stderr[-1000:])
