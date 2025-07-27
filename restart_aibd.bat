@echo off
echo Restarting AI-BD with latest features...
cd /d "c:\Users\Admin\Desktop\React projects\aiBD"

echo Stopping any running instances...
taskkill /f /im python.exe 2>nul

echo Starting updated AI-BD...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" hybrid_app.py

pause
