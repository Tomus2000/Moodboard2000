@echo off
echo ============================================
echo Starting Student Moodmeter Streamlit App
echo ============================================
echo.
echo Make sure you have:
echo 1. Installed dependencies: pip install -r requirements.txt
echo 2. Downloaded NLTK data: python -c "import nltk; nltk.download('stopwords'); nltk.download('punkt')"
echo 3. Created .env file with your configuration
echo.
echo Starting Streamlit...
echo.

cd /d "%~dp0"

REM Try to start Streamlit
py -m streamlit run app.py

if %errorlevel% neq 0 (
    echo.
    echo ERROR: Could not start Streamlit!
    echo.
    echo Trying alternative method...
    python -m streamlit run app.py
)

if %errorlevel% neq 0 (
    echo.
    echo ============================================
    echo STREAMLIT FAILED TO START
    echo ============================================
    echo.
    echo Please check:
    echo 1. Python is installed: py --version
    echo 2. Streamlit is installed: py -m pip list | findstr streamlit
    echo 3. All dependencies are installed: py -m pip install -r requirements.txt
    echo 4. There are no errors in app.py
    echo.
    echo To test if Streamlit works, try:
    echo   py -m streamlit run test_streamlit.py
    echo.
    pause
)


