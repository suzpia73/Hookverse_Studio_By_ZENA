import os
import math
from collections import deque
from typing import Tuple, Any
from PIL import Image, ImageDraw, ImageFilter

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
raw_path = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo_raw_source.png")
src_logo_path = raw_path if os.path.exists(raw_path) else os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo.png")

dst_logo1 = os.path.join(WORKSPACE, "assets", "images", "hookverse_studio_logo_transparent.png")
dst_logo2 = os.path.join(WORKSPACE, "assets", "HOOKVERSE_공식_3대_브랜딩_완제품", "03_공식원형앰블럼_636x636_투명HQ.png")
dst_review = os.path.join(WORKSPACE, "assets", "images", "review", "flawless_crystal_master_emblem.png")


def get_rgba(img: Image.Image, x: int, y: int) -> Tuple[int, int, int, int]:
    val: Any = img.getpixel((x, y))
    if isinstance(val, tuple) and len(val) >= 4:
        return int(val[0]), int(val[1]), int(val[2]), int(val[3])
    if isinstance(val, tuple) and len(val) >= 3:
        return int(val[0]), int(val[1]), int(val[2]), 255
    return 0, 0, 0, 0


def get_gray(img: Image.Image, x: int, y: int) -> int:
    val: Any = img.getpixel((x, y))
    if isinstance(val, (int, float)):
        return int(val)
    if isinstance(val, tuple) and len(val) > 0:
        return int(val[0])
    return 0


src = Image.open(src_logo_path).convert("RGBA")
W, H = src.size

cx: float = 395.0
cy: float = 390.0

r_outer: float = 314.0          # 외곽 24K 골든 림 테두리 (r > 314는 100% 무조건 투명 차단)
r_sprocket_outer: float = 304.0 # 필름 타공 링 외곽
r_sprocket_inner: float = 263.0 # 필름 타공 링 내측
r_mid_ring: float = 249.0       # 중간 금색 구분 링 (타공 링과 글자 링 사이)
r_inner: float = 216.0          # 내측 금색 링 (글자 링과 HV 중앙 로고 사이)

# -------------------------------------------------------------
# 1. 4x 슈퍼샘플링 외곽 원형 마스크 (r <= 314.0 완벽 정원)
# -------------------------------------------------------------
scale = 4
m_outer = Image.new("L", (W * scale, H * scale), 0)
d_outer = ImageDraw.Draw(m_outer)
d_outer.ellipse([(cx - r_outer)*scale, (cy - r_outer)*scale, (cx + r_outer)*scale, (cy + r_outer)*scale], fill=255)
mask_outer = m_outer.resize((W, H), Image.Resampling.LANCZOS)

# -------------------------------------------------------------
# 2. 4x 슈퍼샘플링 40개 필름 타공 구멍 완벽 일치 마스크 (대각 발광 빛 왜곡/이중현상 0%)
# -------------------------------------------------------------
mask_holes_hi = Image.new("L", (W * scale, H * scale), 0)
cx_hi = cx * scale
cy_hi = cy * scale
r_mid_hi = 278.5 * scale
half_r_hi = 13.5 * scale
half_t_hi = 13.1 * scale
corner_hi = 4.0 * scale

for k in range(40):
    ang_deg = 270.25 + k * 9.0
    ang_rad = math.radians(ang_deg)
    hx = cx_hi + r_mid_hi * math.cos(ang_rad)
    hy = cy_hi + r_mid_hi * math.sin(ang_rad)
    
    cos_t = -math.sin(ang_rad)
    sin_t = math.cos(ang_rad)
    cos_r = math.cos(ang_rad)
    sin_r = math.sin(ang_rad)
    
    pts = []
    corners = [
        (half_t_hi - corner_hi, half_r_hi - corner_hi, 0),
        (-half_t_hi + corner_hi, half_r_hi - corner_hi, 90),
        (-half_t_hi + corner_hi, -half_r_hi + corner_hi, 180),
        (half_t_hi - corner_hi, -half_r_hi + corner_hi, 270)
    ]
    for cc_t, cc_r, base_ang in corners:
        for step in range(5):
            arc_a = math.radians(base_ang + step * 22.5)
            px_loc = cc_t + corner_hi * math.cos(arc_a)
            py_loc = cc_r + corner_hi * math.sin(arc_a)
            wx = hx + px_loc * cos_t + py_loc * cos_r
            wy = hy + px_loc * sin_t + py_loc * sin_r
            pts.append((wx, wy))
            
    d_holes = ImageDraw.Draw(mask_holes_hi)
    d_holes.polygon(pts, fill=255)

mask_holes = mask_holes_hi.resize((W, H), Image.Resampling.LANCZOS)
print("[+] 40개 필름 타공 4x 슈퍼샘플링 마스크 완성!")

# -------------------------------------------------------------
# 3. 중앙 HV 로고 본체 추출 마스크 (BFS 최대 연결 요소 + V-tip 보존)
# -------------------------------------------------------------
raw_letter_mask = Image.new("L", (W, H), 0)
for y in range(H):
    for x in range(W):
        d = math.hypot(x - cx, y - cy)
        if d < 230:
            pr, pg, pb, _ = get_rgba(src, x, y)
            bright = max(pr, pg, pb)
            sat = max(pr, pg, pb) - min(pr, pg, pb)
            
            if pr < 20 and pg < 20 and pb < 20:
                continue
            is_v_tip = (pg <= 6) and (pr + pb >= 55)
            if not is_v_tip:
                if max(pr, pb) < 50 and sat < 20:
                    continue
            is_hv = False
            if is_v_tip:
                is_hv = True
            elif pb > pg + 15 and pb >= 40:
                is_hv = True
            elif pr > pg + 20 and pr >= 60 and pb >= 35:
                is_hv = True
            elif pr > 100 and pr > pg + 30:
                is_hv = True
            elif (pr >= 40 and pb >= 40) and pg <= 15:
                is_hv = True
            elif (pr + pb > 2.0 * pg + 15) and max(pr, pb) >= 55:
                is_hv = True
            elif bright > 150 and (pr > 130 or pb > 130) and abs(pr - pb) < 45:
                is_hv = True
                
            if is_hv:
                raw_letter_mask.putpixel((x, y), 255)

dilated = raw_letter_mask.filter(ImageFilter.MaxFilter(5))
closed = dilated.filter(ImageFilter.MinFilter(5))

visited = [[False]*W for _ in range(H)]
components = []
for y in range(H):
    for x in range(W):
        if get_gray(closed, x, y) == 255 and not visited[y][x]:
            comp = []
            q = deque([(x, y)])
            visited[y][x] = True
            while q:
                curr_x, curr_y = q.popleft()
                comp.append((curr_x, curr_y))
                for dx, dy in [(-1,0), (1,0), (0,-1), (0,1)]:
                    nx, ny = curr_x + dx, curr_y + dy
                    if 0 <= nx < W and 0 <= ny < H:
                        if not visited[ny][nx] and get_gray(closed, nx, ny) == 255:
                            visited[ny][nx] = True
                            q.append((nx, ny))
            components.append(comp)

components.sort(key=len, reverse=True)
hv_pure_mask = Image.new("L", (W, H), 0)
for x, y in components[0]:
    hv_pure_mask.putpixel((x, y), 255)

hv_alpha = hv_pure_mask.filter(ImageFilter.GaussianBlur(1.0))
print("[+] 중앙 HV 로고 100% 순수 마스크 추출 완료!")

# -------------------------------------------------------------
# 4. 무결점 원형 엠블럼 최종 합성
# -------------------------------------------------------------
result = Image.new("RGBA", (W, H), (0, 0, 0, 0))

for y in range(H):
    for x in range(W):
        o_val: int = get_gray(mask_outer, x, y)
        if o_val == 0:
            continue
            
        d = math.hypot(x - cx, y - cy)
        pr, pg, pb, _ = get_rgba(src, x, y)
        bright = max(pr, pg, pb)
        sat = bright - min(pr, pg, pb)
        
        letter_a: int = get_gray(hv_alpha, x, y)
        hole_val: int = get_gray(mask_holes, x, y)
        
        if d < r_inner:
            if letter_a > 15:
                fa: int = int(letter_a * (o_val / 255.0))
                result.putpixel((x, y), (pr, pg, pb, fa))
        elif r_inner <= d < r_mid_ring:
            if letter_a > 120 and (pg <= 10 or (pr >= 40 and pb >= 40)):
                result.putpixel((x, y), (pr, pg, pb, o_val))
            else:
                if bright < 45 and sat < 20:
                    result.putpixel((x, y), (14, 12, 10, o_val))
                elif bright < 75 and sat < 30:
                    t = (bright - 45) / 30.0
                    nr = int(14 * (1.0 - t) + pr * t)
                    ng = int(12 * (1.0 - t) + pg * t)
                    nb = int(10 * (1.0 - t) + pb * t)
                    result.putpixel((x, y), (nr, ng, nb, o_val))
                else:
                    result.putpixel((x, y), (pr, pg, pb, o_val))
        elif r_mid_ring <= d < r_sprocket_inner:
            result.putpixel((x, y), (pr, pg, pb, o_val))
        elif r_sprocket_inner <= d < r_sprocket_outer:
            if hole_val > 0:
                hole_alpha: int = int(o_val * (1.0 - hole_val / 255.0))
                if hole_alpha > 0:
                    result.putpixel((x, y), (pr, pg, pb, hole_alpha))
            else:
                result.putpixel((x, y), (pr, pg, pb, o_val))
        else:
            result.putpixel((x, y), (pr, pg, pb, o_val))

# -------------------------------------------------------------
# 5. 628x628 완벽 정원 크롭 및 단일 진실 공급원(SSOT) 동시 배포
# -------------------------------------------------------------
crop_box = (int(cx - r_outer), int(cy - r_outer), int(cx + r_outer), int(cy + r_outer))
final_emblem = result.crop(crop_box)

final_emblem.save(dst_logo1, "PNG")
final_emblem.save(dst_logo2, "PNG")
final_emblem.save(dst_review, "PNG")

print(f"[+] 🎉 628x628 무결점 원형 엠블럼 제작 및 배포 완료!")
print(f"    - 공식 1: {dst_logo1}")
print(f"    - 공식 2: {dst_logo2}")
print(f"    - 리뷰용: {dst_review}")
