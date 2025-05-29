from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from django.db.models import Q
from .models import User, LeaveRequest, SecurityLog
from .forms import CustomAuthenticationForm, UserRegistrationForm, UserProfileForm, LeaveRequestForm, LeaveReviewForm, SecurityLogForm
from functools import wraps

# Custom decorators for user types
def user_type_required(user_type):
    def decorator(view_func):
        @wraps(view_func)
        def _wrapped_view(request, *args, **kwargs):
            if request.user.is_authenticated and request.user.user_type == user_type:
                return view_func(request, *args, **kwargs)
            messages.error(request, f'You must be a {user_type} to access this page.')
            return redirect('login')
        return _wrapped_view
    return decorator

# Authentication views
def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name}!')
                
                # Redirect based on user type
                if user.user_type == 'employee':
                    return redirect('employee_dashboard')
                elif user.user_type == 'manager':
                    return redirect('manager_dashboard')
                elif user.user_type == 'security':
                    return redirect('security_dashboard')
                else:
                    return redirect('admin_dashboard')
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid form submission.')
    else:
        form = CustomAuthenticationForm()
    
    return render(request, 'leave_app/login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'Account created for {user.username}!')
            return redirect('login')
    else:
        form = UserRegistrationForm()
    
    return render(request, 'leave_app/register.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out.')
    return redirect('login')

# Employee views
@login_required
@user_type_required('employee')
def employee_dashboard(request):
    leave_requests = LeaveRequest.objects.filter(employee=request.user).order_by('-created_at')
    
    context = {
        'leave_requests': leave_requests,
        'pending_count': leave_requests.filter(status='pending').count(),
        'approved_count': leave_requests.filter(status='approved').count(),
        'rejected_count': leave_requests.filter(status='rejected').count(),
    }
    
    return render(request, 'leave_app/employee/dashboard.html', context)

@login_required
@user_type_required('employee')
def create_leave_request(request):
    if request.method == 'POST':
        form = LeaveRequestForm(request.POST)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.employee = request.user
            leave_request.save()
            messages.success(request, 'Leave request submitted successfully!')
            return redirect('employee_dashboard')
    else:
        form = LeaveRequestForm()
    
    return render(request, 'leave_app/employee/create_leave_request.html', {'form': form})

@login_required
@user_type_required('employee')
def view_leave_request(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk, employee=request.user)
    return render(request, 'leave_app/employee/view_leave_request.html', {'leave_request': leave_request})

# Manager views
@login_required
@user_type_required('manager')
def manager_dashboard(request):
    pending_requests = LeaveRequest.objects.filter(status='pending').order_by('-created_at')
    recent_reviewed = LeaveRequest.objects.filter(
        Q(status='approved') | Q(status='rejected')
    ).order_by('-review_date')[:10]
    
    context = {
        'pending_requests': pending_requests,
        'recent_reviewed': recent_reviewed,
        'pending_count': pending_requests.count(),
    }
    
    return render(request, 'leave_app/manager/dashboard.html', context)

@login_required
@user_type_required('manager')
def review_leave_request(request, pk):
    leave_request = get_object_or_404(LeaveRequest, pk=pk)
    
    if request.method == 'POST':
        form = LeaveReviewForm(request.POST, instance=leave_request)
        if form.is_valid():
            leave_request = form.save(commit=False)
            leave_request.reviewed_by = request.user
            leave_request.review_date = timezone.now()
            leave_request.save()
            
            status = 'approved' if leave_request.status == 'approved' else 'rejected'
            messages.success(request, f'Leave request {status} successfully!')
            return redirect('manager_dashboard')
    else:
        form = LeaveReviewForm(instance=leave_request)
    
    return render(request, 'leave_app/manager/review_leave_request.html', {
        'form': form,
        'leave_request': leave_request
    })

# Security views
@login_required
@user_type_required('security')
def security_dashboard(request):
    approved_requests = LeaveRequest.objects.filter(status='approved').order_by('-review_date')
    recent_logs = SecurityLog.objects.all().order_by('-timestamp')[:10]
    
    context = {
        'approved_requests': approved_requests,
        'recent_logs': recent_logs,
    }
    
    return render(request, 'leave_app/security/dashboard.html', context)

@login_required
@user_type_required('security')
def log_employee_action(request, leave_request_id):
    leave_request = get_object_or_404(LeaveRequest, pk=leave_request_id, status='approved')
    
    if request.method == 'POST':
        form = SecurityLogForm(request.POST)
        if form.is_valid():
            log = form.save(commit=False)
            log.employee = leave_request.employee
            log.leave_request = leave_request
            log.security_officer = request.user
            log.save()
            
            messages.success(request, f'Employee action logged successfully!')
            return redirect('security_dashboard')
    else:
        form = SecurityLogForm()
    
    return render(request, 'leave_app/security/log_action.html', {
        'form': form,
        'leave_request': leave_request
    })

# Admin views (optional)
@login_required
@user_type_required('admin')
def admin_dashboard(request):
    users = User.objects.all().order_by('-date_joined')
    leave_requests = LeaveRequest.objects.all().order_by('-created_at')[:10]
    security_logs = SecurityLog.objects.all().order_by('-timestamp')[:10]
    
    context = {
        'users': users,
        'leave_requests': leave_requests,
        'security_logs': security_logs,
        'employee_count': User.objects.filter(user_type='employee').count(),
        'manager_count': User.objects.filter(user_type='manager').count(),
        'security_count': User.objects.filter(user_type='security').count(),
    }
    
    return render(request, 'leave_app/admin/dashboard.html', context)

# Profile view
@login_required
def profile_view(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('profile')
    else:
        form = UserProfileForm(instance=request.user)
    
    return render(request, 'leave_app/profile.html', {'form': form})