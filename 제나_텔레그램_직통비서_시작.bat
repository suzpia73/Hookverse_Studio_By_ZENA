@echo off
chcp 65001 > nul
title Hookverse Studio - 제나 텔레그램 직통 비서봇
echo ========================================================
echo 🌸 Hookverse Studio 제나 텔레그램 직통 비서봇 가동
echo 오빠가 자리 비우실 때 스마트폰 텔레그램으로 편하게 말씀하세요!
echo ========================================================
cd /d "d:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"
"C:\Users\june2\AppData\Local\Programs\Python\Python314\python.exe" tools\zena_telegram_bot.py
pause
