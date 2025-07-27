@echo off
echo Installing AI-BD Training Dependencies...
echo ========================================
cd /d "c:\Users\Admin\Desktop\React projects\aiBD"

echo.
echo Activating virtual environment...
call ".venv\Scripts\activate.bat"

echo.
echo Installing required packages...
echo This may take a few minutes...

pip install --upgrade pip
pip install Flask==2.3.3
pip install Werkzeug==2.3.7
pip install scikit-learn==1.3.0
pip install nltk==3.8.1
pip install numpy==1.24.3
pip install pandas==1.5.3
pip install joblib==1.3.2

echo.
echo Testing installation...
python -c "import sklearn, nltk, numpy, pandas; print('All packages installed successfully!')"

if %errorlevel% equ 0 (
    echo.
    echo ✓ Installation complete!
    echo ✓ Training features are now available
    echo.
    echo Run run_chatbot.bat to start AI-BD with full training features
) else (
    echo.
    echo ✗ Installation had issues
    echo You can still use the simple version without training features
)

echo.
pause
