@echo off
echo Starting AI-BD with Training Features...
cd /d "c:\Users\Admin\Desktop\React projects\aiBD"

echo Checking training dependencies...
"C:/Users/Admin/Desktop\React projects\aiBD/.venv/Scripts/python.exe" -c "import sklearn, nltk, numpy, pandas; print('Training modules available!')" 2>nul
if %errorlevel% neq 0 (
    echo Training modules not installed!
    echo Run install_training.bat to install them.
    echo Starting simple version instead...
    echo.
    "C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" simple_app.py
) else (
    echo Training modules found! Starting full version...
    "C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" app.py
)

pause
