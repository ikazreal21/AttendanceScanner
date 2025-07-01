# Attendance Scanner Executable

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
