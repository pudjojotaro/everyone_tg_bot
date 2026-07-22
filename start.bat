@echo off
setlocal
cd /d "%~dp0"

where python >nul 2>nul
if errorlevel 1 (
    echo Python was not found on this PC.
    echo Install it from https://www.python.org/downloads/ ^(check "Add Python to PATH" during install^), then double-click this file again.
    pause
    exit /b 1
)

if not exist venv (
    echo Creating virtual environment...
    python -m venv venv
    call venv\Scripts\activate.bat
    echo Installing dependencies...
    pip install -q -r requirements.txt
) else (
    call venv\Scripts\activate.bat
)

if not exist .env (
    echo.
    echo First-time setup: paste your bot token from @BotFather below.
    set /p BOT_TOKEN=Bot token:
    echo BOT_TOKEN=%BOT_TOKEN%> .env
)

echo.
echo Starting the bot... ^(close this window to stop it^)
python bot.py

pause
