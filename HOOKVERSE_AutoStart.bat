@echo off
:: HOOKVERSE 자동 실행기 — PC 켤 때 바로 실행
:: 이 파일을 시작프로그램 폴더에 넣으면 로그인할 때마다 자동 시작

title HOOKVERSE AutoRunner
echo [HOOKVERSE] 에이전트 자동 실행 시작...
cd /d "D:\HOOKVERSE-SYSTEM\HOOKVERSE_STUDIO_V2"

:: 로그인 직후 네트워크와 로컬 AI가 준비될 시간을 넉넉히 확보
timeout /t 180 /nobreak > nul

:: 로그인 직후 한 번 실행 (오후에 PC를 켜도 당일 작업 처리)
start "HOOKVERSE_RunNow" /min python auto_runner.py --now

:: 백그라운드 상주 스케줄러 실행 (매일 15:00 대기)
start "HOOKVERSE_Scheduler" /min python auto_runner.py --time 15:00


echo [HOOKVERSE] 오늘의 자동 작업을 백그라운드에서 실행합니다.
timeout /t 3 /nobreak > nul
