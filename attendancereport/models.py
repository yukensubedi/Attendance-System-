from django.db import models
from user.models import AuditableModel
from django.contrib.auth import get_user_model


User = get_user_model()


class Attendance(AuditableModel):
    student = models.ForeignKey(User, on_delete=models.CASCADE, limit_choices_to={'is_verified': True})
    status = models.BooleanField(default=False)  # True for present, False for absent

    def __str__(self):
        return f"{self.student.first_name} {self.student.last_name} - {self.created_at}"
