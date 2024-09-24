from django.utils import timezone
from django.conf import settings
from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from .models import Attendance
from datetime import datetime

@receiver(user_logged_in)
def check_attendance_on_login(sender, user, request, **kwargs):
    if user.is_verified:
        # Get the current date and time
        now = timezone.now()
        today = now.date()
        
        cutoff_time = datetime.strptime(settings.ATTENDANCE_CUTOFF_TIME, '%H:%M').time()

        # Check if the current time is after the cutoff time
        if now.time() >= cutoff_time:
            # Check if attendance for today already exists
            attendance_record = Attendance.objects.filter(student=user, created_at__date=today).exists()
            

            if not attendance_record:
                # Mark the student absent if no record exists
                Attendance.objects.create(student=user, status=False)   