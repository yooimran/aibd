@echo off
setlocal enabledelayedexpansion
echo Installing AI-BD Training Features (Windows Optimized)...
cd /d "c:\Users\Admin\Desktop\React projects\aiBD"

echo.
echo Upgrading pip to latest version...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install --upgrade pip

echo.
echo Installing packages with pre-compiled wheels...
echo This may take a few minutes...

REM Install packages one by one with specific Windows-friendly versions
echo.
echo [1/4] Installing NumPy...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install numpy==1.24.3 --only-binary=all

echo.
echo [2/4] Installing Pandas...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install pandas==2.0.3 --only-binary=all

echo.
echo [3/4] Installing Scikit-learn...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install scikit-learn==1.3.0 --only-binary=all

echo.
echo [4/4] Installing NLTK...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install nltk==3.8.1 --only-binary=all

echo.
echo Downloading NLTK data...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -c "import nltk; nltk.download('punkt', quiet=True); nltk.download('stopwords', quiet=True); print('NLTK data downloaded!')"

echo.
echo Testing installation...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -c "import sklearn, nltk, numpy, pandas; print('✓ All packages installed successfully!')"
if %errorlevel% equ 0 (
    echo.
    echo ✓ Training features installed successfully!
    echo You can now use the full AI-BD with machine learning capabilities.
) else (
    echo.
    echo ✗ Installation verification failed
    echo Trying alternative installation method...
    echo.
    
    REM Try installing from a different index
    echo Installing from alternative package index...
    "C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install --trusted-host pypi.org --trusted-host pypi.python.org --trusted-host files.pythonhosted.org numpy pandas scikit-learn nltk
    
    echo.
    echo Re-testing installation...
    "C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -c "import sklearn, nltk, numpy, pandas; print('✓ All packages installed successfully!')"
    if %errorlevel% equ 0 (
        echo ✓ Training features installed successfully with alternative method!
    ) else (
        echo ✗ Installation still failed
        echo.
        echo This might be due to:
        echo 1. Missing Visual C++ Build Tools
        echo 2. Python version compatibility
        echo 3. Network restrictions
        echo.
        echo You can still use the simple version without ML features.
    )
)

echo.
pause
