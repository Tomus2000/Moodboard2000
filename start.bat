@echo off
echo Starting Student Moodmeter...
echo.

REM Try different Python commands
python -m streamlit run app.py 2>nul
if %errorlevel% neq 0 (
    py -m streamlit run app.py 2>nul
    if %errorlevel% neq 0 (
        echo.
        echo ERROR: Python not found!
        echo.
        echo Please install Python 3.10+ from https://www.python.org/
        echo Or make sure Python is in your PATH.
        echo.
        pause
    )
)


