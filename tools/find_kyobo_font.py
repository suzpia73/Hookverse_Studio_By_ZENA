import os
import glob

# Check Windows fonts
win_fonts = glob.glob(r"C:\Windows\Fonts\*kyobo*") + glob.glob(r"C:\Windows\Fonts\*Kyobo*") + glob.glob(r"C:\Windows\Fonts\*손글씨*")
print("Windows fonts:", win_fonts)

# Also check AppData fonts (where Vrew often downloads fonts)
appdata_fonts = glob.glob(r"C:\Users\june2\AppData\Local\Microsoft\Windows\Fonts\*")
kyobo_appdata = [f for f in appdata_fonts if "kyobo" in f.lower() or "손글씨" in f]
print("AppData fonts:", kyobo_appdata)

# Check Vrew cache / fonts
vrew_paths = glob.glob(r"C:\Users\june2\AppData\Local\*vrew*\*font*") + glob.glob(r"C:\Users\june2\AppData\Roaming\*vrew*\*font*")
print("Vrew font paths:", vrew_paths)
