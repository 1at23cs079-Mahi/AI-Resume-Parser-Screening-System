@echo off
title Resume Parser AI Launcher
color 0B
cls
echo =====================================================================
echo               RESUME PARSER AI - INTERNSHIP PROJECT
echo =====================================================================
echo.
echo   [1/2] Launching Python FastAPI Backend Server...
echo         * Running NLTK pre-processor pipelines...
echo         * Pre-training TF-IDF Vectorizer and KMeans clustering...
echo.

:: Start the backend in a separate terminal window
start "FastAPI Backend Server" /min cmd /c "cd backend && python -m uvicorn main:app --host 127.0.0.1 --port 8000"

:: Small wait for server startup
timeout /t 3 /nobreak >nul

echo   [2/2] Opening Interactive Screening Dashboard...
echo         * Launching premium React/Tailwind front-end in default browser...
echo.

:: Open frontend in default browser
start "" "frontend\index.html"

echo =====================================================================
echo   STATUS: ACTIVE AND RUNNING!
echo =====================================================================
echo.
echo   - Backend API: http://127.0.0.1:8000
echo   - Frontend:    frontend\index.html
echo.
echo   To close the server, close the minimized "FastAPI Backend Server" window.
echo.
echo   Press any key to exit this launcher launcher window...
pause >nul
