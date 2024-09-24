from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, RegisterView, LoginView, AttendanceReportAPI, MarkAttendanceAPI

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')

urlpatterns = [
    path('signup/', RegisterView.as_view(), name='signup-api'),
    path('login/', LoginView.as_view(), name='login-api'),
    path('attendance/report/', AttendanceReportAPI.as_view(), name='attendance_report_api'),
    path('attendance/', MarkAttendanceAPI.as_view(), name='mark_attendance_api'),
    path('', include(router.urls)),  # Include user update routes
]
