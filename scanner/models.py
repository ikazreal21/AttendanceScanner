from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import datetime, timedelta
import uuid

class User(AbstractUser):
    """Custom User model with role-based access"""
    USER_TYPES = (
        ('student', 'Student'),
        ('professor', 'Professor'),
        ('admin', 'Admin'),
    )
    
    user_type = models.CharField(max_length=10, choices=USER_TYPES, default='student')
    student_id = models.CharField(max_length=20, blank=True, null=True, unique=True)
    barcode = models.CharField(max_length=50, blank=True, null=True, unique=True)
    phone = models.CharField(max_length=15, blank=True, null=True)
    
    def __str__(self):
        return f"{self.get_full_name()} ({self.user_type})"
    
    def generate_barcode(self):
        """Generate a unique barcode for the user"""
        while True:
            # Generate a UUID-based barcode (12 characters, alphanumeric)
            barcode = str(uuid.uuid4()).replace('-', '').upper()[:12]
            
            # Check if barcode already exists
            if not User.objects.filter(barcode=barcode).exists():
                self.barcode = barcode
                self.save()
                return barcode
    
    def save(self, *args, **kwargs):
        # Auto-generate barcode if not provided
        if not self.barcode:
            self.generate_barcode()
        super().save(*args, **kwargs)

class Room(models.Model):
    """Room model for class locations"""
    name = models.CharField(max_length=50)
    capacity = models.IntegerField(default=30)
    building = models.CharField(max_length=50, blank=True, null=True)
    floor = models.IntegerField(default=1)
    
    def __str__(self):
        return f"{self.name} - {self.building}" if self.building else self.name

class Subject(models.Model):
    """Subject/Course model"""
    code = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    units = models.IntegerField(default=3)
    
    def __str__(self):
        return f"{self.code} - {self.name}"

class Schedule(models.Model):
    """Class schedule model"""
    DAYS_OF_WEEK = (
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday'),
    )
    
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    professor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'professor'})
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    day_of_week = models.CharField(max_length=10, choices=DAYS_OF_WEEK)
    start_time = models.TimeField()
    end_time = models.TimeField()
    semester = models.CharField(max_length=20, default='2024-1')
    academic_year = models.CharField(max_length=10, default='2024-2025')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['room', 'day_of_week', 'start_time', 'end_time', 'semester']
    
    def __str__(self):
        return f"{self.subject.code} - {self.professor.get_full_name()} - {self.room.name} ({self.get_day_of_week_display()})"

class Enrollment(models.Model):
    """Student enrollment in subjects"""
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    enrolled_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['student', 'schedule']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.schedule.subject.code}"

class Attendance(models.Model):
    """Attendance record model"""
    STATUS_CHOICES = (
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused'),
    )
    
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'student'})
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.DateTimeField(blank=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='absent')
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ['student', 'schedule', 'date']
    
    def __str__(self):
        return f"{self.student.get_full_name()} - {self.schedule.subject.code} - {self.date}"
    
    @property
    def duration(self):
        """Calculate duration of attendance"""
        if self.time_in and self.time_out:
            return self.time_out - self.time_in
        return None

class ProfessorSession(models.Model):
    """Professor's time-in/out session for a class"""
    professor = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'professor'})
    schedule = models.ForeignKey(Schedule, on_delete=models.CASCADE)
    date = models.DateField()
    time_in = models.DateTimeField(blank=True, null=True)
    time_out = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['professor', 'schedule', 'date']
    
    def __str__(self):
        return f"{self.professor.get_full_name()} - {self.schedule.subject.code} - {self.date}"
    
    def can_students_time_in(self):
        """Check if students can time in (professor must be present)"""
        return self.is_active and self.time_in is not None
    
    def can_professor_time_out(self):
        """Check if professor can time out (15-minute interval)"""
        if not self.time_in:
            return False
        time_since_time_in = timezone.now() - self.time_in
        return time_since_time_in >= timedelta(minutes=15)

class BarcodeLog(models.Model):
    """Log of all barcode scans"""
    barcode = models.CharField(max_length=50)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    scan_time = models.DateTimeField(auto_now_add=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    success = models.BooleanField(default=False)
    message = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return f"{self.barcode} - {self.scan_time} - {'Success' if self.success else 'Failed'}"
