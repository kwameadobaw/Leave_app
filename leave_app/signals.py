from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import LeaveRequest

@receiver(post_save, sender=LeaveRequest)
def notify_leave_request_status_change(sender, instance, created, **kwargs):
    """Send email notifications when leave request status changes"""
    # Skip if this is a new leave request being created
    if created:
        # Notify managers about new leave request
        # This is commented out as email configuration is not set up
        # subject = f'New Leave Request: {instance.employee.get_full_name()}'
        # message = f'{instance.employee.get_full_name()} has submitted a new leave request.\n\nLeave Type: {instance.get_leave_type_display()}\nDuration: {instance.start_date} to {instance.end_date}\nReason: {instance.reason}'
        # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [manager.email for manager in User.objects.filter(user_type='manager')])
        pass
    else:
        # This is an update to an existing leave request
        if instance.status in ['approved', 'rejected'] and instance.review_date:
            # Notify employee about the status change
            # This is commented out as email configuration is not set up
            # subject = f'Leave Request {instance.get_status_display()}'
            # message = f'Your leave request has been {instance.get_status_display()}.\n\nLeave Type: {instance.get_leave_type_display()}\nDuration: {instance.start_date} to {instance.end_date}\nReviewed by: {instance.reviewed_by.get_full_name()}\nComments: {instance.review_comment or "No comments provided."}'
            # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [instance.employee.email])
            
            # If approved, notify security
            if instance.status == 'approved':
                # This is commented out as email configuration is not set up
                # subject = f'Approved Leave: {instance.employee.get_full_name()}'
                # message = f'{instance.employee.get_full_name()} has been approved for leave.\n\nEmployee ID: {instance.employee.employee_id}\nLeave Type: {instance.get_leave_type_display()}\nDuration: {instance.start_date} to {instance.end_date}'
                # send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [security.email for security in User.objects.filter(user_type='security')])
                pass