@echo off
echo Building Attendance Scanner Executable...
echo.

REM Check if PyInstaller is installed
python -c "import PyInstaller" 2>nul
if errorlevel 1 (
    echo Installing PyInstaller...
    pip install pyinstaller
)

REM Install all required dependencies
echo Installing required dependencies...
pip install -r requirements.txt

REM Build the executable
echo Building executable...
pyinstaller attendance_scanner.spec

echo.
echo Build complete! The executable is in the 'dist' folder.
echo You can run 'AttendanceScanner.exe' to start the application.
pause