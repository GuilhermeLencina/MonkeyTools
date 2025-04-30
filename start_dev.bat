@echo off
cd /d %~dp0

echo ========================================
echo Ativando ambiente virtual...
call venv\Scripts\activate

echo ========================================
echo Verificando processos travados na porta 5050...
for /f "tokens=5" %%a in ('netstat -aon ^| findstr :5050') do taskkill /PID %%a /F >nul 2>&1

echo ========================================
echo Configurando ambiente Flask...
set FLASK_APP=main.py
set FLASK_ENV=development

echo ========================================
echo Iniciando servidor Flask com Auto Reload...
flask run --host=127.0.0.1 --port=5050

pause
