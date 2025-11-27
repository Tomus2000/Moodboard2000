@echo off
echo ========================================
echo Starting Student Moodmeter...
echo ========================================
echo.

REM Change to the script directory
cd /d "%~dp0"

REM Start Streamlit
echo Starting Streamlit server...
echo.
py -m streamlit run app.py

REM If the above fails, try alternative methods
if %errorlevel% neq 0 (
    echo.
    echo Trying alternative method...
    python -m streamlit run app.py
)

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Could not start Streamlit!
    echo.
    echo Please make sure:
    echo 1. Python is installed (python.org)
    echo 2. Dependencies are installed: pip install -r requirements.txt
    echo 3. You are in the project directory
    echo.
    pause
)


