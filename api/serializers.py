from rest_framework import serializers
from django.contrib.auth import get_user_model
from attendancereport.models import Attendance

User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'address', 'password']

    def create(self, validated_data):
        user = User(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            last_name=validated_data['last_name'],
            date_of_birth=validated_data.get('date_of_birth'),
            phone_number=validated_data.get('phone_number'),
            address=validated_data.get('address'),
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class UpdateUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'date_of_birth', 'phone_number', 'address']
        read_only_fields = ['email']  


class AttendanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Attendance
        fields = ['id', 'student', 'status', 'created_at', 'updated_at']  

    def create(self, validated_data):
        # Automatically assign the logged-in user as the student
        validated_data['student'] = self.context['request'].user
        return super().create(validated_data)