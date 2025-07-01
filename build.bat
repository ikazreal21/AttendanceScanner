@echo off
echo ============================================================
echo Attendance Scanner - Executable Builder
echo ============================================================
echo.

echo Checking Python installation...
python --version
if errorlevel 1 (
    echo Error: Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

echo.
echo Installing required packages...
pip install pyinstaller

echo.
echo Building executable...
python build_exe.py

echo.
echo Build process completed!
echo Check the 'dist' folder for your executable.
echo.
pause 