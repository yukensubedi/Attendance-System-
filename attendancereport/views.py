from django.views.generic import TemplateView, View
from django.shortcuts import redirect
from django.contrib import messages
from django.utils import timezone
from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Attendance
import json
from django.core.serializers.json import DjangoJSONEncoder
from datetime import timedelta



class MarkAttendanceView(LoginRequiredMixin, View):
    """
    View to handle attendance marking. Only verified users can mark their attendance once per day.
    """

    def post(self, request, *args, **kwargs):
        """
        Handle POST requests to mark attendance. Includes validation for verified users
        and checking if attendance has already been marked for today.
        """
        user = request.user
        
        if not user.is_verified:
            messages.error(request, "You must be a verified user to mark attendance.")
            return redirect('home')

        try:
            if Attendance.objects.filter(student=user, created_at__date=timezone.now().date()).exists():
                messages.error(request, "Attendance has already been marked for today.")
                return redirect('attendance_report')

            Attendance.objects.create(student=user, status=True)
            messages.success(request, "Your attendance has been marked for the day.")
        except Exception as e:
            
            messages.error(request, "An error occurred while marking attendance.")
            return redirect('home')

        return redirect('attendance_report')


class AttendanceReportView(LoginRequiredMixin, TemplateView):
    """
    View to display a report of the user's attendance for the past week and month.
    """
    template_name = 'attendance.html'

    def get_context_data(self, **kwargs):
        """
        Add weekly and monthly attendance data to the context in JSON format for rendering charts or tables.
        """
        context = super().get_context_data(**kwargs)
        user = self.request.user
        today = timezone.now().date()

        try:
            last_week = today - timedelta(days=6)
            weekly_attendance = Attendance.objects.filter(
                student=user,
                created_at__date__range=[last_week, today]
            ).order_by('created_at')

            last_month = today - timedelta(days=30)
            monthly_attendance = Attendance.objects.filter(
                student=user,
                created_at__date__gte=last_month
            ).order_by('created_at')

            weekly_data = [
                {'date': attendance.created_at.date(), 'status': attendance.status}
                for attendance in weekly_attendance
            ]
            monthly_data = [
                {'date': attendance.created_at.date(), 'status': attendance.status}
                for attendance in monthly_attendance
            ]

            context['weekly_data'] = json.dumps(weekly_data, cls=DjangoJSONEncoder)
            context['monthly_data'] = json.dumps(monthly_data, cls=DjangoJSONEncoder)

            attendance_exists = Attendance.objects.filter(
                student=user, 
                created_at__date=today
            ).exists()

            context['status'] = attendance_exists

        except ObjectDoesNotExist:
            context['weekly_data'] = json.dumps([])
            context['monthly_data'] = json.dumps([])
            context['status'] = False
            messages.error(self.request, "No attendance data found.")

        except Exception as e:
            messages.error(self.request, "An error occurred while fetching the attendance report.")

        return context
