#!/usr/bin/env python
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
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting the application: {e}")
        import traceback
        traceback.print_exc()
        input("Press Enter to exit...")

if __name__ == '__main__':
    main()
