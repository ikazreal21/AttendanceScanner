from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Room, Subject, Schedule, Enrollment, Attendance, ProfessorSession, BarcodeLog

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'first_name', 'last_name', 'email', 'user_type', 'student_id', 'barcode')
    list_filter = ('user_type', 'is_active', 'is_staff')
    search_fields = ('username', 'first_name', 'last_name', 'email', 'student_id', 'barcode')
    ordering = ('username',)
    
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'student_id', 'barcode', 'phone')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'student_id', 'barcode', 'phone')}),
    )

@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ('name', 'building', 'floor', 'capacity')
    list_filter = ('building', 'floor')
    search_fields = ('name', 'building')
    ordering = ('building', 'floor', 'name')

@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'units', 'description')
    search_fields = ('code', 'name')
    ordering = ('code',)

@admin.register(Schedule)
class ScheduleAdmin(admin.ModelAdmin):
    list_display = ('subject', 'professor', 'room', 'day_of_week', 'start_time', 'end_time', 'semester', 'is_active')
    list_filter = ('day_of_week', 'semester', 'academic_year', 'is_active', 'professor')
    search_fields = ('subject__code', 'subject__name', 'professor__username', 'room__name')
    ordering = ('day_of_week', 'start_time')
    date_hierarchy = 'created_at'

@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'schedule', 'enrolled_at')
    list_filter = ('schedule__semester', 'schedule__subject')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'schedule__subject__code')
    ordering = ('student__username', 'schedule__subject__code')
    date_hierarchy = 'enrolled_at'

@admin.register(Attendance)
class AttendanceAdmin(admin.ModelAdmin):
    list_display = ('student', 'schedule', 'date', 'status', 'time_in', 'time_out')
    list_filter = ('status', 'date', 'schedule__subject', 'schedule__professor')
    search_fields = ('student__username', 'student__first_name', 'student__last_name', 'schedule__subject__code')
    ordering = ('-date', 'schedule__start_time', 'student__username')
    date_hierarchy = 'date'
    readonly_fields = ('created_at', 'updated_at')

@admin.register(ProfessorSession)
class ProfessorSessionAdmin(admin.ModelAdmin):
    list_display = ('professor', 'schedule', 'date', 'time_in', 'time_out', 'is_active')
    list_filter = ('is_active', 'date', 'schedule__subject', 'professor')
    search_fields = ('professor__username', 'professor__first_name', 'professor__last_name', 'schedule__subject__code')
    ordering = ('-date', 'schedule__start_time')
    date_hierarchy = 'date'
    readonly_fields = ('created_at',)

@admin.register(BarcodeLog)
class BarcodeLogAdmin(admin.ModelAdmin):
    list_display = ('barcode', 'user', 'scan_time', 'success', 'ip_address')
    list_filter = ('success', 'scan_time')
    search_fields = ('barcode', 'user__username', 'message')
    ordering = ('-scan_time',)
    date_hierarchy = 'scan_time'
    readonly_fields = ('scan_time',)
