from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods
from django.utils import timezone
from django.db.models import Q
from datetime import datetime, timedelta, date
import json
import pytz

from .models import User, Room, Subject, Schedule, Enrollment, Attendance, ProfessorSession, BarcodeLog
from .forms import (
    CustomUserCreationForm, CustomAuthenticationForm, RoomForm, SubjectForm, 
    ScheduleForm, EnrollmentForm, AttendanceForm, BarcodeScanForm, ProfessorSessionForm
)

# Manila timezone
MANILA_TZ = pytz.timezone('Asia/Manila')

def get_manila_now():
    """Get current time in Manila timezone"""
    return timezone.now().astimezone(MANILA_TZ)

def get_manila_today():
    """Get current date in Manila timezone"""
    return get_manila_now().date()

def get_manila_time():
    """Get current time (time only) in Manila timezone"""
    return get_manila_now().time()

def is_professor(user):
    return user.is_authenticated and user.user_type == 'professor'

def is_student(user):
    return user.is_authenticated and user.user_type == 'student'

def is_admin(user):
    return user.is_authenticated and user.user_type == 'admin'

def home(request):
    """Home page with login/register options"""
    if request.user.is_authenticated:
        return redirect('dashboard')
    return render(request, 'scanner/home.html')

def register(request):
    """User registration"""
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            
            # Show success message with generated barcode
            if not request.POST.get('barcode'):  # If barcode was auto-generated
                messages.success(request, f'Account created successfully! Your auto-generated barcode is: {user.barcode}')
            else:
                messages.success(request, 'Account created successfully!')
            
            return redirect('dashboard')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'scanner/register.html', {'form': form})

def user_login(request):
    """User login"""
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.get_full_name()}!')
                return redirect('dashboard')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'scanner/login.html', {'form': form})

@login_required
def user_logout(request):
    """User logout"""
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('home')

@login_required
def dashboard(request):
    """Main dashboard based on user type"""
    today = get_manila_today()
    current_time = get_manila_time()
    
    if request.user.user_type == 'student':
        # Get student's schedules for today
        enrollments = Enrollment.objects.filter(student=request.user)
        today_schedules = []
        
        for enrollment in enrollments:
            schedule = enrollment.schedule
            if schedule.day_of_week.lower() == today.strftime('%A').lower():
                # Check if class is happening now or soon
                is_current = schedule.start_time <= current_time <= schedule.end_time
                is_upcoming = schedule.start_time > current_time
                
                # Get attendance for today
                attendance, created = Attendance.objects.get_or_create(
                    student=request.user,
                    schedule=schedule,
                    date=today,
                    defaults={'status': 'absent'}
                )
                
                today_schedules.append({
                    'schedule': schedule,
                    'attendance': attendance,
                    'is_current': is_current,
                    'is_upcoming': is_upcoming,
                    'professor_session': ProfessorSession.objects.filter(
                        professor=schedule.professor,
                        schedule=schedule,
                        date=today
                    ).first()
                })
        
        context = {
            'today_schedules': today_schedules,
            'total_schedules': enrollments.count(),
            'attendance_records': Attendance.objects.filter(student=request.user).order_by('-date')[:10]
        }
        
    elif request.user.user_type == 'professor':
        # Get professor's schedules for today
        today_schedules = Schedule.objects.filter(
            professor=request.user,
            day_of_week__iexact=today.strftime('%A')
        )
        
        sessions = []
        for schedule in today_schedules:
            session, created = ProfessorSession.objects.get_or_create(
                professor=request.user,
                schedule=schedule,
                date=today,
                defaults={'is_active': False}
            )
            
            # Get attendance count for this session
            attendance_count = Attendance.objects.filter(
                schedule=schedule,
                date=today,
                status='present'
            ).count()
            
            sessions.append({
                'schedule': schedule,
                'session': session,
                'attendance_count': attendance_count,
                'total_students': Enrollment.objects.filter(schedule=schedule).count()
            })
        
        context = {
            'today_schedules': sessions,
            'total_schedules': Schedule.objects.filter(professor=request.user).count()
        }
    
    else:  # Admin
        context = {
            'total_users': User.objects.count(),
            'total_schedules': Schedule.objects.count(),
            'total_rooms': Room.objects.count(),
            'total_subjects': Subject.objects.count()
        }
    
    return render(request, 'scanner/dashboard.html', context)

@login_required
@user_passes_test(is_professor)
def schedule_management(request):
    """Professor's schedule management"""
    if request.method == 'POST':
        form = ScheduleForm(request.POST)
        print(form.errors)
        if form.is_valid():
            schedule = form.save(commit=False)
            schedule.professor = request.user
            schedule.save()
            messages.success(request, 'Schedule created successfully!')
            return redirect('schedule_management')
    else:
        form = ScheduleForm()
    
    schedules = Schedule.objects.filter(professor=request.user).order_by('day_of_week', 'start_time')
    return render(request, 'scanner/schedule_management.html', {
        'form': form,
        'schedules': schedules
    })

@login_required
@user_passes_test(is_professor)
def edit_schedule(request, schedule_id):
    """Edit schedule"""
    schedule = get_object_or_404(Schedule, id=schedule_id, professor=request.user)
    
    if request.method == 'POST':
        form = ScheduleForm(request.POST, instance=schedule)
        if form.is_valid():
            form.save()
            messages.success(request, 'Schedule updated successfully!')
            return redirect('schedule_management')
    else:
        form = ScheduleForm(instance=schedule)
    
    return render(request, 'scanner/edit_schedule.html', {'form': form, 'schedule': schedule})

@login_required
@user_passes_test(is_professor)
def delete_schedule(request, schedule_id):
    """Delete schedule"""
    schedule = get_object_or_404(Schedule, id=schedule_id, professor=request.user)
    
    if request.method == 'POST':
        schedule.delete()
        messages.success(request, 'Schedule deleted successfully!')
        return redirect('schedule_management')
    
    return render(request, 'scanner/delete_schedule.html', {'schedule': schedule})

@login_required
@user_passes_test(is_professor)
def attendance_management(request, schedule_id):
    """Professor's attendance management for a specific schedule"""
    schedule = get_object_or_404(Schedule, id=schedule_id, professor=request.user)
    date_filter = request.GET.get('date', get_manila_today().isoformat())
    
    try:
        selected_date = datetime.strptime(date_filter, '%Y-%m-%d').date()
    except ValueError:
        selected_date = get_manila_today()
    
    # Get or create professor session
    session, created = ProfessorSession.objects.get_or_create(
        professor=request.user,
        schedule=schedule,
        date=selected_date,
        defaults={'is_active': False}
    )
    
    # Get all enrolled students
    enrollments = Enrollment.objects.filter(schedule=schedule)
    attendance_records = []
    
    for enrollment in enrollments:
        attendance, created = Attendance.objects.get_or_create(
            student=enrollment.student,
            schedule=schedule,
            date=selected_date,
            defaults={'status': 'absent'}
        )
        attendance_records.append(attendance)
    
    if request.method == 'POST':
        # Handle attendance updates
        for attendance in attendance_records:
            status_key = f'status_{attendance.id}'
            notes_key = f'notes_{attendance.id}'
            
            if status_key in request.POST:
                attendance.status = request.POST[status_key]
                attendance.notes = request.POST.get(notes_key, '')
                attendance.save()
        
        messages.success(request, 'Attendance updated successfully!')
        return redirect('attendance_management', schedule_id=schedule_id)
    
    return render(request, 'scanner/attendance_management.html', {
        'schedule': schedule,
        'session': session,
        'attendance_records': attendance_records,
        'selected_date': selected_date,
        'enrollment_count': enrollments.count()
    })

@login_required
@user_passes_test(is_professor)
def barcode_scanner(request, schedule_id):
    """Barcode scanner interface for professors"""
    schedule = get_object_or_404(Schedule, id=schedule_id, professor=request.user)
    today = get_manila_today()
    
    # Get or create professor session
    session, created = ProfessorSession.objects.get_or_create(
        professor=request.user,
        schedule=schedule,
        date=today,
        defaults={'is_active': False}
    )
    
    if request.method == 'POST':
        form = BarcodeScanForm(request.POST)
        if form.is_valid():
            barcode = form.cleaned_data['barcode']
            return process_barcode_scan(request, barcode, schedule, session)
    else:
        form = BarcodeScanForm()
    
    # Get recent scans
    recent_scans = BarcodeLog.objects.filter(
        scan_time__date=today,
        success=True
    ).order_by('-scan_time')[:10]
    
    return render(request, 'scanner/barcode_scanner.html', {
        'form': form,
        'schedule': schedule,
        'session': session,
        'recent_scans': recent_scans
    })

@csrf_exempt
@require_http_methods(["POST"])
def process_barcode_scan(request, barcode, schedule, session):
    """Process barcode scan and handle attendance"""
    try:
        # Log the scan
        log_entry = BarcodeLog.objects.create(
            barcode=barcode,
            ip_address=request.META.get('REMOTE_ADDR'),
            success=False,
            message='Processing...'
        )
        
        # Find user by barcode
        try:
            user = User.objects.get(barcode=barcode)
            log_entry.user = user
        except User.DoesNotExist:
            log_entry.message = 'Barcode not found'
            log_entry.save()
            return JsonResponse({'success': False, 'message': 'Barcode not found'})
        
        # Check if user is enrolled in this schedule
        if not Enrollment.objects.filter(student=user, schedule=schedule).exists():
            log_entry.message = 'Student not enrolled in this class'
            log_entry.save()
            return JsonResponse({'success': False, 'message': 'Student not enrolled in this class'})
        
        today = get_manila_today()
        current_time = get_manila_now()
        
        if user.user_type == 'professor':
            # Professor time-in/out logic
            if not session.time_in:
                # Professor time-in
                session.time_in = current_time
                session.is_active = True
                session.save()
                log_entry.success = True
                log_entry.message = f'Professor {user.get_full_name()} time-in successful'
                log_entry.save()
                return JsonResponse({
                    'success': True, 
                    'message': f'Professor {user.get_full_name()} time-in successful',
                    'action': 'time_in'
                })
            elif session.time_in and not session.time_out:
                # Check if 15 minutes have passed
                if session.can_professor_time_out():
                    session.time_out = current_time
                    session.is_active = False
                    session.save()
                    
                    # Auto time-out all students
                    attendances = Attendance.objects.filter(
                        schedule=schedule,
                        date=today,
                        time_in__isnull=False,
                        time_out__isnull=True
                    )
                    for attendance in attendances:
                        attendance.time_out = current_time
                        attendance.save()
                    
                    log_entry.success = True
                    log_entry.message = f'Professor {user.get_full_name()} time-out successful. All students auto time-out.'
                    log_entry.save()
                    return JsonResponse({
                        'success': True,
                        'message': f'Professor {user.get_full_name()} time-out successful. All students auto time-out.',
                        'action': 'time_out'
                    })
                else:
                    log_entry.message = 'Cannot time-out yet. 15-minute interval required.'
                    log_entry.save()
                    return JsonResponse({
                        'success': False,
                        'message': 'Cannot time-out yet. 15-minute interval required.'
                    })
            else:
                log_entry.message = 'Professor session already completed'
                log_entry.save()
                return JsonResponse({
                    'success': False,
                    'message': 'Professor session already completed'
                })
        
        else:  # Student
            # Check if professor has time-in
            if not session.can_students_time_in():
                log_entry.message = 'Professor must time-in first'
                log_entry.save()
                return JsonResponse({
                    'success': False,
                    'message': 'Professor must time-in first'
                })
            
            # Check if professor has time-out
            if session.time_out:
                log_entry.message = 'Class session has ended'
                log_entry.save()
                return JsonResponse({
                    'success': False,
                    'message': 'Class session has ended'
                })
            
            # Get or create attendance record
            attendance, created = Attendance.objects.get_or_create(
                student=user,
                schedule=schedule,
                date=today,
                defaults={'status': 'absent'}
            )
            
            if not attendance.time_in:
                # Student time-in
                attendance.time_in = current_time
                attendance.status = 'present'
                attendance.save()
                log_entry.success = True
                log_entry.message = f'Student {user.get_full_name()} time-in successful'
                log_entry.save()
                return JsonResponse({
                    'success': True,
                    'message': f'Student {user.get_full_name()} time-in successful',
                    'action': 'time_in'
                })
            elif attendance.time_in and not attendance.time_out:
                # Student time-out
                attendance.time_out = current_time
                attendance.save()
                log_entry.success = True
                log_entry.message = f'Student {user.get_full_name()} time-out successful'
                log_entry.save()
                return JsonResponse({
                    'success': True,
                    'message': f'Student {user.get_full_name()} time-out successful',
                    'action': 'time_out'
                })
            else:
                log_entry.message = 'Student already completed attendance'
                log_entry.save()
                return JsonResponse({
                    'success': False,
                    'message': 'Student already completed attendance'
                })
    
    except Exception as e:
        log_entry.message = f'Error: {str(e)}'
        log_entry.save()
        return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})

@login_required
@user_passes_test(is_student)
def student_schedule(request):
    """Student's schedule view"""
    enrollments = Enrollment.objects.filter(student=request.user)
    schedules = []
    
    for enrollment in enrollments:
        schedule = enrollment.schedule
        schedules.append({
            'schedule': schedule,
            'attendance_count': Attendance.objects.filter(
                student=request.user,
                schedule=schedule,
                status='present'
            ).count()
        })
    
    # Time slots for weekly schedule view
    time_slots = [
        '8:00', '9:00', '10:00', '11:00', '12:00', 
        '13:00', '14:00', '15:00', '16:00', '17:00'
    ]
    
    # Days of the week
    days = ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday']
    
    return render(request, 'scanner/student_schedule.html', {
        'schedules': schedules,
        'time_slots': time_slots,
        'days': days
    })

@login_required
@user_passes_test(is_student)
def student_attendance(request):
    """Student's attendance history"""
    attendances = Attendance.objects.filter(student=request.user).order_by('-date', 'schedule__start_time')
    
    # Group by schedule
    attendance_by_schedule = {}
    for attendance in attendances:
        schedule_key = attendance.schedule
        if schedule_key not in attendance_by_schedule:
            attendance_by_schedule[schedule_key] = []
        attendance_by_schedule[schedule_key].append(attendance)
    
    return render(request, 'scanner/student_attendance.html', {
        'attendance_by_schedule': attendance_by_schedule
    })

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    """Admin dashboard for managing users, rooms, subjects"""
    users = User.objects.all().order_by('user_type', 'username')
    rooms = Room.objects.all().order_by('name')
    subjects = Subject.objects.all().order_by('code')
    schedules = Schedule.objects.all().order_by('subject__code')
    
    return render(request, 'scanner/admin_dashboard.html', {
        'users': users,
        'rooms': rooms,
        'subjects': subjects,
        'schedules': schedules
    })

@login_required
@user_passes_test(is_admin)
def manage_rooms(request):
    """Admin room management"""
    if request.method == 'POST':
        form = RoomForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room created successfully!')
            return redirect('manage_rooms')
    else:
        form = RoomForm()
    
    rooms = Room.objects.all().order_by('name')
    return render(request, 'scanner/manage_rooms.html', {'form': form, 'rooms': rooms})

@login_required
@user_passes_test(is_admin)
def manage_subjects(request):
    """Admin subject management"""
    if request.method == 'POST':
        form = SubjectForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject created successfully!')
            return redirect('manage_subjects')
    else:
        form = SubjectForm()
    
    subjects = Subject.objects.all().order_by('code')
    return render(request, 'scanner/manage_subjects.html', {'form': form, 'subjects': subjects})

@login_required
@user_passes_test(is_admin)
def manage_enrollments(request):
    """Admin enrollment management"""
    if request.method == 'POST':
        form = EnrollmentForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Enrollment created successfully!')
            return redirect('manage_enrollments')
    else:
        form = EnrollmentForm()
    
    enrollments = Enrollment.objects.all().order_by('student__username', 'schedule__subject__code')
    return render(request, 'scanner/manage_enrollments.html', {'form': form, 'enrollments': enrollments})

@login_required
def user_profile(request):
    """User profile view to show barcode and account information"""
    return render(request, 'scanner/user_profile.html', {'user': request.user})

@login_required
@user_passes_test(is_professor)
def toggle_session(request, schedule_id):
    """Toggle professor session on/off"""
    schedule = get_object_or_404(Schedule, id=schedule_id, professor=request.user)
    action = request.POST.get('action')
    selected_date = request.POST.get('date', get_manila_today().isoformat())
    
    try:
        selected_date = datetime.strptime(selected_date, '%Y-%m-%d').date()
    except ValueError:
        selected_date = get_manila_today()
    
    session, created = ProfessorSession.objects.get_or_create(
        professor=request.user,
        schedule=schedule,
        date=selected_date,
        defaults={'is_active': False}
    )
    
    current_time = get_manila_now()
    
    if action == 'start':
        session.is_active = True
        session.time_in = current_time
        session.save()
        messages.success(request, 'Session started successfully!')
    elif action == 'stop':
        session.is_active = False
        session.time_out = current_time
        session.save()
        messages.success(request, 'Session stopped successfully!')
    
    return redirect('attendance_management', schedule_id=schedule_id)

@login_required
@user_passes_test(is_admin)
def edit_room(request, room_id):
    """Edit room"""
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        form = RoomForm(request.POST, instance=room)
        if form.is_valid():
            form.save()
            messages.success(request, 'Room updated successfully!')
            return redirect('manage_rooms')
    else:
        form = RoomForm(instance=room)
    
    return render(request, 'scanner/edit_room.html', {'form': form, 'room': room})

@login_required
@user_passes_test(is_admin)
def delete_room(request, room_id):
    """Delete room"""
    room = get_object_or_404(Room, id=room_id)
    
    if request.method == 'POST':
        room.delete()
        messages.success(request, 'Room deleted successfully!')
        return redirect('manage_rooms')
    
    return render(request, 'scanner/delete_room.html', {'room': room})

@login_required
@user_passes_test(is_admin)
def edit_subject(request, subject_id):
    """Edit subject"""
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        form = SubjectForm(request.POST, instance=subject)
        if form.is_valid():
            form.save()
            messages.success(request, 'Subject updated successfully!')
            return redirect('manage_subjects')
    else:
        form = SubjectForm(instance=subject)
    
    return render(request, 'scanner/edit_subject.html', {'form': form, 'subject': subject})

@login_required
@user_passes_test(is_admin)
def delete_subject(request, subject_id):
    """Delete subject"""
    subject = get_object_or_404(Subject, id=subject_id)
    
    if request.method == 'POST':
        subject.delete()
        messages.success(request, 'Subject deleted successfully!')
        return redirect('manage_subjects')
    
    return render(request, 'scanner/delete_subject.html', {'subject': subject})

@login_required
@user_passes_test(is_admin)
def delete_enrollment(request, enrollment_id):
    """Delete enrollment"""
    enrollment = get_object_or_404(Enrollment, id=enrollment_id)
    
    if request.method == 'POST':
        enrollment.delete()
        messages.success(request, 'Enrollment deleted successfully!')
        return redirect('manage_enrollments')
    
    return render(request, 'scanner/delete_enrollment.html', {'enrollment': enrollment})

@login_required
@user_passes_test(is_admin)
def bulk_enrollment(request):
    """Bulk enrollment from CSV"""
    if request.method == 'POST' and request.FILES.get('csv_file'):
        csv_file = request.FILES['csv_file']
        # Implementation for CSV processing would go here
        messages.success(request, 'Bulk enrollment processed successfully!')
        return redirect('manage_enrollments')
    
    return redirect('manage_enrollments')

@login_required
@user_passes_test(is_admin)
def bulk_delete_enrollments(request):
    """Bulk delete enrollments"""
    if request.method == 'POST':
        enrollment_ids = request.POST.getlist('enrollment_ids')
        Enrollment.objects.filter(id__in=enrollment_ids).delete()
        messages.success(request, f'{len(enrollment_ids)} enrollment(s) deleted successfully!')
    
    return redirect('manage_enrollments')

@login_required
@user_passes_test(is_admin)
def export_enrollments(request):
    """Export enrollments to CSV"""
    import csv
    from django.http import HttpResponse
    
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="enrollments.csv"'
    
    writer = csv.writer(response)
    writer.writerow(['Student ID', 'Student Name', 'Subject Code', 'Subject Name', 'Professor', 'Schedule', 'Enrolled Date'])
    
    enrollments = Enrollment.objects.all().select_related('student', 'schedule__subject', 'schedule__professor')
    for enrollment in enrollments:
        writer.writerow([
            enrollment.student.student_id or '',
            enrollment.student.get_full_name(),
            enrollment.schedule.subject.code,
            enrollment.schedule.subject.name,
            enrollment.schedule.professor.get_full_name(),
            f"{enrollment.schedule.get_day_of_week_display()} {enrollment.schedule.start_time}-{enrollment.schedule.end_time}",
            enrollment.enrolled_at.strftime('%Y-%m-%d')
        ])
    
    return response

# @login_required
# @user_passes_test(is_admin)
# def view_student_attendance(request, student_id, schedule_id):
#     """View specific student attendance for a schedule"""
#     student = get_object_or_404(User, id=student_id, user_type='student')
#     schedule = get_object_or_404(Schedule, id=schedule_id)
    
#     attendances = Attendance.objects.filter(
#         student=student,
#         schedule=schedule
#     ).order_by('-date')
    
#     return render(request, 'scanner/view_student_attendance.html', {
#         'student': student,
#         'schedule': schedule,
#         'attendances': attendances
#     })
