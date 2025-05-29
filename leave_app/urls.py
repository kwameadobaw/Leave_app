from django.urls import path
from . import views

urlpatterns = [
    # Authentication URLs
    path('', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('logout/', views.logout_view, name='logout'),
    
    # Employee URLs
    path('employee/dashboard/', views.employee_dashboard, name='employee_dashboard'),
    path('employee/leave/create/', views.create_leave_request, name='create_leave_request'),
    path('employee/leave/<int:pk>/', views.view_leave_request, name='view_leave_request'),
    
    # Manager URLs
    path('manager/dashboard/', views.manager_dashboard, name='manager_dashboard'),
    path('manager/leave/<int:pk>/review/', views.review_leave_request, name='review_leave_request'),
    
    # Security URLs
    path('security/dashboard/', views.security_dashboard, name='security_dashboard'),
    path('security/log/<int:leave_request_id>/', views.log_employee_action, name='log_employee_action'),
    
    # Admin URLs
    path('admin/dashboard/', views.admin_dashboard, name='admin_dashboard'),
    
    # Profile URL
    path('profile/', views.profile_view, name='profile'),
]