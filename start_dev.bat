@echo off
cd /d %~dp0
title MonkeyTools - Startup

REM === ATIVAR ANSI ESCAPE SEQUENCES ===
>nul reg query HKCU\Console | find "VirtualTerminalLevel" >nul
if errorlevel 1 reg add HKCU\Console /v VirtualTerminalLevel /t REG_DWORD /d 1 >nul

REM === DEFINIR CORES ===
set "ok=[[92mOK[0m]"
set "warn=[[93mAVISO[0m]"
set "err=[[91mERRO[0m]"

echo %ok% Iniciando MonkeyTools...

REM === VERIFICAR AMBIENTE VIRTUAL ===
if not exist "venv\Scripts\activate.bat" (
    echo %err% Ambiente virtual não encontrado em 'venv\'!
    echo.
    echo     Para criar: python -m venv venv
    pause
    exit /b
)

echo %ok% Ativando ambiente virtual...
call venv\Scripts\activate.bat

REM === VERIFICAR .env ===
if not exist ".env" (
    echo %warn% Arquivo .env não encontrado!
    echo.
    echo     Crie um .env com SECRET_KEY e DATABASE_URL antes de continuar.
    pause
    exit /b
)

REM === MATAR PROCESSOS NA PORTA 5050 ===
echo %ok% Limpando processos na porta 5050...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5050') do taskkill /PID %%a /F >nul 2>&1

REM === CONFIGURAR FLASK ===
set FLASK_APP=main.py
set FLASK_ENV=development

echo %ok% Iniciando servidor Flask...
flask run --host=127.0.0.1 --port=5050

pause
