#!/usr/bin/env python3
"""
create_cut03_pov.py — 컷 03: 뉴라 시점(POV) 스마트폰 1% 배터리 화면 매크로 클로즈업 생성기
오빠의 피드백 반영:
1. 카메라를 향해 폰을 내미는 부자연스러운 포즈 영구 박멸 ➡️ 뉴라의 눈으로 직접 폰을 내려다보는 1인칭 POV 접사 샷!
2. 3번(스마트폰 POV 접사)과 4번(수화기 통화 바스트샷)의 앵글 및 피사체 완벽 차별화!
3. 폭우 빗방울 텍스처와 1997 기지국 부재(서비스 불가지역) 팩트 무결점 UI!
"""

import os
import math
from PIL import Image, ImageDraw, ImageFont, ImageFilter

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
OUTPUT_PATH = os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut03.jpg")

# 1080x1920 9:16 비율
W, H = 1080, 1920

# 1. 배경: 비 내리는 1997년 공중전화 부스와 네온 불빛 보케 (기존 컷에서 추출 후 심도 블러)
base_bg_path = os.path.join(WORKSPACE, "assets", "images", "review", "review_cut04_call.jpg")
if os.path.exists(base_bg_path):
    bg = Image.open(base_bg_path).convert("RGB")
    bg = bg.resize((W, H), Image.Resampling.LANCZOS)
    # 극적인 심도 표현: 배경을 강하게 블러(Bokeh) 처리하여 스마트폰에 초점 집중
    bg = bg.filter(ImageFilter.GaussianBlur(radius=24))
    # 어두운 밤 부스 분위기 톤 다운
    dimmer = Image.new("RGB", (W, H), (10, 15, 20))
    bg = Image.blend(bg, dimmer, 0.45)
else:
    bg = Image.new("RGB", (W, H), (15, 20, 28))

draw = ImageDraw.Draw(bg, "RGBA")

# 2. 스마트폰 본체 렌더링 (핸드헬드 POV 구도: 화면 하단 중앙에서 살짝 위로 비스듬히 들려 있는 상태)
phone_w = 780
phone_h = 1420
phone_x = (W - phone_w) // 2
phone_y = (H - phone_h) // 2 + 60

# 스마트폰 외곽 그림자
for r in range(40, 0, -5):
    alpha = int(80 * (1 - r / 40))
    draw.rounded_rectangle(
        [phone_x - r, phone_y - r, phone_x + phone_w + r, phone_y + phone_h + r],
        radius=50 + r,
        fill=(0, 0, 0, alpha)
    )

# 스마트폰 메탈 프레임 (다크 티타늄)
draw.rounded_rectangle(
        [phone_x - 6, phone_y - 6, phone_x + phone_w + 6, phone_y + phone_h + 6],
        radius=56,
        fill=(40, 45, 52, 255),
        outline=(90, 100, 115, 200),
        width=3
)

# 스마트폰 블랙 베젤
draw.rounded_rectangle(
        [phone_x, phone_y, phone_x + phone_w, phone_y + phone_h],
        radius=50,
        fill=(8, 10, 14, 255)
)

# 스마트폰 OLED 디스플레이 영역
screen_margin = 18
screen_x1 = phone_x + screen_margin
screen_y1 = phone_y + screen_margin
screen_x2 = phone_x + phone_w - screen_margin
screen_y2 = phone_y + phone_h - screen_margin

draw.rounded_rectangle(
        [screen_x1, screen_y1, screen_x2, screen_y2],
        radius=36,
        fill=(3, 5, 8, 255)
)

# 3. 스마트폰 화면 UI 렌더링
# 다이나믹 아일랜드 / 상단 펀치홀
punch_w, punch_h = 160, 36
punch_x = (W - punch_w) // 2
punch_y = screen_y1 + 20
draw.rounded_rectangle([punch_x, punch_y, punch_x + punch_w, punch_y + punch_h], radius=18, fill=(0, 0, 0, 255))

# 폰트 로드 (윈도우 기본 폰트)
font_large = None
font_mid = None
font_small = None
font_bold = None

for font_name in ["malgunbd.ttf", "arialbd.ttf", "segoeui.ttf"]:
    font_path = os.path.join(r"C:\Windows\Fonts", font_name)
    if os.path.exists(font_path):
        try:
            if not font_large: font_large = ImageFont.truetype(font_path, 88)
            if not font_mid: font_mid = ImageFont.truetype(font_path, 42)
            if not font_small: font_small = ImageFont.truetype(font_path, 28)
            if not font_bold: font_bold = ImageFont.truetype(font_path, 54)
        except Exception:
            pass

if not font_large:
    font_large = font_mid = font_small = font_bold = ImageFont.load_default()

# 3.1 상단 상태바 (1997 타임슬립 팩트: 서비스 안 됨!)
draw.text((screen_x1 + 40, screen_y1 + 24), "00:05", fill=(200, 210, 225, 230), font=font_small)
draw.text((screen_x2 - 340, screen_y1 + 24), "❌ 서비스 지역 아님", fill=(240, 80, 80, 240), font=font_small)

# 3.2 날짜 헤더
draw.text((W // 2, phone_y + 180), "1997년 11월 20일 목요일", fill=(140, 160, 185, 220), font=font_small, anchor="mm")
draw.text((W // 2, phone_y + 260), "00:05:14", fill=(245, 250, 255, 255), font=font_large, anchor="mm")

# 3.3 중앙: 경고 박스 & 빨간색 배터리 1% 아이콘
box_y1 = phone_y + 440
box_y2 = phone_y + 880
draw.rounded_rectangle([screen_x1 + 40, box_y1, screen_x2 - 40, box_y2], radius=24, fill=(25, 12, 16, 230), outline=(220, 50, 70, 220), width=3)

# 배터리 심볼 렌더링
bat_w, bat_h = 240, 110
bat_x = (W - bat_w) // 2
bat_y = box_y1 + 70

# 배터리 외곽선
draw.rounded_rectangle([bat_x, bat_y, bat_x + bat_w, bat_y + bat_h], radius=18, outline=(230, 60, 80, 255), width=5)
# 배터리 + 극 단자
draw.rounded_rectangle([bat_x + bat_w + 3, bat_y + 32, bat_x + bat_w + 16, bat_y + bat_h - 32], radius=6, fill=(230, 60, 80, 255))

# 1% 잔량 게이지 (빨간색)
gauge_w = int((bat_w - 20) * 0.08)  # 8% 너비로 1% 위험 표시
draw.rounded_rectangle([bat_x + 10, bat_y + 10, bat_x + 10 + gauge_w, bat_y + bat_h - 10], radius=8, fill=(245, 45, 65, 255))

# 배터리 1% 텍스트
draw.text((W // 2, bat_y + bat_h + 60), "배터리 1% 남음", fill=(255, 70, 90, 255), font=font_bold, anchor="mm")
draw.text((W // 2, bat_y + bat_h + 120), "기지국 신호 없음 (통신 불가)", fill=(210, 180, 190, 220), font=font_mid, anchor="mm")
draw.text((W // 2, bat_y + bat_h + 180), "30초 후 디바이스 전원이 차단됩니다", fill=(180, 120, 130, 200), font=font_small, anchor="mm")

# 3.4 하단: 긴급 경고 팝업
alert_y = phone_y + 940
draw.rounded_rectangle([screen_x1 + 40, alert_y, screen_x2 - 40, alert_y + 180], radius=20, fill=(15, 22, 32, 230), outline=(80, 120, 170, 150), width=2)
draw.text((screen_x1 + 70, alert_y + 40), "⚠️ 네트워크 오류", fill=(255, 200, 90, 255), font=font_mid)
draw.text((screen_x1 + 70, alert_y + 105), "1997년 셀룰러망 감지 실패 · 공중전화 유선망 이용 권장", fill=(160, 185, 210, 220), font=font_small)

# 4. 스마트폰 화면 위로 튀긴 실제 빗방울 효과 (Macro Raindrop Layer)
import random
random.seed(1997)
rain_layer = Image.new("RGBA", (W, H), (0, 0, 0, 0))
rain_draw = ImageDraw.Draw(rain_layer)

for _ in range(65):
    rx = random.randint(screen_x1 + 10, screen_x2 - 10)
    ry = random.randint(screen_y1 + 10, screen_y2 - 10)
    rw = random.randint(6, 18)
    rh = rw + random.randint(2, 16)
    # 물방울 하이라이트
    rain_draw.ellipse([rx, ry, rx + rw, ry + rh], fill=(255, 255, 255, random.randint(40, 120)), outline=(180, 210, 240, 160), width=1)
    # 굴절 그림자
    rain_draw.arc([rx - 1, ry - 1, rx + rw + 1, ry + rh + 1], 0, 180, fill=(0, 0, 0, 90), width=2)

bg.paste(Image.alpha_composite(bg.convert("RGBA"), rain_layer).convert("RGB"))

# 5. 최종 이미지 저장
bg.save(OUTPUT_PATH, "JPEG", quality=95)
print(f"[+] ✅ 컷 03 POV 매크로 클로즈업 안착 완료: {OUTPUT_PATH} ({os.path.getsize(OUTPUT_PATH)} bytes)")
