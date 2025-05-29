from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('security', 'Security'),
        ('admin', 'Admin'),
    )
    user_type = models.CharField(max_length=20, choices=USER_TYPE_CHOICES, default='employee')
    employee_id = models.CharField(max_length=20, unique=True, null=True, blank=True)
    department = models.CharField(max_length=100, null=True, blank=True)
    profile_picture = models.ImageField(upload_to='profile_pics', null=True, blank=True)

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

class LeaveRequest(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )
    LEAVE_TYPE_CHOICES = (
        ('sick', 'Sick Leave'),
        ('vacation', 'Vacation'),
        ('personal', 'Personal'),
        ('other', 'Other'),
    )
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPE_CHOICES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    reviewed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='reviewed_requests')
    review_date = models.DateTimeField(null=True, blank=True)
    review_comment = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee.username}'s {self.get_leave_type_display()} ({self.get_status_display()})"
    
    @property
    def duration(self):
        """Calculate the duration of leave in days"""
        return (self.end_date - self.start_date).days + 1

class SecurityLog(models.Model):
    ACTION_CHOICES = (
        ('entry', 'Entry'),
        ('exit', 'Exit'),
        ('denied', 'Access Denied'),
    )
    
    employee = models.ForeignKey(User, on_delete=models.CASCADE, related_name='security_logs')
    leave_request = models.ForeignKey(LeaveRequest, on_delete=models.CASCADE, related_name='security_logs', null=True, blank=True)
    action = models.CharField(max_length=20, choices=ACTION_CHOICES)
    timestamp = models.DateTimeField(auto_now_add=True)
    security_officer = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='handled_logs')
    notes = models.TextField(null=True, blank=True)
    
    def __str__(self):
        return f"{self.employee.username} - {self.get_action_display()} at {self.timestamp}"