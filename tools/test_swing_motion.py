import subprocess
import imageio_ffmpeg

ffmpeg_exe = imageio_ffmpeg.get_ffmpeg_exe()
logo_path = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\hookverse_studio_logo_transparent.png"
output_test = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\videos\test_swing.mp4"

# Pendulum swing:
# 1) Angle tilts with sin: a = sin(2*PI*t/1.8) * 0.18  (~10.3 degrees)
# 2) Position sways left-right: x = 860 + sin(2*PI*t/1.8) * 20
# 3) Height lifts slightly at peak of swing (pendulum physics): y = 35 - cos(4*PI*t/1.8)*4
filter_str = (
    "color=c=black:s=1080x1920:d=3,format=rgba[bg];"
    f"[0:v]scale=165:165,format=rgba,rotate='a=sin(2*PI*t/1.8)*0.18:ow=hypot(iw,ih):oh=ow:c=none'[logo];"
    f"[bg][logo]overlay=x='860 + sin(2*PI*t/1.8)*20 - (w-165)/2':y='35 - cos(4*PI*t/1.8)*4 - (h-165)/2'[v]"
)

cmd = [
    ffmpeg_exe, "-y",
    "-i", logo_path,
    "-filter_complex", filter_str,
    "-map", "[v]",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-t", "3",
    output_test
]

res = subprocess.run(cmd, capture_output=True, text=True)
print("Return code:", res.returncode)
if res.returncode != 0:
    print("Stderr:", res.stderr[-500:])
else:
    print("Success! Test swing video created at:", output_test)
