import subprocess
import imageio_ffmpeg

ffmpeg = imageio_ffmpeg.get_ffmpeg_exe()
v = r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\videos\test_swing.mp4"
subprocess.run([ffmpeg, "-y", "-ss", "00:00:00.45", "-i", v, "-vframes", "1", r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\test_swing_right.jpg"])
subprocess.run([ffmpeg, "-y", "-ss", "00:00:01.35", "-i", v, "-vframes", "1", r"d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\images\review\test_swing_left.jpg"])
print("Snapshots saved.")
