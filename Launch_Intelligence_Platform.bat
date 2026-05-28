@echo off
title Resume Parser AI Project Launcher
color 0A
cls
echo =======================================================================
echo                      RESUME PARSER AI PROJECT
echo =======================================================================
echo.
echo   [1/3] Verifying and installing required python dependencies...
echo         * Running pip install -r requirements.txt...
echo.
python -m pip install -r requirements.txt

echo.
echo   [2/3] Booting Flask Application Server...
echo         * Pre-training Multi-Classifier ML Models...
echo         * Seeding SQLite Database tables...
echo.
:: Start Flask server in minimized console
start "Flask Recruitment Server" /min cmd /c "python app.py"

:: Delay for ML fit and DB setup
timeout /t 5 /nobreak >nul

echo   [3/3] Opening Interactive Recruiter Dashboard...
echo         * Launching browser UI at http://127.0.0.1:5000...
echo.
start "" "http://127.0.0.1:5000"

echo =======================================================================
echo   STATUS: COMPLETED & ACTIVE!
echo =======================================================================
echo.
echo   - Recruiter Hub: http://127.0.0.1:5000
echo   - AI Chatbot:    http://127.0.0.1:5000/chatbot
echo   - Analytics:     http://127.0.0.1:5000/analytics
echo.
echo   Press any key to exit this launcher window...
pause >nul
