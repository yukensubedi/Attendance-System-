from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm, AuthenticationForm
from django.contrib.auth import authenticate
from .models import User
from django.core.exceptions import ValidationError
from datetime import date

class UserCreationForm(UserCreationForm):
    """
    A form for creating new  users.
    Includes all the required fields, plus repeated password.
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'address']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder':'Email'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'First Name'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Last Name'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder':'Date of Birth'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'Phone Number'}),
            'address': forms.Textarea(attrs={'class': 'form-control', 'placeholder':'Address'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Password'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control', 'placeholder':'Confirm Password'}),
        }

    def clean_date_of_birth(self):
            dob = self.cleaned_data.get('date_of_birth')
            if dob:
                # Check if the date is in the future
                if dob > date.today():
                    raise ValidationError("Date of birth cannot be in the future.")
            return dob


   


class UserUpdateForm(UserChangeForm):
    """
    A form for updating  user information.
    Includes all the fields on the user.
    """
    class Meta:
        model = User
        fields = ['email', 'first_name', 'last_name', 'date_of_birth', 'phone_number', 'address']
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'date_of_birth': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'phone_number': forms.TextInput(attrs={'class': 'form-control'}),
            'address': forms.Textarea(attrs={'class': 'form-control'}),
        }