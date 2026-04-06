@echo off
TITLE Hypercloud Launcher
echo ============================================================
echo HYPERCLOUD WINDOWS LAUNCHER
echo ============================================================
echo.

:: Check if Python is installed
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not in PATH!
    echo Please install Python from https://www.python.org/
    pause
    exit /b
)

:: Run the portable launcher script
python run_hypercloud.py

pause
