@echo off
echo Creating AI-BD Training Data Structure...
echo ========================================
cd /d "c:\Users\Admin\Desktop\React projects\aiBD"

"C:/Users/Admin/Desktop/React projects/aiBD/.venv/Scripts/python.exe" create_training_data.py

echo.
echo Opening training data folder...
explorer "training_data"

pause
