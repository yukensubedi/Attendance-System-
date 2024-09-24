from rest_framework import generics, viewsets, status
from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authentication import TokenAuthentication
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from .serializers import UserRegistrationSerializer, UpdateUserSerializer, AttendanceSerializer
from attendancereport.models import Attendance
from rest_framework.decorators import action
from django.utils import timezone
from datetime import timedelta
from drf_spectacular.utils import extend_schema, OpenApiParameter
from .pagination import CustomPagination 


from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterView(generics.CreateAPIView):
    """
    API for user registration.

    This endpoint allows any user to register. No authentication is required.
    """
    queryset = User.objects.all()
    serializer_class = UserRegistrationSerializer
    permission_classes = [AllowAny]


class UserViewSet(viewsets.ModelViewSet):
    """
    API for updating user details.

    This endpoint allows authenticated users to update their own profile. 
    Admins can update any user's profile.
    """
    queryset = User.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Restrict queryset to the logged-in user's details.
        """
        return User.objects.filter(id=self.request.user.id)


class LoginView(ObtainAuthToken):
    """
    API for user login and token generation.

    This endpoint returns an authentication token when valid credentials are provided.
    """
    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'user_id': user.id})


class MarkAttendanceAPI(APIView):
    """
    API for marking attendance.

    This endpoint allows authenticated and verified users to mark attendance for the current day.
    If attendance has already been marked for today, an error is returned.
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user

        
        if not user.is_verified:
            return Response({"error": "You must be a verified user"}, status=status.HTTP_403_FORBIDDEN)

         
        if Attendance.objects.filter(student=user, created_at__date=timezone.now().date()).exists():
            return Response({"error": "Attendance has already been marked for today"}, status=status.HTTP_400_BAD_REQUEST)

        
        attendance_record = Attendance.objects.create(student=user, status=True)
        attendance_data = AttendanceSerializer(attendance_record).data

        return Response({
            "message": "Your attendance has been marked for the day",
            "attendance": attendance_data
        }, status=status.HTTP_201_CREATED)


class AttendanceReportAPI(APIView):
    """
    API for fetching attendance reports.

    This endpoint allows authenticated users to fetch either a weekly or monthly attendance report.
    The type of report is determined by the 'type' query parameter ('weekly' or 'monthly').
    """
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

    @extend_schema(
        parameters=[
            OpenApiParameter(
                'type', 
                type=str, 
                description='Type of report to fetch (either "weekly" or "monthly")',
                required=True,
                enum=['weekly', 'monthly']   
            ),
        ],
        responses={
            200: 'Successful response',
            400: 'Invalid parameter'
        },
    )
    def get(self, request, *args, **kwargs):
        user = request.user
        today = timezone.now().date()

        
        report_type = request.query_params.get('type')

        
        if report_type not in ['weekly', 'monthly']:
            return Response({"error": "The 'type' parameter is required and must be 'weekly' or 'monthly'."}, status=400)

        if report_type == 'weekly':
            # Fetch weekly attendance data (last 7 days)
            last_week = today - timedelta(days=6)
            attendance = Attendance.objects.filter(
                student=user,
                created_at__date__range=[last_week, today]
            ).order_by('created_at')

        elif report_type == 'monthly':
            # Fetch monthly attendance data (last 30 days)
            last_month = today - timedelta(days=30)
            attendance = Attendance.objects.filter(
                student=user,
                created_at__date__gte=last_month
            ).order_by('created_at')

         # Apply pagination
        paginator = CustomPagination()
        paginated_attendance = paginator.paginate_queryset(attendance, request)
        attendance_data = AttendanceSerializer(paginated_attendance, many=True).data

        # Return paginated response
        return paginator.get_paginated_response(attendance_data)