#!/usr/bin/env python
"""
Build script for creating an executable of the Attendance Scanner Django application.
This script uses PyInstaller to create a standalone .exe file.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path

def install_pyinstaller():
    """Install PyInstaller if not already installed."""
    try:
        import PyInstaller
        print("PyInstaller is already installed.")
    except ImportError:
        print("Installing PyInstaller...")
        subprocess.check_call([sys.executable, "-m", "pip", "install", "pyinstaller"])
        print("PyInstaller installed successfully.")

def create_spec_file():
    """Create a PyInstaller spec file for the Django application."""
    spec_content = '''# -*- mode: python ; coding: utf-8 -*-

block_cipher = None

a = Analysis(
    ['manage.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('scanner/templates', 'scanner/templates'),
        ('static', 'static'),
        ('AttendanceScanner', 'AttendanceScanner'),
        ('db.sqlite3', '.'),
    ],
    hiddenimports=[
        'django',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        'scanner',
        'scanner.models',
        'scanner.views',
        'scanner.forms',
        'scanner.admin',
        'scanner.urls',
        'AttendanceScanner.settings',
        'AttendanceScanner.urls',
        'AttendanceScanner.wsgi',
        'django.db.backends.sqlite3',
        'django.template.loaders.filesystem',
        'django.template.loaders.app_directories',
    ],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)

pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.zipfiles,
    a.datas,
    [],
    name='AttendanceScanner',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
'''
    
    with open('AttendanceScanner.spec', 'w') as f:
        f.write(spec_content)
    print("Created PyInstaller spec file: AttendanceScanner.spec")

def create_launcher_script():
    """Create a launcher script that will be the entry point for the executable."""
    launcher_content = '''#!/usr/bin/env python
"""
Launcher script for Attendance Scanner Django application.
This script sets up the Django environment, starts the development server, and opens the browser.
"""

import os
import sys
import django
import threading
import webbrowser
import time
from pathlib import Path

def setup_django():
    """Set up Django environment."""
    # Find the directory containing this script
    current_dir = Path(__file__).parent.resolve()
    # Change working directory to where manage.py is
    os.chdir(current_dir)
    print(f"Changed working directory to: {os.getcwd()}")
    sys.path.insert(0, str(current_dir))
    # Set Django settings module
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'AttendanceScanner.settings')
    # Configure Django
    django.setup()

def open_browser():
    """Open the default web browser to the app URL after a short delay."""
    time.sleep(2)  # Wait for server to start
    webbrowser.open('http://127.0.0.1:8000')

def main():
    """Main function to run the Django development server and open browser."""
    try:
        setup_django()
        print("=" * 60)
        print("Attendance Scanner System")
        print("=" * 60)
        print("Starting the application...")
        print("The application will be available at: http://127.0.0.1:8000")
        print("A browser window will open automatically.")
        print("Press Ctrl+C to stop the server")
        print("=" * 60)
        # Start a thread to open the browser
        threading.Thread(target=open_browser, daemon=True).start()
        # Import and run Django management command
        from django.core.management import execute_from_command_line
        manage_py_path = str(Path(__file__).parent / 'manage.py')
        execute_from_command_line([manage_py_path, 'runserver', '127.0.0.1:8000'])
    except KeyboardInterrupt:
        print("\\nShutting down server...")
    except Exception as e:
        print(f"Error starting the application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()
'''
    
    with open('launcher.py', 'w') as f:
        f.write(launcher_content)
    print("Created launcher script: launcher.py")

def build_executable():
    """Build the executable using PyInstaller."""
    print("Building executable...")
    
    # Run PyInstaller
    cmd = [
        sys.executable, "-m", "PyInstaller",
        "--onefile",
        "--console",
        "--name=AttendanceScanner",
        "--add-data=scanner/templates;scanner/templates",
        "--add-data=static;static",
        "--add-data=AttendanceScanner;AttendanceScanner",
        "--add-data=db.sqlite3;.",
        "--hidden-import=django",
        "--hidden-import=django.contrib.admin",
        "--hidden-import=django.contrib.auth",
        "--hidden-import=django.contrib.contenttypes",
        "--hidden-import=django.contrib.sessions",
        "--hidden-import=django.contrib.messages",
        "--hidden-import=django.contrib.staticfiles",
        "--hidden-import=scanner",
        "--hidden-import=scanner.models",
        "--hidden-import=scanner.views",
        "--hidden-import=scanner.forms",
        "--hidden-import=scanner.admin",
        "--hidden-import=scanner.urls",
        "--hidden-import=AttendanceScanner.settings",
        "--hidden-import=AttendanceScanner.urls",
        "--hidden-import=AttendanceScanner.wsgi",
        "--hidden-import=django.db.backends.sqlite3",
        "--hidden-import=django.template.loaders.filesystem",
        "--hidden-import=django.template.loaders.app_directories",
        "launcher.py"
    ]
    
    try:
        subprocess.check_call(cmd)
        print("Executable built successfully!")
        print("Location: dist/AttendanceScanner.exe")
    except subprocess.CalledProcessError as e:
        print(f"Error building executable: {e}")
        return False
    
    return True

def create_readme():
    """Create a README file for the executable."""
    readme_content = '''# Attendance Scanner Executable

This is a standalone executable version of the Attendance Scanner Django application.

## How to Use

1. **Run the executable**: Double-click `AttendanceScanner.exe`
2. **Access the application**: Open your web browser and go to `http://127.0.0.1:8000`
3. **Stop the application**: Press Ctrl+C in the console window or close the console

## First Time Setup

If this is the first time running the application:

1. The application will create a new database if one doesn't exist
2. You'll need to create a superuser account to access the admin panel
3. To create a superuser, run the executable and then open a new command prompt:
   ```
   AttendanceScanner.exe createsuperuser
   ```

## Features

- Complete attendance management system
- Barcode scanning functionality
- User management (Students, Professors, Administrators)
- Schedule management
- Attendance reports

## Troubleshooting

- If the application doesn't start, check that port 8000 is not in use
- Make sure you have write permissions in the directory where the executable is located
- The application requires an internet connection for some features

## System Requirements

- Windows 10 or later
- No additional software installation required
- The executable includes all necessary dependencies
'''
    
    with open('dist/README.txt', 'w') as f:
        f.write(readme_content)
    print("Created README file: dist/README.txt")

def main():
    """Main function to orchestrate the build process."""
    print("=" * 60)
    print("Attendance Scanner - Executable Builder")
    print("=" * 60)
    
    # Check if we're in the right directory
    if not os.path.exists('manage.py'):
        print("Error: manage.py not found. Please run this script from the Django project root.")
        return
    
    # Install PyInstaller
    install_pyinstaller()
    
    # Create launcher script
    create_launcher_script()
    
    # Build executable
    if build_executable():
        # Create README
        create_readme()
        
        print("=" * 60)
        print("Build completed successfully!")
        print("Executable location: dist/AttendanceScanner.exe")
        print("=" * 60)
    else:
        print("Build failed. Please check the error messages above.")

if __name__ == '__main__':
    main() 