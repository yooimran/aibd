@echo off
echo.
echo ===============================================
echo   AI-BD Training Features Quick Installer
echo ===============================================
echo.
echo This will install machine learning libraries for:
echo • Advanced AI responses
echo • Feedback system (👍👎 buttons)
echo • Training analytics
echo • Response learning
echo.
echo Installation may take 2-5 minutes...
echo.
set /p confirm="Install training features? (y/n): "
if /i not "%confirm%"=="y" goto :end

echo.
echo Installing packages...
cd /d "c:\Users\Admin\Desktop\React projects\aiBD"

echo • Upgrading pip...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install --upgrade pip --quiet

echo • Installing Flask...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install Flask==2.3.3 --quiet

echo • Installing scikit-learn...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install scikit-learn==1.3.0 --quiet

echo • Installing NLTK...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install nltk==3.8.1 --quiet

echo • Installing NumPy...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install numpy==1.24.3 --quiet

echo • Installing Pandas...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install pandas==1.5.3 --quiet

echo • Installing Joblib...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -m pip install joblib==1.3.2 --quiet

echo.
echo Testing installation...
"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" -c "import sklearn, nltk, numpy, pandas; print('✓ All packages installed successfully!')"

if %errorlevel% equ 0 (
    echo.
    echo ✓ Training features installed successfully!
    echo ✓ AI-BD now has advanced learning capabilities
    echo.
    echo You can now:
    echo • Use feedback buttons (👍👎) to train AI
    echo • Access training panel (🧠 icon)
    echo • View training analytics
    echo • Teach AI-BD custom responses
    echo.
    echo Starting AI-BD with training features...
    echo.
    "C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" app.py
) else (
    echo.
    echo ✗ Installation had issues
    echo You can still use the simple version
    echo.
    echo Starting simple version...
    "C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" simple_app.py
)

:end
pause
