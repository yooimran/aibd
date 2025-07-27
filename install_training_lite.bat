
@echo off
setlocal enabledelayedexpansion
echo Installing AI-BD Training Features (Lightweight Version)...
cd /d "c:\Users\Admin\Desktop\React projects\aiBD"

echo.
echo This version uses lightweight alternatives that don't require compilation:
echo - NumPy: Essential for numerical operations
echo - NLTK: Natural language processing
echo - Joblib: Already installed for model persistence
echo.

echo Upgrading pip...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install --upgrade pip

echo.
echo Installing lightweight packages...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install numpy nltk

echo.
echo Downloading NLTK data...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); print('NLTK data ready!')"

echo.
echo Testing installation...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -c "import numpy, nltk; print('✓ Core packages installed!')"

if %errorlevel% equ 0 (
    echo.
    echo ✓ Lightweight training features installed!
    echo Note: This version has basic ML capabilities without pandas/sklearn
) else (
    echo ✗ Installation failed
)

echo.
pause
