@echo off
chcp 65001 > nul
set OUT_DIR=d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2\assets\fonts
if not exist "%OUT_DIR%" mkdir "%OUT_DIR%"
set OUT_FILE=%OUT_DIR%\FontdinerSwanky-Regular.ttf

echo [*] Checking local Vrew font cache...
powershell -Command "Get-ChildItem -Path $env:LOCALAPPDATA, $env:APPDATA -Recurse -Filter '*Fontdiner*' -ErrorAction SilentlyContinue | Select-Object -First 1 -ExpandProperty FullName" > "%TEMP%\fontpath.txt"
set /p LOCAL_FONT=<"%TEMP%\fontpath.txt"

if exist "%LOCAL_FONT%" (
    echo [+] Found in local cache: %LOCAL_FONT%
    copy /y "%LOCAL_FONT%" "%OUT_FILE%"
    goto :done
)

echo [*] Downloading from Google Fonts...
curl -L -k -o "%OUT_FILE%" "https://github.com/google/fonts/raw/main/ofl/fontdinerswanky/FontdinerSwanky-Regular.ttf"

:done
if exist "%OUT_FILE%" (
    echo [+] Successfully acquired: %OUT_FILE%
) else (
    echo [-] Failed to acquire font.
)
