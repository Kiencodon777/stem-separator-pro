@echo off
chcp 65001 >nul
title Stem Separator Pro v2.5 - Khởi Chạy
color 0b

echo ========================================================
echo        STEM SEPARATOR PRO v2.5 - KHỞI CHẠY HỆ THỐNG
echo ========================================================
echo.

set "PYTHON_EXE=c:\Users\anhan\Downloads\Sdk\karaoke_engine\.venv\Scripts\python.exe"
set "SERVER_SCRIPT=%~dp0server.py"

if not exist "%PYTHON_EXE%" (
    echo [LOI] Khong tim thay Python venv tai:
    echo %PYTHON_EXE%
    echo Vui long kiem tra lai thu muc!
    pause
    exit /b 1
)

echo [*] Dang khoi dong Web Server tren cong 8090...
echo [*] Trinh duyet se tu dong mo sau vai giay...
echo.

:: Mo trinh duyet sau 2 giay
start "" powershell -Command "Start-Sleep -Seconds 2; Start-Process 'http://localhost:8090'"

:: Chay FastAPI Server
"%PYTHON_EXE%" "%SERVER_SCRIPT%"

if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [THONG BAO] Server da dung hoac gap su co.
    pause
)
