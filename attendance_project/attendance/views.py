from django.shortcuts import render, redirect
from django.utils import timezone
from .models import Attendance, UserProfile
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils import timezone
from datetime import timedelta, datetime
from django.http import JsonResponse


# Login Module
def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            user_profile = user.userprofile
            if user_profile.role == 'employee':
                messages.success(request, 'Logged in Successfully.')
                return redirect('employee_dashboard')
            elif user_profile.role == 'manager':
                messages.success(request, 'Logged in Successfully.')
                return redirect('manager_dashboard')
            else:
                # Handle admin or other roles
                return redirect('admin_dashboard')
        else:
            messages.error(request, 'Invalid username or password.')
    
    return render(request, 'login.html') 

# Logout Module
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
@user_passes_test(lambda u: u.userprofile.role == 'manager')
def manager_dashboard(request):
    # Implement manager dashboard logic here
    return render(request, 'manager_dashboard.html')

@login_required
@user_passes_test(lambda u: u.userprofile.role == 'employee')
def employee_dashboard(request):
    if request.method == 'POST' and request.headers.get('x-requested-with') == 'XMLHttpRequest':
        user_profile = UserProfile.objects.get(user=request.user)
        # response_data = {}

        if 'clock_in' in request.POST:
            clock_in_time = timezone.now().time()
            date = timezone.now().date()
            Attendance.objects.create(user_profile=user_profile, clock_in_time=clock_in_time, date=date)
            # response_data['message'] = 'Clocked in successfully!'
        elif 'clock_out' in request.POST:
            clock_out_time = timezone.now().time()
            attendance_record = Attendance.objects.filter(user_profile=user_profile, date=timezone.now().date()).latest('clock_in_time')
            attendance_record.clock_out_time = clock_out_time
            attendance_record.save()
            # response_data['message'] = 'Clocked out successfully!'
        elif 'break_in' in request.POST:
            break_in_time = timezone.now()
            attendance_record = Attendance.objects.filter(user_profile=user_profile, date=timezone.now().date()).latest('clock_in_time')
            attendance_record.break_in_time = break_in_time
            attendance_record.save()
            # response_data['message'] = 'Break started successfully!'
        elif 'break_out' in request.POST:
            break_out_time = timezone.now()
            attendance_record = Attendance.objects.filter(user_profile=user_profile, date=timezone.now().date()).latest('clock_in_time')
            attendance_record.break_out_time = break_out_time
            attendance_record.save()
            # response_data['message'] = 'Break ended successfully!'

        return JsonResponse(response_data)
    
    return render(request, 'employee_dashboard.html', {
        'current_time': timezone.now(),
    })

@login_required
def clock_in(request):
    if request.method == 'POST':
        attendance, created = Attendance.objects.get_or_create(user_profile=request.user.userprofile, clock_in_time__date=timezone.now().date())
        attendance.clock_in_time = timezone.now()
        attendance.save()
    return redirect('attendance_page')

@login_required
def clock_out(request):
    if request.method == 'POST':
        attendance = Attendance.objects.get(user_profile=request.user.userprofile, clock_in_time__date=timezone.now().date())
        attendance.clock_out_time = timezone.now()
        attendance.save()
    return redirect('attendance_page')

@login_required
def break_in(request):
    if request.method == 'POST':
        attendance = Attendance.objects.get(user_profile=request.user.userprofile, clock_in_time__date=timezone.now().date())
        attendance.break_in_time = timezone.now()
        attendance.save()
    return redirect('attendance_page')

@login_required
def break_out(request):
    if request.method == 'POST':
        attendance = Attendance.objects.get(user_profile=request.user.userprofile, clock_in_time__date=timezone.now().date())
        attendance.break_out_time = timezone.now()
        attendance.save()
    return redirect('attendance_page')

@login_required
@user_passes_test(lambda u: u.userprofile.role == 'employee')
def attendance_page(request):
    user_profile = UserProfile.objects.get(user=request.user)
    # user_profile = request.user.userprofile
    attendances = Attendance.objects.filter(user_profile=user_profile).order_by('-clock_in_time')
    # attendances = Attendance.objects.filter(user_profile=user_profile)
    print(f"Number of attendances: {attendances.count()}") 
    
    for attendance in attendances:
        if attendance.clock_in_time and attendance.clock_out_time:
            # Duration calculations are already handled in the model's save method
            pass

    return render(request, 'attendance_page.html', {'attendances': attendances})

@login_required
@user_passes_test(lambda u: u.userprofile.role == 'manager')
def manager_attendance_page(request):
    attendances = Attendance.objects.all().order_by('-date')
    
    for attendance in attendances:
        if attendance.clock_in_time and attendance.clock_out_time:
            # Duration calculations are already handled in the model's save method
            pass

    return render(request, 'attendance_record.html', {'attendances': attendances})
