from django.apps import AppConfig

class LeaveAppConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'leave_app'
    
    def ready(self):
        import leave_app.signals  # Import signals