@echo off
cd /d "%~dp0"
echo Starting Streamlit app...
echo.
py -m streamlit run app.py --server.port 8501 --server.headless false
pause



