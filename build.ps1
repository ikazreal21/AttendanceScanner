# Attendance Scanner Executable Builder
# PowerShell Script

Write-Host "============================================================" -ForegroundColor Green
Write-Host "Attendance Scanner - Executable Builder" -ForegroundColor Green
Write-Host "============================================================" -ForegroundColor Green
Write-Host ""

# Check if Python is installed
try {
    $pythonVersion = python --version 2>&1
    Write-Host "Python found: $pythonVersion" -ForegroundColor Green
} catch {
    Write-Host "Error: Python is not installed or not in PATH" -ForegroundColor Red
    Write-Host "Please install Python 3.8+ and try again" -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Check if we're in the right directory
if (-not (Test-Path "manage.py")) {
    Write-Host "Error: manage.py not found. Please run this script from the Django project root." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Install PyInstaller
Write-Host "Installing PyInstaller..." -ForegroundColor Yellow
try {
    pip install pyinstaller
    Write-Host "PyInstaller installed successfully!" -ForegroundColor Green
} catch {
    Write-Host "Error installing PyInstaller. Please check your internet connection." -ForegroundColor Red
    Read-Host "Press Enter to exit"
    exit 1
}

# Run the build script
Write-Host "Building executable..." -ForegroundColor Yellow
try {
    python build_exe.py
    Write-Host "Build completed successfully!" -ForegroundColor Green
    Write-Host "Check the 'dist' folder for your executable." -ForegroundColor Green
} catch {
    Write-Host "Error during build process. Please check the error messages above." -ForegroundColor Red
}

Write-Host ""
Read-Host "Press Enter to exit" 