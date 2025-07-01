import os
import sys
import django
from django.core.wsgi import get_wsgi_application
from wsgiref.simple_server import make_server
import webbrowser

if __name__ == "__main__":
    # Set the Django settings module
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "AttendanceScanner.settings")
    
    # Disable autoreload to avoid PyInstaller issues
    os.environ['DJANGO_AUTORELOAD_ENV'] = 'false'
    
    # Initialize Django
    django.setup()
    
    # Get the WSGI application
    application = get_wsgi_application()
    
    # Create and run the server
    print("Starting Attendance Scanner Server...")
    print("Access the application at: http://localhost:8000")
    print("Press Ctrl+C to stop the server")
    
    try:
        with make_server('0.0.0.0', 8000, application) as httpd:
            print("Server running on http://0.0.0.0:8000")
            webbrowser.open('http://localhost:8000')
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nServer stopped.")
    except Exception as e:
        print(f"Error starting server: {e}")
        input("Press Enter to exit...")
