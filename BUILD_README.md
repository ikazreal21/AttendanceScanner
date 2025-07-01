# Building Attendance Scanner Executable

This directory contains scripts to create a standalone executable (.exe) file for the Attendance Scanner Django application.

## Quick Start

### Option 1: Using Batch File (Windows)

1. Double-click `build.bat`
2. Wait for the build process to complete
3. Find your executable in the `dist` folder

### Option 2: Using PowerShell (Windows)

1. Right-click `build.ps1` and select "Run with PowerShell"
2. Wait for the build process to complete
3. Find your executable in the `dist` folder

### Option 3: Using Python Script

1. Open command prompt in this directory
2. Run: `python build_exe.py`
3. Find your executable in the `dist` folder

## Prerequisites

- Python 3.8 or higher
- All Django project dependencies installed (`pip install -r requirements.txt`)
- Windows operating system (for .exe creation)

## What the Scripts Do

1. **Install PyInstaller**: Automatically installs PyInstaller if not already installed
2. **Create Launcher**: Generates a launcher script that properly initializes Django
3. **Build Executable**: Uses PyInstaller to create a single .exe file
4. **Include Dependencies**: Packages all necessary files (templates, static files, database)
5. **Create Documentation**: Generates a README for the executable

## Output

After successful build, you'll find:

- `dist/AttendanceScanner.exe` - The main executable
- `dist/README.txt` - Instructions for using the executable

## Using the Executable

1. **Run the executable**: Double-click `AttendanceScanner.exe`
2. **Access the application**: Open your browser and go to `http://127.0.0.1:8000`
3. **Stop the application**: Press Ctrl+C in the console window

## Troubleshooting

### Common Issues

1. **Python not found**: Make sure Python is installed and in your PATH
2. **Dependencies missing**: Run `pip install -r requirements.txt` first
3. **Port 8000 in use**: Close other applications using port 8000
4. **Permission errors**: Run as administrator if needed

### Build Errors

If the build fails:

1. Check that all Django dependencies are installed
2. Ensure you're running the script from the project root directory
3. Try running the Python script directly: `python build_exe.py`
4. Check the console output for specific error messages

## File Structure

```
├── build_exe.py          # Main Python build script
├── build.bat             # Windows batch file
├── build.ps1             # PowerShell script
├── build_requirements.txt # Minimal requirements for building
├── BUILD_README.md       # This file
└── dist/                 # Output directory (created after build)
    ├── AttendanceScanner.exe
    └── README.txt
```

## Notes

- The executable includes all necessary dependencies
- The database file (db.sqlite3) is included in the executable
- Templates and static files are packaged with the executable
- The executable runs a Django development server on localhost:8000
- No additional software installation is required on target machines
