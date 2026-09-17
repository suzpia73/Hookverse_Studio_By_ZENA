import os
import subprocess
import imageio_ffmpeg

WORKSPACE = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
test_ass = os.path.join(WORKSPACE, "assets", "subtitles", "test_wave_drop.ass")
ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()

content = """[Script Info]
ScriptType: v4.00+
PlayResX: 1080
PlayResY: 1920
ScaledBorderAndShadow: yes

[V4+ Styles]
Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding
Style: VrewWaveDrop,KyoboHandwriting2019A1,76,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,100,100,1,0,1,5.0,0.0,2,60,60,240,1

[Events]
Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text
Dialogue: 0,0:00:00.00,0:00:03.50,VrewWaveDrop,,0,0,0,,{\\move(540,1500,540,1680,0,450)\\fscx40\\fscy40\\t(0,450,\\fscx108\\fscy108)\\t(450,700,\\fscx100\\fscy100)}어둠 속에서 좁혀오는 검은 양복의 사냥꾼들.
"""

with open(test_ass, "w", encoding="utf-8") as f:
    f.write(content)

img = os.path.join(WORKSPACE, "assets", "images", "IMF2화", "IMF전날밤의비밀_ep02_cut02.jpg")
out_mp4 = os.path.join(WORKSPACE, "assets", "videos", "test_wave_drop.mp4")
fonts_dir = os.path.join(WORKSPACE, "assets", "fonts").replace("\\", "/").replace(":", r"\:")
sub_path = test_ass.replace("\\", "/").replace(":", r"\:")

vf = f"scale=1080:1920:force_original_aspect_ratio=increase,crop=1080:1920,subtitles='{sub_path}':fontsdir='{fonts_dir}'"

cmd = [
    ffmpeg, "-y", "-loop", "1", "-t", "3.5", "-i", img,
    "-vf", vf, "-c:v", "libx264", "-pix_fmt", "yuv420p", out_mp4
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("FFmpeg returncode:", res.returncode)
if res.returncode != 0:
    print(res.stderr[-500:])
else:
    print("SUCCESS! Test video created:", out_mp4)

    # Extract test frames to check the drop and scale!
    for t, label in [("0.1", "t01_drop_start"), ("0.3", "t03_dropping"), ("0.5", "t05_bounce_apex"), ("0.8", "t08_settled")]:
        snap = os.path.join(WORKSPACE, "assets", "images", "review", f"sub_motion_{label}.jpg")
        subprocess.run([ffmpeg, "-y", "-ss", t, "-i", out_mp4, "-frames:v", "1", snap], capture_output=True)
        print("Snapshot saved:", snap)
