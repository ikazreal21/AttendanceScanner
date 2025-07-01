from django.contrib.auth import views as auth_views

from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path('', views.home, name='home'),
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    
    # Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),
    path('profile/', views.user_profile, name='user_profile'),
    
    # Professor views
    path('schedule/', views.schedule_management, name='schedule_management'),
    path('schedule/<int:schedule_id>/edit/', views.edit_schedule, name='edit_schedule'),
    path('schedule/<int:schedule_id>/delete/', views.delete_schedule, name='delete_schedule'),
    path('schedule/<int:schedule_id>/attendance/', views.attendance_management, name='attendance_management'),
    path('schedule/<int:schedule_id>/scanner/', views.barcode_scanner, name='barcode_scanner'),
    path('schedule/<int:schedule_id>/toggle-session/', views.toggle_session, name='toggle_session'),
    
    # Student views
    path('my-schedule/', views.student_schedule, name='student_schedule'),
    path('my-attendance/', views.student_attendance, name='student_attendance'),
    
    # Admin views
    path('admin-dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('manage-rooms/', views.manage_rooms, name='manage_rooms'),
    path('manage-rooms/<int:room_id>/edit/', views.edit_room, name='edit_room'),
    path('manage-rooms/<int:room_id>/delete/', views.delete_room, name='delete_room'),
    path('manage-subjects/', views.manage_subjects, name='manage_subjects'),
    path('manage-subjects/<int:subject_id>/edit/', views.edit_subject, name='edit_subject'),
    path('manage-subjects/<int:subject_id>/delete/', views.delete_subject, name='delete_subject'),
    path('manage-enrollments/', views.manage_enrollments, name='manage_enrollments'),
    path('manage-enrollments/<int:enrollment_id>/delete/', views.delete_enrollment, name='delete_enrollment'),
    path('manage-enrollments/bulk/', views.bulk_enrollment, name='bulk_enrollment'),
    path('manage-enrollments/bulk-delete/', views.bulk_delete_enrollments, name='bulk_delete_enrollments'),
    path('manage-enrollments/export/', views.export_enrollments, name='export_enrollments'),
    path('barcode_image/', views.barcode_image, name='barcode_image'),
    # path('student/<int:student_id>/schedule/<int:schedule_id>/attendance/', views.view_student_attendance, name='view_student_attendance'),
]