from django.apps import AppConfig


class AttendancereportConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'attendancereport'

    def ready(self):
        import attendancereport.signals