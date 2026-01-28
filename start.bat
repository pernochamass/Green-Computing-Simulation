@echo off
echo ====================================================================
echo Green Computing Power Manager - Quick Start
echo Group 40 - Operating Systems Project
echo ====================================================================
echo.

echo [1/3] Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo ERROR: Python is not installed or not in PATH
    echo Please install Python from https://www.python.org/
    pause
    exit /b 1
)
echo Python found!
echo.

echo [2/3] Installing dependencies...
if exist myenv\Scripts\activate.bat (
    echo Activating virtual environment...
    call myenv\Scripts\activate.bat
)
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)
echo Dependencies installed!
echo.

echo [3/3] Starting backend server...
echo.
echo ====================================================================
echo INSTRUCTIONS:
echo 1. Backend server will start below
echo 2. Keep this window open
echo 3. Open 'index_integrated.html' in your browser
echo 4. Click "Start Monitoring"
echo ====================================================================
echo.
echo Press Ctrl+C to stop the server when done
echo.

python power_backend.py

pause
