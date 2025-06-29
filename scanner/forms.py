from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import User, Room, Subject, Schedule, Enrollment, Attendance, ProfessorSession
import uuid

class CustomUserCreationForm(UserCreationForm):
    """Custom user registration form"""
    user_type = forms.ChoiceField(choices=User.USER_TYPES, widget=forms.Select(attrs={'class': 'form-control'}))
    student_id = forms.CharField(max_length=20, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    barcode = forms.CharField(max_length=50, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    phone = forms.CharField(max_length=15, required=False, widget=forms.TextInput(attrs={'class': 'form-control'}))
    
    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'user_type', 'student_id', 'barcode', 'phone', 'password1', 'password2')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            if isinstance(field.widget, (forms.TextInput, forms.EmailInput, forms.PasswordInput)):
                field.widget.attrs.update({'class': 'form-control'})
    
    def clean(self):
        cleaned_data = super().clean()
        user_type = cleaned_data.get('user_type')
        student_id = cleaned_data.get('student_id')
        
        # Handle student_id based on user type
        if user_type == 'student':
            # For students, student_id is required
            if not student_id:
                self.add_error('student_id', 'Student ID is required for students.')
            else:
                # Check if student_id already exists
                if User.objects.filter(student_id=student_id).exists():
                    self.add_error('student_id', 'A user with this Student ID already exists.')
        else:
            # For non-students, clear student_id to avoid conflicts
            cleaned_data['student_id'] = None
        
        # Generate barcode if not provided
        if not cleaned_data.get('barcode'):
            cleaned_data['barcode'] = self.generate_unique_barcode()
        
        return cleaned_data
    
    def generate_unique_barcode(self):
        """Generate a unique barcode"""
        while True:
            # Generate a UUID-based barcode (32 characters, alphanumeric)
            barcode = str(uuid.uuid4()).replace('-', '').upper()[:12]
            
            # Check if barcode already exists
            if not User.objects.filter(barcode=barcode).exists():
                return barcode
    
    def save(self, commit=True):
        user = super().save(commit=False)
        
        # Set student_id based on user type
        user_type = self.cleaned_data.get('user_type')
        if user_type == 'student':
            user.student_id = self.cleaned_data.get('student_id')
        else:
            user.student_id = None
        
        # Ensure barcode is set
        if not user.barcode:
            user.barcode = self.generate_unique_barcode()
        
        if commit:
            user.save()
        return user

class CustomAuthenticationForm(AuthenticationForm):
    """Custom login form"""
    username = forms.CharField(widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password'}))
    
    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')
        
        if username and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError('Invalid username or password.')
            else:
                self.confirm_login_allowed(self.user_cache)
        
        return self.cleaned_data

class RoomForm(forms.ModelForm):
    """Room creation/editing form"""
    class Meta:
        model = Room
        fields = ['name', 'capacity', 'building', 'floor']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'capacity': forms.NumberInput(attrs={'class': 'form-control'}),
            'building': forms.TextInput(attrs={'class': 'form-control'}),
            'floor': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class SubjectForm(forms.ModelForm):
    """Subject creation/editing form"""
    class Meta:
        model = Subject
        fields = ['code', 'name', 'description', 'units']
        widgets = {
            'code': forms.TextInput(attrs={'class': 'form-control'}),
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'units': forms.NumberInput(attrs={'class': 'form-control'}),
        }

class ScheduleForm(forms.ModelForm):
    """Schedule creation/editing form"""
    class Meta:
        model = Schedule
        fields = ['subject', 'room', 'day_of_week', 'start_time', 'end_time', 'semester', 'academic_year']
        widgets = {
            'subject': forms.Select(attrs={'class': 'form-control'}),
            'room': forms.Select(attrs={'class': 'form-control'}),
            'day_of_week': forms.Select(attrs={'class': 'form-control'}),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'semester': forms.TextInput(attrs={'class': 'form-control'}),
            'academic_year': forms.TextInput(attrs={'class': 'form-control'}),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        start_time = cleaned_data.get('start_time')
        end_time = cleaned_data.get('end_time')
        
        if start_time and end_time and start_time >= end_time:
            raise forms.ValidationError('End time must be after start time.')
        
        return cleaned_data

class EnrollmentForm(forms.ModelForm):
    """Student enrollment form"""
    class Meta:
        model = Enrollment
        fields = ['student', 'schedule']
        widgets = {
            'student': forms.Select(attrs={'class': 'form-control'}),
            'schedule': forms.Select(attrs={'class': 'form-control'}),
        }

class AttendanceForm(forms.ModelForm):
    """Attendance editing form for professors"""
    class Meta:
        model = Attendance
        fields = ['status', 'notes']
        widgets = {
            'status': forms.Select(attrs={'class': 'form-control'}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }

class BarcodeScanForm(forms.Form):
    """Barcode scanning form"""
    barcode = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Scan barcode here...',
            'autofocus': True,
            'id': 'barcode-input'
        })
    )

class ProfessorSessionForm(forms.ModelForm):
    """Professor session form"""
    class Meta:
        model = ProfessorSession
        fields = ['schedule', 'date']
        widgets = {
            'schedule': forms.Select(attrs={'class': 'form-control'}),
            'date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
        }
