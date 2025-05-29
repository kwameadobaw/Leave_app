from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, LeaveRequest, SecurityLog

class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'employee_id', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'employee_id', 'department', 'profile_picture')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('Additional Info', {'fields': ('user_type', 'employee_id', 'department', 'profile_picture')}),
    )
    search_fields = ('username', 'email', 'first_name', 'last_name', 'employee_id')
    ordering = ('username',)

class LeaveRequestAdmin(admin.ModelAdmin):
    list_display = ('employee', 'leave_type', 'start_date', 'end_date', 'status', 'created_at')
    list_filter = ('status', 'leave_type')
    search_fields = ('employee__username', 'employee__employee_id', 'reason')
    date_hierarchy = 'created_at'
    readonly_fields = ('created_at', 'updated_at')

class SecurityLogAdmin(admin.ModelAdmin):
    list_display = ('employee', 'action', 'timestamp', 'security_officer')
    list_filter = ('action', 'timestamp')
    search_fields = ('employee__username', 'employee__employee_id', 'notes')
    date_hierarchy = 'timestamp'
    readonly_fields = ('timestamp',)

admin.site.register(User, CustomUserAdmin)
admin.site.register(LeaveRequest, LeaveRequestAdmin)
admin.site.register(SecurityLog, SecurityLogAdmin)