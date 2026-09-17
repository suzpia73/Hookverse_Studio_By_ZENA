@echo off
chcp 65001 > nul
echo =====================================================================
echo [Hookverse Studio] Episode 02 Master Video Production Pipeline
echo =====================================================================

set PYTHON_EXE=C:\Users\june2\AppData\Local\Programs\Python\Python314\python.exe

if not exist "%PYTHON_EXE%" (
    echo [-] Python executable not found at %PYTHON_EXE%
    exit /b 1
)

echo [*] Python located: %PYTHON_EXE%
echo [*] Running standard_cinema_engine.py...

"%PYTHON_EXE%" tools\standard_cinema_engine.py

if %ERRORLEVEL% equ 0 (
    echo [+] =====================================================================
    echo [+] SUCCESS: Episode 02 Master Video & Verification Snapshots Completed!
    echo [+] =====================================================================
) else (
    echo [-] FAILED with error code %ERRORLEVEL%
    exit /b %ERRORLEVEL%
)
