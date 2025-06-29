# Attendance Scanner System

A comprehensive Django-based attendance management system that uses barcode scanning for efficient student attendance tracking in educational institutions.

## Features

### 🔐 Authentication & User Management

- **Multi-user System**: Support for Students, Professors, and Administrators
- **Secure Login**: Custom authentication with user type validation
- **Profile Management**: User profiles with barcode generation and management

### 📊 Dashboard

- **Role-based Dashboards**: Different views for students, professors, and admins
- **Real-time Statistics**: Attendance counts, class schedules, and system overview
- **Quick Actions**: Easy access to frequently used features

### 👨‍🏫 Professor Features

- **Schedule Management**: Create and manage class schedules
- **Barcode Scanner**: Real-time attendance scanning interface
- **Session Control**: Start/stop attendance sessions
- **Attendance Management**: Manual attendance editing and review
- **Attendance Reports**: View and export attendance data

### 👨‍🎓 Student Features

- **Schedule View**: View enrolled classes and schedules
- **Attendance History**: Track personal attendance records
- **Barcode Display**: Show personal barcode for scanning
- **Weekly Schedule**: Visual weekly class schedule

### 👨‍💼 Admin Features

- **Room Management**: Add, edit, and manage classrooms
- **Subject Management**: Create and manage academic subjects
- **Enrollment Management**: Manage student enrollments
- **Bulk Operations**: Import/export enrollments via CSV
- **System Overview**: Monitor system statistics

### 📱 Barcode System

- **Automatic Generation**: Unique barcodes for each user
- **Real-time Scanning**: Instant attendance recording
- **Validation**: Ensures only enrolled students can be marked present
- **Session Control**: Professors control when scanning is active

## Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (can be configured for PostgreSQL/MySQL)
- **Frontend**: Bootstrap 5, Font Awesome, Chart.js
- **Authentication**: Django's built-in authentication system
- **Barcode**: Text-based barcode system (easily extensible to QR codes)

## Installation

### Prerequisites

- Python 3.8+
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**

   ```bash
   git clone <repository-url>
   cd AttendanceScanner
   ```

2. **Create virtual environment**

   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**

   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**

   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**

   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Open your browser and go to `http://127.0.0.1:8000/`
   - Login with your superuser credentials

## Usage Guide

### For Administrators

1. **Initial Setup**

   - Create rooms using the "Manage Rooms" section
   - Add subjects using the "Manage Subjects" section
   - Create user accounts for professors and students

2. **Enrollment Management**
   - Enroll students in subjects using "Manage Enrollments"
   - Use bulk import for large numbers of enrollments
   - Export enrollment data for reporting

### For Professors

1. **Schedule Management**

   - Create class schedules with subjects, rooms, and time slots
   - Edit or delete schedules as needed

2. **Attendance Taking**
   - Start a session when class begins
   - Use the barcode scanner to scan student barcodes
   - Manually edit attendance if needed
   - Stop the session when class ends

### For Students

1. **Accessing the System**

   - Login with your credentials
   - View your schedule and attendance history
   - Display your barcode for scanning

2. **Barcode Usage**
   - Your barcode is automatically generated
   - Present it to your professor for scanning
   - Check your attendance status after class

## Database Models

### Core Models

- **User**: Extended user model with user types and barcodes
- **Room**: Classroom information and capacity
- **Subject**: Academic subjects and course information
- **Schedule**: Class schedules with time slots
- **Enrollment**: Student enrollment in subjects
- **Attendance**: Attendance records with timestamps
- **ProfessorSession**: Professor's class sessions
- **BarcodeLog**: Log of all barcode scans

## API Endpoints

### Authentication

- `POST /login/` - User login
- `POST /logout/` - User logout
- `POST /register/` - User registration

### Professor Endpoints

- `GET /schedule/` - Schedule management
- `POST /schedule/<id>/attendance/` - Attendance management
- `POST /schedule/<id>/scanner/` - Barcode scanner
- `POST /schedule/<id>/toggle-session/` - Session control

### Student Endpoints

- `GET /my-schedule/` - View personal schedule
- `GET /my-attendance/` - View attendance history

### Admin Endpoints

- `GET /manage-rooms/` - Room management
- `GET /manage-subjects/` - Subject management
- `GET /manage-enrollments/` - Enrollment management

## Configuration

### Settings

Key settings in `settings.py`:

- `DEBUG`: Set to `False` in production
- `SECRET_KEY`: Change in production
- `DATABASES`: Configure your database
- `STATIC_URL` and `STATIC_ROOT`: Static file configuration

### Environment Variables

Create a `.env` file for sensitive settings:

```
SECRET_KEY=your-secret-key
DEBUG=False
DATABASE_URL=your-database-url
```

## Deployment

### Production Setup

1. Set `DEBUG = False` in settings
2. Configure a production database (PostgreSQL recommended)
3. Set up static file serving
4. Configure your web server (nginx + gunicorn recommended)
5. Set up SSL certificates

### Docker Deployment

```bash
# Build the image
docker build -t attendance-scanner .

# Run the container
docker run -p 8000:8000 attendance-scanner
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new features
5. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Support

For support and questions:

- Create an issue in the repository
- Contact the development team
- Check the documentation

## Roadmap

### Future Features

- [ ] QR Code support
- [ ] Mobile app integration
- [ ] Advanced reporting and analytics
- [ ] Email notifications
- [ ] Integration with LMS systems
- [ ] API for third-party integrations
- [ ] Multi-language support
- [ ] Advanced user permissions

### Performance Improvements

- [ ] Database optimization
- [ ] Caching implementation
- [ ] Background task processing
- [ ] API rate limiting

## Changelog

### Version 1.0.0

- Initial release
- Basic attendance tracking
- Barcode scanning system
- User management
- Role-based access control
