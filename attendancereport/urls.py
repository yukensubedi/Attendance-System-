from django.urls import path
from .views import MarkAttendanceView, AttendanceReportView

urlpatterns = [
    path('attendance/', MarkAttendanceView.as_view(), name='mark_attendance'),
    path('attendance/report/', AttendanceReportView.as_view(), name='attendance_report'),
    path('', AttendanceReportView.as_view(), name='attendance_report'),
]

