import os
import subprocess
import imageio_ffmpeg

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
test_ass = os.path.join(WORKSPACE, "assets", "subtitles", "test_vrew_purple_sub.ass")
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

# Exact Vrew styling:
# Fontsize: 90pt (Vrew 300pt)
# PrimaryColour: &H00FFFFFF (Pure White)
# OutlineColour: &H00D030A0 (Vibrant Purple / Neon Violet #A030D0)
# BackColour: &H80000000 (Soft Black Shadow for contrast)
# Outline: 5.2, Shadow: 2.0
# Motion:
# Start at Y=1380, scale 25% (뉴라의 손목/팔뚝쯤)
# Drop towards bottom with 112% scale at t=380ms
# Settle to Y=1725 with 100% scale at t=550ms

content = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: VrewPurple,KyoboHandwriting2019A1,90,&H00FFFFFF,&H000000FF,&H00D030A0,&H80000000,1,0,0,0,100,100,1,0,1,5.2,2.0,2,60,60,195,1
Style: VrewPurpleEmphasis,KyoboHandwriting2019A1,95,&H00FFFFFF,&H000000FF,&H00D030A0,&H80000000,1,0,0,0,100,100,1,0,1,5.8,2.2,2,60,60,195,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:03.50,VrewPurple,,0,0,0,,{\\move(540,1380,540,1725,0,380)\\fscx25\\fscy25\\t(0,380,\\fscx112\\fscy112)\\t(380,550,\\fscx100\\fscy100)}어둠 속에서 좁혀오는 검은 양복의 사냥꾼들.
"""

with open(test_ass, "w", encoding="utf-8") as f:
    f.write(content)

img = os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut02.jpg")
out_mp4 = os.path.join(WORKSPACE, "assets", "videos", "test_vrew_purple.mp4")
fonts_dir = os.path.join(WORKSPACE, "assets", "fonts").replace("\\", "/").replace(":", r"\:")
sub_path = test_ass.replace("\\", "/").replace(":", r"\:")

vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles='{sub_path}':fontsdir='{fonts_dir}'"

cmd = [
    ffmpeg, "-y", "-loop", "1", "-t", "3.5", "-i", img,
    "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", out_mp4
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("FFmpeg returncode:", res.returncode)
if res.returncode == 0:
    for t, label in [("0.05", "01_start_wrist"), ("0.25", "02_mid_drop"), ("0.38", "03_bottom_overshoot"), ("0.8", "04_settled_final")]:
        snap = os.path.join(WORKSPACE, "assets", "images", "review", f"sub_purple_{label}.jpg")
        subprocess.run([ffmpeg, "-y", "-ss", t, "-i", out_mp4, "-frames:v", "1", snap], capture_output=True)
        print("Saved:", snap)
