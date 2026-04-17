@echo off
TITLE Swasthya Sahayak - Local AI Servers
COLOR 0A

echo ==========================================
echo    SWASTHYA SAHAYAK - LOCAL AI ENGINE
echo ==========================================
echo.
echo [1/2] Launching Backend AI (Port 8000)...
start /B cmd /c "cd backend && python -m uvicorn main:app --port 8000"

echo [2/2] Launching Frontend UI (Port 5173)...
start /B cmd /c "cd frontend && npm run dev"

echo.
echo ==========================================
echo Servers are running!
echo UI: http://localhost:5173
echo.
echo IMPORTANT: KEEP THIS WINDOW OPEN!
echo If you close this, the site will stop working.
echo ==========================================
pause
