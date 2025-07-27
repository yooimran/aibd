@echo off
setlocal enabledelayedexpansion
echo Starting AI-BD Chatbot...
cd /d "c:\Users\Admin\Desktop\React projects\aiBD"

echo Checking Python environment...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -c "import sys; print('Python version:', sys.version)" 2>nul
if %errorlevel% neq 0 (
    echo Error: Python environment not found!
    echo Please run the setup again.
    pause
    exit /b 1
)

echo Starting AI-BD...
echo.
echo Checking for training features...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -c "import sklearn, nltk, numpy, pandas; print('Training features available!')" 2>nul
if %errorlevel% neq 0 (
    echo Training features not installed.
    echo.
    echo Options:
    echo 1. Continue with simple version (basic AI)
    echo 2. Install full training features (requires Visual C++ Build Tools)
    echo 3. Install lightweight training features (recommended for Windows)
    echo.
    set /p choice="Choose option (1, 2, or 3): "
    if "!choice!"=="2" (
        echo.
        echo Installing full training features...
        call install_training_windows.bat
        echo.
        echo Starting AI-BD with training features...
        "C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" hybrid_app.py
    ) else if "!choice!"=="3" (
        echo.
        echo Installing lightweight training features...
        call install_training_lite.bat
        echo.
        echo Starting AI-BD with lightweight training...
        "C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" hybrid_app.py
    ) else (
        echo.
        echo Starting basic version...
        "C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" hybrid_app.py
    )
) else (
    echo Training features found! Starting full version...
    "C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" hybrid_app.py
)

pause
